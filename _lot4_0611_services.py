# -*- coding: utf-8 -*-
"""Lot 4, n° 20 : une page par service, 7 pages neuves en 4 langues, à partir des JSON de _lot4_contenu/ (textes relus) et du
gabarit de la page Pessah de chaque langue (héros, intro, « ce que comprend », étapes, FAQ, formulaire, suite). Idempotent :
relancer réécrit les pages à l'identique. Photos réelles seulement (chalets Winter Prestige, Pexels pour le traîneau).
Écrit aussi : index.md de chaque page, liste des 9 services sur la page /kosher-services-french-alps/ (marqueur LOT4-SVC-LIENS).
Ensuite : python _build_sitemap.py (sitemap.xml, llms.txt).   Depuis site-v5/ : python _lot4_0611_services.py"""
import glob, html, io, json, os, re, urllib.parse as U
from PIL import Image
from markdownify import markdownify as md
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://mishpachatours.com"; MODELE = "kosher-pesach-french-alps"
LANGS = [("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")]
HUB = {"en": "Kosher services in the Alps", "fr": "Services casher dans les Alpes", "es": "Servicios kosher en los Alpes", "he": "שירותים כשרים באלפים"}
HOME = {"en": "Home", "fr": "Accueil", "es": "Inicio", "he": "דף הבית"}
# slug : (source photo, largeur max) ; les variantes 640/960/max sont écrites dans img/h/<slug>-<w>.webp
PHOTOS = {
 "private-kosher-chalet-alps": ("img/h/wp-ext-bleu-1600.webp", 1600),
 "private-kosher-chef-alps": ("img/chalet/courchevel-cuisine-1.jpg", 1264),
 "kosher-meals-delivered-alps": ("img/chalet/valthorens-cuisine-salle-a-manger.jpg", 1264),
 "shabbat-holiday-meals-alps": ("img/chalet/w/wp-salle-a-manger-1-1280.webp", 1280),
 "minyan-sefer-torah-alps": ("img/chalet/valthorens-vue-balcon.jpg", 1264),
 "spa-massage-alps": ("img/chalet/megeve-spa-mont-blanc.jpg", 1600),
 "activities-alps-kosher-families": ("img/h/reve-traineau-1600.webp", 1600),
}
PHOTOS2 = {  # seconde grande photo, dans « ce que comprend » (06/11 : une seule photo par page = page vide)
 "private-kosher-chalet-alps": "/img/chalet/w/courchevel-salon-cheminee", "private-kosher-chef-alps": "/img/chalet/w/valthorens-table",
 "kosher-meals-delivered-alps": "/img/chalet/w/renard-salle-a-manger", "shabbat-holiday-meals-alps": "/img/chalet/w/valthorens-table",
 "minyan-sefer-torah-alps": "/img/chalet/w/megeve-facade-neige", "spa-massage-alps": "/img/chalet/w/aigle-sauna", "activities-alps-kosher-families": "/img/h/reve-ski"}
def photo2(slug):
    b = PHOTOS2[slug]; ws = [640, 960, 1600] if b.startswith("/img/h/") else [640, 960, 1280]
    return (f'<figure class="svc-ph"><img src="{b}-960.webp" srcset="' + ", ".join(f"{b}-{w}.webp {w}w" for w in ws) +
            '" sizes="(min-width:900px) 1100px, 100vw" alt="" width="1280" height="960" loading="lazy" decoding="async"></figure>')
ORDRE = ["private-kosher-chalet-alps", "private-kosher-chef-alps", "kosher-meals-delivered-alps", "shabbat-holiday-meals-alps",
         "minyan-sefer-torah-alps", "kosher-van-transfers", "kosher-ski-holidays-french-alps", "spa-massage-alps", "activities-alps-kosher-families"]
EXIST = {  # pages existantes gardées à leur URL : (libellé, sous-titre) par langue, photo pour la grille du hub
 "kosher-van-transfers": {"en": ("Private van transfers", "airport, station, resort"), "fr": ("Transferts en van privé", "aéroport, gare, station"), "es": ("Traslados en van privada", "aeropuerto, estación, pistas"), "he": ("הסעות בוואן פרטי", "שדה תעופה, רכבת, אתר הסקי"), "img": "/img/cartes/hub-kosher-van-transfers.webp"},
 "kosher-ski-holidays-french-alps": {"en": ("Kosher ski holidays", "the week, resort by resort"), "fr": ("Vacances au ski casher", "la semaine, station par station"), "es": ("Vacaciones de esquí kosher", "la semana, estación por estación"), "he": ("חופשת סקי כשרה", "השבוע, אתר אחר אתר"), "img": "/img/cartes/reve-ski.webp"},
}

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); io.open(p, "w", encoding="utf-8", newline="").write(s)
def esc(s): return html.escape(s, quote=True)
def ltr(l, s):
    if l != "he": return s
    return re.sub(r"(?<![\w\"'=/])([A-Za-z][A-Za-z' .\-]*[A-Za-z]|\d[\d .:\-]*\d|\d)(?![\w\"'=/])", r'<span dir="ltr">\1</span>', s)
def sub1(motif, rempl, s):
    r, n = re.subn(motif, rempl, s, count=1, flags=re.S); assert n == 1, motif[:80]; return r

def photo(slug):
    src, wmax = PHOTOS[slug]; im = Image.open(src).convert("RGB"); ws = [640, 960, wmax]
    for w in ws:
        out = f"img/h/{slug}-{w}.webp"
        if not os.path.exists(out): im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, "WEBP", quality=82)
    h = round(im.height * wmax / im.width)
    return (f'<img src="/img/h/{slug}-960.webp" srcset="' + ", ".join(f"/img/h/{slug}-{w}.webp {w}w" for w in ws) +
            f'" sizes="100vw" alt="" width="{wmax}" height="{h}" fetchpriority="high">')

def jsonld(l, pre, slug, t):
    url = f"{BASE}/{pre}{slug}/"; lang = {"en": "en", "fr": "fr", "es": "es", "he": "he"}[l]
    ld = [
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": HOME[l], "item": f"{BASE}/{pre}"},
        {"@type": "ListItem", "position": 2, "name": HUB[l], "item": f"{BASE}/{pre}kosher-services-french-alps/"},
        {"@type": "ListItem", "position": 3, "name": f'{t["h1"]} {t["h1_i"]}'.strip(), "item": url}]},
     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]], "inLanguage": lang},
     {"@context": "https://schema.org", "@type": "WebPage", "@id": url, "url": url, "name": t["title"], "description": t["description"],
      "inLanguage": lang, "dateModified": "2026-11-06", "author": {"@id": f"{BASE}/#organization"}, "publisher": {"@id": f"{BASE}/#organization"},
      "isPartOf": {"@type": "WebSite", "url": f"{BASE}/{pre}", "name": "Mishpacha Tours"}},
     {"@context": "https://schema.org", "@type": "Service", "name": f'{t["h1"]} {t["h1_i"]}'.strip(), "description": t["description"], "url": url,
      "serviceType": t["voyage"], "provider": {"@id": f"{BASE}/#organization"}, "areaServed": {"@type": "Place", "name": "French Alps"}, "inLanguage": lang},
    ]
    return json.dumps(ld, ensure_ascii=False)

def page(l, pre, slug, t):
    s = rd(f"{pre}{MODELE}/index.html").replace("\r\n", "\n")
    s = re.sub(r"<!--LOT4-PESSAH-->.*?<!--/LOT4-PESSAH-->", "", s, flags=re.S)
    s = re.sub(r"<!--LOT4-PESSAH-FAQ-->.*?<!--/LOT4-PESSAH-FAQ-->", "", s, flags=re.S)
    s = s.replace(MODELE, slug)                                                   # canonical, hreflang, sélecteur de langue, og:url
    titre = esc(t["title"]) + " | Mishpacha Tours"; desc = esc(t["description"])
    s = sub1(r"<title>.*?</title>", f"<title>{titre}</title>", s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titre}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s)
    s = sub1(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{BASE}/img/og-mishpacha-tours.jpg">', s)
    s = re.sub(r'<meta name="twitter:(title|description)" content="[^"]*">', lambda m: f'<meta name="twitter:{m.group(1)}" content="{titre if m.group(1)=="title" else desc}">', s)
    s = sub1(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + jsonld(l, pre, slug, t) + "</script>", s)
    # héros
    s = sub1(r'<img src="/img/h/pessah-table-960\.webp"[^>]*>', lambda m: photo(slug), s)
    s = sub1(r"<h1>.*?</h1>", f'<h1>{ltr(l, esc(t["h1"]))}<br><i>{ltr(l, esc(t["h1_i"]))}</i></h1>', s)
    voy = U.quote(t["voyage"]); wa = U.quote(t["wa"], safe="")
    s = s.replace("?i=e&amp;voyage=Pesach%20in%20the%20Alps", f"?i=a&amp;voyage={voy}")
    s = re.sub(r'(href="https://wa\.me/33652092301\?text=)[^"]*"', lambda m: m.group(1) + wa + '"', s)
    s = s.replace('<input type="hidden" name="i" value="e">', '<input type="hidden" name="i" value="a">')
    s = s.replace('<input type="hidden" name="voyage" value="Pesach in the Alps">', f'<input type="hidden" name="voyage" value="{esc(t["voyage"])}">')
    # fil d'Ariane et phrase sous la bannière
    s = sub1(r'<p class="fil lead-fil">.*?</p>', f'<p class="fil lead-fil"><a href="/{pre}">{HOME[l]}</a> / <a href="/{pre}kosher-services-french-alps/">{HUB[l]}</a> / {ltr(l, esc(t["h1"]))}</p>', s)
    s = sub1(r'<div class="bn-intro wrap"><p>.*?</p></div>', f'<div class="bn-intro wrap"><p>{ltr(l, esc(t["hero_sub"]))}</p></div>', s)
    # intro
    col = "".join(f"<div><b>{ltr(l, esc(b))}</b><span>{ltr(l, esc(x))}</span></div>" for b, x in t["trois"])
    paras = "".join(f"<p>{ltr(l, esc(x))}</p>" for x in t["intro"])
    s = sub1(r'<div class="mf"><p class="mf-phrase">.*?</div></div>(?:<p>.*?</p>)+</div></section>',
             f'<div class="mf"><p class="mf-phrase">{ltr(l, esc(t["phrase"]))}</p><div class="mf-col">{col}</div></div>{paras}</div></section>', s)
    # ce que comprend
    li = "".join(f'<li class="dk-sans-ico"><b>{ltr(l, esc(b))}</b> {ltr(l, esc(x))}</li>' for b, x in t["inclus"])
    s = sub1(r'(<div class="clair clair-2 ss beige"><div class="wrap">)<h2>.*?</h2><ul class="dk-cartes dk-rail">.*?</ul>',
             lambda m: m.group(1) + f'<h2>{ltr(l, esc(t["inclus_titre"][0]))} <i>{ltr(l, esc(t["inclus_titre"][1]))}</i></h2>{photo2(slug)}<ul class="dk-cartes dk-rail">{li}</ul>', s)
    # étapes
    ol = "".join(f'<li><b>{i+1}</b><div><h3>{ltr(l, esc(h))}</h3><p>{ltr(l, esc(x))}</p></div></li>' for i, (h, x) in enumerate(t["etapes"]))
    s = sub1(r'(<section class="ss wrap etapes">)<h2>.*?</h2><ol>.*?</ol>', lambda m: m.group(1) + f'<h2>{ltr(l, esc(t["etapes_titre"][0]))} <i>{ltr(l, esc(t["etapes_titre"][1]))}</i></h2><ol>{ol}</ol>', s)
    # FAQ
    dq = "".join(f"<details><summary>{ltr(l, esc(q))}</summary><p>{ltr(l, esc(a))}</p></details>" for q, a in t["faq"])
    s = sub1(r'(<section class="clair ss wrap faq">)<h2>.*?</h2>(?:<details>.*?</details>)+', lambda m: m.group(1) + f'<h2>{ltr(l, esc(t["faq_titre"][0]))} <i>{ltr(l, esc(t["faq_titre"][1]))}</i></h2>{dq}', s)
    # bloc final
    s = sub1(r'(<div class="lead-final-tete">.*?<div>)<h2>.*?</h2><p>.*?</p>', lambda m: m.group(1) + f'<h2>{ltr(l, esc(t["final_titre"][0]))} <i>{ltr(l, esc(t["final_titre"][1]))}</i>.</h2><p>{ltr(l, esc(t["final_p"]))}</p>', s)
    return s

def index_md(l, pre, slug, s):
    body = re.search(r"<main[^>]*>(.*?)</main>", s, re.S).group(1)
    body = re.sub(r"<(form|svg|script|style)\b.*?</\1>", "", body, flags=re.S)
    body = re.sub(r'<img[^>]*>', "", body)
    txt = md(body, heading_style="ATX", strip=["a"] if False else None)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)">', s).group(1)
    return (f"> {html.unescape(desc)}\n\nSource: {BASE}/{pre}{slug}/ (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n" + txt + "\n")

n = 0
for slug in PHOTOS:
    d = json.load(open(f"_lot4_contenu/{slug}.json", encoding="utf-8"))
    for l, pre in LANGS:
        s = page(l, pre, slug, d[l]); wr(f"{pre}{slug}/index.html", s); wr(f"{pre}{slug}/index.md", index_md(l, pre, slug, s)); n += 1
print("pages de service écrites :", n)

# liste des 9 services sur la page hub, 4 langues (après « Tous les services, une seule demande »)
A, Z = "<!--LOT4-SVC-LIENS-->", "<!--/LOT4-SVC-LIENS-->"
TITRE = {"en": ("Our services, ", "page by page"), "fr": ("Nos services, ", "page par page"), "es": ("Nuestros servicios, ", "página a página"), "he": ("השירותים שלנו, ", "עמוד אחר עמוד")}
for l, pre in LANGS:
    p = f"{pre}kosher-services-french-alps/index.html"; s = rd(p)
    s = re.sub(re.escape(A) + ".*?" + re.escape(Z), "", s, flags=re.S)
    items = []   # grille de cartes photo (Moshé 06/11 : « c'est toujours un peu vide, repas casher »)
    for slug in ORDRE:
        if slug in EXIST: lab, sous, img = EXIST[slug][l][0], EXIST[slug][l][1], EXIST[slug]["img"]
        else:
            t = json.load(open(f"_lot4_contenu/{slug}.json", encoding="utf-8"))[l]; lab, sous, img = t["h1"], t["h1_i"], f"/img/h/{slug}-640.webp"
        items.append(f'<a class="svc-carte" href="/{pre}{slug}/"><img src="{img}" alt="" width="640" height="480" loading="lazy" decoding="async"><span class="svc-t">{ltr(l, esc(lab))}</span><span class="svc-s">{ltr(l, esc(sous))}</span></a>')
    # 06/11 2 h 40 (Moshé : « ça manque de beauté et de luxe ») : la grille est remplacée par « Votre journée » (_lot4_0611_casher_v3.py) ;
    # ce bloc ne fait plus que retirer l'ancien marqueur.
    wr(p, s)
print("hub : ancienne grille retirée (remplacée par _lot4_0611_casher_v3.py)")
