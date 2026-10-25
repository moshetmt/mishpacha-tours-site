# -*- coding: utf-8 -*-
"""Rail de photos des pages chalet (25/10/2026, retour de Mendel : « la 3e photo est noire sur iPhone »).
Cause : les photos du rail sont des JPG pleine taille en loading="lazy" dans un défilement horizontal ; Safari ne charge
que les 2 premières, la 3e s'affiche noire le temps du téléchargement. Correctif, idempotent :
  1. WebP 640 et 960 px dans img/chalet/w/ pour chaque photo du rail (srcset, le JPG reste en 1600w) ;
  2. les 3 premières photos après le héros en loading="eager", les suivantes en lazy (galerie.js précharge au défilement).
    python _rail_leger.py   (depuis site-v5/ ; _galerie_chalets.py produit déjà ce balisage pour les pages neuves)"""
import glob, os, re
from PIL import Image, ImageOps
os.makedirs("img/chalet/w", exist_ok=True)
def webp(stem, w):
    dst = f"img/chalet/w/{stem}-{w}.webp"
    if not os.path.exists(dst):
        im = ImageOps.exif_transpose(Image.open(f"img/chalet/{stem}.jpg")).convert("RGB"); ww = min(w, im.width)
        im.resize((ww, round(im.height * ww / im.width)), Image.LANCZOS).save(dst, "WEBP", quality=80, method=6)
    return dst
def balise(stem, W, H, alt, eager):
    webp(stem, 640); webp(stem, 960)
    return (f'<img src="/img/chalet/w/{stem}-960.webp" srcset="/img/chalet/w/{stem}-640.webp 640w, /img/chalet/w/{stem}-960.webp 960w, /img/chalet/{stem}.jpg {W}w" '
            f'sizes="100vw" alt="{alt}" width="{W}" height="{H}" loading="{"eager" if eager else "lazy"}" decoding="async">')
pages = 0; photos = set()
for p in glob.glob("**/index.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    if 'class="gal-rail"' not in h: continue
    def rail(m):
        k = [0]
        def img(mm):
            stem, alt, W, H = mm.group(1), mm.group(2), mm.group(3), mm.group(4); k[0] += 1; photos.add(stem)
            return balise(stem, W, H, alt, k[0] <= 3)
        # forme d'origine (JPG seul) et forme déjà convertie (pour rester idempotent)
        s = re.sub(r'<img src="/img/chalet/([^"/]+)\.jpg" alt="([^"]*)" width="(\d+)" height="(\d+)" loading="\w+" decoding="async">', img, m.group(0))
        k[0] = 0
        s = re.sub(r'<img src="/img/chalet/w/([^"/]+)-960\.webp" srcset="[^"]*" sizes="100vw" alt="([^"]*)" width="(\d+)" height="(\d+)" loading="\w+" decoding="async">', img, s)
        return s
    h2 = re.sub(r'<div class="gal-rail".*?</div>', rail, h, flags=re.S)
    if h2 != h: open(p, "w", encoding="utf-8").write(h2); pages += 1
print(pages, "pages, ", len(photos), "photos, ", len(glob.glob("img/chalet/w/*.webp")), "WebP")
