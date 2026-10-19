# -*- coding: utf-8 -*-
"""Retouches de la bannière 3 après les 13 vocaux de Mendel du 15/10 soir (02-meetings/2026-10-15-audios-mendel-retours-site.md).
Idempotent, à lancer après _lead.py :
 1. « Personnaliser mon séjour » (formulaire, pré-rempli) devient le bouton principal, WhatsApp passe en lien dessous ;
 2. la puce « Strictly kosher » dit aussi « Chalav Yisrael » (tout ce que l'équipe sert l'est : argument, plus un choix) ;
 3. la page hiver et /alps/ prennent la photo de neige éclatante du chalet (wp-soleil) à la place de la piste brunâtre."""
import io, os, re
from _lead import PAGES, STATIONS
ICI = os.path.dirname(os.path.abspath(__file__))
LANGS = ('en', 'fr', 'es', 'he')
BTN = {'en': 'Plan my trip', 'fr': 'Personnaliser mon séjour', 'es': 'Preparar mi viaje', 'he': 'לתכנן את הטיול'}
BTN_VAN = {'en': 'Request a van', 'fr': 'Demander un van', 'es': 'Pedir una furgoneta', 'he': 'להזמין ואן'}
WA = {'en': 'Or message us on WhatsApp', 'fr': 'Ou écrivez-nous sur WhatsApp', 'es': 'O escríbanos por WhatsApp', 'he': 'או כתבו לנו בוואטסאפ'}
KOSHER = {'en': ('Strictly kosher', 'Strictly kosher, Chalav Yisrael'), 'fr': ('Strictement casher', "Strictement casher, 'Halav Yisrael"),
          'es': ('Estrictamente kosher', 'Estrictamente kosher, Chalav Yisrael'), 'he': ('שומר כשרות', 'שומר כשרות, חלב ישראל')}
PHOTO_HIVER = {'stock/alpes-ski.jpg': 'chalet/wp-soleil.jpg'}
CSS = ('/* LEAD retouches 15/10 : formulaire d\'abord, WhatsApp en lien */\n'
       '.lead3-btns{display:flex;flex-wrap:wrap;align-items:center;gap:12px 22px;margin-top:26px}.lead-hero3 .lead3-btns .btn-hero{margin-top:0}'
       '.lead3-wa{display:inline-flex;align-items:center;gap:8px;color:#FFFAED;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:4px}'
       '.lead3-wa svg{width:20px;height:20px;fill:currentColor}\n')
RX_BTN = re.compile(r'<a class="btn-hero" href="(https://wa\.me/[^"]*)" rel="noopener"><svg><use href="#wa"/></svg>([^<]*)</a>')


def lien_plan(slug, typ, lang):
    base = '/plan-your-trip/' if lang == 'en' else f'/{lang}/plan-your-trip/'
    if typ == 'van': return base + '?i=c'
    if slug in STATIONS: return base + '?i=a&lieu=' + STATIONS[slug][1]['en'].replace(' ', '%20').replace("'", '%27')
    if typ == 'chalet': return base + '?i=a&lieu=Les%20Deux%20Alpes'
    return base + '?i=a'


n = 0
for slug, (photo, typ, voyage) in PAGES.items():
    for lang in LANGS:
        p = os.path.join(ICI, *([slug] if lang == 'en' else [lang, slug]), 'index.html')
        if not os.path.exists(p): continue
        s = io.open(p, encoding='utf8', newline='').read()
        if 'lead-hero3' not in s: continue
        s0 = s
        # 1. boutons
        if 'lead3-btns' not in s:
            txt = (BTN_VAN if typ == 'van' else BTN)[lang]
            s = RX_BTN.sub(lambda m: (f'<div class="lead3-btns"><a class="btn-hero" href="{lien_plan(slug, typ, lang)}">{txt}</a>'
                                      f'<a class="lead3-wa" href="{m.group(1)}" rel="noopener"><svg><use href="#wa"/></svg>{WA[lang]}</a></div>'), s, count=1)
        # 2. puce Chalav Yisrael (pas sur la page van) ; sans effet depuis le 19/10, les pastilles ne sont plus dans la bannière
        if typ != 'van' and '<ul class="lead-puces">' in s:
            a, b = KOSHER[lang]
            if f'<li>{b}</li>' not in s:
                s = re.sub(r'(<ul class="lead-puces">.*?)<li>' + re.escape(a) + '</li>', lambda m: m.group(1) + f'<li>{b}</li>', s, count=1, flags=re.S)
        # 3. photo d'hiver
        for old, new in PHOTO_HIVER.items():
            if photo == old and f'/img/{old}' in s:
                s = s.replace(f'<img src="/img/{old}" alt="" width="1600" height="1067" fetchpriority="high">', f'<img src="/img/{new}" alt="" width="1600" height="1600" fetchpriority="high">', 1)
                s = re.sub(rf'<img src="/img/{re.escape(old)}" alt="" width="\d+" height="\d+" fetchpriority="high">', f'<img src="/img/{new}" alt="" width="1600" height="1600" fetchpriority="high">', s, count=1)
        if s != s0:
            io.open(p, 'w', encoding='utf8', newline='').write(s); n += 1
css_p = os.path.join(ICI, 'styles.css'); css = io.open(css_p, encoding='utf8', newline='').read()
if '.lead3-btns' not in css:
    io.open(css_p, 'w', encoding='utf8', newline='').write(css.rstrip('\n') + '\n' + CSS)
print(n, 'pages retouchées')
