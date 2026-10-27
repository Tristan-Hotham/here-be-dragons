# Here Be Dragons

The dragons, worms and wyrms of British folklore and place names. Does every dragon sit next to a church, a barrow, a hillfort or a river? This study places 26 named dragon, worm and serpent legends at the village, hill or wood their written source names, collects all 135 Dragon, Drake, Worm and Serpent names on the Ordnance Survey's open gazetteer of Great Britain, and compares each with 50 ordinary places of the same kind from the same 50 km square, and with random points of land.

**Interactive version:** https://tristan-hotham.github.io/here-be-dragons/

**Paper:** https://doi.org/10.5281/zenodo.23689964

**Blog post:** https://blog.tristanhotham.com/2026/10/27/here-be-dragons/

By Dr Tristan Hotham (Independent researcher, ORCID 0000-0003-4931-9349). Companion studies: [Is the Barrow a European Thing?](https://tristan-hotham.github.io/barrows-of-europe/) (the barrow data), [Whose Church Is It?](https://tristan-hotham.github.io/saints-and-wells/) (church dedications), [Within Sight](https://tristan-hotham.github.io/within-sight/) (hillforts), [Gallows Hill](https://tristan-hotham.github.io/gallows-hill/) (the same matched-name method).

## Headline results

- Legends: 29 British legends with a place were collected from English Wikipedia and D. L. Ashliman's British Dragons texts; 26 could be placed with OS Open Names (24 in England, 1 in Scotland, 1 in Wales).
- The legends cling to the church: 77% lie within 1 km of a church in Wikidata, against 55% of matched places of the same kind and 34% of random land (chance 0.015). Median distance 303 m against 824 m. In 11 of the 26 stories, the source itself ties the legend to a church.
- No closer to barrows, hillforts or rivers: within 2 km of a barrow 23% (matched 20%), within 2 km of a hillfort 23% (18%), within 500 m of a named river 19% (16%). Next to at least one of the four: 92% against 75%.
- Names: 135 OS names contain Dragon (11), Drake (11 with a mound word, 28 others), Worm (30 as a word, 51 other Worm- names) or Serpent (4). Only 5 have a dragon reading in a source checked here. As a whole they sit no nearer churches, hillforts or rivers than matched names; barrows: 26% within 2 km against 20% (chance 0.048).
- The barrow signal is northern: 33% of 60 names in the north of England and Scotland lie within 2 km of a recorded barrow or cairn, against 16% of matched names (chance below 0.001); in the south 20% against 22%. Drake Howe on Cringle Moor is 10 m from a recorded barrow; the two Drakelows read as "dragon's mound" are 7.3 km and 13.8 km from the nearest.
- Worms of the north: 4 of the 5 legends whose creature is a worm are in the north. The names do not follow: 12.6 Worm-as-a-word names per 100,000 OS features in the north, 9.8 in the south.
- St George: 7.3% of churches within 5 km of a legend are dedicated to St George or St Michael, against 5.4% near matched places and 3.9% of all churches; a St George church within 5 km: 27% of legends against 14% (chance 0.090). Suggestive, not more.

## Files

- `index.html`: the interactive page (Leaflet map, charts). Data are embedded.
- `header.png`: social card (1200 by 630).
- `data/legends.csv`: every legend: id, name, creature word, source (WPL, WPA or ASH), source URL, the phrase that names the place, whether the source ties the story to a church (with a note), St George flag, the OS Open Names feature used, its coordinates and a sentence saying how it was placed.
- `data/legends_measured.csv`: the placed legends with every distance (nearest church and its name, nearest St George or St Michael church, barrow, hillfort, named river, any named watercourse).
- `data/dragon_names.csv`: one row per OS Open Names feature in the six classes (`code/terms.py`), with OS type, coordinates (WGS84 and British National Grid), region, control stratum, whether a source supports a dragon reading (with the reading and its URL), and the same distances.
- `data/controls.csv.gz`: the 50 matched names and 50 random land points for each legend and name (`parent_os_feature_row` is the OS row of the legend place or name), with the same distances.
- `data/test_results.csv`: every test: group, measure, control type, observed value, control value, 95% range of the replicate controls, chance value.
- `data/results.json`: every number used on the page, in the paper, the blog post and the collage.
- `code/legends.py`: the legends with sources and places. `code/terms.py`: the name classes, with tests.
- `code/01_points.py`, `code/02_measure.py`, `code/03_analyse.py`, `code/04_build_site.py`, `code/05_header.py`: run in that order. `release/` holds the paper and blog figure scripts and `reddit/` the collage.

## Method in brief

Legends come from the English Wikipedia "List of dragons in mythology and folklore" and the articles on individual legends (wikitext of 27 October 2026, and pages read that day), and from D. L. Ashliman's British Dragons texts (https://sites.pitt.edu/~dash/britishdragons.html). Each is placed at the most specific place its source names that OS Open Names also lists. A Wikidata query for dragon items timed out, so Wikidata adds no legends. Names are OS Open Names features with words beginning Dragon, Drake, Worm or Serpent (34 Dragonfly, Serpentine, Serpentwalk and Wormwood names set aside); the classes describe form, not origin. Controls: for each legend or name, 50 OS names of the same local type from the same 50 km grid square (100 km, then country, when fewer than 20), with every dragon-word name excluded, and 50 random land points in the same square; 2,000 replicate control sets, one control per place, two-sided chance values. Distances: 36,435 Wikidata church buildings in Great Britain (dedications as parsed in Whose Church Is It?); 12,387 barrows, cairns and mounds (OpenStreetMap and Wikidata, via Is the Barrow a European Thing?); 3,610 hillforts (Atlas of Hillforts of Britain and Ireland); named rivers in OS Open Rivers (River or Afon names and tidal rivers).

Caveats: the legends are few and the sources favour England and stories with church monuments; a legend placed at a village shares that village's church, which is why the controls are villages too; Wikidata churches are of every date; barrow records vary a lot by area; river crossings could not be tested, only distance to a river; 13 measures on many groups, so isolated chance values near 0.05 should be read with caution. The classes of names are not etymologies.

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
