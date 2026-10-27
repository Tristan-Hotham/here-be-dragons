"""Step 2. Measure every point in ../work/points.csv.

Adds, for each point (all distances in km, straight line on the British National Grid):
  church_km      nearest church building in Wikidata (Great Britain, any date), as parsed in Whose Church Is It?
  gm_km          nearest church whose dedication is St George or St Michael (same source)
  george_km      nearest church dedicated to St George
  barrow_km      nearest barrow, cairn or burial mound (OpenStreetMap and Wikidata, as compiled in Is the Barrow
                 a European Thing?), Great Britain only
  hillfort_km    nearest hillfort in the Atlas of Hillforts of Britain and Ireland (England, Scotland, Wales)
  river_km       nearest named river in OS Open Rivers (watercourses named "River ..." or "Afon ...", and tidal rivers)
  water_km       nearest named watercourse of any kind in OS Open Rivers (river, beck, burn, brook ...)
Writes ../work/measured.csv and small layers for the page (../work/layers.json).
Run: python3 code/02_measure.py
"""
import json, os, sqlite3, time
import numpy as np, pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree
from shapely import wkb
import shapely
from shapely.geometry import shape

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
HIST = os.environ.get("HIST", os.path.dirname(ROOT))
WORK = os.path.join(ROOT, "work")
TR = Transformer.from_crs(4326, 27700, always_xy=True)
t0 = time.time()
P = pd.read_csv(os.path.join(WORK, "points.csv"), keep_default_na=False, na_values=[""])
XY = np.c_[P.x.values, P.y.values]
cty = json.load(open(os.path.join(HIST, "how-roman-is-your-road", "data", "counties.geojson")))
land = shapely.union_all([shape(f["geometry"]) for f in cty["features"]])
shapely.prepare(land)
layers = {}


def nearest(lon, lat, key):
    x, y = TR.transform(np.asarray(lon, float), np.asarray(lat, float))
    d, i = cKDTree(np.c_[x, y]).query(XY)
    return d / 1000, i


# ---------- churches ----------
C = pd.read_csv(os.path.join(HIST, "saints-and-wells", "data", "churches.csv.gz"))
C = C[C.country == "GB"].dropna(subset=["lon", "lat"])
C = C[shapely.contains_xy(land, C.lon.values, C.lat.values)].reset_index(drop=True)
P["church_km"], i = nearest(C.lon, C.lat, "church"); P["church"] = C.label.values[i]
G = C[C.all_dedications.fillna("").str.contains(r"\bGeorge\b|\bMichael\b")].reset_index(drop=True)
P["gm_km"], i = nearest(G.lon, G.lat, "gm"); P["gm"] = G.label.values[i]
GG = C[C.all_dedications.fillna("").str.contains(r"\bGeorge\b")].reset_index(drop=True)
P["george_km"], i = nearest(GG.lon, GG.lat, "george")
layers["gm"] = [[round(a, 4), round(b, 4), l, ("George" if "George" in str(d) else "Michael")] for a, b, l, d in zip(G.lat, G.lon, G.label, G.all_dedications)]
counts = dict(n_churches=int(len(C)), n_gm=int(len(G)), n_george=int(len(GG)),
              n_michael=int(C.all_dedications.fillna("").str.contains(r"\bMichael\b").sum()))
print("churches", counts, round(time.time() - t0))

# ---------- barrows ----------
B = pd.read_csv(os.path.join(HIST, "barrows-of-europe", "data", "barrows.csv"), usecols=["src", "name", "lon", "lat", "country", "kind"])
B = B[B.country == "United Kingdom"]
B = B[shapely.contains_xy(land, B.lon.values, B.lat.values)].reset_index(drop=True)
P["barrow_km"], i = nearest(B.lon, B.lat, "barrow"); P["barrow"] = B.name.fillna("").values[i]
counts["n_barrows"] = int(len(B)); counts["barrows_by_kind"] = B.kind.value_counts().to_dict()
layers["barrows"] = np.round(np.c_[B.lat.values, B.lon.values], 3).tolist()
print("barrows", len(B), round(time.time() - t0))

# ---------- hillforts ----------
H = pd.read_csv(os.path.join(HIST, "within-sight", "data", "forts_visibility.csv"), usecols=["atlas_id", "name", "country", "lat", "lon"])
H = H[H.country.isin(["England", "Scotland", "Wales"])].reset_index(drop=True)
P["hillfort_km"], i = nearest(H.lon, H.lat, "hillfort"); P["hillfort"] = H.name.values[i]
counts["n_hillforts"] = int(len(H))
layers["hillforts"] = [[round(a, 4), round(b, 4), n] for a, b, n in zip(H.lat, H.lon, H.name)]
print("hillforts", len(H), round(time.time() - t0))


# ---------- rivers ----------
def densify(lines, step=50.0):
    out = []
    for c in lines:
        a, b = c[:-1], c[1:]
        L = np.hypot(*(b - a).T)
        n = np.maximum(1, np.ceil(L / step).astype(int))
        for (ax, ay), (bx, by), k in zip(a, b, n):
            t = np.arange(k) / k
            out.append(np.c_[ax + (bx - ax) * t, ay + (by - ay) * t])
        out.append(c[-1:])
    return np.concatenate(out)


con = sqlite3.connect(os.path.join(HIST, "osrivers", "Data", "oprvrs_gb.gpkg"))
riv, wat, rlay = [], [], []
for blob, form, name in con.execute("select geometry, form, watercourse_name from watercourse_link where watercourse_name is not null and form in ('inlandRiver','tidalRiver')"):
    env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    c = np.asarray(wkb.loads(bytes(blob[8 + env:])).coords)[:, :2]
    wat.append(c)
    if form == "tidalRiver" or name.startswith("River ") or name.startswith("Afon "):
        riv.append(c)
con.close()
P["river_km"] = cKDTree(densify(riv)).query(XY)[0] / 1000
P["water_km"] = cKDTree(densify(wat, 100.0)).query(XY)[0] / 1000
counts["n_river_links"] = len(riv); counts["n_water_links"] = len(wat)
counts["river_length_km"] = float(sum(np.hypot(*np.diff(c, axis=0).T).sum() for c in riv) / 1000)
print("rivers", len(riv), len(wat), round(time.time() - t0))
P.to_csv(os.path.join(WORK, "measured.csv"), index=False)
json.dump(dict(layers=layers, counts=counts), open(os.path.join(WORK, "layers.json"), "w"), separators=(",", ":"))
print("done", round(time.time() - t0))
