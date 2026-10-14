# -*- coding: utf-8 -*-
"""Retire les mosaïques de photos posées en bas de page (opérateur, 14/10 : « ça fait vraiment dégueulasse, ça fait Claude »).
Garde la galerie de la page chalet, placée sous la bannière (photos du produit). Idempotent, 4 langues.
À relancer après toute régénération par _build_guide.py, _build_pratique.py, _build_tours.py ou _patch_pratique.py."""
import os, io, re
ICI = os.path.dirname(os.path.abspath(__file__))
GARDER = ('kosher-chalet-les-deux-alpes',)
TAG = re.compile(r'<(/?)div\b[^>]*>')

def bloc(s, i):
    """Renvoie (début, fin) du <div> parent .ss.wrap de la mosaïque ouverte en i, ou de la mosaïque seule."""
    deb = s.rfind('<div', 0, i)
    j = s.rfind('<div class="ss wrap">', 0, i)
    if j != -1 and s[j + len('<div class="ss wrap">'):i].strip() == '':
        deb = j
    else:
        deb = i
    prof = 0
    for m in TAG.finditer(s, deb):
        prof += -1 if m.group(1) else 1
        if prof == 0:
            return deb, m.end()
    return None

total = 0
for root, d, f in os.walk(ICI):
    if any(x in root for x in ('_candidats', '.git', '_pages')) or any(g in root for g in GARDER):
        continue
    for n in f:
        if n != 'index.html':
            continue
        p = os.path.join(root, n)
        s = io.open(p, encoding='utf8', newline='').read()
        t = s
        while True:
            i = t.find('<div class="mosaique')
            if i == -1:
                break
            b = bloc(t, i)
            if not b:
                break
            t = t[:b[0]] + t[b[1]:]
        if t != s:
            io.open(p, 'w', encoding='utf8', newline='').write(t)
            total += 1
print('pages nettoyées :', total)
