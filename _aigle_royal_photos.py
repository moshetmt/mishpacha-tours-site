# -*- coding: utf-8 -*-
"""Photos du chalet Aigle Royal (Les Ménuires), 02/11/2026. Photos réelles du propriétaire, retouche légère seulement
(même luxe() que _photos_reelles.py : niveaux à moitié, contraste +3 %, netteté fine ; Moshé 01/11). Jamais d'agrandissement,
aucune métadonnée (EXIF, GPS). Sources : 00-brief/references/2026-11-02-aigle-royal/orig/ (hors git).
Écartées : table dressée avec bouteilles de vin non casher (img-3558, effacement propre impossible sans IA), plaque au nom du chalet (img-3284), panneau de porte (img-3295), photos d'été avec voitures (dsc-0125, dsc-0127).
Idempotent : réécrit img/chalet/aigle-*.jpg. Ensuite : _galerie_chalets.py puis _images_legeres.py (WebP 640/960/1280)."""
import pathlib
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parents[1] / "00-brief" / "references" / "2026-11-02-aigle-royal" / "orig"
if not SRC.exists():   # worktree : les originaux restent dans le dépôt principal (hors git)
    SRC = pathlib.Path(r"E:\projet site\ads-os\clients\mishpacha-tours\00-brief\references\2026-11-02-aigle-royal\orig")

PHOTOS = {
    "aigle-exterieur-neige": "img-3346",
    "aigle-chalet-hiver": "img-3283",
    "aigle-sejour": "img-3561",
    "aigle-salon": "fa2d02a5-55f0-4034-8b66-a6bd739fc0ef",
    "aigle-salon-cuisine": "img-8758",
    "aigle-cuisine": "img-3595",
    "aigle-chambre-double": "img-3593",
    "aigle-chambre-lits": "img-8706",
    "aigle-chambre-trois-lits": "img-8712",
    "aigle-chambre-bleue": "img-8715",
    "aigle-salle-d-eau": "img-3308",
    "aigle-sauna": "pxl-20211101-102001859",
    "aigle-salon-jeux": "img-8730",
    "aigle-balcon-sud": "img-3600",
}


def luxe(im):
    import numpy as np
    a = np.asarray(im).astype(np.float32) / 255.0
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    lo, hi = np.percentile(L, 0.1), np.percentile(L, 99.9)
    n = np.clip((a - lo) / max(hi - lo, 0.3), 0, 1)
    a = a * 0.5 + n * 0.5
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8"))
    out = ImageEnhance.Contrast(out).enhance(1.03)
    return out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=3))


if __name__ == "__main__":
    for nom, src in PHOTOS.items():
        f = next(SRC.glob(src + ".*"))
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        if src == "img-3561":   # bouteilles de vin non casher à droite de la table (Moshé 02/11) : recadré avant elles
            im = im.crop((0, 0, 935, im.height))
        if src == "img-3283":   # plaque au nom du chalet sur le bardage : recouverte par le bois juste au-dessus
            im.paste(im.crop((532, 344, 568, 380)), (532, 379))
        dst = ICI / "img" / "chalet" / f"{nom}.jpg"
        luxe(im).save(dst, "JPEG", quality=88, optimize=True, progressive=True)
        print(dst.name, im.size)
