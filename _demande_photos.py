# -*- coding: utf-8 -*-
"""Photos des tuiles « Build your stay » du formulaire /plan-your-trip/ (03/11) : photos réelles déjà publiées sur le site
   (chalets du 02/11, Commons CC0, Pexels, Unsplash ; aucune image générée), recadrées 4:3 et réduites en WebP 480 px. Idempotent.
   python _demande_photos.py (depuis site-v5/)"""
import os
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join("img", "illus", "form-svc")
PHOTOS = {
    "chalet": "img/chalet/aigle-exterieur-neige.jpg",
    "chef": "img/chalet/aurore-cuisine.jpg",
    "livre": "img/chalet/aurore-salle-a-manger.jpg",
    "shabbat": "img/stock/hallah.jpg",              # Commons CC0 (Sarah Stierch)
    "butler": "img/chalet/aurore-salon-cheminee.jpg",
    "transfert": "img/stock/hub-kosher-van-transfers.jpg",   # Unsplash
    "ski": "img/reve/ski.jpg",                       # Pexels 15318901
    "activites": "img/reve/traineau.jpg",            # Pexels 5619157
    "lyon": "img/synagogue-tilsitt-galerie.jpg",
    "skimateriel": "img/stock/hub-kosher-ski-holidays-french-alps.jpg",
    "skiforfaits": "img/stock/alpes-ski.jpg",        # Commons CC0 (Megève)
    "massage": "img/chalet/aigle-sauna.jpg",
    "cacher": "img/chalet/aigle-cuisine.jpg",
    "plata": "img/chalet/courchevel-salle-a-manger.jpg",
    "minyan": "img/stock/chabad-priere.jpg",          # Commons CC BY-SA 4.0
    "mikve": "img/stock/mikve.jpg",
}
os.makedirs(OUT, exist_ok=True)
for k, src in PHOTOS.items():
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > 4 / 3:
        nw = int(h * 4 / 3); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * 3 / 4); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((480, 360), Image.LANCZOS)
    im.save(os.path.join(OUT, k + ".webp"), "WEBP", quality=74, method=6)
    print("ok", k)
