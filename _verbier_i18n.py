# -*- coding: utf-8 -*-
"""29/10 : traductions FR / ES / HE de la page Verbier (source : _pages/kosher-verbier.py).
Rendu par le même moteur que _build_guide.py, puis greffé dans la copie préparée fr|es|he/kosher-verbier/index.html
(contenu de <main>, title, description, og, pied et bouton WhatsApp flottant repris de Crans-Montana dans la même langue).
Ne s'applique qu'à une copie encore marquée data-i18n="todo" (sauf --force). Lancer avec py -3.14 depuis site-v5.
30/10 : plus de livraison de repas (Mendel, validé par Moshé) : chef privé sur place, courses apportées, ou chalet seul."""
import io, os, re, sys, shutil, importlib.util, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.argv, FORCE = [sys.argv[0]], "--force" in sys.argv
import _build_guide as G
import _build_i18n as I
spec = importlib.util.spec_from_file_location("v", "_pages/kosher-verbier.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
EN = m.PAGE
S = "kosher-verbier"

FR = dict(
  title="Casher à Verbier : chef privé, Shabbat et minyan",
  desc="Casher à Verbier, en Valais, l’hiver comme l’été : un chef privé cuisine dans votre chalet, Shabbat, fêtes, minyan et Séfer Torah. Un seul devis écrit.",
  h1="Verbier, strictement casher", ital="le balcon des 4 Vallées",
  intro="Verbier se trouve à environ 1 500 m, en Valais, en haut des 4 Vallées, avec le Mont Fort à 3 330 m. Nous organisons votre séjour casher : un chef privé qui cuisine dans votre chalet, les courses casher apportées par notre équipe, Shabbat, minyan et Séfer Torah, en un seul devis écrit.",
  chips=["Environ 1 500 m, Mont Fort 3 330 m", "Environ 1 h 50 de l’aéroport de Genève, 3 h 40 de Lyon", "Hiver et été", "Vérifié le 30 octobre 2026"],
  crumb="Les Alpes, strictement casher",
  sections=[
    ("Ce que nous organisons <i>à Verbier</i>", """<ul>
<li><b>Un chalet ou un appartement avec chef privé.</b> Notre équipe casher basée dans les Alpes rend la cuisine casher et le chef cuisine sur place, tous les repas de la semaine. L’hiver, vous rentrez des 4 Vallées pour trouver la table dressée ; l’été, des sentiers de VTT ou d’un concert du festival.</li>
<li><b>Les courses casher, apportées.</b> Viande, vin, ’hallot et épicerie voyagent avec le chef, déclarés à la douane suisse quand il le faut ; le reste s’achète dans les commerces casher de Genève ou de Lausanne en montant. Dites-nous où vous dormez : dans le village, plus haut sur les pistes, ou en bas au Châble, car la route qui monte ajoute des minutes par temps de neige.</li>
<li><b>Shabbat.</b> Les repas de Shabbat, les ’hallot et le vin sont cuisinés et dressés avant l’allumage des bougies. Rien n’est préparé pendant Shabbat ni un jour de fête.</li>
<li><b>Les fêtes.</b> Hanouka, Pourim, Pessah ou Souccot en Valais. Dites-nous quelle fête tombe pendant votre semaine.</li>
<li><b>Un minyan et un Séfer Torah.</b> Aucune synagogue n’est répertoriée à Verbier : le minyan se forme avec les familles qui nous écrivent pour la même semaine. Donnez-nous vos dates tôt et nous les regroupons, avec un Séfer Torah.</li>
<li><b>Le chalet seul.</b> Si vous préférez cuisiner vous-mêmes, nous trouvons le chalet et nous vous disons où faire vos courses casher avant de monter. Demandez-le ainsi.</li>
<li><b>Un séjour sur mesure, de A à Z.</b> Chalet, chef, transferts depuis Genève, Shabbat, les fêtes, un minyan : une demande, un devis. Les familles et les groupes venus de l’étranger sont notre cœur de cible, y compris les grands groupes et les hôtes hébréophones. Verbier est à plus de trois heures de notre cuisine des Alpes françaises : nous n’y livrons pas de repas, le chef vient chez vous.</li>
</ul>
<p>Strictement casher. Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de chaque service : <a href="../kosher-services-french-alps/">services casher dans les Alpes</a>.</p>"""),
    ("Casher <i>à Verbier</i>", """<p>La surveillance est rarement écrite noir sur blanc : renseignez-vous avant de réserver.</p>
<ul>
<li><b>Restaurant, commerce ou hôtel casher.</b> Aucun trouvé dans la station. Comptez sur votre chef, ou apportez votre nourriture.</li>
<li><b>Synagogue et Beth Habad.</b> Aucun n’est répertorié à Verbier ni dans le val de Bagnes. La synagogue la plus proche en Valais est à <a href="../kosher-crans-montana/">Crans-Montana</a>, ouverte par saison.</li>
<li><b>Hôtes juifs.</b> La Fédération suisse des communautés israélites a ajouté Verbier à son projet d’été pour les visiteurs juifs en 2022 : des familles juives viennent bien, l’été comme l’hiver.</li>
<li><b>Grandes communautés les plus proches.</b> Genève et Lausanne, toutes deux sur la route depuis l’aéroport de Genève, ont des synagogues, des commerces casher et des traiteurs. Faites vos courses là avant de monter.</li>
<li><b>Saison.</b> Les remontées de Verbier sont annoncées du 5 décembre 2026 au 25 avril 2027, avec des ouvertures le week-end en novembre si la neige le permet. L’ensemble des 4 Vallées est annoncé du 12 décembre 2026 au 18 avril 2027.</li>
</ul>"""),
    ("L’hiver et l’été <i>à Verbier</i>", """<ul>
<li><b>L’hiver.</b> Verbier ouvre sur les 4 Vallées, environ 410 km de pistes reliées à Nendaz, Veysonnaz, Thyon et La Tzoumaz, le plus grand domaine skiable de Suisse. Le Mont Fort le domine à 3 330 m. Le soleil se couche tôt un vendredi de décembre : les repas de Shabbat sont dressés bien avant la fermeture des remontées.</li>
<li><b>L’été.</b> Plus de 500 km de sentiers de randonnée et plus de 800 km de pistes de VTT partent du village. Le Verbier Festival propose des concerts de musique classique du 15 juillet au 1er août 2027. Le chef prépare des paniers-repas pour la randonnée sur demande.</li>
<li><b>Minyan et Shabbat.</b> Sans synagogue dans la station, chaque minyan à Verbier se forme avec les familles qui nous écrivent, avec un Séfer Torah. Les horaires de Shabbat s’affichent en direct sur les pages Alpes de ce site.</li>
</ul>"""),
    ("Comment ça <i>se passe</i>", [
      ("Dites-nous", "Verbier, vos dates, le nombre de personnes, l’endroit où vous dormez, et ce qu’il vous faut : un chef, Shabbat, une fête, un minyan, ou le chalet seul. Par WhatsApp ou avec le formulaire en bas de cette page."),
      ("Nous montons le séjour", "Le jour même, nous vérifions avec notre équipe dans les Alpes ce qui est possible pour vos dates à Verbier : chef, cuisine, courses, minyan. Un seul interlocuteur du début à la fin."),
      ("Vous recevez un devis", "Le prix dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager."),
    ]),
    ("Se rendre <i>à Verbier</i>", """<ul>
<li><b>Depuis l’aéroport de Genève :</b> environ 1 h 50 par la route, le long du lac puis de la vallée du Rhône, avant de monter depuis Le Châble.</li>
<li><b>En train :</b> environ 2 h 40 depuis Genève, avec un changement à Martigny pour Le Châble. Les week-ends d’hiver et les jours fériés, des trains directs vont jusqu’au Châble.</li>
<li><b>Depuis Le Châble :</b> la télécabine monte à Verbier en environ 20 minutes et circule de 5 h 10 à 23 h 55 ; un bus fait le même trajet au même tarif.</li>
<li><b>Depuis Sion :</b> environ 50 minutes en voiture.</li>
<li><b>Depuis Lyon-Saint-Exupéry :</b> environ 3 h 40 par la route via Genève. Lyon convient aux vols long-courriers et à de premières courses casher avant la montée : <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, la porte des Alpes</a>.</li>
<li><b>Passage depuis la France :</b> munissez-vous d’un passeport ou d’une carte d’identité pour chaque voyageur, enfants compris, et achetez en ligne la vignette autoroutière suisse avant la frontière, car la route depuis Genève emprunte les autoroutes suisses. Les produits casher voyagent avec le chef et sont déclarés à la douane quand il le faut.</li>
<li><b>Vous atterrissez à Lyon avec quelques heures devant vous ?</b> <a href="../tours/stopover/">L’Escale</a> : une visite privée de 3 heures du patrimoine juif de Lyon, entre l’avion et la route.</li>
</ul>"""),
    ("Verbier <i>sur la carte</i>", "Repère sur la place Centrale, dans le village."),
    ("Casher à Verbier : <i>vos questions</i>", [
      ("Combien ça coûte ?", "Cela dépend des dates, du nombre de personnes et du menu. Vous recevez un devis écrit avant de vous engager. Nous ne publions aucun prix."),
      ("Livrez-vous des repas casher à Verbier ?", "Non. Verbier est à plus de trois heures de notre cuisine des Alpes françaises : aucun repas n’y est livré. Un chef privé vient dans votre chalet avec les courses casher et cuisine sur place, ou vous prenez le chalet seul et cuisinez vous-mêmes."),
      ("Y a-t-il un minyan à Verbier ?", "Aucune synagogue n’est répertoriée dans la station. Un minyan dépend du nombre de familles présentes à Verbier cette semaine-là. Donnez-nous vos dates tôt et nous les regroupons, avec un Séfer Torah."),
      ("Travaillez-vous l’été comme l’hiver ?", "Oui. Verbier accueille randonneurs, vététistes et festivaliers l’été et skieurs l’hiver, et les services sont les mêmes : chef privé, Shabbat, fêtes, minyan."),
      ("Pouvez-vous organiser un séjour pour un grand groupe ?", "Oui. Les groupes et les familles venus de l’étranger sont notre cœur de cible. Envoyez le nombre de personnes, les dates et ce qu’il vous faut, et vous recevez un seul devis écrit."),
      ("Qui surveille la cacherout des repas ?", "Notre équipe casher basée dans les Alpes cuisine sous le réseau ’Habad des Alpes. Le détail de la surveillance accompagne votre devis."),
    ]),
    ("Casher à Verbier cette saison ?", "Bonjour, nous allons à Verbier. Dates : / Nombre de personnes : / Il nous faut (chef, Shabbat, fête, minyan, chalet seul) :"),
  ],
  related=["Les Alpes, strictement casher", "Services casher dans les Alpes, en détail", "Vacances au ski casher dans les Alpes", "L’été dans les Alpes pour les familles juives", "Lyon, la porte des Alpes", "Casher à Zermatt", "Casher à Crans-Montana"],
  source="Sources : Verbier Tourisme (verbier.ch), Verbier 4Vallées (verbier4vallees.ch), seeverbier.com, verbier.com, myswitzerland.com, valais.ch, swissjews.ch, chabadswitzerland.com, gokosher.com, skikosher.com, hebcal.com ; notre équipe dans les Alpes pour les services. Vérifié le 30 octobre 2026.",
  fixe={"Home": "Accueil", "Ask on WhatsApp": "Écrire sur WhatsApp", "Get a quote": "Demander un devis", "Same-day reply, never on Shabbat.": "Réponse le jour même, jamais pendant Shabbat.", "Keep <i>reading</i>": "Pour <i>aller plus loin</i>"},
)

ES = dict(
  title="Kosher en Verbier: chef privado, Shabat y minián",
  desc="Verbier, en el Valais, estrictamente kosher en invierno y verano: un chef privado cocina en su chalé, Shabat, fiestas, minián y Séfer Torá. Un presupuesto.",
  h1="Verbier", ital="estrictamente kosher, 4 Vallées",
  intro="Verbier está a unos 1.500 m en el Valais, en lo alto de los 4 Vallées, con el Mont Fort a 3.330 m. Organizamos su estancia kosher: un chef privado que cocina en su chalé, con la compra kosher traída por nuestro equipo, Shabat, minián y Séfer Torá, en un único presupuesto por escrito.",
  chips=["Unos 1.500 m, Mont Fort 3.330 m", "Unas 1 h 50 del aeropuerto de Ginebra, 3 h 40 de Lyon", "Invierno y verano", "Comprobado el 30 de octubre de 2026"],
  crumb="Los Alpes, estrictamente kosher",
  sections=[
    ("Lo que organizamos <i>en Verbier</i>", """<ul>
<li><b>Un chalé o un apartamento con chef privado.</b> Nuestro equipo kosher con base en los Alpes kosheriza la cocina y el chef cocina allí mismo, todas las comidas de la semana. En invierno vuelve de los 4 Vallées a una mesa servida; en verano, de las rutas en bicicleta o de un concierto del festival.</li>
<li><b>La compra kosher, traída.</b> Carne, vino, jalot y productos secos viajan con el chef, declarados en la aduana suiza cuando hace falta; el resto se compra en las tiendas kosher de Ginebra o Lausana de camino. Díganos dónde duerme: en el pueblo, más arriba en las pistas o abajo en Le Châble, porque la carretera de subida añade minutos con nieve.</li>
<li><b>Shabat.</b> Las comidas de Shabat, las jalot y el vino se cocinan y se sirven antes del encendido de las velas. No se prepara nada en Shabat ni en día de fiesta.</li>
<li><b>Las fiestas.</b> Janucá, Purim, Pésaj o Sucot en el Valais. Díganos qué fiesta cae en su semana.</li>
<li><b>Un minián y un Séfer Torá.</b> No hay ninguna sinagoga registrada en Verbier, así que el minián se forma con las familias que nos escriben para la misma semana. Denos sus fechas pronto y las agrupamos, con un Séfer Torá.</li>
<li><b>El chalé solo.</b> Si prefiere cocinar usted mismo, buscamos el chalé y le decimos dónde hacer la compra kosher antes de subir. Pídalo así.</li>
<li><b>Una estancia a medida, de la A a la Z.</b> Chalé, chef, traslados desde Ginebra, Shabat, las fiestas, un minián: una solicitud, un presupuesto. Las familias y los grupos del extranjero son nuestro núcleo, incluidos los grupos grandes y los huéspedes de habla hebrea. Verbier está a más de tres horas de nuestra cocina en los Alpes franceses: allí no entregamos comidas, el chef va a su casa.</li>
</ul>
<p>Estrictamente kosher. Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Detalle de cada servicio: <a href="../kosher-services-french-alps/">servicios kosher en los Alpes</a>.</p>"""),
    ("Kosher <i>en Verbier</i>", """<p>La supervisión rara vez está por escrito, así que compruébelo antes de reservar.</p>
<ul>
<li><b>Restaurante, tienda u hotel kosher.</b> Ninguno en la estación. Cuente con su chef, o traiga su comida.</li>
<li><b>Sinagoga y casa Jabad.</b> Ninguna registrada en Verbier ni en el Val de Bagnes. La sinagoga más cercana en el Valais está en <a href="../kosher-crans-montana/">Crans-Montana</a>, abierta por temporadas.</li>
<li><b>Huéspedes judíos.</b> La Federación Suiza de Comunidades Judías añadió Verbier a su proyecto de verano para visitantes judíos en 2022: las familias judías vienen, en verano como en invierno.</li>
<li><b>Grandes comunidades más cercanas.</b> Ginebra y Lausana, ambas en la ruta desde el aeropuerto de Ginebra, tienen sinagogas, tiendas kosher y servicios de catering. Haga allí sus compras antes de subir.</li>
<li><b>Temporada.</b> Los remontes de Verbier están anunciados del 5 de diciembre de 2026 al 25 de abril de 2027, con aperturas de fin de semana en noviembre si hay nieve. El conjunto de los 4 Vallées está anunciado del 12 de diciembre de 2026 al 18 de abril de 2027.</li>
</ul>"""),
    ("Invierno y verano <i>en Verbier</i>", """<ul>
<li><b>Invierno.</b> Verbier se abre a los 4 Vallées, unos 410 km de pistas unidas con Nendaz, Veysonnaz, Thyon y La Tzoumaz, el mayor dominio esquiable de Suiza. El Mont Fort lo corona a 3.330 m. El sol se pone pronto un viernes de diciembre, así que las comidas de Shabat se sirven mucho antes del cierre de los remontes.</li>
<li><b>Verano.</b> Más de 500 km de senderos y más de 800 km de rutas de bicicleta de montaña salen del pueblo. El Verbier Festival ofrece conciertos de música clásica del 15 de julio al 1 de agosto de 2027. El chef prepara comidas para llevar a la ruta con antelación.</li>
<li><b>Minián y Shabat.</b> Sin sinagoga en la estación, cada minián en Verbier se forma con las familias que nos escriben, con un Séfer Torá. Los horarios de Shabat aparecen en directo en las páginas de los Alpes de este sitio.</li>
</ul>"""),
    ("Cómo <i>funciona</i>", [
      ("Escríbanos", "Verbier, sus fechas, el número de personas, dónde duerme y lo que necesita: un chef, Shabat, una fiesta, un minián o el chalé solo. Por WhatsApp o con el formulario al pie de esta página."),
      ("Lo preparamos", "El mismo día comprobamos con nuestro equipo en los Alpes lo que es posible para sus fechas en Verbier: chef, cocina, compra, minián. Un único contacto de principio a fin."),
      ("Recibe un presupuesto", "El precio depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse."),
    ]),
    ("Cómo llegar <i>a Verbier</i>", """<ul>
<li><b>Desde el aeropuerto de Ginebra:</b> unas 1 h 50 por carretera, a lo largo del lago y del valle del Ródano, y luego la subida desde Le Châble.</li>
<li><b>En tren:</b> unas 2 h 40 desde Ginebra, con cambio en Martigny para Le Châble. Los fines de semana de invierno y los festivos hay trenes directos hasta Le Châble.</li>
<li><b>Desde Le Châble:</b> el telecabina sube a Verbier en unos 20 minutos y funciona de 5:10 a 23:55; un autobús hace el mismo trayecto con la misma tarifa.</li>
<li><b>Desde Sion:</b> unos 50 minutos en coche.</li>
<li><b>Desde Lyon-Saint-Exupéry:</b> unas 3 h 40 por carretera vía Ginebra. Lyon conviene a los vuelos de largo recorrido y a una primera compra kosher antes de subir: <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, puerta de los Alpes</a>.</li>
<li><b>Al cruzar desde Francia:</b> lleve pasaporte o documento de identidad para cada viajero, niños incluidos, y compre en línea la viñeta de las autopistas suizas antes de la frontera, porque la ruta desde Ginebra usa autopistas suizas. Los productos kosher viajan con el chef y se declaran en la aduana cuando hace falta.</li>
<li><b>¿Aterriza en Lyon con unas horas libres?</b> <a href="../tours/stopover/">La Escala</a>: una visita privada de 3 horas del Lyon judío entre el avión y la carretera.</li>
</ul>"""),
    ("Verbier <i>en el mapa</i>", "Marcador en la Place Centrale, en el pueblo."),
    ("Kosher en Verbier: <i>preguntas</i>", [
      ("¿Cuánto cuesta?", "Depende de las fechas, del número de personas y del menú. Recibe un presupuesto por escrito antes de comprometerse. No publicamos precios."),
      ("¿Entregan comidas kosher en Verbier?", "No. Verbier está a más de tres horas de nuestra cocina en los Alpes franceses, así que allí no se entregan comidas. Un chef privado va a su chalé con la compra kosher y cocina allí mismo, o toma el chalé solo y cocina usted mismo."),
      ("¿Hay minián en Verbier?", "No hay ninguna sinagoga registrada en la estación. Un minián depende de cuántas familias estén en Verbier esa semana. Denos sus fechas pronto y las agrupamos, con un Séfer Torá."),
      ("¿Trabajan en verano además de en invierno?", "Sí. Verbier recibe a senderistas, ciclistas y público del festival en verano y a esquiadores en invierno, y los servicios son los mismos: chef privado, Shabat, fiestas, minián."),
      ("¿Pueden organizar una estancia para un grupo grande?", "Sí. Los grupos y las familias del extranjero son nuestro núcleo. Envíe el número de personas, las fechas y lo que necesita, y recibe un único presupuesto por escrito."),
      ("¿Quién supervisa la comida?", "Nuestro equipo kosher con base en los Alpes cocina bajo la red Jabad de los Alpes. Los detalles de la supervisión acompañan su presupuesto."),
    ]),
    ("¿Kosher en Verbier esta temporada?", "Hola, vamos a Verbier. Fechas: / Número de personas: / Necesitamos (chef, Shabat, fiesta, minián, chalé solo):"),
  ],
  related=["Los Alpes, estrictamente kosher", "Servicios kosher en los Alpes, en detalle", "Vacaciones de esquí kosher en los Alpes", "Verano en los Alpes para familias judías", "Lyon, puerta de los Alpes", "Kosher en Zermatt", "Kosher en Crans-Montana"],
  source="Fuentes: Verbier Tourisme (verbier.ch), Verbier 4Vallées (verbier4vallees.ch), seeverbier.com, verbier.com, myswitzerland.com, valais.ch, swissjews.ch, chabadswitzerland.com, gokosher.com, skikosher.com, hebcal.com; nuestro equipo en los Alpes para los servicios. Comprobado el 30 de octubre de 2026.",
  fixe={"Home": "Inicio", "Ask on WhatsApp": "Escribir por WhatsApp", "Get a quote": "Pedir presupuesto", "Same-day reply, never on Shabbat.": "Respuesta el mismo día, nunca en Shabat.", "Keep <i>reading</i>": "Siga <i>leyendo</i>"},
)

HE = dict(
  title="ורבייה כשר: שף פרטי, שבת ומניין",
  desc="ורבייה כשר לחלוטין בקנטון ואלה, בחורף ובקיץ: שף פרטי מבשל בצ'אלה שלכם, הקניות הכשרות מגיעות איתו, שבת, חגים, מניין וספר תורה. הצעת מחיר אחת בכתב.",
  h1="ורבייה, כשר לחלוטין", ital="על המרפסת השטופה בשמש של ארבעת העמקים",
  intro="ורבייה שוכן בגובה של כ-1,500 מטר בקנטון ואלה, בראש אזור ארבעת העמקים, ופסגת מון פור מתנשאת ל-3,330 מטר. אנחנו מארגנים את החופשה הכשרה שלכם: שף פרטי שמבשל בצ'אלה שלכם, קניות כשרות שהצוות שלנו מביא, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
  chips=["כ-1,500 מטר, מון פור 3,330 מטר", "כשעה ו-50 דקות משדה התעופה של ז'נבה, 3 שעות ו-40 דקות מליון", "חורף וקיץ", "נבדק ב-30 באוקטובר 2026"],
  crumb="האלפים, כשרים לחלוטין",
  sections=[
    ("מה אנחנו מארגנים <i>בוורבייה</i>", """<ul>
<li><b>צ'אלה או דירה עם שף פרטי.</b> הצוות הכשר שלנו, שבסיסו באלפים, מכשיר את המטבח והשף מבשל במקום, כל ארוחה בשבוע. בחורף חוזרים מהמסלולים לשולחן ערוך; בקיץ, משבילי האופניים או מקונצרט בפסטיבל.</li>
<li><b>הקניות הכשרות מגיעות איתו.</b> בשר, יין, חלות ומצרכים יבשים נוסעים עם השף, ומוצהרים במכס השווייצרי כשצריך; את השאר קונים בחנויות הכשרות של ז'נבה או לוזאן בדרך למעלה. ספרו לנו איפה אתם ישנים: בכפר, גבוה יותר על המדרונות, או למטה בלה שאבל, כי הדרך למעלה מוסיפה דקות בשלג.</li>
<li><b>שבת.</b> ארוחות השבת, החלות והיין מבושלים וערוכים לפני הדלקת הנרות. שום דבר לא מוכן בשבת או בחג.</li>
<li><b>החגים.</b> חנוכה, פורים, פסח או סוכות בקנטון ואלה. ספרו לנו איזה חג חל בשבוע שלכם.</li>
<li><b>מניין וספר תורה.</b> אין בית כנסת רשום בוורבייה, ולכן המניין נבנה מהמשפחות שכותבות לנו לאותו שבוע. שלחו לנו את התאריכים מוקדם ונחבר ביניהן, עם ספר תורה.</li>
<li><b>הצ'אלה בלבד.</b> אם אתם מעדיפים לבשל בעצמכם, אנחנו מוצאים את הצ'אלה ואומרים לכם איפה לקנות אוכל כשר לפני העלייה. בקשו את זה כך.</li>
<li><b>חופשה בהתאמה אישית, מא' ועד ת'.</b> צ'אלה, שף, הסעות מז'נבה, שבת, החגים, מניין: פנייה אחת, הצעת מחיר אחת. משפחות וקבוצות מחו״ל הן הלב של העבודה שלנו, כולל קבוצות גדולות ודוברי עברית. ורבייה נמצא יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות: השף מגיע אליכם.</li>
</ul>
<p>שומר כשרות. הצוות הכשר שלנו באלפים מבשל תחת רשת חב"ד של האלפים. פירוט כל שירות: <a href="../kosher-services-french-alps/">שירותים כשרים באלפים</a>.</p>"""),
    ("כשר <i>בוורבייה</i>", """<p>ההשגחה כמעט אף פעם לא כתובה, אז כדאי לבדוק לפני שמזמינים.</p>
<ul>
<li><b>מסעדה, חנות או מלון כשרים.</b> לא נמצאו באתר. סמכו על השף שלכם, או הביאו את האוכל שלכם.</li>
<li><b>בית כנסת ובית חב"ד.</b> אינם רשומים בוורבייה ולא בעמק באן. בית הכנסת הקרוב ביותר בקנטון ואלה נמצא ב<a href="../kosher-crans-montana/">קראן מונטנה</a>, ופתוח לפי עונות.</li>
<li><b>אורחים יהודים.</b> התאחדות הקהילות היהודיות בשווייץ צירפה את ורבייה ב-2022 לפרויקט הקיץ שלה למבקרים יהודים: משפחות יהודיות אכן מגיעות, בקיץ כמו בחורף.</li>
<li><b>הקהילות הגדולות הקרובות.</b> בז'נבה ובלוזאן, שתיהן על הדרך משדה התעופה של ז'נבה, יש בתי כנסת, חנויות כשרות וקייטרינג. עשו שם קניות לפני העלייה.</li>
<li><b>עונה.</b> הרכבלים של ורבייה מתוכננים לפעול מ-5 בדצמבר 2026 עד 25 באפריל 2027, עם פתיחה בסופי שבוע בנובמבר אם יש שלג. אזור ארבעת העמקים כולו מתוכנן לפעול מ-12 בדצמבר 2026 עד 18 באפריל 2027.</li>
</ul>"""),
    ("חורף וקיץ <i>בוורבייה</i>", """<ul>
<li><b>חורף.</b> ורבייה נפתח אל ארבעת העמקים, כ-410 ק״מ של מסלולים המחברים חמישה אתרים, אזור הסקי הגדול בשווייץ. פסגת מון פור מתנשאת מעליו ל-3,330 מטר. השקיעה מוקדמת ביום שישי בדצמבר, ולכן ארוחות השבת ערוכות הרבה לפני סגירת הרכבלים.</li>
<li><b>קיץ.</b> יותר מ-500 ק״מ של שבילי הליכה ויותר מ-800 ק״מ של שבילי אופני הרים יוצאים מהכפר. פסטיבל ורבייה מביא קונצרטים של מוזיקה קלאסית מ-15 ביולי עד 1 באוגוסט 2027. השף מכין ארוחות לדרך בתיאום מראש.</li>
<li><b>מניין ושבת.</b> אין בית כנסת באתר, ולכן כל מניין בוורבייה נבנה מהמשפחות שכותבות לנו, עם ספר תורה. זמני השבת מופיעים בזמן אמת בעמודי האלפים באתר הזה.</li>
</ul>"""),
    ("איך זה <i>עובד</i>", [
      ("כתבו לנו", "ורבייה, התאריכים, מספר המשתתפים, איפה אתם ישנים ומה אתם צריכים: שף, שבת, חג, מניין, או צ'אלה בלבד. בוואטסאפ או בטופס בתחתית העמוד."),
      ("אנחנו מסדרים", "באותו יום אנחנו בודקים עם הצוות שלנו באלפים מה אפשרי בתאריכים שלכם בוורבייה: שף, מטבח, קניות, מניין. איש קשר אחד מההתחלה ועד הסוף."),
      ("מקבלים הצעת מחיר אחת", "המחיר תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות."),
    ]),
    ("איך מגיעים <i>לוורבייה</i>", """<ul>
<li><b>משדה התעופה של ז'נבה:</b> כשעה ו-50 דקות בכביש, לאורך האגם ועמק הרון, ואז עלייה מלה שאבל.</li>
<li><b>ברכבת:</b> כשעתיים ו-40 דקות מז'נבה, עם החלפה במרטיני לכיוון לה שאבל. בסופי שבוע בחורף ובחגים יש רכבות ישירות עד לה שאבל.</li>
<li><b>מלה שאבל:</b> הרכבל עולה לוורבייה בכ-20 דקות ופועל מ-5:10 עד 23:55; אוטובוס עושה את אותה דרך באותו מחיר נסיעה.</li>
<li><b>מסיון:</b> כ-50 דקות ברכב.</li>
<li><b>מנמל התעופה ליון-סנט-אקזופרי:</b> כ-3 שעות ו-40 דקות בכביש דרך ז'נבה. ליון מתאימה לטיסות ארוכות ולקניות כשרות ראשונות לפני העלייה להרים: <a href="../lyon-gateway-to-the-alps-kosher/">ליון, שער האלפים</a>.</li>
<li><b>מעבר מצרפת:</b> קחו דרכון או תעודת זהות לכל נוסע, כולל ילדים, וקנו מראש ברשת את מדבקת הכבישים המהירים של שווייץ (ויניטה) לפני הגבול, כי הדרך מז'נבה עוברת בכבישים מהירים שווייצריים. המוצרים הכשרים נוסעים עם השף ומוצהרים במכס כשצריך.</li>
<li><b>נוחתים בליון עם כמה שעות פנויות?</b> <a href="../tours/stopover/">העצירה בליון</a>: סיור פרטי של 3 שעות בעקבות יהדות ליון, בין המטוס לדרך.</li>
</ul>"""),
    ("ורבייה <i>על המפה</i>", "הסימון על הכיכר המרכזית של הכפר."),
    ("כשר בוורבייה: <i>שאלות</i>", [
      ("כמה זה עולה?", "זה תלוי בתאריכים, במספר המשתתפים ובתפריט. אתם מקבלים הצעת מחיר בכתב לפני כל התחייבות. אנחנו לא מפרסמים מחירים."),
      ("יש משלוח ארוחות כשרות לוורבייה?", "לא. ורבייה נמצא יותר משלוש שעות מהמטבח שלנו באלפים הצרפתיים, ולכן אין שם משלוח ארוחות. שף פרטי מגיע לצ'אלה שלכם עם הקניות הכשרות ומבשל במקום, או שאתם לוקחים את הצ'אלה בלבד ומבשלים בעצמכם."),
      ("יש מניין בוורבייה?", "אין בית כנסת רשום באתר. מניין תלוי במספר המשפחות שנמצאות בוורבייה באותו שבוע. שלחו לנו את התאריכים מוקדם ונחבר ביניהן, עם ספר תורה."),
      ("אתם עובדים גם בקיץ, לא רק בחורף?", "כן. בקיץ ורבייה פתוח למטיילים, לרוכבי אופניים ולבאי הפסטיבל, ובחורף לגולשים, והשירותים זהים: שף פרטי, שבת, חגים, מניין."),
      ("אפשר לארגן חופשה לקבוצה גדולה?", "כן. קבוצות ומשפחות מחו״ל הן הלב של העבודה שלנו. שלחו את מספר המשתתפים, התאריכים ומה אתם צריכים, ותקבלו הצעת מחיר אחת בכתב."),
      ("מי משגיח על האוכל?", "הצוות הכשר שלנו באלפים מבשל תחת רשת חב\"ד של האלפים. פרטי ההשגחה מצורפים להצעת המחיר."),
    ]),
    ("כשר בוורבייה העונה?", "שלום, אנחנו נוסעים לוורבייה. תאריכים: / מספר משתתפים: / אנחנו צריכים (שף, שבת, חג, מניין, צ'אלה בלבד):"),
  ],
  related=["האלפים, כשרים לחלוטין", "שירותים כשרים באלפים, בפירוט", "חופשות סקי כשרות באלפים", "קיץ באלפים למשפחות יהודיות", "ליון, שער האלפים", "כשר בצרמט", "כשר בקראן מונטנה"],
  source="מקורות: Verbier Tourisme (verbier.ch), Verbier 4Vallées (verbier4vallees.ch), seeverbier.com, verbier.com, myswitzerland.com, valais.ch, swissjews.ch, chabadswitzerland.com, gokosher.com, skikosher.com, hebcal.com; הצוות שלנו באלפים לגבי השירותים. נבדק ב-30 באוקטובר 2026.",
  fixe={"Home": "דף הבית", "Ask on WhatsApp": "כתבו לנו בוואטסאפ", "Get a quote": "בקשו הצעת מחיר", "Same-day reply, never on Shabbat.": "מענה באותו יום, לעולם לא בשבת.", "Keep <i>reading</i>": "להמשך <i>קריאה</i>"},
)

def page(lang, T):
    """PAGE anglais où chaque texte est remplacé par sa traduction (même ordre de sections)."""
    P = dict(EN); secs = []; k = 0
    for s in EN["sections"]:
        s = dict(s); t = T["sections"][k]; k += 1
        if s["type"] in ("text", "beige"): s["h2"], s["html"] = t
        elif s["type"] == "steps": s["h2"], s["items"] = t
        elif s["type"] == "map": s["h2"], s["note"] = t
        elif s["type"] == "faq": s["h2"], s["items"] = t
        elif s["type"] == "cta": s["txt"], s["msg"] = t
        secs.append(s)
    P.update(slug=f"_tmp-verbier-{lang}", title=T["title"], desc=T["desc"], h1=T["h1"], ital=T["ital"], intro=T["intro"], chips=T["chips"],
             crumb=(EN["crumb"][0], T["crumb"]), sections=secs, related=[(u, t) for (u, _), t in zip(EN["related"], T["related"])], source=T["source"])
    return P

def nbsp_fr(h):
    """Typographie française dans le texte (pas dans les balises) : espace insécable avant : ; ? ! et dans les nombres."""
    def f(m):
        t = m.group(0)
        t = re.sub(r" ([:;?!])", "\u00a0\\1", t)
        t = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", t)
        t = re.sub(r"(\d) (h|m|km|min|minutes|heures)\b", "\\1\u00a0\\2", t)
        return t
    return re.sub(r">[^<]+<", f, h)

for lang, T in (("fr", FR), ("es", ES), ("he", HE)):
    dst = f"{lang}/{S}/index.html"
    cur = I.rd(dst)
    if 'data-i18n="todo"' not in cur and not FORCE: print("déjà traduit", dst); continue
    P = page(lang, T)
    G.build(P)
    out = io.open(f"{P['slug']}/index.html", encoding="utf-8").read(); shutil.rmtree(P["slug"])
    main = out[out.index("<main>"):out.index("</main>") + 7]
    main = main.replace(f'<p class="source">{T["source"]} Compiled by Mishpacha Tours from these sources. Checked {G.CHECKED}.</p>', f'<p class="source">{T["source"]}</p>')
    for a, b in T["fixe"].items(): main = main.replace(a, b)
    main = I.absolutize(main, S)
    for q in I.LOT:
        qp = f"/{q}/" if q else "/"
        main = re.sub(r'href="' + re.escape(qp) + r'(#[^"]*)?"', lambda mm: f'href="/{lang}{qp}{mm.group(1) or ""}"', main)
    if lang == "fr": main = nbsp_fr(main)
    h = cur[:cur.index("<main>")] + main + cur[cur.index("</main>") + 7:]
    tt, dd = html.escape(T["title"]), html.escape(T["desc"])
    if lang == "fr": tt, dd = nbsp_fr(">" + tt + "<")[1:-1], nbsp_fr(">" + dd + "<")[1:-1]
    h = re.sub(r"<title>.*?</title>", f"<title>{tt} | Mishpacha Tours</title>", h, count=1)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda mm: mm.group(1) + dd, h)
    for k in ('property="og:title"', 'name="twitter:title"'):
        h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda mm: mm.group(1) + f"{tt} | Mishpacha Tours", h)
    ref = I.rd(f"{lang}/kosher-crans-montana/index.html")
    pied = re.search(r'<footer class="pied">.*?</footer>', ref, re.S).group(0)
    h = re.sub(r'<footer class="pied">.*?</footer>', lambda _: pied, h, count=1, flags=re.S)
    flot = re.search(r'<a class="wa-flottant"[^>]*>.*?</a>', ref, re.S).group(0)
    h = re.sub(r'<a class="wa-flottant"[^>]*>.*?</a>', lambda _: flot, h, count=1, flags=re.S)
    h = h.replace(' data-i18n="todo"', "", 1)
    I.wr(dst, h); print("traduit", dst)
