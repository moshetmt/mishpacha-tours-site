# -*- coding: utf-8 -*-
"""Page station « kosher Avoriaz » /kosher-avoriaz/ en 4 langues, 05/11/2026.

Clonage de la page station Chamonix publiée dans chaque langue (Haute-Savoie, accès Genève, aucune carte chalet), puis
remplacement du contenu propre à Avoriaz. Jamais d'édition HTML à la main. Idempotent : relancer réécrit les 4 pages et leurs
index.md à l'identique (date figée) ; sitemap et llms.txt vérifient leur marque.
Ne touche que kosher-avoriaz/ (4 langues, html + md), img/h/st-avoriaz-*.webp, img/og/kosher-avoriaz.jpg, sitemap.xml, llms.txt.

Faits sourcés (relevés le 05/11/2026) :
- 1 800 m, Haute-Savoie, massif du Chablais, Portes du Soleil (12 stations France et Suisse), station piétonne depuis sa création en 1966,
  architecte Jacques Labro (architecture organique, bâtiments en forme de pyramide) : https://www.avoriaz.com/en/discover/the-resort/history/
- accès : Genève 1 h 25 par la route, aéroport de Genève 85 km, Lyon 2 h 40 / 212 km, téléphérique des Prodains Express 4 min depuis la vallée de
  Morzine, navettes SAT Léman / Altibus depuis l'aéroport : https://www.avoriaz.com/sejourner/acces-et-transport/venir-a-avoriaz/
- saison « du 11 décembre au 18 avril » : https://www.avoriaz.com/ (page relevée le 05/11/2026, année non écrite sur la page)
- coordonnées : OpenStreetMap, nœud « Avoriaz » 46.1925, 6.7703 (Hebcal accepte ces coordonnées, fuseau Europe/Paris)
- Morzine, Montriond, Châtel : même domaine (webcams et plan du site de la station)
Ce que la page ne dit PAS : aucune livraison de repas (non confirmée par Mendel), aucun prix, aucun chalet, aucun Beth Habad (non prouvé),
aucun lien vers les stations absentes. Photo : Pexels 11358802 (voir CREDITS.md).
Lancer depuis site-v5 : python _station_avoriaz.py"""
import io
import json
import os
import re
import urllib.parse as U
from markdownify import markdownify as md

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SLUG, MODELE = "kosher-avoriaz", "kosher-chamonix"
BASE = "https://mishpachatours.com"
DATE = "2026-11-05"
LAT, LON = 46.1925, 6.7703
LANGS = {"en": "", "fr": "fr/", "es": "es/", "he": "he/"}
SUFFIXE = " | Mishpacha Tours"


def rdr(p): return io.open(p, encoding="utf-8", newline="").read()
def rd(p): return rdr(p).replace("\r\n", "\n")   # arbre en CRLF (autocrlf) : le modele est lu en LF
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)


def sub1(motif, rempl, s, flags=re.S):
    """Remplacement regex qui doit trouver exactement une occurrence."""
    r, n = re.subn(motif, rempl, s, flags=flags)
    assert n == 1, (motif[:90], n)
    return r


def lis(items, cls="dk-sans-ico"):
    return "".join(f'<li class="{cls}"><b>{b}</b> {p}</li>\n' for b, p in items)


LTR = lambda x: f'<span dir="ltr">{x}</span>'

T = {
 "en": dict(
  noms=[("Chamonix", "Avoriaz")],
  title="Kosher Avoriaz: Chef, Shabbat and Minyan | Mishpacha Tours",
  desc="Kosher Avoriaz, the car-free resort of the Portes du Soleil: private chef, Shabbat, holidays, minyan and Sefer Torah on request. One written quote.",
  h1="Avoriaz, strictly kosher<br><i>car-free, in the Portes du Soleil</i>",
  sous="Avoriaz sits at 1,800 m in Haute-Savoie, in a village with no cars.",
  phrase="Ski Avoriaz by day. Walk back to a set table, a minyan, and Shabbat ready.",
  col1=("A private chef, meals on request", "The kitchen is kashered, and the meals of the week are arranged with you."),
  intro="Built in 1966, Avoriaz has no cars: you walk or you ski. We organise your kosher stay: private chef, Shabbat, minyan and Sefer Torah, in one written quote.",
  org=[("A private chef in your accommodation.", "Chalet or flat, rented by you: our kosher team based in the Alps makes the kitchen kosher and cooks for your group, from breakfast to the Shabbat table."),
       ("Kosher meals, on request.", "Tell us your dates and how many you are, and we say what is possible for your week in Avoriaz. In a resort without cars, how a meal reaches your door is settled in the quote, not promised in advance."),
       ("Shabbat.", "Shabbat meals, challot and wine are arranged with you beforehand and ready before candle lighting. Nothing is brought on Shabbat or on a holiday."),
       ("The holidays.", "Purim falls in March, inside the ski season. Tell us which holiday falls in your week."),
       ("A minyan and a Sefer Torah.", "No permanent minyan is published in the resort: it depends on the families there that week. Give us your dates and we group the families who write to us."),
       ("A tailor-made stay, A to Z.", "A large family, or several families together? Tell us the number of adults and children. Chalet or flat, chef, transfers from Geneva, Shabbat, the holidays: one request, one quote. Hebrew-speaking guests are welcome.")],
  kos=[("Kosher restaurant or shop.", "None is published in Avoriaz. Plan on a private chef, or bring your food."),
       ("Groceries before you climb.", "Avoriaz has no cars, so shop before you go up. Lyon has certified shops: {a}."),
       ("Season.", "The ski season runs from 11 December to 18 April according to the resort's website. Check the dates and the lift pass before you book.")],
  kos_a="what to buy and where",
  src="Source: ",
  res_h2=("A resort", "without cars"),
  res=[("No cars, from the start.", "Created in 1966, Avoriaz was designed as a 100% pedestrian village (avoriaz.com). You leave the car in a car park at the entrance, or ride the Prodains cable car up from the valley: 4 minutes, then you go on foot or on skis."),
       ("A village drawn in one piece.", "Architect Jacques Labro designed it in the spirit of organic architecture, with pyramid-shaped buildings."),
       ("The Portes du Soleil at your door.", "Avoriaz sits at the heart of the Portes du Soleil, a ski area linking 12 resorts in France and Switzerland. Morzine, Montriond and Châtel belong to the same area: if you sleep in one of these villages, tell us."),
       ("Families.", "No road to cross with children, and accommodation with the skis at the door. Large families and several families together are our core: send the number of adults and children.")],
  et1="Avoriaz, your dates, the number of adults and children, where you sleep, and what you need: a chef, meals, Shabbat, a holiday, a minyan. By WhatsApp or with the form at the bottom of this page.",
  et2="The same day, we check with our team in the Alps what is possible in Avoriaz for your dates: chef, kitchen, meals, minyan. One contact from start to finish.",
  acces=[("From Geneva airport:", "about 1 h 25 by road, 85 km according to the resort. Shuttles run from the airport to the Prodains cable car or to the reception area of the village. Add time on a winter Saturday."),
         ("The last stretch, on foot.", "Avoriaz has no cars: you park at the entrance or ride the Prodains Express cable car up from the valley (4 minutes), then you walk."),
         ("From Lyon-Saint-Exupéry airport:", "212 km, about 2 h 40 by road according to the resort. Lyon suits long-haul flights and a first kosher shop before you climb: {a}.")],
  note="Pin on the centre of the village.",
  faq=[("Can you bring kosher meals to a flat in Avoriaz?", "Meals are arranged on request. Avoriaz has no cars, so the quote says how they reach you. Send your dates, the number of people and where you sleep."),
       ("Is there a minyan in Avoriaz?", "No permanent minyan is published in the resort. It depends on the families there that week: send your dates early and we group them, with a Sefer Torah on request."),
       ("We sleep in Morzine, Montriond or Châtel, not in Avoriaz. Can you help?", "Yes. These villages share the Portes du Soleil with Avoriaz. Tell us where you sleep and your dates: the private chef and the Shabbat table are organised where you stay, and the quote confirms what is possible."),
       ("Can you organise a stay for a large family or a group?", "Yes. Send the number of adults and children, the dates and what you need, and you receive one written quote.")],
  pesach_a="Pesach in the Alps",
  vois=("Kosher Chamonix", "Megève", "Chamonix"),
  llms="Kosher Avoriaz: Chef, Shabbat and Minyan"),

 "fr": dict(
  noms=[("Chamonix", "Avoriaz")],
  title="Casher à Avoriaz : chef, repas, Shabbat, minyan | Mishpacha Tours",
  desc="Avoriaz, station sans voitures des Portes du Soleil, strictement casher : chef privé, Shabbat, fêtes, minyan et Sefer Torah sur demande. Un devis écrit.",
  h1="Avoriaz, strictement casher<br><i>sans voitures, au cœur des Portes du Soleil</i>",
  sous="Avoriaz se trouve à 1 800 m en Haute-Savoie, dans un village sans voitures.",
  phrase="Skiez à Avoriaz le jour. Rentrez à pied vers une table dressée, un minyan et Shabbat prêt.",
  col1=("Un chef privé, des repas sur demande", "La cuisine est cachérisée, et les repas de la semaine se préparent avec vous."),
  intro="Née en 1966, Avoriaz n’a pas de voitures : on marche ou on skie. Nous organisons votre séjour casher : chef privé, Shabbat, minyan et Sefer Torah, en un seul devis écrit.",
  org=[("Un chef privé là où vous logez.", "Chalet ou appartement que vous louez : notre équipe casher des Alpes cachérise la cuisine et cuisine pour votre groupe, du petit-déjeuner à la table de Shabbat."),
       ("Des repas casher, sur demande.", "Dites-nous vos dates et combien vous êtes, nous vous disons ce qui est possible pour votre semaine à Avoriaz. Dans une station sans voitures, la façon dont un repas arrive jusqu’à vous se fixe dans le devis, elle n’est pas promise d’avance."),
       ("Shabbat.", "Repas de Shabbat, hallot et vin se préparent avec vous à l’avance et sont prêts avant l’allumage des bougies. Rien n’est apporté pendant Shabbat ni un jour de fête."),
       ("Les fêtes.", "Pourim tombe en mars, en pleine saison de ski. Dites-nous quelle fête tombe pendant votre semaine."),
       ("Un minyan et un Sefer Torah.", "Aucun minyan permanent n’est publié dans la station : il dépend des familles présentes cette semaine-là. Donnez-nous vos dates et nous réunissons les familles qui nous écrivent."),
       ("Un séjour sur mesure, de A à Z.", "Une grande famille, ou plusieurs familles ensemble ? Dites-nous le nombre d’adultes et d’enfants. Chalet ou appartement, chef, transferts depuis Genève, Shabbat, fêtes : une demande, un devis. Les hôtes hébréophones sont les bienvenus.")],
  kos=[("Restaurant ou commerce casher.", "Aucun n’est publié à Avoriaz. Prévoyez un chef privé, ou apportez votre nourriture."),
       ("Les courses avant de monter.", "Avoriaz n’a pas de voitures : faites vos courses avant la montée. Lyon a des commerces certifiés, {a}."),
       ("Saison.", "La saison de ski court du 11 décembre au 18 avril selon le site de la station. Vérifiez les dates et le forfait avant de réserver.")],
  kos_a="quoi acheter et où",
  src="Source : ",
  res_h2=("Une station", "sans voitures"),
  res=[("Sans voitures depuis le début.", "Créée en 1966, Avoriaz a été conçue comme un village 100 % piéton (avoriaz.com). On laisse la voiture dans un parking à l’entrée, ou on monte par le téléphérique des Prodains depuis la vallée : 4 minutes, puis on continue à pied ou à ski."),
       ("Un village dessiné d’un seul tenant.", "L’architecte Jacques Labro l’a conçu dans l’esprit de l’architecture organique, avec des bâtiments en forme de pyramide."),
       ("Les Portes du Soleil à votre porte.", "Avoriaz est au cœur des Portes du Soleil, un domaine qui relie 12 stations entre la France et la Suisse. Morzine, Montriond et Châtel font partie du même domaine : si vous logez dans l’un de ces villages, dites-le-nous."),
       ("Les familles.", "Pas de route à traverser avec des enfants, et des logements skis aux pieds. Les grandes familles et les groupes de plusieurs familles sont notre cœur de métier : envoyez le nombre d’adultes et d’enfants.")],
  et1="Avoriaz, vos dates, le nombre d’adultes et d’enfants, où vous dormez, et ce dont vous avez besoin : un chef, des repas, Shabbat, une fête, un minyan. Par WhatsApp ou avec le formulaire en bas de cette page.",
  et2="Le jour même, nous vérifions avec notre équipe dans les Alpes ce qui est possible à Avoriaz pour vos dates : chef, cuisine, repas, minyan. Un seul interlocuteur du début à la fin.",
  acces=[("Depuis l’aéroport de Genève :", "environ 1 h 25 par la route, 85 km selon la station. Des navettes relient l’aéroport au téléphérique des Prodains ou à l’accueil du village. Prévoyez plus de temps un samedi d’hiver."),
         ("Le dernier tronçon, à pied.", "Avoriaz n’a pas de voitures : on se gare à l’entrée ou on monte par le téléphérique des Prodains Express depuis la vallée (4 minutes), puis on marche."),
         ("Depuis l’aéroport de Lyon-Saint-Exupéry :", "212 km, environ 2 h 40 par la route selon la station. Lyon convient aux vols long-courriers et à de premières courses casher avant la montée : {a}.")],
  note="Repère au centre du village.",
  faq=[("Peut-on avoir des repas casher dans un appartement à Avoriaz ?", "Les repas se font sur demande. Avoriaz n’a pas de voitures : le devis précise comment ils vous parviennent. Envoyez vos dates, le nombre de personnes et l’endroit où vous dormez."),
       ("Y a-t-il un minyan à Avoriaz ?", "Aucun minyan permanent n’est publié dans la station. Il dépend des familles présentes cette semaine-là : envoyez vos dates tôt, nous les réunissons, avec un Sefer Torah sur demande."),
       ("Nous logeons à Morzine, Montriond ou Châtel, pas à Avoriaz. Pouvez-vous nous aider ?", "Oui. Ces villages partagent les Portes du Soleil avec Avoriaz. Dites-nous où vous dormez et à quelles dates : le chef privé et la table de Shabbat s’organisent là où vous logez, et le devis confirme ce qui est possible."),
       ("Peut-on organiser un séjour pour une grande famille ou un groupe ?", "Oui. Envoyez le nombre d’adultes et d’enfants, les dates et ce dont vous avez besoin : vous recevez un seul devis écrit.")],
  pesach_a="Pessah dans les Alpes",
  vois=("Chamonix casher", "Megève", "Chamonix"),
  llms="Casher à Avoriaz : chef, repas, Shabbat, minyan"),

 "es": dict(
  noms=[("Chamonix", "Avoriaz")],
  title="Kosher en Avoriaz: chef, comidas, Shabat, minián | Mishpacha Tours",
  desc="Avoriaz, estación sin coches de Portes du Soleil, estrictamente kosher: chef privado, Shabat, fiestas, minián y Sefer Torá bajo petición. Un presupuesto por escrito.",
  h1="Avoriaz<br><i>estrictamente kosher, sin coches, en Portes du Soleil</i>",
  sous="Avoriaz se encuentra a 1.800 m en Alta Saboya, en un pueblo sin coches.",
  phrase="Esquíe en Avoriaz de día. Vuelva a pie a una mesa servida, un minián y el Shabat listo.",
  col1=("Chef privado, comidas bajo petición", "La cocina está kosherizada y las comidas de la semana se preparan con ustedes."),
  intro="Construida en 1966, Avoriaz no tiene coches: se camina o se esquía. Organizamos su estancia kosher: chef privado, Shabat, minián y Sefer Torá, en un solo presupuesto por escrito.",
  org=[("Un chef privado donde se aloje.", "Chalé o apartamento que usted alquile: nuestro equipo kosher de los Alpes kosheriza la cocina y cocina para su grupo, del desayuno a la mesa de Shabat."),
       ("Comidas kosher, bajo petición.", "Díganos sus fechas y cuántos son, y le decimos qué es posible para su semana en Avoriaz. En una estación sin coches, cómo llega una comida hasta su puerta se fija en el presupuesto, no se promete de antemano."),
       ("Shabat.", "Las comidas de Shabat, las jalot y el vino se preparan con usted de antemano y están listos antes del encendido de las velas. No se trae nada durante el Shabat ni en una fiesta."),
       ("Las fiestas.", "Purim cae en marzo, en plena temporada de esquí. Díganos qué fiesta cae en su semana."),
       ("Un minián y un Sefer Torá.", "En la estación no hay publicado ningún minián permanente: depende de las familias presentes esa semana. Dénos sus fechas y reunimos a las familias que nos escriben."),
       ("Una estancia a medida, de la A a la Z.", "¿Una familia numerosa, o varias familias juntas? Díganos el número de adultos y de niños. Chalé o apartamento, chef, traslados desde Ginebra, Shabat, fiestas: una solicitud, un presupuesto. Los huéspedes de habla hebrea son bienvenidos.")],
  kos=[("Restaurante o tienda kosher.", "No hay ninguno publicado en Avoriaz. Cuente con un chef privado, o traiga su comida."),
       ("La compra antes de subir.", "Avoriaz no tiene coches: haga la compra antes de subir. Lyon tiene tiendas certificadas, {a}."),
       ("Temporada.", "La temporada de esquí va del 11 de diciembre al 18 de abril según el sitio de la estación. Compruebe las fechas y el forfait antes de reservar.")],
  kos_a="qué comprar y dónde",
  src="Fuente: ",
  res_h2=("Una estación", "sin coches"),
  res=[("Sin coches desde el principio.", "Creada en 1966, Avoriaz se concibió como un pueblo 100 % peatonal (avoriaz.com). Se deja el coche en un aparcamiento a la entrada, o se sube en el teleférico de Prodains desde el valle: 4 minutos, y luego se sigue a pie o esquiando."),
       ("Un pueblo dibujado de una pieza.", "El arquitecto Jacques Labro lo concibió con el espíritu de la arquitectura orgánica, con edificios en forma de pirámide."),
       ("Portes du Soleil a su puerta.", "Avoriaz está en el corazón de Portes du Soleil, un dominio que une 12 estaciones entre Francia y Suiza. Morzine, Montriond y Châtel forman parte del mismo dominio: si se aloja en uno de esos pueblos, díganoslo."),
       ("Las familias.", "Sin carretera que cruzar con niños, y alojamientos con los esquís a pie de puerta. Las familias numerosas y los grupos de varias familias son nuestro núcleo: envíe el número de adultos y de niños.")],
  et1="Avoriaz, sus fechas, el número de adultos y de niños, dónde se aloja y qué necesita: chef, comidas, Shabat, una fiesta, un minián. Por WhatsApp o con el formulario al final de esta página.",
  et2="El mismo día comprobamos con nuestro equipo en los Alpes qué es posible en Avoriaz para sus fechas: chef, cocina, comidas, minián. Un solo contacto de principio a fin.",
  acces=[("Desde el aeropuerto de Ginebra:", "unas 1 h 25 por carretera, 85 km según la estación. Hay autobuses lanzadera del aeropuerto al teleférico de Prodains o a la zona de recepción del pueblo. Cuente más tiempo un sábado de invierno."),
         ("El último tramo, a pie.", "Avoriaz no tiene coches: se aparca a la entrada o se sube en el teleférico Prodains Express desde el valle (4 minutos), y luego se camina."),
         ("Desde el aeropuerto de Lyon-Saint-Exupéry:", "212 km, unas 2 h 40 por carretera según la estación. Lyon es adecuada para vuelos de largo recorrido y para una primera compra kosher antes de subir: {a}.")],
  note="Marca en el centro del pueblo.",
  faq=[("¿Pueden traer comidas kosher a un apartamento en Avoriaz?", "Las comidas se hacen bajo petición. Avoriaz no tiene coches: el presupuesto indica cómo les llegan. Envíe sus fechas, el número de personas y dónde se aloja."),
       ("¿Hay minián en Avoriaz?", "En la estación no hay publicado ningún minián permanente. Depende de las familias presentes esa semana: envíe sus fechas pronto, las reunimos, con un Sefer Torá bajo petición."),
       ("Nos alojamos en Morzine, Montriond o Châtel, no en Avoriaz. ¿Pueden ayudarnos?", "Sí. Esos pueblos comparten Portes du Soleil con Avoriaz. Díganos dónde se aloja y en qué fechas: el chef privado y la mesa de Shabat se organizan donde ustedes se alojen, y el presupuesto confirma qué es posible."),
       ("¿Pueden organizar una estancia para una familia numerosa o un grupo?", "Sí. Envíe el número de adultos y de niños, las fechas y lo que necesita, y recibirá un solo presupuesto por escrito.")],
  pesach_a="Pésaj en los Alpes",
  vois=("Chamonix kosher", "Megève", "Chamonix"),
  llms="Kosher en Avoriaz: chef, comidas, Shabat, minián"),

 "he": dict(
  noms=[("בשמוני", "באבוריאז"), ("לשמוני", "לאבוריאז"), ("שמוני", "אבוריאז"), ("Chamonix", "Avoriaz")],
  title="אבוריאז כשר: שף פרטי, שבת ומניין | Mishpacha Tours",
  desc="אבוריאז, אתר הסקי ללא מכוניות בפורט דו סוליי, כשר לחלוטין: שף פרטי, שבת, חגים, מניין וספר תורה לפי בקשה. הצעת מחיר אחת בכתב.",
  h1="אבוריאז, כשר לחלוטין<br><i>ללא מכוניות, בלב פורט דו סוליי</i>",
  sous="אבוריאז שוכנת בגובה 1,800 מ' באלפים הצרפתיים, בכפר שאין בו מכוניות.",
  phrase="ביום עושים סקי באבוריאז. בערב חוזרים ברגל לשולחן ערוך, למניין ולשבת מוכנה.",
  col1=("שף פרטי, וארוחות לפי בקשה", "המטבח מוכשר, והארוחות של השבוע מסודרות איתכם."),
  intro="אבוריאז נבנתה ב-1966 כאתר שאין בו מכוניות: הולכים ברגל או גולשים. אנחנו מארגנים לכם שהות כשרה: שף פרטי, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
  org=[("שף פרטי במקום הלינה שלכם.", "צ'אלה או דירה ששכרתם: הצוות הכשר שלנו שבסיסו באלפים מכשיר את המטבח ומבשל לקבוצה שלכם, מארוחת הבוקר ועד שולחן השבת."),
       ("ארוחות כשרות לפי בקשה.", "ספרו לנו את התאריכים וכמה אתם, ונאמר מה אפשרי לשבוע שלכם באבוריאז. באתר בלי מכוניות, הדרך שבה ארוחה מגיעה אליכם נקבעת בהצעת המחיר, ולא מובטחת מראש."),
       ("שבת.", "סעודות שבת, חלות ויין מתואמים איתכם מראש ומוכנים לפני הדלקת הנרות. בשבת ובחג שום דבר לא מובא."),
       ("החגים.", "פורים חל במרץ, בתוך עונת הסקי. כתבו איזה חג חל בשבוע שלכם."),
       ("מניין וספר תורה.", "באתר לא מתפרסם מניין קבוע: הוא תלוי במשפחות שנמצאות שם באותו שבוע. מסרו לנו את התאריכים ואנו מרכזים את המשפחות שכותבות לנו."),
       ("שהייה בהתאמה אישית, מא' ועד ת'.", "משפחה גדולה, או כמה משפחות יחד? ספרו לנו כמה מבוגרים וכמה ילדים. צ'אלה או דירה, שף, הסעות מז'נבה, שבת, החגים: בקשה אחת, הצעת מחיר אחת. אורחים דוברי עברית מתקבלים בברכה.")],
  kos=[("מסעדה או חנות כשרות.", "באבוריאז לא מתפרסמות כאלה. תכננו שף פרטי, או הביאו את האוכל שלכם."),
       ("קניות לפני העלייה.", "באבוריאז אין מכוניות, ולכן עושים קניות לפני העלייה. בליון יש חנויות עם תעודת כשרות: {a}."),
       ("עונה.", "עונת הסקי נמשכת מ-11 בדצמבר עד 18 באפריל, לפי אתר הסקי. בדקו את התאריכים ואת כרטיס הרכבל לפני ההזמנה.")],
  kos_a="מה לקנות ואיפה",
  src="מקור: ",
  res_h2=("אתר", "בלי מכוניות"),
  res=[("בלי מכוניות מההתחלה.", f"אבוריאז נוסדה ב-1966 ותוכננה ככפר להולכי רגל בלבד (avoriaz.com). את הרכב משאירים בחניון בכניסה, או עולים ברכבל {LTR('Prodains')} מהעמק: ארבע דקות, ומשם ברגל או על סקי."),
       ("כפר שתוכנן כמקשה אחת.", f"האדריכל {LTR('Jacques Labro')} תכנן אותו ברוח האדריכלות האורגנית, עם בניינים בצורת פירמידה."),
       ("פורט דו סוליי ליד הדלת.", f"אבוריאז שוכנת בלב פורט דו סוליי, אזור סקי שמחבר 12 אתרים בצרפת ובשווייץ. מורזין, {LTR('Montriond')} ו-{LTR('Châtel')} שייכים לאותו אזור: אם אתם ישנים באחד הכפרים האלה, ספרו לנו."),
       ("משפחות.", "אין כביש לחצות עם ילדים, ויש לינה שהסקי בה ליד הדלת. משפחות גדולות וכמה משפחות יחד הן הלב שלנו: שלחו כמה מבוגרים וכמה ילדים.")],
  et1="אבוריאז, התאריכים שלכם, כמה מבוגרים וכמה ילדים, איפה אתם ישנים, ומה אתם צריכים: שף, ארוחות, שבת, חג, מניין. בוואטסאפ או בטופס בתחתית הדף.",
  et2="באותו יום אנו בודקים עם הצוות שלנו באלפים מה אפשרי באבוריאז לתאריכים שלכם: שף, מטבח, ארוחות, מניין. איש קשר אחד מההתחלה ועד הסוף.",
  acces=[("משדה התעופה של ז'נבה:", "כשעה ו-25 דקות בכביש, 85 ק\"מ לפי האתר. הסעות יוצאות מהשדה אל רכבל " + LTR("Prodains") + " או אל אזור הקבלה של הכפר. הוסיפו זמן בשבת של החורף."),
         ("הקטע האחרון, ברגל.", "באבוריאז אין מכוניות: מחנים בכניסה או עולים ברכבל " + LTR("Prodains Express") + " מהעמק (ארבע דקות), וממשיכים ברגל."),
         ("מנמל התעופה ליון-סנט-אקזופרי:", "212 ק\"מ, כשעתיים ו-40 דקות בכביש לפי האתר. ליון מתאימה לטיסות ארוכות ולקנייה כשרה ראשונה לפני העלייה להרים: {a}.")],
  note="סימון במרכז הכפר.",
  faq=[("אפשר לקבל ארוחות כשרות לדירה באבוריאז?", "הארוחות מסודרות לפי בקשה. באבוריאז אין מכוניות, ולכן הצעת המחיר מפרטת איך הן מגיעות אליכם. שלחו את התאריכים, את מספר המשתתפים ואת המקום שבו אתם ישנים."),
       ("האם יש מניין באבוריאז?", "באתר לא מתפרסם מניין קבוע. הוא תלוי במשפחות שנמצאות שם באותו שבוע: מסרו לנו את התאריכים מוקדם ואנו מרכזים אותן, עם ספר תורה לפי בקשה."),
       ("אנחנו ישנים במורזין, ב-<span dir=\"ltr\">Montriond</span> או ב-<span dir=\"ltr\">Châtel</span> ולא באבוריאז. אפשר לעזור?", "כן. הכפרים האלה חולקים עם אבוריאז את פורט דו סוליי. ספרו לנו איפה אתם ישנים ומתי: השף ושולחן השבת מסודרים במקום הלינה שלכם, והצעת המחיר מאשרת מה אפשרי."),
       ("אפשר לארגן שהות למשפחה גדולה או לקבוצה?", "כן. שלחו כמה מבוגרים וכמה ילדים, את התאריכים ואת מה שאתם צריכים, ותקבלו הצעת מחיר אחת בכתב.")],
  pesach_a="פסח באלפים",
  vois=("כשר בשמוני", "במג'ב", "בשמוני"),
  llms="Kosher Avoriaz: Chef, Shabbat and Minyan (Hebrew page: אבוריאז כשר)"),
}


def traiter_noms(s, noms):
    for old, new in noms:
        s = s.replace(U.quote(old, safe=""), U.quote(new, safe="")).replace(old, new)
    return s


def page(lang, pre):
    t = T[lang]
    s = rd(f"{pre}{MODELE}/index.html")
    # 0. segments site-wide laissés tels quels (menu des chalets, pied, liste H de la vue de transition, qui reçoit Avoriaz)
    gardes = []
    def garder(m):
        gardes.append(m.group(0)); return f"\x00{len(gardes) - 1}\x00"
    for motif in (r'<!--KIT-WP:vt-->.*?<!--/KIT-WP:vt-->', r'<div class="nav-ch-menu">.*?<a class="nav-ch-tous"[^>]*>[^<]*</a></div>',
                  r'<footer class="pied">.*?</footer>'):
        s, n = re.subn(motif, garder, s, flags=re.S); assert n == 1, motif
    assert '"kosher-chamonix","kosher-annecy"' in gardes[0]
    gardes[0] = gardes[0].replace('"kosher-chamonix","kosher-annecy"', '"kosher-chamonix","kosher-avoriaz","kosher-annecy"')

    # 1. adresse, visuels, nom de la station (texte brut et messages WhatsApp encodés)
    s = s.replace(MODELE, SLUG).replace("st-chamonix", "st-avoriaz")
    s = traiter_noms(s, t["noms"])

    # 2. en-tête : title, description, og, JSON-LD
    titre = t["title"]; court = titre.replace(SUFFIXE, "")
    s = sub1(r"<title>.*?</title>", f"<title>{titre}</title>", s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{court}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{t["desc"]}">', s)

    # 3. héros : H1, phrase d'altitude (dans le héros ou dans le bloc bn-intro selon la langue)
    s = sub1(r"<h1>.*?</h1>", f"<h1>{t['h1']}</h1>", s)
    if '<p class="hero-sous">' in s:
        s = sub1(r'<p class="hero-sous">.*?</p>', f'<p class="hero-sous">{t["sous"]}</p>', s)
    else:
        s = sub1(r'(<div class="bn-intro wrap"><p>).*?(</p></div>)', lambda m: m.group(1) + t["sous"] + m.group(2), s)

    # 4. manifeste (phrase + première colonne) et phrase d'introduction
    s = sub1(r'<p class="mf-phrase">.*?</p>', f'<p class="mf-phrase">{t["phrase"]}</p>', s)
    s = sub1(r'(<div class="mf-col"><div>)<b>.*?</b><span>.*?</span>(</div>)',
             lambda m: f'{m.group(1)}<b>{t["col1"][0]}</b><span>{t["col1"][1]}</span>{m.group(2)}', s)
    s = sub1(r"(<!--/MANIFESTE-->)<p>.*?</p>", lambda m: m.group(1) + f"<p>{t['intro']}</p>", s)

    # 5. « Ce que nous organisons » : six cartes réécrites ; le paragraphe Pessah (hors saison) est retiré, son lien sert à la FAQ
    m = re.search(r'<section class="clair clair-2 ss wrap conseils"><h2>.*?</section>', s, re.S)
    sec = m.group(0)
    pes = re.search(r'<p>[^<]*<a href="([^"]*kosher-pesach-french-alps/)">[^<]*</a>[^<]*</p>', sec)
    assert pes, lang
    href_pesach = pes.group(1)
    sec2 = sub1(r'(<ul class="dk-cartes dk-rail">\n).*?(</ul>)', lambda k: k.group(1) + lis(t["org"]) + k.group(2), sec)
    sec2 = sec2.replace(pes.group(0), "")
    s = s[:m.start()] + sec2 + s[m.end():]

    # 6. « Casher à Avoriaz » (bloc beige à pictogramme) : trois puces, source. Lien vers la page Lyon repris du bloc « accès ».
    lyon = re.search(r'<a href="([^"]*lyon-gateway-to-the-alps-kosher/)">([^<]*)</a>', s)
    lyon_href, lyon_txt = lyon.group(1), lyon.group(2)
    lien_lyon = f'<a href="{lyon_href}">{t["kos_a"]}</a>'
    kos = [(b, p.format(a=lien_lyon)) for b, p in t["kos"]]
    kos[1] = (kos[1][0], kos[1][1])
    def beige(m):
        ul = '<ul class="dk-cartes dk-rail">\n' + lis([(b, p) for b, p in kos[:1]]) \
             + f'<li class="dk-lien1 dk-sans-ico"><b>{kos[1][0]}</b> {kos[1][1]}</li>\n' + lis(kos[2:]) + "</ul>\n"
        return m.group(1) + "\n" + ul + f'<p>{t["src"]}<a href="https://www.avoriaz.com/" rel="noopener">avoriaz.com</a>.</p>' + m.group(3)
    s = sub1(r'(<div class="clair ss beige"><div class="wrap"><h2 class="dk-h2">.*?</h2>)(?:<p>[^<]*</p>)?\n(<ul class="dk-cartes dk-rail">.*?</p>)(</div></div>)', beige, s)

    # 7. « Une station sans voitures » (remplace « Hiver et été dans la vallée »)
    def resort(m):
        return (m.group(1) + f"{t['res_h2'][0]} <i>{t['res_h2'][1]}</i>" + m.group(3) + '<ul class="dk-cartes">\n' + lis(t["res"]) + "</ul>" + m.group(5))
    s = sub1(r'(<section class="clair clair-2 ss wrap conseils"><h2 class="dk-h2"><img[^>]*>)(.*?)(</h2>)(<ul class="dk-cartes">.*?</ul>)(</section>)', resort, s)

    # 8. Shabbat : coordonnées d'Avoriaz (le nom est déjà changé)
    s = sub1(r"latitude=45\.9237&longitude=6\.8694", f"latitude={LAT}&longitude={LON}", s)

    # 9. « Comment ça se passe » : paragraphes 1 et 2 (le 3 est celui du modèle)
    et = iter([t["et1"], t["et2"]])
    def etapes(m):
        return re.sub(r"(<h3>[^<]*</h3><p>)[^<]*(</p>)", lambda k: k.group(1) + (next(et, None) or k.group(0)[len(k.group(1)):-len(k.group(2))]) + k.group(2), m.group(0))
    s = sub1(r'<section class="ss wrap etapes">.*?</section>', etapes, s)

    # 10. accès : Genève, dernier tronçon, Lyon ; le lien « escale à Lyon » du modèle est conservé
    def acces(m):
        liens = re.findall(r'<li class="dk-lien1 dk-sans-ico">.*?</li>', m.group(2), re.S)
        stop = [x for x in liens if "stopover" in x]
        assert len(stop) == 1, lang
        a = [(b, p.format(a=f'<a href="{lyon_href}">{lyon_txt}</a>')) for b, p in t["acces"]]
        corps = lis(a[:2]) + f'<li class="dk-lien1 dk-sans-ico"><b>{a[2][0]}</b> {a[2][1]}</li>\n' + stop[0] + "\n"
        return m.group(1) + corps + m.group(3)
    s = sub1(r'(<div class="clair ss beige"><div class="wrap"><h2>[^\n]*?</h2><ul class="dk-cartes">\n)(.*?)(</ul></div></div>)', acces, s)

    # 11. carte : repère au centre du village
    pts = [{"n": "Avoriaz", "a": "74110 Avoriaz", "ll": [LAT, LON]}]
    s = sub1(r'data-points="[^"]*"', 'data-points="' + json.dumps(pts, ensure_ascii=False).replace('"', "&quot;") + '"', s)
    s = sub1(r'<p class="carte-note">[^<]*</p>', f'<p class="carte-note">{t["note"]}</p>', s)

    # 12. bloc « Un minyan sur place / Repas livrés » (Beth Habad non prouvé pour Avoriaz, livraison non confirmée) : retiré
    s = sub1(r'<section class="clair ss wrap minyan-bh">.*?</section>\n?', "", s)
    # 13. mini-catalogue de chalets (aucun chalet cité sur cette page) : retiré
    s = sub1(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", "", s)

    # 14. FAQ : première et dernière questions du modèle gardées, cinq propres à la station entre les deux
    m = re.search(r'(<section class="clair clair-2 ss wrap faq">.*?</h2>)(.*?)(</section>)', s, re.S)
    det = re.findall(r"<details>.*?</details>", m.group(2), re.S)
    assert len(det) == 6, (lang, len(det))
    lien_pes = f'<a href="{href_pesach}">{t["pesach_a"]}</a>'
    neuf = "".join(f"<details><summary>{q}</summary><p>{r.format(a=lien_pes)}</p></details>" for q, r in t["faq"])
    s = s[:m.start()] + m.group(1) + det[0] + neuf + det[-1] + m.group(3) + s[m.end():]
    qa = []
    for d in [det[0]] + [f"<details><summary>{q}</summary><p>{r.format(a=t['pesach_a'])}</p></details>" for q, r in t["faq"]] + [det[-1]]:
        q = re.sub(r"<[^>]+>", "", re.search(r"<summary>(.*?)</summary>", d, re.S).group(1))
        a = re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", d, re.S).group(1))
        qa.append((q, a))

    # 15. stations voisines : Megève, Chamonix, Annecy, toutes les stations (Courmayeur, en Italie, retirée)
    def voisines(m):
        li = re.findall(r"<li[^>]*>.*?</li>", m.group(2), re.S)
        meg = [x for x in li if "kosher-megeve/" in x]; ann = [x for x in li if "kosher-annecy/" in x]
        tout = [x for x in li if "/alps/" in x]
        assert len(meg) == len(ann) == len(tout) == 1, lang
        lab, ancien, nouveau = t["vois"]
        cha = meg[0].replace("kosher-megeve/", "kosher-chamonix/")
        txt = re.search(r">([^<]*)</a>", cha).group(1)
        cha = cha.replace(f">{txt}</a>", f">{txt.replace(ancien if ancien in txt else 'Megève', nouveau if ancien in txt else 'Chamonix')}</a>")
        assert os.path.exists(f"{pre}kosher-chamonix/index.html")
        return m.group(1) + meg[0] + cha + ann[0] + tout[0] + m.group(3)
    s = sub1(r'(<section class="clair ss wrap conseils" id="voisines">.*?<ul class="dk-suite">)(.*?)(</ul></section>)', voisines, s)

    # 16. JSON-LD : WebPage, Service, FAQPage
    mm = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    ld = json.loads(mm.group(2))
    for o in ld:
        if o["@type"] == "WebPage":
            o.update(name=court, description=t["desc"], dateModified=DATE)
        if o["@type"] == "Service":
            o["areaServed"] = {"@type": "Place", "name": "Avoriaz",
                               "address": {"@type": "PostalAddress", "addressLocality": "Avoriaz", "postalCode": "74110",
                                           "addressRegion": "Haute-Savoie", "addressCountry": "FR"},
                               "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON}}
            o["serviceType"] = {"en": "Private kosher chef, kosher meals on request, Shabbat and holiday meals, minyan and Sefer Torah in Avoriaz",
                                "fr": "Chef casher privé, repas casher sur demande, repas de Shabbat et de fêtes, minyan et Sefer Torah à Avoriaz",
                                "es": "Chef kosher privado, comidas kosher bajo petición, comidas de Shabat y fiestas, minián y Sefer Torá en Avoriaz",
                                "he": "שף כשר פרטי, ארוחות כשרות לפי בקשה, סעודות שבת וחג, מניין וספר תורה באבוריאז"}[lang]
        if o["@type"] == "FAQPage":
            o["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
    s = s[:mm.start(2)] + json.dumps(ld, ensure_ascii=False) + s[mm.end(2):]

    for i, g in enumerate(gardes):
        s = s.replace(f"\x00{i}\x00", g)
    # contrôle : aucune trace de Chamonix hors des segments site-wide et de la liste des voisines
    corps = re.sub(r'<section class="clair ss wrap conseils" id="voisines">.*?</section>', "", s, flags=re.S)
    corps = re.sub(r'<footer class="pied">.*?</footer>', "", corps, flags=re.S)
    corps = re.sub(r'<div class="nav-ch-menu">.*?</div>', "", corps, flags=re.S)
    corps = re.sub(r'<!--KIT-WP:vt-->.*?<!--/KIT-WP:vt-->', "", corps, flags=re.S)
    for bad in ("hamonix", "שמוני", "Mont Blanc", "Mont-Blanc", "Aiguille", "Arve", "1,040", "1 040", "1.040", "Megève", "King David", "Loup Blanc", "Flocon", "Belle Étoile", "Aigle", "Beth Habad", "בית חב"):
        assert bad not in corps, (lang, bad, corps[corps.find(bad) - 80:corps.find(bad) + 80])
    os.makedirs(f"{pre}{SLUG}", exist_ok=True)
    wr(f"{pre}{SLUG}/index.html", s)
    ecrire_md(f"{pre}{SLUG}/index.html")
    print("page", f"{pre}{SLUG}/index.html")


def ecrire_md(p):
    """index.md : même code que _agentic.py, section 3, pour cette seule page."""
    def meta(h, name):
        r = re.search(rf'<meta name="{name}" content="([^"]*)"', h); return r.group(1) if r else ""
    d = os.path.dirname(p).replace("\\", "/")
    h = open(p, encoding="utf-8").read()
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)([^)\s]*)\)", lambda mm: "](" + __import__("urllib.parse").parse.urljoin(url, mm.group(1)) + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {meta(h, 'description')}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    open(os.path.join(os.path.dirname(p), "index.md"), "w", encoding="utf-8").write(out)


def sitemap_llms():
    s = rd("sitemap.xml"); lignes = s.split("\n")
    for pre in LANGS.values():
        loc = f"{BASE}/{pre}{SLUG}/"
        if f"<loc>{loc}</loc>" in s: continue
        urls = [i for i, x in enumerate(lignes) if "<loc>" in x]
        i = next((i for i in urls if re.search(r"<loc>([^<]*)</loc>", lignes[i]).group(1) > loc), urls[-1] + 1)
        lignes.insert(i, f"  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><priority>0.7</priority></url>"); s = "\n".join(lignes)
        print("sitemap", loc)
    wr("sitemap.xml", s)
    s = rd("llms.txt")
    if f"({BASE}/{SLUG}/)" not in s:
        lignes = s.split("\n")
        i = next(i for i, x in enumerate(lignes) if f"({BASE}/{MODELE}/)" in x)
        lignes.insert(i + 1, f"- [{T['en']['llms']}]({BASE}/{SLUG}/): {T['en']['desc']}")
        wr("llms.txt", "\n".join(lignes)); print("llms.txt")


for lang, pre in LANGS.items():
    page(lang, pre)
sitemap_llms()
print("done")
