"""Lot 1 du 16/11/2026 : reparations (barre basse, #how, bloc final Lyon, cookies, debord tablette, champ date, hreflang, metas, sitemap).
Idempotent : relance = zero changement. Usage : python -X utf8 _lot1_1611_rep.py   (depuis n'importe quel dossier)."""
import os, re, glob

SITE = os.path.dirname(os.path.abspath(__file__))
CRLF = {}
def lire(p):
    s = open(os.path.join(SITE, p), encoding='utf8', newline='').read()
    CRLF[p] = '\r\n' in s
    return s.replace('\r\n', '\n')
def ecrire(p, s):
    if CRLF.get(p): s = s.replace('\n', '\r\n')
    open(os.path.join(SITE, p), 'w', encoding='utf8', newline='').write(s)
compte = {}
def note(k, n=1): compte[k] = compte.get(k, 0) + n

def pages():
    for p in glob.glob(SITE + '/**/index.html', recursive=True):
        rel = os.path.relpath(p, SITE).replace('\\', '/')
        if rel.startswith('_') or '/_' in rel: continue
        yield rel

# ---------- 1. barre basse : affichage grille reserve au telephone, icone bornee ----------
def r1():
    s = lire('lv.css')
    if '/*LOT1-1611-bb*/' not in s:
        L = s.split('\n')
        i = next(k for k, l in enumerate(L) if '.barre-basse{display:grid !important;grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;gap:8px' in l)
        assert '.barre-basse a{height:48px' in L[i + 1]
        L[i] = '@media (max-width:899.98px){/*LOT1-1611-bb*/\n' + L[i]
        L[i + 1] = L[i + 1] + '\n}'
        s = '\n'.join(L); ecrire('lv.css', s); note('1 lv.css barre-basse limitee a <900px')
    c = lire('styles.css')
    ancre = '.barre-basse{display:none}\n'
    ajout = '.barre-basse svg{width:20px;height:20px;max-width:24px;max-height:24px;flex:none}/*LOT1-1611-bb*/\n'
    if ajout not in c:
        assert ancre in c
        c = c.replace(ancre, ancre + ajout, 1); ecrire('styles.css', c); note('1 styles.css icone bornee')

# ---------- 9. debord tablette : le trait pointille des etapes depasse de 32 px ----------
def r9():
    c = lire('styles.css')
    v = '  .pratique-hero ~ .etapes ol{grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px}\n'
    n = '  .pratique-hero ~ .etapes ol{grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;overflow-x:clip}/*LOT1-1611*/\n'
    if n in c: return
    assert v in c
    ecrire('styles.css', c.replace(v, n, 1)); note('9 styles.css overflow-x:clip sur .etapes ol')

# ---------- cookies : texte court (js/mesure.js) ----------
COURT = {
    "'We use cookies to measure visits and the results of our ads.'": "'Cookies to measure visits and ads.'",
    "'Nous utilisons des cookies pour mesurer les visites et les résultats de nos annonces.'": "'Cookies de mesure des visites et annonces.'",
    "'Usamos cookies para medir las visitas y los resultados de nuestros anuncios.'": "'Cookies para medir visitas y anuncios.'",
    "'אנו משתמשים בעוגיות כדי למדוד ביקורים ותוצאות של הפרסומות שלנו.'": "'עוגיות למדידת ביקורים ופרסומות.'",
}
def r8_js():
    s = lire('js/mesure.js'); k = 0
    for a, b in COURT.items():
        if a in s: s = s.replace(a, b); k += 1
    if k: ecrire('js/mesure.js', s); note('8 js/mesure.js texte du bandeau raccourci (4 langues)', 1)

# ---------- bloc CSS unique en fin de lv.css ----------
P = 'html body.lv' + ''.join(':not(#r%d)' % i for i in range(1, 12))
P12 = 'html body.lv' + ''.join(':not(#r%d)' % i for i in range(1, 13))
Q16 = 'html body.lv.l4' + ''.join(':not(#q%d)' % i for i in range(1, 16))
BLOC = '''/* ===LOT1-1611=== lot 1 reparations du 16/11/2026 (_lot1_1611_rep.py) : defauts 6, 7, 8, 13 */
/* 6. « How it works » des pages Lyon (#how noir, lv.css l.1260 met color:#fff mais le -webkit-text-fill-color noir de la regle « 11. Comment ca marche » l.1128 l'emporte) : remplissage blanc ; chiffres en or brossé (A88F5E sur #111 = 6,1:1) */
%(L)s.l4-lyon #how :is(h2,h2 i,h2 em,.sous,p,li,li span,li p){color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important}
%(L)s.l4-lyon #how ol li b{color:#A88F5E !important;-webkit-text-fill-color:#A88F5E !important}
/* 7. bloc final des pages Lyon : titre noir, texte noir, lien WhatsApp noir souligne (le remplissage text-fill creme/jaune pale venait d'ailleurs) */
%(P)s :is(.cta-pratique,.ticket-zone .ticket) :is(h2,h2 i,h2 em,p,.fiche-note,small){color:#111111 !important;-webkit-text-fill-color:#111111 !important;opacity:1 !important}
%(P)s :is(.cta-pratique,.ticket-zone .ticket) a.wa{color:#111111 !important;-webkit-text-fill-color:#111111 !important;text-decoration:underline !important;text-underline-offset:3px !important;opacity:1 !important}
%(P)s :is(.cta-pratique,.ticket-zone .ticket) a.wa svg{fill:#111111 !important;color:#111111 !important}
/* 8. bandeau cookies sur telephone : une bande de 48 px, boutons de 44 px, ne recouvre ni le titre ni le bouton du premier ecran */
@media (max-width:899.98px){
%(Q)s .cb{box-sizing:border-box !important;display:flex !important;flex-wrap:nowrap !important;align-items:center !important;justify-content:space-between !important;gap:8px !important;height:48px !important;min-height:0 !important;padding:2px 12px !important;font-size:11px !important;line-height:1.2 !important}
%(Q)s .cb p{flex:1 1 auto !important;min-width:0 !important;margin:0 !important;font-size:11px !important;line-height:1.2 !important}
%(Q)s .cb-b{flex:none !important;width:auto !important;gap:6px !important}
%(Q)s .cb button{flex:none !important;min-width:0 !important;height:44px !important;min-height:44px !important;padding:0 12px !important;font-size:11px !important;letter-spacing:.08em !important}
}
/* 13. widget des visites de Lyon : dates sur toute la largeur (le champ de 113 px coupait « 12 al 15 de o ») */
@media (min-width:900px){%(P)s .hero-texte #chercheur .duo{grid-template-columns:minmax(0,1fr) !important;gap:10px !important}}
/* ===/LOT1-1611=== */
''' % {'P': P, 'Q': P12, 'L': Q16}

def bloc():
    s = lire('lv.css')
    a = s.find('/* ===LOT1-1611===')
    if a >= 0:
        b = s.find('/* ===/LOT1-1611=== */', a) + len('/* ===/LOT1-1611=== */\n')
        if s[a:b] == BLOC: return
        s = s[:a] + BLOC + s[b:]
    else:
        s = s.rstrip('\n') + '\n' + BLOC
    ecrire('lv.css', s); note('6/7/8/13 lv.css bloc LOT1-1611')

# ---------- 14. hreflang des 4 pages EN ----------
def r14():
    for slug in ('kosher-verbier', 'kosher-gstaad', 'kosher-davos', 'kosher-ski-anywhere'):
        for l in ('', 'fr/', 'es/', 'he/'):
            assert os.path.exists(os.path.join(SITE, l + slug, 'index.html')), l + slug
        p = slug + '/index.html'; h = lire(p)
        if 'hreflang' in h: continue
        B = 'https://mishpachatours.com/'
        blk = ('<link rel="alternate" hreflang="en" href="%(b)s%(s)s/">\n<link rel="alternate" hreflang="x-default" href="%(b)s%(s)s/">\n'
               '<link rel="alternate" hreflang="fr" href="%(b)sfr/%(s)s/">\n<link rel="alternate" hreflang="es" href="%(b)ses/%(s)s/">\n'
               '<link rel="alternate" hreflang="he" href="%(b)she/%(s)s/">\n') % {'b': B, 's': slug}
        m = re.search(r'<meta name="twitter:card"[^>]*>\n', h)
        assert m, p
        ecrire(p, h[:m.end()] + blk + h[m.end():]); note('14 hreflang ajoute (pages EN)')

# ---------- 15, 16. titres et descriptions ----------
def sub(p, pairs, cle):
    h = lire(p); o = h
    for a, b in pairs:
        h = h.replace(a, b)
    if h != o: ecrire(p, h); note(cle)

def r15_16():
    d_old = 'La Grande Synagogue de Lyon (1864) est fermée aux visiteurs hors Journées du patrimoine. Accès, horaires de prière et adresse.'
    d_new = 'Fermée au public hors Journées du patrimoine, la Grande Synagogue de Lyon (1864) s’ouvre à notre visite privée, sous réserve des horaires et de la sécurité.'
    sub('fr/grande-synagogue-lyon/index.html', [(d_old, d_new)], '15 description grande-synagogue FR')
    t_new = 'Quartier juif de Lyon : rue Juiverie, histoire et visite'
    dd_old = 'La rue Juiverie, ancien quartier juif de Lyon dans le Vieux Lyon, doit son nom à la communauté médiévale. Ce qui reste, ce qui a disparu, comment la visiter.'
    dd_new = 'Le quartier juif médiéval de Lyon et la rue Juiverie : ce qu’on y voit encore, ce qui a disparu, et la visite guidée privée avec une guide juive diplômée.'
    p = 'fr/rue-juiverie-lyon/index.html'; h = lire(p); o = h
    h = re.sub(r'(<title>)Rue Juiverie, le quartier juif de Lyon\s*:\s*histoire et visite \| Mishpacha Tours(</title>)', lambda m: m.group(1) + t_new + m.group(2), h)
    h = re.sub(r'(<meta property="og:title" content=")Rue Juiverie, le quartier juif de Lyon\s*:\s*histoire et visite \| Mishpacha Tours(")', lambda m: m.group(1) + t_new + m.group(2), h)
    h = h.replace(dd_old, dd_new)
    if h != o: ecrire(p, h); note('16 titre+description+og rue-juiverie FR')

# ---------- 17. sitemap ----------
def r17():
    s = lire('sitemap.xml')
    u = 'https://mishpachatours.com/he/kosher-chalet-megeve/'
    if u in s: return
    assert os.path.exists(os.path.join(SITE, 'he/kosher-chalet-megeve/index.html'))
    ref = '  <url><loc>https://mishpachatours.com/he/kosher-chalet-les-menuires/</loc>'
    i = s.index(ref); j = s.index('\n', i) + 1
    s = s[:j] + '  <url><loc>%s</loc><lastmod>2026-11-07</lastmod><priority>0.7</priority></url>\n' % u + s[j:]
    ecrire('sitemap.xml', s); note('17 sitemap : he/kosher-chalet-megeve')

for f in (r1, r9, r8_js, bloc, r14, r15_16, r17): f()
print('Reparations appliquees (0 = deja en place) :')
for k in sorted(compte): print(' ', k, compte[k])
if not compte: print('  aucune modification')
