"""r/dataisbeautiful collage for Here Be Dragons (2400 x 3000 px).
Every number comes from ../data/results.json and the data files. Run from this folder: python3 collage.py
Fonts: FONT_DIR with FrauncesVar.ttf, SourceSerif4-*.ttf and IBMPlexMono-*.ttf (github.com/google/fonts).
"""
import json, os
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
HIST = os.environ.get("HIST", os.path.dirname(ROOT))
F = os.environ.get("FONT_DIR", "/tmp/claude-0/-home-claude/c232619d-81e0-53f3-9de6-41e973630753/scratchpad/fonts") + "/"
for f in ["FrauncesVar.ttf", "IBMPlexMono-Regular.ttf", "IBMPlexMono-Medium.ttf", "SourceSerif4-Regular.ttf", "SourceSerif4-Semibold.ttf", "SourceSerif4-It.ttf"]:
    fm.fontManager.addfont(F + f)
DISP = fm.FontProperties(fname=F + "FrauncesVar.ttf", weight=900)
SER, MONO = "Source Serif 4", "IBM Plex Mono"
BG, FG, MUT, LAND = "#DDEBE1", "#13221A", "#4A6255", "#C3D8CA"
HOT, GOLD, VIO, BLUE, BAND = "#B8231B", "#A0700F", "#5A3E8E", "#2D5E8A", "#97B0A0"

R = json.load(open(os.path.join(ROOT, "data", "results.json")))
G = R["groups"]
L = pd.read_csv(os.path.join(ROOT, "data", "legends_measured.csv"))
N = pd.read_csv(os.path.join(ROOT, "data", "dragon_names.csv"), keep_default_na=False, na_values=[""])
base = pd.read_csv(os.path.join(HIST, "osnames_gb.tsv"), sep="\t", usecols=["x", "y"]).sample(150000, random_state=1)
pc = lambda v: f"{v * 100:.0f}%"

fig = plt.figure(figsize=(12, 15), dpi=200, facecolor=BG)
# illuminated frame: gold double rule
for inset, lw in ((0.012, 2.2), (0.018, 0.9)):
    fig.add_artist(Rectangle((inset, inset * 0.8), 1 - 2 * inset, 1 - 1.6 * inset, transform=fig.transFigure, fill=False, ec=GOLD, lw=lw))

# title with a scarlet initial
fig.text(0.045, 0.972, "D", fontproperties=DISP, fontsize=96, color=HOT, va="top")
fig.text(0.128, 0.962, "oes every dragon", fontproperties=DISP, fontsize=46, color=FG, va="top")
fig.text(0.128, 0.920, "live by the church?", fontproperties=DISP, fontsize=46, color=FG, va="top")
fig.text(0.045, 0.852, f"{R['n_legends']} named dragon, worm and serpent legends of Britain, placed where their sources put them,\n"
         f"and {R['n_names']} Dragon, Drake, Worm and Serpent place names, each compared with 50 ordinary places nearby.",
         family=SER, fontsize=15, color=FG, va="top", linespacing=1.4)
# a small wyrm under the title
xx = np.linspace(0.045, 0.62, 400)
fig.add_artist(plt.Line2D(xx, 0.8705 + 0.0040 * np.sin((xx - 0.045) * 48), transform=fig.transFigure, color=HOT, lw=2.2, solid_capstyle="round"))
fig.add_artist(plt.Polygon([[0.62, 0.8705], [0.633, 0.8745], [0.630, 0.8675]], closed=True, transform=fig.transFigure, color=HOT))

# hero map
ax = fig.add_axes([0.02, 0.255, 0.56, 0.55])
ax.scatter(base.x, base.y, s=0.3, c=LAND, lw=0, rasterized=True)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(60000, 660000); ax.set_ylim(5000, 980000)
CC = {"worm_word": (VIO, "Worm as a word"), "worm_compound": (BLUE, "Other Worm-"), "drake_mound": (GOLD, "Drake + mound word"),
      "drake_other": ("#C49A4E", "Other Drake"), "dragon": ("#E0645C", "Dragon"), "serpent": ("#1F6E62", "Serpent")}
for c, (col, lab) in CC.items():
    q = N[N.cls == c]
    ax.scatter(q.x, q.y, s=16, c=col, lw=0.4, edgecolors=BG, zorder=3, label=f"{lab}  {len(q)}")
ax.scatter(L.x, L.y, s=420, c=HOT, alpha=0.18, lw=0, zorder=4)
ax.scatter(L.x, L.y, s=95, c=HOT, edgecolors="white", lw=1.2, zorder=5, label=f"Legend  {len(L)}")
LBL = {"lambton": ("Lambton Worm", 60000, 25000), "linton": ("Worm of Linton", -175000, 20000), "laidly": ("Laidly Worm", 30000, 30000),
       "sockburn": ("Sockburn Worm", 45000, -5000), "wantley": ("Dragon of Wantley", 45000, 0), "mordiford": ("Mordiford", -150000, 18000),
       "knucker": ("Knucker of Lyminster", -110000, -45000), "uffington": ("Dragon Hill, Uffington", 40000, 95000),
       "ludham": ("Ludham", -20000, 32000), "graban": ("Llandeilo Graban", -170000, -70000)}
for r in L.itertuples():
    if r.id in LBL:
        t, dx, dy = LBL[r.id]
        ax.annotate(t, xy=(r.x, r.y), xytext=(r.x + dx, r.y + dy), family=SER, fontsize=11, color=FG, style="italic",
                    arrowprops=dict(arrowstyle="-", color=FG, lw=0.6), zorder=6)
h, l = ax.get_legend_handles_labels()
fig.legend(h[::-1], l[::-1], loc="upper left", bbox_to_anchor=(0.045, 0.80), frameon=False, prop={"family": MONO, "size": 10.5},
           labelcolor=FG, handletextpad=0.2, labelspacing=0.45, markerscale=0.9)

# right column: big numbers
g = G["legends"]
notes = [
    (pc(g["church_1"]["match"]["obs"]), f"of the legends lie within 1 km of a church.\nOrdinary places of the same kind nearby:\n{pc(g['church_1']['match']['base'])}. Random land: {pc(g['church_1']['rand']['base'])}."),
    (f"{g['church_med']['match']['obs'] * 1000:.0f} m", f"median distance from a legend to a church,\nagainst {g['church_med']['match']['base'] * 1000:.0f} m for matched places. In {R['legends_church_story']} of\nthe {R['n_legends']} stories the slayer or the dragon\nturns up in the church itself."),
    (pc(g["any4"]["match"]["obs"]), f"sit next to a church, barrow, hillfort or river.\nBut so do {pc(g['any4']['match']['base'])} of ordinary places. Barrows,\nhillforts, rivers alone: legends {pc(g['barrow_2']['match']['obs'])}, {pc(g['hillfort_2']['match']['obs'])}, {pc(g['river_05']['match']['obs'])};\nmatched places {pc(g['barrow_2']['match']['base'])}, {pc(g['hillfort_2']['match']['base'])}, {pc(g['river_05']['match']['base'])}."),
    (pc(G["names_north"]["barrow_2"]["match"]["obs"]), f"of northern dragon-word names lie within\n2 km of a recorded barrow (matched: {pc(G['names_north']['barrow_2']['match']['base'])}).\nYet both Drakelows, 'dragon's mound', are\n{R['supported_rows'][2]['barrow_km']:.1f} and {R['supported_rows'][3]['barrow_km']:.1f} km from one."),
]
tx = fig.add_axes([0.6, 0.27, 0.37, 0.53]); tx.axis("off")
for (big, small), y in zip(notes, [1.0, 0.75, 0.50, 0.25]):
    tx.text(0, y, big, fontproperties=DISP, fontsize=34, color=HOT, va="top", transform=tx.transAxes)
    tx.text(0, y - 0.075, small, family=SER, fontsize=12.5, color=FG, va="top", transform=tx.transAxes, linespacing=1.3)

# bottom row: the four companions
fig.text(0.045, 0.252, "LEGENDS AGAINST 50 MATCHED PLACES EACH  (bars: share of places; whiskers: 95% range of 2,000 draws)", family=MONO, fontsize=10.5, color=MUT)
P4 = [("church_1", "Church within 1 km"), ("barrow_2", "Barrow within 2 km"), ("hillfort_2", "Hillfort within 2 km"), ("river_05", "River within 500 m")]
for i, (k, lab) in enumerate(P4):
    a = fig.add_axes([0.06 + i * 0.235, 0.122, 0.19, 0.098], facecolor=BG)
    x = g[k]
    vals = [x["match"]["obs"], x["match"]["base"], x["rand"]["base"]]
    a.bar([0, 1, 2], [v * 100 for v in vals], color=[HOT, BAND, BAND], width=0.7)
    for j, (lo, hi) in enumerate([(None, None), (x["match"]["base_lo"], x["match"]["base_hi"]), (x["rand"]["base_lo"], x["rand"]["base_hi"])]):
        if lo is not None: a.errorbar(j, (lo + hi) * 50, yerr=(hi - lo) * 50, color=FG, lw=1, capsize=4)
        a.text(j, vals[j] * 100 + 3 if j == 0 else (hi or 0) * 100 + 3, pc(vals[j]), ha="center", family=MONO, fontsize=11, color=FG)
    a.set_ylim(0, 95); a.set_xticks([0, 1, 2]); a.set_xticklabels(["legends", "matched", "random"], family=MONO, fontsize=10)
    a.set_yticks([]); [a.spines[s].set_visible(False) for s in ("top", "right", "left")]; a.spines["bottom"].set_color(MUT)
    a.tick_params(length=0, colors=FG)
    a.set_title(lab, family=SER, fontsize=13, color=FG, pad=4, fontweight="semibold")

fig.text(0.045, 0.026,
         "Data: legends from English Wikipedia (CC BY-SA 4.0) and D. L. Ashliman, British Dragons (University of Pittsburgh),\n"
         "placed with OS Open Names. Names: OS Open Names; rivers: OS Open Rivers (contains OS data © Crown copyright and database\n"
         "right 2026, OGL v3). Churches: Wikidata (CC0). Barrows: OpenStreetMap (ODbL) and Wikidata. Hillforts: Atlas of Hillforts of\n"
         "Britain and Ireland (CC BY-SA 4.0). Name classes describe form only: most Drake and Worm names need not be dragons.\n"
         "Analysis and chart: Tristan Hotham, with Python and matplotlib.",
         family=MONO, fontsize=8.6, color=MUT, linespacing=1.45)
fig.savefig(os.path.join(HERE, "here_be_dragons.png"), facecolor=BG, dpi=200)
print("ok")
