# -*- coding: utf-8 -*-
"""Copies FR / ES / HE de la page /kosher-van-transfers/ (meme structure que _pages/kosher-van-transfers.py).
Lexique : « שומר כשרות », jamais « למהדרין » ; jamais le mot Israel ; pas de tiret cadratin."""

SVC = {"@context": "https://schema.org", "@type": "Service"}

FR = dict(
  title="Transferts en van privé en France et à l'étranger",
  desc="Un van privé depuis un aéroport, une gare, un hôtel ou une station, partout en France et à l'étranger. Chauffeur agréé, sur devis, jamais le Shabbat.",
  h1="Transferts en van privé", ital="jamais le Shabbat",
  intro="Un seul message, un seul chauffeur. Dites-nous d'où vous partez, où vous allez, la date, combien vous êtes et combien de bagages vous avez. Nous trouvons un chauffeur agréé dans notre réseau et organisons un van privé pour votre famille ou votre groupe, avec de la place pour les valises, les poussettes et les skis. Aéroport, gare, hôtel, station de ski ou ville : partout en France, et à l'étranger aussi.",
  chips=["D'un point A à un point B", "Vans pour familles et groupes", "Sur devis", "Jamais le Shabbat"],
  crumb=("../jewish-lyon-guide/", "Guide juif de Lyon"),
  sections=[
    dict(type="text", h2="Ce que <i>vous obtenez</i>",
      html="<ul><li><b>Un message sur WhatsApp.</b> Vous écrivez une fois, nous trouvons le chauffeur et le véhicule.</li><li><b>Un van pour une famille ou un groupe.</b> De la place pour tout le monde, avec valises, poussettes et skis.</li><li><b>Un chauffeur du réseau Habad.</b> Nous demandons à notre contact dans le réseau Habad local, là où vous atterrissez ou là où vous séjournez. Le chauffeur est discret et connaît les horaires de Shabbat.</li><li><b>Jamais pendant le Shabbat ni les fêtes.</b> Nous ne réservons aucune course qui roule pendant le Shabbat ou une fête juive. Chaque transfert se planifie autour de l'entrée et de la sortie du Shabbat.</li><li><b>Un devis, puis une course confirmée.</b> Il n'y a pas de grille de prix. Chaque transfert est chiffré sur demande, par écrit, avant que vous vous engagiez.</li></ul><p>La course est effectuée et facturée par un chauffeur agréé de notre réseau ; nous trouvons le chauffeur et nous organisons tout pour vous.</p>"),
    dict(type="steps", h2="Comment ça <i>marche</i>", items=[
      ("Envoyez un message", "Touchez le bouton : le message est prêt. Indiquez d'où vous partez, où vous allez, la date, combien vous êtes et combien de bagages. Ajoutez votre numéro de vol ou de train si vous l'avez."),
      ("Nous trouvons votre chauffeur", "Nous demandons à notre contact dans le réseau Habad local un chauffeur avec un van adapté à votre groupe."),
      ("Vous recevez un devis", "Vous recevez le prix par écrit avant que rien ne soit confirmé. La course est effectuée et facturée par un chauffeur agréé de notre réseau ; nous trouvons le chauffeur et nous organisons tout pour vous."),
      ("Votre chauffeur vous retrouve", "Votre chauffeur est au lieu convenu à l'heure convenue. Chaque course est planifiée autour du Shabbat et des fêtes."),
    ]),
    dict(type="beige", h2="De A <i>à B</i>",
      html="<ul><li><b>Aéroports et gares.</b> Prise en charge à votre atterrissage ou à votre arrivée, dépose pour votre départ.</li><li><b>Hôtels et chalets.</b> De votre porte à la suivante.</li><li><b>Stations de ski.</b> De l'aéroport ou de la gare directement à la station, avec les skis. Voir nos <a href='../kosher-ski-holidays-french-alps/'>vacances au ski casher</a>.</li><li><b>Villes et longues distances.</b> Lyon-Paris, d'une ville à une autre, ou ailleurs. Au-delà de la France, envoyez-nous le trajet et nous interrogeons nos contacts.</li></ul>"),
    dict(type="text", h2="Le Shabbat et <i>les fêtes</i>",
      html="<p>Nous ne faisons jamais de transfert pendant le Shabbat ni les fêtes juives. Si votre vol atterrit un vendredi après-midi ou juste après le Shabbat, dites-le-nous : nous planifions la prise en charge autour des horaires, et nous disons clairement quand une course n'est pas possible.</p>"),
    dict(type="faq", h2="Transferts en van : <i>questions</i>", items=[
      ("Où pouvez-vous nous emmener ?", "D'un point à un autre en France : aéroport, gare, hôtel, chalet, station de ski ou ville. Nous organisons aussi des courses à l'étranger. Envoyez-nous le trajet et nous interrogeons nos contacts."),
      ("Combien coûte un transfert en van ?", "Il n'y a pas de grille de prix. Le prix dépend de la distance, de la date, de la taille du groupe et des bagages. Vous recevez un devis écrit avant de confirmer."),
      ("Qui conduit, et qui facture ?", "Un chauffeur agréé de notre réseau conduit et facture la course. Mishpacha Tours ne vend pas le transport en son nom : nous trouvons le chauffeur et nous organisons tout pour vous."),
      ("Peut-on voyager le vendredi soir ou pendant le Shabbat ?", "Non. Nous ne faisons jamais de course pendant le Shabbat ni les fêtes juives. Pour une arrivée le vendredi, nous planifions la prise en charge autour de l'allumage des bougies."),
      ("Y a-t-il de la place pour nos valises, poussettes et skis ?", "Le van est choisi pour votre groupe. Donnez-nous le nombre de personnes et ce que vous transportez (valises, poussettes, skis) dans votre premier message, et nous trouvons un véhicule adapté."),
    ]),
    dict(type="cta", txt="Besoin d'un van de A à B ?", msg="Transfert en van : de … à …, date : …, nombre de personnes : …, bagages : …"),
  ],
  related=[("../kosher-services-french-alps/", "Services casher dans les Alpes"), ("../kosher-ski-holidays-french-alps/", "Vacances au ski casher dans les Alpes"), ("../lyon-gateway-to-the-alps-kosher/", "Lyon, porte des Alpes"), ("../flights-to-lyon/", "Vols vers Lyon"), ("../plan-your-trip/", "Préparer votre voyage")],
  alt="Un van de transport de passagers noir couvert de neige fraîche",
  tour="Transfert en van",
  svc=dict(name="Transferts en van privé en France et à l'étranger", serviceType="Transfert en van privé",
           description="Un van privé depuis un aéroport, une gare, un hôtel ou une station de ski, partout en France et à l'étranger, effectué et facturé par un chauffeur agréé du réseau Mishpacha Tours. Sur devis, jamais le Shabbat ni les fêtes juives."),
  note="Vous recevez un devis écrit avant de vous engager.",
  voyage="Transfert en van, d'un point A à un point B",
  carte=("Transferts en van privé", "Aéroport, gare, hôtel, station de ski, ville : un van et un chauffeur agréé, sur devis, jamais le Shabbat"),
  menu="Transferts en van",
  accueil=("Besoin seulement d'un transfert ?", "Un van privé d'un point A à un point B, partout en France et à l'étranger. Sur devis.", "Transferts en van"),
)

ES = dict(
  title="Traslados en van privado en Francia y el extranjero",
  desc="Un van privado desde un aeropuerto, una estación o un hotel, a toda Francia y al extranjero. Conductor autorizado de nuestra red, con presupuesto, nunca en Shabat.",
  h1="Traslados en van privado", ital="nunca en Shabat",
  intro="Un solo mensaje, un solo conductor. Díganos desde dónde sale, adónde va, la fecha, cuántos viajan y cuánto equipaje llevan. Encontramos un conductor autorizado en nuestra red y organizamos un van privado para su familia o su grupo, con espacio para maletas, cochecitos y esquís. Aeropuerto, estación, hotel, estación de esquí o ciudad: a cualquier punto de Francia, y también del extranjero.",
  chips=["De un punto A a un punto B", "Vans para familias y grupos", "Con presupuesto", "Nunca en Shabat"],
  crumb=("../jewish-lyon-guide/", "Guía del Lyon judío"),
  sections=[
    dict(type="text", h2="Lo que <i>obtiene</i>",
      html="<ul><li><b>Un mensaje por WhatsApp.</b> Usted escribe una vez y nosotros encontramos al conductor y el vehículo.</li><li><b>Un van para una familia o un grupo.</b> Espacio para todos, con maletas, cochecitos y esquís.</li><li><b>Un conductor de la red Habad.</b> Consultamos a nuestro contacto de la red Habad local, allí donde aterriza o donde se aloja. El conductor es discreto y conoce los horarios de Shabat.</li><li><b>Nunca durante Shabat ni en las fiestas.</b> No reservamos ningún trayecto que se haga en Shabat o en una fiesta judía. Cada traslado se planifica en torno a la entrada y la salida de Shabat.</li><li><b>Un presupuesto, y después un trayecto confirmado.</b> No hay tarifa publicada. Cada traslado se presupuesta a petición, por escrito, antes de que usted se comprometa.</li></ul><p>El trayecto lo realiza y lo factura un conductor autorizado de nuestra red; nosotros encontramos al conductor y lo organizamos todo por usted.</p>"),
    dict(type="steps", h2="Cómo <i>funciona</i>", items=[
      ("Envíe un mensaje", "Toque el botón: el mensaje ya está escrito. Indique desde dónde sale, adónde va, la fecha, cuántos son y cuánto equipaje llevan. Añada su número de vuelo o de tren si lo tiene."),
      ("Encontramos a su conductor", "Pedimos a nuestro contacto de la red Habad local un conductor con un van adecuado para su grupo."),
      ("Recibe un presupuesto", "Recibe el precio por escrito antes de que se confirme nada. El trayecto lo realiza y lo factura un conductor autorizado de nuestra red; nosotros encontramos al conductor y lo organizamos todo por usted."),
      ("Su conductor le recibe", "Su conductor está en el lugar acordado a la hora acordada. Cada trayecto se planifica en torno a Shabat y las fiestas."),
    ]),
    dict(type="beige", h2="De A <i>a B</i>",
      html="<ul><li><b>Aeropuertos y estaciones de tren.</b> Recogida cuando aterriza o llega, y traslado para su salida.</li><li><b>Hoteles y chalés.</b> De su puerta a la siguiente.</li><li><b>Estaciones de esquí.</b> Del aeropuerto o de la estación directamente a la estación de esquí, con los esquís. Vea nuestras <a href='../kosher-ski-holidays-french-alps/'>vacaciones de esquí kosher</a>.</li><li><b>Ciudades y largas distancias.</b> De Lyon a París, de una ciudad a otra, o a cualquier otro lugar. Fuera de Francia, envíenos el trayecto y consultamos a nuestros contactos.</li></ul>"),
    dict(type="text", h2="Shabat y <i>las fiestas</i>",
      html="<p>Nunca hacemos un traslado durante Shabat ni en las fiestas judías. Si su vuelo aterriza un viernes por la tarde o justo después de Shabat, díganoslo: planificamos la recogida en torno a los horarios y decimos con claridad cuándo un trayecto no es posible.</p>"),
    dict(type="faq", h2="Traslados en van: <i>preguntas</i>", items=[
      ("¿Adónde pueden llevarnos?", "De cualquier punto a cualquier otro de Francia: aeropuerto, estación de tren, hotel, chalé, estación de esquí o ciudad. También organizamos trayectos en el extranjero. Envíenos el trayecto y consultamos a nuestros contactos."),
      ("¿Cuánto cuesta un traslado en van?", "No hay tarifa publicada. El precio depende de la distancia, de la fecha, del tamaño del grupo y del equipaje. Recibe un presupuesto por escrito antes de confirmar."),
      ("¿Quién conduce y quién factura?", "Un conductor autorizado de nuestra red conduce y factura el trayecto. Mishpacha Tours no vende el transporte en su propio nombre: nosotros encontramos al conductor y lo organizamos todo por usted."),
      ("¿Podemos viajar el viernes por la noche o en Shabat?", "No. Nunca hacemos un trayecto durante Shabat ni en las fiestas judías. Para una llegada en viernes, planificamos la recogida en torno al encendido de las velas."),
      ("¿Hay espacio para nuestro equipaje, cochecitos y esquís?", "El van se elige para su grupo. Indíquenos en su primer mensaje el número de personas y lo que llevan (maletas, cochecitos, esquís), y encontramos un vehículo adecuado."),
    ]),
    dict(type="cta", txt="¿Necesita un van de A a B?", msg="Traslado en van: de … a …, fecha: …, número de personas: …, equipaje: …"),
  ],
  related=[("../kosher-services-french-alps/", "Servicios kosher en los Alpes"), ("../kosher-ski-holidays-french-alps/", "Vacaciones de esquí kosher en los Alpes"), ("../lyon-gateway-to-the-alps-kosher/", "Lyon, puerta de los Alpes"), ("../flights-to-lyon/", "Vuelos a Lyon"), ("../plan-your-trip/", "Planifique su viaje")],
  alt="Un van de pasajeros negro cubierto de nieve fresca",
  tour="Traslado en van",
  svc=dict(name="Traslados en van privado en Francia y el extranjero", serviceType="Traslado en van privado",
           description="Un van privado desde un aeropuerto, una estación, un hotel o una estación de esquí, a cualquier punto de Francia y del extranjero, realizado y facturado por un conductor autorizado de la red de Mishpacha Tours. Con presupuesto, nunca en Shabat ni en las fiestas judías."),
  note="Recibe un presupuesto por escrito antes de comprometerse.",
  voyage="Traslado en van, de un punto A a un punto B",
  carte=("Traslados en van privado", "Aeropuerto, estación, hotel, estación de esquí, ciudad: un van y un conductor autorizado, con presupuesto, nunca en Shabat"),
  menu="Traslados en van",
  accueil=("¿Solo necesita un traslado?", "Un van privado de un punto A a un punto B, a cualquier punto de Francia y del extranjero. Con presupuesto.", "Traslados en van"),
)

HE = dict(
  title="הסעות בוואן פרטי בצרפת ובחו״ל",
  desc="ואן פרטי משדה תעופה, מתחנת רכבת, ממלון או מאתר סקי לכל נקודה בצרפת ובחו״ל. נהג מורשה מרשת חב״ד שלנו, לפי הצעת מחיר, לעולם לא בשבת.",
  h1="הסעות בוואן פרטי", ital="מנקודה א׳ לנקודה ב׳, לעולם לא בשבת",
  intro="הודעה אחת, נהג אחד. כתבו לנו מאיפה אתם יוצאים, לאן אתם נוסעים, באיזה תאריך, כמה אתם ומה כמות המזוודות. אנחנו מאתרים נהג מורשה ברשת שלנו ומארגנים ואן פרטי למשפחה או לקבוצה שלכם, עם מקום למזוודות, לעגלות ולציוד סקי. שדה תעופה, תחנת רכבת, מלון, אתר סקי או עיר: בכל מקום בצרפת, וגם בחו״ל.",
  chips=["מנקודה א׳ לנקודה ב׳", "ואנים למשפחות ולקבוצות", "לפי הצעת מחיר", "לעולם לא בשבת"],
  crumb=("../jewish-lyon-guide/", "המדריך לליון היהודית"),
  sections=[
    dict(type="text", h2="מה <i>מקבלים</i>",
      html="<ul><li><b>הודעה אחת בוואטסאפ.</b> אתם כותבים פעם אחת ואנחנו מוצאים את הנהג והרכב.</li><li><b>ואן למשפחה או לקבוצה.</b> מקום לכל החבורה, עם מזוודות, עגלות וציוד סקי.</li><li><b>נהג מרשת חב״ד.</b> אנחנו פונים לאיש הקשר שלנו ברשת חב״ד המקומית, במקום שבו אתם נוחתים או שוהים. הנהג דיסקרטי ומכיר את זמני השבת.</li><li><b>לעולם לא בשבת ובחגים.</b> אנחנו לא מזמינים נסיעה שנעשית בשבת או בחג יהודי. כל הסעה מתוכננת סביב כניסת השבת ויציאתה.</li><li><b>הצעת מחיר, ואז נסיעה מאושרת.</b> אין מחירון. כל הסעה מתומחרת לפי בקשה, בכתב, לפני שאתם מתחייבים.</li></ul><p>הנסיעה מבוצעת ומחויבת על ידי נהג מורשה מהרשת שלנו; אנחנו מאתרים את הנהג ומסדרים לכם הכול.</p>"),
    dict(type="steps", h2="איך זה <i>עובד</i>", items=[
      ("שולחים הודעה אחת", "לוחצים על הכפתור וההודעה מוכנה. כתבו מאיפה אתם יוצאים, לאן, באיזה תאריך, כמה אתם וכמה מזוודות. הוסיפו מספר טיסה או רכבת אם יש לכם."),
      ("אנחנו מוצאים את הנהג", "אנחנו פונים לאיש הקשר שלנו ברשת חב״ד המקומית ומבקשים נהג עם ואן שמתאים לקבוצה שלכם."),
      ("מקבלים הצעת מחיר", "אתם מקבלים את המחיר בכתב לפני שמשהו מאושר. הנסיעה מבוצעת ומחויבת על ידי נהג מורשה מהרשת שלנו; אנחנו מאתרים את הנהג ומסדרים לכם הכול."),
      ("הנהג פוגש אתכם", "הנהג מחכה במקום שסוכם בשעה שסוכמה. כל נסיעה מתוכננת סביב השבת והחגים."),
    ]),
    dict(type="beige", h2="מנקודה א׳ <i>לנקודה ב׳</i>",
      html="<ul><li><b>שדות תעופה ותחנות רכבת.</b> איסוף בנחיתה או בהגעה, והסעה ליציאה שלכם.</li><li><b>מלונות וצ׳אלטים.</b> מהדלת שלכם עד הדלת הבאה.</li><li><b>אתרי סקי.</b> משדה התעופה או מהתחנה ישר לאתר, עם ציוד הסקי. ראו את <a href='../kosher-ski-holidays-french-alps/'>חופשות הסקי הכשרות</a> שלנו.</li><li><b>ערים ומרחקים ארוכים.</b> מליון לפריז, מעיר לעיר, או לכל מקום אחר. מחוץ לצרפת, שלחו לנו את המסלול ואנחנו פונים לאנשי הקשר שלנו.</li></ul>"),
    dict(type="text", h2="שבת <i>וחגים</i>",
      html="<p>אנחנו לא מבצעים הסעה בשבת או בחגים יהודיים. אם הטיסה שלכם נוחתת ביום שישי אחר הצהריים או מיד אחרי השבת, כתבו לנו: אנחנו מתכננים את האיסוף סביב הזמנים, ואומרים בבירור כשנסיעה לא אפשרית.</p>"),
    dict(type="faq", h2="הסעות בוואן: <i>שאלות</i>", items=[
      ("לאן אתם יכולים לקחת אותנו?", "מכל נקודה לכל נקודה בצרפת: שדה תעופה, תחנת רכבת, מלון, צ׳אלט, אתר סקי או עיר. אנחנו מארגנים גם נסיעות בחו״ל. שלחו לנו את המסלול ואנחנו פונים לאנשי הקשר שלנו."),
      ("כמה עולה הסעה בוואן?", "אין מחירון. המחיר תלוי במרחק, בתאריך, בגודל הקבוצה ובמזוודות. אתם מקבלים הצעת מחיר בכתב לפני שאתם מאשרים."),
      ("מי נוהג ומי מוציא חשבונית?", "נהג מורשה מהרשת שלנו נוהג ומחייב את הנסיעה. Mishpacha Tours לא מוכרת את ההסעה בשמה: אנחנו מאתרים את הנהג ומסדרים לכם הכול."),
      ("אפשר לנסוע במוצאי שבת או בשבת?", "בשבת לא. אנחנו לא מבצעים נסיעה בשבת או בחגים יהודיים. להגעה ביום שישי אנחנו מתכננים את האיסוף סביב הדלקת הנרות."),
      ("יש מקום למזוודות, לעגלות ולציוד הסקי?", "הוואן נבחר לפי הקבוצה שלכם. כתבו לנו בהודעה הראשונה כמה אתם ומה אתם מביאים (מזוודות, עגלות, ציוד סקי), ואנחנו מוצאים רכב שמתאים."),
    ]),
    dict(type="cta", txt="צריכים ואן מנקודה א׳ לנקודה ב׳?", msg="הסעה בוואן: מ… ל…, תאריך: …, מספר אנשים: …, מזוודות: …"),
  ],
  related=[("../kosher-services-french-alps/", "שירותים כשרים באלפים"), ("../kosher-ski-holidays-french-alps/", "חופשות סקי כשרות באלפים"), ("../lyon-gateway-to-the-alps-kosher/", "ליון, שער האלפים"), ("../flights-to-lyon/", "טיסות לליון"), ("../plan-your-trip/", "תכננו את הטיול")],
  alt="ואן נוסעים שחור מכוסה בשלג טרי",
  tour="הסעה בוואן",
  svc=dict(name="הסעות בוואן פרטי בצרפת ובחו״ל", serviceType="הסעה בוואן פרטי",
           description="ואן פרטי משדה תעופה, מתחנת רכבת, ממלון או מאתר סקי לכל נקודה בצרפת ובחו״ל, בביצוע ובחיוב של נהג מורשה מהרשת של Mishpacha Tours. לפי הצעת מחיר, לעולם לא בשבת ובחגים יהודיים."),
  note="תקבלו הצעת מחיר בכתב לפני שתתחייבו.",
  voyage="הסעה בוואן, מנקודה א׳ לנקודה ב׳",
  carte=("הסעות בוואן פרטי", "שדה תעופה, תחנת רכבת, מלון, אתר סקי, עיר: ואן ונהג מורשה, לפי הצעת מחיר, לעולם לא בשבת"),
  menu="הסעות בוואן",
  accueil=("צריכים רק הסעה?", "ואן פרטי מנקודה א׳ לנקודה ב׳, בכל מקום בצרפת ובחו״ל. לפי הצעת מחיר.", "הסעות בוואן"),
)

EN_EXTRA = dict(
  alt="A traveller with his suitcase next to a green passenger van, a mountain behind",
  tour="Van transfer",
  note="You receive a written quote before you commit.",
  voyage="Van transfer, point A to point B",
  carte=("Private van transfers", "Airport, station, hotel, ski resort, city: a van and a licensed driver, quote on request, never on Shabbat"),
  menu="Van transfers",
  accueil=("Only need a ride?", "A private van from point A to point B, anywhere in France and abroad. Quote on request.", "Van transfers"),
)

TR = {"fr": FR, "es": ES, "he": HE}
