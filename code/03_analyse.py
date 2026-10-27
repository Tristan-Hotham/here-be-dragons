"""Step 3. Compare the legends and the dragon names with their controls and write the results.

For each group and each measure, the observed statistic (a median or a share) is compared with 2,000 replicate
control sets. Each replicate takes one control at random for every legend or name:
  match   an ordinary OS name of the same local type (village with village, hill with hill) from the same 50 km square
  rand    a random land point in the same 50 km square
Chance values are two-sided: twice the share of replicates on the far side of the observed value.

Writes ../data/results.json, ../data/dragon_names.csv, ../data/legends_measured.csv, ../data/test_results.csv,
../data/controls.csv.gz and ../work/site.json.
Run: python3 code/03_analyse.py
"""
import json, os, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np, pandas as pd
from terms import LABEL, CLASSES

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
WORK = os.path.join(ROOT, "work"); DATA = os.path.join(ROOT, "data")
NREP = 2000
rng = np.random.default_rng(1405)
P = pd.read_csv(os.path.join(WORK, "measured.csv"), keep_default_na=False, na_values=[""])
LAY = json.load(open(os.path.join(WORK, "layers.json")))
CNT = json.load(open(os.path.join(WORK, "counts.json")))
NORTH = {"North East", "North West", "Yorkshire and the Humber", "Scotland"}
P["north"] = P.region.isin(NORTH)

# each legend or name is preceded by its 50 matched and 50 random controls (see 01_points.py)
isobs = P.set.isin(["legend", "name"]).values
blk = np.r_[0, np.cumsum(isobs)[:-1]]
P["blk"] = blk
obs = P[isobs].copy().reset_index(drop=True)
assert (P[~isobs].groupby("blk").size() == 100).all() and len(obs) == P.blk.nunique()
K = 50

MEAS = {
    "church_1":    ("church_km", "lt", 1.0, "Share within 1 km of a church"),
    "church_med":  ("church_km", "median", None, "Median distance to a church (km)"),
    "barrow_2":    ("barrow_km", "lt", 2.0, "Share within 2 km of a barrow or burial cairn"),
    "barrow_med":  ("barrow_km", "median", None, "Median distance to a barrow (km)"),
    "hillfort_2":  ("hillfort_km", "lt", 2.0, "Share within 2 km of a hillfort"),
    "hillfort_med": ("hillfort_km", "median", None, "Median distance to a hillfort (km)"),
    "river_05":    ("river_km", "lt", 0.5, "Share within 500 m of a named river"),
    "river_med":   ("river_km", "median", None, "Median distance to a named river (km)"),
    "water_025":   ("water_km", "lt", 0.25, "Share within 250 m of any named watercourse"),
    "gm_5":        ("gm_km", "lt", 5.0, "Share within 5 km of a St George or St Michael church"),
    "gm_med":      ("gm_km", "median", None, "Median distance to a St George or St Michael church (km)"),
    "george_5":    ("george_km", "lt", 5.0, "Share within 5 km of a St George church"),
    "any4":        ("any4", "mean", None, "Share next to at least one: church 1 km, barrow 2 km, hillfort 2 km or river 500 m"),
}
P["any4"] = ((P.church_km < 1) | (P.barrow_km < 2) | (P.hillfort_km < 2) | (P.river_km < 0.5)).astype(float)
obs["any4"] = P.loc[isobs, "any4"].values
cols = sorted(set(m[0] for m in MEAS.values()))
CM = {}
for s in ("match", "rand"):
    q = P[P.set == s].sort_values(["blk", "pid"])
    CM[s] = {c: q[c].values.reshape(len(obs), K) for c in cols}


def stat(v, kind, thr):
    ok = ~np.isnan(v)
    if kind == "median": return np.nanmedian(v, -1)
    if kind == "mean": return np.nanmean(v, -1)
    if kind == "lt": return np.where(ok, v < thr, False).sum(-1) / ok.sum(-1)


def test(mask, mk, cs):
    col, kind, thr, _ = MEAS[mk]
    o = obs[col].values[mask]
    ov = float(stat(o[None], kind, thr)[0])
    C = CM[cs][col][mask]
    pick = rng.integers(0, K, size=(NREP, C.shape[0]))
    b = stat(np.take_along_axis(np.broadcast_to(C, (NREP,) + C.shape), pick[..., None], 2)[..., 0], kind, thr)
    allc = float(stat(C.ravel()[None], kind, thr)[0])
    p = min(1.0, 2 * min((b >= ov).mean(), (b <= ov).mean()))
    return dict(obs=ov, base=allc, base_lo=float(np.percentile(b, 2.5)), base_hi=float(np.percentile(b, 97.5)), p=float(p),
                n=int(mask.sum()), ratio=(ov / allc if allc else None))


isleg = (obs.set == "legend").values
core = obs.cls.isin(["dragon", "drake_mound", "worm_word", "serpent"]).values
GROUPS = {
    "legends": isleg,
    "legends_feature": isleg & (obs.type != "populatedPlace").values,
    "legends_settlement": isleg & (obs.type == "populatedPlace").values,
    "legends_church_story": isleg & obs.church_story.astype(str).eq("True").values,
    "legends_no_church_story": isleg & ~obs.church_story.astype(str).eq("True").values,
    "names": ~isleg,
    "names_core": ~isleg & core,
    "names_other": ~isleg & ~core,
    "names_north": ~isleg & obs.north.values,
    "names_south": ~isleg & ~obs.north.values,
}
for c in CLASSES:
    GROUPS[c] = (~isleg) & (obs.cls == c).values
GROUPS["drake_all"] = (~isleg) & obs.cls.str.startswith("drake").values
GROUPS["worm_all"] = (~isleg) & obs.cls.str.startswith("worm").values

R = {"n_rep": NREP, "k_controls": K, "groups": {}}
rows = []
for g, mask in GROUPS.items():
    R["groups"][g] = {"n": int(mask.sum())}
    if mask.sum() == 0: continue
    for mk in MEAS:
        R["groups"][g][mk] = {}
        for cs in ("match", "rand"):
            r = test(mask, mk, cs)
            R["groups"][g][mk][cs] = r
            rows.append(dict(group=g, measure=mk, label=MEAS[mk][3], control=cs, **r))
    print(g, "done", int(mask.sum()))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "test_results.csv"), index=False, float_format="%.4f")
R["n_measures"] = len(MEAS)

# ---------- counts ----------
LG = pd.read_csv(os.path.join(DATA, "legends.csv"), keep_default_na=False, na_values=[""])
nm = obs[~isleg]
lg = obs[isleg]
R["n_os_features"] = CNT["n_os_features"]
R["n_excluded"] = CNT["n_excluded"]
R["n_legends_listed"] = int(len(LG))
R["n_legends"] = int(isleg.sum())
R["n_legends_unplaced"] = int(LG.lat.isna().sum())
R["legends_by_src"] = LG.src.value_counts().to_dict()
R["legends_by_word"] = lg.word.value_counts().to_dict()
R["legends_feature"] = int(GROUPS["legends_feature"].sum())
R["legends_settlement"] = int(GROUPS["legends_settlement"].sum())
R["legends_church_story"] = int(GROUPS["legends_church_story"].sum())
R["legends_george"] = int(lg.george.astype(str).eq("True").sum())
R["legends_by_country"] = lg.country.value_counts().to_dict()
R["legends_north"] = int(lg.north.sum())
R["legends_south"] = int((~lg.north).sum())
R["legends_worm_north"] = int((lg.north & lg.word.eq("worm")).sum())
R["legends_worm_south"] = int((~lg.north & lg.word.eq("worm")).sum())
R["legends_ne"] = int(lg.region.isin(["North East"]).sum() + ((lg.region == "Scotland") & (lg.lat < 56)).sum())
R["n_names"] = int(len(nm))
R["n_core"] = int(core.sum())
R["by_class"] = nm.cls.value_counts().to_dict()
R["by_class_country"] = {k: v for k, v in pd.crosstab(nm.cls, nm.country).to_dict(orient="index").items()}
R["by_type"] = nm.local_type.value_counts().head(8).to_dict()
R["names_supported"] = int(nm.supported.astype(str).eq("True").sum())
R["names_by_country"] = nm.country.value_counts().to_dict()
# rates per 10,000 OS features, by region
reg = CNT["os_by_region"]
R["rate_by_region"] = {r: {"n": int((nm.region == r).sum()), "worm": int(((nm.region == r) & nm.cls.str.startswith("worm")).sum()),
                           "drake": int(((nm.region == r) & nm.cls.str.startswith("drake")).sum()),
                           "dragon": int(((nm.region == r) & nm.cls.isin(["dragon", "serpent"])).sum()),
                           "legends": int((lg.region == r).sum()), "os": int(reg[r]),
                           "per10k": float((nm.region == r).sum() / reg[r] * 1e4)} for r in reg}
osn = sum(reg[r] for r in reg if r in NORTH); oss = sum(reg[r] for r in reg if r not in NORTH)
R["north"] = {"os": osn, "names": int(nm.north.sum()), "per10k": float(nm.north.sum() / osn * 1e4),
              "worm": int((nm.north & nm.cls.str.startswith("worm")).sum()), "worm_word": int((nm.north & nm.cls.eq("worm_word")).sum()),
              "drake": int((nm.north & nm.cls.str.startswith("drake")).sum()), "dragon": int((nm.north & nm.cls.eq("dragon")).sum())}
R["south"] = {"os": oss, "names": int((~nm.north).sum()), "per10k": float((~nm.north).sum() / oss * 1e4),
              "worm": int((~nm.north & nm.cls.str.startswith("worm")).sum()), "worm_word": int((~nm.north & nm.cls.eq("worm_word")).sum()),
              "drake": int((~nm.north & nm.cls.str.startswith("drake")).sum()), "dragon": int((~nm.north & nm.cls.eq("dragon")).sum())}
for k in ("north", "south"):
    R[k]["worm_word_per100k"] = R[k]["worm_word"] / R[k]["os"] * 1e5
    R[k]["worm_per100k"] = R[k]["worm"] / R[k]["os"] * 1e5
    R[k]["drake_per100k"] = R[k]["drake"] / R[k]["os"] * 1e5
R["layers"] = LAY["counts"]
R["gm_share_all_churches"] = LAY["counts"]["n_gm"] / LAY["counts"]["n_churches"]

# George or Michael among churches near legends: share of churches within 5 km that are George or Michael
from scipy.spatial import cKDTree
from pyproj import Transformer
TR = Transformer.from_crs(4326, 27700, always_xy=True)
C = pd.read_csv(os.path.join(os.environ.get("HIST", os.path.dirname(ROOT)), "saints-and-wells", "data", "churches.csv.gz"))
C = C[C.country == "GB"].dropna(subset=["lon", "lat"])
cx, cy = TR.transform(C.lon.values, C.lat.values)
isgm = C.all_dedications.fillna("").str.contains(r"\bGeorge\b|\bMichael\b").values
T = cKDTree(np.c_[cx, cy])


def gm_share(df):
    idx = T.query_ball_point(np.c_[df.x.values, df.y.values], 5000)
    allc = sorted(set(j for ii in idx for j in ii))
    return dict(n_churches=len(allc), n_gm=int(isgm[allc].sum()), share=float(isgm[allc].mean()) if allc else None)


R["gm_near_legends"] = gm_share(lg)
R["gm_near_legend_controls"] = gm_share(P[(P.set == "match") & (P.cls == "legend")])
R["gm_near_names"] = gm_share(nm)

# ---------- curves for charts ----------
def hist(col, edges, mask, cs="match"):
    ob = obs[col].values[mask]
    cb = CM[cs][col][mask].ravel()
    clip = lambda v: np.clip(v, edges[0], edges[-1] - 1e-9)
    return dict(edges=list(map(float, edges)), obs=(np.histogram(clip(ob), edges)[0] / len(ob)).round(4).tolist(),
                ctrl=(np.histogram(clip(cb), edges)[0] / len(cb)).round(4).tolist(), n_obs=int(len(ob)))


R["curves"] = {
    "leg_church": hist("church_km", np.arange(0, 4.5, 0.5), GROUPS["legends"]),
    "names_church": hist("church_km", np.arange(0, 4.5, 0.5), GROUPS["names"]),
    "names_barrow": hist("barrow_km", np.arange(0, 11, 1.0), GROUPS["names"]),
    "names_river": hist("river_km", np.arange(0, 8.5, 0.5), GROUPS["names"]),
}

# ---------- tables ----------
lgm = lg.merge(LG[["id", "legend", "src", "url", "phrase", "church_note"]], left_on="lid", right_on="id", how="left")
keep = ["id", "legend", "word", "name", "local_type", "county", "country", "region", "lat", "lon", "x", "y", "src", "url", "phrase",
        "church_story", "church_note", "george", "church", "church_km", "gm", "gm_km", "barrow_km", "hillfort", "hillfort_km", "river_km", "water_km"]
lgm[keep].rename(columns={"name": "os_name", "church": "nearest_church", "gm": "nearest_george_or_michael"}).round(4).to_csv(
    os.path.join(DATA, "legends_measured.csv"), index=False)
R["legend_rows"] = [{k: (None if pd.isna(v) else (round(v, 3) if isinstance(v, float) else (bool(v) if isinstance(v, (bool, np.bool_)) else v)))
                     for k, v in r.items()} for r in lgm[["id", "legend", "word", "name", "county", "church_km", "gm_km", "barrow_km", "hillfort_km", "river_km", "church_story", "george"]].to_dict(orient="records")]
for r in R["legend_rows"]:
    r["church_story"] = str(r["church_story"]) == "True"; r["george"] = str(r["george"]) == "True"
nmo = nm.copy()
nmo["os_feature_row"] = nmo.fid
ncols = ["os_feature_row", "name", "name2", "cls", "local_type", "lat", "lon", "x", "y", "country", "region", "county", "stratum",
         "supported", "reading", "reading_src", "church", "church_km", "gm", "gm_km", "george_km", "barrow", "barrow_km", "hillfort", "hillfort_km", "river_km", "water_km"]
nmo[ncols].round(4).to_csv(os.path.join(DATA, "dragon_names.csv"), index=False)
cc = P[P.set.isin(["match", "rand"])].copy()
cc["parent_kind"] = np.where(cc.cls == "legend", "legend", "name")
cc["parent_os_feature_row"] = obs.fid.values[cc.blk.values]
cc[["set", "parent_kind", "parent_os_feature_row", "name", "local_type", "lat", "lon", "church_km", "gm_km", "barrow_km", "hillfort_km", "river_km", "water_km"]].round(3).to_csv(
    os.path.join(DATA, "controls.csv.gz"), index=False, compression="gzip")
# supported names and Drake mound names in detail
R["supported_rows"] = [dict(name=r.name, county=r.county, cls=r.cls, reading=r.reading, src=r.reading_src, barrow_km=round(r.barrow_km, 2),
                            church_km=round(r.church_km, 2), barrow=r.barrow) for r in nm[nm.supported.astype(str).eq("True")].itertuples()]
R["drake_mound_rows"] = [dict(name=r.name, name2=r.name2, county=r.county, barrow_km=round(r.barrow_km, 2), barrow=r.barrow, church_km=round(r.church_km, 2))
                         for r in nm[nm.cls == "drake_mound"].sort_values("barrow_km").itertuples()]
R["drake_mound_barrow_1"] = int((nm[nm.cls == "drake_mound"].barrow_km < 1).sum())
# closest legend to a church, and the ones far from one
R["legends_far_from_church"] = [r["legend"] for r in R["legend_rows"] if r["church_km"] >= 1]
json.dump(R, open(os.path.join(DATA, "results.json"), "w"), indent=1, default=lambda v: None if v != v else v)

# ---------- compact data for the page ----------
site = dict(
    leg=[[round(r.lat, 5), round(r.lon, 5), r.legend, r.word, r.name, r.county, r.url, r.phrase, int(str(r.church_story) == "True"),
          r.church_note, int(str(r.george) == "True"), r.church, round(r.church_km, 2), round(r.barrow_km, 2), round(r.hillfort_km, 2), round(r.river_km, 2), r.src]
         for r in lgm.itertuples()],
    names=[[round(r.lat, 5), round(r.lon, 5), r.name + (f" ({r.name2})" if isinstance(r.name2, str) and r.name2 else ""), r.cls, r.local_type, r.county or r.country,
            int(str(r.supported) == "True"), r.reading, r.church, round(r.church_km, 2), round(r.barrow_km, 2), round(r.hillfort_km, 2), round(r.river_km, 2)]
           for r in nm.itertuples()],
    gm=LAY["layers"]["gm"], barrows=LAY["layers"]["barrows"], hillforts=LAY["layers"]["hillforts"],
)
json.dump(site, open(os.path.join(WORK, "site.json"), "w"), separators=(",", ":"))
print("results written")
