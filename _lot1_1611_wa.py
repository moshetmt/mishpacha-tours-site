# -*- coding: utf-8 -*-
"""Lot 1 du 16/11/2026 (plan : clients/mishpacha-tours/06-reports/2026-11-16-etude-site-plan-reparation.md, lot 1 ligne 10 et lot 3).

A. Message WhatsApp par page. Réécrit le paramètre text= de TOUS les liens https://wa.me/33652092301 (HTML, index.md, gabarit
   JavaScript du « chercheur », replis des formulaires) : le message nomme le site, la page lue (nom tiré du title) et le sujet,
   dans la langue de la page. Les liens vers 33781823193 (Beth Habad de Grenoble) et le numéro ne changent jamais.
   Règle : un lien dont le sujet est plus précis que la page (data-offre, tours de /jewish-lyon-tours/, message propre de la page)
   garde son sujet et reçoit la mention de la page ; un lien générique, nu, dans une autre langue ou sur un autre sujet
   (Lyon sur une page Alpes et l'inverse) prend le message de la page ou le gabarit du type.
B. Ligne « visite privée dès 290 € » (lien WhatsApp, data-offre="prix-290") juste sous le h1 des pages patrimoine de Lyon.
   CSS dans un seul bloc en fin de lv.css.

Les liens sont repérés par leur href (jamais par les classes du parent) : le script se rejoue après tout script qui réécrit
l'en-tête et le panneau de menu. Idempotent : une 2e passe ne change rien.

    python -X utf8 _lot1_1611_wa.py [--dry]   (depuis site-v5/)"""
import io, os, re, sys, glob, html, collections
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
PH, BH = "33652092301", "33781823193"
WA = "https://wa.me/" + PH
DRY = "--dry" in sys.argv
PRIVEES = {"espace", "maquette-chalet-lv"}          # outils privés, hors périmètre
MAXLEN = 220

# ---------------------------------------------------------------- gabarits (table type -> message, par langue, une seule fois)
HELLO = {"en": "Hello Mishpacha Tours,", "fr": "Bonjour Mishpacha Tours,", "es": "Hola Mishpacha Tours,", "he": "שלום Mishpacha Tours,"}
ORIGIN = {"en": "I am reading “{p}”.", "fr": "je lis « {p} ».", "es": "leo «{p}».", "he": 'קראתי את העמוד "{p}".'}
ORIGIN_ANCIEN = {"he": 'פנייה מהעמוד "{p}".'}
# gabarits de repli par type (reprise des formulations déjà en ligne ; seuls « chalet » et la langue de visite en hébreu sont neufs)
GABARIT = {
    "general": {"en": "I would like to ask about your services. Dates: / Number of people:",
                "fr": "je voudrais des informations sur vos services. Dates : / Nombre de personnes :",
                "es": "quisiera información sobre sus servicios. Fechas: / Número de personas:",
                "he": "אשמח לקבל מידע על השירותים שלכם. תאריכים: / מספר אנשים:"},
    "lyon": {"en": "I would like to ask about a private Jewish tour of Lyon. Dates: / Number of people: / Preferred language:",
             "fr": "je souhaite me renseigner sur une visite juive privée de Lyon. Dates : / Nombre de personnes : / Langue souhaitée :",
             "es": "quisiera información sobre una visita judía privada en Lyon. Fechas: / Número de personas: / Idioma preferido:",
             "he": "אשמח לברר על סיור יהודי פרטי בליון. תאריכים: / מספר משתתפים: / שפה מועדפת:"},
    "alps": {"en": "We are going to the Alps. Resort: / Dates: / Number of people: / We need (chef, delivered meals, Shabbat, holiday, minyan):",
             "fr": "nous allons dans les Alpes. Station : / Dates : / Nombre de personnes : / Besoins (chef, repas livrés, Shabbat, fête, minyan) :",
             "es": "vamos a los Alpes. Estación: / Fechas: / Número de personas: / Necesitamos (chef, comidas entregadas, Shabat, fiesta, minyan):",
             "he": "נרצה שירותים כשרים באלפים. אתר סקי: / תאריכים: / מספר משתתפים: / שירותים (צ'אלה עם שף, ארוחות במשלוח, שבת, חג, מניין):"},
    "chalet": {"en": "We would like this kosher chalet. Dates: / Number of guests:",
               "fr": "nous souhaitons ce chalet casher. Dates : / Nombre de personnes :",
               "es": "quisiéramos este chalé kosher. Fechas: / Número de personas:",
               "he": "אנחנו מעוניינים בצ'אלה הכשרה. תאריכים: / מספר אורחים:"},
}
GAB_TYPE = {"home": "general", "general": "general", "mixed": "general", "lyon": "lyon", "tour": "lyon", "alps": "alps",
            "station": "alps", "hub_chalets": "alps", "villa": "alps", "chalet": "chalet"}
HE_LANG = "שפת הסיור (אנגלית, צרפתית או ספרדית): אנגלית"
HE_FIX = (("מז'ב", "מג'ב"), ("צ'אלט", "צ'אלה"))
# gabarit du « chercheur » de réservation (JavaScript, 5 pages en service, présent en code mort sur les autres)
CHERCHEUR = {
    "en": "I would like to check availability for the ${f.tour.value} tour. Dates: ${f.dates.value||'/'} / Number of people: ${f.personnes.value||'/'} / Preferred language:",
    "fr": "je souhaite vérifier les disponibilités pour la visite ${f.tour.value}. Dates : ${f.dates.value||'/'} / Nombre de personnes : ${f.personnes.value||'/'} / Langue souhaitée :",
    "es": "quisiera consultar la disponibilidad de la visita ${f.tour.value}. Fechas: ${f.dates.value||'/'} / Número de personas: ${f.personnes.value||'/'} / Idioma preferido:",
    "he": "אשמח לבדוק זמינות לסיור ${f.tour.value}. תאריכים: ${f.dates.value||'/'} / מספר משתתפים: ${f.personnes.value||'/'} / שפה מועדפת:",
}
# noms des 5 tours (reprise des noms déjà employés dans les messages et les formulaires du site)
TOURS = {
    "tours/jewish-lyon": {"en": "Jewish Lyon tour", "fr": "Visite du Lyon juif", "es": "Visita del Lyon judío", "he": "סיור ליון היהודית"},
    "tours/memory-chrd": {"en": "Memory tour, CHRD", "fr": "Visite Mémoire, CHRD", "es": "Visita Memoria, CHRD", "he": "סיור הזיכרון, CHRD"},
    "tours/memory-montluc-neveh-shalom": {"en": "Memory tour, Montluc and Neveh Shalom", "fr": "Visite Mémoire, Montluc et Neveh Shalom",
                                          "es": "Visita Memoria, Montluc y Neveh Shalom", "he": "סיור הזיכרון, מונלוק ונווה שלום"},
    "tours/stopover": {"en": "Stopover tour", "fr": "Visite Escale à Lyon", "es": "Visita Escala", "he": "סיור עצירת הביניים"},
    "tours/izieu": {"en": "Izieu day trip", "fr": "Excursion à Izieu", "es": "Excursión a Izieu", "he": "טיול יום לאיזיה"},
}

# ---------------------------------------------------------------- types de page (par slug EN, une seule fois)
STATIONS = {"kosher-alpe-dhuez", "kosher-annecy", "kosher-avoriaz", "kosher-cervinia", "kosher-chamonix", "kosher-cortina",
            "kosher-courchevel", "kosher-courmayeur", "kosher-crans-montana", "kosher-davos", "kosher-grenoble", "kosher-gstaad",
            "kosher-la-plagne", "kosher-les-arcs", "kosher-les-deux-alpes", "kosher-les-menuires", "kosher-megeve", "kosher-st-moritz",
            "kosher-val-disere", "kosher-val-thorens", "kosher-verbier", "kosher-zermatt", "kosher-ski-anywhere"}
LYON = {"chrd-lyon", "grande-synagogue-lyon", "jewish-cemetery-lyon", "jewish-history-lyon", "maison-izieu", "montluc-prison-lyon",
        "mikveh-lyon", "rue-juiverie-lyon", "synagogues-lyon", "jewish-lyon-guide", "jewish-lyon-itinerary-2-days",
        "jewish-travel-lyon-faq", "is-lyon-safe-for-jewish-visitors", "shabbat-in-lyon", "chabad-lyon",
        "kosher-shabbat-meals-catering-lyon", "kosher-restaurants-lyon", "things-to-do-in-lyon",
        "where-to-stay-lyon-jewish-travellers", "lyon-weather"}
MIXED = {"jewish-life-around-lyon", "lyon-gateway-to-the-alps-kosher", "flights-to-lyon", "summer-in-the-alps-jewish-families",
         "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps"}
ALPS = {"alps", "activities-alps-kosher-families", "kosher-meals-delivered-alps", "kosher-pesach-french-alps",
        "kosher-services-french-alps", "kosher-van-transfers", "minyan-sefer-torah-alps", "private-kosher-chef-alps",
        "private-kosher-chalet-alps", "shabbat-holiday-meals-alps", "spa-massage-alps"}
GENERAL = {"about", "contact", "contact-quick", "contact-quick/thanks", "credits", "legal", "privacy", "terms", "merci",
           "plan-your-trip"}
PAGE_DOM = {"lyon": "lyon", "tour": "lyon", "alps": "alps", "station": "alps", "hub_chalets": "alps", "villa": "alps",
            "chalet": "alps", "home": "both", "general": "both", "mixed": "both"}

def type_page(slug):
    if slug == "": return "home"
    if slug.startswith("tours/") or slug == "jewish-lyon-tours": return "tour"
    if slug == "kosher-chalets": return "hub_chalets"
    if slug == "kosher-villa-saint-tropez": return "villa"
    if re.match(r"kosher-(?:family-|luxury-pool-|pool-|slope-)?chalet-", slug): return "chalet"
    if slug in STATIONS: return "station"
    if slug in LYON: return "lyon"
    if slug in MIXED: return "mixed"
    if slug in ALPS: return "alps"
    if slug in GENERAL: return "general"
    return None

# ---------------------------------------------------------------- utilitaires
def lire(p): return io.open(p, encoding="utf-8", newline="").read()
def ecrire(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

def lang_slug(rel):
    p = rel.split("/")[:-1]
    l = p[0] if p and p[0] in ("fr", "es", "he") else "en"
    return l, "/".join(p[1:] if l != "en" else p)

def decode(v): return None if v is None else unquote(v)
def encode(t): return quote(t, safe="")

GREET_RE = re.compile(r"^(?:Hello|Bonjour|Hola|Buenos días|שלום)(?:\s+Mishpacha Tours)?\s*,\s*")
def _origin_re(l):
    alts = []
    for o in (ORIGIN[l], ORIGIN_ANCIEN.get(l)):
        if o:
            pre, post = o.split("{p}")
            alts.append(re.escape(pre) + r".*?" + re.escape(post))
    return re.compile(re.escape(HELLO[l]) + r"\s+(?:" + "|".join(alts) + r")\s*", re.S)
ORIGIN_RE = {l: _origin_re(l) for l in HELLO}

def sans_origine(t, l):
    return ORIGIN_RE[l].sub("", t, count=1) if ORIGIN_RE[l].match(t) else t
def reste(t, l):
    """texte sans la mention de page ni la salutation"""
    return GREET_RE.sub("", sans_origine(t, l), count=1).strip()

def cap(t): return t[:1].upper() + t[1:] if t[:1].isalpha() else t
HE_TEXTE = (   # remplacements exacts (relecture du 17/11/2026, rapport 2026-11-17-relecture-hebreu-lot1.md)
    ("תחנה:", "אתר סקי:"),                                                      # F1
    ("את הסיור ליון היהודית", "את סיור ליון היהודית"),                           # F2
    ("האלפים כשר לחלוטין", "האלפים כשרים לחלוטין"),                              # F4
    ("אני מבקש הצעת מחיר", "אשמח לקבל הצעת מחיר"),                               # M6
    ("אני מתכנן נסיעה לליון ויש לי כמה שאלות", "אנחנו מתכננים נסיעה לליון ויש לנו כמה שאלות"),
    ("אני מחפש מקווה בליון", "אשמח למצוא מקווה בליון"),
    ("אני מעוניין במניין ובספר תורה באלפים", "נשמח למניין ולספר תורה באלפים"),
    ("אני מעוניין בארוחות שבת באלפים", "נשמח לארוחות שבת באלפים"),
    ("אני מתכנן/ת נסיעה לליון ומעוניין/ת בסיור פרטי איתכם", "אנחנו מתכננים נסיעה לליון ונשמח לסיור פרטי איתכם"),
    ("סיור הזיכרון, הזמנה ל-CHRD", "סיור הזיכרון, כולל הזמנת הכניסה ל-CHRD"),    # M8
    ("סיור הזיכרון, הזמנה למונלוק ולנווה שלום", "סיור הזיכרון במונלוק ובנווה שלום"),
    ("וגילאים)", "וגילים)"),                                                     # M11
    ("לואל טורנס", "לוואל טורנס"),                                               # M13
    ("בוילרבאן", "בווילרבאן"),
)
HE_REGEX = (
    (r"בצ'אלה כשר(?![א-ת])", "בצ'אלה כשרה"),                                    # F3
    (r"אנו מעוניינים ב\(([^)]*)\):", r"נשמח ל: \1"),                          # M14
    (r"(?<![א-ת])אתר:", "אתר סקי:"),                                             # M3
    (r"ארוחות כשרות באתר(?! הסקי)", "ארוחות כשרות באתר הסקי"),
)
def corriger(t, l):
    if l == "he":
        for a, b in HE_FIX + HE_TEXTE: t = t.replace(a, b)
        for a, b in HE_REGEX: t = re.sub(a, b, t)
        if "יש לי שאלה על Mishpacha Tours" in t:                                  # M9 : pas de ligne de langue sans visite
            t = re.sub(r"\s*/\s*(?:שפה מועדפת:|שפת הסיור[^:]*: אנגלית)\s*$", "", t)
        t = re.sub(r"שפה(?: מועדפת)?:\s*$", HE_LANG, t)
    return t

# pages hébreu : titres et sous-titre de menu (F3, F4, F5, M16), repérés par le texte seul
HE_PAGE = (("צ'אלות פרטיות, כשרות למהדרין", "צ'אלות פרטיות כשרות"),              # F5
           ("10 חדרי טווין", "10 חדרים עם מיטות נפרדות"), ("מגלשיים בדלת", "סקי מהדלת"),   # M16
           ("ארוחות משלוח, מניין", "ארוחות במשלוח, מניין"),
           ("בוילרבאן", "בווילרבאן"), ("לואל טורנס", "לוואל טורנס"))               # M13
def hebreu_page(t, slug):
    for a, b in HE_PAGE: t = t.replace(a, b)
    if slug == "spa-massage-alps": t = re.sub(r"(בצ(?:'|&#39;|&#x27;|’)אלה כשר)(?![א-ת])", r"\1ה", t)
    if slug == "alps": t = t.replace("האלפים כשר לחלוטין", "האלפים כשרים לחלוטין")
    return t

# message nommant la station, l'escale ou la villa (M4, M5, M10) : pages hébreu dont le message restait général
STATIONS_SANS_NOM = {"kosher-" + x for x in "annecy avoriaz cervinia chamonix cortina courmayeur crans-montana grenoble la-plagne les-arcs st-moritz val-disere verbier zermatt".split()}
def message_he(slug, nom):
    if slug in STATIONS_SANS_NOM:
        st = re.sub(r"\s*כשר$", "", nom)
        besoins = "שף, שבת, חג, מניין" if slug == "kosher-verbier" else "שף, ארוחות במשלוח, שבת, חג, מניין"
        return "אנחנו נוסעים ל%s%s. תאריכים: / מספר משתתפים: / אנחנו צריכים (%s):" % ("ו" if st.startswith("ו") else "", st, besoins)
    if slug in ("lyon-gateway-to-the-alps-kosher", "kosher-ski-holidays-french-alps"):
        return "אנחנו נוחתים בליון בדרך לאלפים ורוצים את סיור עצירת הביניים. שעת הגעה: / שעת המשך הנסיעה: / אתר סקי: / מספר משתתפים:"
    if slug == "kosher-villa-saint-tropez":
        return "אנחנו מעוניינים בווילה הכשרה בסן טרופה. תאריכים: / מספר אורחים:"
    return None
def composer(l, nom, r):
    return f"{HELLO[l]} {ORIGIN[l].format(p=nom)} {cap(corriger(r, l)).strip()}"

# langue d'un texte (hébreu par l'alphabet, FR/ES/EN par mots-outils) ; None = signal insuffisant
_W = {
 "en": set("hello would like we the number people tour planning going about for our and your services need language preferred question guests private am to of in on you i".split()),
 "fr": set("bonjour je nous souhaite souhaitons voudrais pour une les des du visite séjour nombre personnes langue vos sur dans besoins station avec casher mon notre suis".split()),
 "es": set("hola buenos días quisiera quisiéramos quiero queremos para una los las visita estancia número personas idioma fechas sus sobre estación necesitamos con mi nuestro el".split()),
}
def lang_of(t):
    he = len(re.findall(r"[֐-׿]", t)); lat = len(re.findall(r"[A-Za-z]", t))
    if he >= 6 and he * 3 >= lat: return "he"
    if he >= 6: return "he"
    toks = re.findall(r"[a-zA-Zéèêàùçñíóúáü]+", t.lower())
    sc = {l: sum(1 for w in toks if w in ws) for l, ws in _W.items()}
    best = sorted(sc.items(), key=lambda kv: -kv[1])
    if best[0][1] < 2 or best[0][1] == best[1][1]: return None
    return best[0][0]

def dom_texte(t):
    L = bool(re.search(r"Lyon|ליון", t)); A = bool(re.search(r"Alp|אלפ", t))
    return "both" if L and A else "lyon" if L else "alps" if A else "neutral"

def nom_page(s, l, slug):
    if slug in TOURS: return TOURS[slug][l]
    if slug == "jewish-lyon-guide" and l == "he":                      # M12 : le H1 plutôt que le mot-clé du title
        mh = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if mh: return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", mh.group(1))).strip().replace(" ,", ",")
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    t = html.unescape(m.group(1)).strip() if m else ""
    parts = [p.strip() for p in re.split(r"\s+\|\s+", t)]
    parts = [p for p in parts if not p.lower().startswith("mishpacha tours")] or parts
    t = re.split(r"\s+·\s+", parts[0])[0]
    t = re.sub(r",\s*Mishpacha Tours$", "", t)
    t = re.sub(r",\s*(?:from|à partir de|desde|החל מ-?)\s.*$", "", t)
    m2 = re.match(r"^(.{4,}?)\s*:\s", t)
    if m2: t = m2.group(1)
    m3 = re.match(r"^(.*?[?？])\s+\S", t)
    if m3: t = m3.group(1)
    return t.strip().rstrip(".")

def court(nom):
    m = re.match(r"^(.{8,}?)(?:,|:| \(| with | avec | con | via | for )", nom)
    return m.group(1) if m else nom
def tronque(nom, n=40):
    if len(nom) <= n: return nom
    w = nom[:n].rsplit(" ", 1)[0].split()
    while len(w) > 1 and (len(w[-1]) <= 3 or w[-1].lower() in ("de", "des", "du", "the", "and", "for")): w.pop()
    return " ".join(w).rstrip(",:;")

# ---------------------------------------------------------------- lecture des liens d'une page
TAG_RE = re.compile(r"<a\b[^>]*>", re.S)
HREF_RE = re.compile(r'href="(https://wa\.me/' + PH + r')(?:\?text=([^"]*))?"')
def liens_page(s):
    out = []
    for m in TAG_RE.finditer(s):
        tag = m.group(0); h = HREF_RE.search(tag)
        if not h: continue
        kind = "prix" if 'data-offre="prix-290"' in tag else "offre" if "data-offre=" in tag else "bare" if h.group(2) is None else "text"
        out.append({"pos": m.start(), "tag": tag, "old": decode(h.group(2)), "kind": kind})
    return out

class Plan:
    """décision de réécriture pour une page"""
    def __init__(self, liens, l, typ, nom, freq, slug=""):
        self.l, self.typ, self.nom, self.freq = l, typ, nom, freq
        self.he_msg = message_he(slug, nom) if l == "he" else None
        pdom = PAGE_DOM[typ]
        cands = collections.Counter(); self.raisons = collections.Counter()
        for L in liens:
            if L["kind"] == "prix": continue
            L["rest"] = None if L["old"] is None else reste(L["old"], l)
            L["bad"] = self.mauvais(L, pdom)
            if not L["bad"] and L["kind"] == "text" and freq.get(L["rest"], 1) < 15: cands[L["rest"]] += 1
        # message propre de la page : le candidat unique, ou le plus rare du site s'il l'est strictement (variantes de panneau exclues)
        self.primaire = None
        if cands:
            rang = sorted(cands, key=lambda r: freq.get(r, 1))
            if len(rang) == 1 or freq.get(rang[0], 1) < freq.get(rang[1], 1): self.primaire = rang[0]
        self.gab = GABARIT[GAB_TYPE[typ]][l]
        self.remplace = self.he_msg or (self.gab if typ == "chalet" else (self.primaire or self.gab))
        self.liens = [L for L in liens if L["kind"] != "prix"]
        self.fixer_nom(nom)
    def fixer_nom(self, nom):
        """un seul nom de page par page : le nom entier, ou le nom court si un message dépasse la limite"""
        def mx(n): return max([len(composer(self.l, n, self.remplace if L["bad"] else L["rest"])) for L in self.liens] or [0])
        self.nom = nom
        for cand in (court(nom), tronque(nom), tronque(court(nom)), tronque(nom, 28), tronque(nom, 20)):   # seul le nom raccourcit, jamais le sujet ni les champs
            if mx(self.nom) <= MAXLEN: break
            if len(cand) < len(self.nom): self.nom = cand
        self.principal = composer(self.l, self.nom, self.remplace)
    def mauvais(self, L, pdom):
        if L["kind"] == "bare": return "nu"
        lg = lang_of(sans_origine(L["old"], self.l))
        if lg is not None and lg != self.l: return "langue"
        if L["kind"] != "offre" and pdom != "both":
            d = dom_texte(L["rest"])
            if d in ("lyon", "alps") and d != pdom: return "sujet"
        if self.he_msg and L["kind"] == "text" and re.match(r"(?:נרצה שירותים כשרים באלפים|אשמח לקבל מידע על השירותים שלכם)", corriger(L["rest"], "he")): return "general-he"
        if self.typ == "chalet" and L["kind"] == "text" and (self.freq.get(L["rest"], 1) >= 15 or not re.search(r"chalet|chalé|צ'אל", L["rest"], re.I)): return "general-chalet"
        return None
    def nouveau(self, L):
        return composer(self.l, self.nom, self.remplace if L["bad"] else L["rest"])   # le sujet précis n'est jamais sacrifié

# ---------------------------------------------------------------- partie B : ligne prix
PRIX = {"en": "Private tour from 290 € · 1 to 4 people", "fr": "Visite privée dès 290 € · 1 à 4 personnes",
        "es": "Visita privada desde 290 € · 1 a 4 personas", "he": "סיור פרטי החל מ-290 € לקבוצה · 1 עד 4 משתתפים"}
PRIX_PAGES = ["rue-juiverie-lyon", "grande-synagogue-lyon", "synagogues-lyon", "chrd-lyon", "montluc-prison-lyon",
              "jewish-history-lyon", "jewish-cemetery-lyon", "jewish-lyon-guide", "jewish-lyon-itinerary-2-days", "things-to-do-in-lyon"]
PRIX_BLOC_RE = re.compile(r'<div class="lot1-prix">.*?</div>', re.S)
CSS_DEB, CSS_FIN = "/* ===LOT1-1611-PRIX=== ligne « visite privée dès 290 € » sous le h1 des pages patrimoine de Lyon (_lot1_1611_wa.py) */", "/* ===/LOT1-1611-PRIX=== */"
_N = "".join(":not(#q%d)" % i for i in range(1, 10))
CSS = CSS_DEB + "\n" + "\n".join([
    f"html body.lv{_N} .hero-texte .lot1-prix{{display:block !important;position:relative;z-index:2;margin:12px auto 0 !important;padding:0 !important;max-width:none !important;text-align:center !important;background:none !important;border:0 !important;box-shadow:none !important}}",
    f"html body.lv{_N} .hero-texte .lot1-prix a{{display:inline-block !important;white-space:nowrap !important;min-height:44px;padding:0 !important;font:400 13px/44px 'Jost',sans-serif !important;letter-spacing:.16em !important;text-transform:uppercase !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;text-decoration:underline !important;text-decoration-color:#A88F5E !important;text-decoration-thickness:1px !important;text-underline-offset:.55em !important;text-decoration-skip-ink:none;background:none !important;border:0 !important;border-radius:4px;box-shadow:none !important;text-shadow:none !important}}",
    f"html body.lv{_N} .hero-texte .lot1-prix a:focus-visible{{outline:2px solid #A88F5E;outline-offset:2px}}",
    f"html[dir=\"rtl\"] body.lv{_N} .hero-texte .lot1-prix a{{letter-spacing:0 !important;font:400 14px/44px Heebo,Jost,sans-serif !important}}",
    f"@media (max-width:899px){{html body.lv{_N} .hero-texte .lot1-prix{{margin-bottom:64px !important}}html body.lv{_N} .hero-texte .lot1-prix a{{font-size:clamp(9px,2.7vw,12px) !important;letter-spacing:.07em !important}}html[dir=\"rtl\"] body.lv{_N} .hero-texte .lot1-prix a{{font-size:clamp(11px,3.4vw,14px) !important}}}}",
    f"@media (min-width:900px){{html body.lv{_N} .hero-texte .lot1-prix{{grid-column:2 / -1 !important;justify-self:center;width:max-content;margin-top:-44px !important}}}}",
    f"html body.lv:not(.bn){_N} .hero-texte .lot1-prix a,html body.lv:not(.bn){_N} .lot1-prix a{{color:#111111 !important;-webkit-text-fill-color:#111111 !important}}",
]) + "\n" + CSS_FIN + "\n"

# ---------------------------------------------------------------- traitement d'une page
def traiter(rel, s, freq, stats, rapport):
    lang, slug = lang_slug(rel)
    typ = type_page(slug)
    if typ is None:
        typ = "general"; rapport["type_inconnu"].append(rel)
    if lang == "he": s = hebreu_page(s, slug)
    nom = nom_page(s, lang, slug)
    liens = liens_page(s)
    plan = Plan(liens, lang, typ, nom, freq, slug)
    out, dernier, nl = [], 0, 0
    carte = {}
    pages_prix = slug in PRIX_PAGES
    for L in liens:
        if L["kind"] == "prix":
            continue
        new = plan.nouveau(L)
        if len(new) > MAXLEN: rapport["trop_long"].append((rel, len(new)))
        carte[L["old"]] = new
        stats["liens"][(typ, lang)] += 1
        stats["decision"][L["bad"] or ("offre" if L["kind"] == "offre" else "gardé")] += 1
        if L["bad"]: stats["bad"][(L["bad"], typ, lang)] += 1
        nt = HREF_RE.sub(lambda m: 'href="%s?text=%s"' % (WA, encode(new)), L["tag"], count=1)
        out.append(s[dernier:L["pos"]]); out.append(nt); dernier = L["pos"] + len(L["tag"]); nl += 1
    out.append(s[dernier:]); s2 = "".join(out)
    # ligne prix (partie B)
    prix_url = WA + "?text=" + encode(plan.principal)
    if pages_prix and typ == "lyon":
        bloc = ('<div class="lot1-prix"><a href="%s" data-offre="prix-290" rel="noopener">%s</a></div>'
                % (prix_url, html.escape(PRIX[lang], quote=False)))
        s2 = PRIX_BLOC_RE.sub("", s2)
        s2, n = re.subn(r"(</h1>)(\s*</div>\s*</section>)", lambda m: m.group(1) + bloc + m.group(2), s2, count=1)
        if not n: rapport["prix_non_pose"].append(rel)
        else: stats["prix"][lang] += 1
    # JavaScript : gabarit du chercheur
    def js(m):
        t = composer(lang, nom, CHERCHEUR[lang])
        t = t.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\u0001").replace("\u0001f.", "${f.").replace("\u0001", "\\${")
        stats["js"]["chercheur"] += 1
        return "const t=`" + t + "`" + m.group(1)
    s2 = re.sub(r"const t=`[^`]*`(;window\.open\('https://wa\.me/" + PH + r"\?text='\+encodeURIComponent\(t\))", js, s2)
    # JavaScript : repli du formulaire court de /contact-quick/
    def cq(m):
        stats["js"]["contact-quick"] += 1
        return m.group(1) + "+' (page: " + nom.replace("\\", "\\\\").replace("'", "\\'") + ")';"
    s2 = re.sub(r"(var t='Hello, I am '\+pre\+'\. '\+\(ouV\?ouV\+'\. ':''\)\+\(nV\?nV\+' guests\.':''\))(?:\+' \(page: [^']*\)')?;", cq, s2)
    # attribut data-wa-sujet sur <body> (lu par js/court.js)
    def body(m):
        tag = re.sub(r'\sdata-wa-sujet="[^"]*"', "", m.group(0))
        return tag[:-1] + ' data-wa-sujet="%s">' % html.escape(nom, quote=True)
    s2 = re.sub(r"<body\b[^>]*>", body, s2, count=1)
    # liens JS non réécrits et résidus
    total = len(re.findall(r"wa\.me/" + PH, s2))
    nhref = len(re.findall(r'href="https://wa\.me/' + PH, s2))
    njs = len(re.findall(r"'https://wa\.me/" + PH + r"\?text='", s2))
    if total != nhref + njs: rapport["residus"].append((rel, total - nhref - njs))
    stats["js"]["non_modifie"] += len(re.findall(r"a\.href='https://wa\.me/" + PH, s2))
    return s2, carte, plan, typ, lang, slug

def md_page(path, carte, plan, slug, lang, typ, stats):
    """miroir index.md : même correspondance ancien -> nouveau"""
    if not os.path.exists(path): return
    m0 = lire(path); m = hebreu_page(m0, slug) if lang == "he" else m0
    def sub(mm):
        old = decode(mm.group(1))
        if old in carte: new = carte[old]
        else:
            L = {"old": old, "kind": "bare" if old is None else "text"}
            if old is not None: L["rest"] = reste(old, lang)
            else: L["rest"] = None
            L["bad"] = plan.mauvais(L, PAGE_DOM[plan.typ]); new = plan.nouveau(L)
        stats["md"]["liens"] += 1
        return WA + "?text=" + encode(new)
    m = re.sub(r"https://wa\.me/" + PH + r"(?:\?text=([^\s)]*))?", sub, m)
    if slug in PRIX_PAGES and typ == "lyon":
        ligne = "[%s](%s?text=%s)" % (PRIX[lang], WA, encode(plan.principal))
        nl = "\r\n" if "\r\n" in m else "\n"
        m = re.sub(r"^\[%s\]\(https://wa\.me/%s[^)]*\)\r?\n\r?\n" % (re.escape(PRIX[lang]), PH), "", m, flags=re.M)
        m, n = re.subn(r"^(# [^\r\n]*\r?\n)(\r?\n)?", lambda mm: mm.group(1) + nl + ligne + nl + nl, m, count=1, flags=re.M)
        if n: stats["md"]["prix"] += 1
    if m != m0:
        stats["md"]["modifies"] += 1
        if not DRY: ecrire(path, m)

def main():
    CSS_SEUL = "--css" in sys.argv
    pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if rel.startswith("_"): continue
        pages.append(rel)
    stats = {k: collections.Counter() for k in ("liens", "decision", "bad", "prix", "js", "md", "pages")}
    rapport = collections.defaultdict(list)
    # 1re passe : fréquence de chaque texte (nombre de pages ; 15 pages ou plus = texte générique)
    contenu, freq = {}, collections.defaultdict(set)
    for rel in ([] if CSS_SEUL else pages):
        l = lang_slug(rel)[0]
        s = lire(os.path.join(ROOT, rel)); contenu[rel] = s
        for L in liens_page(s):
            if L["old"] is not None and L["kind"] == "text": freq[reste(L["old"], l)].add(rel)
    freq = {r: len(ps) for r, ps in freq.items()}
    # 2e passe
    avant_bh = apres_bh = 0
    for rel in ([] if CSS_SEUL else pages):
        s = contenu[rel]
        avant_bh += s.count("wa.me/" + BH)
        if lang_slug(rel)[1] in PRIVEES:
            rapport["privees"].append((rel, s.count("wa.me/" + PH))); continue
        s2, carte, plan, typ, lang, slug = traiter(rel, s, freq, stats, rapport)
        stats["pages"][(typ, lang)] += 1
        apres_bh += s2.count("wa.me/" + BH)
        md_page(os.path.join(ROOT, rel[:-len("index.html")] + "index.md"), carte, plan, slug, lang, typ, stats)
        if s2 != s:
            stats["pages"]["modifiees"] += 1
            if not DRY: ecrire(os.path.join(ROOT, rel), s2)
    # CSS
    css_p = os.path.join(ROOT, "lv.css"); css = lire(css_p)
    css = re.sub(r"\r?\n?" + re.escape(CSS_DEB[:30]) + r".*?" + re.escape(CSS_FIN) + r"\r?\n?", "", css, flags=re.S)
    nl = "\r\n" if "\r\n" in css else "\n"
    css2 = css.rstrip("\r\n") + nl + nl + CSS.replace("\n", nl)
    if css2 != lire(css_p):
        stats["pages"]["css"] += 1
        if not DRY: ecrire(css_p, css2)
    # js/court.js : repli du formulaire court avec la page d'origine
    cj_p = os.path.join(ROOT, "js", "court.js"); cj = lire(cj_p)
    ancien = "var t = T('msg-salut', 'Hello, I am') + ' ' + pre + '.' + (ou ? ' ' + ou + '.' : '');"
    if ancien in cj and "LOT1-1611" not in cj:
        nv = ancien[:-1] + " + (document.body.getAttribute('data-wa-sujet') ? ' (' + ({ fr: 'page', es: 'página', he: 'עמוד' }[(document.documentElement.lang || '').slice(0, 2)] || 'page') + ': ' + document.body.getAttribute('data-wa-sujet') + ')' : ''); /* LOT1-1611 : page d'origine */"
        stats["js"]["court.js"] += 1
        if not DRY: ecrire(cj_p, cj.replace(ancien, nv, 1))
    # comptes
    print("pages traitees :", sum(v for k, v in stats["pages"].items() if isinstance(k, tuple)), "| modifiees :", stats["pages"]["modifiees"], "| css :", stats["pages"]["css"])
    print("BH avant/apres :", avant_bh, apres_bh)
    print("liens par type/langue :")
    for typ in sorted({k[0] for k in stats["liens"]}):
        print("  %-12s" % typ, "  ".join("%s=%d(%dp)" % (l, stats["liens"][(typ, l)], stats["pages"][(typ, l)]) for l in ("en", "fr", "es", "he")))
    print("decisions :", dict(stats["decision"]))
    print("remplacements (raison, type, langue) :", dict(stats["bad"]))
    print("prix par langue :", dict(stats["prix"]))
    print("js :", dict(stats["js"]), "| md :", dict(stats["md"]))
    for k in ("type_inconnu", "trop_long", "prix_non_pose", "residus", "privees"):
        print(k, ":", rapport[k][:30], "(%d)" % len(rapport[k]))

if __name__ == "__main__":
    main()
