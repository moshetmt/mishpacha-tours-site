# -*- coding: utf-8 -*-
"""Retours de Moshé du 04/11/2026 (14 h 27-14 h 32, captures iPhone de la préversion). Idempotent, marqueurs RET-0411.
Tout le site :
 - barre du bas WhatsApp / Plan your trip : deux boutons séparés (écart 8 px, coins 4 px, 48 px de haut), marge de sécurité de l'iPhone
   portée par le conteneur et plus par les boutons (avant : boîtes de ~90 px collées bord à bord) ; bandeau cookies posé au-dessus ;
 - plus de gris en bande (#F4F4F2 du bloc final, de « How it works » et des zones ticket) : blanc + filet.
Pages Winter Prestige (body.wp-nav, 140) :
 - logo WP en or brossé (SVG à dégradé) avec le reflet qui passe toutes les 7 s (coupé si mouvement réduit), en-tête et pied ;
 - « POWERED BY » + « mishpacha tours » en Suez One blanc (police du logo) au lieu du SVG en capitales, en-tête et pied ;
 - flocon WP à la place du bonhomme dans le bloc « your week, organised » ;
 - fiches (32) : « Request the catalogue » mène au formulaire (?catalogue=<chalet>, arrive dans la colonne params de Leads), plus au PDF ;
 - bloc « Sources: our team in the Alps… » retiré des fiches (HTML et index.md).
Loup Blanc : héros = spa face au Mont-Blanc (photo réelle du bien, 4:3 natif, sans miroir), 2e = façade sous la neige ; vue à l'arbre retirée."""
import re, glob, os
from PIL import Image, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = {"en": "", "fr": "/fr", "es": "/es", "he": "/he"}

# ---------- 1. SVG or brossé ----------
def brosse(src, dst, stops):
    t = open(f"img/{src}", encoding="utf-8").read()
    g = '<linearGradient id="br" x1="0" y1="0" x2="1" y2=".35">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient>"
    t = t.replace('fill="#C9A961"', 'fill="url(#br)"').replace('stroke="#C9A961"', 'stroke="url(#br)"')
    t = t.replace("<defs>", "<defs>" + g, 1) if "<defs>" in t else re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + "<defs>" + g + "</defs>", t, count=1)
    open(f"img/{dst}", "w", encoding="utf-8").write(t)

CLAIR = [(0, "#8C7448"), (.3, "#C2A874"), (.48, "#E8D6A6"), (.66, "#B0965F"), (1, "#8C7448")]   # sur fond noir
FONCE = [(0, "#5E4C30"), (.35, "#8E7647"), (.5, "#B39A64"), (.68, "#7A6440"), (1, "#5E4C30")]  # sur fond blanc (#7A6440 = 5,1:1)
brosse("wp-flocon-or.svg", "wp-flocon-brosse-clair.svg", CLAIR)
brosse("wp-mot-or.svg", "wp-mot-brosse-clair.svg", CLAIR)
brosse("wp-flocon-or.svg", "wp-flocon-brosse-fonce.svg", FONCE)

# ---------- 2. photos Loup Blanc (recadrage seul, sans miroir : un Mont-Blanc inversé serait un faux paysage) ----------
SRC = "../../00-brief/references/2026-10-16-megeve-bibi/originaux-hd/"
def poser(src, stem, W, H):
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert("RGB"); w, h = im.size
    if w / h > W / H:
        nw = round(h * W / H); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w * H / W); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((W, H), Image.LANCZOS); im.save(f"img/chalet/{stem}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    for d, tailles in (("img/h", (640, 960, 1600)), ("img/chalet/w", (640, 960, 1280)), ("img/chalet/min", (336, 672))):
        for x in tailles:
            x2 = min(x, W); im.resize((x2, round(H * x2 / W)), Image.LANCZOS).save(f"{d}/{stem}-{x}.webp", "WEBP", quality=80, method=6)

poser("site/Chalet-Remy-St-Gervais-chalet-rdc-SPA-1.jpg", "megeve-spa-mont-blanc", 1600, 1200)
poser("site/Chalet-Remy-St-Gervais-chalet-TERRASSE-SUD-4.jpg", "megeve-facade-neige", 1200, 900)

def tag_h(stem, alt, W, H, prio):
    return (f'<img src="/img/h/{stem}-960.webp" srcset="/img/h/{stem}-640.webp 640w, /img/h/{stem}-960.webp 960w, /img/h/{stem}-1600.webp 1600w" '
            f'sizes="(min-width:900px) 58vw, 100vw" alt="{alt}" width="{W}" height="{H}" ' + ('fetchpriority="high"' if prio else 'loading="lazy"') + ' decoding="async">')

# ---------- 3. pages ----------
CAT = {"kosher-chalet-les-deux-alpes": "king-david", "kosher-slope-chalet-les-deux-alpes": "rochebrune", "kosher-chalet-courchevel": "flocon-dore",
       "kosher-chalet-val-thorens": "belle-etoile", "kosher-chalet-megeve": "loup-blanc", "kosher-chalet-les-menuires": "aigle-royal",
       "kosher-chalet-courchevel-aurore-boreale": "aurore-boreale", "kosher-chalet-courchevel-renard-argente": "renard-argente"}
PW = '<span class="wp-pw2" translate="no">POWERED BY <b>mishpacha tours</b></span>'
def REF(svg): return f'<span class="wpb-r" style="--logo:url(/img/{svg})">'

cpt = dict(entete=0, pied=0, final=0, cat=0, sources=0, md=0, rail=0)
for f in sorted(glob.glob("**/index.html", recursive=True)):
    f = f.replace("\\", "/"); s = open(f, encoding="utf-8").read()
    if not re.search(r'<body[^>]*class="[^"]*\bwp-nav\b', s):
        continue
    o = s; parts = f.split("/"); lang = parts[0] if parts[0] in ("fr", "es", "he") else "en"; slug = parts[-2] if len(parts) > 1 else ""
    # en-tête : flocon et mot en or brossé, reflet sur le mot, « POWERED BY mishpacha tours » en texte
    if "RET-0411:entete" not in s and "<!--LOGO-WP:entete-->" in s:
        s = s.replace('<img class="wp-fl" src="/img/wp-flocon-or.svg"', '<img class="wp-fl" src="/img/wp-flocon-brosse-clair.svg"', 1)
        s, n1 = re.subn(r'(<img class="wp-mot" src=")/img/wp-mot-or\.svg("[^>]*>)', lambda m: REF("wp-mot-brosse-clair.svg") + m.group(1) + "/img/wp-mot-brosse-clair.svg" + m.group(2) + "</span>", s, count=1)
        s, n2 = re.subn(r'<img class="wp-pw" src="/img/wp-powered-or\.svg"[^>]*>', lambda m: PW + "<!--RET-0411:entete-->", s, count=1)
        assert n1 and n2, f
        cpt["entete"] += 1
    # pied
    if "RET-0411:pied" not in s:
        bloc = ('<div class="logo-pied wp-v3"><!--RET-0411:pied--><a class="wp-lock" href="' + L[lang] + '/kosher-chalets/" aria-label="Winter Prestige, powered by Mishpacha Tours">'
                '<img class="wp-lock-fl" src="/img/wp-flocon-brosse-clair.svg" alt="" width="84" height="84"><span class="wp-lock-col">' + REF("wp-mot-brosse-clair.svg") +
                '<img class="wp-lock-mot" src="/img/wp-mot-brosse-clair.svg" alt="Winter Prestige" width="250" height="20"></span>' + PW + '</span></a></div>')
        s, n = re.subn(r'<p class="logo-pied wp-v3">.*?</p>', lambda m: bloc, s, count=1, flags=re.S)
        assert n, f
        cpt["pied"] += 1
    # bloc final : flocon WP à la place du bonhomme
    a = '<img class="lead-final-hassid" src="/img/picto-hassid-creme.svg" alt="" width="240" height="243"'
    if a in s:
        s = s.replace(a, '<img class="lead-final-hassid wp-fl-final" src="/img/wp-flocon-brosse-fonce.svg" alt="" width="240" height="240"', 1); cpt["final"] += 1
    # flocon de la barre collante en or brossé foncé (fond blanc)
    s = s.replace('<img class="lc-wpfl" src="/img/wp-flocon-or.svg"', '<img class="lc-wpfl" src="/img/wp-flocon-brosse-fonce.svg"', 1)
    # fiches : catalogue sur demande, sources retirées
    if slug in CAT:
        url = f'{L[lang]}/plan-your-trip/?i=a&amp;catalogue={CAT[slug]}'
        s, n = re.subn(r'(<a class="lc-btn lc-noir lc-(?:cta|mini)"[^>]*?) href="/catalogues/[^"]+\.pdf" target="_blank" rel="noopener"', lambda m: m.group(1) + ' href="' + url + '"', s)
        if n: cpt["cat"] += 1
        s, n = re.subn(r'<section class="clair clair-2 wrap"><p class="source">.*?</p></section>\s*', "", s, flags=re.S)
        if n: cpt["sources"] += 1
        md = f[:-len("index.html")] + "index.md"
        if os.path.exists(md):
            m0 = open(md, encoding="utf-8").read()
            m2 = re.sub(r"\n(?:Sources?|Fuentes?|מקורות)\s?:[^\n]*Mishpacha Tours[^\n]*\n", "\n", m0)
            if m2 != m0: open(md, "w", encoding="utf-8").write(m2); cpt["md"] += 1
    # Loup Blanc : rail
    if slug == "kosher-chalet-megeve" and "megeve-spa-mont-blanc" not in s:
        m = re.search(r'<img src="/img/h/megeve-vue-mont-blanc-960\.webp"[^>]*>', s); assert m, f
        alt = re.search(r'alt="([^"]*)"', m.group(0)).group(1)
        neuf = tag_h("megeve-spa-mont-blanc", alt, 1600, 1200, True) + tag_h("megeve-facade-neige", alt, 1200, 900, False)
        s = s[:m.start()] + neuf + s[m.end():]
        k = len(re.findall(r"<img ", re.search(r'<div class="lc-piste" id="lcPiste">(.*?)<div class="lc-progres">', s, re.S).group(1)))
        s = re.sub(r'(id="lcBarre" style="width:)[0-9.]+%', lambda x: f"{x.group(1)}{100 / k:.3f}%", s)
        s = re.sub(r'(<span class="lc-compte" id="lcCompte" dir="ltr">1 / )\d+', lambda x: f"{x.group(1)}{k}", s)
        cpt["rail"] += 1
    if s != o:
        open(f, "w", encoding="utf-8").write(s)
print(cpt)

# ---------- 4. CSS tout le site (fin de lv.css) ----------
P = "html body.lv" + "".join(f":not(#r{i})" for i in range(1, 12))
CSS = f"""/* ===RET-0411=== retours Moshé du 04/11 (_retours_04_11.py) : barre du bas en deux boutons séparés, plus de gris en bande */
{P} .barre-basse{{display:grid !important;grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;gap:8px !important;padding:8px 12px calc(8px + env(safe-area-inset-bottom)) !important;height:auto !important;background:#FFFFFF !important;border-top:1px solid #E6E6E6 !important;border-radius:0 !important;box-shadow:none !important;overflow:visible !important;pointer-events:auto !important}}
{P} .barre-basse a{{height:48px !important;padding:0 10px !important;margin:0 !important;border-radius:4px !important;box-shadow:none !important}}
@media (max-width:899px){{{P}.bb-on .cb{{bottom:calc(65px + env(safe-area-inset-bottom)) !important}}{P} .cb{{z-index:80 !important}}}}
{P} main>section.lead-final{{background:#FFFFFF !important;box-shadow:none !important;clip-path:none !important;border-top:1px solid #E6E6E6 !important}}
{P} main>section.lead-final .lead-form{{background:#FFFFFF !important;border:1px solid #E6E6E6 !important;box-shadow:none !important}}
{P} main>section#how{{background:#FFFFFF !important;box-shadow:none !important;clip-path:none !important;border-top:1px solid #E6E6E6;border-bottom:1px solid #E6E6E6}}
{P} main>.ticket-zone{{background:#FFFFFF !important;box-shadow:none !important;clip-path:none !important}}
/* ===/RET-0411=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===RET-0411===.*?/\* ===/RET-0411=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)

# ---------- 5. CSS des pages WP (fin de wp-v3.css) ----------
W = "body.wp-nav"
WX = "html body.lv.wp-nav" + "".join(f":not(#r{i})" for i in range(1, 12))  # plus fort que la règle Jost !important de lv.css
WCSS = f"""/* ===RET-0411=== */
.wpb-r{{position:relative;display:block;line-height:0;width:max-content}}
.wpb-r::after{{content:"";position:absolute;inset:0;background:linear-gradient(105deg,transparent 40%,rgba(255,246,222,.95) 50%,transparent 60%) no-repeat;background-size:250% 100%;background-position:120% 0;-webkit-mask:var(--logo) center/100% 100% no-repeat;mask:var(--logo) center/100% 100% no-repeat;animation:wp-reflet 7s ease-in-out 1.2s infinite;pointer-events:none}}
@media (prefers-reduced-motion:reduce){{.wpb-r::after{{animation:none;display:none}}}}
{WX} .wp-pw2{{display:block;font-family:'Jost',system-ui,sans-serif !important;font-weight:500 !important;text-transform:uppercase;letter-spacing:.15em !important;color:#C2A874 !important;white-space:nowrap;line-height:1}}
{WX} .wp-pw2 b{{font-family:'Suez One','Noto Serif Hebrew',Georgia,serif !important;font-weight:400 !important;text-transform:none !important;letter-spacing:.01em !important;color:#FFFFFF !important;font-size:1.25em}}
{WX} .nav .wp-entete .wp-pw2{{font-size:calc(var(--wpmotw) / 25);margin-top:5px;max-width:var(--wpmotw)}}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8) footer.pied .logo-pied.wp-v3{{display:block;margin:64px 0 32px}}
{W} footer.pied .wp-lock{{display:inline-flex;align-items:center;gap:18px;text-decoration:none !important}}
{W} footer.pied .wp-lock img{{filter:none !important}}
{W} footer.pied .wp-lock .wp-lock-fl{{width:72px !important;height:72px !important;flex:none}}
{W} footer.pied .wp-lock .wp-lock-mot{{display:block;width:230px !important;height:auto !important;max-width:none}}
{W} footer.pied .wp-lock .wp-pw2{{font-size:11px;margin-top:9px}}
{W} .lead-final .wp-fl-final{{filter:none !important;width:64px !important;height:64px !important}}
{W} :is(.pyt-flottant,.barre-basse .bb-plan)::before{{background:linear-gradient(100deg,#8C7448,#E8D6A6 48%,#B0965F 66%,#8C7448) !important}}
@media (min-width:900px){{{W} footer.pied .wp-lock .wp-lock-fl{{width:88px !important;height:88px !important}}{W} footer.pied .wp-lock .wp-lock-mot{{width:280px !important}}{W} footer.pied .wp-lock .wp-pw2{{font-size:13px}}}}
/* ===/RET-0411=== */
"""
wv = open("wp-v3.css", encoding="utf-8").read()
wv = re.sub(r"/\* ===RET-0411=== \*/.*?/\* ===/RET-0411=== \*/\n", "", wv, flags=re.S)
open("wp-v3.css", "w", encoding="utf-8").write(wv.rstrip("\n") + "\n" + WCSS)
print("css ok")
