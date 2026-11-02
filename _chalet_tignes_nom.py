# -*- coding: utf-8 -*-
"""Nom commercial du chalet de Tignes (clé ch9), en un seul endroit. Proposition par défaut du 02/11 : « Étoile Polaire »,
à confirmer par Moshé. Changer le nom = changer NOM et NOM_HE ici, puis relancer dans l'ordre :
    python _chalet_tignes_photos.py ; python _chalet_tignes.py ;
    (apps-script/mendel) python catalogue_chalet.py ch9 en|fr|he ; remettre seulement ch9 dans chalets.json
    (d["ch9"] = {l: chalets_extraire.page("ch9", l)} : relancer tout chalets_extraire.py réécrit ch1 à ch8) ; python build.py
Translittération hébraïque sur le modèle des autres chalets (Belle Étoile = בל אטואל).
Restent écrits en dur (à changer à la main avec le nom) : apps-script/mendel/espace.html (CHALETS, CATALOGUES « etoile-polaire »,
GRILLE_VUE) et grille-mendel/grille.html (ligne ch9). Après un renommage, supprimer les anciens img/chalet/**/<prefixe>-* et
catalogues/<slug>-*, puis relancer _chalet_tignes.py (il retire et repose menu et cartes, mais les anciens fichiers restent)."""
import re
import unicodedata

NOM = "Étoile Polaire"
NOM_HE = "אטואל פולר"


def _ascii(x):
    return unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()


SLUG_CAT = re.sub(r"[^a-z0-9]+", "-", _ascii(NOM)).strip("-")   # etoile-polaire : nom des PDF du catalogue
PREFIXE = SLUG_CAT.split("-")[-1]                                 # polaire : préfixe des photos
