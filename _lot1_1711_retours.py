"""Retours de Moshé du 17/11 sur la préversion du lot 1. Idempotent. À lancer APRÈS _lot1_1611_entete.py.
1. ב״ה : sorti de l'en-tête (il ne suit plus au défilement), posé en haut à droite de la page sous l'en-tête, en gris.
2. Cartes photo de l'accueil (.reve) : titre dans la photo, sur la ligne de la flèche.
Usage : python -X utf8 _lot1_1711_retours.py
"""
import re, glob, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
EXCLUS = ('espace' + os.sep, 'maquette-chalet-lv' + os.sep)

RE_BH_HEADER = re.compile(r'\s*<span class="mt-bh"[^>]*>[^<]*</span>(?=\s*</header>)')
RE_BH_PAGE = re.compile(r'\n?<span class="mt-bh-page[^"]*"[^>]*>[^<]*</span>')
RE_HEADER = re.compile(r'<header class="mt-tete"[^>]*>.*?</header>', re.S)


def page(t):
    m = RE_HEADER.search(t)
    if not m:
        return t
    h = m.group(0)
    fond = 'photo' if 'data-fond="photo"' in h else 'plein'
    h2 = RE_BH_HEADER.sub('', h)
    t = t[:m.start()] + h2 + t[m.end():]
    t = RE_BH_PAGE.sub('', t)
    fin = t.find('</header>', m.start()) + len('</header>')
    span = f'\n<span class="mt-bh-page mt-bh-{fond}" lang="he" dir="rtl" aria-hidden="true">ב״ה</span>'
    return t[:fin] + span + t[fin:]


CSS_ENTETE = r"""
/* LOT1-1711-BH (Moshé 17/11) : le ב״ה est posé une fois, tout en haut à droite de la page, comme en tête d'une feuille ; il ne suit pas le défilement ; gris (pas un bouton) */
.mt-bh-page{position:absolute;top:4px;right:16px;z-index:70;font:400 11px/11px Heebo,"Noto Serif Hebrew",sans-serif;letter-spacing:0;direction:rtl;unicode-bidi:isolate;white-space:nowrap;pointer-events:none;user-select:none;color:#A6A6A6}
@media (min-width:768px){.mt-bh-page{top:6px;right:10px;font-size:12px;line-height:12px}}
@media print{.mt-bh-page{color:#555}}
/* /LOT1-1711-BH */
"""

CSS_LV = r"""
/* LOT1-1711-CARTES (Moshé 17/11) : cartes photo de l'accueil = bande blanche en bas de la photo, titre noir et flèche alignés dessus ; fiche chalet = air entre les boutons et le texte */
html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figure{padding:0 !important;overflow:hidden !important;background:#FFFFFF !important}
html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figure::before{content:none !important;display:none !important}
html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figcaption{position:absolute !important;inset:auto 0 0 0 !important;z-index:2;height:auto !important;min-height:60px !important;box-sizing:border-box !important;display:flex !important;align-items:center !important;padding:10px 0 !important;padding-inline:16px 68px !important;margin:0 !important;background:#FFFFFF !important;color:#111111 !important;-webkit-text-fill-color:#111111 !important;font:400 13px/1.3 'Jost',system-ui,sans-serif !important;letter-spacing:.08em !important;text-transform:uppercase !important;text-align:start !important;white-space:normal !important;overflow:visible !important}
html[dir="rtl"] body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figcaption{letter-spacing:0 !important;font:400 16px/1.3 Heebo,system-ui,sans-serif !important}
html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figure::after{z-index:3;width:40px !important;height:40px !important;bottom:10px !important;inset-inline-end:12px !important;top:auto !important;box-shadow:none !important}
@media (min-width:900px){html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figcaption{font-size:12px !important;min-height:56px !important;padding-inline:14px 62px !important}html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .reve-grille figure::after{bottom:8px !important;inset-inline-end:10px !important}}
html body.lv:not(#x1):not(#x2):not(#x3):not(#x4):not(#x5):not(#x6):not(#x7):not(#x8):not(#x9):not(#x10):not(#x11):not(#x12):not(#x13):not(#x14):not(#x15):not(#x16) .lc-desc{margin-top:28px !important}
/* /LOT1-1711-CARTES */
"""


def bloc(fichier, marque, css):
    t = open(fichier, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    css = css.strip('\n').replace('\n', nl)
    r = re.compile(r'(\r?\n)*/\* ' + marque + r' .*?/\* /' + marque + r' \*/(\r?\n)?', re.S)
    base = r.sub('', t).rstrip('\r\n')
    neuf = base + nl + css + nl
    if neuf != t:
        open(fichier, 'w', encoding='utf-8', newline='').write(neuf)
        return 1
    return 0


n = 0
for f in glob.glob('**/index.html', recursive=True):
    if f.startswith('_') or (os.sep + '_') in f or f.startswith(EXCLUS):
        continue
    t = open(f, encoding='utf-8', newline='').read()
    t2 = page(t)
    if t2 != t:
        open(f, 'w', encoding='utf-8', newline='').write(t2)
        n += 1
print('pages modifiées (ב״ה) :', n)
print('entete.css modifié :', bloc('entete.css', 'LOT1-1711-BH', CSS_ENTETE))
print('lv.css modifié :', bloc('lv.css', 'LOT1-1711-CARTES', CSS_LV))
