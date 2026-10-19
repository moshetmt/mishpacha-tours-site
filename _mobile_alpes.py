# -*- coding: utf-8 -*-
"""Passe mobile des pages Alpes (audit 06-reports/2026-10-19-mobile-ux-alpes.md, sections 1 à 4 validées par Moshé le 19/10).
Téléphone seulement (≤ 899 px), ordinateur inchangé. Idempotent, `--strip` retire tout.
  1. Bannière 3 : hauteur au contenu (plus un écran plein ancré en bas), fil d'Ariane masqué, logo Winter Prestige à 280 px.
     (Les pastilles ont été retirées du HTML par l'autre session le 19/10, accord Moshé.)
  2. Intro au hassid : deux ou trois lignes visibles, « Read more » pour le reste (classe dk-intro + bouton dk-plus de _decor.py).
  3. Cartes chalet : mêmes cartes, moins d'air (photo 16/10, marges et corps resserrés).
  4. Cartes à pictogramme : dessin réduit à gauche du titre, texte pleine largeur, à partir de la 2e carte le texte est replié
     sous le titre (js/mobile-alpes.js enveloppe le texte au chargement, le HTML reste entier pour Google).
Pages : celles qui ont la bannière 3 (lead-hero3). CSS : bloc ===MOBILE-ALPES=== avant le bloc KIT-WP de styles.css, en LF.
À lancer en fin de chaîne, après _decor.py et _kit_wp.py."""
import glob, io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STRIP = "--strip" in sys.argv
D, F = "/* ===MOBILE-ALPES=== */", "/* ===/MOBILE-ALPES=== */"
MARK = "<!--MOB-ALPES-->"
MORE = {"en": "Read more", "fr": "Lire la suite", "es": "Leer más", "he": "להמשך קריאה"}
LANGS = ("fr", "es", "he")

CSS = """@media (max-width:899px){
/* 1. bannière : titre et bouton dans le premier demi-écran */
body .lead-hero3:not(.lead-hero3-illus){height:auto;min-height:0;max-height:none}
body .lead-hero3 > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
body .lead-hero3 .lead3-texte{position:relative;padding-top:88px;padding-bottom:20px}
.lead-hero3 .lead3-texte .lead-fil{display:none}
.lead-hero3 .lead3-bloc{padding:16px 18px 20px}
.lead-hero3 .lead3-bloc > p{margin-top:10px}
.lead-hero3 .lead3-bloc > .lead3-btns{margin-top:14px}
.lead-hero3 .lead3-bloc .kwp-hero-wp{margin-bottom:12px;padding-bottom:12px}
.lead-hero3 .lead3-bloc .kwp-hero-wp img{max-width:280px;margin-inline-start:-6px}
.lead-hero3 .lead3-texte h1{font-size:34px}
.lead-hero3 .lead3-texte h1 i{margin-top:8px}
/* 2. intro au hassid : repliée */
.lead-intro{grid-template-columns:56px 1fr;gap:12px;align-items:start}
.lead-intro .lead-mascotte{width:56px;margin-top:0}
.lead-intro p.dk-intro:not(.dk-ouvert){display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:4;overflow:hidden}
.lead-intro .dk-plus{display:inline-block}
/* 2b. intro en statement éditorial sur les pages noir et or (Moshé 20/10, version 1a) : filet or, texte serif or lumière,
   le bonhomme en or lumière marche sur le filet. Pages claires (été, van) : disposition inchangée. */
body.kwp-hiver .lead-intro{display:block;padding-top:30px;padding-bottom:30px}
body.kwp-hiver .lead-intro>.lead-mascotte{display:block;width:auto;height:38px;margin:0 0 0 2px;content:url(/img/picto-hassid-or-lumiere.svg)}
body.kwp-hiver .lead-intro>div{max-width:none}
body.kwp-hiver .lead-intro>div::before{content:"";display:block;width:40px;height:1px;background:#C9A961;margin:0 0 16px}
body.kwp-hiver .lead-intro>div>p{font-family:Fraunces,Georgia,serif;font-weight:300;font-size:21px;line-height:1.4;color:#E3BE80}
body.kwp-hiver .lead-intro>div>p.dk-intro:not(.dk-ouvert){-webkit-line-clamp:6}
body.kwp-hiver .lead-intro .dk-plus{color:#C9A961}
[dir=rtl] body.kwp-hiver .lead-intro>.lead-mascotte{margin:0 2px 0 0}
/* 3. cartes chalet : moins d'air, même carte */
body .kwp-cartes{gap:16px;margin-top:18px}
body .kwp-photo{aspect-ratio:16/10}
body .kwp-seau{width:72px;height:72px;bottom:-26px;inset-inline-end:12px}
body .kwp-corps{padding:14px 16px 16px}
body .kwp-lieu{font-size:11px;padding-inline-end:84px}
body .kwp-cartes .kwp-carte h3{font-size:20px;margin:4px 0 10px;padding-inline-end:0}
body .kwp-chiffres{gap:8px 12px}
body .kwp-chiffres li{font-size:13.5px}
body .kwp-chiffres b{font-size:15.5px}
body .kwp-chiffres svg{width:20px;height:20px}
body .kwp-casher{margin-top:12px;padding:9px 12px;font-size:13.5px;line-height:1.4}
body .kwp-cartes .kwp-dispo{margin:8px 0 0!important;font-size:12.5px}
body .kwp-pied{padding-top:10px;margin-top:12px}
body .kwp-pied img{width:36px;height:36px}
body .kwp-pied .btn-noir{padding:10px 16px;font-size:14px}
body .kwp-tous{margin-top:14px}
html.mob-alpes .dk-cartes.dk-rail{grid-auto-flow:row;grid-auto-columns:auto;overflow:visible;margin-inline:0;padding-inline:0;scroll-snap-type:none}
html.mob-alpes .dk-cartes.dk-rail > li{padding:12px 14px}
/* 4. cartes à pictogramme : dessin à gauche du titre, texte pleine largeur, repli à partir de la 3e (classes posées par js/mobile-alpes.js) */
html.mob-alpes .dk-cartes > li{display:grid;grid-template-columns:40px 1fr;column-gap:12px;align-items:center;padding:12px 14px;min-height:0}
html.mob-alpes .dk-cartes > li > .dk-ico{position:static;grid-row:1;grid-column:1;width:40px!important;height:40px!important;padding:8px}
html.mob-alpes .dk-cartes > li > .dk-des{padding:0!important}
html.mob-alpes .dk-cartes > li > b{grid-column:2;margin:0;font-size:18px;line-height:1.2}
html.mob-alpes .dk-cartes > li > .dk-corps{grid-column:1 / -1;margin-top:8px;font-size:14.5px;line-height:1.5}
html.mob-alpes .dk-cartes > li.dk-pli > b{cursor:pointer;padding-inline-end:28px;position:relative}
html.mob-alpes .dk-cartes > li.dk-pli > b::after{content:"";position:absolute;inset-inline-end:4px;top:50%;width:9px;height:9px;margin-top:-7px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);transition:transform .2s;opacity:.7}
html.mob-alpes .dk-cartes > li.dk-pli.dk-ouvert > b::after{transform:rotate(225deg);margin-top:-2px}
html.mob-alpes .dk-cartes > li.dk-pli:not(.dk-ouvert) > .dk-corps{display:none}
/* 5. étapes « How it works » : numéro à gauche, texte aligné à gauche, moins d'air */
body.kwp-hiver .etapes ol>li,body .etapes ol>li{display:grid;grid-template-columns:28px 1fr;column-gap:12px;align-items:start;text-align:start;padding:10px 0;margin:0}
body.kwp-hiver .etapes ol>li>b,body .etapes ol>li>b{font-size:15px;line-height:1.4;margin:0}
body.kwp-hiver .etapes ol>li h3,body .etapes ol>li h3{margin:0 0 4px;font-size:19px;line-height:1.2;text-align:start}
body.kwp-hiver .etapes ol>li p,body .etapes ol>li p{margin:0;font-size:14.5px;line-height:1.5;text-align:start}
body.kwp-hiver .cta-etapes,body .cta-etapes{margin-top:8px}
/* 6. stations en pastilles : 44 px sous le pouce */
body.kwp-hiver .kwp-pastilles a,body .kwp-pastilles a{min-height:44px;padding:0 16px}
/* 14. « Keep reading » : une ligne par lien, toute la ligne cliquable, 48 px */
body.kwp-hiver .dk-suite>li,body .dk-suite>li{position:relative;display:flex;align-items:center;gap:12px;min-height:48px;padding:6px 0}
body.kwp-hiver .dk-suite>li>.dk-vigico,body .dk-suite>li>.dk-vigico{width:36px!important;height:36px!important;margin:0}
body.kwp-hiver .dk-suite>li>a,body .dk-suite>li>a{flex:1;display:flex;align-items:center;min-height:44px;font-size:15px;line-height:1.35}
body .dk-suite>li>a::after{content:"";position:absolute;inset:0}
}"""

JS = """<script data-mob-alpes>(function(){if(!matchMedia('(max-width:899px)').matches)return;var H=document.documentElement;H.classList.add('mob-alpes');
document.querySelectorAll('.dk-cartes').forEach(function(ul){var lis=[].slice.call(ul.children);lis.forEach(function(li,i){var b=li.querySelector(':scope > b');if(!b)return;
var corps=document.createElement('span');corps.className='dk-corps';var n=b.nextSibling;while(n){var s=n.nextSibling;corps.appendChild(n);n=s}
if(corps.textContent.replace(/\\s+/g,'')){li.appendChild(corps)}else{return}
if(i>=0){li.classList.add('dk-pli');   /* 20/10 Moshe : toutes les cartes repliables, pas seulement des la 3e */b.setAttribute('role','button');b.setAttribute('tabindex','0');b.setAttribute('aria-expanded','false');
var t=function(){var o=li.classList.toggle('dk-ouvert');b.setAttribute('aria-expanded',o?'true':'false')};b.addEventListener('click',t);b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();t()}})}})})})();</script>"""

def css():
    p = "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
    s2 = re.sub(r"\n?/\* ===MOBILE-ALPES=== \*/.*?/\* ===/MOBILE-ALPES=== \*/\n?", "\n", s, flags=re.S)
    if not STRIP:
        bloc = D + "\n" + CSS + "\n" + F + "\n"
        i = s2.find("/* ===KIT-WP=== */")
        s2 = (s2[:i] + bloc + s2[i:]) if i >= 0 else s2.rstrip("\n") + "\n" + bloc
    if s2 != s: io.open(p, "w", encoding="utf-8", newline="\n").write(s2); return 1
    return 0

def page(path):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    if "lead-hero3" not in s: return 0
    lang = path.split("/")[0] if path.split("/")[0] in LANGS else "en"
    # retrait (idempotence et --strip)
    s = re.sub(re.escape(MARK) + r".*?</script>\n?", "", s, flags=re.S)
    s = re.sub(r'(<section class="ss wrap lead-intro">.*?<div><p) class="dk-intro( dk-ouvert)?"', r"\1", s, count=1, flags=re.S)
    s = re.sub(r'(<section class="ss wrap lead-intro">.*?<div><p>.*?</p>)<button class="dk dk-plus dk-plus-lead"[^>]*>[^<]*</button>', r"\1", s, count=1, flags=re.S)
    mi = re.search(r'<section class="ss wrap lead-intro">.*?<div><p[^>]*>(.*?)</p>', s, re.S)
    longue = bool(mi) and len(re.sub(r"<[^>]+>", "", mi.group(1)).split()) > 70   # intro courte (19/10) : rien à replier
    if not STRIP and longue:
        s = re.sub(r'(<section class="ss wrap lead-intro">.*?<div><p)(>.*?</p>)',
                   lambda m: m.group(1) + ' class="dk-intro"' + m.group(2) + '<button class="dk dk-plus dk-plus-lead" type="button" aria-expanded="false" onclick="this.previousElementSibling.classList.add(\'dk-ouvert\');this.remove()">' + MORE[lang] + '</button>',
                   s, count=1, flags=re.S)
    if not STRIP:
        s = s.replace("</body>", MARK + JS + "\n</body>", 1)
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

if __name__ == "__main__":
    n = css()
    pages = [p.replace("\\", "/") for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith(("_", "preview/"))]
    pages = [p for p in pages if "/preview/" not in p]
    n += sum(page(p) for p in pages)
    print("_mobile_alpes :", n, "fichier(s) modifié(s)", "(strip)" if STRIP else "")
