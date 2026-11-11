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
    "piscine": ("51-piscine", (680, 400, 1920, 1280), [], None),        # personne et peignoirs brodés à gauche écartés ; fichier 1920 px net
    "salle-a-manger-vue": ("60-photos-supplementaires", None, [], None),
    "salon": ("03-salon-2", None, [], None),
    "cuisine-blanche": ("06-cuisine-equipee-2", (430, 0, 1920, 1280), [], None),   # viennoiseries à gauche écartées
    "chambre-1": ("14-chambre-1", None, [], None),
    "chambre-2": ("16-chambre-2", None, [], None),
    "chambre-3": ("15-chambre-1", None, [], None),
    "dortoir": ("23-chambre-9", None, [], None),
    "salle-de-bain": ("26-salle-de-bains-entiere-1", None, [], None),
    "hiver": ("36-arriere-cour", None, [], None),
    "terrasse": ("41-exterieur", None, [], None),
}
# 11/11 (relecture Opus) : coordonnées en pixels du fichier source 1920 x 1440 (la première version les avait saisies pour 2400 x 1800)
B = {
    "exterieur": ("01-photo", (160, 0, 1610, 880), [], None),             # 11/11 2e passage : cadrage large coupé juste au-dessus de la plaque (y 897-928), les deux sapins gardés ; 1450 x 880
    "cuisine": ("12-photo", (0, 0, 1400, 1050), [], None),               # sol à carreau en croix écarté
    "chambre-1": ("20-photo", (200, 330, 1680, 1440), [], None),         # médaillon de plafond en forme de croix écarté
    "chambre-2": ("17-photo", None, [], None),
    "chambre-3": ("21-photo", (300, 330, 1780, 1440), [], None),         # idem
    "chambre-4": ("13-photo", None, [], None),                           # remplace la chambre à tête de cerf (réserve B13)
    "salle-de-bain": ("19-photo", (0, 320, 1493, 1440), [], None),       # plafond octogonal écarté (réserve B19)
    "jacuzzi": ("06-photo", None, [], None),
    "jacuzzi-cascade": ("05-photo", None, [], None),
    "detente": ("25-photo", None, [], None),
}

# 11/11 (2e passage) : chalets C (Les Houches, vallée de Chamonix) et D (Les Deux Alpes, piscine). Recadrages calculés sur les dimensions RÉELLES des
# fichiers sources (1800 x 1200 pour C ; D : tailles variables, notées en commentaire). Chaque photo a été ouverte en pleine taille (controle-photos.csv).
# D : les fichiers portrait de 2560 px sont des agrandissements annonce de natifs de 1309 à 1321 px : le facteur d'échelle ramène la sortie à la largeur native.
C = {
    "exterieur": ("01-facade-jour", (650, 150, 1600, 1150), [], None),          # télécabine orange à gauche exclue ; 4e passage : statue de chamois en pierre (x>1610) exclue ; 950 x 1000
    "salon": ("52-salon-cheminee", (0, 371, 1800, 1200), [], None),             # 4e passage : livre « Evolène » sur la cheminée (y<350) exclu ; 1800 x 829
    "cuisine": ("13-cuisine", None, [], None),
    "suite": ("47-suite-parentale-lit", None, [], None),
    "chambre-ours": ("42-chambre-ours", (0, 380, 1200, 1280), [], None),         # portrait 1200 x 1800 recadré en 4:3
    "piscine": ("46-piscine-interieure-vue", (90, 0, 1710, 1012), [], None),     # 1800 x 1012 recadré en 1,6:1
    "bain-nordique": ("34-bain-nordique-coucher-soleil", (300, 110, 1200, 920), [], None),   # flûtes (x<290) et seau à champagne (x>1215) exclus
    "salle-de-bain": ("40-salle-de-bain-suite-parentale", None, [], None),
    "dortoir": ("09-dortoir-couloir", (0, 250, 1200, 1150), [], None),           # portrait 1200 x 1800 recadré en 4:3
    "facade-nuit": ("03-facade-nuit-allee", (720, 100, 1800, 1000), [], None),   # télécabine (x 650-700) exclue
    "salon-canapes": ("48-salon-canapes", None, [], None),
}
D = {
    "exterieur": ("52-exterieur", (160, 40, 1840, 1050), [], None),              # 1920 x 1280 : graffitis à gauche et benne en bas à droite exclus
    "salle-a-manger-vue": ("14-espace-repas", None, [], None),
    "salon": ("hd/D87_2125", (0, 0, 1321, 845), [], None),   # 5e passage, photo de studio du site du propriétaire (planche n° 28, 1321 x 1056 natif) : verres à pied et livre de la table basse (y>858) exclus ; foyer, banquette de fenêtre, bibliothèque gardés ; 1321 x 845, natif
    "chambre-1": ("21-chambre-3", (768, 1000, 2560, 2344), [], None),            # 2560 x 3413 ; 4e passage : livre « Une terre promise » de la niche (x<768) exclu ; 1792 x 1344
    "chambre-2": ("29-chambre-5", None, [], None),
    "chambre-3": ("33-chambre-6", (0, 1000, 2560, 2920), [], 1321 / 2560),       # 4e passage, réserve D33 (remplace D16 : livre « Une terre promise » dans la niche) : 2560 x 3841, natif ~1321
    "dortoir": ("19-chambre-2", (0, 513, 2560, 2433), [], None),                 # 2560 x 3413, natif 3024
    "piscine": ("53-piscine", None, [], None),
    "piscine-vue": ("54-piscine", (0, 0, 1860, 1707), [], 1981 / 2560),          # 2560 x 1707, natif 1981 : carafe et verre de la console (x>1880) exclus
    "salle-de-bain": ("40-salle-de-bains-entiere-1", (0, 1197, 2560, 3117), [], None),   # 2560 x 3413, natif 3024
    "salle-de-bain-2": ("41-salle-de-bains-entiere-2", None, [], None),
    "cinema": ("hd/D87_2264", (300, 0, 1922, 1282), [], None),   # 5e passage, studio (planche n° 33, 1922 x 1282 natif) : remplace la prise de téléphone sombre (annonce 07) ; gobelets sur la table d'appoint à gauche (x<300) exclus ; 1622 x 1282 réduit à 1600
    "facade-jour": ("hd/D87_1774", (0, 0, 1321, 1240), [], None),   # 5e passage, studio (planche n° 13, 1321 x 1321 natif) : ciel bleu, sans neige ; aucun lettrage ; chaussée du bas écartée ; 1321 x 1240, natif
}
SERIES = (("a", A, "a-saint-gervais"), ("b", B, "b-courchevel"), ("c", C, "c-les-houches"), ("d", D, "d-les-deux-alpes"))


def fabriquer(cle, suffixe, spec, dossier):
    src, box, flous, echelle = spec
    p = CH[cle]
    chemin = next(iter(sorted((REF / dossier / "photos-source-hd").glob(f"{src[3:]}_*.jpg")))) if src.startswith("hd/") else REF / dossier / "photos" / f"{src}.jpg"  # hd/ = préfixe du fichier du site du propriétaire
    im = ImageOps.exif_transpose(Image.open(chemin)).convert("RGB")
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
