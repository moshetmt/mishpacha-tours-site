# -*- coding: utf-8 -*-
"""Allègement des images (21/10/2026), sans changer l'apparence. Passe FINALE et idempotente : à relancer en dernier, après
_zones.py, _kit_wp.py, _lead.py, _chalet_hero.py, _decor.py et _images_cartes.py (ils réécrivent les anciens chemins .jpg/.png).
Les originaux restent sur le disque ; les WebP sont de nouveaux fichiers, mêmes proportions, aucun recadrage, aucune métadonnée.

  1. vignettes des chalets (tiroir du menu, mini(), carte()) : img/chalet/min/<nom>-336.webp et -672.webp
  2. héros (<img fetchpriority="high"> en .jpg) : srcset WebP 640w/960w/1600w/2400w (jamais au-dessus de la source), sizes="100vw",
     fetchpriority, width, height conservés, pas de loading=lazy ajouté. Fichiers dans img/h/
  3. illustrations PNG (img/illus/*.png) : img/illus/w/<nom>.webp, 520 px (700 px pour flat-stopover, affichée jusqu'à 560 px)
  4. photos des cartes de hub (<div class="photo"><img>) : img/cartes/<nom>.webp, 704 px (2 x 352 px affichés au maximum)
Usage : python _images_legeres.py [--check]   (--check : compte sans écrire)"""
import glob, io, os, re, sys
from PIL import Image, ImageOps

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
CHECK = "--check" in sys.argv
Q = 80
CH = {"wp-ext-bleu": "chalet", "slope-facade": "chalet", "courchevel-ext": "chalet", "megeve-n0-apt-sejour": "chalet", "st-tropez-facade": "villa"}
PRIS = {}   # destination -> source, pour détecter deux sources de même nom


def fabriquer(src, dst, largeur):
    """WebP de `largeur` px (jamais agrandi), mêmes proportions. Renvoie la largeur réellement écrite."""
    if dst in PRIS and PRIS[dst] != src:
        raise SystemExit(f"collision de nom : {dst} <- {PRIS[dst]} et {src}")
    PRIS[dst] = src
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    im.load()
    w = min(largeur, im.width)
    if os.path.exists(dst) or CHECK:
        return w
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() or im.mode == "P" and "transparency" in im.info else "RGB")
    if w != im.width:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "WEBP", quality=Q, method=6)
    return w


def chemin(src):
    """/img/x, ../img/x, img/x -> (préfixe, 'img/x') ; None si autre."""
    m = re.match(r"^((?:\.\./)*/?)(img/[^\"?#]+)$", src)
    return (m.group(1), m.group(2)) if m else None


stats = {"nav": 0, "kwp-v": 0, "carte": 0, "hero": 0, "illus": 0, "hub": 0}


def min_chalet(stem, w):
    d = f"img/chalet/min/{stem}-{w}.webp"
    fabriquer(f"img/{CH[stem]}/{stem}.jpg", d, w)
    return "/" + d


def vignettes(h):
    def f(taille, cle):
        def r(m):
            stem = m.group(3)
            if stem not in CH:
                return m.group(0)
            stats[cle] += 1
            return m.group(1) + m.group(2) + min_chalet(stem, taille) + '"'
        return r
    rx = r'(<a class="%s"[^>]*>\s*<img )(src=")/img/(?:chalet|villa)/([\w-]+)\.jpg"'
    h = re.sub(rx % "nav-ch-v", f(336, "nav"), h)
    h = re.sub(rx % "kwp-v", f(336, "kwp-v"), h)
    h = re.sub(r'(<div class="kwp-photo">\s*<img )(src=")/img/(?:chalet|villa)/([\w-]+)\.jpg"', f(672, "carte"), h)
    return h


def heros(h):
    def r(m):
        t = m.group(0)
        if "srcset=" in t or "fetchpriority=\"high\"" not in t:
            return t
        s = re.search(r'\ssrc="([^"]+)"', t)
        c = chemin(s.group(1)) if s else None
        if not c or not c[1].lower().endswith(".jpg"):
            return t
        pre, rel = c
        stem = os.path.splitext(os.path.basename(rel))[0]
        nat = ImageOps.exif_transpose(Image.open(rel)).width
        larges = [w for w in (640, 960, 1600, 2400) if w < nat] + [min(nat, 2400)]
        larges = sorted(set(larges))
        jeu = []
        for w in larges:
            fabriquer(rel, f"img/h/{stem}-{w}.webp", w); jeu.append((w, f"{pre}img/h/{stem}-{w}.webp"))
        src = next((u for w, u in jeu if w >= 960), jeu[-1][1])
        stats["hero"] += 1
        t = t.replace(s.group(0), f' src="{src}" srcset="{", ".join(f"{u} {w}w" for w, u in jeu)}" sizes="100vw"', 1)
        return t
    return re.sub(r"<img\b[^>]*>", r, h)


def illus(h):
    def r(m):
        pre, nom = m.group(2), m.group(3)
        lg = 700 if nom == "flat-stopover" else 520
        fabriquer(f"img/illus/{nom}.png", f"img/illus/w/{nom}.webp", lg)
        stats["illus"] += 1
        return f'{m.group(1)}{pre}img/illus/w/{nom}.webp"'
    return re.sub(r'(<img\b[^>]*?\ssrc=")((?:\.\./)*/?)img/illus/([\w-]+)\.png"', r, h)


def hubs(h):
    def r(m):
        pre, rel = m.group(2), m.group(3)
        stem = os.path.splitext(os.path.basename(rel))[0]
        fabriquer("img/" + rel, f"img/cartes/{stem}.webp", 704)
        stats["hub"] += 1
        return f'{m.group(1)}{pre}img/cartes/{stem}.webp"'
    return re.sub(r'(<div class="photo"><img src=")((?:\.\./)*/?)img/([\w/-]+\.jpg)"', r, h)


def main():
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    n = 0
    for p in pages:
        h = io.open(p, encoding="utf-8", newline="").read()
        t = hubs(illus(heros(vignettes(h))))
        if t != h:
            n += 1
            if not CHECK:
                io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(f"_images_legeres : {n} pages modifiées sur {len(pages)} ;", stats, f";{len(PRIS)} WebP{' (simulation)' if CHECK else ''}")


if __name__ == "__main__":
    main()
