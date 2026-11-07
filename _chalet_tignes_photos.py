# -*- coding: utf-8 -*-
"""Photos du chalet de Tignes (deux chalets mitoyens loués ensemble, clé ch9), 02/11/2026. Photos réelles de l'annonce du
propriétaire (1440 px), retouche légère seulement (luxe() de _aigle_royal_photos.py), sans métadonnées, jamais d'agrandissement.
Sources : 00-brief/references/2026-11-02-chalet-tignes/orig/NN.jpg (hors git, .gitignore local).
Le préfixe des fichiers vient de _chalet_tignes_nom.PREFIXE : changer le nom du chalet = changer NOM puis relancer.

Écartées (02/11) :
- 00, 11, 13, 14 : sculpture de femme nue dans le salon ou derrière la table (pudeur, clientèle religieuse) ; 14 a aussi
  une bouteille de champagne sur la table basse ;
- 26 : bouteille de champagne et flûtes sur un plateau posé sur le lit ;
- 28, 29, 33 : tables de petit déjeuner servies (charcuterie et fromages non casher sur 29, seau à glace sur 28, bouteille sur 33) ;
- 20 : tableau d'une femme épaules nues au mur de la chambre ;
- 15 : doublon de 04 ; 17, 18, 19 : été (produit d'hiver) ;
- 02, 24, 27 : façade côté rue avec porte de garage et poubelles (registre luxe) ;
- 22 : enseigne d'une résidence voisine lisible à droite, recadrée (x < 970) ; 23 : porte de garage en bas, recadrée (y < 770).
- 25 (salon) : table de petit déjeuner servie avec bouteilles à droite ; recadrée sur le salon et la cheminée (x < 1000).
- 05 (jacuzzi) : bouteille de champagne et flûtes sur le plateau, à gauche ; recadrée à droite du plateau (x >= 720) et sous la voiture garée au fond (y >= 430)."""
import pathlib
from PIL import Image, ImageOps
from _aigle_royal_photos import luxe
from _chalet_tignes_nom import PREFIXE

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parents[1] / "00-brief" / "references" / "2026-11-02-chalet-tignes" / "orig"

# suffixe -> (photo source, recadrage éventuel (x0, y0, x1, y1))
PHOTOS = {
    "exterieur-neige": ("22", (0, 0, 970, 1079)), "chalets-neige": ("21", None), "vue-aerienne": ("23", (0, 0, 1440, 770)),
    "terrasse-nuit": ("01", None),
    "jacuzzi": ("05", (720, 430, 1440, 961)),
    "sejour": ("07", None), "salon-cheminee": ("12", None), "salon": ("25", (0, 0, 1000, 961)), "salon-feu": ("32", None),
    "salle-a-manger": ("09", None), "cuisine": ("06", None),
    "suite-1": ("04", None), "suite-2": ("08", None), "suite-3": ("16", None), "suite-4": ("30", None), "suite-5": ("31", None),
    "suite-douche": ("10", None), "salle-de-bain": ("03", None),
}
STEMS = {k: f"{PREFIXE}-{k}" for k in PHOTOS}

if __name__ == "__main__":
    for k, (src, box) in PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(SRC / f"{src}.jpg")).convert("RGB")
        if box:
            im = im.crop(box)
        luxe(im).save(ICI / "img" / "chalet" / f"{STEMS[k]}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        print(STEMS[k], im.size)
