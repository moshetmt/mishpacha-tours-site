# -*- coding: utf-8 -*-
"""02/11 : champ caché « lieu » du formulaire des pages chalet (4 langues). Les pages clonées de Val Thorens gardaient
value="Val Thorens" en hébreu (remplace_noms ne traitait que l'hébreu) : les demandes de ces pages arrivaient avec la
mauvaise station. Ce script pose la station du chalet, page par page. Idempotent, ne touche qu'à ce champ.
Le générateur (_chalet_aigle_royal.page) pose aussi la bonne valeur depuis le 02/11, mais les pages ont été retouchées
après génération (titres, H1) : ne pas les régénérer pour corriger ce champ, lancer ce script.
    python _lieu_formulaire.py [--dry]   (depuis site-v5/)"""
import io
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
DRY = "--dry" in sys.argv
STATION = {
    "kosher-chalet-les-deux-alpes": "Les Deux Alpes", "kosher-slope-chalet-les-deux-alpes": "Les Deux Alpes",
    "kosher-chalet-courchevel": "Courchevel", "kosher-chalet-courchevel-aurore-boreale": "Courchevel",
    "kosher-chalet-courchevel-renard-argente": "Courchevel", "kosher-chalet-megeve": "Megève",
    "kosher-chalet-val-thorens": "Val Thorens", "kosher-chalet-les-menuires": "Les Ménuires",
    "kosher-chalet-tignes": "Tignes", "kosher-chalet-saint-gervais": "Saint-Gervais Mont-Blanc", "kosher-chalet-courchevel-1850": "Courchevel", "kosher-villa-saint-tropez": "Saint-Tropez",
}
CHAMP = re.compile(r'(<input type="hidden" name="lieu" value=")([^"]*)(")')

if __name__ == "__main__":
    for slug, st in STATION.items():
        for l in ("", "fr/", "es/", "he/"):
            p = ICI / f"{l}{slug}" / "index.html"
            if not p.exists():
                continue
            s = io.open(p, encoding="utf-8", newline="").read()
            avant = CHAMP.findall(s)
            if not avant:
                print(f"{l}{slug} : pas de champ lieu")
                continue
            t = CHAMP.sub(lambda m: m.group(1) + st + m.group(3), s)
            if t != s:
                print(f"{l}{slug} : {', '.join(a[1] for a in avant)} -> {st}")
                if not DRY:
                    io.open(p, "w", encoding="utf-8", newline="").write(t)
