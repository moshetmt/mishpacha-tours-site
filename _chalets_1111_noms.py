# -*- coding: utf-8 -*-
"""Noms commerciaux des deux chalets du 11/11/2026, en un seul endroit. Noms PROVISOIRES (Moshé tranchera).
Changer un nom = changer NOM / NOM_HE ici, puis relancer dans l'ordre :
    python _chalets_1111_photos.py ; python _chalets_1111.py ;
    (apps-script/mendel) python catalogue_chalet.py ch12|ch13 en|fr|he ; python _chalets_1111_devis.py ; python build.py
Aucune URL, aucun nom de fichier image ou PDF ne contient le nom : slugs de fichiers = PREFIXE.
Ce module n'importe rien (les modules d'enregistrement _kit_wp, _galerie_chalets, _zones l'importent).
🛑 Aucun nom d'origine, d'hôte, d'agence, de hameau ni de rue dans ce dépôt public : la liste des interdits vit dans
00-brief/references/2026-11-11-chalets-*/interdits.txt (hors site)."""

CH = {
    "a": dict(
        slug="kosher-chalet-saint-gervais", prefixe="saint-gervais", cle="sg", ch="ch12",
        nom="Voie Lactée", nom_he="ווי לקטה", lieu="Saint-Gervais Mont-Blanc", lieu_he="סן ז'רווה מון בלאן",
        lieu_q="Saint-Gervais%20Mont-Blanc", svc="Saint-Gervais Mont-Blanc", catalogue="saint-gervais",
        coord="latitude=45.8920&longitude=6.7130",   # centre de Saint-Gervais-les-Bains (commune), pas l'adresse
        og_kicker="KOSHER CHALET · SAINT-GERVAIS MONT-BLANC",
    ),
    "b": dict(
        slug="kosher-chalet-courchevel-1850", prefixe="courchevel-1850", cle="c18", ch="ch13",
        nom="Lynx Doré", nom_he="לינקס דורה", lieu="Courchevel 1850", lieu_he="קורשבל 1850",
        lieu_q="Courchevel", svc="Courchevel", catalogue="courchevel-1850",
        coord="latitude=45.4154&longitude=6.6364",   # point Courchevel de la page station
        og_kicker="KOSHER CHALET · COURCHEVEL 1850",
    ),
}
ORDRE_CLES = ("a", "b")
