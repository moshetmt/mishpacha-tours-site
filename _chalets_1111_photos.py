# -*- coding: utf-8 -*-
"""Photos des deux chalets du 11/11/2026 (Saint-Gervais Mont-Blanc, Courchevel 1850). Photos réelles des fiches lues le 11/11,
recadrage et luxe() léger de _aigle_royal_photos.py seulement, AUCUNE IA générative, aucun étalonnage, aucune métadonnée,
jamais d'agrandissement. Sources : 00-brief/references/2026-11-11-chalets-*/{a-saint-gervais,b-courchevel}/photos/ (hors site).
Contrôle de chaque photo (vue en pleine taille le 11/11) : 06-reports/2026-11-11-chalets-*/controle-photos.csv.
B : photos en HDR saturé, une baisse de saturation identique sur toute la série (SAT_B). A53/A54 : natifs à 768 px,
sortie à 40 % de la largeur du fichier de 1920 px (jamais de x4 lissé). Les noms de fichiers viennent de PREFIXE (pas du nom commercial).
Idempotent : réécrit les JPG à l'identique. Lancer depuis site-v5 : python _chalets_1111_photos.py"""
import pathlib
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from _aigle_royal_photos import luxe
from _chalets_1111_noms import CH

ICI = pathlib.Path(__file__).resolve().parent
REF = next((ICI.parents[1] / "00-brief" / "references").glob("2026-11-11-chalets-*"))
SAT_B = 0.92
MAXW = 1600

# suffixe -> (fichier source, recadrage (x0,y0,x1,y1) en pixels du fichier, zones à flouter, facteur d'échelle fixe ou None)
A = {
    "exterieur": ("42-exterieur", (560, 0, 1920, 1020), [], None),      # bande de remontée avec lettrage écartée (bas gauche)
    "salle-a-manger": ("08-salle-a-manger-1", None, [], None),
    "salle-a-manger-vue": ("60-photos-supplementaires", None, [], None),
    "salon": ("03-salon-2", None, [], None),
    "cuisine-bois": ("05-cuisine-equipee-1", None, [], None),
    "cuisine-blanche": ("06-cuisine-equipee-2", (430, 0, 1920, 1280), [], None),   # viennoiseries à gauche écartées
    "piscine": ("53-piscine", (422, 422, 1920, 1574), [], 0.4),         # peignoir brodé à gauche écarté ; natif 768 px
    "piscine-salon": ("54-piscine", (0, 600, 1920, 2040), [], 0.4),     # natif 768 px
    "chambre-1": ("14-chambre-1", None, [], None),
    "chambre-2": ("16-chambre-2", None, [], None),
    "chambre-3": ("15-chambre-1", None, [], None),
    "dortoir": ("23-chambre-9", None, [], None),
    "salle-de-bain": ("26-salle-de-bains-entiere-1", None, [], None),
    "hiver": ("36-arriere-cour", None, [], None),
    "terrasse": ("41-exterieur", None, [], None),
}
B = {
    "exterieur": ("01-photo", None, [(1095, 1108, 1200, 1175)], None),   # plaque ovale au-dessus de la porte floutée
    "salon": ("11-photo", None, [(1212, 950, 1312, 1050)], None),        # sac à logo sur la chaise floutée
    "cuisine": ("12-photo", None, [], None),
    "chambre-1": ("20-photo", (250, 412, 2100, 1800), [], None),         # médaillon de plafond en forme de croix écarté
    "chambre-2": ("17-photo", None, [], None),
    "chambre-3": ("21-photo", (375, 412, 2225, 1800), [], None),         # idem
    "chambre-4": ("24-photo", None, [], None),
    "salle-de-bain": ("16-photo", None, [], None),
    "jacuzzi": ("06-photo", None, [], None),
    "jacuzzi-cascade": ("05-photo", None, [], None),
    "detente": ("25-photo", None, [], None),
}
SERIES = (("a", A, "a-saint-gervais"), ("b", B, "b-courchevel"))


def fabriquer(cle, suffixe, spec, dossier):
    src, box, flous, echelle = spec
    p = CH[cle]
    im = ImageOps.exif_transpose(Image.open(REF / dossier / "photos" / f"{src}.jpg")).convert("RGB")
    if box:
        im = im.crop(box)
    for b in flous:
        z = im.crop(b).filter(ImageFilter.GaussianBlur(14))
        im.paste(z, b[:2])
    if echelle:
        im = im.resize((round(im.width * echelle), round(im.height * echelle)), Image.LANCZOS)
    elif im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    if cle == "b":
        im = ImageEnhance.Color(im).enhance(SAT_B)
    out = luxe(im)
    return out


if __name__ == "__main__":
    for cle, serie, dossier in SERIES:
        for suf, spec in serie.items():
            o = fabriquer(cle, suf, spec, dossier)
            clean = Image.new("RGB", o.size); clean.paste(o)   # aucune métadonnée
            nom = f"{CH[cle]['prefixe']}-{suf}"
            clean.save(ICI / "img" / "chalet" / f"{nom}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
            print(nom, o.size)
