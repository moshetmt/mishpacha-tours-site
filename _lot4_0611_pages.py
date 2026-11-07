# -*- coding: utf-8 -*-
"""Lot 4 contenu, retouches HTML des pages existantes (n° 17 et 19), idempotent. Depuis site-v5/ : python _lot4_0611_pages.py
 - classe body « l4 » sur les pages du lot (déclenche le bloc CSS LOT4-0611) ;
 - page services : titre de la carte traduit (il restait en anglais sur FR, ES, HE) ;
 - « Yhia Lahiany » → « Yehia Lahiany » partout (graphie de l'ETAT.md et du certificat)."""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["kosher-services-french-alps", "kosher-pesach-french-alps", "summer-in-the-alps-jewish-families", "jewish-lyon-tours"]
LANGS = ["", "fr/", "es/", "he/"]
CARTE = {"fr/": "Aéroport de Lyon-Saint-Exupéry", "es/": "Aeropuerto de Lyon-Saint-Exupéry", "he/": "נמל התעופה ליון סנט-אקזופרי"}
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

n = 0
for page in PAGES:
    for l in LANGS:
        p = f"{l}{page}/index.html"
        s = rd(p); s0 = s
        s = re.sub(r'<body class="(?![^"]*\bl4\b)([^"]*)"', r'<body class="\1 l4"', s, count=1)
        if page == "jewish-lyon-tours":
            s = re.sub(r'<body class="(?![^"]*\bl4-lyon\b)([^"]*)"', r'<body class="\1 l4-lyon"', s, count=1)
        if page == "kosher-services-french-alps" and l in CARTE:
            s = s.replace('<h2 class="centre carte-titre">Lyon-Saint-Exupéry airport</h2>', f'<h2 class="centre carte-titre">{CARTE[l]}</h2>')
        if s != s0: wr(p, s); n += 1
print("classe l4 et carte :", n, "page(s) modifiée(s)")

m = 0
for p in glob.glob("**/index.html", recursive=True):
    if p.startswith(("_brouillons", "_candidats")): continue
    s = rd(p)
    if "Yhia" in s:
        wr(p, s.replace("Yhia Lahiany", "Yehia Lahiany")); m += 1
print("Yhia → Yehia :", m, "page(s)")
