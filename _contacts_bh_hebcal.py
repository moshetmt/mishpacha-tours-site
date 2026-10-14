# -*- coding: utf-8 -*-
"""Contacts, Beth Habad, Hebcal : post-traitement idempotent des sorties HTML des 4 langues (ordres operateur du 14/10).
  python _contacts_bh_hebcal.py   : apres les builds et _zones.py, AVANT _decor.py (relancer _decor.py ensuite). Peut tourner deux fois.
1. Aucun numero de telephone dans le texte visible ni dans les meta (le JSON-LD n'est pas touche). Les liens wa.me / tel: gardent leur href.
2. Bloc « Minyan » (+ « repas livres ») vers le WhatsApp du Beth Habad (33781823193) sur les pages Alpes ; tout le reste du WhatsApp = operateur.
3. Plus de Grenoble sur les pages Deux Alpes (reseau Chabad « cote Grenoble », parquet de Grenoble).
4. Plus de renvoi vers Hebcal dans le texte visible : encadre d'horaires de Shabbat affiche en direct (API JSON Hebcal, geonameid par station).
Les pages ne sont pas regenerees : les sources _pages/*.py et _gabarit.html portent encore l'ancien texte, donc ce script doit passer apres tout build.
"""
import glob, io, os, re, urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
LANGS = ("fr", "es", "he")
WA_BH = "33781823193"

# ---------------------------------------------------------------- 1. numeros
NUM = r"\+33 6 52 09 23 01"
OUVRIR = {"en": "Open the chat", "fr": "Ouvrir la conversation", "es": "Abrir el chat", "he": "פתחו שיחה"}
N3 = r"0[1-9](?: \d\d){4}"  # numeros francais de tiers (restaurants, delegues, Beth Din, memoriaux)


def sans_numeros(h, lang):
    def seg(t):
        t = re.sub(r"(WhatsApp|וואטסאפ)(?:[\s‎‏\xa0]|&nbsp;)*" + NUM, r"\1", t, flags=re.I)
        t = re.sub(r">" + NUM + "</a>", ">" + OUVRIR[lang] + "</a>", t)
        t = re.sub(r"[‎‏]?" + NUM, "WhatsApp", t)
        # Beth Habad de Grenoble (page ski) : le numero et « appelez les deux »
        t = re.sub(r"(habadgrenoblealpes\.com)\.[^<]*?04 85 02 84 47[^<]*(</small>)", r"\1\2", t)
        # numeros de tiers
        t = re.sub(r",\s*" + N3 + r"\)", ")", t)
        t = re.sub(r"\s*\(" + N3 + r"\)", "", t)
        t = re.sub(r",\s*" + N3 + r"(?=[,<.])", "", t)
        t = re.sub(r"\s*:\s+" + N3 + r"(?=\.)", "", t)
        t = re.sub(r"\s+(?:on|en el|al|au)\s+" + N3, "", t)
        t = re.sub(r"\s+ב-" + N3, "", t)
        t = re.sub(r"(?<=[֐-׿])\s+" + N3, "", t)
        return t
    return segments(h, seg)


def segments(h, f):
    """Applique f aux parties hors <script> (JSON-LD et JS intacts)."""
    p = re.split(r"(<script\b.*?</script>)", h, flags=re.S)
    return "".join(x if i % 2 else f(x) for i, x in enumerate(p))


# ---------------------------------------------------------------- 3. Grenoble (pages Deux Alpes)
GRENOBLE = [
    ("the Chabad network of the Alps on the Grenoble side", "the Beth Habad of the Alps"),
    ("the Grenoble prosecutor's office", "the prosecutor's office"),
    ("le réseau Chabad des Alpes, côté Grenoble", "le Beth Habad des Alpes"),
    ("au parquet de Grenoble", "au parquet"),
    ("la red Chabad de los Alpes en el lado de Grenoble", "el Beth Habad de los Alpes"),
    ("a la fiscalía de Grenoble", "a la fiscalía"),
    ("רשת חב״ד באלפים בצד גרנובל", "בית חב״ד באלפים"),
    ("לפרקליטות גרנובל", "לפרקליטות"),
]


def sans_grenoble(h):
    return segments(h, lambda t: _rep(t, GRENOBLE))


def _rep(t, table):
    for a, b in table:
        t = t.replace(a, b)
    return t


# ---------------------------------------------------------------- 4. Hebcal
PLACES = {  # slug : (geonameid, {lang: nom})
    "kosher-alpe-dhuez": (3013022, dict(en="Alpe d'Huez", fr="Alpe d’Huez", es="Alpe d'Huez", he="אלפ ד'ואז")),
    "kosher-annecy": (3037543, dict(en="Annecy", fr="Annecy", es="Annecy", he="אנסי")),
    "kosher-chalet-les-deux-alpes": (6354942, dict(en="Les Deux Alpes", fr="Les Deux Alpes", es="Les Deux Alpes", he="לה דז אלפ")),
    "kosher-chamonix": (3027301, dict(en="Chamonix", fr="Chamonix", es="Chamonix", he="שמוני")),
    "kosher-courchevel": (3023065, dict(en="Courchevel", fr="Courchevel", es="Courchevel", he="קורשבל")),
    "kosher-grenoble": (3014728, dict(en="Grenoble", fr="Grenoble", es="Grenoble", he="גרנובל")),
    "kosher-la-plagne": (2996874, dict(en="La Plagne", fr="La Plagne", es="La Plagne", he="לה פלאן")),
    "kosher-les-arcs": (3030949, dict(en="Les Arcs", fr="Les Arcs", es="Les Arcs", he="לז ארק")),
    "kosher-les-deux-alpes": (6354942, dict(en="Les Deux Alpes", fr="Les Deux Alpes", es="Les Deux Alpes", he="לה דז אלפ")),
    "kosher-megeve": (2994768, dict(en="Megève", fr="Megève", es="Megève", he="מז'ב")),
    "kosher-val-disere": (2971074, dict(en="Val d'Isère", fr="Val d’Isère", es="Val d'Isère", he="ואל דיזר")),
    "kosher-val-thorens": (6544556, dict(en="Val Thorens", fr="Val Thorens", es="Val Thorens", he="ואל טורנס")),
    # pages multi-stations : Albertville, au centre des Alpes
    "kosher-ski-holidays-french-alps": (3038266, dict(en="the Alps", fr="les Alpes", es="los Alpes", he="האלפים")),
    "summer-in-the-alps-jewish-families": (3038266, dict(en="the Alps", fr="les Alpes", es="los Alpes", he="האלפים")),
}
MULTI = {"kosher-ski-holidays-french-alps", "summer-in-the-alps-jewish-families"}
LYON = {"shabbat-in-lyon", "synagogues-lyon", "jewish-lyon-guide"}
LYON_GID = 2996944
TITRE = {"en": "Shabbat in {} this week", "fr": "Shabbat cette semaine : {}", "es": "Shabat esta semana: {}", "he": "שבת השבוע: {}"}
REPLI = {"en": "Candle lighting falls as early as 16:30 in December and after 21:00 in June.",
         "fr": "L’allumage des bougies tombe dès 16:30 en décembre et après 21:00 en juin.",
         "es": "El encendido de velas cae hacia las 16:30 en diciembre y después de las 21:00 en junio.",
         "he": "הדלקת הנרות חלה כבר ב-16:30 בדצמבר, ואחרי 21:00 ביוני."}
NOTE = {"en": "Times for Albertville, in the heart of the Alps. Your resort can differ by a few minutes.",
        "fr": "Horaires d’Albertville, au cœur des Alpes. Votre station peut différer de quelques minutes.",
        "es": "Horarios de Albertville, en el corazón de los Alpes. Su estación puede diferir en unos minutos.",
        "he": "הזמנים לאלברטוויל, בלב האלפים. באתר שלכם הם עשויים להיות שונים בכמה דקות."}
JS = {"en": ("en-GB", "Candle lighting: ", "Havdalah: "), "fr": ("fr-FR", "Allumage des bougies : ", "Havdala : "),
      "es": ("es-ES", "Encendido de velas: ", "Havdalá: "), "he": ("he-IL", "הדלקת נרות: ", "הבדלה: ")}

# phrases mixtes a recoudre a la main (le reste des phrases « Hebcal » est supprime)
SPECIAL = [
    # page ski : on garde la consigne « demandez les horaires des offices »
    (r"Look it up for your resort with Hebcal, and ask your Chabad", "Ask your Chabad", True),
    (r"Consultez-le pour votre station avec Hebcal, et demandez les horaires des offices", "Demandez les horaires des offices", True),
    (r"Consúltela para su estación con Hebcal y pida a su contacto de Chabad", "Pida a su contacto de Chabad", True),
    (r"בדקו אותו לאתר שלכם ב-Hebcal, ושאלו את איש הקשר", "שאלו את איש הקשר", True),
    # shabbat-in-lyon
    (r", from Hebcal for Lyon", " for Lyon", False), (r", from Hebcal\.", ".", False),
    (r", d’après Hebcal pour Lyon", " pour Lyon", False), (r", d’après Hebcal\.", ".", False),
    (r", según Hebcal para Lyon", " para Lyon", False), (r", según Hebcal\.", ".", False),
    (r", מתוך Hebcal עבור ליון", " עבור ליון", False), (r", מתוך Hebcal\.", ".", False),
    (r",\s*hebcal\.com", "", False),  # liste de sources
]


def script_shabbat(lang, gid, multi):
    loc, c, hv = JS[lang]
    note = '+"<br><small>' + NOTE[lang] + '</small>"' if multi else ""
    return ('<script data-shabbat>\nfetch("https://www.hebcal.com/shabbat?cfg=json&geonameid=%d&M=on&lg=%s").then(r=>r.json()).then(d=>{'
            'const it=d.items;const c=it.find(i=>i.category==="candles"),h=it.find(i=>i.category==="havdalah"),p=it.find(i=>i.category==="parashat");'
            'if(!c&&!h)return;'
            'const f=s=>new Date(s).toLocaleTimeString("%s",{hour:"2-digit",minute:"2-digit",timeZone:"Europe/Paris"});'
            'const dd=s=>new Date(s).toLocaleDateString("%s",{weekday:"long",day:"numeric",month:"long",timeZone:"Europe/Paris"});'
            'document.querySelector("#shabbat .shabbat-corps").innerHTML=(p?"<b>"+p.title+"</b><br>":"")'
            '+(c?"%s<b>"+f(c.date)+"</b>, "+dd(c.date)+"<br>":"")+(h?"%s<b>"+f(h.date)+"</b>, "+dd(h.date):"")%s'
            '}).catch(()=>{});\n</script>') % (gid, lang, loc, loc, c, hv, note)


def fin_section(h, idx):
    """Fin de la section de premier niveau qui contient la position idx."""
    ops = list(re.finditer(r'<section class="ss [^"]*">|<div class="ss beige[^"]*">', h[:idx]))
    if not ops:
        return idx
    o = ops[-1]
    tag = "section" if o.group(0).startswith("<section") else "div"
    depth, pos = 0, o.start()
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), h[pos:]):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return pos + m.end()
    return idx


BLOC = re.compile(r"<(p|li)(\s[^>]*)?>(.*?)</\1>", re.S)


def vide(s):
    s = re.sub(r'<img class="dk[^>]*>|<svg class="dk.*?</svg>|<button class="dk.*?</button>', "", s, flags=re.S)
    return not re.sub(r"<[^>]+>|\s|&nbsp;", "", s)


def sans_hebcal(h, slug):
    """Supprime toute phrase de paragraphe ou de puce qui renvoie vers Hebcal. Rend (html, position apres le premier bloc touche)."""
    ancre = [None]
    for rx, b, ancrer in SPECIAL:
        h2 = re.sub(rx, b, h)
        if ancrer and h2 != h:
            m = re.search(re.escape(b), h2)
            ancre[0] = m.end() if m else None
        h = h2
    out, last = [], 0
    for m in BLOC.finditer(h):
        inner = m.group(3)
        if "hebcal" not in inner.lower():
            continue
        parts = re.split(r"((?<=\.)\s+(?![^<]*>)|(?<=</b>)\s+)", inner)
        ph, seps = parts[0::2], parts[1::2]
        keep = [i for i, t in enumerate(ph) if "hebcal" not in t.lower()]
        new = ""
        for n, i in enumerate(keep):
            new += (seps[i - 1] if n and i > 0 and i - 1 < len(seps) and keep[n - 1] == i - 1 else (" " if n else "")) + ph[i]
        out.append(h[last:m.start()])
        out.append("" if vide(new) else "<%s%s>%s</%s>" % (m.group(1), m.group(2) or "", new.strip(), m.group(1)))
        last = m.end()
        if ancre[0] is None:
            ancre[0] = sum(len(x) for x in out)
    out.append(h[last:])
    return "".join(out), ancre[0]


def encadre(h, lang, slug, ancre):
    if slug in LYON:
        gid, multi = LYON_GID, False
    elif slug in PLACES:
        gid, multi = PLACES[slug][0], slug in MULTI
    else:
        return h
    rx = re.compile(r'<script[^>]*>\s*fetch\("https://www\.hebcal\.com/shabbat\?cfg=json.*?</script>', re.S)
    sc = script_shabbat(lang, gid, multi)
    if 'id="shabbat"' in h:
        return rx.sub(lambda m: sc, h)
    nom = PLACES[slug][1][lang]
    corps = REPLI[lang] + (" " + NOTE[lang] if multi else "")
    bloc = ('<section class="ss wrap shabbat-bloc"><div class="shabbat" id="shabbat"><p class="shabbat-titre">%s</p>'
            '<p class="shabbat-corps">%s</p></div>\n%s</section>\n') % (TITRE[lang].format(nom), corps, sc)
    if ancre:
        i = fin_section(h, ancre)
        return h[:i] + "\n" + bloc + h[i:]
    i = h.index('<section class="ss wrap faq">')
    return h[:i] + bloc + h[i:]


# ---------------------------------------------------------------- 2. Beth Habad : minyan public et repas livres
MINYAN = {
    "en": dict(h2="A minyan in the <i>resort</i>", p="Shabbat and weekday prayers with the Beth Habad of the Alps: tell them your dates.",
               b="Minyan: WhatsApp the Beth Habad", h3="Kosher meals delivered",
               p2="Kosher meals brought to your accommodation in the resort, ordered through the Beth Habad of the Alps. Give them your dates and the number of people.",
               b2="Kosher meals delivered: WhatsApp the Beth Habad",
               m="Hello, we would like to join a minyan in the Alps. Resort: {} / Dates: / Number of people:",
               m2="Hello, we are in the Alps and would like kosher meals delivered. Resort: {} / Dates: / Number of people:"),
    "fr": dict(h2="Un minyan en <i>station</i>", p="Prières de Shabbat et de semaine avec le Beth Habad des Alpes : indiquez-leur vos dates.",
               b="Minyan : écrire au Beth Habad sur WhatsApp", h3="Repas casher livrés",
               p2="Des repas casher livrés à votre hébergement en station, commandés auprès du Beth Habad des Alpes. Indiquez-leur vos dates et le nombre de personnes.",
               b2="Repas casher livrés : écrire au Beth Habad sur WhatsApp",
               m="Bonjour, nous aimerions participer à un minyan dans les Alpes. Station : {} / Dates : / Nombre de personnes :",
               m2="Bonjour, nous sommes dans les Alpes et aimerions des repas casher livrés. Station : {} / Dates : / Nombre de personnes :"),
    "es": dict(h2="Un minián en la <i>estación</i>", p="Oraciones de Shabat y de entre semana con el Beth Habad de los Alpes: indíqueles sus fechas.",
               b="Minián: escribir al Beth Habad por WhatsApp", h3="Comidas kosher a domicilio",
               p2="Comidas kosher entregadas en su alojamiento en la estación, encargadas al Beth Habad de los Alpes. Indíqueles sus fechas y el número de personas.",
               b2="Comidas kosher a domicilio: escribir al Beth Habad por WhatsApp",
               m="Hola, nos gustaría participar en un minián en los Alpes. Estación: {} / Fechas: / Número de personas:",
               m2="Hola, estamos en los Alpes y nos gustaría que nos entregaran comidas kosher. Estación: {} / Fechas: / Número de personas:"),
    "he": dict(h2="מניין <i>באתר</i>", p="תפילות שבת וימי חול עם בית חב״ד באלפים: מסרו להם את התאריכים.",
               b="מניין: כתבו לבית חב״ד בוואטסאפ", h3="ארוחות כשרות במשלוח",
               p2="ארוחות כשרות מגיעות אל מקום הלינה שלכם באתר, בהזמנה דרך בית חב״ד באלפים. מסרו להם את התאריכים ואת מספר האנשים.",
               b2="ארוחות כשרות במשלוח: כתבו לבית חב״ד בוואטסאפ",
               m="שלום, נשמח להצטרף למניין באלפים. אתר: {} / תאריכים: / מספר אנשים:",
               m2="שלום, אנחנו באלפים ונשמח לקבל ארוחות כשרות במשלוח. אתר: {} / תאריכים: / מספר אנשים:"),
}
PAGES_BH = {"alps", "kosher-services-french-alps", "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps",
            "lyon-gateway-to-the-alps-kosher", "summer-in-the-alps-jewish-families", "kosher-chalet-les-deux-alpes"} | {
    s for s in PLACES if s not in MULTI}
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg>'


def bloc_minyan(h, lang, slug):
    if 'class="ss wrap minyan-bh"' in h:
        return h
    t = MINYAN[lang]
    lieu = PLACES[slug][1][lang] if slug in PLACES and slug not in MULTI else ""
    url = lambda m: "https://wa.me/%s?text=%s" % (WA_BH, urllib.parse.quote(m.format(lieu).replace(" Station : / ", " ").replace(" Resort: / ", " ")
                                                                           if not lieu else m.format(lieu), safe=""))
    btn = lambda href, txt: '<p class="cta-hero cta-bh"><a class="btn-noir" href="%s" rel="noopener">%s%s</a></p>' % (href, WA_SVG, txt)
    meals = slug != "kosher-services-french-alps"  # la page services a deja son bouton repas vers le Beth Habad
    b = ('<section class="ss wrap minyan-bh"><div class="minyan-corps"><h2>%s</h2><p>%s</p>%s'
         % (t["h2"], t["p"], btn(url(t["m"]), t["b"])))
    if meals:
        b += '<h3>%s</h3><p>%s</p>%s' % (t["h3"], t["p2"], btn(url(t["m2"]), t["b2"]))
    b += "</div></section>\n"
    i = h.index('<section class="ss wrap faq">')
    return h[:i] + b + h[i:]


# ---------------------------------------------------------------- orchestration
def traiter(path):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    slug = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    h0 = io.open(p, encoding="utf-8").read()
    h = sans_numeros(h0, lang)
    if slug in ("kosher-les-deux-alpes", "kosher-chalet-les-deux-alpes"):
        h = sans_grenoble(h)
    if slug != "privacy":
        h, ancre = sans_hebcal(h, slug)
        if slug in PLACES or slug in LYON:
            h = encadre(h, lang, slug, ancre)
    if slug in PAGES_BH:
        h = bloc_minyan(h, lang, slug)
    if h != h0:
        io.open(p, "w", encoding="utf-8", newline="\n").write(h)
        return 1
    return 0


if __name__ == "__main__":
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    n = sum(traiter(p) for p in pages)
    t = io.open("llms.txt", encoding="utf-8").read()
    t2 = re.sub(r"WhatsApp\s*" + NUM, "WhatsApp", t)
    if t2 != t:
        io.open("llms.txt", "w", encoding="utf-8", newline="\n").write(t2)
        n += 1
    print(n, "fichiers modifies sur", len(pages) + 1)
