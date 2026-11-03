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
.filet{{width:84px;height:1px;background:linear-gradient(90deg,#F6DC8C 0%,#E2B44A 45%,#C8902A 100%)}}
.base{{font-weight:300;font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:#6B6B6B}}
[dir=rtl] .kicker{{letter-spacing:.12em}}
[dir=rtl] h1{{font-family:'Heebo',sans-serif;font-weight:300;letter-spacing:0;font-size:56px}}
[dir=rtl] .base{{letter-spacing:.06em;font-weight:400}}
</style></head><body>
<div class="panneau">
  <div class="logo"><img src="file:///{picto}" alt=""><span class="mot">mishpacha tours</span></div>
  <div><div class="kicker">{kicker}</div><h1>{titre}</h1><div class="filet"></div></div>
  <div class="base">{base}</div>
</div>
<div class="photo"></div>
</body></html>"""


def rendre(pg, lang, dest):
    kicker, titre, base = TEXTES[lang]
    html = GABARIT.format(W=W, H=H, lang=lang or "en", dir="rtl" if lang == "he" else "ltr",
                          photo=PHOTO.replace("\\", "/"), picto=os.path.join(ROOT, "img", "picto-hassid.svg").replace("\\", "/"),
                          kicker=kicker, titre=titre, base=base)
    tmp = os.path.join(ROOT, "_og_lv_tmp.html"); open(tmp, "w", encoding="utf-8").write(html)
    pg.goto("file:///" + tmp.replace("\\", "/"), wait_until="networkidle")
    pg.evaluate("async () => { await document.fonts.ready; }")
    pg.wait_for_function("document.fonts.check('40px \"Suez One\"') && document.fonts.check('52px Jost')", timeout=20000)
    pg.wait_for_timeout(300)
    png = pg.screenshot(type="png")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    for q in (86, 82, 78, 74, 70):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() < 179000 or q == 70: break
    with open(dest, "wb") as f: f.write(buf.getvalue())
    return buf.tell()


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


if __name__ == "__main__": main()
