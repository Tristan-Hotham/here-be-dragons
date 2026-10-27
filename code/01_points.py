"""Step 1. Build the points to measure.

Writes ../work/points.csv, one row per point:
  set = legend  named legends from legends.py, placed at the OS Open Names feature the source names
        name    OS Open Names features whose name falls in a class of terms.py
        match   matched ordinary names: for each legend or name, K OS features of the same local type drawn at
                random from the same 50 km grid square (100 km, then country, as fallbacks when fewer than 20)
        rand    random land points: for each legend or name, K points on land in the same 50 km square
Also writes ../data/legends.csv (every legend with its source, phrase, the OS feature used and how it was placed).
Shared inputs are read in place from the folder above this repository (set HIST to change it).
Run: python3 code/01_points.py
"""
import json, os
import numpy as np, pandas as pd
from pyproj import Transformer
import shapely
from shapely.geometry import shape
from terms import classify, excluded, ANY, SUPPORTED
from legends import LEGENDS

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
HIST = os.environ.get("HIST", os.path.dirname(ROOT))
WORK = os.path.join(ROOT, "work"); os.makedirs(WORK, exist_ok=True)
DATA = os.path.join(ROOT, "data"); os.makedirs(DATA, exist_ok=True)
K = 50
rng = np.random.default_rng(20261027)
TI = Transformer.from_crs(27700, 4326, always_xy=True)

os_ = pd.read_csv(os.path.join(HIST, "osnames_gb.tsv"), sep="\t", dtype=str, keep_default_na=False)
for c in ("lat", "lon", "x", "y"):
    os_[c] = os_[c].astype(float)
os_["fid"] = np.arange(len(os_))
for s in (50000, 100000):
    os_[f"c{s//1000}"] = (os_.x // s).astype(int).astype(str) + "_" + (os_.y // s).astype(int).astype(str)
os_["cls"] = [classify(a) or (classify(b) if b else None) for a, b in zip(os_.name1, os_.name2)]
os_["excl"] = [excluded(a) or excluded(b) for a, b in zip(os_.name1, os_.name2)]
dragonish = os_.name1.str.contains(ANY) | os_.name2.str.contains(ANY)
pool = os_[~dragonish]
groups = {s: pool.groupby([f"c{s}", "local_type"]).indices for s in (50, 100)}
gc = pool.groupby(["country", "local_type"]).indices

# land outline for random points (ONS counties, as in How Roman Is Your Road)
cty = json.load(open(os.path.join(HIST, "how-roman-is-your-road", "data", "counties.geojson")))
land = shapely.union_all([shape(f["geometry"]) for f in cty["features"]])
shapely.prepare(land)

rows = []


def add(set_, r, cls, extra):
    rows.append(dict(set=set_, parent=r.fid if set_ in ("legend", "name") else extra.pop("parent"), fid=r.fid, cls=cls,
                     name=r.name1, name2=r.name2, local_type=r.local_type, type=r.type, lat=r.lat, lon=r.lon, x=r.x, y=r.y,
                     country=r.country, region=r.region, county=r.county or r.district, **extra))


def controls(r, cls, key):
    idx = None
    for s in (50, 100):
        ii = groups[s].get((getattr(r, f"c{s}"), r.local_type))
        if ii is not None and len(ii) >= 20:
            idx, st = ii, f"{s} km"; break
    if idx is None:
        idx, st = gc[(r.country, r.local_type)], "country"
    for j in rng.choice(idx, K, replace=len(idx) < K):
        q = pool.iloc[j]
        rows.append(dict(set="match", parent=key, fid=int(q.fid), cls=cls, name=q.name1, name2=q.name2, local_type=q.local_type,
                         type=q.type, lat=q.lat, lon=q.lon, x=q.x, y=q.y, country=q.country, region=q.region,
                         county=q.county or q.district, stratum=st))
    cx, cy = (r.x // 50000) * 50000, (r.y // 50000) * 50000
    got = []
    while len(got) < K:
        xs = cx + rng.random(200) * 50000; ys = cy + rng.random(200) * 50000
        lo, la = TI.transform(xs, ys)
        ok = shapely.contains_xy(land, lo, la)
        got += [(a, b, c, d) for a, b, c, d, o in zip(xs, ys, la, lo, ok) if o]
    for a, b, c, d in got[:K]:
        rows.append(dict(set="rand", parent=key, fid=-1, cls=cls, name="", name2="", local_type="", type="", lat=c, lon=d,
                         x=a, y=b, country=r.country, region=r.region, county="", stratum="50 km"))
    return st


# ---------- legends ----------
leg_rows = []
for L in LEGENDS:
    out = {k: L[k] for k in ("id", "legend", "word", "src", "url", "phrase", "church", "church_note", "george")}
    out["source"] = {"WPL": "Wikipedia: List of dragons in mythology and folklore (wikitext, 27 Oct 2026)",
                     "WPA": "Wikipedia article on the legend (read 27 Oct 2026)",
                     "ASH": "D. L. Ashliman, British Dragons, Folklore and Mythology Electronic Texts (read 27 Oct 2026)"}[L["src"]]
    if L["os"] is None:
        out.update(os_name="", os_local_type="", os_county="", lat=None, lon=None, placed="not placed: " + (L["church_note"] or "no place named"))
        leg_rows.append(out); continue
    nm, ct = L["os"]
    m = os_[((os_.name1 == nm) | (os_.name2 == nm)) & ((os_.county == ct) | (os_.district == ct))]
    assert len(m) == 1, (L["id"], len(m))
    r = next(m.itertuples())
    kind = "named feature" if r.type != "populatedPlace" else "settlement"
    out.update(os_name=r.name1, os_local_type=r.local_type, os_county=ct, lat=r.lat, lon=r.lon, region=r.region,
               placed=f"OS Open Names {r.local_type} '{r.name1}' ({ct}), the {kind} named in the source")
    leg_rows.append(out)
    st = controls(r, "legend", r.fid)
    add("legend", r, "legend", dict(stratum=st, lid=L["id"], word=L["word"], church_story=L["church"], george=L["george"]))
LG = pd.DataFrame(leg_rows)
LG.to_csv(os.path.join(DATA, "legends.csv"), index=False)
print("legends placed", LG.lat.notna().sum(), "of", len(LG))

# ---------- names ----------
names = os_[os_.cls.notna()]
for r in names.itertuples():
    sup = SUPPORTED.get((r.name1, r.county or r.district))
    st = controls(r, r.cls, r.fid)
    add("name", r, r.cls, dict(stratum=st, supported=bool(sup), reading=sup[0] if sup else "", reading_src=sup[1] if sup else ""))
print("names", len(names), names.cls.value_counts().to_dict())
ex = os_[os_.excl]
ex[["name1", "name2", "local_type", "county", "country", "lat", "lon"]].to_csv(os.path.join(WORK, "excluded_names.csv"), index=False)
print("excluded", len(ex))

P = pd.DataFrame(rows)
P.insert(0, "pid", np.arange(len(P)))
P.to_csv(os.path.join(WORK, "points.csv"), index=False)
print(P.groupby(["set"]).size().to_dict())
print("strata", P[P.set == "match"].groupby("stratum").size().to_dict())
json.dump({"n_os_features": int(len(os_)), "n_excluded": int(len(ex)),
           "excluded_by_word": {w: int(ex.name1.str.contains(w).sum() + ex.name2.str.contains(w).sum()) for w in ("Dragonfly", "Serpentine", "Serpentwalk", "Wormwood")},
           "os_by_region": os_.groupby("region").size().to_dict()},
          open(os.path.join(WORK, "counts.json"), "w"))
