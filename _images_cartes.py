# -*- coding: utf-8 -*-
"""Photos des cartes .hub-carte (reproche du 14/10 : pédalo pour les Beth Habad, rue pour le mikvé, même piste de Megève
sur toutes les stations). Une photo par sujet, choisie à la main, licences dans CREDITS.md. Idempotent, 4 langues.
À relancer après toute régénération de _build_hub.py (avant _decor.py)."""
import os, re, io
ICI = os.path.dirname(os.path.abspath(__file__))
PHOTO = {
    # choix de Moshé du 15/10 (planche photos-hub-2026-10-15)
    'kosher-restaurants-lyon': 'stock/hub-kosher-restaurants-lyon.jpg',
    'kosher-shabbat-meals-catering-lyon': 'stock/hub-kosher-shabbat-meals-catering-lyon.jpg',
    'mikveh-lyon': 'stock/hub-mikveh-lyon.jpg',
    'where-to-stay-lyon-jewish-travellers': 'stock/hub-where-to-stay-lyon-jewish-travellers.jpg',
    'jewish-cemetery-lyon': 'stock/hub-jewish-cemetery-lyon.jpg',
    'alps': 'stock/hub-alps.jpg',
    'kosher-vacation-french-alps': 'stock/hub-kosher-vacation-french-alps.jpg',
    'flights-to-lyon': 'stock/hub-flights-to-lyon.jpg',
    'kosher-van-transfers': 'stock/hub-kosher-van-transfers.jpg',
    'kosher-val-thorens': 'stock/hub-kosher-val-thorens.jpg',
    'kosher-courchevel': 'stock/hub-kosher-courchevel.jpg',
    'kosher-megeve': 'stock/hub-kosher-megeve.jpg',
    'kosher-alpe-dhuez': 'stock/hub-kosher-alpe-dhuez.jpg',
    'kosher-les-deux-alpes': 'stock/hub-kosher-les-deux-alpes.jpg',
    'kosher-chalet-les-deux-alpes': 'chalet/wp-ext-bleu.jpg',   # vraie photo du chalet (Moshé, 15/10)
    'kosher-grenoble': 'stock/hub-kosher-grenoble.jpg',
    'kosher-annecy': 'stock/hub-kosher-annecy.jpg',
    'kosher-chamonix': 'stock/hub-kosher-chamonix.jpg',
    'kosher-les-arcs': 'stock/hub-kosher-les-arcs.jpg',
    'kosher-la-plagne': 'stock/hub-kosher-la-plagne.jpg',
    'kosher-val-disere': 'stock/hub-kosher-val-disere.jpg',
    'stopover': 'stock/hub-tours-stopover.jpg',
    'lyon-gateway-to-the-alps-kosher': 'stock/hub-lyon-gateway-to-the-alps-kosher.jpg',
    'rue-juiverie-lyon': 'stock/hub-rue-juiverie-lyon.jpg',
    'jewish-lyon-itinerary-2-days': 'stock/hub-jewish-lyon-itinerary-2-days.jpg',
    'jewish-travel-lyon-faq': 'stock/hub-jewish-travel-lyon-faq.jpg',
    'jewish-life-around-lyon': 'stock/hub-jewish-life-around-lyon.jpg',
    # 2e tour du 15/10
    'synagogues-lyon': 'stock/hub-synagogues-lyon.jpg',
    'shabbat-in-lyon': 'stock/hub-shabbat-in-lyon.jpg',
    'chabad-lyon': 'stock/hub-chabad-lyon.jpg',
    'kosher-services-french-alps': 'stock/hub-kosher-services-french-alps.jpg',
    'kosher-ski-holidays-french-alps': 'stock/hub-kosher-ski-holidays-french-alps.jpg',
    'grande-synagogue-lyon': 'stock/hub-grande-synagogue-lyon.jpg',
    'chrd-lyon': 'stock/hub-chrd-lyon.jpg',
    'is-lyon-safe-for-jewish-visitors': 'stock/hub-is-lyon-safe-for-jewish-visitors.jpg',
    'jewish-lyon': 'stock/hub-tours-jewish-lyon.jpg',
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
