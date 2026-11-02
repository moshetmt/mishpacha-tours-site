# -*- coding: utf-8 -*-
"""Photos des chalets « Aurore Boréale » et « Renard Argenté » (Courchevel 1550), 02/11/2026, noms choisis par Moshé.
Photos réelles des fiches du propriétaire, retouche légère seulement (luxe() de _aigle_royal_photos.py), sans métadonnées.
Sources : 00-brief/references/2026-11-02-marcandou/ (hors git). 🛑 Jamais le vrai nom des chalets ni du hameau côté client.
Écartées : enseigne au nom du chalet sur la façade (ilulissat-40233), affiche avec visages (ikamiut-40260, 40261),
entrées et cabine décorative (ilulissat-40232, 40236, 40250, ikamiut-40265)."""
import pathlib
from PIL import Image, ImageOps
from _aigle_royal_photos import luxe

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parents[1] / "00-brief" / "references" / "2026-11-02-marcandou"
if not SRC.exists():
    SRC = pathlib.Path(r"E:\projet site\ads-os\clients\mishpacha-tours\00-brief\references\2026-11-02-marcandou")

PHOTOS = {
    # Aurore Boréale (3 suites)
    "aurore-exterieur-piscine": "ilulissat/ilulissat-40251", "aurore-vue-aerienne": "ilulissat/bandeau-40270",
    "aurore-piscine": "ilulissat/ilulissat-40234", "aurore-piscine-facade": "ilulissat/ilulissat-40235",
    "aurore-sejour": "ilulissat/ilulissat-40249", "aurore-salon": "ilulissat/ilulissat-40248", "aurore-salon-cheminee": "ilulissat/ilulissat-40247",
    "aurore-salle-a-manger": "ilulissat/ilulissat-40246", "aurore-cuisine": "ilulissat/ilulissat-40245", "aurore-salon-tv": "ilulissat/ilulissat-40237",
    "aurore-suite-1": "ilulissat/ilulissat-40240", "aurore-suite-2": "ilulissat/ilulissat-40242", "aurore-suite-3": "ilulissat/ilulissat-40244",
    "aurore-salle-de-bain-1": "ilulissat/ilulissat-40243", "aurore-salle-de-bain-2": "ilulissat/ilulissat-40241", "aurore-salle-de-bain-3": "ilulissat/ilulissat-40239",
    # Renard Argenté (2 suites)
    "renard-exterieur-neige": "ikamiut/ikamiut-40266", "renard-facade": "ikamiut/bandeau-40271", "renard-chalet-neige": "ikamiut/ikamiut-40252",
    "renard-bain-nordique": "ikamiut/ikamiut-40253", "renard-sejour": "ikamiut/ikamiut-40263", "renard-salon": "ikamiut/ikamiut-40264",
    "renard-salon-vue": "ikamiut/ikamiut-40262", "renard-cuisine": "ikamiut/ikamiut-40259", "renard-salle-a-manger": "ikamiut/ikamiut-40258",
    "renard-suite-1": "ikamiut/ikamiut-40255", "renard-suite-2": "ikamiut/ikamiut-40257", "renard-chambre": "ikamiut/ikamiut-40254",
    "renard-salle-de-bain": "ikamiut/ikamiut-40256",
}

if __name__ == "__main__":
    for nom, src in PHOTOS.items():
        f = next((SRC / src).parent.glob((SRC / src).name + "*.jpg"))
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        luxe(im).save(ICI / "img" / "chalet" / f"{nom}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        print(nom, im.size)
