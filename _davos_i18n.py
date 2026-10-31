# -*- coding: utf-8 -*-
"""30/10 : traductions FR / ES / HE de la page Davos (source : _pages/kosher-davos.py), moteur _i18n_page.py.
Formule chef privé seulement ; jamais de nom d'hôtel concurrent. py -3.14 _davos_i18n.py [--force] depuis site-v5."""
import sys
FORCE = "--force" in sys.argv; sys.argv = [sys.argv[0]]
from _i18n_page import traduire, FIXE
S = "kosher-davos"

FR = dict(
  title="Casher à Davos : chef privé et Shabbat",
  desc="Casher à Davos, dans les Grisons, à 1 560 m : un chef privé cuisine dans votre chalet, Shabbat, fêtes, minyan et Séfer Torah. Un seul devis écrit.",
  h1="Davos, casher", ital="chef et Shabbat à 1 560 m",
  intro="Davos se trouve à 1 560 m dans les Grisons, la ville la plus haute des Alpes, sous le Parsenn et le Jakobshorn. Nous organisons votre séjour casher : un chef privé qui cuisine dans votre chalet ou votre appartement, les courses casher apportées par notre équipe, Shabbat, minyan et Séfer Torah, en un seul devis écrit.",
  chips=["1 560 m, Weissfluhgipfel 2 844 m", "Environ 2 h de l’aéroport de Zurich", "Hiver et été", "Vérifié le 30 octobre 2026"],
  crumb="Les Alpes, strictement casher",
  sections=[
    ("Ce que nous organisons <i>à Davos</i>", """<ul>
<li><b>Un chalet ou un appartement avec chef privé.</b> Notre équipe casher basée dans les Alpes rend la cuisine casher et le chef cuisine sur place, tous les repas de la semaine. L’hiver, vous rentrez du Parsenn ou du Jakobshorn pour trouver la table dressée ; l’été, du lac ou des sentiers.</li>
<li><b>Les courses casher, apportées.</b> Viande, vin, ’hallot et épicerie voyagent avec le chef, déclarés à la douane suisse quand il le faut ; le reste s’achète dans les commerces casher de Zurich, à environ deux heures. Dites-nous où vous dormez : Davos Platz, Davos Dorf, ou l’une des vallées latérales.</li>
<li><b>Shabbat.</b> Les repas de Shabbat, les ’hallot et le vin sont cuisinés et dressés avant l’allumage des bougies. Rien n’est préparé pendant Shabbat ni un jour de fête.</li>
<li><b>Les fêtes.</b> Hanouka, Pourim, Pessah ou Souccot dans les Grisons. Dites-nous quelle fête tombe pendant votre semaine.</li>
<li><b>Un minyan et un Séfer Torah.</b> Des familles juives viennent à Davos depuis plus d’un siècle, et en haute saison vous êtes rarement la seule famille pratiquante en ville. Nous formons le minyan avec les familles qui nous écrivent pour la même semaine : donnez-nous vos dates tôt, avec un Séfer Torah sur demande.</li>
<li><b>Un séjour sur mesure, de A à Z.</b> Chalet, chef, transferts depuis Zurich, Shabbat, les fêtes, un minyan : une demande, un devis. Les familles et les groupes venus de l’étranger sont notre cœur de cible, y compris les grands groupes et les hôtes hébréophones. Davos est à bien plus de trois heures de notre cuisine des Alpes françaises : nous n’y livrons pas de repas, le chef vient chez vous.</li>
</ul>
<p>Strictement casher. Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de chaque service : <a href="../kosher-services-french-alps/">services casher dans les Alpes</a>.</p>"""),
    ("Casher <i>à Davos</i>", """<p>La surveillance est rarement écrite noir sur blanc : renseignez-vous avant de réserver.</p>
<ul>
<li><b>Restaurant, commerce ou hôtel casher.</b> Saisonnier au mieux, et pas chaque année. Nous n’en dépendons pas : comptez sur votre chef, ou apportez votre nourriture.</li>
<li><b>Synagogue et Beth Habad.</b> Aucune synagogue permanente n’est répertoriée à Davos. La communauté la plus proche est Zurich, à environ deux heures, avec synagogues, commerces casher et traiteurs.</li>
<li><b>Hôtes juifs.</b> Davos accueille des visiteurs juifs depuis son époque de station de cure ; l’hiver, les familles pratiquantes font partie du paysage de la Promenade.</li>
<li><b>Janvier.</b> Le Forum économique mondial remplit la ville une semaine en janvier : réservez très tôt pour cette semaine-là, ou choisissez-en une autre.</li>
<li><b>Saison.</b> Les remontées de Davos Klosters tournent en général de fin novembre à mi-avril, le Jakobshorn un peu plus tard. Vérifiez les dates de votre semaine avant de réserver.</li>
</ul>"""),
    ("L’hiver et l’été <i>à Davos</i>", """<ul>
<li><b>L’hiver.</b> Six domaines autour de Davos et Klosters, environ 300 km de pistes : le Parsenn avec le Weissfluhgipfel à 2 844 m, le Jakobshorn, Pischa, Rinerhorn, Madrisa et la Schatzalp. Le soleil se couche tôt un vendredi de décembre : les repas de Shabbat sont dressés bien avant la fermeture des remontées.</li>
<li><b>L’été.</b> Quelque 700 km de sentiers de randonnée, le lac de Davos, le VTT, et le Davos Festival des jeunes musiciens en août. Le chef prépare des paniers-repas pour la randonnée sur demande.</li>
<li><b>Minyan et Shabbat.</b> Chaque minyan à Davos se forme avec les familles qui nous écrivent, avec un Séfer Torah. Les horaires de Shabbat s’affichent en direct sur cette page.</li>
</ul>"""),
    ("Comment ça <i>se passe</i>", [
      ("Dites-nous", "Davos, vos dates, le nombre de personnes, l’endroit où vous dormez, et ce qu’il vous faut : un chef, Shabbat, une fête, un minyan. Par WhatsApp ou avec le formulaire en bas de cette page."),
      ("Nous montons le séjour", "Le jour même, nous vérifions avec notre équipe dans les Alpes ce qui est possible pour vos dates à Davos : chef, cuisine, courses, minyan. Un seul interlocuteur du début à la fin."),
      ("Vous recevez un devis", "Le prix dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager."),
    ]),
    ("Se rendre <i>à Davos</i>", """<ul>
<li><b>Depuis l’aéroport de Zurich :</b> environ 2 h par la route via Landquart et le Prättigau.</li>
<li><b>En train :</b> environ 2 h 15 depuis l’aéroport de Zurich, avec un changement à Landquart pour le Chemin de fer rhétique jusqu’à Davos Dorf et Davos Platz.</li>
<li><b>Depuis l’aéroport de Genève :</b> environ 4 h 30 par la route ; une longue journée, mieux avec un arrêt à Zurich pour les courses casher.</li>
<li><b>Depuis Milan :</b> environ 3 h 30 par la route.</li>
<li><b>Depuis Lyon-Saint-Exupéry :</b> environ 5 h 30 par la route. Pour Davos, Zurich est l’aéroport naturel ; Lyon convient à un séjour qui commence dans les Alpes françaises : <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, la porte des Alpes</a>.</li>
<li><b>Entrée en Suisse :</b> munissez-vous d’un passeport ou d’une carte d’identité pour chaque voyageur, enfants compris, et achetez en ligne la vignette autoroutière suisse avant la frontière. Les produits casher voyagent avec le chef et sont déclarés à la douane quand il le faut.</li>
</ul>"""),
    ("Davos <i>sur la carte</i>", "Repère sur la Promenade, à Davos Platz."),
    ("Casher à Davos : <i>vos questions</i>", [
      ("Combien ça coûte ?", "Cela dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager. Nous ne publions aucun prix."),
      ("Livrez-vous des repas casher à Davos ?", "Non. Davos est à bien plus de trois heures de notre cuisine des Alpes françaises : aucun repas n’y est livré. Un chef privé vient dans votre chalet avec les courses casher et cuisine sur place."),
      ("Y a-t-il un minyan à Davos ?", "Aucune synagogue permanente n’est répertoriée. En haute saison, un minyan se forme plus facilement à Davos que dans la plupart des stations, car des familles pratiquantes viennent chaque hiver. Donnez-nous vos dates tôt et nous regroupons les familles qui nous écrivent, avec un Séfer Torah sur demande."),
      ("Travaillez-vous l’été comme l’hiver ?", "Oui. Davos accueille randonneurs, vététistes et festivaliers l’été et skieurs l’hiver, et les services sont les mêmes : chef privé, Shabbat, fêtes, minyan."),
      ("Pouvez-vous organiser un séjour pour un grand groupe ?", "Oui. Les groupes et les familles venus de l’étranger sont notre cœur de cible. Envoyez le nombre de personnes, les dates et ce qu’il vous faut, et vous recevez un seul devis écrit."),
      ("Qui surveille la cacherout des repas ?", "Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de la surveillance accompagne votre devis."),
    ]),
    ("Casher à Davos cette saison ?", "Bonjour, nous allons à Davos. Dates : / Nombre de personnes : / Il nous faut (chef, Shabbat, fête, minyan) :"),
  ],
  related=["Les Alpes, strictement casher", "Services casher dans les Alpes, en détail", "Vacances au ski casher dans les Alpes", "L’été dans les Alpes pour les familles juives", "Casher à Saint-Moritz", "Casher à Verbier", "Casher à Gstaad"],
  source="Sources : Davos Klosters (davos.ch), Chemin de fer rhétique et CFF (sbb.ch), myswitzerland.com, swissjews.ch, chabadswitzerland.com, hebcal.com ; notre équipe dans les Alpes pour les services. Vérifié le 30 octobre 2026.",
  fixe=FIXE["fr"],
)

ES = dict(
  title="Kosher en Davos: chef privado y Shabat",
  desc="Davos, en los Grisones, a 1.560 m, estrictamente kosher: un chef privado cocina en su chalé, Shabat, fiestas, minián y Séfer Torá. Un único presupuesto.",
  h1="Davos, kosher", ital="chef y Shabat a 1.560 m",
  intro="Davos está a 1.560 m en los Grisones, la ciudad más alta de los Alpes, bajo el Parsenn y el Jakobshorn. Organizamos su estancia kosher: un chef privado que cocina en su chalé o apartamento, con la compra kosher traída por nuestro equipo, Shabat, minián y Séfer Torá, en un único presupuesto por escrito.",
  chips=["1.560 m, Weissfluhgipfel 2.844 m", "Unas 2 h del aeropuerto de Zúrich", "Invierno y verano", "Comprobado el 30 de octubre de 2026"],
  crumb="Los Alpes, estrictamente kosher",
  sections=[
    ("Lo que organizamos <i>en Davos</i>", """<ul>
<li><b>Un chalé o un apartamento con chef privado.</b> Nuestro equipo kosher con base en los Alpes kosheriza la cocina y el chef cocina allí mismo, todas las comidas de la semana. En invierno vuelve del Parsenn o del Jakobshorn a una mesa servida; en verano, del lago o de los senderos.</li>
<li><b>La compra kosher, traída.</b> Carne, vino, jalot y productos secos viajan con el chef, declarados en la aduana suiza cuando hace falta; el resto se compra en las tiendas kosher de Zúrich, a unas dos horas. Díganos dónde duerme: Davos Platz, Davos Dorf o uno de los valles laterales.</li>
<li><b>Shabat.</b> Las comidas de Shabat, las jalot y el vino se cocinan y se sirven antes del encendido de las velas. No se prepara nada en Shabat ni en día de fiesta.</li>
<li><b>Las fiestas.</b> Janucá, Purim, Pésaj o Sucot en los Grisones. Díganos qué fiesta cae en su semana.</li>
<li><b>Un minián y un Séfer Torá.</b> Las familias judías vienen a Davos desde hace más de un siglo, y en temporada alta rara vez es usted la única familia observante en la ciudad. Formamos el minián con las familias que nos escriben para la misma semana: denos sus fechas pronto, con un Séfer Torá a petición.</li>
<li><b>Una estancia a medida, de la A a la Z.</b> Chalé, chef, traslados desde Zúrich, Shabat, las fiestas, un minián: una solicitud, un presupuesto. Las familias y los grupos del extranjero son nuestro núcleo, incluidos los grupos grandes y los huéspedes de habla hebrea. Davos está a mucho más de tres horas de nuestra cocina en los Alpes franceses: allí no entregamos comidas, el chef va a su casa.</li>
</ul>
<p>Estrictamente kosher. Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Detalle de cada servicio: <a href="../kosher-services-french-alps/">servicios kosher en los Alpes</a>.</p>"""),
    ("Kosher <i>en Davos</i>", """<p>La supervisión rara vez está por escrito, así que compruébelo antes de reservar.</p>
<ul>
<li><b>Restaurante, tienda u hotel kosher.</b> Estacional como mucho, y no todos los años. No dependemos de ello: cuente con su chef, o traiga su comida.</li>
<li><b>Sinagoga y casa Jabad.</b> No hay ninguna sinagoga permanente registrada en Davos. La comunidad más cercana es Zúrich, a unas dos horas, con sinagogas, tiendas kosher y servicios de catering.</li>
<li><b>Huéspedes judíos.</b> Davos recibe visitantes judíos desde su época de estación de cura; en invierno, las familias observantes forman parte del paisaje de la Promenade.</li>
<li><b>Enero.</b> El Foro Económico Mundial llena la ciudad una semana de enero: reserve muy pronto para esa semana, o elija otra.</li>
<li><b>Temporada.</b> Los remontes de Davos Klosters suelen funcionar de finales de noviembre a mediados de abril, el Jakobshorn algo más tarde. Compruebe las fechas de su semana antes de reservar.</li>
</ul>"""),
    ("Invierno y verano <i>en Davos</i>", """<ul>
<li><b>Invierno.</b> Seis dominios alrededor de Davos y Klosters, unos 300 km de pistas: el Parsenn con el Weissfluhgipfel a 2.844 m, el Jakobshorn, Pischa, Rinerhorn, Madrisa y la Schatzalp. El sol se pone pronto un viernes de diciembre, así que las comidas de Shabat se sirven mucho antes del cierre de los remontes.</li>
<li><b>Verano.</b> Unos 700 km de senderos, el lago de Davos, bicicleta de montaña y el Davos Festival de jóvenes músicos en agosto. El chef prepara comidas para llevar a la ruta con antelación.</li>
<li><b>Minián y Shabat.</b> Cada minián en Davos se forma con las familias que nos escriben, con un Séfer Torá. Los horarios de Shabat aparecen en directo en esta página.</li>
</ul>"""),
    ("Cómo <i>funciona</i>", [
      ("Escríbanos", "Davos, sus fechas, el número de personas, dónde duerme y lo que necesita: un chef, Shabat, una fiesta, un minián. Por WhatsApp o con el formulario al pie de esta página."),
      ("Lo preparamos", "El mismo día comprobamos con nuestro equipo en los Alpes lo que es posible para sus fechas en Davos: chef, cocina, compra, minián. Un único contacto de principio a fin."),
      ("Recibe un presupuesto", "El precio depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse."),
    ]),
    ("Cómo llegar <i>a Davos</i>", """<ul>
<li><b>Desde el aeropuerto de Zúrich:</b> unas 2 h por carretera vía Landquart y el Prättigau.</li>
<li><b>En tren:</b> unas 2 h 15 desde el aeropuerto de Zúrich, con cambio en Landquart para el Ferrocarril Rético hasta Davos Dorf y Davos Platz.</li>
<li><b>Desde el aeropuerto de Ginebra:</b> unas 4 h 30 por carretera; un día largo, mejor con parada en Zúrich para la compra kosher.</li>
<li><b>Desde Milán:</b> unas 3 h 30 por carretera.</li>
<li><b>Desde Lyon-Saint-Exupéry:</b> unas 5 h 30 por carretera. Para Davos, Zúrich es el aeropuerto natural; Lyon conviene a una estancia que empieza en los Alpes franceses: <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, puerta de los Alpes</a>.</li>
<li><b>Al entrar en Suiza:</b> lleve pasaporte o documento de identidad para cada viajero, niños incluidos, y compre en línea la viñeta de las autopistas suizas antes de la frontera. Los productos kosher viajan con el chef y se declaran en la aduana cuando hace falta.</li>
</ul>"""),
    ("Davos <i>en el mapa</i>", "Marcador en la Promenade, en Davos Platz."),
    ("Kosher en Davos: <i>preguntas</i>", [
      ("¿Cuánto cuesta?", "Depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse. No publicamos precios."),
      ("¿Entregan comidas kosher en Davos?", "No. Davos está a mucho más de tres horas de nuestra cocina en los Alpes franceses, así que allí no se entregan comidas. Un chef privado va a su chalé con la compra kosher y cocina allí mismo."),
      ("¿Hay minián en Davos?", "No hay ninguna sinagoga permanente registrada. En temporada alta, un minián se forma más fácilmente en Davos que en la mayoría de las estaciones, porque cada invierno vienen familias observantes. Denos sus fechas pronto y agrupamos a las familias que nos escriben, con un Séfer Torá a petición."),
      ("¿Trabajan en verano además de en invierno?", "Sí. Davos recibe a senderistas, ciclistas y público del festival en verano y a esquiadores en invierno, y los servicios son los mismos: chef privado, Shabat, fiestas, minián."),
      ("¿Pueden organizar una estancia para un grupo grande?", "Sí. Los grupos y las familias del extranjero son nuestro núcleo. Envíe el número de personas, las fechas y lo que necesita, y recibe un único presupuesto por escrito."),
      ("¿Quién supervisa la comida?", "Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Los detalles de la supervisión acompañan su presupuesto."),
    ]),
    ("¿Kosher en Davos esta temporada?", "Hola, vamos a Davos. Fechas: / Número de personas: / Necesitamos (chef, Shabat, fiesta, minián):"),
  ],
  related=["Los Alpes, estrictamente kosher", "Servicios kosher en los Alpes, en detalle", "Vacaciones de esquí kosher en los Alpes", "Verano en los Alpes para familias judías", "Kosher en St. Moritz", "Kosher en Verbier", "Kosher en Gstaad"],
  source="Fuentes: Davos Klosters (davos.ch), Ferrocarril Rético y SBB (sbb.ch), myswitzerland.com, swissjews.ch, chabadswitzerland.com, hebcal.com; nuestro equipo en los Alpes para los servicios. Comprobado el 30 de octubre de 2026.",
  fixe=FIXE["es"],
)

HE = dict(
  title="דאבוס כשר: שף פרטי ושבת",
  desc="דאבוס כשר לחלוטין, בגובה 1,560 מטר, בחורף ובקיץ: שף פרטי מבשל בצ'אלה שלכם, הקניות הכשרות מגיעות איתו, שבת, חגים, מניין וספר תורה. הצעת מחיר אחת בכתב.",
  h1="דאבוס, כשר לחלוטין", ital="שף ושבת בגובה 1,560 מטר",
  intro="דאבוס שוכנת בגובה 1,560 מטר בקנטון גראובינדן, העיר הגבוהה ביותר באלפים, למרגלות הפארזן והיאקובסהורן. אנחנו מארגנים את החופשה הכשרה שלכם: שף פרטי שמבשל בצ'אלה או בדירה שלכם, קניות כשרות שהצוות שלנו מביא, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
  chips=["1,560 מטר, וייספלוגיפפל 2,844 מטר", "כשעתיים משדה התעופה של ציריך", "חורף וקיץ", "נבדק ב-30 באוקטובר 2026"],
  crumb="האלפים, כשרים לחלוטין",
  sections=[
    ("מה אנחנו מארגנים <i>בדאבוס</i>", """<ul>
<li><b>צ'אלה או דירה עם שף פרטי.</b> הצוות הכשר שלנו, שבסיסו באלפים, מכשיר את המטבח והשף מבשל במקום, כל ארוחה בשבוע. בחורף חוזרים מהפארזן או מהיאקובסהורן לשולחן ערוך; בקיץ, מהאגם או מהשבילים.</li>
<li><b>הקניות הכשרות מגיעות איתו.</b> בשר, יין, חלות ומצרכים יבשים נוסעים עם השף, ומוצהרים במכס השווייצרי כשצריך; את השאר קונים בחנויות הכשרות של ציריך, כשעתיים נסיעה. ספרו לנו איפה אתם ישנים: דאבוס פלאץ, דאבוס דורף, או אחד העמקים הצדדיים.</li>
<li><b>שבת.</b> ארוחות השבת, החלות והיין מבושלים וערוכים לפני הדלקת הנרות. שום דבר לא מוכן בשבת או בחג.</li>
<li><b>החגים.</b> חנוכה, פורים, פסח או סוכות בגראובינדן. ספרו לנו איזה חג חל בשבוע שלכם.</li>
<li><b>מניין וספר תורה.</b> משפחות יהודיות מגיעות לדאבוס כבר יותר ממאה שנה, ובעונה הגבוהה אתם כמעט אף פעם לא המשפחה השומרת היחידה בעיר. אנחנו בונים את המניין מהמשפחות שכותבות לנו לאותו שבוע: שלחו לנו את התאריכים מוקדם, עם ספר תורה לפי בקשה.</li>
<li><b>חופשה בהתאמה אישית, מא' ועד ת'.</b> צ'אלה, שף, הסעות מציריך, שבת, החגים, מניין: פנייה אחת, הצעת מחיר אחת. משפחות וקבוצות מחו״ל הן הלב של העבודה שלנו, כולל קבוצות גדולות ודוברי עברית. דאבוס רחוקה הרבה יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות: השף מגיע אליכם.</li>
</ul>
<p>שומר כשרות. הצוות הכשר שלנו באלפים מבשל תחת רשת חב"ד של האלפים. פירוט כל שירות: <a href="../kosher-services-french-alps/">שירותים כשרים באלפים</a>.</p>"""),
    ("כשר <i>בדאבוס</i>", """<p>ההשגחה כמעט אף פעם לא כתובה, אז כדאי לבדוק לפני שמזמינים.</p>
<ul>
<li><b>מסעדה, חנות או מלון כשרים.</b> עונתי במקרה הטוב, ולא בכל שנה. אנחנו לא תלויים בזה: סמכו על השף שלכם, או הביאו את האוכל שלכם.</li>
<li><b>בית כנסת ובית חב"ד.</b> אין בית כנסת קבוע רשום בדאבוס. הקהילה הקרובה ביותר היא ציריך, כשעתיים נסיעה, עם בתי כנסת, חנויות כשרות וקייטרינג.</li>
<li><b>אורחים יהודים.</b> דאבוס מארחת מבקרים יהודים עוד מימיה כעיירת מרפא; בחורף, משפחות שומרות מצוות הן חלק מהנוף של הפרומנדה.</li>
<li><b>ינואר.</b> הפורום הכלכלי העולמי ממלא את העיר שבוע אחד בינואר: הזמינו מוקדם מאוד לשבוע הזה, או בחרו שבוע אחר.</li>
<li><b>עונה.</b> הרכבלים של דאבוס קלוסטרס פועלים בדרך כלל מסוף נובמבר עד אמצע אפריל, היאקובסהורן קצת יותר מאוחר. בדקו את התאריכים של השבוע שלכם לפני שמזמינים.</li>
</ul>"""),
    ("חורף וקיץ <i>בדאבוס</i>", """<ul>
<li><b>חורף.</b> שישה אזורי סקי סביב דאבוס וקלוסטרס, כ-300 ק״מ של מסלולים: הפארזן עם פסגת וייספלוגיפפל בגובה 2,844 מטר, היאקובסהורן, פישה, רינרהורן, מדריזה והשאצאלפ. השקיעה מוקדמת ביום שישי בדצמבר, ולכן ארוחות השבת ערוכות הרבה לפני סגירת הרכבלים.</li>
<li><b>קיץ.</b> כ-700 ק״מ של שבילי הליכה, אגם דאבוס, אופני הרים, ופסטיבל דאבוס של מוזיקאים צעירים באוגוסט. השף מכין ארוחות לדרך בתיאום מראש.</li>
<li><b>מניין ושבת.</b> כל מניין בדאבוס נבנה מהמשפחות שכותבות לנו, עם ספר תורה. זמני השבת מופיעים בזמן אמת בעמוד הזה.</li>
</ul>"""),
    ("איך זה <i>עובד</i>", [
      ("כתבו לנו", "דאבוס, התאריכים, מספר המשתתפים, איפה אתם ישנים ומה אתם צריכים: שף, שבת, חג, מניין. בוואטסאפ או בטופס בתחתית העמוד."),
      ("אנחנו מסדרים", "באותו יום אנחנו בודקים עם הצוות שלנו באלפים מה אפשרי בתאריכים שלכם בדאבוס: שף, מטבח, קניות, מניין. איש קשר אחד מההתחלה ועד הסוף."),
      ("מקבלים הצעת מחיר אחת", "המחיר תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות."),
    ]),
    ("איך מגיעים <i>לדאבוס</i>", """<ul>
<li><b>משדה התעופה של ציריך:</b> כשעתיים בכביש דרך לנדקוורט ועמק הפרטיגאו.</li>
<li><b>ברכבת:</b> כשעתיים ורבע משדה התעופה של ציריך, עם החלפה בלנדקוורט לרכבת הרטית עד דאבוס דורף ודאבוס פלאץ.</li>
<li><b>משדה התעופה של ז'נבה:</b> כ-4 שעות וחצי בכביש; יום ארוך, עדיף עם עצירה בציריך לקניות הכשרות.</li>
<li><b>ממילאנו:</b> כ-3 שעות וחצי בכביש.</li>
<li><b>מנמל התעופה ליון-סנט-אקזופרי:</b> כ-5 שעות וחצי בכביש. לדאבוס, ציריך היא שדה התעופה הטבעי; ליון מתאימה לחופשה שמתחילה באלפים הצרפתיים: <a href="../lyon-gateway-to-the-alps-kosher/">ליון, שער האלפים</a>.</li>
<li><b>כניסה לשווייץ:</b> קחו דרכון או תעודת זהות לכל נוסע, כולל ילדים, וקנו מראש ברשת את מדבקת הכבישים המהירים של שווייץ (ויניטה) לפני הגבול. המוצרים הכשרים נוסעים עם השף ומוצהרים במכס כשצריך.</li>
</ul>"""),
    ("דאבוס <i>על המפה</i>", "הסימון על הפרומנדה, בדאבוס פלאץ."),
    ("כשר בדאבוס: <i>שאלות</i>", [
      ("כמה זה עולה?", "זה תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות. אנחנו לא מפרסמים מחירים."),
      ("יש משלוח ארוחות כשרות לדאבוס?", "לא. דאבוס רחוקה הרבה יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות. שף פרטי מגיע לצ'אלה שלכם עם הקניות הכשרות ומבשל במקום."),
      ("יש מניין בדאבוס?", "אין בית כנסת קבוע רשום. בעונה הגבוהה קל יותר לבנות מניין בדאבוס מאשר ברוב אתרי הסקי, כי משפחות שומרות מצוות מגיעות בכל חורף. שלחו לנו את התאריכים מוקדם ונחבר בין המשפחות שכותבות לנו, עם ספר תורה לפי בקשה."),
      ("אתם עובדים גם בקיץ, לא רק בחורף?", "כן. בקיץ דאבוס פתוחה למטיילים, לרוכבי אופניים ולבאי הפסטיבל, ובחורף לגולשים, והשירותים זהים: שף פרטי, שבת, חגים, מניין."),
      ("אפשר לארגן חופשה לקבוצה גדולה?", "כן. קבוצות ומשפחות מחו״ל הן הלב של העבודה שלנו. שלחו את מספר המשתתפים, התאריכים ומה אתם צריכים, ותקבלו הצעת מחיר אחת בכתב."),
      ("מי משגיח על האוכל?", "הצוות הכשר שלנו באלפים מבשל תחת רשת חב\"ד של האלפים. פרטי ההשגחה מצורפים להצעת המחיר."),
    ]),
    ("כשר בדאבוס העונה?", "שלום, אנחנו נוסעים לדאבוס. תאריכים: / מספר משתתפים: / אנחנו צריכים (שף, שבת, חג, מניין):"),
  ],
  related=["האלפים, כשרים לחלוטין", "שירותים כשרים באלפים, בפירוט", "חופשות סקי כשרות באלפים", "קיץ באלפים למשפחות יהודיות", "כשר בסנט מוריץ", "כשר בוורבייה", "כשר בגשטאד"],
  source="מקורות: Davos Klosters (davos.ch), הרכבת הרטית ו-SBB (sbb.ch), myswitzerland.com, swissjews.ch, chabadswitzerland.com, hebcal.com; הצוות שלנו באלפים לגבי השירותים. נבדק ב-30 באוקטובר 2026.",
  fixe=FIXE["he"],
)

traduire(S, FR, ES, HE, FORCE)
