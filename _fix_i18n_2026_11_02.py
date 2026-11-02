# -*- coding: utf-8 -*-
"""Correctifs des traductions FR / ES / HE du 02/11/2026 (rapport 06-reports/2026-11-02-controle-zones/). Idempotent.
    python _fix_i18n_2026_11_02.py         : applique, puis lancer _md_pages.py sur les pages listées
    python _fix_i18n_2026_11_02.py --sec   : montre ce qui changerait, n'écrit rien
1. Liens internes des pages traduites qui partaient vers la page anglaise alors que la traduction existe.
2. Baseline du pied traduite (BASELINE de _zones.py et PIED_WP de _kit_wp.py, désormais par langue dans ces deux scripts).
3. Zones restées sur l'ancien gabarit après _ton_expert.py (14/10) et _icones_or.py (30/10) : reliquats retirés,
   phrases manquantes traduites, icônes or et classes dk-* recopiées de la zone anglaise, ordre des zones aligné.
Le sceau Winter Prestige (#C9A961, kwp-seau) reste tel quel : palette WP figée le 13/10."""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEC = "--sec" in sys.argv
LANGS = ("fr", "es", "he")
MANQUES = []


def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def chemin(lang, page): return "/".join(([lang] if lang != "en" else []) + ([page] if page else []) + ["index.html"])


def pages_en():
    out = {""}
    for p in glob.glob("**/index.html", recursive=True):
        d = os.path.dirname(p).replace("\\", "/")
        if d and not d.startswith("_") and d.split("/")[0] not in LANGS + ("espace", "preview", "merci"):
            out.add(d)
    return out


# ---------- 1. liens vers la page anglaise ----------
EXCLUS = re.compile(r'<details class="langue".*?</details>|<div class="panneau-langs">.*?</div>', re.S)

def liens(s, lang, page, en):
    corps = s.find("<body")
    zones_exclues = [(m.start(), m.end()) for m in EXCLUS.finditer(s)]
    def fix(m):
        if m.start() < corps or any(a <= m.start() < b for a, b in zones_exclues):
            return m.group(0)
        h = m.group(3)
        ch = h.split("#")[0].split("?")[0].strip("/")
        if (h.startswith(f"/{lang}/") or not ch or ch == page or ch not in en or "." in ch.split("/")[-1]
                or not os.path.exists(os.path.join(lang, ch, "index.html"))):
            return m.group(0)
        return m.group(1) + m.group(2) + "/" + lang + h + m.group(2)
    return re.sub(r"""(<a\b[^>]*?\bhref=)(["'])(/[^"']*)\2""", fix, s)


# ---------- 2. baseline du pied ----------
BASELINE = {"fr": {"Kosher Stays in the Alps": "Séjours casher dans les Alpes",
                   "Kosher Holidays in the Alps and Lyon": "Séjours casher dans les Alpes et à Lyon"},
            "es": {"Kosher Stays in the Alps": "Estancias kosher en los Alpes",
                   "Kosher Holidays in the Alps and Lyon": "Vacaciones kosher en los Alpes y Lyon"},
            "he": {"Kosher Stays in the Alps": "חופשות כשרות באלפים",
                   "Kosher Holidays in the Alps and Lyon": "חופשות כשרות באלפים ובליון"}}
PIED_WP = {"fr": " · avec Winter Prestige", "es": " · con Winter Prestige", "he": " · עם Winter Prestige"}

def baseline(s, lang):
    def fix(m):
        t = m.group(2)
        wp = t.endswith(" · with Winter Prestige")
        if wp: t = t[: -len(" · with Winter Prestige")]
        t = BASELINE[lang].get(t, t)
        return m.group(1) + t + (PIED_WP[lang] if wp else "") + m.group(3)
    return re.sub(r'(<p class="logo-pied">.*?<small>)([^<]*)(</small>)', fix, s, count=1, flags=re.S)


# ---------- 3. zones ----------
RACINE = re.compile(r'<(section|div) class="[^"]*\bss\b[^"]*"[^>]*>')

def bloc(s, marqueur):
    """(début, fin) de la zone (section ou div de classe ss) qui contient le marqueur."""
    i = s.find(marqueur)
    if i < 0: return None
    r = [m for m in RACINE.finditer(s, 0, min(len(s), i + len(marqueur) + 500)) if m.start() <= i]
    if not r: return None
    m = r[-1]; tag = m.group(1); prof = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, s[m.start():]):
        prof += -1 if t.group(1) else 1
        if prof == 0: return m.start(), m.start() + t.end()
    return None


def habiller(en, tr):
    """Recopie sur la zone traduite le décor de la zone anglaise : balise racine, picto du h2, classe de la liste,
    icône or de chaque puce (et classe de la puce), flèche des listes dk-suite, icône du premier paragraphe."""
    tr = RACINE.sub(lambda m: RACINE.match(en).group(0), tr, count=1)
    h2_en = re.search(r"<h2[^>]*>(<img[^>]*>)?", en)
    if h2_en.group(1) and not re.search(r"<h2[^>]*><img", tr):
        tr = re.sub(r"<h2[^>]*>", lambda m: h2_en.group(0), tr, count=1)
    ul_en = re.search(r"<ul[^>]*>", en)
    if ul_en: tr = re.sub(r"<ul[^>]*>", lambda m: ul_en.group(0), tr, count=1)
    li_en = re.findall(r"<li[^>]*>(?:<img[^>]*>)?", en)
    li_tr = re.findall(r"<li[^>]*>(?:<img[^>]*>)?", tr)
    if li_en and len(li_en) != len(li_tr):
        raise ValueError(f"puces : {len(li_en)} EN, {len(li_tr)} traduites")
    it = iter(li_en)
    tr = re.sub(r"<li[^>]*>(?:<img[^>]*>)?", lambda m: next(it), tr)
    fl = re.search(r'<svg class="dk dk-fleche".*?</svg>', en)
    if fl and "dk-fleche" not in tr:
        tr = re.sub(r"(<li\b.*?)(</li>)", lambda m: m.group(1) + fl.group(0) + m.group(2), tr, flags=re.S)
    p_en = re.search(r'</h2>\s*<p>(<img class="dk dk-ico dk-ico-(?:note|recit)[^>]*>)', en)
    if p_en and not re.search(r'</h2>\s*<p><img', tr):
        tr = re.sub(r"(</h2>\s*<p>)", lambda m: m.group(1) + p_en.group(1), tr, count=1)
    return tr


def carte(lang, slug, titre, texte):
    btn = {"fr": "Ouvrir", "es": "Abrir", "he": "פתחו"}[lang]
    return (f'<a class="hub-carte" href="/{lang}/{slug}/"><div class="photo"><img src="/img/cartes/hub-{slug}.webp" alt="" loading="lazy"></div>'
            f'<div class="corps"><h3>{titre}</h3><p>{texte}</p><span class="btn-noir">{btn}</span></div></a>')

SUISSE_ITALIE = ["kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana", "kosher-verbier", "kosher-gstaad", "kosher-davos",
                 "kosher-cervinia", "kosher-courmayeur", "kosher-cortina", "kosher-ski-anywhere"]
CARTES = {
    "fr": [("Casher à Zermatt", "Village sans voitures au pied du Cervin, l’hiver comme l’été : chef, repas, Shabbat, fêtes, minyan"),
           ("Casher à Saint-Moritz", "L’Engadine, l’hiver comme l’été : chef, repas, Shabbat, fêtes, minyan"),
           ("Casher à Crans-Montana", "Le plateau ensoleillé du Valais, à deux heures de Genève : chef, repas, Shabbat, fêtes, minyan"),
           ("Casher à Verbier", "Les 4 Vallées au-dessus de la vallée du Rhône, l’hiver comme l’été : chef privé, Shabbat, fêtes, minyan"),
           ("Casher à Gstaad", "Le Saanenland et Glacier 3000, l’hiver comme l’été : chef privé, Shabbat, fêtes, minyan"),
           ("Casher à Davos", "La ville la plus haute des Alpes, Parsenn et Jakobshorn, l’hiver comme l’été : chef privé, Shabbat, fêtes, minyan"),
           ("Casher à Cervinia", "Le versant italien du Cervin, de la neige de novembre à mai : chef, repas, Shabbat, fêtes, minyan"),
           ("Casher à Courmayeur", "Le versant italien du Mont-Blanc, la station italienne la plus proche de Lyon : chef, repas, Shabbat, fêtes, minyan"),
           ("Casher à Cortina d’Ampezzo", "Les Dolomites, l’hiver comme l’été : chef, repas, Shabbat, fêtes, minyan"),
           ("Ski casher, ailleurs", "Autriche, Amérique du Nord ou toute station hors de notre liste : un chef privé qui voyage avec vous, Shabbat, minyan, transferts")],
    "es": [("Kosher en Zermatt", "Pueblo sin coches al pie del Cervino, invierno y verano: chef, comidas, Shabat, fiestas, minián"),
           ("Kosher en St. Moritz", "La Engadina, en invierno y en verano: chef, comidas, Shabat, fiestas, minián"),
           ("Kosher en Crans-Montana", "La meseta soleada del Valais, a dos horas de Ginebra: chef, comidas, Shabat, fiestas, minián"),
           ("Kosher en Verbier", "Las 4 Vallées sobre el valle del Ródano, invierno y verano: chef privado, Shabat, fiestas, minián"),
           ("Kosher en Gstaad", "El Saanenland y Glacier 3000, invierno y verano: chef privado, Shabat, fiestas, minián"),
           ("Kosher en Davos", "La ciudad más alta de los Alpes, Parsenn y Jakobshorn, invierno y verano: chef privado, Shabat, fiestas, minián"),
           ("Kosher en Cervinia", "La vertiente italiana del Cervino, nieve de noviembre a mayo: chef, comidas, Shabat, fiestas, minián"),
           ("Kosher en Courmayeur", "La vertiente italiana del Mont Blanc, la estación italiana más cercana a Lyon: chef, comidas, Shabat, fiestas, minián"),
           ("Kosher en Cortina d'Ampezzo", "Los Dolomitas, invierno y verano: chef, comidas, Shabat, fiestas, minián"),
           ("Esquí kosher, en cualquier lugar", "Austria, Norteamérica o cualquier estación fuera de nuestra lista: un chef privado que viaja con usted, Shabat, minián, traslados")],
    "he": [("כשר בצרמט", "כפר ללא מכוניות מתחת להר מטרהורן, בחורף ובקיץ: שף, ארוחות, שבת, חגים, מניין"),
           ("כשר בסנט מוריץ", "האנגדין, בחורף ובקיץ: שף, ארוחות, שבת, חגים, מניין"),
           ("כשר בקראן מונטנה", "הרמה השטופה בשמש של הוואלה, שעתיים מז'נבה: שף, ארוחות, שבת, חגים, מניין"),
           ("כשר בורבייה", "ארבעת העמקים מעל עמק הרון, בחורף ובקיץ: שף פרטי, שבת, חגים, מניין"),
           ("כשר בגשטאד", 'אזור זאנן וקרחון <span dir="ltr">Glacier 3000</span>, בחורף ובקיץ: שף פרטי, שבת, חגים, מניין'),
           ("כשר בדאבוס", "העיר הגבוהה ביותר באלפים, פרסן ויאקובסהורן, בחורף ובקיץ: שף פרטי, שבת, חגים, מניין"),
           ("כשר בצרביניה", "הצד האיטלקי של המטרהורן, שלג מנובמבר עד מאי: שף, ארוחות, שבת, חגים, מניין"),
           ("כשר בקורמאיור", "הצד האיטלקי של המון בלאן, אתר הסקי האיטלקי הקרוב ביותר לליון: שף, ארוחות, שבת, חגים, מניין"),
           ("כשר בקורטינה ד'אמפצו", "הדולומיטים, בחורף ובקיץ: שף, ארוחות, שבת, חגים, מניין"),
           ("סקי כשר, בכל יעד", "אוסטריה, צפון אמריקה או כל אתר שאינו ברשימה שלנו: שף פרטי שנוסע איתכם, שבת, מניין, הסעות")],
}

BTN_HE = """<button class="dk dk-plus dk-plus-recit" type="button" aria-expanded="false" onclick="this.parentElement.classList.add('dk-ouvert');this.remove()">להמשך קריאה</button>"""
ICO_RECIT = '<img class="dk dk-ico dk-ico-recit dk-des" src="/img/ico/or/book-open.svg" alt="" width="96" height="96" loading="lazy">'
MF_HE = ('<!--MANIFESTE--><div class="mf"><p class="mf-phrase">ביום עושים סקי. בערב חוזרים לשולחן ערוך, למניין ולשבת מוכנה.</p><div class="mf-col">'
         '<div><b>שף פרטי או ארוחות במשלוח</b><span>המטבח מוכשר, וכל ארוחה בשבוע מסודרת.</span></div>'
         '<div><b>שבת וחגים, הכול מוכן</b><span>חלות, יין, נרות ומניין עם ספר תורה לפי בקשה.</span></div>'
         '<div><b>הצעת מחיר אחת בכתב, באותו יום</b><span>האתר שלכם, התאריכים שלכם, הקבוצה שלכם. איש קשר אחד מההתחלה ועד הסוף.</span></div>'
         '</div></div><!--/MANIFESTE-->')

# (page, langue, opération, arguments). Ordre : texte d'abord, décor ensuite, ordre des zones à la fin.
OPS = []
def R(page, lang, avant, apres): OPS.append(("remplacer", page, lang, avant, apres))
def H(page, lang, marq_en, marq_tr): OPS.append(("habiller", page, lang, marq_en, marq_tr))
def X(page, lang, marq): OPS.append(("retirer", page, lang, marq))
def D(page, lang, marq, apres): OPS.append(("deplacer", page, lang, marq, apres))

# is-lyon-safe-for-jewish-visitors : reste de « The facts, sourced » (retirée de l'EN par _ton_expert.py le 14/10)
P = "is-lyon-safe-for-jewish-visitors"
for l, faits, bon, suite in (("fr", "<h2>Les faits</h2>", "<h2>Bon sens <i>", "<h2>Pour <i>aller plus loin</i>"),
                             ("es", "<h2>Los hechos, <i>con fuentes</i></h2>", "<h2>Sentido común <i>", "<h2>Siga <i>leyendo</i>"),
                             ("he", "<h2>העובדות</h2>", "<h2>שכל ישר <i>", "<h2>להמשך <i>קריאה</i>")):
    X(P, l, faits)
    H(P, l, "<h2>Common sense <i>", bon)
    H(P, l, "<h2>Keep <i>reading</i>", suite)

# kosher-megeve : adresse de 2014 retirée de l'EN (14/10), bloc minyan en dk-note
P = "kosher-megeve"
R(P, "fr", "<p>L’information date de 2014 : confirmez l’adresse pour vos dates.</p>", "")
R(P, "es", "<p>En las fuentes aparecen dos lugares: 136 route Edmond de Rothschild, 74120 Megève, o una sala llamada «Maison de la Montagne». Como se publicó en 2014, confirme la dirección para sus fechas.</p>", "")
R(P, "he", '<p>136 route Edmond de Rothschild, 74120 Megève, או חדר בשם "Maison de la Montagne". הפרסום הוא מ-2014, ולכן אשרו את הכתובת לתאריכים שלכם.</p>', "")
for l, m in (("fr", "<h2>Minyan et Shabbat <i>à Megève"), ("es", "<h2>Minián y Shabat <i>en Megève"), ("he", "<h2>מניין ושבת <i>במג'ב")):
    H(P, l, "<h2>Minyan and Shabbat <i>in Megève", m)
R(P, "es", " No hemos comprobado que funcione esta temporada ni quién lo supervisa.", "")
R(P, "es", "\n<li><b>Un programa de Kosher Winter Sports.</b>No la hemos comprobado.</li>", "")
H(P, "es", "Kosher <i>in Megève</i></h2>", "Kosher <i>en Megève</i></h2>")

# kosher-les-deux-alpes : « Safe, by design » remis à sa place (après le bloc Shabbat), sans le reliquat de reportage
P = "kosher-les-deux-alpes"
R(P, "fr", "<p>Le même reportage cite des familles qui disent se sentir bien accueillies.</p>\n", "")
R(P, "fr", "en station comme à Lyon.<a ", "en station comme à Lyon. Notre standard est décrit sur la page <a ")
R(P, "es", "<p>El mismo reportaje recoge a familias que dicen sentirse bienvenidas.</p>\n", "")
for l, m in (("fr", "<h2>La sécurité, <i>pensée dès le départ</i>"), ("es", "<h2>Seguridad, <i>por diseño</i>")):
    H(P, l, "<h2>Safe, <i>by design</i>", m)
    D(P, l, m, '<section class="clair clair-2 ss wrap shabbat-bloc"')
R(P, "he", "<li><b>מלונות שלמים.</b> אף מלון ואף תוכנית אינם מוזכרים בשמם ללה דז אלפ.</li>",
  "<li><b>עונת קיץ כשרה.</b> משפחות יהודיות אורתודוקסיות מגיעות ללה דז אלפ בקיץ כבר עשרות שנים, וסמינר של בית ליובאוויטש, של כמה מאות משתתפים במשך שלושה שבועות, עובר בין אתרי האלפים.</li>\n"
  "<li><b>מלונות שלמים.</b> ארגונים כשרים שוכרים לעיתים קרובות מלונות שלמים באתרי האלפים לקיץ. אף מלון ואף תוכנית אינם מוזכרים בשמם בלה דז אלפ.</li>")
H(P, "he", "Kosher <i>in Les Deux Alpes</i></h2>", "כשר <i>בלה דז אלפ</i></h2>")

# kosher-annecy : la synagogue manquait, reliquats d'article retirés (ES)
P = "kosher-annecy"
R(P, "fr", "<li><b>Commerce ou restaurant casher.</b>", "<li><b>Une synagogue.</b> 18 rue de Narvik, 74000 Annecy.</li>\n<li><b>Commerce ou restaurant casher.</b>")
R(P, "es", "<li><b>Tienda o restaurante kosher.</b>", "<li><b>Una sinagoga.</b> 18 rue de Narvik, 74000 Annecy.</li>\n<li><b>Tienda o restaurante kosher.</b>")
R(P, "es", " El mismo artículo afirma que Annecy no tiene ninguna tienda ni ningún restaurante kosher, y que los residentes compran la comida kosher en ciudades cercanas.", "")
R(P, "es", " El artículo la sitúa en unas 50 familias.", "")
H(P, "fr", "Kosher <i>in Annecy</i></h2>", "Casher <i>à Annecy</i></h2>")
H(P, "es", "Kosher <i>in Annecy</i></h2>", "Kosher <i>en Annecy</i></h2>")

# kosher-alpe-dhuez (HE) : l'été 2026 manquait
P = "kosher-alpe-dhuez"
R(P, "he", "וכ-1% כיום.</li>", 'וכ-1% כיום.</li>\n<li><b>קיץ 2026.</b> המארגן <span dir="ltr">Niphla Events</span> אירח 250 אורחים באוגוסט 2026 במקום ששכר באלפ ד\'ואז.</li>')
H(P, "he", "Kosher <i>in Alpe d'Huez</i></h2>", "כשר <i>באלפ ד'ואז</i></h2>")

# kosher-courmayeur : « Saison » retirée de l'EN, « None found » manquait (ES, HE), titre ES aligné
P = "kosher-courmayeur"
R(P, "fr", "\n<li><b>Saison.</b> Vérifiez avant de prendre un forfait.</li>", "")
R(P, "es", "\n<li><b>Temporada.</b> Compruébelas antes de comprar un forfait.</li>", "")
R(P, "he", '\n<li><b>עונה.</b> תאריכי הפתיחה של המעליות ושל ה-<span dir="ltr">Skyway</span></li>', "")
R(P, "es", "<h2>Kosher en Courmayeur: <i>lo que encontramos</i></h2>", "<h2>Kosher en Courmayeur</h2>")
R(P, "es", "en Courmayeur.</b> Los listados", "en Courmayeur.</b> No hemos encontrado ninguno. Los listados")
R(P, "es", "valle de Aosta.</b> La presencia", "valle de Aosta.</b> Ninguna en Courmayeur ni en Aosta. La presencia")
R(P, "he", "כשרים בקורמאיור.</b> רשימות", "כשרים בקורמאיור.</b> לא מצאנו. רשימות")
R(P, "he", "בעמק אאוסטה.</b> הנוכחות", "בעמק אאוסטה.</b> לא מצאנו בקורמאיור ולא באאוסטה. הנוכחות")
for l, m in (("fr", "Casher à Courmayeur</h2>"), ("es", "Kosher en Courmayeur</h2>"), ("he", "כשר בקורמאיור</h2>")):
    H(P, l, "Kosher in Courmayeur</h2>", m)

# kosher-zermatt (FR) : « aucun trouvé » et « Hôtes juifs » retirés de l'EN
P = "kosher-zermatt"
R(P, "fr", "à Zermatt.</b> Nous n’en avons trouvé aucun. Prévoyez", "à Zermatt.</b> Prévoyez")
R(P, "fr", "au village.</b> Nous n’en avons trouvé aucun à Zermatt. Les centres", "au village.</b> Les centres")
R(P, "fr", "\n<li><b>Hôtes juifs à Zermatt.</b> C’est pourquoi un minyan s’y constitue semaine après semaine.</li>", "")
H(P, "fr", "Kosher in Zermatt</h2>", "Casher à Zermatt</h2>")

# summer-in-the-alps-jewish-families : puce « aucun nommé » retirée de l'EN ; HE : phrase manquante, Chamonix au lexique
P = "summer-in-the-alps-jewish-families"
R(P, "es", "<li><b>Hoteles o centros kosher de verano en los Alpes.</b> No nombramos ninguno.</li>", "")
R(P, "he", "<li><b>מלונות או מרכזים כשרים לקיץ באלפים.</b> איננו מציינים אף אחד.</li>", "")
R(P, "he", "ומג'ב (Megève).</b>כתבו להרב", "ומג'ב (Megève).</b> שום דבר לא מעיד שהם פועלים בקיץ. כתבו להרב")
R(P, "he", "<b>שאמוני (Chamonix).</b>", "<b>שמוני (Chamonix).</b>")
H(P, "es", "High resorts in summer</h2>", "Estaciones de altura en verano</h2>")
H(P, "he", "High resorts in summer</h2>", "אתרי הרים גבוהים בקיץ</h2>")

# phrases manquantes en hébreu (contrôle LONGUEUR)
R("kosher-les-arcs", "he", "<b>מלון כשר עונתי בארק 2000.</b>עונת", "<b>מלון כשר עונתי בארק 2000.</b> האתר שלו מציין משגיח במשרה מלאה והשגחה של רב מפריז. עונת")
R("kosher-val-disere", "he", "<b>אתר סקי אחד עם טין.</b> הנקודה", "<b>אתר סקי אחד עם טין.</b> תחום הסקי טין-ואל דיזר, לשעבר אספאס קילי (Espace Killy), מציע 300 ק״מ של מסלולים. הנקודה")
R("kosher-ski-holidays-french-alps", "he", "<p>בקשו את התעודה.</p>",
  "<p>שפים פרטיים מפרסמים בישול 'גלאט כשר' במג'ב, בשמוני ובקורשבל. ההשגחה שלהם אינה מצוינת באתרים שלהם, ולכן איננו מציגים אותם כמלונות כשרים. בקשו את התעודה.</p>")
R("kosher-vacation-french-alps", "he", "<div><p>את זה Mishpacha Tours מארגנת",
  "<div><p>אתם רוצים נופש כשר בחו״ל בלי מלון כשר: צ'אלה או דירה משלכם, באתר סקי אמיתי בחורף או ליד אגם בקיץ, והוודאות שהאוכל, השבת והתפילה מסודרים. את זה Mishpacha Tours מארגנת")
R("kosher-vacation-french-alps", "he", "הצוות הכשר שלנו שבסיסו באלפים. אתם שולחים", "הצוות הכשר שלנו נמצא באלפים. אתם שולחים")
R("kosher-chalet-les-deux-alpes", "he", '<img class="lead-mascotte" src="/img/picto-hassid-vert.svg" alt="" width="797" height="806" loading="lazy"><div></div></section>',
  '<img class="lead-mascotte" src="/img/picto-hassid-vert.svg" alt="" width="797" height="806" loading="lazy"><div>' + MF_HE +
  "<p>שישה חדרי שינה ו-16 מיטות, לשלוש משפחות קטנות או למשפחה אחת גדולה. שף פרטי מבשל ארוחות כשרות בצ'אלה, או שהארוחות מגיעות במשלוח; שבת וחגים עם מניין וספר תורה, לפי המשפחות הנוכחות. בקשה אחת, הצעת מחיר אחת בכתב.</p></div></section>")

# kosher-pesach-french-alps : deux phrases de l'intro manquaient dans les 3 langues
P = "kosher-pesach-french-alps"
R(P, "fr", "<p>Le séjour est devisé et facturé", "<p>Un programme de Pessah pour votre seule famille ou votre seul groupe, dans un chalet privé des Alpes françaises. Vous comparez un programme de Pessah à l’hôtel et un chalet rien qu’à vous ? Envoyez vos dates : vous recevez un devis écrit. Le séjour est devisé et facturé")
R(P, "es", "<p>La estancia la presupuesta y factura", "<p>Un programa de Pésaj solo para su familia o su grupo, en un chalé privado de los Alpes franceses. ¿Comparan un programa de Pésaj en hotel con un chalé solo para ustedes? Envíen sus fechas: recibirán un presupuesto por escrito. La estancia la presupuesta y factura")
R(P, "es", "¿Compara un programa de Pésaj en hotel con un chalé solo para ustedes? Envíe sus fechas: recibirá un presupuesto",
  "¿Comparan un programa de Pésaj en hotel con un chalé solo para ustedes? Envíen sus fechas: recibirán un presupuesto")   # ustedes partout sur la page
R(P, "he", "<p>השהייה מתומחרת ומחויבת", "<p>תוכנית פסח למשפחה שלכם או לקבוצה שלכם בלבד, בצ'אלה פרטית באלפים הצרפתיים. משווים בין תוכנית פסח במלון לבין צ'אלה משלכם? שלחו את התאריכים ותקבלו הצעת מחיר בכתב. השהייה מתומחרת ומחויבת")

# jewish-history-lyon (HE) : Moyen Âge en récit dépliable comme l'EN, dernière phrase manquante
P = "jewish-history-lyon"
R(P, "he", '<section class="ss wrap conseils"><h2>ימי הביניים, <i>והסוף במאה ה-15</i></h2><p>יהודים',
  '<section class="ss wrap conseils dk-recit"><h2>ימי הביניים, <i>והסוף במאה ה-15</i></h2><p>' + ICO_RECIT + 'יהודים')
R(P, "he", "יהדות ליון</a>.</p><p>הקהילה הזו", "יהדות ליון</a>.</p>" + BTN_HE + "<p>הקהילה הזו")
R(P, "he", "(Trévoux) הסמוכה.</p></section>", "(Trévoux) הסמוכה.</p><p>על התוצאה כולם מסכימים: במשך כשלוש מאות שנה לא מתועדת שום קהילה יהודית בליון.</p></section>")

# jewish-lyon-guide : les 10 cartes Suisse, Italie et « ailleurs » manquaient ; HE : sous-titres de 5 cartes
OPS.append(("cartes", "jewish-lyon-guide"))
for slug, nom in (("kosher-val-thorens", "בואל טורנס"), ("kosher-courchevel", "בקורשבל"), ("kosher-megeve", "במג'ב"),
                  ("kosher-alpe-dhuez", "באלפ ד'ואז"), ("kosher-les-deux-alpes", "בלה דז אלפ")):
    R("jewish-lyon-guide", "he", f'<h3>כשר {nom}</h3><span class="btn-noir">',
      f'<h3>כשר {nom}</h3><p>שף, ארוחות, שבת, חגים, מניין {nom}: מה אנחנו מסדרים</p><span class="btn-noir">')


def zones(lang, page, s, en):
    for op in OPS:
        if op[1] != page or (op[0] != "cartes" and op[2] != lang): continue
        if op[0] == "remplacer":
            avant, apres = op[3], op[4]
            texte = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>|<[^>]*$", "", x)).strip()
            t_s, t_av, t_ap = texte(s), texte(avant), texte(apres)
            fait = bool(t_ap) and t_av in t_ap and t_ap in t_s   # insertion déjà faite (le décor a pu changer depuis)
            if avant in s and not fait: s = s.replace(avant, apres, 1)
            elif fait or (apres and t_ap in t_s): pass
            elif apres:
                MANQUES.append(f"{lang}/{page} : introuvable « {avant[:70]} »")
            elif not apres and SEC:
                MANQUES.append(f"{lang}/{page} : à retirer, absent (déjà fait ?) « {avant[:70]} »")
        elif op[0] == "retirer":
            b = bloc(s, op[3])
            if b: s = s[:b[0]] + s[b[1]:]
        elif op[0] == "habiller":
            be, bt = bloc(en, op[3]), bloc(s, op[4])
            if not be or not bt:
                MANQUES.append(f"{lang}/{page} : zone introuvable {op[3][:40]!r} / {op[4][:40]!r}"); continue
            try:
                n = habiller(en[be[0]:be[1]], s[bt[0]:bt[1]])
            except ValueError as e:
                MANQUES.append(f"{lang}/{page} {op[4][:40]!r} : {e}"); continue
            s = s[:bt[0]] + n + s[bt[1]:]
        elif op[0] == "deplacer":
            b = bloc(s, op[3]); a = bloc(s, op[4])
            if not b or not a:
                MANQUES.append(f"{lang}/{page} : déplacement impossible {op[3][:40]!r}"); continue
            if b[0] >= a[1] and re.match(r"\s*$", s[a[1]:b[0]]): continue   # déjà juste après
            morceau = s[b[0]:b[1]]
            s = s[:b[0]] + s[b[1]:]
            a = bloc(s, op[4])
            s = s[:a[1]] + morceau + s[a[1]:]
        elif op[0] == "cartes":
            if f'href="/{lang}/kosher-zermatt/"' in s and 'class="hub-carte" href="/%s/kosher-zermatt/"' % lang in s: continue
            m = re.search(r'<a class="hub-carte" href="/%s/kosher-val-disere/">.*?</a>' % lang, s)
            if not m: MANQUES.append(f"{lang}/{page} : carte Val d'Isère introuvable"); continue
            ajout = "".join(carte(lang, slug, t, x) for slug, (t, x) in zip(SUISSE_ITALIE, CARTES[lang]))
            s = s[:m.end()] + ajout + s[m.end():]
    return s


def main():
    en_set = pages_en()
    pages_ops = {op[1] for op in OPS}
    modifiees, contenu = [], []
    for lang in LANGS:
        for page in sorted(en_set):
            p = chemin(lang, page)
            if not os.path.exists(p): continue
            s0 = rd(p)
            s = liens(s0, lang, page, en_set)
            s = baseline(s, lang)
            if page in pages_ops:
                s1 = s
                s = zones(lang, page, s, rd(chemin("en", page)))
                if s != s1: contenu.append(f"{lang}/{page}" if page else lang)
            if s != s0:
                modifiees.append(p)
                if not SEC: wr(p, s)
    print(len(modifiees), "pages modifiées" + (" (essai, rien d'écrit)" if SEC else ""))
    print("zones modifiées :", " ".join(contenu) or "aucune")
    for m in MANQUES: print("MANQUE", m)


if __name__ == "__main__":
    main()
