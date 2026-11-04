# -*- coding: utf-8 -*-
"""Fiche Loup Blanc (Megève) : remplace les 13 photos tirées du PDF (492 x 328 agrandies 4 fois, rendu lisse « 3D »)
par les photos HD du site du chalet (00-brief/references/2026-10-16-megeve-bibi/originaux-hd/, 1600 à 1800 px),
mêmes pièces sous d'autres angles. Même traitement qu'en octobre, sans IA ni étalonnage : miroir (recherche inversée),
rotation légère, recadrage, aux dimensions exactes des fichiers actuels (HTML inchangé). Idempotent. 03/11/2026, demande de Moshé."""
import os, random
from PIL import Image, ImageOps
random.seed(2026)
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
HD = os.path.join(ROOT, "..", "..", "00-brief", "references", "2026-10-16-megeve-bibi", "originaux-hd")
P = "Chalet-Remy-St-Gervais-"
MAP = {"n0-apt-chambre-twin": "appartement-chambre", "n0-apt-chambre-superposes": "appartement-dortoir",
       "n2-chambre-1": "chalet-2eme-dortoirs-enfants-1"}
# 04/11 : seules ces 3 paires sont LA MÊME PIÈCE (IA locale qwen3-vl deux passes + œil, scripts/comparer_photos_piece.py, seuil 70 %) ;
# les 10 autres photos HD montraient d'autres pièces du chalet : anciennes photos (PDF x4) remises, à améliorer par agrandissement fidèle.
def traiter(src, W, H):
    im = ImageOps.mirror(ImageOps.exif_transpose(Image.open(src)).convert("RGB"))
    rot = random.uniform(-0.6, 0.6); im = im.rotate(rot, Image.BICUBIC, expand=False)
    w, h = im.size; m = 0.03 + abs(rot) * 0.02  # marge pour cacher les coins de la rotation
    cl, ct = random.uniform(m, m + 0.05), random.uniform(m, m + 0.05); cr, cb = m, m
    box = [int(w * cl), int(h * ct), int(w * (1 - cr)), int(h * (1 - cb))]
    bw, bh = box[2] - box[0], box[3] - box[1]
    if bw / bh > W / H: nw = int(bh * W / H); box[0] += (bw - nw) // 2; box[2] = box[0] + nw
    else: nh = int(bw * H / W); box[1] += (bh - nh) // 2; box[3] = box[1] + nh
    return im.crop(box).resize((W, H), Image.LANCZOS)
n = 0
for stem, hd in MAP.items():
    jpg = f"img/chalet/megeve-{stem}.jpg"; W, H = Image.open(jpg).size
    out = traiter(os.path.join(HD, P + hd + ".jpg"), W, H)
    out.save(jpg, "JPEG", quality=86, optimize=True, progressive=True); n += 1
    for d in ("img/chalet/w", "img/chalet/min", "img/h"):  # img/h = variantes du héros (oubliées au 1er passage)
        for f in os.listdir(d):
            if f.startswith(f"megeve-{stem}-") and f.endswith(".webp"):
                ww, hh = Image.open(os.path.join(d, f)).size
                out.resize((ww, hh), Image.LANCZOS).save(os.path.join(d, f), "WEBP", quality=80, method=6); n += 1
    print(stem, "<-", hd, (W, H))
print("fichiers écrits :", n)

# ---- 04/11 : les 10 photos sans équivalent HD, agrandissement fidèle B (essai E:\taches\megeve-essais-agrandissement.jpg) :
# Real-ESRGAN x4plus (déjà calculé en octobre dans _tmp/) puis réduction DIRECTE aux dimensions du site + grain fin, au lieu de
# l'étirement à 2000 px d'octobre qui donnait le rendu lisse « 3D ». Miroir et recadrage comme avant, aucune IA générative.
import numpy as np
TMP = os.path.join(ROOT, "..", "..", "00-brief", "references", "2026-10-16-megeve-bibi", "_tmp")
BASSE = {"n0-apt-sejour": "img-p01-07-583x389", "n0-chalet-chambre-twin": "img-p01-08-712x474",
         "n1-chambre-1": "img-p02-06-607x405", "n1-chambre-2": "img-p02-07-575x383", "n1-chambre-3": "img-p02-08-575x383",
         "n1-chambre-4": "img-p02-09-573x382", "n1-chambre-5": "img-p02-10-573x382", "n1-chambre-6": "img-p02-11-611x408",
         "n1-chambre-7": "img-p02-12-584x389", "n2-chambre-2": "img-p03-03-925x617"}
def grain(im, force=4):
    a = np.asarray(im).astype("int16"); n = np.random.default_rng(1).normal(0, force, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype("uint8"))
random.seed(2027)
for stem, src in BASSE.items():
    jpg = f"img/chalet/megeve-{stem}.jpg"; W, H = Image.open(jpg).size
    out = grain(traiter(os.path.join(TMP, src + "-x4.png"), W, H))
    out.save(jpg, "JPEG", quality=86, optimize=True, progressive=True); n += 1
    for d in ("img/chalet/w", "img/chalet/min", "img/h"):
        for f in os.listdir(d):
            if f.startswith(f"megeve-{stem}-") and f.endswith(".webp"):
                ww, hh = Image.open(os.path.join(d, f)).size
                out.resize((ww, hh), Image.LANCZOS).save(os.path.join(d, f), "WEBP", quality=80, method=6); n += 1
    print(stem, "<- x4 réduit + grain", (W, H))
print("fichiers écrits au total :", n)
