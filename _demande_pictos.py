# -*- coding: utf-8 -*-
"""Pictos de l'écran 1 du formulaire /plan-your-trip/ (02/11) : 6 dessins de la famille Mishpacha (version -petit, noir sur blanc),
   recopiés dans img/illus/famille/form/ avec un viewBox carré centré sur le dessin réel (getBBox), pour que les 6 se centrent
   au pixel près dans la même boîte (règle du 02/11 : pictos d'une série alignés et mesurés, scripts/controle_alignement.py).
   Source : 00-brief/charte-graphique/pictos-famille/ du dépôt principal (dossier non suivi par git). Idempotent.
   python _demande_pictos.py (depuis site-v5/)"""
import os, re, io
from playwright.sync_api import sync_playwright

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = r"E:\projet site\ads-os\clients\mishpacha-tours\00-brief\charte-graphique\pictos-famille"
OUT = os.path.join("img", "illus", "famille", "form")
PICTOS = {   # branche du formulaire -> picto
    "a": "montagne/pere-A-skis-petit.svg",    # séjour dans les Alpes : le père et ses skis
    "b": "base/mere-petit.svg",               # j'ai déjà mon logement : la mère, sans objet
    "e": "base/garcon-petit.svg",             # Pessah ou une fête : le garçon (kippa, tsitsit)
    "d": "base/pere-petit.svg",               # visite de Lyon : le père qui marche, canne
    "c": "montagne/van-petit.svg",            # transfert en van : le van (dessiné le 02/11, Moshé : plus de chiens)
    "f": "base/fille-petit.svg",              # autre chose : la fille
}
MARGE = 0.04

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for k, rel in PICTOS.items():
        s = io.open(os.path.join(SRC, rel), encoding="utf-8").read()
        pg.set_content(s)
        bb = pg.evaluate("() => { const g = document.querySelector('svg'); const r = g.getBBox(); return [r.x, r.y, r.width, r.height]; }")
        x, y, w, h = bb
        c = max(w, h) * (1 + 2 * MARGE)
        vb = f"{x + w / 2 - c / 2:.1f} {y + h / 2 - c / 2:.1f} {c:.1f} {c:.1f}"
        s = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', s, count=1)
        s = re.sub(r'\s(width|height)="[^"]*"', "", s.split(">", 1)[0], count=2) + ">" + s.split(">", 1)[1]
        nom = os.path.join(OUT, f"intention-{k}.svg")
        io.open(nom, "w", encoding="utf-8", newline="\n").write(s)
        print("ok", nom, vb)
    b.close()
