# -*- coding: utf-8 -*-
"""21/10 : /lyon-weather/. PAGE = source anglaise lue par _build_guide.py. PAGE_FR, PAGE_ES, PAGE_HE = traductions (meme structure).
Chiffres : Meteo-France, fiche climatologique Lyon-Bron, normales 1991-2020 (lue le 21/10/2026). Previsions : API Open-Meteo sans cle, rendues dans la page."""

import json
MOIS = (("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"),
        ("Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"),
        ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"),
        ("ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"))
TMAX = (7.1, 9.0, 13.8, 17.4, 21.5, 25.6, 28.2, 28.0, 23.1, 17.7, 11.4, 7.7)
TMIN = (1.1, 1.4, 4.2, 7.2, 11.2, 15.0, 17.0, 16.6, 12.8, 9.6, 4.9, 2.0)
PLUIE = (49.8, 41.6, 49.4, 68.9, 80.9, 74.1, 67.4, 65.5, 82.5, 99.8, 87.2, 53.7)
JOURS = (8.1, 7.9, 8.4, 9.0, 10.3, 8.5, 7.5, 7.2, 7.3, 9.9, 9.4, 9.2)
FICHE = "https://donneespubliques.meteofrance.fr/FichesClim/FICHECLIM_69029001.pdf"
WA_MSG = ("Hello, I am planning a stay in Lyon and would like a Jewish visit and Shabbat arranged. Dates: / Number of people: / Preferred language:",
          "Bonjour, je prépare un séjour à Lyon et souhaite une visite juive et un Shabbat organisés. Dates : / Nombre de personnes : / Langue souhaitée :",
          "Hola, preparo una estancia en Lyon y quisiera una visita judía y un Shabat organizados. Fechas: / Número de personas: / Idioma preferido:",
          "שלום, אנחנו מתכננים שהות בליון ורוצים סיור יהודי ושבת מסודרים. תאריכים: / מספר משתתפים: / שפה מועדפת:")

CSS = """.meteo7{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:10px;margin-top:18px}
.jm{background:var(--blanc);border-radius:15px;padding:14px 12px;text-align:center;display:flex;flex-direction:column;gap:4px}
.jm b{font-family:var(--titre);font-weight:400;font-size:18px}
.jm .d{font-size:13px;opacity:.7}
.jm .c{font-size:15px;min-height:2.4em;display:flex;align-items:center;justify-content:center}
.jm .t{font-size:17px}
.jm .t i{opacity:.65;font-style:normal}
.jm .p{font-size:13px;opacity:.75}
.meteo-msg{grid-column:1/-1;text-align:center;opacity:.8}
.meteo-tab-wrap{overflow-x:auto;margin-top:14px}
.meteo-tab{width:100%;border-collapse:collapse;font-size:15px;background:var(--blanc);border-radius:15px;overflow:hidden}
.meteo-tab th,.meteo-tab td{padding:9px 12px;border-bottom:1px solid rgba(28,27,31,.12);text-align:start;white-space:nowrap}
.meteo-tab th{font-weight:600;background:var(--beige)}
.meteo-tab tr:last-child td{border-bottom:0}"""


def widget(L):
    _ = lambda *a: a[L]
    lab = {
        "clear": _("Clear", "Dégagé", "Despejado", "בהיר"), "part": _("Partly cloudy", "Éclaircies", "Parcialmente nublado", "מעונן חלקית"),
        "cloud": _("Overcast", "Couvert", "Nublado", "מעונן"), "fog": _("Fog", "Brouillard", "Niebla", "ערפל"),
        "drizzle": _("Drizzle", "Bruine", "Llovizna", "טפטוף"), "rain": _("Rain", "Pluie", "Lluvia", "גשם"),
        "show": _("Showers", "Averses", "Chubascos", "ממטרים"), "snow": _("Snow", "Neige", "Nieve", "שלג"),
        "storm": _("Storm", "Orage", "Tormenta", "סופת רעמים"),
    }
    loc = _("en-GB", "fr-FR", "es-ES", "he-IL")
    pluie = _("Rain ", "Pluie ", "Lluvia ", "גשם ")
    shab = _("Shabbat", "Shabbat", "Shabat", "שבת")
    chargement = _("Loading the forecast...", "Chargement des prévisions...", "Cargando la previsión...", "טוענים את התחזית...")
    echec = _("The forecast is unavailable right now. The official forecast is on Météo-France: ", "Les prévisions sont indisponibles pour le moment. Les prévisions officielles sont sur Météo-France : ",
              "La previsión no está disponible ahora. La previsión oficial está en Météo-France: ", "התחזית אינה זמינה כרגע. התחזית הרשמית נמצאת באתר Météo-France: ")
    js = ('(function(){var box=document.getElementById("meteo7");if(!box)return;var T=' + json.dumps(lab, ensure_ascii=False) + ';'
          'function lbl(c){if(c===0)return T.clear;if(c<=2)return T.part;if(c===3)return T.cloud;if(c<=48)return T.fog;if(c<=57)return T.drizzle;if(c<=67)return T.rain;if(c<=77)return T.snow;if(c<=82)return T.show;if(c<=86)return T.snow;return T.storm}'
          'function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}'
          'fetch("https://api.open-meteo.com/v1/forecast?latitude=45.7578&longitude=4.832&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FParis")'
          '.then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){var x=d.daily;box.textContent="";'
          'x.time.forEach(function(s,i){var dt=new Date(s+"T12:00:00");var c=el("div","jm");'
          'c.appendChild(el("b","",dt.toLocaleDateString("' + loc + '",{weekday:"long"})));'
          'c.appendChild(el("span","d",dt.toLocaleDateString("' + loc + '",{day:"numeric",month:"short"})+(dt.getDay()===6?" \\u00b7 ' + shab + '":"")));'
          'c.appendChild(el("span","c",lbl(x.weathercode[i])));'
          'var t=el("span","t",Math.round(x.temperature_2m_max[i])+"\\u00b0");var m=el("i","", " / "+Math.round(x.temperature_2m_min[i])+"\\u00b0");t.appendChild(m);c.appendChild(t);'
          'var p=x.precipitation_probability_max[i];c.appendChild(el("span","p",p==null?"":"' + pluie + '"+p+"%"));box.appendChild(c)})})'
          '.catch(function(){box.textContent="";var p=el("p","meteo-msg","' + echec + '");var a=el("a","","Météo-France");a.href="https://meteofrance.com/previsions-meteo-france/lyon/69000";a.rel="noopener";p.appendChild(a);box.appendChild(p)})})();')
    return ('<section class="ss wrap meteo-live" id="forecast"><h2 class="centre">'
            + _("The next seven days <i>in Lyon</i>", "Les sept prochains jours <i>à Lyon</i>", "Los próximos siete días <i>en Lyon</i>", "שבעת הימים הקרובים <i>בליון</i>")
            + '</h2><div class="meteo7" id="meteo7" aria-live="polite"><p class="meteo-msg">' + chargement + '</p></div>'
            + '<p class="carte-note">' + _("Forecast from Open-Meteo, read each time you open the page. The official forecast is on ", "Prévisions Open-Meteo, lues à chaque ouverture de la page. Les prévisions officielles sont sur ",
                                           "Previsión de Open-Meteo, leída cada vez que abre la página. La previsión oficial está en ", "תחזית מ-Open-Meteo, נטענת בכל פתיחה של הדף. התחזית הרשמית נמצאת באתר ")
            + '<a href="https://meteofrance.com/previsions-meteo-france/lyon/69000" rel="noopener">Météo-France</a>.</p>'
            + '<style>' + CSS + '</style><script>' + js + '</script></section>')


def page(L):
    _ = lambda *a: a[L]
    a = lambda u, t: f'<a href="{u}">{t}</a>'
    dec = (lambda x: f"{x:.1f}") if L in (0, 3) else (lambda x: f"{x:.1f}".replace(".", ","))

    heads = _(("Month", "Day high (°C)", "Night low (°C)", "Rain (mm)", "Rain days"), ("Mois", "Maximale (°C)", "Minimale (°C)", "Pluie (mm)", "Jours de pluie"),
              ("Mes", "Máxima (°C)", "Mínima (°C)", "Lluvia (mm)", "Días de lluvia"), ("חודש", "מקסימום (°C)", "מינימום (°C)", "גשם (מ״מ)", "ימי גשם"))
    rows = "".join(f"<tr><td>{MOIS[L][i]}</td><td>{dec(TMAX[i])}</td><td>{dec(TMIN[i])}</td><td>{dec(PLUIE[i])}</td><td>{dec(JOURS[i])}</td></tr>" for i in range(12))
    tab = ('<div class="meteo-tab-wrap"><table class="meteo-tab"><thead><tr>' + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>" + rows + "</tbody></table></div>"
           '<p class="source">' + _("Source: " + a(FICHE, "Météo-France, climatological sheet of Lyon-Bron") + ", normals 1991 to 2020, station at 202 m altitude east of the city, read on 21 October 2026. Rain days count days with at least 1 mm.",
                                   "Source : " + a(FICHE, "Météo-France, fiche climatologique de Lyon-Bron") + ", normales 1991 à 2020, station à 202 m d’altitude à l’est de la ville, consultée le 21 octobre 2026. Les jours de pluie comptent les jours avec au moins 1 mm.",
                                   "Fuente: " + a(FICHE, "Météo-France, ficha climatológica de Lyon-Bron") + ", normales de 1991 a 2020, estación a 202 m de altitud al este de la ciudad, consultada el 21 de octubre de 2026. Los días de lluvia cuentan los días con al menos 1 mm.",
                                   "מקור: " + a(FICHE, "Météo-France, דף האקלים של ליון-ברון") + ", ממוצעים 1991 עד 2020, תחנה בגובה 202 מ׳ מזרחית לעיר, נקרא ב-21 באוקטובר 2026. ימי גשם הם ימים עם 1 מ״מ לפחות.")
           + "</p>")
    tab = tab.replace("", "")

    seasons = ("<ul>"
               + "<li><b>" + _("Winter, December to February.", "L’hiver, de décembre à février.", "Invierno, de diciembre a febrero.", "חורף, מדצמבר עד פברואר.") + "</b> "
               + _("Daytime highs of 7.7 °C in December, 7.1 °C in January and 9.0 °C in February; nights at 2.0, 1.1 and 1.4 °C. It freezes on 10 to 13 nights a month. Rain: 41.6 to 53.7 mm a month, on 8 or 9 days.",
                   "Maximales de 7,7 °C en décembre, 7,1 °C en janvier et 9,0 °C en février ; nuits à 2,0, 1,1 et 1,4 °C. Il gèle 10 à 13 nuits par mois. Pluie : 41,6 à 53,7 mm par mois, sur 8 ou 9 jours.",
                   "Máximas de 7,7 °C en diciembre, 7,1 °C en enero y 9,0 °C en febrero; noches a 2,0, 1,1 y 1,4 °C. Hiela entre 10 y 13 noches al mes. Lluvia: de 41,6 a 53,7 mm al mes, en 8 o 9 días.",
                   "מקסימום של 7.7 °C בדצמבר, 7.1 °C בינואר ו-9.0 °C בפברואר; לילות של 2.0, 1.1 ו-1.4 °C. יש כפור ב-10 עד 13 לילות בחודש. גשם: 41.6 עד 53.7 מ״מ בחודש, ב-8 או 9 ימים.")
               + "</li>"
               + "<li><b>" + _("Spring, March to May, with Pesach.", "Le printemps, de mars à mai, avec Pessah.", "Primavera, de marzo a mayo, con Pésaj.", "אביב, ממרץ עד מאי, עם פסח.") + "</b> "
               + _("Highs climb from 13.8 °C in March to 17.4 °C in April and 21.5 °C in May; lows from 4.2 to 11.2 °C. May is the wettest spring month, with 80.9 mm over 10 days. Pesach falls in this season, so pack for sun and rain.",
                   "Les maximales passent de 13,8 °C en mars à 17,4 °C en avril et 21,5 °C en mai ; les minimales de 4,2 à 11,2 °C. Mai est le mois de printemps le plus pluvieux, avec 80,9 mm sur 10 jours. Pessah tombe à cette saison : prévoyez le soleil et la pluie.",
                   "Las máximas suben de 13,8 °C en marzo a 17,4 °C en abril y 21,5 °C en mayo; las mínimas, de 4,2 a 11,2 °C. Mayo es el mes más lluvioso de la primavera, con 80,9 mm en 10 días. Pésaj cae en esta estación: prepare equipaje para sol y lluvia.",
                   "המקסימום עולה מ-13.8 °C במרץ ל-17.4 °C באפריל ול-21.5 °C במאי; המינימום מ-4.2 ל-11.2 °C. מאי הוא חודש האביב הגשום ביותר, עם 80.9 מ״מ ב-10 ימים. פסח חל בעונה הזאת, ולכן אורזים לשמש ולגשם.")
               + "</li>"
               + "<li><b>" + _("Summer, June to August.", "L’été, de juin à août.", "Verano, de junio a agosto.", "קיץ, מיוני עד אוגוסט.") + "</b> "
               + _("Highs of 25.6 °C in June, 28.2 °C in July and 28.0 °C in August; lows between 15.0 and 17.0 °C. The thermometer passes 30 °C on 6 days in June and about 11 days in July and in August. Rain: 65.5 to 74.1 mm a month.",
                   "Maximales de 25,6 °C en juin, 28,2 °C en juillet et 28,0 °C en août ; minimales entre 15,0 et 17,0 °C. Le thermomètre dépasse 30 °C pendant 6 jours en juin et environ 11 jours en juillet et en août. Pluie : 65,5 à 74,1 mm par mois.",
                   "Máximas de 25,6 °C en junio, 28,2 °C en julio y 28,0 °C en agosto; mínimas entre 15,0 y 17,0 °C. El termómetro supera los 30 °C durante 6 días en junio y unos 11 días en julio y en agosto. Lluvia: de 65,5 a 74,1 mm al mes.",
                   "מקסימום של 25.6 °C ביוני, 28.2 °C ביולי ו-28.0 °C באוגוסט; מינימום בין 15.0 ל-17.0 °C. המדחום עובר 30 °C במשך 6 ימים ביוני ובערך 11 ימים ביולי ובאוגוסט. גשם: 65.5 עד 74.1 מ״מ בחודש.")
               + "</li>"
               + "<li><b>" + _("Autumn, when the rain returns.", "L’automne, quand la pluie revient.", "Otoño, cuando vuelve la lluvia.", "סתיו, כשהגשם חוזר.") + "</b> "
               + _("September is still warm, with highs of 23.1 °C; October drops to 17.7 °C and November to 11.4 °C. October is the wettest month of the year, with 99.8 mm over about 10 days, and November follows with 87.2 mm.",
                   "Septembre reste doux, avec des maximales de 23,1 °C ; octobre descend à 17,7 °C et novembre à 11,4 °C. Octobre est le mois le plus pluvieux de l’année, avec 99,8 mm sur environ 10 jours, et novembre suit avec 87,2 mm.",
                   "Septiembre sigue siendo cálido, con máximas de 23,1 °C; octubre baja a 17,7 °C y noviembre a 11,4 °C. Octubre es el mes más lluvioso del año, con 99,8 mm en unos 10 días, y noviembre le sigue con 87,2 mm.",
                   "ספטמבר עדיין חם, עם מקסימום של 23.1 °C; אוקטובר יורד ל-17.7 °C ונובמבר ל-11.4 °C. אוקטובר הוא החודש הגשום ביותר בשנה, עם 99.8 מ״מ בכ-10 ימים, ונובמבר אחריו עם 87.2 מ״מ.")
               + "</li></ul>")

    pack = (_("<p><b>Winter.</b> A warm coat, a hat and gloves, and shoes with grip: the cobbles of Vieux Lyon are slippery when wet or frosted.</p>",
              "<p><b>Hiver.</b> Un manteau chaud, un bonnet, des gants et des chaussures qui accrochent : les pavés du Vieux Lyon glissent quand ils sont mouillés ou gelés.</p>",
              "<p><b>Invierno.</b> Un abrigo grueso, gorro, guantes y calzado con buen agarre: los adoquines de Vieux Lyon resbalan cuando están mojados o helados.</p>",
              "<p><b>חורף.</b> מעיל חם, כובע, כפפות ונעליים עם אחיזה: אבני הריצוף של ליון העתיקה חלקות כשהן רטובות או קפואות.</p>")
            + _("<p><b>Spring and autumn.</b> Layers and a light waterproof. It rains on 7 to 10 days a month in these seasons, and a morning at 6 °C can turn into an afternoon at 17 °C.</p>",
                "<p><b>Printemps et automne.</b> Des couches et un imperméable léger. Il pleut 7 à 10 jours par mois à ces saisons, et un matin à 6 °C peut devenir un après-midi à 17 °C.</p>",
                "<p><b>Primavera y otoño.</b> Capas y un impermeable ligero. Llueve de 7 a 10 días al mes en estas estaciones, y una mañana a 6 °C puede convertirse en una tarde a 17 °C.</p>",
                "<p><b>אביב וסתיו.</b> שכבות ומעיל גשם קל. יורד גשם 7 עד 10 ימים בחודש בעונות האלה, ובוקר של 6 °C יכול להפוך לאחר צהריים של 17 °C.</p>")
            + _("<p><b>Summer.</b> Light clothes, a hat, water and sun cream. July and August pass 30 °C on about eleven days each, so start early and keep the middle of the day for a museum or the shade of the quays.</p>",
                "<p><b>Été.</b> Des vêtements légers, un chapeau, de l’eau et de la crème solaire. Juillet et août dépassent 30 °C environ onze jours chacun : partez tôt et gardez le milieu de la journée pour un musée ou l’ombre des quais.</p>",
                "<p><b>Verano.</b> Ropa ligera, sombrero, agua y crema solar. Julio y agosto superan los 30 °C en unos once días cada uno: salga temprano y reserve el mediodía para un museo o la sombra de los muelles.</p>",
                "<p><b>קיץ.</b> בגדים קלים, כובע, מים וקרם הגנה. ביולי ובאוגוסט עוברים 30 °C בערך אחד עשר ימים בכל חודש, ולכן יוצאים מוקדם ושומרים את אמצע היום למוזיאון או לצל של הגדות.</p>")
            + _("<p><b>All year.</b> Shoes for walking: Vieux Lyon is cobbled, the Croix-Rousse is steep and a Shabbat on foot is long. You walk to synagogue in whatever weather there is, so pack a proper coat, not only an umbrella.</p>",
                "<p><b>Toute l’année.</b> Des chaussures de marche : le Vieux Lyon est pavé, la Croix-Rousse est raide et un Shabbat à pied est long. On va à la synagogue par tous les temps : prenez un vrai manteau, pas seulement un parapluie.</p>",
                "<p><b>Todo el año.</b> Calzado para caminar: Vieux Lyon está empedrado, la Croix-Rousse es empinada y un Shabat a pie es largo. Se va a la sinagoga con el tiempo que haga: lleve un abrigo de verdad, no solo un paraguas.</p>",
                "<p><b>כל השנה.</b> נעליים להליכה: ליון העתיקה מרוצפת באבנים, קרואה-רוס תלולה ושבת ברגל היא ארוכה. הולכים לבית הכנסת בכל מזג אוויר, ולכן אורזים מעיל של ממש ולא רק מטרייה.</p>"))

    plan = ("<ul>"
            + "<li><b>" + _("Rain: museums and covered traboules.", "Pluie : les musées et les traboules couvertes.", "Lluvia: museos y traboules cubiertas.", "גשם: מוזיאונים וטרבולים מקורים.") + "</b> "
            + _("Go to the CHRD (Wednesday to Sunday), the Confluences museum (Tuesday to Sunday), the Musée des Beaux-Arts (closed Tuesday) or the Institut Lumière (Tuesday to Sunday). In Vieux Lyon, the traboules take you from one street to the next under cover. Each place is described on " + a("../things-to-do-in-lyon/", "Things to do in Lyon") + ".",
                "Allez au CHRD (du mercredi au dimanche), au musée des Confluences (du mardi au dimanche), au musée des Beaux-Arts (fermé le mardi) ou à l’Institut Lumière (du mardi au dimanche). Dans le Vieux Lyon, les traboules vous mènent d’une rue à l’autre à l’abri. Chaque lieu est décrit sur " + a("../things-to-do-in-lyon/", "Que faire à Lyon") + ".",
                "Vaya al CHRD (de miércoles a domingo), al museo de las Confluences (de martes a domingo), al Museo de Bellas Artes (cerrado el martes) o al Institut Lumière (de martes a domingo). En Vieux Lyon, las traboules le llevan de una calle a otra a cubierto. Cada lugar se describe en " + a("../things-to-do-in-lyon/", "Qué hacer en Lyon") + ".",
                "הולכים ל-CHRD (מיום רביעי עד יום ראשון), למוזיאון קונפלואנס (מיום שלישי עד יום ראשון), למוזיאון לאמנויות יפות (סגור ביום שלישי) או למכון לומייר (מיום שלישי עד יום ראשון). בליון העתיקה, הטרבולים מעבירים אתכם מרחוב לרחוב מתחת לגג. כל מקום מתואר ב" + a("../things-to-do-in-lyon/", "מה לעשות בליון") + ".")
            + "</li>"
            + "<li><b>" + _("Sun and clear sky: lake, quays and hills.", "Soleil et ciel dégagé : le lac, les quais et les collines.", "Sol y cielo despejado: lago, muelles y colinas.", "שמש ושמיים בהירים: אגם, גדות וגבעות.") + "</b> "
            + _("Spend it outdoors: the Parc de la Tête d’Or and its lake, the quays of the Saône and the Rhône, the climb to the Croix-Rousse. In July and August start early and rest at midday; highs average 28 °C and pass 30 °C on about eleven days.",
                "Passez-le dehors : le parc de la Tête d’Or et son lac, les quais de la Saône et du Rhône, la montée à la Croix-Rousse. En juillet et en août, partez tôt et reposez-vous à midi ; les maximales atteignent 28 °C en moyenne et dépassent 30 °C environ onze jours.",
                "Pásela al aire libre: el parque de la Tête d’Or y su lago, los muelles del Saona y del Ródano, la subida a la Croix-Rousse. En julio y agosto salga temprano y descanse a mediodía; las máximas rondan los 28 °C y superan los 30 °C en unos once días.",
                "מעבירים אותו בחוץ: פארק טט ד’אור והאגם שלו, רציפי הסון והרון, העלייה לקרואה-רוס. ביולי ובאוגוסט יוצאים מוקדם ונחים בצהריים; המקסימום הממוצע הוא 28 °C והוא עובר 30 °C בכאחד עשר ימים.")
            + "</li>"
            + "<li><b>" + _("Snow in town: time for the Alps.", "Neige en ville : c’est l’heure des Alpes.", "Nieve en la ciudad: es la hora de los Alpes.", "שלג בעיר: הגיע הזמן לאלפים.") + "</b> "
            + _("Snow in the city is rare: on average only five days a year stay below freezing all day. When Lyon turns white, the resorts are white too. Take a " + a("../kosher-van-transfers/", "van") + " to the stations: see " + a("../alps/", "the Alps, strictly kosher") + ".",
                "La neige en ville est rare : en moyenne, seulement cinq jours par an restent sous zéro toute la journée. Quand Lyon blanchit, les stations sont blanches aussi. Prenez un " + a("../kosher-van-transfers/", "van") + " vers les stations : voir " + a("../alps/", "les Alpes, strictement casher") + ".",
                "La nieve en la ciudad es rara: de media, solo cinco días al año se mantienen bajo cero todo el día. Cuando Lyon se pone blanca, las estaciones también lo están. Tome una " + a("../kosher-van-transfers/", "furgoneta") + " hacia las estaciones: vea " + a("../alps/", "los Alpes, estrictamente kosher") + ".",
                "שלג בעיר הוא נדיר: בממוצע רק חמישה ימים בשנה נשארים מתחת לאפס כל היום. כשליון מלבינה, גם אתרי הסקי לבנים. לוקחים " + a("../kosher-van-transfers/", "ואן") + " לאתרים: ראו " + a("../alps/", "האלפים, כשר לחלוטין") + ".")
            + "</li>"
            + "<li><b>" + _("Shabbat entry: 16:30 in December, 21:00 in June.", "Entrée de Shabbat : 16 h 30 en décembre, 21 h en juin.", "Entrada del Shabat: 16:30 en diciembre, 21:00 en junio.", "כניסת שבת: 16:30 בדצמבר, 21:00 ביוני.") + "</b> "
            + _("Candle lighting falls as early as 16:30 in December and after 21:00 in June. In winter, end Friday’s sightseeing early and be back at your table before dark; in summer the long Friday leaves room for a late visit. Exact times for this week are just below. See " + a("../shabbat-in-lyon/", "Shabbat in Lyon") + ".",
                "L’allumage des bougies tombe dès 16 h 30 en décembre et après 21 h en juin. En hiver, terminez tôt les visites du vendredi et soyez à table avant la nuit ; en été, le long vendredi laisse place à une visite tardive. Les horaires exacts de cette semaine sont juste en dessous. Voir " + a("../shabbat-in-lyon/", "Shabbat à Lyon") + ".",
                "El encendido de velas cae hacia las 16:30 en diciembre y después de las 21:00 en junio. En invierno, termine pronto las visitas del viernes y esté a la mesa antes de que oscurezca; en verano, el viernes largo deja sitio para una visita tardía. Los horarios exactos de esta semana están justo debajo. Vea " + a("../shabbat-in-lyon/", "Shabat en Lyon") + ".",
                "הדלקת הנרות חלה כבר ב-16:30 בדצמבר ואחרי 21:00 ביוני. בחורף מסיימים את סיורי יום שישי מוקדם וחוזרים לשולחן לפני החשכה; בקיץ יום שישי הארוך משאיר מקום לביקור מאוחר. הזמנים המדויקים לשבוע הזה מופיעים ממש מתחת. ראו " + a("../shabbat-in-lyon/", "שבת בליון") + ".")
            + "</li></ul>")

    faq = [
        (_("When is the best time to visit Lyon?", "Quelle est la meilleure période pour visiter Lyon ?", "¿Cuál es la mejor época para visitar Lyon?", "מתי הזמן הטוב ביותר לבקר בליון?"),
         _("Late spring and early autumn: highs between 17 and 26 °C in April, May, June and September. July and August are the hottest, December and January the coldest, October the wettest.",
           "La fin du printemps et le début de l’automne : maximales entre 17 et 26 °C en avril, mai, juin et septembre. Juillet et août sont les plus chauds, décembre et janvier les plus froids, octobre le plus pluvieux.",
           "El final de la primavera y el principio del otoño: máximas de entre 17 y 26 °C en abril, mayo, junio y septiembre. Julio y agosto son los más calurosos, diciembre y enero los más fríos, octubre el más lluvioso.",
           "סוף האביב ותחילת הסתיו: מקסימום בין 17 ל-26 °C באפריל, מאי, יוני וספטמבר. יולי ואוגוסט החמים ביותר, דצמבר וינואר הקרים ביותר, ואוקטובר הגשום ביותר.")),
        (_("Does it snow in Lyon?", "Neige-t-il à Lyon ?", "¿Nieva en Lyon?", "האם יורד שלג בליון?"),
         _("Rarely, and not for long. Météo-France counts about five days a year when the temperature stays below freezing all day, and 42 nights with frost. For snow to play in, go to the " + a("../alps/", "Alps") + ".",
           "Rarement, et pas longtemps. Météo-France compte environ cinq jours par an où la température reste sous zéro toute la journée, et 42 nuits de gel. Pour jouer dans la neige, allez dans les " + a("../alps/", "Alpes") + ".",
           "Pocas veces, y no por mucho tiempo. Météo-France cuenta unos cinco días al año en que la temperatura se mantiene bajo cero todo el día, y 42 noches con helada. Para jugar en la nieve, vaya a los " + a("../alps/", "Alpes") + ".",
           "לעיתים רחוקות, ולא לזמן רב. Météo-France סופרת בערך חמישה ימים בשנה שבהם הטמפרטורה נשארת מתחת לאפס כל היום, ו-42 לילות עם כפור. כדי לשחק בשלג נוסעים ל" + a("../alps/", "אלפים") + ".")),
        (_("Is Lyon too hot in summer?", "Lyon est-elle trop chaude l’été ?", "¿Hace demasiado calor en Lyon en verano?", "האם ליון חמה מדי בקיץ?"),
         _("July and August average 28 °C by day and pass 30 °C on about eleven days each. Walk early, give the morning to the quays or the Tête d’Or, and keep museums for midday.",
           "Juillet et août font 28 °C en moyenne le jour et dépassent 30 °C environ onze jours chacun. Marchez tôt, donnez la matinée aux quais ou à la Tête d’Or, et gardez les musées pour midi.",
           "Julio y agosto promedian 28 °C de día y superan los 30 °C en unos once días cada uno. Camine temprano, dedique la mañana a los muelles o a la Tête d’Or y reserve los museos para el mediodía.",
           "ביולי ובאוגוסט הממוצע ביום הוא 28 °C והטמפרטורה עוברת 30 °C בכאחד עשר ימים בכל חודש. הולכים מוקדם, נותנים את הבוקר לגדות או לפארק טט ד’אור, ושומרים את המוזיאונים לצהריים.")),
        (_("What time does Shabbat start in Lyon?", "À quelle heure commence le Shabbat à Lyon ?", "¿A qué hora empieza el Shabat en Lyon?", "מתי נכנסת השבת בליון?"),
         _("As early as 16:30 in December and after 21:00 in June. This page shows the exact times for this week, and " + a("../shabbat-in-lyon/", "Shabbat in Lyon") + " has the prayer times.",
           "Dès 16 h 30 en décembre et après 21 h en juin. Cette page affiche les horaires exacts de la semaine, et " + a("../shabbat-in-lyon/", "Shabbat à Lyon") + " donne les horaires de prière.",
           "Desde las 16:30 en diciembre y después de las 21:00 en junio. Esta página muestra los horarios exactos de la semana, y " + a("../shabbat-in-lyon/", "Shabat en Lyon") + " tiene los horarios de oración.",
           "כבר ב-16:30 בדצמבר ואחרי 21:00 ביוני. הדף הזה מציג את הזמנים המדויקים לשבוע, וב" + a("../shabbat-in-lyon/", "שבת בליון") + " יש את זמני התפילה.")),
    ]

    return dict(
        slug="lyon-weather",
        title=_("Lyon weather by season and this week's forecast", "Météo à Lyon par saison et prévisions de la semaine", "El tiempo en Lyon por estaciones y previsión semanal", "מזג האוויר בליון: לפי עונות ותחזית השבוע"),
        desc=_("Lyon weather by season from Météo-France averages, what to pack, a live seven-day forecast and a plan for rain, sun, snow and Shabbat times.",
               "Météo à Lyon par saison d’après Météo-France, quoi mettre dans la valise, prévisions à sept jours en direct et un programme selon pluie, soleil, neige et Shabbat.",
               "El tiempo en Lyon por estaciones según Météo-France, qué meter en la maleta, previsión en directo a siete días y un plan según lluvia, sol, nieve y Shabat.",
               "מזג האוויר בליון לפי עונות על פי ממוצעי Météo-France, מה לארוז, תחזית חיה לשבעה ימים ותוכנית לפי גשם, שמש, שלג וזמני שבת."),
        h1=_("Lyon weather", "Météo à Lyon", "El tiempo en Lyon", "מזג האוויר בליון"),
        ital=_("by season, with this week’s forecast", "par saison, avec les prévisions de la semaine", "por estaciones, con la previsión de la semana", "לפי עונות, עם תחזית השבוע"),
        intro=_("Lyon has four real seasons. Winter days stay near 7 °C, with frost on about ten nights a month; July days average 28 °C; October is the wettest month. The figures below are Météo-France averages for 1991 to 2020. Further down, a live seven-day forecast tells you what to do this week, and when Shabbat comes in.",
                "Lyon a quatre vraies saisons. Les journées d’hiver restent autour de 7 °C, avec du gel environ dix nuits par mois ; les journées de juillet font 28 °C en moyenne ; octobre est le mois le plus pluvieux. Les chiffres ci-dessous sont les moyennes de Météo-France pour 1991 à 2020. Plus bas, des prévisions à sept jours en direct disent quoi faire cette semaine, et à quelle heure entre le Shabbat.",
                "Lyon tiene cuatro estaciones de verdad. Los días de invierno rondan los 7 °C, con helada unas diez noches al mes; los días de julio promedian 28 °C; octubre es el mes más lluvioso. Las cifras de abajo son promedios de Météo-France de 1991 a 2020. Más abajo, una previsión en directo a siete días dice qué hacer esta semana y a qué hora entra el Shabat.",
                "בליון יש ארבע עונות של ממש. ימי החורף נשארים סביב 7 °C, עם כפור בערך עשרה לילות בחודש; ימי יולי מגיעים בממוצע ל-28 °C; אוקטובר הוא החודש הגשום ביותר. המספרים למטה הם ממוצעים של Météo-France לשנים 1991 עד 2020. בהמשך, תחזית חיה לשבעה ימים אומרת מה לעשות השבוע ומתי נכנסת השבת."),
        chips=[],
        illus="flat-stopover.png",
        crumb=("../jewish-lyon-guide/", _("Jewish Lyon guide", "Guide du Lyon juif", "Guía del Lyon judío", "המדריך לליון היהודית")),
        sections=[
            dict(type="text", h2=_("Lyon weather <i>by season</i>", "La météo à Lyon <i>par saison</i>", "El tiempo en Lyon <i>por estaciones</i>", "מזג האוויר בליון <i>לפי עונות</i>"), html=seasons),
            dict(type="beige", h2=_("The twelve months, <i>in numbers</i>", "Les douze mois, <i>en chiffres</i>", "Los doce meses, <i>en cifras</i>", "שנים עשר החודשים, <i>במספרים</i>"), html=tab),
            dict(type="text", h2=_("What to <i>pack</i>", "Quoi mettre <i>dans la valise</i>", "Qué meter <i>en la maleta</i>", "מה <i>לארוז</i>"), html=pack),
            widget(L),
            dict(type="beige", h2=_("Plan the day <i>by the weather</i>", "Organiser la journée <i>selon le temps</i>", "Organizar el día <i>según el tiempo</i>", "לתכנן את היום <i>לפי מזג האוויר</i>"), html=plan),
            dict(type="shabbat"),
            dict(type="faq", h2=_("Lyon weather: <i>questions</i>", "Météo à Lyon : <i>questions</i>", "El tiempo en Lyon: <i>preguntas</i>", "מזג האוויר בליון: <i>שאלות</i>"), items=faq),
            dict(type="cta", txt=_("Want a Lyon visit and Shabbat planned around the weather?", "Envie d’une visite à Lyon et d’un Shabbat organisés selon le temps ?", "¿Quiere una visita a Lyon y un Shabat organizados según el tiempo?", "רוצים סיור בליון ושבת מתוכננים לפי מזג האוויר?"), msg=WA_MSG[L]),
        ],
        related=[("../things-to-do-in-lyon/", _("Things to do in Lyon", "Que faire à Lyon", "Qué hacer en Lyon", "מה לעשות בליון")),
                 ("../tours/jewish-lyon/", _("Jewish Lyon tour, 2 h 30", "Visite du Lyon juif, 2 h 30", "Visita del Lyon judío, 2 h 30", "סיור ליון היהודית, שעתיים וחצי")),
                 ("../shabbat-in-lyon/", _("Shabbat in Lyon", "Shabbat à Lyon", "Shabat en Lyon", "שבת בליון")),
                 ("../where-to-stay-lyon-jewish-travellers/", _("Where to stay in Lyon", "Où loger à Lyon", "Dónde alojarse en Lyon", "איפה לישון בליון")),
                 ("../kosher-van-transfers/", _("Van and transfers", "Van et transferts", "Furgoneta y traslados", "ואן והסעות")),
                 ("../alps/", _("The Alps, strictly kosher", "Les Alpes, strictement casher", "Los Alpes, estrictamente kosher", "האלפים, כשר לחלוטין"))],
        jsonld=None, ticket=True,
        VERIF=[
            "Températures, pluie et jours de pluie : fiche climatologique Météo-France de Lyon-Bron, normales 1991-2020, station à 202 m d'altitude, lue le 21/10/2026 (donneespubliques.meteofrance.fr/FichesClim/FICHECLIM_69029001.pdf, recoupée avec la page Wikipédia Lyon). Les 12 mois du tableau sont copiés tels quels.",
            "Jours à 30 °C ou plus (juin 6,0, juillet 11,2, août 10,7), jours à Tx <= 0 °C (4,8 par an) et nuits à Tn <= 0 °C (42,4 par an, 10 à 13 par mois de décembre à février) : mêmes fiche et date. Les phrases « environ onze jours », « cinq jours par an » et « 42 nuits » en sont des arrondis.",
            "Bron est à l'est de Lyon et plus chaud que le Vieux Lyon de quelques dixièmes : la page le dit (station à 202 m, à l'est de la ville). Les moyennes ne prédisent pas une semaine donnée.",
            "Heures d'entrée de Chabbat « dès 16 h 30 en décembre, après 21 h en juin » : texte repris des pages Shabbat existantes (Hebcal, Lyon). L'encadré du jour est l'API Hebcal posée par _contacts_bh_hebcal.py.",
            "Prévisions à sept jours : API Open-Meteo sans clé, lue à chaque ouverture ; aucun chiffre de prévision n'est écrit dans le HTML. Si l'API échoue, repli texte vers Météo-France. Aucune règle CSP dans vercel.json, aucun ajout nécessaire.",
            "Les jours d'ouverture des musées cités dans « Organiser la journée selon le temps » viennent de la page things-to-do-in-lyon (sites officiels lus le 21/10/2026). Aucun prix, aucun numéro, aucun partenaire.",
            "Hébreu : traduit par Claude avec le lexique de relecture-hebreu, pas relu par un natif.",
        ],
    )


PAGE = page(0)
PAGE_FR = page(1)
PAGE_ES = page(2)
PAGE_HE = page(3)
