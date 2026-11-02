# -*- coding: utf-8 -*-
"""Lot 2 de Courchevel 1550, 02/11/2026 : chalets « Aurore Boréale » (3 suites, piscine chauffée) et « Renard Argenté » (2 suites,
bain nordique), noms choisis par Moshé. Même moteur que _chalet_aigle_royal.py (clone de la page Val Thorens publiée), cartes et
liens posés à côté de Flocon Doré, le chalet voisin. Idempotent.
🛑 Jamais le vrai nom des chalets, du hameau ni de l'exploitant. Prix « Sur demande » tant que les lignes ch7 et ch8 de la grille
de Mendel sont vides. Ensuite : _marcandou_photos.py doit avoir tourné. Lancer depuis site-v5 : python _chalets_courchevel_lot2.py"""
import html as H
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import _chalet_aigle_royal as A   # noqa: E402  (page(), jsonld(), index_md(), webp(), K, G)
import _chalets_textes_luxe as LUXE   # noqa: E402

K, G = A.K, A.G
LANGS = A.LANGS
pfx = A.pfx
COORD = "latitude=45.4154&longitude=6.6364"   # Courchevel, Shabbat Hebcal (même point que la page station)
CUISINE = {l: A.TX[l]["bref"][-1] for l in LANGS}
SHABBAT = {l: A.TX[l]["shabbat"] for l in LANGS}

COMMUN = {
 "en": dict(acces="<b>From Lyon-Saint-Exupéry.</b> About 2 h 15 to 2 h 30 by road. Geneva, about 2 h 30.", vt_lien="Chalet Flocon Doré, Courchevel",
            loc=("map-pin", "Location.", "In a private hamlet of Courchevel Village, at 1,550 metres, among the larch trees. The village centre and the snow front are 400 metres away; in winter, a shuttle takes you to the slopes."),
            pistes=("How far are the slopes?", "The village centre and the snow front are 400 metres away. In winter, a shuttle takes you to the slopes and back."),
            noms_lieu=[("Val Thorens", "Courchevel")], dispo="Availability is confirmed for your dates with each request."),
 "fr": dict(acces="<b>Depuis Lyon-Saint-Exupéry.</b> Environ 2 h 15 à 2 h 30 par la route. Depuis Genève, environ 2 h 30.", vt_lien="Chalet Flocon Doré, Courchevel",
            loc=("map-pin", "Situation.", "Dans un hameau privé de Courchevel Village, à 1 550 mètres, au milieu des mélèzes. Le centre du village et le front de neige sont à 400 mètres ; l'hiver, une navette vous conduit aux pistes."),
            pistes=("Les pistes sont-elles loin ?", "Le centre du village et le front de neige sont à 400 mètres. L'hiver, une navette vous conduit aux pistes et vous ramène."),
            noms_lieu=[("Val Thorens", "Courchevel")], dispo="La disponibilité est confirmée pour vos dates à chaque demande."),
 "es": dict(acces="<b>Desde Lyon-Saint-Exupéry.</b> Unas 2 h 15 a 2 h 30 por carretera. Desde Ginebra, unas 2 h 30.", vt_lien="Chalet Flocon Doré, Courchevel",
            loc=("map-pin", "Ubicación.", "En una aldea privada de Courchevel Village, a 1.550 metros, entre los alerces. El centro del pueblo y el frente de nieve están a 400 metros; en invierno, un servicio de traslado le lleva a las pistas."),
            pistes=("¿Están lejos las pistas?", "El centro del pueblo y el frente de nieve están a 400 metros. En invierno, un servicio de traslado le lleva a las pistas y le trae de vuelta."),
            noms_lieu=[("Val Thorens", "Courchevel")], dispo="La disponibilidad se confirma para sus fechas con cada solicitud."),
 "he": dict(acces="<b>מנמל התעופה ליון-סנט-אקזופרי.</b> כשעתיים ורבע עד שעתיים וחצי בנסיעה. מג'נבה, כשעתיים וחצי.", vt_lien="צ'אלה פלוקון דורה, קורשבל",
            loc=("map-pin", "מיקום.", "בכפר פרטי בקורשבל וילאז', בגובה 1,550 מטר, בין עצי הלגש. מרכז הכפר וחזית השלג במרחק 400 מטר; בחורף, הסעה לוקחת אתכם למסלולים."),
            pistes=("המסלולים רחוקים?", "מרכז הכפר וחזית השלג במרחק 400 מטר. בחורף, הסעה לוקחת אתכם למסלולים ומחזירה אתכם."),
            noms_lieu=[("בואל טורנס", "בקורשבל"), ("ואל טורנס", "קורשבל")], dispo="הזמינות מאושרת לתאריכים שלכם בכל פנייה."),
}
PRIX = {"en": ("From €{%s_basse_vente} per week", "Price on request"), "fr": ("À partir de {%s_basse_vente} € la semaine", "Prix sur demande"),
        "es": ("Desde {%s_basse_vente} € por semana", "Precio a consultar"), "he": ("החל מ־<bdi dir='ltr'>{%s_basse_vente} €</bdi> לשבוע", "מחיר לפי בקשה")}
ALT = {"en": "Chalet {n}", "fr": "Le Chalet {n}", "es": "El Chalet {n}", "he": "הצ'אלה בקורשבל"}

CHALETS = {
 "au": dict(slug="kosher-chalet-courchevel-aurore-boreale", ch="ch7", nom="Aurore Boréale", nom_he="אורור בוראל", t={
  "en": dict(title="Chalet Aurore Boréale, kosher, Courchevel",
             desc="Chalet Aurore Boréale in Courchevel: a private kosher chalet for 6 to 8 guests, 3 suites, heated outdoor pool, hammam and hot tub. Chef, Shabbat, minyan.",
             ital="3 suites, heated outdoor pool", hero="A stone and wood chalet in a private hamlet of Courchevel, among the larch trees.",
             intro="Three suites and a TV lounge that turns into a fourth bedroom, for 6 to 8 guests. A pool heated all year, a hammam and a hot tub. The village centre and the snow front are 400 metres away. Chef or delivered meals, Shabbat and minyan.",
             bref=[("x-couch", "The living room.", "Open and bright, with a hanging fireplace in the middle, a long wooden table for the meals and wide windows onto the trees. Two terraces face south."),
                   ("bed-double", "Three suites,", "each with its own bathroom: a bath with jets, a hammam shower, a bath and shower. The TV lounge turns into a fourth bedroom. A guest WC."),
                   ("waves", "Pool, hammam, hot tub.", "The outdoor pool is heated all year, with a counter-current to swim against. A hammam and a hot tub for the end of the ski day."),
                   ("snowflake", "Ski room.", "A ski room at the entrance, and parking with one covered space."),
                   ("check", "Comforts.", "Two floors, fibre wifi and a sound system in the rooms.")],
             apres="The chalet welcomes 6 to 8 guests.",
             faq=[("How many people can stay?", "6 to 8 guests: three suites, and the TV lounge turns into a fourth bedroom. One family, or two small families together."),
                  ("Is the pool heated in winter?", "Yes. The outdoor pool is heated all year, with a counter-current. A hammam and a hot tub complete it.")],
             web="Kosher chalet in Courchevel, 6 to 8 guests, heated pool and hammam",
             ld_desc="A private kosher chalet in Courchevel: three suites for 6 to 8 guests, an outdoor pool heated all year, a hammam and a hot tub, 400 m from the snow front. Chef or delivered meals, Shabbat and minyan."),
  "fr": dict(title="Chalet Aurore Boréale, casher, Courchevel",
             desc="Le Chalet Aurore Boréale à Courchevel : chalet casher privé pour 6 à 8 personnes, 3 suites, piscine extérieure chauffée, hammam et bain à remous. Chef, Chabbat, minyan.",
             ital="3 suites, piscine chauffée", hero="Un chalet de pierre et de bois dans un hameau privé de Courchevel, au milieu des mélèzes.",
             intro="Trois suites et un salon TV qui devient une quatrième chambre, pour 6 à 8 personnes. Une piscine chauffée toute l'année, un hammam et un bain à remous. Le centre du village et le front de neige sont à 400 mètres. Chef ou repas livrés, Chabbat et minyan.",
             bref=[("x-couch", "Le séjour.", "Ouvert et lumineux, avec une cheminée suspendue au centre, une longue table en bois pour les repas et de grandes baies sur les arbres. Deux terrasses plein sud."),
                   ("bed-double", "Trois suites,", "chacune avec sa salle de bain : balnéo, douche hammam, bain et douche. Le salon TV devient une quatrième chambre. Un WC invités."),
                   ("waves", "Piscine, hammam, bain à remous.", "La piscine extérieure est chauffée toute l'année, avec une nage à contre-courant. Un hammam et un bain à remous pour la fin de journée."),
                   ("snowflake", "Local à skis.", "Un local à skis à l'entrée, et un parking dont une place couverte."),
                   ("check", "Confort.", "Deux niveaux, wifi fibre et son dans les pièces.")],
             apres="Le chalet accueille 6 à 8 personnes.",
             faq=[("Combien de personnes peuvent séjourner ?", "6 à 8 personnes : trois suites, et le salon TV devient une quatrième chambre. Une famille, ou deux petites familles ensemble."),
                  ("La piscine est-elle chauffée l'hiver ?", "Oui. La piscine extérieure est chauffée toute l'année, avec une nage à contre-courant. Un hammam et un bain à remous la complètent.")],
             web="Chalet casher à Courchevel, 6 à 8 personnes, piscine chauffée et hammam",
             ld_desc="Un chalet casher privé à Courchevel : trois suites pour 6 à 8 personnes, une piscine extérieure chauffée toute l'année, un hammam et un bain à remous, à 400 m du front de neige. Chef ou repas livrés, Chabbat et minyan."),
  "es": dict(title="Chalet Aurore Boréale, kosher, Courchevel",
             desc="Chalet Aurore Boréale en Courchevel: chalet kosher privado para 6 a 8 personas, 3 suites, piscina exterior climatizada, hammam y jacuzzi. Chef, Shabat, minyán.",
             ital="3 suites, piscina climatizada", hero="Un chalet de piedra y madera en una aldea privada de Courchevel, entre los alerces.",
             intro="Tres suites y una sala de TV que se convierte en cuarto dormitorio, para 6 a 8 personas. Una piscina climatizada todo el año, un hammam y un jacuzzi. El centro del pueblo y el frente de nieve están a 400 metros. Chef o comidas a domicilio, Shabat y minyán.",
             bref=[("x-couch", "El salón.", "Abierto y luminoso, con una chimenea suspendida en el centro, una larga mesa de madera para las comidas y grandes ventanales hacia los árboles. Dos terrazas orientadas al sur."),
                   ("bed-double", "Tres suites,", "cada una con su baño: bañera de hidromasaje, ducha hammam, bañera y ducha. La sala de TV se convierte en cuarto dormitorio. Un aseo para invitados."),
                   ("waves", "Piscina, hammam, jacuzzi.", "La piscina exterior está climatizada todo el año, con nado contracorriente. Un hammam y un jacuzzi para el final del día."),
                   ("snowflake", "Guardaesquís.", "Un guardaesquís en la entrada, y aparcamiento con una plaza cubierta."),
                   ("check", "Comodidades.", "Dos plantas, wifi de fibra y sonido en las estancias.")],
             apres="El chalet recibe de 6 a 8 personas.",
             faq=[("¿Cuántas personas pueden alojarse?", "De 6 a 8 personas: tres suites, y la sala de TV se convierte en cuarto dormitorio. Una familia, o dos familias pequeñas juntas."),
                  ("¿La piscina está climatizada en invierno?", "Sí. La piscina exterior está climatizada todo el año, con nado contracorriente. Un hammam y un jacuzzi la completan.")],
             web="Chalet kosher en Courchevel, 6 a 8 personas, piscina climatizada y hammam",
             ld_desc="Un chalet kosher privado en Courchevel: tres suites para 6 a 8 personas, una piscina exterior climatizada todo el año, un hammam y un jacuzzi, a 400 m del frente de nieve. Chef o comidas a domicilio, Shabat y minyán."),
  "he": dict(title="צ'אלה אורור בוראל, קורשבל: כשרה, בריכה מחוממת",
             desc="צ'אלה אורור בוראל בקורשבל: צ'אלה כשרה פרטית ל-6 עד 8 אורחים, 3 סוויטות, בריכה חיצונית מחוממת, חמאם וג'קוזי. שף, שבת ומניין.",
             ital="3 סוויטות, בריכה מחוממת", hero="צ'אלה מאבן ומעץ בכפר פרטי בקורשבל, בין עצי הלגש.",
             intro="שלוש סוויטות וחדר טלוויזיה שהופך לחדר שינה רביעי, ל-6 עד 8 אורחים. בריכה מחוממת כל השנה, חמאם וג'קוזי. מרכז הכפר וחזית השלג במרחק 400 מטר. שף או ארוחות במשלוח, שבת ומניין.",
             bref=[("x-couch", "הסלון.", "פתוח ומואר, עם אח תלויה במרכז, שולחן עץ ארוך לארוחות וחלונות גדולים אל העצים. שתי מרפסות הפונות דרומה."),
                   ("bed-double", "שלוש סוויטות,", "לכל אחת חדר רחצה משלה: אמבט ג'קוזי, מקלחת חמאם, אמבטיה ומקלחת. חדר הטלוויזיה הופך לחדר שינה רביעי. שירותי אורחים."),
                   ("waves", "בריכה, חמאם וג'קוזי.", "הבריכה החיצונית מחוממת כל השנה, עם שחייה נגד הזרם. חמאם וג'קוזי לסוף יום הסקי."),
                   ("snowflake", "חדר סקי.", "חדר סקי בכניסה, וחניה עם מקום מקורה אחד."),
                   ("check", "נוחות.", "שתי קומות, Wi-Fi בסיבים ומערכת שמע בחדרים.")],
             apres="הצ'אלה מארחת 6 עד 8 אורחים.",
             faq=[("כמה אנשים יכולים להתארח?", "6 עד 8 אורחים: שלוש סוויטות, וחדר הטלוויזיה הופך לחדר שינה רביעי. משפחה אחת, או שתי משפחות קטנות יחד."),
                  ("הבריכה מחוממת בחורף?", "כן. הבריכה החיצונית מחוממת כל השנה, עם שחייה נגד הזרם, ולצדה חמאם וג'קוזי.")],
             web="צ'אלה כשרה בקורשבל, 6 עד 8 אורחים, בריכה מחוממת וחמאם",
             ld_desc="צ'אלה כשרה פרטית בקורשבל: שלוש סוויטות ל-6 עד 8 אורחים, בריכה חיצונית מחוממת כל השנה, חמאם וג'קוזי, 400 מטר מחזית השלג. שף או ארוחות במשלוח, שבת ומניין.")}),
 "re": dict(slug="kosher-chalet-courchevel-renard-argente", ch="ch8", nom="Renard Argenté", nom_he="רנאר ארז'נטה", t={
  "en": dict(title="Chalet Renard Argenté, kosher, Courchevel",
             desc="Chalet Renard Argenté in Courchevel: a private kosher chalet for 2 to 6 guests, 2 suites, an outdoor Nordic bath heated to 40 °C. Chef, Shabbat, minyan.",
             ital="2 suites, Nordic bath", hero="A small wood and stone chalet in a private hamlet of Courchevel, for a couple or a young family.",
             intro="Two suites and a sofa bed in the living room, for 2 to 6 guests. An outdoor Nordic bath heated to 40 °C, a wood stove, a home cinema. The village centre and the snow front are 400 metres away. Chef or delivered meals, Shabbat and minyan.",
             bref=[("x-couch", "The living room.", "Under the beams, with a wood stove, wide windows onto the mountains and a home cinema. The kitchen and the dining table are on the same floor."),
                   ("bed-double", "Two suites,", "each with its own bathroom, one with a walk-in shower. A sofa bed in the living room for two more guests. A guest WC."),
                   ("waves", "Nordic bath.", "A wooden bath outside, heated to 40 °C, on the landscaped terrace. A balcony on the other side."),
                   ("check", "Comforts.", "Two floors, safes, parking with one covered space.")],
             apres="The chalet welcomes 2 to 6 guests.",
             faq=[("How many people can stay?", "2 to 6 guests: two suites, and a sofa bed in the living room. A couple, or a family with young children."),
                  ("What is the Nordic bath?", "A wooden bath outside on the terrace, heated to 40 °C. You sit in hot water with the snow all around.")],
             web="Kosher chalet in Courchevel, 2 to 6 guests, Nordic bath",
             ld_desc="A private kosher chalet in Courchevel: two suites for 2 to 6 guests, an outdoor Nordic bath heated to 40 °C, a wood stove, 400 m from the snow front. Chef or delivered meals, Shabbat and minyan."),
  "fr": dict(title="Chalet Renard Argenté, casher, Courchevel",
             desc="Le Chalet Renard Argenté à Courchevel : chalet casher privé pour 2 à 6 personnes, 2 suites, bain nordique extérieur chauffé à 40 °C. Chef, Chabbat, minyan.",
             ital="2 suites, bain nordique", hero="Un petit chalet de bois et de pierre dans un hameau privé de Courchevel, pour un couple ou une jeune famille.",
             intro="Deux suites et un canapé-lit au salon, pour 2 à 6 personnes. Un bain nordique extérieur chauffé à 40 °C, un poêle à bois, un home cinéma. Le centre du village et le front de neige sont à 400 mètres. Chef ou repas livrés, Chabbat et minyan.",
             bref=[("x-couch", "Le séjour.", "Sous les poutres, avec un poêle à bois, de grandes baies sur les montagnes et un home cinéma. La cuisine et la table sont au même étage."),
                   ("bed-double", "Deux suites,", "chacune avec sa salle de bain, dont une douche à l'italienne. Un canapé-lit au salon pour deux personnes de plus. Un WC invités."),
                   ("waves", "Bain nordique.", "Un bain en bois à l'extérieur, chauffé à 40 °C, sur la terrasse paysagère. Un balcon de l'autre côté."),
                   ("check", "Confort.", "Deux niveaux, coffres-forts, parking dont une place couverte.")],
             apres="Le chalet accueille 2 à 6 personnes.",
             faq=[("Combien de personnes peuvent séjourner ?", "2 à 6 personnes : deux suites, et un canapé-lit au salon. Un couple, ou une famille avec de jeunes enfants."),
                  ("Qu'est-ce que le bain nordique ?", "Un bain en bois à l'extérieur, sur la terrasse, chauffé à 40 °C. On s'y assoit dans l'eau chaude, la neige tout autour.")],
             web="Chalet casher à Courchevel, 2 à 6 personnes, bain nordique",
             ld_desc="Un chalet casher privé à Courchevel : deux suites pour 2 à 6 personnes, un bain nordique extérieur chauffé à 40 °C, un poêle à bois, à 400 m du front de neige. Chef ou repas livrés, Chabbat et minyan."),
  "es": dict(title="Chalet Renard Argenté, kosher, Courchevel",
             desc="Chalet Renard Argenté en Courchevel: chalet kosher privado para 2 a 6 personas, 2 suites, baño nórdico exterior a 40 °C. Chef, Shabat, minyán.",
             ital="2 suites, baño nórdico", hero="Un pequeño chalet de madera y piedra en una aldea privada de Courchevel, para una pareja o una familia joven.",
             intro="Dos suites y un sofá cama en el salón, para 2 a 6 personas. Un baño nórdico exterior a 40 °C, una estufa de leña, un cine en casa. El centro del pueblo y el frente de nieve están a 400 metros. Chef o comidas a domicilio, Shabat y minyán.",
             bref=[("x-couch", "El salón.", "Bajo las vigas, con una estufa de leña, grandes ventanales hacia las montañas y un cine en casa. La cocina y la mesa están en la misma planta."),
                   ("bed-double", "Dos suites,", "cada una con su baño, una con ducha a ras de suelo. Un sofá cama en el salón para dos personas más. Un aseo para invitados."),
                   ("waves", "Baño nórdico.", "Una bañera de madera al aire libre, a 40 °C, en la terraza ajardinada. Un balcón al otro lado."),
                   ("check", "Comodidades.", "Dos plantas, cajas fuertes, aparcamiento con una plaza cubierta.")],
             apres="El chalet recibe de 2 a 6 personas.",
             faq=[("¿Cuántas personas pueden alojarse?", "De 2 a 6 personas: dos suites y un sofá cama en el salón. Una pareja, o una familia con niños pequeños."),
                  ("¿Qué es el baño nórdico?", "Una bañera de madera al aire libre, en la terraza, a 40 °C. Uno se sienta en el agua caliente, con la nieve alrededor.")],
             web="Chalet kosher en Courchevel, 2 a 6 personas, baño nórdico",
             ld_desc="Un chalet kosher privado en Courchevel: dos suites para 2 a 6 personas, un baño nórdico exterior a 40 °C, una estufa de leña, a 400 m del frente de nieve. Chef o comidas a domicilio, Shabat y minyán."),
  "he": dict(title="צ'אלה רנאר ארז'נטה, קורשבל: כשרה, אמבט נורדי",
             desc="צ'אלה רנאר ארז'נטה בקורשבל: צ'אלה כשרה פרטית ל-2 עד 6 אורחים, 2 סוויטות, אמבט נורדי חיצוני מחומם ל-40 מעלות. שף, שבת ומניין.",
             ital="2 סוויטות, אמבט נורדי", hero="צ'אלה קטנה מעץ ומאבן בכפר פרטי בקורשבל, לזוג או למשפחה צעירה.",
             intro="שתי סוויטות וספה נפתחת בסלון, ל-2 עד 6 אורחים. אמבט נורדי חיצוני מחומם ל-40 מעלות, תנור עצים וקולנוע ביתי. מרכז הכפר וחזית השלג במרחק 400 מטר. שף או ארוחות במשלוח, שבת ומניין.",
             bref=[("x-couch", "הסלון.", "תחת קורות העץ, עם תנור עצים, חלונות גדולים אל ההרים וקולנוע ביתי. המטבח ושולחן האוכל באותה קומה."),
                   ("bed-double", "שתי סוויטות,", "לכל אחת חדר רחצה משלה, ובאחת מקלחת ללא סף. ספה נפתחת בסלון לעוד שני אורחים. שירותי אורחים."),
                   ("waves", "אמבט נורדי.", "אמבט עץ בחוץ, מחומם ל-40 מעלות, על המרפסת המעוצבת. מרפסת נוספת בצד השני."),
                   ("check", "נוחות.", "שתי קומות, כספות, וחניה עם מקום מקורה אחד.")],
             apres="הצ'אלה מארחת 2 עד 6 אורחים.",
             faq=[("כמה אנשים יכולים להתארח?", "2 עד 6 אורחים: שתי סוויטות וספה נפתחת בסלון. זוג, או משפחה עם ילדים קטנים."),
                  ("מה זה אמבט נורדי?", "אמבט עץ בחוץ על המרפסת, מחומם ל-40 מעלות. יושבים במים חמים, והשלג מסביב.")],
             web="צ'אלה כשרה בקורשבל, 2 עד 6 אורחים, אמבט נורדי",
             ld_desc="צ'אלה כשרה פרטית בקורשבל: שתי סוויטות ל-2 עד 6 אורחים, אמבט נורדי חיצוני מחומם ל-40 מעלות, תנור עצים, 400 מטר מחזית השלג. שף או ארוחות במשלוח, שבת ומניין.")}),
}
H2_CO = {"en": ("Our chalets", "in Courchevel"), "fr": ("Nos chalets", "à Courchevel"), "es": ("Nuestros chalets", "en Courchevel"), "he": ("הצ'אלות שלנו", "בקורשבל")}
INTERDITS = ("marcandou", "ilulissat", "ikamiut", "sisimiut", "nuuk", "pinoncély", "pinoncely")


def tx(cle):
    c = CHALETS[cle]
    out = {}
    for l in LANGS:
        b, m = c["t"][l], COMMUN[l]
        nom = c["nom_he"] if l == "he" else c["nom"]
        out[l] = dict(b, bref=[m["loc"]] + b["bref"] + [CUISINE[l]], apres=b["apres"] + " " + m["dispo"], shabbat=SHABBAT[l], acces=m["acces"],
                      prix=(PRIX[l][0] % c["ch"], PRIX[l][1]), faq=[b["faq"][0], m["pistes"], b["faq"][1]],
                      alt=ALT[l].format(n=nom), vt_lien=m["vt_lien"], voisin="kosher-chalet-courchevel",
                      noms=([("בל אטואל", nom)] if l == "he" else [("Chalet Belle Étoile", "Chalet " + nom), ("Belle Étoile", nom)]) + m["noms_lieu"],
                      suite_noms=[("kosher-val-thorens/", "kosher-courchevel/")] + m["noms_lieu"], lieu_q="Courchevel", svc="Courchevel")
    return LUXE.appliquer(out, {"au": LUXE.AU, "re": LUXE.RE}[cle])


def regler(cle):
    """Règle le moteur de _chalet_aigle_royal.py sur ce chalet."""
    c = CHALETS[cle]
    A.SLUG, A.GC = c["slug"], G.CHALETS[c["slug"]]
    A.HERO = A.GC["hero"]
    A.STEMS = A.ORDRE = [s for _, _, ss in A.GC["pieces"] for s in ss]
    A.TX = tx(cle)
    A.COORD_AR = COORD
    A.DIM = {s: A.webp(s) for s in A.STEMS}


def carte(lang, cle):
    tpl, repli = PRIX[lang][0] % CHALETS[cle]["ch"], PRIX[lang][1]
    return K.carte(lang, cle).replace('<p class="kwp-dispo">', f'<p class="kwp-prix" data-prix-tpl="{A.attr_(tpl)}">{repli}</p><p class="kwp-dispo">', 1)


def apres_carte_co(bloc, lang):
    lien = f'href="{pfx(lang)}/kosher-chalet-courchevel/"'
    i = bloc.find(lien)
    while i >= 0 and bloc.rfind('<article class="kwp-carte', 0, i) < bloc.rfind("</article>", 0, i):
        i = bloc.find(lien, i + 1)
    j = bloc.find("</article>", i) + len("</article>")
    return bloc[:j] + carte(lang, "au") + carte(lang, "re") + bloc[j:]


def brancher():
    slugs = [c["slug"] for c in CHALETS.values()]
    n = 0
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = (r[len(lang) + 1:] if lang != "en" else r)[: -len("index.html")].strip("/")
        s = A.lire(p); o = s
        for sl in slugs:
            s = A.retirer(s, lang, sl)
        if f'class="nav-ch-v" href="{pfx(lang)}/{slugs[0]}/"' not in s:
            nav = ""
            for k, (u, img) in enumerate(K.CH_URL):
                if u in slugs:
                    b, d = K.NAV_CH[lang][2][k]
                    nav += (f'<a class="nav-ch-v" href="{pfx(lang)}/{u}/"><img src="{img}" alt="" width="96" height="64" loading="lazy">'
                            f'<span><b>{H.escape(b, quote=False)}</b>{H.escape(d, quote=False)}</span></a>')
            s = re.sub(rf'(<a class="nav-ch-v" href="{pfx(lang)}/kosher-chalet-courchevel/">.*?</a>)', lambda m: m.group(1) + nav, s, count=1, flags=re.S)
        s = s.replace('"kosher-chalet-les-menuires"];', '"kosher-chalet-les-menuires","' + '","'.join(slugs) + '"];')
        for nom in ("accueil", "hub", "duo", "co"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{pfx(lang)}/{slugs[0]}/"' not in m.group(0) and f'href="{pfx(lang)}/kosher-chalet-courchevel/"' in m.group(0):
                b = apres_carte_co(m.group(0), lang).replace("kwp-cartes kwp-cinq", "kwp-cartes kwp-six")
                if nom == "co":
                    b = b.replace("kwp-cartes kwp-seule", "kwp-cartes kwp-six")
                    b = re.sub(r"<h2>.*?</h2>", f"<h2>{H2_CO[lang][0]} <i>{H2_CO[lang][1]}</i></h2>", b, count=1, flags=re.S)
                s = s[:m.start()] + b + s[m.end():]
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug not in slugs and f'href="{pfx(lang)}/{slugs[0]}/"' not in m.group(0):
            sauf = slug if slug in [u for u, _ in K.CH_URL] else None
            s = s[:m.start()] + K.bloc("mini", K.mini(lang, sauf)) + s[m.end():]
        n += A.ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = A.lire(p); o = s
    for c in reversed(list(CHALETS.values())):
        if f"/{c['slug']}/" in s:
            continue
        for lang in ("", "fr/", "es/", "he/"):
            m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}kosher-chalet-courchevel/</loc>.*?</url>", s, flags=re.S)
            if m:
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>2026-11-02</lastmod>",
                              re.sub(r"(https://mishpachatours\.com/(?:(?:fr|es|he)/)?)kosher-chalet-courchevel/", r"\g<1>" + c["slug"] + "/", m.group(0)))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
    n = A.ecrire(p, s, o)
    p = ICI / "llms.txt"; s = A.lire(p); o = s
    lignes = s.split("\n")
    i = next(k for k, l in enumerate(lignes) if "/kosher-chalet-courchevel/" in l)
    ajout = {"au": "private kosher chalet in Courchevel, 6 to 8 guests, 3 suites, outdoor pool heated all year, hammam and hot tub; price on request.",
             "re": "private kosher chalet in Courchevel, 2 to 6 guests, 2 suites, outdoor Nordic bath at 40 °C; price on request."}
    for cle in ("re", "au"):
        c = CHALETS[cle]
        if f"/{c['slug']}/" not in s:
            lignes.insert(i + 1, f"- [Chalet {c['nom']}, kosher, Courchevel]({A.BASE}/{c['slug']}/): {ajout[cle]}")
    return n + A.ecrire(p, "\n".join(lignes), o)


if __name__ == "__main__":
    for cle in CHALETS:
        regler(cle)
        for lang in LANGS:
            dst = A.page(lang)
            h = A.lire(dst).lower()
            for mot in INTERDITS:
                assert mot not in h, (dst, mot)
            A.index_md(dst)
            print("page", dst.relative_to(ICI))
    print("pages branchées :", brancher())
    print("sitemap + llms :", sitemap_llms())
