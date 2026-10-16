# -*- coding: utf-8 -*-
"""Bandeau vert et baseline du pied selon la zone de la page (decision operateur du 13/10 : « adapte en fonction de la zone »).
  python _zones.py   : apres les builds et les traductions, AVANT _decor.py. Idempotent.
Zones : alpes (stations, chalet, services, ski, ete), general (accueil, about, contact, legal), lyon (tout le reste).
Les liens « Tours » et « Your guide » des menus (ancres /#tours et /#guide de l'ancien accueil) partent vers /jewish-lyon-tours/."""
import glob, io, os, re

LANGS = ("fr", "es", "he")
ALPES = {"alps", "kosher-alpe-dhuez", "kosher-annecy", "kosher-chalet-les-deux-alpes", "kosher-chamonix", "kosher-courchevel",
         "kosher-grenoble", "kosher-la-plagne", "kosher-les-arcs", "kosher-les-deux-alpes", "kosher-megeve", "kosher-services-french-alps",
         "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps", "kosher-val-disere", "kosher-val-thorens",
         "kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana", "kosher-cervinia", "kosher-courmayeur", "kosher-cortina",
         "lyon-gateway-to-the-alps-kosher", "summer-in-the-alps-jewish-families", "flights-to-lyon"}
GENERAL = {"", "plan-your-trip", "kosher-van-transfers", "about", "contact", "privacy", "terms", "credits", "merci", "jewish-life-around-lyon"}

BASELINE = {"alpes": "Kosher Stays in the Alps", "general": "Kosher Holidays in the Alps and Lyon", "lyon": "Jewish Tours of Lyon"}
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

# Menu a 4 entrees (15/10) : Winter, Summer, Jewish Lyon + bouton « Plan your trip ». Reecrit en entier a chaque passage (idempotent).
ENTREES = {"en": ("Winter", "Summer", "Jewish Lyon", "Plan your trip"),
           "fr": ("Hiver", "Été", "Lyon juif", "Préparer mon voyage"),
           "es": ("Invierno", "Verano", "Lyon judío", "Planificar mi viaje"),
           "he": ("חורף", "קיץ", "ליון היהודית", "לתכנן את הטיול")}
WA_HE = "דברו איתנו בוואטסאפ"
SECOND = {"en": ("Our chalet", "Resorts", "Jewish Lyon guide", "Van transfers", "Explore"),
          "fr": ("Notre chalet", "Stations", "Guide du Lyon juif", "Transferts en van", "Explorer"),
          "es": ("Nuestro chalé", "Estaciones", "Guía del Lyon judío", "Traslados en van", "Explorar"),
          "he": ("הצ'אלה שלנו", "אתרי הסקי", "המדריך ליהדות ליון", "הסעות בוואן", "גלו")}

def menu_html(lang, pre, wa):
    w, s_, l, p = ENTREES[lang]
    base = f'<a href="{pre}/alps/">{w}</a>\n    <a href="{pre}/summer-in-the-alps-jewish-families/">{s_}</a>\n    <a href="{pre}/jewish-lyon-tours/">{l}</a>\n    '
    if lang == "he":
        return base + f'<a href="{pre}/plan-your-trip/">{p}</a>', base + f'<a href="{pre}/plan-your-trip/">{p}</a>', f'\n    <a class="nav-cta nav-cta-wa" href="{wa}" rel="noopener">{WA_HE}</a>'
    cta = f'<a class="nav-cta" href="{pre}/plan-your-trip/">{p}</a>'
    return base + cta, base + cta, ""

def second_links(lang, pre):
    c, r, g, v, _ = SECOND[lang]
    return [(c, f"{pre}/kosher-chalet-les-deux-alpes/"), (g, f"{pre}/jewish-lyon-guide/"), (v, f"{pre}/kosher-van-transfers/")]

# Stations en pastilles dans le menu (reproche du 15/10 : « ou on se renseigne sur les villes maintenant ? »)
STATIONS = [("Les Deux Alpes", "kosher-les-deux-alpes"), ("Courchevel", "kosher-courchevel"), ("Val Thorens", "kosher-val-thorens"),
            ("Megève", "kosher-megeve"), ("Alpe d'Huez", "kosher-alpe-dhuez"), ("Val d'Isère", "kosher-val-disere"), ("Les Arcs", "kosher-les-arcs"),
            ("La Plagne", "kosher-la-plagne"), ("Chamonix", "kosher-chamonix"), ("Annecy", "kosher-annecy"), ("Grenoble", "kosher-grenoble"),
            ("Zermatt", "kosher-zermatt"), ("St. Moritz", "kosher-st-moritz"), ("Crans-Montana", "kosher-crans-montana"), ("Cervinia", "kosher-cervinia"), ("Courmayeur", "kosher-courmayeur"), ("Cortina d'Ampezzo", "kosher-cortina")]
def stations_html(lang, pre):
    return ('\n  <div class="panneau-st"><p>' + SECOND[lang][1] + '</p>' +
            "".join(f'<a href="{pre}/{slug}/">{nom}</a>' for nom, slug in STATIONS) + '</div>')

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
    n = re.sub(r'(<div class="panneau"[^>]*>\s*<nav[^>]*>.*?</nav>)', lambda m: m.group(1) + stations_html(lang, pre0) + '\n  <div class="panneau-sec">' + "".join(f'<a href="{u}">{t}</a>' for t, u in sec) + "</div>", n, count=1, flags=re.S)
    n = re.sub(r'\s*<details class="pied-explore">.*?</details>', "", n, count=1, flags=re.S)
    expl = '\n    <details class="pied-explore"><summary>' + SECOND[lang][4] + "</summary><p>" + "<br>".join(f'<a href="{u}">{t}</a>' for t, u in [sec[0], (SECOND[lang][1], f"{pre0}/#resorts")] + sec[1:]) + "</p></details>"
    n = re.sub(r'(<footer class="pied">\s*<div class="cols">.*?)(\s*</div>\s*<p class="logo-pied">)', lambda m: m.group(1) + expl + m.group(2), n, count=1, flags=re.S)
    n = re.sub(r'(<p class="logo-pied">.*?<small>).*?(</small>)', lambda m: m.group(1) + BASELINE[z] + m.group(2), n, count=1, flags=re.S)
    pre = "" if lang == "en" else "/" + lang
    n = re.sub(r'href="(?:(?:\.\./)+|/(?:fr/|es/|he/)?)#(tours|guide)"', lambda m: f'href="{pre}/jewish-lyon-tours/#{m.group(1)}"', n)
    if n != h:
        io.open(path, "w", encoding="utf-8", newline="\n").write(n)
        return 1
    return 0

if __name__ == "__main__":
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    print(sum(traiter(p) for p in pages), "pages modifiees sur", len(pages))
