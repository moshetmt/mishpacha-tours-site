# -*- coding: utf-8 -*-
"""Offre van (ordre operateur du 14/10) : page /kosher-van-transfers/ en 4 langues + visibilite. Idempotent.
  python _van.py            : tout (page, hub, menu, accueil, formulaire, sitemap, llms.txt, css)
  python _van.py page       : seulement la page et ses 3 copies
  python _van.py visibilite : seulement le post-traitement des autres pages
Ne relance PAS _build_hub.py / _build_pratique.py / _build_guide.py sur les autres pages : la page est generee seule
(_build_guide.build sur ce module uniquement), les copies FR/ES/HE reprennent le chrome (menu, formulaire, pied) d'une page deja
traduite. Ordre ensuite : _zones.py (fait ici pour les 4 pages), _contacts_bh_hebcal.py, _images_cartes.py, _decor.py, _qa.py.
"""
import glob, importlib.util, io, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
sys.path.insert(0, ICI)

SLUG = "kosher-van-transfers"
PHOTO = "img/stock/van-neige.jpg"
TPL = "kosher-services-french-alps"   # page deja traduite dont on reprend le chrome
LANGS = ("fr", "es", "he")

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

import _van_textes as T
spec = importlib.util.spec_from_file_location("van_page", f"_pages/{SLUG}.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
EN = mod.PAGE
EN_X = T.EN_EXTRA
TXT = {"en": dict(EN_X, menu=EN_X["menu"]), **T.TR}
CLES = ("title", "desc", "h1", "ital", "intro", "chips", "crumb", "sections", "related")

# ------------------------------------------------------------------ page
def page():
    import _build_guide as G, _build_i18n as I
    G.build(EN)
    h = rd(f"{SLUG}/index.html")
    h = h.replace('<option value="Izieu">Izieu</option></select>', f'<option value="Izieu">Izieu</option><option value="Van transfer" selected>{EN_X["tour"]}</option></select>', 1)
    h = hero(h, "en").replace('Same-day reply, never on Shabbat.', EN_X["note"])
    wr(f"{SLUG}/index.html", h)
    finals = {}
    for lang in LANGS:
        P = dict(EN, **{k: T.TR[lang][k] for k in CLES})
        G.build(P)                                   # texte traduit dans le gabarit anglais, ecrit dans SLUG/index.html
        I.LOT = [SLUG]; I.FORCE = True
        I.prepare()                                  # -> {lang}/SLUG/index.html pour les 3 langues (chemins absolus, canonical, hreflang) ; seule la copie de {lang} est gardee
        gen = rd(f"{lang}/{SLUG}/index.html")
        tpl = rd(f"{lang}/{TPL}/index.html")
        g = generiques(tpl)
        top = gen[gen.index("<main>"):gen.index('<div class="ticket-zone"')]
        top = top.replace('<a href="/">Home</a>', f'<a href="/{lang}/">{g["home"]}</a>')
        top = top.replace('Ask on WhatsApp</a><a class="pill" href="#book">Get a quote</a>', f'{g["hero"]}</a><a class="pill" href="#book">{g["pill"]}</a>')
        top = top.replace('Ask on WhatsApp</a><p class="fiche-note">Same-day reply, never on Shabbat.</p>', f'{g["cta"]}</a><p class="fiche-note">{T.TR[lang]["note"]}</p>')
        top = top.replace("<h2>Keep <i>reading</i></h2>", f'<h2>{g["lire"]}</h2>')
        top = hero(top, lang)
        tail = tpl[tpl.index('<div class="ticket-zone"'):]
        tail = re.sub(r'<option value="Alps - kosher services">[^<]*</option>', f'<option value="Van transfer" selected>{T.TR[lang]["tour"]}</option>', tail)
        tail = re.sub(r'<link rel="stylesheet" href="https://cdnjs[^>]*leaflet[^>]*>\s*<script src="[^"]*leaflet[^"]*"></script>\s*<script>\s*document\.querySelectorAll\("\.carte-osm"\).*?</script>', "", tail, flags=re.S)
        body_top = tpl[tpl.index("<body"):tpl.index("<main>")]
        head = gen[:gen.index("<body")]
        finals[lang] = head + body_top + top + tail
        print("page", lang)
    # EN a nouveau (la derniere G.build ecrit la copie traduite), puis hreflang + selecteur de toutes les langues sur SLUG seulement
    G.build(EN)
    h = rd(f"{SLUG}/index.html")
    h = h.replace('<option value="Izieu">Izieu</option></select>', f'<option value="Izieu">Izieu</option><option value="Van transfer" selected>{EN_X["tour"]}</option></select>', 1)
    wr(f"{SLUG}/index.html", hero(h, "en").replace("Same-day reply, never on Shabbat.", EN_X["note"]))
    for lang in LANGS: wr(f"{lang}/{SLUG}/index.html", finals[lang])
    I.LOT = [SLUG]; I.FORCE = False
    I.prepare()
    for lang in LANGS:
        p = f"{lang}/{SLUG}/index.html"
        s = rd(p)
        s = I.selector(I.strip_alt(s).replace("</head>", I.alternates(SLUG) + "</head>", 1), SLUG, lang)
        s = s.replace(' data-i18n="todo"', "")
        wr(p, s)
    I.ld()
    for lang in LANGS:      # Service : nom, type et description traduits
        p = f"{lang}/{SLUG}/index.html"; s = rd(p); x = T.TR[lang]["svc"]
        def fix(m):
            import json
            data = json.loads(m.group(1)); bl = data if isinstance(data, list) else [data]
            for b in bl:
                if b.get("@type") == "Service": b.update(name=x["name"], serviceType=x["serviceType"], description=x["description"], inLanguage=lang)
            return '<script type="application/ld+json">' + json.dumps(bl if isinstance(data, list) else bl[0], ensure_ascii=False) + "</script>"
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, count=1, flags=re.S)
        wr(p, s)
    import _zones
    for p in [f"{SLUG}/index.html"] + [f"{l}/{SLUG}/index.html" for l in LANGS]: _zones.traiter(p)

def generiques(tpl):
    m = tpl[tpl.index("<main>"):]
    g = {}
    a = re.search(r'<p class="cta-hero"><a class="btn-noir"[^>]*><svg[^>]*><use href="#wa"/></svg>(.*?)</a><a class="pill" href="#book">(.*?)</a></p>', m, re.S)
    g["hero"], g["pill"] = a.group(1), a.group(2)
    b = re.search(r'<section class="ss wrap cta-pratique">.*?<use href="#wa"/></svg>(.*?)</a><p class="fiche-note">(.*?)</p>', m, re.S)
    g["cta"], g["note"] = b.group(1), b.group(2)
    g["home"] = re.search(r'<p class="fil"><a href="[^"]*">(.*?)</a>', m).group(1)
    g["lire"] = re.findall(r"<h2>(.*?)</h2>", m[:m.index('<div class="ticket-zone"')])[-1]
    return g

def hero(h, lang):
    """Illustration minimale maison (img/stock/van-neige.jpg, Gemini au style du pictogramme, 14/10) dans le hero."""
    pre = "../" if lang == "en" else "/"
    alt = TXT[lang]["alt"]
    h = re.sub(r'<img src="[^"]*illus/[a-z-]+\.png" alt="" width="700" height="700">',
               f'<img class="photo-hero illus-hero" src="{pre}{PHOTO}" alt="{alt}" width="1800" height="1200" fetchpriority="high">', h, count=1)
    if "tete-photo" not in h: h = h.replace('<div class="pratique-tete">', '<div class="pratique-tete tete-photo">', 1)
    return h

# ------------------------------------------------------------------ visibilite
def fichiers():
    for p in glob.glob("**/index.html", recursive=True):
        q = p.replace("\\", "/")
        if q.startswith(("_", ".")) or "/_" in q: continue
        yield q

def lang_de(p):
    t = p.split("/")[0]
    return (t if t in LANGS else "en")

def menu(h, lang):
    pre = "" if lang == "en" else "/" + lang
    lien = f'<a href="{pre}/{SLUG}/">{TXT[lang]["menu"]}</a>'
    def bloc(m):
        s = m.group(0)
        if f"/{SLUG}/" in s: return s
        return re.sub(r'(<a href="[^"]*/plan-your-trip/">[^<]*</a>)', lambda k: lien + "\n    " + k.group(1), s, count=1)
    h = re.sub(r'<nav class="liens".*?</nav>', bloc, h, count=1, flags=re.S)
    h = re.sub(r'(<div class="panneau"[^>]*>\s*<nav[^>]*>.*?</nav>)', bloc, h, count=1, flags=re.S)
    return h

def accueil(h, lang):
    if 'class="ac-van"' in h or 'class="ac-stations compacte"' not in h: return h
    pre = "" if lang == "en" else "/" + lang
    t, d, b = TXT[lang]["accueil"]
    band = (f'\n  <div class="ac-van"><img src="/img/des/car.webp" alt="" width="96" height="96" loading="lazy"><b>{t}</b><p>{d}</p>'
            f'<a class="btn-noir" href="{pre}/{SLUG}/">{b}</a></div>')
    return re.sub(r'(<ul class="ac-stations compacte">.*?</ul>)', lambda m: m.group(1) + band, h, count=1, flags=re.S)

def formulaire(h, lang):
    if "name=\"voyage\"" not in h or TXT[lang]["voyage"] in h: return h
    chips = re.findall(r'<label><input type="checkbox" name="voyage" value="[^"]*"><span>[^<]*</span></label>', h)
    if not chips: return h
    nouveau = f'<label><input type="checkbox" name="voyage" value="{TXT[lang]["voyage"]}"><span>{TXT[lang]["voyage"]}</span></label>'
    return h.replace(chips[-1], nouveau + chips[-1], 1)

def hub(h, lang):
    if re.search(rf'class="hub-carte" href="[^"]*/{SLUG}/"', h): return h
    cartes = re.findall(rf'<a class="hub-carte" href="[^"]*?/{TPL}/"[^>]*>.*?</a>', h, re.S)
    if not cartes: return h
    c = cartes[0]
    pre = "" if lang == "en" else "/" + lang
    n = re.sub(rf'href="[^"]*?/{TPL}/"', f'href="{pre}/{SLUG}/"' if lang != "en" else f'href="../{SLUG}/"', c)
    n = re.sub(r'(<img src=")[^"]*(")', lambda m: m.group(1) + ("../" if lang == "en" else "/") + PHOTO + m.group(2), n, count=1)
    t, d = TXT[lang]["carte"]
    n = re.sub(r"<h3>.*?</h3>", f"<h3>{t}</h3>", n, count=1, flags=re.S)
    n = re.sub(r"<p>.*?</p>", f"<p>{d}</p>", n, count=1, flags=re.S)
    return h.replace(c, c + n, 1)

def sitemap():
    s = rd("sitemap.xml")
    if f"/{SLUG}/" in s: return
    lignes = "".join(f"  <url><loc>https://mishpachatours.com/{('' if l == 'en' else l + '/')}{SLUG}/</loc><lastmod>2026-10-14</lastmod><priority>0.7</priority></url>\n" for l in ("en",) + LANGS)
    for l in ("en",) + LANGS:
        ancre = f"  <url><loc>https://mishpachatours.com/{('' if l == 'en' else l + '/')}lyon-gateway-to-the-alps-kosher/</loc>"
        ligne = f"  <url><loc>https://mishpachatours.com/{('' if l == 'en' else l + '/')}{SLUG}/</loc><lastmod>2026-10-14</lastmod><priority>0.7</priority></url>\n"
        s = s.replace(ancre, ligne + ancre, 1)
    wr("sitemap.xml", s)

def llms():
    s = rd("llms.txt")
    if f"/{SLUG}/" in s: return
    ligne = f"- [{EN['title']}](https://mishpachatours.com/{SLUG}/): {EN['desc']}\n"
    ancre = [l for l in s.splitlines(True) if "/summer-in-the-alps-jewish-families/" in l][0]
    wr("llms.txt", s.replace(ancre, ancre + ligne, 1))

CSS = """
/* offre van (14/10) : photo en tete de page et bande de l'accueil */
.pratique-tete.tete-photo img.photo-hero{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:4px;margin:0}
.dk-cartes + p{margin-top:22px}
.ac-van{display:grid;grid-template-columns:72px 1fr;gap:6px 18px;align-items:center;margin:36px auto 0;max-width:860px;padding:22px 22px 24px;background:var(--jaune);border-radius:15px}
.ac-van img{grid-row:1 / span 2;width:72px;height:72px;object-fit:contain}
.ac-van b{font-family:var(--titre);font-weight:300;font-size:22px;line-height:1.2}
.ac-van p{font-size:16px;line-height:1.45;margin:0}
.ac-van .btn-noir{grid-column:1 / -1;margin-top:18px;justify-self:start;width:auto;display:inline-flex;padding:0 28px}
@media (min-width:900px){
  .pratique-tete.tete-photo{grid-template-columns:1fr 1fr}
  .pratique-tete.tete-photo img.photo-hero{order:0;width:100%;height:auto}
  .ac-van{grid-template-columns:84px 1fr auto;gap:6px 22px}
  .ac-van img{width:84px;height:84px}
  .ac-van b{grid-column:2;grid-row:1;align-self:end}
  .ac-van p{grid-column:2;grid-row:2;align-self:start}
  .ac-van .btn-noir{grid-column:3;grid-row:1 / span 2;margin:0}
}
"""

def visibilite():
    n = 0
    for p in fichiers():
        lang = lang_de(p)
        h = rd(p); o = h
        h = menu(h, lang)
        if p in ("index.html", "fr/index.html", "es/index.html", "he/index.html"): h = accueil(h, lang)
        if p.endswith("plan-your-trip/index.html"): h = formulaire(h, lang)
        if p.endswith("jewish-lyon-guide/index.html"): h = hub(h, lang)
        if h != o: wr(p, h); n += 1
    print(n, "pages de visibilite modifiees")
    sitemap(); llms()
    c = rd("styles.css")
    if ".ac-van{" not in c: wr("styles.css", c + CSS)

if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if a in ("tout", "page"): page()
    if a in ("tout", "visibilite"): visibilite()
