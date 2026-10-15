# -*- coding: utf-8 -*-
"""Genere /plan-your-trip/ (EN) et remplace le formulaire des copies fr/ es/ he/ : formulaire de demande EN ETAPES (14/10).
   python _build_demande.py (depuis site-v5/). Une question (ou un petit groupe) par ecran, des branches selon l'intention
   (sejour complet / j'ai deja mon logement / van / Lyon / fete / autre), barre de progression, recapitulatif, etat en sessionStorage.
   Envoi vers le meme Apps Script que les autres formulaires, MEMES champs et MEME format qu'avant (le 13/10) :
   colonnes tour / dates / personnes / langue / nom / contact, tout le reste concatene dans `message`.
   Les textes viennent de _demande_textes.py (page du 13/10, relue en 4 langues) et _demande_nouveaux.py (textes de l'11/10 : etapes).
   Les copies traduites gardent leur pied ; le hero (15/10), la section du formulaire et son script sont remplaces."""
from _head import head_page, webpage, crumbs, BASE
from _demande_nouveaux import t, LAB, LAB_NEW, JSX
import re, os, json, html, io, urllib.request

LANGS = ("en", "fr", "es", "he")
LOCALE = {"en": "en-GB", "fr": "fr-FR", "es": "es-ES", "he": "he-IL"}
MERCI = {"en": "/merci/", "fr": "/fr/merci/", "es": "/es/merci/", "he": "/he/merci/"}

# ---------------------------------------------------------------- page EN (tete, hero)
home = open("_gabarit.html", encoding="utf-8").read()
head = home[:home.index("<main>")]; foot = home[home.index("</main>")+7:]
def rel(s):
    for a, b in [('href="img/','href="../img/'),('src="img/','src="../img/'),('src="fonts/','src="../fonts/'),('href="fonts/','href="../fonts/'),
                 ('href="styles.css"','href="../styles.css"'),('href="./"','href="../"'),('href="#tours"','href="../#tours"'),('href="#why"','href="../#why"'),
                 ('href="#before"','href="../#before"'),('href="#guide"','href="../#guide"'),('href="fr/"','href="../fr/"'),('href="es/"','href="../es/"'),
                 ('href="he/"','href="../he/"'),('href="credits.html"','href="../credits.html"'),('href="#book"','href="#demande"'),('href="jewish-lyon-guide/"','href="../jewish-lyon-guide/"')]:
        s = s.replace(a, b)
    return s
P = "/plan-your-trip/"
TITLE = "Plan your kosher trip to the Alps or Lyon | Mishpacha Tours"
DESC = "One form for your whole trip: dates, family, chalet or hotel, chef and meals, Shabbat and minyan, transfers, ski, Lyon tours. You get a day-by-day programme with the price."
h = rel(head)
h = re.sub(r"<title>.*?</title>", "<title>" + TITLE + "</title>", h)
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', h)
h = head_page(h, P, TITLE.split(" | ")[0], DESC, [webpage(P, TITLE.split(" | ")[0], DESC), crumbs([("Plan your trip", P)])])

FIL = {"en": ('<a href="../">Home</a>', "Plan your trip"), "fr": ('<a href="/fr/">Accueil</a>', "Préparer votre voyage"),
       "es": ('<a href="/es/">Inicio</a>', "Planifique su viaje"), "he": ('<a href="/he/">ראשי</a>', "תכננו את הטיול")}
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"/></svg>'
def hero(lang):
    T = lambda s: html.escape(t(s, lang), quote=True)
    home, cur = FIL[lang]
    puces = "".join(f"<li>{CHECK}{T(x)}</li>" for x in ["Free", "No commitment", "Reply within one business day", "A few minutes"])
    return ('<section class="pratique-hero demande-hero"><div class="wrap">\n'
            f'  <p class="fil">{home} / {cur}</p>\n'
            f'  <h1>{T("Plan your")} <span>{T("kosher trip")}</span></h1>\n'
            f'  <p class="dm-promesse">{T("Answer a few questions. We send you a day-by-day programme with the price.")}</p>\n'
            f'  <ul class="dm-puces">{puces}</ul>\n'
            '</div></section>')

# ---------------------------------------------------------------- le formulaire, par langue
# Branches : a sejour complet, b j'ai deja mon logement, c van, d Lyon, e fete, f autre
PATHS = {
    "a": ["intention", "quoi", "dates", "groupe", "logement", "repas", "cacherout", "religieux", "transport", "ski", "lyon", "extras", "budget", "final"],
    "b": ["intention", "ou", "dates", "groupe", "religieux", "repas", "cacherout", "message", "budget", "final"],
    "c": ["intention", "trajet", "quand", "groupe", "bagages", "message", "final"],
    "d": ["intention", "lyon", "jour", "groupe", "message", "final"],
    "e": ["intention", "fete", "dates", "groupe", "logement", "repas", "cacherout", "religieux", "extras", "budget", "final"],
    "f": ["intention", "message", "dates", "groupe", "budget", "final"],
}
LAB_ORDER = ["voyage", "lieu", "lieu_pas_choisi", "adresse", "van_depart", "van_arrivee", "arrivee", "creneau", "depart", "heure", "flexible", "adultes", "enfants", "bebes", "bebe_materiel", "hommes", "bagages",
             "logement", "chambres", "logement_opt", "repas", "repas_jours", "allergies", "cacherout", "cacherout_detail", "minyan_niveau", "religieux", "rite", "aeroport", "vol_ville", "vols_pris", "vol", "transport",
             "ski", "niveau", "lyon", "langue_visite", "extras", "priorites", "budget", "budget_vols", "message", "ville", "urgence", "pour_qui"]
INDICATIFS = '<option value="">{code}</option>' + "".join(f'<option value="{v}">{v} {c}</option>' for v, c in [
    ("+1", "US / CA"), ("+44", "UK"), ("+972", "IL"), ("+33", "FR"), ("+32", "BE"), ("+41", "CH"), ("+34", "ES"), ("+39", "IT"), ("+49", "DE"), ("+31", "NL"),
    ("+54", "AR"), ("+52", "MX"), ("+55", "BR"), ("+61", "AU"), ("+27", "ZA"), ("+7", "RU"), ("+380", "UA")])

# ---------------------------------------------------------------- pictogrammes (Lucide, licence ISC, lucide-static 0.460.0, caches dans _candidats/lucide/)
# Un pictogramme par choix : « il ne faut pas avoir besoin de lire pour comprendre » (operateur, 15/10). Cle = texte EN de l'option ;
# « nom/b:texte » (bloc de budget) ou « nom:texte » l'emporte sur « texte ». Jamais deux fois la meme icone dans un meme ecran (assert au build).
LUCIDE_V = "0.460.0"
ICONES = {
    # quoi (a) et fete (e)
    "Ski holiday with a chalet": "mountain-snow", "Hanukkah in the Alps": "flame", "Pesach in the Alps": "wine", "Summer in the Alps": "sun", "Something else": "sparkles",
    "Sukkot": "tent", "Rosh Hashanah and Yom Kippur": "calendar-days", "Purim": "venetian-mask", "Shavuot": "milk", "Another holiday": "sparkles",
    # ou (b)
    "Not chosen yet, minyan first": "map-pin",
    # dates, jour
    "Dates are flexible": "calendar-range", "Dates are fixed": "calendar-check", "Arrive before Shabbat": "sunset", "Can shift 1-2 days if cheaper": "arrow-left-right",
    "Morning": "sunrise", "Afternoon": "sun", "Either": "shuffle",
    # bagages, groupe
    "Large suitcases": "luggage", "Cabin bags only": "backpack", "Skis or snowboards": "snowflake", "Baby seats or boosters": "baby", "Wheelchair or walker": "accessibility",
    "Baby cots": "bed-single", "High chairs": "armchair", "Car seats": "car",
    # logement
    "A private chalet": "house", "Apartments, same residence": "building", "A hotel": "hotel", "Advise me": "lightbulb",
    "Near the Beth Chabad or shul": "landmark", "Ski-in ski-out or near the slopes": "mountain-snow", "Daily cleaning": "spray-can", "Laundry": "washing-machine",
    # repas, cacherout
    "Private chef in the chalet": "chef-hat", "Meals delivered every day": "truck", "Shabbat meals only": "wine", "Breakfast and dinner": "coffee",
    "Groceries ready on arrival": "shopping-basket", "We cook, with delivery": "cooking-pot", "No meals needed": "ban",
    "Chalav Yisrael": "milk", "Pas Yisrael": "croissant", "Glatt / Beit Yosef": "beef", "Chassidic shechita": "drumstick", "Kitniyot-free (Pesach)": "bean-off", "Gluten-free or allergies": "wheat-off",
    # religieux
    "The minyan is essential": "star", "Nice to have": "thumbs-up", "Not needed": "ban",
    "Minyan on Shabbat": "users", "Minyan every day": "calendar-days", "Sefer Torah in the chalet": "scroll-text", "Candles, wine, challot": "flame", "Hot plate and urn": "coffee",
    "Eruv or carrying advice": "fence", "Mikveh nearby": "droplets", "Holiday items (lulav, menorah)": "package-open", "Fast day or holiday": "calendar-clock",
    # transport
    "Flying to Lyon": "plane-landing", "Flying to Geneva": "plane", "Flying to Paris then train": "train-front", "Arriving by car": "car", "Not decided yet": "circle-help",
    "Flights already booked": "circle-check", "Not booked yet": "hourglass",
    "Private airport transfer": "car-front", "A van and driver for the stay": "bus", "A rental car": "key-round", "Help with flights": "plane-takeoff",
    # activites : hiver
    "Ski passes": "ticket", "Rental delivered to the chalet": "package", "We bring our own skis": "backpack", "Ski school for children": "school", "Private instructor": "graduation-cap",
    "Non-skiers in the group": "coffee", "Snowmobile": "gauge", "Snowshoeing": "footprints", "Dog sledding": "dog", "Sledging": "cloud-snow", "Ice rink": "snowflake",
    "Cross-country skiing": "tree-pine", "Helicopter flight": "plane",
    # activites : ete
    "Guided hike": "mountain", "Mountain bike or e-bike": "bike", "Via ferrata": "anchor", "Rafting": "life-buoy", "Canyoning": "droplets", "Lake swimming": "waves",
    "Hot-air balloon": "cloud-sun", "Climbing for children": "biceps-flexed", "Fishing": "fish", "Farm and cheese visit": "tractor",
    # activites : pour tous
    "Paragliding": "wind", "Massage and spa": "bath", "A van and driver on call": "bus",
    # lyon
    "Jewish Lyon walk (2.5 h)": "footprints", "Stopover (3 h) on the way": "hourglass", "Memory: CHRD museum": "library", "Memory: Montluc, Neveh Shalom": "lock",
    "Day trip to Izieu": "bus", "Kosher restaurant tips": "utensils", "Shabbat with a Chabad family": "heart",
    "English": "message-circle", "Hebrew": "message-square-text", "French": "message-square", "Spanish": "message-circle-more",
    # extras
    "Babysitter": "baby", "Fireworks": "sparkles", "A simcha to celebrate": "party-popper", "Photographer or videographer": "camera", "DJ or live music": "music",
    "Flowers and table decoration": "flower-2", "Kids' entertainer": "toy-brick", "Security escort (quoted)": "shield-check", "Reduced mobility": "accessibility",
    # priorites, budget
    "Staying within budget": "scale", "Close to the shul or Beth Chabad": "landmark", "A guaranteed minyan": "users", "A beautiful, well-known resort": "mountain",
    "Great skiing": "mountain-snow", "A private chef": "chef-hat", "Comfort and space": "armchair", "Calm for small children": "baby",
    "Under 10 000 €": "piggy-bank", "10 000 to 25 000 €": "coins", "25 000 to 50 000 €": "wallet", "50 000 to 100 000 €": "banknote", "Over 100 000 €": "gem",
    "Not sure yet, advise us": "circle-help",
    "budget/b:Under 3 000 €": "piggy-bank", "budget/b:3 000 to 10 000 €": "coins", "budget/b:10 000 to 25 000 €": "wallet", "budget/b:Over 25 000 €": "banknote",
    "Flights included in this budget": "plane", "Flights not included": "ban",
    # final
    "No rush": "hourglass", "Within a week please": "calendar-clock", "Urgent, we travel soon": "siren",
    "Booking for someone else": "briefcase", "Someone else decides with me": "handshake",
}
def icone(nom):
    """SVG Lucide en ligne (cache _candidats/lucide/<nom>.svg, telecharge une fois sur unpkg a version figee)."""
    f = os.path.join("_candidats", "lucide", nom + ".svg")
    if not os.path.exists(f):
        raw = urllib.request.urlopen(f"https://unpkg.com/lucide-static@{LUCIDE_V}/icons/{nom}.svg", timeout=30).read().decode("utf-8")
        io.open(f, "w", encoding="utf-8", newline="\n").write(raw)
    raw = io.open(f, encoding="utf-8").read()
    corps = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)
    corps = re.sub(r"\s+", " ", corps).strip()
    return ('<svg class="dm-ic" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{corps}</svg>')
def nom_icone(name, b, en):
    for k in (f"{name}/{b}:{en}", f"{name}:{en}", en):
        if k in ICONES: return ICONES[k]
    raise KeyError(f"pas de pictogramme pour : {name} / {en}")

def esc(s): return html.escape(s, quote=True)
def insec(s): return re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", s).replace(" \u20ac", "\u00a0\u20ac")   # montants jamais coupes
COCHE = '<svg class="dm-coche" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3 8.5l3.2 3.2L13 5" pathLength="16"/></svg>'
BOUGIE = ('<svg class="dm-bougie" viewBox="0 0 24 40" width="22" height="36" aria-hidden="true" focusable="false">'
          '<path class="flamme" d="M12 1c3 4 5 7 5 10a5 5 0 0 1-10 0c0-3 2-6 5-10z"/>'
          '<path class="meche" d="M12 16v4"/><rect class="cire" x="6" y="20" width="12" height="18" rx="1.5"/></svg>')
FLOCON = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"><path d="M8 1v14M1.7 4.5l12.6 7M1.7 11.5l12.6-7M5.5 2.2L8 4.4l2.5-2.2M5.5 13.8L8 11.6l2.5 2.2"/></svg>')
FLOCONS = '<span class="dm-neige" aria-hidden="true">' + "".join(f'<i style="--x:{x}%;--d:{d}ms">{FLOCON}</i>' for x, d in [(6, -300), (22, -1900), (38, -900), (55, -2700), (71, -1400), (86, -500), (95, -3100)]) + "</span>"

def formulaire(lang):
    T = lambda s: t(s, lang)
    E = lambda s: esc(t(s, lang))
    IMG = "../img/" if lang == "en" else "/img/"
    def battr(b): return f' data-b="{b}"' if b else ""
    def sattr(x): return f' data-s="{x}"' if x else ""
    journal = []   # (nom, branches, icone, texte) des choix de l'ecran en cours ; verifie et vide par etape()
    def chips(name, opts, multi=True, b=""):
        """opts : texte EN, ou (texte EN, branches, cle, saison). saison : w = hiver seulement, s = ete seulement."""
        typ = "checkbox" if multi else "radio"
        out = []
        for o in opts:
            en, ob, k, sa = (o, "", "", "") if isinstance(o, str) else (o + ("", "", ""))[:4]
            kk = f' data-k="{k}"' if k else ""
            ic = nom_icone(name, b, en)
            journal.append((name, ob or b, ic, en))
            out.append(f'<label{battr(ob)}{sattr(sa)}><input type="{typ}" name="{name}" value="{E(en)}" data-en="{esc(en)}"{kk}>{icone(ic)}<span>{COCHE}{insec(E(en))}</span></label>')
        return f'<div class="dm-chips"{battr(b)}>' + "".join(out) + "</div>"
    def champ(id_, name, label, typ="text", ph="", b="", extra="", sa=""):
        phh = f' placeholder="{E(ph)}"' if ph else ""
        return f'<div class="dm-champ"{battr(b)}{sattr(sa)}><label for="{id_}">{E(label)}</label><input type="{typ}" id="{id_}" name="{name}"{phh}{extra}></div>'
    def zone(id_, name, label, ph, b=""):
        return f'<div class="dm-champ"{battr(b)}><label for="{id_}">{E(label)}</label><textarea id="{id_}" name="{name}" rows="3" placeholder="{E(ph)}"></textarea></div>'
    def compteur(name, label, b=""):
        return (f'<div class="dm-cpt"{battr(b)}><span class="lib" id="l-{name}">{E(label)}</span><div class="cpt">'
                f'<button type="button" class="moins" aria-label="{E("Fewer")}: {E(label)}">&#8722;</button>'
                f'<span class="cpt-n"><input type="number" id="c-{name}" name="{name}" min="0" max="99" value="0" inputmode="numeric" aria-labelledby="l-{name}"></span>'
                f'<button type="button" class="plus" aria-label="{E("More")}: {E(label)}">+</button></div></div>')
    def ages(name, label, ph):
        return (f'<div class="dm-champ dm-ages cache" data-for="{name}"><label for="c-{name}_ages">{E(label)}</label>'
                f'<input type="text" id="c-{name}_ages" name="{name}_ages" placeholder="{E(ph)}"></div>')
    def etape(id_, titres, aide, corps, cls="", deco="", deco_t="", sur=""):
        """titres : texte EN, ou liste de (texte EN, branches)."""
        seen = {}
        for nm, bb, ic, en in journal:
            for (b2, en2) in seen.get(ic, []):
                assert not (set(bb or "abcdef") & set(b2 or "abcdef")), f"pictogramme {ic} repete dans l'ecran {id_} : {en2} / {en}"
            seen.setdefault(ic, []).append((bb, en))
        journal.clear()
        if isinstance(titres, str): titres = [(titres, "")]
        hs = "".join(f'<h2 tabindex="-1"{battr(b)}>{E(x)}{deco_t}</h2>' for x, b in titres)
        if isinstance(aide, str): aide = [(aide, "")]
        ps = "".join(f'<p{battr(b)}>{E(x)}</p>' for x, b in aide)
        su = f'<p class="dm-sur">{E(sur)}</p>' if sur else ""
        return f'<div class="dm-bloc etape {cls}" id="e-{id_}" data-e="{id_}" role="group"><div class="dm-tete">{su}{hs}{ps}{deco}</div>{corps}</div>\n'

    # ---- intention : grosses tuiles
    def tuile(val, icone, titre, sous, voyage):
        return (f'<label class="dm-tuile"><input type="radio" name="intention" value="{val}" data-voyage="{E(voyage)}">'
                f'<img src="{IMG}des/{icone}.webp" alt="" width="44" height="44" loading="lazy"><b>{E(titre)}</b><span>{E(sous)}</span></label>')
    tuiles = '<div class="dm-tuiles">' + "".join([
        tuile("a", "mountain-snow", "A full stay in the Alps", "Chalet, chef, Shabbat, minyan", "A full stay in the Alps"),
        tuile("b", "house", "I already have my place", "Minyan, meals, Sefer Torah", "Services where we already stay (minyan, Sefer Torah, meals)"),
        tuile("e", "sparkles", "Pesach or a holiday", "A full holiday programme", "Holiday programme (Pesach or other)"),
        tuile("d", "landmark", "A Jewish Lyon tour", "Guided, 2.5 hours", "Jewish Lyon tour"),
        tuile("c", "car", "A van transfer", "From A to B, with a driver", "Van transfer, point A to point B"),
        tuile("f", "message-circle", "Something else", "Tell us in your words", "Something else"),
    ]) + "</div>"
    wa_q1 = f'<p class="dm-wa">{E("Prefer to talk?")} <a href="{JSX[lang]["wa"]}" rel="noopener">{E("Message us on WhatsApp")}</a></p>'
    S = []
    S.append(etape("intention", "What can we do for you?", [],
                   tuiles + wa_q1, "dm-intention", sur="Question 1"))
    # ---- a : sejour complet
    S.append(etape("quoi", "What kind of stay, and where?", "Tick everything that applies. A region is enough.",
                   chips("voyage", [("Ski holiday with a chalet", "", "winter"), ("Hanukkah in the Alps", "", "winter"), ("Pesach in the Alps", "", "winter"), ("Summer in the Alps", "", "summer"), "Something else"]) +
                   champ("lieu-quoi", "lieu", "Resort, town or region you have in mind", ph="Courchevel, Les Deux Alpes, not sure yet")))
    # ---- b : j'ai deja mon logement
    S.append(etape("ou", "Where are you staying?", "The resort and the address of your chalet, apartment or hotel.",
                   champ("lieu-ou", "lieu", "Resort or resorts you are considering", ph="Morzine, Châtel, Les Deux Alpes") +
                   chips("lieu_pas_choisi", ["Not chosen yet, minyan first"]) +
                   champ("adresse", "adresse", "Address or name of the accommodation", ph="Chalet Le Sapin, 12 route du Lac")))
    # ---- e : fete
    S.append(etape("fete", "Which holiday?", "Tick the holiday or holidays, and the place if you know it.",
                   chips("voyage", ["Pesach in the Alps", "Hanukkah in the Alps", "Sukkot", "Rosh Hashanah and Yom Kippur", "Purim", "Shavuot", "Another holiday"]) +
                   champ("lieu-fete", "lieu", "Resort, town or region you have in mind", ph="Courchevel, Les Deux Alpes, not sure yet")))
    # ---- dates (a b d e f)
    S.append(etape("dates", "When do you travel?", "Approximate is fine.",
                   '<div class="dm-duo">' + champ("arrivee", "arrivee", "Arrival", typ="date") + champ("depart", "depart", "Departure", typ="date") + "</div>" +
                   '<p class="dm-nuits" id="dm-nuits" hidden aria-live="polite"></p>' +
                   f'<p class="dm-erreur" id="dm-date-err" role="alert" hidden>{E("The departure is before the arrival.")}</p>' +
                   chips("flexible", ["Dates are flexible", "Dates are fixed", "Arrive before Shabbat", "Can shift 1-2 days if cheaper"])))
    # ---- jour (d : Lyon)
    S.append(etape("jour", "Which day?", [],
                   champ("arrivee-jour", "arrivee", "Date", typ="date") + chips("creneau", ["Morning", "Afternoon", "Either"], multi=False)))
    # ---- van : trajet, quand, bagages
    S.append(etape("trajet", "Where from, and where to?", "Address, airport, station or hotel. A town name is enough.",
                   champ("van_depart", "van_depart", "Pick-up point", ph="Lyon Saint-Exupéry airport") +
                   champ("van_arrivee", "van_arrivee", "Drop-off point", ph="Les Deux Alpes, chalet")))
    S.append(etape("quand", "When?", "Date and pick-up time. Add the flight if you land.",
                   '<div class="dm-duo">' + champ("arrivee-van", "arrivee", "Date", typ="date") + champ("heure", "heure", "Pick-up time", typ="time") + "</div>" +
                   champ("vol-van", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30")))
    S.append(etape("bagages", "Luggage and equipment", "Skis and baby seats change the vehicle we send.",
                   chips("bagages", ["Large suitcases", "Cabin bags only", "Skis or snowboards", "Baby seats or boosters", "Wheelchair or walker"])))
    # ---- groupe (tous)
    S.append(etape("groupe", "Who is coming?", "Children's ages help us choose rooms, ski school and cots.",
                   compteur("adultes", "Adults") + compteur("enfants", "Children") +
                   ages("enfants", "Ages of the children", "9 and 12") +
                   compteur("bebes", "Babies") + ages("bebes", "Ages of the babies", "10 months") +
                   '<div class="dm-mat cache" data-for="bebes">' + chips("bebe_materiel", ["Baby cots", "High chairs", "Car seats"]) + "</div>" +
                   compteur("hommes", "Men over bar mitzvah age, for the minyan", b="abe")))
    # ---- logement (a e)
    S.append(etape("logement", "Where would you like to sleep?", "Pick what suits you. We advise if you are not sure.",
                   chips("logement", ["A private chalet", "Apartments, same residence", "A hotel", "Advise me"]) +
                   champ("chambres", "chambres", "Bedrooms and bathrooms needed", ph="5 bedrooms, 3 bathrooms") +
                   chips("logement_opt", ["Near the Beth Chabad or shul", "Ski-in ski-out or near the slopes", "Daily cleaning", "Laundry"])))
    # ---- repas (a b e)
    S.append(etape("repas", "Which meals do you need?", "Our team cooks or delivers; tell us your standard.",
                   chips("repas", [("Private chef in the chalet", "ae"), "Meals delivered every day", "Shabbat meals only", "Breakfast and dinner",
                                   "Groceries ready on arrival", "We cook, with delivery", ("No meals needed", "", "none")]) +
                   champ("repas_jours", "repas_jours", "Which days?", ph="Shabbat only, or every day from 25 July to 15 August") +
                   champ("allergies", "allergies", "Allergies or special diets", ph="Nut allergy for one child")))
    S.append(etape("cacherout", "Your kashrut standard", "Tick what you keep. We follow it exactly.",
                   chips("cacherout", ["Chalav Yisrael", "Pas Yisrael", "Glatt / Beit Yosef", "Chassidic shechita", "Kitniyot-free (Pesach)", "Gluten-free or allergies"]) +
                   champ("cacherout_detail", "cacherout_detail", "Anything else about kashrut, allergies or preferences", ph="One vegetarian, nut allergy for a child")))
    S.append(etape("religieux", "Shabbat, prayer and holidays", "What do you need on site?",
                   chips("minyan_niveau", ["The minyan is essential", "Nice to have", "Not needed"], multi=False) +
                   chips("religieux", ["Minyan on Shabbat", "Minyan every day", "Sefer Torah in the chalet", "Candles, wine, challot", "Hot plate and urn",
                                       "Eruv or carrying advice", "Mikveh nearby", "Holiday items (lulav, menorah)", "Fast day or holiday"]) +
                   champ("rite", "rite", "Nusach or community, if it matters for the minyan", ph="Chabad, Ashkenaz, Sefarad, Edot HaMizrach"), deco_t=BOUGIE))
    S.append(etape("transport", "Getting there and around", "We organise transfers from the airport and in the resort.",
                   chips("aeroport", ["Flying to Lyon", "Flying to Geneva", "Flying to Paris then train", "Arriving by car", "Not decided yet"], multi=False) +
                   champ("vol_ville", "vol_ville", "City you fly from", ph="New York, Tel Aviv, London") +
                   chips("vols_pris", ["Flights already booked", "Not booked yet"], multi=False) +
                   champ("vol", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30") +
                   chips("transport", ["Private airport transfer", "A van and driver for the stay", "A rental car", "Help with flights"])))
    S.append(etape("ski", "Activities", "Tick what tempts you. We arrange it all on site.",
                   chips("ski", [("Ski passes", "", "", "w"), ("Rental delivered to the chalet", "", "", "w"), ("We bring our own skis", "", "", "w"), ("Ski school for children", "", "", "w"),
                                 ("Private instructor", "", "", "w"), ("Non-skiers in the group", "", "", "w"), ("Snowmobile", "", "", "w"), ("Snowshoeing", "", "", "w"),
                                 ("Dog sledding", "", "", "w"), ("Sledging", "", "", "w"), ("Ice rink", "", "", "w"), ("Cross-country skiing", "", "", "w"), ("Helicopter flight", "", "", "w"),
                                 ("Guided hike", "", "", "s"), ("Mountain bike or e-bike", "", "", "s"), ("Via ferrata", "", "", "s"), ("Rafting", "", "", "s"), ("Canyoning", "", "", "s"),
                                 ("Lake swimming", "", "", "s"), ("Hot-air balloon", "", "", "s"), ("Climbing for children", "", "", "s"), ("Fishing", "", "", "s"),
                                 ("Farm and cheese visit", "", "", "s"), "Paragliding", "Massage and spa", "A van and driver on call"]) +
                   champ("niveau", "niveau", "Ski levels in the group", ph="4 good skiers, 2 beginners, 2 children in ski school", sa="w"), deco=FLOCONS))
    S.append(etape("lyon", "A visit in Lyon?", "Tick the visits that interest you. Tours are held in English, French or Spanish.",
                   chips("lyon", ["Jewish Lyon walk (2.5 h)", "Stopover (3 h) on the way", "Memory: CHRD museum",
                                  "Memory: Montluc, Neveh Shalom", "Day trip to Izieu", "Kosher restaurant tips", "Shabbat with a Chabad family"]) +
                   f'<p class="dm-sous">{E("Language of the visit")}</p>' + chips("langue_visite", ["English", "French", "Spanish"], multi=False) +
                   '<p class="dm-note">' + E("To enter the Grande Synagogue, the community's security team will ask for your names and passports once the tour is confirmed.") + "</p>"))
    S.append(etape("extras", "Extras", "Everything here is optional.",
                   chips("extras", ["Babysitter", "Fireworks", "A simcha to celebrate", "Photographer or videographer", "DJ or live music",
                                    "Flowers and table decoration", "Kids' entertainer", "Security escort (quoted)", "Reduced mobility"]) +
                   zone("message-extras", "message", "Anything else we should know", "Last year we went to Switzerland. We want to be two minutes from the shul.")))
    prio = chips("priorites", ["Staying within budget", "Close to the shul or Beth Chabad", "A guaranteed minyan", "A beautiful, well-known resort",
                                ("Great skiing", "a"), ("A private chef", "ae"), "Comfort and space", "Calm for small children"])
    S.append(etape("budget", "What matters most, and what budget feels right?", "We are advisers: we build the best programme within your budget, never above it.",
                   prio + f'<p class="dm-max" id="dm-max" role="status" hidden>{E("Three at most")}</p>' +
                   f'<p class="dm-sous">{E("Budget")}</p>' +
                   chips("budget", ["Under 10 000 €", "10 000 to 25 000 €", "25 000 to 50 000 €", "50 000 to 100 000 €", "Over 100 000 €", "Not sure yet, advise us"], multi=False, b="aef") +
                   chips("budget", ["Under 3 000 €", "3 000 to 10 000 €", "10 000 to 25 000 €", "Over 25 000 €", "Not sure yet, advise us"], multi=False, b="b") +
                   chips("budget_vols", ["Flights included in this budget", "Flights not included"], multi=False, b="ae")))
    S.append(etape("message", [("Anything else we should know?", "bcd"), ("Tell us what you have in mind", "f")],
                   [("Optional.", "bcd"), ("Write it the way you would say it. We take it from there.", "f")],
                   zone("message-bcd", "message", "Anything else we should know", "Anything that helps: a baby, a late arrival, a special diet.", b="bcd") +
                   zone("message-f", "message", "Tell us what you have in mind", "A bar mitzvah weekend in the Alps for 30 guests", b="f")))
    # ---- final : recapitulatif + contact
    contact = ('<div class="dm-duo">' + champ("nom", "nom", "Your name", extra=' autocomplete="name" required') + champ("ville", "ville", "Where you live", ph="Brooklyn, London, Tel Aviv") + "</div>" +
        f'<div class="dm-champ"><label for="f-tel">{E("WhatsApp number")}</label><div class="tel"><select id="f-indicatif" name="indicatif" aria-label="{E("Country code")}" required>'
        + INDICATIFS.replace("{code}", E("Code")) + '</select><input type="tel" id="f-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="212 555 0100" pattern="[0-9 ().-]{6,16}" required></div></div>' +
        champ("email", "email", "Email (optional)", typ="email", extra=' autocomplete="email"') +
        f'<p class="dm-sous">{E("Language we should answer in")}</p>' + chips("langue", ["English", "Hebrew", "French", "Spanish"], multi=False) +
        f'<p class="dm-sous">{E("How soon?")}</p>' + chips("urgence", ["No rush", "Within a week please", "Urgent, we travel soon"], multi=False) +
        chips("pour_qui", ["Booking for someone else", "Someone else decides with me"]))
    recap = (f'<div class="dm-recap"><img class="dm-hassid" src="{IMG}picto-hassid-vert.svg" alt="" width="200" height="200"><div><h3>{E("Your request so far")}</h3><ul id="dm-recap" class="dm-recap-liste"></ul></div></div>')
    S.append(etape("final", "Almost done", "Check your answers, then tell us how to reach you.", recap + contact +
                   f'<p class="dm-erreur" id="dm-erreur" hidden>{esc(JSX[lang]["err"])}</p>', "dm-contact"))

    wa = JSX[lang]["wa"]
    prog = (f'<div class="dm-prog" id="dm-prog" hidden><div class="dm-prog-txt" id="dm-prog-txt" aria-live="polite"></div>'
            f'<div class="dm-piste" id="dm-piste"><span class="dm-hp" aria-hidden="true"><img src="{IMG}picto-hassid-vert.svg" alt="" width="24" height="34"></span>'
            f'<div class="dm-barre" id="dm-barre-c" role="progressbar" aria-label="{E("Progress")}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="dm-barre"></i></div></div></div>')
    nav = (f'<div class="dm-nav"><button type="button" class="dm-retour" id="dm-back" hidden>{E("Back")}</button>'
           f'<button type="button" class="btn-noir" id="dm-next" hidden>{E("Next")}</button>'
           f'<button type="submit" class="btn-noir" id="dm-send">{esc(JSX[lang]["envoyer"])}</button></div>'
           f'<p class="dm-petit" id="dm-petit"><small>{esc(JSX[lang]["petit"])}</small></p>')
    noscript = f'<noscript><p class="dm-noscript">{E("This form needs JavaScript. Write to us on WhatsApp instead.")} <a href="{wa}" rel="noopener">WhatsApp</a></p></noscript>'
    piege = {"en": "Company", "fr": "Société", "es": "Empresa", "he": "חברה"}[lang]
    return ('<section class="ss wrap demande" id="demande">\n<form id="formDemande" novalidate autocomplete="off">\n'
            f'  <div class="piege" aria-hidden="true"><label for="f-societe">{piege}</label><input type="text" id="f-societe" name="societe" tabindex="-1" autocomplete="off"></div>\n'
            f'  {noscript}\n  {prog}\n  ' + "  ".join(S) + f'  {nav}\n</form>\n</section>')

JS_TPL = r'''<script>
(function(){var f=document.getElementById('formDemande');if(!f)return;
var C=__CFG__;
var KEY='mt-demande-'+C.lang;
var ctrls=[].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(e){return e.name!=='societe'});
ctrls.forEach(function(e){e.scr=e.closest('.etape').getAttribute('data-e')});
var etapes=[].slice.call(f.querySelectorAll('.etape'));
var prog=document.getElementById('dm-prog'),barre=document.getElementById('dm-barre'),barreC=document.getElementById('dm-barre-c'),ptxt=document.getElementById('dm-prog-txt');
var bBack=document.getElementById('dm-back'),bNext=document.getElementById('dm-next'),bSend=document.getElementById('dm-send'),petit=document.getElementById('dm-petit');
var cur='intention',ret='',lastPc=-1,sent=false;
var dl=window.dataLayer=window.dataLayer||[];
var piste=document.getElementById('dm-piste'),mx=document.getElementById('dm-max'),nuitsP=document.getElementById('dm-nuits'),dateErr=document.getElementById('dm-date-err');
function mo(){return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: no-preference)').matches)}
function anim(el,cls){if(!el||!mo())return;el.classList.remove(cls);void el.offsetWidth;el.classList.add(cls);
 var fn=function(ev){if(ev.target!==el)return;el.classList.remove(cls);el.removeEventListener('animationend',fn)};el.addEventListener('animationend',fn)}
function branch(){var r=f.querySelector('input[name="intention"]:checked');return r?r.value:''}
function path(){var b=branch();if(!b)return ['intention'];var p=C.paths[b].slice();
 var r=ctrls.filter(function(e){return e.name==='repas'&&e.checked});
 if(r.length&&r.every(function(e){return e.getAttribute('data-k')==='none'}))p=p.filter(function(x){return x!=='cacherout'});
 return p}
function sync(){var b=branch(),p=path();
 var hs=false,hw=false;ctrls.forEach(function(e){if(e.scr==='quoi'&&e.name==='voyage'&&e.checked){var k=e.getAttribute('data-k');if(k==='summer')hs=true;if(k==='winter')hw=true}});
 [].forEach.call(f.querySelectorAll('[data-s]'),function(n){var s=n.getAttribute('data-s');n.hidden=s==='w'?(hs&&!hw):(hw&&!hs)});
 [].forEach.call(f.querySelectorAll('[data-b]'),function(n){n.hidden=n.getAttribute('data-b').indexOf(b)<0});
 ctrls.forEach(function(e){var ok=p.indexOf(e.scr)>=0;
  if(ok){var n=e.parentNode;while(n&&n!==f){if(n.getAttribute&&((n.getAttribute('data-b')&&n.getAttribute('data-b').indexOf(b)<0)||(n.getAttribute('data-s')&&n.hidden))){ok=false;break}n=n.parentNode}}
  if(ok){var w=e.closest('[data-for]');if(w){var ci=f.querySelector('input[name="'+w.getAttribute('data-for')+'"]');if(!(parseInt(ci.value,10)>0))ok=false}}
  e.disabled=e.name==='intention'?false:!ok});
 [].forEach.call(f.querySelectorAll('.dm-ages,.dm-mat'),function(w){var i=f.querySelector('input[name="'+w.getAttribute('data-for')+'"]');w.classList.toggle('cache',!(parseInt(i.value,10)>0))});
 return p}
function els(n){return ctrls.filter(function(e){return e.name===n&&!e.disabled})}
function raw(n){var a=els(n);if(!a.length)return '';var t=a[0].type;if(t==='checkbox'||t==='radio'){return a.filter(function(e){return e.checked}).map(function(e){return e.value}).join(', ')}return a[0].value.trim()}
function fdate(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return v;try{return new Date(+m[1],+m[2]-1,+m[3],12).toLocaleDateString(C.loc,{day:'numeric',month:'long',year:'numeric'})}catch(x){return v}}
function voyage(){var r=f.querySelector('input[name="intention"]:checked');var a=r?[r.getAttribute('data-voyage')]:[];
 els('voyage').forEach(function(e){if(e.checked&&a.indexOf(e.value)<0)a.push(e.value)});return a.join(', ')}
function val(n){
 if(n==='arrivee'||n==='depart'){var d=raw(n);return d?fdate(d):''}
 if(n==='adultes'||n==='hommes'){var x=parseInt(raw(n),10);return x>0?String(x):''}
 if(n==='enfants'||n==='bebes'){var y=parseInt(raw(n),10);if(!(y>0))return '';var g=raw(n+'_ages');return y+(g?' ('+g+')':'')}
 if(n==='voyage')return voyage();
 if(n==='logement'&&branch()==='b')return C.k.logementB;
 return raw(n)}
function screenOf(k){var e=els(k)[0];return e?e.scr:''}
function recap(an){var ul=document.getElementById('dm-recap');ul.textContent='';var n=0;var go=an&&mo();
 C.lab.forEach(function(kv){var k=kv[0],v=val(k);if(!v||screenOf(k)==='final')return;n++;
  var li=document.createElement('li'),a=document.createElement('span'),b=document.createElement('span');
  if(go){li.className='ap';li.style.setProperty('--i',n-1)}
  a.className='k';a.textContent=kv[1];b.className='v';b.textContent=v;li.appendChild(a);li.appendChild(b);
  var tg=k==='voyage'?'intention':screenOf(k);
  if(tg){var bt=document.createElement('button');bt.type='button';bt.className='dm-edit';bt.textContent=C.t.edit;bt.setAttribute('data-go',tg);li.appendChild(bt)}
  ul.appendChild(li)});
 if(!n){var li=document.createElement('li');li.className='vide';li.textContent=C.t.vide;ul.appendChild(li)}}
function save(){try{sessionStorage.setItem(KEY,JSON.stringify({c:cur,v:ctrls.map(function(e){return e.type==='checkbox'||e.type==='radio'?(e.checked?1:0):e.value})}))}catch(x){}}
function load(){try{var s=JSON.parse(sessionStorage.getItem(KEY)||'null');if(!s||!s.v||s.v.length!==ctrls.length)return;
 ctrls.forEach(function(e,i){if(e.type==='checkbox'||e.type==='radio')e.checked=!!s.v[i];else e.value=s.v[i]});cur=s.c||'intention'}catch(x){}}
function dnum(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);return m?Date.UTC(+m[1],+m[2]-1,+m[3]):null}
function nights(){var a=dnum(raw('arrivee')),d=dnum(raw('depart'));return a!==null&&d!==null?Math.round((d-a)/864e5):null}
function render(an){var p=sync();if(p.indexOf(cur)<0)cur='intention';
 etapes.forEach(function(e){e.hidden=e.getAttribute('data-e')!==cur});
 var i=p.indexOf(cur),last=cur==='final',b=branch();
 bBack.hidden=i<=0;bNext.hidden=last;document.querySelector('.dm-nav').hidden=cur==='intention';bSend.hidden=!last;petit.hidden=!last;var nn=cur==='dates'?nights():null,bad=nn!==null&&nn<0;
 nuitsP.hidden=!(nn!==null&&nn>=1);if(!nuitsP.hidden)nuitsP.textContent=nn===1?C.t.nuit:C.t.nuits.replace('{n}',nn);dateErr.hidden=!bad;
 bNext.disabled=(cur==='intention'&&!b)||(cur==='budget'&&!raw('budget'))||bad;
 prog.hidden=p.length<2;ptxt.textContent=C.t.step.replace('{n}',i+1).replace('{t}',p.length);
 var pc=Math.round((i+1)/p.length*100);barre.style.width=pc+'%';barreC.setAttribute('aria-valuenow',pc);
 piste.style.setProperty('--pc',pc+'%');if(lastPc>=0&&pc!==lastPc)anim(piste.querySelector('.dm-hp img'),'saute');lastPc=pc;
 if(last)recap(an);
 save()}
function show(id,push,focus){var p=sync();if(p.indexOf(id)<0)id='intention';
 var oi=p.indexOf(cur),ni=p.indexOf(id);if(mo()&&oi>=0&&id!==cur)f.setAttribute('data-dir',ni<oi?'back':'fwd');else f.removeAttribute('data-dir');
 cur=id;if(id==='final')ret='';
 render(true);
 dl.push({event:'form_step',step:cur,step_index:p.indexOf(cur)+1,branch:branch()});
 if(push){try{history.pushState({e:cur},'','#e-'+cur)}catch(x){}}
 if(focus){var h=document.querySelector('.etape[data-e="'+cur+'"] h2:not([hidden])');if(h)h.focus({preventScroll:true});
  var r=f.getBoundingClientRect();if(r.top<0||r.top>200)window.scrollTo({top:window.pageYOffset+r.top-90,behavior:'smooth'})}}
function next(){var p=path(),i=p.indexOf(cur);if(ret){var r=ret;ret='';show(r,true,true);return}if(i>=0&&i<p.length-1)show(p[i+1],true,true)}
function back(){ret='';var p=path(),i=p.indexOf(cur);if(i>0)show(p[i-1],true,true)}
bNext.addEventListener('click',next);bBack.addEventListener('click',back);
f.addEventListener('click',function(ev){
 var tu=ev.target.closest&&ev.target.closest('.dm-tuile');if(tu&&ev.target.tagName!=='INPUT'&&cur==='intention'){var ri=tu.querySelector('input');if(ri&&ri.checked){setTimeout(next,120);return}}
 var go=ev.target.closest&&ev.target.closest('.dm-edit');if(go){ret='final';show(go.getAttribute('data-go'),true,true);return}
 var bt=ev.target.closest&&ev.target.closest('.cpt button');if(!bt)return;
 var inp=bt.parentNode.querySelector('input'),v0=parseInt(inp.value,10)||0,plus=bt.className==='plus',v=Math.max(0,Math.min(99,v0+(plus?1:-1)));inp.value=v;
 if(v!==v0&&mo()){var w=inp.parentNode,o=document.createElement('span');o.className='cpt-old';o.setAttribute('aria-hidden','true');o.textContent=v0;w.appendChild(o);
  w.setAttribute('data-sens',plus?'up':'down');anim(inp,'glisse');o.addEventListener('animationend',function(){o.remove()})}
 if(!plus&&v0===0)anim(bt.parentNode,'secoue');
 inp.dispatchEvent(new Event('input',{bubbles:true}))});
function onchg(ev){var t=ev.target;
 if(t.name==='arrivee'&&t.type==='date'){[].forEach.call(f.querySelectorAll('input[name="depart"]'),function(x){x.min=t.value})}
 if(ev.type==='change'&&t.name==='priorites'){mx.hidden=true;
  if(t.checked&&els('priorites').filter(function(e){return e.checked}).length>3){t.checked=false;mx.hidden=false}}
 if(ev.type==='change'&&t.checked&&(t.type==='checkbox'||t.type==='radio')){var lb=t.closest('label');
  if(lb&&lb.classList.contains('dm-tuile'))anim(lb,'dm-anim');else if(lb&&lb.parentNode.classList.contains('dm-chips'))anim(lb,'dm-anim')}
 render();
 if(ev.type==='change'&&t.name==='intention'){dl.push({event:'form_start',branch:t.value});setTimeout(next,mo()?420:220)}}
f.addEventListener('change',onchg);f.addEventListener('input',onchg);
window.addEventListener('popstate',function(ev){var id=ev.state&&ev.state.e;show(id||'intention',false,true)});
f.addEventListener('submit',function(ev){ev.preventDefault();if(sent)return;
 if(cur!=='final'){if(!bNext.disabled)next();return}
 if(f.elements.societe&&f.elements.societe.value){location.href=C.merci;return}
 var nom=val('nom'),tel=val('tel'),ind=val('indicatif');var err=document.getElementById('dm-erreur');
 if(!nom||!tel||!ind){err.hidden=false;err.scrollIntoView({behavior:'smooth',block:'center'});return}
 var parts=[];C.lab.forEach(function(kv){var v=val(kv[0]);if(v)parts.push(kv[1]+': '+v)});
 var dates=[val('arrivee'),val('depart')].filter(Boolean).join(C.k.datesj);
 var pers=val('adultes')?val('adultes')+C.k.adultes:'';if(val('enfants'))pers+=(pers?' + ':'')+val('enfants')+C.k.enfants;if(val('bebes'))pers+=(pers?' + ':'')+val('bebes')+C.k.bebes;
 var payload=JSON.stringify({tour:C.k.tour+(val('voyage')||C.k.none),dates:dates,personnes:pers,langue:val('langue'),nom:nom,contact:(ind+' '+tel.replace(/[^0-9]/g,'')).trim()+(val('email')?' / '+val('email'):''),message:parts.join(' | '),page:location.pathname,params:location.search});
 try{var u=window.MISHPACHA_ENDPOINT||'ENDPOINT_APPS_SCRIPT_A_POSER';if(navigator.sendBeacon){navigator.sendBeacon(u,new Blob([payload],{type:'text/plain;charset=UTF-8'}))}else{fetch(u,{method:'POST',mode:'no-cors',keepalive:true,body:payload})}}catch(e){}
 try{sessionStorage.removeItem(KEY)}catch(e){}
 dl.push({event:'generate_lead',branch:branch(),budget:val('budget')});
 sent=true;
 if(mo()){bSend.disabled=true;bSend.textContent='';var im=new Image();im.src=C.img+'picto-hassid-vert.svg';im.alt='';im.width=22;im.height=30;im.className='dm-marche';
  bSend.appendChild(im);bSend.appendChild(document.createTextNode(' '+C.t.sending));setTimeout(function(){location.href=C.merci},600)}
 else location.href=C.merci});
function prefill(){var q;try{q=new URLSearchParams(location.search)}catch(x){return}
 function s(k){var v=q.get(k);return v?v.replace(/[\u0000-\u001f<>]/g,'').trim().slice(0,80):''}
 function n(k){var v=(q.get(k)||'').trim();return /^\d{1,2}$/.test(v)?parseInt(v,10):null}
 function d(k){var v=s(k),m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return '';var x=new Date(Date.UTC(+m[1],+m[2]-1,+m[3]));
  return x.getUTCFullYear()===+m[1]&&x.getUTCMonth()===+m[2]-1&&x.getUTCDate()===+m[3]?v:''}
 function fill(name,v){ctrls.forEach(function(e){if(e.name===name)e.value=v})}
 var i=s('i').toLowerCase(),r=/^[a-f]$/.test(i)?ctrls.filter(function(e){return e.name==='intention'&&e.value===i})[0]:null;
 if(r){r.checked=true;cur=path()[1]||'intention';dl.push({event:'form_start',branch:i})}
 var l=s('lieu');if(l)fill('lieu',l);
 var a=d('arrivee'),b=d('depart');if(a)fill('arrivee',a);if(b)fill('depart',b);if(a)ctrls.forEach(function(e){if(e.name==='depart')e.min=a});
 ['adultes','enfants','bebes'].forEach(function(k){var v=n(k);if(v!==null)fill(k,String(v))});
 var vy=s('voyage').toLowerCase();if(vy)ctrls.forEach(function(e){if(e.name==='voyage'&&(e.getAttribute('data-en')||e.value).toLowerCase()===vy)e.checked=true})}
load();prefill();f.classList.add('js');show(cur,false,false);try{history.replaceState({e:cur},'')}catch(x){}
})();
</script>'''

def js(lang):
    T = lambda s: t(s, lang)
    lab = dict(LAB[lang]); i = LANGS.index(lang)
    for k, v in LAB_NEW.items(): lab[k] = v[i]
    cfg = {"lang": lang, "loc": LOCALE[lang], "merci": MERCI[lang], "paths": PATHS, "img": "../img/" if lang == "en" else "/img/",
           "lab": [[k, lab[k]] for k in LAB_ORDER],
           "k": {"tour": JSX[lang]["tour"], "none": JSX[lang]["none"], "datesj": JSX[lang]["datesj"], "adultes": JSX[lang]["adultes"], "enfants": JSX[lang]["enfants"],
                 "bebes": JSX[lang]["bebes"], "logementB": T("Already booked, I need services only")},
           "t": {"step": T("Step {n} of {t}"), "edit": T("Edit"), "vide": T("Nothing filled in yet."),
                 "nuits": T("{n} nights"), "nuit": T("1 night"), "sending": T("Sending…")}}
    assert set(LAB_ORDER) >= set(LAB[lang]), set(LAB[lang]) - set(LAB_ORDER)
    return JS_TPL.replace("__CFG__", json.dumps(cfg, ensure_ascii=False))

# ---------------------------------------------------------------- CSS (bloc delimite dans styles.css)
CSS_A, CSS_Z = "/* ===DEMANDE-ETAPES=== */", "/* ===/DEMANDE-ETAPES=== */"
CSS = CSS_A + """
.etape[hidden],[data-b][hidden],[data-s][hidden],.cache{display:none!important}
.demande .piege{position:absolute;left:0;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
.demande form{max-width:760px}
.dm-prog,.dm-nav,.dm-petit{display:none}
.demande form.js .dm-prog{display:grid;gap:8px}
.demande form.js .dm-prog[hidden]{display:none}
.demande form.js .dm-nav{display:flex}
.demande form.js .dm-petit{display:block}
.demande form.js .dm-petit[hidden]{display:none}
.dm-prog-txt{font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.dm-barre{height:8px;border-radius:999px;background:rgba(28,27,31,.12);overflow:hidden}
.dm-barre i{display:block;height:100%;width:0;background:var(--vert);border-radius:999px;transition:width .25s}
.dm-bloc legend h2:focus{outline:none}
.etape{display:block}
.etape > .dm-tete{margin:0 0 20px}
.etape > .dm-tete h2{font-size:26px}
.etape > .dm-tete p{margin-top:4px;font-size:14px;opacity:.7}
.etape > * + *{margin-top:16px}
.dm-noscript{padding:14px 18px;border-radius:15px;background:var(--jaune);font-weight:600}
.dm-sous{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin:6px 0 -6px}
.dm-intention{background:var(--blanc);border-radius:18px;padding:16px 14px 14px}
.dm-intention > .dm-tete{margin-bottom:12px}
.dm-sur{margin:0;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--vert);opacity:1}
.etape > .dm-tete p.dm-sur{margin-top:0;font-size:12px;opacity:1}
.dm-intention > .dm-tete h2{margin:4px 0 0;font-family:var(--titre);font-weight:700;font-size:23px;line-height:1.15}
.dm-tuiles{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.dm-tuile{position:relative;display:grid;gap:3px;align-content:start;min-height:112px;padding:10px 12px;border-radius:14px;border:1px solid rgba(28,27,31,.2);background:var(--creme);cursor:pointer}
.dm-tuile input{position:absolute;opacity:0;width:0;height:0}
.dm-tuile img{width:44px;height:44px;object-fit:contain}
.dm-tuile b{font-weight:700;font-size:15px;line-height:1.2}
.dm-tuile span{font-size:12.5px;line-height:1.3;opacity:.7}
.dm-tuile:has(input:checked){background:var(--jaune);border-color:var(--jaune)}
.dm-tuile:has(input:focus-visible){outline:3px solid var(--vert-c);outline-offset:2px}
.dm-wa{margin:14px 0 4px;text-align:center;font-size:14px}
.dm-wa a{color:var(--encre);font-weight:600}
.demande-hero{padding:14px 0 0}
.demande-hero ~ .ss.demande{margin-top:16px;padding-top:0}
.demande-hero h1{margin:6px 0 0;font-family:var(--titre);font-weight:700;font-size:36px;line-height:1.05;letter-spacing:-.01em}
.demande-hero h1 span{color:var(--vert)}
.dm-promesse{margin:10px 0 0;font-size:16px;line-height:1.45;max-width:36em}
.dm-puces{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 0;padding:0;list-style:none}
.dm-puces li{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;background:var(--beige);border-radius:999px;padding:5px 10px}
.dm-puces svg{width:14px;height:14px;fill:none;stroke:var(--vert);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.dm-hassid{display:block;width:200px;height:auto;margin:0 auto}
.dm-cpt{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:8px 0;border-bottom:1px solid rgba(28,27,31,.1)}
.dm-cpt .lib{font-weight:600;font-size:16px;line-height:1.3}
.cpt{display:flex;align-items:center;gap:6px;direction:ltr;flex:none}
.cpt button{width:48px;height:48px;border-radius:50%;border:1px solid rgba(28,27,31,.25);background:var(--creme);font-size:24px;line-height:1;cursor:pointer;color:var(--encre);padding:0}
.cpt button:hover{background:var(--jaune)}
.cpt input{width:56px;text-align:center;border:0;background:transparent;padding:0;font:inherit;font-size:22px;font-weight:600;color:var(--encre);-moz-appearance:textfield;appearance:textfield}
.cpt input::-webkit-outer-spin-button,.cpt input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.dm-champ input[type=date],.dm-champ input[type=time]{min-height:50px}
.dm-ages{padding-top:4px}
.dm-recap{display:grid;gap:18px;align-items:center}
.dm-recap h3{font-family:var(--titre);font-weight:400;font-size:22px;margin-bottom:8px}
.dm-recap-liste{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.dm-recap-liste li{display:grid;grid-template-columns:1fr auto;gap:0 12px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(28,27,31,.12)}
.dm-recap-liste .k{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;opacity:.7;grid-column:1}
.dm-recap-liste .v{grid-column:1;font-size:16px;line-height:1.35}
.dm-recap-liste .dm-edit{grid-column:2;grid-row:1 / span 2;min-height:44px;min-width:44px;padding:0 14px;border-radius:999px;border:1px solid rgba(28,27,31,.25);background:var(--blanc);font:inherit;font-size:14px;font-weight:600;cursor:pointer;color:var(--encre)}
.dm-recap-liste .dm-edit:hover{background:var(--jaune)}
.dm-recap-liste .vide{display:block;opacity:.7}
.dm-contact .dm-recap{padding-bottom:18px}
.dm-nav{max-width:760px;margin:80px auto 0;justify-content:space-between;align-items:center;gap:14px}
.dm-retour{min-height:54px;padding:0 28px;border-radius:999px;border:1px solid var(--encre);background:transparent;font:inherit;font-size:16px;font-weight:600;color:var(--encre);cursor:pointer}
.dm-retour:hover{background:var(--jaune);border-color:var(--jaune)}
.dm-nav .btn-noir{min-height:54px;padding:0 36px;font-size:16px;margin-inline-start:auto}
.dm-nav .btn-noir:disabled{opacity:.35;cursor:default}
.dm-nav [hidden]{display:none!important}
.demande form.js .dm-nav[hidden]{display:none}
.dm-petit{max-width:760px;margin:80px auto 0;text-align:center;font-size:13px;opacity:.7}
.demande{padding-bottom:80px}
.dm-note{font-size:14px;line-height:1.45;padding:12px 16px;border-radius:15px;background:var(--creme);border:1px solid rgba(28,27,31,.15)}
.dm-nuits{font-weight:600;font-size:15px}
.dm-max{font-size:14px;font-weight:600;color:var(--rouge)}
.dm-erreur[hidden],.dm-nuits[hidden],.dm-max[hidden]{display:none}
.dm-coche,.dm-bougie,.dm-neige,.dm-hp{display:none}
.dm-coche{fill:none;stroke:var(--encre);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.cpt-n{display:block;position:relative;width:56px;overflow:hidden}
.cpt-n input{display:block;width:100%}
.dm-tete{position:relative}
@media (prefers-reduced-motion: no-preference){
  /* 1. hassid sur la barre */
  .demande form.js .dm-piste{position:relative;padding-top:38px}
  .dm-hp{display:block;position:absolute;bottom:calc(100% - 38px + 6px);left:var(--pc,0%);transform:translateX(-100%);transition:left .4s cubic-bezier(.2,.8,.2,1);line-height:0;pointer-events:none}
  .dm-hp img{display:block;height:34px;width:auto}
  [dir=rtl] .dm-hp{left:auto;right:var(--pc,0%);transform:translateX(100%);transition-property:right}
  [dir=rtl] .dm-hp img{transform:scaleX(-1)}
  .dm-hp img.saute{animation:dm-saute .4s ease-out}
  @keyframes dm-saute{0%,50%,100%{translate:0 0}25%,75%{translate:0 -3px}}
  /* 2. tuiles */
  .dm-tuile{transition:transform .2s ease-out,box-shadow .2s ease-out,background-color .2s}
  @media (hover:hover) and (pointer:fine){.dm-tuile:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(28,27,31,.12)}}
  .dm-tuile.dm-anim img{animation:dm-rebond .35s ease-out}
  @keyframes dm-rebond{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
  /* 3. cases */
  .dm-chips label{transition:background-color .2s,border-color .2s}
  .dm-chips label.dm-anim{animation:dm-pop .25s cubic-bezier(.2,.8,.2,1)}
  @keyframes dm-pop{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
  .dm-coche{display:inline-block;width:0;height:16px;margin-inline-end:0;stroke-dasharray:16;stroke-dashoffset:16;transition:stroke-dashoffset .25s ease-out .05s,width .2s ease-out,margin .2s ease-out}
  .dm-chips label:has(input:checked) .dm-coche{width:16px;margin-inline-end:6px;stroke-dashoffset:0}
  .dm-chips label{overflow:hidden}
  .dm-chips span{display:inline-flex;align-items:center}
  /* 4. compteurs */
  .cpt-old{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:600;color:var(--encre);pointer-events:none}
  .cpt-n[data-sens=up] .cpt-old{animation:dm-sort-haut .2s ease-out forwards}
  .cpt-n[data-sens=up] input.glisse{animation:dm-entre-bas .2s ease-out}
  .cpt-n[data-sens=down] .cpt-old{animation:dm-sort-bas .2s ease-out forwards}
  .cpt-n[data-sens=down] input.glisse{animation:dm-entre-haut .2s ease-out}
  @keyframes dm-sort-haut{to{transform:translateY(-100%);opacity:0}}
  @keyframes dm-sort-bas{to{transform:translateY(100%);opacity:0}}
  @keyframes dm-entre-bas{from{transform:translateY(100%);opacity:0}}
  @keyframes dm-entre-haut{from{transform:translateY(-100%);opacity:0}}
  .cpt.secoue{animation:dm-secoue .25s ease-out}
  @keyframes dm-secoue{0%,100%{transform:translateX(0)}20%{transform:translateX(-5px)}45%{transform:translateX(5px)}70%{transform:translateX(-3px)}}
  /* 5. bougie et flocons */
  .dm-bougie{display:inline-block;vertical-align:-6px;margin-inline-start:10px;overflow:visible}
  .dm-bougie .cire{fill:var(--blanc);stroke:var(--encre);stroke-width:1.5}
  .dm-bougie .meche{stroke:var(--encre);stroke-width:1.5;stroke-linecap:round}
  .dm-bougie .flamme{fill:var(--jaune);stroke:var(--encre);stroke-width:1;transform-box:fill-box;transform-origin:50% 100%;animation:dm-vacille 2.5s ease-in-out infinite}
  @keyframes dm-vacille{0%,100%{opacity:1;transform:scale(1) rotate(0)}30%{opacity:.82;transform:scale(.93,1.06) rotate(-3deg)}60%{opacity:.95;transform:scale(1.05,.95) rotate(2deg)}80%{opacity:.86;transform:scale(.96,1.04) rotate(-1deg)}}
  .dm-neige{display:block;position:absolute;inset:0;overflow:hidden;pointer-events:none}
  .dm-neige i{position:absolute;top:-20px;left:var(--x);opacity:0;line-height:0;animation:dm-tombe 3.6s linear var(--d) infinite}
  .dm-neige svg{fill:none;stroke:var(--vert);stroke-width:1.2;stroke-linecap:round}
  [dir=rtl] .dm-neige i{left:auto;right:var(--x)}
  @keyframes dm-tombe{0%{opacity:0;transform:translateY(0) rotate(0)}12%{opacity:.75}85%{opacity:.75}100%{opacity:0;transform:translateY(120px) rotate(200deg)}}
  /* 6. passage d'ecran */
  .demande form[data-dir=fwd]{--dx:24px}
  .demande form[data-dir=back]{--dx:-24px}
  [dir=rtl] .demande form[data-dir=fwd]{--dx:-24px}
  [dir=rtl] .demande form[data-dir=back]{--dx:24px}
  .demande form[data-dir] .etape:not([hidden]){animation:dm-entre .3s ease-out backwards}
  @keyframes dm-entre{from{opacity:0;transform:translateX(var(--dx))}}
  /* 7. recapitulatif */
  .dm-recap-liste li.ap{animation:dm-ligne .3s ease-out calc(var(--i)*30ms) backwards}
  @keyframes dm-ligne{from{opacity:0;transform:translateY(6px)}}
  /* 8. envoi */
  .dm-nav .btn-noir img.dm-marche{display:inline-block;vertical-align:middle;height:30px;width:auto;margin-inline-end:6px;transform-origin:50% 100%;animation:dm-marche .3s ease-in-out infinite alternate}
  @keyframes dm-marche{from{transform:rotate(-6deg) translateY(0)}to{transform:rotate(6deg) translateY(-3px)}}
  /* 9. page merci : le hassid danse a l'ouverture */
  img.hassid-merci{transform-origin:50% 100%;animation:dm-danse 3.2s ease-in-out infinite}
  @keyframes dm-danse{0%,60%,100%{transform:rotate(0) translateY(0)}7.5%,37.5%{transform:rotate(-6deg) translateY(-6px)}15%,45%{transform:rotate(0) translateY(0)}22.5%,52.5%{transform:rotate(6deg) translateY(-6px)}30%{transform:rotate(0) translateY(0)}}
  [dir=rtl] img.hassid-merci{animation-name:dm-danse-rtl}
  @keyframes dm-danse-rtl{0%,60%,100%{transform:scaleX(-1) rotate(0) translateY(0)}7.5%,37.5%{transform:scaleX(-1) rotate(-6deg) translateY(-6px)}15%,45%{transform:scaleX(-1) rotate(0) translateY(0)}22.5%,52.5%{transform:scaleX(-1) rotate(6deg) translateY(-6px)}30%{transform:scaleX(-1) rotate(0) translateY(0)}}
}
@media (min-width:700px){
  .demande-hero{padding-top:24px}
  .demande-hero ~ .ss.demande{margin-top:28px}
  .demande-hero ~ .ss.demande form{margin-inline:0}
  .demande-hero h1{font-size:48px}
  .dm-promesse{font-size:19px}
  .dm-intention{padding:24px 24px 20px}
  .dm-intention > .dm-tete h2{font-size:28px}
  .dm-tuile{min-height:128px;padding:16px;gap:6px}
  .dm-tuile b{font-size:17px}
  .dm-tuile span{font-size:14px}
  .dm-recap{grid-template-columns:200px 1fr;gap:28px}
}
@media (min-width:900px){
  .dm-tuiles{grid-template-columns:repeat(3,1fr);gap:12px}
}
@media (max-width:699px){
  /* telephone (Moshe, 15/10 : « il faut scroller pour l'utiliser ») : en-tete reduit, progression en haut, Retour et Suivant toujours sous le pouce */
  body:has(#formDemande) .pratique-hero{padding-bottom:0}
  .demande form.js .dm-prog{position:sticky;top:0;z-index:19;background:var(--creme);padding:10px 0 8px;margin:0 -16px;padding-inline:16px}
  .demande form.js .dm-nav{position:sticky;bottom:0;z-index:20;margin:20px -16px 0;padding:12px 16px calc(12px + env(safe-area-inset-bottom));background:var(--creme);border-top:1px solid rgba(28,27,31,.12)}
  .dm-nav .btn-noir,.dm-retour{min-height:52px}
  .dm-nav .btn-noir{flex:1;padding:0 20px}
  .dm-petit{margin-top:16px}
  .etape > .dm-tete{margin-bottom:14px}
  .etape > .dm-tete h2{font-size:23px}
  body:has(#formDemande) .wa-flottant{display:none!important}
  .demande{padding-bottom:24px}
}
/* cases en cartes a pictogramme (Moshe 15/10 : « il ne faut pas avoir besoin de lire pour comprendre ») : picto 26 px en haut a gauche (a droite en RTL), mot dessous, case 18 px dans le coin oppose */
.demande .dm-chips{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.demande .dm-chips label{display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:8px;min-height:84px;padding:12px;border-radius:14px;line-height:1.2;font-size:15px;font-weight:500;text-align:start;overflow:hidden}
.demande .dm-chips .dm-ic{flex:none;display:block;width:26px;height:26px;color:var(--vert);transition:color .15s}
.demande .dm-chips label:has(input:checked) .dm-ic{color:var(--encre)}
.demande .dm-chips span{display:block}
.demande .dm-chips label::before{content:"";position:absolute;inset-inline-end:12px;top:16px;width:18px;height:18px;border:1.5px solid rgba(28,27,31,.45);border-radius:6px;background:var(--blanc) center/12px no-repeat;transition:background-color .15s,border-color .15s}
.demande .dm-chips label:has(input[type=radio])::before{border-radius:50%}
.demande .dm-chips label:has(input:checked)::before{background-color:var(--encre);border-color:var(--encre);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M3 8.2l3.2 3.2L13 4.6' fill='none' stroke='%23FCDE73' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")}
.demande .dm-chips .dm-coche{display:none!important}
.demande .dm-chips input:checked ~ span{font-weight:600}
@media (min-width:700px){.demande .dm-chips{grid-template-columns:repeat(3,1fr)}}
""" + CSS_Z

def update_css():
    c = open("styles.css", encoding="utf-8").read()
    if CSS_A in c:
        a = c.index(CSS_A); z = c.index(CSS_Z) + len(CSS_Z)
        c = c[:a] + CSS + c[z:]
    else:
        c = c.rstrip("\n") + "\n" + CSS + "\n"
    io.open("styles.css", "w", encoding="utf-8", newline="\n").write(c)

def merci_danse():
    """Pose la classe de la danse sur le hassid des 4 pages /merci/ (idempotent)."""
    for p in ("merci/index.html", "fr/merci/index.html", "es/merci/index.html", "he/merci/index.html"):
        s = io.open(p, encoding="utf-8").read()
        n = s.replace('class="hassid-grand" src=', 'class="hassid-grand hassid-merci" src=')
        if n != s: io.open(p, "w", encoding="utf-8", newline="\n").write(n)
        assert "hassid-merci" in n, p
    print("ok merci (4 langues)")

# ---------------------------------------------------------------- ecriture
if __name__ == "__main__":
    update_css()
    merci_danse()
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener", "document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
    f = f.replace('<script src="/config.js"></script>', '<script src="/config.js"></script>\n' + js("en"), 1)
    os.makedirs("plan-your-trip", exist_ok=True)
    io.open("plan-your-trip/index.html", "w", encoding="utf-8", newline="\n").write(h + "<main>\n" + hero("en") + "\n\n" + formulaire("en") + "\n</main>" + f)
    print("ok plan-your-trip")
    for lang in ("fr", "es", "he"):
        p = f"{lang}/plan-your-trip/index.html"
        s = io.open(p, encoding="utf-8").read()
        a = s.index('<section class="pratique-hero'); b = s.index("</section>", a) + len("</section>")
        s = s[:a] + hero(lang) + s[b:]
        a = s.index('<section class="ss wrap demande" id="demande">'); b = s.index("</section>", a) + len("</section>")
        s = s[:a] + formulaire(lang) + s[b:]
        s, n = re.subn(r"<script>\n\(function\(\)\{var f=document.getElementById\('formDemande'\);if\(!f\)return;.*?</script>", lambda m: js(lang), s, count=1, flags=re.S)
        assert n == 1, p
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("ok", p)
