# Here Be Dragons

The dragons, worms and wyrms of British folklore and place names. Does every dragon sit next to a church, a barrow, a hillfort or a river? This study places {{n_legends|int}} named dragon, worm and serpent legends at the village, hill or wood their written source names, collects all {{n_names|int}} Dragon, Drake, Worm and Serpent names on the Ordnance Survey's open gazetteer of Great Britain, and compares each with {{k_controls|int}} ordinary places of the same kind from the same 50 km square, and with random points of land.

**Interactive version:** https://tristan-hotham.github.io/here-be-dragons/

**Paper:** https://doi.org/10.5281/zenodo.23689964

**Blog post:** https://blog.tristanhotham.com/2026/10/27/here-be-dragons/

By Dr Tristan Hotham (Independent researcher, ORCID 0000-0003-4931-9349). Companion studies: [Is the Barrow a European Thing?](https://tristan-hotham.github.io/barrows-of-europe/) (the barrow data), [Whose Church Is It?](https://tristan-hotham.github.io/saints-and-wells/) (church dedications), [Within Sight](https://tristan-hotham.github.io/within-sight/) (hillforts), [Gallows Hill](https://tristan-hotham.github.io/gallows-hill/) (the same matched-name method).

## Headline results

- Legends: {{n_legends_listed|int}} British legends with a place were collected from English Wikipedia and D. L. Ashliman's British Dragons texts; {{n_legends|int}} could be placed with OS Open Names ({{legends_by_country.England|int}} in England, {{legends_by_country.Scotland|int}} in Scotland, {{legends_by_country.Wales|int}} in Wales).
- The legends cling to the church: {{groups.legends.church_1.match.obs|pct0}} lie within 1 km of a church in Wikidata, against {{groups.legends.church_1.match.base|pct0}} of matched places of the same kind and {{groups.legends.church_1.rand.base|pct0}} of random land (chance {{groups.legends.church_1.match.p|p}}). Median distance {{groups.legends.church_med.match.obs|m}} against {{groups.legends.church_med.match.base|m}}. In {{legends_church_story|int}} of the {{n_legends|int}} stories, the source itself ties the legend to a church.
- No closer to barrows, hillforts or rivers: within 2 km of a barrow {{groups.legends.barrow_2.match.obs|pct0}} (matched {{groups.legends.barrow_2.match.base|pct0}}), within 2 km of a hillfort {{groups.legends.hillfort_2.match.obs|pct0}} ({{groups.legends.hillfort_2.match.base|pct0}}), within 500 m of a named river {{groups.legends.river_05.match.obs|pct0}} ({{groups.legends.river_05.match.base|pct0}}). Next to at least one of the four: {{groups.legends.any4.match.obs|pct0}} against {{groups.legends.any4.match.base|pct0}}.
- Names: {{n_names|int}} OS names contain Dragon ({{by_class.dragon|int}}), Drake ({{by_class.drake_mound|int}} with a mound word, {{by_class.drake_other|int}} others), Worm ({{by_class.worm_word|int}} as a word, {{by_class.worm_compound|int}} other Worm- names) or Serpent ({{by_class.serpent|int}}). Only {{names_supported|int}} have a dragon reading in a source checked here. As a whole they sit no nearer churches, hillforts or rivers than matched names; barrows: {{groups.names.barrow_2.match.obs|pct0}} within 2 km against {{groups.names.barrow_2.match.base|pct0}} (chance {{groups.names.barrow_2.match.p|p}}).
- The barrow signal is northern: {{groups.names_north.barrow_2.match.obs|pct0}} of {{groups.names_north.n|int}} names in the north of England and Scotland lie within 2 km of a recorded barrow or cairn, against {{groups.names_north.barrow_2.match.base|pct0}} of matched names (chance {{groups.names_north.barrow_2.match.p|p}}); in the south {{groups.names_south.barrow_2.match.obs|pct0}} against {{groups.names_south.barrow_2.match.base|pct0}}. Drake Howe on Cringle Moor is {{drake_mound_rows.0.barrow_km|m}} from a recorded barrow; the two Drakelows read as "dragon's mound" are {{supported_rows.2.barrow_km|km1}} and {{supported_rows.3.barrow_km|km1}} from the nearest.
- Worms of the north: {{legends_worm_north|int}} of the {{legends_by_word.worm|int}} legends whose creature is a worm are in the north. The names do not follow: {{north.worm_word_per100k|f1}} Worm-as-a-word names per 100,000 OS features in the north, {{south.worm_word_per100k|f1}} in the south.
- St George: {{gm_near_legends.share|pct1}} of churches within 5 km of a legend are dedicated to St George or St Michael, against {{gm_near_legend_controls.share|pct1}} near matched places and {{gm_share_all_churches|pct1}} of all churches; a St George church within 5 km: {{groups.legends.george_5.match.obs|pct0}} of legends against {{groups.legends.george_5.match.base|pct0}} (chance {{groups.legends.george_5.match.p|p}}). Suggestive, not more.

## Files

- `index.html`: the interactive page (Leaflet map, charts). Data are embedded.
- `header.png`: social card (1200 by 630).
- `data/legends.csv`: every legend: id, name, creature word, source (WPL, WPA or ASH), source URL, the phrase that names the place, whether the source ties the story to a church (with a note), St George flag, the OS Open Names feature used, its coordinates and a sentence saying how it was placed.
- `data/legends_measured.csv`: the placed legends with every distance (nearest church and its name, nearest St George or St Michael church, barrow, hillfort, named river, any named watercourse).
- `data/dragon_names.csv`: one row per OS Open Names feature in the six classes (`code/terms.py`), with OS type, coordinates (WGS84 and British National Grid), region, control stratum, whether a source supports a dragon reading (with the reading and its URL), and the same distances.
- `data/controls.csv.gz`: the {{k_controls|int}} matched names and {{k_controls|int}} random land points for each legend and name (`parent_os_feature_row` is the OS row of the legend place or name), with the same distances.
- `data/test_results.csv`: every test: group, measure, control type, observed value, control value, 95% range of the replicate controls, chance value.
- `data/results.json`: every number used on the page, in the paper, the blog post and the collage.
- `code/legends.py`: the legends with sources and places. `code/terms.py`: the name classes, with tests.
- `code/01_points.py`, `code/02_measure.py`, `code/03_analyse.py`, `code/04_build_site.py`, `code/05_header.py`: run in that order. `release/` holds the paper and blog figure scripts and `reddit/` the collage.

## Method in brief

Legends come from the English Wikipedia "List of dragons in mythology and folklore" and the articles on individual legends (wikitext of 27 October 2026, and pages read that day), and from D. L. Ashliman's British Dragons texts (https://sites.pitt.edu/~dash/britishdragons.html). Each is placed at the most specific place its source names that OS Open Names also lists. A Wikidata query for dragon items timed out, so Wikidata adds no legends. Names are OS Open Names features with words beginning Dragon, Drake, Worm or Serpent ({{n_excluded|int}} Dragonfly, Serpentine, Serpentwalk and Wormwood names set aside); the classes describe form, not origin. Controls: for each legend or name, {{k_controls|int}} OS names of the same local type from the same 50 km grid square (100 km, then country, when fewer than 20), with every dragon-word name excluded, and {{k_controls|int}} random land points in the same square; 2,000 replicate control sets, one control per place, two-sided chance values. Distances: {{layers.n_churches|int}} Wikidata church buildings in Great Britain (dedications as parsed in Whose Church Is It?); {{layers.n_barrows|int}} barrows, cairns and mounds (OpenStreetMap and Wikidata, via Is the Barrow a European Thing?); {{layers.n_hillforts|int}} hillforts (Atlas of Hillforts of Britain and Ireland); named rivers in OS Open Rivers (River or Afon names and tidal rivers).

Caveats: the legends are few and the sources favour England and stories with church monuments; a legend placed at a village shares that village's church, which is why the controls are villages too; Wikidata churches are of every date; barrow records vary a lot by area; river crossings could not be tested, only distance to a river; {{n_measures|int}} measures on many groups, so isolated chance values near 0.05 should be read with caution. The classes of names are not etymologies.

## Rerun

Needs Python 3 with pandas, numpy, scipy, shapely 2 and pyproj (and playwright for the header). Place these one folder above this repository (or set `HIST`): `osnames_gb.tsv` (OS Open Names extract), `osrivers/Data/oprvrs_gb.gpkg` (OS Open Rivers), `how-roman-is-your-road/data/counties.geojson` (land outline), `saints-and-wells/data/churches.csv.gz`, `barrows-of-europe/data/barrows.csv` and `within-sight/data/forts_visibility.csv`. Then run the scripts in `code/` in order.

## Sources and licence

- Legends: English Wikipedia, CC BY-SA 4.0 (https://en.wikipedia.org/wiki/List_of_dragons_in_mythology_and_folklore and the articles linked in `data/legends.csv`); D. L. Ashliman (ed.), British Dragons, Folklore and Mythology Electronic Texts, University of Pittsburgh, https://sites.pitt.edu/~dash/britishdragons.html (short quoted phrases only).
- Place names and rivers: OS Open Names and OS Open Rivers. Contains OS data © Crown copyright and database right 2026. Open Government Licence v3.0.
- Land outline: Office for National Statistics counties, OGL v3.0.
- Churches: Wikidata, CC0, via https://github.com/Tristan-Hotham/saints-and-wells
- Barrows: © OpenStreetMap contributors (ODbL 1.0) and Wikidata (CC0), via https://github.com/Tristan-Hotham/barrows-of-europe
- Hillforts: Lock, G. and Ralston, I. (2017) Atlas of Hillforts of Britain and Ireland, https://hillforts.arch.ox.ac.uk, CC BY-SA 4.0, via https://github.com/Tristan-Hotham/within-sight
- Base map tiles on the page: Esri. Map library: Leaflet.

Because the Wikipedia text and the Atlas of Hillforts data are CC BY-SA, the derived data (`data/`) and the text are released under CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); distances to barrows derive from OpenStreetMap data under the ODbL. Code (`code/`) is MIT (see `LICENSE`).

## Citation

Hotham, T. (2026) *Here Be Dragons: the dragons, worms and wyrms of British folklore and place names.* Data study and paper. Zenodo. https://doi.org/10.5281/zenodo.23689964

I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped prepare the analysis code. I reviewed and checked all text and results.
