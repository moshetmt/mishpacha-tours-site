# -*- coding: utf-8 -*-
"""11/11/2026 : réponses de Mendel (16 vocaux, 01-emails/2026-11-11-vocaux-mendel-services/) et décisions de prix de Moshé
reportées sur les 7 pages de service, en 4 langues. Idempotent.

  python _mendel_1111.py sources   # corrige seulement les JSON de _lot4_contenu/ et _manifeste*  (commit b)
  python _mendel_1111.py sorties   # régénère les pages (via _lot4_0611_services.py), corrige le hub, le formulaire, llms.txt (commit c)

Prix : plus aucun prix du chef nulle part ; chalets 9 500 / 23 500 = chalet seul ; Chabbat 45 / 40 / 30 sans total ; enfants 50 % jusqu'à 5 ans.
Mendel : bougies non comprises, commande le mercredi soir avant Chabbat, minyan sur demande (Sefer Torah si minyan assuré),
bain nordique à Courchevel (petit chalet), masseur pour les hommes et masseuse pour les femmes, activités sur demande sans tarif.
Après _lot4_0611_services.py : le gabarit (page Pessah) apporte la classe l3-luxe au <body> des pages de service ; elle n'était pas en ligne
(le lot 3 est passé après), on la retire pour ne pas changer le dessin. Pages kosher-* : gardent la classe, comme en ligne."""
import glob, io, json, os, re, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
LANGS = [("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")]
SLUGS = ["private-kosher-chalet-alps", "private-kosher-chef-alps", "kosher-meals-delivered-alps", "shabbat-holiday-meals-alps",
         "minyan-sefer-torah-alps", "spa-massage-alps", "activities-alps-kosher-families"]

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

# ------------------------------------------------------------------ textes : {slug: {langue: {chemin: valeur}}}
P = {s: {} for s in SLUGS}

P["private-kosher-chalet-alps"]["en"] = {
 "title": "Private Kosher Chalet in the Alps, Chef and Meals on Quote",
 "description": "A private, strictly kosher chalet in the French Alps with a kashered kitchen. Private chef and meals are added on quote. Written quote before commitment.",
 "hero_sub": "A chalet of your own, with a private chef and the meals of the week and of Shabbat on quote.",
 "trois[2][1]": "A private chef handles weekday and Shabbat meals, on quote, at the chalet or delivered.",
 "intro[0]": "Mishpacha Tours organises stays in private chalets in the Alps, strictly kosher, for your family or your group. Each chalet can come with its own team, on quote: a private chef, and the meals of the week and of Shabbat. The kitchen is kashered before you arrive. You ski, you walk, you rest. When you come back, the table is set.",
 "inclus[1][0]": "A private chef, on quote.",
 "inclus[1][1]": "The chef cooks on site and takes care of all the meals of the week, so nobody has to cook on holiday. Priced separately from the chalet.",
 "inclus[2][0]": "Weekday and Shabbat meals, on quote.",
 "etapes[2][1]": "The kitchen is kashered before you arrive. If you chose the chef, the chef takes care of the meals of the week and of Shabbat.",
 "faq[0][1]": "Prices are per chalet and per week, for the chalet alone. They start from €9,500 for Belle Étoile (Val Thorens) and from €23,500 for Loup Blanc (near Megève). The private chef and the meals come on top, on quote. The price for your dates is given to you in writing with the quote.",
 "faq[1][1]": "A private chef cooks on site, in the kashered kitchen of the chalet, and takes care of all the meals of the week. The chef is priced on quote, on top of the chalet. Meals are served at the chalet or delivered.",
 "faq[2][1]": "Yes. Shabbat meals are possible, at the chalet or delivered, on quote on top of the chalet. Give us your dates and we tell you the nearest minyan. We do not reply during Shabbat.",
 "faq[4][1]": "Yes: the price shown is for the chalet alone, and the chef and the meals are added on quote if you want them. We can also kasher the kitchen of a chalet you rent elsewhere. Tell us what you need and we send you a written quote.",
}
P["private-kosher-chalet-alps"]["fr"] = {
 "title": "Chalet privé casher dans les Alpes, chef et repas sur devis",
 "description": "Un chalet privé strictement casher dans les Alpes, cuisine cachérisée. Chef privé et repas en plus, sur devis. Devis écrit avant tout engagement.",
 "hero_sub": "Votre chalet, avec un chef privé et les repas de la semaine et de Chabbat sur devis.",
 "trois[2][1]": "Un chef privé assure les repas de la semaine et de Chabbat, sur devis, au chalet ou livrés.",
 "intro[0]": "Mishpacha Tours organise vos séjours dans des chalets privés des Alpes, strictement casher, pour votre famille ou votre groupe. Chaque chalet peut venir avec son équipe, sur devis : un chef privé, les repas de la semaine et de Chabbat. La cuisine est cachérisée avant votre arrivée. Vous skiez, vous marchez, vous vous reposez. À votre retour, la table est dressée.",
 "inclus[1][0]": "Un chef privé, sur devis.",
 "inclus[1][1]": "Le chef cuisine sur place et assure tous les repas de la semaine. Personne n'a besoin de cuisiner pendant les vacances. Prix à part du chalet.",
 "inclus[2][0]": "Les repas de la semaine et de Chabbat, sur devis.",
 "etapes[2][1]": "La cuisine est cachérisée avant votre arrivée. Si vous avez choisi le chef, il assure les repas de la semaine et de Chabbat.",
 "faq[0][1]": "Les prix sont par chalet et par semaine, pour le chalet seul. Ils démarrent à partir de 9 500 € pour Belle Étoile (Val Thorens) et à partir de 23 500 € pour Loup Blanc (près de Megève). Le chef privé et les repas viennent en plus, sur devis. Le prix pour vos dates vous est remis par écrit avec le devis.",
 "faq[1][1]": "Un chef privé cuisine sur place, dans la cuisine cachérisée du chalet, et assure tous les repas de la semaine. Il se chiffre sur devis, en plus du chalet. Les repas sont servis au chalet ou livrés.",
 "faq[2][1]": "Oui. Les repas de Chabbat sont possibles, au chalet ou livrés, sur devis en plus du chalet. Donnez-nous vos dates et nous vous indiquons le minyan le plus proche. Nous ne répondons pas pendant Chabbat.",
 "faq[4][1]": "Oui : le prix affiché est celui du chalet seul, et le chef et les repas s'ajoutent sur devis si vous les voulez. Nous pouvons aussi cachériser la cuisine d'un chalet que vous louez ailleurs. Dites-nous ce qu'il vous faut et nous vous remettons un devis écrit.",
}
P["private-kosher-chalet-alps"]["es"] = {
 "title": "Chalé privado kosher en los Alpes, chef y comidas a presupuesto",
 "description": "Un chalé privado estrictamente kosher en los Alpes, con cocina kasherizada. Chef privado y comidas aparte, a presupuesto. Presupuesto escrito antes de comprometerse.",
 "hero_sub": "Su chalé, con un chef privado y las comidas de la semana y del Shabat a presupuesto.",
 "trois[2][1]": "Un chef privado se ocupa de las comidas de la semana y del Shabat, a presupuesto, en el chalé o a domicilio.",
 "intro[0]": "Mishpacha Tours organiza estancias en chalés privados de los Alpes, estrictamente kosher, para su familia o su grupo. Cada chalé puede venir con su propio equipo, a presupuesto: un chef privado y las comidas de la semana y del Shabat. La cocina se kasheriza antes de su llegada. Usted esquía, pasea y descansa. Al volver, la mesa está puesta.",
 "inclus[1][0]": "Un chef privado, a presupuesto.",
 "inclus[1][1]": "El chef cocina en el sitio y se ocupa de todas las comidas de la semana, para que nadie tenga que cocinar de vacaciones. Se cobra aparte del chalé.",
 "inclus[2][0]": "Comidas de la semana y del Shabat, a presupuesto.",
 "etapes[2][1]": "La cocina se kasheriza antes de su llegada. Si eligió el chef, este se ocupa de las comidas de la semana y del Shabat.",
 "faq[0][1]": "Los precios son por chalé y por semana, solo por el chalé. Parten desde 9.500 € para Belle Étoile (Val Thorens) y desde 23.500 € para Loup Blanc (cerca de Megève). El chef privado y las comidas se añaden, a presupuesto. El precio para sus fechas se le entrega por escrito con el presupuesto.",
 "faq[1][1]": "Un chef privado cocina en el sitio, en la cocina kasherizada del chalé, y se ocupa de todas las comidas de la semana. Se presupuesta aparte, además del chalé. Las comidas se sirven en el chalé o se entregan.",
 "faq[2][1]": "Sí. Las comidas de Shabat son posibles, en el chalé o a domicilio, a presupuesto además del chalé. Indíquenos sus fechas y le decimos cuál es el minyan más cercano. No respondemos durante el Shabat.",
 "faq[4][1]": "Sí: el precio indicado es el del chalé solo, y el chef y las comidas se añaden a presupuesto si los desea. También podemos kasherizar la cocina de un chalé que alquile en otro lugar. Díganos lo que necesita y le enviamos un presupuesto escrito.",
}
P["private-kosher-chalet-alps"]["he"] = {
 "title": "צ'אלה פרטית כשרה באלפים, שף וארוחות לפי הצעת מחיר",
 "description": "צ'אלה פרטית כשרה באלפים עם מטבח שהוכשר לפני ההגעה. שף פרטי וארוחות בנוסף, לפי הצעת מחיר. הצעת מחיר בכתב לפני כל התחייבות.",
 "hero_sub": "צ'אלה משלכם, ושף פרטי וארוחות של ימי החול ושל שבת, לפי הצעת מחיר.",
 "trois[2][1]": "שף פרטי מכין את ארוחות ימי החול ואת ארוחות שבת, לפי הצעת מחיר, בצ'אלה או במשלוח.",
 "intro[0]": "Mishpacha Tours מארגנת חופשות כשרות בצ'אלהים פרטיים באלפים, למשפחה או לקבוצה שלכם, בלי ויתור על נוחות. לצ'אלה אפשר להוסיף צוות משלו, לפי הצעת מחיר: שף פרטי וארוחות של ימי החול ושל שבת, בצ'אלה או במשלוח. המטבח מוכשר לפני ההגעה. אתם גולשים, מטיילים ונחים. כשאתם חוזרים, השולחן כבר ערוך.",
 "inclus[1][0]": "שף פרטי, לפי הצעת מחיר.",
 "inclus[1][1]": "השף מבשל במקום ואחראי על כל ארוחות השבוע, כך שאף אחד לא צריך לבשל בחופשה. המחיר נפרד מהמחיר של הצ'אלה.",
 "inclus[2][0]": "ארוחות של ימי החול ושל שבת, לפי הצעת מחיר.",
 "etapes[2][1]": "המטבח מוכשר לפני ההגעה שלכם. אם בחרתם בשף, הוא מטפל בארוחות של ימי החול ושל שבת, כך שאתם נכנסים ישר לחופשה.",
 "faq[0][1]": "המחירים הם לצ'אלה ולשבוע, לצ'אלה בלבד. הם מתחילים ב-9,500 € עבור Belle Étoile (ואל טורנס) וב-23,500 € עבור Loup Blanc (ליד מג'ב). השף הפרטי והארוחות מתווספים, לפי הצעת מחיר. המחיר לתאריכים שלכם נמסר בכתב עם הצעת המחיר.",
 "faq[1][1]": "שף פרטי מבשל במקום, במטבח המוכשר של הצ'אלה, ואחראי על כל ארוחות השבוע. המחיר שלו נפרד ובא בנוסף לצ'אלה, לפי הצעת מחיר. הארוחות מוגשות בצ'אלה או מגיעות במשלוח.",
 "faq[2][1]": "כן. ארוחות שבת אפשריות, בצ'אלה או במשלוח, לפי הצעת מחיר ובנוסף לצ'אלה. מסרו לנו את התאריכים ונגיד לכם איפה המניין הקרוב ביותר. איננו משיבים בשבת.",
 "faq[4][1]": "כן: המחיר שמוצג הוא של הצ'אלה בלבד, והשף והארוחות מתווספים לפי הצעת מחיר אם תרצו. אפשר גם להכשיר את המטבח של צ'אלה ששכרתם במקום אחר. ספרו לנו מה אתם צריכים ונשלח לכם הצעת מחיר בכתב.",
}

P["private-kosher-chef-alps"]["en"] = {
 "title": "Private Kosher Chef in Your Alps Chalet, on Quote",
 "description": "A private kosher chef cooks in your chalet in the Alps: kashered kitchen, a menu built with you, groceries included. On quote, 4 days minimum.",
 "intro[1]": "The chef is priced on quote, for a minimum of 4 days; a single day is possible, at a higher price. Groceries are included, and the price depends on the number of guests. Exceptional products (champagne, fine wines, caviar, special cuts of meat) and mid-week deliveries are extra. Beyond three hours by road from Grenoble, in Verbier or elsewhere in Switzerland for example, meals are not delivered, so the private chef is the formula we offer. Switzerland, Italy and Austria are possible on request.",
 "faq[0][1]": "On quote, for a minimum of 4 days. A single day is possible, at a higher price. Groceries are included and the price depends on the number of guests. Exceptional products (champagne, fine wines, caviar, special cuts of meat) and mid-week deliveries are extra. The price for your dates is sent to you in writing, before any commitment.",
}
P["private-kosher-chef-alps"]["fr"] = {
 "title": "Chef privé casher en chalet, Alpes, sur devis",
 "description": "Un chef privé casher cuisine dans votre chalet des Alpes : cuisine cachérisée, menu construit avec vous, courses comprises. Sur devis, 4 jours minimum.",
 "intro[1]": "Le chef se chiffre sur devis, pour 4 jours minimum ; une seule journée est possible, plus chère. Les courses sont comprises et le prix dépend du nombre de convives. Les produits d'exception (champagne, grands vins, caviar, viandes spéciales) et les livraisons en milieu de semaine sont en supplément. Au-delà de 3 h de route de Grenoble, à Verbier ou ailleurs en Suisse par exemple, les repas ne sont pas livrés : le chef privé est alors la formule que nous proposons. Suisse, Italie et Autriche sont possibles sur demande.",
 "faq[0][1]": "Sur devis, pour 4 jours minimum. Une seule journée est possible, plus chère. Les courses sont comprises et le prix dépend du nombre de convives. Les produits d'exception (champagne, grands vins, caviar, viandes spéciales) et les livraisons en milieu de semaine sont en supplément. Le prix pour vos dates vous est envoyé par écrit avant tout engagement.",
}
P["private-kosher-chef-alps"]["es"] = {
 "title": "Chef privado kosher en su chalé de los Alpes, a presupuesto",
 "description": "Un chef privado kosher cocina en su chalé de los Alpes: cocina kasherizada, menú construido con usted, compras incluidas. A presupuesto, mínimo 4 días.",
 "intro[1]": "El chef se presupuesta, con un mínimo de 4 días; un solo día es posible, a un precio más alto. Las compras están incluidas y el precio depende del número de comensales. Los productos excepcionales (champán, grandes vinos, caviar, carnes especiales) y las entregas a mitad de semana se cobran aparte. A más de 3 horas por carretera de Grenoble, en Verbier o en otro lugar de Suiza por ejemplo, no se entregan comidas: el chef privado es entonces la fórmula que ofrecemos. Suiza, Italia y Austria son posibles bajo petición.",
 "faq[0][1]": "A presupuesto, con un mínimo de 4 días. Un solo día es posible, a un precio más alto. Las compras están incluidas y el precio depende del número de comensales. Los productos excepcionales (champán, grandes vinos, caviar, carnes especiales) y las entregas a mitad de semana se cobran aparte. El precio para sus fechas se envía por escrito antes de cualquier compromiso.",
}
P["private-kosher-chef-alps"]["he"] = {
 "title": "שף פרטי כשר בצ'אלה באלפים, לפי הצעת מחיר",
 "description": "שף פרטי כשר מבשל בצ'אלה שלכם באלפים: מטבח שהוכשר, תפריט שנבנה איתכם, הקניות כלולות. לפי הצעת מחיר, מינימום 4 ימים.",
 "intro[1]": "המחיר לפי הצעת מחיר, למינימום 4 ימים; אפשר גם יום אחד, במחיר גבוה יותר. הקניות כלולות והמחיר תלוי במספר הסועדים. מוצרים יוצאי דופן (שמפניה, יינות מובחרים, קוויאר, בשרים מיוחדים) ומשלוחים באמצע השבוע הם בתוספת. במרחק של יותר משלוש שעות נסיעה מגרנובל, למשל Verbier או במקום אחר בשווייץ, ארוחות אינן מגיעות במשלוח, ולכן שף פרטי הוא הפתרון שאנחנו מציעים. שווייץ, איטליה ואוסטריה אפשריות לפי בקשה.",
 "faq[0][1]": "לפי הצעת מחיר, למינימום 4 ימים. אפשר גם יום אחד, במחיר גבוה יותר. הקניות כלולות והמחיר תלוי במספר הסועדים. מוצרים יוצאי דופן (שמפניה, יינות מובחרים, קוויאר, בשרים מיוחדים) ומשלוחים באמצע השבוע הם בתוספת. המחיר לתאריכים שלכם נשלח אליכם בכתב לפני כל התחייבות.",
}

P["kosher-meals-delivered-alps"]["en"] = {
 "inclus[1][1]": "Starter, main course and dessert, from €28 per person per day. Children up to age 5 pay 50% less; from age 6, full price.",
 "inclus[3][1]": "Friday dinner €45, Saturday lunch €40, seudah shlishit €30 (optional), per person. Challot and wine are delivered on Friday and included. Shabbat candles are not included. A plata or a kumkum is on sale.",
 "inclus[4][1]": "Hanukkah candles and lighting, the meal for Purim, and Pesach on request. The reading of the Megillah is on special request, with a contribution to costs. Tell us which festival falls during your week.",
 "etapes[2][1]": "Orders are taken by Wednesday evening at the latest, the one before the Shabbat concerned, with full payment at the time of order. The meals then arrive every two days.",
 "faq[0][1]": "Per person and per day: the full formula, morning, midday and evening, from €78, and dinner alone, with starter, main course and dessert, from €28. Starting prices vary by resort and season. Children up to age 5 pay 50% less; from age 6, full price.",
 "faq[2][1]": "Yes. Friday dinner is €45, Saturday lunch €40 and seudah shlishit €30 (optional), per person, at the same price in every resort. Challot and wine are delivered on Friday and included; candles are not. Order by the Wednesday evening before Shabbat. Delivery to Courchevel and Megève is confirmed: its cost is added to the price of the meals and shared when several families order in the same resort. A person alone orders the full Shabbat, Friday dinner and Saturday lunch. We also tell you the nearest minyan for your dates.",
 "faq[4][1]": "Orders are taken by Wednesday evening at the latest, the one before the Shabbat concerned, with full payment at the time of order. Send us your dates early and we confirm what is possible in your resort.",
}
P["kosher-meals-delivered-alps"]["fr"] = {
 "inclus[1][1]": "Entrée, plat et dessert, à partir de 28 € par personne et par jour. Les enfants jusqu'à 5 ans paient 50 % de moins ; à partir de 6 ans, plein tarif.",
 "inclus[3][1]": "Dîner du vendredi soir 45 €, déjeuner du samedi 40 €, seouda chlichit 30 € (en option), par personne. Hallot et vin livrés le vendredi et compris. Les bougies de Chabbat ne sont pas comprises. Une plata ou un koumkoum sont en vente.",
 "inclus[4][1]": "Bougies et allumage de Hanouka, repas de Pourim, Pessah sur demande. La lecture de la Méguila se fait sur demande spéciale, avec une participation aux frais. Dites-nous quelle fête tombe pendant votre semaine.",
 "etapes[2][1]": "La commande se prend au plus tard le mercredi soir qui précède le Chabbat concerné, avec paiement complet à la commande. Les repas arrivent ensuite tous les deux jours.",
 "faq[0][1]": "Par personne et par jour : formule complète (matin, midi, soir) à partir de 78 €, soir seul (entrée, plat, dessert) à partir de 28 €. Prix de départ selon station et saison. Enfants jusqu'à 5 ans : 50 % de moins ; à partir de 6 ans, plein tarif.",
 "faq[2][1]": "Oui. Le dîner du vendredi soir est à 45 €, le déjeuner du samedi à 40 € et la seouda chlichit à 30 € (en option), par personne, au même prix dans toutes les stations. Hallot et vin sont livrés le vendredi et compris ; les bougies ne le sont pas. Commandez au plus tard le mercredi soir qui précède le Chabbat. La livraison à Courchevel et à Megève est confirmée : son coût s'ajoute au prix des repas et se partage quand plusieurs familles commandent dans la même station. Une personne seule commande le Chabbat complet, dîner du vendredi et déjeuner du samedi. Nous vous indiquons aussi le minyan le plus proche pour vos dates.",
 "faq[4][1]": "La commande se prend au plus tard le mercredi soir qui précède le Chabbat concerné, avec paiement complet à la commande. Envoyez-nous vos dates tôt et nous confirmons ce qui est possible dans votre station.",
}
P["kosher-meals-delivered-alps"]["es"] = {
 "inclus[1][1]": "Entrante, plato principal y postre, desde 28 € por persona y día. Los niños hasta 5 años pagan un 50 % menos; a partir de 6 años, tarifa completa.",
 "inclus[3][1]": "Cena del viernes 45 €, almuerzo del sábado 40 €, seudá shlishit 30 € (opcional), por persona. Jalot y vino se entregan el viernes y están incluidos. Las velas de Shabat no están incluidas. Hay una plata o un kumkum en venta.",
 "inclus[4][1]": "Velas y encendido de Janucá, comida de Purim, Pésaj bajo petición. La lectura de la Meguilá se hace bajo petición especial, con una participación en los gastos. Díganos qué fiesta cae durante su semana.",
 "etapes[2][1]": "El pedido se hace a más tardar el miércoles por la noche que precede al Shabat en cuestión, con pago completo al pedir. Las comidas llegan después cada dos días.",
 "faq[0][1]": "Por persona y por día: la fórmula completa, mañana, mediodía y noche, desde 78 €, y solo la cena, con entrante, plato principal y postre, desde 28 €. Los precios de partida varían según la estación y la temporada. Los niños hasta 5 años pagan un 50 % menos; a partir de 6 años, tarifa completa.",
 "faq[2][1]": "Sí. La cena del viernes cuesta 45 €, el almuerzo del sábado 40 € y la seudá shlishit 30 € (opcional), por persona, al mismo precio en todas las estaciones. Jalot y vino se entregan el viernes y están incluidos; las velas no. Pida a más tardar el miércoles por la noche que precede al Shabat. La entrega en Courchevel y Megève está confirmada: su coste se suma al precio de las comidas y se reparte cuando varias familias piden en la misma estación. Una persona sola pide el Shabat completo, cena del viernes y almuerzo del sábado. También le indicamos el minyan más cercano para sus fechas.",
 "faq[4][1]": "El pedido se hace a más tardar el miércoles por la noche que precede al Shabat en cuestión, con pago completo al pedir. Envíenos sus fechas con tiempo y le confirmamos lo que es posible en su estación.",
}
P["kosher-meals-delivered-alps"]["he"] = {
 "inclus[1][1]": "ראשונה, מנה עיקרית וקינוח, החל מ-28 € לאדם ליום. ילדים עד גיל 5 משלמים חצי מחיר; מגיל 6, מחיר מלא.",
 "inclus[3][1]": "ארוחת ליל שבת 45 €, ארוחת צהריים בשבת 40 €, סעודה שלישית 30 € (אופציונלית), לאדם. חלות ויין מגיעים ביום שישי וכלולים. נרות שבת אינם כלולים. פלטה או קומקום זמינים לרכישה.",
 "inclus[4][1]": "נרות והדלקה בחנוכה, וארוחה בפורים, ופסח לפי בקשה. קריאת המגילה בבקשה מיוחדת, בהשתתפות בעלויות. ספרו לנו איזה חג חל בשבוע שלכם.",
 "etapes[2][1]": "ההזמנה מתקבלת עד יום רביעי בערב, זה שלפני השבת הרלוונטית, והתשלום המלא הוא בעת ההזמנה. אחר כך הארוחות מגיעות אחת לשני ימים.",
 "faq[0][1]": "לאדם וליום: החבילה המלאה, בוקר, צהריים וערב, החל מ-78 €, וארוחת ערב בלבד, עם ראשונה, מנה עיקרית וקינוח, החל מ-28 €. המחירים משתנים לפי אתר הסקי והעונה. ילדים עד גיל 5 משלמים חצי מחיר; מגיל 6, מחיר מלא.",
 "faq[2][1]": "כן. ארוחת ליל שבת עולה 45 €, ארוחת צהריים בשבת 40 € וסעודה שלישית 30 € (אופציונלית), לאדם, באותו מחיר בכל אתרי הסקי. חלות ויין מגיעים ביום שישי וכלולים; נרות אינם כלולים. הזמינו עד יום רביעי בערב שלפני השבת. משלוח לקורשבל ולמג'ב מאושר: עלותו מתווספת למחיר הארוחות ומתחלקת כשכמה משפחות מזמינות באותו אתר. אדם יחיד מזמין שבת מלאה, ארוחת ליל שבת וארוחת צהריים בשבת. נגיד לכם גם איפה המניין הקרוב ביותר בתאריכים שלכם.",
 "faq[4][1]": "ההזמנה מתקבלת עד יום רביעי בערב, זה שלפני השבת הרלוונטית, והתשלום המלא הוא בעת ההזמנה. שלחו לנו את התאריכים מוקדם ונאשר מה אפשרי באתר הסקי שלכם.",
}

P["shabbat-holiday-meals-alps"]["en"] = {
 "trois[1][1]": "They reach you on Friday, included in the price.",
 "intro[0]": "A week in the mountains often includes a Shabbat, and sometimes a holiday. Mishpacha Tours organises the meals with its kosher team based in the Alps: Friday evening dinner, Saturday lunch and seouda shlishit, each priced per person, at the same price in every resort. Challot and wine are delivered on Friday and included; Shabbat candles are not.",
 "inclus[2][1]": "30 € per person, for the third meal of Shabbat. This meal is optional.",
 "inclus[3][1]": "Delivered on Friday and included in the price. Shabbat candles are not included. Plata or koumkoum are on sale for Shabbat.",
 "inclus[4][1]": "Candles and lighting for Hanukkah, a meal for Purim, Pesach on request. The Megillah reading is on special request, with a contribution to costs.",
 "etapes[0][1]": "Send your resort, dates and number of people on WhatsApp, by the Wednesday evening before Shabbat. We reply the same day.",
 "faq[0][1]": "Friday dinner is 45 €, Saturday lunch 40 € and seouda shlishit 30 €, per person, at the same price in every resort. The seouda shlishit is optional. Delivery is added to the price of the meals and shared when several families order in the same resort.",
 "faq[3][1]": "We offer candles and lighting for Hanukkah and a meal for Purim. The Megillah reading is on special request, with a contribution to costs. Pesach is on request, with its own page. Tell us which holiday falls during your week.",
 "faq[4][1]": "Yes, to your apartment, chalet or hotel, including Courchevel and Megève. Order by the Wednesday evening before Shabbat. A person alone orders the full Shabbat, Friday dinner and Saturday lunch. Beyond 3 hours by road from Grenoble we do not deliver meals: a private chef is the option there.",
}
P["shabbat-holiday-meals-alps"]["fr"] = {
 "trois[1][1]": "Ils vous sont livrés le vendredi, compris dans le prix.",
 "intro[0]": "Une semaine à la montagne comprend souvent un Chabbat, parfois une fête. Mishpacha Tours organise les repas avec son équipe casher basée dans les Alpes : dîner du vendredi soir, déjeuner du samedi et seouda chlichit, chacun au prix par personne, le même dans toutes les stations. Hallot et vin vous sont livrés le vendredi et sont compris ; les bougies de Chabbat ne le sont pas.",
 "inclus[2][1]": "30 € par personne, pour le troisième repas de Chabbat. Ce repas est en option.",
 "inclus[3][1]": "Livrés le vendredi, compris dans le prix. Les bougies de Chabbat ne sont pas comprises. Plata ou koumkoum en vente pour le Chabbat.",
 "inclus[4][1]": "Bougies et allumage de Hanouka, repas de Pourim, Pessah sur demande. La lecture de la Méguila se fait sur demande spéciale, avec une participation aux frais.",
 "etapes[0][1]": "Envoyez-nous votre station, vos dates et le nombre de personnes sur WhatsApp, au plus tard le mercredi soir qui précède le Chabbat. Réponse le jour même.",
 "faq[0][1]": "Le dîner du vendredi coûte 45 €, le déjeuner du samedi 40 € et la seouda chlichit 30 €, par personne, au même prix dans toutes les stations. La seouda chlichit est en option. La livraison s'ajoute au prix des repas et se partage quand plusieurs familles commandent dans la même station.",
 "faq[3][1]": "Nous proposons bougies et allumage de Hanouka et un repas de Pourim. La lecture de la Méguila se fait sur demande spéciale, avec une participation aux frais. Pessah se fait sur demande, avec sa page dédiée. Dites-nous quelle fête tombe pendant votre semaine.",
 "faq[4][1]": "Oui, à votre appartement, chalet ou hôtel, y compris à Courchevel et à Megève. Commandez au plus tard le mercredi soir qui précède le Chabbat. Une personne seule commande le Chabbat complet, dîner du vendredi et déjeuner du samedi. Au-delà de 3 h de route de Grenoble, nous ne livrons pas de repas : la formule chef privé s'applique.",
}
P["shabbat-holiday-meals-alps"]["es"] = {
 "trois[1][1]": "Le llegan el viernes, incluidos en el precio.",
 "intro[0]": "Una semana en la montaña suele incluir un Shabat, y a veces una fiesta. Mishpacha Tours organiza las comidas con su equipo kosher instalado en los Alpes: cena del viernes, almuerzo del sábado y seudá shlishit, cada una con su precio por persona, el mismo en todas las estaciones. Los jalot y el vino se entregan el viernes y están incluidos; las velas de Shabat no.",
 "inclus[2][1]": "30 € por persona, para la tercera comida de Shabat. Esta comida es opcional.",
 "inclus[3][1]": "Entregados el viernes, incluidos en el precio. Las velas de Shabat no están incluidas. Plata o koumkoum a la venta para el Shabat.",
 "inclus[4][1]": "Velas y encendido de Janucá, comida de Purim, Pésaj bajo petición. La lectura de la Meguilá se hace bajo petición especial, con una participación en los gastos.",
 "etapes[0][1]": "Envíenos su estación, sus fechas y el número de personas por WhatsApp, a más tardar el miércoles por la noche que precede al Shabat. Respuesta el mismo día.",
 "faq[0][1]": "La cena del viernes cuesta 45 €, el almuerzo del sábado 40 € y la seudá shlishit 30 €, por persona, al mismo precio en todas las estaciones. La seudá shlishit es opcional. La entrega se suma al precio de las comidas y se reparte cuando varias familias piden en la misma estación.",
 "faq[3][1]": "Ofrecemos velas y encendido de Janucá y una comida de Purim. La lectura de la Meguilá se hace bajo petición especial, con una participación en los gastos. Pésaj se hace bajo petición, con su propia página. Díganos qué fiesta cae durante su semana.",
 "faq[4][1]": "Sí, en su apartamento, chalet u hotel, incluidos Courchevel y Megève. Pida a más tardar el miércoles por la noche que precede al Shabat. Una persona sola pide el Shabat completo, cena del viernes y almuerzo del sábado. A más de 3 horas por carretera de Grenoble no entregamos comidas: se aplica la fórmula de chef privado.",
}
P["shabbat-holiday-meals-alps"]["he"] = {
 "trois[1][1]": "מגיעים אליכם ביום שישי, כלולים במחיר.",
 "intro[0]": "שבוע בהרים כולל לא פעם שבת, ולפעמים גם חג. Mishpacha Tours מארגנת את הארוחות עם צוות הכשרות שלה, שיושב באלפים: ארוחת ערב בליל שישי, ארוחת צהריים בשבת וסעודה שלישית, כל אחת במחיר לאדם, ואותו מחיר בכל אתרי הסקי. חלות ויין מגיעים ביום שישי וכלולים, נרות שבת אינם כלולים.",
 "inclus[2][1]": "30 € לאדם, לארוחה השלישית של שבת. ארוחה זו אופציונלית.",
 "inclus[3][1]": "מגיעים ביום שישי וכלולים במחיר. נרות שבת אינם כלולים. פלטה או קומקום חשמלי למכירה לקראת שבת.",
 "inclus[4][1]": "נרות והדלקה לחנוכה, סעודה לפורים, פסח לפי בקשה. קריאת המגילה בבקשה מיוחדת, בהשתתפות בעלויות.",
 "etapes[0][1]": "שלחו את אתר הסקי, התאריכים ומספר המשתתפים בוואטסאפ, עד יום רביעי בערב שלפני השבת. אנחנו משיבים באותו יום.",
 "faq[0][1]": "ארוחת שישי בערב 45 €, ארוחת שבת בצהריים 40 € וסעודה שלישית 30 €, לאדם, באותו מחיר בכל אתרי הסקי. הסעודה השלישית אופציונלית. המשלוח מתווסף למחיר הארוחות ומתחלק כשכמה משפחות מזמינות באותו אתר.",
 "faq[3][1]": "אנחנו מציעים נרות והדלקה לחנוכה וסעודה לפורים. קריאת המגילה בבקשה מיוחדת, בהשתתפות בעלויות. פסח לפי בקשה, בדף ייעודי. כתבו לנו איזה חג חל בשבוע שלכם.",
 "faq[4][1]": "כן, לדירה, לצ'אלה או למלון, כולל קורשבל ומג'ב. הזמינו עד יום רביעי בערב שלפני השבת. אדם יחיד מזמין שבת מלאה, ארוחת ליל שבת וארוחת צהריים בשבת. מעל 3 שעות נסיעה מגרנובל אין משלוח ארוחות: שם מציעים שף פרטי.",
}

P["minyan-sefer-torah-alps"]["en"] = {
 "description": "A minyan and a Sefer Torah on request in your resort, in winter and in summer. The Sefer Torah is brought only once the minyan is assured. Give us your dates early.",
 "hero_sub": "On request, we gather the families in your resort; the Sefer Torah comes once the minyan is assured.",
 "trois[1][1]": "The team brings a Sefer Torah to your resort once the minyan is assured.",
 "intro[0]": "A minyan is a service on request. When several families stay in the same resort, our kosher team based in the Alps can bring them together for a minyan. It works in winter and in summer, on weekdays too. The more families we know about, the easier the minyan is to form.",
 "intro[1]": "So give us your dates early. Shabbat and weekday prayers take place with Beth Habad of the Alps. A Sefer Torah is brought only if the minyan is assured. Courchevel and Megève have a Beth Habad, but the minyan is not guaranteed there outside the school holidays. A contribution to costs may be requested.",
 "inclus[1][0]": "A Sefer Torah, once the minyan is assured.",
 "inclus[1][1]": "The team brings a Sefer Torah to your resort only if the minyan is complete, in winter and in summer.",
 "inclus[3][1]": "Both resorts have a Beth Habad, which coordinates the minyan and Shabbat. The minyan is not guaranteed there outside the school holidays.",
 "etapes[2][1]": "We tell you what is possible, depending on the families present. The Sefer Torah is brought once the minyan is assured.",
 "faq[0][1]": "The minyan is not free: a contribution to costs may be requested. We have no price to give you on this page. Tell us your dates, and we answer in writing before any commitment on your side. The Megillah reading is on special request, also with a contribution to costs.",
 "faq[3][1]": "No. A minyan is offered on request, depending on the families present, and the Sefer Torah is brought only if the minyan is assured. The earlier you give your dates, the easier it is to form.",
 "faq[4][1]": "Yes. A minyan is possible in every resort in summer, and on weekdays too. A Sefer Torah is brought once the minyan is assured. Tell us your resort and your dates.",
 "faq[5][1]": "Courchevel 1850 and Megève have a Beth Habad on site, but the minyan there is not guaranteed outside the school holidays, when the resorts are quiet. It depends on the families present.",
}
P["minyan-sefer-torah-alps"]["fr"] = {
 "description": "Un minyan et un Sefer Torah sur demande dans votre station, l'hiver comme l'été. Le Sefer Torah n'est apporté que si le minyan est assuré. Donnez-nous vos dates tôt.",
 "hero_sub": "Sur demande, nous réunissons les familles de votre station ; le Sefer Torah suit quand le minyan est assuré.",
 "trois[1][1]": "L'équipe apporte un Sefer Torah dans votre station quand le minyan est assuré.",
 "intro[0]": "Le minyan est un service sur demande. Quand plusieurs familles séjournent dans la même station, notre équipe casher basée dans les Alpes peut les réunir pour un minyan. Cela fonctionne l'hiver et l'été, en semaine aussi. Plus nous connaissons de familles, plus le minyan est facile à former.",
 "intro[1]": "Donnez-nous donc vos dates tôt. Les prières de Chabbat et de semaine ont lieu avec le Beth Habad des Alpes. Un Sefer Torah n'est apporté que si le minyan est assuré. Courchevel et Megève ont un Beth Habad, mais le minyan n'y est pas garanti hors vacances scolaires. Une participation aux frais peut être demandée.",
 "inclus[1][0]": "Un Sefer Torah, quand le minyan est assuré.",
 "inclus[1][1]": "L'équipe n'apporte un Sefer Torah dans votre station que si le minyan est complet, l'hiver comme l'été.",
 "inclus[3][1]": "Les deux stations ont un Beth Habad, qui coordonne le minyan et le Chabbat. Le minyan n'y est pas garanti hors vacances scolaires.",
 "etapes[2][1]": "Nous vous disons ce qui est possible, selon les familles présentes. Le Sefer Torah est apporté quand le minyan est assuré.",
 "faq[0][1]": "Le minyan n'est pas gratuit : une participation aux frais peut être demandée. Nous n'avons pas de prix à vous donner sur cette page. Donnez-nous vos dates, nous répondons par écrit avant tout engagement de votre part. La lecture de la Méguila se fait sur demande spéciale, avec aussi une participation aux frais.",
 "faq[3][1]": "Non. Un minyan se propose sur demande, selon les familles présentes, et le Sefer Torah n'est apporté que si le minyan est assuré. Plus vous donnez vos dates tôt, plus il est facile à former.",
 "faq[4][1]": "Oui. Un minyan est possible dans toutes les stations l'été, en semaine aussi. Un Sefer Torah est apporté quand le minyan est assuré. Dites-nous votre station et vos dates.",
 "faq[5][1]": "Courchevel 1850 et Megève ont un Beth Habad sur place, mais le minyan n'y est pas garanti hors vacances scolaires, quand les stations sont calmes. Cela dépend des familles présentes.",
}
P["minyan-sefer-torah-alps"]["es"] = {
 "description": "Un minyan y un Sefer Torá bajo petición en su estación, en invierno y en verano. El Sefer Torá solo se lleva si el minyan está asegurado. Dénos sus fechas con tiempo.",
 "hero_sub": "Bajo petición, reunimos a las familias de su estación; el Sefer Torá llega cuando el minyan está asegurado.",
 "trois[1][1]": "El equipo lleva un Sefer Torá a su estación cuando el minyan está asegurado.",
 "intro[0]": "El minyan es un servicio bajo petición. Cuando varias familias se alojan en la misma estación, nuestro equipo kosher instalado en los Alpes puede reunirlas para un minyan. Funciona en invierno y en verano, también entre semana. Cuantas más familias conocemos, más fácil es formar el minyan.",
 "intro[1]": "Dénos, pues, sus fechas con tiempo. Las oraciones de Shabat y de entre semana se hacen con el Beth Habad de los Alpes. Solo se lleva un Sefer Torá si el minyan está asegurado. Courchevel y Megève tienen un Beth Habad, pero el minyan no está garantizado allí fuera de las vacaciones escolares. Puede pedirse una participación en los gastos.",
 "inclus[1][0]": "Un Sefer Torá, cuando el minyan está asegurado.",
 "inclus[1][1]": "El equipo solo lleva un Sefer Torá a su estación si el minyan está completo, en invierno y en verano.",
 "inclus[3][1]": "Ambas estaciones tienen un Beth Habad, que coordina el minyan y el Shabat. El minyan no está garantizado allí fuera de las vacaciones escolares.",
 "etapes[2][1]": "Le decimos qué es posible, según las familias presentes. El Sefer Torá se lleva cuando el minyan está asegurado.",
 "faq[0][1]": "El minyan no es gratuito: puede pedirse una participación en los gastos. No tenemos un precio que darle en esta página. Dénos sus fechas y respondemos por escrito antes de cualquier compromiso por su parte. La lectura de la Meguilá se hace bajo petición especial, también con una participación en los gastos.",
 "faq[3][1]": "No. Un minyan se ofrece bajo petición, según las familias presentes, y el Sefer Torá solo se lleva si el minyan está asegurado. Cuanto antes nos dé sus fechas, más fácil es formarlo.",
 "faq[4][1]": "Sí. En verano un minyan es posible en todas las estaciones, también entre semana. Se lleva un Sefer Torá cuando el minyan está asegurado. Díganos su estación y sus fechas.",
 "faq[5][1]": "Courchevel y Megève tienen un Beth Habad en el lugar, pero el minyan no está garantizado allí fuera de las vacaciones escolares, cuando las estaciones están tranquilas. Depende de las familias presentes.",
}
P["minyan-sefer-torah-alps"]["he"] = {
 "description": "מניין וספר תורה לפי בקשה באתר הסקי שלכם, בחורף ובקיץ. ספר התורה מובא רק כשהמניין מובטח. ספרו לנו את התאריכים מוקדם.",
 "hero_sub": "לפי בקשה אנחנו מכנסים את המשפחות באתר שלכם; ספר התורה מגיע כשהמניין מובטח.",
 "trois[1][1]": "הצוות מביא ספר תורה לאתר שלכם כשהמניין מובטח.",
 "intro[0]": "מניין הוא שירות לפי בקשה. כשכמה משפחות שוהות באותו אתר, צוות הכשרות שלנו שיושב באלפים יכול לכנס אותן למניין. זה עובד בחורף ובקיץ, וגם בימי חול. ככל שאנחנו מכירים יותר משפחות, קל יותר להרכיב מניין.",
 "intro[1]": "לכן ספרו לנו את התאריכים מוקדם. תפילות שבת וימי חול נערכות עם בית חב״ד של האלפים. ספר תורה מובא רק אם המניין מובטח. בקורשבל ובמג'ב יש בית חב״ד, אבל המניין שם אינו מובטח מחוץ לחופשות בית הספר. ייתכן שתתבקשו להשתתף בעלויות.",
 "inclus[1][0]": "ספר תורה, כשהמניין מובטח.",
 "inclus[1][1]": "הצוות מביא ספר תורה לאתר שלכם רק אם המניין שלם, בחורף ובקיץ.",
 "inclus[3][1]": "בשני האתרים יש בית חב״ד, שמרכז את המניין ואת השבת. המניין שם אינו מובטח מחוץ לחופשות בית הספר.",
 "etapes[2][1]": "נגיד לכם מה אפשרי, לפי המשפחות הנוכחיות. ספר התורה מובא כשהמניין מובטח.",
 "faq[0][1]": "המניין אינו ללא עלות: ייתכן שתתבקשו להשתתף בעלויות. אין לנו מחיר למסור בדף הזה. ספרו לנו את התאריכים, ואנחנו משיבים בכתב לפני כל התחייבות מצדכם. קריאת המגילה בבקשה מיוחדת, גם היא בהשתתפות בעלויות.",
 "faq[3][1]": "לא. מניין מוצע לפי בקשה, לפי המשפחות הנוכחיות, וספר התורה מובא רק אם המניין מובטח. ככל שתמסרו את התאריכים מוקדם יותר, קל יותר להרכיב אותו.",
 "faq[4][1]": "כן. בקיץ מניין אפשרי בכל האתרים, וגם בימי חול. ספר תורה מובא כשהמניין מובטח. ספרו לנו את האתר ואת התאריכים.",
 "faq[5][1]": "בקורשבל 1850 ובמג'ב יש בית חב״ד במקום, אבל המניין שם אינו מובטח מחוץ לחופשות בית הספר, כשהאתרים שקטים. זה תלוי במשפחות הנוכחיות.",
}

P["spa-massage-alps"]["en"] = {
 "phrase": "Come back from the slopes to warm water and silence.",
 "description": "Heated pool, hammam, Nordic bath, jacuzzi or sauna at your private kosher chalet. A masseur for men, a masseuse for women, on request.",
 "trois[2][1]": "A masseur for men, a masseuse for women or a pedicurist at the chalet, on request, appears on your single quote.",
 "intro[1]": "In Megève, the spa faces the Mont-Blanc. The house is silent. If you would like a massage or a pedicurist at the chalet, tell us. The massage is given by a masseur for men and a masseuse for women, in every resort. It is on request, and it joins the same quote as your stay.",
 "inclus[1][1]": "The Nordic bath is in Courchevel, in the small chalet. Tell us if you would like it, and we check it fits your dates.",
 "inclus[4][0]": "Massage or pedicurist, on request.",
 "inclus[4][1]": "A masseur for men and a masseuse for women, in every resort. We pass on your wishes and tell you what is possible. No promise is made before we have checked.",
 "faq[0][1]": "It depends on the chalet. Heated pools and a hammam in Courchevel, a jacuzzi and a sauna in Les Menuires and near Megève, a Nordic bath in the small chalet in Courchevel. Tell us your resort, we tell you what is there.",
 "faq[1][1]": "Yes, on request, in every resort. The massage is given by a masseur for men and a masseuse for women. We cannot promise availability before checking your resort and dates. It appears on the same quote as your stay.",
 "faq[3][1]": "We reply every day except Shabbat. Meals and service at the chalet are shomer Shabbat.",
}
P["spa-massage-alps"]["fr"] = {
 "phrase": "Rentrez des pistes vers l'eau chaude et le silence.",
 "description": "Piscine chauffée, hammam, bain nordique, jacuzzi ou sauna dans votre chalet privé casher. Masseur pour les hommes, masseuse pour les femmes, sur demande.",
 "trois[2][1]": "Un masseur pour les hommes, une masseuse pour les femmes ou une pédicure au chalet, sur demande, figure sur votre devis unique.",
 "intro[1]": "À Megève, le spa fait face au Mont-Blanc. La maison est silencieuse. Si vous souhaitez un massage ou une pédicure au chalet, dites-le-nous. Le massage est assuré par un masseur pour les hommes et une masseuse pour les femmes, dans toutes les stations. C'est sur demande, et cela rejoint le même devis que votre séjour.",
 "inclus[1][1]": "Le bain nordique est à Courchevel, dans le petit chalet. Dites-nous si vous le souhaitez, nous vérifions qu'il convient à vos dates.",
 "inclus[4][0]": "Massage ou pédicure, sur demande.",
 "inclus[4][1]": "Un masseur pour les hommes et une masseuse pour les femmes, dans toutes les stations. Nous transmettons vos souhaits et vous disons ce qui est possible. Aucune promesse avant vérification.",
 "faq[0][1]": "Cela dépend du chalet. Piscines chauffées et hammam à Courchevel, jacuzzi et sauna aux Menuires et près de Megève, bain nordique dans le petit chalet de Courchevel. Donnez-nous votre station, nous vous disons ce qui s'y trouve.",
 "faq[1][1]": "Oui, sur demande, dans toutes les stations. Le massage est assuré par un masseur pour les hommes et une masseuse pour les femmes. Nous ne pouvons pas promettre une disponibilité avant d'avoir vérifié votre station et vos dates. Cela figure sur le même devis que votre séjour.",
 "faq[3][1]": "Nous répondons tous les jours sauf le Chabbat. Les repas et le service du chalet sont shomer Chabbat.",
}
P["spa-massage-alps"]["es"] = {
 "phrase": "Vuelva de las pistas al agua caliente y al silencio.",
 "description": "Piscina climatizada, hammam, baño nórdico, jacuzzi o sauna en su chalet privado kosher. Masajista para hombres y masajista para mujeres, bajo petición.",
 "trois[2][1]": "Un masajista para hombres, una masajista para mujeres o una pedicura en el chalet, bajo petición, figura en su presupuesto único.",
 "intro[1]": "En Megève, el spa mira al Mont Blanc. La casa está en silencio. Si desea un masaje o una pedicura en el chalet, díganoslo. El masaje lo da un masajista para los hombres y una masajista para las mujeres, en todas las estaciones. Es bajo petición y se suma al mismo presupuesto que su estancia.",
 "inclus[1][1]": "El baño nórdico está en Courchevel, en el chalet pequeño. Díganos si lo desea y comprobamos que encaje con sus fechas.",
 "inclus[4][0]": "Masaje o pedicura, bajo petición.",
 "inclus[4][1]": "Un masajista para los hombres y una masajista para las mujeres, en todas las estaciones. Transmitimos sus deseos y le decimos qué es posible. No prometemos nada antes de comprobarlo.",
 "faq[0][1]": "Depende del chalet. Piscinas climatizadas y hammam en Courchevel, jacuzzi y sauna en Les Menuires y cerca de Megève, baño nórdico en el chalet pequeño de Courchevel. Indíquenos su estación y le decimos qué hay.",
 "faq[1][1]": "Sí, bajo petición, en todas las estaciones. El masaje lo da un masajista para los hombres y una masajista para las mujeres. No podemos prometer disponibilidad antes de comprobar su estación y sus fechas. Figura en el mismo presupuesto que su estancia.",
 "faq[3][1]": "Respondemos todos los días excepto el Shabat. Las comidas y el servicio del chalet son shomer Shabat.",
}
P["spa-massage-alps"]["he"] = {
 "phrase": "חזרו מהמסלולים אל מים חמים ושקט.",
 "description": "בריכה מחוממת, חמאם, אמבט נורדי, ג'קוזי או סאונה בצ'אלה פרטית כשרה. מעסה לגברים ומעסה לנשים לפי בקשה, בהצעת מחיר אחת בכתב.",
 "trois[2][1]": "מעסה לגברים, מעסה לנשים או פדיקוריסטית בצ'אלה, לפי בקשה, מופיעים באותה הצעה.",
 "intro[1]": "במג'ב הספא פונה אל מון בלאן. הבית שקט. אם תרצו עיסוי או פדיקוריסטית בצ'אלה, כתבו לנו. העיסוי ניתן על ידי מעסה לגברים ומעסה לנשים, בכל אתרי הסקי. זה לפי בקשה, וזה נכנס לאותה הצעת מחיר של החופשה.",
 "inclus[1][1]": "האמבט הנורדי נמצא בקורשבל, בצ'אלה הקטנה. כתבו לנו אם תרצו, ונבדוק שהוא מתאים לתאריכים שלכם.",
 "inclus[4][0]": "עיסוי או פדיקוריסטית, לפי בקשה.",
 "inclus[4][1]": "מעסה לגברים ומעסה לנשים, בכל אתרי הסקי. אנחנו מעבירים את בקשתכם ואומרים לכם מה אפשרי. לא מבטיחים לפני שבדקנו.",
 "faq[0][1]": "זה תלוי בצ'אלה. בריכות מחוממות וחמאם בקורשבל, ג'קוזי וסאונה בלה מנואר וליד מג'ב, אמבט נורדי בצ'אלה הקטנה בקורשבל. כתבו לנו את אתר הסקי ונאמר לכם מה יש שם.",
 "faq[1][1]": "כן, לפי בקשה, בכל אתרי הסקי. העיסוי ניתן על ידי מעסה לגברים ומעסה לנשים. איננו יכולים להבטיח זמינות לפני שבדקנו את אתר הסקי ואת התאריכים. זה מופיע באותה הצעה של החופשה.",
 "faq[3][1]": "אנחנו עונים בכל יום חוץ משבת. הארוחות והשירות בצ'אלה שומר שבת.",
}

P["activities-alps-kosher-families"]["en"] = {
 "description": "Ski rental, dog sled, mountain guide, rental car, transfers and event organisation for kosher families in the Alps. All on request, on one written quote.",
 "hero_sub": "Skis, dog sled, guide, transfers, events: all on request, on a single written quote.",
 "trois[0][1]": "Ski rental, dog sled, snowmobile, mountain guide, rental car, transfers.",
 "intro[0]": "Your stay does not stop at the chalet. Tell us what your family would enjoy and we add it to the same quote: skis to rent, a ride behind a dog sled, a mountain guide, a car for the week, transfers to and from the airport or station. Everything is on request, so nothing is booked before you have approved it, and no price is published.",
 "intro[1]": "In summer, the Alps open onto lakes and walks. Annecy, Aix-les-Bains and Grenoble are close, and a villa in Saint-Tropez is possible. We also organise events: a private evening with a DJ, a birthday, mostly in summer at the Saint-Tropez villa, with summer rates on request. We plan no activity on Shabbat or on holidays. Whatever is not listed here, ask us and we check.",
 "faq[0][1]": "On request, on one quote: ski rental, dog sled, snowmobile, mountain guide, rental car, transfers and event organisation. In summer: lakes, walks, Annecy, Aix-les-Bains, Grenoble and a villa in Saint-Tropez. For anything else, ask us and we check.",
 "faq[1][1]": "Everything is on request and no price is published. Each activity is priced on your written quote, with the price for your dates, before any commitment. Transfers are carried out and billed by the driver.",
 "faq[3][1]": "A mountain guide is possible on request. For lift passes and ski instructors, nothing is confirmed: tell us what you need, we check with the team and answer in writing. Ski rental is available on request.",
}
ACT_NEW_EN = {1: ["Dog sled and snowmobile.", "A ride behind a team of sled dogs, or a snowmobile outing, on request. Tell us your resort and we tell you what we can arrange."],
              2: ["Mountain guide.", "A mountain guide, on request. Tell us your resort and your dates, and we tell you what we can arrange."],
              5: ["Event organisation.", "A private evening with a DJ, a birthday: we organise it for one or two evenings and take care of everything, mostly in summer at the Saint-Tropez villa, and in winter too on request. Summer rates on request."]}
P["activities-alps-kosher-families"]["fr"] = {
 "description": "Location de skis, traîneau à chiens, guide de montagne, voiture, transferts et organisation d'événements, pour familles casher dans les Alpes. Tout sur demande, un seul devis.",
 "hero_sub": "Skis, traîneau à chiens, guide, transferts, événements : tout sur demande, sur un seul devis écrit.",
 "trois[0][1]": "Location de skis, traîneau à chiens, motoneige, guide de montagne, voiture, transferts.",
 "intro[0]": "Votre séjour ne s'arrête pas au chalet. Dites-nous ce qui plairait à votre famille et nous l'ajoutons au même devis : des skis à louer, une balade en traîneau à chiens, un guide de montagne, une voiture pour la semaine, des transferts depuis l'aéroport ou la gare. Tout est sur demande, rien n'est réservé avant votre accord, et aucun tarif n'est publié.",
 "intro[1]": "L'été, les Alpes s'ouvrent sur les lacs et les sentiers. Annecy, Aix-les-Bains et Grenoble sont proches, et une villa à Saint-Tropez est possible. Nous organisons aussi des événements : une soirée privée avec DJ, un anniversaire, surtout l'été à la villa de Saint-Tropez, tarifs d'été sur demande. Nous ne prévoyons aucune activité le Chabbat ni les jours de fête. Pour tout ce qui n'est pas listé ici, demandez-nous, nous vérifions.",
 "faq[0][1]": "Sur demande, sur un seul devis : location de skis, traîneau à chiens, motoneige, guide de montagne, location de voiture, transferts et organisation d'événements. L'été : lacs, marche, Annecy, Aix-les-Bains, Grenoble et une villa à Saint-Tropez. Pour le reste, demandez-nous, nous vérifions.",
 "faq[1][1]": "Tout est sur demande et aucun tarif n'est publié. Chaque activité est chiffrée sur votre devis écrit, au prix de vos dates, avant tout engagement. Les transferts sont effectués et facturés par le chauffeur.",
 "faq[3][1]": "Un guide de montagne est possible sur demande. Pour les forfaits de remontées et les moniteurs, rien n'est confirmé : dites-nous ce qu'il vous faut, nous vérifions avec l'équipe et répondons par écrit. La location de skis est possible sur demande.",
}
ACT_NEW_FR = {1: ["Traîneau à chiens et motoneige.", "Une balade derrière un attelage de chiens de traîneau, ou une sortie en motoneige, sur demande. Dites-nous votre station, nous vous disons ce que nous pouvons organiser."],
              2: ["Guide de montagne.", "Un guide de montagne, sur demande. Dites-nous votre station et vos dates, nous vous disons ce que nous pouvons organiser."],
              5: ["Organisation d'événements.", "Une soirée privée avec DJ, un anniversaire : nous l'organisons pour un soir ou deux et nous nous occupons de tout, surtout l'été à la villa de Saint-Tropez, et l'hiver aussi sur demande. Tarifs d'été sur demande."]}
P["activities-alps-kosher-families"]["es"] = {
 "description": "Alquiler de esquís, trineo de perros, guía de montaña, coche, traslados y organización de eventos para familias kosher en los Alpes. Todo bajo petición, un solo presupuesto.",
 "hero_sub": "Esquís, trineo de perros, guía, traslados, eventos: todo bajo petición, en un solo presupuesto.",
 "trois[0][1]": "Alquiler de esquís, trineo de perros, moto de nieve, guía de montaña, coche, traslados.",
 "intro[0]": "Su estancia no termina en el chalet. Díganos qué le gustaría a su familia y lo añadimos al mismo presupuesto: esquís de alquiler, un paseo en trineo de perros, un guía de montaña, un coche para la semana, traslados desde el aeropuerto o la estación. Todo es bajo petición, nada se reserva sin su acuerdo y no se publica ninguna tarifa.",
 "intro[1]": "En verano, los Alpes se abren a lagos y senderos. Annecy, Aix-les-Bains y Grenoble están cerca, y es posible una villa en Saint-Tropez. También organizamos eventos: una velada privada con DJ, un cumpleaños, sobre todo en verano en la villa de Saint-Tropez, con tarifas de verano bajo petición. No prevemos ninguna actividad en Shabat ni en días de fiesta. Para lo que no figura aquí, pregúntenos y lo comprobamos.",
 "faq[0][1]": "Bajo petición, en un solo presupuesto: alquiler de esquís, trineo de perros, moto de nieve, guía de montaña, alquiler de coche, traslados y organización de eventos. En verano: lagos, paseos, Annecy, Aix-les-Bains, Grenoble y una villa en Saint-Tropez. Para lo demás, pregúntenos y lo comprobamos.",
 "faq[1][1]": "Todo es bajo petición y no se publica ninguna tarifa. Cada actividad se cotiza en su presupuesto escrito, al precio de sus fechas, antes de cualquier compromiso. Los traslados los realiza y factura el conductor.",
 "faq[3][1]": "Un guía de montaña es posible bajo petición. Para los forfaits de remontes y los monitores, nada está confirmado: díganos lo que necesita, lo comprobamos con el equipo y respondemos por escrito. El alquiler de esquís es posible bajo petición.",
}
ACT_NEW_ES = {1: ["Trineo de perros y moto de nieve.", "Un paseo con un tiro de perros de trineo, o una salida en moto de nieve, bajo petición. Díganos su estación y le decimos qué podemos organizar."],
              2: ["Guía de montaña.", "Un guía de montaña, bajo petición. Díganos su estación y sus fechas y le decimos qué podemos organizar."],
              5: ["Organización de eventos.", "Una velada privada con DJ, un cumpleaños: lo organizamos para una o dos noches y nos ocupamos de todo, sobre todo en verano en la villa de Saint-Tropez, y también en invierno bajo petición. Tarifas de verano bajo petición."]}
P["activities-alps-kosher-families"]["he"] = {
 "description": "השכרת סקי, מזחלת כלבים, מדריך הרים, רכב שכור, העברות וארגון אירועים למשפחות כשרות באלפים. הכול לפי בקשה, בהצעת מחיר אחת בכתב.",
 "hero_sub": "סקי, מזחלת כלבים, מדריך, העברות, אירועים: הכול לפי בקשה, בהצעת מחיר אחת בכתב.",
 "trois[0][1]": "השכרת סקי, מזחלת כלבים, אופנוע שלג, מדריך הרים, רכב שכור, העברות.",
 "intro[0]": "החופשה שלכם לא נעצרת בצ'אלה. כתבו לנו מה המשפחה תאהב ונוסיף את זה לאותה הצעה: סקי להשכרה, נסיעה במזחלת כלבים, מדריך הרים, רכב לשבוע, העברות מהשדה או מהתחנה. הכול לפי בקשה, שום דבר לא נסגר לפני שאישרתם, ולא מפורסם מחיר.",
 "intro[1]": "בקיץ האלפים נפתחים לאגמים ולשבילים. אנסי, Aix-les-Bains וגרנובל קרובים, ואפשר גם וילה בסן טרופה. אנחנו מארגנים גם אירועים: ערב פרטי עם די-ג'יי, יום הולדת, בעיקר בקיץ בווילה בסן טרופה, ומחירי הקיץ לפי בקשה. איננו מתכננים שום פעילות בשבת ובימי חג. על כל מה שלא כתוב כאן, שאלו אותנו ונבדוק.",
 "faq[0][1]": "לפי בקשה, בהצעה אחת: השכרת סקי, מזחלת כלבים, אופנוע שלג, מדריך הרים, רכב שכור, העברות וארגון אירועים. בקיץ: אגמים, הליכה, אנסי, Aix-les-Bains, גרנובל ווילה בסן טרופה. על כל השאר, שאלו ונבדוק.",
 "faq[1][1]": "הכול לפי בקשה ולא מפורסם מחיר. כל פעילות מתומחרת בהצעה הכתובה, במחיר התאריכים שלכם, לפני כל התחייבות. ההעברות מבוצעות ומחויבות על ידי הנהג.",
 "faq[3][1]": "מדריך הרים אפשרי לפי בקשה. לגבי כרטיסי רכבלים ומדריכי סקי, שום דבר עדיין לא מאושר: כתבו לנו מה אתם צריכים, נבדוק עם הצוות ונענה בכתב. השכרת סקי אפשרית לפי בקשה.",
}
ACT_NEW_HE = {1: ["מזחלת כלבים ואופנוע שלג.", "נסיעה אחרי צוות כלבי מזחלת, או טיול באופנוע שלג, לפי בקשה. כתבו לנו את אתר הסקי ונאמר לכם מה אפשר לארגן."],
              2: ["מדריך הרים.", "מדריך הרים, לפי בקשה. כתבו לנו את אתר הסקי ואת התאריכים ונאמר לכם מה אפשר לארגן."],
              5: ["ארגון אירועים.", "ערב פרטי עם די-ג'יי, יום הולדת: אנחנו מארגנים אותו לערב או לשניים ודואגים להכול, בעיקר בקיץ בווילה בסן טרופה, ובחורף גם כן לפי בקשה. מחירי הקיץ לפי בקשה."]}
ACT_NEW = {"en": ACT_NEW_EN, "fr": ACT_NEW_FR, "es": ACT_NEW_ES, "he": ACT_NEW_HE}

def setp(d, path, val):
    toks = re.findall(r"[^.\[\]]+", path); o = d
    for t in toks[:-1]: o = o[int(t)] if t.isdigit() else o[t]
    last = toks[-1]
    if last.isdigit(): o[int(last)] = val
    else: o[last] = val

def sources():
    for slug in SLUGS:
        p = f"_lot4_contenu/{slug}.json"; d = json.loads(rd(p))
        for l, kv in P[slug].items():
            for path, val in kv.items(): setp(d[l], path, val)
        if slug == "activities-alps-kosher-families":     # 6 éléments -> 7 : traîneau et motoneige, guide, événements ; skis, voiture, transferts, été gardés
            for l in ("en", "fr", "es", "he"):
                inc = d[l]["inclus"]
                if len(inc) == 6:    # ordre d'origine : 0 skis, 1 traîneau, 2 voiture, 3 transferts, 4 extras événements, 5 été
                    d[l]["inclus"] = [inc[0], ACT_NEW[l][1], ACT_NEW[l][2], inc[2], inc[3], ACT_NEW[l][5], inc[5]]
        wr(p, json.dumps(d, ensure_ascii=False, indent=1).replace("\n", "\r\n"))
    # blurb du manifeste (« Chabbat et fêtes, préparés ») : plus de bougies
    for p in ("_manifeste.py", "_manifeste_trad.json"):
        s = rd(p)
        for a, b in MANIF: s = s.replace(a, b)
        wr(p, s)
    print("sources : 7 JSON + manifeste")

MANIF = [("Challot, wine, candles, and a minyan with a Sefer Torah on request.", "Challot and wine, and a minyan with a Sefer Torah on request."),
         ("Hallot, vin, bougies, et un minyan avec Sefer Torah sur demande.", "Hallot et vin, et un minyan avec Sefer Torah sur demande."),
         ("Jalot, vino, velas y un minyan con Sefer Torá bajo pedido.", "Jalot y vino, y un minyan con Sefer Torá bajo pedido."),
         ("חלות, יין, נרות ומניין עם ספר תורה לפי בקשה.", "חלות, יין ומניין עם ספר תורה לפי בקשה.")]

# ------------------------------------------------------------------ hub, formulaire, llms.txt
SP = r"[\s\xa0 ]"
def strip_bdi(t): return re.sub(r"</?bdi[^>]*>", "", t)
HUB = {
 "en": dict(
   cost=(r"Shabbat meals cost €30 to €45\. A private chef starts at .*?per day, a chalet at (.*?) per week\.",
         "Shabbat meals are €45 for Friday dinner, €40 for Saturday lunch and €30 for seuda shlishit, which is optional. A private chef is quoted for your group, for a minimum of 4 days. A chalet starts at {c} per week, for the chalet alone, with the chef and the meals on quote."),
   row=(r"(<li><span>Private kosher chef in your chalet), per day</span><b[^>]*>from €1,568</b></li>", r"\1</span><b>On quote, 4 days minimum</b></li>"),
   rowmd=(r"(- Private kosher chef in your chalet), per day\*\*from €1,568\*\*", r"\1**On quote, 4 days minimum**"),
   kids=("Children up to 5: about 30% less.", "Children up to 5: 50% less. From age 6, full price."),
   mg=("a Megillah reading", "a Megillah reading on special request")),
 "fr": dict(
   cost=(r"les repas de Chabbat coûtent de 30 à 45 €\. Un chef privé part de .*? par jour, un chalet de (.*?) la semaine\.",
         "les repas de Chabbat coûtent 45 € le dîner du vendredi, 40 € le déjeuner du samedi et 30 € la seouda chlichit, en option. Un chef privé se chiffre pour votre groupe, pour 4 jours minimum. Un chalet part de {c} la semaine, chalet seul, avec le chef et les repas sur devis."),
   row=(r"(<li><span>Chef privé casher dans votre chalet), par jour</span><b[^>]*>à partir de 1" + SP + r"568" + SP + r"€</b></li>", r"\1</span><b>Sur devis, 4 jours minimum</b></li>"),
   rowmd=(r"(- Chef privé casher dans votre chalet), par jour\*\*à partir de 1" + SP + r"568" + SP + r"€\*\*", r"\1**Sur devis, 4 jours minimum**"),
   kids=("Enfants jusqu’à 5 ans : environ 30 % de moins.", "Enfants jusqu’à 5 ans : 50 % de moins. À partir de 6 ans, plein tarif."),
   mg=("une lecture de la Méguila", "une lecture de la Méguila sur demande spéciale")),
 "es": dict(
   cost=(r"las comidas de Shabat cuestan de 30 a 45 €\. Un chef privado parte de .*? por día y un chalé de (.*?) por semana\.",
         "las comidas de Shabat cuestan 45 € la cena del viernes, 40 € el almuerzo del sábado y 30 € la seudá shlishit, opcional. Un chef privado se presupuesta para su grupo, con un mínimo de 4 días. Un chalé parte de {c} por semana, solo el chalé, con el chef y las comidas a presupuesto."),
   row=(r"(<li><span>Chef privado kosher en su chalé), por día</span><b[^>]*>desde 1\.568 €</b></li>", r"\1</span><b>A presupuesto, mínimo 4 días</b></li>"),
   rowmd=(r"(- Chef privado kosher en su chalé), por día\*\*desde 1\.568 €\*\*", r"\1**A presupuesto, mínimo 4 días**"),
   kids=("Niños hasta 5 años: alrededor de un 30 % menos.", "Niños hasta 5 años: un 50 % menos. A partir de 6 años, tarifa completa."),
   mg=("una lectura de la Meguilá", "una lectura de la Meguilá bajo petición especial")),
 "he": dict(
   cost=(r"ארוחות שבת עולות\s*(?:<bdi[^>]*>)?\s*30–45 €\s*(?:</bdi>)?\s*\. מחיר שף פרטי מתחיל ב־.*?ומחיר צ'אלה ב־(.*?) לשבוע\.",
         "ארוחות שבת עולות <bdi dir=\"ltr\">45 €</bdi> לארוחת ליל שבת, <bdi dir=\"ltr\">40 €</bdi> לארוחת הצהריים בשבת ו־<bdi dir=\"ltr\">30 €</bdi> לסעודה שלישית, שהיא אופציונלית. שף פרטי מתומחר לפי הקבוצה, למינימום 4 ימים. מחיר צ'אלה מתחיל ב־{c} לשבוע, לצ'אלה בלבד, והשף והארוחות לפי הצעת מחיר."),
   row=(r"(<li><span>שף פרטי כשר בצ'אלה שלכם), ליום</span><b[^>]*>.*?</b></li>", r"\1</span><b>לפי הצעת מחיר, מינימום 4 ימים</b></li>"),
   rowmd=(r"(- שף פרטי כשר בצ'אלה שלכם), ליום\*\*[^*]*\*\*", r"\1**לפי הצעת מחיר, מינימום 4 ימים**"),
   kids=("ילדים עד גיל 5: כ־30% פחות.", "ילדים עד גיל 5: 50% פחות. מגיל 6, מחיר מלא."),
   mg=("קריאת מגילה", "קריאת מגילה בבקשה מיוחדת")),
}
FORM_CHEF = {"en": "on quote", "fr": "sur devis", "es": "a presupuesto", "he": "לפי הצעת מחיר"}

def hub():
    n = 0
    for l, pre in LANGS:
        h = HUB[l]
        for ext in ("html", "md"):
            p = f"{pre}kosher-services-french-alps/index.{ext}"; s = o = rd(p)
            def cost(m, l=l, h=h):
                t = h["cost"][1].replace("{c}", m.group(1))
                return t if "<bdi" in m.group(0) or l != "he" else strip_bdi(t)
            s = re.sub(h["cost"][0], cost, s, flags=re.S)
            s = re.sub(*(h["row"] if ext == "html" else h["rowmd"]), s, flags=re.S)
            s = s.replace(*h["kids"]).replace(h["mg"][1], h["mg"][0]).replace(*h["mg"])   # mg : idempotent
            if s != o: wr(p, s); n += 1
    print("hub : fichiers touchés", n)

def formulaire():
    n = 0
    for l, pre in LANGS:
        p = f"{pre}plan-your-trip/index.html"; s = o = rd(p)
        t = FORM_CHEF[l]
        s = re.sub(r'<small data-pf="chef" data-pf-tpl="[^"]*">.*?</small>', f'<small data-pf="chef" data-pf-tpl="{t}">{t}</small>', s, flags=re.S)
        if s != o: wr(p, s); n += 1
    print("formulaire : pages touchées", n)

def manifeste_partout():
    n = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_")) and d not in ("img", "catalogues", "js", "css", "fonts", "mendel", "apps-script")]
        for f in files:
            if f in ("index.html", "index.md"):
                p = os.path.join(root, f); s = o = rd(p)
                for a, b in MANIF: s = s.replace(a, b)
                if s != o: wr(p, s); n += 1
    print("manifeste : pages touchées", n)

def llms():
    """llms.txt : seules les lignes des 7 pages changent (titre et description de la page EN). Pas de _build_sitemap.py : il réécrit tout le sitemap."""
    import html as H
    raw = rd("llms.txt"); crlf = "\r\n" in raw; lines = raw.replace("\r\n", "\n").split("\n")
    for slug in SLUGS:
        h = rd(f"{slug}/index.html")
        t = H.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1)).replace(" | Mishpacha Tours", "")
        d = H.unescape(re.search(r'<meta name="description" content="([^"]*)">', h).group(1))
        key = f"(https://mishpachatours.com/{slug}/)"
        for i, l in enumerate(lines):
            if l.startswith("- [") and key in l: lines[i] = f"- [{t}]{key}: {d}"
    out = "\n".join(lines)
    wr("llms.txt", out.replace("\n", "\r\n") if crlf else out)

def sorties():
    subprocess.run([sys.executable, "_lot4_0611_services.py"], check=True)
    for slug in SLUGS:
        if slug.startswith("kosher-"): continue
        for l, pre in LANGS:
            p = f"{pre}{slug}/index.html"; s = rd(p)
            wr(p, s.replace('<body class="l3-luxe ', '<body class="', 1))
    manifeste_partout(); hub(); formulaire()
    llms()
    print("sorties régénérées")

if __name__ == "__main__":
    {"sources": sources, "sorties": sorties}[sys.argv[1] if len(sys.argv) > 1 else "sources"]()
