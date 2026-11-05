# -*- coding: utf-8 -*-
"""Genere le formulaire de /plan-your-trip/ (4 langues) : 3 ecrans en charte « Louis Vuitton » (Moshe 02/11, 22 h 30).
   python _build_demande.py (depuis site-v5/), puis python _prefill_court.py, puis python _charte_lv.py sur les 4 pages.
   1. « What can we do for you? » : 6 lignes a picto de la famille Mishpacha (img/illus/famille/form/, _demande_pictos.py), un toucher avance.
   2. « Where, when, how many? » : lieu, dates, souplesse, groupe, champs du van ou de la visite ; le reste de l'ancien tunnel
      (logement, repas, minyan, voyage, activites, Lyon, extras) en sections repliees facultatives, selon le choix de l'ecran 1.
   3. « Your contact » : prenom, WhatsApp (indicatif en liste preremplie), e-mail facultatif ; budget et derniers points replies ; accord ; envoi.
   Envoi vers le meme Apps Script, MEMES cles JSON et MEMES libelles anglais dans message_en qu'avant le 02/11 (la feuille, le mail,
   le PDF et l'Espace Mendel lisent ces libelles : « Resort or place », « Arrival », « Adults »...). Seul changement : plus de champ
   « Last name », la cle nom porte le prenom. Reponses gardees en localStorage (30 jours), effacees a l'envoi.
   Les textes viennent de _demande_textes.py et _demande_nouveaux.py. Ancienne version (7 ecrans) : historique git."""
from _head import head_page, webpage, crumbs, BASE
from _demande_nouveaux import t, LAB, LAB_NEW, JSX
import re, os, json, html, io

LANGS = ("en", "fr", "es", "he")
LAB_NEW["torah_niveau"] = ("Sefer Torah", "Sefer Torah", "Séfer Torá", "ספר תורה")
LAB_NEW["shabbat_niveau"] = ("Shabbat meals", "Repas de Chabbat", "Comidas de Shabat", "ארוחות שבת")
LAB_NEW["eruv_niveau"] = ("Eruv and mikveh", "Érouv et mikvé", "Eruv y mikve", "עירוב ומקווה")
LAB_NEW["mois"] = ("Months", "Mois", "Meses", "חודשים")
LAB_NEW["budget_fit"] = ("Budget fit", "Adéquation du budget", "Ajuste del presupuesto", "התאמת התקציב")   # 03/11 : ligne ajoutee au message, ignoree par fiche_() de Code.gs (libelle inconnu = resume seulement)
LOCALE = {"en": "en-GB", "fr": "fr-FR", "es": "es-ES", "he": "he-IL"}
MERCI = {"en": "/merci/", "fr": "/fr/merci/", "es": "/es/merci/", "he": "/he/merci/"}

FIL = {"en": ('<a href="../">Home</a>', "Plan your trip"), "fr": ('<a href="/fr/">Accueil</a>', "Préparer votre voyage"),
       "es": ('<a href="/es/">Inicio</a>', "Planifique su viaje"), "he": ('<a href="/he/">ראשי</a>', "תכננו את הטיול")}

# 02/11 : textes neufs du formulaire en 3 ecrans (EN, FR, ES, HE ; hebreu relu selon le skill relecture-hebreu)
NEUF = {
    "Where, when, how many?": ("Où, quand, combien ?", "¿Dónde, cuándo, cuántos?", "איפה, מתי, כמה?"),
    "Your contact": ("Vos coordonnées", "Sus datos de contacto", "פרטי הקשר שלכם"),
    "We answer you on WhatsApp.": ("Nous vous répondons sur WhatsApp.", "Le respondemos por WhatsApp.", "נחזור אליכם בוואטסאפ."),
    "We answer you on WhatsApp the same day.": ("Nous vous répondons sur WhatsApp le jour même.", "Le respondemos por WhatsApp el mismo día.", "נחזור אליכם בוואטסאפ באותו היום."),
    "Not chosen yet, advise us": ("Pas encore choisi, conseillez-nous", "Aún sin elegir, aconséjennos", "עוד לא בחרנו, ייעצו לנו"),
    "More details (optional)": ("Plus de détails (facultatif)", "Más detalles (opcional)", "פרטים נוספים (לא חובה)"),
    "Accommodation": ("Hébergement", "Alojamiento", "לינה"),
    "Budget and priorities": ("Budget et priorités", "Presupuesto y prioridades", "תקציב וסדרי עדיפויות"),
    "A few more things": ("Encore quelques points", "Algunas cosas más", "עוד כמה דברים"),
    "Which holiday?": ("Quelle fête ?", "¿Qué fiesta?", "איזה חג?"),
    "Continue": ("Continuer", "Continuar", "המשיכו"),
    "Total budget for the stay, if you have one": ("Budget total du séjour, si vous en avez un", "Presupuesto total de la estancia, si tiene uno", "התקציב הכולל לשהות, אם יש לכם"),
    "The total budget for the whole stay and the whole group, for example 15,000 €.": ("Le budget total du séjour pour tout le groupe, par exemple 15 000 €.", "El presupuesto total de la estancia para todo el grupo, por ejemplo 15.000 €.", "התקציב הכולל לכל השהות ולכל הקבוצה, לדוגמה 15,000 €."),
    "Where would you like to stay?": ("Où souhaitez-vous séjourner ?", "¿Dónde le gustaría alojarse?", "איפה תרצו לשהות?"),
    "Choose a resort, or let us advise you.": ("Choisissez une station, ou laissez-nous vous conseiller.", "Elija una estación o déjenos aconsejarle.", "בחרו אתר, או תנו לנו לייעץ לכם."),
    "Another resort": ("Une autre station", "Otra estación", "אתר אחר"),
    "When are you coming?": ("Quand venez-vous ?", "¿Cuándo vienen?", "מתי אתם מגיעים?"),
    "Approximate dates are fine.": ("Des dates approximatives suffisent.", "Las fechas aproximadas sirven.", "תאריכים משוערים זה בסדר."),
    "Your stay and meals": ("Votre hébergement et vos repas", "Su alojamiento y sus comidas", "הלינה והארוחות"),
    "Meals": ("Repas", "Comidas", "ארוחות"),
    "Minyan and Shabbat": ("Minyan et Chabbat", "Minyan y Shabat", "מניין ושבת"),
    "Your budget and your wishes": ("Votre budget et vos envies", "Su presupuesto y sus deseos", "התקציב והבקשות שלכם"),
    "Both are optional.": ("Les deux sont facultatifs.", "Ambos son opcionales.", "שניהם לא חובה."),
    "Anything else?": ("Autre chose ?", "¿Algo más?", "עוד משהו?"),
    "Morzine, Zermatt, Verbier": ("Morzine, Zermatt, Verbier", "Morzine, Zermatt, Verbier", "צרמט, סנט מוריץ"),
    "Flying to Grenoble": ("Vol vers Grenoble", "Vuelo a Grenoble", "טסים לגרנובל"),
    "Another airport, or not sure yet": ("Un autre aéroport, ou pas encore décidé", "Otro aeropuerto, o aún no decidido", "שדה תעופה אחר, או שעוד לא החלטנו"),
    "Build your stay": ("Composez votre séjour", "Diseñe su estancia", "בנו את החופשה שלכם"),
    "Add everything you would like. We confirm each service with you.": ("Ajoutez tout ce qui vous ferait plaisir. Nous confirmons chaque service avec vous.", "Añada todo lo que le apetezca. Confirmamos cada servicio con usted.", "הוסיפו כל מה שתרצו. נאשר איתכם כל שירות."),
    "+ Add": ("+ Ajouter", "+ Añadir", "+ הוספה"),
    "Added ✓": ("Ajouté ✓", "Añadido ✓", "נוסף ✓"),
    "1 service added": ("1 service ajouté", "1 servicio añadido", "שירות אחד נוסף"),
    "{n} services added": ("{n} services ajoutés", "{n} servicios añadidos", "{n} שירותים נוספו"),
    "Private chalet": ("Chalet privé", "Chalé privado", "צ'אלה פרטית"),
    "Kosher chalets with the Winter Prestige team.": ("Des chalets casher avec l'équipe Winter Prestige.", "Chalés kosher con el equipo de Winter Prestige.", "צ'אלות כשרות עם הצוות של Winter Prestige"),
    "Private chef": ("Chef privé", "Chef privado", "שף פרטי"),
    "A kosher chef cooks every meal in your chalet.": ("Un chef casher cuisine tous vos repas au chalet.", "Un chef kosher cocina todas sus comidas en el chalé.", "שף כשר מבשל את כל הארוחות בצ'אלה."),
    "Meals delivered": ("Repas livrés", "Comidas a domicilio", "ארוחות במשלוח"),
    "Ready-to-heat kosher meals, delivered every two days.": ("Des repas casher prêts à réchauffer, livrés tous les deux jours.", "Comidas kosher listas para calentar, entregadas cada dos días.", "ארוחות כשרות מוכנות לחימום, במשלוח כל יומיים."),
    "Shabbat meals": ("Repas de Chabbat", "Comidas de Shabat", "ארוחות שבת"),
    "Friday dinner, Saturday lunch and seuda shlishit.": ("Dîner du vendredi, déjeuner du samedi et seouda chlichit.", "Cena del viernes, almuerzo del sábado y seudá shlishit.", "ארוחת ליל שבת, סעודת שבת וסעודה שלישית."),
    "Private minyan and Sefer Torah": ("Minyan privé et Sefer Torah", "Minyan privado y Séfer Torá", "מניין פרטי וספר תורה"),
    "We gather the minyan and bring a Sefer Torah to your chalet.": ("Nous réunissons le minyan et apportons un Sefer Torah au chalet.", "Reunimos el minyan y llevamos un Séfer Torá al chalé.", "אנחנו מארגנים מניין ומביאים ספר תורה לצ'אלה."),
    "Private butler": ("Majordome privé", "Mayordomo privado", "באטלר פרטי"),
    "A butler at your service in the chalet.": ("Un majordome à votre service au chalet.", "Un mayordomo a su servicio en el chalé.", "באטלר לשירותכם בצ'אלה."),
    "Airport transfer by van": ("Transfert aéroport en van", "Traslado en van desde el aeropuerto", "הסעה בוואן משדה התעופה"),
    "From Lyon or Geneva airport to your door, with a driver.": ("De l'aéroport de Lyon ou de Genève jusqu'à votre porte, avec chauffeur.", "Del aeropuerto de Lyon o Ginebra hasta su puerta, con conductor.", "משדה התעופה של ליון או ז'נבה עד הדלת, עם נהג."),
    "Ski lessons, equipment, passes": ("Cours, matériel et forfaits de ski", "Clases, material y forfaits de esquí", "שיעורי סקי, ציוד וכרטיסי מעליות"),
    "Instructors, rental delivered to the chalet, passes ready.": ("Moniteurs, matériel livré au chalet, forfaits prêts.", "Monitores, material entregado en el chalé, forfaits listos.", "מדריכים, ציוד שמגיע לצ'אלה, כרטיסים מוכנים."),
    "Snowmobile or dog sledding": ("Motoneige ou chiens de traîneau", "Moto de nieve o trineo de perros", "אופנוע שלג או מזחלת כלבים"),
    "Activities": ("Activités", "Actividades", "פעילויות"),
    "Snowmobile, dog sledding.": ("Motoneige, chiens de traîneau.", "Moto de nieve, trineo de perros.", "אופנוע שלג, מזחלת כלבים."),
    "Guided, 2 hours, before or after the Alps.": ("Visite guidée de 2 h, avant ou après les Alpes.", "Visita guiada de 2 horas, antes o después de los Alpes.", "סיור מודרך של שעתיים, לפני או אחרי האלפים."),
    "Your budget": ("Votre budget", "Su presupuesto", "התקציב שלכם"),
    "From about {x} for your selection": ("À partir d'environ {x} pour votre sélection", "Desde unos {x} para su selección", "החל מכ־{x} לבחירה שלכם"),
    ", plus services on request.": (", plus les services sur demande.", ", más los servicios a consultar.", ", ועוד שירותים לפי בקשה."),
    "Your selection is a large project: we will build it with you.": ("Votre sélection est un beau projet : nous le construirons avec vous.", "Su selección es un gran proyecto: lo construiremos con usted.", "הבחירה שלכם היא פרויקט גדול: נבנה אותו יחד איתכם."),
    "Add your dates to see an estimate.": ("Ajoutez vos dates pour voir une estimation.", "Añada sus fechas para ver una estimación.", "הוסיפו תאריכים כדי לראות הערכה."),
    "Your budget fits your selection.": ("Votre budget correspond à votre sélection.", "Su presupuesto se ajusta a su selección.", "התקציב שלכם מתאים לבחירה שלכם."),
    "With this budget we will suggest the closest option (delivered meals instead of a chef, for example).": ("Avec ce budget, nous vous proposerons l'option la plus proche (des repas livrés plutôt qu'un chef, par exemple).", "Con este presupuesto le propondremos la opción más cercana (comidas a domicilio en lugar de un chef, por ejemplo).", "עם התקציב הזה נציע לכם את האפשרות הקרובה ביותר (למשל ארוחות במשלוח במקום שף)."),
    "This is below what a private kosher stay in the Alps costs. We may not be able to help; consider delivered meals or an apartment.": ("C'est en dessous du prix d'un séjour casher privé dans les Alpes. Nous risquons de ne pas pouvoir vous aider ; pensez aux repas livrés ou à un appartement.", "Está por debajo de lo que cuesta una estancia kosher privada en los Alpes. Es posible que no podamos ayudarle; piense en comidas a domicilio o en un apartamento.", "זה פחות ממה שעולה חופשה כשרה פרטית באלפים. ייתכן שלא נוכל לעזור; שקלו ארוחות במשלוח או דירה."),
    "fits": ("correspond", "se ajusta", "מתאים"),
    "below": ("en dessous", "por debajo", "מתחת"),
    "far below": ("très en dessous", "muy por debajo", "הרבה מתחת"),
    "estimate": ("estimation", "estimación", "הערכה"),
    "For your {g} guests, {n} {p}, with {s}, plan from about {x}": ("Pour vos {g} voyageurs, {n} {p}, avec {s}, comptez à partir d'environ {x}", "Para sus {g} viajeros, {n} {p}, con {s}, cuente desde unos {x}", "ל־{g} האורחים שלכם, {n} {p}, עם {s}: החל מכ־{x}"),
    "For your {g} guests, {n} {p}. Add services to see a starting price.": ("Pour vos {g} voyageurs, {n} {p}. Ajoutez des services pour voir un prix de départ.", "Para sus {g} viajeros, {n} {p}. Añada servicios para ver un precio de partida.", "ל־{g} האורחים שלכם, {n} {p}. הוסיפו שירותים כדי לראות מחיר התחלתי."),
    ", plus services on request": (", plus les services sur demande", ", más los servicios a consultar", ", ועוד שירותים לפי בקשה"),
    "in {p}": ("à {p}", "en {p}", "ב־{p}"),
    "in the Alps": ("dans les Alpes", "en los Alpes", "באלפים"),
    " or ": (" ou ", " o ", " או "),
    " and ": (" et ", " y ", " ו"),
    "a week": ("une semaine", "una semana", "שבוע"),
    "a chalet": ("un chalet", "un chalé", "צ'אלה"),
    "a private chef": ("un chef privé", "un chef privado", "שף פרטי"),
    "delivered meals": ("des repas livrés", "comidas a domicilio", "ארוחות במשלוח"),
    "the Lyon tour": ("la visite de Lyon", "la visita de Lyon", "הסיור בליון"),
    "A very busy period: the best chalets go early.": ("Une période très demandée : les plus beaux chalets partent tôt.", "Un periodo muy solicitado: los mejores chalés se reservan pronto.", "תקופה עמוסה מאוד: הצ'אלות היפות נתפסות מוקדם."),
    "One of the most sought-after resorts in the Alps.": ("L'une des stations les plus recherchées des Alpes.", "Una de las estaciones más buscadas de los Alpes.", "אחד האתרים המבוקשים ביותר באלפים."),
    "For a large group we combine chalets.": ("Pour un grand groupe, nous associons plusieurs chalets.", "Para un grupo grande, combinamos varios chalés.", "לקבוצה גדולה אנחנו משלבים כמה צ'אלות."),
    "Below this": ("En dessous", "Por debajo", "פחות מזה"),
    "Around this": ("À peu près", "Más o menos", "בסביבות זה"),
    "Above this": ("Au-dessus", "Por encima", "יותר מזה"),
    "I'd rather discuss it": ("J'aimerais en parler", "Prefiero hablarlo", "מעדיפים לדבר על זה"),
    "Thank you. We will suggest the closest option:": ("Merci. Nous vous proposerons l'option la plus proche :", "Gracias. Le propondremos la opción más cercana:", "תודה. נציע לכם את האפשרות הקרובה ביותר:"),
    "delivered meals instead of a private chef": ("des repas livrés plutôt qu'un chef privé", "comidas a domicilio en lugar de un chef privado", "ארוחות במשלוח במקום שף פרטי"),
    "a resort with lower prices, such as Val Thorens": ("une station aux prix plus doux, comme Val Thorens", "una estación con precios más suaves, como Val Thorens", "אתר במחירים נוחים יותר, כמו ואל טורנס"),
    "an apartment instead of a private chalet": ("un appartement plutôt qu'un chalet privé", "un apartamento en lugar de un chalé privado", "דירה במקום צ'אלה פרטית"),
    "a shorter stay or fewer services": ("un séjour plus court ou moins de services", "una estancia más corta o menos servicios", "שהות קצרה יותר או פחות שירותים"),
    "Perfect: we will build your stay around this.": ("Parfait : nous construirons votre séjour autour de ce budget.", "Perfecto: construiremos su estancia en torno a este presupuesto.", "מצוין: נבנה את החופשה סביב התקציב הזה."),
    "Wonderful: we can add every comfort you wish.": ("Merveilleux : nous pourrons ajouter tout le confort que vous souhaitez.", "Maravilloso: podremos añadir todas las comodidades que desee.", "נהדר: נוכל להוסיף כל פינוק שתרצו."),
    "We'll talk it through on WhatsApp.": ("Nous en parlerons ensemble sur WhatsApp.", "Lo hablaremos juntos por WhatsApp.", "נדבר על זה יחד בוואטסאפ."),
    "around": ("à peu près", "más o menos", "בסביבות"),
    "above": ("au-dessus", "por encima", "מעל"),
    "discuss": ("à discuter", "a hablar", "לשיחה"),
    "Your budget, if you have one": ("Votre budget, si vous en avez un", "Su presupuesto, si lo tiene", "התקציב שלכם, אם יש"),
    "I already have my place": ("J'ai déjà mon logement", "Ya tengo mi alojamiento", "כבר יש לנו לינה"),
    "Where are you staying?": ("Où logez-vous ?", "¿Dónde se alojan?", "איפה אתם שוהים?"),
    "Choose one resort or several, or let us advise you.": ("Une ou plusieurs stations, ou laissez-nous vous conseiller.", "Una o varias estaciones, o déjenos aconsejarle.", "אתר אחד או כמה, או תנו לנו לייעץ."),
    "Tell us the resort and the address.": ("Indiquez la station et l'adresse.", "Indíquenos la estación y la dirección.", "ספרו לנו את האתר ואת הכתובת."),
    "Which months?": ("Quels mois ?", "¿Qué meses?", "באילו חודשים?"),
    "November": ("Novembre", "Noviembre", "נובמבר"), "December": ("Décembre", "Diciembre", "דצמבר"), "January": ("Janvier", "Enero", "ינואר"),
    "February": ("Février", "Febrero", "פברואר"), "March": ("Mars", "Marzo", "מרץ"), "April": ("Avril", "Abril", "אפריל"), "Summer": ("Été", "Verano", "קיץ"),
    "A holiday during your stay?": ("Une fête pendant le séjour ?", "¿Una fiesta durante la estancia?", "חג בזמן השהות?"),
    "Tap everything you would like. We confirm each service with you.": ("Touchez tout ce qui vous ferait plaisir. Nous confirmons chaque service avec vous.", "Toque todo lo que le apetezca. Confirmamos cada servicio con usted.", "געו בכל מה שתרצו. נאשר איתכם כל שירות."),
    "Van transfer": ("Transfert en van", "Traslado en van", "הסעה בוואן"),
    "Ski": ("Ski", "Esquí", "סקי"),
    "Lyon tour": ("Visite de Lyon", "Visita de Lyon", "סיור בליון"),
    "Stay and meals": ("Séjour et repas", "Estancia y comidas", "לינה וארוחות"),
    "Extras": ("Extras", "Extras", "תוספות"),
    "Add what would make the stay perfect.": ("Ajoutez ce qui rendrait le séjour parfait.", "Añada lo que haría perfecta la estancia.", "הוסיפו את מה שיהפוך את החופשה למושלמת."),
    "In your dates: {f}": ("Dans vos dates : {f}", "En sus fechas: {f}", "בתאריכים שלכם: {f}"),
    "Not sure, advise me": ("Pas sûr, conseillez-moi", "No estoy seguro, aconséjenme", "לא בטוחים, ייעצו לנו"),
    "Edit": ("Modifier", "Editar", "עריכה"),
    "{n} guests": ("{n} voyageurs", "{n} viajeros", "{n} אורחים"),
    "By month": ("Par mois", "Por meses", "לפי חודש"),
    "I have exact dates": ("J'ai des dates précises", "Tengo fechas exactas", "יש לנו תאריכים מדויקים"),
    "Ski lessons": ("Cours de ski", "Clases de esquí", "שיעורי סקי"),
    "Ski equipment": ("Matériel de ski", "Material de esquí", "ציוד סקי"),
    "Massages": ("Massages", "Masajes", "עיסויים"),
    "Kitchen kashering": ("Cachérisation de la cuisine", "Kasherización de la cocina", "הכשרת המטבח"),
    "Minyan in the chalet": ("Minyan au chalet", "Minyan en el chalé", "מניין בצ'אלה"),
    "Sefer Torah for the Shabbat reading": ("Sefer Torah pour la lecture de Chabbat", "Séfer Torá para la lectura de Shabat", "ספר תורה לקריאה בשבת"),
    "Eruv and mikveh nearby": ("Érouv et mikvé à proximité", "Eruv y mikve cerca", "עירוב ומקווה בקרבת מקום"),
    "Essential": ("Indispensable", "Imprescindible", "הכרחי"),
    "We'll focus on what matters most: your kosher meals. Many families book their own apartment, and we take care of the meals, Shabbat and the minyan.": ("Nous nous concentrons sur l'essentiel : vos repas casher. Beaucoup de familles réservent leur propre appartement, et nous nous occupons des repas, du Chabbat et du minyan.", "Nos centramos en lo esencial: sus comidas kosher. Muchas familias reservan su propio apartamento y nosotros nos ocupamos de las comidas, el Shabat y el minyan.", "נתמקד במה שהכי חשוב: הארוחות הכשרות שלכם. משפחות רבות מזמינות דירה בעצמן, ואנחנו דואגים לארוחות, לשבת ולמניין."),
    "Switch to the essentials": ("Passer à l'essentiel", "Pasar a lo esencial", "לעבור לעיקר"),
    "Undo": ("Annuler", "Deshacer", "ביטול"),
    "below (essentials proposed)": ("en dessous (essentiel proposé)", "por debajo (lo esencial propuesto)", "מתחת (הוצע העיקר)"),
    "below (essentials chosen)": ("en dessous (essentiel choisi)", "por debajo (lo esencial elegido)", "מתחת (נבחר העיקר)"),
    "Optional.": ("Facultatif.", "Opcional.", "לא חובה."),
}
NEUF.update({   # 04/11 : parcours b en 3 ecrans, ecran « besoins »
    "What do you need?": ("De quoi avez-vous besoin ?", "¿Qué necesitan?", "מה אתם צריכים?"),
    "Shabbat meals only": ("Repas de Chabbat seulement", "Solo las comidas de Shabat", "ארוחות שבת בלבד"),
    "Private transfer": ("Transfert privé", "Traslado privado", "הסעה פרטית"),
    "Full stay": ("Séjour complet", "Estancia completa", "שהות מלאה"),
    "Change": ("Modifier", "Cambiar", "שינוי"),
})
def tt(s, lang):
    if s in NEUF: return s if lang == "en" else NEUF[s][LANGS.index(lang) - 1]
    return t(s, lang)

# 03/11 (Moshe : « Mendel change un prix dans sa grille, le formulaire suit ») : les prix viennent de la grille de Mendel, comme le reste du site.
# js/prix.js lit le JSON public (?prix=1, lignes cochees « Public ») et l'expose (window.MT_PRIX + evenement mt-prix) ; le JS du formulaire
# en tire les vignettes et l'estimation (fonction grille()). Les valeurs ci-dessous ne servent que de REPLI (grille muette ou ligne non publiee) :
# ce sont les prix deja publies sur le site au 30/10. Cles lues : ch1..ch11_basse_vente, c_chef_vente, r_soir_vente, r_vendredi/samedi/seouda_vente, l_zoneA_vente.
PRIX_N = {"chalet": 9500, "chef": 1568, "soir": 28, "livraison": 180, "shabbat": 115, "shab_min": 30, "shab_max": 45, "lyon": 290}   # shabbat = 45 + 40 + 30 (vendredi, samedi, seouda)
# vignettes : {a} (et {b}) = montants, remplaces par le JS quand la grille repond ; « lyon » n'est pas dans la grille de Mendel (visites de la guide)
PRIX_TPL = {
    "en": {"chalet": "from €{a} / week", "chef": "from €{a} / day", "soir": "from €{a} / person / day", "shabbat": "€{a} to €{b} / person / meal",
           "lyon": "€290 / group of 1 to 4", "demande": "On request", "from": "from €{a}"},
    "fr": {"chalet": "à partir de {a} € / semaine", "chef": "à partir de {a} € / jour", "soir": "à partir de {a} € / pers. / jour", "shabbat": "{a} à {b} € / pers. / repas",
           "lyon": "290 € / groupe de 1 à 4", "demande": "Sur demande", "from": "dès {a} €"},
    "es": {"chalet": "desde {a} € / semana", "chef": "desde {a} € / día", "soir": "desde {a} € / pers. / día", "shabbat": "{a} a {b} € / pers. / comida",
           "lyon": "290 € / grupo de 1 a 4", "demande": "A consultar", "from": "desde {a} €"},
    "he": {"chalet": 'החל מ־<bdi dir="ltr">{a} €</bdi> / שבוע', "chef": 'החל מ־<bdi dir="ltr">{a} €</bdi> / יום', "soir": 'החל מ־<bdi dir="ltr">{a} €</bdi> / אדם / יום',
           "shabbat": '<bdi dir="ltr">{a}–{b} €</bdi> / אדם / ארוחה', "lyon": '<bdi dir="ltr">290 €</bdi> / קבוצה של 1 עד 4', "demande": "לפי בקשה", "from": "החל מ־<bdi dir=\"ltr\">{a} €</bdi>"},
}
PRIX_AB = {"chalet": ("chalet", None), "chef": ("chef", None), "soir": ("soir", None), "shabbat": ("shab_min", "shab_max")}
def montant(n, lang):
    s = f"{int(n):,}"
    return s.replace(",", " " if lang == "fr" else "." if lang == "es" else ",")
def prix_vignette(lang, k):
    """<small> d'une vignette : texte de repli + data-pf / data-pf-tpl pour la mise a jour par la grille."""
    tpl = PRIX_TPL[lang][k].replace(" €", " €")   # montant et euro jamais separes
    if k not in PRIX_AB: return f"<small>{tpl}</small>"
    a, b = PRIX_AB[k]
    txt = tpl.replace("{a}", montant(PRIX_N[a], lang)).replace("{b}", montant(PRIX_N[b], lang) if b else "")
    return f'<small data-pf="{k}" data-pf-tpl="{html.escape(tpl, quote=True)}">{txt}</small>'

def hero(lang):
    T = lambda s: html.escape(tt(s, lang), quote=True)
    home, cur = FIL[lang]
    return ('<section class="pf-hero"><div class="wrap">\n'
            f'  <p class="fil">{home} / {cur}</p>\n'
            f'  <h1>{T("Plan your")} {T("kosher trip")}</h1>\n'
            f'  <p class="pf-promesse">{T("Answer a few questions. We send you a day-by-day programme with the price.")}</p>\n'
            '</div></section>')

# ---------------------------------------------------------------- le formulaire, par langue
# Branches : a sejour complet, b j'ai deja mon logement, c van, d Lyon, e fete, f autre. Trois ecrans pour toutes.
ALPES = ["ou", "quand", "qui", "services", "extras", "minyan", "budget", "final"]   # 03/11 : plus d'ecran « projet », Alpes par defaut
BESOINS_B = ["ou", "quand", "qui", "besoins", "final"]   # 04/11 : b = « j'ai deja mon logement » ; lien prerempli (i=b, lieu, arrivee) : ou et quand sautes, 3 ecrans
PATHS = {"a": ALPES, "b": BESOINS_B, "e": ALPES, "c": ["trajet", "quandvan", "qui", "budget", "final"],
         "d": ["lyon", "qui", "budget", "final"], "f": ["message", "ou", "quand", "qui", "budget", "final"]}
# prix de depart d'un chalet par station (« a partir de » publies sur /kosher-chalets/, semaine en basse saison) ; autres stations : 9 500 (le plus bas publie)
FETES_NOMS = {'Pesach in the Alps': ('Pesach', 'Pessah', 'Pésaj', 'פסח'), 'Hanukkah in the Alps': ('Hanukkah', 'Hanoucca', 'Janucá', 'חנוכה'), 'Sukkot': ('Sukkot', 'Souccot', 'Sucot', 'סוכות'), 'Rosh Hashanah and Yom Kippur': ('Rosh Hashanah and Yom Kippur', 'Roch Hachana et Yom Kippour', 'Rosh Hashaná y Yom Kipur', 'ראש השנה ויום כיפור'), 'Purim': ('Purim', 'Pourim', 'Purim', 'פורים'), 'Shavuot': ('Shavuot', 'Chavouot', 'Shavuot', 'שבועות')}
CHALET_BASE = {"Val Thorens": 9500, "Les Menuires": 9500, "Les Deux Alpes": 13000, "Courchevel": 17500, "Megève": 23500}
STATIONS_PRINC = ["Courchevel", "Val Thorens", "Les Menuires", "Tignes", "Megève", "Les Deux Alpes", "Val d'Isère", "Alpe d'Huez", "Chamonix", "Les Arcs", "La Plagne"]
STATIONS_HE = {"Courchevel": "קורשבל", "Val Thorens": "ואל טורנס", "Tignes": "טין", "Les Menuires": "לה מנואר", "Megève": "מג'ב", "Les Deux Alpes": "לה דז אלפ", "Val d'Isère": "ואל דיזר",
               "Alpe d'Huez": "אלפ ד'ואז", "Chamonix": "שמוני", "Les Arcs": "לז ארק", "La Plagne": "לה פלאן"}
LAB_ORDER = ["voyage", "lieu", "lieu_pas_choisi", "adresse", "van_depart", "van_arrivee", "aller_retour", "arrivee", "creneau", "depart", "heure", "retour_date", "retour_heure", "flexible", "mois", "familles", "adultes", "enfants", "bebes", "bebe_materiel", "hommes", "bagages",
             "logement", "chambres", "sdb", "logement_opt", "repas", "repas_jours", "allergies", "cacherout", "cacherout_detail", "minyan_niveau", "torah_niveau", "shabbat_niveau", "eruv_niveau", "religieux", "rite", "aeroport", "vol_ville", "vols_pris", "vol", "transport",
             "ski", "niveau", "lyon", "langue_visite", "extras", "budget_total", "budget_fit", "budget", "budget_vols", "priorites", "message", "ville", "urgence", "pour_qui"]
INDICATIFS = '<option value="">{code}</option>' + "".join(f'<option value="{v}">{v} {c}</option>' for v, c in [
    ("+1", "US / CA"), ("+44", "UK"), ("+972", "IL"), ("+33", "FR"), ("+32", "BE"), ("+41", "CH"), ("+34", "ES"), ("+39", "IT"), ("+49", "DE"), ("+31", "NL"),
    ("+54", "AR"), ("+52", "MX"), ("+55", "BR"), ("+61", "AU"), ("+27", "ZA"), ("+7", "RU"), ("+380", "UA")])
STATIONS = [("Courchevel",), ("Les Deux Alpes",), ("Megève",), ("Val Thorens",), ("Les Menuires",), ("Tignes",), ("Méribel",), ("Alpe d'Huez",), ("Chamonix",), ("Les Arcs",), ("La Plagne",), ("Val d'Isère",),
            ("Morzine",), ("Avoriaz",), ("Les Gets",), ("Châtel",), ("Montriond",), ("La Clusaz",), ("Saint-Gervais",), ("Combloux",), ("Serre Chevalier",), ("Flaine",), ("Samoëns",), ("La Rosière",),
            ("Annecy",), ("Grenoble",), ("Zermatt",), ("St. Moritz",), ("Crans-Montana",), ("Verbier",), ("Davos",), ("Gstaad",), ("Saas-Fee",), ("Cervinia",), ("Courmayeur",), ("Cortina d'Ampezzo",)]

def esc(s): return html.escape(s, quote=True)
def insec(s): return re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", s).replace(" \u20ac", "\u00a0\u20ac")   # montants jamais coupes

# 20/10 (C4, option A) : accord explicite, art. 9 RGPD (allergies = sante, minyan = pratique religieuse).
ACCORD = {
    "en": ("I agree that my answers (including allergies and religious observance) may be passed to the team in the Alps to prepare my quote.", "Privacy policy", "/privacy/", "Please tick this box so we can send your quote."),
    "fr": ("J'accepte que mes réponses (dont allergies et pratique religieuse) soient transmises à l'équipe des Alpes pour préparer mon devis.", "Politique de confidentialité", "/fr/privacy/", "Cochez cette case pour que nous puissions vous envoyer votre devis."),
    "es": ("Acepto que mis respuestas (incluidas las alergias y la práctica religiosa) se transmitan al equipo de los Alpes para preparar mi presupuesto.", "Política de privacidad", "/es/privacy/", "Marque esta casilla para que podamos enviarle su presupuesto."),
    "he": ("אני מסכים/ה שתשובותיי (כולל אלרגיות ושמירת מצוות) יועברו לצוות באלפים לצורך הכנת הצעת המחיר שלי.", "מדיניות הפרטיות", "/he/privacy/", "סמנו את התיבה כדי שנוכל לשלוח לכם את הצעת המחיר."),
}

def formulaire(lang):
    E = lambda s: esc(tt(s, lang))
    IMG = "../img/" if lang == "en" else "/img/"
    def battr(b): return f' data-b="{b}"' if b else ""
    def sattr(x): return f' data-s="{x}"' if x else ""
    def chips(name, opts, multi=True, b="", cls=""):
        """opts : texte EN, ou (texte EN, branches, cle, saison). saison : w = hiver seulement, s = ete seulement."""
        typ = "checkbox" if multi else "radio"
        out = []
        for o in opts:
            en, ob, k, sa = (o, "", "", "") if isinstance(o, str) else (o + ("", "", ""))[:4]
            kk = f' data-k="{k}"' if k else ""
            out.append(f'<label class="pf-c"{battr(ob)}{sattr(sa)}><input type="{typ}" name="{name}" value="{E(en)}" data-en="{esc(en)}"{kk}><span>{insec(E(en))}</span></label>')
        return f'<div class="pf-chips{" " + cls if cls else ""}"{battr(b)}>' + "".join(out) + "</div>"
    def champ(id_, name, label, typ="text", ph="", b="", extra="", sa=""):
        phh = f' placeholder="{E(ph)}"' if ph else ""
        return f'<div class="pf-champ"{battr(b)}{sattr(sa)}><label for="{id_}">{E(label)}</label><input type="{typ}" id="{id_}" name="{name}"{phh}{extra}></div>'
    def zone(id_, name, label, ph, b=""):
        return f'<div class="pf-champ"{battr(b)}><label for="{id_}">{E(label)}</label><textarea id="{id_}" name="{name}" rows="3" placeholder="{E(ph)}"></textarea></div>'
    def compteur(name, label, b="", v=0):
        return (f'<div class="pf-cpt"{battr(b)}><span class="lib" id="l-{name}">{E(label)}</span><div class="cpt">'
                f'<button type="button" class="moins" aria-label="{E("Fewer")}: {E(label)}">&#8722;</button>'
                f'<input type="number" id="c-{name}" name="{name}" min="0" max="99" value="{v}" inputmode="numeric" aria-labelledby="l-{name}">'
                f'<button type="button" class="plus" aria-label="{E("More")}: {E(label)}">+</button></div></div>')
    def ages(name, label, ph, opts=()):
        return (f'<div class="pf-champ pf-ages cache" data-for="{name}"><label for="c-{name}_ages">{E(label)}</label>'
                f'<input type="text" id="c-{name}_ages" name="{name}_ages" placeholder="{E(ph)}">' + (sugg(f"c-{name}_ages", opts) if opts else "") + '</div>')
    def sous(x, b=""): return f'<p class="pf-sous"{battr(b)}>{E(x)}</p>'
    def sugg(id_, opts, b="", sa=""):
        """Propositions pendant la saisie d'un champ libre (Moshe, 20/10). opts : texte EN traduit, ou ("texte",) brut."""
        out = []
        for o in opts:
            en, brut = (o, False) if isinstance(o, str) else (o[0], True)
            v = esc(en) if brut else E(en)
            out.append(f'<button type="button" data-v="{v}">{v}</button>')
        return f'<div class="pf-auto"{battr(b)}{sattr(sa)} data-for="{id_}" hidden>' + "".join(out) + "</div>"
    def si(cond, corps): return f'<div data-si="{esc(cond)}" hidden>{corps}</div>'
    def pli(titre, corps, b="", sa=""):
        """Section facultative repliee : un titre a toucher, le nombre de choix coches en badge."""
        return (f'<details class="pf-pli"{battr(b)}{sattr(sa)}><summary>{E(titre)}<span class="pf-pli-n" data-t="{E("{n} selected")}" hidden></span></summary>'
                f'<div class="pf-pli-c">{corps}</div></details>')
    def etape(id_, titres, aide, corps, cls="", avant=""):
        if isinstance(titres, str): titres = [(titres, "")]
        hs = "".join(f'<h2 tabindex="-1"{battr(b)}>{E(x)}</h2>' for x, b in titres)
        if isinstance(aide, str): aide = [(aide, "")]
        ps = "".join(f'<p{battr(b)}>{E(x)}</p>' for x, b in aide if x)
        return f'<div class="pf-etape {cls}" id="e-{id_}" data-e="{id_}" role="group">{avant}<div class="pf-tete">{hs}{ps}</div>{corps}</div>\n'

    # ================= 03/11 (Moshe) : plus d'ecran « projet ». Sejour dans les Alpes par defaut ; i= de l'adresse (pages Lyon, van, Pessah) choisit le parcours.
    # Les boutons radio « intention » restent, caches, pour envoyer la meme cle tour qu'avant.
    cache_int = ('<div class="pf-int" hidden>' + "".join(
        f'<input type="radio" name="intention" value="{v}" data-voyage="{E(voy)}" data-en="{esc(voy)}">' for v, voy in [
            ("a", "A full stay in the Alps"), ("b", "Services where we already stay (chef, meals, minyan, transfers)"), ("e", "Holiday programme (Pesach or other)"),
            ("d", "Jewish Lyon tour"), ("c", "Van transfer, point A to point B"), ("f", "Something else")]) + "</div>")
    S = []
    ou = ('<div class="pf-pastilles">' + "".join(
              f'<button type="button" class="pf-pas" aria-pressed="false" data-lieu="{esc(st)}"><span{" dir=" + chr(34) + "ltr" + chr(34) if lang == "he" and st not in STATIONS_HE else ""}>{esc(STATIONS_HE.get(st, st) if lang == "he" else st)}</span></button>'
              for st in STATIONS_PRINC) + "</div>" +
          '<input type="hidden" name="lieu" id="lieu">' +
          champ("lieu-autre", "lieu_autre", "Another resort", ph="Morzine, Zermatt, Verbier") + sugg("lieu-autre", STATIONS) +
          chips("lieu_pas_choisi", ["Not chosen yet, advise us"], b="aef") +
          f'<div data-b="abe"><div class="pf-seg-b" role="radiogroup" aria-label="{E("Where would you like to stay?")}">'
          f'<label class="pf-seg"><input type="radio" name="deja" value="0" data-en="Full stay" checked><span>{E("Full stay")}</span></label>'
          f'<label class="pf-seg"><input type="radio" name="deja" value="1" data-en="I already have my place"><span>{E("I already have my place")}</span></label></div></div>')
    def bascule(val_en, texte, coche=False):
        return (f'<label class="pf-seg"><input type="radio" name="flexible" value="{E(val_en)}" data-en="{esc(val_en)}"{" checked" if coche else ""}><span>{E(texte)}</span></label>')
    quand = ('<div class="pf-seg-b pf-bascule" role="radiogroup">' + bascule("Dates are flexible", "By month", True) + bascule("Dates are fixed", "I have exact dates") + "</div>" +
             si("flexible=Dates are fixed",
                '<div class="pf-duo">' + champ("arrivee", "arrivee", "Arrival", typ="date") + champ("depart", "depart", "Departure", typ="date") + "</div>" +
                '<p class="pf-info" id="dm-nuits" hidden aria-live="polite"></p>' +
                f'<p class="pf-info" id="dm-shabbat" hidden data-t="{E("Shabbat during your stay:")}"></p>' +
                f'<p class="pf-erreur" id="dm-date-err" role="alert" hidden>{E("The departure is before the arrival.")}</p>' +
                f'<p class="pf-info" id="dm-fete" hidden data-t="{E("In your dates: {f}")}"></p>') +
             si("flexible=Dates are flexible", chips("mois", ["November", "December", "January", "February", "March", "April", "Summer", "Not decided yet"])) +
             f'<div data-b="abe" id="dm-fetes">{sous("A holiday during your stay?")}' +
             chips("voyage", ["Pesach in the Alps", "Hanukkah in the Alps", "Sukkot", "Rosh Hashanah and Yom Kippur", "Purim", "Shavuot", "Another holiday"], cls="pf-flow") + "</div>")
    qui = (compteur("adultes", "Adults", v=2) + compteur("enfants", "Children") +
           ages("enfants", "Ages of the children", "9 and 12", [(str(n),) for n in range(2, 18)]) +
           compteur("bebes", "Babies") + ages("bebes", "Ages of the babies", "10 months", ["3 months", "6 months", "1 year", "18 months", "2 years"]) +
           '<div class="pf-mat cache" data-for="bebes">' + chips("bebe_materiel", ["Baby cots", "High chairs", "Car seats"], cls="pf-flow") + "</div>" +
           compteur("familles", "Families or households", b="abef", v=1) +
           compteur("chambres", "Bedrooms", b="a") +
           f'<div data-b="c">{sous("Luggage and equipment")}' + chips("bagages", ["Large suitcases", "Cabin bags only", "Skis or snowboards", "Baby seats or boosters", "Wheelchair or walker"], cls="pf-flow") + "</div>")
    # ---- Build your stay : tuiles photo (photos reelles du site, _demande_photos.py), un toucher = ajoute
    def tuile(name, val_en, titre, photo, prix, b="", sa="", svc=""):
        return (f'<label class="pf-tl"{battr(b)}{sattr(sa)}><input type="checkbox" name="{name}" value="{E(val_en)}" data-en="{esc(val_en)}" data-svc="{svc}">'
                f'<span class="pf-tl-img"><img src="{IMG}illus/form-svc/{photo}.webp" alt="" width="480" height="360" loading="lazy"><b>{E(titre)}</b><i aria-hidden="true"></i></span>'
                + prix_vignette(lang, prix) + '</label>')
    services = ('<div class="pf-tls">' +
                tuile("logement", "A private chalet", "Private chalet", "chalet", "chalet", b="aef", svc="chalet") +
                tuile("repas", "Private chef in the chalet", "Private chef", "chef", "chef", svc="chef") +
                tuile("repas", "Meals delivered, ready to heat", "Meals delivered", "livre", "soir", svc="livre") +
                tuile("repas", "Shabbat meals only", "Shabbat meals", "shabbat", "shabbat", svc="shabbat") + "</div>" +
                chips("repas", ["Advise me"]) +
                champ("allergies", "allergies", "Allergies or special diets", ph="Nut allergy for one child"))
    extras = ('<div class="pf-tls pf-tls2">' +
                tuile("extras", "Private butler", "Private butler", "butler", "demande") +
                tuile("transport", "Private airport transfer", "Van transfer", "transfert", "demande") +
                tuile("ski", "Ski lessons", "Ski lessons", "ski", "demande", sa="w") +
                tuile("ski", "Ski equipment", "Ski equipment", "skimateriel", "demande", sa="w") +
                tuile("ski", "Ski passes", "Ski passes", "skiforfaits", "demande", sa="w") +
                tuile("ski", "Snowmobile or dog sledding", "Activities", "activites", "demande", sa="w") +
                tuile("ski", "Massage and spa", "Massages", "massage", "demande") +
                tuile("cacherout", "Kitchen kashering", "Kitchen kashering", "cacher", "demande") +
                tuile("religieux", "Hot plate and urn", "Hot plate and urn", "plata", "demande") +
                tuile("lyon", "Jewish Lyon walk (2 h)", "Lyon tour", "lyon", "lyon", svc="lyon") + "</div>")
    # ---- Minyan et Chabbat (Moshe 03/11) : une ligne par besoin, vignette + trois pastilles Essential / Nice to have / Not needed
    def besoin(name, titre, img, vals):
        ps = "".join(f'<label class="pf-niv"><input type="radio" name="{name}" value="{E(v)}" data-en="{esc(v)}"><span>{E(t_)}</span></label>' for v, t_ in vals)
        return (f'<div class="pf-bes"><div class="pf-bes-t"><img src="{img}" alt="" width="40" height="40"><b>{E(titre)}</b></div><div class="pf-nivs">{ps}</div></div>')
    NIV = [("Essential", "Essential"), ("Nice to have", "Nice to have"), ("Not needed", "Not needed")]
    minyan = ('<div class="pf-bess">' +
              besoin("minyan_niveau", "Minyan in the chalet", f"{IMG}illus/form-svc/minyan.webp", [("The minyan is essential", "Essential"), ("Nice to have", "Nice to have"), ("Not needed", "Not needed")]) +
              besoin("torah_niveau", "Sefer Torah for the Shabbat reading", f"{IMG}illus/form-svc/sefer-torah.svg", NIV) +
              besoin("shabbat_niveau", "Shabbat meals", f"{IMG}illus/form-svc/shabbat.webp", NIV) +
              besoin("eruv_niveau", "Eruv and mikveh nearby", f"{IMG}illus/form-svc/mikve.webp", NIV) + "</div>" +
              si("minyan_niveau!=Not needed", compteur("hommes", "Men over bar mitzvah age, for the minyan")))
    # ---- 04/11 : « De quoi avez-vous besoin ? » (parcours b) : repas, allergies, ajouts. Memes cles et memes valeurs que les anciens ecrans services / extras / minyan.
    def bchip(name, en, titre, prix="", sa="", pre=""):
        pr = f'<small>{prix}</small>' if prix else ""
        return (f'<label class="pf-c pf-bn"{sattr(sa)}><input type="checkbox" name="{name}" value="{E(en)}" data-en="{esc(en)}"' + (f' data-pre="{pre}"' if pre else "") + f'>'
                f'<span><b>{insec(E(titre))}</b>{pr}</span></label>')
    def px(cle=""):
        """Prix « a partir de » d'un ajout : lu dans la grille (data-px = cle MT_PRIX), « sur demande » tant que la grille ne le publie pas."""
        if not cle: return f'{PRIX_TPL[lang]["demande"]}'
        return f'<span data-px="{cle}" data-px-tpl="{html.escape(PRIX_TPL[lang]["from"], quote=True)}">{PRIX_TPL[lang]["demande"]}</span>'
    besoins = ('<p class="pf-sous">' + E("Meals") + '</p><div class="pf-chips pf-bchips">' +
               bchip("repas", "Private chef in the chalet", "Private chef") + bchip("repas", "Meals delivered, ready to heat", "Meals delivered") +
               bchip("repas", "Shabbat meals only", "Shabbat meals only", pre="shabbat") + bchip("repas", "Advise me", "Advise me") + "</div>" +
               champ("allergies-b", "allergies", "Allergies or special diets", ph="Nut allergy for one child") +
               '<p class="pf-sous">' + E("Extras") + '</p><div class="pf-chips pf-bchips">' +
               bchip("minyan_niveau", "The minyan is essential", "Minyan in the chalet", px()) + bchip("cacherout", "Kitchen kashering", "Kitchen kashering", px("c_cacher_vente")) +
               bchip("religieux", "Hot plate and urn", "Hot plate and urn", px("r_plata_vente")) + bchip("transport", "Private airport transfer", "Private transfer", px()) +
               bchip("ski", "Ski passes", "Ski passes", px(), sa="w") + "</div>")
    # ---- Budget : phrase personnalisee, details en mots, un toucher pour situer son budget, champ libre facultatif
    budget = (f'<div data-b="abe"><p class="pf-perso" id="dm-perso" aria-live="polite"></p><ul class="pf-notes" id="dm-notes"></ul>' +
              '<div class="pf-avis" id="dm-avis">' + chips("budget_avis", ["Below this", "Around this", "Above this", "I'd rather discuss it"], multi=False) + "</div>" +
              f'<p class="pf-fit" id="dm-fit" role="status" hidden></p>' +
              f'<p class="pf-ess" id="dm-ess" hidden><button type="button" class="pf-ess-b" id="dm-ess-b" data-a="{E("Switch to the essentials")}" data-u="{E("Undo")}">{E("Switch to the essentials")}</button></p></div>' +
              champ("budget-total", "budget_total", "Total budget for the stay, if you have one", ph="€", extra=' inputmode="numeric"', b="abef") +
              f'<p class="pf-bhint" id="dm-bhint" role="status" hidden>{E("The total budget for the whole stay and the whole group, for example 15,000 €.")}</p>')
    trajet = (champ("van_depart", "van_depart", "Pick-up point", ph="Lyon Saint-Exupéry airport") +
              sugg("van_depart", ["Geneva airport", "Lyon airport", "Lyon Part-Dieu station", "Our chalet"] + STATIONS) +
              champ("van_arrivee", "van_arrivee", "Drop-off point", ph="Les Deux Alpes, chalet") +
              sugg("van_arrivee", ["Our chalet"] + STATIONS + ["Geneva airport", "Lyon airport", "Lyon Part-Dieu station"]) +
              chips("aller_retour", ["One way", "Return trip"], multi=False))
    quandvan = (sous("Outbound") + '<div class="pf-duo">' + champ("arrivee-van", "arrivee", "Date", typ="date") + champ("heure", "heure", "Pick-up time", typ="time") + "</div>" +
                si("aller_retour=Return trip", sous("Return") + '<div class="pf-duo">' + champ("retour_date", "retour_date", "Return date", typ="date") +
                   champ("retour_heure", "retour_heure", "Return pick-up time", typ="time") + "</div>") +
                champ("vol-van", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30"))
    lyon = (chips("lyon", ["Jewish Lyon walk (2 h)", "Stopover (3 h) on the way", "Memory: CHRD museum", "Memory: Montluc, Neveh Shalom", "Day trip to Izieu", "Shabbat with a Chabad family"], cls="pf-flow") +
            sous("Which day?") + champ("arrivee-jour", "arrivee", "Date", typ="date") + chips("creneau", ["Morning", "Afternoon", "Either"], multi=False, cls="pf-flow") +
            sous("Language of the visit") + chips("langue_visite", ["English", "French", "Spanish"], multi=False, cls="pf-flow") +
            '<p class="pf-note">' + E("To enter the Grande Synagogue, the community's security team will ask for your names and passports once the tour is confirmed.") + "</p>")
    message_f = zone("message-f", "message", "Tell us what you have in mind", "A bar mitzvah weekend in the Alps for 30 guests")
    S += [etape("message", "Tell us what you have in mind", "Write it the way you would say it. We take it from there.", message_f),
          etape("ou", [("Where would you like to stay?", "aef"), ("Where are you staying?", "b")], [("Choose one resort or several, or let us advise you.", "aef"), ("Tell us the resort and the address.", "b")], ou),
          etape("quand", "When are you coming?", "Approximate dates are fine.", quand),
          etape("trajet", "Where from, and is there a return?", "Address, airport, station or hotel. A town name is enough.", trajet),
          etape("quandvan", "When?", "Date and time of each trip. Add the flight if you land or take off.", quandvan),
          etape("lyon", "Which visit, and when?", "Tours are held in English, French or Spanish.", lyon),
          etape("qui", "Who is coming?", [("Count the whole group, all families together.", "abef"), ("Children's ages help us choose rooms, ski school and cots.", "cd")], qui,
                avant='<p class="pf-recap" id="dm-recap" hidden></p>'),
          etape("services", "Stay and meals", "Tap everything you would like. We confirm each service with you.", services),
          etape("extras", "Extras", "Add what would make the stay perfect.", extras),
          etape("minyan", "Minyan and Shabbat", "", minyan),
          etape("besoins", "What do you need?", "", besoins),
          etape("budget", [("Your budget", "abe"), ("Your budget and your wishes", "f"), ("Anything else?", "cd")], [("Optional.", "cdf")], budget)]

    # ================= dernier ecran : contact
    contact = (cache_int + champ("prenom", "prenom", "First name", extra=' autocomplete="given-name" required') +
        f'<div class="pf-champ"><label for="f-tel">{E("WhatsApp number")}</label><div class="pf-tel"><select id="f-indicatif" name="indicatif" aria-label="{E("Country code")}" required>'
        + INDICATIFS.replace("{code}", E("Code")) + '</select><input type="tel" id="f-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="212 555 0100" pattern="[0-9 ().-]{6,16}" required></div></div>' +
        champ("adresse", "adresse", "Address or name of the accommodation", ph="Chalet Le Sapin, 12 route du Lac", b="b") +
        champ("email", "email", "Email (optional)", typ="email", extra=' autocomplete="email"') +
        zone("message-fin", "message", "Anything else we should know", "Anything that helps: a baby, a late arrival, a special diet.", b="abcde") +
        '<p class="pf-resume" id="dm-resume" hidden></p>')
    S.append(etape("final", "Your contact", "We answer you on WhatsApp the same day.", contact + f'<p class="pf-erreur" id="dm-erreur" hidden>{esc(JSX[lang]["err"])}</p>', "pf-contact"))

    prog = (f'<div class="pf-prog" id="dm-prog"><button type="button" class="pf-retour" id="dm-back" hidden aria-label="{E("Back")}"><span aria-hidden="true"></span>{E("Back")}</button>'
            f'<span class="pf-prog-txt" id="dm-prog-txt" aria-live="polite"></span>'
            f'<div class="pf-barre" id="dm-barre-c" role="progressbar" aria-label="{E("Progress")}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="dm-barre"></i></div></div>')
    nav = (f'<p class="pf-accord" id="dm-accord" hidden><label><input type="checkbox" id="dm-accord-cb" name="accord" required> '
           f'<span>{esc(ACCORD[lang][0])} <a href="{ACCORD[lang][2]}" target="_blank" rel="noopener">{esc(ACCORD[lang][1])}</a></span></label>'
           f'<small class="pf-erreur" id="dm-accord-err" role="alert" hidden>{esc(ACCORD[lang][3])}</small></p>'
           f'<div class="pf-nav" id="dm-nav"><span class="pf-nsvc" id="dm-nsvc" hidden data-un="{E("1 service added")}" data-n="{E("{n} services added")}"></span>'
           f'<button type="button" class="btn-noir" id="dm-next" hidden>{E("Continue")}</button>'
           f'<button type="submit" class="btn-noir" id="dm-send" hidden>{esc(JSX[lang]["envoyer"])}</button></div>'
           f'<p class="pf-petit" id="dm-petit" hidden><small>{esc(JSX[lang]["petit"])}</small></p>')
    noscript = f'<noscript><p class="pf-note">{E("This form needs JavaScript. Write to us on WhatsApp instead.")} <a href="{JSX[lang]["wa"]}" rel="noopener">WhatsApp</a></p></noscript>'
    piege = {"en": "Company", "fr": "Société", "es": "Empresa", "he": "חברה"}[lang]
    return ('<section class="pf ss wrap" id="demande">\n<form id="formDemande" class="pf-form" novalidate autocomplete="off">\n'
            f'  <div class="piege" aria-hidden="true"><label for="f-societe">{piege}</label><input type="text" id="f-societe" name="societe" tabindex="-1" autocomplete="off"></div>\n'
            f'  {noscript}\n  {prog}\n  ' + "  ".join(S) + f'  {nav}\n</form>\n</section>')

JS_TPL = r'''<script>
(function(){var f=document.getElementById('formDemande');if(!f)return;
var C=__CFG__;
var KEY='mt-plan-v4-'+C.lang,TTL=2592e6;
var ctrls=[].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(e){return e.name!=='societe'&&e.name!=='accord'});
var accord=document.getElementById('dm-accord'),accordCb=document.getElementById('dm-accord-cb'),accordErr=document.getElementById('dm-accord-err');
ctrls.forEach(function(e){e.scr=e.closest('.pf-etape').getAttribute('data-e')});
var etapes=[].slice.call(f.querySelectorAll('.pf-etape'));
var barre=document.getElementById('dm-barre'),barreC=document.getElementById('dm-barre-c'),ptxt=document.getElementById('dm-prog-txt');
var nav=document.getElementById('dm-nav'),bBack=document.getElementById('dm-back'),bNext=document.getElementById('dm-next'),bSend=document.getElementById('dm-send'),petit=document.getElementById('dm-petit');
var pre=false,skip=false,reskip=false,ptr=0,repasTouched=false,restaure=false,cur='',base='a',sent=false,lieuIn=document.getElementById('lieu'),autreIn=document.getElementById('lieu-autre');
function mo(){return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: no-preference)').matches)}
var dl=window.dataLayer=window.dataLayer||[];
var mx=document.getElementById('dm-max'),nuitsP=document.getElementById('dm-nuits'),dateErr=document.getElementById('dm-date-err');
function branch(){var r=f.querySelector('input[name="intention"]:checked');return r?r.value:''}
function path(){var b=branch()||'a',p=C.paths[b].slice();if(b==='b'&&skip)p=p.filter(function(x){return x!=='ou'&&x!=='quand'});return p}
/* data-si="nom=valeur" : visible si cette case est cochee ; "nom!=valeur" : visible si une case est cochee et que ce n'est pas celle-la */
function siOk(c){var m=/^(\w+)(!?=)(.*)$/.exec(c);if(!m)return true;var on=ctrls.filter(function(e){return e.name===m[1]&&e.checked}).map(function(e){return e.getAttribute('data-en')||e.value});
 return m[2]==='='?on.indexOf(m[3])>=0:(on.length>0&&on.indexOf(m[3])<0)}
function sync(){var b=branch(),p=path();
 var hs=false,hw=false,m=/^\d{4}-(\d\d)/.exec(raw0('arrivee'));if(m){var mm=+m[1];if(mm>=5&&mm<=10)hs=true;else hw=true}
 [].forEach.call(f.querySelectorAll('[data-s]'),function(n){if(n.classList.contains('pf-auto'))return;var s=n.getAttribute('data-s');n.hidden=s==='w'?(hs&&!hw):(hw&&!hs)});
 [].forEach.call(f.querySelectorAll('[data-b]'),function(n){if(n.classList.contains('pf-auto'))return;n.hidden=n.getAttribute('data-b').indexOf(b)<0});
 [].forEach.call(f.querySelectorAll('[data-si]'),function(n){n.hidden=!siOk(n.getAttribute('data-si'))});
 ctrls.forEach(function(e){var ok=p.indexOf(e.scr)>=0||(skip&&b==='b'&&(e.scr==='ou'||e.scr==='quand'));
  if(ok){var n=e.parentNode;while(n&&n!==f){if(n.getAttribute&&((n.getAttribute('data-b')&&n.getAttribute('data-b').indexOf(b)<0)||((n.getAttribute('data-s')||n.getAttribute('data-si'))&&n.hidden))){ok=false;break}n=n.parentNode}}
  if(ok){var w=e.closest('[data-for]');if(w){var ci=f.querySelector('input[name="'+w.getAttribute('data-for')+'"]');if(!(parseInt(ci.value,10)>0))ok=false}}
  e.disabled=e.name==='intention'?false:!ok});
 [].forEach.call(f.querySelectorAll('.pf-ages,.pf-mat'),function(w){var i=f.querySelector('input[name="'+w.getAttribute('data-for')+'"]');w.classList.toggle('cache',!(parseInt(i.value,10)>0))});
 return p}
function raw0(n){var e=ctrls.filter(function(x){if(x.name!==n||!x.value)return false;var w=x.closest('[data-b]');return !w||w.getAttribute('data-b').indexOf(branch())>=0})[0];return e?e.value:''}
function els(n){return ctrls.filter(function(e){return e.name===n&&!e.disabled})}
function raw(n){var a=els(n);if(!a.length)return '';var t=a[0].type;if(t==='checkbox'||t==='radio'){return a.filter(function(e){return e.checked}).map(function(e){return e.value}).join(', ')}return a[0].value.trim()}
function fdate(v,loc){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return v;try{return new Date(+m[1],+m[2]-1,+m[3],12).toLocaleDateString(loc||C.loc,{day:'numeric',month:'long',year:'numeric'})}catch(x){return v}}
function voyage(en){var r=f.querySelector('input[name="intention"]:checked');var a=r?[r.getAttribute(en?'data-en':'data-voyage')]:[];
 els('voyage').forEach(function(e){if(e.checked){var v=en?(e.getAttribute('data-en')||e.value):e.value;if(a.indexOf(v)<0)a.push(v)}});return a.join(', ')}
function rawEn(n){var a=els(n);if(!a.length)return '';var t=a[0].type;if(t==='checkbox'||t==='radio'){return a.filter(function(e){return e.checked}).map(function(e){return e.getAttribute('data-en')||e.value}).join(', ')}return a[0].value.trim()}
function euros(s){var d=s.replace(/[^\d]/g,'');if(!d)return s;return d.replace(/\B(?=(\d{3})+(?!\d))/g,' ')+' €'}
/* val(n, true) : version anglaise (data-en des cases), pour le mail et le PDF transmis aux partenaires quelle que soit la langue du client */
function val(n,en){
 if(n==='arrivee'||n==='depart'||n==='retour_date'){var d=raw(n);return d?fdate(d,en?'en-GB':''):''}
 if(n==='adultes'||n==='hommes'||n==='familles'||n==='chambres'||n==='sdb'){var x=parseInt(raw(n),10);return x>0?String(x):''}
 if(n==='enfants'||n==='bebes'){var y=parseInt(raw(n),10);if(!(y>0))return '';var g=raw(n+'_ages');return y+(g?' ('+g+')':'')}
 if(n==='voyage')return voyage(en);
 if(n==='logement'&&branch()==='b')return en?'Already booked, I need services only':C.k.logementB;
 if(n==='budget_total'){var bn=bnum(raw(n));return bn?euros(String(bn)):raw(n)}
 if(n==='religieux'){var rl=(en?rawEn(n):raw(n)),tv=ctrls.filter(function(e){return e.name==='torah_niveau'&&e.checked&&!e.disabled})[0];if(tv&&tv.getAttribute('data-en')!=='Not needed'){var st=en?'Sefer Torah in the chalet':C.t.torah;rl=rl?rl+', '+st:st}return rl}
 if(n==='budget_fit'){var k=fitK();if(!k)return '';var es=estim();if(k==='below')k=essOn?'below_c':'below_p';return (en?{below_c:'below (essentials chosen)',below_p:'below (essentials proposed)'}[k]||k:C.t['k_'+k])+(es&&es.e?' ('+(en?'estimate':C.t.estimate)+' '+euros(String(es.e))+')':'')}
 return en?rawEn(n):raw(n)}
/* budget saisi : chiffres seuls, « 20k », « 20 mil », « 20 mille », « 20 אלף » = milliers */
function bnum(s){s=String(s||'').toLowerCase();var m=/(\d[\d\s.,\u00a0]*)\s*(k|mil|mille|\u05d0\u05dc\u05e3)?/.exec(s);if(!m)return 0;var d=m[1].replace(/[^\d]/g,'');if(!d)return 0;var v=parseInt(d,10);if(m[2])v*=1000;return v}
function num(n){return parseInt(raw(n),10)||0}
function pers(){return num('adultes')+num('enfants')}
function stSel(){return [].map.call(f.querySelectorAll('.pf-pas.on'),function(x){return x.getAttribute('data-lieu')})}
function majLieu(){var a=stSel(),o=(autreIn&&autreIn.value||'').trim();if(o)a.push(o);if(lieuIn)lieuIn.value=a.join(', ')}
function initLieu(){if(!lieuIn)return;var rest=[];(lieuIn.value||'').split(/,\s*/).forEach(function(x){if(!x)return;var b=null;[].forEach.call(f.querySelectorAll('.pf-pas'),function(y){if(y.getAttribute('data-lieu')===x)b=y});if(b)b.classList.add('on');else rest.push(x)});
 if(rest.length&&autreIn&&!autreIn.value)autreIn.value=rest.join(', ');majLieu()}
/* parcours : Alpes par defaut ; « I already have my place » = b ; une fete cochee = e ; i= de l'adresse (Lyon d, van c, autre f) garde son parcours */
function deja(){return ctrls.some(function(e){return e.name==='deja'&&e.value==='1'&&e.checked})}
function majBr(){var dd=ctrls.filter(function(e){return e.name==='deja'});if(dd.length&&!dd.some(function(e){return e.checked}))dd[0].checked=true;var dj=deja(),v=base;if('abe'.indexOf(base)>=0){var hol=ctrls.some(function(e){return e.name==='voyage'&&e.checked});v=dj?'b':(hol?'e':'a')}
 var r=ctrls.filter(function(e){return e.name==='intention'&&e.value===v})[0];if(r)r.checked=true}
function dnum0(n){var e=ctrls.filter(function(x){return x.name===n&&!x.disabled&&x.type==='date'})[0];return e?dnum(e.value):null}
function nshab(nn){var a=dnum(raw('arrivee'));if(a===null)return Math.max(1,Math.floor(nn/7));var c=0;for(var k=0;k<nn;k++){if(new Date(a+k*864e5).getUTCDay()===5)c++}return c}
/* 03/11 : prix de la grille de Mendel (js/prix.js expose window.MT_PRIX et l'evenement mt-prix) ; sans grille, C.prix et C.chaletBase (repli) restent.
   Chalet d'une station = semaine basse la moins chere de ses chalets : Deux Alpes ch1 ch2, Courchevel ch3 ch7 ch8, Megeve ch4, Val Thorens ch5, Tignes ch9 a ch11 ;
   Les Menuires estimee comme Val Thorens tant que Mendel n'a pas repondu (Moshe 03/11) ; sans station : le moins cher de tous.
   Chef c_chef_vente ; repas du soir r_soir_vente ; Chabbat vendredi + samedi + seouda ; livraison l_zoneA_vente (la plus basse : l'estimation reste basse). */
function grille(G){if(!G)return;var g=function(){var l=[].slice.call(arguments).map(function(k){return G[k]}).filter(function(v){return v>0});return l.length?Math.min.apply(null,l):0};
 var b=function(i){return 'ch'+i+'_basse_vente'},st={'Les Deux Alpes':g(b(1),b(2)),'Courchevel':g(b(3),b(7),b(8)),'Megève':g(b(4)),'Val Thorens':g(b(5)),'Tignes':g(b(9),b(10),b(11))};
 st['Les Menuires']=st['Val Thorens'];Object.keys(st).forEach(function(k){if(st[k])C.chaletBase[k]=st[k]});
 var tous=g(b(1),b(2),b(3),b(4),b(5),b(6),b(7),b(8),b(9),b(10),b(11));if(tous)C.prix.chalet=tous;
 if(G.c_chef_vente>0)C.prix.chef=G.c_chef_vente;if(G.r_soir_vente>0)C.prix.soir=G.r_soir_vente;if(G.l_zoneA_vente>0)C.prix.livraison=G.l_zoneA_vente;
 var sh=[G.r_vendredi_vente,G.r_samedi_vente,G.r_seouda_vente];if(sh.every(function(v){return v>0})){C.prix.shabbat=sh[0]+sh[1]+sh[2];C.prix.shab_min=Math.min.apply(null,sh);C.prix.shab_max=Math.max.apply(null,sh)}
 var ab={chalet:['chalet'],chef:['chef'],soir:['soir'],shabbat:['shab_min','shab_max']},sep=C.lang==='fr'?'\u00a0':C.lang==='es'?'.':',';
 var m=function(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,sep)};
 [].forEach.call(f.querySelectorAll('[data-pf]'),function(el){var k=ab[el.getAttribute('data-pf')];if(!k)return;var t=el.getAttribute('data-pf-tpl').replace('{a}',m(C.prix[k[0]]));if(k[1])t=t.replace('{b}',m(C.prix[k[1]]));el.innerHTML=t});
 [].forEach.call(f.querySelectorAll('[data-px]'),function(el){var v=G[el.getAttribute('data-px')];if(v>0)el.innerHTML=el.getAttribute('data-px-tpl').replace('{a}',m(v))})}
function chaletBase(){var l=stSel().map(function(x){return C.chaletBase[x]||C.prix.chalet});return l.length?Math.min.apply(null,l):C.prix.chalet}
/* Estimation indicative « a partir de » (03/11), volontairement basse : elle sert a prevenir, jamais a refuser. Prix = ceux publies sur le site (PRIX_N, CHALET_BASE).
   nuits = depart - arrivee ; sans dates fixes : une semaine (7 nuits, 1 Chabbat). personnes = adultes + enfants (bebes non comptes) ; Chabbat = vendredis du sejour.
   chalet : prix de depart de la station choisie (la moins chere si plusieurs ; 9 500 sinon) x nuits / 7, au prorata ; chef : 1 568 x nuits ;
   si chef : repas livres et repas de Chabbat comptent 0 (regle des devis de Mendel, espace.html : le chef annule les lignes de repas) ;
   sinon repas livres : 28 (diner seul) x personnes x nuits + 180 x arrondi superieur (nuits / 2) livraisons ; Chabbat : (45 + 40 + 30) x personnes x Chabbat ;
   visite de Lyon : 290 par groupe ; services sur demande : 0 (« plus les services sur demande »). Aucune hausse de saison chiffree. */
function estim(){var nn=nights(),wk=false;if(!(nn>0)){nn=7;wk=true}var s={},dem=false;
 ctrls.forEach(function(e){if(!e.checked||e.disabled||!e.closest('.pf-tl'))return;var k=e.getAttribute('data-svc');if(k)s[k]=1;else dem=true});
 var P=C.prix,p=pers(),e=0;
 if(s.chalet)e+=chaletBase()*nn/7;
 if(s.chef)e+=P.chef*nn;else{if(s.livre)e+=P.soir*p*nn+P.livraison*Math.ceil(nn/2);if(s.shabbat)e+=P.shabbat*p*nshab(nn)}
 if(s.lyon)e+=P.lyon;
 return {e:Math.floor(e),dem:dem,nn:nn,wk:wk,s:s}}
var AV={'Below this':'below','Around this':'around','Above this':'above',"I'd rather discuss it":'discuss'};
function avisK(){var r=els('budget_avis').filter(function(e){return e.checked})[0];return r?AV[r.getAttribute('data-en')]:''}
/* « Budget fit » : la reponse touchee (below / around / above / discuss) ; sans toucher, le montant saisi compare a l'estimation (>= 110 % above, >= 90 % around, sinon below) */
function fitK(){if('abe'.indexOf(branch()||'x')<0)return '';var a=avisK();if(a)return a;var es=estim(),b=bnum(raw('budget_total'));if(!es.e||b<1000)return '';var r=b/es.e;return r>=1.1?'above':r>=.9?'around':'below'}
function liste(a){if(a.length<2)return a.join('');return a.slice(0,-1).join(', ')+C.t.et+a[a.length-1]}
function occupe(){var hol=ctrls.some(function(e){return e.name==='voyage'&&e.checked&&/Hanukkah|Pesach/.test(e.getAttribute('data-en'))});
 var mois=ctrls.some(function(e){return e.name==='mois'&&e.checked&&!e.disabled&&/December|February/.test(e.getAttribute('data-en'))});
 var a=dnum(raw('arrivee')),nn=nights(),per=false;if(a!==null&&nn>0&&nn<=90){for(var k=0;k<nn;k++){var d=new Date(a+k*864e5),m=d.getUTCMonth()+1,j=d.getUTCDate();if((m===12&&j>=20)||(m===1&&j<=5)||(m===2&&j>=6)||(m===3&&j<=8)){per=true;break}}}
 return hol||mois||per}
function bdi(el,txt){var b=document.createElement('bdi');b.dir='ltr';b.textContent=txt;el.appendChild(b)}
function majBudget(){var el=document.getElementById('dm-perso');if(!el)return;var ft=document.getElementById('dm-fit'),ul=document.getElementById('dm-notes'),av=document.getElementById('dm-avis');
 if('abe'.indexOf(branch()||'x')<0){el.textContent='';ft.hidden=true;return}
 var es=estim(),g=num('adultes')+num('enfants')+num('bebes'),st=stSel().map(function(x){return C.stHe[x]||x}),o=(autreIn&&autreIn.value||'').trim();
 var lieu=st.length?C.t.dans.replace('{p}',st.join(C.t.ou)):(o?C.t.dans.replace('{p}',o):C.t.alpes);
 var nuits=es.wk?C.t.semaine:(es.nn===1?C.t.nuit:C.t.nuits.replace('{n}',es.nn));
 var sv=['chalet','chef','livre','shabbat','lyon'].filter(function(k){return es.s[k]}).map(function(k){return C.t['s_'+k]});
 el.textContent='';
 if(es.e>=1e5)el.textContent=C.t.large;
 else{var tpl=(es.e>0?C.t.perso:C.t.perso0).replace('{g}',g).replace('{n}',nuits).replace('{p}',lieu).replace('{s}',liste(sv)),x=es.e<1000?Math.floor(es.e/100)*100:Math.floor(es.e/500)*500,pt=tpl.split('{x}');
  el.appendChild(document.createTextNode(pt[0]));if(pt.length>1){bdi(el,x.toLocaleString(C.loc)+' €');el.appendChild(document.createTextNode(pt[1]+(es.dem?C.t.dem:'')))}}
 ul.textContent='';var notes=[];if(occupe())notes.push(C.t.n_occupe);if(stSel().some(function(x){return x==='Courchevel'||x==='Megève'}))notes.push(C.t.n_station);if(g>=10)notes.push(C.t.n_groupe);
 notes.forEach(function(t){var li=document.createElement('li');li.textContent=t;ul.appendChild(li)});
 av.hidden=!(es.e>0&&es.e<1e5);
 var k=av.hidden?'':avisK();ft.hidden=!k;if(!k)return;ft.className='pf-fit pf-fit-'+k;
 ft.textContent=C.t['f_'+k];var eb=document.getElementById('dm-ess'),bb=document.getElementById('dm-ess-b');eb.hidden=k!=='below'||(!essOn&&!es.s.chalet&&!es.s.chef);bb.textContent=bb.getAttribute(essOn?'data-u':'data-a')}
/* « Switch to the essentials » (Moshe 03/11) : un toucher retire chalet prive et chef, ajoute repas livres et repas de Chabbat ; annulable */
var essOn=false,essAvant=null;
function essentiels(){var tl=ctrls.filter(function(e){return e.closest('.pf-tl')&&e.getAttribute('data-svc')});
 if(!essOn){essAvant=tl.map(function(e){return e.checked});tl.forEach(function(e){var k=e.getAttribute('data-svc');if(k==='chalet'||k==='chef')e.checked=false;if(k==='livre'||k==='shabbat')e.checked=true});essOn=true}
 else{tl.forEach(function(e,i){if(essAvant)e.checked=essAvant[i]});essOn=false}
 render()}
/* fetes proposees selon les mois choisis (dates souples) ; avec des dates exactes, toutes, et celles des dates cochees d'office */
var FMOIS={'Pesach in the Alps':['March','April'],'Hanukkah in the Alps':['December','November'],'Purim':['March','February'],'Shavuot':['Summer'],'Sukkot':[],'Rosh Hashanah and Yom Kippur':[]};
function fetesMois(){var bloc=document.getElementById('dm-fetes');if(!bloc)return;var fixe=ctrls.some(function(e){return e.name==='flexible'&&e.checked&&e.getAttribute('data-en')==='Dates are fixed'});
 var mois=ctrls.filter(function(e){return e.name==='mois'&&e.checked}).map(function(e){return e.getAttribute('data-en')}),n=0;
 [].forEach.call(bloc.querySelectorAll('.pf-c'),function(l){var i=l.querySelector('input'),k=i.getAttribute('data-en'),m=FMOIS[k];
  var vis=fixe||i.checked||(mois.length&&(m===undefined||m.some(function(x){return mois.indexOf(x)>=0})));l.classList.toggle('pf-off',!vis);if(vis)n++});
 bloc.classList.toggle('pf-off',!n)}
function majN(){var el=document.getElementById('dm-nsvc');if(!el)return;var n=ctrls.filter(function(e){return e.checked&&!e.disabled&&e.closest('.pf-tl')}).length;el.hidden=!(cur==='services'&&n>0);el.textContent='';
 if(n===1)el.textContent=el.getAttribute('data-un');else{var t=el.getAttribute('data-n').split('{n}'),b=document.createElement('bdi');b.textContent=n;el.appendChild(document.createTextNode(t[0]));el.appendChild(b);el.appendChild(document.createTextNode(t[1]||''))}}
/* fetes deduites des dates (calendrier Hebcal, diaspora, veille comprise) : cochees d'office, decochables ; l'utilisateur garde le dernier mot pour des dates donnees */
var FETES=[["Rosh Hashanah and Yom Kippur","2026-09-11","2026-09-21",2026],["Sukkot","2026-09-25","2026-10-04",2026],["Hanukkah in the Alps","2026-12-04","2026-12-12",2026],
 ["Purim","2027-03-22","2027-03-23",2027],["Pesach in the Alps","2027-04-21","2027-04-29",2027],["Shavuot","2027-06-10","2027-06-12",2027],
 ["Rosh Hashanah and Yom Kippur","2027-10-01","2027-10-11",2027],["Sukkot","2027-10-15","2027-10-24",2027],["Hanukkah in the Alps","2027-12-24","2028-01-01",2027],
 ["Purim","2028-03-11","2028-03-12",2028],["Pesach in the Alps","2028-04-10","2028-04-18",2028],["Shavuot","2028-05-30","2028-06-01",2028]];
var feteVu='';
function fetes(){var a=dnum(raw('arrivee')),d=dnum(raw('depart')),el=document.getElementById('dm-fete');if(!el)return;if(a===null||d===null||d<a){el.hidden=true;return}
 var tr=FETES.filter(function(x){return dnum(x[1])<=d&&dnum(x[2])>=a}),cle=a+'-'+d;
 if(cle!==feteVu){feteVu=cle;tr.forEach(function(x){ctrls.forEach(function(e){if(e.name==='voyage'&&e.getAttribute('data-en')===x[0])e.checked=true})});majBr()}
 el.hidden=!tr.length;el.textContent=el.getAttribute('data-t').replace('{f}',tr.map(function(x){return (C.fetes[x[0]]||x[0])+' '+x[3]}).join(', '))}
/* services evidents preajoutes a la premiere visite (Moshe 03/11) : chalet + repas de Chabbat pour un sejour complet ; repas de Chabbat seuls si « j'ai deja mon logement » */
function preajout(){ctrls.forEach(function(e){var k=e.getAttribute('data-svc');if((k==='shabbat'||k==='chalet')&&branch()!=='b')e.checked=true})}
/* resume une ligne au-dessus d'Envoyer ; chaque morceau ramene a son ecran, puis Continuer revient ici */
var ret='';
function resume(){var el=document.getElementById('dm-resume');if(!el)return;el.textContent='';var p=path(),morceaux=[];
 var g=num('adultes')+num('enfants')+num('bebes');if(g)morceaux.push([C.t.invites.replace('{n}',g),'qui']);
 var l=(lieuIn&&lieuIn.value)||'';if(l&&(p.indexOf('ou')>=0||skip))morceaux.push([l,'ou']);
 var a=raw('arrivee'),d=raw('depart');if(a&&d)morceaux.push([fcourt(a)+'–'+fcourt(d),(p.indexOf('quand')>=0||skip)?'quand':(p.indexOf('quandvan')>=0?'quandvan':'lyon')]);
 else{var m=raw('mois');if(m)morceaux.push([m,'quand'])}
 var sv=ctrls.filter(function(e){return e.checked&&!e.disabled&&e.closest('.pf-tl,.pf-bn')}).map(function(e){var t=e.closest('.pf-tl,.pf-bn').querySelector('b');return t?t.textContent:e.value});
 if(sv.length)morceaux.push([sv.join(', '),p.indexOf('services')>=0?'services':(p.indexOf('besoins')>=0?'besoins':'extras')]);
 if(!morceaux.length){el.hidden=true;return}
 morceaux.forEach(function(m,i){if(i){el.appendChild(document.createTextNode(' · '))}var b=document.createElement('button');b.type='button';b.className='pf-res-b';b.textContent=m[0];b.setAttribute('data-go',m[1]);el.appendChild(b)});
 var ed=document.createElement('span');ed.className='pf-res-e';ed.textContent=' '+C.t.edit;el.appendChild(ed);el.hidden=false}
function fcourt(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return v;try{return new Date(+m[1],+m[2]-1,+m[3],12).toLocaleDateString(C.loc,{day:'numeric',month:'short'})}catch(x){return v}}
/* 04/11 : lien prerempli (i=b, lieu, arrivee) : ou et quand sautes, rappel en une ligne en haut de « qui », chaque morceau ramene a son ecran */
function frange(a,d){var m=/^(\d{4})-(\d\d)-(\d\d)$/,x=m.exec(a),y=m.exec(d||'');if(!x)return '';var A=new Date(+x[1],+x[2]-1,+x[3],12),o={day:'numeric',month:'long',year:'numeric'};
 try{if(y){var D=new Date(+y[1],+y[2]-1,+y[3],12),fm=new Intl.DateTimeFormat(C.loc,o);if(fm.formatRange)return fm.formatRange(A,D).replace(/[\u2013\u2014]/g,'-');return fcourt(a)+'-'+fcourt(d)}return A.toLocaleDateString(C.loc,o)}catch(e){return a+(d?'-'+d:'')}}
function recap(){var el=document.getElementById('dm-recap');if(!el)return;if(!skip||cur!=='qui'){el.hidden=true;return}
 el.textContent='';var l=((lieuIn&&lieuIn.value)||'').split(/,\s*/).filter(Boolean).map(function(x){return C.stHe[x]||x}).join(', '),d=frange(raw('arrivee'),raw('depart')),k=0;
 function bt(txt,w,c){var b=document.createElement('button');b.type='button';b.className=c;b.setAttribute('data-edit',w);b.textContent=txt;if(k++)el.appendChild(document.createTextNode(' \u00b7 '));el.appendChild(b)}
 if(l)bt(l,'ou','pf-rc-b');if(d)bt(d,'quand','pf-rc-b');bt(C.t.change,'all','pf-rc-e');el.hidden=false}
/* repas de Chabbat precoche (parcours b) quand le sejour couvre une nuit de vendredi a samedi, tant que les repas n'ont pas ete touches */
function hasShab(){var a=dnum(raw('arrivee')),nn=nights();return a!==null&&nn>0&&nshab(nn)>0}
function defautRepas(){if(cur!=='besoins'||repasTouched||branch()!=='b')return;var rs=els('repas');if(!rs.length||rs.some(function(e){return e.checked}))return;
 if(hasShab())rs.forEach(function(e){if(e.getAttribute('data-pre')==='shabbat')e.checked=true})}
/* brillance de selection : un balayage clair, une fois, seulement apres un toucher ou un clic (jamais au clavier, jamais en mouvement reduit) */
document.addEventListener('pointerdown',function(){ptr=Date.now()},true);
function flash(el){if(!mo())return;el.classList.remove('pf-flash');void el.offsetWidth;el.classList.add('pf-flash');el.addEventListener('animationend',function g(){el.classList.remove('pf-flash');el.removeEventListener('animationend',g)})}
function ckey(e){return (e.type==='checkbox'||e.type==='radio')?'k:'+e.name+'|'+(e.getAttribute('data-en')||e.value):'i:'+(e.id||e.name)}
/* 02/11 : reponses gardees dans ce navigateur (localStorage, 30 jours), par champ et non par position ; effacees a l'envoi */
function save(){try{var v={};ctrls.forEach(function(e){if(e.type==='checkbox'||e.type==='radio'){if(e.checked)v[ckey(e)]=1}else if(e.value)v[ckey(e)]=e.value});
 localStorage.setItem(KEY,JSON.stringify({t:Date.now(),c:cur,v:v}))}catch(x){}}
function load(){try{var s=JSON.parse(localStorage.getItem(KEY)||'null');if(!s||!s.v)return;if(!(Date.now()-s.t<TTL)){localStorage.removeItem(KEY);return}
 ctrls.forEach(function(e){var k=ckey(e);if(e.type==='checkbox'||e.type==='radio')e.checked=!!s.v[k];else if(k in s.v)e.value=s.v[k]});cur=s.c||'';restaure=true}catch(x){}}
function dnum(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);return m?Date.UTC(+m[1],+m[2]-1,+m[3]):null}
function nights(){var a=dnum(raw('arrivee')),d=dnum(raw('depart'));return a!==null&&d!==null?Math.round((d-a)/864e5):null}
function shabbats(nn){var el=document.getElementById('dm-shabbat');var a=dnum(raw('arrivee'));if(cur!=='quand'||!(nn>0)||a===null||nn>60){el.hidden=true;return}
 var out=[];for(var k=0;k<nn;k++){var d=new Date(a+k*864e5);if(d.getUTCDay()===5){var s=new Date(a+(k+1)*864e5);out.push(s.toLocaleDateString(C.loc,{day:'numeric',month:'long',timeZone:'UTC'}))}}
 el.hidden=!out.length;el.textContent=el.getAttribute('data-t')+' '+out.join(', ')}
function norm(x){return x.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'')}
function autoc(inp){var g=f.querySelector('.pf-auto[data-for="'+inp.id+'"]');if(!g)return;var segs=inp.value.split(/,\s*/),q=norm(segs[segs.length-1].trim());var n=0;
 [].forEach.call(g.children,function(b){var t=norm(b.getAttribute('data-v')),ok=(!q||t.indexOf(q)>=0)&&t!==q&&n<6;b.hidden=!ok;if(ok)n++});g.hidden=!n}
f.addEventListener('input',function(ev){if(ev.target.matches&&ev.target.matches('input[type=text]'))autoc(ev.target)});
f.addEventListener('focusin',function(ev){if(ev.target.matches&&ev.target.matches('input[type=text]'))autoc(ev.target)});
f.addEventListener('focusout',function(ev){var g=ev.target.id&&f.querySelector('.pf-auto[data-for="'+ev.target.id+'"]');if(g)setTimeout(function(){g.hidden=true},200)});
function plis(){[].forEach.call(f.querySelectorAll('.pf-pli'),function(d){var n=d.querySelectorAll('input:checked').length,b=d.querySelector('.pf-pli-n');b.hidden=!n;b.textContent=b.getAttribute('data-t').replace('{n}',n)})}
function render(){fetes();var p=sync();if(p.indexOf(cur)<0)cur=p[0];defautRepas();
 etapes.forEach(function(e){e.hidden=e.getAttribute('data-e')!==cur});
 var i=p.indexOf(cur),last=cur==='final',b=branch();f.classList.toggle('avance',i>0);
 nav.hidden=false;bBack.hidden=i<=0;bNext.hidden=last;bSend.hidden=!last;petit.hidden=!last;accord.hidden=!last;if(!sent)bSend.disabled=false;
 var nn=cur==='quand'?nights():null,bad=nn!==null&&nn<0;shabbats(nn);
 nuitsP.hidden=!(nn!==null&&nn>=1);if(!nuitsP.hidden)nuitsP.textContent=nn===1?C.t.nuit:C.t.nuits.replace('{n}',nn);dateErr.hidden=!bad;
 bNext.disabled=bad;
 var n=i+1,N=p.length;ptxt.textContent=C.t.step.replace('{n}',n).replace('{t}',N);var pc=Math.round(n/N*100);
 [].forEach.call(f.querySelectorAll('.pf-pas'),function(x){x.setAttribute('aria-pressed',x.classList.contains('on')?'true':'false')});barre.style.width=pc+'%';barreC.setAttribute('aria-valuenow',pc);
 majN();fetesMois();majBudget();recap();if(last)resume();
 save()}
function show(id,push,focus){var p=sync();if(p.indexOf(id)<0)id=p[0];
 var oi=p.indexOf(cur),ni=p.indexOf(id);f.setAttribute('data-dir',ni<oi?'back':'fwd');
 cur=id;render();
 dl.push({event:'form_step',step:cur,step_index:p.indexOf(cur)+1,branch:branch()});
 if(push){try{history.pushState({e:cur},'','#e-'+cur)}catch(x){}}
 if(focus){var h=document.querySelector('.pf-etape[data-e="'+cur+'"] h2:not([hidden])');if(h)h.focus({preventScroll:true});
  var r=f.getBoundingClientRect();if(r.top<0||r.top>200)window.scrollTo({top:window.pageYOffset+r.top-90,behavior:'smooth'})}}
function next(){if(ret){var r=ret;ret='';if(reskip){skip=true;reskip=false}show(r,true,true);return}var p=path(),i=p.indexOf(cur);if(i>=0&&i<p.length-1)show(p[i+1],true,true)}
function back(){var p=path(),i=p.indexOf(cur);if(i>0)show(p[i-1],true,true)}
bNext.addEventListener('click',next);bBack.addEventListener('click',back);
f.addEventListener('click',function(ev){
 var sg=ev.target.closest&&ev.target.closest('.pf-auto button');if(sg){var inp=document.getElementById(sg.parentNode.getAttribute('data-for')),v=sg.getAttribute('data-v'),segs=inp.value.split(/,\s*/);
  segs[segs.length-1]=v;inp.value=segs.join(', ');sg.parentNode.hidden=true;inp.focus();inp.dispatchEvent(new Event('input',{bubbles:true}));return}
 if(ev.target.closest&&ev.target.closest('#dm-ess-b')){essentiels();return}
 var ed=ev.target.closest&&ev.target.closest('[data-edit]');if(ed){var w=ed.getAttribute('data-edit');skip=false;if(w==='all'){ret='';reskip=false}else{ret='qui';reskip=true}show(w==='quand'?'quand':'ou',true,true);return}
 var rb=ev.target.closest&&ev.target.closest('.pf-res-b');if(rb){var g=rb.getAttribute('data-go');if(skip&&(g==='ou'||g==='quand')){skip=false;reskip=true}ret='final';show(g,true,true);return}
 var ps=ev.target.closest&&ev.target.closest('.pf-pas');if(ps){ps.classList.toggle('on');if(ps.classList.contains('on')&&Date.now()-ptr<800)flash(ps);var pc0=f.querySelector('input[name="lieu_pas_choisi"]');if(pc0)pc0.checked=false;majLieu();render();return}
 var bt=ev.target.closest&&ev.target.closest('.cpt button');if(!bt)return;
 var inp=bt.parentNode.querySelector('input'),v0=parseInt(inp.value,10)||0,plus=bt.className==='plus',v=Math.max(0,Math.min(99,v0+(plus?1:-1)));inp.value=v;
 inp.dispatchEvent(new Event('input',{bubbles:true}))});
function onchg(ev){var t=ev.target;
 if(t===accordCb&&t.checked){accord.classList.remove('pf-manque');accordErr.hidden=true}
 if(t.getAttribute&&t.getAttribute('aria-invalid')==='true'&&(t.value||'').trim())t.setAttribute('aria-invalid','false');
 if(t.name==='arrivee'&&t.type==='date'){[].forEach.call(f.querySelectorAll('input[name="depart"]'),function(x){x.min=t.value})}
 if(ev.type==='change'&&t.name==='priorites'){mx.hidden=true;
  if(t.checked&&els('priorites').filter(function(e){return e.checked}).length>3){t.checked=false;mx.hidden=false}}
 if(ev.type==='change'&&ev.isTrusted&&t.name==='lieu_pas_choisi'&&t.checked){[].forEach.call(f.querySelectorAll('.pf-pas.on'),function(x){x.classList.remove('on')});autreIn.value='';majLieu()}
 if(t===autreIn)majLieu();
 if(t.name==='deja'||t.name==='voyage')majBr();
 if(t.name==='repas'&&ev.isTrusted)repasTouched=true;
 if(t.name==='budget_total'){var bn=bnum(t.value),es0=estim(),bh=document.getElementById('dm-bhint');if(bh)bh.hidden=!(bn>0&&bn<1000);
  if(bn>=1000&&es0.e){var r0=bn/es0.e,k0=r0>=1.1?'Above this':r0>=.9?'Around this':'Below this';els('budget_avis').forEach(function(e){e.checked=(e.getAttribute('data-en')===k0)})}}
 render();
 if(ev.type==='change'&&ev.isTrusted&&t.checked&&Date.now()-ptr<800){var lb=t.closest&&t.closest('.pf-c,.pf-tl,.pf-niv');if(lb)flash(lb)}
 /* un toucher, passage automatique quand la reponse ne demande rien de plus */
 if(ev.type==='change'&&ev.isTrusted&&t.checked){var en=t.getAttribute('data-en');
  if(t.name==='minyan_niveau'&&(en==='Not needed'||en==='Not sure, advise me'))setTimeout(next,mo()?380:120);
  if(t.name==='budget_avis'&&en!=='Below this')setTimeout(next,mo()?900:500)}}
f.addEventListener('change',onchg);f.addEventListener('input',onchg);
window.addEventListener('popstate',function(ev){var id=ev.state&&ev.state.e;show(id||path()[0],false,true)});
f.addEventListener('submit',function(ev){ev.preventDefault();if(sent)return;
 if(cur!=='final'){if(!bNext.disabled)next();return}
 if(f.elements.societe&&f.elements.societe.value){location.href=C.merci;return}
 var nom=val('prenom'),tel=val('tel'),ind=val('indicatif');var err=document.getElementById('dm-erreur');
 var manque=[];['prenom','indicatif','tel'].forEach(function(n){var e=f.elements[n];if(!e)return;var vide=!(e.value||'').trim();e.setAttribute('aria-invalid',vide?'true':'false');if(vide)manque.push(e)});
 accord.classList.toggle('pf-manque',!accordCb.checked);
 if(manque.length||!accordCb.checked){err.hidden=!manque.length;accordErr.hidden=accordCb.checked;
  var first=manque.length?manque[0]:accordCb;first.focus({preventScroll:true});first.scrollIntoView({behavior:'smooth',block:'center'});return}
 var parts=[];C.lab.forEach(function(kv){var v=val(kv[0]);if(v)parts.push(kv[1]+': '+v)});
 var partsEn=[];C.labEn.forEach(function(kv){var v=val(kv[0],true);if(v)partsEn.push(kv[1]+': '+v)});
 var dates=[val('arrivee'),val('depart')].filter(Boolean).join(C.k.datesj);
 var pers=val('adultes')?val('adultes')+C.k.adultes:'';if(val('enfants'))pers+=(pers?' + ':'')+val('enfants')+C.k.enfants;if(val('bebes'))pers+=(pers?' + ':'')+val('bebes')+C.k.bebes;
 var nn=nights();
 var payload=JSON.stringify({tour:C.k.tour+(val('voyage')||C.k.none),dates:dates,personnes:pers,langue:C.langNom,nom:nom,contact:(ind+' '+tel.replace(/[^0-9]/g,'')).trim()+(val('email')?' / '+val('email'):''),message:parts.join(' | '),message_en:partsEn.join(' | '),nuits:nn!==null&&nn>0?nn:'',page:location.pathname,params:location.search});
 // On attend la reponse du script avant « merci » ; en cas d'echec, la demande part par WhatsApp en un geste.
 sent=true;var lab0=bSend.textContent;bSend.disabled=true;bSend.textContent=C.t.sending;
 var fini=false,ok=function(){if(fini)return;fini=true;try{localStorage.removeItem(KEY)}catch(e){}
  dl.push({event:'generate_lead',branch:branch(),budget:val('budget_total')||val('budget')});location.href=C.merci},
 ko=function(){if(fini)return;fini=true;sent=false;bSend.disabled=false;bSend.textContent=lab0;
  var txt=(nom+' · '+dates+' · '+pers+'\n'+parts.join('\n')).slice(0,1800);
  var box=document.getElementById('dm-repli');if(!box){box=document.createElement('p');box.id='dm-repli';box.className='pf-erreur';nav.parentNode.insertBefore(box,nav)}
  box.hidden=false;box.innerHTML='';box.appendChild(document.createTextNode(C.t.ko[0]+' '));
  var a=document.createElement('a');a.href='https://wa.me/33652092301?text='+encodeURIComponent(txt);a.rel='noopener';a.textContent=C.t.ko[1];a.className='btn-noir';box.appendChild(a);
  box.scrollIntoView({behavior:'smooth',block:'center'});dl.push({event:'form_error'})};
 setTimeout(ko,20000);
 try{fetch(window.MISHPACHA_ENDPOINT,{method:'POST',body:payload}).then(function(r){return r.json()}).then(function(j){j&&j.ok?ok():ko()})['catch'](ko)}catch(e){ko()}});
function prefill(){var q;try{q=new URLSearchParams(location.search)}catch(x){return}
 function s(k){var v=q.get(k);return v?v.replace(/[\u0000-\u001f<>]/g,'').trim().slice(0,80):''}
 function n(k){var v=(q.get(k)||'').trim();return /^\d{1,2}$/.test(v)?parseInt(v,10):null}
 function d(k){var v=s(k),m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return '';var x=new Date(Date.UTC(+m[1],+m[2]-1,+m[3]));
  return x.getUTCFullYear()===+m[1]&&x.getUTCMonth()===+m[2]-1&&x.getUTCDate()===+m[3]?v:''}
 function fill(name,v){ctrls.forEach(function(e){if(e.name===name&&e.type!=='checkbox'&&e.type!=='radio')e.value=v})}
 var i=s('i').toLowerCase(),r=/^[a-f]$/.test(i)?ctrls.filter(function(e){return e.name==='intention'&&e.value===i})[0]:null;
 if(r){r.checked=true;base=i;if(i==='b')ctrls.forEach(function(e){if(e.name==='deja')e.checked=e.value==='1'})}
 var l=s('lieu');if(l)fill('lieu',l);
 var a=d('arrivee'),b=d('depart');if(a)fill('arrivee',a);if(b)fill('depart',b);if(a)ctrls.forEach(function(e){if(e.name==='flexible')e.checked=(e.getAttribute('data-en')==='Dates are fixed')});if(a)ctrls.forEach(function(e){if(e.name==='depart')e.min=a});
 ['adultes','enfants','bebes'].forEach(function(k){var v=n(k);if(v!==null)fill(k,String(v))});
 var vy=s('voyage').toLowerCase();if(vy)ctrls.forEach(function(e){if(e.name==='voyage'&&(e.getAttribute('data-en')||e.value).toLowerCase()===vy)e.checked=true});
 if(i==='b'&&l&&a){pre=true;skip=true}}
/* indicatif prerempli (Moshe 02/11 : jamais tape) : langue du navigateur, puis fuseau, puis langue de la page */
function devine(sel){if(!sel||sel.value)return;var R={US:'+1',CA:'+1',GB:'+44',IL:'+972',FR:'+33',BE:'+32',CH:'+41',ES:'+34',IT:'+39',DE:'+49',NL:'+31',AR:'+54',MX:'+52',BR:'+55',AU:'+61',ZA:'+27',RU:'+7',UA:'+380'},
 L={he:'+972',iw:'+972',fr:'+33',es:'+34',it:'+39',de:'+49',nl:'+31',ru:'+7',uk:'+380',pt:'+55'};
 function poser(v){if(v&&!sel.value&&[].some.call(sel.options,function(o){return o.value===v}))sel.value=v}
 (navigator.languages||[navigator.language||'']).forEach(function(l){var m=/^([a-z]{2,3})(?:-([A-Z]{2}))?/i.exec(l||'');if(!m)return;poser(m[2]?R[m[2].toUpperCase()]:'');poser(L[m[1].toLowerCase()])});
 if(!sel.value){var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(x){}
  poser(/Jerusalem|Tel_Aviv/.test(tz)?'+972':/^America\/(New_York|Chicago|Denver|Los_Angeles|Toronto|Montreal)/.test(tz)?'+1':/London/.test(tz)?'+44':/Paris/.test(tz)?'+33':'')}
 if(!sel.value)poser(C.indic)}
/* bandeau cookies : le bouton Continuer colle en bas se pose au-dessus du bandeau tant qu'il est affiche */
function cb(){var c=document.querySelector('.cb'),h=c&&!c.hidden?Math.ceil(c.getBoundingClientRect().height):0;document.documentElement.style.setProperty('--pf-cb',h+'px')}
try{new MutationObserver(cb).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']})}catch(x){}
window.addEventListener('resize',cb);
if(window.MT_PRIX)grille(window.MT_PRIX);document.addEventListener('mt-prix',function(ev){grille(ev.detail);majBudget()});
load();prefill();majBr();if(!restaure)preajout();initLieu();devine(f.elements.indicatif);f.classList.add('js');dl.push({event:'form_start',branch:branch()});show(cur||path()[0],false,false);cb();try{history.replaceState({e:cur},'')}catch(x){}
})();
</script>'''

def js(lang):
    T = lambda s: tt(s, lang)
    lab = dict(LAB[lang]); i = LANGS.index(lang)
    for k, v in LAB_NEW.items(): lab[k] = v[i]
    lab_en = dict(LAB["en"]); lab_en.update({k: v[0] for k, v in LAB_NEW.items()})
    KO = {"fr": ["Votre demande n’est pas partie. Envoyez-la-nous sur WhatsApp en un geste :", "Envoyer sur WhatsApp"],
          "es": ["Su solicitud no se envió. Envíenosla por WhatsApp con un toque:", "Enviar por WhatsApp"],
          "he": ["הבקשה לא נשלחה. שלחו לנו בוואטסאפ בלחיצה אחת:", "שליחה בוואטסאפ"],
          "en": ["Your request did not go through. Send it to us on WhatsApp in one tap:", "Send on WhatsApp"]}[lang]
    cfg = {"lang": lang, "langNom": {"en": "English", "fr": "Français", "es": "Español", "he": "עברית"}[lang], "loc": LOCALE[lang], "merci": MERCI[lang], "paths": PATHS, "total": 8, "chaletBase": CHALET_BASE, "fetes": {k: v[LANGS.index(lang)] for k, v in FETES_NOMS.items()}, "stHe": STATIONS_HE if lang == "he" else {},
           "indic": {"he": "+972", "fr": "+33", "es": "+34", "en": ""}[lang],
           "lab": [[k, lab[k]] for k in LAB_ORDER], "labEn": [[k, lab_en[k]] for k in LAB_ORDER],
           "k": {"tour": JSX[lang]["tour"], "none": JSX[lang]["none"], "datesj": JSX[lang]["datesj"], "adultes": JSX[lang]["adultes"], "enfants": JSX[lang]["enfants"],
                 "bebes": JSX[lang]["bebes"], "logementB": T("Already booked, I need services only")},
           "prix": PRIX_N, "t": {"step": T("Step {n} of {t}"), "invites": T("{n} guests"), "edit": T("Edit"), "change": T("Change"), "perso": T("For your {g} guests, {n} {p}, with {s}, plan from about {x}"), "perso0": T("For your {g} guests, {n} {p}. Add services to see a starting price."), "large": T("Your selection is a large project: we will build it with you."), "dem": T(", plus services on request"), "dans": T("in {p}"), "alpes": T("in the Alps"), "ou": T(" or "), "et": T(" and "), "semaine": T("a week"), "s_chalet": T("a chalet"), "s_chef": T("a private chef"), "s_livre": T("delivered meals"), "s_shabbat": T("Shabbat meals"), "s_lyon": T("the Lyon tour"), "n_occupe": T("A very busy period: the best chalets go early."), "n_station": T("One of the most sought-after resorts in the Alps."), "n_groupe": T("For a large group we combine chalets."), "f_below": T("We'll focus on what matters most: your kosher meals. Many families book their own apartment, and we take care of the meals, Shabbat and the minyan."), "torah": T("Sefer Torah in the chalet"), "k_below_p": T("below (essentials proposed)"), "k_below_c": T("below (essentials chosen)"), "p_chef": T("delivered meals instead of a private chef"), "p_station": T("a resort with lower prices, such as Val Thorens"), "p_appart": T("an apartment instead of a private chalet"), "p_court": T("a shorter stay or fewer services"), "f_around": T("Perfect: we will build your stay around this."), "f_above": T("Wonderful: we can add every comfort you wish."), "f_discuss": T("We'll talk it through on WhatsApp."), "k_below": T("below"), "k_around": T("around"), "k_above": T("above"), "k_discuss": T("discuss"), "estimate": T("estimate"),"nuits": T("{n} nights"), "nuit": T("1 night"), "sending": T("Sending…"), "ko": KO}}
    assert set(LAB_ORDER) >= set(LAB[lang]), set(LAB[lang]) - set(LAB_ORDER)
    return JS_TPL.replace("__CFG__", json.dumps(cfg, ensure_ascii=False))

# ---------------------------------------------------------------- CSS (bloc delimite dans styles.css), charte LV
# Prefixe de lv.css (7 :not(#id)) : passe devant valora*.css et les anciennes regles .dm-* ; classes pf-* neuves, aucune regle ancienne ne les touche.
P = "html body.valora.lv" + "".join(f":not(#lv{i})" for i in range(1, 8))
CSS_A, CSS_Z = "/* ===DEMANDE-ETAPES=== */", "/* ===/DEMANDE-ETAPES=== */"
CSS = CSS_A + """
/* Formulaire /plan-your-trip/ en 3 ecrans, charte LV (02/11) : blanc, noir pour les boutons, filets gris, coins 4 px, aucune carte ni ombre. */
.pf-etape[hidden],.pf [data-b][hidden],.pf [data-s][hidden],.pf [data-si][hidden],.pf .cache,.pf [hidden]{display:none!important}
P main>section.pf-hero:not(#pf0){padding:18px 0 0!important;margin:0!important;background:#FFFFFF}
P .pf-hero .wrap{max-width:688px!important;margin:0 auto!important;padding:0 24px!important;box-sizing:border-box}
P .pf-hero .fil{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#6B6B6B!important;opacity:1!important;margin:0}
P .pf-hero .fil a{color:#6B6B6B!important}
P main .pf-hero h1{margin:10px 0 0!important;font-size:clamp(26px,4.4vw,44px)!important;font-weight:300!important;letter-spacing:.08em!important}
P .pf-promesse{margin:10px 0 0;max-width:34em;font-size:15px;line-height:1.5;color:#6B6B6B!important}
body:has(#formDemande.avance) .pf-hero{display:none!important}
P main>section.pf:not(#pf0){padding:22px 24px 72px!important;max-width:688px!important;box-sizing:border-box;margin:0 auto!important;background:#FFFFFF;color:#111111}
P .pf-form{max-width:720px;margin:0}
P .pf .piege{position:absolute;left:0;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
/* progression 1 / 3 */
P .pf-prog{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:12px 14px;min-height:28px;margin:0 0 30px}
P .pf-prog-txt{grid-column:2;justify-self:end;font-size:11px;font-weight:400;letter-spacing:.2em;text-transform:uppercase;color:#111111}
P .pf-barre{grid-column:1 / -1;height:1px;background:#E6E6E6;overflow:hidden}
P .pf-barre i{display:block;height:100%;width:33%;background:#111111;transition:width .3s}
/* tetes d'ecran */
P .pf-tete{margin:0 0 30px}
P main .pf-tete h2{margin:0!important;font-size:26px!important;line-height:1.2!important;letter-spacing:.08em!important;outline:none}
P .pf-tete p{margin:6px 0 0;font-size:14px;line-height:1.45;color:#6B6B6B!important}
/* ecran 1 : six lignes, picto 48 px centre, hauteur fixe (controle_alignement.py --ancre centre) */
P .pf-choix{border-top:1px solid #E6E6E6}
P .pf-ligne{position:relative;display:grid;grid-template-columns:56px 1fr 20px;align-items:center;gap:0 14px;height:80px;padding:0 4px;border-bottom:1px solid #E6E6E6;cursor:pointer;overflow:hidden;transition:background-color .15s}
P .pf-ligne input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-ligne img{display:block;width:48px;height:48px;object-fit:contain;justify-self:center}
P .pf-l-t{display:grid;gap:3px;min-width:0}
P .pf-l-t b{font-size:13.5px;font-weight:400!important;letter-spacing:.1em;text-transform:uppercase;line-height:1.25;color:#111111}
P .pf-l-t small{font-size:13px;line-height:1.3;color:#6B6B6B}
P .pf-fl{width:9px;height:9px;border-top:1px solid #111111;border-right:1px solid #111111;transform:rotate(45deg);justify-self:center}
html[dir=rtl] .pf-ligne .pf-fl{transform:rotate(-135deg)!important}
P .pf-ligne:hover,P .pf-ligne:has(input:checked){background:#F4F4F2}
P .pf-ligne:has(input:checked) b{color:#5B3A29}
P .pf-ligne:has(input:focus-visible){outline:2px solid #111111;outline-offset:-2px}
P .pf-wa{margin:20px 0 0;text-align:center;font-size:14px;color:#6B6B6B!important}
P .pf-wa a{color:#111111!important;text-decoration:underline;text-underline-offset:3px}
/* champs */
P .pf-etape > * + *{margin-top:20px}
P .pf-sous{margin:26px 0 8px!important;font-size:11px;font-weight:400;letter-spacing:.2em;text-transform:uppercase;color:#111111!important}
P .pf-champ{position:relative;display:grid;gap:6px}
P .pf-champ label{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#6B6B6B}
P .pf-champ :is(input,select,textarea){width:100%;box-sizing:border-box;min-height:48px;padding:11px 13px;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;color:#111111;font-size:16px;font-weight:300;box-shadow:none;color-scheme:light}
P .pf-champ textarea{min-height:88px;resize:vertical}
P .pf-champ :is(input,select,textarea):focus{outline:none;border-color:#111111}
P .pf-champ ::placeholder{color:#9A9A9A}
P .pf-champ [aria-invalid=true]{border-color:#9B2C1F}
P .pf-duo{display:grid;grid-template-columns:1fr 1fr;gap:12px}
P .pf-tel{display:grid;grid-template-columns:136px 1fr;gap:8px;direction:ltr}
P .pf :is(.btn-noir,.pf-retour,summary,.pf-sous,label,.pf-l-t b):lang(he){letter-spacing:0!important}
P .pf :is(.pf-tel input,.pf-tel select,.cpt input,.pf-prog-txt){font-family:'Jost',system-ui,sans-serif!important}
P .pf-prog-txt{direction:ltr;unicode-bidi:isolate}
P main .pf-tete h2:lang(he),P main .pf-hero h1:lang(he){letter-spacing:0!important}
P:has(#formDemande.avance) main>section.pf:not(#pf0){padding-top:48px!important}
P .pf-tel select{-webkit-appearance:none;appearance:none;padding:0 28px 0 12px;background:#FFFFFF url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23111' stroke-width='1.2'/%3E%3C/svg%3E") no-repeat right 10px center;font-size:15px}
P .pf-auto{position:absolute;top:100%;left:0;right:0;z-index:5;margin-top:2px;background:#FFFFFF;border:1px solid #111111;border-radius:4px;overflow:hidden}
P .pf-auto button{display:block;width:100%;text-align:start;padding:12px 14px;border:0;border-top:1px solid #E6E6E6;background:#FFFFFF;font-size:15px;font-weight:300;color:#111111;cursor:pointer}
P .pf-auto button:first-child{border-top:0}
P .pf-auto button:hover,P .pf-auto button:focus-visible{background:#F4F4F2}
/* cases : liste a coches, sans cadre ni pastille, deux colonnes */
P .pf-chips{display:grid;grid-template-columns:1fr;gap:10px}
P #e-quand .pf-chips{grid-template-columns:1fr 1fr}
/* 03/11 : cartes de services (« Build your stay »), panier, estimation et alertes de budget */
P .pf-svcs{display:grid;grid-template-columns:1fr;gap:10px}
P .pf-svc{position:relative;display:grid;grid-template-columns:1fr auto;align-items:center;gap:6px 14px;padding:16px 16px 16px 18px;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;cursor:pointer;transition:border-color .15s,background-color .15s}
P .pf-svc input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-svc:hover{border-color:#111111}
P .pf-svc:has(input:focus-visible){outline:2px solid #111111;outline-offset:2px}
P .pf-svc-t{display:grid;gap:4px;min-width:0}
P .pf-svc-t b{font-size:13.5px;font-weight:400!important;letter-spacing:.1em;text-transform:uppercase;line-height:1.3;color:#111111}
P .pf-svc-t small{font-size:13.5px;line-height:1.4;color:#6B6B6B}
P .pf-svc-p{font-style:normal;font-size:13px;color:#5B3A29}
P .pf-svc-add{flex:none;min-width:92px;padding:9px 12px;border:1px solid #111111;border-radius:4px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;text-align:center;color:#111111;background:#FFFFFF}
P .pf-svc-add .d{display:none}
P .pf-svc-add i{font-style:normal!important}
P .pf-svc:has(input:checked){border-color:#111111;background:#F4F4F2}
P .pf-svc:has(input:checked) .pf-svc-add{background:#111111;color:#FFFFFF}
P .pf-svc:has(input:checked) .pf-svc-add .a{display:none}
P .pf-svc:has(input:checked) .pf-svc-add .d{display:inline}
P .pf-svc-add:lang(he),P .pf-svc-t b:lang(he){letter-spacing:0}
P .pf-nsvc{flex:none;font-size:12px;letter-spacing:.08em;color:#5B3A29}
P .pf-est{margin:0 0 6px;padding:16px 0;border-top:1px solid #E6E6E6;border-bottom:1px solid #E6E6E6;font-size:16px;line-height:1.45;color:#111111}
P .pf-est:empty{display:none}
P .pf-fit{margin:10px 0 0;padding:0 0 0 14px;border-left:2px solid #6B6B6B;font-size:14px;line-height:1.5;color:#111111}
html[dir=rtl] .pf-fit{padding:0 14px 0 0!important;border-left:0!important;border-right:2px solid #6B6B6B!important}
P .pf-fit-fits{border-color:#111111}
P .pf-fit-fits::before{content:'\2713  '}
P .pf-fit-below{border-color:#5B3A29}
P .pf-fit-far-below{border-color:#9B2C1F;color:#9B2C1F}

P .pf [data-b] > * + *{margin-top:20px}
P #e-quand .pf-c{padding:12px 14px;font-size:14.5px}
P .pf-c{position:relative;display:flex;align-items:center;min-height:56px;padding:14px 18px;box-sizing:border-box;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;font-size:15px;line-height:1.3;cursor:pointer;transition:background-color .15s,border-color .15s,color .15s}
P .pf-c input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-c:hover{border-color:#111111}
P .pf-c:has(input:focus-visible){outline:2px solid #111111;outline-offset:2px}
P .pf-pastilles{display:grid;grid-template-columns:1fr 1fr;gap:10px}
P .pf-pas{min-height:56px;padding:12px 14px;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;color:#111111;font-size:15px;font-weight:300;line-height:1.25;text-align:center;cursor:pointer;transition:background-color .15s,border-color .15s,color .15s}
P .pf-pas:hover{border-color:#111111}
P .pf-pas.on{background:#111111;border-color:#111111;color:#FFFFFF}
P .pf-c:has(input:checked){background:#111111;border-color:#111111;color:#FFFFFF}
P .pf-c:has(input:checked) span{color:#FFFFFF!important}
P .pf-chips:has(> .pf-c:only-child){grid-template-columns:1fr}
/* compteurs */
P .pf-cpt{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:56px;border-bottom:1px solid #E6E6E6}
P .pf-cpt .lib{font-size:15px;line-height:1.3}
P .pf-cpt .cpt{display:flex;align-items:center;gap:4px;direction:ltr;flex:none}
P .pf-cpt .cpt button{width:42px;height:42px;padding:0;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;color:#111111;font-size:20px;font-weight:300;line-height:1;cursor:pointer}
P .pf-cpt .cpt button:hover{border-color:#111111}
P .pf-cpt .cpt input{width:44px;border:0;background:transparent;padding:0;text-align:center;font-size:19px;font-weight:300;color:#111111;-moz-appearance:textfield;appearance:textfield}
P .pf-cpt .cpt input::-webkit-outer-spin-button,P .pf-cpt .cpt input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
/* sections repliees */
P .pf-plus{margin-top:30px}
P details.pf-pli{border-top:1px solid #E6E6E6;margin:0!important}
P details.pf-pli:last-child{border-bottom:1px solid #E6E6E6}
P details.pf-pli summary{display:flex;align-items:center;gap:10px;min-height:52px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#111111;cursor:pointer;list-style:none}
P details.pf-pli summary::-webkit-details-marker{display:none}
P details.pf-pli summary::after{content:"";margin-inline-start:auto;width:8px;height:8px;border-right:1px solid #111111;border-bottom:1px solid #111111;transform:rotate(45deg);transition:transform .2s}
P details.pf-pli[open] summary::after{transform:rotate(-135deg)}
P .pf-pli-n{font-size:11px;letter-spacing:.04em;text-transform:none;color:#5B3A29}
P .pf-pli-c{padding:0 0 18px}
P .pf-pli-c > * + *{margin-top:14px}
P .pf-contact .pf-pli:first-of-type{margin-top:28px!important}
/* textes d'aide, erreurs, notes */
P .pf-info{font-size:13.5px;color:#5B3A29!important;margin:8px 0 0}
P .pf-aide{font-size:13px;color:#6B6B6B!important}
P .pf-erreur{font-size:13.5px;color:#9B2C1F!important}
P .pf-erreur .btn-noir{display:table;margin:14px auto 0}
P .pf-note{font-size:13.5px;line-height:1.5;padding:12px 0 0;border-top:1px solid #E6E6E6;color:#6B6B6B!important}
/* accord, navigation */
P .pf-accord{margin:32px 0 0;font-size:13.5px;line-height:1.5}
P .pf-accord label{display:flex;gap:12px;align-items:flex-start;cursor:pointer}
P .pf-accord input{flex:none;width:20px;height:20px;margin:1px 0 0;accent-color:#111111}
P .pf-accord a{color:#111111!important;text-decoration:underline;text-underline-offset:3px}
P .pf-accord .pf-erreur{display:block;margin:8px 0 0;margin-inline-start:32px}
P .pf-accord.pf-manque span{color:#9B2C1F}
P .pf-nav{display:flex;align-items:center;gap:12px;margin:36px 0 0}
P .pf-nav .btn-noir:not(#pf0){min-height:52px;padding:0 34px;margin-inline-start:auto;background:#111111!important;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;border:1px solid #111111!important;border-radius:4px!important;font-size:12px!important;letter-spacing:.2em!important;text-transform:uppercase}
P .pf-nav .btn-noir:disabled{opacity:.35;cursor:default}
P .pf-nav .btn-noir:not(#pf0):lang(he){letter-spacing:0!important;font-size:15px!important}
P .pf-retour{grid-column:1;display:inline-flex;align-items:center;gap:8px;min-height:28px;padding:0;border:0;background:none;color:#111111;font-size:11px;letter-spacing:.2em;text-transform:uppercase;cursor:pointer}
P .pf-retour span{width:7px;height:7px;border-left:1px solid #111111;border-bottom:1px solid #111111;transform:rotate(45deg)}
html[dir=rtl] .pf-retour span{transform:rotate(-135deg)!important}
@media (prefers-reduced-motion:no-preference){P .pf-form[data-dir] .pf-etape:not([hidden]){animation:pf-in .38s ease-out}P .pf-form[data-dir=back]{--pf-dx:-18px}html[dir=rtl] .pf-form[data-dir=fwd]{--pf-dx:-18px}html[dir=rtl] .pf-form[data-dir=back]{--pf-dx:18px}}
@keyframes pf-in{from{opacity:0;transform:translateX(var(--pf-dx,18px))}}
P .pf-petit{margin:16px 0 0;text-align:center;font-size:12.5px;color:#6B6B6B!important}
body:has(#formDemande) .wa-flottant{display:none!important}
@media (min-width:700px){
  P main>section.pf-hero:not(#pf0){padding-top:36px!important}
  P main>section.pf:not(#pf0){padding-top:34px!important}
  P main .pf-tete h2{font-size:34px!important}
  P .pf-chips{grid-template-columns:1fr 1fr;gap:12px}
  P .pf-pastilles{grid-template-columns:repeat(3,1fr)}
  P .pf-ligne{height:84px}
}
@media (max-width:699px){
  /* telephone : Continuer colle en bas, au-dessus du bandeau cookies quand il est affiche (--pf-cb, mesure en JS) */
  P .pf-form{padding-bottom:96px}
  P .pf-nav{position:fixed;left:0;right:0;bottom:var(--pf-cb,0px);z-index:60;margin:0;padding:10px 24px calc(10px + env(safe-area-inset-bottom));background:#FFFFFF;border-top:1px solid #E6E6E6}
  P .pf-nav .btn-noir{flex:1;padding:0 18px}
  P .pf-chips{gap:10px}
  P .pf-c{font-size:15px}
  body:has(#formDemande.avance) .pied{display:none}
}
/* 03/11 v4 (Moshe : « condense, ultra luxe, sans swiper ») : chaque ecran tient dans 390 x 844, en-tete, barre, bouton et bandeau cookies compris */
body:has(#formDemande) .pied{display:none!important}
P .pf-tl{position:relative;display:grid;grid-template-columns:52px 1fr;align-items:center;gap:0 14px;height:64px;padding:6px 40px 6px 6px;box-sizing:border-box;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;cursor:pointer;overflow:hidden;transition:border-color .15s}
P .pf-tl input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-tl-img{display:contents}
P .pf-tl img{grid-row:1 / span 2;width:52px;height:52px;object-fit:cover;border-radius:2px;display:block}
P .pf-tl b{align-self:end;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px;font-weight:400!important;letter-spacing:.06em;text-transform:uppercase;line-height:1.2;color:#111111}
P .pf-tl small{align-self:start;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:12px;line-height:1.25;color:#5B3A29;margin-top:3px}
P .pf-tl i{position:absolute;top:50%;margin-top:-10px;inset-inline-end:12px;width:20px;height:20px;border:1px solid #CFCFCF;box-sizing:border-box;background:#FFFFFF!important;opacity:1!important;border-radius:50%;background:#111111;opacity:0;transition:opacity .15s}
P .pf-tl:has(input:checked) i::after{content:"";position:absolute;left:6px;top:3px;width:4px;height:8px;border-right:1.5px solid #FFFFFF;border-bottom:1.5px solid #FFFFFF;transform:rotate(45deg)}
P .pf-tl:has(input:checked){border:2px solid #111111;padding:5px 39px 5px 5px}
P .pf-tl{--x:0}
P .pf-tl:has(input:checked) i{background:#111111!important;border-color:#111111}
P .pf-tl:has(input:focus-visible){outline:2px solid #111111;outline-offset:2px}
P .pf-tl b:lang(he){letter-spacing:0}
P .pf-tls{display:grid;grid-template-columns:1fr;gap:8px}
P .pf-mcs{display:grid;grid-template-columns:1fr 1fr;gap:8px}
P .pf-mc{position:relative;display:grid;justify-items:center;align-content:center;gap:8px;height:112px;padding:8px;box-sizing:border-box;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;text-align:center;font-size:13.5px;line-height:1.25;cursor:pointer}
P .pf-mc input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-mc img{width:48px;height:48px;display:block}
P .pf-mc:has(input:checked){border:2px solid #111111;padding:7px;background:#F4F4F2}
P .pf-mc:has(input:focus-visible){outline:2px solid #111111;outline-offset:2px}
P .pf-pastilles{grid-template-columns:repeat(3,1fr)!important;gap:8px}
P .pf-pas{min-height:44px;padding:6px 6px;font-size:13px;letter-spacing:.02em}
P .pf-pas.on{background:#111111!important;border-color:#111111!important;color:#FFFFFF!important}
P .pf-pas.on span{color:#FFFFFF!important}
P .pf-perso{margin:0;font-size:17px;line-height:1.45;color:#111111}
P .pf-notes{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:4px}
P .pf-notes li{font-size:13px;line-height:1.4;color:#5B3A29}
P .pf-notes li::before{content:"";display:inline-block;width:5px;height:5px;margin-inline-end:8px;vertical-align:2px;background:#5B3A29}
P .pf-notes:empty{display:none}
P .pf-avis .pf-chips{grid-template-columns:1fr 1fr!important}
P .pf-avis[hidden]{display:none!important}
P .pf-resume{margin:12px 0 0;padding:8px 0 0;text-transform:none!important;letter-spacing:0!important;border-top:1px solid #E6E6E6;font-size:13.5px;line-height:1.5;color:#111111}
P .pf-res-b{padding:0;border:0;background:none;font:inherit;font-size:13.5px!important;text-transform:none!important;letter-spacing:0!important;color:inherit;text-decoration:underline;text-decoration-color:#CFCFCF;text-underline-offset:3px;cursor:pointer}
P .pf-res-e{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6B6B6B}
P #e-quand .pf-chips{grid-template-columns:1fr 1fr}
P #e-quand [data-si] .pf-chips{grid-template-columns:repeat(4,1fr)}
P #e-quand [data-si] .pf-c{padding:8px 4px;justify-content:center;text-align:center;font-size:13px}
@media (max-width:699px){
  P main>section.pf-hero:not(#pf0){position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);padding:0!important}
  P main>section.pf:not(#pf0){padding:40px 24px 0!important}
  P .pf-form{padding-bottom:calc(76px + var(--pf-cb,0px))}
  P .pf-prog{margin:0 0 16px;min-height:24px;gap:8px 12px}
  P .pf-tete{margin:0 0 14px}
  P main .pf-tete h2{font-size:21px!important;line-height:1.2!important}
  P .pf-tete p{margin-top:4px;font-size:13px}
  P .pf-etape > * + *,P .pf [data-b] > * + *{margin-top:12px}
  P .pf-sous{margin:16px 0 6px!important}
  P .pf-chips{gap:8px}
  P .pf-c{min-height:46px;padding:10px 14px;font-size:14px}
  P .pf-cpt{min-height:50px}
  P .pf-cpt .cpt button{width:38px;height:38px}
  P .pf-champ{gap:4px}
  P .pf-champ :is(input,select){min-height:44px;padding:9px 12px}
  P .pf-champ textarea{min-height:52px;height:52px}
  P .pf-nav{padding:8px 24px calc(8px + env(safe-area-inset-bottom))!important}
  P .pf-nav .btn-noir:not(#pf0){min-height:48px}
  P .pf-accord{margin-top:14px;font-size:12.5px}
  P .pf-petit{display:none!important}
  P .pf-wa{display:none}
}
/* 03/11 v5 : dates par mois par defaut, extras compacts sur 2 colonnes, minyan en lignes a trois pastilles, bouton « essentiels » */
P .pf-off{display:none!important}
P .pf-bascule{grid-template-columns:1fr 1fr!important}
P .pf-tls2{grid-template-columns:1fr 1fr!important;gap:8px}
P .pf-tls2 .pf-tl{grid-template-columns:40px 1fr;gap:0 8px;height:56px;padding:5px 26px 5px 5px}
P .pf-tls2 .pf-tl:has(input:checked){padding:4px 25px 4px 4px}
P .pf-tls2 .pf-tl img{width:40px;height:40px}
P .pf-tls2 .pf-tl b{font-size:11.5px;letter-spacing:.04em;white-space:normal;line-height:1.15;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
P .pf-tls2 .pf-tl small{font-size:10.5px}
P .pf-tls2 .pf-tl i{width:16px;height:16px;margin-top:-8px;inset-inline-end:6px}
P .pf-tls2 .pf-tl:has(input:checked) i::after{left:5px;top:2px;width:3.5px;height:7px}
P .pf-bess{display:grid;gap:10px}
P .pf-bes{display:grid;gap:6px;padding:0 0 10px;border-bottom:1px solid #E6E6E6}
P .pf-bes-t{display:flex;align-items:center;gap:10px}
P .pf-bes-t img{width:32px;height:32px;object-fit:cover;border-radius:2px;flex:none}
P .pf-bes-t b{font-size:13px;font-weight:400!important;letter-spacing:.06em;text-transform:uppercase;line-height:1.25}
P .pf-bes-t b:lang(he){letter-spacing:0}
P .pf-nivs{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
P .pf-niv{position:relative;display:flex;align-items:center;justify-content:center;min-height:38px;padding:4px 6px;box-sizing:border-box;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;font-size:12.5px;line-height:1.15;text-align:center;cursor:pointer}
P .pf-niv input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
P .pf-niv:has(input:checked){background:#111111;border-color:#111111;color:#FFFFFF}
P .pf-niv:has(input:focus-visible){outline:2px solid #111111;outline-offset:2px}
P .pf-ess{margin:10px 0 0}
P .pf-ess-b{min-height:40px;padding:0 16px;border:1px solid #111111;border-radius:4px;background:#FFFFFF;color:#111111;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
P .pf-ess-b:lang(he){letter-spacing:0}
/* 03/11 : page /merci/ en charte LV */
P main>section.pf-merci:not(#pf0){padding:56px 24px 72px!important;background:#FFFFFF}
P .pf-merci-c{max-width:640px;margin:0 auto;text-align:center}
P .pf-merci-hp{display:block;width:40px;height:auto;margin:0 auto 22px}
P .pf-merci .fil{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#6B6B6B!important;opacity:1!important;margin:0}
P .pf-merci .fil a{color:#6B6B6B!important}
P main .pf-merci h1{margin:14px 0 0!important;font-size:clamp(24px,4vw,38px)!important;font-weight:300!important;letter-spacing:.08em!important;line-height:1.2!important}
P main .pf-merci h1:lang(he){letter-spacing:0!important}
P .pf-merci-t{margin:16px auto 0;max-width:30em;font-size:16px;line-height:1.55;color:#111111}
P .pf-merci-b:not(#pf0){display:inline-flex;align-items:center;gap:10px;margin-top:30px;min-height:52px;padding:0 28px;background:#111111!important;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;border:1px solid #111111!important;border-radius:4px!important;font-size:12px!important;letter-spacing:.18em!important;text-transform:uppercase}
P .pf-merci-b svg{width:18px;height:18px;fill:currentColor}
P .pf-merci-r{margin-top:26px;font-size:13px}
P .pf-merci-r a{color:#111111!important;text-decoration:underline;text-underline-offset:3px}
/* 03/11 : vignette « Lyon tour » (prix sur deux lignes au besoin, jamais coupe) */
P .pf-tls2 .pf-tl small{white-space:normal;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;text-overflow:clip}
/* 03/11 : petits ecrans (iPhone SE 375 x 667) : chaque ecran tient au-dessus de Continuer, bandeau cookies affiche, sans defiler */
@media (max-width:699px) and (max-height:760px){
  P main>section.pf:not(#pf0){padding-top:30px!important}
  P .pf-prog{margin:0 0 10px;min-height:22px}
  P .pf-tete{margin:0 0 10px}
  P main .pf-tete h2{font-size:18px!important;line-height:1.2!important}
  P .pf-tete p{margin-top:3px;font-size:12.5px;line-height:1.35}
  P .pf-etape > * + *,P .pf [data-b] > * + *{margin-top:8px}
  P .pf-sous{margin:10px 0 4px!important}
  P .pf-pastilles{gap:6px}
  P .pf-pas{min-height:36px;padding:3px 4px;font-size:12px;line-height:1.15}
  P #e-ou{display:grid;grid-template-columns:1fr 1fr;column-gap:8px;align-items:start}
  P #e-ou>*{grid-column:1/-1}
  P #e-ou>.pf-chips,P #e-ou>div[data-b="abe"]{grid-column:auto}
  P #e-ou>.pf-chips .pf-c,P #e-ou>div[data-b="abe"] .pf-c{height:100%}
  P #e-ou>.pf-chips{display:grid}
  P .pf-chips{gap:6px}
  P .pf-c{min-height:40px;padding:7px 12px;font-size:13px;line-height:1.25}
  P .pf-cpt{min-height:40px}
  P .pf-cpt .cpt button{width:34px;height:34px}
  P .pf-champ{gap:3px}
  P .pf-champ :is(input,select){min-height:40px;padding:7px 12px}
  P .pf-champ textarea{min-height:40px;height:40px}
  P .pf-tls{gap:6px}
  P .pf-tl{height:54px;padding:4px 40px 4px 4px;grid-template-columns:46px 1fr}
  P .pf-tl:has(input:checked){padding:3px 39px 3px 3px}
  P .pf-tl img{width:46px;height:46px}
  P .pf-tls2 .pf-tl{height:50px;grid-template-columns:38px 1fr}
  P .pf-tls2 .pf-tl img{width:38px;height:38px}
  P .pf-bess{gap:6px}
  P .pf-bes{gap:4px;padding:0 0 6px}
  P .pf-bes-t img{width:26px;height:26px}
  P .pf-niv{min-height:34px}
  P .pf-resume{margin-top:8px;padding-top:6px;font-size:12.5px;line-height:1.4}
  P .pf-res-b{font-size:12.5px!important}
  P .pf-accord{margin-top:8px!important;font-size:11.5px;line-height:1.35}
  P .pf-nav{padding:6px 24px calc(6px + env(safe-area-inset-bottom))!important}
  P .pf-nav .btn-noir:not(#pf0){min-height:44px}
  P:has(#formDemande) .cb{padding:8px 12px!important;gap:8px!important}
  P:has(#formDemande) .cb p{font-size:12px!important;line-height:1.3!important}
  P:has(#formDemande) .cb button{min-height:34px!important;padding:0 10px!important;letter-spacing:.08em!important}
  P:has(#formDemande.avance) main>section.pf:not(#pf0){padding-top:30px!important}
  P .pf-champ>*+*{margin-top:0!important}
  P .pf-resume{display:none!important}
  P .pf-tls:not(.pf-tls2){grid-template-columns:1fr 1fr}
  P .pf-tls:not(.pf-tls2) .pf-tl{height:60px;grid-template-columns:38px 1fr;gap:0 8px;padding:4px 26px 4px 4px}
  P .pf-tls:not(.pf-tls2) .pf-tl:has(input:checked){padding:3px 25px 3px 3px}
  P .pf-tls:not(.pf-tls2) .pf-tl img{width:38px;height:52px}
  P .pf-tls:not(.pf-tls2) .pf-tl b{font-size:11.5px;letter-spacing:.04em;white-space:normal;line-height:1.15}
  P .pf-tls:not(.pf-tls2) .pf-tl small{font-size:10.5px;white-space:normal;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;text-overflow:clip}
  P .pf-tls:not(.pf-tls2) .pf-tl i{width:16px;height:16px;margin-top:-8px;inset-inline-end:6px}
  P .pf-tls:not(.pf-tls2) .pf-tl:has(input:checked) i::after{left:5px;top:2px;width:3.5px;height:7px}
}

/* 04/11 v6 (retour de Moshe sur l'ecran « Quand » : « joli, mais pas intuitif, tous les boutons se ressemblent ») : trois familles lisibles sans lire.
   (a) CHOIX = cases et chips : trait gris fin ; choisi = fond noir, texte or brosse #A88F5E (6,1:1 sur #111111), balayage clair une fois.
   (b) CONTROLES D'INTERFACE = segments sur une ligne, filet or de 2 px sous le segment actif : ils changent l'ecran, ils ne repondent pas.
   (c) CHAMPS = filet bas seul, libelle en petites capitales grises au-dessus. Continuer reste seul en noir plein. */
P .pf-c,P .pf-pas,P .pf-niv,P .pf-tl{position:relative;overflow:hidden;border:1px solid #CFCFCF;border-radius:4px;background:#FFFFFF;color:#111111;transition:background-color .16s cubic-bezier(.23,1,.32,1),border-color .16s cubic-bezier(.23,1,.32,1),color .16s cubic-bezier(.23,1,.32,1),transform .16s cubic-bezier(.23,1,.32,1)}
/* lv.css colle « label>span{color:#5E5E5E!important} » avec 8 :not(#lv) : c'est ce gris qui rendait le choix coche illisible sur le noir (le :is() de cette regle contient #formContact : 9 identifiants). Prefixe renforce : 9 :not(#lv). */
Q .pf-c span,Q .pf-pas span,Q .pf-niv span{color:#111111!important}
P .pf-c:hover,P .pf-pas:hover,P .pf-niv:hover,P .pf-tl:hover{border-color:#111111}
P .pf-c:has(input:checked),P .pf-pas.on,P .pf-niv:has(input:checked),P .pf-tl:has(input:checked){background:#111111;border-color:#111111;color:#A88F5E}
Q .pf-c:has(input:checked) span,Q .pf-niv:has(input:checked) span,Q .pf-c:has(input:checked) b,Q .pf-c:has(input:checked) small,Q .pf-pas.on span{color:#A88F5E!important}
Q .pf-bn small span{color:inherit!important}
Q .pf-tl b{color:#111111!important}
Q .pf-tl:has(input:checked) b,Q .pf-tl:has(input:checked) small{color:#A88F5E!important}
P .pf-tl:has(input:checked) i{background:#A88F5E!important;border-color:#A88F5E!important}
P .pf-tl:has(input:checked) i::after{border-color:transparent #111111 #111111 transparent}
P .pf-c::before,P .pf-pas::before,P .pf-niv::before,P .pf-tl::before{content:"";position:absolute;top:0;bottom:0;left:0;right:0;z-index:1;pointer-events:none;opacity:0;transform:translateX(-110%);background:linear-gradient(105deg,rgba(255,255,255,0) 28%,rgba(255,255,255,.5) 50%,rgba(255,255,255,0) 72%)}
@media (prefers-reduced-motion:no-preference){
  P .pf-flash::before{animation:pf-brille .7s cubic-bezier(.4,0,.2,1) 1}
  P .pf-c:active,P .pf-pas:active,P .pf-niv:active,P .pf-tl:active{transform:scale(.97)}
}
@keyframes pf-brille{from{opacity:1;transform:translateX(-110%)}to{opacity:1;transform:translateX(110%)}}
/* (b) controles segmentes : bascule des dates, « j'ai deja mon logement » */
P .pf-seg-b{display:flex;align-items:stretch;margin:0;border-bottom:1px solid #E0E0E0}
P .pf-seg{position:relative;flex:1 1 0;display:flex;align-items:center;justify-content:center;min-width:0;min-height:44px;padding:6px 6px 8px;box-sizing:border-box;text-align:center;font-size:13.5px;font-weight:300;line-height:1.2;letter-spacing:0;color:#6B6B6B;cursor:pointer;transition:color .16s cubic-bezier(.23,1,.32,1)}
P .pf-seg input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
Q .pf-seg span{color:inherit!important}
P .pf-seg::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#A88F5E;opacity:0;transform:scaleX(.5);transition:transform .22s cubic-bezier(.23,1,.32,1),opacity .22s cubic-bezier(.23,1,.32,1)}
P .pf-seg:hover{color:#111111}
P .pf-seg:has(input:checked){color:#111111;font-weight:400}
P .pf-seg:has(input:checked)::after{opacity:1;transform:scaleX(1)}
P .pf-seg:has(input:focus-visible){outline:2px solid #111111;outline-offset:-2px}
/* (c) champs : filet bas seul */
P .pf-champ :is(input,select,textarea){border:0;border-bottom:1px solid #CFCFCF;border-radius:0;background-color:transparent;padding:6px 0 8px;min-height:44px;box-shadow:none;font-family:inherit;-webkit-appearance:none;appearance:none;transition:border-color .16s ease-out,box-shadow .16s ease-out}
P .pf-champ textarea{min-height:52px;height:52px;resize:none}
P .pf-champ :is(input,select,textarea):focus{border-bottom-color:#111111;box-shadow:0 1px 0 0 #111111;outline:none}
P .pf-champ input[type=date]{display:block;text-align:start}
P .pf-champ input[type=date]::-webkit-date-and-time-value{text-align:start}
P .pf-tel select{padding:6px 22px 8px 0;background-position:right 2px center}
P .pf-cpt{border-bottom-color:#CFCFCF}
P .pf-cpt .cpt button{border:0;background:transparent;width:44px;height:44px;border-radius:50%;font-size:24px}
P .pf-cpt .cpt button:hover{background:#F4F4F2}
P .pf-cpt .cpt button:active{background:#E6E6E6}
@media (max-width:699px){P .pf-nsvc{display:none!important}}
P .pf-ess-b{min-height:36px;padding:0 0 2px;border:0;border-bottom:1px solid #A88F5E;border-radius:0;background:none}
/* rappel du lien prerempli, en haut de « qui » */
P .pf-recap{margin:0 0 12px;font-size:13px;line-height:1.5;color:#6B6B6B}
P .pf-rc-b{padding:6px 2px;margin:-6px 0;border:0;background:none;font:inherit;color:#111111;text-decoration:underline;text-decoration-color:#CFCFCF;text-underline-offset:3px;cursor:pointer}
P .pf-rc-e{padding:6px 2px;margin:-6px 0;border:0;background:none;font:inherit;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6B6B6B;cursor:pointer}
P .pf-rc-e:lang(he){letter-spacing:0;font-size:13px}
/* ecran « besoins » du parcours b */
P .pf-bchips{display:grid;grid-template-columns:1fr 1fr;gap:8px}
P .pf-bn{min-height:46px;padding:7px 12px;justify-content:flex-start}
P .pf-bn>span{display:grid;gap:1px;min-width:0}
Q .pf-bn b{font-size:13.5px;font-weight:400;line-height:1.2;color:#111111!important}
P .pf-bn small span{display:inline;color:inherit}
Q .pf-bn small{font-size:11.5px;line-height:1.2;color:#6B6B6B!important}
P .pf-chips.pf-flow{display:flex!important;flex-wrap:wrap;gap:6px}
P .pf-flow .pf-c{min-height:36px;padding:6px 12px;font-size:13px;flex:0 0 auto}
P #e-besoins .pf-sous{margin:14px 0 6px!important}
P #e-besoins>.pf-sous:first-of-type{margin-top:0!important}
@media (max-width:699px) and (max-height:760px){
  P #e-ou>.pf-chips,P #e-ou>div[data-b="abe"]{grid-column:1/-1}
  P #e-besoins .pf-sous{margin:8px 0 4px!important}
  P .pf-bchips{gap:6px}
  P .pf-bn{min-height:42px;padding:5px 10px}
  P .pf-seg{min-height:40px}
  P .pf-champ :is(input,select){min-height:38px;padding:5px 0 6px}
  P .pf-cpt .cpt button{width:38px;height:38px;font-size:22px}
}
@media (max-width:699px) and (max-height:620px){
  P .pf-tete p{display:none}
  Q main .pf-tete h2{font-size:15px!important;letter-spacing:.03em!important;line-height:1.2!important}
  P .pf-champ textarea{min-height:36px;height:36px}
  P #e-quand:has(input[name=flexible][data-en="Dates are fixed"]:checked) #dm-fetes .pf-c:not(:has(input:checked)):not(:has(input[data-en="Another holiday"])){display:none}
  P .pf-pas{min-height:32px;padding:2px 3px;font-size:11.5px;line-height:1.12}
  P .pf-pastilles{gap:5px}
  P #e-besoins .pf-sous{display:none}
  P:has(#formDemande) .cb{padding:6px 12px!important;gap:8px!important}
  P:has(#formDemande) .cb p{font-size:11px!important;line-height:1.2!important}
  P:has(#formDemande) .cb button{min-height:30px!important;padding:0 8px!important}
  P #e-final>*+*{margin-top:4px}
  P .pf-cpt{min-height:34px}
  P .pf-cpt .cpt button{width:34px;height:34px}
  P .pf-recap{margin:0 0 4px;line-height:1.3}
  P .pf-bn{min-height:38px}
  P .pf-accord{margin-top:4px!important}
  Q .pf-bn b{font-size:12.5px!important}
  Q .pf-bn small{font-size:10.5px!important}
  P .pf-bn{padding:4px 8px}
  P #e-besoins>.pf-sous:first-of-type{display:none}
  P .pf-bn{min-height:40px;padding:4px 10px}
}
/* 05/11 (Moshe : « il manque des elements en or, dans les barres ») : barre de progression, puces et filet du message de budget en or brosse ; aide du montant */
P .pf-barre{height:2px}
P .pf-barre i{background:#A88F5E}
P .pf-notes li::before{background:#A88F5E}
P .pf-fit,P .pf-fit-fits{border-left-color:#A88F5E}
P .pf-champ :is(input,select,textarea):focus-visible{outline:none}
P .pf-bhint{margin:6px 0 0;font-size:13px;line-height:1.4;color:#5B3A29}
P .pf-bhint[hidden]{display:none}
/* 05/11 : ecran final du b (adresse du logement ajoutee) : sur petit ecran, ou tant que le bandeau cookies est affiche, le titre « Vos coordonnees » reste lu par les lecteurs d'ecran mais ne prend plus de hauteur ; aucun texte retreci */
@media (max-width:699px) and (max-height:620px){
  P #e-final .pf-tete{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;margin:0}
}
@media (max-width:699px) and (max-height:760px){
  P:has(.cb:not([hidden])) #e-final .pf-tete{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;margin:0}
}
""".replace("P:has", P + ":has").replace("P ", P + " ").replace(",P ", "," + P + " ").replace("Q ", P + ":not(#lv8):not(#lv9) ").replace(",Q ", "," + P + ":not(#lv8):not(#lv9) ") + CSS_Z

def update_css():
    c = open("styles.css", encoding="utf-8").read()
    if CSS_A in c:
        a = c.index(CSS_A); z = c.index(CSS_Z) + len(CSS_Z)
        c = c[:a] + CSS + c[z:]
    else:
        c = c.rstrip("\n") + "\n" + CSS + "\n"
    io.open("styles.css", "w", encoding="utf-8", newline="\n").write(c)

# ---------------------------------------------------------------- ecriture
HERO_RE = re.compile(r'<section class="(?:pratique-hero demande-hero|pf-hero)">.*?</section>', re.S)
FORM_RE = re.compile(r'<section class="[^"]*\b(?:demande|pf)\b[^"]*" id="demande">.*?</section>', re.S)
JS_RE = re.compile(r"<script>\n\(function\(\)\{var f=document.getElementById\('formDemande'\);if\(!f\)return;.*?</script>", re.S)
if __name__ == "__main__":
    update_css()
    for lang in LANGS:
        p = "plan-your-trip/index.html" if lang == "en" else f"{lang}/plan-your-trip/index.html"
        s = io.open(p, encoding="utf-8").read()
        s, n1 = HERO_RE.subn(lambda m: hero(lang), s, count=1)
        s, n2 = FORM_RE.subn(lambda m: formulaire(lang), s, count=1)
        s, n3 = JS_RE.subn(lambda m: js(lang), s, count=1)
        assert (n1, n2, n3) == (1, 1, 1), (p, n1, n2, n3)
        s = s.replace('<link rel="stylesheet" href="/valora-form.css">', "")
        if '/js/prix.js' not in s: s = s.replace('</body>', '<script src="/js/prix.js" defer></script>\n</body>', 1)   # 03/11 : prix de la grille de Mendel
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("ok", p)
