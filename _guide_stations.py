# -*- coding: utf-8 -*-
"""Guide des stations et renforcement Val Thorens / Courchevel (livrable 06-reports/2026-10-30-contenus-alpes-he-en.md,
validé par Moshé le 30/10 : « intègre le guide des stations »). EN et HE seulement (ES gelé par le comité, pas de cible FR Alpes).
Idempotent : relancer ne change rien. Lancer depuis site-v5/ : python _guide_stations.py

1. Page neuve /french-ski-resorts-kosher-guide/ et /he/french-ski-resorts-kosher-guide/ : clone de la page
   /kosher-ski-holidays-french-alps/ de la même langue (en-tête, CSS Valora, menu, pied, formulaire #book, WhatsApp flottant),
   <main> remplacé par le guide, hreflang en + he + x-default seulement, sélecteur de langue EN et HE seulement
   (voir SEULES dans _build_i18n.py), JSON-LD BreadcrumbList + FAQPage + WebPage dans la langue de la page.
2. Val Thorens et Courchevel, EN et HE : title, meta, og, H1, fil d'Ariane, paragraphes 1 et 2, bloc « ce que le devis peut
   inclure » avant la carte chalet, JSON-LD (WebPage, BreadcrumbList). Sources tenues à jour : _pages/kosher-val-thorens.py,
   _pages/kosher-courchevel.py, _pages/alps.py (EN) et _intros_courtes_trad.json (intro HE).
3. HE Courchevel : phrase manquante de la puce « שפים פרטיים » rétablie.
4. Liens entrants sur /alps/ et /he/alps/ : guide (puce Grenoble), Val Thorens (puce Grenoble), Courchevel (puce Courchevel).
5. index.md des pages touchées (même moteur que _agentic.py).
Aucun prix, aucun nombre de chalets. Ne touche ni aux blocs de prix, ni à _seo_semaine1.py, ni à js/prix.js.
Ne pas lancer « _build_i18n.py ld » sur tout le site : il remet en anglais le JSON-LD de 39 pages (constaté le 30/10)."""
import html, io, json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DATE = "2026-10-30"
BASE = "https://mishpachatours.com"
SLUG = "french-ski-resorts-kosher-guide"
B = lambda s: f'<bdi dir="ltr">{s}</bdi>'
MARQUE = "<!--GUIDE-STATIONS-->"

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
def esc(s): return html.escape(s, quote=True)
def plat(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def ecrire(p, s):
    """Écrit seulement si le contenu change ; garde les fins de ligne du fichier existant."""
    if os.path.exists(p):
        o = rd(p)
        if "\r\n" in o and "\r\n" not in s: s = s.replace("\n", "\r\n")
        if s == o: print("ok   ", p); return
    wr(p, s); print("écrit", p)

def remplace(s, old, new, p):
    if new in s and (old not in s or old in new): return s
    assert old in s, f"introuvable dans {p} : {old[:100]}"
    return s.replace(old, new)

LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
def ld(s, fn):
    m = LD.search(s); d = json.loads(m.group(2)); fn(d if isinstance(d, list) else [d])
    return s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]

def meta(s, title, desc):
    """title + description + og/twitter (même échappement que les pages existantes)."""
    s = re.sub(r"<title>.*?</title>", lambda _: f"<title>{esc(title)} | Mishpacha Tours</title>", s, count=1, flags=re.S)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + esc(desc), s)
    for k in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + esc(title), s)
    return s

# =====================================================================================================================
# 1. Guide des stations
# =====================================================================================================================
EN = dict(
  title="French Ski Resorts for Kosher Families",
  desc="Eleven French ski resorts compared for a kosher family: altitude, ski level, time from Lyon and Geneva, and what our kosher team organises in each one.",
  crumbs=[("Home", "/"), ("The Alps, strictly kosher", "/alps/"), ("French ski resorts, a kosher guide", None)],
  h1="French ski resorts, a kosher guide", ital="altitude, ski level, travel time and the kosher side, resort by resort",
  intro=["Most kosher families who ski in France choose between Les 3 Vallées (Val Thorens, Courchevel), Les Deux Alpes and Megève.",
         "Val Thorens is the highest resort in Europe, Les Deux Alpes has the largest share of easy slopes in this guide, and Megève and Annecy are the closest to Geneva. In every resort below, our kosher team based in the Alps organises a private chef in your chalet or delivered meals, Shabbat ready before candle lighting and, when enough families are there that week, a minyan with a Sefer Torah."],
  choisir=("How to choose <i>your resort</i>",
           "Start with the level of the youngest skier in the family. Resorts with a high share of easy slopes (Les Deux Alpes, La Plagne) suit beginners and children; Tignes and Val d'Isère suit confident skiers. Then look at the road: on a Friday, the drive has to end well before candle lighting, and a winter Saturday or a snowfall can add an hour. Lyon-Saint-Exupéry is about two hours from most resorts; Geneva is closer to Megève, Chamonix and Annecy."),
  h2_stations="The resorts, <i>one by one</i>",
  labels=("Altitude.", "Ski level.", "The road.", "The kosher side."),
  stations=[
    ("Val Thorens", "kosher-val-thorens", "Kosher Val Thorens",
     "2,300 m, the highest ski resort in Europe, in Les 3 Vallées.",
     "Les 3 Vallées count 600 km of slopes, 56 % easy, 34 % intermediate, 10 % difficult. Every level finds its runs.",
     "From Lyon: 2 h 30 without traffic. From Geneva: ask us for the transfer time.",
     "Private chef or delivered meals, Shabbat and the holidays; a minyan when enough families are in the resort that week."),
    ("Courchevel", "kosher-courchevel", "Kosher Courchevel",
     "About 1,850 m for Courchevel 1850, with its lower villages, in Les 3 Vallées.",
     "The same 600 km area as Val Thorens, 56 % easy slopes.",
     "From Lyon: 2 h 10 without traffic. From Geneva: ask us for the transfer time.",
     "A Chabad house in winter, which we coordinate with for your minyan and Shabbat; chef or delivered meals in Courchevel 1850 and the villages."),
    ("Les Deux Alpes", "kosher-les-deux-alpes", "Kosher Les Deux Alpes",
     "1,650 m, with a glacier above the resort.",
     "220 km of slopes, 65 % easy, the highest share in this guide. Good for beginners and families.",
     "From Lyon: 2 h 10 in dry conditions. From Geneva: ask us for the transfer time.",
     "Orthodox families have come here in summer for decades; our kosher chalets are in the resort, with a chef or delivered meals."),
    ("Megève", "kosher-megeve", "Kosher Megève",
     "About 1,050 m, on the Évasion Mont-Blanc area.",
     "The Megève and Saint-Gervais slopes count 185 km, 37 % easy and 48 % intermediate. Families and relaxed skiers.",
     "From Lyon: 2 h 10 without traffic. From Geneva: 1 h 15 by road.",
     "A Chabad house in winter; for a minyan in your week, we build it with the Chabad network of the Alps and bring a Sefer Torah."),
    ("Alpe d'Huez", "kosher-alpe-dhuez", "Kosher Alpe d'Huez",
     "About 1,860 m, the main resort of the Grand Domaine.",
     "250 km of slopes, 52 % intermediate. Best for skiers who already link their turns.",
     "From Lyon: 2 h 20, the last stretch up 21 hairpin bends. From Grenoble: 1 h. From Geneva: ask us.",
     "A long kosher summer history; our team covers the Grenoble side of the massif."),
    ("Chamonix", "kosher-chamonix", "Kosher Chamonix",
     "The town sits at about 1,040 m, at the foot of Mont Blanc; the ski areas climb to 2,767 m at Grands Montets.",
     "Separate high mountain areas (Brévent and Flégère, Grands Montets, Les Houches, Le Tour). Our source does not publish a level split for the valley.",
     "From Lyon: 2 h 15 to 3 h. From Geneva: 1 h 15 to 1 h 30, the closest airport.",
     "No kosher hotel or shop in the valley; we deliver meals or send a chef, in winter and in summer."),
    ("La Plagne", "kosher-la-plagne", "Kosher La Plagne",
     "11 villages, up to Plagne Aime 2000 at about 2,100 m.",
     "225 km of slopes, about 62 % easy, linked to Les Arcs in Paradiski (425 km). Good for families.",
     "From Lyon: 2 h 14 without traffic. From Geneva: 2 h 20.",
     "Tell us your village, as deliveries are planned village by village."),
    ("Les Arcs", "kosher-les-arcs", "Kosher Les Arcs",
     "Four villages, Arc 1600, 1800, 1950 and 2000.",
     "200 km of slopes, about half of them easy, linked to La Plagne.",
     "From Lyon: 2 h 25 to 3 h to Bourg-Saint-Maurice, then the climb. From Geneva: 2 h 30 to 3 h.",
     "No kosher shop or restaurant in the resort in winter; chef or delivered meals, and a minyan when enough families are there."),
    ("Val d'Isère", "kosher-val-disere", "Kosher Val d'Isère",
     "1,850 m, sharing 300 km of slopes with Tignes, up to 3,456 m.",
     "63 % intermediate and 27 % difficult. For confident skiers.",
     "From Lyon: 2 h 30 to 3 h. From Geneva: 2 h 40 to 3 h 30.",
     "Chalets are the usual way to stay, so a chef or delivered meals fit well. The last 32 km are mountain road: plan Friday arrivals with a wide margin before candle lighting."),
    ("Grenoble", "kosher-grenoble", "Kosher Grenoble",
     "214 m. A city, not a ski resort: your base for the Isère resorts.",
     "Depends on the resort you drive to (Alpe d'Huez is 1 h away).",
     "From Lyon: about 1 h by road, or 1 h 04 by direct TGV from the airport. From Geneva: ask us.",
     "A Beth Habad and two synagogues in the city; chef or delivered meals in town or in the resort."),
    ("Annecy", "kosher-annecy", "Kosher Annecy",
     "447 m, on the lake. In winter, families ski at La Clusaz, 37 minutes away.",
     "La Clusaz counts 125 km of slopes, 54 % easy.",
     "From Lyon: 1 h 15. From Geneva: 45 minutes.",
     "A small synagogue, so a minyan for your week is built ahead; chef or delivered meals by the lake or in the Aravis."),
  ],
  source="Ski area figures: skiresort.info, consulted on 30 October 2026. Altitudes and travel times: our resort pages.",
  qui=("Who organises <i>your kosher week</i>",
       "Stays, transfers and meals are organised and invoiced by our kosher team based in the Alps. The team cooks under the Chabad network of the Alps, and the supervision details come in writing with your quote. Nothing is delivered on Shabbat or a holiday: everything is in place before candle lighting."),
  h2_faq="French ski resorts: <i>questions</i>",
  faq=[("Which French ski resort suits a kosher family with young children?",
        "Les Deux Alpes and La Plagne have the largest share of easy slopes in this guide. In both, our team brings a chef or delivered meals to your chalet or apartment, and Shabbat is ready before candle lighting."),
       ("How far are the resorts from Lyon and Geneva?",
        "Most resorts are about two hours from Lyon-Saint-Exupéry without traffic. Megève, Chamonix and Annecy are closer to Geneva, between 45 minutes and 1 h 30. Add time on a winter Saturday or in snow."),
       ("Is there a minyan in every resort?",
        "A minyan depends on how many families are in the resort that week. Courchevel 1850 and Megève have a Chabad house in winter. Elsewhere, give us your dates early and we group the families who write to us, with a Sefer Torah.")],
  h2_suite="Keep <i>reading</i>",
  suite=[("mountain-snow", "/alps/", "The Alps, strictly kosher"), ("snowflake", "/kosher-ski-holidays-french-alps/", "Kosher ski holidays in the Alps"),
         ("chef-hat", "/kosher-services-french-alps/", "Kosher services in the Alps"), ("house", "/kosher-chalets/", "Our kosher chalets")],
)

HE = dict(
  title="אתרי סקי בצרפת: מדריך כשר, אתר אחר אתר",
  desc="אתרי סקי בצרפת למשפחה ששומרת כשרות: גובה, רמת סקי, זמן נסיעה מליון ומז'נבה, ומה הצוות הכשר שלנו מארגן בכל אתר, משף פרטי בצ'אלה ועד מניין.",
  crumbs=[("דף הבית", "/he/"), ("האלפים, כשרים לחלוטין", "/he/alps/"), ("אתרי סקי בצרפת, מדריך כשר", None)],
  h1="אתרי סקי בצרפת, מדריך כשר", ital="גובה, רמת סקי, זמן נסיעה והצד הכשר, אתר אחר אתר",
  intro=["רוב המשפחות ששומרות כשרות ועושות סקי בצרפת בוחרות בין שלושת העמקים (ואל טורנס, קורשבל), לה דז אלפ ומג'ב.",
         "ואל טורנס הוא אתר הסקי הגבוה באירופה, בלה דז אלפ שיעור המסלולים הקלים הוא הגבוה ביותר במדריך הזה, ומג'ב ואנסי הם הקרובים ביותר לז'נבה. בכל אחד מהאתרים כאן, הצוות הכשר שלנו שבסיסו באלפים מארגן שף פרטי בצ'אלה או ארוחות במשלוח, שבת מוכנה לפני הדלקת הנרות, וכשיש מספיק משפחות באותו שבוע, מניין עם ספר תורה."],
  choisir=("איך בוחרים <i>אתר סקי</i>",
           f"מתחילים מהרמה של הגולש הצעיר במשפחה. אתרים עם הרבה מסלולים קלים (לה דז אלפ, לה פלאן) מתאימים למתחילים ולילדים; {B('Tignes')} וואל דיזר מתאימים לגולשים מנוסים. אחר כך בודקים את הדרך: ביום שישי הנסיעה צריכה להסתיים הרבה לפני הדלקת הנרות, ובסוף שבוע של חורף או בשלג הנסיעה מתארכת לפעמים בשעה. נמל התעופה של ליון נמצא כשעתיים מרוב האתרים; ז'נבה קרובה יותר למג'ב, לשמוני ולאנסי."),
  h2_stations="אתרי הסקי, <i>אחד אחד</i>",
  labels=("גובה.", "רמת סקי.", "הדרך.", "הצד הכשר."),
  stations=[
    ("ואל טורנס", "kosher-val-thorens", "ואל טורנס כשר",
     "2,300 מ', אתר הסקי הגבוה באירופה, בשלושת העמקים.",
     "בשלושת העמקים 600 ק\"מ של מסלולים, 56% קלים, 34% בינוניים, 10% קשים. יש מסלולים לכל רמה.",
     "מליון: כשעתיים וחצי ללא פקקים. מז'נבה: שאלו אותנו על זמן ההסעה.",
     "שף פרטי או ארוחות במשלוח, שבת וחגים; מניין כשיש מספיק משפחות באתר באותו שבוע."),
    ("קורשבל", "kosher-courchevel", "קורשבל כשר",
     "כ-1,850 מ' בקורשבל 1850, ולצידה כפרים נמוכים יותר, בשלושת העמקים.",
     "אותו אזור של 600 ק\"מ כמו ואל טורנס, 56% מסלולים קלים.",
     "מליון: שעתיים ועשר דקות ללא פקקים. מז'נבה: שאלו אותנו על זמן ההסעה.",
     "בית חב״ד בחורף, שאיתו אנו מתאמים את המניין ואת השבת שלכם; שף או ארוחות במשלוח בקורשבל 1850 ובכפרים."),
    ("לה דז אלפ", "kosher-les-deux-alpes", "לה דז אלפ כשר",
     "1,650 מ', עם קרחון מעל האתר.",
     "220 ק\"מ של מסלולים, 65% קלים, השיעור הגבוה ביותר במדריך. מתאים למתחילים ולמשפחות.",
     "מליון: שעתיים ועשר דקות בכביש יבש. מז'נבה: שאלו אותנו על זמן ההסעה.",
     "משפחות שומרות מצוות מגיעות לכאן בקיץ כבר עשרות שנים; הצ'אלות הכשרות שלנו נמצאות באתר, עם שף או ארוחות במשלוח."),
    ("מג'ב", "kosher-megeve", "מג'ב כשר",
     f"כ-1,050 מ', באזור הסקי {B('Évasion Mont-Blanc')}.",
     f"במסלולי מג'ב ו-{B('Saint-Gervais')} יש 185 ק\"מ, 37% קלים ו-48% בינוניים. למשפחות ולגולשים רגועים.",
     "מליון: שעתיים ועשר דקות ללא פקקים. מז'נבה: שעה ורבע בכביש.",
     "בית חב״ד בחורף; את המניין לשבוע שלכם אנחנו מארגנים עם רשת חב״ד באלפים, ומביאים ספר תורה."),
    ("אלפ ד'ואז", "kosher-alpe-dhuez", "אלפ ד'ואז כשר",
     f"כ-1,860 מ', האתר המרכזי של {B('Grand Domaine')}.",
     "250 ק\"מ של מסלולים, 52% בינוניים. מתאים למי שכבר גולש בביטחון.",
     "מליון: שעתיים ועשרים דקות, והקטע האחרון עולה ב-21 פיתולים. מגרנובל: שעה. מז'נבה: שאלו אותנו.",
     "היסטוריה ארוכה של קיץ כשר; הצוות שלנו מכסה את צד גרנובל של הרכס."),
    ("שמוני", "kosher-chamonix", "שמוני כשר",
     f"העיירה בגובה של כ-1,040 מ', למרגלות המון בלאן; אזורי הסקי מגיעים עד 2,767 מ' ב-{B('Grands Montets')}.",
     "כמה אזורי הרים גבוהים נפרדים. המקור שלנו לא מפרסם חלוקה לפי רמות לעמק.",
     "מליון: שעתיים ורבע עד שלוש שעות. מז'נבה: שעה ורבע עד שעה וחצי, נמל התעופה הקרוב ביותר.",
     "אין בעמק מלון או חנות כשרים; אנחנו דואגים לארוחות במשלוח או לשף, בחורף ובקיץ."),
    ("לה פלאן", "kosher-la-plagne", "לה פלאן כשר",
     f"11 כפרים, עד {B('Plagne Aime 2000')} בגובה של כ-2,100 מ'.",
     f"225 ק\"מ של מסלולים, כ-62% קלים, מחובר ללז ארק באזור {B('Paradiski')} (425 ק\"מ). מתאים למשפחות.",
     "מליון: שעתיים ורבע ללא פקקים. מז'נבה: שעתיים ועשרים דקות.",
     "כתבו לנו באיזה כפר תשהו, כי המשלוחים מתוכננים כפר אחר כפר."),
    ("לז ארק", "kosher-les-arcs", "לז ארק כשר",
     f"ארבעה כפרים: {B('Arc 1600, 1800, 1950, 2000')}.",
     "200 ק\"מ של מסלולים, כמחציתם קלים, מחובר ללה פלאן.",
     f"מליון: שעתיים ועשרים וחמש דקות עד שלוש שעות עד {B('Bourg-Saint-Maurice')}, ואחר כך העלייה. מז'נבה: שעתיים וחצי עד שלוש שעות.",
     "בחורף אין באתר חנות או מסעדה כשרות; שף או ארוחות במשלוח, ומניין כשיש מספיק משפחות."),
    ("ואל דיזר", "kosher-val-disere", "ואל דיזר כשר",
     f"1,850 מ', ו-300 ק\"מ של מסלולים משותפים עם {B('Tignes')}, עד 3,456 מ'.",
     "63% בינוניים ו-27% קשים. לגולשים מנוסים.",
     "מליון: שעתיים וחצי עד שלוש שעות. מז'נבה: שעתיים וארבעים דקות עד שלוש שעות וחצי.",
     "רוב האורחים לנים בצ'אלות, ולכן שף או ארוחות במשלוח מתאימים כאן. 32 הק\"מ האחרונים הם כביש הררי: תכננו הגעה ביום שישי עם מרווח גדול לפני הדלקת הנרות."),
    ("גרנובל", "kosher-grenoble", "גרנובל כשר",
     f"214 מ'. עיר ולא אתר סקי: הבסיס שלכם לאתרי הסקי של {B('Isère')}.",
     "לפי האתר שאליו נוסעים (אלפ ד'ואז במרחק שעה).",
     f"מליון: כשעה בכביש, או שעה וארבע דקות ברכבת {B('TGV')} ישירה מנמל התעופה. מז'נבה: שאלו אותנו.",
     "בית חב״ד ושני בתי כנסת בעיר; שף או ארוחות במשלוח בעיר או באתר."),
    ("אנסי", "kosher-annecy", "אנסי כשר",
     f"447 מ', על שפת האגם. בחורף המשפחות גולשות ב-{B('La Clusaz')}, במרחק 37 דקות.",
     f"ב-{B('La Clusaz')} יש 125 ק\"מ של מסלולים, 54% קלים.",
     "מליון: שעה ורבע. מז'נבה: 45 דקות.",
     f"בית כנסת קטן, ולכן את המניין לשבוע שלכם מארגנים מראש; שף או ארוחות במשלוח ליד האגם או בהרי {B('Aravis')}."),
  ],
  source=f"נתוני אזורי הסקי: {B('skiresort.info')}, נבדקו ב-30 באוקטובר 2026. גבהים וזמני נסיעה: דפי האתרים שלנו.",
  qui=("מי מארגן <i>את השבוע הכשר שלכם</i>",
       "השהייה מתומחרת ומחויבת על ידי הצוות הכשר שלנו שבסיסו באלפים. הצוות מבשל תחת רשת חב״ד באלפים, ופרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר. שומר שבת: שום דבר לא מגיע בשבת או בחג, הכול מסודר לפני הדלקת הנרות."),
  h2_faq="אתרי סקי בצרפת: <i>שאלות</i>",
  faq=[("איזה אתר סקי בצרפת מתאים למשפחה ששומרת כשרות עם ילדים קטנים?",
        "לה דז אלפ ולה פלאן הם האתרים עם שיעור המסלולים הקלים הגבוה ביותר במדריך הזה. בשניהם הצוות שלנו מביא שף או ארוחות במשלוח לצ'אלה או לדירה שלכם, והשבת מוכנה לפני הדלקת הנרות."),
       ("כמה זמן נוסעים לאתרים מליון ומז'נבה?",
        "רוב האתרים נמצאים כשעתיים מנמל התעופה של ליון ללא פקקים. מג'ב, שמוני ואנסי קרובים יותר לז'נבה, בין 45 דקות לשעה וחצי. הוסיפו זמן בסוף שבוע של חורף או בשלג."),
       ("האם יש מניין בכל אתר?",
        "המניין תלוי במספר המשפחות שנמצאות באתר באותו שבוע. בקורשבל 1850 ובמג'ב יש בית חב״ד בחורף. בשאר האתרים, מסרו לנו את התאריכים מוקדם ואנו מרכזים את המשפחות שכותבות לנו, עם ספר תורה.")],
  h2_suite="להמשך <i>קריאה</i>",
  suite=[("mountain-snow", "/he/alps/", "האלפים, כשרים לחלוטין"), ("snowflake", "/he/kosher-ski-holidays-french-alps/", "חופשות סקי כשרות באלפים"),
         ("chef-hat", "/he/kosher-services-french-alps/", "שירותים כשרים באלפים"), ("house", "/he/kosher-chalets/", "הצ'אלות הכשרות שלנו")],
)

ICO = '<img class="dk dk-ico dk-vigico dk-des" src="/img/ico/or/{}.svg" alt="" width="96" height="96" loading="lazy">'
FLECHE = '<svg class="dk dk-fleche" aria-hidden="true" focusable="false"><use href="/img/pictos.svg#arrow-right"/></svg>'

def corps(T):
    """Sections du guide, entre la bande d'intro et le formulaire #book (classes Valora des pages Alpes)."""
    st = "".join(
        f'<h3 style="margin-top:2em">{n}</h3><ul><li><b>{T["labels"][0]}</b> {a}</li><li><b>{T["labels"][1]}</b> {lv}</li>'
        f'<li><b>{T["labels"][2]}</b> {r}</li><li><b>{T["labels"][3]}</b> {k}</li></ul>'
        f'<p><a href="{"/he" if T is HE else ""}/{s}/">{ancre}</a></p>'
        for n, s, ancre, a, lv, r, k in T["stations"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in T["faq"])
    suite = "".join(f'<li>{ICO.format(i)}<a href="{u}">{t}</a>{FLECHE}</li>' for i, u, t in T["suite"])
    return (f'{MARQUE}<section class="clair clair-2 ss wrap conseils"><h2>{T["choisir"][0]}</h2><p>{T["choisir"][1]}</p></section>'
            f'<section class="clair ss wrap conseils guide-stations"><h2>{T["h2_stations"]}</h2>{st}<p class="source">{T["source"]}</p></section>'
            f'<section class="clair clair-2 ss wrap conseils"><h2>{T["qui"][0]}</h2><p>{T["qui"][1]}</p></section>'
            f'<section class="clair ss wrap faq"><h2>{T["h2_faq"]}</h2>{faq}</section>\n'), \
           f'<section class="clair ss wrap conseils"><h2>{T["h2_suite"]}</h2><ul class="dk-suite">{suite}</ul></section>'

def jsonld(T, url):
    crumbs = [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + (u or url)} for i, (n, u) in enumerate(T["crumbs"])]
    lang = "he" if T is HE else "en"
    return [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs},
            {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "publisher": {"@id": BASE + "/#organization"},
             "mainEntity": [{"@type": "Question", "name": plat(q), "acceptedAnswer": {"@type": "Answer", "text": plat(a)}} for q, a in T["faq"]]},
            {"@context": "https://schema.org", "@type": "WebPage", "@id": BASE + url, "url": BASE + url, "name": T["title"], "description": T["desc"],
             "inLanguage": lang, "dateModified": DATE, "author": {"@id": BASE + "/#organization"}, "publisher": {"@id": BASE + "/#organization"},
             "isPartOf": {"@type": "WebSite", "url": BASE + "/", "name": "Mishpacha Tours"}}]

def selecteur(lang):
    """Sélecteur réduit à EN et HE (pas de FR ni d'ES pour cette page)."""
    cour = ' aria-current="true"'
    li_en = f'<li><a href="/{SLUG}/"{cour if lang == "en" else ""}><img class="drapeau" src="/img/flags/gb.svg" alt="" width="20" height="20">English</a></li>'
    li_he = f'<li><a href="/he/{SLUG}/"{cour if lang == "he" else ""} lang="he" dir="rtl"><img class="drapeau" src="/img/flags/il.svg" alt="" width="20" height="20">עברית</a></li>'
    cur = ("EN", "English", "gb") if lang == "en" else ("HE", "עברית", "il")
    return (f'<details class="langue">\n      <summary aria-label="{cur[0]}, language: {cur[1]}"><img class="drapeau" src="/img/flags/{cur[2]}.svg" alt="" width="20" height="20"><span class="code">{cur[0]}</span></summary>\n'
            f'      <ul>\n        {li_en}\n        {li_he}\n      </ul>\n    </details>')

def guide(lang):
    T = EN if lang == "en" else HE
    pre = "" if lang == "en" else "he/"
    url = f"/{pre}{SLUG}/"
    src = f"{pre}kosher-ski-holidays-french-alps/index.html"
    s = rd(src).replace("\r\n", "\n")
    # en-tête
    s = meta(s, T["title"], T["desc"])
    s = s.replace(f"{BASE}/{pre}kosher-ski-holidays-french-alps/", BASE + url)   # canonical, og:url
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', "", s)
    alt = (f'<link rel="alternate" hreflang="en" href="{BASE}/{SLUG}/">\n<link rel="alternate" hreflang="x-default" href="{BASE}/{SLUG}/">\n'
           f'<link rel="alternate" hreflang="he" href="{BASE}/he/{SLUG}/">\n')
    assert s.count('<link rel="stylesheet" href="/valora.css">') == 1, src
    s = s.replace('<link rel="stylesheet" href="/valora.css">', alt + '<link rel="stylesheet" href="/valora.css">', 1)
    m = LD.search(s); s = s[:m.start(2)] + json.dumps(jsonld(T, url), ensure_ascii=False) + s[m.end(2):]
    s = re.sub(r'<details class="langue">.*?</details>', lambda _: selecteur(lang), s, count=1, flags=re.S)
    # <main> : héros, bande d'intro, corps, formulaire #book, à lire aussi
    a, b = s.index("<main>"), s.index("</main>")
    main = s[a:b]
    fil = " / ".join(f'<a href="{u}">{n}</a>' if u else n for n, u in T["crumbs"])
    main = re.sub(r'<p class="fil lead-fil">.*?</p>', lambda _: f'<p class="fil lead-fil">{fil}</p>', main, count=1, flags=re.S)
    main = re.sub(r"<h1>.*?</h1>(\s*)<p>.*?</p>", lambda mm: f'<h1>{T["h1"]}<br><i>{T["ital"]}</i></h1>{mm.group(1)}<p>{T["intro"][0]}</p>', main, count=1, flags=re.S)
    main = re.sub(r"(<!--/MANIFESTE-->)<p>.*?</p>(</div></section>)", lambda mm: f"{mm.group(1)}<p>{T['intro'][1]}</p>{mm.group(2)}", main, count=1, flags=re.S)
    i = main.index("</section>", main.index("lead-intro")) + len("</section>")
    j = main.index('<section class="ss lead-final"')
    k = main.index("</section>", j) + len("</section>")
    c, suite = corps(T)
    main = main[:i] + c + main[j:k] + suite + "\n\n\n"
    s = s[:a] + main + s[b:]
    ecrire(f"{pre}{SLUG}/index.html", s)

# =====================================================================================================================
# 2. Val Thorens et Courchevel
# =====================================================================================================================
STATIONS = {
 ("en", "kosher-val-thorens"): dict(
   title="Kosher Val Thorens: Ski Holiday, Chef",
   desc="Kosher Val Thorens ski holiday at 2,300 m, the highest resort in Europe: a private chef or delivered meals, Shabbat and a minyan. One written quote.",
   h1=("Val Thorens, strictly kosher<br><i>at 2,300 m, the highest resort in Europe</i>", "Kosher Val Thorens<br><i>a kosher ski holiday at 2,300 m, the highest resort in Europe</i>"),
   fil=("Val Thorens, strictly kosher</p>", "Kosher Val Thorens</p>"), crumb="Kosher Val Thorens",
   p1=("Val Thorens sits at 2,300 m in Les 3 Vallées, the highest ski resort in Europe.",
       "Kosher Val Thorens, for the whole week: the resort sits at 2,300 m in Les 3 Vallées, the highest ski resort in Europe, and our kosher team based in the Alps cooks for you on site."),
   p2=("Its season runs from 21 November 2026 to 2 May 2027. We organise your kosher stay: private chef or delivered meals, Shabbat, minyan and Sefer Torah, in one written quote.",
       "The Val Thorens season runs from 21 November 2026 to 2 May 2027. For a kosher stay in Val Thorens, we arrange a private chef in your chalet or meals delivered to your apartment, Shabbat ready before candle lighting, and a minyan with a Sefer Torah when enough families are there that week. One written quote."),
   kit="<!--KIT-WP:vth-->",
   bloc=("What your Val Thorens quote <i>can include</i>", [
     "A private chef in your chalet or apartment, the kitchen made kosher by our team.",
     "Hot kosher meals delivered to your apartment or hotel, for the week, with notice.",
     "Shabbat meals, challot and wine on Friday, before candle lighting.",
     "Hanukkah, Purim or Pesach on the mountain, on request.",
     "A minyan with a Sefer Torah, depending on how many families are in the resort that week.",
     "Transfers from Lyon, on quote."], "Stays, transfers and meals are organised and invoiced by our kosher team based in the Alps.")),
 ("he", "kosher-val-thorens"): dict(
   title=None,   # title HE inchangé (livrable 4.1 : déjà « ואל טורנס כשר » en tête)
   desc="ואל טורנס כשר: חופשת סקי כשרה בגובה 2,300 מ', באתר הגבוה באירופה. שף פרטי בצ'אלה או ארוחות במשלוח, שבת ומניין, בהצעת מחיר אחת בכתב.",
   h1=("ואל טורנס, כשר לחלוטין<br><i>בגובה 2,300 מ', האתר הגבוה באירופה</i>", "ואל טורנס כשר<br><i>חופשת סקי כשרה בגובה 2,300 מ', באתר הגבוה באירופה</i>"),
   fil=("ואל טורנס, כשר לחלוטין</p>", "ואל טורנס כשר</p>"), crumb="ואל טורנס כשר",
   p1=("ואל טורנס שוכנת בגובה 2,300 מ' בשלושת העמקים, אתר הסקי הגבוה באירופה.",
       "ואל טורנס כשר, לכל השבוע: האתר שוכן בגובה 2,300 מ' בשלושת העמקים, אתר הסקי הגבוה באירופה, והצוות הכשר שלנו שבסיסו באלפים מבשל בשבילכם במקום."),
   p2=("העונה נמשכת מ-21 בנובמבר 2026 עד 2 במאי 2027. אנחנו מארגנים לכם שהות כשרה: שף פרטי או ארוחות עד הדירה, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
       "העונה בוואל טורנס נמשכת מ-21 בנובמבר 2026 עד 2 במאי 2027. לחופשה כשרה בוואל טורנס אנחנו מסדרים שף פרטי בצ'אלה או ארוחות במשלוח לדירה, שבת מוכנה לפני הדלקת הנרות, ומניין עם ספר תורה כשיש מספיק משפחות באותו שבוע. הצעת מחיר אחת בכתב."),
   kit="<!--KIT-WP:vth-->",
   bloc=("מה אפשר לכלול <i>בהצעת המחיר לוואל טורנס</i>", [
     "שף פרטי בצ'אלה או בדירה, והצוות שלנו מכשיר את המטבח.",
     "ארוחות חמות כשרות במשלוח לדירה או למלון, לאורך השבוע, בהתראה מראש.",
     "סעודות שבת, חלות ויין ביום שישי, לפני הדלקת הנרות.",
     "חנוכה, פורים או פסח בהרים, לפי בקשה.",
     "מניין עם ספר תורה, לפי מספר המשפחות באתר באותו שבוע.",
     "הסעות מליון, בהצעת מחיר."], "השהייה מתומחרת ומחויבת על ידי הצוות הכשר שלנו שבסיסו באלפים.")),
 ("en", "kosher-courchevel"): dict(
   title="Kosher Courchevel: Ski Holiday, Chef",
   desc="Kosher Courchevel ski holiday in Courchevel 1850 and its villages: a private chef or delivered meals, Shabbat, holidays and a minyan. One written quote.",
   h1=("Courchevel, strictly kosher<br><i>Courchevel 1850 and its villages, in Les 3 Vallées</i>", "Kosher Courchevel<br><i>a kosher ski holiday in Courchevel 1850 and its villages, in Les 3 Vallées</i>"),
   fil=("Courchevel, strictly kosher</p>", "Kosher Courchevel</p>"), crumb="Kosher Courchevel",
   p1=("Courchevel 1850 sits at about 1,850 m in Les 3 Vallées.",
       "Kosher Courchevel, for the whole week: Courchevel 1850 sits at about 1,850 m in Les 3 Vallées, and its Chabad house runs in winter; we coordinate with it for your minyan and your Shabbat."),
   p2=("The season runs from 4 December 2026 to 18 April 2027. We organise your kosher stay: private chef or delivered meals, Shabbat, minyan and Sefer Torah, in one written quote.",
       "The Courchevel season runs from 4 December 2026 to 18 April 2027. For a kosher stay in Courchevel, we arrange a private chef in your chalet or meals delivered to your apartment or hotel, in Courchevel 1850 and the villages, Shabbat ready before candle lighting, and a minyan with a Sefer Torah. One written quote."),
   kit="<!--KIT-WP:co-->",
   bloc=("What your Courchevel quote <i>can include</i>", [
     "A private chef in your chalet or apartment, the kitchen made kosher by our team.",
     "Hot kosher meals delivered in Courchevel 1850 and the villages, for the week, with notice.",
     "Shabbat meals, challot and wine on Friday, before candle lighting.",
     "Hanukkah, Purim or Pesach, on request.",
     "A minyan with a Sefer Torah for your dates, when the families present call for it.",
     "Transfers from Lyon, on quote."], "Stays, transfers and meals are organised and invoiced by our kosher team based in the Alps.")),
 ("he", "kosher-courchevel"): dict(
   title=None,   # title HE inchangé (livrable 5.1)
   desc="קורשבל כשר: חופשת סקי כשרה בקורשבל 1850 ובכפרים, בשלושת העמקים. שף פרטי בצ'אלה או ארוחות במשלוח, שבת, חגים ומניין, בהצעת מחיר אחת.",
   h1=("קורשבל, כשר לחלוטין<br><i>קורשבל 1850 וכפריה, בשלושת העמקים</i>", "קורשבל כשר<br><i>חופשת סקי כשרה בקורשבל 1850 ובכפריה, בשלושת העמקים</i>"),
   fil=("קורשבל, כשר לחלוטין</p>", "קורשבל כשר</p>"), crumb="קורשבל כשר",
   p1=("קורשבל 1850 שוכנת בגובה של כ-1,850 מ' בשלושת העמקים.",
       "קורשבל כשר, לכל השבוע: קורשבל 1850 שוכנת בגובה של כ-1,850 מ' בשלושת העמקים, ובחורף פועל בה בית חב״ד, שאיתו אנו מתאמים את המניין ואת השבת שלכם."),
   p2=("העונה נמשכת מ-4 בדצמבר 2026 עד 18 באפריל 2027. אנחנו מארגנים לכם שהות כשרה: שף פרטי או ארוחות עד הדירה, שבת, מניין וספר תורה, בהצעת מחיר אחת בכתב.",
       "העונה בקורשבל נמשכת מ-4 בדצמבר 2026 עד 18 באפריל 2027. לחופשה כשרה בקורשבל אנחנו מסדרים שף פרטי בצ'אלה או ארוחות במשלוח לדירה או למלון, בקורשבל 1850 ובכפרים, שבת מוכנה לפני הדלקת הנרות, ומניין עם ספר תורה. הצעת מחיר אחת בכתב."),
   kit="<!--KIT-WP:co-->",
   bloc=("מה אפשר לכלול <i>בהצעת המחיר לקורשבל</i>", [
     "שף פרטי בצ'אלה או בדירה, והצוות שלנו מכשיר את המטבח.",
     "ארוחות חמות כשרות במשלוח בקורשבל 1850 ובכפרים, לאורך השבוע, בהתראה מראש.",
     "סעודות שבת, חלות ויין ביום שישי, לפני הדלקת הנרות.",
     "חנוכה, פורים או פסח, לפי בקשה.",
     "מניין עם ספר תורה לתאריכים שלכם, כשהמשפחות שנמצאות באתר מבקשות.",
     "הסעות מליון, בהצעת מחיר."], "השהייה מתומחרת ומחויבת על ידי הצוות הכשר שלנו שבסיסו באלפים."),
   extra=[("<b>שפים פרטיים.</b> ההשגחה אינה מצוינת בדפים שלהן.",
           "<b>שפים פרטיים.</b> סוכנויות מפרסמות שפים פרטיים \"גלאט כשר\" בקורשבל. ההשגחה אינה מצוינת בדפים שלהן.")]),
}

def station(lang, slug, C):
    p = ("he/" if lang == "he" else "") + f"{slug}/index.html"
    s = rd(p).replace("\r\n", "\n")
    title = C["title"] or html.unescape(re.search(r"<title>(.*?) \| Mishpacha Tours</title>", s).group(1))
    s = meta(s, title, C["desc"])
    s = remplace(s, C["h1"][0], C["h1"][1], p)
    s = remplace(s, C["fil"][0], C["fil"][1], p)
    s = remplace(s, f"<p>{C['p1'][0]}</p>", f"<p>{C['p1'][1]}</p>", p)
    s = remplace(s, f"<p>{C['p2'][0]}</p>", f"<p>{C['p2'][1]}</p>", p)
    for old, new in C.get("extra", []): s = remplace(s, old, new, p)
    if MARQUE not in s:
        h2, items, role = C["bloc"]
        bloc = (f'{MARQUE}<section class="clair clair-2 ss wrap conseils"><h2>{h2}</h2><ul>' + "".join(f"<li>{x}</li>" for x in items)
                + f"</ul><p>{role}</p></section>")
        assert s.count("</section>" + C["kit"]) == 1, (p, C["kit"])
        s = s.replace("</section>" + C["kit"], "</section>" + bloc + C["kit"], 1)
    fil = re.search(r'<p class="fil lead-fil">(.*?)</p>', s, re.S).group(1).split(" / ")
    def fn(liste):
        for b in liste:
            t = b.get("@type")
            if t == "WebPage":
                b["name"], b["description"], b["dateModified"] = title, C["desc"], DATE
            if t == "BreadcrumbList" and len(b["itemListElement"]) == len(fil):
                for it, n in zip(b["itemListElement"], fil): it["name"] = plat(n)
    s = ld(s, fn)
    ecrire(p, s)

def sources_en():
    """Sources EN des générateurs (_pages) : mêmes textes que les pages, pour qu'une régénération les garde."""
    for slug in ("kosher-val-thorens", "kosher-courchevel"):
        C = STATIONS[("en", slug)]; p = f"_pages/{slug}.py"; s = rd(p); crlf = "\r\n" in s; s = s.replace("\r\n", "\n")
        old_t = re.search(r'  title="([^"]*)",', s).group(1); s = s.replace(f'  title="{old_t}",', f'  title="{C["title"]}",', 1)
        old_d = re.search(r'  desc="([^"]*)",', s).group(1); s = s.replace(f'  desc="{old_d}",', f'  desc="{C["desc"]}",', 1)
        h1, ital = C["h1"][1].split("<br><i>"); ital = ital[:-4]
        s = re.sub(r'  h1="[^"]*", ital="[^"]*",', lambda _: f'  h1="{h1}", ital="{ital}",', s, count=1)
        s = re.sub(r'  intro="[^"]*",', lambda _: f'  intro="{C["p1"][1]} {C["p2"][1]}",', s, count=1)
        if MARQUE not in s:
            h2, items, role = C["bloc"]
            sec = (f'    dict(type="text", h2="{h2}", html="""{MARQUE}<ul>\n' + "".join(f"<li>{x}</li>\n" for x in items) + f'</ul>\n<p>{role}</p>"""),\n')
            s = s.replace("  sections=[\n", "  sections=[\n" + sec, 1)
        if crlf: s = s.replace("\n", "\r\n")
        ecrire(p, s)
    # intro HE (source de _intros_courtes.py)
    p = "_intros_courtes_trad.json"; d = json.loads(rd(p))
    for slug in ("kosher-val-thorens", "kosher-courchevel"):
        C = STATIONS[("he", slug)]; d["he"][slug] = f"{C['p1'][1]} {C['p2'][1]}"
    o = rd(p); n = json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if o.endswith("\n") else "")
    if json.loads(o) != d: ecrire(p, n)
    else: print("ok   ", p)

# =====================================================================================================================
# 4. Liens entrants sur /alps/ et /he/alps/
# =====================================================================================================================
ALPS = {
 "alps/index.html": [
   ("plus Val Thorens and Les Menuires in the Belleville valley: meals, chalets, Shabbat, holidays, minyan and Sefer Torah.</li>",
    "plus Val Thorens and Les Menuires in the Belleville valley: meals, chalets, Shabbat, holidays, minyan and Sefer Torah. Details: <a href=\"/kosher-val-thorens/\">kosher ski holiday in Val Thorens</a>. Compare them all: <a href=\"/french-ski-resorts-kosher-guide/\">French ski resorts, a kosher guide</a>.</li>"),
   ("Courchevel 1850 and Megève have a Chabad house in winter: we coordinate with it for your minyan and your Shabbat.</li>",
    "Courchevel 1850 and Megève have a Chabad house in winter: we coordinate with it for your minyan and your Shabbat. Details: <a href=\"/kosher-courchevel/\">kosher Courchevel</a>.</li>")],
 "he/alps/index.html": [
   ("וכן ואל טורנס ולה מנואיר בעמק בלוויל: ארוחות, צ'אלות, שבת, חגים, מניין וספר תורה.</li>",
    "וכן ואל טורנס ולה מנואיר בעמק בלוויל: ארוחות, צ'אלות, שבת, חגים, מניין וספר תורה. פרטים: <a href=\"/he/kosher-val-thorens/\">חופשה כשרה בוואל טורנס</a>. להשוואה בין כולם: <a href=\"/he/french-ski-resorts-kosher-guide/\">אתרי סקי בצרפת, מדריך כשר</a>.</li>"),
   ("בקורשבל 1850 ובמג'ב יש בית חב״ד בחורף: אנו מתאמים איתו את המניין ואת השבת שלכם.</li>",
    "בקורשבל 1850 ובמג'ב יש בית חב״ד בחורף: אנו מתאמים איתו את המניין ואת השבת שלכם. פרטים: <a href=\"/he/kosher-courchevel/\">קורשבל כשר</a>.</li>")],
}
def alps():
    for p, reps in ALPS.items():
        s = rd(p).replace("\r\n", "\n")
        for old, new in reps: s = remplace(s, old, new, p)
        ecrire(p, s)
    # source EN /alps/ : liens relatifs comme le reste du module
    p = "_pages/alps.py"; s = rd(p); crlf = "\r\n" in s; s = s.replace("\r\n", "\n")
    for old, new in ALPS["alps/index.html"]:
        new = new.replace('href="/kosher-val-thorens/"', 'href="../kosher-val-thorens/"').replace('href="/french-ski-resorts-kosher-guide/"', 'href="../french-ski-resorts-kosher-guide/"').replace('href="/kosher-courchevel/"', 'href="../kosher-courchevel/"')
        s = remplace(s, old, new, p)
    if crlf: s = s.replace("\n", "\r\n")
    ecrire(p, s)

# =====================================================================================================================
# 5. index.md des pages touchées (même moteur que la section 3 de _agentic.py)
# =====================================================================================================================
def markdown(d):
    from markdownify import markdownify as md
    p = d + "/index.html"; h = rd(p)
    main = re.search(r"<main.*?</main>", h, re.S).group(0)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", main, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    desc = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    url = BASE + "/" + d + "/"
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {desc}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    ecrire(d + "/index.md", out)

TOUCHEES = [SLUG, "he/" + SLUG, "kosher-val-thorens", "he/kosher-val-thorens", "kosher-courchevel", "he/kosher-courchevel", "alps", "he/alps"]

if __name__ == "__main__":
    guide("en"); guide("he")
    for (lang, slug), C in STATIONS.items(): station(lang, slug, C)
    sources_en()
    alps()
    for d in TOUCHEES: markdown(d)
