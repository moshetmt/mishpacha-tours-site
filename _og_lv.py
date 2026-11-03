# -*- coding: utf-8 -*-
"""Images de partage (og:image) a la charte LV (03/11/2026, demande de Moshe apres la story de Mendel qui montrait
   encore l'ancien logo creme). Idempotent.

   IMAGES (1200x630, JPEG < 180 Ko), rendues par Chromium a partir d'un gabarit HTML qui reprend la charte LV :
   blanc dominant, lockup (picto hassid + mot-marque Suez One), titre en Jost capitales, un filet d'or, baseline grise,
   photo reelle du chalet King David (wp-ext-bleu.jpg) en pleine hauteur a droite (a gauche en hebreu). Aucun cadre, aucun arrondi.
     img/og-mishpacha-tours.jpg        : image generique (170 pages : Lyon, services, legales...), texte sans langue
     img/og-accueil-<en|fr|es|he>.jpg  : accueil de chaque langue, titre dans la langue
   PAGES : les 4 accueils pointent sur leur image ; leur og:title perd le prefixe « Mishpacha Tours, » (deja dans og:site_name,
   le titre etait coupe sur telephone). Les pages Alpes gardent leur image Winter Prestige (_og_wp.py).
   PAGES ALPES : python _og_lv.py wp -> les 35 img/og/<slug>.jpg (lockup Winter Prestige en or brosse #7A6440, photo du heros de la page) ;
   remplace le rendu de _og_wp.py, qui ne fait plus que poser les balises.
   Python systeme : python _og_lv.py [--apercu]  (--apercu : ecrit seulement dans _og_lv_apercu/, ne touche a rien)"""
import io, os, re, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://mishpachatours.com"
PHOTO = os.path.join(ROOT, "img", "chalet", "wp-ext-bleu.jpg")
W, H = 1200, 630

TEXTES = {
    # lang : (kicker, titre, baseline)
    None: ("ALPS · LYON", "Strictly kosher<br>holidays", "Strictly kosher · Shomer Shabbat"),
    "en": ("ALPS · LYON", "Strictly kosher<br>holidays", "Strictly kosher · Shomer Shabbat"),
    "fr": ("ALPES · LYON", "Vacances<br>strictement casher", "Strictement casher · Shomer Shabbat"),
    "es": ("ALPES · LYON", "Vacaciones kosher<br>en los Alpes", "Estrictamente kosher · Shomer Shabat"),
    "he": ("האלפים · ליון", "חופשת סקי<br>כשרה באלפים", "שומר כשרות · שומר שבת"),
}

GABARIT = """<!doctype html><html lang="{lang}" dir="{dir}"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Suez+One&family=Heebo:wght@300;400&display=block">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#fff}}
body{{display:flex;font-family:'Jost','Heebo',sans-serif;color:#111}}
.panneau{{width:690px;height:100%;padding:56px 64px 52px;display:flex;flex-direction:column;justify-content:space-between;background:#fff}}
.photo{{flex:1;height:100%;background:url('file:///{photo}') center 45%/cover no-repeat}}
.logo{{display:flex;align-items:center;gap:14px}}
.logo img{{width:52px;height:62px;display:block}}
.logo .mot{{font-family:'Suez One',serif;font-size:40px;line-height:1;color:#111;white-space:nowrap}}
.kicker{{font-weight:400;font-size:17px;letter-spacing:.32em;color:#6B6B6B;text-transform:uppercase}}
h1{{font-family:'Jost','Heebo',sans-serif;font-weight:400;font-size:46px;line-height:1.14;letter-spacing:.05em;text-transform:uppercase;margin:22px 0 28px}}
.filet{{width:84px;height:1px;background:#A88F5E}}
.wp{{display:flex;align-items:center;gap:22px}}
.wp .fl{{width:80px;height:80px;display:block}}
.wp .col{{display:flex;flex-direction:column;gap:9px}}
.wp .mot{{width:330px;height:auto;display:block}}
.wp .pw{{width:330px;height:auto;display:block}}
.wp .sp{{width:440px;height:auto;display:block}}
.base{{font-weight:300;font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:#6B6B6B}}
[dir=rtl] .kicker{{letter-spacing:.12em}}
[dir=rtl] h1{{font-family:'Heebo',sans-serif;font-weight:300;letter-spacing:0;font-size:56px}}
[dir=rtl] .base{{letter-spacing:.06em;font-weight:400}}
</style></head><body>
<div class="panneau">
  {lockup}
  <div><div class="kicker">{kicker}</div><h1>{titre}</h1><div class="filet"></div></div>
  <div class="base">{base}</div>
</div>
<div class="photo"></div>
</body></html>"""


LOCKUP_MT = '<div class="logo"><img src="file:///{picto}" alt=""><span class="mot">mishpacha tours</span></div>'
LOCKUP_WP = ('<div class="wp"><img class="fl" src="file:///{d}/wp-flocon-brosse.svg" alt=""><div class="col">'
             '<img class="mot" src="file:///{d}/wp-mot-brosse.svg" alt=""><img class="pw" src="file:///{d}/wp-powered-brosse.svg" alt=""></div></div>')
LOCKUP_SP = '<div class="wp"><img class="sp" src="file:///{d}/sp-long-brosse.svg" alt=""></div>'
OR_KIT, OR_BROSSE = "#C9A961", "#7A6440"   # or du kit WP -> or brosse fonce de la charte LV (5,1:1 sur fond clair, phase 2 du 03/11)

# Pages Alpes (35 familles, image partagee par les 4 langues, texte sans langue comme la generique) : (kicker, titre)
# Pages ete (logo Summer Prestige, sp-long-or.svg recolore en or brosse) : (kicker, titre)
SP_TEXTES = {
    "summer-in-the-alps-jewish-families": ("KOSHER SUMMER", "The Riviera,<br>the lakes, the Alps"),
    "kosher-villa-saint-tropez": ("KOSHER VILLA · PRIVATE BEACH", "Saint-Tropez"),
}
WP_TEXTES = {
    "alps": ("THE ALPS", "Strictly kosher,<br>winter and summer"),
    "kosher-alpe-dhuez": ("KOSHER SKI · ISÈRE", "Alpe d'Huez"),
    "kosher-annecy": ("KOSHER · LAKE AND ARAVIS", "Annecy"),
    "kosher-cervinia": ("KOSHER SKI · ITALY", "Cervinia"),
    "kosher-chalet-courchevel-aurore-boreale": ("KOSHER CHALET · COURCHEVEL", "Aurore Boréale"),
    "kosher-chalet-courchevel-renard-argente": ("KOSHER CHALET · COURCHEVEL", "Renard Argenté"),
    "kosher-chalet-courchevel": ("KOSHER CHALET · COURCHEVEL", "Flocon Doré"),
    "kosher-chalet-les-deux-alpes": ("KOSHER CHALET · LES DEUX ALPES", "King David"),
    "kosher-chalet-les-menuires": ("KOSHER CHALET · LES MÉNUIRES", "Aigle Royal"),
    "kosher-chalet-megeve": ("KOSHER CHALET · MEGÈVE", "Loup Blanc"),
    "kosher-chalet-val-thorens": ("KOSHER CHALET · VAL THORENS", "Belle Étoile"),
    "kosher-chalets": ("THE ALPS", "Our kosher<br>chalets"),
    "kosher-chamonix": ("KOSHER SKI · MONT BLANC", "Chamonix"),
    "kosher-cortina": ("KOSHER SKI · DOLOMITES", "Cortina d'Ampezzo"),
    "kosher-courchevel": ("KOSHER CHALETS", "Courchevel"),
    "kosher-courmayeur": ("KOSHER SKI · ITALY", "Courmayeur"),
    "kosher-crans-montana": ("KOSHER SKI · SWITZERLAND", "Crans-Montana"),
    "kosher-davos": ("KOSHER SKI · SWITZERLAND", "Davos"),
    "kosher-grenoble": ("KOSHER · ISÈRE", "Grenoble"),
    "kosher-gstaad": ("KOSHER SKI · SWITZERLAND", "Gstaad"),
    "kosher-la-plagne": ("KOSHER SKI · SAVOIE", "La Plagne"),
    "kosher-les-arcs": ("KOSHER SKI · SAVOIE", "Les Arcs"),
    "kosher-les-deux-alpes": ("KOSHER CHALETS", "Les Deux Alpes"),
    "kosher-les-menuires": ("KOSHER CHALET", "Les Ménuires"),
    "kosher-megeve": ("KOSHER CHALET", "Megève"),
    "kosher-pesach-french-alps": ("FRENCH ALPS", "Kosher Pesach<br>2027"),
    "kosher-services-french-alps": ("THE ALPS", "Private kosher chef,<br>Shabbat, minyan"),
    "kosher-ski-anywhere": ("KOSHER SKI", "Anywhere<br>you choose"),
    "kosher-ski-holidays-french-alps": ("FRENCH ALPS", "Kosher ski<br>holidays"),
    "kosher-slope-chalet-les-deux-alpes": ("KOSHER CHALET · LES DEUX ALPES", "Rochebrune"),
    "kosher-st-moritz": ("KOSHER SKI · ENGADINE", "St. Moritz"),
    "kosher-val-disere": ("KOSHER SKI · SAVOIE", "Val d'Isère"),
    "kosher-val-thorens": ("KOSHER CHALET", "Val Thorens"),
    "kosher-verbier": ("KOSHER SKI · SWITZERLAND", "Verbier"),
    "kosher-zermatt": ("KOSHER SKI · SWITZERLAND", "Zermatt"),
}


def svg_brosses(tmpdir):
    """Les 3 SVG du lockup WP de l'en-tete recolores en or brosse, ecrits dans tmpdir."""
    for n in ("flocon", "mot", "powered"):
        t = open(os.path.join(ROOT, "img", f"wp-{n}-or.svg"), encoding="utf-8").read().replace(OR_KIT, OR_BROSSE)
        open(os.path.join(tmpdir, f"wp-{n}-brosse.svg"), "w", encoding="utf-8").write(t)
    t = open(os.path.join(ROOT, "img", "sp-long-or.svg"), encoding="utf-8").read().replace("#E3C48E", OR_BROSSE).replace("#F6EFE3", OR_BROSSE)
    open(os.path.join(tmpdir, "sp-long-brosse.svg"), "w", encoding="utf-8").write(t)


def rendre_html(pg, html, dest):
    tmp = os.path.join(ROOT, "_og_lv_tmp.html"); open(tmp, "w", encoding="utf-8").write(html)
    pg.goto("file:///" + tmp.replace("\\", "/"), wait_until="networkidle")
    pg.evaluate("async () => { await document.fonts.ready; }")
    pg.wait_for_function("document.fonts.check('46px Jost')", timeout=20000)   # Suez One n'est charge que par le lockup Mishpacha : fonts.ready s'en charge
    pg.wait_for_timeout(300)
    png = pg.screenshot(type="png")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    for q in (86, 82, 78, 74, 70):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() < 179000 or q == 70: break
    with open(dest, "wb") as f: f.write(buf.getvalue())
    return buf.tell()


def photo_fiche(h):
    """Fiches chalet de la phase 3 (plus de <section class="hero">) : premiere <img fetchpriority="high">, plus grande variante du srcset."""
    m = re.search(r'<img ([^>]*fetchpriority="high"[^>]*)>', h)
    if not m: return None
    a = m.group(1); cands = []
    s0 = re.search(r' src="([^"]+)"', " " + a)
    if s0: cands.append((0, s0.group(1)))
    ss = re.search(r'srcset="([^"]+)"', a)
    if ss:
        for part in ss.group(1).split(","):
            u = part.strip().split()
            if len(u) == 2 and u[1].endswith("w"): cands.append((int(u[1][:-1]), u[0]))
    for _, u in sorted(cands, reverse=True):
        pth = os.path.join(ROOT, u.lstrip("/"))
        if os.path.isfile(pth): return pth
    return None


def rendre_wp(pg, slug, photo, tmpdir, dest):
    sp = slug in SP_TEXTES
    kicker, titre = (SP_TEXTES if sp else WP_TEXTES)[slug]
    html = GABARIT.format(W=W, H=H, lang="en", dir="ltr", photo=photo.replace("\\", "/"), kicker=kicker, titre=titre,
                          base=TEXTES[None][2], lockup=(LOCKUP_SP if sp else LOCKUP_WP).format(d=tmpdir.replace("\\", "/")))
    return rendre_html(pg, html, dest)


def wp(apercu=False):
    """Les 35 images img/og/<slug>.jpg des pages Alpes (remplace le rendu photo + logo de _og_wp.py ; 03/11 soir, Moshe :
    « le Winter Prestige est invisible a cause du fond, et on avait dit or brosse »)."""
    from _og_wp import photo_heros
    out = os.path.join(ROOT, "_og_lv_apercu", "og") if apercu else os.path.join(ROOT, "img", "og")
    os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as tmpdir, sync_playwright() as p:
        svg_brosses(tmpdir)
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        gros, sans = [], []
        for slug in sorted(WP_TEXTES) + sorted(SP_TEXTES):
            f = os.path.join(ROOT, slug, "index.html")
            h = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
            ph = photo_heros(h) or photo_fiche(h)
            if not ph: sans.append(slug); continue
            n = rendre_wp(pg, slug, ph, tmpdir, os.path.join(out, slug + ".jpg"))
            if n > 179000: gros.append((slug, n))
        b.close()
    tmp = os.path.join(ROOT, "_og_lv_tmp.html")
    if os.path.exists(tmp): os.remove(tmp)
    modif = 0   # pages ete : balises og:image / twitter:image vers img/og/<slug>.jpg (les pages WP les ont deja par _og_wp.py)
    for slug in SP_TEXTES:
        for lang in ("en", "fr", "es", "he"):
            f = os.path.join(ROOT, slug if lang == "en" else os.path.join(lang, slug), "index.html")
            if not os.path.isfile(f): continue
            h = open(f, encoding="utf-8").read(); url = f"{BASE}/img/og/{slug}.jpg"
            n = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
            if n != h and not apercu: open(f, "w", encoding="utf-8", newline="").write(n); modif += 1
    print("pages ete modifiees :", modif)
    print("images WP + SP ecrites :", len(WP_TEXTES) + len(SP_TEXTES) - len(sans), "| sans photo :", sans, "| > 180 Ko :", gros, "| dossier :", out)


def rendre(pg, lang, dest):
    kicker, titre, base = TEXTES[lang]
    html = GABARIT.format(W=W, H=H, lang=lang or "en", dir="rtl" if lang == "he" else "ltr",
                          photo=PHOTO.replace("\\", "/"), picto=os.path.join(ROOT, "img", "picto-hassid.svg").replace("\\", "/"),
                          kicker=kicker, titre=titre, base=base, lockup=LOCKUP_MT.format(picto=os.path.join(ROOT, "img", "picto-hassid.svg").replace("\\", "/")))
    return rendre_html(pg, html, dest)


def pages_accueil(lang):
    return os.path.join(ROOT, "index.html") if lang == "en" else os.path.join(ROOT, lang, "index.html")


def main():
    apercu = "--apercu" in sys.argv
    out = os.path.join(ROOT, "_og_lv_apercu") if apercu else os.path.join(ROOT, "img")
    os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        n = rendre(pg, None, os.path.join(out, "og-mishpacha-tours.jpg")); print("og-mishpacha-tours.jpg", n, "octets")
        for lang in ("en", "fr", "es", "he"):
            n = rendre(pg, lang, os.path.join(out, f"og-accueil-{lang}.jpg")); print(f"og-accueil-{lang}.jpg", n, "octets")
        b.close()
    tmp = os.path.join(ROOT, "_og_lv_tmp.html")
    if os.path.exists(tmp): os.remove(tmp)
    if apercu: print("apercu seulement, pages non modifiees :", out); return
    modif = 0
    for lang in ("en", "fr", "es", "he"):
        f = pages_accueil(lang); h = open(f, encoding="utf-8").read()
        url = f"{BASE}/img/og-accueil-{lang}.jpg"
        n = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
        n = re.sub(r'(<meta property="og:title" content=")Mishpacha Tours, ([^"]*")', lambda m: m.group(1) + m.group(2)[0].upper() + m.group(2)[1:], n)
        if n != h: open(f, "w", encoding="utf-8", newline="").write(n); modif += 1
    print("accueils modifies :", modif)


if __name__ == "__main__":
    if "wp" in sys.argv: wp("--apercu" in sys.argv)
    else: main()
