# -*- coding: utf-8 -*-
"""Galerie plein ecran « facon Le Collectionist » sur les 5 pages chalet (22/10/2026, Moshe : « il n'y a que 3 photos qui se battent en duel »).
Pages : kosher-chalet-courchevel, kosher-chalet-les-deux-alpes, kosher-slope-chalet-les-deux-alpes, kosher-chalet-megeve, kosher-chalet-val-thorens,
EN + fr/ es/ he/ (20 fichiers). Ce script :
  1. RETIRE le diaporama diapo() de _kit_wp.py (bloc KIT-WP:galerie ou section galerie-wp kwp-diapo) sur ces 20 pages ; la villa Saint-Tropez garde le sien ;
  2. pose dans la banniere (section lead-hero3) le bouton « Voir toutes les photos (N) » (ordinateur) et le rail de photos qu'on fait glisser (telephone) ;
  3. pose avant </main> la galerie plein ecran (colonne des pieces + photos par piece), pilotee par js/galerie.js ;
  4. ecrit le bloc CSS /* ===GALERIE=== */ a la fin de styles.css ;
  5. fabrique les photos neuves img/chalet/<chalet>-<piece>-<n>.jpg (1600 px max, metadonnees vides) et les vignettes img/chalet/min/<nom>-336.webp.
Idempotent : les blocs <!--GALERIE:hero--> et <!--GALERIE:overlay--> sont remplaces a chaque passage.
Usage : python _galerie_chalets.py [--dry | --strip]     (--dry : compte les fichiers qui changeraient, n'ecrit rien ; --strip : enleve la galerie)
CHAINE : A LANCER APRES _kit_wp.py (qui repose le diaporama), AVANT _images_legeres.py (passe finale des WebP)."""
import html as H
import io, os, pathlib, re, sys
from PIL import Image, ImageOps

ICI = pathlib.Path(__file__).resolve().parent
os.chdir(ICI)
DRY = "--dry" in sys.argv
STRIP = "--strip" in sys.argv
LANGS = ("en", "fr", "es", "he")
REF = ICI.parents[1] / "00-brief" / "references"
COU = REF / "2026-10-16-chalet-sisimiut-courchevel" / "rerendu-galerie"
DA = REF / "2026-10-13-photos-chalet-deux-alpes"
ME = REF / "2026-10-16-megeve-bibi" / "rerendu"

# ---------------------------------------------------------------- photos neuves (stem -> source)
def _da(n):
    r = sorted(DA.glob(f"{n:02d}-*.jpg"))
    return r[0] if r else None

NEW = {
    "courchevel-salon-1": COU / "gal-40215.jpg", "courchevel-cuisine-1": COU / "gal-40217.jpg",
    "courchevel-chambre-1": COU / "gal-40220.jpg", "courchevel-chambre-2": COU / "gal-40222.jpg", "courchevel-chambre-3": COU / "gal-40224.jpg",
    "courchevel-chambre-4": COU / "gal-40226.jpg", "courchevel-chambre-5": COU / "sisimiut-3.jpg", "courchevel-chambre-6": COU / "sisimiut-5.jpg",
    "courchevel-chambre-7": COU / "gal-40219.jpg",
    "courchevel-sdb-1": COU / "gal-40221.jpg", "courchevel-sdb-2": COU / "gal-40225.jpg", "courchevel-sdb-3": COU / "gal-40227.jpg",
    "wp-salon-1": _da(35), "wp-salon-2": _da(20), "wp-salon-3": _da(42), "wp-salle-a-manger-1": _da(14), "wp-cuisine-1": _da(15),
    "wp-chambre-1": _da(3), "wp-chambre-2": _da(34), "wp-chambre-3": _da(41), "wp-chambre-4": _da(43), "wp-chambre-5": _da(18),
    "wp-chambre-6": _da(22), "wp-chambre-7": _da(5),
    "wp-sdb-1": _da(1), "wp-sdb-2": _da(27), "wp-sdb-3": _da(39),
    "megeve-n1-chambre-4": ME / "megeve-n1-chambre-4.jpg", "megeve-n1-chambre-6": ME / "megeve-n1-chambre-6.jpg",
    "megeve-n1-chambre-7": ME / "megeve-n1-chambre-7.jpg", "megeve-n2-chambre-2": ME / "megeve-n2-chambre-2.jpg",
}

# ---------------------------------------------------------------- textes
def t(en, fr, es, he):
    return dict(en=en, fr=fr, es=es, he=he)

PIECE = {
    "salon": t("Living room", "Salon", "Salón", "סלון"),
    "salle": t("Dining room", "Salle à manger", "Comedor", "חדר אוכל"),
    "cuisine": t("Kitchen", "Cuisine", "Cocina", "מטבח"),
    "salle-cuisine": t("Dining room and kitchen", "Salle à manger et cuisine", "Comedor y cocina", "חדר אוכל ומטבח"),
    "suite": t("Master suite", "Suite parentale", "Suite principal", "סוויטת ההורים"),
    "chambres": t("Bedrooms", "Chambres", "Habitaciones", "חדרי שינה"),
    "sdb": t("Bathrooms", "Salles de bain", "Baños", "חדרי רחצה"),
    "sdb1": t("Bathroom", "Salle de bain", "Baño", "חדר רחצה"),
    "piscines": t("Pools", "Piscines", "Piscinas", "בריכות"),
    "ext": t("Exterior", "Extérieur", "Exterior", "חוץ"),
    "vues": t("Views", "Les vues", "Las vistas", "נוף"),
    "ext-vues": t("Exterior and views", "Extérieur et vues", "Exterior y vistas", "חוץ ונוף"),
    "apt-salon": t("Apartment living room", "Séjour de l'appartement", "Salón del apartamento", "סלון הדירה"),
    "n1": t("First-floor bedrooms", "Chambres du premier étage", "Habitaciones del primer piso", "חדרי שינה בקומה הראשונה"),
    "n0": t("Ground-floor bedrooms", "Chambres du rez-de-chaussée", "Habitaciones de la planta baja", "חדרי שינה בקומת הקרקע"),
    "n2": t("Attic bedrooms", "Chambres sous le toit", "Habitaciones bajo el tejado", "חדרי שינה בעליית הגג"),
}
TXT = {
    "voir": t("View all photos", "Voir toutes les photos", "Ver todas las fotos", "לכל התמונות"),
    "court": t("Photos", "Photos", "Fotos", "תמונות"),
    "fermer": t("Close the gallery", "Fermer la galerie", "Cerrar la galería", "סגירת הגלריה"),
    "retour": t("Back to the page", "Retour à la page", "Volver a la página", "חזרה לעמוד"),
    "pieces": t("Rooms", "Pièces", "Estancias", "חדרים"),
}

# ---------------------------------------------------------------- les 5 chalets
CHALETS = {
    "kosher-chalet-courchevel": dict(
        hero="courchevel-ext",
        nom=t("Courchevel Chalet", "Chalet de Courchevel", "Chalé de Courchevel", "הצ'אלה בקורשבל"),
        pieces=[("salon", "salon", ["courchevel-salon-cheminee", "courchevel-salon-lustre", "courchevel-salon-1"]),
                ("salle", "salle", ["courchevel-salle-a-manger"]),
                ("cuisine", "cuisine", ["courchevel-cuisine-1"]),
                ("chambres", "chambres", ["courchevel-chambre", "courchevel-chambre-1", "courchevel-chambre-2", "courchevel-chambre-3", "courchevel-chambre-4",
                                          "courchevel-chambre-5", "courchevel-chambre-6", "courchevel-chambre-7"]),
                ("sdb", "sdb", ["courchevel-sdb-2", "courchevel-sdb-3", "courchevel-sdb-1"]),
                ("piscines", "piscines", ["courchevel-piscine-ext", "courchevel-piscine-int"]),
                ("ext", "ext", ["courchevel-ext"])]),
    "kosher-chalet-les-deux-alpes": dict(
        hero="wp-ext-bleu",
        nom=t("Les Deux Alpes Chalet", "Chalet des Deux Alpes", "Chalé de Les Deux Alpes", "הצ'אלה בלה דז אלפ"),
        pieces=[("salon", "salon", ["wp-salon-1", "living", "wp-salon-2", "wp-salon-3"]),
                ("salle", "salle", ["dining", "wp-salle-a-manger-1"]),
                ("cuisine", "cuisine", ["kitchen", "wp-cuisine-1"]),
                ("chambres", "chambres", ["wp-chambre-1", "bedroom-crib", "wp-chambre-2", "wp-chambre-3", "wp-chambre-4", "wp-chambre-5", "wp-chambre-6", "wp-chambre-7"]),
                ("sdb", "sdb", ["wp-sdb-1", "wp-sdb-2", "wp-sdb-3"]),
                ("ext", "ext", ["wp-ext-bleu", "wp-balcon-detail", "wp-allee", "wp-nuit"]),
                ("vues", "vues", ["wp-pistes-balcon", "wp-soleil", "view"])]),
    "kosher-slope-chalet-les-deux-alpes": dict(
        hero="slope-facade",
        nom=t("The Slope Chalet", "Le chalet des pistes", "El chalet de las pistas", "צ'אלה המסלולים"),
        pieces=[("salon", "salon", ["slope-salon-canape", "slope-salon-baie"]),
                ("salle-cuisine", "salle-cuisine", ["slope-sejour-table"]),
                ("chambres", "chambres", ["slope-chambre-double", "slope-chambre-double-2", "slope-chambre-double-3", "slope-chambre-sous-toit"]),
                ("sdb", "sdb1", ["slope-sdb-baignoire"]),
                ("ext", "ext", ["slope-facade", "slope-exterieur-neige"])]),
    "kosher-chalet-megeve": dict(
        hero="megeve-n0-apt-sejour",
        nom=t("The Mont Blanc Chalet", "Le chalet du Mont Blanc", "El chalet del Mont Blanc", "צ'אלה מון בלאן"),
        pieces=[("apt-salon", "apt-salon", ["megeve-n0-apt-sejour"]),
                ("n1", "n1", ["megeve-n1-chambre-1", "megeve-n1-chambre-2", "megeve-n1-chambre-3", "megeve-n1-chambre-4", "megeve-n1-chambre-5",
                              "megeve-n1-chambre-6", "megeve-n1-chambre-7"]),
                ("n0", "n0", ["megeve-n0-chalet-chambre-twin", "megeve-n0-apt-chambre-twin", "megeve-n0-apt-chambre-superposes"]),
                ("n2", "n2", ["megeve-n2-chambre-1", "megeve-n2-chambre-2"])]),
    "kosher-chalet-val-thorens": dict(
        hero="valthorens-exterieur-neige",
        nom=t("The Val Thorens Chalet", "Le chalet de Val Thorens", "El chalet de Val Thorens", "הצ'אלה בואל טורנס"),
        pieces=[("salon", "salon", ["valthorens-salon-poele", "valthorens-salon-baie"]),
                ("salle-cuisine", "salle-cuisine", ["valthorens-cuisine-salle-a-manger", "valthorens-table"]),
                ("suite", "suite", ["valthorens-suite-parentale", "valthorens-suite-mezzanine"]),
                ("chambres", "chambres", ["valthorens-chambre-balcon", "valthorens-chambre-2", "valthorens-chambre-3"]),
                ("sdb", "sdb1", ["valthorens-salle-de-bain"]),
                ("ext-vues", "ext-vues", ["valthorens-exterieur-neige", "valthorens-chalet-neige", "valthorens-vue-balcon"])]),
}

SVG_X = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/></svg>'
SVG_BACK = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M20 12H5M11 5l-7 7 7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'


# ---------------------------------------------------------------- images
def jpg_path(stem):
    return ICI / "img" / "chalet" / f"{stem}.jpg"


def fabriquer_jpg(stem):
    """Photo neuve : 1600 px de large au plus, orientation appliquee, AUCUNE metadonnee (EXIF, GPS), jamais d'agrandissement."""
    dst = jpg_path(stem)
    if dst.exists():
        return
    src = NEW.get(stem)
    if not src or not pathlib.Path(src).exists():
        raise SystemExit(f"photo introuvable : {stem} (source {src})")
    im = ImageOps.exif_transpose(Image.open(src))
    im = im.convert("RGB")
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    clean = Image.new("RGB", im.size)
    clean.paste(im)
    clean.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    print("photo", dst.name, im.size)


def vignette(stem):
    d = ICI / "img" / "chalet" / "min" / f"{stem}-336.webp"
    if d.exists():
        return
    d.parent.mkdir(parents=True, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(jpg_path(stem))).convert("RGB")
    w = min(336, im.width)
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(d, "WEBP", quality=80, method=6)


_DIM = {}


def dim(stem):
    if stem not in _DIM:
        with Image.open(jpg_path(stem)) as im:
            _DIM[stem] = im.size
    return _DIM[stem]


# ---------------------------------------------------------------- blocs HTML
def e(s):
    return H.escape(s, quote=True)


def bloc_hero(lang, c, hero_attrs):
    toutes = [s for _, _, ss in c["pieces"] for s in ss]
    n = len(toutes)
    ordre = [c["hero"]] + [s for s in toutes if s != c["hero"]]
    nom = c["nom"][lang]
    imgs = []
    for i, s in enumerate(ordre):
        if i == 0 and hero_attrs:
            imgs.append(f'<img {hero_attrs} alt="{e(nom)}" loading="lazy" decoding="async">')
        else:
            w, h = dim(s)   # WebP 640/960 dans img/chalet/w/ (produits par _rail_leger.py) ; 3 premières en eager : la 3e photo restait noire sur iPhone (25/10)
            imgs.append(f'<img src="/img/chalet/w/{s}-960.webp" srcset="/img/chalet/w/{s}-640.webp 640w, /img/chalet/w/{s}-960.webp 960w, /img/chalet/{s}.jpg {w}w" sizes="100vw" alt="{e(nom)}" width="{w}" height="{h}" loading="{"eager" if i <= 3 else "lazy"}" decoding="async">')
    btn = (f'<button type="button" class="gal-btn" data-gal-open aria-haspopup="dialog" aria-controls="galerie">'
           f'<span class="gal-l">{e(TXT["voir"][lang])}</span><span class="gal-c">{e(TXT["court"][lang])}</span> ({n})</button>')
    return (f'<!--GALERIE:hero--><div class="gal-rail" role="group" aria-roledescription="carousel" aria-label="{e(nom)}" data-n="{n}">{"".join(imgs)}</div>'
            f'<span class="gal-cpt" aria-hidden="true">1/{len(ordre)}</span>{btn}<!--/GALERIE:hero-->')


def bloc_overlay(lang, c):
    nom = c["nom"][lang]
    som, corps = [], []
    for cle, pk, stems in c["pieces"]:
        titre = PIECE[pk][lang]
        som.append(f'<a href="#g-{cle}"><img src="/img/chalet/min/{stems[0]}-336.webp" alt="" width="154" height="108" loading="lazy" decoding="async">'
                   f'<span>{e(titre)}</span></a>')
        figs = []
        for i, s in enumerate(stems):
            w, h = dim(s)
            cl = ' class="v"' if w / h < 0.9 else ""
            figs.append(f'<figure{cl}><img src="/img/chalet/{s}.jpg" alt="{e(titre)}" width="{w}" height="{h}" loading="lazy" decoding="async"></figure>')
        corps.append(f'<section class="gal-piece" id="g-{cle}"><h3>{e(titre)}</h3><div class="gal-grid">{"".join(figs)}</div></section>')
    return (f'<!--GALERIE:overlay--><div class="gal" id="galerie" role="dialog" aria-modal="true" aria-label="{e(nom)}" tabindex="-1" hidden>'
            f'<div class="gal-side"><button type="button" class="gal-back" data-gal-close aria-label="{e(TXT["retour"][lang])}">{SVG_BACK}</button>'
            f'<h2 class="gal-nom">{e(nom)}</h2><nav class="gal-som" aria-label="{e(TXT["pieces"][lang])}">{"".join(som)}</nav></div>'
            f'<button type="button" class="gal-x" data-gal-close aria-label="{e(TXT["fermer"][lang])}">{SVG_X}</button>'
            f'<div class="gal-main">{"".join(corps)}</div></div><!--/GALERIE:overlay-->')


RE_HERO = re.compile(r"<!--GALERIE:hero-->.*?<!--/GALERIE:hero-->", re.S)
RE_OVER = re.compile(r"\n?<!--GALERIE:overlay-->.*?<!--/GALERIE:overlay-->", re.S)
RE_DIAPO = re.compile(r'\n?(?:<!--KIT-WP:galerie-->)?<section class="ss wrap galerie-wp kwp-diapo"[^>]*>.*?</section>(?:<!--/KIT-WP:galerie-->)?', re.S)
RE_HEROSEC = re.compile(r'<section class="hero lead-hero3(?: has-gal)?">\s*(<img [^>]*>)', re.S)


def transformer(s, lang, c):
    s = s.replace(chr(13) + chr(10), chr(10))   # pages du site en LF (git autocrlf les remet en CRLF)
    s = RE_HERO.sub("", s)
    s = RE_OVER.sub("", s)
    s = RE_DIAPO.sub("", s)
    s = s.replace('<section class="hero lead-hero3 has-gal">', '<section class="hero lead-hero3">')
    s = re.sub(r'\n?<script src="/js/galerie.js" defer></script>', "", s)
    if STRIP:
        return s
    m = RE_HEROSEC.search(s)
    if not m:
        raise SystemExit("section hero lead-hero3 introuvable")
    img = m.group(1)
    attrs = " ".join(a for a in re.findall(r'(?:src|srcset|sizes|width|height)="[^"]*"', img))
    s = s[:m.start()] + '<section class="hero lead-hero3 has-gal">\n  ' + img + bloc_hero(lang, c, attrs) + s[m.end():]
    i = s.find("</main>")
    if i < 0:
        raise SystemExit("</main> introuvable")
    i += len("</main>")   # hors de <main> : les regles « main h2 » des pages hiver ne doivent pas toucher la galerie
    s = s[:i] + "\n" + bloc_overlay(lang, c) + s[i:]
    j = s.find('<script src="/js/anim.js" defer></script>')
    if j < 0:
        raise SystemExit("anim.js introuvable")
    j += len('<script src="/js/anim.js" defer></script>')
    return s[:j] + '\n<script src="/js/galerie.js" defer></script>' + s[j:]


# ---------------------------------------------------------------- CSS
CSS = r"""/* ===GALERIE=== galerie plein ecran facon Le Collectionist (22/10), pilotee par js/galerie.js, blocs poses par _galerie_chalets.py */
.gal-rail,.gal-cpt{display:none}
.gal-btn{position:absolute;z-index:3;inset-inline-end:48px;bottom:72px;margin:0;padding:12px 16px;border:0;border-radius:0;background:rgba(15,15,15,.7);color:#fff;font:inherit;font-size:14px;line-height:19.6px;text-transform:uppercase;letter-spacing:1px;white-space:nowrap;cursor:pointer}
.gal-btn:hover{background:rgba(15,15,15,.88)}
.gal-btn:focus-visible,.gal-x:focus-visible,.gal-back:focus-visible,.gal-som a:focus-visible{outline:2px solid #fff;outline-offset:2px;box-shadow:0 0 0 4px #1C1B1F}
.gal-c{display:none}
.lead-hero3::before{pointer-events:none}
html.gal-ouvert,html.gal-ouvert body{overflow:hidden}
.gal[hidden]{display:none}
.gal{position:fixed;inset:0;z-index:2147483000;background:#fff;color:#1a1a1a;font-family:inherit;overscroll-behavior:contain;outline:0}
html body .gal h2,html body .gal h3{font-family:inherit;font-weight:400;font-style:normal;text-transform:uppercase;color:#1a1a1a;margin:0;text-wrap:balance}
.gal-back{display:none}
html body .gal .gal-som a{display:block;color:#1a1a1a;text-decoration:none;font-size:14px;font-weight:400}
.gal .gal-som img{display:none}
.gal-x{position:absolute;z-index:4;top:24px;inset-inline-end:24px;width:40px;height:40px;border:0;border-radius:50%;background:#fff;color:#1a1a1a;box-shadow:0 1px 6px rgba(0,0,0,.28);cursor:pointer;display:grid;place-items:center;padding:0}
.gal-x:focus-visible,.gal-back:focus-visible,.gal-som a:focus-visible{outline:2px solid #1a1a1a;box-shadow:none}
.gal figure{margin:0}
.gal figure img{display:block}
@media (min-width:900px){
  .gal{display:flex}
  .gal-side{flex:0 0 383px;box-sizing:border-box;padding:56px 32px 40px;overflow-y:auto;scrollbar-width:thin}
  html body .gal .gal-nom{font-size:28px;line-height:1.2;letter-spacing:.07em;margin-bottom:56px}
  html body .gal .gal-som a{line-height:29.5px;padding:0}
  html body .gal .gal-som a:hover,html body .gal .gal-som a[aria-current="true"]{text-decoration:underline;text-underline-offset:4px}
  html body .gal .gal-som a[aria-current="true"]{font-weight:500}
  .gal-main{flex:1;min-width:0;overflow-y:auto;scrollbar-width:none;overscroll-behavior:contain}
  .gal-main::-webkit-scrollbar{display:none}
  .gal-piece{padding:0 0 8px}
  html body .gal .gal-piece h3{font-size:24px;line-height:1.25;letter-spacing:.09em;padding:56px 0 24px}
  html body .gal .gal-piece:first-child h3{padding-top:44px}
  .gal-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  .gal-grid figure{aspect-ratio:520/429;overflow:hidden;background:#f1efec}
  .gal-grid figure:first-child,.gal-grid figure:last-child:nth-child(even){grid-column:1/-1;aspect-ratio:1057/594}
  .gal-grid img{width:100%;height:100%;object-fit:cover}
  .gal-grid figure.v img{object-fit:contain}
}
@media (max-width:899px){
  .gal{overflow-y:auto;-webkit-overflow-scrolling:touch}
  .gal-x{display:none}
  .gal-back{display:grid;place-items:center;width:44px;height:44px;margin:6px 0 0 -10px;padding:0;border:0;background:none;color:#1a1a1a;cursor:pointer}
  [dir="rtl"] .gal-back{margin:6px -10px 0 0;transform:scaleX(-1)}
  .gal-side{padding:8px 16px 4px}
  html body .gal .gal-nom{font-size:24px;line-height:1.2;letter-spacing:.06em;margin:14px 0 20px}
  .gal-som{display:flex;gap:16px;overflow-x:auto;margin:0 -16px;padding:0 16px 12px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .gal-som::-webkit-scrollbar{display:none}
  html body .gal .gal-som a{flex:0 0 154px}
  .gal .gal-som img{display:block;width:154px;height:108px;object-fit:cover;background:#f1efec}
  .gal .gal-som span{display:block;margin-top:8px;line-height:1.3}
  html body .gal .gal-piece h3{font-size:20px;line-height:1.25;letter-spacing:.08em;padding:28px 16px 12px}
  .gal-grid figure{margin:0 0 8px}
  .gal-grid img{width:100%;height:auto}
  .gal-main{padding-bottom:32px}
  .lead-hero3.has-gal > img{display:none}
  .gal-rail{display:flex;position:absolute;inset:0;z-index:0;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .gal-rail::-webkit-scrollbar{display:none}
  .gal-rail img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;object-position:50% 20%;scroll-snap-align:start;scroll-snap-stop:always}
  .lead-hero3.has-gal .lead3-texte{pointer-events:none}
  .lead-hero3.has-gal .lead3-bloc,.lead-hero3.has-gal .lead3-texte a{pointer-events:auto}
  .gal-cpt{display:block;position:absolute;z-index:3;top:14px;inset-inline-end:14px;padding:6px 10px;background:rgba(15,15,15,.7);color:#fff;font-size:14px;line-height:19.6px;pointer-events:none}
  .gal-btn{top:14px;bottom:auto;inset-inline-end:auto;inset-inline-start:14px;padding:8px 12px}
  .gal-l{display:none}.gal-c{display:inline}
}
@media (prefers-reduced-motion:reduce){.gal-rail{scroll-behavior:auto}}
/* ===/GALERIE=== */"""


def maj_css():
    p = ICI / "styles.css"
    s = p.read_text(encoding="utf-8")
    new = re.sub(r"\n?/\* ===GALERIE===.*?/\* ===/GALERIE=== \*/", "", s, flags=re.S)
    if not STRIP:
        new = new.rstrip("\n") + "\n" + CSS + "\n"
    return p, s, new


def main():
    if not DRY and not STRIP:
        for c in CHALETS.values():
            for _, _, ss in c["pieces"]:
                for s in ss:
                    fabriquer_jpg(s)
                    vignette(s)
    elif DRY:
        for c in CHALETS.values():
            for _, _, ss in c["pieces"]:
                for s in ss:
                    if not jpg_path(s).exists():
                        print("photo manquante (dry)", s)
    chg = 0
    for slug, c in CHALETS.items():
        for lang in LANGS:
            p = ICI / (f"{slug}/index.html" if lang == "en" else f"{lang}/{slug}/index.html")
            s = io.open(p, encoding="utf-8", newline="").read()
            if not jpg_path(c["hero"]).exists():
                raise SystemExit("hero absent")
            for _, _, ss in c["pieces"]:
                for st in ss:
                    if jpg_path(st).exists():
                        dim(st)
            new = transformer(s, lang, c) if all(jpg_path(st).exists() for _, _, ss in c["pieces"] for st in ss) else s
            if new != s:
                chg += 1
                if not DRY:
                    io.open(p, "w", encoding="utf-8", newline="").write(new)
    p, a, b = maj_css()
    if a != b:
        chg += 1
        if not DRY:
            p.write_text(b, encoding="utf-8", newline="")
    print(f"_galerie_chalets : {chg} fichier(s) {'a modifier' if DRY else 'modifie(s)'}")
    return chg


if __name__ == "__main__":
    main()
