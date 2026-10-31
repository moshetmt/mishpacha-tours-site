# -*- coding: utf-8 -*-
"""Maillage interne du 30/10/2026 (plan : clients/mishpacha-tours/06-reports/2026-10-30-internal-linking.md).
Idempotent, 4 langues (EN racine, fr/, es/, he/), index.html puis index.md régénéré (même logique que _agentic.py).
À relancer après toute régénération ; une 2e passe ne change rien.

1. Lyon tours : une phrase avec un lien vers /jewish-lyon-tours/ dans le premier tiers des 14 pages patrimoine et pratique
   de Lyon (ancre descriptive, variée, jamais « Tours »). Rien si le corps lie déjà la page.
2. Stations voisines : bloc « Stations voisines » (3 ou 4 stations du même massif, pays entre parenthèses quand il change,
   plus le hub /alps/) avant « Pour aller plus loin » sur les 20 pages station. Même balisage que ce bloc (section ss wrap, dk-suite).
3. Pessah : une phrase avec l'ancre « Pessah dans les Alpes, chalet privé et cuisine cachérisée » sur l'accueil, le hub
   /kosher-chalets/, les 5 fiches chalet (près du bloc Chabbat) et les 11 stations françaises (après le bloc chef).
4. Pages jamais explorées : /jewish-lyon-guide/ et /jewish-lyon-itinerary-2-days/ ajoutés à la liste « Pour aller plus loin »
   de rue-juiverie, montluc et mikveh (lien vers la copie de la même langue) ; /synagogues-lyon/ y figure déjà.

    python _maillage.py   (depuis site-v5/)"""
import io, os, re, glob
from markdownify import markdownify as md

BASE = "https://mishpachatours.com"
LANGS = [("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")]

def lire(p): return io.open(p, encoding="utf-8", newline="").read()
def ecrire(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def chemin(pref, slug): return f"{pref}{slug}/index.html" if slug else f"{pref}index.html"
def corps(s):
    """<main> sans nav, header, footer : là où comptent les liens de contenu"""
    m = re.search(r"<main.*?</main>", s, re.S)
    return re.sub(r"<(nav|header|footer)\b.*?</\1>", "", m.group(0), flags=re.S) if m else ""
def lie(s, slug):
    return re.search(r'href="(?:\.\./|/(?:fr|es|he)/|/)' + re.escape(slug) + r'/"', corps(s)) is not None
def texte(x): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.sub(r"<(script|style|svg)\b.*?</\1>", "", x, flags=re.S)))

# ---------------------------------------------------------------------------------------------------------------------
# 1. Lyon tours
A = '<a href="../jewish-lyon-tours/">'
LYON = {
 "rue-juiverie-lyon": {
  "en": f"We walk this street on {A}the guided walk through Jewish Lyon</a>.",
  "fr": f"Nous parcourons cette rue pendant {A}la visite guidée du quartier juif de Lyon</a>.",
  "es": f"Recorremos esta calle durante {A}la visita guiada por el Lyon judío</a>.",
  "he": f"אנחנו עוברים ברחוב הזה במהלך {A}הסיור המודרך בליון היהודית</a>."},
 "montluc-prison-lyon": {
  "en": f"Montluc is a stop on {A}our Memory tour of Montluc and the CHRD</a>.",
  "fr": f"Montluc est une étape de {A}notre visite Mémoire, Montluc et le CHRD</a>.",
  "es": f"Montluc es una etapa de {A}nuestra visita Memoria, Montluc y el CHRD</a>.",
  "he": f"מונלוק הוא תחנה {A}בסיור הזיכרון שלנו, מונלוק ו-CHRD</a>."},
 "synagogues-lyon": {
  "en": f"{A}Our private tours of Jewish Lyon</a> take you inside the Grande Synagogue.",
  "fr": f"{A}Nos visites privées du patrimoine juif de Lyon</a> vous font entrer dans la Grande Synagogue.",
  "es": f"{A}Nuestras visitas privadas por el Lyon judío</a> le llevan al interior de la Gran Sinagoga.",
  "he": f"{A}הסיורים הפרטיים שלנו בליון היהודית</a> מכניסים אתכם לבית הכנסת הגדול."},
 "mikveh-lyon": {
  "en": f"Our guide also leads {A}the Jewish heritage tours of Lyon</a>.",
  "fr": f"Notre guide mène aussi {A}les visites du patrimoine juif de Lyon</a>.",
  "es": f"Nuestra guía también dirige {A}las visitas del patrimonio judío de Lyon</a>.",
  "he": f"המדריכה שלנו מובילה גם את {A}סיורי המורשת היהודית של ליון</a>."},
 "chrd-lyon": {
  "en": f"The CHRD is one of the two sites of {A}the Memory tour, Montluc and the CHRD</a>.",
  "fr": f"Le CHRD est l’un des deux lieux de {A}la visite Mémoire, Montluc et le CHRD</a>.",
  "es": f"El CHRD es uno de los dos lugares de {A}la visita Memoria, Montluc y el CHRD</a>.",
  "he": f"ה-CHRD הוא אחד משני האתרים {A}בסיור הזיכרון, מונלוק ו-CHRD</a>."},
 "maison-izieu": {
  "en": f"We take you there on {A}the Izieu day trip with a Jewish guide</a>.",
  "fr": f"Nous vous y emmenons avec {A}l’excursion à Izieu avec une guide juive</a>.",
  "es": f"Le llevamos allí con {A}la excursión a Izieu con una guía judía</a>.",
  "he": f"אנחנו לוקחים אתכם לשם {A}בטיול יום לאיזיה עם מדריכה יהודית</a>."},
 "chabad-lyon": {
  "en": f"For the heritage side, {A}our guided tours of Jewish Lyon</a> start a few minutes away.",
  "fr": f"Pour le patrimoine, {A}nos visites guidées du quartier juif de Lyon</a> partent à quelques minutes de là.",
  "es": f"Para el patrimonio, {A}nuestras visitas guiadas por el Lyon judío</a> salen a pocos minutos.",
  "he": f"{A}הסיורים המודרכים שלנו בליון היהודית</a> יוצאים במרחק דקות ספורות משם."},
 "grande-synagogue-lyon": {
  "en": f"Entry is part of {A}the only tour inside the Grande Synagogue</a>.",
  "fr": f"L’entrée fait partie de {A}la seule visite qui entre dans la Grande Synagogue</a>.",
  "es": f"La entrada forma parte de {A}la única visita que entra en la Gran Sinagoga</a>.",
  "he": f"הכניסה היא חלק {A}מהסיור היחיד שמכניס אתכם לבית הכנסת הגדול</a>."},
 "shabbat-in-lyon": {
  "en": f"Before Shabbat comes in, {A}a Friday walk through Jewish Lyon</a> ends well before candle lighting.",
  "fr": f"Avant l’entrée du Shabbat, {A}une visite du quartier juif de Lyon le vendredi</a> se termine bien avant l’allumage.",
  "es": f"Antes de que entre el Shabat, {A}una visita por el Lyon judío el viernes</a> termina mucho antes del encendido.",
  "he": f"לפני כניסת השבת, {A}סיור בליון היהודית ביום שישי</a> מסתיים הרבה לפני הדלקת הנרות."},
 "jewish-cemetery-lyon": {
  "en": f"The cemetery can be added to {A}a private tour of Jewish Lyon</a> on request.",
  "fr": f"Le cimetière s’ajoute à {A}une visite privée du patrimoine juif de Lyon</a> sur demande.",
  "es": f"El cementerio se añade a {A}una visita privada por el Lyon judío</a> bajo petición.",
  "he": f"אפשר להוסיף את בית הקברות {A}לסיור פרטי בליון היהודית</a> לפי בקשה."},
 "jewish-history-lyon": {
  "en": f"This history is told on site, on {A}the walking tour of Jewish Lyon</a>.",
  "fr": f"Cette histoire se raconte sur place, pendant {A}nos visites du patrimoine juif de Lyon</a>.",
  "es": f"Esta historia se cuenta sobre el terreno, en {A}la visita a pie por el Lyon judío</a>.",
  "he": f"ההיסטוריה הזאת מסופרת במקום, {A}בסיור הרגלי בעקבות יהדות ליון</a>."},
 "kosher-restaurants-lyon": {
  "en": f"Lunch here fits between two stops of {A}the Jewish Lyon tour</a>.",
  "fr": f"Un déjeuner ici se cale entre deux étapes de {A}la visite du quartier juif de Lyon</a>.",
  "es": f"Un almuerzo aquí encaja entre dos paradas de {A}la visita por el Lyon judío</a>.",
  "he": f"ארוחת צהריים כאן משתלבת בין שתי תחנות של {A}הסיור בליון היהודית</a>."},
 "kosher-shabbat-meals-catering-lyon": {
  "en": f"Pair the meal with {A}a guided visit of Jewish Lyon</a> before Shabbat.",
  "fr": f"Associez le repas à {A}une visite guidée des lieux juifs de Lyon</a> avant Shabbat.",
  "es": f"Combine la comida con {A}una visita guiada por el Lyon judío</a> antes del Shabat.",
  "he": f"שלבו את הארוחה עם {A}סיור מודרך בליון היהודית</a> לפני שבת."},
 "things-to-do-in-lyon": {
  "en": f"For the Jewish side of the city, start with {A}our guided tours of Jewish Lyon</a>.",
  "fr": f"Pour le côté juif de la ville, commencez par {A}nos visites guidées du patrimoine juif de Lyon</a>.",
  "es": f"Para el lado judío de la ciudad, empiece por {A}nuestras visitas guiadas por el Lyon judío</a>.",
  "he": f"לצד היהודי של העיר, התחילו {A}בסיורים המודרכים שלנו בליון היהודית</a>."},
}

def lyon_tours(s, phrase):
    if lie(s, "jewish-lyon-tours"): return s, "déjà"
    m = re.search(r"<main>(.*?)</main>", s, re.S); b = m.group(1); deb = m.start(1)
    h = b.find("</section>") + len("</section>")                     # fin du héros
    total = len(texte(b))
    p = re.search(r'<p(?: class="sous[^"]*")?>', b[h:])
    if p and len(texte(b[:h + p.start()])) <= total / 3:
        ouvre = h + p.start()
    else:                                                          # premier paragraphe trop bas : l'intro du héros
        p = re.search(r'<p class="intro-fiche[^"]*">', b)
        if not p: return s, "sans paragraphe"
        ouvre = p.start()
    ferme = b.find("</p>", ouvre)
    b = b[:ferme] + " " + phrase + b[ferme:]
    return s[:deb] + b + s[m.end(1):], "ajouté"

# ---------------------------------------------------------------------------------------------------------------------
# 2. Stations voisines
PAYS = {"fr": {"en": "France", "fr": "France", "es": "Francia", "he": "צרפת"},
        "ch": {"en": "Switzerland", "fr": "Suisse", "es": "Suiza", "he": "שווייץ"},
        "it": {"en": "Italy", "fr": "Italie", "es": "Italia", "he": "איטליה"}}
# slug : (nom latin, nom hébreu, pays, voisines dans l'ordre)
STATIONS = {
 "courchevel":     ("Courchevel", "קורשבל", "fr", ["val-thorens", "la-plagne", "les-arcs", "val-disere"]),
 "val-thorens":    ("Val Thorens", "ואל טורנס", "fr", ["courchevel", "la-plagne", "les-arcs", "val-disere"]),
 "les-arcs":       ("Les Arcs", "לז ארק", "fr", ["la-plagne", "val-disere", "courchevel", "val-thorens"]),
 "la-plagne":      ("La Plagne", "לה פלאן", "fr", ["les-arcs", "val-disere", "courchevel", "val-thorens"]),
 "val-disere":     ("Val d’Isère", "ואל דיזר", "fr", ["les-arcs", "la-plagne", "courchevel", "val-thorens"]),
 "les-deux-alpes": ("Les Deux Alpes", "לה דז אלפ", "fr", ["alpe-dhuez", "grenoble", "val-thorens"]),
 "alpe-dhuez":     ("Alpe d’Huez", "אלפ ד'ואז", "fr", ["les-deux-alpes", "grenoble", "val-thorens"]),
 "grenoble":       ("Grenoble", "גרנובל", "fr", ["les-deux-alpes", "alpe-dhuez", "courchevel"]),
 "megeve":         ("Megève", "מג'ב", "fr", ["chamonix", "annecy", "courmayeur"]),
 "chamonix":       ("Chamonix", "שמוני", "fr", ["megeve", "annecy", "courmayeur"]),
 "annecy":         ("Annecy", "אנסי", "fr", ["megeve", "chamonix", "courchevel"]),
 "verbier":        ("Verbier", "ורבייה", "ch", ["crans-montana", "zermatt", "gstaad"]),
 "gstaad":         ("Gstaad", "גשטאד", "ch", ["verbier", "crans-montana", "davos"]),
 "davos":          ("Davos", "דאבוס", "ch", ["st-moritz", "gstaad", "zermatt"]),
 "zermatt":        ("Zermatt", "צרמט", "ch", ["crans-montana", "verbier", "cervinia"]),
 "st-moritz":      ("St. Moritz", "סנט מוריץ", "ch", ["davos", "zermatt", "cortina"]),
 "crans-montana":  ("Crans-Montana", "קראן מונטנה", "ch", ["verbier", "zermatt", "gstaad"]),
 "cervinia":       ("Cervinia", "צרביניה", "it", ["zermatt", "courmayeur", "cortina"]),
 "courmayeur":     ("Courmayeur", "קורמאיור", "it", ["chamonix", "cervinia", "cortina"]),
 "cortina":        ("Cortina", "קורטינה ד'אמפצו", "it", ["cervinia", "courmayeur", "st-moritz"]),
}
STATIONS_FR = [k for k, v in STATIONS.items() if v[2] == "fr"]
H2_VOISINES = {"en": "Nearby <i>resorts</i>", "fr": "Stations <i>voisines</i>", "es": "Estaciones <i>cercanas</i>", "he": "אתרי סקי <i>סמוכים</i>"}
HUB = {"en": "All our resorts in the Alps", "fr": "Toutes nos stations dans les Alpes", "es": "Todas nuestras estaciones en los Alpes", "he": "כל אתרי הסקי שלנו באלפים"}
ICO = '<img class="dk dk-ico dk-vigico dk-des" src="/img/ico/or/{ico}.svg" alt="" width="96" height="96" loading="lazy">'
FLECHE = '<svg class="dk dk-fleche" aria-hidden="true" focusable="false"><use href="/img/pictos.svg#arrow-right"/></svg>'
def li(ico, href, ancre): return f"<li>{ICO.format(ico=ico)}<a href=\"{href}\">{ancre}</a>{FLECHE}</li>"

def nom_station(slug, lang):
    nom, he, pays, _ = STATIONS[slug]
    return {"en": f"Kosher {nom}", "fr": f"{nom} casher", "es": f"{nom} kosher", "he": f"כשר ב{he}"}[lang]

def bloc_voisines(slug, lang):
    pays = STATIONS[slug][2]; lis = []
    for v in STATIONS[slug][3]:
        ancre = nom_station(v, lang)
        if STATIONS[v][2] != pays: ancre += f" ({PAYS[STATIONS[v][2]][lang]})"
        lis.append(li("mountain-snow", f"../kosher-{v}/", ancre))
    lis.append(li("snowflake", "../alps/", HUB[lang]))
    return f'<section class="clair ss wrap conseils" id="voisines"><h2>{H2_VOISINES[lang]}</h2><ul class="dk-suite">{"".join(lis)}</ul></section>\n'

def voisines(s, slug, lang):
    bloc = bloc_voisines(slug, lang)
    if 'id="voisines"' in s:
        n = re.sub(r'<section class="clair ss wrap conseils" id="voisines">.*?</section>\n', lambda _: bloc, s, count=1, flags=re.S)
        return n, ("à jour" if n != s else "déjà")
    m = re.search(r"<main>(.*?)</main>", s, re.S); b = m.group(1)
    i = b.rfind('<section class="clair ss wrap conseils"><h2>')          # « Pour aller plus loin », dernier bloc du contenu
    if i < 0 or "dk-suite" not in b[i:]: return s, "sans bloc de fin"
    b = b[:i] + bloc + b[i:]
    return s[:m.start(1)] + b + s[m.end(1):], "ajouté"

# ---------------------------------------------------------------------------------------------------------------------
# 3. Pessah
ANCRE_PESSAH = {"en": "Pesach in the Alps, private chalet and kashered kitchen",
                "fr": "Pessah dans les Alpes, chalet privé et cuisine cachérisée",
                "es": "Pésaj en los Alpes, chalé privado y cocina kasherizada",
                "he": "פסח באלפים, צ'אלה פרטית ומטבח מוכשר"}
PH_CHALET = {"en": "For Pesach, we prepare the chalet too: {a}.", "fr": "Pour Pessah, nous préparons aussi le chalet : {a}.",
             "es": "Para Pésaj, también preparamos el chalé: {a}.", "he": "לפסח אנחנו מכינים גם את הצ'אלה: {a}."}
PH_STATION = {"en": "We also organise Pesach: {a}.", "fr": "Nous organisons aussi Pessah : {a}.",
              "es": "También organizamos Pésaj: {a}.", "he": "אנחנו מארגנים גם את פסח: {a}."}
CHALETS = ["kosher-chalet-courchevel", "kosher-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-chalet-val-thorens", "kosher-slope-chalet-les-deux-alpes"]

def phrase_pessah(gabarit, lang, href):
    return gabarit[lang].format(a=f'<a href="{href}">{ANCRE_PESSAH[lang]}</a>')

def pessah(s, lang, ou, pref):
    if ANCRE_PESSAH[lang] + "</a>" in corps(s): return s, "déjà"
    if ou == "accueil":                                   # sous-titre du bloc « Comment voulez-vous voyager ? », à côté de la carte Pessah
        ph = phrase_pessah(PH_CHALET, lang, f"/{pref}kosher-pesach-french-alps/")
        m = re.search(r'(<section class="clair ss beige" id="trips">.*?<p class="sous">.*?)(</p>)', s, re.S)
        if not m: return s, "sans bloc"
        return s[:m.end(1)] + " " + ph + s[m.end(1):], "ajouté"
    if ou in ("hub", "chalet"):                           # premier encadré beige : « Ce que comprend chaque séjour » / « Chabbat au chalet »
        ph = phrase_pessah(PH_CHALET, lang, "../kosher-pesach-french-alps/")
        m = re.search(r'<div class="clair ss beige(?: dk-recit)?"><div class="wrap"><h2>.*?(</div></div>)', s, re.S)
        if not m: return s, "sans bloc"
        return s[:m.start(1)] + f"<p>{ph}</p>" + s[m.start(1):], "ajouté"
    if ou == "station":                                   # après la ligne de garantie du bloc « Ce que nous organisons »
        ph = phrase_pessah(PH_STATION, lang, "../kosher-pesach-french-alps/")
        m = re.search(r'<p class="dk-garanties">.*?</p>', s, re.S)
        if not m: return s, "sans bloc"
        return s[:m.end()] + f"<p>{ph}</p>" + s[m.end():], "ajouté"

# ---------------------------------------------------------------------------------------------------------------------
# 4. Pages jamais explorées : liste « Pour aller plus loin » de 3 pages FR à affichages (et leurs copies)
EXPLO = [("jewish-lyon-guide", "compass", {"en": "Jewish Lyon, the complete guide", "fr": "Le patrimoine juif de Lyon, le guide complet",
                                            "es": "Lyon judío, la guía completa", "he": "ליון היהודית, המדריך המלא"}),
         ("jewish-lyon-itinerary-2-days", "route", {"en": "Jewish Lyon in two days", "fr": "Le patrimoine juif de Lyon en deux jours",
                                                     "es": "Lyon judío en dos días", "he": "ליון היהודית בשני ימים"})]
PAGES_EXPLO = ["rue-juiverie-lyon", "montluc-prison-lyon", "mikveh-lyon"]

def explo(s, lang):
    ajouts = [li(ico, f"../{slug}/", ancres[lang]) for slug, ico, ancres in EXPLO if not lie(s, slug)]
    if not ajouts: return s, "déjà"
    m = re.search(r"<main>(.*?)</main>", s, re.S); b = m.group(1)
    i = b.rfind('<ul class="dk-suite">')
    if i < 0: return s, "sans liste"
    j = b.find("</ul>", i)
    b = b[:j] + "".join(ajouts) + b[j:]
    return s[:m.start(1)] + b + s[m.end(1):], "ajouté"

# ---------------------------------------------------------------------------------------------------------------------
# index.md : même logique que _agentic.py (section 3)
def meta(h, name):
    r = re.search(rf'<meta name="{name}" content="([^"]*)"', h); return r.group(1) if r else ""

def markdown(p):
    d = os.path.dirname(p).replace("\\", "/")
    h = lire(p)
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {meta(h, 'description')}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    q = os.path.join(os.path.dirname(p), "index.md")
    ancien = lire(q) if os.path.exists(q) else ""
    if "\r\n" in ancien: out = out.replace("\n", "\r\n")
    if out != ancien: ecrire(q, out); return 1
    return 0

# ---------------------------------------------------------------------------------------------------------------------
def main():
    bilan = {}; touchees = set(); nb_html = 0
    def passe(chantier, slug, lang, pref, f):
        nonlocal nb_html
        p = chemin(pref, slug)
        if not os.path.exists(p): bilan.setdefault(chantier, []).append(f"{lang}:{slug}:ABSENT"); return
        s = lire(p); n, etat = f(s)
        if n != s: ecrire(p, n); nb_html += 1
        touchees.add(p)
        if etat not in ("déjà",): bilan.setdefault(chantier, []).append(f"{lang}:{slug}:{etat}")
    for lang, pref in LANGS:
        for slug, phrases in LYON.items():
            passe("1 Lyon tours", slug, lang, pref, lambda s: lyon_tours(s, phrases[lang]))
        for slug in STATIONS:
            passe("2 Stations voisines", f"kosher-{slug}", lang, pref, lambda s, slug=slug: voisines(s, slug, lang))
        passe("3 Pessah", "", lang, pref, lambda s: pessah(s, lang, "accueil", pref))
        passe("3 Pessah", "kosher-chalets", lang, pref, lambda s: pessah(s, lang, "hub", pref))
        for slug in CHALETS:
            passe("3 Pessah", slug, lang, pref, lambda s: pessah(s, lang, "chalet", pref))
        for slug in STATIONS_FR:
            passe("3 Pessah", f"kosher-{slug}", lang, pref, lambda s: pessah(s, lang, "station", pref))
        for slug in PAGES_EXPLO:
            passe("4 Pages non explorées", slug, lang, pref, lambda s: explo(s, lang))
    nb_md = sum(markdown(p) for p in sorted(touchees))
    for k in sorted(bilan):
        v = bilan[k]; print(k, ":", len(v), "changement(s)", "" if len(v) < 12 else "", ", ".join(v) if len(v) <= 12 else "")
        for x in v:
            if not x.endswith(("ajouté", "à jour")): print("   ⚠", x)
    print(f"{nb_html} index.html modifiés, {nb_md} index.md régénérés, {len(touchees)} pages contrôlées")

if __name__ == "__main__":
    main()
