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
LOCALE = {"en": "en-GB", "fr": "fr-FR", "es": "es-ES", "he": "he-IL"}
MERCI = {"en": "/merci/", "fr": "/fr/merci/", "es": "/es/merci/", "he": "/he/merci/"}

FIL = {"en": ('<a href="../">Home</a>', "Plan your trip"), "fr": ('<a href="/fr/">Accueil</a>', "Préparer votre voyage"),
       "es": ('<a href="/es/">Inicio</a>', "Planifique su viaje"), "he": ('<a href="/he/">ראשי</a>', "תכננו את הטיול")}

# 02/11 : textes neufs du formulaire en 3 ecrans (EN, FR, ES, HE ; hebreu relu selon le skill relecture-hebreu)
NEUF = {
    "Where, when, how many?": ("Où, quand, combien ?", "¿Dónde, cuándo, cuántos?", "איפה, מתי, כמה?"),
    "Your contact": ("Vos coordonnées", "Sus datos de contacto", "פרטי הקשר שלכם"),
    "We answer you on WhatsApp.": ("Nous vous répondons sur WhatsApp.", "Le respondemos por WhatsApp.", "נחזור אליכם בוואטסאפ."),
    "Not chosen yet, advise us": ("Pas encore choisi, conseillez-nous", "Aún sin elegir, aconséjennos", "עוד לא בחרנו, ייעצו לנו"),
    "More details (optional)": ("Plus de détails (facultatif)", "Más detalles (opcional)", "פרטים נוספים (לא חובה)"),
    "Accommodation": ("Hébergement", "Alojamiento", "לינה"),
    "Budget and priorities": ("Budget et priorités", "Presupuesto y prioridades", "תקציב וסדרי עדיפויות"),
    "A few more things": ("Encore quelques points", "Algunas cosas más", "עוד כמה דברים"),
    "Which holiday?": ("Quelle fête ?", "¿Qué fiesta?", "איזה חג?"),
    "Continue": ("Continuer", "Continuar", "המשיכו"),
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
    "Optional.": ("Facultatif.", "Opcional.", "לא חובה."),
}
def tt(s, lang):
    if s in NEUF: return s if lang == "en" else NEUF[s][LANGS.index(lang) - 1]
    return t(s, lang)

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
ALPES = ["intention", "ou", "quand", "qui", "sejour", "minyan", "budget", "final"]
PATHS = {"a": ALPES, "b": ALPES, "e": ALPES, "c": ["intention", "trajet", "quandvan", "qui", "budget", "final"],
         "d": ["intention", "lyon", "qui", "budget", "final"], "f": ["intention", "message", "ou", "quand", "qui", "budget", "final"]}
STATIONS_PRINC = ["Courchevel", "Val Thorens", "Les Menuires", "Tignes", "Megève", "Les Deux Alpes", "Val d'Isère", "Alpe d'Huez", "Chamonix", "Les Arcs", "La Plagne"]
STATIONS_HE = {"Courchevel": "קורשבל", "Val Thorens": "ואל טורנס", "Les Menuires": "לה מנואר", "Megève": "מג'ב", "Les Deux Alpes": "לה דז אלפ", "Val d'Isère": "ואל דיזר",
               "Alpe d'Huez": "אלפ ד'ואז", "Chamonix": "שמוני", "Les Arcs": "לז ארק", "La Plagne": "לה פלאן"}
LAB_ORDER = ["voyage", "lieu", "lieu_pas_choisi", "adresse", "van_depart", "van_arrivee", "aller_retour", "arrivee", "creneau", "depart", "heure", "retour_date", "retour_heure", "flexible", "familles", "adultes", "enfants", "bebes", "bebe_materiel", "hommes", "bagages",
             "logement", "chambres", "sdb", "logement_opt", "repas", "repas_jours", "allergies", "cacherout", "cacherout_detail", "minyan_niveau", "religieux", "rite", "aeroport", "vol_ville", "vols_pris", "vol", "transport",
             "ski", "niveau", "lyon", "langue_visite", "extras", "budget_total", "budget", "budget_vols", "priorites", "message", "ville", "urgence", "pour_qui"]
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
    def chips(name, opts, multi=True, b=""):
        """opts : texte EN, ou (texte EN, branches, cle, saison). saison : w = hiver seulement, s = ete seulement."""
        typ = "checkbox" if multi else "radio"
        out = []
        for o in opts:
            en, ob, k, sa = (o, "", "", "") if isinstance(o, str) else (o + ("", "", ""))[:4]
            kk = f' data-k="{k}"' if k else ""
            out.append(f'<label class="pf-c"{battr(ob)}{sattr(sa)}><input type="{typ}" name="{name}" value="{E(en)}" data-en="{esc(en)}"{kk}><span>{insec(E(en))}</span></label>')
        return f'<div class="pf-chips"{battr(b)}>' + "".join(out) + "</div>"
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
    def etape(id_, titres, aide, corps, cls=""):
        if isinstance(titres, str): titres = [(titres, "")]
        hs = "".join(f'<h2 tabindex="-1"{battr(b)}>{E(x)}</h2>' for x, b in titres)
        if isinstance(aide, str): aide = [(aide, "")]
        ps = "".join(f'<p{battr(b)}>{E(x)}</p>' for x, b in aide if x)
        return f'<div class="pf-etape {cls}" id="e-{id_}" data-e="{id_}" role="group"><div class="pf-tete">{hs}{ps}</div>{corps}</div>\n'

    # ================= ecran 1 : six lignes a picto
    def ligne(val, titre, sous_, voyage):
        return (f'<label class="pf-ligne"><input type="radio" name="intention" value="{val}" data-voyage="{E(voyage)}" data-en="{esc(voyage)}">'
                f'<img src="{IMG}illus/famille/form/intention-{val}.svg" alt="" width="48" height="48">'
                f'<span class="pf-l-t"><b>{E(titre)}</b><small>{E(sous_)}</small></span><span class="pf-fl" aria-hidden="true"></span></label>')
    lignes = '<div class="pf-choix">' + "".join([
        ligne("a", "A full stay in the Alps", "Chalet, chef, Shabbat, minyan", "A full stay in the Alps"),
        ligne("b", "I already have my place", "Chef, meals, minyan, transfers", "Services where we already stay (chef, meals, minyan, transfers)"),
        ligne("e", "Pesach or a holiday", "A full holiday programme", "Holiday programme (Pesach or other)"),
        ligne("d", "A Jewish Lyon tour", "Guided, 2 hours", "Jewish Lyon tour"),
        ligne("c", "A van transfer", "From A to B, with a driver", "Van transfer, point A to point B"),
        ligne("f", "Something else", "Tell us in your words", "Something else"),
    ]) + "</div>"
    wa_q1 = f'<p class="pf-wa">{E("Prefer to talk?")} <a href="{JSX[lang]["wa"]}" rel="noopener">{E("Message us on WhatsApp")}</a></p>'
    S = [etape("intention", "What can we do for you?", [], lignes + wa_q1, "pf-intention")]

    # ================= un ecran par question (Moshe 03/11 : « une conciergerie de luxe, page apres page ») ; aucune section repliee
    ou = ('<div class="pf-pastilles">' + "".join(
              f'<button type="button" class="pf-pas" data-lieu="{esc(st)}"><span{" dir=" + chr(34) + "ltr" + chr(34) if lang == "he" and st not in STATIONS_HE else ""}>{esc(STATIONS_HE.get(st, st) if lang == "he" else st)}</span></button>'
              for st in STATIONS_PRINC) + "</div>" +
          chips("lieu_pas_choisi", ["Not chosen yet, advise us"]) +
          champ("lieu", "lieu", "Another resort", ph="Morzine, Zermatt, Verbier") +
          sugg("lieu", STATIONS))
    quand = (f'<div data-b="e">{sous("Which holiday?")}' +
             chips("voyage", ["Pesach in the Alps", "Hanukkah in the Alps", "Sukkot", "Rosh Hashanah and Yom Kippur", "Purim", "Shavuot", "Another holiday"]) + "</div>" +
             '<div class="pf-duo">' + champ("arrivee", "arrivee", "Arrival", typ="date") + champ("depart", "depart", "Departure", typ="date") + "</div>" +
             '<p class="pf-info" id="dm-nuits" hidden aria-live="polite"></p>' +
             f'<p class="pf-info" id="dm-shabbat" hidden data-t="{E("Shabbat during your stay:")}"></p>' +
             f'<p class="pf-erreur" id="dm-date-err" role="alert" hidden>{E("The departure is before the arrival.")}</p>' +
             chips("flexible", ["Dates are fixed", "Dates are flexible"], multi=False) +
             f'<div data-b="abe">{sous("Your flights")}' +
             chips("aeroport", ["Flying to Lyon", "Flying to Geneva", "Flying to Grenoble", "Another airport, or not sure yet"], multi=False) +
             chips("vols_pris", ["Flights already booked", "Not booked yet"], multi=False) +
             champ("vol_ville", "vol_ville", "City you fly from", ph="New York, Tel Aviv, London") +
             sugg("vol_ville", [("New York",), ("Brooklyn",), ("Miami",), ("Los Angeles",), ("Montreal",), ("Toronto",), ("Tel Aviv",), ("Jerusalem",), ("London",), ("Manchester",), ("Paris",), ("Antwerp",), ("Brussels",), ("Zurich",), ("Geneva",), ("Buenos Aires",), ("Mexico City",), ("São Paulo",), ("Johannesburg",)]) + "</div>")
    qui = (compteur("adultes", "Adults", v=2) + compteur("enfants", "Children") +
           ages("enfants", "Ages of the children", "9 and 12", [(str(n),) for n in range(2, 18)]) +
           compteur("bebes", "Babies") + ages("bebes", "Ages of the babies", "10 months", ["3 months", "6 months", "1 year", "18 months", "2 years"]) +
           '<div class="pf-mat cache" data-for="bebes">' + chips("bebe_materiel", ["Baby cots", "High chairs", "Car seats"]) + "</div>" +
           compteur("familles", "Families or households", b="abef", v=1) +
           compteur("chambres", "Bedrooms", b="a") +
           f'<div data-b="c">{sous("Luggage and equipment")}' + chips("bagages", ["Large suitcases", "Cabin bags only", "Skis or snowboards", "Baby seats or boosters", "Wheelchair or walker"]) + "</div>")
    sejour = (f'<div data-b="ae">{sous("Accommodation")}' + chips("logement", ["A private chalet", "Apartments, same residence", "A hotel", "Advise me"], multi=False) + "</div>" +
              champ("adresse", "adresse", "Address or name of the accommodation", ph="Chalet Le Sapin, 12 route du Lac", b="b") +
              sous("Meals") + chips("repas", ["Private chef in the chalet", "Meals delivered, ready to heat", "Shabbat meals only", "Advise me", ("No meals needed", "", "none")], multi=False) +
              champ("allergies", "allergies", "Allergies or special diets", ph="Nut allergy for one child"))
    minyan = (chips("minyan_niveau", ["The minyan is essential", "Nice to have", "Not needed"], multi=False) +
              si("minyan_niveau!=Not needed", compteur("hommes", "Men over bar mitzvah age, for the minyan")) +
              chips("religieux", ["Sefer Torah in the chalet"]))
    budget = (champ("budget-total", "budget_total", "Total budget for the whole stay", ph="€", extra=' inputmode="numeric"', b="abef") +
              f'<p class="pf-aide" data-b="abef">{E("Optional, but it helps us aim right. One figure for the whole group and the whole stay, flights aside.")}</p>' +
              zone("message-fin", "message", "Anything else we should know", "Anything that helps: a baby, a late arrival, a special diet.", b="abcde"))
    trajet = (champ("van_depart", "van_depart", "Pick-up point", ph="Lyon Saint-Exupéry airport") +
              sugg("van_depart", ["Geneva airport", "Lyon airport", "Lyon Part-Dieu station", "Our chalet"] + STATIONS) +
              champ("van_arrivee", "van_arrivee", "Drop-off point", ph="Les Deux Alpes, chalet") +
              sugg("van_arrivee", ["Our chalet"] + STATIONS + ["Geneva airport", "Lyon airport", "Lyon Part-Dieu station"]) +
              chips("aller_retour", ["One way", "Return trip"], multi=False))
    quandvan = (sous("Outbound") + '<div class="pf-duo">' + champ("arrivee-van", "arrivee", "Date", typ="date") + champ("heure", "heure", "Pick-up time", typ="time") + "</div>" +
                si("aller_retour=Return trip", sous("Return") + '<div class="pf-duo">' + champ("retour_date", "retour_date", "Return date", typ="date") +
                   champ("retour_heure", "retour_heure", "Return pick-up time", typ="time") + "</div>") +
                champ("vol-van", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30"))
    lyon = (chips("lyon", ["Jewish Lyon walk (2 h)", "Stopover (3 h) on the way", "Memory: CHRD museum", "Memory: Montluc, Neveh Shalom", "Day trip to Izieu", "Shabbat with a Chabad family"]) +
            sous("Which day?") + champ("arrivee-jour", "arrivee", "Date", typ="date") + chips("creneau", ["Morning", "Afternoon", "Either"], multi=False) +
            sous("Language of the visit") + chips("langue_visite", ["English", "French", "Spanish"], multi=False) +
            '<p class="pf-note">' + E("To enter the Grande Synagogue, the community's security team will ask for your names and passports once the tour is confirmed.") + "</p>")
    message_f = zone("message-f", "message", "Tell us what you have in mind", "A bar mitzvah weekend in the Alps for 30 guests")
    S += [etape("message", "Tell us what you have in mind", "Write it the way you would say it. We take it from there.", message_f),
          etape("ou", "Where would you like to stay?", "Choose a resort, or let us advise you.", ou),
          etape("quand", "When are you coming?", "Approximate dates are fine.", quand),
          etape("trajet", "Where from, and is there a return?", "Address, airport, station or hotel. A town name is enough.", trajet),
          etape("quandvan", "When?", "Date and time of each trip. Add the flight if you land or take off.", quandvan),
          etape("lyon", "Which visit, and when?", "Tours are held in English, French or Spanish.", lyon),
          etape("qui", "Who is coming?", [("Count the whole group, all families together.", "abef"), ("Children's ages help us choose rooms, ski school and cots.", "cd")], qui),
          etape("sejour", "Your stay and meals", "Pick what suits you. We advise if you are not sure.", sejour),
          etape("minyan", "Minyan and Shabbat", "", minyan),
          etape("budget", [("Your budget and your wishes", "abef"), ("Anything else?", "cd")], [("Both are optional.", "abe"), ("Optional.", "cdf")], budget)]

    # ================= dernier ecran : contact
    contact = (champ("prenom", "prenom", "First name", extra=' autocomplete="given-name" required') +
        f'<div class="pf-champ"><label for="f-tel">{E("WhatsApp number")}</label><div class="pf-tel"><select id="f-indicatif" name="indicatif" aria-label="{E("Country code")}" required>'
        + INDICATIFS.replace("{code}", E("Code")) + '</select><input type="tel" id="f-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="212 555 0100" pattern="[0-9 ().-]{6,16}" required></div></div>' +
        champ("email", "email", "Email (optional)", typ="email", extra=' autocomplete="email"'))
    S.append(etape("final", "Your contact", "We answer you on WhatsApp.", contact + f'<p class="pf-erreur" id="dm-erreur" hidden>{esc(JSX[lang]["err"])}</p>', "pf-contact"))

    prog = (f'<div class="pf-prog" id="dm-prog"><button type="button" class="pf-retour" id="dm-back" hidden aria-label="{E("Back")}"><span aria-hidden="true"></span>{E("Back")}</button>'
            f'<span class="pf-prog-txt" id="dm-prog-txt" aria-live="polite"></span>'
            f'<div class="pf-barre" id="dm-barre-c" role="progressbar" aria-label="{E("Progress")}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="dm-barre"></i></div></div>')
    nav = (f'<p class="pf-accord" id="dm-accord" hidden><label><input type="checkbox" id="dm-accord-cb" name="accord" required> '
           f'<span>{esc(ACCORD[lang][0])} <a href="{ACCORD[lang][2]}" target="_blank" rel="noopener">{esc(ACCORD[lang][1])}</a></span></label>'
           f'<small class="pf-erreur" id="dm-accord-err" role="alert" hidden>{esc(ACCORD[lang][3])}</small></p>'
           f'<div class="pf-nav" id="dm-nav" hidden>'
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
var KEY='mt-plan-v2-'+C.lang,TTL=2592e6;
var ctrls=[].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(e){return e.name!=='societe'&&e.name!=='accord'});
var accord=document.getElementById('dm-accord'),accordCb=document.getElementById('dm-accord-cb'),accordErr=document.getElementById('dm-accord-err');
ctrls.forEach(function(e){e.scr=e.closest('.pf-etape').getAttribute('data-e')});
var etapes=[].slice.call(f.querySelectorAll('.pf-etape'));
var barre=document.getElementById('dm-barre'),barreC=document.getElementById('dm-barre-c'),ptxt=document.getElementById('dm-prog-txt');
var nav=document.getElementById('dm-nav'),bBack=document.getElementById('dm-back'),bNext=document.getElementById('dm-next'),bSend=document.getElementById('dm-send'),petit=document.getElementById('dm-petit');
var cur='intention',sent=false,lieuIn=document.getElementById('lieu');
function mo(){return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: no-preference)').matches)}
var dl=window.dataLayer=window.dataLayer||[];
var mx=document.getElementById('dm-max'),nuitsP=document.getElementById('dm-nuits'),dateErr=document.getElementById('dm-date-err');
function branch(){var r=f.querySelector('input[name="intention"]:checked');return r?r.value:''}
function path(){var b=branch();if(!b)return ['intention'];return C.paths[b].slice()}
/* data-si="nom=valeur" : visible si cette case est cochee ; "nom!=valeur" : visible si une case est cochee et que ce n'est pas celle-la */
function siOk(c){var m=/^(\w+)(!?=)(.*)$/.exec(c);if(!m)return true;var on=ctrls.filter(function(e){return e.name===m[1]&&e.checked}).map(function(e){return e.getAttribute('data-en')||e.value});
 return m[2]==='='?on.indexOf(m[3])>=0:(on.length>0&&on.indexOf(m[3])<0)}
function sync(){var b=branch(),p=path();
 var hs=false,hw=false,m=/^\d{4}-(\d\d)/.exec(raw0('arrivee'));if(m){var mm=+m[1];if(mm>=5&&mm<=10)hs=true;else hw=true}
 [].forEach.call(f.querySelectorAll('[data-s]'),function(n){if(n.classList.contains('pf-auto'))return;var s=n.getAttribute('data-s');n.hidden=s==='w'?(hs&&!hw):(hw&&!hs)});
 [].forEach.call(f.querySelectorAll('[data-b]'),function(n){if(n.classList.contains('pf-auto'))return;n.hidden=n.getAttribute('data-b').indexOf(b)<0});
 [].forEach.call(f.querySelectorAll('[data-si]'),function(n){n.hidden=!siOk(n.getAttribute('data-si'))});
 ctrls.forEach(function(e){var ok=p.indexOf(e.scr)>=0;
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
 if(n==='budget_total')return euros(raw(n));
 return en?rawEn(n):raw(n)}
function ckey(e){return (e.type==='checkbox'||e.type==='radio')?'k:'+e.name+'|'+(e.getAttribute('data-en')||e.value):'i:'+(e.id||e.name)}
/* 02/11 : reponses gardees dans ce navigateur (localStorage, 30 jours), par champ et non par position ; effacees a l'envoi */
function save(){try{var v={};ctrls.forEach(function(e){if(e.type==='checkbox'||e.type==='radio'){if(e.checked)v[ckey(e)]=1}else if(e.value)v[ckey(e)]=e.value});
 localStorage.setItem(KEY,JSON.stringify({t:Date.now(),c:cur,v:v}))}catch(x){}}
function load(){try{var s=JSON.parse(localStorage.getItem(KEY)||'null');if(!s||!s.v)return;if(!(Date.now()-s.t<TTL)){localStorage.removeItem(KEY);return}
 ctrls.forEach(function(e){var k=ckey(e);if(e.type==='checkbox'||e.type==='radio')e.checked=!!s.v[k];else if(k in s.v)e.value=s.v[k]});cur=s.c||'intention'}catch(x){}}
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
function render(){var p=sync();plis();if(p.indexOf(cur)<0)cur='intention';
 etapes.forEach(function(e){e.hidden=e.getAttribute('data-e')!==cur});
 var i=p.indexOf(cur),last=cur==='final',b=branch();f.classList.toggle('avance',cur!=='intention');
 nav.hidden=cur==='intention';bBack.hidden=i<=0;bNext.hidden=last;bSend.hidden=!last;petit.hidden=!last;accord.hidden=!last;if(!sent)bSend.disabled=false;
 var nn=cur==='quand'?nights():null,bad=nn!==null&&nn<0;shabbats(nn);
 nuitsP.hidden=!(nn!==null&&nn>=1);if(!nuitsP.hidden)nuitsP.textContent=nn===1?C.t.nuit:C.t.nuits.replace('{n}',nn);dateErr.hidden=!bad;
 bNext.disabled=(cur==='intention'&&!b)||bad;
 var n=i+1,N=b?p.length:C.total;ptxt.textContent=C.t.step.replace('{n}',n).replace('{t}',N);var pc=Math.round(n/N*100);
 [].forEach.call(f.querySelectorAll('.pf-pas'),function(x){var on=!!lieuIn&&lieuIn.value===x.getAttribute('data-lieu');x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false')});barre.style.width=pc+'%';barreC.setAttribute('aria-valuenow',pc);
 save()}
function show(id,push,focus){var p=sync();if(p.indexOf(id)<0)id='intention';
 var oi=p.indexOf(cur),ni=p.indexOf(id);f.setAttribute('data-dir',ni<oi?'back':'fwd');
 cur=id;render();
 dl.push({event:'form_step',step:cur,step_index:p.indexOf(cur)+1,branch:branch()});
 if(push){try{history.pushState({e:cur},'','#e-'+cur)}catch(x){}}
 if(focus){var h=document.querySelector('.pf-etape[data-e="'+cur+'"] h2:not([hidden])');if(h)h.focus({preventScroll:true});
  var r=f.getBoundingClientRect();if(r.top<0||r.top>200)window.scrollTo({top:window.pageYOffset+r.top-90,behavior:'smooth'})}}
function next(){var p=path(),i=p.indexOf(cur);if(i>=0&&i<p.length-1)show(p[i+1],true,true)}
function back(){var p=path(),i=p.indexOf(cur);if(i>0)show(p[i-1],true,true)}
bNext.addEventListener('click',next);bBack.addEventListener('click',back);
f.addEventListener('click',function(ev){
 var sg=ev.target.closest&&ev.target.closest('.pf-auto button');if(sg){var inp=document.getElementById(sg.parentNode.getAttribute('data-for')),v=sg.getAttribute('data-v'),segs=inp.value.split(/,\s*/);
  segs[segs.length-1]=v;inp.value=segs.join(', ');sg.parentNode.hidden=true;inp.focus();inp.dispatchEvent(new Event('input',{bubbles:true}));return}
 var ps=ev.target.closest&&ev.target.closest('.pf-pas');if(ps){lieuIn.value=ps.getAttribute('data-lieu');var pc0=f.querySelector('input[name="lieu_pas_choisi"]');if(pc0)pc0.checked=false;render();setTimeout(next,mo()?260:60);return}
 var tu=ev.target.closest&&ev.target.closest('.pf-ligne');if(tu&&ev.target.tagName!=='INPUT'&&cur==='intention'){var ri=tu.querySelector('input');if(ri&&ri.checked){setTimeout(next,120);return}}
 var bt=ev.target.closest&&ev.target.closest('.cpt button');if(!bt)return;
 var inp=bt.parentNode.querySelector('input'),v0=parseInt(inp.value,10)||0,plus=bt.className==='plus',v=Math.max(0,Math.min(99,v0+(plus?1:-1)));inp.value=v;
 inp.dispatchEvent(new Event('input',{bubbles:true}))});
function onchg(ev){var t=ev.target;
 if(t===accordCb&&t.checked){accord.classList.remove('pf-manque');accordErr.hidden=true}
 if(t.getAttribute&&t.getAttribute('aria-invalid')==='true'&&(t.value||'').trim())t.setAttribute('aria-invalid','false');
 if(t.name==='arrivee'&&t.type==='date'){[].forEach.call(f.querySelectorAll('input[name="depart"]'),function(x){x.min=t.value})}
 if(ev.type==='change'&&t.name==='priorites'){mx.hidden=true;
  if(t.checked&&els('priorites').filter(function(e){return e.checked}).length>3){t.checked=false;mx.hidden=false}}
 if(ev.type==='change'&&ev.isTrusted&&t.name==='lieu_pas_choisi'&&t.checked){lieuIn.value='';render();setTimeout(next,mo()?260:60);return}
 render();
 if(ev.type==='change'&&t.name==='intention'){dl.push({event:'form_start',branch:t.value});setTimeout(next,220)}}
f.addEventListener('change',onchg);f.addEventListener('input',onchg);
window.addEventListener('popstate',function(ev){var id=ev.state&&ev.state.e;show(id||'intention',false,true)});
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
 if(r){r.checked=true;cur=path()[1]||'intention';dl.push({event:'form_start',branch:i})}
 var l=s('lieu');if(l)fill('lieu',l);
 var a=d('arrivee'),b=d('depart');if(a)fill('arrivee',a);if(b)fill('depart',b);if(a)ctrls.forEach(function(e){if(e.name==='depart')e.min=a});
 ['adultes','enfants','bebes'].forEach(function(k){var v=n(k);if(v!==null)fill(k,String(v))});
 var vy=s('voyage').toLowerCase();if(vy)ctrls.forEach(function(e){if(e.name==='voyage'&&(e.getAttribute('data-en')||e.value).toLowerCase()===vy)e.checked=true})}
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
load();prefill();devine(f.elements.indicatif);f.classList.add('js');show(cur,false,false);cb();try{history.replaceState({e:cur},'')}catch(x){}
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
    cfg = {"lang": lang, "langNom": {"en": "English", "fr": "Français", "es": "Español", "he": "עברית"}[lang], "loc": LOCALE[lang], "merci": MERCI[lang], "paths": PATHS, "total": 8,
           "indic": {"he": "+972", "fr": "+33", "es": "+34", "en": ""}[lang],
           "lab": [[k, lab[k]] for k in LAB_ORDER], "labEn": [[k, lab_en[k]] for k in LAB_ORDER],
           "k": {"tour": JSX[lang]["tour"], "none": JSX[lang]["none"], "datesj": JSX[lang]["datesj"], "adultes": JSX[lang]["adultes"], "enfants": JSX[lang]["enfants"],
                 "bebes": JSX[lang]["bebes"], "logementB": T("Already booked, I need services only")},
           "t": {"step": T("Step {n} of {t}"), "nuits": T("{n} nights"), "nuit": T("1 night"), "sending": T("Sending…"), "ko": KO}}
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
""".replace("P:has", P + ":has").replace("P ", P + " ").replace(",P ", "," + P + " ") + CSS_Z

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
        s = s.replace('<link rel="stylesheet" href="/valora-form.css">', "")   # 02/11 : formulaire en charte LV, plus de feuille Valora du formulaire
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("ok", p)
