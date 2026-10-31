# -*- coding: utf-8 -*-
"""30/10 : traductions FR / ES / HE de la page Gstaad (source : _pages/kosher-gstaad.py), moteur _i18n_page.py.
Formule chef privé seulement (Mendel, validé par Moshé). py -3.14 _gstaad_i18n.py [--force] depuis site-v5."""
import sys
FORCE = "--force" in sys.argv; sys.argv = [sys.argv[0]]
from _i18n_page import traduire, FIXE
S = "kosher-gstaad"

FR = dict(
  title="Casher à Gstaad : chef privé et Shabbat",
  desc="Casher à Gstaad, l’hiver comme l’été : un chef privé cuisine dans votre chalet, Shabbat, fêtes, minyan et Séfer Torah. Un seul devis écrit.",
  h1="Gstaad, casher", ital="un chef privé dans le chalet",
  intro="Gstaad se trouve à environ 1 050 m dans le Saanenland, canton de Berne, avec le Glacier 3000 au-dessus, à 3 000 m. Nous organisons votre séjour casher : un chef privé qui cuisine dans votre chalet, les courses casher apportées par notre équipe, Shabbat, minyan et Séfer Torah, en un seul devis écrit.",
  chips=["Environ 1 050 m, Glacier 3000 à 3 000 m", "Environ 2 h de l’aéroport de Genève, 3 h 45 de Lyon", "Hiver et été", "Vérifié le 30 octobre 2026"],
  crumb="Les Alpes, strictement casher",
  sections=[
    ("Ce que nous organisons <i>à Gstaad</i>", """<ul>
<li><b>Un chalet ou un appartement avec chef privé.</b> Notre équipe casher basée dans les Alpes rend la cuisine casher et le chef cuisine sur place, tous les repas de la semaine. L’hiver, vous rentrez de l’Eggli ou de la Wispile pour trouver la table dressée ; l’été, des sentiers ou d’un concert du festival Menuhin.</li>
<li><b>Les courses casher, apportées.</b> Viande, vin, ’hallot et épicerie voyagent avec le chef, déclarés à la douane suisse quand il le faut ; le reste s’achète dans les commerces casher de Genève, de Lausanne ou de Berne en route. Dites-nous où vous dormez : à Gstaad même, à Saanen, Schönried ou Saanenmöser, ou plus haut dans un hameau.</li>
<li><b>Shabbat.</b> Les repas de Shabbat, les ’hallot et le vin sont cuisinés et dressés avant l’allumage des bougies. Rien n’est préparé pendant Shabbat ni un jour de fête.</li>
<li><b>Les fêtes.</b> Hanouka, Pourim, Pessah ou Souccot dans l’Oberland bernois. Dites-nous quelle fête tombe pendant votre semaine.</li>
<li><b>Un minyan et un Séfer Torah.</b> Aucune synagogue n’est répertoriée à Gstaad ni dans le Saanenland : le minyan se forme avec les familles qui nous écrivent pour la même semaine. Donnez-nous vos dates tôt et nous les regroupons, avec un Séfer Torah.</li>
<li><b>Un séjour sur mesure, de A à Z.</b> Chalet, chef, transferts depuis Genève ou Zurich, Shabbat, les fêtes, un minyan : une demande, un devis. Les familles et les groupes venus de l’étranger sont notre cœur de cible, y compris les grands groupes et les hôtes hébréophones. Gstaad est à plus de trois heures de notre cuisine des Alpes françaises : nous n’y livrons pas de repas, le chef vient chez vous.</li>
</ul>
<p>Strictement casher. Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de chaque service : <a href="../kosher-services-french-alps/">services casher dans les Alpes</a>.</p>"""),
    ("Casher <i>à Gstaad</i>", """<p>La surveillance est rarement écrite noir sur blanc : renseignez-vous avant de réserver.</p>
<ul>
<li><b>Restaurant, commerce ou hôtel casher.</b> Aucun trouvé dans la station. Comptez sur votre chef, ou apportez votre nourriture.</li>
<li><b>Synagogue et Beth Habad.</b> Aucun n’est répertorié à Gstaad ni dans le Saanenland. Les synagogues les plus proches sont à Berne, à environ 1 h 30, et à Lausanne et Genève sur la route depuis l’aéroport.</li>
<li><b>Grandes communautés les plus proches.</b> Genève, Lausanne et Berne ont des synagogues, des commerces casher et des traiteurs. Faites vos courses là avant de monter.</li>
<li><b>Saison.</b> Les remontées de Gstaad tournent en général de début décembre à début avril ; le Glacier 3000 ouvre plus tôt à l’automne et ferme plus tard au printemps. Vérifiez les dates de votre semaine avant de réserver.</li>
</ul>"""),
    ("L’hiver et l’été <i>à Gstaad</i>", """<ul>
<li><b>L’hiver.</b> Le domaine de Gstaad relie le Saanenland et le Pays-d’Enhaut, environ 200 km de pistes entre les pentes des villages et le Glacier 3000. Les pistes restent douces et ensoleillées, faites pour les familles ; le glacier ajoute de la neige en altitude pour les meilleurs skieurs. Le soleil se couche tôt un vendredi de décembre : les repas de Shabbat sont dressés bien avant la fermeture des remontées.</li>
<li><b>L’été.</b> Des sentiers de randonnée depuis chaque village, les lacs de Lauenen et d’Arnensee, et le festival Menuhin avec des concerts de musique classique de juillet à septembre. Le chef prépare des paniers-repas pour la randonnée sur demande.</li>
<li><b>Minyan et Shabbat.</b> Sans synagogue dans la station, chaque minyan à Gstaad se forme avec les familles qui nous écrivent, avec un Séfer Torah. Les horaires de Shabbat s’affichent en direct sur cette page.</li>
</ul>"""),
    ("Comment ça <i>se passe</i>", [
      ("Dites-nous", "Gstaad, vos dates, le nombre de personnes, l’endroit où vous dormez, et ce qu’il vous faut : un chef, Shabbat, une fête, un minyan. Par WhatsApp ou avec le formulaire en bas de cette page."),
      ("Nous montons le séjour", "Le jour même, nous vérifions avec notre équipe dans les Alpes ce qui est possible pour vos dates à Gstaad : chef, cuisine, courses, minyan. Un seul interlocuteur du début à la fin."),
      ("Vous recevez un devis", "Le prix dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager."),
    ]),
    ("Se rendre <i>à Gstaad</i>", """<ul>
<li><b>Depuis l’aéroport de Genève :</b> environ 2 h par la route, le long du lac jusqu’à Aigle, puis la montée par Les Diablerets et le col du Pillon, ou par Bulle et Château-d’Œx.</li>
<li><b>En train :</b> environ 3 h depuis Genève, avec un changement à Montreux pour la ligne GoldenPass jusqu’à Gstaad.</li>
<li><b>Depuis l’aéroport de Zurich :</b> environ 2 h 45 par la route via Berne et Spiez ; en train environ 3 h avec des changements à Berne et à Zweisimmen.</li>
<li><b>Depuis Berne :</b> environ 1 h 30 en voiture.</li>
<li><b>Depuis Lyon-Saint-Exupéry :</b> environ 3 h 45 par la route via Genève. Lyon convient aux vols long-courriers et à de premières courses casher avant la montée : <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, la porte des Alpes</a>.</li>
<li><b>Passage depuis la France :</b> munissez-vous d’un passeport ou d’une carte d’identité pour chaque voyageur, enfants compris, et achetez en ligne la vignette autoroutière suisse avant la frontière. Les produits casher voyagent avec le chef et sont déclarés à la douane quand il le faut.</li>
<li><b>Vous atterrissez à Lyon avec quelques heures devant vous ?</b> <a href="../tours/stopover/">L’Escale</a> : une visite privée de 3 heures du patrimoine juif de Lyon, entre l’avion et la route.</li>
</ul>"""),
    ("Gstaad <i>sur la carte</i>", "Repère sur la Promenade, dans le village."),
    ("Casher à Gstaad : <i>vos questions</i>", [
      ("Combien ça coûte ?", "Cela dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager. Nous ne publions aucun prix."),
      ("Livrez-vous des repas casher à Gstaad ?", "Non. Gstaad est à plus de trois heures de notre cuisine des Alpes françaises : aucun repas n’y est livré. Un chef privé vient dans votre chalet avec les courses casher et cuisine sur place."),
      ("Y a-t-il un minyan à Gstaad ?", "Aucune synagogue n’est répertoriée dans la station. Un minyan dépend du nombre de familles présentes à Gstaad cette semaine-là. Donnez-nous vos dates tôt et nous les regroupons, avec un Séfer Torah."),
      ("Travaillez-vous l’été comme l’hiver ?", "Oui. Gstaad accueille randonneurs et festivaliers l’été et skieurs l’hiver, et les services sont les mêmes : chef privé, Shabbat, fêtes, minyan."),
      ("Pouvez-vous organiser un séjour pour un grand groupe ?", "Oui. Les groupes et les familles venus de l’étranger sont notre cœur de cible. Envoyez le nombre de personnes, les dates et ce qu’il vous faut, et vous recevez un seul devis écrit."),
      ("Qui surveille la cacherout des repas ?", "Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de la surveillance accompagne votre devis."),
    ]),
    ("Casher à Gstaad cette saison ?", "Bonjour, nous allons à Gstaad. Dates : / Nombre de personnes : / Il nous faut (chef, Shabbat, fête, minyan) :"),
  ],
  related=["Les Alpes, strictement casher", "Services casher dans les Alpes, en détail", "Vacances au ski casher dans les Alpes", "L’été dans les Alpes pour les familles juives", "Lyon, la porte des Alpes", "Casher à Verbier", "Casher à Crans-Montana"],
  source="Sources : Gstaad Saanenland Tourismus (gstaad.ch), Glacier 3000 (glacier3000.ch), CFF (sbb.ch), swissjews.ch, chabadswitzerland.com, hebcal.com ; notre équipe dans les Alpes pour les services. Vérifié le 30 octobre 2026.",
  fixe=FIXE["fr"],
)

ES = dict(
  title="Kosher en Gstaad: chef privado y Shabat",
  desc="Gstaad estrictamente kosher, en invierno y en verano: un chef privado cocina en su chalé, Shabat, fiestas, minián y Séfer Torá. Un único presupuesto.",
  h1="Gstaad, kosher", ital="chef privado en el chalé",
  intro="Gstaad está a unos 1.050 m en el Saanenland, cantón de Berna, con el Glacier 3000 por encima, a 3.000 m. Organizamos su estancia kosher: un chef privado que cocina en su chalé, con la compra kosher traída por nuestro equipo, Shabat, minián y Séfer Torá, en un único presupuesto por escrito.",
  chips=["Unos 1.050 m, Glacier 3000 a 3.000 m", "Unas 2 h del aeropuerto de Ginebra, 3 h 45 de Lyon", "Invierno y verano", "Comprobado el 30 de octubre de 2026"],
  crumb="Los Alpes, estrictamente kosher",
  sections=[
    ("Lo que organizamos <i>en Gstaad</i>", """<ul>
<li><b>Un chalé o un apartamento con chef privado.</b> Nuestro equipo kosher con base en los Alpes kosheriza la cocina y el chef cocina allí mismo, todas las comidas de la semana. En invierno vuelve del Eggli o de la Wispile a una mesa servida; en verano, de los senderos o de un concierto del festival Menuhin.</li>
<li><b>La compra kosher, traída.</b> Carne, vino, jalot y productos secos viajan con el chef, declarados en la aduana suiza cuando hace falta; el resto se compra en las tiendas kosher de Ginebra, Lausana o Berna de camino. Díganos dónde duerme: en el propio Gstaad, en Saanen, Schönried o Saanenmöser, o más arriba en una aldea.</li>
<li><b>Shabat.</b> Las comidas de Shabat, las jalot y el vino se cocinan y se sirven antes del encendido de las velas. No se prepara nada en Shabat ni en día de fiesta.</li>
<li><b>Las fiestas.</b> Janucá, Purim, Pésaj o Sucot en el Oberland bernés. Díganos qué fiesta cae en su semana.</li>
<li><b>Un minián y un Séfer Torá.</b> No hay ninguna sinagoga registrada en Gstaad ni en el Saanenland, así que el minián se forma con las familias que nos escriben para la misma semana. Denos sus fechas pronto y las agrupamos, con un Séfer Torá.</li>
<li><b>Una estancia a medida, de la A a la Z.</b> Chalé, chef, traslados desde Ginebra o Zúrich, Shabat, las fiestas, un minián: una solicitud, un presupuesto. Las familias y los grupos del extranjero son nuestro núcleo, incluidos los grupos grandes y los huéspedes de habla hebrea. Gstaad está a más de tres horas de nuestra cocina en los Alpes franceses: allí no entregamos comidas, el chef va a su casa.</li>
</ul>
<p>Estrictamente kosher. Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Detalle de cada servicio: <a href="../kosher-services-french-alps/">servicios kosher en los Alpes</a>.</p>"""),
    ("Kosher <i>en Gstaad</i>", """<p>La supervisión rara vez está por escrito, así que compruébelo antes de reservar.</p>
<ul>
<li><b>Restaurante, tienda u hotel kosher.</b> Ninguno en la estación. Cuente con su chef, o traiga su comida.</li>
<li><b>Sinagoga y casa Jabad.</b> Ninguna registrada en Gstaad ni en el Saanenland. Las sinagogas más cercanas están en Berna, a 1 h 30, y en Lausana y Ginebra en la ruta desde el aeropuerto.</li>
<li><b>Grandes comunidades más cercanas.</b> Ginebra, Lausana y Berna tienen sinagogas, tiendas kosher y servicios de catering. Haga allí sus compras antes de subir.</li>
<li><b>Temporada.</b> Los remontes de Gstaad suelen funcionar de principios de diciembre a principios de abril; el Glacier 3000 abre antes en otoño y cierra más tarde en primavera. Compruebe las fechas de su semana antes de reservar.</li>
</ul>"""),
    ("Invierno y verano <i>en Gstaad</i>", """<ul>
<li><b>Invierno.</b> El dominio de Gstaad une el Saanenland y el Pays-d'Enhaut, unos 200 km de pistas entre las laderas de los pueblos y el Glacier 3000. Las pistas son suaves y soleadas, pensadas para familias; el glaciar añade nieve en altura para los mejores esquiadores. El sol se pone pronto un viernes de diciembre, así que las comidas de Shabat se sirven mucho antes del cierre de los remontes.</li>
<li><b>Verano.</b> Senderos desde cada pueblo, los lagos de Lauenen y Arnensee, y el festival Menuhin con conciertos de música clásica de julio a septiembre. El chef prepara comidas para llevar a la ruta con antelación.</li>
<li><b>Minián y Shabat.</b> Sin sinagoga en la estación, cada minián en Gstaad se forma con las familias que nos escriben, con un Séfer Torá. Los horarios de Shabat aparecen en directo en esta página.</li>
</ul>"""),
    ("Cómo <i>funciona</i>", [
      ("Escríbanos", "Gstaad, sus fechas, el número de personas, dónde duerme y lo que necesita: un chef, Shabat, una fiesta, un minián. Por WhatsApp o con el formulario al pie de esta página."),
      ("Lo preparamos", "El mismo día comprobamos con nuestro equipo en los Alpes lo que es posible para sus fechas en Gstaad: chef, cocina, compra, minián. Un único contacto de principio a fin."),
      ("Recibe un presupuesto", "El precio depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse."),
    ]),
    ("Cómo llegar <i>a Gstaad</i>", """<ul>
<li><b>Desde el aeropuerto de Ginebra:</b> unas 2 h por carretera, a lo largo del lago hasta Aigle y luego la subida por Les Diablerets y el Col du Pillon, o por Bulle y Château-d'Œx.</li>
<li><b>En tren:</b> unas 3 h desde Ginebra, con cambio en Montreux para la línea GoldenPass hasta Gstaad.</li>
<li><b>Desde el aeropuerto de Zúrich:</b> unas 2 h 45 por carretera vía Berna y Spiez; en tren unas 3 h con cambios en Berna y Zweisimmen.</li>
<li><b>Desde Berna:</b> una hora y media en coche.</li>
<li><b>Desde Lyon-Saint-Exupéry:</b> unas 3 h 45 por carretera vía Ginebra. Lyon conviene a los vuelos de largo recorrido y a una primera compra kosher antes de subir: <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, puerta de los Alpes</a>.</li>
<li><b>Al cruzar desde Francia:</b> lleve pasaporte o documento de identidad para cada viajero, niños incluidos, y compre en línea la viñeta de las autopistas suizas antes de la frontera. Los productos kosher viajan con el chef y se declaran en la aduana cuando hace falta.</li>
<li><b>¿Aterriza en Lyon con unas horas libres?</b> <a href="../tours/stopover/">La Escala</a>: una visita privada de 3 horas del Lyon judío entre el avión y la carretera.</li>
</ul>"""),
    ("Gstaad <i>en el mapa</i>", "Marcador en la Promenade, en el pueblo."),
    ("Kosher en Gstaad: <i>preguntas</i>", [
      ("¿Cuánto cuesta?", "Depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse. No publicamos precios."),
      ("¿Entregan comidas kosher en Gstaad?", "No. Gstaad está a más de tres horas de nuestra cocina en los Alpes franceses, así que allí no se entregan comidas. Un chef privado va a su chalé con la compra kosher y cocina allí mismo."),
      ("¿Hay minián en Gstaad?", "No hay ninguna sinagoga registrada en la estación. Un minián depende de cuántas familias estén en Gstaad esa semana. Denos sus fechas pronto y las agrupamos, con un Séfer Torá."),
      ("¿Trabajan en verano además de en invierno?", "Sí. Gstaad recibe a senderistas y público del festival en verano y a esquiadores en invierno, y los servicios son los mismos: chef privado, Shabat, fiestas, minián."),
      ("¿Pueden organizar una estancia para un grupo grande?", "Sí. Los grupos y las familias del extranjero son nuestro núcleo. Envíe el número de personas, las fechas y lo que necesita, y recibe un único presupuesto por escrito."),
      ("¿Quién supervisa la comida?", "Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Los detalles de la supervisión acompañan su presupuesto."),
    ]),
    ("¿Kosher en Gstaad esta temporada?", "Hola, vamos a Gstaad. Fechas: / Número de personas: / Necesitamos (chef, Shabat, fiesta, minián):"),
  ],
  related=["Los Alpes, estrictamente kosher", "Servicios kosher en los Alpes, en detalle", "Vacaciones de esquí kosher en los Alpes", "Verano en los Alpes para familias judías", "Lyon, puerta de los Alpes", "Kosher en Verbier", "Kosher en Crans-Montana"],
  source="Fuentes: Gstaad Saanenland Tourismus (gstaad.ch), Glacier 3000 (glacier3000.ch), SBB (sbb.ch), swissjews.ch, chabadswitzerland.com, hebcal.com; nuestro equipo en los Alpes para los servicios. Comprobado el 30 de octubre de 2026.",
  fixe=FIXE["es"],
)

HE = dict(
  title="גשטאד כשר: שף פרטי ושבת",
  desc="גשטאד כשר לחלוטין, בחורף ובקיץ: שף פרטי מבשל בצ'אלה שלכם, הקניות הכשרות מגיעות איתו, שבת, חגים, מניין וספר תורה. הצעת מחיר אחת בכתב, הכל מאורגן מראש.",
  h1="גשטאד, כשר לחלוטין", ital="שף פרטי בצ'אלה שלכם",
  intro="גשטאד שוכן בגובה של כ-1,050 מטר באזור זאננלנד שבקנטון ברן, ומעליו גלסייה 3000 בגובה 3,000 מטר. אנחנו מארגנים את החופשה הכשרה שלכם: שף פרטי שמבשל בצ'אלה שלכם, קניות כשרות שהצוות שלנו מביא, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
  chips=["כ-1,050 מטר, גלסייה 3000 בגובה 3,000 מטר", "כשעתיים משדה התעופה של ז'נבה, 3 שעות ו-45 דקות מליון", "חורף וקיץ", "נבדק ב-30 באוקטובר 2026"],
  crumb="האלפים, כשרים לחלוטין",
  sections=[
    ("מה אנחנו מארגנים <i>בגשטאד</i>", """<ul>
<li><b>צ'אלה או דירה עם שף פרטי.</b> הצוות הכשר שלנו, שבסיסו באלפים, מכשיר את המטבח והשף מבשל במקום, כל ארוחה בשבוע. בחורף חוזרים מהאגלי או מהוויספילה לשולחן ערוך; בקיץ, מהשבילים או מקונצרט בפסטיבל מנוחין.</li>
<li><b>הקניות הכשרות מגיעות איתו.</b> בשר, יין, חלות ומצרכים יבשים נוסעים עם השף, ומוצהרים במכס השווייצרי כשצריך; את השאר קונים בחנויות הכשרות של ז'נבה, לוזאן או ברן בדרך. ספרו לנו איפה אתם ישנים: בגשטאד עצמה, בזאנן, בשנריד או בזאננמזר, או גבוה יותר בכפר קטן.</li>
<li><b>שבת.</b> ארוחות השבת, החלות והיין מבושלים וערוכים לפני הדלקת הנרות. שום דבר לא מוכן בשבת או בחג.</li>
<li><b>החגים.</b> חנוכה, פורים, פסח או סוכות באוברלנד הברני. ספרו לנו איזה חג חל בשבוע שלכם.</li>
<li><b>מניין וספר תורה.</b> אין בית כנסת רשום בגשטאד ולא בזאננלנד, ולכן המניין נבנה מהמשפחות שכותבות לנו לאותו שבוע. שלחו לנו את התאריכים מוקדם ונחבר ביניהן, עם ספר תורה.</li>
<li><b>חופשה בהתאמה אישית, מא' ועד ת'.</b> צ'אלה, שף, הסעות מז'נבה או מציריך, שבת, החגים, מניין: פנייה אחת, הצעת מחיר אחת. משפחות וקבוצות מחו״ל הן הלב של העבודה שלנו, כולל קבוצות גדולות ודוברי עברית. גשטאד נמצאת יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות: השף מגיע אליכם.</li>
</ul>
<p>שומר כשרות. הצוות הכשר שלנו באלפים מבשל תחת רשת חב"ד של האלפים. פירוט כל שירות: <a href="../kosher-services-french-alps/">שירותים כשרים באלפים</a>.</p>"""),
    ("כשר <i>בגשטאד</i>", """<p>ההשגחה כמעט אף פעם לא כתובה, אז כדאי לבדוק לפני שמזמינים.</p>
<ul>
<li><b>מסעדה, חנות או מלון כשרים.</b> לא נמצאו באתר. סמכו על השף שלכם, או הביאו את האוכל שלכם.</li>
<li><b>בית כנסת ובית חב"ד.</b> אינם רשומים בגשטאד ולא בזאננלנד. בתי הכנסת הקרובים נמצאים בברן, כשעה וחצי נסיעה, ובלוזאן ובז'נבה על הדרך משדה התעופה.</li>
<li><b>הקהילות הגדולות הקרובות.</b> בז'נבה, בלוזאן ובברן יש בתי כנסת, חנויות כשרות וקייטרינג. עשו שם קניות לפני העלייה.</li>
<li><b>עונה.</b> הרכבלים של גשטאד פועלים בדרך כלל מתחילת דצמבר עד תחילת אפריל; גלסייה 3000 נפתח מוקדם יותר בסתיו ונסגר מאוחר יותר באביב. בדקו את התאריכים של השבוע שלכם לפני שמזמינים.</li>
</ul>"""),
    ("חורף וקיץ <i>בגשטאד</i>", """<ul>
<li><b>חורף.</b> אזור הסקי של גשטאד מחבר את זאננלנד ואת פיי ד'אנו, כ-200 ק״מ של מסלולים בין מדרונות הכפרים לגלסייה 3000. המסלולים מתונים ושטופי שמש, מתאימים למשפחות; הקרחון מוסיף שלג בגובה לגולשים הטובים. השקיעה מוקדמת ביום שישי בדצמבר, ולכן ארוחות השבת ערוכות הרבה לפני סגירת הרכבלים.</li>
<li><b>קיץ.</b> שבילי הליכה מכל כפר, האגמים לאוונן וארננזה, ופסטיבל מנוחין עם קונצרטים של מוזיקה קלאסית מיולי עד ספטמבר. השף מכין ארוחות לדרך בתיאום מראש.</li>
<li><b>מניין ושבת.</b> אין בית כנסת באתר, ולכן כל מניין בגשטאד נבנה מהמשפחות שכותבות לנו, עם ספר תורה. זמני השבת מופיעים בזמן אמת בעמוד הזה.</li>
</ul>"""),
    ("איך זה <i>עובד</i>", [
      ("כתבו לנו", "גשטאד, התאריכים, מספר המשתתפים, איפה אתם ישנים ומה אתם צריכים: שף, שבת, חג, מניין. בוואטסאפ או בטופס בתחתית העמוד."),
      ("אנחנו מסדרים", "באותו יום אנחנו בודקים עם הצוות שלנו באלפים מה אפשרי בתאריכים שלכם בגשטאד: שף, מטבח, קניות, מניין. איש קשר אחד מההתחלה ועד הסוף."),
      ("מקבלים הצעת מחיר אחת", "המחיר תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות."),
    ]),
    ("איך מגיעים <i>לגשטאד</i>", """<ul>
<li><b>משדה התעופה של ז'נבה:</b> כשעתיים בכביש, לאורך האגם עד אגל, ואז עלייה דרך לה דיאבלרה ומעבר פיון, או דרך ביל ושאטו ד'ה.</li>
<li><b>ברכבת:</b> כ-3 שעות מז'נבה, עם החלפה במונטרה לקו גולדן פאס עד גשטאד.</li>
<li><b>משדה התעופה של ציריך:</b> כשעתיים ו-45 דקות בכביש דרך ברן ושפיץ; ברכבת כ-3 שעות עם החלפות בברן ובצווייזימן.</li>
<li><b>מברן:</b> כשעה וחצי ברכב.</li>
<li><b>מנמל התעופה ליון-סנט-אקזופרי:</b> כ-3 שעות ו-45 דקות בכביש דרך ז'נבה. ליון מתאימה לטיסות ארוכות ולקניות כשרות ראשונות לפני העלייה להרים: <a href="../lyon-gateway-to-the-alps-kosher/">ליון, שער האלפים</a>.</li>
<li><b>מעבר מצרפת:</b> קחו דרכון או תעודת זהות לכל נוסע, כולל ילדים, וקנו מראש ברשת את מדבקת הכבישים המהירים של שווייץ (ויניטה) לפני הגבול. המוצרים הכשרים נוסעים עם השף ומוצהרים במכס כשצריך.</li>
<li><b>נוחתים בליון עם כמה שעות פנויות?</b> <a href="../tours/stopover/">העצירה בליון</a>: סיור פרטי של 3 שעות בעקבות יהדות ליון, בין המטוס לדרך.</li>
</ul>"""),
    ("גשטאד <i>על המפה</i>", "הסימון על הפרומנדה, בכפר."),
    ("כשר בגשטאד: <i>שאלות</i>", [
      ("כמה זה עולה?", "זה תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות. אנחנו לא מפרסמים מחירים."),
      ("יש משלוח ארוחות כשרות לגשטאד?", "לא. גשטאד נמצאת יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות. שף פרטי מגיע לצ'אלה שלכם עם הקניות הכשרות ומבשל במקום."),
      ("יש מניין בגשטאד?", "אין בית כנסת רשום באתר. מניין תלוי במספר המשפחות שנמצאות בגשטאד באותו שבוע. שלחו לנו את התאריכים מוקדם ונחבר ביניהן, עם ספר תורה."),
      ("אתם עובדים גם בקיץ, לא רק בחורף?", "כן. בקיץ גשטאד פתוחה למטיילים ולבאי הפסטיבל, ובחורף לגולשים, והשירותים זהים: שף פרטי, שבת, חגים, מניין."),
      ("אפשר לארגן חופשה לקבוצה גדולה?", "כן. קבוצות ומשפחות מחו״ל הן הלב של העבודה שלנו. שלחו את מספר המשתתפים, התאריכים ומה אתם צריכים, ותקבלו הצעת מחיר אחת בכתב."),
      ("מי משגיח על האוכל?", "הצוות הכשר שלנו באלפים מבשל תחת רשת חב\"ד של האלפים. פרטי ההשגחה מצורפים להצעת המחיר."),
    ]),
    ("כשר בגשטאד העונה?", "שלום, אנחנו נוסעים לגשטאד. תאריכים: / מספר משתתפים: / אנחנו צריכים (שף, שבת, חג, מניין):"),
  ],
  related=["האלפים, כשרים לחלוטין", "שירותים כשרים באלפים, בפירוט", "חופשות סקי כשרות באלפים", "קיץ באלפים למשפחות יהודיות", "ליון, שער האלפים", "כשר בוורבייה", "כשר בקראן מונטנה"],
  source="מקורות: Gstaad Saanenland Tourismus (gstaad.ch), Glacier 3000 (glacier3000.ch), SBB (sbb.ch), swissjews.ch, chabadswitzerland.com, hebcal.com; הצוות שלנו באלפים לגבי השירותים. נבדק ב-30 באוקטובר 2026.",
  fixe=FIXE["he"],
)

traduire(S, FR, ES, HE, FORCE)
