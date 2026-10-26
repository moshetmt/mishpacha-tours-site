# -*- coding: utf-8 -*-
"""Cartes chalet (Moshé, 26/10/2026, capture iPhone) : la ligne « Les Deux Alpes · with Winter Prestige » collait à la photo ;
elle descend sous l'encadré « Strictly kosher ». Idempotent, toutes les pages ; _kit_wp.py produit déjà ce balisage.
    python _lieu_bas.py   (depuis site-v5/)"""
import glob, re
n = 0
for p in glob.glob("**/*.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    h2 = re.sub(r'<div class="kwp-corps">(<div class="kwp-lieu">.*?</div>)(.*?<p class="kwp-casher">.*?</p>)',
                lambda m: f'<div class="kwp-corps">{m.group(2)}{m.group(1)}', h, flags=re.S)
    if h2 != h: open(p, "w", encoding="utf-8").write(h2); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* LIEU-BAS */" not in css:
    css += """
/* LIEU-BAS */ /* 26/10 : lieu sous l'encadré casher, titre en tête de carte */
body .kwp-corps>.kwp-lieu{margin-top:14px;padding-inline-end:0}
body .kwp-carte .kwp-corps>h3:first-child{margin-top:0;padding-top:18px}
body .kwp-carte .kwp-corps>.kwp-lieu+.kwp-dispo{margin-top:8px}
/* Safari : en grille subgrid, la photo 3:2 débordait sur la 1re ligne de texte (page des chalets, ordinateur) */
.kwp-cartes .kwp-carte>.kwp-photo{aspect-ratio:auto;height:0;padding-bottom:66.667%}
@media (min-width:900px){body .kwp-cartes .kwp-corps>.kwp-lieu{margin-top:0;padding:14px 22px 0}.kwp-cartes .kwp-corps>h3:first-child{padding-top:22px}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
