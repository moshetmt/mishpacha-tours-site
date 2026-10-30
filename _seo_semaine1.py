# -*- coding: utf-8 -*-
"""SEO semaine 1 (comité du 30/10, décisions de Moshé du 30/10), 4 langues, idempotent. À relancer après toute régénération
des pages touchées (python _seo_semaine1.py depuis site-v5/, puis python _agentic.py pour les index.md).

1. Pessah : « 2027 » dans le title, le H1 et la meta ; question « Quand tombe Pessah 2027 ? » (dates Hebcal : premier seder le
   mercredi 21/04/2027 au soir, fête du jeudi 22 au jeudi 29/04/2027, 8 jours en diaspora) ; « Pesach programme » et « Passover
   programme » dans le corps EN. Aucune période de séjour, aucun inclus, aucun Offer, aucun prix de Pessah (NO-GO du comité).
2. Prix « à partir de » (grille de Mendel des 28-29/10, décision de Moshé du 30/10, basse saison, sans hausse) : bloc des prix de la
   page services (repas 78 et 28 €, seouda 30 €, livraison 180 à 360 €, cachérisation 680 €, chef 1 568 €/jour, chalets), FAQ prix
   des 5 pages chalet, cartes chalet de tout le site, FAQ du hub des chalets. Offers « minPrice » dans le JSON-LD Service des chalets.
3. Titles FR : /fr/rue-juiverie-lyon/ et /fr/mikveh-lyon/ (graphies « mikvé » et « mikve »).
4. JSON-LD de l'entité sur /about/ : sameAs vers la fiche Google (déjà sur l'accueil).
5. Rôle d'apporteur, phrase déjà en ligne sur /alps/ : « The stay is quoted and invoiced by our kosher team based in the Alps. »
   sur Pessah, services, hub et pages chalet.
Le FAQPage des pages touchées est reconstruit depuis la FAQ visible de la page (même texte, même langue).
Ne pas lancer « _build_i18n.py ld » sur ces pages : il remet le JSON-LD traduit en anglais (constaté le 30/10)."""
import html, io, json, re, sys

DATE = "2026-10-30"
LANGS = ("", "fr", "es", "he")
B = lambda s: f'<bdi dir="ltr">{s}</bdi>'

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def chemin(l, slug): return (l + "/" if l else "") + slug + "/index.html"
def pfx(l): return "/" + l if l else ""
def plat(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

ROLE = {"": "The stay is quoted and invoiced by our kosher team based in the Alps.",
        "fr": "Le séjour est devisé et facturé par notre équipe casher basée dans les Alpes.",
        "es": "La estancia la presupuesta y factura nuestro equipo kosher con base en los Alpes.",
        "he": "השהייה מתומחרת ומחויבת על ידי הצוות הכשר שלנו שבסיסו באלפים."}

# ---------- JSON-LD ----------
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

def faq_visible(h):
    m = re.search(r'<section class="[^"]*\bfaq\b[^"]*">(.*?)</section>', h, re.S)
    if not m: return None
    return [(plat(q), plat(a)) for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", m.group(1), re.S)]

def ld(h, fn):
    m = LD.search(h)
    d = json.loads(m.group(2)); liste = d if isinstance(d, list) else [d]
    fn(liste)
    js = json.dumps(d, ensure_ascii=False)
    return h[:m.start(2)] + js + h[m.end(2):]

def ld_commun(h, extra=None):
    """FAQPage = FAQ visible ; dateModified du WebPage ; fonction extra pour le reste."""
    faq = faq_visible(h)
    def fn(liste):
        for b in liste:
            t = b.get("@type")
            if t == "FAQPage" and faq:
                b["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
            if t == "WebPage":
                b["dateModified"] = DATE
        if extra: extra(liste)
    return ld(h, fn)

def remplace(h, old, new, p, obligatoire=True):
    if new in h and old not in h: return h
    if old not in h:
        if obligatoire: raise SystemExit(f"introuvable dans {p} : {old[:90]}")
        return h
    return h.replace(old, new)

# ---------- 1. Pessah ----------
P_TITRE = {"": ("Kosher Pesach in the Alps, in a private chalet", "Kosher Pesach 2027 in the French Alps, in a private chalet"),
           "fr": ("Pessah casher dans les Alpes, en chalet privé", "Pessah 2027 casher dans les Alpes, en chalet privé"),
           "es": ("Pésaj kosher en los Alpes, en un chalé privado", "Pésaj 2027 kosher en los Alpes, en un chalé privado"),
           "he": ("פסח כשר באלפים, בצ'אלה פרטית", "פסח כשר 2027 באלפים, בצ'אלה פרטית")}
P_H1 = {"": ("Kosher Pesach<br><i>in the Alps</i>", "Kosher Pesach 2027<br><i>in the French Alps</i>"),
        "fr": ("Pessah casher<br><i>dans les Alpes</i>", "Pessah 2027 casher<br><i>dans les Alpes</i>"),
        "es": ("Pésaj kosher<br><i>en los Alpes</i>", "Pésaj 2027 kosher<br><i>en los Alpes</i>"),
        "he": ("פסח כשר<br><i>באלפים</i>", "פסח כשר 2027<br><i>באלפים</i>")}
P_DESC = {"": ("Pesach in a private chalet in the French Alps", "Pesach 2027 in a private chalet in the French Alps"),
          "fr": ("Pessah en chalet privé dans les Alpes avec", "Pessah 2027 en chalet privé dans les Alpes avec"),
          "es": ("Pésaj en un chalé privado en los Alpes con", "Pésaj 2027 en un chalé privado en los Alpes con"),
          "he": ("פסח בצ'אלה פרטית באלפים הצרפתיים", "פסח 2027 בצ'אלה פרטית באלפים הצרפתיים")}
P_FAQ = {
 "": ("When is Pesach 2027?",
      "The first seder is on the evening of Wednesday 21 April 2027 (15 Nisan 5787), the second on the evening of Thursday 22 April. "
      "Pesach runs from Thursday 22 to Thursday 29 April 2027: eight days, as kept in the diaspora. Dates from the Hebcal calendar."),
 "fr": ("Quand tombe Pessah 2027 ?",
        "Le premier seder a lieu le mercredi 21 avril 2027 au soir (15 Nissan 5787), le second le jeudi 22 avril au soir. "
        "Pessah dure du jeudi 22 au jeudi 29 avril 2027 : huit jours en diaspora. Dates du calendrier Hebcal."),
 "es": ("¿Cuándo es Pésaj 2027?",
        "El primer séder es el miércoles 21 de abril de 2027 por la noche (15 de Nisán de 5787), el segundo el jueves 22 de abril por la noche. "
        "Pésaj va del jueves 22 al jueves 29 de abril de 2027: ocho días, como en la diáspora. Fechas del calendario Hebcal."),
 "he": ("מתי חל פסח 2027?",
        "ליל הסדר הראשון חל ביום רביעי, 21 באפריל 2027 (ליל ט״ו בניסן תשפ״ז), וליל הסדר השני ביום חמישי, 22 באפריל. "
        "החג נמשך מיום חמישי, 22 באפריל, עד יום חמישי, 29 באפריל 2027: שמונה ימים, כמנהג חו״ל. התאריכים לפי לוח " + B("Hebcal") + "."),
}
P_CORPS_EN = ("A Pesach programme for your family or your group alone, in a private chalet in the French Alps. "
              "Comparing a hotel Passover programme with a chalet of your own? Send your dates: you receive a written quote. ")

def pessah():
    for l in LANGS:
        p = chemin(l, "kosher-pesach-french-alps"); h = rd(p); o = h
        a, n = P_TITRE[l]
        for x, y in ((a, n), (html.escape(a, quote=True), html.escape(n, quote=True)), (a.replace("'", "&#x27;"), n.replace("'", "&#x27;"))):
            h = h.replace(x + " | Mishpacha Tours", y + " | Mishpacha Tours")
        assert n in html.unescape(h), p
        h = remplace(h, *P_H1[l], p)
        a, n = P_DESC[l]
        for x, y in ((a, n), (a.replace("'", "&#x27;"), n.replace("'", "&#x27;"))):
            h = h.replace(x, y)
        assert n in html.unescape(h), p
        q, r = P_FAQ[l]
        h = re.sub(r"(<details><summary>" + re.escape(q) + r"</summary><p>).*?(</p></details>)", lambda m: m.group(1) + r + m.group(2), h, count=1, flags=re.S)
        if f"<summary>{q}</summary>" not in h:
            i = h.find('<section class="clair ss wrap faq">'); j = h.find("</h2>", i) + 5
            assert i > 0, p
            h = h[:j] + f"<details><summary>{q}</summary><p>{r}</p></details>" + h[j:]
        # intro : rôle d'apporteur (4 langues) et, en anglais, « Pesach programme » / « Passover programme »
        if ROLE[l] not in h:
            i = h.find('<section class="clair ss wrap lead-intro">'); j = h.find("</div></section>", i)
            assert i > 0 and j > 0, p
            ajout = (P_CORPS_EN if not l else "") + ROLE[l]
            h = h[:j] + f"<p>{ajout}</p>" + h[j:]
        def extra(liste, l=l):
            for b in liste:
                if b.get("@type") == "WebPage": b["name"] = P_TITRE[l][1]
                if b.get("@type") == "Service" and P_DESC[l][0] in b.get("description", ""):
                    b["description"] = b["description"].replace(P_DESC[l][0], P_DESC[l][1])
                assert b.get("@type") != "Service" or "offers" not in b, "Pessah : jamais d'Offer"
        h = ld_commun(h, extra)
        if h != o: wr(p, h); print("pessah", p)

# ---------- 2. Prix ----------
CHALETS = [  # (slug, clé _kit_wp, prix semaine)
    ("kosher-chalet-val-thorens", "vth", 9500), ("kosher-slope-chalet-les-deux-alpes", "sl", 13000),
    ("kosher-chalet-les-deux-alpes", "da", 13500), ("kosher-chalet-courchevel", "co", 17500), ("kosher-chalet-megeve", "me", 23500)]
NOMS = {  # noms des chalets choisis par Mendel le 30/10 à 1 h 04 (_retouches_30_10.py, commit 44e7df8)
 "": {"vth": "Chalet Belle Étoile, Val Thorens", "sl": "Chalet Rochebrune, Les Deux Alpes", "da": "Chalet King David, Les Deux Alpes", "co": "Chalet Flocon Doré, Courchevel", "me": "Chalet Loup Blanc, near Megève"},
 "fr": {"vth": "Chalet Belle Étoile, Val Thorens", "sl": "Chalet Rochebrune, Les Deux Alpes", "da": "Chalet King David, Les Deux Alpes", "co": "Chalet Flocon Doré, Courchevel", "me": "Chalet Loup Blanc, près de Megève"},
 "es": {"vth": "Chalet Belle Étoile, Val Thorens", "sl": "Chalet Rochebrune, Les Deux Alpes", "da": "Chalet King David, Les Deux Alpes", "co": "Chalet Flocon Doré, Courchevel", "me": "Chalet Loup Blanc, cerca de Megève"},
 "he": {"vth": "צ'אלה בל אטואל, ואל טורנס", "sl": "צ'אלה רושברון, לה דז אלפ", "da": "צ'אלה קינג דייוויד, לה דז אלפ", "co": "צ'אלה פלוקון דורה, קורשבל", "me": "צ'אלה לו בלאן, ליד מג'ב"}}

def eur(l, n):
    if l == "": return f"€{n:,}"
    if l == "fr": return f"{n:,}".replace(",", " ") + " €"
    if l == "es": return f"{n:,}".replace(",", ".") + " €"
    return B(f"{n:,} €")

APARTIR = {"": lambda v: "from " + v, "fr": lambda v: "à partir de " + v, "es": lambda v: "desde " + v, "he": lambda v: "החל מ־" + v}
SEMAINE = {"": "From {} per week", "fr": "À partir de {} la semaine", "es": "Desde {} por semana", "he": "החל מ־{} לשבוע"}

# ---------- prix reliés à la grille (Moshé 30/10 : « si je change un chiffre, ça change sur le site ») ----------
# js/prix.js remplace le texte par le prix coché « Public » dans l'écran Publier de l'Apps Script ; sans prix publié, le texte reste.
# Clés de la grille : ch1 King David, ch2 Rochebrune, ch3 Flocon Doré, ch4 Loup Blanc, ch5 Belle Étoile, c_chef, c_cacher.
CLES = {"da": "ch1_basse_vente", "sl": "ch2_basse_vente", "co": "ch3_basse_vente", "me": "ch4_basse_vente", "vth": "ch5_basse_vente"}
def eur_tpl(l, cle):
    if l == "": return "€{" + cle + "}"
    if l == "he": return B("{" + cle + "} €")
    return "{" + cle + "} €"
def attr(tpl):
    """Valeur d'attribut entre apostrophes (les sources _pages/*.py gardent leurs guillemets)."""
    return tpl.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
def span_tpl(tpl, texte): return f"<span data-prix-tpl='{attr(tpl)}'>{texte}</span>"
def prix_chalet(l, k, n): return span_tpl(APARTIR[l](eur_tpl(l, CLES[k])), APARTIR[l](eur(l, n)))

# libellé de la ligne : (nouvelle valeur, retirer data-prix-tpl)
LIGNES = {
 "": {"Full board: breakfast, lunch and dinner": ("from €78", False), "Dinner only: starter, main course, dessert": ("from €28", False),
      "Seuda shlishit": ("€30", False), "Delivery every two days, any resort in France": ("€180 to €360", True),
      "Kashering the kitchen of the chalet you rent": ("On request", True)},
 "fr": {"Formule complète : matin, midi et soir": ("à partir de 78 €", False), "Soir seul : entrée, plat, dessert": ("à partir de 28 €", False),
        "Seouda chlichit": ("30 €", False), "Livraison tous les deux jours, toute station française": ("180 à 360 €", True),
        "Cachérisation de la cuisine du chalet que vous louez": ("Sur demande", True)},
 "es": {"Pensión completa: desayuno, almuerzo y cena": ("desde 78 €", False), "Solo cena: entrante, plato principal y postre": ("desde 28 €", False),
        "Seudá shlishit": ("30 €", False), "Entrega cada dos días, cualquier estación de Francia": ("de 180 a 360 €", True),
        "Kasherización de la cocina del chalé que alquila": ("Bajo pedido", True)},
 "he": {"פנסיון מלא: בוקר, צהריים וערב": ("החל מ־" + B("78 €"), False), "ערב בלבד: מנה ראשונה, עיקרית וקינוח": ("החל מ־" + B("28 €"), False),
        "סעודה שלישית": (B("30 €"), False), "משלוח כל יומיים, לכל אתר סקי בצרפת": (B("180–360 €"), True),
        "הכשרת המטבח בצ'אלה ששכרתם": ("לפי בקשה", True)},
}
CHEF = {"": ("Private kosher chef in your chalet, per day", "from €1,568"),
        "fr": ("Chef privé casher dans votre chalet, par jour", "à partir de 1 568 €"),
        "es": ("Chef privado kosher en su chalé, por día", "desde 1.568 €"),
        "he": ("שף פרטי כשר בצ'אלה שלכם, ליום", "החל מ־" + B("1,568 €"))}
H2 = {"": ("Delivered meals: <i>the prices</i>", "The prices: <i>meals, chef and chalets</i>"),
      "fr": ("Repas livrés : <i>les prix</i>", "Les prix : <i>repas, chef et chalets</i>"),
      "es": ("Comidas a domicilio: <i>los precios</i>", "Los precios: <i>comidas, chef y chalés</i>"),
      "he": ("ארוחות במשלוח: <i>המחירים</i>", "המחירים: <i>ארוחות, שף וצ'אלות</i>")}
INTRO = {"": ("<p>Per person, per day.", "<p>Meals: per person, per day."), "fr": ("<p>Par personne et par jour.", "<p>Repas : par personne et par jour."),
         "es": ("<p>Por persona y por día.", "<p>Comidas: por persona y por día."), "he": ("<p>לאדם ליום.", "<p>ארוחות: לאדם ליום.")}
CH_TETE = {"": ("A chalet <i>for the week</i>", "Per chalet, per week. Starting prices: the price for your dates comes in writing with your quote."),
           "fr": ("Un chalet <i>pour la semaine</i>", "Par chalet et par semaine. Prix de départ : le prix pour vos dates vous est remis par écrit avec le devis."),
           "es": ("Un chalé <i>para la semana</i>", "Por chalé y por semana. Precios de partida: el precio para sus fechas llega por escrito con el presupuesto."),
           "he": ("צ'אלה <i>לשבוע</i>", "לצ'אלה לשבוע. מחירי פתיחה: המחיר לתאריכים שלכם נשלח בכתב עם הצעת המחיר.")}

def variantes(s):
    """Graphies possibles dans le HTML : telle quelle, espace fine insécable avant : ; ? (page services FR), apostrophe échappée."""
    fine = re.sub(r" ([:;?!])", "\u202f\\1", s)
    insec = re.sub(r" ([:;?!])", "\u00a0\\1", s)
    return [s, fine, insec, s.replace("'", "&#x27;")]

def rv(h, a, n, p):
    """Remplace a par n dans la graphie trouvée (espace insécable ou fine reprise dans n). Idempotent."""
    for va, vn in zip(variantes(a), variantes(n)):
        if vn in h and va not in h: return h
        if va in h: return h.replace(va, vn)
    raise SystemExit(f"introuvable dans {p} : {a[:90]}")

def ligne_val(bloc, label, val, sans_tpl, p):
    m = None
    for v in variantes(label):
        m = re.search(r"(<li[^>]*>(?:<img[^>]*>)?<span>" + re.escape(v) + r"</span>)<b([^>]*)>(.*?)</b>", bloc)
        if m: break
    if not m: raise SystemExit(f"ligne introuvable {p} : {label}")
    # sans_tpl : True = retirer data-prix-tpl, False = garder tel quel, chaîne = poser ce gabarit
    attrs = (" data-prix-tpl='" + attr(sans_tpl) + "'") if isinstance(sans_tpl, str) else ("" if sans_tpl else m.group(2))
    return bloc[:m.start()] + f"{m.group(1)}<b{attrs}>{val}</b>" + bloc[m.end():]

SERV_FAQ = {
 "": [("from €180 to €350 per delivery", "from €180 to €360 per delivery"),
      ("Delivered meals start at €27 per person per day for dinner only and €75 for full board, plus delivery; Shabbat meals cost €35 to €45. A chalet with a private chef is quoted for your group.",
       "Delivered meals start at €28 per person per day for dinner only and €78 for full board, plus delivery; Shabbat meals cost €30 to €45. A private chef starts at €1,568 per day, a chalet at €9,500 per week."),
      ("You deal with one contact from start to finish.</p>", "You deal with one contact from start to finish. " + ROLE[""] + "</p>")],
 "fr": [("de 180 à 350 € la livraison", "de 180 à 360 € la livraison"),
        ("Les repas livrés partent de 27 € par personne et par jour pour le soir seul et de 75 € pour la formule complète, plus la livraison ; les repas de Chabbat coûtent de 35 à 45 €. Un chalet avec chef privé se chiffre pour votre groupe.",
         "Les repas livrés partent de 28 € par personne et par jour pour le soir seul et de 78 € pour la formule complète, plus la livraison ; les repas de Chabbat coûtent de 30 à 45 €. Un chef privé part de 1 568 € par jour, un chalet de 9 500 € la semaine."),
        ("Vous traitez avec un seul interlocuteur du début à la fin.</p>", "Vous traitez avec un seul interlocuteur du début à la fin. " + ROLE["fr"] + "</p>")],
 "es": [("de 180 a 350 € por entrega", "de 180 a 360 € por entrega"),
        ("Las comidas a domicilio parten de 27 € por persona y día para la cena y de 75 € para la pensión completa, más la entrega; las comidas de Shabat cuestan de 35 a 45 €. Un chalé con chef privado se presupuesta para su grupo.",
         "Las comidas a domicilio parten de 28 € por persona y día para la cena y de 78 € para la pensión completa, más la entrega; las comidas de Shabat cuestan de 30 a 45 €. Un chef privado parte de 1.568 € por día y un chalé de 9.500 € por semana."),
        ("Trata con un solo contacto de principio a fin.</p>", "Trata con un solo contacto de principio a fin. " + ROLE["es"] + "</p>")],
 "he": [(B("180–350 €") + " למשלוח", B("180–360 €") + " למשלוח"),
        ("ארוחות במשלוח מתחילות ב־" + B("27 €") + " לאדם ליום לארוחת ערב בלבד וב־" + B("75 €") + " לפנסיון מלא, בתוספת משלוח; ארוחות שבת עולות " + B("35–45 €") + ". צ'אלה עם שף פרטי מתומחרת לפי הקבוצה.",
         "ארוחות במשלוח מתחילות ב־" + B("28 €") + " לאדם ליום לארוחת ערב בלבד וב־" + B("78 €") + " לפנסיון מלא, בתוספת משלוח; ארוחות שבת עולות " + B("30–45 €") + ". מחיר שף פרטי מתחיל ב־" + B("1,568 €") + " ליום, ומחיר צ'אלה ב־" + B("9,500 €") + " לשבוע."),
        ("אתם מתנהלים מול איש קשר אחד מההתחלה ועד הסוף.", "אתם מתנהלים מול איש קשר אחד מההתחלה ועד הסוף. " + ROLE["he"]),
        (". שף פרטי מתחיל ב־" + B("1,568 €") + " ליום, וצ'אלה ב־" + B("9,500 €") + " לשבוע.", ". מחיר שף פרטי מתחיל ב־" + B("1,568 €") + " ליום, ומחיר צ'אלה ב־" + B("9,500 €") + " לשבוע.")],
}
# Montants du chef et du chalet de la FAQ reliés à la grille : la paire part de la phrase finale ci-dessus (même texte), pour que la
# relance du script la retrouve ; HE a aussi la paire sur le fragment de la 4e ligne.
def _tpl(l, s):
    return s.replace(eur(l, 1568), span_tpl(eur_tpl(l, "c_chef_vente"), eur(l, 1568)), 1).replace(eur(l, 9500), span_tpl(eur_tpl(l, "ch5_basse_vente"), eur(l, 9500)), 1)
for _l in LANGS:
    SERV_FAQ[_l].append((SERV_FAQ[_l][1][1], _tpl(_l, SERV_FAQ[_l][1][1])))
SERV_FAQ["he"].append((SERV_FAQ["he"][3][1], _tpl("he", SERV_FAQ["he"][3][1])))

def services():
    for l in LANGS:
        p = chemin(l, "kosher-services-french-alps"); h = rd(p); o = h
        m = re.search(r'(<section[^>]*id="meal-prices"[^>]*>)(.*?)(</section>)', h, re.S)
        assert m, p
        bloc = m.group(2)
        for label, (val, sans) in LIGNES[l].items():
            bloc = ligne_val(bloc, label, val, sans, p)
        for a, b in (H2[l], INTRO[l]):
            for va, vb in zip(variantes(a), variantes(b)):
                bloc = bloc.replace(va, vb)
        if CHEF[l][0] not in bloc:
            i = bloc.find("</ul></div>", bloc.find('<div class="prix-table">'))
            bloc = bloc[:i] + f"<li><span>{CHEF[l][0]}</span><b>{CHEF[l][1]}</b></li>" + bloc[i:]
        bloc = ligne_val(bloc, CHEF[l][0], CHEF[l][1], APARTIR[l](eur_tpl(l, "c_chef_vente")), p)
        bloc = re.sub(r'<h3>[^<]*<i>[^<]*</i></h3><p>[^<]*</p><div class="prix-table prix-chalets">.*?</ul></div>', "", bloc, flags=re.S)
        if "prix-chalets" not in bloc:
            lis = "".join(f'<li><span><a href="{pfx(l)}/{slug}/">{NOMS[l][k]}</a></span><b data-prix-tpl=\'{attr(APARTIR[l](eur_tpl(l, CLES[k])))}\'>{APARTIR[l](eur(l, prix))}</b></li>' for slug, k, prix in CHALETS)
            t, intro = CH_TETE[l]
            i = bloc.find('<p class="note">')
            bloc = bloc[:i] + f'<h3>{t}</h3><p>{intro}</p><div class="prix-table prix-chalets"><ul>{lis}</ul></div>' + bloc[i:]
        h = h[:m.start(2)] + bloc + h[m.end(2):]
        for a, b in SERV_FAQ[l]:  # paires dans l'ordre ; une paire dont ni l'ancien ni le nouveau n'est présent arrête le script
            if b in h: continue
            if a in h: h = h.replace(a, b); continue
            if not any(a == y for _, y in SERV_FAQ[l]) and not any(b == x for x, _ in SERV_FAQ[l]):
                raise SystemExit(f"introuvable dans {p} : {a[:90]}")
        h = ld_commun(h)
        if h != o: wr(p, h); print("services", p)

C_Q = {"": "How much does it cost?", "fr": "Combien ça coûte ?", "es": "¿Cuánto cuesta?", "he": "כמה זה עולה?"}
C_R = {"": "{} for the chalet. The final price depends on your dates, the number of people and the services you choose: you receive a written quote before you commit to anything. " + ROLE[""],
       "fr": "{} pour le chalet. Le prix final dépend de vos dates, du nombre de personnes et des services que vous choisissez : vous recevez un devis écrit avant tout engagement. " + ROLE["fr"],
       "es": "{} el chalé. El precio final depende de sus fechas, del número de personas y de los servicios que elija: recibe un presupuesto por escrito antes de comprometerse. " + ROLE["es"],
       "he": "{} לצ'אלה. המחיר הסופי תלוי בתאריכים, במספר המשתתפים ובשירותים שתבחרו: אתם מקבלים הצעת מחיר בכתב לפני שאתם מתחייבים לדבר. " + ROLE["he"]}

def offre(prix):
    return {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": prix, "priceCurrency": "EUR", "unitText": "week"}}

def chalets():
    for slug, k, prix in CHALETS:
        for l in LANGS:
            p = chemin(l, slug); h = rd(p); o = h
            rep = C_R[l].format(span_tpl(SEMAINE[l].format(eur_tpl(l, CLES[k])), SEMAINE[l].format(eur(l, prix))))
            h, n = re.subn(r"(<details><summary>" + re.escape(C_Q[l]) + r"</summary><p>)(.*?)(</p></details>)", lambda m: m.group(1) + rep + m.group(3), h, count=1, flags=re.S)
            assert n == 1, p
            def extra(liste):
                for b in liste:
                    if b.get("@type") == "Service": b["offers"] = offre(prix)
            h = ld_commun(h, extra)
            if h != o: wr(p, h); print("chalet", p)
        # source EN du générateur
        pg = f"_pages/{slug}.py"; s = rd(pg)
        rep_en = C_R[""].format(span_tpl(SEMAINE[""].format(eur_tpl("", CLES[k])), SEMAINE[""].format(eur("", prix))))
        n = re.sub(r'(\("How much does it cost\?", ")[^"]*(")', lambda m: m.group(1) + rep_en + m.group(2), s, count=1)
        if '"offers"' not in n:
            n = re.sub(r'(jsonld=\{.*)\},\n', lambda m: m.group(1) + ', "offers": ' + json.dumps(offre(prix)) + "},\n", n, count=1)
        if n != s: wr(pg, n); print("source", pg)

HUB_Q = {"": "How much does a chalet cost?", "fr": "Combien coûte un chalet ?", "es": "¿Cuánto cuesta un chalé?", "he": "כמה עולה צ'אלה?"}
# Les Deux Alpes = le moins cher des deux chalets (Rochebrune, ch2)
HUB_R = {
 "": "For a week in the chalet: Val Thorens " + prix_chalet("", "vth", 9500) + ", Les Deux Alpes " + prix_chalet("", "sl", 13000) + ", Courchevel " + prix_chalet("", "co", 17500) + ", near Megève " + prix_chalet("", "me", 23500) + ". The price for your dates and your services comes in one written quote. " + ROLE[""],
 "fr": "Pour une semaine au chalet : Val Thorens " + prix_chalet("fr", "vth", 9500) + ", Les Deux Alpes " + prix_chalet("fr", "sl", 13000) + ", Courchevel " + prix_chalet("fr", "co", 17500) + ", près de Megève " + prix_chalet("fr", "me", 23500) + ". Le prix pour vos dates et vos services vous est remis dans un seul devis écrit. " + ROLE["fr"],
 "es": "Por una semana en el chalé: Val Thorens " + prix_chalet("es", "vth", 9500) + ", Les Deux Alpes " + prix_chalet("es", "sl", 13000) + ", Courchevel " + prix_chalet("es", "co", 17500) + ", cerca de Megève " + prix_chalet("es", "me", 23500) + ". El precio para sus fechas y sus servicios llega en un solo presupuesto por escrito. " + ROLE["es"],
 "he": "לשבוע בצ'אלה: ואל טורנס " + prix_chalet("he", "vth", 9500) + ", לה דז אלפ " + prix_chalet("he", "sl", 13000) + ", קורשבל " + prix_chalet("he", "co", 17500) + ", ליד מג'ב " + prix_chalet("he", "me", 23500) + ". המחיר לתאריכים ולשירותים שלכם נשלח בהצעת מחיר אחת בכתב. " + ROLE["he"],
}

def hub():
    for l in LANGS:
        p = chemin(l, "kosher-chalets"); h = rd(p); o = h
        if l == "es":  # règle du 28/10 : jamais le nombre de chalets (oubli de la passe du 29/10 sur le hub ES)
            h = h.replace("Cinco chalés kosher en los Alpes", "Nuestros chalés kosher en los Alpes").replace("Cinco chalés con todo lo kosher resuelto", "Nuestros chalés, con todo lo kosher resuelto")
        if f"<summary>{HUB_Q[l]}</summary>" not in h:
            i = h.find('<section class="clair ss wrap faq">'); i = h.find("</details>", i) + len("</details>")
            assert i > 20, p
            h = h[:i] + f"<details><summary>{HUB_Q[l]}</summary><p>{HUB_R[l]}</p></details>" + h[i:]
        else:  # réponse déjà posée : remise à jour (prix reliés à la grille)
            h = re.sub(r"(<details><summary>" + re.escape(HUB_Q[l]) + r"</summary><p>)(.*?)(</p></details>)", lambda m: m.group(1) + HUB_R[l] + m.group(3), h, count=1, flags=re.S)
        h = ld_commun(h)
        if h != o: wr(p, h); print("hub", p)
    pg = "_pages/kosher-chalets.py"; s = rd(pg)
    if HUB_Q[""] not in s:
        m = re.search(r'h2="Kosher chalets: <i>questions</i>", items=\[\n(\s*\(.*?\),\n)', s)
        if m:
            n = s[:m.end()] + f'      ("{HUB_Q[""]}", "{HUB_R[""]}"),\n' + s[m.end():]
            wr(pg, n); print("source", pg)
    else:
        n = re.sub(r'(\("' + re.escape(HUB_Q[""]) + r'", ")[^"]*(")', lambda m: m.group(1) + HUB_R[""] + m.group(2), s, count=1)
        if n != s: wr(pg, n); print("source", pg)

CARTE = re.compile(r'<article class="kwp-carte[^"]*">.*?</article>', re.S)

def cartes():
    import glob
    lien = {k: slug for slug, k, _ in CHALETS}
    prix = {k: v for _, k, v in CHALETS}
    k_n = 0
    for f in glob.glob("**/index.html", recursive=True):
        if f.replace("\\", "/").split("/")[0] in ("preview", "node_modules", "_captures"): continue
        parts = f.replace("\\", "/").split("/")
        l = parts[0] if parts[0] in ("fr", "es", "he") else ""
        h = rd(f); o = h
        def pose(m):
            a = m.group(0)
            if 'class="kwp-dispo"' not in a and 'class="kwp-prix"' not in a: return a
            for k, slug in lien.items():
                if re.search(r'<h3><a href="(?:%s)?/%s/">' % (re.escape(pfx(l)), slug), a) or re.search(r'<h3><a href="(?:\.\./)+%s/">' % slug, a):
                    ouvre = f"<p class=\"kwp-prix\" data-prix-tpl='{attr(SEMAINE[l].format(eur_tpl(l, CLES[k])))}'>"
                    if 'class="kwp-prix"' in a:  # prix déjà posé par la passe du 30/10 : on le relie à la grille
                        return a if "data-prix-tpl" in a else a.replace('<p class="kwp-prix">', ouvre, 1)
                    return a.replace('<p class="kwp-dispo">', f'{ouvre}{SEMAINE[l].format(eur(l, prix[k]))}</p><p class="kwp-dispo">', 1)
            return a
        h = CARTE.sub(pose, h)
        if h != o: wr(f, h); k_n += 1
    print("cartes chalet avec prix :", k_n, "pages")
    css = rd("valora.css")
    if "/* PRIX-30-10 */" not in css:
        wr("valora.css", css + "\n/* PRIX-30-10 */ /* prix « à partir de » des cartes chalet et du bloc des prix (Moshé 30/10) */\n"
           "body .kwp-carte .kwp-corps>.kwp-prix{margin:10px 0 0;padding:0 22px;font-size:15px;letter-spacing:.02em;color:var(--jaune,#C9A961)}\n"
           ".repas-prix h3{margin:40px 0 8px}\n.repas-prix .prix-chalets a{color:inherit;text-decoration:underline;text-underline-offset:3px}\n")

# ---------- 3. Lyon FR ----------
LYON = {
 "fr/rue-juiverie-lyon/index.html": dict(
   titre=("Quartier juif de Lyon : la rue Juiverie", "Rue Juiverie, le quartier juif de Lyon : histoire et visite"),
   h1=("Rue Juiverie, Lyon<br><i>la rue qui a gardé le nom</i>", "Rue Juiverie<br><i>le quartier juif de Lyon</i>"),
   desc=("La rue Juiverie, dans le Vieux Lyon, doit son nom à la communauté juive médiévale. Ce qui reste, ce qui a disparu et comment la visiter avec une guide juive.",
         "La rue Juiverie, ancien quartier juif de Lyon dans le Vieux Lyon, doit son nom à la communauté médiévale. Ce qui reste, ce qui a disparu, comment la visiter."),
   texte=None),
 "fr/mikveh-lyon/index.html": dict(
   titre=("Mikvé à Lyon et Villeurbanne : adresses, contacts", "Mikvé à Lyon : adresses, horaires, comment réserver"),
   h1=("Mikvé à Lyon<br><i>adresses et qui appeler</i>", "Mikvé à Lyon<br><i>adresses, horaires, comment réserver</i>"),
   desc=("Huit mikvaot à Lyon et Villeurbanne, avec adresses et téléphones. Le Mikvé Haya Mouchka, 60 rue Crillon, est indiqué ouvert chaque soir. Comment demander avant de voyager.",
         "Mikvé (ou mikve) à Lyon et Villeurbanne : huit adresses avec téléphones, le Mikvé Haya Mouchka ouvert chaque soir, et comment réserver avant de voyager."),
   texte=("Lyon et Villeurbanne comptent plusieurs mikvaot.", "Lyon et Villeurbanne comptent plusieurs mikvaot (on écrit aussi mikve ou mikveh).")),
}

def lyon():
    for p, d in LYON.items():
        h = rd(p); o = h
        a, n = d["titre"]
        h = rv(h, a + " | Mishpacha Tours", n + " | Mishpacha Tours", p)
        h = rv(h, *d["h1"], p)
        h = rv(h, *d["desc"], p)
        if d["texte"]: h = rv(h, *d["texte"], p)
        titre = re.search(r"<title>(.*?) \| Mishpacha Tours</title>", h).group(1)
        desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1))
        def extra(liste):
            for b in liste:
                if b.get("@type") == "WebPage": b["name"] = html.unescape(titre); b["description"] = desc
        h = ld_commun(h, extra)
        if h != o: wr(p, h); print("lyon", p)

# ---------- 4. sameAs sur /about/ ----------
GBP = "https://maps.google.com/?cid=6228049695326569266"

def about():
    for l in LANGS:
        p = chemin(l, "about"); h = rd(p); o = h
        def extra(liste):
            for b in liste:
                if b.get("@id") == "https://mishpachatours.com/#organization": b["sameAs"] = [GBP]
        h = ld(h, extra)
        if h != o: wr(p, h); print("about", p)
    pg = "_pages/about.py"; s = rd(pg)
    if '"sameAs"' not in s:
        n = s.replace('"@id": "https://mishpachatours.com/#organization", "name": "Mishpacha Tours",',
                      '"@id": "https://mishpachatours.com/#organization", "name": "Mishpacha Tours", "sameAs": ["' + GBP + '"],', 1)
        if n != s: wr(pg, n); print("source", pg)

if __name__ == "__main__":
    pessah(); services(); chalets(); hub(); cartes(); lyon(); about()
