# -*- coding: utf-8 -*-
"""Section « The chalet in pictures » des 32 fiches : les photos 1 et 4 sont en pleine largeur sur ordinateur depuis le 04/11
(lv-chalet.css, plus de trou blanc) ; leur attribut sizes passe de 40vw à 92vw pour que le navigateur charge une variante nette.
Les deux photos du duo gardent 40vw. Idempotent."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
n = 0
for f in sorted(glob.glob("kosher-*chalet-*/index.html") + glob.glob("*/kosher-*chalet-*/index.html")):
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<div class="lc-photos">(.*?)</div></div>', s, re.S)
    if not m: continue
    b = m.group(1); duo = re.search(r'<div class="lc-duo">.*?</div>', b, re.S)
    def fix(seg): return seg.replace('sizes="(min-width:900px) 40vw, 100vw"', 'sizes="(min-width:900px) 92vw, 100vw"')
    nb = fix(b[:duo.start()]) + b[duo.start():duo.end()] + fix(b[duo.end():])
    if nb != b: s = s[:m.start(1)] + nb + s[m.end(1):]; open(f, "w", encoding="utf-8").write(s); n += 1
print("fiches modifiées :", n)
