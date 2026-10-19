# -*- coding: utf-8 -*-
"""Photos HD de Mendel (14/10, usage site autorisé) sur l'accueil (4 langues) et en galerie sur la page chalet (4 langues).
Les fichiers img/chalet/wp-*.jpg sont exportés depuis 00-brief/photos-winter-prestige-2026-10-14/hd/.
python _photos_winter_prestige.py   (idempotent)
"""
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent

ALT = {
    "en": dict(hero="Our chalet in Les Deux Alpes under a blue sky, carved balconies and deep snow",
               nuit="The chalet at night, lights on, a path dug through the snow",
               allee="The path to the chalet door between two walls of snow",
               table="The festive table set for Shabbat in the chalet",
               pistes="The slopes and the lifts seen from the chalet balcony"),
    "fr": dict(hero="Notre chalet aux Deux Alpes sous un ciel bleu, balcons sculptés et neige épaisse",
               nuit="Le chalet la nuit, lumières allumées, une allée creusée dans la neige",
               allee="L'allée vers la porte du chalet entre deux murs de neige",
               table="La table de fête dressée pour Chabbat dans le chalet",
               pistes="Les pistes et les remontées vues depuis le balcon du chalet"),
    "es": dict(hero="Nuestro chalé en Les Deux Alpes bajo un cielo azul, balcones tallados y nieve profunda",
               nuit="El chalé de noche, con las luces encendidas y un sendero abierto en la nieve",
               allee="El camino hacia la puerta del chalé entre dos muros de nieve",
               table="La mesa de fiesta puesta para Shabat en el chalé",
               pistes="Las pistas y los remontes vistos desde el balcón del chalé"),
    "he": dict(hero="הצ'אלה שלנו בלה דז אלפ תחת שמיים כחולים, מרפסות מגולפות ושלג עמוק",
               nuit="הצ'אלה בלילה, האורות דולקים, שביל חפור בשלג",
               allee="השביל אל דלת הצ'אלה בין שתי חומות שלג",
               table="שולחן החג ערוך לשבת בצ'אלה",
               pistes="המסלולים והרכבלים כפי שנראים ממרפסת הצ'אלה"),
}

GALERIE = {
    "en": [("wp-ext-bleu", "The chalet under a blue sky, the morning after a snowfall"), ("wp-soleil", "Fresh snow on the terrace, the massif in the sun"),
           ("wp-nuit", "Evening at the chalet"), ("wp-neige-tombe", "Snow falling, seen from the shelter"),
           ("wp-table-fete", "The Shabbat table"),
           ("wp-guacamole", "Guacamole with edible flowers, by the chef"), ("wp-siddour", "A siddur on the balcony rail"),
           ("wp-balcon-detail", "The carved balconies")],
    "fr": [("wp-ext-bleu", "Le chalet sous un ciel bleu, le lendemain d'une chute de neige"), ("wp-soleil", "Neige fraîche sur la terrasse, le massif au soleil"),
           ("wp-nuit", "Le soir au chalet"), ("wp-neige-tombe", "La neige qui tombe, vue de l'abri"),
           ("wp-table-fete", "La table de Chabbat"),
           ("wp-guacamole", "Guacamole aux fleurs comestibles, par le chef"), ("wp-siddour", "Un siddour sur la rambarde du balcon"),
           ("wp-balcon-detail", "Les balcons sculptés")],
    "es": [("wp-ext-bleu", "El chalé bajo un cielo azul, la mañana después de una nevada"), ("wp-soleil", "Nieve fresca en la terraza, el macizo al sol"),
           ("wp-nuit", "La noche en el chalé"), ("wp-neige-tombe", "La nieve cayendo, vista desde el refugio"),
           ("wp-table-fete", "La mesa de Shabat"),
           ("wp-guacamole", "Guacamole con flores comestibles, del chef"), ("wp-siddour", "Un sidur en la barandilla del balcón"),
           ("wp-balcon-detail", "Los balcones tallados")],
    "he": [("wp-ext-bleu", "הצ'אלה תחת שמיים כחולים, בבוקר שאחרי השלג"), ("wp-soleil", "שלג טרי על המרפסת, ההרים בשמש"),
           ("wp-nuit", "ערב בצ'אלה"), ("wp-neige-tombe", "שלג יורד, מבט מהמחסה"),
           ("wp-table-fete", "שולחן השבת"),
           ("wp-guacamole", "גוואקמולי עם פרחי מאכל, של השף"), ("wp-siddour", "סידור על מעקה המרפסת"),
           ("wp-balcon-detail", "המרפסות המגולפות")],
}


def accueil(lang):
    p = ICI / ("index.html" if lang == "en" else f"{lang}/index.html")
    h = p.read_text(encoding="utf-8")
    pre = "img/" if lang == "en" else "/img/"
    a = ALT[lang]
    n = 0
    # hero
    h, k = re.subn(r'<img src="%schalet/(?:dining|wp-ext-bleu)\.jpg" alt="[^"]*" width="1800" height="1350" fetchpriority="high">' % re.escape(pre),
                   f'<img src="{pre}chalet/wp-ext-bleu.jpg" alt="{a["hero"]}" width="1800" height="1350" fetchpriority="high">', h); n += k
    # carte « chalet » des portes
    h, k = re.subn(r'<img src="%schalet/(?:living|wp-nuit)\.jpg" alt="" loading="lazy">' % re.escape(pre),
                   f'<img src="{pre}chalet/wp-nuit.jpg" alt="" loading="lazy">', h); n += k
    # bloc chalet : grande + 2 petites
    h, k = re.subn(r'<img class="grande" src="%schalet/(?:living|wp-allee)\.jpg" alt="[^"]*" width="\d+" height="\d+" loading="lazy">' % re.escape(pre),
                   f'<img class="grande" src="{pre}chalet/wp-allee.jpg" alt="{a["allee"]}" width="1600" height="1600" loading="lazy">', h); n += k
    h, k = re.subn(r'<img src="%schalet/(?:bedroom-crib|wp-table-fete)\.jpg" alt="[^"]*" width="\d+" height="\d+" loading="lazy">' % re.escape(pre),
                   f'<img src="{pre}chalet/wp-table-fete.jpg" alt="{a["table"]}" width="1600" height="1600" loading="lazy">', h); n += k
    h, k = re.subn(r'<img src="%schalet/(?:view|wp-pistes-balcon)\.jpg" alt="[^"]*" width="\d+" height="\d+" loading="lazy">' % re.escape(pre),
                   f'<img src="{pre}chalet/wp-pistes-balcon.jpg" alt="{a["pistes"]}" width="1600" height="1600" loading="lazy">', h); n += k
    assert n == 5 or 'class="ss wrap ac-chalet"' not in h, (lang, n)   # 19/10 : bloc ac-chalet remplacé par les cartes KIT-WP:accueil
    p.write_text(h, encoding="utf-8")
    print("accueil", lang, n)


TITRE_GAL = {"en": "The chalet in pictures", "fr": "Le chalet en images", "es": "El chalé en imágenes", "he": "הצ'אלה בתמונות"}


def chalet(lang):
    """Galerie en rail (20/10, Moshé : « très moche » en mosaïque sous la bannière) : une rangée à faire glisser sur téléphone,
       grille de 3 sur ordinateur, légende sous la photo, placée APRÈS les cartes « Where you sleep », jamais sous la bannière."""
    p = ICI / ("kosher-chalet-les-deux-alpes/index.html" if lang == "en" else f"{lang}/kosher-chalet-les-deux-alpes/index.html")
    h = p.read_text(encoding="utf-8")
    pre = "../img/" if lang == "en" else "/img/"
    figs = "".join(f'<figure><img src="{pre}chalet/{f}.jpg" alt="{c}" loading="lazy" width="1600" height="1200"><figcaption>{c}</figcaption></figure>'
                   for f, c in GALERIE[lang])
    bloc = f'<section class="ss wrap galerie-wp"><h2>{TITRE_GAL[lang]}</h2><div class="galerie-rail">{figs}</div></section>'
    h = re.sub(r'\n?<div class="ss wrap galerie-wp">.*?</div></div>', "", h, count=1, flags=re.S)   # ancienne mosaique sous la banniere
    h = re.sub(r'\n?<section class="ss wrap galerie-wp">.*?</section>', "", h, count=1, flags=re.S)
    j = h.find('<section class="ss wrap lead-offre">')
    assert j >= 0, "section lead-offre introuvable"
    i = h.find("</section>", j) + len("</section>")
    h = h[:i] + "\n" + bloc + h[i:]
    p.write_text(h, encoding="utf-8")
    print("chalet", lang, len(GALERIE[lang]), "photos")


for lang in ("en", "fr", "es", "he"):
    accueil(lang)
    chalet(lang)
