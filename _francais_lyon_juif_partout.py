# -*- coding: utf-8 -*-
"""« Lyon juif » ne se dit pas (Moshé 21/10 pour le menu, 27/10 pour tout le site). Le 21/10 seuls le menu et le pied
avaient changé (_francais_lyon_juif.py) ; ici titres, h1, meta, JSON-LD et texte courant des pages FR, et les scripts
sources. Keyword Planner FR (27/10) : « lyon juif » 10 recherches/mois, « quartier juif lyon » 110. Idempotent.
    python _francais_lyon_juif_partout.py   (depuis site-v5/)"""
import glob, re
R = [  # du plus long au plus court
    ("Lyon juif, visite guidée juive privée de Lyon", "Visite guidée privée du quartier juif de Lyon"),
    ("Le Lyon juif, le guide complet", "Le guide juif complet de Lyon"),
    ("Le Lyon juif et la Grande Synagogue", "Le quartier juif et la Grande Synagogue de Lyon"),
    ("La rue Juiverie et le Lyon juif médiéval", "La rue Juiverie et le quartier juif médiéval de Lyon"),
    ("Lyon juif en deux jours", "Le patrimoine juif de Lyon en deux jours"),
    ("Visite guidée du Lyon juif", "Visite guidée du quartier juif de Lyon"),
    ("Guide du Lyon juif", "Guide juif de Lyon"),
    ("Visite du Lyon juif", "Visite du quartier juif de Lyon"),
    ("visite du Lyon juif", "visite du quartier juif de Lyon"),
    ("Visite Lyon juif", "Visite du quartier juif"),
    ("visite Lyon juif", "visite du quartier juif"),
    ("Balade dans le Lyon juif", "Balade dans le quartier juif de Lyon"),
    ("dans le Lyon juif", "dans les lieux juifs de Lyon"),
    ("du Lyon juif", "du patrimoine juif de Lyon"),
    ("Le Lyon juif", "Le patrimoine juif de Lyon"),
    ("le Lyon juif", "le patrimoine juif de Lyon"),
    ("Lyon juif", "Visite juive à Lyon"),  # reste : libellés isolés (menus, options)
]
def corriger(s):
    for a, b in R:
        s = s.replace(a, b)
    return s
n = 0
fichiers = glob.glob("fr/**/*.html", recursive=True) + glob.glob("fr/**/*.md", recursive=True)
fichiers += ["_demande_nouveaux.py", "_demande_textes.py", "_offres_lyon.py", "_pages/lyon-weather.py", "_pages/things-to-do-in-lyon.py", "_van_textes.py"]
for p in fichiers:
    try:
        s = open(p, encoding="utf-8").read()
    except FileNotFoundError:
        continue
    t = corriger(s)
    if t != s:
        open(p, "w", encoding="utf-8").write(t); n += 1
print(n, "fichiers corrigés")
