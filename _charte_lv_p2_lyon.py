# -*- coding: utf-8 -*-
"""Charte LV phase 2, lot B2 (03/11/2026) : héros photo des articles Lyon (pages à section pratique-hero).
Vraie photo du lieu sous voile (lv.css A10), à la place du dessin or ; fil et h1 déplacés dans le héros photo.
Photos réelles déjà créditées (CREDITS.md), aucune retouchée par Gemini (les c-* et *-tilsitt-* sont exclues).
Pose aussi le script LV-ENTETE sur toutes les pages à pratique-hero. Idempotent.
    python _charte_lv_p2_lyon.py"""
import pathlib, re
from PIL import Image

ICI = pathlib.Path(__file__).resolve().parent
IMG = ICI / "img"
SORTIE = IMG / "h"

# photo -> (source, focus vertical 0..1)
PHOTOS = {
    "synagogue-tilsitt-facade": ("stock/hub-grande-synagogue-lyon.jpg", .5),
    "chrd-masques": ("stock/chrd-7.jpg", .5),
    "lyon-part-dieu": ("stock/lyon-partdieu.jpg", .5),
    "vieux-lyon-voute": ("stock/rose-6.jpg", .55),
    "juiverie-traboule-20": ("stock/traboule-1.jpg", .5),
    "izieu-classe": ("stock/izieu-1.jpg", .5),
    "vieux-lyon-rue": ("stock/hub-rue-juiverie-lyon.jpg", .5),
    "chabbat-bougies": ("stock/hub-shabbat-in-lyon.jpg", .5),
    "lyon-tete-d-or": ("stock/lyon-tetedor.jpg", .5),
}
ALT = {
    "synagogue-tilsitt-facade": {"en": "The Grande Synagogue of Lyon on quai Tilsitt", "fr": "La Grande Synagogue de Lyon, quai Tilsitt", "es": "La Gran Sinagoga de Lyon, quai Tilsitt", "he": "בית הכנסת הגדול של ליון, quai Tilsitt"},
    "chrd-masques": {"en": "Gas masks in the CHRD collections, Lyon", "fr": "Masques à gaz des collections du CHRD, Lyon", "es": "Máscaras de gas de las colecciones del CHRD, Lyon", "he": "מסכות גז באוסף ה-CHRD, ליון"},
    "lyon-part-dieu": {"en": "A train at Lyon Part-Dieu station", "fr": "Un train en gare de Lyon Part-Dieu", "es": "Un tren en la estación de Lyon Part-Dieu", "he": "רכבת בתחנת Lyon Part-Dieu"},
    "vieux-lyon-voute": {"en": "A vaulted passage in Vieux Lyon", "fr": "Un passage voûté du Vieux Lyon", "es": "Un pasaje abovedado del Vieux Lyon", "he": "מעבר מקומר בעיר העתיקה של ליון"},
    "juiverie-traboule-20": {"en": "Arcades of the traboule at 20 rue Juiverie, Lyon", "fr": "Arcades de la traboule du 20 rue Juiverie, Lyon", "es": "Arcadas de la traboule del número 20 de la rue Juiverie, Lyon", "he": "קשתות ב-traboule של rue Juiverie 20, ליון"},
    "izieu-classe": {"en": "The classroom of the Maison d'Izieu", "fr": "La salle de classe de la Maison d'Izieu", "es": "El aula de la Maison d'Izieu", "he": "הכיתה ב-Maison d'Izieu"},
    "vieux-lyon-rue": {"en": "A street in Vieux Lyon", "fr": "Une rue du Vieux Lyon", "es": "Una calle del Vieux Lyon", "he": "רחוב בעיר העתיקה של ליון"},
    "chabbat-bougies": {"en": "Shabbat candles and a kiddush cup", "fr": "Bougies de Chabbat et coupe de kiddouch", "es": "Velas de Shabat y copa de kidush", "he": "נרות שבת וגביע קידוש"},
    "lyon-tete-d-or": {"en": "The lake of the Parc de la Tête d'Or, Lyon", "fr": "Le lac du parc de la Tête d'Or, Lyon", "es": "El lago del parque de la Tête d'Or, Lyon", "he": "האגם בפארק Tête d'Or, ליון"},
}
ARTICLES = {
    "chabad-lyon": "synagogue-tilsitt-facade",
    "chrd-lyon": "chrd-masques",
    "flights-to-lyon": "lyon-part-dieu",
    "grande-synagogue-lyon": "synagogue-tilsitt-facade",
    "is-lyon-safe-for-jewish-visitors": "synagogue-tilsitt-facade",
    "jewish-cemetery-lyon": "vieux-lyon-voute",
    "jewish-history-lyon": "juiverie-traboule-20",
    "jewish-life-around-lyon": "izieu-classe",
    "jewish-lyon-guide": "synagogue-tilsitt-facade",
    "jewish-lyon-itinerary-2-days": "vieux-lyon-rue",
    "jewish-travel-lyon-faq": "lyon-tete-d-or",
    "kosher-restaurants-lyon": "vieux-lyon-rue",
    "kosher-shabbat-meals-catering-lyon": "chabbat-bougies",
    "lyon-gateway-to-the-alps-kosher": "lyon-part-dieu",
    "lyon-weather": "lyon-tete-d-or",
    "maison-izieu": "izieu-classe",
    "mikveh-lyon": "synagogue-tilsitt-facade",
    "montluc-prison-lyon": "vieux-lyon-voute",
    "rue-juiverie-lyon": "juiverie-traboule-20",
    "shabbat-in-lyon": "chabbat-bougies",
    "synagogues-lyon": "synagogue-tilsitt-facade",
    "things-to-do-in-lyon": "lyon-tete-d-or",
    "where-to-stay-lyon-jewish-travellers": "vieux-lyon-rue",
}
EYEBROW = {"en": "Jewish Lyon", "fr": "Patrimoine juif de Lyon", "es": "El Lyon judío", "he": "יהדות ליון"}
ENTETE = ('<script>/*LV-ENTETE*/(function(){var b=document.body;if(!document.querySelector(".ac-hero,.lv-hero-photo,main>section.hero"))return;'
          'b.classList.add("lv-transp");var f=function(){b.classList.toggle("lv-plein",window.scrollY>60)};'
          'window.addEventListener("scroll",f,{passive:true});f()})();</script>')
RE_ENTETE = re.compile(r'<script>/\*LV-ENTETE\*/.*?</script>', re.S)


def webp():
    """Recadrage 3:2 centré, WebP 640/960/max(<=1600), qualité 78, sans retouche. Renvoie {photo: (larg_max, haut_max)}."""
    tailles, crees = {}, 0
    for nom, (src, fy) in PHOTOS.items():
        im = Image.open(IMG / src).convert("RGB")
        w, h = im.size
        if w / h >= 1.5:
            cw, ch = round(h * 1.5), h
            box = ((w - cw) // 2, 0, (w - cw) // 2 + cw, h)
        else:
            cw, ch = w, round(w / 1.5)
            top = min(max(round(h * fy - ch / 2), 0), h - ch)
            box = (0, top, w, top + ch)
        im = im.crop(box)
        grand = min(1600, cw)
        for lw in (640, 960, grand):
            out = SORTIE / f"hl-{nom}-{lw}.webp"
            if not out.exists():
                im.resize((lw, round(lw / 1.5)), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)
                crees += 1
        tailles[nom] = (grand, round(grand / 1.5))
    return tailles, crees


def heros(nom, lang, taille, fil, h1):
    gw, gh = taille
    srcset = ", ".join(f"/img/h/hl-{nom}-{lw}.webp {lw}w" for lw in sorted({640, 960, gw}))
    return (f'<section class="lv-hero-photo">\n'
            f'  <img src="/img/h/hl-{nom}-960.webp" srcset="{srcset}" sizes="100vw" alt="{ALT[nom][lang]}" '
            f'width="{gw}" height="{gh}" fetchpriority="high" decoding="async">\n'
            f'  <div class="hero-texte">\n    {fil}\n    <p class="lv-eyebrow">{EYEBROW[lang]}</p>\n    {h1}\n  </div>\n</section>\n')


def main():
    tailles, crees = webp()
    modifiees, entete, ignorees, sans_lv = 0, 0, [], []
    for p in sorted(ICI.rglob("*.html")):
        t = p.read_text(encoding="utf-8")
        if 'class="pratique-hero' not in t:
            continue
        rel = p.relative_to(ICI).as_posix().split("/")
        lang = rel[0] if rel[0] in ("fr", "es", "he") else "en"
        slug = (rel[1] if lang != "en" else rel[0]) if len(rel) > 1 else ""
        n = t
        if slug in ARTICLES and 'class="lv-hero-photo"' not in n:
            m = re.search(r'<section class="pratique-hero"[^>]*>.*?</section>', n, re.S)
            bloc = m.group(0)
            fils = re.findall(r'<p class="fil">.*?</p>', bloc, re.S)
            h1s = re.findall(r'<h1[^>]*>.*?</h1>', bloc, re.S)
            ills = re.findall(r'\n?\s*<img[^>]*data-illus="[^"]*"[^>]*>', bloc)
            if len(fils) != 1 or len(h1s) != 1 or len(ills) != 1:
                ignorees.append(f"{'/'.join(rel)} fil={len(fils)} h1={len(h1s)} illus={len(ills)}")
            else:
                nb = bloc.replace(fils[0], "", 1).replace(h1s[0], "", 1).replace(ills[0], "", 1)
                nom = ARTICLES[slug]
                n = n.replace(bloc, heros(nom, lang, tailles[nom], fils[0], h1s[0]) + nb, 1)
        if ENTETE not in n:
            if RE_ENTETE.search(n):
                n = RE_ENTETE.sub(lambda _: ENTETE, n, count=1)
            else:
                n = n.replace("</body>", ENTETE + "\n</body>", 1)
        if not re.search(r'<body[^>]*class="[^"]*\blv\b', n):
            sans_lv.append("/".join(rel))
        if n != t:
            if 'class="lv-hero-photo"' in n and 'class="lv-hero-photo"' not in t:
                modifiees += 1
            if ENTETE in n and ENTETE not in t:
                entete += 1
            p.write_text(n, encoding="utf-8")
    print(f"webp crees: {crees}")
    print(f"heros photo poses: {modifiees}")
    print(f"script LV-ENTETE pose/remplace: {entete}")
    print(f"pages ignorees: {len(ignorees)}", *ignorees, sep="\n  ")
    print(f"pages sans body.lv: {len(sans_lv)}", *sans_lv[:10], sep="\n  ")


if __name__ == "__main__":
    main()
