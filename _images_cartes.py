# -*- coding: utf-8 -*-
"""Photos des cartes .hub-carte (reproche du 14/10 : pédalo pour les Beth Habad, rue pour le mikvé, même piste de Megève
sur toutes les stations). Une photo par sujet, choisie à la main, licences dans CREDITS.md. Idempotent, 4 langues.
À relancer après toute régénération de _build_hub.py (avant _decor.py)."""
import os, re, io
ICI = os.path.dirname(os.path.abspath(__file__))
PHOTO = {
    'chabad-lyon': 'stock/chabad-priere.jpg',
    'mikveh-lyon': 'stock/mikve.jpg',
    'kosher-val-thorens': 'stock/st-val-thorens.jpg',
    'kosher-courchevel': 'stock/st-courchevel.jpg',
    'kosher-megeve': 'stock/st-megeve.jpg',
    'kosher-alpe-dhuez': 'stock/st-alpe-dhuez.jpg',
    'kosher-les-deux-alpes': 'stock/st-les-deux-alpes.jpg',
    'kosher-chalet-les-deux-alpes': 'chalet/wp-ext-bleu.jpg',
    'kosher-van-transfers': 'stock/van-neige.jpg',
    'kosher-grenoble': 'stock/st-grenoble.jpg',
    'kosher-annecy': 'stock/annecy-lac.jpg',
    'kosher-chamonix': 'stock/st-chamonix.jpg',
    'kosher-les-arcs': 'stock/st-les-arcs.jpg',
    'kosher-la-plagne': 'stock/st-la-plagne.jpg',
    'kosher-val-disere': 'stock/st-val-disere.jpg',
}
RX = re.compile(r'(<a class="hub-carte" href="[^"]*?/?([a-z0-9-]+)/"[^>]*>\s*<div class="photo"><img src=")([^"]*?img/)([^"]+)(")')
total = 0
for root, d, f in os.walk(ICI):
    if any(x in root for x in ('_candidats', '.git', '_pages')):
        continue
    for n in f:
        if n != 'index.html':
            continue
        p = os.path.join(root, n)
        s = io.open(p, encoding='utf8', newline='').read()
        def sub(m):
            new = PHOTO.get(m.group(2))
            return m.group(0) if not new else m.group(1) + m.group(3) + new + m.group(5)
        t, k = RX.subn(sub, s)
        if t != s:
            io.open(p, 'w', encoding='utf8', newline='').write(t)
            total += 1
print('pages modifiées :', total)
