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
       "n0-apt-sejour": "appartement-interieur1", "n0-chalet-chambre-twin": "chalet-RDC-Suite-PMR-5-1",
       "n1-chambre-1": "chalet-1er-Chambres-twin-EST-2", "n1-chambre-2": "chalet-1er-Chambres-twin-EST-3",
       "n1-chambre-3": "chalet-RDC-Suite-PMR-2", "n1-chambre-4": "chalet-1er-Junior-suite-OUEST-1",
       "n1-chambre-5": "chalet-1er-Junior-suite-OUEST-5", "n1-chambre-6": "chalet-1er-Junior-suite-OUEST-3",
       "n1-chambre-7": "chalet-2eme-palier-enfants-01",
       "n2-chambre-1": "chalet-2eme-dortoirs-enfants-1", "n2-chambre-2": "chalet-2eme-dortoirs-enfants-2"}
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
    for d in ("img/chalet/w", "img/chalet/min"):
        for f in os.listdir(d):
            if f.startswith(f"megeve-{stem}-") and f.endswith(".webp"):
                ww, hh = Image.open(os.path.join(d, f)).size
                out.resize((ww, hh), Image.LANCZOS).save(os.path.join(d, f), "WEBP", quality=80, method=6); n += 1
    print(stem, "<-", hd, (W, H))
print("fichiers écrits :", n)
