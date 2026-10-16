# -*- coding: utf-8 -*-
"""Lot du 16/10 : branche les 6 stations suisses et italiennes dans toutes les listes du site (idempotent)."""
import io, re
NEW = [  # slug, en, fr, es, he, geonameid, carte (titre, texte)
 ("kosher-zermatt", "Zermatt", "Zermatt", "Zermatt", "צרמט", 2657928, ("Kosher in Zermatt", "Car-free village under the Matterhorn, winter and summer: chef, meals, Shabbat, holidays, minyan")),
 ("kosher-st-moritz", "St. Moritz", "Saint-Moritz", "St. Moritz", "סנט מוריץ", 2658813, ("Kosher in St. Moritz", "The Engadine in winter and summer: chef, meals, Shabbat, holidays, minyan")),
 ("kosher-crans-montana", "Crans-Montana", "Crans-Montana", "Crans-Montana", "קראן מונטנה", 6559506, ("Kosher in Crans-Montana", "The sunny plateau of the Valais, two hours from Geneva: chef, meals, Shabbat, holidays, minyan")),
 ("kosher-cervinia", "Cervinia", "Cervinia", "Cervinia", "צרביניה", 6534766, ("Kosher in Cervinia", "Italy's side of the Matterhorn, snow from November to May: chef, meals, Shabbat, holidays, minyan")),
 ("kosher-courmayeur", "Courmayeur", "Courmayeur", "Courmayeur", "קורמאייר", 3177872, ("Kosher in Courmayeur", "The Italian side of Mont Blanc, the closest Italian resort to Lyon: chef, meals, Shabbat, holidays, minyan")),
 ("kosher-cortina", "Cortina d'Ampezzo", "Cortina d'Ampezzo", "Cortina d'Ampezzo", "קורטינה", 3177952, ("Kosher in Cortina d'Ampezzo", "The Dolomites, winter and summer: chef, meals, Shabbat, holidays, minyan")),
]
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def patch(path, anchor, add, check):
    s = rd(path)
    if check in s: print("ok   ", path); return
    assert anchor in s, (path, anchor)
    wr(path, s.replace(anchor, anchor + add, 1)); print("patch", path)

# 1. hub : cartes apres Val d'Isere
patch("_build_hub.py", '  ("kosher-val-disere/", "stock/alpes-ski.jpg", "Kosher in Val d\'Isère", "From late November to May: chef, meals, Shabbat, holidays, minyan in Val d\'Isère"),\n',
      "".join(f'  ("{s}/", "stock/alpes-ski.jpg", "{c[0]}", "{c[1]}"),\n' for s, *_, c in NEW), '"kosher-zermatt/"')
# 2. zones : ALPES + pastilles du menu
patch("_zones.py", '"kosher-val-disere", "kosher-val-thorens",', "\n         " + ", ".join(f'"{s}"' for s, *_ in NEW) + ",", '"kosher-zermatt",')
patch("_zones.py", '("Annecy", "kosher-annecy"), ("Grenoble", "kosher-grenoble")', ",\n            " + ", ".join(f'("{en}", "{s}")' for s, en, *_ in NEW), '("Zermatt", "kosher-zermatt")')
# 3. lead : photo + nom par langue
patch("_lead.py", " 'kosher-val-disere': ('stock/st-val-disere.jpg', dict(en=\"Val d'Isère\", fr=\"Val d'Isère\", es=\"Val d'Isère\", he='ואל דיזר')),\n",
      "".join(f" '{s}': ('stock/st-{s[7:]}.jpg', dict(en=\"{en}\", fr=\"{fr}\", es=\"{es}\", he='{he}')),\n" for s, en, fr, es, he, *_ in NEW), "'kosher-zermatt'")
# 4. prefill
patch("_prefill.py", '"kosher-megeve": "Megève", "kosher-val-disere": "Val d\'Isère", "kosher-val-thorens": "Val Thorens"', ",\n            " + ", ".join(f'"{s}": "{en}"' for s, en, *_ in NEW), '"kosher-zermatt"')
# 5. decor : hassid
patch("_decor.py", '"kosher-van-transfers", "kosher-chalet-les-deux-alpes"', ",\n                " + ", ".join(f'"{s}"' for s, *_ in NEW), '"kosher-zermatt"')
s = rd("_decor.py")
if "zermatt" not in s.split("mountain-snow")[0][-200:]:
    s = s.replace('chamonix|arcs|plagne", "mountain-snow")', 'chamonix|arcs|plagne|zermatt|moritz|crans|cervinia|courmayeur|cortina", "mountain-snow")'); wr("_decor.py", s); print("patch _decor regex")
# 6. images cartes
patch("_images_cartes.py", "    'kosher-val-disere': 'stock/hub-kosher-val-disere.jpg',\n", "".join(f"    '{s}': 'stock/hub-{s}.jpg',\n" for s, *_ in NEW), "'kosher-zermatt'")
# 7. hebcal
patch("_contacts_bh_hebcal.py", '    "kosher-val-thorens": (6544556, dict(en="Val Thorens", fr="Val Thorens", es="Val Thorens", he="ואל טורנס")),\n',
      "".join(f'    "{s}": ({g}, dict(en="{en}", fr="{fr}", es="{es}", he="{he}")),\n' for s, en, fr, es, he, g, _ in NEW), '"kosher-zermatt"')
# 8. animations : flocons
s = rd("_animations.py")
if "zermatt" not in s:
    s = s.replace("val-disere|val-thorens|ski-holidays-french-alps|chalet-les-deux-alpes)", "val-disere|val-thorens|zermatt|st-moritz|crans-montana|cervinia|courmayeur|cortina|ski-holidays-french-alps|chalet-les-deux-alpes)"); wr("_animations.py", s); print("patch _animations")
# 9. page /alps/ : liste resort by resort
s = rd("_pages/alps.py")
if "kosher-zermatt" not in s:
    s = s.replace('<a href="../kosher-val-disere/">Val d\'Isère</a></li>',
      '<a href="../kosher-val-disere/">Val d\'Isère</a>. In Switzerland: <a href="../kosher-zermatt/">Zermatt</a>, <a href="../kosher-st-moritz/">St. Moritz</a>, <a href="../kosher-crans-montana/">Crans-Montana</a>. In Italy: <a href="../kosher-cervinia/">Cervinia</a>, <a href="../kosher-courmayeur/">Courmayeur</a>, <a href="../kosher-cortina/">Cortina d\'Ampezzo</a></li>')
    wr("_pages/alps.py", s); print("patch _pages/alps.py")
print("done")
