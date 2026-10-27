"""Step 4. Build ../index.html from page_template.html, and ../README.md from README_template.md.

Every number in the text is a placeholder like {{groups.legends.church_1.match.obs|pct0}}, filled from
../data/results.json. Map points and chart numbers are embedded in the page as `const D = ...`.
Formats: int (thousands commas), pct0, pct1, f1, f2, km1, km2, m (km shown in metres), p (chance value), words, Words, raw.
Run: python3 code/04_build_site.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
R = json.load(open(os.path.join(ROOT, "data", "results.json")))
site = json.load(open(os.path.join(ROOT, "work", "site.json")))
NORTH = {"North East", "North West", "Yorkshire and the Humber", "Scotland"}
site["G"] = {g: R["groups"][g] for g in ("legends", "names", "names_core", "names_north", "names_south", "drake_mound", "worm_word",
                                          "legends_church_story", "legends_no_church_story")}
site["BC"] = R["by_class_country"]
site["REG"] = {k: dict(v, north=k in NORTH) for k, v in R["rate_by_region"].items()}


def get(path):
    v = R
    for k in path.split("."):
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def fmt(v, f):
    if f == "int": return f"{int(round(v)):,}"
    if f == "pct0": return f"{v * 100:.0f}%"
    if f == "pct1": return f"{v * 100:.1f}%"
    if f == "f1": return f"{v:.1f}"
    if f == "f2": return f"{v:.2f}"
    if f == "km1": return f"{v:.1f} km"
    if f == "km2": return f"{v:.2f} km"
    if f == "m": return f"{v * 1000:,.0f} m"
    if f == "p": return "below 0.001" if v < 0.001 else f"{v:.3f}"
    if f == "words":
        w = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen".split()
        return w[int(v)] if int(v) < len(w) else f"{int(v):,}"
    if f == "Words": return fmt(v, "words").capitalize()
    return str(v)


def sub(m):
    path, _, f = m.group(1).partition("|")
    return fmt(get(path.strip()), f.strip() or "raw")


def fill(t):
    return re.sub(r"\{\{(.+?)\}\}", sub, t)


t = fill(open(os.path.join(HERE, "page_template.html")).read())
data = json.dumps(site, separators=(",", ":"), ensure_ascii=False).replace("–", "-").replace("—", "-").replace("</", "<\\/")
t = t.replace("/*DATA*/", "const D = " + data + ";")
open(os.path.join(ROOT, "index.html"), "w").write(t)
print("index.html", len(t.encode()) // 1024, "KB")
open(os.path.join(ROOT, "README.md"), "w").write(fill(open(os.path.join(HERE, "README_template.md")).read()))
print("README.md written")
