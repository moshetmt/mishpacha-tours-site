# -*- coding: utf-8 -*-
"""Image de partage (og:image) par page Alpes, avec le logo Winter Prestige. Idempotent. Consigne Moshe 03/11/2026
   (demande de Mendel Attal) : le lien d'une page chalet ou Alpes partage une image au logo Winter Prestige.

   PERIMETRE : toute page <lang>/<slug>/index.html dont le <body> porte la classe kwp-hiver ou kwp-ete,
   OU dont le HTML contient <!--KIT-WP:hero-->. L'accueil, Lyon, legales, merci, demande ne bougent pas.
   IMAGE : img/og/<slug>.jpg 1200x630 (qualite 82, < 180 Ko), photo REELLE du heros (plus grande variante de img/h/),
   degrade sombre en bas, logo wp-long-or-powered.svg en bas a gauche (hauteur 120 px).
   Une image par FAMILLE de page (slug sans prefixe de langue) : les 4 langues partagent la meme.
   LOGO : le SVG est rendu par Chromium (Playwright) a 3x puis reduit, aucun logo redessine.
   Puis og:image et twitter:image des pages du perimetre pointent sur https://mishpachatours.com/img/og/<slug>.jpg.
   Python systeme : python _og_wp.py"""
import glob, os, re, io, sys, tempfile
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://mishpachatours.com"
LANGS = ("fr", "es", "he")
W, H, LOGO_H = 1200, 630, 120

def famille(rel):
    """'fr/kosher-chalet-x/index.html' -> ('fr','kosher-chalet-x')"""
    p = rel.replace("\\", "/").split("/")[:-1]
    lang = p[0] if p and p[0] in LANGS else "en"
    if lang != "en": p = p[1:]
    return lang, "-".join(p)

def dans_perimetre(h):
    """kwp-hiver / kwp-ete, ou bloc KIT-WP:hero. Exclu : le bloc porte le logo Summer Prestige (villa de Saint-Tropez, /img/sp-)."""
    b = re.search(r"<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->", h, re.S)
    if b and "/img/sp-" in b.group(0): return False
    return bool(re.search(r'<body[^>]*class="[^"]*kwp-(hiver|ete)', h)) or "<!--KIT-WP:hero-->" in h

def photo_heros(h):
    """Premiere <img> photo (pas un SVG, pas un logo wp-) apres <section class="hero" ; plus grande variante existante."""
    i = h.find('<section class="hero')
    if i < 0: return None
    for m in re.finditer(r'<img ([^>]*)>', h[i:i + 6000]):
        a = m.group(1)
        s0 = re.search(r' src="([^"]+)"', " " + a)
        if not s0 or s0.group(1).endswith(".svg") or s0.group(1).startswith("/img/wp-"): continue
        cands = [(0, s0.group(1))]
        ss = re.search(r'srcset="([^"]+)"', a)
        if ss:
            for part in ss.group(1).split(","):
                u = part.strip().split()
                if len(u) == 2 and u[1].endswith("w"): cands.append((int(u[1][:-1]), u[0]))
        for _, u in sorted(cands, reverse=True):
            p = os.path.join(ROOT, u.lstrip("/"))
            if os.path.isfile(p): return p
        return None
    return None

def rendre_logo(tmp):
    """SVG -> PNG transparent via Chromium, 3x puis LANCZOS a LOGO_H de haut."""
    from playwright.sync_api import sync_playwright
    svg = os.path.join(ROOT, "img", "wp-long-or-powered.svg")
    ratio = 1221.6 / 430.2
    w, h = round(LOGO_H * ratio * 3), LOGO_H * 3
    out = os.path.join(tmp, "logo.png")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h})
        html = os.path.join(tmp, "logo.html")
        open(html, "w", encoding="utf-8").write(f'<body style="margin:0;background:transparent"><img id="l" src="file:///{svg.replace(chr(92),"/")}" style="width:{w}px;height:{h}px;display:block"></body>')
        pg.goto("file:///" + html.replace(chr(92), "/"))
        pg.wait_for_function("document.getElementById('l').complete && document.getElementById('l').naturalWidth>0")
        pg.screenshot(path=out, omit_background=True); b.close()
    im = Image.open(out).convert("RGBA")
    return im.resize((round(LOGO_H * ratio), LOGO_H), Image.LANCZOS)

def fabriquer(photo, logo, dest):
    im = Image.open(photo).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = max(0, min(im.height - H, round((im.height - H) * 0.4)))
    im = im.crop((x, y, x + W, y + H)).convert("RGBA")
    deg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(deg)
    for yy in range(H):
        t = yy / H
        a = 0.12 * 255 + (max(0, (t - 0.40) / 0.60) ** 1.0) * 0.82 * 255
        d.line([(0, yy), (W, yy)], fill=(10, 10, 12, round(min(a, 235))))
    im = Image.alpha_composite(im, deg)
    # voile supplementaire a gauche sous le logo, pour que la ligne Powered by se lise sur un bois clair
    voile = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dv = ImageDraw.Draw(voile)
    for xx in range(700):
        a = round(0.5 * 255 * (1 - xx / 700) ** 1.3)
        dv.line([(xx, H - 260), (xx, H)], fill=(8, 8, 10, a))
    mask = Image.linear_gradient("L").resize((1, 260)).resize((700, 260))
    voile_a = voile.crop((0, H - 260, 700, H)); r, g, b, al = voile_a.split()
    from PIL import ImageChops
    voile_a.putalpha(ImageChops.multiply(al, mask))
    im.alpha_composite(voile_a, (0, H - 260))
    im.alpha_composite(logo, (48, H - LOGO_H - 40))
    im = im.convert("RGB")
    for q in (82, 78, 74, 70):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() < 179000 or q == 70: break
    with open(dest, "wb") as f: f.write(buf.getvalue())
    return buf.tell()

def main():
    pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        if rel.startswith("_") or rel == "index.html": continue
        h = open(f, encoding="utf-8").read()
        if dans_perimetre(h): pages.append((rel, f, h))
    par_lang = {}
    for rel, _, _ in pages: par_lang[famille(rel)[0]] = par_lang.get(famille(rel)[0], 0) + 1
    print("pages retenues par langue :", par_lang, "total", len(pages))
    os.makedirs(os.path.join(ROOT, "img", "og"), exist_ok=True)
    sources = {}
    for rel, _, h in pages:
        lang, slug = famille(rel)
        ph = photo_heros(h)
        if ph and (slug not in sources or lang == "en"): sources[slug] = ph
    manque = sorted({famille(r)[1] for r, _, _ in pages} - set(sources))
    if manque: print("SANS PHOTO DE HEROS (image Mishpacha conservee) :", manque)
    with tempfile.TemporaryDirectory() as tmp:
        logo = rendre_logo(tmp)
        gros = []
        for slug, ph in sorted(sources.items()):
            n = fabriquer(ph, logo, os.path.join(ROOT, "img", "og", slug + ".jpg"))
            if n > 179000: gros.append((slug, n))
    print("images ecrites :", len(sources), "| au-dessus de 180 Ko :", gros)
    modif = 0
    for rel, f, h in pages:
        slug = famille(rel)[1]
        if slug not in sources: continue
        url = f"{BASE}/img/og/{slug}.jpg"
        n = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
        if n != h: open(f, "w", encoding="utf-8", newline="").write(n); modif += 1
    print("pages modifiees :", modif)

if __name__ == "__main__": main()
