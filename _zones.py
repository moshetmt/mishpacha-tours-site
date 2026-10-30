# -*- coding: utf-8 -*-
"""Bandeau vert et baseline du pied selon la zone de la page (decision operateur du 13/10 : « adapte en fonction de la zone »).
  python _zones.py   : apres les builds et les traductions, AVANT _decor.py. Idempotent.
Zones : alpes (stations, chalet, services, ski, ete), general (accueil, about, contact, legal), lyon (tout le reste).
Les liens « Tours » et « Your guide » des menus (ancres /#tours et /#guide de l'ancien accueil) partent vers /jewish-lyon-tours/."""
import glob, io, os, re

LANGS = ("fr", "es", "he")
ALPES = {"alps", "kosher-alpe-dhuez", "kosher-annecy", "kosher-chalet-les-deux-alpes", "kosher-chamonix", "kosher-courchevel",
         "kosher-grenoble", "kosher-chalets", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-chalet-val-thorens", "kosher-la-plagne", "kosher-les-arcs", "kosher-les-deux-alpes", "kosher-megeve", "kosher-services-french-alps",
         "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps", "kosher-val-disere", "kosher-val-thorens",
         "kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana", "kosher-cervinia", "kosher-verbier", "kosher-courmayeur", "kosher-cortina",
         "lyon-gateway-to-the-alps-kosher", "summer-in-the-alps-jewish-families", "flights-to-lyon"}
GENERAL = {"", "plan-your-trip", "kosher-villa-saint-tropez", "kosher-van-transfers", "about", "contact", "privacy", "terms", "credits", "merci", "jewish-life-around-lyon"}

BASELINE = {"alpes": "Kosher Stays in the Alps", "general": "Kosher Holidays in the Alps and Lyon", "lyon": "Jewish Tours of Lyon"}
# Pages hiver (noir et or, Moshé 19/10) : la baseline nomme le partenaire, notre logo reste. La liste vit dans _kit_wp.py (HIVER).
# _kit_wp importe _zones (menu Chalets), donc pas d'import en retour : on lit HIVER et PIED_WP dans le texte du script.
def _liste_hiver():
    src = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_kit_wp.py"), encoding="utf-8").read()
    ns = {}
    for nom in ("STATIONS_SANS_CHALET", "HIVER", "PIED_WP"):
        m = re.search(r"^%s = (.*?)(?=^\S)" % nom, src, flags=re.S | re.M)
        exec(nom + " = " + m.group(1).split("  #")[0].strip(), ns)
    return set(ns["HIVER"]), ns["PIED_WP"]
HIVER_WP, PIED_WP = _liste_hiver()
BANDEAU = {  # (texte, lien)
    "alpes": {"en": ("Strictly kosher stays in the Alps, one day-by-day programme. ", "Describe your stay."),
              "fr": ("Séjours strictement casher dans les Alpes, un programme jour par jour. ", "Décrivez votre séjour."),
              "es": ("Estancias estrictamente kosher en los Alpes, un programa día a día. ", "Describa su estancia."),
              "he": ("חופשות כשרות באלפים, תוכנית מפורטת יום אחר יום. ", "ספרו לנו על החופשה.")},
    "general": {"en": ("Strictly kosher holidays in the Alps and Lyon, shomer shabbat. ", "Describe your stay."),
                "fr": ("Séjours strictement casher dans les Alpes et à Lyon, shomer shabbat. ", "Décrivez votre séjour."),
                "es": ("Vacaciones estrictamente kosher en los Alpes y Lyon, shomer Shabat. ", "Describa su estancia."),
                "he": ("חופשות כשרות באלפים ובליון. שומר כשרות · שומר שבת. ", "ספרו לנו על החופשה.")},
    "lyon": {"en": ("Private tours, Sunday to Friday morning. ", "Check a date on WhatsApp."),
             "fr": ("Visites privées, du dimanche au vendredi matin. ", "Vérifier une date sur WhatsApp."),
             "es": ("Visitas privadas, de domingo a viernes por la mañana. ", "Consulte una fecha por WhatsApp."),
             "he": ("סיורים פרטיים, מיום ראשון עד יום שישי בבוקר. ", "בדיקת תאריך בוואטסאפ.")},
}

# Menu a 5 entrees (25/10, decisions Moshe) : Chalets, Resorts, Chef & Shabbat, Summer, Jewish Lyon + bouton « Plan your trip ».
# Panneau telephone plein ecran : les 5 entrees avec une ligne de sous-titre, le bouton, WhatsApp, e-mail, langues en codes.
# Les 17 stations et les chalets ne sont plus dans le panneau : ils vivent dans le pied (liens texte, maillage) et dans les pages.
ENTREES = {"en": ("Chalets", "Resorts", "Chef & Shabbat", "Summer", "Jewish Lyon", "Plan your trip"),
           "fr": ("Chalets", "Stations", "Chef & Chabbat", "Été", "Visite juive à Lyon", "Personnaliser mon séjour"),
           "es": ("Chalets", "Estaciones", "Chef y Shabat", "Verano", "Lyon judío", "Planificar mi viaje"),
           "he": ("צ'אלות", "אתרי סקי", "שף ושבת", "קיץ", "ליון היהודית", "לתכנן את הטיול")}
SOUS = {"en": ("Five private chalets, strictly kosher", "Eighteen resorts in France, Switzerland and Italy", "Private chef, delivered meals, minyan, transfers", "Villa in Saint-Tropez, the lakes, the mountains", "The guided visit and the Jewish guide to Lyon"),
        "fr": ("Des chalets privés, strictement casher", "Dix-huit stations en France, en Suisse et en Italie", "Chef privé, repas livrés, minyan, transferts", "Villa à Saint-Tropez, les lacs, la montagne", "La visite guidée et le guide juif de Lyon"),
        "es": ("Chalets privados, estrictamente kosher", "Dieciocho estaciones en Francia, Suiza e Italia", "Chef privado, comidas entregadas, minyán, traslados", "Villa en Saint-Tropez, los lagos, la montaña", "La visita guiada y la guía del Lyon judío"),
        "he": ("צ'אלות פרטיות, בהקפדה על כשרות", "שמונה־עשר אתרי סקי בצרפת, בשווייץ ובאיטליה", "שף פרטי, ארוחות משלוח, מניין, הסעות", "וילה בסן־טרופה, האגמים, ההרים", "הסיור המודרך והמדריך ליהדות ליון")}
URLS = ("/kosher-chalets/", "/alps/", "/kosher-services-french-alps/", "/summer-in-the-alps-jewish-families/", "/jewish-lyon-tours/")
PIED_PAN = {"en": ("Same-day reply. Never on Shabbat.", "contact@mishpachatours.com"), "fr": ("Réponse le jour même. Jamais pendant Chabbat.", "contact@mishpachatours.com"),
            "es": ("Respuesta el mismo día. Nunca en Shabat.", "contact@mishpachatours.com"), "he": ("מענה באותו יום. לעולם לא בשבת.", "contact@mishpachatours.com")}
WA_HE = "דברו איתנו בוואטסאפ"
CHALETS = {"en": ("Chalets", "See the chalets", (("Les Deux Alpes", "6 + 1 bedrooms · 2 min from the slopes"), ("Les Deux Alpes · Slope Chalet", "6 bedrooms · skis on at the door"), ("Courchevel", "5 suites · heated pools"), ("Near Megève", "10 twin bedrooms · Mont Blanc"), ("Val Thorens", "3 en-suite bedrooms · ski in ski out"))),
           "fr": ("Chalets", "Voir les chalets", (("Les Deux Alpes", "6 + 1 chambres · à 2 min des pistes"), ("Les Deux Alpes · chalet des pistes", "6 chambres · skis aux pieds"), ("Courchevel", "5 suites · piscines chauffées"), ("Près de Megève", "10 chambres twin · Mont Blanc"), ("Val Thorens", "3 chambres en suite · skis aux pieds"))),
           "es": ("Chalets", "Ver los chalets", (("Les Deux Alpes", "6 + 1 habitaciones · a 2 min de las pistas"), ("Les Deux Alpes · chalet de las pistas", "6 habitaciones · esquís puestos en la puerta"), ("Courchevel", "5 suites · piscinas climatizadas"), ("Cerca de Megève", "10 habitaciones twin · Mont Blanc"), ("Val Thorens", "3 habitaciones con baño · esquí a pie de puerta"))),
           "he": ("צ'אלות", "לראות את הצ'אלות", (("לה דז אלפ", "6 + 1 חדרים · 2 דק' מהמסלולים"), ("לה דז אלפ · צ'אלה המסלולים", "6 חדרים · מגלשיים בדלת"), ("קורשבל", "5 סוויטות · בריכות מחוממות"), ("ליד מג'ב", "10 חדרי טווין · מון בלאן"), ("ואל טורנס", "3 חדרי שינה עם חדר רחצה · סקי מהדלת")))}
# 21/10 : vignettes WebP de 336 px (img/chalet/min/, fabriquées par _images_legeres.py) au lieu des JPG pleine taille (2 032 Ko téléchargés par le tiroir mobile)
CH_URL = (("kosher-chalet-les-deux-alpes", "/img/chalet/min/wp-ext-bleu-336.webp"), ("kosher-slope-chalet-les-deux-alpes", "/img/chalet/min/slope-facade-336.webp"), ("kosher-chalet-courchevel", "/img/chalet/min/courchevel-ext-336.webp"), ("kosher-chalet-megeve", "/img/chalet/min/megeve-n0-apt-sejour-336.webp"), ("kosher-chalet-val-thorens", "/img/chalet/min/valthorens-exterieur-neige-336.webp"))

def chalets_html(lang, pre):
    lib, tous, items = CHALETS[lang]
    vign = "".join(f'<a class="nav-ch-v" href="{pre}/{u}/"><img src="{img}" alt="" width="96" height="64" loading="lazy"><span><b>{n}</b>{d}</span></a>'
                   for (u, img), (n, d) in zip(CH_URL, items))
    return (f'<div class="nav-ch"><a class="nav-ch-lien" href="{pre}/kosher-chalets/">{lib}</a>'
            f'<div class="nav-ch-menu">{vign}<a class="nav-ch-tous" href="{pre}/kosher-chalets/">{tous}</a></div></div>')
SECOND = {"en": ("Our chalet", "Resorts", "Jewish Lyon guide", "Van transfers", "Explore"),
          "fr": ("Notre chalet", "Stations", "Guide juif de Lyon", "Transferts en van", "Explorer"),
          "es": ("Nuestro chalé", "Estaciones", "Guía del Lyon judío", "Traslados en van", "Explorar"),
          "he": ("הצ'אלה שלנו", "אתרי הסקי", "המדריך ליהדות ליון", "הסעות בוואן", "גלו")}

def menu_html(lang, pre, wa):
    e = ENTREES[lang]; so = SOUS[lang]
    nav = chalets_html(lang, pre) + "".join(f'\n    <a href="{pre}{u}">{t}</a>' for t, u in zip(e[1:5], URLS[1:]))
    pan = "".join(f'\n    <a href="{pre}{u}">{t}<small>{st}</small></a>' for t, u, st in zip(e[:5], URLS, so))
    cta = f'\n    <a class="nav-cta" href="{pre}/plan-your-trip/">{e[5]}</a>'
    extra = f'\n    <a class="nav-cta nav-cta-wa" href="{wa}" rel="noopener">{WA_HE}</a>' if lang == "he" else ""
    return nav + cta, pan + cta, extra

def second_links(lang, pre):
    c, r, g, v, _ = SECOND[lang]
    return [(CHALETS[lang][0], f"{pre}/kosher-chalets/"), (g, f"{pre}/jewish-lyon-guide/"), (v, f"{pre}/kosher-van-transfers/")]

# Stations en pastilles dans le menu (reproche du 15/10 : « ou on se renseigne sur les villes maintenant ? »)
STATIONS = [("Les Deux Alpes", "kosher-les-deux-alpes"), ("Courchevel", "kosher-courchevel"), ("Val Thorens", "kosher-val-thorens"),
            ("Megève", "kosher-megeve"), ("Alpe d'Huez", "kosher-alpe-dhuez"), ("Val d'Isère", "kosher-val-disere"), ("Les Arcs", "kosher-les-arcs"),
            ("La Plagne", "kosher-la-plagne"), ("Chamonix", "kosher-chamonix"), ("Annecy", "kosher-annecy"), ("Grenoble", "kosher-grenoble"),
            ("Zermatt", "kosher-zermatt"), ("St. Moritz", "kosher-st-moritz"), ("Crans-Montana", "kosher-crans-montana"), ("Verbier", "kosher-verbier"), ("Cervinia", "kosher-cervinia"), ("Courmayeur", "kosher-courmayeur"), ("Cortina d'Ampezzo", "kosher-cortina")]
def stations_html(lang, pre):
    return ""
def pied_stations(lang, pre):
    return ('<details class="pied-stations"><summary>' + SECOND[lang][1] + "</summary><p>" +
            "<br>".join(f'<a href="{pre}/{slug}/">{nom}</a>' for nom, slug in STATIONS) + "</p></details>")

def zone(page): return "alpes" if page in ALPES else "general" if page in GENERAL else "lyon"

def traiter(path):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    page = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    z = zone(page)
    h = io.open(path, encoding="utf-8").read()
    txt, lien = BANDEAU[z][lang]
    pre0 = "" if lang == "en" else "/" + lang
    n = re.sub(r'(<div class="strip"><span class="bh" lang="he">ב״ה</span>).*?(<a href="[^"]*">).*?(</a></div>)',
               lambda m: m.group(1) + txt + m.group(2) + lien + m.group(3), h, count=1, flags=re.S)
    if z in ("alpes", "general"):
        n = re.sub(r'(<div class="strip"><span class="bh" lang="he">ב״ה</span>[^<]*<a href=")[^"]*(")', lambda m: m.group(1) + pre0 + "/plan-your-trip/" + m.group(2), n, count=1)
    wa = re.search(r'<a class="panneau-wa" href="([^"]*)"', n)
    nav_h, pan_h, extra = menu_html(lang, pre0, wa.group(1) if wa else "")
    n = re.sub(r'(<nav class="liens"[^>]*>)(.*?)(\s*</nav>)', lambda m: m.group(1) + "\n    " + nav_h + extra + m.group(3), n, count=1, flags=re.S)
    n = re.sub(r'(<div class="panneau"[^>]*>\s*<nav[^>]*>)(.*?)(\s*</nav>)', lambda m: m.group(1) + "\n    " + pan_h + m.group(3), n, count=1, flags=re.S)
    sec = second_links(lang, pre0)
    n = re.sub(r'\s*<div class="panneau-st">.*?</div>', "", n, count=1, flags=re.S)
    n = re.sub(r'\s*<div class="panneau-sec">.*?</div>', "", n, count=1, flags=re.S)
    n = re.sub(r'\s*<div class="panneau-bas">.*?</div>\s*</div>', "", n, count=1, flags=re.S)
    rep, mail = PIED_PAN[lang]
    cur = ' aria-current="true"'
    langs = "".join(f'<a href="{("" if l == "en" else "/" + l) + ("/" + page if page else "") + "/"}"{cur if l == lang else ""}>{l.upper()}</a>' for l in ("en", "fr", "es", "he"))
    n = re.sub(r'(<a class="panneau-wa"[^>]*>.*?</a>)', lambda m: m.group(1) + f'\n  <div class="panneau-bas"><a href="mailto:{mail}">{mail}</a><span>{rep}</span><div class="panneau-langs">{langs}</div></div>', n, count=1, flags=re.S)
    n = re.sub(r'\s*<details class="pied-explore">.*?</details>', "", n, count=1, flags=re.S)
    expl = '\n    <details class="pied-explore"><summary>' + SECOND[lang][4] + "</summary><p>" + "<br>".join(f'<a href="{u}">{t}</a>' for t, u in [sec[0], (SECOND[lang][1], f"{pre0}/#resorts")] + sec[1:]) + "</p></details>"
    n = re.sub(r'\s*<details class="pied-stations">.*?</details>', "", n, count=1, flags=re.S)
    n = re.sub(r'(<footer class="pied">\s*<div class="cols">.*?)(\s*</div>\s*<p class="logo-pied">)', lambda m: m.group(1) + expl + "\n    " + pied_stations(lang, pre0) + m.group(2), n, count=1, flags=re.S)
    base = BASELINE[z] + (PIED_WP if page in HIVER_WP else "")
    n = re.sub(r'(<p class="logo-pied">.*?<small>).*?(</small>)', lambda m: m.group(1) + base + m.group(2), n, count=1, flags=re.S)
    pre = "" if lang == "en" else "/" + lang
    n = re.sub(r'href="(?:(?:\.\./)+|/(?:fr/|es/|he/)?)#(tours|guide)"', lambda m: f'href="{pre}/jewish-lyon-tours/#{m.group(1)}"', n)
    if n != h:
        io.open(path, "w", encoding="utf-8", newline="\n").write(n)
        return 1
    return 0

if __name__ == "__main__":
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    print(sum(traiter(p) for p in pages), "pages modifiees sur", len(pages))
