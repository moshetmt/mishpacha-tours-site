# -*- coding: utf-8 -*-
"""Textes du formulaire en etapes (14/10) : traductions (fr, es, he) des textes nouveaux.
   Les textes de la page du 13/10 (relus en 4 langues) sont dans _demande_textes.py (OLD, LAB, JSX)."""
import re
from _demande_textes import OLD, LAB, JSX

for _k in list(OLD):
    _m = re.match(r"\d+\. (.*)", _k)
    if _m: OLD[_m.group(1)] = tuple(re.sub(r"^\d+\. ", "", x) for x in OLD[_k])

NEW = {
"Step {n} of {t}": ("Étape {n} sur {t}", "Paso {n} de {t}", "שלב {n} מתוך {t}"),
"Code": ("Indicatif", "Prefijo", "קידומת"),
"Progress": ("Progression", "Progreso", "התקדמות"),
"Back": ("Retour", "Atrás", "חזרה"),
"Next": ("Suivant", "Siguiente", "הבא"),
"Edit": ("Modifier", "Modificar", "עריכה"),
"Fewer": ("Moins", "Menos", "פחות"),
"More": ("Plus", "Más", "יותר"),
"Your request so far": ("Votre demande jusqu'ici", "Su solicitud hasta ahora", "הבקשה שלכם עד כה"),
"Almost done": ("Presque terminé", "Casi listo", "כמעט סיימנו"),
"Check your answers, then tell us how to reach you.": ("Vérifiez vos réponses, puis dites-nous comment vous joindre.", "Revise sus respuestas y díganos cómo contactarle.", "בדקו את התשובות ואז ספרו לנו איך ליצור קשר."),
"Nothing filled in yet.": ("Rien n'est encore rempli.", "Todavía no ha completado nada.", "עוד לא מילאתם כלום."),
"This form needs JavaScript. Write to us on WhatsApp instead.": ("Ce formulaire demande JavaScript. Écrivez-nous plutôt sur WhatsApp.", "Este formulario necesita JavaScript. Escríbanos mejor por WhatsApp.", "הטופס דורש JavaScript. כתבו לנו בוואטסאפ."),
"Language we should answer in": ("Langue de notre réponse", "Idioma de nuestra respuesta", "שפת התשובה שלנו"),
"How soon?": ("Dans quel délai ?", "¿En qué plazo?", "תוך כמה זמן?"),
# intention
"What can we do for you?": ("Que pouvons-nous faire pour vous ?", "¿Qué podemos hacer por usted?", "במה נוכל לעזור?"),
"Pick the closest one. The next questions depend on it.": ("Choisissez le plus proche. Les questions suivantes en dépendent.", "Elija la opción más cercana. Las siguientes preguntas dependen de ella.", "בחרו את הקרוב ביותר. השאלות הבאות תלויות בבחירה."),
"A full stay in the Alps": ("Un séjour complet dans les Alpes", "Una estancia completa en los Alpes", "שהייה מלאה באלפים"),
"Chalet, chef, Shabbat, minyan and transfers, all organised.": ("Chalet, chef, Shabbat, minyan et transferts, tout organisé.", "Chalé, chef, Shabat, minyan y traslados, todo organizado.", "צ'אלה, שף, שבת, מניין והסעות, הכול מאורגן."),
"I already have my accommodation": ("J'ai déjà mon logement", "Ya tengo mi alojamiento", "כבר יש לנו לינה"),
"Minyan, Sefer Torah, Shabbat and meals where you stay.": ("Minyan, Sefer Torah, Shabbat et repas là où vous logez.", "Minyan, Séfer Torá, Shabat y comidas donde se aloja.", "מניין, ספר תורה, שבת וארוחות במקום שבו אתם לנים."),
"Services where we already stay (minyan, Sefer Torah, meals)": ("Services là où nous logeons déjà (minyan, Sefer Torah, repas)", "Servicios donde ya nos alojamos (minyan, Séfer Torá, comidas)", "שירותים במקום שבו אנחנו כבר לנים (מניין, ספר תורה, ארוחות)"),
"A van transfer": ("Un transfert en van", "Un traslado en van", "הסעה בוואן"),
"From point A to point B, with a driver.": ("D'un point A à un point B, avec chauffeur.", "De un punto A a un punto B, con conductor.", "מנקודה א׳ לנקודה ב׳, עם נהג."),
"A Jewish Lyon tour": ("Une visite du Lyon juif", "Una visita del Lyon judío", "סיור בעקבות יהדות ליון"),
"A guided walk in English, French or Spanish.": ("Une visite guidée en anglais, en français ou en espagnol.", "Una visita guiada en inglés, francés o español.", "סיור מודרך באנגלית, בצרפתית או בספרדית."),
"Pesach or a holiday": ("Pessah ou une fête", "Pésaj o una fiesta", "פסח או חג"),
"A full programme for the holiday, at the kosher standard you keep.": ("Un programme complet pour la fête, au niveau de cacherout que vous suivez.", "Un programa completo para la fiesta, con el nivel de kashrut que usted sigue.", "תוכנית מלאה לחג, ברמת הכשרות שאתם שומרים."),
"Holiday programme (Pesach or other)": ("Programme de fête (Pessah ou autre)", "Programa de fiesta (Pésaj u otra)", "תוכנית חג (פסח או אחר)"),
"Tell us in your own words.": ("Dites-le avec vos mots.", "Cuéntenoslo con sus palabras.", "ספרו לנו במילים שלכם."),
# sejour complet
"What kind of stay, and where?": ("Quel type de séjour, et où ?", "¿Qué tipo de estancia y dónde?", "איזו שהייה, ואיפה?"),
"Tick everything that applies. A region is enough.": ("Cochez tout ce qui convient. Une région suffit.", "Marque todo lo que corresponda. Una región basta.", "סמנו כל מה שמתאים. אזור מספיק."),
"When do you travel?": ("Quand partez-vous ?", "¿Cuándo viaja?", "מתי אתם נוסעים?"),
"Who is coming?": ("Qui vient ?", "¿Quiénes viajan?", "מי מגיע?"),
"Children": ("Enfants", "Niños", "ילדים"),
"Babies": ("Bébés", "Bebés", "תינוקות"),
"Ages of the children": ("Âges des enfants", "Edades de los niños", "גילאי הילדים"),
"9 and 12": ("9 et 12 ans", "9 y 12 años", "9 ו-12"),
"Ages of the babies": ("Âges des bébés", "Edades de los bebés", "גילאי התינוקות"),
"10 months": ("10 mois", "10 meses", "10 חודשים"),
"Pick what suits you. We advise if you are not sure.": ("Choisissez ce qui vous convient. Nous vous conseillons si vous hésitez.", "Elija lo que le convenga. Le aconsejamos si no está seguro.", "בחרו מה שמתאים. נייעץ לכם אם אתם לא בטוחים."),
"Which meals do you need?": ("De quels repas avez-vous besoin ?", "¿Qué comidas necesita?", "אילו ארוחות אתם צריכים?"),
"No meals needed": ("Pas besoin de repas", "No necesitamos comidas", "אין צורך בארוחות"),
"Which days?": ("Quels jours ?", "¿Qué días?", "אילו ימים?"),
"Shabbat only, or every day from 25 July to 15 August": ("Seulement Shabbat, ou tous les jours du 25 juillet au 15 août", "Solo Shabat, o todos los días del 25 de julio al 15 de agosto", "רק שבת, או כל יום מ-25 ביולי עד 15 באוגוסט"),
"Your kashrut standard": ("Votre niveau de cacherout", "Su nivel de kashrut", "רמת הכשרות שלכם"),
"Tick what you keep. We follow it exactly.": ("Cochez ce que vous suivez. Nous l'appliquons à la lettre.", "Marque lo que usted sigue. Lo aplicamos al pie de la letra.", "סמנו מה שאתם שומרים. נקפיד על כך."),
"A visit in Lyon?": ("Une visite à Lyon ?", "¿Una visita en Lyon?", "ביקור בליון?"),
"Tick the visits that interest you. Tours are held in English, French or Spanish.": ("Cochez les visites qui vous intéressent. Les visites se font en anglais, en français ou en espagnol.", "Marque las visitas que le interesen. Las visitas se hacen en inglés, francés o español.", "סמנו את הסיורים שמעניינים אתכם. הסיורים מתקיימים באנגלית, בצרפתית או בספרדית."),
"Language of the visit": ("Langue de la visite", "Idioma de la visita", "שפת הסיור"),
"Extras and budget": ("Extras et budget", "Extras y presupuesto", "תוספות ותקציב"),
"Everything here is optional.": ("Tout est facultatif ici.", "Todo es opcional aquí.", "הכול כאן לא חובה."),
# j'ai deja mon logement
"Where are you staying?": ("Où logez-vous ?", "¿Dónde se aloja?", "איפה אתם לנים?"),
"The resort and the address of your chalet, apartment or hotel.": ("La station et l'adresse de votre chalet, appartement ou hôtel.", "La estación y la dirección de su chalé, apartamento u hotel.", "האתר והכתובת של הצ'אלה, הדירה או המלון."),
"Resort or town": ("Station ou ville", "Estación o ciudad", "אתר או עיר"),
"Morzine, Châtel, Les Deux Alpes": ("Morzine, Châtel, Les Deux Alpes", "Morzine, Châtel, Les Deux Alpes", "מורזין, שאטל, לה דז אלפ"),
"Address or name of the accommodation": ("Adresse ou nom du logement", "Dirección o nombre del alojamiento", "כתובת או שם של הלינה"),
"Chalet Le Sapin, 12 route du Lac": ("Chalet Le Sapin, 12 route du Lac", "Chalet Le Sapin, 12 route du Lac", "Chalet Le Sapin, 12 route du Lac"),
# fete
"Which holiday?": ("Quelle fête ?", "¿Qué fiesta?", "איזה חג?"),
"Tick the holiday or holidays, and the place if you know it.": ("Cochez la ou les fêtes, et le lieu si vous le connaissez.", "Marque la fiesta o las fiestas, y el lugar si lo conoce.", "סמנו את החג או החגים, ואת המקום אם אתם יודעים."),
"Sukkot": ("Souccot", "Sucot", "סוכות"),
"Rosh Hashanah and Yom Kippur": ("Roch Hachana et Yom Kippour", "Rosh Hashaná y Yom Kipur", "ראש השנה ויום כיפור"),
"Purim": ("Pourim", "Purim", "פורים"),
"Shavuot": ("Chavouot", "Shavuot", "שבועות"),
"Another holiday": ("Une autre fête", "Otra fiesta", "חג אחר"),
# van
"Where from, and where to?": ("D'où, et vers où ?", "¿Desde dónde y hasta dónde?", "מאיפה ולאן?"),
"Address, airport, station or hotel. A town name is enough.": ("Adresse, aéroport, gare ou hôtel. Un nom de ville suffit.", "Dirección, aeropuerto, estación u hotel. Basta el nombre de la ciudad.", "כתובת, שדה תעופה, תחנה או מלון. שם עיר מספיק."),
"Pick-up point": ("Point de prise en charge", "Punto de recogida", "נקודת איסוף"),
"Lyon Saint-Exupéry airport": ("Aéroport de Lyon Saint-Exupéry", "Aeropuerto de Lyon Saint-Exupéry", "שדה התעופה ליון סן-אקזופרי"),
"Drop-off point": ("Point d'arrivée", "Punto de destino", "נקודת יעד"),
"Les Deux Alpes, chalet": ("Les Deux Alpes, chalet", "Les Deux Alpes, chalé", "לה דז אלפ, צ'אלה"),
"When?": ("Quand ?", "¿Cuándo?", "מתי?"),
"Date and pick-up time. Add the flight if you land.": ("Date et heure de prise en charge. Ajoutez le vol si vous atterrissez.", "Fecha y hora de recogida. Añada el vuelo si aterriza.", "תאריך ושעת איסוף. הוסיפו את הטיסה אם אתם נוחתים."),
"Date": ("Date", "Fecha", "תאריך"),
"Pick-up time": ("Heure de prise en charge", "Hora de recogida", "שעת איסוף"),
"Luggage and equipment": ("Bagages et équipement", "Equipaje y material", "מטען וציוד"),
"Skis and baby seats change the vehicle we send.": ("Les skis et les sièges bébé changent le véhicule envoyé.", "Los esquís y las sillas para bebé cambian el vehículo que enviamos.", "מגלשי סקי וכיסאות תינוק משנים את הרכב שנשלח."),
"Large suitcases": ("Grandes valises", "Maletas grandes", "מזוודות גדולות"),
"Cabin bags only": ("Bagages cabine seulement", "Solo equipaje de mano", "רק תיקי יד"),
"Skis or snowboards": ("Skis ou snowboards", "Esquís o snowboards", "מגלשי סקי או סנובורד"),
"Baby seats or boosters": ("Sièges bébé ou rehausseurs", "Sillas para bebé o elevadores", "כיסאות תינוק או מושבי הגבהה"),
"Wheelchair or walker": ("Fauteuil roulant ou déambulateur", "Silla de ruedas o andador", "כיסא גלגלים או הליכון"),
# message
"Anything else we should know?": ("Autre chose à nous dire ?", "¿Algo más que debamos saber?", "עוד משהו שכדאי שנדע?"),
"Anything that helps: a baby, a late arrival, a special diet.": ("Tout ce qui aide : un bébé, une arrivée tardive, un régime particulier.", "Cualquier detalle útil: un bebé, una llegada tardía, una dieta especial.", "כל דבר שעוזר: תינוק, הגעה מאוחרת, תזונה מיוחדת."),
"Tell us what you have in mind": ("Dites-nous ce que vous avez en tête", "Cuéntenos qué tiene en mente", "ספרו לנו מה יש לכם בראש"),
"Write it the way you would say it. We take it from there.": ("Écrivez-le comme vous le diriez. Nous prenons le relais.", "Escríbalo como lo diría. Nosotros seguimos desde ahí.", "כתבו את זה כמו שהייתם אומרים. אנחנו נמשיך משם."),
"A bar mitzvah weekend in the Alps for 30 guests": ("Un week-end de bar mitsva dans les Alpes pour 30 invités", "Un fin de semana de bar mitzvá en los Alpes para 30 invitados", "סוף שבוע בר מצווה באלפים ל-30 אורחים"),
}

# cles de recapitulatif ajoutees : (EN, FR, ES, HE)
LAB_NEW = {
"adresse": ("Accommodation address", "Adresse du logement", "Dirección del alojamiento", "כתובת הלינה"),
"van_depart": ("Pick-up", "Prise en charge", "Recogida", "איסוף"),
"van_arrivee": ("Drop-off", "Destination", "Destino", "יעד"),
"heure": ("Time", "Heure", "Hora", "שעה"),
"bagages": ("Luggage", "Bagages", "Equipaje", "מטען"),
"repas_jours": ("Meal days", "Jours de repas", "Días de comidas", "ימי ארוחות"),
}

LANGS = ("en", "fr", "es", "he")

def t(en, lang):
    if lang == "en": return en
    i = LANGS.index(lang) - 1
    src = NEW.get(en) or OLD.get(en)
    if src is None: raise KeyError("texte non traduit : " + en)
    return src[i]
