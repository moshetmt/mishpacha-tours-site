# -*- coding: utf-8 -*-
"""Poses du hassid du logo (Gemini sur le picto, 14/10) vectorisées en SVG par pypotrace, en trois couleurs
(noir, vert #2D5132, crème #FFFAED), dans img/hassid/. Usage : python _hassid_poses.py [numéros, ex. 1 4 7 ; défaut : toutes]."""
import os, sys, io
import numpy as np
from PIL import Image
import potrace
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, '_candidats', 'hassid-poses-2026-10-14')
OUT = os.path.join(ICI, 'img', 'hassid'); os.makedirs(OUT, exist_ok=True)
NOMS = {1: 'danse', 2: 'chant', 3: 'repas', 4: 'ski', 5: 'priere', 6: 'saut', 7: 'van', 8: 'valise'}
COULEURS = {'noir': '#1C1B1F', 'vert': '#2D5132', 'creme': '#FFFAED'}
choix = [int(x) for x in sys.argv[1:]] or list(NOMS)

def trace(png):
    im = Image.open(png).convert('L')
    a = np.array(im) < 140                      # noir = forme
    ys, xs = np.where(a)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    m = 24
    a = a[max(0, y0 - m):y1 + m, max(0, x0 - m):x1 + m]
    h, w = a.shape
    bm = potrace.Bitmap(a)
    path = bm.trace(turdsize=12, alphamax=1.0, opttolerance=0.2)
    d = []
    for c in path:
        s = c.start_point
        d.append(f'M{s.x:.1f} {s.y:.1f}')
        for seg in c:
            if seg.is_corner:
                d.append(f'L{seg.c.x:.1f} {seg.c.y:.1f} L{seg.end_point.x:.1f} {seg.end_point.y:.1f}')
            else:
                d.append(f'C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}')
        d.append('Z')
    return w, h, ' '.join(d)

for n in choix:
    w, h, d = trace(os.path.join(SRC, f'pose-{n}.png'))
    for cle, hexa in COULEURS.items():
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><path fill="{hexa}" fill-rule="evenodd" d="{d}"/></svg>'
        io.open(os.path.join(OUT, f'hassid-{NOMS[n]}-{cle}.svg'), 'w', encoding='utf8').write(svg)
    print(NOMS[n], f'{w}x{h}', len(d) // 1000, 'k')
