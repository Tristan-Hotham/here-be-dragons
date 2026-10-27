"""Name classes for dragon-like words in OS Open Names.

A match means only that the letters are there. None of these classes is an etymology:
Old English draca ("dragon") and wyrm ("dragon, serpent, worm") are possible sources, but so are
personal names, the male duck (drake), a surname (Drake) and other roots. Every name is a
"possible" dragon name unless a source on disk or a cited web page supports a dragon reading
(see SUPPORTED below).

Classes
  dragon        the word Dragon (not Dragonfly)
  drake_mound   Drake joined to a mound or hill word: -low, -loe, Law, Howe, Knowe
  drake_other   any other Drake name (possessive Drake's forms are flagged; they are more often
                a surname or a duck than a dragon, but I do not decide that here)
  worm_word     Worm or Worms as a word of its own, or Wormhill / Wormshill / Hag Worm
  worm_compound other names that begin Worm- (Wormley, Wormington, Wormit ...), where the first
                element may well be a personal name or something else entirely
  serpent       Serpent (not Serpentine, a garden or rock word, and not Serpentwalk)
Excluded but counted: Dragonfly, Serpentine, Serpentwalk, Wormwood (a plant).
Run the tests: python3 code/terms.py
"""
import re

EXCLUDE = re.compile(r"Dragonfly|Serpentine|Serpentwalk|Wormwood|Serpentine Walk")
DRAGON = re.compile(r"\bDragon")
DRAKE_MOUND = re.compile(r"\bDrake\s*(lo[we]|loe|Law|Howe|Knowe|knowe)", re.I)
DRAKE = re.compile(r"\bDrake")
WORM_WORD = re.compile(r"\b(Hagg? )?Worms?\b|\bWorm(s)?hill\b|\bWormshell\b|\bWormhole\b")
WORM = re.compile(r"\bWorm")
SERPENT = re.compile(r"\bSerpent")
ANY = re.compile(r"Dragon|\bDrake|\bWorm|\bSerpent")
CLASSES = ["dragon", "drake_mound", "drake_other", "worm_word", "worm_compound", "serpent"]
LABEL = {"dragon": "Dragon", "drake_mound": "Drake + mound word", "drake_other": "Other Drake",
         "worm_word": "Worm as a word", "worm_compound": "Other Worm-", "serpent": "Serpent"}

# Names for which a cited source gives a dragon reading. (os name, county) -> (reading, source)
SUPPORTED = {
    ("Drakelow", "Derbyshire"): ("'Dragon's Mound'", "https://en.wikipedia.org/wiki/Drakelow"),
    ("Drakelow Park", "Derbyshire"): ("same place as Drakelow, 'Dragon's Mound'", "https://en.wikipedia.org/wiki/Drakelow"),
    ("Drakelow", "Worcestershire"): ("'Dragon's Mound'", "https://en.wikipedia.org/wiki/Drakelow,_Worcestershire"),
    ("Wormhill", "Derbyshire"): ("Wruenele: 'Wruen' worm, reptile or dragon, and 'ele' hill (local folklore of a dragon at Knotlow)",
                                 "https://en.wikipedia.org/wiki/List_of_dragons_in_mythology_and_folklore"),
    ("Dragon Hill", "Oxfordshire"): ("tradition, recorded by 1738, that St George slew the dragon here",
                                     "https://en.wikipedia.org/wiki/Dragon_Hill,_Uffington"),
}


def classify(name):
    if not name or EXCLUDE.search(name):
        return None
    if DRAGON.search(name): return "dragon"
    if DRAKE_MOUND.search(name): return "drake_mound"
    if DRAKE.search(name): return "drake_other"
    if WORM_WORD.search(name): return "worm_word"
    if WORM.search(name): return "worm_compound"
    if SERPENT.search(name): return "serpent"
    return None


def excluded(name):
    return bool(name) and bool(EXCLUDE.search(name)) and bool(ANY.search(name))


if __name__ == "__main__":
    T = {"Dragon Hill": "dragon", "Dragonfly Pool": None, "Dragonby": "dragon", "Drakelow": "drake_mound",
         "Lower Drakeloe Pond": "drake_mound", "Drake Law": "drake_mound", "Drake Howe": "drake_mound",
         "Drakeknowe Plantation": "drake_mound", "Drake Knowe Wood": "drake_mound", "Drake's Island": "drake_other",
         "Drakes Broughton": "drake_other", "Worm Hill": "worm_word", "Worms Cleuch": "worm_word",
         "Wormhill": "worm_word", "Wormshill": "worm_word", "Hag Worm Hill": "worm_word", "Hagg Worm Haw Moss": "worm_word",
         "Wormley": "worm_compound", "Wormit": "worm_compound", "Wormwood Scrubs": None, "Serpent Brae": "serpent",
         "The Serpentine": None, "Serpentwalk Plantation": None, "Drakemyre": "drake_other", "Drakelow Gorse": "drake_mound"}
    for k, v in T.items():
        assert classify(k) == v, (k, classify(k), v)
    print("terms ok")
