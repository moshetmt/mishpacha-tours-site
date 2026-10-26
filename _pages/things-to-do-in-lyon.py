# -*- coding: utf-8 -*-
"""21/10 : /things-to-do-in-lyon/. PAGE = source anglaise lue par _build_guide.py. PAGE_FR, PAGE_ES, PAGE_HE = traductions
(meme structure, memes liens relatifs), lues par le script d'assemblage des copies (voir le rapport). Ne pas mettre de prix ni de numero."""

import re
LAB = (("Time:", "Children:", "Kosher:", "Shabbat:"), ("Durée :", "Enfants :", "Casher :", "Shabbat :"),
       ("Duración:", "Niños:", "Kosher:", "Shabat:"), ("משך:", "ילדים:", "כשר:", "שבת:"))
WA_MSG = ("Hello, I am planning a stay in Lyon and would like a Jewish visit and Shabbat arranged. Dates: / Number of people: / Preferred language:",
          "Bonjour, je prépare un séjour à Lyon et souhaite une visite juive et un Shabbat organisés. Dates : / Nombre de personnes : / Langue souhaitée :",
          "Hola, preparo una estancia en Lyon y quisiera una visita judía y un Shabat organizados. Fechas: / Número de personas: / Idioma preferido:",
          "שלום, אנחנו מתכננים שהות בליון ורוצים סיור יהודי ושבת מסודרים. תאריכים: / מספר משתתפים: / שפה מועדפת:")


def page(L):
    _ = lambda *a: a[L]
    a = lambda u, t: f'<a href="{u}">{t}</a>'

    def fact(t, k, c, s):
        lab = LAB[L]
        return f"<br><b>{lab[0]}</b> {t[L]} <b>{lab[1]}</b> {k[L]} <b>{lab[2]}</b> {c[L]} <b>{lab[3]}</b> {s[L]}"

    KR = a("../kosher-restaurants-lyon/", _("Kosher in Lyon", "Casher à Lyon", "Kosher en Lyon", "אוכל כשר בליון"))
    SHAB_ALL = ("open on Saturday; we visit Sunday to Friday.", "ouvert le samedi ; nous visitons du dimanche au vendredi.",
                "abierto el sábado; visitamos de domingo a viernes.", "פתוח בשבת; אנחנו מבקרים מיום ראשון עד יום שישי.")

    vieux = (f"<li><b>{_('Vieux Lyon: a walk through the traboules.', 'Le Vieux Lyon : une promenade dans les traboules.', 'Vieux Lyon: un paseo por las traboules.', 'ליון העתיקה (Vieux Lyon): הליכה בין הטרבולים (traboules).')}</b> "
             + _("A Renaissance quarter between the Saône and the hill, listed by UNESCO in 1998. Walk rue Saint-Jean and rue du Bœuf, then " + a("../rue-juiverie-lyon/", "rue Juiverie") + ", the street that kept the name of the medieval Jewish community. Traboules are covered passages that cut through the buildings from one street to the next. Some stay open in the daytime; a closed door belongs to the residents, so leave it.",
                 "Un quartier Renaissance entre la Saône et la colline, classé à l’UNESCO en 1998. Remontez la rue Saint-Jean et la rue du Bœuf, puis la " + a("../rue-juiverie-lyon/", "rue Juiverie") + ", la rue qui a gardé le nom de la communauté juive du Moyen Âge. Les traboules sont des passages couverts qui traversent les immeubles d’une rue à l’autre. Certaines restent ouvertes en journée ; une porte fermée appartient aux habitants, on la laisse.",
                 "Un barrio renacentista entre el Saona y la colina, declarado por la UNESCO en 1998. Recorra la rue Saint-Jean y la rue du Bœuf, y después la " + a("../rue-juiverie-lyon/", "rue Juiverie") + ", la calle que conservó el nombre de la comunidad judía medieval. Las traboules son pasajes cubiertos que atraviesan los edificios de una calle a otra. Algunas permanecen abiertas de día; una puerta cerrada pertenece a los vecinos, y se respeta.",
                 "רובע מימי הרנסנס בין הסון לגבעה, שנכלל ברשימת אונסק״ו ב-1998. הולכים ברחוב סנט-ז'אן (rue Saint-Jean) וברחוב דו בף (rue du Bœuf), ואחר כך ברחוב " + a("../rue-juiverie-lyon/", "ז'ויברי (rue Juiverie)") + ", הרחוב ששמר על שם הקהילה היהודית של ימי הביניים. הטרבולים הם מעברים מקורים שחוצים את הבניינים מרחוב לרחוב. חלקם פתוחים ביום; דלת סגורה שייכת לדיירים, ולכן משאירים אותה.")
             + fact(("2 to 3 hours.", "2 à 3 heures.", "2 a 3 horas.", "שעתיים עד שלוש."),
                    ("yes, the passages are a game for them; the cobbles are hard on strollers.", "oui, les passages les amusent ; les pavés sont durs pour les poussettes.", "sí, los pasajes les divierten; los adoquines son duros para los cochecitos.", "כן, המעברים הם משחק בשבילם; האבנים קשות לעגלות."),
                    ("restaurants of the Presqu’île and the 2nd arrondissement, 10 minutes on foot. See " + KR + ".", "restaurants de la Presqu’île et du 2e arrondissement, à 10 minutes à pied. Voir " + KR + ".", "restaurantes de la Presqu’île y del 2.º distrito, a 10 minutos a pie. Vea " + KR + ".", "מסעדות הפרסקיל (Presqu'île) והרובע ה-2, כ-10 דקות הליכה. ראו " + KR + "."),
                    ("the streets are always open; we guide Sunday to Friday.", "les rues sont toujours ouvertes ; nous guidons du dimanche au vendredi.", "las calles están siempre abiertas; guiamos de domingo a viernes.", "הרחובות פתוחים תמיד; אנחנו מדריכים מיום ראשון עד יום שישי."))
             + "</li>")
    fourviere = (f"<li><b>{_('Fourvière: two thousand years of Roman history.', 'Fourvière : deux mille ans d’histoire romaine.', 'Fourvière: dos mil años de historia romana.', 'פורבייר (Fourvière): אלפיים שנות היסטוריה רומית.')}</b> "
                 + _("The Roman theatres sit on the hill above Vieux Lyon, on the site of Lugdunum, the capital of the Gauls. The Grand Théâtre dates from about 15 BC and the open-air site is free to enter. Take the F2 funicular from Vieux Lyon to the Minimes-Théâtres romains station. The Lugdunum museum next door is open Tuesday to Sunday.",
                     "Les théâtres romains dominent le Vieux Lyon, sur le site de Lugdunum, capitale des Gaules. Le Grand Théâtre date d’environ 15 av. J.-C. et le site de plein air est en accès libre. Prenez le funiculaire F2 depuis le Vieux Lyon jusqu’à la station Minimes-Théâtres romains. Le musée Lugdunum, juste à côté, est ouvert du mardi au dimanche.",
                     "Los teatros romanos se alzan en la colina sobre Vieux Lyon, en el sitio de Lugdunum, capital de las Galias. El Gran Teatro data de hacia el 15 a. C. y la entrada al recinto al aire libre es gratuita. Tome el funicular F2 desde Vieux Lyon hasta la estación Minimes-Théâtres romains. El museo Lugdunum, justo al lado, abre de martes a domingo.",
                     "התיאטראות הרומיים נמצאים על הגבעה שמעל ליון העתיקה, במקום שבו שכנה לוגדונום (Lugdunum), בירת גאליה. התיאטרון הגדול (Grand Théâtre) נבנה בסביבות 15 לפני הספירה, והכניסה לאתר הפתוח חופשית. עולים ברכבל ההרים F2 מליון העתיקה לתחנת Minimes-Théâtres romains. מוזיאון לוגדונום הסמוך פתוח מיום שלישי עד יום ראשון.")
                 + fact(("1 to 2 hours.", "1 à 2 heures.", "1 a 2 horas.", "שעה עד שעתיים."),
                        ("yes, they climb the tiers; the hill is steep, so take the funicular.", "oui, ils grimpent les gradins ; la colline est raide, prenez le funiculaire.", "sí, suben por las gradas; la colina es empinada, tome el funicular.", "כן, הם מטפסים על המדרגות; הגבעה תלולה, ולכן עולים ברכבל."),
                        ("none on the hill; eat in the 2nd arrondissement before you climb. See " + KR + ".", "aucun sur la colline ; mangez dans le 2e arrondissement avant de monter. Voir " + KR + ".", "ninguno en la colina; coma en el 2.º distrito antes de subir. Vea " + KR + ".", "אין בגבעה; אוכלים ברובע ה-2 לפני העלייה. ראו " + KR + "."),
                        ("free access every day, 7:00 to 21:00 from 15 April to 15 September and to 19:00 the rest of the year; we guide Sunday to Friday.", "accès libre tous les jours, de 7 h à 21 h du 15 avril au 15 septembre et jusqu’à 19 h le reste de l’année ; nous guidons du dimanche au vendredi.", "acceso libre todos los días, de 7:00 a 21:00 del 15 de abril al 15 de septiembre y hasta las 19:00 el resto del año; guiamos de domingo a viernes.", "כניסה חופשית בכל יום, 7:00 עד 21:00 מ-15 באפריל עד 15 בספטמבר, ועד 19:00 בשאר השנה; אנחנו מדריכים מיום ראשון עד יום שישי."))
                 + "</li>")
    croix = (f"<li><b>{_('Croix-Rousse: a walk up to the silk weavers’ wall.', 'La Croix-Rousse : une montée jusqu’au mur des canuts.', 'La Croix-Rousse: un paseo hasta el muro de los canuts.', 'קרואה-רוס (Croix-Rousse): הליכה אל קיר האורגים.')}</b> "
             + _("The hill of the canuts, the silk weavers. The Mur des Canuts, on boulevard des Canuts, is a trompe-l’œil painted over 1,200 m² that shows the neighbourhood as it lived. Take metro line C to Croix-Rousse instead of climbing the slopes. Rue Sainte-Catherine, where our " + a("../tours/jewish-lyon/", "Jewish Lyon tour") + " ends, runs down the same hill.",
                 "La colline des canuts, les ouvriers de la soie. Le Mur des Canuts, boulevard des Canuts, est un trompe-l’œil peint sur 1 200 m² qui montre le quartier tel qu’il vivait. Prenez le métro ligne C jusqu’à Croix-Rousse plutôt que de grimper les pentes. La rue Sainte-Catherine, où se termine notre " + a("../tours/jewish-lyon/", "visite du quartier juif de Lyon") + ", descend la même colline.",
                 "La colina de los canuts, los tejedores de seda. El Mur des Canuts, en el boulevard des Canuts, es un trampantojo pintado sobre 1200 m² que muestra el barrio tal como vivía. Tome la línea C del metro hasta Croix-Rousse en lugar de subir las cuestas. La rue Sainte-Catherine, donde termina nuestra " + a("../tours/jewish-lyon/", "visita del Lyon judío") + ", baja por la misma colina.",
                 "גבעת הקאנו (canuts), אורגי המשי. קיר הקאנו (Mur des Canuts) בשדרות des Canuts הוא ציור מטעה עין על פני 1,200 מ״ר שמראה את השכונה כפי שחיה. מגיעים ברכבת התחתית קו C לתחנת Croix-Rousse במקום לטפס במדרונות. רחוב סנט-קתרין (rue Sainte-Catherine), שבו מסתיים " + a("../tours/jewish-lyon/", "הסיור שלנו בליון היהודית") + ", יורד באותה גבעה.")
             + fact(("1 to 2 hours.", "1 à 2 heures.", "1 a 2 horas.", "שעה עד שעתיים."),
                    ("yes, with the metro for the climb.", "oui, avec le métro pour la montée.", "sí, con el metro para la subida.", "כן, עם הרכבת התחתית לעלייה."),
                    ("down the hill, on the Presqu’île. See " + KR + ".", "en bas de la colline, sur la Presqu’île. Voir " + KR + ".", "al pie de la colina, en la Presqu’île. Vea " + KR + ".", "למרגלות הגבעה, בפרסקיל. ראו " + KR + "."),
                    ("the wall is outdoors and always visible; we guide Sunday to Friday.", "le mur est en plein air et toujours visible ; nous guidons du dimanche au vendredi.", "el muro está al aire libre y siempre visible; guiamos de domingo a viernes.", "הקיר נמצא בחוץ ונראה תמיד; אנחנו מדריכים מיום ראשון עד יום שישי."))
             + "</li>")

    tete = (f"<li><b>{_('Parc de la Tête d’Or: a lake, a free zoo, rose gardens.', 'Parc de la Tête d’Or : un lac, un zoo gratuit, des roseraies.', 'Parque de la Tête d’Or: un lago, un zoo gratuito, rosaledas.', 'פארק טט ד’אור (Parc de la Tête d’Or): אגם, גן חיות חינם, גני ורדים.')}</b> "
            + _("The best place in Lyon for children. The park covers 105 hectares and is free. The zoo is free too, as are the three rose gardens and the botanical garden. Boats and pedal boats go out on the lake when the weather allows.",
                "Le meilleur endroit de Lyon pour les enfants. Le parc couvre 105 hectares et son entrée est gratuite. Le zoo l’est aussi, comme les trois roseraies et le jardin botanique. Barques et pédalos sortent sur le lac quand le temps le permet.",
                "El mejor lugar de Lyon para los niños. El parque ocupa 105 hectáreas y es gratuito. El zoo también lo es, igual que las tres rosaledas y el jardín botánico. Barcas y pedales salen al lago cuando el tiempo lo permite.",
                "המקום הטוב ביותר בליון לילדים. הפארק משתרע על 105 הקטרים והכניסה חופשית. גם גן החיות חינם, וכך גם שלושת גני הוורדים והגן הבוטני. סירות וסירות פדלים יוצאות לאגם כשמזג האוויר מאפשר.")
            + fact(("3 hours or half a day.", "3 heures ou une demi-journée.", "3 horas o media jornada.", "שלוש שעות או חצי יום."),
                   ("yes, the first choice.", "oui, le premier choix.", "sí, la primera opción.", "כן, הבחירה הראשונה."),
                   ("the 6th arrondissement borders the park. See " + KR + ".", "le 6e arrondissement borde le parc. Voir " + KR + ".", "el 6.º distrito linda con el parque. Vea " + KR + ".", "הרובע ה-6 גובל בפארק. ראו " + KR + "."),
                   ("the park is open every day, 6:30 to 20:30 (to 22:30 from 15 April to 14 October). The zoo opens 9:30 to 17:00 (17:45 in summer) and closes on Tuesday, so plan another day.", "le parc est ouvert tous les jours, de 6 h 30 à 20 h 30 (jusqu’à 22 h 30 du 15 avril au 14 octobre). Le zoo ouvre de 9 h 30 à 17 h (17 h 45 l’été) et ferme le mardi : prévoyez un autre jour.", "el parque abre todos los días, de 6:30 a 20:30 (hasta las 22:30 del 15 de abril al 14 de octubre). El zoo abre de 9:30 a 17:00 (17:45 en verano) y cierra el martes, así que elija otro día.", "הפארק פתוח בכל יום, 6:30 עד 20:30 (עד 22:30 מ-15 באפריל עד 14 באוקטובר). גן החיות פתוח 9:30 עד 17:00 (17:45 בקיץ) וסגור ביום שלישי, ולכן בוחרים יום אחר."))
            + "</li>")
    presq = (f"<li><b>{_('Presqu’île and Place Bellecour: a walk between two rivers.', 'La Presqu’île et la place Bellecour : une promenade entre deux fleuves.', 'La Presqu’île y la place Bellecour: un paseo entre dos ríos.', 'הפרסקיל (Presqu’île) וכיכר בלקור (Place Bellecour): הליכה בין שני נהרות.')}</b> "
             + _("The peninsula between the Rhône and the Saône. Place Bellecour, one of the largest open squares in Europe, has Louis XIV on horseback at its centre. Walk north along rue de la République to place des Terreaux and the town hall.",
                 "La presqu’île entre le Rhône et la Saône. La place Bellecour, l’une des plus grandes places d’Europe, a Louis XIV à cheval en son centre. Remontez la rue de la République jusqu’à la place des Terreaux et l’hôtel de ville.",
                 "La península entre el Ródano y el Saona. La place Bellecour, una de las plazas abiertas más grandes de Europa, tiene en el centro a Luis XIV a caballo. Siga hacia el norte por la rue de la République hasta la place des Terreaux y el ayuntamiento.",
                 "הלשון שבין הרון לסון. כיכר בלקור היא אחת הכיכרות הפתוחות הגדולות באירופה, ובמרכזה לואי ה-14 רכוב על סוס. הולכים צפונה ברחוב de la République עד כיכר Terreaux ועיריית ליון.")
             + fact(("2 hours.", "2 heures.", "2 horas.", "שעתיים."),
                    ("yes, there is room to run.", "oui, il y a de la place pour courir.", "sí, hay sitio para correr.", "כן, יש מקום לרוץ."),
                    ("the restaurants of the 2nd arrondissement are a few minutes away. See " + KR + ".", "les restaurants du 2e arrondissement sont à quelques minutes. Voir " + KR + ".", "los restaurantes del 2.º distrito están a pocos minutos. Vea " + KR + ".", "המסעדות של הרובע ה-2 במרחק כמה דקות. ראו " + KR + "."),
                    ("the square is always open; most shops close on Sunday, so Sunday suits squares and quays better than shopping.", "la place est toujours ouverte ; la plupart des boutiques ferment le dimanche, le dimanche convient donc mieux aux places et aux quais qu’aux achats.", "la plaza está siempre abierta; la mayoría de las tiendas cierran el domingo, así que el domingo conviene más a plazas y muelles que a las compras.", "הכיכר פתוחה תמיד; רוב החנויות סגורות ביום ראשון, ולכן יום ראשון מתאים יותר לכיכרות ולגדות מאשר לקניות."))
             + "</li>")
    fresque = (f"<li><b>{_('Fresque des Lyonnais: thirty figures of local history.', 'La Fresque des Lyonnais : trente figures de l’histoire locale.', 'La Fresque des Lyonnais: treinta figuras de la historia local.', 'ציור הקיר של תושבי ליון (Fresque des Lyonnais): שלושים דמויות מההיסטוריה המקומית.')}</b> "
               + _("A painted wall of about 800 m² on the quai de la Pêcherie, at the corner of rue de la Martinière, with around thirty people from two thousand years of Lyon’s history, from the Lumière brothers to Antoine de Saint-Exupéry. Children play spot the person.",
                   "Un mur peint d’environ 800 m² sur le quai de la Pêcherie, à l’angle de la rue de la Martinière, avec une trentaine de personnages de deux mille ans d’histoire lyonnaise, des frères Lumière à Antoine de Saint-Exupéry. Les enfants jouent à retrouver chaque personnage.",
                   "Un muro pintado de unos 800 m² en el quai de la Pêcherie, en la esquina de la rue de la Martinière, con una treintena de personajes de dos mil años de historia de Lyon, de los hermanos Lumière a Antoine de Saint-Exupéry. Los niños juegan a encontrar a cada personaje.",
                   "קיר צבוע בשטח של כ-800 מ״ר ברציף de la Pêcherie, בפינת רחוב de la Martinière, עם כשלושים דמויות מאלפיים שנות היסטוריה של ליון, מהאחים לומייר ועד אנטואן דה סנט-אכזופרי. הילדים משחקים באיתור הדמויות.")
               + fact(("20 minutes.", "20 minutes.", "20 minutos.", "עשרים דקות."),
                      ("yes.", "oui.", "sí.", "כן."),
                      ("the Presqu’île, near Vieux Lyon. See " + KR + ".", "la Presqu’île, près du Vieux Lyon. Voir " + KR + ".", "la Presqu’île, cerca de Vieux Lyon. Vea " + KR + ".", "הפרסקיל, ליד ליון העתיקה. ראו " + KR + "."),
                      ("outdoors and always open; we guide Sunday to Friday.", "en plein air et toujours ouverte ; nous guidons du dimanche au vendredi.", "al aire libre y siempre abierta; guiamos de domingo a viernes.", "בחוץ ופתוח תמיד; אנחנו מדריכים מיום ראשון עד יום שישי."))
               + "</li>")
    quais = (f"<li><b>{_('The quays: an hour by bike along two rivers.', 'Les quais : une heure à vélo le long de deux fleuves.', 'Los muelles: una hora en bici junto a dos ríos.', 'הגדות: שעה באופניים לאורך שני נהרות.')}</b> "
             + _("Both rivers have riverside paths away from the traffic. The Rhône banks are wide, with lawns and flat paths; the Saône quays are quieter and face Vieux Lyon. Vélo’v self-service bikes stand in stations along both. Walk instead if you prefer.",
                 "Les deux fleuves ont des berges aménagées à l’écart de la circulation. Les berges du Rhône sont larges, avec des pelouses et des allées plates ; les quais de la Saône sont plus calmes et font face au Vieux Lyon. Des Vélo’v en libre-service sont installés le long des deux. Marchez plutôt si vous préférez.",
                 "Los dos ríos tienen caminos de ribera alejados del tráfico. Las orillas del Ródano son anchas, con césped y caminos llanos; los muelles del Saona son más tranquilos y miran a Vieux Lyon. Hay bicicletas Vélo’v de autoservicio en estaciones a lo largo de ambos. Si prefiere, vaya a pie.",
                 "בשני הנהרות יש שבילי גדה הרחוקים מהתנועה. גדות הרון רחבות, עם מדשאות ושבילים ישרים; רציפי הסון שקטים יותר ופונים אל ליון העתיקה. אופני שיתוף Vélo’v עומדים בתחנות לאורך שניהם. אם מעדיפים, הולכים ברגל.")
             + fact(("1 to 2 hours.", "1 à 2 heures.", "1 a 2 horas.", "שעה עד שעתיים."),
                    ("yes, the Rhône banks are flat and away from cars.", "oui, les berges du Rhône sont plates et loin des voitures.", "sí, las orillas del Ródano son llanas y están lejos de los coches.", "כן, גדות הרון שטוחות ורחוקות ממכוניות."),
                    ("both banks reach the Presqu’île. See " + KR + ".", "les deux rives rejoignent la Presqu’île. Voir " + KR + ".", "las dos orillas llegan a la Presqu’île. Vea " + KR + ".", "שתי הגדות מגיעות לפרסקיל. ראו " + KR + "."),
                    ("the paths are always open; we do not ride on Shabbat, a walk on the banks suits Friday afternoon.", "les berges sont toujours ouvertes ; nous ne roulons pas le Shabbat, une promenade à pied convient au vendredi après-midi.", "los caminos están siempre abiertos; no montamos en bici en Shabat, un paseo a pie conviene al viernes por la tarde.", "השבילים פתוחים תמיד; אנחנו לא רוכבים בשבת, וטיול רגלי על הגדות מתאים לשישי אחר הצהריים."))
             + "</li>")
    partdieu = (f"<li><b>{_('Part-Dieu: the shopping centre.', 'La Part-Dieu : le centre commercial.', 'La Part-Dieu: el centro comercial.', 'פר-דייה (Part-Dieu): הקניון.')}</b> "
                + _("Lyon’s main shopping centre, around the station in the 3rd arrondissement: clothes, shoes, chargers and everything you forgot. Shops open Monday to Saturday from 9:30 to 20:00, and on some Sundays. A certified kosher grocery for Shabbat shopping lies in the same arrondissement.",
                    "Le principal centre commercial de Lyon, autour de la gare dans le 3e arrondissement : vêtements, chaussures, chargeurs et tout ce que vous avez oublié. Les boutiques ouvrent du lundi au samedi de 9 h 30 à 20 h, et certains dimanches. Une épicerie casher certifiée pour les courses de Shabbat se trouve dans le même arrondissement.",
                    "El principal centro comercial de Lyon, alrededor de la estación en el 3.er distrito: ropa, calzado, cargadores y todo lo que olvidó. Las tiendas abren de lunes a sábado de 9:30 a 20:00, y algunos domingos. En el mismo distrito hay una tienda de alimentación kosher certificada para las compras de Shabat.",
                    "הקניון הראשי של ליון, סביב התחנה ברובע ה-3: בגדים, נעליים, מטענים וכל מה ששכחתם. החנויות פתוחות מיום שני עד שבת מ-9:30 עד 20:00, ובחלק מימי ראשון. מכולת כשרה בהשגחה לקניות השבת נמצאת באותו רובע.")
                + fact(("1 to 2 hours.", "1 à 2 heures.", "1 a 2 horas.", "שעה עד שעתיים."),
                       ("yes, it is a mall.", "oui, c’est un centre commercial.", "sí, es un centro comercial.", "כן, זה קניון."),
                       ("order your Shabbat food before Thursday. See " + KR + ".", "commandez vos repas de Shabbat avant jeudi. Voir " + KR + ".", "encargue sus comidas de Shabat antes del jueves. Vea " + KR + ".", "מזמינים את אוכל השבת לפני יום חמישי. ראו " + KR + "."),
                       ("shops open on Saturday; we shop Sunday to Friday.", "les boutiques ouvrent le samedi ; nous faisons les courses du dimanche au vendredi.", "las tiendas abren el sábado; compramos de domingo a viernes.", "החנויות פתוחות בשבת; אנחנו קונים מיום ראשון עד יום שישי."))
                + "</li>")

    conf = (f"<li><b>{_('Confluences museum: science and societies.', 'Le musée des Confluences : sciences et sociétés.', 'Museo de las Confluences: ciencias y sociedades.', 'מוזיאון קונפלואנס (Musée des Confluences): מדעים וחברות אנושיות.')}</b> "
            + _("A glass and steel building at the southern tip of the Presqu’île, where the Rhône and the Saône meet, at 86 quai Perrache. Natural sciences and human societies, with temporary exhibitions.",
                "Un bâtiment de verre et d’acier à la pointe sud de la Presqu’île, là où le Rhône et la Saône se rejoignent, au 86 quai Perrache. Sciences naturelles et sociétés humaines, avec des expositions temporaires.",
                "Un edificio de vidrio y acero en el extremo sur de la Presqu’île, donde se unen el Ródano y el Saona, en el 86 quai Perrache. Ciencias naturales y sociedades humanas, con exposiciones temporales.",
                "מבנה זכוכית ופלדה בקצה הדרומי של הפרסקיל, במקום שבו הרון והסון נפגשים, ב-86 quai Perrache. מדעי הטבע וחברות אנושיות, עם תערוכות מתחלפות.")
            + fact(("2 to 3 hours.", "2 à 3 heures.", "2 a 3 horas.", "שעתיים עד שלוש."),
                   ("yes; choose a few galleries rather than the whole museum.", "oui ; choisissez quelques salles plutôt que tout le musée.", "sí; elija unas pocas salas en lugar de todo el museo.", "כן; בוחרים כמה אולמות במקום את כל המוזיאון."),
                   ("eat in the 2nd arrondissement before or after; the museum is about 2.5 km south of Bellecour. See " + KR + ".", "mangez dans le 2e arrondissement avant ou après ; le musée est à environ 2,5 km au sud de Bellecour. Voir " + KR + ".", "coma en el 2.º distrito antes o después; el museo está a unos 2,5 km al sur de Bellecour. Vea " + KR + ".", "אוכלים ברובע ה-2 לפני או אחרי; המוזיאון נמצא כ-2.5 ק״מ דרומית לבלקור. ראו " + KR + "."),
                   ("open Tuesday to Sunday, 10:30 to 18:30 (also Monday in zone A school holidays outside summer). We visit on Tuesday to Friday or Sunday.", "ouvert du mardi au dimanche, de 10 h 30 à 18 h 30 (aussi le lundi pendant les vacances scolaires de la zone A hors été). Nous visitons du mardi au vendredi ou le dimanche.", "abierto de martes a domingo, de 10:30 a 18:30 (también el lunes en las vacaciones escolares de la zona A fuera del verano). Visitamos de martes a viernes o el domingo.", "פתוח מיום שלישי עד יום ראשון, 10:30 עד 18:30 (גם ביום שני בחופשות בית הספר של אזור A מחוץ לקיץ). אנחנו מבקרים מיום שלישי עד שישי או ביום ראשון."))
            + "</li>")
    lumiere = (f"<li><b>{_('Institut Lumière: the family villa and the first film.', 'L’Institut Lumière : la villa de famille et le premier film.', 'El Institut Lumière: la villa familiar y la primera película.', 'מכון לומייר (Institut Lumière): וילת המשפחה והסרט הראשון.')}</b> "
               + _("The birthplace of cinema, at 25 rue du Premier-Film in the 8th arrondissement: the Lumière family villa and the site of the factory where the brothers shot one of the first films in 1895.",
                   "Le berceau du cinéma, au 25 rue du Premier-Film dans le 8e arrondissement : la villa de la famille Lumière et le site de l’usine où les frères ont tourné l’un des premiers films en 1895.",
                   "La cuna del cine, en el 25 rue du Premier-Film, en el 8.º distrito: la villa de la familia Lumière y el lugar de la fábrica donde los hermanos rodaron una de las primeras películas en 1895.",
                   "ערש הקולנוע, ב-25 rue du Premier-Film ברובע ה-8: וילת משפחת לומייר ואתר המפעל שבו צילמו האחים אחד הסרטים הראשונים ב-1895.")
               + fact(("1.5 to 2 hours.", "1 h 30 à 2 heures.", "1,5 a 2 horas.", "שעה וחצי עד שעתיים."),
                      ("from about eight.", "à partir d’environ huit ans.", "a partir de unos ocho años.", "מגיל שמונה בערך."),
                      ("eat before you go, in the 3rd or the 6th arrondissement; metro line D reaches Monplaisir-Lumière. See " + KR + ".", "mangez avant d’y aller, dans le 3e ou le 6e arrondissement ; le métro ligne D dessert Monplaisir-Lumière. Voir " + KR + ".", "coma antes de ir, en el 3.er o el 6.º distrito; la línea D del metro llega a Monplaisir-Lumière. Vea " + KR + ".", "אוכלים לפני ההגעה, ברובע ה-3 או ה-6; קו D של הרכבת התחתית מגיע לתחנת Monplaisir-Lumière. ראו " + KR + "."),
                      ("open Tuesday to Sunday, 10:00 to 18:30. We visit on Tuesday to Friday or Sunday.", "ouvert du mardi au dimanche, de 10 h à 18 h 30. Nous visitons du mardi au vendredi ou le dimanche.", "abierto de martes a domingo, de 10:00 a 18:30. Visitamos de martes a viernes o el domingo.", "פתוח מיום שלישי עד יום ראשון, 10:00 עד 18:30. אנחנו מבקרים מיום שלישי עד שישי או ביום ראשון."))
               + "</li>")
    beaux = (f"<li><b>{_('Musée des Beaux-Arts: a visit through 70 rooms.', 'Le musée des Beaux-Arts : une visite à travers 70 salles.', 'Museo de Bellas Artes: una visita por 70 salas.', 'המוזיאון לאמנויות יפות (Musée des Beaux-Arts): ביקור בין 70 אולמות.')}</b> "
             + _("Art from antiquity to today in 70 rooms and 7,000 m², at 20 place des Terreaux, with a sculpture garden.",
                 "L’art de l’Antiquité à aujourd’hui dans 70 salles et 7 000 m², au 20 place des Terreaux, avec un jardin de sculptures.",
                 "Arte de la Antigüedad a hoy en 70 salas y 7000 m², en el 20 place des Terreaux, con un jardín de esculturas.",
                 "אמנות מהעת העתיקה ועד היום ב-70 אולמות ו-7,000 מ״ר, ב-20 place des Terreaux, עם גן פסלים.")
             + fact(("2 hours.", "2 heures.", "2 horas.", "שעתיים."),
                    ("from about ten, with a short route chosen in advance.", "à partir d’environ dix ans, avec un court parcours choisi à l’avance.", "a partir de unos diez años, con un recorrido corto elegido de antemano.", "מגיל עשר בערך, עם מסלול קצר שנבחר מראש."),
                    ("the Presqu’île, a few minutes away. See " + KR + ".", "la Presqu’île, à quelques minutes. Voir " + KR + ".", "la Presqu’île, a pocos minutos. Vea " + KR + ".", "הפרסקיל, במרחק כמה דקות. ראו " + KR + "."),
                    ("open Wednesday to Monday, 10:00 to 18:00 (10:30 on Friday), closed on Tuesday. We visit on any other day, Sunday to Friday.", "ouvert du mercredi au lundi, de 10 h à 18 h (10 h 30 le vendredi), fermé le mardi. Nous visitons tous les autres jours, du dimanche au vendredi.", "abierto de miércoles a lunes, de 10:00 a 18:00 (10:30 el viernes), cerrado el martes. Visitamos cualquier otro día, de domingo a viernes.", "פתוח מיום רביעי עד יום שני, 10:00 עד 18:00 (10:30 ביום שישי), סגור ביום שלישי. אנחנו מבקרים בכל יום אחר, מיום ראשון עד שישי."))
             + "</li>")

    synag = (f"<li><b>{_('Grande Synagogue: the building we take you inside.', 'La Grande Synagogue : le bâtiment où nous vous faisons entrer.', 'La Gran Sinagoga: el edificio al que le llevamos dentro.', 'בית הכנסת הגדול (Grande Synagogue): המבנה שאנחנו מכניסים אתכם אליו.')}</b> "
             + _("Inaugurated in 1864 at 13 quai Tilsitt, it is still a working synagogue and is closed to visitors outside the Heritage Days. Mishpacha Tours holds the special authorisation and takes private groups inside on its 2 h 30 " + a("../tours/jewish-lyon/", "Jewish Lyon tour") + ", subject to opening hours and security on the day. It is the one visit on this page that you cannot make alone. " + a("../grande-synagogue-lyon/", "The Grande Synagogue, in detail") + ".",
                 "Inaugurée en 1864 au 13 quai Tilsitt, elle reste une synagogue en activité et est fermée aux visiteurs hors Journées du patrimoine. Mishpacha Tours détient l’autorisation spéciale et fait entrer des groupes privés lors de sa " + a("../tours/jewish-lyon/", "visite du quartier juif de Lyon") + " de 2 h 30, sous réserve des horaires et de la sécurité du jour. C’est la seule visite de cette page que vous ne pouvez pas faire seuls. " + a("../grande-synagogue-lyon/", "La Grande Synagogue, en détail") + ".",
                 "Inaugurada en 1864 en el 13 quai Tilsitt, sigue siendo una sinagoga en activo y está cerrada a los visitantes fuera de las Jornadas del Patrimonio. Mishpacha Tours posee la autorización especial y lleva a grupos privados al interior en su " + a("../tours/jewish-lyon/", "visita del Lyon judío") + " de 2 h 30, sujeta al horario y a la seguridad del día. Es la única visita de esta página que no puede hacer por su cuenta. " + a("../grande-synagogue-lyon/", "La Gran Sinagoga, en detalle") + ".",
                 "נחנך ב-1864 ב-13 quai Tilsitt, הוא בית כנסת פעיל וסגור למבקרים מחוץ לימי המורשת האירופיים. Mishpacha Tours מחזיקה באישור המיוחד ומכניסה קבוצות פרטיות פנימה ב" + a("../tours/jewish-lyon/", "סיור ליון היהודית") + " בן שעתיים וחצי, בכפוף לשעות הפתיחה ולאבטחה ביום עצמו. זה הביקור היחיד בדף הזה שאי אפשר לעשות לבד. " + a("../grande-synagogue-lyon/", "בית הכנסת הגדול, בפירוט") + ".")
             + fact(("2 h 30 with the tour.", "2 h 30 avec la visite.", "2 h 30 con la visita.", "שעתיים וחצי עם הסיור."),
                    ("from about eight.", "à partir d’environ huit ans.", "a partir de unos ocho años.", "מגיל שמונה בערך."),
                    ("the 2nd arrondissement, a short walk. See " + KR + ".", "le 2e arrondissement, à quelques pas. Voir " + KR + ".", "el 2.º distrito, a pocos pasos. Vea " + KR + ".", "הרובע ה-2, כמה צעדים משם. ראו " + KR + "."),
                    ("services are held, but visitors are not admitted; our visits run Sunday to Friday morning.", "des offices ont lieu, mais les visiteurs ne sont pas admis ; nos visites ont lieu du dimanche au vendredi matin.", "se celebran oficios, pero no se admiten visitantes; nuestras visitas son de domingo a viernes por la mañana.", "מתקיימות תפילות, אבל מבקרים אינם נכנסים; הסיורים שלנו מתקיימים מיום ראשון עד יום שישי בבוקר."))
             + "</li>")
    chrd = (f"<li><b>{_('CHRD: the memory museum.', 'Le CHRD : le musée de la mémoire.', 'El CHRD: el museo de la memoria.', 'CHRD: מוזיאון הזיכרון.')}</b> "
            + _("The Centre d’histoire de la résistance et de la déportation, at 14 avenue Berthelot, in the former Gestapo headquarters of Lyon. Our private visit follows the Jewish thread of the occupation: the raids, the deportations, the children of Izieu. " + a("../chrd-lyon/", "The CHRD, in detail") + ".",
                "Le Centre d’histoire de la résistance et de la déportation, au 14 avenue Berthelot, dans l’ancien siège de la Gestapo à Lyon. Notre visite privée suit le fil juif de l’Occupation : les rafles, les déportations, les enfants d’Izieu. " + a("../chrd-lyon/", "Le CHRD, en détail") + ".",
                "El Centre d’histoire de la résistance et de la déportation, en el 14 avenue Berthelot, en la antigua sede de la Gestapo en Lyon. Nuestra visita privada sigue el hilo judío de la ocupación: las redadas, las deportaciones, los niños de Izieu. " + a("../chrd-lyon/", "El CHRD, en detalle") + ".",
                "מרכז ההיסטוריה של ההתנגדות והגירוש (Centre d’histoire de la résistance et de la déportation) ב-14 avenue Berthelot, במטה הגסטאפו לשעבר בליון. הביקור הפרטי שלנו עוקב אחרי החוט היהודי של הכיבוש: הפשיטות, הגירושים, ילדי איזיה. " + a("../chrd-lyon/", "ה-CHRD, בפירוט") + ".")
            + fact(("2 h 30.", "2 h 30.", "2 h 30.", "שעתיים וחצי."),
                   ("teenagers; for younger ones, talk to us first.", "adolescents ; pour des plus jeunes, parlez-en d’abord avec nous.", "adolescentes; para los más pequeños, hable antes con nosotros.", "בני נוער; לצעירים יותר, מדברים איתנו קודם."),
                   ("the 6th or the 2nd arrondissement, by metro. See " + KR + ".", "le 6e ou le 2e arrondissement, en métro. Voir " + KR + ".", "el 6.º o el 2.º distrito, en metro. Vea " + KR + ".", "הרובע ה-6 או ה-2, ברכבת התחתית. ראו " + KR + "."),
                   ("open Wednesday to Sunday, 10:00 to 18:00, closed Monday and Tuesday. We visit on Wednesday to Friday or Sunday.", "ouvert du mercredi au dimanche, de 10 h à 18 h, fermé le lundi et le mardi. Nous visitons du mercredi au vendredi ou le dimanche.", "abierto de miércoles a domingo, de 10:00 a 18:00, cerrado lunes y martes. Visitamos de miércoles a viernes o el domingo.", "פתוח מיום רביעי עד יום ראשון, 10:00 עד 18:00, סגור בימים שני ושלישי. אנחנו מבקרים מיום רביעי עד שישי או ביום ראשון."))
            + "</li>")
    izieu = (f"<li><b>{_('Izieu: a full-day visit.', 'Izieu : une visite d’une journée.', 'Izieu: una visita de un día entero.', 'איזיה (Izieu): ביקור של יום שלם.')}</b> "
             + _("The Maison d’Izieu is the memorial to the 44 Jewish children arrested on 6 April 1944, one hour from Lyon by road. We spend the day there with a van and driver. The main access bridge is closed for works until November 2026, with a signed detour. " + a("../maison-izieu/", "The Maison d’Izieu, in detail") + ".",
                 "La Maison d’Izieu est le mémorial des 44 enfants juifs arrêtés le 6 avril 1944, à une heure de Lyon par la route. Nous y passons la journée avec un van et un chauffeur. Le pont d’accès principal est fermé pour travaux jusqu’en novembre 2026, avec une déviation fléchée. " + a("../maison-izieu/", "La Maison d’Izieu, en détail") + ".",
                 "La Maison d’Izieu es el memorial de los 44 niños judíos detenidos el 6 de abril de 1944, a una hora de Lyon por carretera. Pasamos allí el día con una furgoneta y chófer. El puente de acceso principal está cerrado por obras hasta noviembre de 2026, con un desvío señalizado. " + a("../maison-izieu/", "La Maison d’Izieu, en detalle") + ".",
                 "בית איזיה (Maison d’Izieu) הוא האנדרטה ל-44 הילדים היהודים שנעצרו ב-6 באפריל 1944, במרחק שעה מליון בכביש. אנחנו מבלים שם יום שלם עם ואן ונהג. גשר הגישה הראשי סגור לעבודות עד נובמבר 2026, עם מעקף מסומן. " + a("../maison-izieu/", "בית איזיה, בפירוט") + ".")
             + fact(("a full day.", "une journée entière.", "un día entero.", "יום שלם."),
                    ("from about eight, the memorial’s minimum age.", "à partir d’environ huit ans, l’âge minimum du mémorial.", "a partir de unos ocho años, la edad mínima del memorial.", "מגיל שמונה בערך, הגיל המינימלי של האנדרטה."),
                    ("bring your own kosher food; picnics are allowed in the orchard.", "apportez votre repas casher ; le pique-nique est autorisé dans le verger.", "lleve su comida kosher; se permite el picnic en el huerto.", "מביאים אוכל כשר מהבית; מותר פיקניק בפרדס."),
                    ("the memorial opens on Saturday from April to August; we visit Sunday to Friday.", "le mémorial ouvre le samedi d’avril à août ; nous visitons du dimanche au vendredi.", "el memorial abre el sábado de abril a agosto; visitamos de domingo a viernes.", "האנדרטה פתוחה בשבת מאפריל עד אוגוסט; אנחנו מבקרים מיום ראשון עד יום שישי."))
             + "</li>")

    MORE = ("Read more", "Lire la suite", "Leer más", "להמשך קריאה")
    # (resume visible 2 phrases, ligne de faits) par lieu, dans l'ordre de l'ecran
    CARDS = {
      "vieux": (("A UNESCO-listed Renaissance quarter between the Saône and the hill. Walk rue Saint-Jean, rue du Bœuf and rue Juiverie, and slip through the traboules.",
                 "Un quartier Renaissance classé à l’UNESCO entre la Saône et la colline. Remontez les rues Saint-Jean, du Bœuf et Juiverie, et glissez-vous dans les traboules.",
                 "Un barrio renacentista declarado por la UNESCO entre el Saona y la colina. Recorra la rue Saint-Jean, la rue du Bœuf y la rue Juiverie, y cuélese por las traboules.",
                 "רובע מימי הרנסנס שנכלל ברשימת אונסק״ו, בין הסון לגבעה. הולכים ברחובות סנט-ז'אן, דו בף וז'ויברי, ונכנסים לטרבולים."),
                ("2 to 3 hours", "2 à 3 heures", "2 a 3 horas", "שעתיים עד שלוש"), ("yes", "oui", "sí", "כן"), ("2nd arrondissement, 10 min", "2e arrondissement, 10 min", "2.º distrito, 10 min", "הרובע ה-2, 10 דקות"), ("open daily", "ouvert tous les jours", "abierto a diario", "פתוח כל יום")),
      "fourviere": (("The Roman theatres of Lugdunum, capital of the Gauls, stand on the hill above Vieux Lyon. The open-air site is free; take the F2 funicular.",
                     "Les théâtres romains de Lugdunum, capitale des Gaules, dominent le Vieux Lyon. Le site de plein air est gratuit ; prenez le funiculaire F2.",
                     "Los teatros romanos de Lugdunum, capital de las Galias, se alzan sobre Vieux Lyon. El recinto al aire libre es gratuito; tome el funicular F2.",
                     "התיאטראות הרומיים של לוגדונום, בירת גאליה, נמצאים על הגבעה שמעל ליון העתיקה. האתר הפתוח חינם; עולים ברכבל F2."),
                    ("1 to 2 hours", "1 à 2 heures", "1 a 2 horas", "שעה עד שעתיים"), ("yes", "oui", "sí", "כן"), ("none on the hill", "aucun sur la colline", "ninguno en la colina", "אין בגבעה"), ("open daily", "ouvert tous les jours", "abierto a diario", "פתוח כל יום")),
      "croix": (("The silk weavers’ hill and its 1,200 m² painted wall, the Mur des Canuts. Take metro line C instead of climbing.",
                 "La colline des canuts et son mur peint de 1 200 m², le Mur des Canuts. Prenez le métro C plutôt que de grimper.",
                 "La colina de los canuts y su muro pintado de 1200 m², el Mur des Canuts. Tome la línea C del metro en lugar de subir a pie.",
                 "גבעת האורגים וקיר הקאנו הצבוע בן 1,200 מ״ר. מגיעים בקו C של הרכבת התחתית במקום לטפס."),
                ("1 to 2 hours", "1 à 2 heures", "1 a 2 horas", "שעה עד שעתיים"), ("yes", "oui", "sí", "כן"), ("Presqu’île, below", "Presqu’île, en bas", "Presqu’île, abajo", "הפרסקיל, למטה"), ("always visible", "toujours visible", "siempre visible", "נראה תמיד")),
      "tete": (("Lyon’s best place for children: 105 free hectares, a free zoo, rose gardens and boats on the lake.",
                "Le meilleur endroit de Lyon pour les enfants : 105 hectares gratuits, un zoo gratuit, des roseraies et des barques sur le lac.",
                "El mejor lugar de Lyon para los niños: 105 hectáreas gratuitas, un zoo gratuito, rosaledas y barcas en el lago.",
                "המקום הטוב ביותר בליון לילדים: 105 הקטרים חינם, גן חיות חינם, גני ורדים וסירות באגם."),
               ("3 hours", "3 heures", "3 horas", "שלוש שעות"), ("yes", "oui", "sí", "כן"), ("6th arrondissement", "6e arrondissement", "6.º distrito", "הרובע ה-6"), ("zoo closed Tuesday", "zoo fermé le mardi", "zoo cerrado el martes", "גן החיות סגור ביום שלישי")),
      "presq": (("The peninsula between the Rhône and the Saône, from the vast Place Bellecour to place des Terreaux along rue de la République.",
                 "La presqu’île entre le Rhône et la Saône, de la vaste place Bellecour à la place des Terreaux par la rue de la République.",
                 "La península entre el Ródano y el Saona, de la enorme place Bellecour a la place des Terreaux por la rue de la République.",
                 "הלשון שבין הרון לסון, מכיכר בלקור הענקית עד כיכר Terreaux ברחוב de la République."),
                ("2 hours", "2 heures", "2 horas", "שעתיים"), ("yes", "oui", "sí", "כן"), ("2nd arrondissement", "2e arrondissement", "2.º distrito", "הרובע ה-2"), ("open daily", "ouvert tous les jours", "abierto a diario", "פתוח כל יום")),
      "fresque": (("An 800 m² painted wall with about thirty figures from Lyon’s history, from the Lumière brothers to Saint-Exupéry.",
                   "Un mur peint de 800 m² avec une trentaine de personnages de l’histoire de Lyon, des frères Lumière à Saint-Exupéry.",
                   "Un muro pintado de 800 m² con una treintena de personajes de la historia de Lyon, de los hermanos Lumière a Saint-Exupéry.",
                   "קיר צבוע בן 800 מ״ר עם כשלושים דמויות מההיסטוריה של ליון, מהאחים לומייר ועד סנט-אכזופרי."),
                  ("20 minutes", "20 minutes", "20 minutos", "עשרים דקות"), ("yes", "oui", "sí", "כן"), ("Presqu’île", "Presqu’île", "Presqu’île", "הפרסקיל"), ("always open", "toujours accessible", "siempre accesible", "פתוח תמיד")),
      "quais": (("Riverside paths away from traffic along both rivers, with Vélo’v self-service bikes. The Rhône banks are flat and wide.",
                 "Des berges aménagées à l’écart de la circulation le long des deux fleuves, avec des Vélo’v en libre-service. Les berges du Rhône sont plates et larges.",
                 "Caminos de ribera alejados del tráfico junto a los dos ríos, con bicicletas Vélo’v de autoservicio. Las orillas del Ródano son llanas y anchas.",
                 "שבילי גדה הרחוקים מהתנועה לאורך שני הנהרות, עם אופני שיתוף Vélo’v. גדות הרון שטוחות ורחבות."),
                ("1 to 2 hours", "1 à 2 heures", "1 a 2 horas", "שעה עד שעתיים"), ("yes", "oui", "sí", "כן"), ("Presqu’île", "Presqu’île", "Presqu’île", "הפרסקיל"), ("open daily", "ouvert tous les jours", "abierto a diario", "פתוח כל יום")),
      "partdieu": (("Lyon’s main shopping centre, for everything you forgot to pack. A certified kosher grocery sits in the same arrondissement.",
                    "Le principal centre commercial de Lyon, pour tout ce que vous avez oublié. Une épicerie casher certifiée se trouve dans le même arrondissement.",
                    "El principal centro comercial de Lyon, para todo lo que olvidó. En el mismo distrito hay una tienda kosher certificada.",
                    "הקניון הראשי של ליון, לכל מה ששכחתם. מכולת כשרה בהשגחה נמצאת באותו רובע."),
                   ("1 to 2 hours", "1 à 2 heures", "1 a 2 horas", "שעה עד שעתיים"), ("yes", "oui", "sí", "כן"), ("3rd arrondissement", "3e arrondissement", "3.er distrito", "הרובע ה-3"), ("shops Monday to Saturday", "boutiques du lundi au samedi", "tiendas de lunes a sábado", "חנויות מיום שני עד שבת")),
      "conf": (("A glass and steel museum of natural sciences and human societies, where the Rhône and the Saône meet.",
                "Un musée de verre et d’acier consacré aux sciences naturelles et aux sociétés humaines, là où le Rhône et la Saône se rejoignent.",
                "Un museo de vidrio y acero de ciencias naturales y sociedades humanas, donde se unen el Ródano y el Saona.",
                "מוזיאון זכוכית ופלדה למדעי הטבע ולחברות אנושיות, במקום שבו הרון והסון נפגשים."),
               ("2 to 3 hours", "2 à 3 heures", "2 a 3 horas", "שעתיים עד שלוש"), ("yes", "oui", "sí", "כן"), ("2nd arrondissement", "2e arrondissement", "2.º distrito", "הרובע ה-2"), ("closed Monday", "fermé le lundi", "cerrado el lunes", "סגור ביום שני")),
      "lumiere": (("The birthplace of cinema: the Lumière family villa and the factory site where one of the first films was shot in 1895.",
                   "Le berceau du cinéma : la villa de la famille Lumière et le site de l’usine où l’un des premiers films a été tourné en 1895.",
                   "La cuna del cine: la villa de la familia Lumière y el lugar de la fábrica donde se rodó una de las primeras películas en 1895.",
                   "ערש הקולנוע: וילת משפחת לומייר ואתר המפעל שבו צולם אחד הסרטים הראשונים ב-1895."),
                  ("1.5 to 2 hours", "1 h 30 à 2 heures", "1,5 a 2 horas", "שעה וחצי עד שעתיים"), ("from about 8", "dès 8 ans environ", "desde unos 8 años", "מגיל 8 בערך"), ("3rd or 6th arrondissement", "3e ou 6e arrondissement", "3.er o 6.º distrito", "הרובע ה-3 או ה-6"), ("closed Monday", "fermé le lundi", "cerrado el lunes", "סגור ביום שני")),
      "beaux": (("Art from antiquity to today in 70 rooms, with a sculpture garden, on place des Terreaux.",
                 "L’art de l’Antiquité à aujourd’hui dans 70 salles, avec un jardin de sculptures, place des Terreaux.",
                 "Arte de la Antigüedad a hoy en 70 salas, con un jardín de esculturas, en la place des Terreaux.",
                 "אמנות מהעת העתיקה ועד היום ב-70 אולמות, עם גן פסלים, בכיכר Terreaux."),
                ("2 hours", "2 heures", "2 horas", "שעתיים"), ("from about 10", "dès 10 ans environ", "desde unos 10 años", "מגיל 10 בערך"), ("Presqu’île", "Presqu’île", "Presqu’île", "הפרסקיל"), ("closed Tuesday", "fermé le mardi", "cerrado el martes", "סגור ביום שלישי")),
      "synag": (("Inaugurated in 1864 and closed to the public, it is the one building we take you inside, on our 2 h 30 Jewish Lyon tour, subject to opening hours and security.",
                 "Inaugurée en 1864 et fermée au public, c’est le seul bâtiment où nous vous faisons entrer, lors de notre visite du quartier juif de Lyon de 2 h 30, sous réserve des horaires et de la sécurité.",
                 "Inaugurada en 1864 y cerrada al público, es el único edificio al que le llevamos dentro, en nuestra visita del Lyon judío de 2 h 30, sujeta al horario y a la seguridad.",
                 "נחנך ב-1864 וסגור לציבור; זה המבנה היחיד שאנחנו מכניסים אתכם אליו, בסיור ליון היהודית בן שעתיים וחצי, בכפוף לשעות הפתיחה ולאבטחה."),
                ("2 h 30 with the tour", "2 h 30 avec la visite", "2 h 30 con la visita", "שעתיים וחצי עם הסיור"), ("from about 8", "dès 8 ans environ", "desde unos 8 años", "מגיל 8 בערך"), ("2nd arrondissement", "2e arrondissement", "2.º distrito", "הרובע ה-2"), ("no visitors on Shabbat", "pas de visiteurs le Shabbat", "sin visitantes en Shabat", "אין מבקרים בשבת")),
      "chrd": (("The resistance and deportation museum, in the former Gestapo headquarters. Our private visit follows the Jewish thread of the occupation.",
                "Le musée de la résistance et de la déportation, dans l’ancien siège de la Gestapo. Notre visite privée suit le fil juif de l’Occupation.",
                "El museo de la resistencia y la deportación, en la antigua sede de la Gestapo. Nuestra visita privada sigue el hilo judío de la ocupación.",
                "מוזיאון ההתנגדות והגירוש, במטה הגסטאפו לשעבר. הביקור הפרטי שלנו עוקב אחרי החוט היהודי של הכיבוש."),
               ("2 h 30", "2 h 30", "2 h 30", "שעתיים וחצי"), ("teenagers", "adolescents", "adolescentes", "בני נוער"), ("6th or 2nd arrondissement", "6e ou 2e arrondissement", "6.º o 2.º distrito", "הרובע ה-6 או ה-2"), ("closed Monday and Tuesday", "fermé lundi et mardi", "cerrado lunes y martes", "סגור בימים שני ושלישי")),
      "izieu": (("The memorial to the 44 Jewish children arrested on 6 April 1944, one hour from Lyon by road. We spend the day there with a van and driver.",
                 "Le mémorial des 44 enfants juifs arrêtés le 6 avril 1944, à une heure de Lyon par la route. Nous y passons la journée avec un van et un chauffeur.",
                 "El memorial de los 44 niños judíos detenidos el 6 de abril de 1944, a una hora de Lyon por carretera. Pasamos allí el día con furgoneta y chófer.",
                 "האנדרטה ל-44 הילדים היהודים שנעצרו ב-6 באפריל 1944, במרחק שעה מליון בכביש. אנחנו מבלים שם יום עם ואן ונהג."),
                ("a full day", "une journée", "un día entero", "יום שלם"), ("from about 8", "dès 8 ans environ", "desde unos 8 años", "מגיל 8 בערך"), ("bring your own food", "apportez votre repas", "lleve su comida", "מביאים אוכל מהבית"), ("check the memorial’s hours", "horaires du mémorial à vérifier", "compruebe el horario del memorial", "בודקים את שעות האנדרטה")),
    }

    def card(li, key):
        vis, t, k, c, o = CARDS[key]
        m = re.match(r"<li>(<b>.*?</b>) (.*)</li>$", li, re.S)
        always = o[0] in ("open daily", "always visible", "always open")
        ts = re.sub(r" (hours?|heures?|horas?)", " h", re.sub(r"(\d(?:[.,]\d)?) (?:to|à|a) (\d)", r"\1–\2", t[L]))
        cs = c[L].replace(" arrondissement", " arr.").replace(" distrito", " dist.")
        line = " · ".join([ts, LAB[L][1].rstrip(":") + " " + k[L], LAB[L][2].rstrip(":") + " " + cs] + ([] if always else [o[L]]))
        first = re.split(r"(?<=[.])\s", vis[L], maxsplit=1)[0]
        return f"<li>{m.group(1)} {first}<br>{line}<details class=\"rl\"><summary>{MORE[L]}</summary><p>{m.group(2)}</p></details></li>"

    vieux, fourviere, croix, tete, presq, fresque, quais, partdieu, conf, lumiere, beaux, synag, chrd, izieu = [
        card(x, k) for x, k in zip([vieux, fourviere, croix, tete, presq, fresque, quais, partdieu, conf, lumiere, beaux, synag, chrd, izieu],
                                   ["vieux", "fourviere", "croix", "tete", "presq", "fresque", "quais", "partdieu", "conf", "lumiere", "beaux", "synag", "chrd", "izieu"])]

    def sec(typ, h2, lis):
        return dict(type=typ, h2=h2, html="<ul>" + "".join(lis) + "</ul>")

    three = ("<p>"
             + f"<b>{_('A family with children: three days.', 'Une famille avec enfants : trois jours.', 'Una familia con niños: tres días.', 'משפחה עם ילדים: שלושה ימים.')}</b><br>"
             + _("Day 1: Vieux Lyon, then the Fresque and Place Bellecour.<br>Day 2: Tête d’Or, with a boat on the lake (not on Tuesday).<br>Day 3: Lumière or Confluences (not on Monday), then the quays.",
                 "Jour 1 : le Vieux Lyon, puis la Fresque et la place Bellecour.<br>Jour 2 : la Tête d’Or, avec une barque sur le lac (pas le mardi).<br>Jour 3 : Lumière ou Confluences (pas le lundi), puis les quais.",
                 "Día 1: Vieux Lyon, después la Fresque y la place Bellecour.<br>Día 2: la Tête d’Or, con una barca en el lago (no el martes).<br>Día 3: Lumière o Confluences (no el lunes), y después los muelles.",
                 "יום 1: ליון העתיקה, ואחר כך ציור הקיר וכיכר בלקור.<br>יום 2: טט ד’אור, עם סירה באגם (לא ביום שלישי).<br>יום 3: לומייר או קונפלואנס (לא ביום שני), ואחר כך הגדות.")
             + "<br><br>"
             + f"<b>{_('A couple: a slower walk, three days.', 'Un couple : une promenade plus lente, trois jours.', 'Una pareja: un paseo más lento, tres días.', 'זוג: הליכה איטית יותר, שלושה ימים.')}</b><br>"
             + _("Day 1: Vieux Lyon and rue Juiverie, then the Roman site.<br>Day 2: Croix-Rousse and the Mur des Canuts, then the Beaux-Arts.<br>Day 3: Grande Synagogue and CHRD with our guide, Wednesday to Friday.",
                 "Jour 1 : le Vieux Lyon et la rue Juiverie, puis le site romain.<br>Jour 2 : la Croix-Rousse et le Mur des Canuts, puis les Beaux-Arts.<br>Jour 3 : la Grande Synagogue et le CHRD avec notre guide, du mercredi au vendredi.",
                 "Día 1: Vieux Lyon y la rue Juiverie, después el sitio romano.<br>Día 2: la Croix-Rousse y el Mur des Canuts, después Bellas Artes.<br>Día 3: la Gran Sinagoga y el CHRD con nuestra guía, de miércoles a viernes.",
                 "יום 1: ליון העתיקה ורחוב ז’ויברי, ואחר כך האתר הרומי.<br>יום 2: קרואה-רוס וקיר הקאנו, ואחר כך המוזיאון לאמנויות יפות.<br>יום 3: בית הכנסת הגדול וה-CHRD עם המדריכה שלנו, מיום רביעי עד שישי.")
             + "<br><br>"
             + f"<b>{_('Passing through on the way to the Alps.', 'De passage vers les Alpes.', 'De paso hacia los Alpes.', 'בדרך לאלפים.')}</b><br>"
             + _("One day: our " + a("../tours/stopover/", "Stopover") + ", three hours with the Grande Synagogue and a kosher lunch.<br>Two days: add Vieux Lyon and Tête d’Or.<br>Then a " + a("../kosher-van-transfers/", "van") + " to " + a("../alps/", "the Alps") + ".",
                 "Un jour : notre " + a("../tours/stopover/", "Escale") + ", trois heures avec la Grande Synagogue et un déjeuner casher.<br>Deux jours : ajoutez le Vieux Lyon et la Tête d’Or.<br>Puis un " + a("../kosher-van-transfers/", "van") + " vers " + a("../alps/", "les Alpes") + ".",
                 "Un día: nuestra " + a("../tours/stopover/", "Escala") + ", tres horas con la Gran Sinagoga y un almuerzo kosher.<br>Dos días: añada Vieux Lyon y la Tête d’Or.<br>Después una " + a("../kosher-van-transfers/", "furgoneta") + " a " + a("../alps/", "los Alpes") + ".",
                 "יום אחד: " + a("../tours/stopover/", "עצירת הביניים") + " שלנו, שלוש שעות עם בית הכנסת הגדול וארוחת צהריים כשרה.<br>יומיים: מוסיפים את ליון העתיקה וטט ד’אור.<br>ואחר כך " + a("../kosher-van-transfers/", "ואן") + " אל " + a("../alps/", "האלפים") + ".")
             + "</p>")

    faq = [
        (_("How many days do I need in Lyon?", "Combien de jours faut-il à Lyon ?", "¿Cuántos días necesito en Lyon?", "כמה ימים צריך בליון?"),
         _("Two days cover Vieux Lyon, the Parc de la Tête d’Or and one museum. Three days add the Grande Synagogue and a Memory visit. Izieu takes a full day on top.",
           "Deux jours couvrent le Vieux Lyon, le parc de la Tête d’Or et un musée. Trois jours ajoutent la Grande Synagogue et une visite de mémoire. Izieu demande une journée entière en plus.",
           "Dos días cubren Vieux Lyon, el parque de la Tête d’Or y un museo. Tres días añaden la Gran Sinagoga y una visita de memoria. Izieu requiere un día entero más.",
           "יומיים מכסים את ליון העתיקה, פארק טט ד’אור ומוזיאון אחד. שלושה ימים מוסיפים את בית הכנסת הגדול וביקור זיכרון. איזיה לוקחת יום שלם נוסף.")),
        (_("What is free in Lyon?", "Qu’est-ce qui est gratuit à Lyon ?", "¿Qué es gratis en Lyon?", "מה חינם בליון?"),
         _("The Parc de la Tête d’Or with its zoo and rose gardens, the Roman site on Fourvière, the Mur des Canuts, the Fresque des Lyonnais, the quays and the traboules that stay open.",
           "Le parc de la Tête d’Or avec son zoo et ses roseraies, le site romain de Fourvière, le Mur des Canuts, la Fresque des Lyonnais, les quais et les traboules restées ouvertes.",
           "El parque de la Tête d’Or con su zoo y sus rosaledas, el sitio romano de Fourvière, el Mur des Canuts, la Fresque des Lyonnais, los muelles y las traboules que siguen abiertas.",
           "פארק טט ד’אור עם גן החיות וגני הוורדים, האתר הרומי בפורבייר, קיר הקאנו, ציור הקיר של תושבי ליון, הגדות והטרבולים שנשארים פתוחים.")),
        (_("What is open on Shabbat?", "Qu’est-ce qui est ouvert le Shabbat ?", "¿Qué está abierto en Shabat?", "מה פתוח בשבת?"),
         _("Parks, squares and quays are open every day, and the museums on this page open on Saturday. We guide Sunday to Friday.",
           "Les parcs, les places et les quais sont ouverts tous les jours, et les musées de cette page ouvrent le samedi. Nous guidons du dimanche au vendredi.",
           "Los parques, plazas y muelles están abiertos todos los días, y los museos de esta página abren el sábado. Guiamos de domingo a viernes.",
           "פארקים, כיכרות וגדות פתוחים בכל יום, והמוזיאונים בדף הזה פתוחים בשבת. אנחנו מדריכים מיום ראשון עד יום שישי.")),
        (_("What do we do if it rains?", "Que faire s’il pleut ?", "¿Qué hacemos si llueve?", "מה עושים אם יורד גשם?"),
         _("Go to the CHRD, the Confluences, the Beaux-Arts or the Institut Lumière, or walk the covered traboules of Vieux Lyon. The " + a("../lyon-weather/", "Lyon weather") + " page has the seven-day forecast and a plan for each kind of day.",
           "Allez au CHRD, aux Confluences, aux Beaux-Arts ou à l’Institut Lumière, ou parcourez les traboules couvertes du Vieux Lyon. La page " + a("../lyon-weather/", "météo à Lyon") + " donne les prévisions à sept jours et un programme pour chaque type de journée.",
           "Vaya al CHRD, a las Confluences, a Bellas Artes o al Institut Lumière, o recorra las traboules cubiertas de Vieux Lyon. La página " + a("../lyon-weather/", "el tiempo en Lyon") + " tiene la previsión a siete días y un plan para cada tipo de día.",
           "הולכים ל-CHRD, למוזיאון קונפלואנס, למוזיאון לאמנויות יפות או למכון לומייר, או עוברים בטרבולים המקורים של ליון העתיקה. בדף " + a("../lyon-weather/", "מזג האוויר בליון") + " יש תחזית לשבעה ימים ותוכנית לכל סוג של יום.")),
    ]

    return dict(
        slug="things-to-do-in-lyon",
        title=_("Things to do in Lyon for Jewish travellers", "Que faire à Lyon quand on est voyageur juif", "Qué hacer en Lyon como viajero judío", "מה לעשות בליון: מקומות למטייל יהודי שומר שבת"),
        desc=_("What to do in Lyon for a Jewish family that keeps Shabbat: fourteen places with time needed, children, kosher food nearby and Shabbat opening.",
               "Que faire à Lyon pour une famille juive qui garde le Shabbat : quatorze lieux, avec durée, enfants, casher à proximité et ouverture le Shabbat.",
               "Qué hacer en Lyon con una familia judía que guarda el Shabat: catorce lugares con duración, niños, comida kosher cerca y apertura en Shabat.",
               "מה לעשות בליון למשפחה יהודית ששומרת שבת: ארבעה עשר מקומות עם משך הביקור, ילדים, אוכל כשר בקרבת מקום ופתיחה בשבת."),
        h1=_("Things to do in Lyon", "Que faire à Lyon", "Qué hacer en Lyon", "מה לעשות בליון"),
        ital=_("for a Jewish family that keeps Shabbat", "pour une famille juive qui garde le Shabbat", "para una familia judía que guarda el Shabat", "למשפחה יהודית ששומרת שבת"),
        intro=_("Give Lyon two or three days: Vieux Lyon and its traboules first, the Parc de la Tête d’Or with children next, a museum for the rainy afternoon. Fourteen places below, each with the time it takes, whether it suits children, where kosher food is nearby and how it fits Shabbat. The Grande Synagogue is the one visit where we take you inside a building that is closed to the public.",
                "Accordez deux ou trois jours à Lyon : le Vieux Lyon et ses traboules d’abord, le parc de la Tête d’Or avec les enfants ensuite, un musée pour l’après-midi de pluie. Quatorze lieux ci-dessous, chacun avec sa durée, son intérêt pour les enfants, le casher à proximité et sa place dans le Shabbat. La Grande Synagogue est la seule visite où nous vous faisons entrer dans un bâtiment fermé au public.",
                "Dedique a Lyon dos o tres días: primero Vieux Lyon y sus traboules, después el parque de la Tête d’Or con los niños, y un museo para la tarde de lluvia. A continuación, catorce lugares, cada uno con su duración, si conviene a los niños, dónde hay comida kosher cerca y cómo encaja con el Shabat. La Gran Sinagoga es la única visita en la que le llevamos al interior de un edificio cerrado al público.",
                "מקצים לליון יומיים או שלושה: קודם ליון העתיקה והטרבולים שלה, אחר כך פארק טט ד’אור עם הילדים, ומוזיאון לאחר הצהריים הגשום. ארבעה עשר מקומות למטה, כל אחד עם משך הביקור, התאמה לילדים, אוכל כשר בקרבת מקום והשילוב עם השבת. בית הכנסת הגדול הוא הביקור היחיד שבו אנחנו מכניסים אתכם לתוך מבנה סגור לציבור."),
        chips=[],
        illus="flat-jewish-lyon.png",
        crumb=("../jewish-lyon-guide/", _("Jewish Lyon guide", "Guide juif de Lyon", "Guía del Lyon judío", "המדריך לליון היהודית")),
        sections=[
            dict(type="text", h2=_("How to read <i>this page</i>", "Comment lire <i>cette page</i>", "Cómo leer <i>esta página</i>", "איך קוראים <i>את הדף הזה</i>"),
                 html=_("<p>Each place shows time, children, kosher nearby and when it is closed; the rest is under Read more. We do not guide on Shabbat, so every plan runs Sunday to Friday. Hours were read on each venue’s website on 21 October 2026.</p><style>.rl{margin-top:6px}.rl summary{cursor:pointer;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:3px;min-height:32px}.rl p{margin-top:6px}@media(max-width:767px){body .dk-cartes>li{display:block!important;padding:12px 14px!important;min-height:0!important}body .dk-cartes>li>.dk-ico{position:static!important;float:inline-start;width:40px!important;height:40px!important;margin:0 12px 4px 0!important;margin-inline-end:12px!important;padding:0!important}body .dk-cartes>li>b{font-size:17px}}</style>",
                        "<p>Chaque lieu indique la durée, les enfants, le casher à proximité et le jour de fermeture ; le reste est sous « Lire la suite ». Nous ne guidons pas le Shabbat : chaque plan va du dimanche au vendredi. Horaires lus sur le site de chaque lieu le 21 octobre 2026.</p><style>.rl{margin-top:6px}.rl summary{cursor:pointer;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:3px;min-height:32px}.rl p{margin-top:6px}@media(max-width:767px){body .dk-cartes>li{display:block!important;padding:12px 14px!important;min-height:0!important}body .dk-cartes>li>.dk-ico{position:static!important;float:inline-start;width:40px!important;height:40px!important;margin:0 12px 4px 0!important;margin-inline-end:12px!important;padding:0!important}body .dk-cartes>li>b{font-size:17px}}</style>",
                        "<p>Cada lugar indica duración, niños, comida kosher cerca y día de cierre; el resto está en «Leer más». No guiamos en Shabat: cada plan va de domingo a viernes. Horarios leídos en la web de cada lugar el 21 de octubre de 2026.</p><style>.rl{margin-top:6px}.rl summary{cursor:pointer;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:3px;min-height:32px}.rl p{margin-top:6px}@media(max-width:767px){body .dk-cartes>li{display:block!important;padding:12px 14px!important;min-height:0!important}body .dk-cartes>li>.dk-ico{position:static!important;float:inline-start;width:40px!important;height:40px!important;margin:0 12px 4px 0!important;margin-inline-end:12px!important;padding:0!important}body .dk-cartes>li>b{font-size:17px}}</style>",
                        "<p>לכל מקום מצוינים משך הביקור, ילדים, אוכל כשר בקרבת מקום ויום סגירה; השאר תחת ״להמשך קריאה״. אנחנו לא מדריכים בשבת, ולכן כל תוכנית נמשכת מיום ראשון עד שישי. השעות נקראו באתר של כל מקום ב-21 באוקטובר 2026.</p><style>.rl{margin-top:6px}.rl summary{cursor:pointer;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:3px;min-height:32px}.rl p{margin-top:6px}@media(max-width:767px){body .dk-cartes>li{display:block!important;padding:12px 14px!important;min-height:0!important}body .dk-cartes>li>.dk-ico{position:static!important;float:inline-start;width:40px!important;height:40px!important;margin:0 12px 4px 0!important;margin-inline-end:12px!important;padding:0!important}body .dk-cartes>li>b{font-size:17px}}</style>")),
            sec("beige", _("Old Lyon <i>and its hills</i>", "Le vieux Lyon <i>et ses collines</i>", "El Lyon antiguo <i>y sus colinas</i>", "ליון העתיקה <i>וגבעותיה</i>"), [vieux, fourviere, croix]),
            sec("text", _("Parks, squares <i>and rivers</i>", "Parcs, places <i>et fleuves</i>", "Parques, plazas <i>y ríos</i>", "פארקים, כיכרות <i>ונהרות</i>"), [tete, presq, fresque, quais, partdieu]),
            sec("beige", _("Museums <i>for a rainy day</i>", "Des musées <i>pour un jour de pluie</i>", "Museos <i>para un día de lluvia</i>", "מוזיאונים <i>ליום גשום</i>"), [conf, lumiere, beaux]),
            sec("text", _("Jewish Lyon <i>and memory</i>", "Le patrimoine juif de Lyon <i>et la mémoire</i>", "El Lyon judío <i>y la memoria</i>", "ליון היהודית <i>והזיכרון</i>"), [synag, chrd, izieu]),
            dict(type="map", h2=_("The places <i>on the map</i>", "Les lieux <i>sur la carte</i>", "Los lugares <i>en el mapa</i>", "המקומות <i>על המפה</i>"), h=300, points=[
                (_("Vieux Lyon, rue Saint-Jean", "Vieux Lyon, rue Saint-Jean", "Vieux Lyon, rue Saint-Jean", "ליון העתיקה, rue Saint-Jean"), "rue Saint-Jean, 69005 Lyon"),
                (_("Roman theatres, Lugdunum", "Théâtres romains, Lugdunum", "Teatros romanos, Lugdunum", "התיאטראות הרומיים, Lugdunum"), "17 rue Cléberg, 69005 Lyon"),
                (_("Mur des Canuts", "Mur des Canuts", "Mur des Canuts", "קיר הקאנו (Mur des Canuts)"), "boulevard des Canuts, 69004 Lyon"),
                (_("Parc de la Tête d'Or", "Parc de la Tête d'Or", "Parque de la Tête d'Or", "פארק טט ד'אור"), "boulevard des Belges, 69006 Lyon"),
                (_("Place Bellecour", "Place Bellecour", "Place Bellecour", "כיכר בלקור"), "place Bellecour, 69002 Lyon"),
                (_("Fresque des Lyonnais", "Fresque des Lyonnais", "Fresque des Lyonnais", "ציור הקיר של תושבי ליון"), "quai de la Pêcherie, 69001 Lyon"),
                (_("Part-Dieu", "Part-Dieu", "Part-Dieu", "פר-דייה"), "17 rue du Docteur Bouchut, 69003 Lyon"),
                (_("Musée des Confluences", "Musée des Confluences", "Museo de las Confluences", "מוזיאון קונפלואנס"), "86 quai Perrache, 69002 Lyon"),
                (_("Institut Lumière", "Institut Lumière", "Institut Lumière", "מכון לומייר"), "25 rue du Premier-Film, 69008 Lyon"),
                (_("Musée des Beaux-Arts", "Musée des Beaux-Arts", "Museo de Bellas Artes", "המוזיאון לאמנויות יפות"), "20 place des Terreaux, 69001 Lyon"),
                (_("Grande Synagogue", "Grande Synagogue", "Gran Sinagoga", "בית הכנסת הגדול"), "13 quai Tilsitt, 69002 Lyon"),
                ("CHRD", "14 avenue Berthelot, 69007 Lyon"),
            ], note=_("Twelve of the fourteen places; the quays run along both rivers and Izieu is one hour from Lyon. Tap a marker for directions.",
                      "Douze des quatorze lieux ; les quais longent les deux fleuves et Izieu est à une heure de Lyon. Touchez un repère pour obtenir l’itinéraire.",
                      "Doce de los catorce lugares; los muelles siguen los dos ríos e Izieu está a una hora de Lyon. Toque un marcador para ver cómo llegar.",
                      "שנים עשר מתוך ארבעה עשר המקומות; הגדות עוברות לאורך שני הנהרות ואיזיה במרחק שעה מליון. הקישו על סמן להוראות הגעה.")),
            dict(type="beige", h2=_("Three days, <i>three ways</i>", "Trois jours, <i>trois façons</i>", "Tres días, <i>tres maneras</i>", "שלושה ימים, <i>שלוש דרכים</i>"), html=three),
            dict(type="faq", h2=_("Visiting Lyon: <i>questions</i>", "Visiter Lyon : <i>questions</i>", "Visitar Lyon: <i>preguntas</i>", "ביקור בליון: <i>שאלות</i>"), items=faq),
            dict(type="cta", txt=_("Want Lyon planned around your dates and Shabbat?", "Envie d’un Lyon organisé autour de vos dates et du Shabbat ?", "¿Quiere un Lyon organizado según sus fechas y el Shabat?", "רוצים ליון מתוכננת סביב התאריכים והשבת שלכם?"), msg=WA_MSG[L]),
        ],
        related=[("../tours/jewish-lyon/", _("Jewish Lyon tour, 2 h 30", "Visite du quartier juif de Lyon, 2 h 30", "Visita del Lyon judío, 2 h 30", "סיור ליון היהודית, שעתיים וחצי")),
                 ("../lyon-weather/", _("Lyon weather by season and this week’s forecast", "Météo à Lyon par saison et prévisions de la semaine", "El tiempo en Lyon por estaciones y previsión de la semana", "מזג האוויר בליון לפי עונות ותחזית השבוע")),
                 ("../shabbat-in-lyon/", _("Shabbat in Lyon", "Shabbat à Lyon", "Shabat en Lyon", "שבת בליון")),
                 ("../kosher-van-transfers/", _("Van and transfers", "Van et transferts", "Furgoneta y traslados", "ואן והסעות"))],
        jsonld=None, ticket=True,
        VERIF=[
            "Jours et horaires d'ouverture lus le 21/10/2026 : Parc de la Tête d'Or (lyon.fr : 6 h 30 à 20 h 30, 22 h 30 du 15/04 au 14/10, 105 ha, zoo 9 h 30 à 17 h ou 17 h 45, fermé le mardi, 3 roseraies), Musée des Confluences (museedesconfluences.fr : mardi à dimanche 10 h 30 à 18 h 30, lundi pendant les vacances de la zone A hors été), Beaux-Arts (mba-lyon.fr : mercredi à lundi 10 h à 18 h, vendredi 10 h 30, fermé mardi, 70 salles et 7 000 m²), Institut Lumière (institut-lumiere.org : mardi à dimanche 10 h à 18 h 30), CHRD et Maison d'Izieu (reprises des pages du site, relevées le 07/10).",
            "Théâtres romains de Fourvière : « accès libre, 7 h à 21 h du 15/04 au 15/09, 7 h à 19 h sinon » vient d'un site tiers (museemusee.com), le site officiel lugdunum.grandlyon.com n'affiche que les horaires du musée (mardi au vendredi 11 h à 18 h, samedi et dimanche 10 h à 18 h). A confirmer par téléphone avant publication. Funiculaire F2 jusqu'à Minimes-Théâtres romains : lyon-visite.info et Wikipédia.",
            "Part-Dieu : boutiques lundi au samedi 9 h 30 à 20 h, certains dimanches (lyon.fr et westfield.com/fr). Le « kosher grocery in the 3rd » reprend la liste du Beth Din de Lyon déjà citée sur la page Kosher shabbat meals ; aucun nom de commerce n'est cité ici.",
            "Chiffres de patrimoine à recouper : UNESCO 1998 (Vieux Lyon), Grand Théâtre vers 15 av. J.-C., Mur des Canuts 1 200 m² (visiterlyon.com), Fresque des Lyonnais environ 800 m² et une trentaine de personnages (visiterlyon.com donne 25 + 6, Wikipédia 24 + 5), Lumière : premier film tourné en 1895 (récit courant, pas de source du site).",
            "Distances et durées (10 minutes à pied du Vieux Lyon au 2e, 2,5 km Bellecour-Confluences, durées de visite) : estimations de l'équipe, à vérifier sur un itinéraire. Aucun restaurant casher du 8e (Institut Lumière) n'est vérifié : la page renvoie vers le 3e et le 6e.",
            "Pont d'accès de la Maison d'Izieu fermé jusqu'en novembre 2026 : repris de la page maison-izieu (relevé du 07/10), à revérifier sur le site du mémorial avant publication.",
            "Aucun prix, aucun numéro de téléphone, aucun nom de partenaire dans les pages. Le bloc des cinq offres « Lyon, réservé en un message » est posé par _offres_lyon.py.",
            "Hébreu : traduit par Claude avec le lexique de relecture-hebreu, pas relu par un natif. Noms latins gardés entre parenthèses dans le texte, comme sur les autres pages /he/ (pas de dir=\"ltr\" : une balise de plus casserait le contrôle de structure EN/HE).",
        ],
    )


PAGE = page(0)
PAGE_FR = page(1)
PAGE_ES = page(2)
PAGE_HE = page(3)
