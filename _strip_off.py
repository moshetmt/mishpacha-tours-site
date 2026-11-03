# -*- coding: utf-8 -*-
"""Bandeau du haut retiré (décision Moshé du 03/11) : la barre `.strip` (« Strictly kosher stays in the Alps. Describe your
stay. » et ses versions FR, ES, HE) perd son texte et son lien. Il ne reste que le ב״ה, dans un `<span class="bh-haut">`
placé au même endroit du HTML ; le CSS (bloc BANDEAU-OFF de lv.css) le pose en haut à droite, comme avant. Sans élément
`.strip`, le script anim.js ne bascule plus `strip-vis` (plus de barre fixe sur téléphone après 220 px de défilement).
Idempotent : une page déjà traitée n'a plus de `.strip`, le script la saute. Aucun autre octet de la page ne bouge."""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
RX = re.compile(r'<div class="strip"><span class="bh" lang="he">ב״ה</span>.*?</div>', re.S)
NEUF = '<span class="bh-haut" lang="he">ב״ה</span>'
n_mod = n_deja = n_sans = 0
for p in sorted(glob.glob("**/index.html", recursive=True)):
    s = io.open(p, encoding="utf-8").read()
    if 'class="bh-haut"' in s and 'class="strip"' not in s:
        n_deja += 1; continue
    t, k = RX.subn(NEUF, s, count=1)
    if not k:
        n_sans += 1; continue
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n_mod += 1
print("bandeau retiré :", n_mod, "pages modifiées,", n_deja, "déjà faites,", n_sans, "sans bandeau")
