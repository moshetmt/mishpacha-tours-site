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
         "lyon-gateway-to-the-alps-kosher", "summer-in-the-alps-jewish-families", "flights-to-lyon"}
GENERAL = {"", "about", "contact", "privacy", "terms", "credits", "merci", "jewish-life-around-lyon"}

BASELINE = {"alpes": "Kosher Stays in the French Alps", "general": "Kosher Holidays in the Alps and Lyon", "lyon": "Jewish Tours of Lyon"}
BANDEAU = {  # (texte, lien)
    "alpes": {"en": ("Strictly kosher stays in the French Alps, one day-by-day programme. ", "Describe your stay."),
              "fr": ("Séjours strictement casher dans les Alpes, un programme jour par jour. ", "Décrivez votre séjour."),
              "es": ("Estancias estrictamente kosher en los Alpes, un programa día a día. ", "Describa su estancia."),
              "he": ("חופשות כשרות באלפים הצרפתיים, תוכנית מפורטת יום אחר יום. ", "ספרו לנו על החופשה.")},
    "general": {"en": ("Strictly kosher holidays in the French Alps and Lyon, shomer shabbat. ", "Describe your stay."),
                "fr": ("Séjours strictement casher dans les Alpes et à Lyon, shomer shabbat. ", "Décrivez votre séjour."),
                "es": ("Vacaciones estrictamente kosher en los Alpes y Lyon, shomer Shabat. ", "Describa su estancia."),
                "he": ("חופשות כשרות באלפים הצרפתיים ובליון. שומר כשרות · שומר שבת. ", "ספרו לנו על החופשה.")},
    "lyon": {"en": ("Private tours, Sunday to Friday morning. ", "Check a date on WhatsApp."),
             "fr": ("Visites privées, du dimanche au vendredi matin. ", "Vérifier une date sur WhatsApp."),
             "es": ("Visitas privadas, de domingo a viernes por la mañana. ", "Consulte una fecha por WhatsApp."),
             "he": ("סיורים פרטיים, מיום ראשון עד יום שישי בבוקר. ", "בדיקת תאריך בוואטסאפ.")},
}

def zone(page): return "alpes" if page in ALPES else "general" if page in GENERAL else "lyon"

def traiter(path):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    page = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    z = zone(page)
    h = io.open(path, encoding="utf-8").read()
    txt, lien = BANDEAU[z][lang]
    n = re.sub(r'(<div class="strip"><span class="bh" lang="he">ב״ה</span>).*?(<a href="[^"]*">).*?(</a></div>)',
               lambda m: m.group(1) + txt + m.group(2) + lien + m.group(3), h, count=1, flags=re.S)
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
