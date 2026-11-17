#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lot 1 du 16/11/2026 : un seul en-tete (composant mt-tete), deux habillages (mt, wp).

Ce que le script fait, et seulement cela :
  1. remplace dans chaque index.html le triplet  span.bh-haut + header.nav + div.panneau
     par un bloc neuf  <!--MT-ENTETE--> ... <!--/MT-ENTETE-->  (en-tete, panneau du burger, ב״ה dans l'en-tete) ;
  2. pose dans <head> la feuille  /entete.css  (en dernier) et le script  /js/entete.js ;
  3. retire de l'script en ligne de chaque page les 3 instructions qui pilotaient l'ancien burger ;
  4. adapte  js/anim.js  (deux selecteurs de l'ancien bouton Plan your trip).

Idempotent : le bloc existant est relu (formes ancienne ou neuve) puis regenere ; deux passes de suite, zero changement.
Source unique par langue : la page d'accueil de la langue (liens de navigation, texte du panneau, 15 chalets du menu).
Ce qui est propre a chaque page (liens du selecteur de langue, lien et texte du bouton, aria-label, lien WhatsApp du
panneau, habillage) est relu dans la page et reporte tel quel. Les liens wa.me ne sont jamais reecrits.

Usage :  python -X utf8 _lot1_1611_entete.py [--dry]
"""
import html as H
import re
import sys
from collections import Counter
from pathlib import Path

import lxml.html

ROOT = Path(__file__).resolve().parent
DRY = '--dry' in sys.argv
EXCLU = ('espace', 'maquette-chalet-lv')
LANGS = ('en', 'fr', 'es', 'he')
PREFIX = {'en': '', 'fr': 'fr/', 'es': 'es/', 'he': 'he/'}
FLAG = {'EN': 'gb', 'FR': 'fr', 'ES': 'es', 'HE': 'il', 'עב': 'il'}
CODE_HE = 'עב'
VER = '1611'

MARK_A, MARK_B = '<!--MT-ENTETE-->', '<!--/MT-ENTETE-->'
LINK_TAG = '<link rel="stylesheet" href="/entete.css?v=%s">' % VER
SCRIPT_TAG = '<script src="/js/entete.js?v=%s" defer></script>' % VER
HERO_SEL = '.ac-hero,.lv-hero-photo,main>section.hero:not(.lead-hero3-illus)'

OLD_MENU_JS = [
    "const m=document.querySelector('.menu'),pa=document.getElementById('panneau');\n",
    "m.addEventListener('click',()=>{const o=pa.hidden;pa.style.top=document.querySelector('.nav').getBoundingClientRect().bottom+'px';pa.hidden=!o;m.setAttribute('aria-expanded',o);document.body.classList.toggle('menu-ouvert',o)});\n",
    "pa.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{pa.hidden=true;m.setAttribute('aria-expanded',false);document.body.classList.remove('menu-ouvert')}));\n",
]

WP_ANIM = ('<script>try{if(!sessionStorage.getItem("wpEntete")){sessionStorage.setItem("wpEntete","1");'
           'document.documentElement.classList.add("wp-anim")}}catch(e){}</script>')


EN_LOGO = 'Mishpacha Tours, Jewish Tours of Lyon'
LANG_FIX = {
    'contact-quick/index.html': {'en': '/contact-quick/', 'fr': '/fr/plan-your-trip/', 'es': '/es/plan-your-trip/', 'he': '/he/plan-your-trip/'},
    'contact-quick/thanks/index.html': {'en': '/', 'fr': '/fr/', 'es': '/es/', 'he': '/he/'},
}


def e(s):
    return H.escape(s or '', quote=False)


def a(s):
    return H.escape(s or '', quote=True)


def txt(el):
    return re.sub(r'\s+', ' ', el.text_content()).strip()


# ------------------------------------------------------------------ pages
def lister_pages():
    out = []
    for p in sorted(ROOT.rglob('index.html')):
        rel = p.relative_to(ROOT).parts
        if rel[0].startswith('_') or rel[0] in EXCLU:
            continue
        out.append(p)
    return out


def langue_de(p):
    rel = p.relative_to(ROOT).parts
    return rel[0] if rel[0] in ('fr', 'es', 'he') else 'en'


# ------------------------------------------------------------------ localiser le bloc
def trouver_bloc(s):
    """Retourne (debut, fin, forme) du bloc d'en-tete dans le HTML s."""
    i = s.find(MARK_A)
    if i >= 0:
        j = s.find(MARK_B, i)
        assert j > 0, 'marqueur de fin absent'
        return i, j + len(MARK_B), 'neuf'
    h0 = s.find('<header class="nav"')
    assert h0 >= 0, 'header.nav absent'
    h1 = s.find('</header>', h0) + len('</header>')
    # ב״ה juste avant ?
    m = re.search(r'<span class="bh-haut"[^>]*>[^<]*</span>\s*$', s[:h0])
    debut = m.start() if m else h0
    entre = s[h1:s.find('<div class="panneau"', h1)]
    assert entre.strip() == '', 'contenu inattendu entre header et panneau : %r' % entre[:80]
    p0 = s.find('<div class="panneau"', h1)
    assert p0 >= 0, 'panneau absent'
    depth, pos = 0, p0
    for m in re.finditer(r'<div\b|</div>', s[p0:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            pos = p0 + m.end()
            break
    return debut, pos, 'ancien'


# ------------------------------------------------------------------ extraction
def lire_bloc(region):
    root = lxml.html.fragment_fromstring(region, create_parent='div')
    d = {}
    hdr = root.cssselect('header')[0]
    d['wp'] = ('wp-entete' in region) if not hdr.get('data-habillage') else hdr.get('data-habillage') == 'wp'
    logo = hdr.cssselect('a.logo, a.mt-logo')[0]
    d['logo_href'], d['logo_label'] = logo.get('href'), logo.get('aria-label')
    nav = hdr.cssselect('nav.liens, nav.mt-nav')[0]
    d['nav_label'] = nav.get('aria-label')
    # liens simples du nav (hors chalets, hors boutons)
    d['liens'] = [(x.get('href'), txt(x)) for x in nav.xpath('./a')
                  if not ({'nav-cta', 'mt-cta', 'nav-cta-wa'} & set((x.get('class') or '').split()))]
    ch = nav.cssselect('div.nav-ch, div.mt-ch')[0]
    chl = ch.cssselect('a.nav-ch-lien, a.mt-ch-lien')[0]
    d['ch_href'], d['ch_label'] = chl.get('href'), txt(chl)
    d['ch_items'] = []
    for v in ch.cssselect('a.nav-ch-v, a.mt-ch-v'):
        img = v.cssselect('img')[0]
        b = v.cssselect('b, span.mt-ch-nom')[0]
        d['ch_items'].append(dict(href=v.get('href'), src=img.get('src'), w=img.get('width'), h=img.get('height'),
                                  nom=txt(b), sous=re.sub(r'\s+', ' ', (b.tail or '')).strip()))
    tous = ch.cssselect('a.nav-ch-tous, a.mt-ch-tous')[0]
    d['ch_tous'] = (tous.get('href'), txt(tous))
    cta = hdr.cssselect('a.nav-cta:not(.nav-cta-wa), a.mt-cta:not(.mt-cta-wa)')[0]
    d['cta'] = (cta.get('href'), txt(cta))
    wa2 = hdr.cssselect('a.nav-cta-wa, a.mt-cta-wa')
    d['wa2'] = (wa2[0].get('href'), txt(wa2[0])) if wa2 else None
    lg = hdr.cssselect('details.langue, details.mt-langue')[0]
    sm = lg.cssselect('summary')[0]
    d['lang_label'] = sm.get('aria-label')
    d['langs'] = []
    for li in lg.cssselect('li > a'):
        nom_el = li.cssselect('span.mt-nom')
        d['langs'].append(dict(href=li.get('href'), lang=li.get('lang'), nom=txt(nom_el[0]) if nom_el else txt(li),
                               cur=li.get('aria-current') == 'true'))
    bu = hdr.cssselect('button.menu, button.mt-burger')[0]
    d['burger_label'] = bu.get('aria-label')
    pan = root.cssselect('div#panneau')[0]
    d['pan_nav_label'] = pan.cssselect('nav')[0].get('aria-label')
    d['pan_items'] = []
    for x in pan.cssselect('nav > a'):
        if {'nav-cta', 'mt-cta', 'mt-panneau-cta'} & set((x.get('class') or '').split()):
            continue
        sm_ = x.cssselect('small')
        d['pan_items'].append((x.get('href'), re.sub(r'\s+', ' ', x.text or '').strip(), txt(sm_[0]) if sm_ else ''))
    pcta = pan.cssselect('nav > a.nav-cta, a.mt-panneau-cta')
    d['pan_cta'] = (pcta[0].get('href'), txt(pcta[0])) if pcta else d['cta']
    wa = pan.cssselect('a.panneau-wa, a.mt-panneau-wa')[0]
    d['pan_wa'] = (wa.get('href'), txt(wa), wa.get('rel'))
    pws = pan.cssselect('a.panneau-wa, a.mt-panneau-wa')
    if not d['wa2'] and len(pws) > 1:          # forme neuve : le second lien WhatsApp (hebreu) vit dans le panneau
        d['wa2'] = (pws[1].get('href'), txt(pws[1]))
    mail = pan.cssselect('a[href^="mailto:"]')[0]
    d['pan_mail'] = (mail.get('href'), txt(mail))
    note = pan.cssselect('.panneau-bas > span, .mt-panneau-bas > span')[0]
    d['pan_note'] = txt(note)
    bh = root.cssselect('span.bh-haut, span.mt-bh, span.mt-bh-page')[0]  # mt-bh-page : posé hors de l'en-tête par _lot1_1711_retours.py
    d['bh'] = txt(bh)
    # 4 pages (davos, gstaad, ski-anywhere, verbier) : le selecteur de l'en-tete renvoyait aux accueils, alors que les pastilles de langue
    # du panneau (supprimees ici, le selecteur est dans l'en-tete a toutes les largeurs) pointaient vers la meme page dans l'autre langue.
    # On reprend alors les liens des pastilles pour le selecteur : aucun lien de langue vers la meme page n'est perdu.
    pills = [(x.get('href'), x.get('aria-current') == 'true') for x in pan.cssselect('div.panneau-langs a')]
    d['langfix'] = False
    homes = {'/', '/fr/', '/es/', '/he/'}
    if len(pills) == 4 and len(d['langs']) == 4 and all(l['href'] in homes for l in d['langs']) and not all(h in homes for h, _ in pills):
        for l, (h, c) in zip(d['langs'], pills):
            l['href'], l['cur'] = h, c
        d['langfix'] = True
    return d


# ------------------------------------------------------------------ rendu
def rendre_ch_menu(src):
    out = []
    for v in src['ch_items']:
        out.append('<a class="mt-ch-v" href="%s"><img src="%s" alt="" width="%s" height="%s" loading="lazy">'
                   '<span><span class="mt-ch-nom">%s</span>%s</span></a>' % (a(v['href']), a(v['src']), a(v['w']), a(v['h']), e(v['nom']), e(v['sous'])))
    out.append('<a class="mt-ch-tous" href="%s">%s</a>' % (a(src['ch_tous'][0]), e(src['ch_tous'][1])))
    return ''.join(out)


def code_de(l):
    return {'en': 'EN', 'fr': 'FR', 'es': 'ES', 'he': CODE_HE}[l]


def rendre(d, src, lang, fond):
    wp = d['wp']
    lg_items = []
    for it in d['langs']:
        l = (it['lang'] or 'en')
        l = 'en' if l not in ('fr', 'es', 'he') else l
        code = code_de(l)
        attrs = ' hreflang="%s"' % l
        if it['lang']:
            attrs += ' lang="%s"' % a(it['lang'])
        if it['lang'] == 'he':
            attrs += ' dir="rtl"'
        if it['cur']:
            attrs += ' aria-current="true"'
        lg_items.append('<li><a href="%s"%s><span class="mt-drapeau mt-fl-%s" aria-hidden="true"></span>'
                        '<span class="mt-code">%s</span><span class="mt-nom">%s</span></a></li>' % (a(it['href']), attrs, FLAG[code], e(code), e(it['nom'])))
    cur = next((it for it in d['langs'] if it['cur']), d['langs'][0])
    cur_l = cur['lang'] if cur['lang'] in ('fr', 'es', 'he') else 'en'
    liens = ''.join('<a class="mt-lien" href="%s">%s</a>' % (a(h), e(t)) for h, t in src['liens'])
    # etiquettes pour lecteurs d'ecran : ni anglais ni libelle neuf. Le libelle anglais generique du logo cede la place au libelle de l'accueil
    # de la langue ; en hebreu, le resume de langue garde les seuls mots hebreux existants (code et nom de la langue).
    logo_label = d['logo_label']
    if lang != 'en' and logo_label == EN_LOGO:
        logo_label = src['logo_label']
    lang_label = d['lang_label']
    if lang == 'he':
        lang_label = '%s, %s' % (code_de('he'), cur['nom'])
    marque = ('<a class="mt-logo" href="%s" aria-label="%s"><img class="forme mt-picto" src="/img/picto-hassid.svg" alt="" width="68" height="95">'
              '<span class="mt-mot" translate="no">mishpacha tours</span></a>' % (a(d['logo_href']), a(logo_label)))
    if wp:
        marque += ('<div class="mt-wp"><img class="mt-wp-fl" src="/img/wp-flocon-brosse-clair.svg" alt="" width="48" height="48">'
                   '<span class="mt-wp-txt"><span class="mt-wp-mot" role="img" aria-label="Winter Prestige"></span>'
                   '<span class="mt-wp-pw" translate="no">POWERED BY <span class="mt-wp-pw-m">mishpacha tours</span></span></span></div>')
    pan_items = ''.join('<a href="%s">%s<small>%s</small></a>' % (a(h), e(t), e(s_)) for h, t, s_ in src['pan_items'])
    # second bouton WhatsApp des pages hebreu (ancien a.nav-cta-wa) : il garde sa fonction. En-tete en mode large,
    # panneau en mode compact (le lien du panneau est deja le meme ; s'il differe, le second lien entre aussi dans le panneau).
    wa2_html = ''   # le second bouton WhatsApp des pages hebreu n'existe ni dans les autres langues ni en ligne : il ne vit que dans le panneau
    header = (
        '<header class="mt-tete" data-habillage="%s" data-fond="%s">\n'
        '  <div class="mt-corps">\n'
        '    <div class="mt-marque">%s</div>\n'
        '    <nav class="mt-nav" aria-label="%s">\n'
        '      <div class="mt-ch"><a class="mt-lien mt-ch-lien" href="%s" aria-haspopup="true" aria-expanded="false">%s</a>'
        '<div class="mt-ch-menu">%s</div></div>\n'
        '      %s\n'
        '    </nav>\n'
        '    <a class="mt-cta" href="%s">%s</a>%s\n'
        '    <details class="mt-langue"><summary aria-label="%s"><span class="mt-code">%s</span></summary><ul>%s</ul></details>\n'
        '    <button class="mt-burger" type="button" aria-label="%s" aria-expanded="false" aria-controls="panneau">'
        '<span></span><span></span><span></span></button>\n'
        '  </div>\n'
        '  <span class="mt-bh" lang="he" dir="rtl">%s</span>\n'
        '</header>'
    ) % ('wp' if wp else 'mt', fond, marque, a(d['nav_label']), a(src['ch_href']), e(src['ch_label']), rendre_ch_menu(src), liens,
         a(d['cta'][0]), e(d['cta'][1]), wa2_html, a(lang_label), e(code_de(cur_l)), ''.join(lg_items), a(d['burger_label']), e(d['bh']))
    wa_href, wa_txt, wa_rel = d['pan_wa']
    wa_label = src['pan_wa'][1]
    wa2_pan = ''
    if d['wa2'] and d['wa2'][0] != wa_href:
        wa2_pan = '\n  <a class="mt-panneau-wa" href="%s" rel="noopener"><svg aria-hidden="true"><use href="#wa"/></svg>%s</a>' % (a(d['wa2'][0]), e(d['wa2'][1]))
    panneau = (
        '<div class="mt-panneau" id="panneau" hidden>\n'
        '  <nav aria-label="%s">%s</nav>\n'
        '  <a class="mt-cta mt-panneau-cta" href="%s">%s</a>\n'
        '  <a class="mt-panneau-wa" href="%s"%s><svg aria-hidden="true"><use href="#wa"/></svg>%s</a>%s\n'
        '  <p class="mt-panneau-bas"><a href="%s">%s</a><span>%s</span></p>\n'
        '</div>'
    ) % (a(d['pan_nav_label']), pan_items, a(d['cta'][0]), e(d['cta'][1]), a(wa_href),
         (' rel="%s"' % a(wa_rel)) if wa_rel else '', e(wa_label), wa2_pan, a(d['pan_mail'][0]), e(d['pan_mail'][1]), e(src['pan_note']))
    return '%s\n%s%s\n%s\n%s' % (MARK_A, (WP_ANIM + '\n') if wp else '', header, panneau, MARK_B)


# ------------------------------------------------------------------ traitement d'une page
def traiter(p, SRC, stats, anomalies):
    s = p.read_text(encoding='utf8')
    orig = s
    lang = langue_de(p)
    i, j, forme = trouver_bloc(s)
    region = s[i:j]
    d = lire_bloc(region)
    # contact-quick : le selecteur renvoyait partout vers /merci/ (bug d'avant). Il pointe vers la page equivalente de chaque langue.
    rel = p.relative_to(ROOT).as_posix()
    if rel in LANG_FIX:
        for it in d['langs']:
            l = it['lang'] if it['lang'] in ('fr', 'es', 'he') else 'en'
            it['href'] = LANG_FIX[rel][l]
    # ב״ה restant ailleurs que dans le bloc : retire (jamais de doublon)
    reste = re.findall(r'<span class="bh-haut"[^>]*>[^<]*</span>', s[:i] + s[j:])
    if reste:
        anomalies.append((str(p.relative_to(ROOT)), 'bh-haut hors bloc retire'))
        s = s[:i] + s[j:]
        s = re.sub(r'<span class="bh-haut"[^>]*>[^<]*</span>\s*', '', s)
        i, j, forme = trouver_bloc(s) if MARK_A in s else (i, j, forme)
    doc = lxml.html.fromstring(orig.encode('utf8'))
    fond = 'photo' if doc.cssselect(HERO_SEL) else 'plein'
    neuf = rendre(d, SRC[lang], lang, fond)
    s = s[:i] + neuf + s[j:]
    # head : feuille et script
    if LINK_TAG not in s:
        s = re.sub(r'<link rel="stylesheet" href="/entete\.css[^"]*">\s*', '', s)
        s = re.sub(r'<script src="/js/entete\.js[^"]*" defer></script>\s*', '', s)
        k = s.find('</head>')
        assert k > 0
        s = s[:k] + LINK_TAG + '\n' + SCRIPT_TAG + '\n' + s[k:]
    # script en ligne : ancien burger
    for ligne in OLD_MENU_JS:
        s = s.replace(ligne, '')
    changed = s != orig
    if changed and not DRY:
        p.write_text(s, encoding='utf8', newline='')
    stats['habillage'][('wp' if d['wp'] else 'mt', lang)] += 1
    stats['fond'][fond] += 1
    stats['forme'][forme] += 1
    if d['wa2']:
        stats['wa2'] += 1
    if d.get('langfix'):
        stats['langfix'].append(str(p.relative_to(ROOT)))
    return changed


def lire_sources():
    SRC = {}
    for l in LANGS:
        p = ROOT / PREFIX[l] / 'index.html'
        s = p.read_text(encoding='utf8')
        i, j, _ = trouver_bloc(s)
        d = lire_bloc(s[i:j])
        assert len(d['ch_items']) == 15, (l, len(d['ch_items']))
        assert len(d['liens']) == 5, (l, d['liens'])
        assert len(d['pan_items']) == 6, (l, d['pan_items'])
        SRC[l] = d
    return SRC


PATCHES_ANIM = [
    ("D.querySelector('.nav .liens a[href$=\"plan-your-trip/\"],.nav .liens a[href$=\"contact-quick/\"]')",
     "D.querySelector('.mt-tete .mt-cta,.nav .liens a[href$=\"plan-your-trip/\"],.nav .liens a[href$=\"contact-quick/\"]')"),
    ("D.querySelector('.nav .liens a.nav-cta')||D.querySelector('.panneau nav a.nav-cta')",
     "D.querySelector('.mt-tete .mt-cta')||D.querySelector('.mt-panneau .mt-cta')||D.querySelector('.nav .liens a.nav-cta')||D.querySelector('.panneau nav a.nav-cta')"),
]


def patch_anim():
    f = ROOT / 'js' / 'anim.js'
    s = f.read_text(encoding='utf8')
    n = 0
    for old, new in PATCHES_ANIM:
        if new in s:
            continue
        assert old in s, 'anim.js : motif introuvable : ' + old[:60]
        s = s.replace(old, new)
        n += 1
    if n and not DRY:
        f.write_text(s, encoding='utf8', newline='')
    return n


def main():
    for f in ('entete.css', 'js/entete.js'):
        assert (ROOT / f).exists(), f + ' manquant'
    SRC = lire_sources()
    stats = {'habillage': Counter(), 'fond': Counter(), 'forme': Counter(), 'wa2': 0, 'langfix': []}
    anomalies = []
    pages = lister_pages()
    changes = 0
    for p in pages:
        try:
            if traiter(p, SRC, stats, anomalies):
                changes += 1
        except Exception as ex:  # noqa
            anomalies.append((str(p.relative_to(ROOT)), 'ERREUR ' + repr(ex)[:200]))
    n_anim = patch_anim()
    print('pages traitees : %d | modifiees : %d | anim.js : %d motif(s) adapte(s)%s' % (len(pages), changes, n_anim, ' (SIMULATION)' if DRY else ''))
    print('formes de depart : %s' % dict(stats['forme']))
    print('fond (data-fond) : %s' % dict(stats['fond']))
    print('pages avec second bouton WhatsApp d\'en-tete (hebreu, conserve : en-tete en mode large, panneau en mode compact) : %d' % stats['wa2'])
    print('habillage x langue :')
    for hab in ('mt', 'wp'):
        row = {l: stats['habillage'][(hab, l)] for l in LANGS}
        print('   %s : %s  (total %d)' % (hab, row, sum(row.values())))
    if stats['langfix']:
        print('selecteur de langue corrige (renvoyait aux accueils, reprend les liens vers la meme page du panneau) : %s' % ', '.join(stats['langfix']))
    for p, m in anomalies:
        print('ANOMALIE', p, m)
    if anomalies:
        sys.exit(1)


if __name__ == '__main__':
    main()
