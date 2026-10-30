# -*- coding: utf-8 -*-
"""30/10 : traductions FR / ES / HE de la page « Ailleurs sur demande » (source : _pages/kosher-ski-anywhere.py), moteur _i18n_page.py.
Aucun montant, aucun seuil de budget (Moshé 30/10). py -3.14 _anywhere_i18n.py [--force] depuis site-v5."""
import sys
FORCE = "--force" in sys.argv; sys.argv = [sys.argv[0]]
from _i18n_page import traduire, FIXE
S = "kosher-ski-anywhere"

FR = dict(
  title="Ski casher ailleurs : chef et Shabbat",
  desc="Kitzbühel, St. Anton, Whistler, Aspen ou toute station hors de notre liste : dites-nous où, nous organisons chef casher, Shabbat, minyan et transferts.",
  h1="Ski casher, ailleurs", ital="dites-nous où, on organise",
  intro="L’Autriche, l’Amérique du Nord, ou une station que nous n’avons pas encore listée : la formule est la même. Un chef privé casher voyage avec vous et cuisine dans votre chalet, Shabbat et les fêtes sont dressés, et nous organisons le minyan et les transferts, avec le même interlocuteur WhatsApp que pour les Alpes.",
  chips=["Autriche, Amérique du Nord, et au-delà", "Un chef privé qui voyage avec vous", "Shabbat, fêtes, minyan sur demande", "Vérifié le 30 octobre 2026"],
  crumb="Les Alpes, strictement casher",
  sections=[
    ("Ce que nous organisons <i>ailleurs</i>", """<ul>
<li><b>Un chef privé casher qui voyage avec vous.</b> Notre équipe basée dans les Alpes envoie un chef dans votre chalet ou votre appartement, rend la cuisine casher et cuisine sur place tous les repas de la semaine. Les courses casher voyagent avec le chef ou viennent de la communauté juive la plus proche.</li>
<li><b>Shabbat et les fêtes.</b> Repas de Shabbat, ’hallot et vin dressés avant l’allumage des bougies ; Hanouka, Pourim, Pessah ou Souccot à la montagne. Rien n’est préparé pendant Shabbat ni un jour de fête.</li>
<li><b>Un minyan.</b> Là où une synagogue ou un Beth Habad existe dans la station, nous vous donnons les horaires. Là où il n’y en a pas, le minyan se forme avec les familles qui nous écrivent pour la même semaine, avec un Séfer Torah sur demande.</li>
<li><b>Les transferts.</b> De l’aéroport le plus proche à la porte du chalet, à des jours qui respectent Shabbat et les fêtes.</li>
<li><b>Le chalet ou l’appartement.</b> Nous le trouvons avec vous, ou nous travaillons avec celui que vous avez déjà réservé.</li>
<li><b>Un seul interlocuteur.</b> Le même numéro WhatsApp que pour les Alpes, du premier message au dernier transfert.</li>
</ul>
<p>Strictement casher. Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de chaque service : <a href="../kosher-services-french-alps/">services casher dans les Alpes</a>.</p>"""),
    ("Où nous <i>allons</i>", """<ul>
<li><b>L’Autriche.</b> Kitzbühel, St. Anton am Arlberg, Lech, Ischgl, Sölden, Saalbach : les commerces casher de Vienne et les Beth Habad d’Autriche aident pour les courses ; le chef fait le reste.</li>
<li><b>L’Amérique du Nord.</b> Whistler, Aspen, Vail, Park City, Mont-Tremblant : un chalet, un chef et Shabbat au même niveau que dans les Alpes, avec les courses casher trouvées sur place.</li>
<li><b>Le reste de la Suisse et de l’Italie.</b> Une station absente de notre liste, comme Andermatt, Engelberg, Laax ou Madonna di Campiglio : même formule, chef et Shabbat.</li>
<li><b>Partout ailleurs.</b> Dites-nous la station. Si nous ne pouvons pas bien faire, nous le disons.</li>
</ul>"""),
    ("Courchevel et les Alpes françaises, <i>où tout est déjà en place</i>", """<p>Avant de prendre l’avion plus loin, regardez ce qui existe déjà dans les Alpes françaises. À <a href="../kosher-courchevel/">Courchevel</a>, <a href="../kosher-megeve/">Megève</a>, <a href="../kosher-val-thorens/">Val Thorens</a> et aux <a href="../kosher-les-deux-alpes/">Deux Alpes</a>, nos <a href="../kosher-chalets/">chalets privés casher</a>, le chef, les repas livrés, le minyan avec le réseau ’Habad des Alpes et les transferts depuis Lyon et Genève sont déjà en place, saison après saison. Tout ce que nous organisons ailleurs part de là.</p>"""),
    ("Comment ça <i>se passe</i>", [
      ("Dites-nous où", "La station, vos dates, le nombre de personnes, l’endroit où vous dormez, et ce qu’il vous faut : un chef, Shabbat, une fête, un minyan, des transferts. Par WhatsApp ou avec le formulaire en bas de cette page."),
      ("Nous vérifions et nous montons le séjour", "Nous vérifions avec notre équipe dans les Alpes ce qui est possible pour vos dates et votre station : chef, cuisine, courses, minyan, voyage du chef. Un seul interlocuteur du début à la fin."),
      ("Vous recevez un devis", "Le prix dépend de la destination, des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager."),
    ]),
    ("Casher ailleurs : <i>vos questions</i>", [
      ("Quelles destinations couvrez-vous ?", "L’Autriche, l’Amérique du Nord et toute station de ski absente de notre liste, en plus des stations de France, de Suisse et d’Italie déjà présentes sur ce site. Dites-nous la station et nous vous disons ce qui est faisable."),
      ("Comment se passent les courses casher loin des Alpes ?", "Une partie voyage avec le chef, une partie s’achète dans le commerce casher ou la communauté juive la plus proche. Nous le préparons avant votre départ, et le détail de la surveillance accompagne votre devis."),
      ("Pouvez-vous organiser un minyan dans une station sans synagogue ?", "Un minyan dépend du nombre de familles présentes cette semaine-là. Donnez-nous vos dates tôt et nous regroupons les familles qui nous écrivent, avec un Séfer Torah sur demande."),
      ("Combien ça coûte ?", "Cela dépend de la destination, des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager. Nous ne publions aucun prix."),
      ("Travaillez-vous aussi l’été ?", "Oui. Randonnée, lacs, festivals : les services sont les mêmes l’été, chef, Shabbat, fêtes, minyan."),
      ("Qui surveille la cacherout des repas ?", "Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de la surveillance accompagne votre devis."),
    ]),
    ("Casher ailleurs cette saison ?", "Bonjour, nous allons à [station], [pays]. Dates : / Nombre de personnes : / Il nous faut (chef, Shabbat, fête, minyan, transferts) :"),
  ],
  related=["Les Alpes, strictement casher", "Services casher dans les Alpes, en détail", "Casher à Courchevel", "Nos chalets privés casher", "Vacances au ski casher dans les Alpes", "Casher à Verbier", "Lyon, la porte des Alpes"],
  source="Sources : notre équipe dans les Alpes pour les services. Les noms de stations sont des exemples, pas des partenariats.",
  fixe=FIXE["fr"],
)

ES = dict(
  title="Kosher en otro destino: chef y Shabat",
  desc="Kitzbühel, St. Anton, Whistler, Aspen o cualquier estación fuera de nuestra lista: díganos dónde y organizamos chef kosher, Shabat, minián y traslados.",
  h1="Kosher, otro destino", ital="díganos dónde, organizamos",
  intro="Austria, Norteamérica o una estación que aún no hemos publicado: la fórmula es la misma. Un chef privado kosher viaja con usted y cocina en su chalé, Shabat y las fiestas quedan servidos, y organizamos el minián y los traslados, con el mismo contacto de WhatsApp que para los Alpes.",
  chips=["Austria, Norteamérica y más allá", "Un chef privado que viaja con usted", "Shabat, fiestas, minián a petición", "Comprobado el 30 de octubre de 2026"],
  crumb="Los Alpes, estrictamente kosher",
  sections=[
    ("Lo que organizamos <i>en cualquier destino</i>", """<ul>
<li><b>Un chef privado kosher que viaja con usted.</b> Nuestro equipo con base en los Alpes envía un chef a su chalé o apartamento, kosheriza la cocina y cocina allí mismo todas las comidas de la semana. La compra kosher viaja con el chef o se consigue en la comunidad judía más cercana.</li>
<li><b>Shabat y las fiestas.</b> Comidas de Shabat, jalot y vino servidos antes del encendido de las velas; Janucá, Purim, Pésaj o Sucot en la montaña. No se prepara nada en Shabat ni en día de fiesta.</li>
<li><b>Un minián.</b> Donde hay sinagoga o casa Jabad en la estación, le damos los horarios. Donde no la hay, el minián se forma con las familias que nos escriben para la misma semana, con un Séfer Torá a petición.</li>
<li><b>Los traslados.</b> Del aeropuerto más cercano a la puerta del chalé, en días que respetan Shabat y las fiestas.</li>
<li><b>El chalé o el apartamento.</b> Lo buscamos con usted, o trabajamos con el que ya ha reservado.</li>
<li><b>Un único contacto.</b> El mismo número de WhatsApp que para los Alpes, del primer mensaje al último traslado.</li>
</ul>
<p>Estrictamente kosher. Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Detalle de cada servicio: <a href="../kosher-services-french-alps/">servicios kosher en los Alpes</a>.</p>"""),
    ("Adónde <i>vamos</i>", """<ul>
<li><b>Austria.</b> Kitzbühel, St. Anton am Arlberg, Lech, Ischgl, Sölden, Saalbach: las tiendas kosher de Viena y las casas Jabad de Austria ayudan con la compra; el chef hace el resto.</li>
<li><b>Norteamérica.</b> Whistler, Aspen, Vail, Park City, Mont-Tremblant: un chalé, un chef y Shabat con el mismo nivel que en los Alpes, con la compra kosher conseguida en el lugar.</li>
<li><b>El resto de Suiza e Italia.</b> Una estación que no está en nuestra lista, como Andermatt, Engelberg, Laax o Madonna di Campiglio: misma fórmula, chef y Shabat.</li>
<li><b>Cualquier otro lugar.</b> Díganos la estación. Si no podemos hacerlo bien, se lo decimos.</li>
</ul>"""),
    ("Courchevel y los Alpes franceses, <i>donde todo está ya listo</i>", """<p>Antes de volar más lejos, mire lo que ya existe en los Alpes franceses. En <a href="../kosher-courchevel/">Courchevel</a>, <a href="../kosher-megeve/">Megève</a>, <a href="../kosher-val-thorens/">Val Thorens</a> y <a href="../kosher-les-deux-alpes/">Les Deux Alpes</a>, nuestros <a href="../kosher-chalets/">chalés privados kosher</a>, el chef, las comidas entregadas, el minián con la red Jabad de los Alpes y los traslados desde Lyon y Ginebra están ya en marcha, temporada tras temporada. Todo lo que organizamos en otros destinos parte de ahí.</p>"""),
    ("Cómo <i>funciona</i>", [
      ("Díganos dónde", "La estación, sus fechas, el número de personas, dónde duerme y lo que necesita: un chef, Shabat, una fiesta, un minián, traslados. Por WhatsApp o con el formulario al pie de esta página."),
      ("Comprobamos y lo preparamos", "Comprobamos con nuestro equipo en los Alpes lo que es posible para sus fechas y su estación: chef, cocina, compra, minián, viaje del chef. Un único contacto de principio a fin."),
      ("Recibe un presupuesto", "El precio depende del destino, de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse."),
    ]),
    ("Kosher en otro destino: <i>preguntas</i>", [
      ("¿Qué destinos cubren?", "Austria, Norteamérica y cualquier estación de esquí que no esté en nuestra lista, además de las estaciones de Francia, Suiza e Italia ya presentes en este sitio. Díganos la estación y le decimos qué es posible."),
      ("¿Cómo funciona la compra kosher lejos de los Alpes?", "Una parte viaja con el chef, otra se compra en la tienda kosher o la comunidad judía más cercana. Lo planificamos antes de su salida, y los detalles de la supervisión acompañan su presupuesto."),
      ("¿Pueden organizar un minián en una estación sin sinagoga?", "Un minián depende de cuántas familias estén allí esa semana. Denos sus fechas pronto y agrupamos a las familias que nos escriben, con un Séfer Torá a petición."),
      ("¿Cuánto cuesta?", "Depende del destino, de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse. No publicamos precios."),
      ("¿Trabajan también en verano?", "Sí. Senderismo, lagos, festivales: los servicios son los mismos en verano, chef, Shabat, fiestas, minián."),
      ("¿Quién supervisa la comida?", "Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Los detalles de la supervisión acompañan su presupuesto."),
    ]),
    ("¿Kosher en otro destino esta temporada?", "Hola, vamos a [estación], [país]. Fechas: / Número de personas: / Necesitamos (chef, Shabat, fiesta, minián, traslados):"),
  ],
  related=["Los Alpes, estrictamente kosher", "Servicios kosher en los Alpes, en detalle", "Kosher en Courchevel", "Nuestros chalés privados kosher", "Vacaciones de esquí kosher en los Alpes", "Kosher en Verbier", "Lyon, puerta de los Alpes"],
  source="Fuentes: nuestro equipo en los Alpes para los servicios. Los nombres de estaciones son ejemplos, no colaboraciones.",
  fixe=FIXE["es"],
)

HE = dict(
  title="סקי כשר בכל יעד: שף, שבת ומניין",
  desc="קיצבוהל, סנט אנטון, ויסלר, אספן או כל אתר סקי שלא ברשימה שלנו: אמרו לנו לאן, ואנחנו מסדרים שף פרטי כשר, שבת, חגים, מניין והסעות.",
  h1="סקי כשר, בכל יעד", ital="אמרו לנו לאן, אנחנו מסדרים",
  intro="אוסטריה, צפון אמריקה, או אתר סקי שעוד לא פרסמנו: הנוסחה זהה. שף פרטי כשר נוסע איתכם ומבשל בצ'אלה שלכם, השבת והחגים ערוכים, ואנחנו מסדרים את המניין ואת ההסעות, עם אותו איש קשר בוואטסאפ כמו לאלפים.",
  chips=["אוסטריה, צפון אמריקה, ומעבר להן", "שף פרטי שנוסע איתכם", "שבת, חגים, מניין לפי בקשה", "נבדק ב-30 באוקטובר 2026"],
  crumb="האלפים, כשרים לחלוטין",
  sections=[
    ("מה אנחנו מארגנים <i>בכל יעד</i>", """<ul>
<li><b>שף פרטי כשר שנוסע איתכם.</b> הצוות שלנו, שבסיסו באלפים, שולח שף לצ'אלה או לדירה שלכם, מכשיר את המטבח ומבשל במקום כל ארוחה בשבוע. הקניות הכשרות נוסעות עם השף או מגיעות מהקהילה היהודית הקרובה.</li>
<li><b>שבת והחגים.</b> ארוחות שבת, חלות ויין ערוכים לפני הדלקת הנרות; חנוכה, פורים, פסח או סוכות בהרים. שום דבר לא מוכן בשבת או בחג.</li>
<li><b>מניין.</b> במקום שיש באתר בית כנסת או בית חב"ד, אנחנו נותנים לכם את הזמנים. במקום שאין, המניין נבנה מהמשפחות שכותבות לנו לאותו שבוע, עם ספר תורה לפי בקשה.</li>
<li><b>הסעות.</b> משדה התעופה הקרוב עד דלת הצ'אלה, בימים שמכבדים את השבת והחגים.</li>
<li><b>הצ'אלה או הדירה.</b> אנחנו מוצאים אותה איתכם, או עובדים עם זו שכבר הזמנתם.</li>
<li><b>איש קשר אחד.</b> אותו מספר וואטסאפ כמו לאלפים, מההודעה הראשונה ועד ההסעה האחרונה.</li>
</ul>
<p>שומר כשרות. הצוות הכשר שלנו באלפים מבשל תחת רשת חב"ד של האלפים. פירוט כל שירות: <a href="../kosher-services-french-alps/">שירותים כשרים באלפים</a>.</p>"""),
    ("לאן אנחנו <i>מגיעים</i>", """<ul>
<li><b>אוסטריה.</b> קיצבוהל, סנט אנטון אם ארלברג, לך, אישגל, זלדן, זאלבך: החנויות הכשרות של וינה ובתי חב"ד באוסטריה עוזרים בקניות; השף עושה את השאר.</li>
<li><b>צפון אמריקה.</b> ויסלר, אספן, וייל, פארק סיטי, מון טרמבלאן: צ'אלה, שף ושבת באותה רמה כמו באלפים, עם קניות כשרות מהמקום.</li>
<li><b>שאר שווייץ ואיטליה.</b> אתר שלא ברשימה שלנו, כמו אנדרמט, אנגלברג, לאקס או מדונה די קמפיליו: אותה נוסחה, שף ושבת.</li>
<li><b>כל מקום אחר.</b> אמרו לנו את שם האתר. אם אנחנו לא יכולים לעשות את זה טוב, נגיד.</li>
</ul>"""),
    ("קורשבל והאלפים הצרפתיים, <i>שם הכל כבר מוכן</i>", """<p>לפני שטסים רחוק יותר, הסתכלו על מה שכבר קיים באלפים הצרפתיים. ב<a href="../kosher-courchevel/">קורשבל</a>, ב<a href="../kosher-megeve/">מג'ב</a>, ב<a href="../kosher-val-thorens/">ואל טורנס</a> וב<a href="../kosher-les-deux-alpes/">לה דז אלפ</a>, <a href="../kosher-chalets/">הצ'אלות הפרטיות הכשרות</a> שלנו, השף, הארוחות במשלוח, המניין עם רשת חב"ד של האלפים וההסעות מליון ומז'נבה כבר עובדים, עונה אחרי עונה. כל מה שאנחנו מארגנים במקום אחר מתחיל משם.</p>"""),
    ("איך זה <i>עובד</i>", [
      ("אמרו לנו לאן", "האתר, התאריכים, מספר המשתתפים, איפה אתם ישנים ומה אתם צריכים: שף, שבת, חג, מניין, הסעות. בוואטסאפ או בטופס בתחתית העמוד."),
      ("אנחנו בודקים ומסדרים", "אנחנו בודקים עם הצוות שלנו באלפים מה אפשרי בתאריכים ובאתר שלכם: שף, מטבח, קניות, מניין, הנסיעה של השף. איש קשר אחד מההתחלה ועד הסוף."),
      ("מקבלים הצעת מחיר אחת", "המחיר תלוי ביעד, בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות."),
    ]),
    ("כשר בכל יעד: <i>שאלות</i>", [
      ("אילו יעדים אתם מכסים?", "אוסטריה, צפון אמריקה וכל אתר סקי שלא ברשימה שלנו, בנוסף לאתרים בצרפת, בשווייץ ובאיטליה שכבר נמצאים באתר הזה. אמרו לנו את שם האתר ונגיד לכם מה אפשרי."),
      ("איך עובדות הקניות הכשרות רחוק מהאלפים?", "חלק נוסע עם השף, חלק נקנה בחנות הכשרה או בקהילה היהודית הקרובה. אנחנו מתכננים את זה לפני היציאה, ופרטי ההשגחה מצורפים להצעת המחיר."),
      ("אפשר לארגן מניין באתר בלי בית כנסת?", "מניין תלוי במספר המשפחות שנמצאות שם באותו שבוע. שלחו לנו את התאריכים מוקדם ונחבר בין המשפחות שכותבות לנו, עם ספר תורה לפי בקשה."),
      ("כמה זה עולה?", "זה תלוי ביעד, בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות. אנחנו לא מפרסמים מחירים."),
      ("אתם עובדים גם בקיץ?", "כן. טיולים, אגמים, פסטיבלים: השירותים זהים בקיץ, שף, שבת, חגים, מניין."),
      ("מי משגיח על האוכל?", "הצוות הכשר שלנו באלפים מבשל תחת רשת חב\"ד של האלפים. פרטי ההשגחה מצורפים להצעת המחיר."),
    ]),
    ("כשר במקום אחר העונה?", "שלום, אנחנו נוסעים ל[אתר], [מדינה]. תאריכים: / מספר משתתפים: / אנחנו צריכים (שף, שבת, חג, מניין, הסעות):"),
  ],
  related=["האלפים, כשרים לחלוטין", "שירותים כשרים באלפים, בפירוט", "כשר בקורשבל", "הצ'אלות הפרטיות הכשרות שלנו", "חופשות סקי כשרות באלפים", "כשר בוורבייה", "ליון, שער האלפים"],
  source="מקורות: הצוות שלנו באלפים לגבי השירותים. שמות האתרים הם דוגמאות, לא שותפויות.",
  fixe=FIXE["he"],
)

traduire(S, FR, ES, HE, FORCE)
