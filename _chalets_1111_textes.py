# -*- coding: utf-8 -*-
"""Textes des deux chalets du 11/11/2026, 4 langues. Registre luxe sobre, phrases courtes, rien qui ne soit dans la fiche
(00-brief/references/2026-11-11-chalets-*/*/fiche.md) : ni surface, ni altitude, ni distance, ni classement, ni nombre de lits.
Capacités et chambres : UN seul dictionnaire (FAITS) qui alimente la fiche, la carte, le JSON-LD, le catalogue et chalets.json.
Toutes les chaînes hébraïques neuves de la session sont ici (liste HE_NEUF en bas, pour la relecture)."""
from _chalets_1111_noms import CH

FAITS = {
    "a": dict(personnes=16, chambres=8, dortoirs=2, cuisines=2, piscine="28"),
    "b": dict(personnes=10, chambres=5, sdb=5),
}
NA, NB = CH["a"]["nom"], CH["b"]["nom"]
HA, HB = CH["a"]["nom_he"], CH["b"]["nom_he"]

# ligne « cuisine » : A a deux cuisines (viande et lait séparés), B garde la ligne commune (une cuisine à cachériser)
CUISINE_A = {
    "en": ("chef-hat", "Two kitchens.", "Meat and dairy stay apart. Kashered by our team before you arrive, included. A chef cooks in the chalet, or kosher meals arrive ready to reheat."),
    "fr": ("chef-hat", "Deux cuisines.", "La viande et le lait restent séparés. Cachérisées par notre équipe avant votre arrivée, incluses. Un chef cuisine au chalet, ou des repas casher arrivent prêts à réchauffer."),
    "es": ("chef-hat", "Dos cocinas.", "La carne y la leche permanecen separadas. Kosherizadas por nuestro equipo antes de su llegada, incluidas. Un chef cocina en el chalet, o las comidas kosher llegan listas para calentar."),
    "he": ("chef-hat", "שני מטבחים.", "בשר וחלב נשארים נפרדים. מוכשרים בידי הצוות שלנו לפני שתגיעו, כלול במחיר. שף מבשל בצ'אלה, או שארוחות כשרות מגיעות מוכנות לחימום."),
}
SHABBAT = {
    "en": "The chef cooks your weekday, Shabbat and holiday meals in the chalet, or your meals are delivered; for Shabbat, they arrive before candle lighting. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your group, Shacharis takes place in your living room.",
    "fr": "Le chef prépare au chalet vos repas de la semaine, de Chabbat et des fêtes, ou vos repas sont livrés ; pour Chabbat, ils arrivent avant l'allumage des bougies. Pour un minyan, nous amenons les ba'hourim et un Séfer Torah : avec les hommes de votre groupe, Cha'harit a lieu dans votre salon.",
    "es": "El chef prepara en el chalet sus comidas de la semana, de Shabat y de las fiestas, o sus comidas llegan ya preparadas; para Shabat, antes del encendido de las velas. Para un minyán, traemos a los bojurim y un Séfer Torá: con los hombres de su grupo, Shajarit se reza en su salón.",
    "he": "השף מכין בצ'אלה את הארוחות שלכם בימי החול, בשבת ובחגים, או שהארוחות מגיעות אליכם במשלוח; לשבת הן מגיעות לפני הדלקת הנרות. למניין אנחנו מביאים בחורים וספר תורה: עם הגברים של הקבוצה שלכם, תפילת שחרית נערכת בסלון שלכם.",
}
ACCES = {
    "en": "<b>From the airport.</b> Transfers from Geneva or Lyon-Saint-Exupéry can be arranged on request.",
    "fr": "<b>Depuis l'aéroport.</b> Les transferts depuis Genève ou Lyon-Saint-Exupéry s'organisent sur demande.",
    "es": "<b>Desde el aeropuerto.</b> Los traslados desde Ginebra o Lyon-Saint-Exupéry se organizan a petición.",
    "he": "<b>מנמל התעופה.</b> אפשר לארגן הסעה מג'נבה או מליון-סנט-אקזופרי לפי בקשה.",
}
DISPO = {"en": "Availability is confirmed for your dates with each request.", "fr": "La disponibilité est confirmée pour vos dates à chaque demande.",
         "es": "La disponibilidad se confirma para sus fechas con cada solicitud.", "he": "הזמינות מאושרת לתאריכים שלכם בכל פנייה."}

T = {
 "a": {
  "en": dict(title=f"Kosher Chalet {NA}, Saint-Gervais",
             desc=f"Chalet {NA} in Saint-Gervais Mont-Blanc: private kosher chalet, 16 guests, indoor heated pool, sauna, two kitchens. Chef, Shabbat, minyan.",
             ital="Saint-Gervais, indoor heated pool", hero="A chalet facing the Mont Blanc range, with an indoor heated pool, for up to 16 guests.",
             intro="Eight bedrooms, each with its own bathroom, and two children's dormitories, for up to 16 guests. An indoor pool heated all year, a sauna, a cinema room, a fireplace and a garage. Two kitchens: meat and dairy stay apart. Chef or delivered meals, Shabbat and minyan.",
             loc=("map-pin", "Location.", "Saint-Gervais Mont-Blanc, facing the Mont Blanc range. The chalet is a few steps from the ski lifts."),
             bref=[("x-couch", "The living room.", "Large sofas around the fireplace, a long dining table and the Mont Blanc range through the picture windows."),
                   ("bed-double", "Eight bedrooms,", "each with its own bathroom: two master rooms, two parental suites with a children's dormitory, four double rooms."),
                   ("waves", "Pool and sauna.", "An indoor pool heated to 28 °C all year, with a sauna beside it."),
                   ("sparkles", "Cinema and games.", "A private cinema room, and a games room with a table football for the children."),
                   ("snowflake", "Ski room and garage.", "A ski room with heated lockers, and a private garage.")],
             apres="The chalet welcomes up to 16 guests.",
             faq=[("How many people can stay?", "Up to 16 guests: eight bedrooms, each with its own bathroom, and two children's dormitories. One large family, or several families together."),
                  ("Is the pool heated in winter?", "Yes. The indoor pool is heated to 28 °C all year, with a sauna beside it.")],
             pistes=("Are the slopes far?", "The chalet is a few steps from the ski lifts. Access to the slopes is confirmed with each request."),
             web="Kosher chalet in Saint-Gervais Mont-Blanc, up to 16 guests, indoor heated pool",
             ld_desc="A private kosher chalet in Saint-Gervais Mont-Blanc: eight bedrooms for up to 16 guests, an indoor pool heated all year, a sauna, a cinema room and two kitchens. Chef or delivered meals, Shabbat and minyan.",
             alt=f"Chalet {NA}", carte=dict(lieu="Saint-Gervais Mont-Blanc", t=f"Chalet {NA}, Saint-Gervais", alt=f"Chalet {NA} in Saint-Gervais Mont-Blanc at dusk",
                                          s=[("8", "bedrooms"), ("Up to 16", "guests"), ("Indoor pool", "heated"), ("2", "kitchens")]),
             nav=(f"Chalet {NA} · Saint-Gervais", "8 bedrooms · indoor heated pool")),
  "fr": dict(title=f"Chalet {NA}, casher, Saint-Gervais",
             desc=f"Le Chalet {NA} à Saint-Gervais Mont-Blanc : chalet casher, 16 personnes, piscine intérieure chauffée, sauna, deux cuisines. Chef, Chabbat, minyan.",
             ital="Saint-Gervais, piscine intérieure chauffée", hero="Un chalet face au massif du Mont-Blanc, avec une piscine intérieure chauffée, jusqu'à 16 personnes.",
             intro="Huit chambres avec leur salle de bain et deux dortoirs d'enfants, jusqu'à 16 personnes. Une piscine intérieure chauffée toute l'année, un sauna, une salle de cinéma, une cheminée et un garage. Deux cuisines : la viande et le lait restent séparés. Chef ou repas livrés, Chabbat et minyan.",
             loc=("map-pin", "Situation.", "Saint-Gervais Mont-Blanc, face au massif du Mont-Blanc. Le chalet est à deux pas des remontées mécaniques."),
             bref=[("x-couch", "Le séjour.", "De grands canapés autour de la cheminée, une longue table et le massif du Mont-Blanc dans les baies vitrées."),
                   ("bed-double", "Huit chambres,", "chacune avec sa salle de bain : deux chambres master, deux suites parentales avec un dortoir pour les enfants, quatre chambres doubles."),
                   ("waves", "Piscine et sauna.", "Une piscine intérieure chauffée à 28 °C toute l'année, avec un sauna à côté."),
                   ("sparkles", "Cinéma et jeux.", "Une salle de cinéma privée, et une salle de jeux avec un baby-foot pour les enfants."),
                   ("snowflake", "Local à skis et garage.", "Un local à skis avec placards chauffants, et un garage privatif.")],
             apres="Le chalet accueille jusqu'à 16 personnes.",
             faq=[("Combien de personnes peuvent séjourner ?", "Jusqu'à 16 personnes : huit chambres avec leur salle de bain, et deux dortoirs d'enfants. Une grande famille, ou plusieurs familles ensemble."),
                  ("La piscine est-elle chauffée l'hiver ?", "Oui. La piscine intérieure est chauffée à 28 °C toute l'année, avec un sauna à côté.")],
             pistes=("Les pistes sont-elles loin ?", "Le chalet est à deux pas des remontées mécaniques. L'accès aux pistes est confirmé à chaque demande."),
             web="Chalet casher à Saint-Gervais Mont-Blanc, jusqu'à 16 personnes, piscine intérieure chauffée",
             ld_desc="Un chalet casher privé à Saint-Gervais Mont-Blanc : huit chambres jusqu'à 16 personnes, une piscine intérieure chauffée toute l'année, un sauna, une salle de cinéma et deux cuisines. Chef ou repas livrés, Chabbat et minyan.",
             alt=f"Le Chalet {NA}", carte=dict(lieu="Saint-Gervais Mont-Blanc", t=f"Chalet {NA}, Saint-Gervais", alt=f"Le Chalet {NA} à Saint-Gervais Mont-Blanc au crépuscule",
                                          s=[("8", "chambres"), ("Jusqu'à 16", "personnes"), ("Piscine", "intérieure chauffée"), ("2", "cuisines")]),
             nav=(f"Chalet {NA} · Saint-Gervais", "8 chambres · piscine intérieure chauffée")),
  "es": dict(title=f"Chalet {NA}, kosher, Saint-Gervais",
             desc=f"Chalet {NA} en Saint-Gervais Mont-Blanc: chalet kosher privado, 16 personas, piscina interior climatizada, sauna, dos cocinas. Chef, Shabat, minyán.",
             ital="Saint-Gervais, piscina interior climatizada", hero="Un chalet frente al macizo del Mont Blanc, con piscina interior climatizada, hasta 16 personas.",
             intro="Ocho habitaciones, cada una con su baño, y dos dormitorios colectivos para niños, hasta 16 personas. Una piscina interior climatizada todo el año, una sauna, una sala de cine, una chimenea y un garaje. Dos cocinas: la carne y la leche permanecen separadas. Chef o comidas a domicilio, Shabat y minyán.",
             loc=("map-pin", "Ubicación.", "Saint-Gervais Mont-Blanc, frente al macizo del Mont Blanc. El chalet está a pocos pasos de los remontes."),
             bref=[("x-couch", "El salón.", "Grandes sofás alrededor de la chimenea, una larga mesa y el macizo del Mont Blanc en los ventanales."),
                   ("bed-double", "Ocho habitaciones,", "cada una con su baño: dos habitaciones master, dos suites parentales con un dormitorio colectivo para niños, cuatro habitaciones dobles."),
                   ("waves", "Piscina y sauna.", "Una piscina interior climatizada a 28 °C todo el año, con una sauna al lado."),
                   ("sparkles", "Cine y juegos.", "Una sala de cine privada, y una sala de juegos con futbolín para los niños."),
                   ("snowflake", "Guardaesquís y garaje.", "Un guardaesquís con armarios calefactados, y un garaje privado.")],
             apres="El chalet recibe hasta 16 personas.",
             faq=[("¿Cuántas personas pueden alojarse?", "Hasta 16 personas: ocho habitaciones, cada una con su baño, y dos dormitorios colectivos para niños. Una familia grande, o varias familias juntas."),
                  ("¿La piscina está climatizada en invierno?", "Sí. La piscina interior está climatizada a 28 °C todo el año, con una sauna al lado.")],
             pistes=("¿Están lejos las pistas?", "El chalet está a pocos pasos de los remontes. El acceso a las pistas se confirma con cada solicitud."),
             web="Chalet kosher en Saint-Gervais Mont-Blanc, hasta 16 personas, piscina interior climatizada",
             ld_desc="Un chalet kosher privado en Saint-Gervais Mont-Blanc: ocho habitaciones hasta 16 personas, una piscina interior climatizada todo el año, una sauna, una sala de cine y dos cocinas. Chef o comidas a domicilio, Shabat y minyán.",
             alt=f"El Chalet {NA}", carte=dict(lieu="Saint-Gervais Mont-Blanc", t=f"Chalet {NA}, Saint-Gervais", alt=f"El Chalet {NA} en Saint-Gervais Mont-Blanc al anochecer",
                                          s=[("8", "habitaciones"), ("Hasta 16", "personas"), ("Piscina", "interior climatizada"), ("2", "cocinas")]),
             nav=(f"Chalet {NA} · Saint-Gervais", "8 habitaciones · piscina interior climatizada")),
  "he": dict(title=f"צ'אלה {HA}, סן ז'רווה: כשרה, בריכה מקורה מחוממת",
             desc=f"צ'אלה {HA} בסן ז'רווה מון בלאן: צ'אלה כשרה פרטית עד 16 אורחים, בריכה מקורה מחוממת, סאונה, חדר קולנוע ושני מטבחים. שף, שבת ומניין.",
             ital="סן ז'רווה, בריכה מקורה מחוממת", hero="צ'אלה מול רכס מון בלאן, עם בריכה מקורה מחוממת, עד 16 אורחים.",
             intro="שמונה חדרי שינה, לכל אחד חדר רחצה משלו, ושני חדרי שינה משותפים לילדים, עד 16 אורחים. בריכה מקורה מחוממת כל השנה, סאונה, חדר קולנוע, אח וחניון. שני מטבחים: בשר וחלב נשארים נפרדים. שף או ארוחות במשלוח, שבת ומניין.",
             loc=("map-pin", "מיקום.", "סן ז'רווה מון בלאן, מול רכס מון בלאן. הצ'אלה במרחק צעדים ספורים ממעליות הסקי."),
             bref=[("x-couch", "הסלון.", "ספות גדולות סביב האח, שולחן אוכל ארוך ורכס מון בלאן מבעד לחלונות הגדולים."),
                   ("bed-double", "שמונה חדרי שינה,", "לכל אחד חדר רחצה משלו: שני חדרי הורים ראשיים, שתי סוויטות הורים עם חדר שינה משותף לילדים, וארבעה חדרים זוגיים."),
                   ("waves", "בריכה וסאונה.", "בריכה מקורה מחוממת ל-28 מעלות כל השנה, ולידה סאונה."),
                   ("sparkles", "קולנוע ומשחקים.", "חדר קולנוע פרטי, וחדר משחקים עם שולחן כדורגל לילדים."),
                   ("snowflake", "חדר סקי וחניון.", "חדר סקי עם ארונות מחוממים, וחניון פרטי.")],
             apres="הצ'אלה מארחת עד 16 אורחים.",
             faq=[("כמה אנשים יכולים להתארח?", "עד 16 אורחים: שמונה חדרי שינה, לכל אחד חדר רחצה משלו, ושני חדרי שינה משותפים לילדים. משפחה גדולה אחת, או כמה משפחות יחד."),
                  ("הבריכה מחוממת בחורף?", "כן. הבריכה המקורה מחוממת ל-28 מעלות כל השנה, ולידה סאונה.")],
             pistes=("המסלולים רחוקים?", "הצ'אלה במרחק צעדים ספורים ממעליות הסקי. הגישה למסלולים מאושרת בכל פנייה."),
             web="צ'אלה כשרה בסן ז'רווה מון בלאן, עד 16 אורחים, בריכה מקורה מחוממת",
             ld_desc="צ'אלה כשרה פרטית בסן ז'רווה מון בלאן: שמונה חדרי שינה עד 16 אורחים, בריכה מקורה מחוממת כל השנה, סאונה, חדר קולנוע ושני מטבחים. שף או ארוחות במשלוח, שבת ומניין.",
             alt="הצ'אלה בסן ז'רווה", carte=dict(lieu="סן ז'רווה מון בלאן", t=f"צ'אלה {HA}, סן ז'רווה", alt=f"צ'אלה {HA} בסן ז'רווה מון בלאן בשעת בין ערביים",
                                          s=[("8", "חדרי שינה"), ("עד 16", "אורחים"), ("בריכה מקורה", "מחוממת"), ("2", "מטבחים")]),
             nav=(f"צ'אלה {HA} · סן ז'רווה", "8 חדרי שינה · בריכה מקורה מחוממת")),
 },
 "b": {
  "en": dict(title=f"Kosher Chalet {NB}, Courchevel 1850",
             desc=f"Chalet {NB} in Courchevel 1850: a private kosher chalet for up to 10 guests, five bedrooms, a stone hot tub and a hammam. Chef, Shabbat, minyan.",
             ital="Courchevel 1850, stone hot tub and hammam", hero="A wood and stone chalet in Courchevel 1850, near the ski lifts, for up to 10 guests.",
             intro="Five bedrooms and five bathrooms for up to 10 guests, on three levels. A spa with a stone hot tub and a hammam, a living room with a large fireplace opening onto the terrace, a ski room. Chef or delivered meals, Shabbat and minyan.",
             loc=("map-pin", "Location.", "In Courchevel 1850, near the ski lifts."),
             bref=[("x-couch", "The living room.", "A large fireplace and a way out to the terrace, a dining area with a large table, and a separate kitchen."),
                   ("bed-double", "Five bedrooms,", "four on the lower level and one under the eaves, with double or twin beds. Five bathrooms, and a TV corner under the roof."),
                   ("waves", "Spa.", "A stone hot tub and a hammam on the lower level, with a shower beside them. There is no pool."),
                   ("snowflake", "Ski room.", "A ski room, a laundry room, and free parking on site.")],
             apres="The chalet welcomes up to 10 guests.",
             faq=[("How many people can stay?", "Up to 10 guests: five bedrooms with double or twin beds, and five bathrooms. One family, or two families together."),
                  ("What is in the spa?", "A stone hot tub and a hammam, with a shower, on the lower level. There is no pool.")],
             pistes=("Are the slopes far?", "The chalet is near the ski lifts of Courchevel 1850. Access to the slopes is confirmed with each request."),
             web="Kosher chalet in Courchevel 1850, up to 10 guests, stone hot tub and hammam",
             ld_desc="A private kosher chalet in Courchevel 1850: five bedrooms for up to 10 guests, a stone hot tub and a hammam, a fireplace, near the ski lifts. Chef or delivered meals, Shabbat and minyan.",
             alt=f"Chalet {NB}", carte=dict(lieu="Courchevel 1850", t=f"Chalet {NB}, Courchevel 1850", alt=f"Chalet {NB} in Courchevel 1850 under the snow",
                                          s=[("5", "bedrooms"), ("Up to 10", "guests"), ("Hot tub", "and hammam"), ("Near", "the ski lifts")]),
             nav=(f"Chalet {NB} · Courchevel 1850", "5 bedrooms · hot tub and hammam")),
  "fr": dict(title=f"Chalet {NB}, casher, Courchevel 1850",
             desc=f"Le Chalet {NB} à Courchevel 1850 : chalet casher privé jusqu'à 10 personnes, cinq chambres, jacuzzi en pierre et hammam. Chef, Chabbat, minyan.",
             ital="Courchevel 1850, jacuzzi en pierre et hammam", hero="Un chalet de bois et de pierre à Courchevel 1850, près des remontées mécaniques, jusqu'à 10 personnes.",
             intro="Cinq chambres et cinq salles de bain pour 10 personnes, sur trois niveaux. Un spa avec jacuzzi en pierre et hammam, un salon avec une grande cheminée qui ouvre sur la terrasse, un local à skis. Chef ou repas livrés, Chabbat et minyan.",
             loc=("map-pin", "Situation.", "À Courchevel 1850, près des remontées mécaniques."),
             bref=[("x-couch", "Le séjour.", "Une grande cheminée et un accès à la terrasse, un coin repas avec une grande table, et une cuisine séparée."),
                   ("bed-double", "Cinq chambres,", "quatre au niveau bas et une sous les combles, en lits doubles ou jumeaux. Cinq salles de bain, et un coin TV sous le toit."),
                   ("waves", "Spa.", "Un jacuzzi en pierre et un hammam au niveau bas, avec une douche à côté. Il n'y a pas de piscine."),
                   ("snowflake", "Local à skis.", "Un local à skis, une buanderie et un parking gratuit sur place.")],
             apres="Le chalet accueille jusqu'à 10 personnes.",
             faq=[("Combien de personnes peuvent séjourner ?", "Jusqu'à 10 personnes : cinq chambres en lits doubles ou jumeaux, et cinq salles de bain. Une famille, ou deux familles ensemble."),
                  ("Que comprend le spa ?", "Un jacuzzi en pierre et un hammam, avec une douche, au niveau bas. Il n'y a pas de piscine.")],
             pistes=("Les pistes sont-elles loin ?", "Le chalet est près des remontées mécaniques de Courchevel 1850. L'accès aux pistes est confirmé à chaque demande."),
             web="Chalet casher à Courchevel 1850, jusqu'à 10 personnes, jacuzzi en pierre et hammam",
             ld_desc="Un chalet casher privé à Courchevel 1850 : cinq chambres jusqu'à 10 personnes, un jacuzzi en pierre et un hammam, une cheminée, près des remontées mécaniques. Chef ou repas livrés, Chabbat et minyan.",
             alt=f"Le Chalet {NB}", carte=dict(lieu="Courchevel 1850", t=f"Chalet {NB}, Courchevel 1850", alt=f"Le Chalet {NB} à Courchevel 1850 sous la neige",
                                          s=[("5", "chambres"), ("Jusqu'à 10", "personnes"), ("Jacuzzi", "et hammam"), ("Près", "des remontées")]),
             nav=(f"Chalet {NB} · Courchevel 1850", "5 chambres · jacuzzi et hammam")),
  "es": dict(title=f"Chalet {NB}, kosher, Courchevel 1850",
             desc=f"Chalet {NB} en Courchevel 1850: chalet kosher privado hasta 10 personas, cinco habitaciones, jacuzzi de piedra y hammam. Chef, Shabat, minyán.",
             ital="Courchevel 1850, jacuzzi de piedra y hammam", hero="Un chalet de madera y piedra en Courchevel 1850, cerca de los remontes, hasta 10 personas.",
             intro="Cinco habitaciones y cinco baños para 10 personas, en tres niveles. Un spa con jacuzzi de piedra y hammam, un salón con una gran chimenea que da a la terraza, un guardaesquís. Chef o comidas a domicilio, Shabat y minyán.",
             loc=("map-pin", "Ubicación.", "En Courchevel 1850, cerca de los remontes."),
             bref=[("x-couch", "El salón.", "Una gran chimenea y salida a la terraza, un comedor con una gran mesa y una cocina independiente."),
                   ("bed-double", "Cinco habitaciones,", "cuatro en el nivel bajo y una bajo el tejado, con camas dobles o gemelas. Cinco baños, y un rincón de TV bajo el tejado."),
                   ("waves", "Spa.", "Un jacuzzi de piedra y un hammam en el nivel bajo, con una ducha al lado. No hay piscina."),
                   ("snowflake", "Guardaesquís.", "Un guardaesquís, un lavadero y aparcamiento gratuito en el lugar.")],
             apres="El chalet recibe hasta 10 personas.",
             faq=[("¿Cuántas personas pueden alojarse?", "Hasta 10 personas: cinco habitaciones con camas dobles o gemelas, y cinco baños. Una familia, o dos familias juntas."),
                  ("¿Qué incluye el spa?", "Un jacuzzi de piedra y un hammam, con una ducha, en el nivel bajo. No hay piscina.")],
             pistes=("¿Están lejos las pistas?", "El chalet está cerca de los remontes de Courchevel 1850. El acceso a las pistas se confirma con cada solicitud."),
             web="Chalet kosher en Courchevel 1850, hasta 10 personas, jacuzzi de piedra y hammam",
             ld_desc="Un chalet kosher privado en Courchevel 1850: cinco habitaciones hasta 10 personas, un jacuzzi de piedra y un hammam, una chimenea, cerca de los remontes. Chef o comidas a domicilio, Shabat y minyán.",
             alt=f"El Chalet {NB}", carte=dict(lieu="Courchevel 1850", t=f"Chalet {NB}, Courchevel 1850", alt=f"El Chalet {NB} en Courchevel 1850 bajo la nieve",
                                          s=[("5", "habitaciones"), ("Hasta 10", "personas"), ("Jacuzzi", "y hammam"), ("Cerca", "de los remontes")]),
             nav=(f"Chalet {NB} · Courchevel 1850", "5 habitaciones · jacuzzi y hammam")),
  "he": dict(title=f"צ'אלה {HB}, קורשבל 1850: כשרה, ג'קוזי וחמאם",
             desc=f"צ'אלה {HB} בקורשבל 1850: צ'אלה כשרה פרטית עד 10 אורחים, חמישה חדרי שינה, ג'קוזי אבן וחמאם. שף, שבת ומניין.",
             ital="קורשבל 1850, ג'קוזי אבן וחמאם", hero="צ'אלה מעץ ומאבן בקורשבל 1850, ליד מעליות הסקי, עד 10 אורחים.",
             intro="חמישה חדרי שינה וחמישה חדרי רחצה ל-10 אורחים, בשלוש קומות. ספא עם ג'קוזי אבן וחמאם, סלון עם אח גדולה הנפתח אל המרפסת, חדר סקי. שף או ארוחות במשלוח, שבת ומניין.",
             loc=("map-pin", "מיקום.", "בקורשבל 1850, ליד מעליות הסקי."),
             bref=[("x-couch", "הסלון.", "אח גדולה ויציאה למרפסת, פינת אוכל עם שולחן גדול, ומטבח נפרד."),
                   ("bed-double", "חמישה חדרי שינה,", "ארבעה בקומה התחתונה ואחד מתחת לגג, עם מיטות זוגיות או נפרדות. חמישה חדרי רחצה, ופינת טלוויזיה מתחת לגג."),
                   ("waves", "ספא.", "ג'קוזי אבן וחמאם בקומה התחתונה, ולידם מקלחת. אין בריכה."),
                   ("snowflake", "חדר סקי.", "חדר סקי, חדר כביסה וחניה חינם במקום.")],
             apres="הצ'אלה מארחת עד 10 אורחים.",
             faq=[("כמה אנשים יכולים להתארח?", "עד 10 אורחים: חמישה חדרי שינה עם מיטות זוגיות או נפרדות, וחמישה חדרי רחצה. משפחה אחת, או שתי משפחות יחד."),
                  ("מה כולל הספא?", "ג'קוזי אבן וחמאם, עם מקלחת, בקומה התחתונה. אין בריכה.")],
             pistes=("המסלולים רחוקים?", "הצ'אלה ליד מעליות הסקי של קורשבל 1850. הגישה למסלולים מאושרת בכל פנייה."),
             web="צ'אלה כשרה בקורשבל 1850, עד 10 אורחים, ג'קוזי אבן וחמאם",
             ld_desc="צ'אלה כשרה פרטית בקורשבל 1850: חמישה חדרי שינה עד 10 אורחים, ג'קוזי אבן וחמאם, אח, ליד מעליות הסקי. שף או ארוחות במשלוח, שבת ומניין.",
             alt="הצ'אלה בקורשבל 1850", carte=dict(lieu="קורשבל 1850", t=f"צ'אלה {HB}, קורשבל 1850", alt=f"צ'אלה {HB} בקורשבל 1850 תחת השלג",
                                          s=[("5", "חדרי שינה"), ("עד 10", "אורחים"), ("ג'קוזי", "וחמאם"), ("ליד", "מעליות הסקי")]),
             nav=(f"צ'אלה {HB} · קורשבל 1850", "5 חדרי שינה · ג'קוזי וחמאם")),
 },
}

# chaînes hébraïques neuves de la session, à relire (relecture-hebreu) : tout ce que contient T["a"]["he"], T["b"]["he"],
# CUISINE_A["he"], SHABBAT["he"], ACCES["he"], DISPO["he"] et les deux noms HA, HB.
def he_neuf():
    out = [HA, HB, CH["a"]["lieu_he"], CH["b"]["lieu_he"], CUISINE_A["he"][1], CUISINE_A["he"][2], SHABBAT["he"], ACCES["he"], DISPO["he"]]
    for cle in ("a", "b"):
        d = T[cle]["he"]
        for k, v in d.items():
            if isinstance(v, str):
                out.append(v)
            elif k == "bref":
                out += [x for t in v for x in t[1:]]
            elif k == "faq":
                out += [x for t in v for x in t]
            elif k in ("loc", "pistes"):
                out += list(v[-2:] if k == "loc" else v)
            elif k == "carte":
                out += [x for x in (v["lieu"], v["t"], v["alt"])] + [y for p in v["s"] for y in p]
            elif k == "nav":
                out += list(v)
    return out
