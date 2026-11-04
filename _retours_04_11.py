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
        s, n1 = re.subn(r'(<img class="wp-mot" src=")/img/wp-mot-or\.svg("[^>]*>)', lambda m: REF("wp-mot-masque.png") + m.group(1) + "/img/wp-mot-brosse-clair.svg" + m.group(2) + "</span>", s, count=1)
        s, n2 = re.subn(r'<img class="wp-pw" src="/img/wp-powered-or\.svg"[^>]*>', lambda m: PW + "<!--RET-0411:entete-->", s, count=1)
        assert n1 and n2, f
        cpt["entete"] += 1
    # pied
    if "RET-0411:pied" not in s:
        bloc = ('<div class="logo-pied wp-v3"><!--RET-0411:pied--><a class="wp-lock" href="' + L[lang] + '/kosher-chalets/" aria-label="Winter Prestige, powered by Mishpacha Tours">'
                '<img class="wp-lock-fl" src="/img/wp-flocon-brosse-clair.svg" alt="" width="84" height="84"><span class="wp-lock-col">' + REF("wp-mot-masque.png") +
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
{P} .barre-basse a{{height:48px !important;padding:0 10px !important;margin:0 !important;border-radius:4px !important;box-shadow:none !important;white-space:normal !important;line-height:1.25 !important;text-align:center !important;letter-spacing:.14em !important}}
@media (max-width:899px){{{P}.bb-on .cb{{bottom:calc(65px + env(safe-area-inset-bottom)) !important}}{P} .cb{{z-index:80 !important}}}}
{P} main>section.lead-final{{background-color:#FFFFFF !important;box-shadow:none !important;clip-path:none !important;border-top:1px solid #E6E6E6 !important}}
{P} main>section.lead-final .lead-form{{background:#FFFFFF !important;border:1px solid #E6E6E6 !important;box-shadow:none !important}}
{P} main>.ticket-zone{{background-color:#FFFFFF !important;box-shadow:none !important;clip-path:none !important}}
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

# ---------- 6. formulaire : « catalogue=<chalet> » prérempli dans le message ----------
NOMS = {"king-david": "King David", "rochebrune": "Rochebrune", "flocon-dore": "Flocon Doré", "belle-etoile": "Belle Étoile", "loup-blanc": "Loup Blanc",
        "aigle-royal": "Aigle Royal", "aurore-boreale": "Aurore Boréale", "renard-argente": "Renard Argenté"}
PHRASE = {"en": "Please send me the catalogue of Chalet {n} and of your services.", "fr": "Merci de m'envoyer le catalogue du chalet {n} et de vos services.",
          "es": "Envíenme, por favor, el catálogo del chalet {n} y de sus servicios.", "he": "אשמח לקבל את הקטלוג של צ'אלה {n} ושל השירותים שלכם."}
import json as _j
for lang, pf in (("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")):
    f = pf + "plan-your-trip/index.html"; s2 = open(f, encoding="utf-8").read()
    s2 = re.sub(r"<script>/\*RET-0411:catalogue\*/.*?</script>", "", s2, flags=re.S)
    js = ("<script>/*RET-0411:catalogue*/(function(){var q;try{q=new URLSearchParams(location.search)}catch(e){return}"
          "var c=(q.get('catalogue')||'').replace(/[^a-z-]/g,''),N=" + _j.dumps(NOMS, ensure_ascii=False) + ",n=N[c];if(!n)return;"
          "var t=document.querySelector('textarea[name=\"message\"]');if(t&&!t.value){t.value=" + _j.dumps(PHRASE[lang], ensure_ascii=False) + ".replace('{n}',n);"
          "t.dispatchEvent(new Event('input',{bubbles:true}))}})();</script>")
    assert "</body>" in s2; s2 = s2.replace("</body>", js + "</body>", 1); open(f, "w", encoding="utf-8").write(s2)
print("formulaires : catalogue prérempli")

# ---------- 7. restes de l'ancien jaune Mishpacha (Moshé 04/11 : « un reste de l'ancien jaune ») ----------
# #FCDE73 écrit en dur : points des cartes Leaflet (fillColor) et soleil / étoiles des horaires de Chabbat -> or brossé #A88F5E.
n_pages = 0
for f in glob.glob("**/index.html", recursive=True):
    t = open(f, encoding="utf-8").read()
    if "#FCDE73" in t or "#fcde73" in t:
        open(f, "w", encoding="utf-8").write(t.replace("#FCDE73", "#A88F5E").replace("#fcde73", "#A88F5E")); n_pages += 1
for g in ("_build_guide.py", "_build_hub.py", "_build_pratique.py", "_contacts_bh_hebcal.py", "_patch_pratique.py"):
    if os.path.exists(g):
        t = open(g, encoding="utf-8").read()
        if "#FCDE73" in t: open(g, "w", encoding="utf-8").write(t.replace("#FCDE73", "#A88F5E"))
print("pages sans #FCDE73 :", n_pages)
JCSS = f"""/* ===RET-0411-JAUNE=== restes de l'ancienne charte (jaune #FCDE73, crème #FFFAED) */
{P} main>section#how li b{{color:#C2A874 !important}}
{P} .sh-ville{{color:#C2A874 !important}}
{P} .sh-moment{{background:rgba(255,255,255,.06) !important}}
{P} .sh-moment svg [fill="#FFFAED"]{{fill:#7A6440}}
{P} .sh-moment svg [stroke="#FFFAED"]{{stroke:#D9D9D9}}
{P} .sh-moment svg [stop-color="#E8875A"]{{stop-color:#C2A874}}
{P} footer.pied details{{border-color:rgba(255,255,255,.18) !important}}
{P} footer.pied a,{P} footer.pied td a,{P} td a,{P} .lead3-texte,{P} .lead3-bloc,{P} .lead3-btns,{P} .kwp-hero-wp{{text-decoration-color:currentColor !important}}
{P} .shabbat-corps small{{display:block;margin-top:18px;font-size:18px !important;line-height:1.4;opacity:1 !important;color:#111111 !important;font-weight:400 !important;letter-spacing:.01em}}
{P} .carte-note{{font-size:15px !important;line-height:1.5;opacity:1 !important;color:#3A3A3A !important;margin-top:14px !important}}
/* ===/RET-0411-JAUNE=== */
"""
lv = open("lv.css", encoding="utf-8").read(); lv = re.sub(r"/\* ===RET-0411-JAUNE===.*?/\* ===/RET-0411-JAUNE=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + JCSS); print("css jaune ok")

# ---------- 8. reflet : masque PNG (Safari décale le reflet avec le SVG du mot) ; alignement de l'encre dans le pied ----------
n8 = 0
for f in glob.glob("**/index.html", recursive=True):
    t = open(f, encoding="utf-8").read()
    if "--logo:url(/img/wp-mot-brosse-clair.svg)" in t:
        open(f, "w", encoding="utf-8").write(t.replace("--logo:url(/img/wp-mot-brosse-clair.svg)", "--logo:url(/img/wp-mot-masque.png)")); n8 += 1
print("reflets en PNG :", n8)
ACSS = """/* ===RET-0411-ALIGN=== pied WP : encre du flocon et du mot sur le bord du texte (mesure au pixel 04/11 : flocon +4 px, mot +6 px) */
body.wp-nav footer.pied .wp-lock .wp-lock-fl{margin-left:-4px}
body.wp-nav footer.pied .wp-lock .wpb-r{margin-left:-6px}
@media (min-width:900px){body.wp-nav footer.pied .wp-lock .wp-lock-fl{margin-left:-5px}body.wp-nav footer.pied .wp-lock .wpb-r{margin-left:-5px}}
html[dir="rtl"] body.wp-nav footer.pied .wp-lock .wp-lock-fl,html[dir="rtl"] body.wp-nav footer.pied .wp-lock .wpb-r{margin-left:0}
/* ===/RET-0411-ALIGN=== */
"""
wv = open("wp-v3.css", encoding="utf-8").read(); wv = re.sub(r"/\* ===RET-0411-ALIGN===.*?/\* ===/RET-0411-ALIGN=== \*/\n", "", wv, flags=re.S)
open("wp-v3.css", "w", encoding="utf-8").write(wv.rstrip("\n") + "\n" + ACSS); print("alignement ok")

# ---------- 9. mot WINTER PRESTIGE = un seul élément masqué (or brossé + reflet sur le même masque : plus de décalage possible) ----------
MOT = '<span class="wpb-m {cls}" role="img" aria-label="Winter Prestige"></span>'
n9 = 0
for f in glob.glob("**/index.html", recursive=True):
    t = open(f, encoding="utf-8").read(); o = t
    t = re.sub(r'<span class="wpb-r" style="--logo:url\(/img/wp-mot-masque\.png\)"><img class="wp-lock-mot"[^>]*></span>', lambda m: MOT.format(cls="wp-lock-mot"), t)
    t = re.sub(r'<span class="wpb-r" style="--logo:url\(/img/wp-mot-masque\.png\)"><img class="wp-mot"[^>]*></span>', lambda m: MOT.format(cls="wp-mot"), t)
    if t != o: open(f, "w", encoding="utf-8").write(t); n9 += 1
print("mots en masque unique :", n9)
MCSS = """/* ===RET-0411-MOT=== */
.wpb-m{display:block;aspect-ratio:1534/120;height:auto;-webkit-mask:url(/img/wp-mot-masque.png) center/100% 100% no-repeat;mask:url(/img/wp-mot-masque.png) center/100% 100% no-repeat;background:linear-gradient(105deg,transparent 40%,rgba(255,246,222,.95) 50%,transparent 60%) 120% 0/250% 100% no-repeat,linear-gradient(100deg,#8C7448 0%,#C2A874 30%,#E8D6A6 48%,#B0965F 66%,#8C7448 100%);animation:wpb-m 7s ease-in-out 1.2s infinite}
@keyframes wpb-m{0%{background-position:120% 0,0 0}22%,100%{background-position:-20% 0,0 0}}
@media (prefers-reduced-motion:reduce){.wpb-m{animation:none}}
body.wp-nav .nav .wp-entete .wpb-m.wp-mot{height:var(--wpmot) !important}
body.wp-nav footer.pied .wp-lock .wpb-m.wp-lock-mot{height:auto !important;margin-left:-6px}
@media (min-width:900px){body.wp-nav footer.pied .wp-lock .wpb-m.wp-lock-mot{margin-left:-5px}}
html[dir="rtl"] body.wp-nav footer.pied .wp-lock .wpb-m.wp-lock-mot{margin-left:0}
/* ===/RET-0411-MOT=== */
"""
wv = open("wp-v3.css", encoding="utf-8").read(); wv = re.sub(r"/\* ===RET-0411-MOT===.*?/\* ===/RET-0411-MOT=== \*/\n", "", wv, flags=re.S)
open("wp-v3.css", "w", encoding="utf-8").write(wv.rstrip("\n") + "\n" + MCSS); print("mot css ok")
