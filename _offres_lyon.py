# -*- coding: utf-8 -*-
"""Bloc fixe de 5 offres réservables en un message, sur chaque page de la zone « lyon » (décision Moshé du 21/10 : Lyon = marketplace
du voyageur juif, niveau 1), 4 langues. Posé juste avant la section finale (lead-final), sinon avant le formulaire, sinon avant </main>.
  python _offres_lyon.py          pose ou remplace le bloc (<!-- OFFRES-LYON --> ... <!-- /OFFRES-LYON -->) et le CSS de styles.css
  python _offres_lyon.py --dry    liste les pages concernées sans rien écrire
  python _offres_lyon.py --strip  retire les blocs et le CSS
Idempotent. Exclus pour l'instant : les hubs jewish-lyon-guide (édités par un autre agent) et legal (page juridique).
La mesure : js/mesure.js écoute déjà tout lien wa.me (événement whatsapp_click, link_location « content »). data-offre sert à la lecture
par lien dans le HTML, il n'est pas transmis à GA4 (mesure.js ne le lit pas)."""
import glob, io, os, re, sys
from urllib.parse import quote
ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
sys.path.insert(0, ICI)
from _zones import zone, LANGS

EXCLUS = {"legal"}
NUM = "33652092301"
DEB, FIN = "<!-- OFFRES-LYON -->", "<!-- /OFFRES-LYON -->"
CSS_DEB, CSS_FIN = "/* OFFRES-LYON */", "/* /OFFRES-LYON */"

# (slug de l'offre, page liée, mini-dessin de img/des/)
OFFRES = [("visite", "tours/jewish-lyon", "landmark"),
          ("shabbat", "kosher-shabbat-meals-catering-lyon", "shabbat-a"),
          ("chef", "kosher-services-french-alps", "chef-hat"),
          ("van", "kosher-van-transfers", "car"),
          ("escorte", "is-lyon-safe-for-jewish-visitors", "shield-check")]

T = {
 "en": dict(h2="Lyon, booked in <i>one message</i>", sous="One request, we organise everything, from the table to the transfer.",
            btn="Book on WhatsApp", plus="See the details", aria="Five private services in Lyon",
            o=[("Guided tour of Jewish Lyon", "A Jewish guide leads the visit in English, French or Spanish, with the inside of the Grande Synagogue. Sunday to Friday midday.",
                "Hello, I would like to book the guided tour of Jewish Lyon. Dates: / Number of people:"),
               ("Shabbat table and kosher meals delivered in Lyon", "Shabbat meals, meals delivered to your hotel, a minyan close by.",
                "Hello, I would like a Shabbat table and kosher meals delivered in Lyon. Dates: / Number of people:"),
               ("Private kosher chef in Lyon and the Alps", "A chef in your apartment or your chalet, in a kitchen made kosher.",
                "Hello, I would like a private kosher chef in Lyon or the Alps. Dates: / Number of people:"),
               ("Private van and transfers", "Lyon airport, Geneva, the Alpine resorts. Never during Shabbat.",
                "Hello, I would like a private van and transfers for my stay in Lyon. Dates: / Number of people:"),
               ("Discreet private escort, on request", "A quiet presence beside your group, only when you ask for it.",
                "Hello, I would like a discreet private escort in Lyon. Dates: / Number of people:")]),
 "fr": dict(h2="Lyon, réservé en <i>un message</i>", sous="Une demande, nous organisons tout, de la table au transfert.",
            btn="Réserver sur WhatsApp", plus="Voir le détail", aria="Cinq services privés à Lyon",
            o=[("Visite guidée du Lyon juif", "Une guide juive mène la visite en anglais, en français ou en espagnol, avec l'intérieur de la Grande Synagogue. Du dimanche au vendredi midi.",
                "Bonjour, je souhaite réserver la visite guidée du Lyon juif. Dates : / Nombre de personnes :"),
               ("Table de Chabbat et repas casher livrés à Lyon", "Repas de Chabbat, repas livrés à l'hôtel, un minyan à proximité.",
                "Bonjour, je souhaite une table de Chabbat et des repas casher livrés à Lyon. Dates : / Nombre de personnes :"),
               ("Chef privé casher à Lyon et dans les Alpes", "Un chef dans votre appartement ou votre chalet, dans une cuisine cachérisée.",
                "Bonjour, je souhaite un chef privé casher à Lyon ou dans les Alpes. Dates : / Nombre de personnes :"),
               ("Van et transferts privés", "Aéroport de Lyon, Genève, stations des Alpes. Jamais pendant Chabbat.",
                "Bonjour, je souhaite un van et des transferts privés pour mon séjour à Lyon. Dates : / Nombre de personnes :"),
               ("Escorte privée discrète, sur demande", "Une présence discrète auprès de votre groupe, seulement si vous la demandez.",
                "Bonjour, je souhaite une escorte privée discrète à Lyon. Dates : / Nombre de personnes :")]),
 "es": dict(h2="Lyon, reservado en <i>un mensaje</i>", sous="Una solicitud, y lo organizamos todo, de la mesa al traslado.",
            btn="Reservar por WhatsApp", plus="Ver el detalle", aria="Cinco servicios privados en Lyon",
            o=[("Visita guiada del Lyon judío", "Una guía judía dirige la visita en inglés, francés o español, con el interior de la Gran Sinagoga. De domingo a viernes a mediodía.",
                "Hola, quisiera reservar la visita guiada del Lyon judío. Fechas: / Número de personas:"),
               ("Mesa de Shabat y comidas kosher a domicilio en Lyon", "Comidas de Shabat, comidas entregadas en el hotel, un minyan cerca.",
                "Hola, quisiera una mesa de Shabat y comidas kosher a domicilio en Lyon. Fechas: / Número de personas:"),
               ("Chef privado kosher en Lyon y los Alpes", "Un chef en su apartamento o su chalet, en una cocina preparada como kosher.",
                "Hola, quisiera un chef privado kosher en Lyon o en los Alpes. Fechas: / Número de personas:"),
               ("Furgoneta y traslados privados", "Aeropuerto de Lyon, Ginebra, estaciones de los Alpes. Nunca durante Shabat.",
                "Hola, quisiera una furgoneta y traslados privados para mi estancia en Lyon. Fechas: / Número de personas:"),
               ("Escolta privada discreta, a petición", "Una presencia discreta junto a su grupo, solo si usted la pide.",
                "Hola, quisiera una escolta privada discreta en Lyon. Fechas: / Número de personas:")]),
 "he": dict(h2="ליון, הכל מסודר <i>בהודעה אחת</i>", sous="בקשה אחת, ואנחנו מסדרים הכל, מהשולחן ועד ההסעה.",
            btn="הזמינו בוואטסאפ", plus="לפרטים", aria="חמישה שירותים פרטיים בליון",
            o=[("סיור מודרך ביהדות ליון", "מדריכה יהודית, ההדרכה באנגלית, בצרפתית או בספרדית, כולל הכניסה לבית הכנסת הגדול. מיום ראשון עד יום שישי בצהריים.",
                "שלום, אשמח להזמין סיור מודרך ביהדות ליון. תאריכים: / מספר משתתפים:"),
               ("שולחן שבת וארוחות כשרות במשלוח בליון", "ארוחות שבת, ארוחות במשלוח עד המלון, מניין קרוב.",
                "שלום, אשמח להזמין שולחן שבת וארוחות כשרות במשלוח בליון. תאריכים: / מספר משתתפים:"),
               ("שף פרטי כשר בליון ובאלפים", "שף בדירה או בצ'אלה שלכם, במטבח שהוכשר במקום.",
                "שלום, אשמח להזמין שף פרטי כשר בליון או באלפים. תאריכים: / מספר משתתפים:"),
               ("ואן והסעות פרטיות", "נמל התעופה של ליון, ז'נבה, אתרי הסקי באלפים. אף פעם לא בשבת.",
                "שלום, אשמח להזמין ואן והסעות פרטיות לחופשה בליון. תאריכים: / מספר משתתפים:"),
               ("ליווי פרטי ודיסקרטי, לפי בקשה", "נוכחות שקטה לצד הקבוצה שלכם, רק כשמבקשים.",
                "שלום, אשמח לקבל ליווי פרטי ודיסקרטי בליון. תאריכים: / מספר משתתפים:")]),
}

CSS = CSS_DEB + """
.of-lyon{background:var(--beige);padding:56px 0 64px}
.of-lyon h2{font-family:var(--titre);font-weight:300;max-width:20em;text-wrap:balance}
.of-lyon h2 i{font-style:italic}
.of-lyon .of-sous{margin-top:12px;font-size:17px;line-height:1.45;max-width:36em}
.of-grille{display:grid;grid-auto-flow:column;grid-auto-columns:min(78%,300px);gap:14px;margin:28px calc(var(--pad) * -1) 0;padding:0 var(--pad) 6px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:var(--pad);scrollbar-width:none}
.of-grille::-webkit-scrollbar{display:none}
.of-carte{display:flex;flex-direction:column;scroll-snap-align:start;background:var(--blanc);border-radius:15px;padding:20px 18px 18px}
.of-ico{width:64px;height:64px;object-fit:contain;margin-bottom:14px}
.of-carte h3{font-size:19px;line-height:1.25;font-weight:600;text-wrap:balance}
.of-carte p{margin-top:8px;font-size:15px;line-height:1.45}
.of-plus{margin-top:10px;font-size:14px;font-weight:500;color:var(--vert);text-decoration:underline;text-underline-offset:3px;align-self:flex-start}
.of-plus::after{content:" \\2192"}
[dir=rtl] .of-plus::after{content:" \\2190"}
.of-btn{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:auto;min-height:48px;padding:0 10px;border-radius:999px;background:var(--jaune);color:#000;font-weight:600;font-size:14px;text-decoration:none;text-align:center}
.of-carte > :nth-last-child(2){margin-bottom:18px}
.of-btn svg{width:18px;height:18px;fill:currentColor;flex:none}
.of-btn:hover{filter:brightness(.96)}
@media (min-width:1100px){
  .of-grille{grid-auto-flow:row;grid-auto-columns:auto;grid-template-columns:repeat(5,1fr);gap:16px;margin-inline:0;padding-inline:0;overflow:visible;scroll-snap-type:none}
}
""" + CSS_FIN


def eol(s): return "\r\n" if "\r\n" in s else "\n"


def bloc(lang, page):
    t = T[lang]
    pre = "" if lang == "en" else "/" + lang
    cartes = []
    for (slug, cible, img), (titre, phrase, msg) in zip(OFFRES, t["o"]):
        href = f"https://wa.me/{NUM}?text={quote(msg, safe='')}"
        plus = "" if cible == page else f'<a class="of-plus" href="{pre}/{cible}/">{t["plus"]}</a>'
        cartes.append(f'<article class="of-carte" role="listitem"><img class="of-ico" src="/img/des/{img}.webp" alt="" width="96" height="96" loading="lazy">'
                      f'<h3>{titre}</h3><p>{phrase}</p>{plus}'
                      f'<a class="of-btn" href="{href}" rel="noopener" data-offre="{slug}"><svg aria-hidden="true"><use href="#wa"/></svg>{t["btn"]}</a></article>')
    return (f'{DEB}<section class="ss of-lyon" id="offres-lyon"><div class="wrap"><h2>{t["h2"]}</h2><p class="of-sous">{t["sous"]}</p>'
            f'<div class="of-grille" role="list" aria-label="{t["aria"]}">' + "".join(cartes) + f'</div></div></section>{FIN}')


def retirer(s):
    return re.sub(re.escape(DEB) + r".*?" + re.escape(FIN) + r"(?:\r?\n)?", "", s, flags=re.S)


def point_insertion(s):
    m = re.search(r'<section class="[^"]*\blead-final\b', s)
    if m: return m.start()
    f = s.find("<form")
    if f > -1:
        d = s.rfind("<section", 0, f)
        if d > -1: return d
    return s.index("</main>")


def traiter(path, mode):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    page = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    if zone(page) != "lyon" or page in EXCLUS:
        return None
    h = io.open(path, encoding="utf-8", newline="").read()
    nl = eol(h)
    n = retirer(h)
    if mode != "strip":
        i = point_insertion(n)
        n = n[:i] + bloc(lang, page) + nl + n[i:]
    if n != h and mode != "dry":
        io.open(path, "w", encoding="utf-8", newline="").write(n)
    return (lang, page, n != h)


def css(mode):
    h = io.open("styles.css", encoding="utf-8", newline="").read()
    nl = eol(h)
    n = re.sub(r"(?:\r?\n)?" + re.escape(CSS_DEB) + r".*?" + re.escape(CSS_FIN), "", h, flags=re.S)
    if mode == "pose":
        n = n.rstrip("\r\n") + nl + CSS.replace("\n", nl) + nl
    if n != h:
        io.open("styles.css", "w", encoding="utf-8", newline="").write(n)
    return n != h


if __name__ == "__main__":
    mode = "strip" if "--strip" in sys.argv else "dry" if "--dry" in sys.argv else "pose"
    pages = sorted(f for f in glob.glob("**/index.html", recursive=True) if not f.replace("\\", "/").startswith(("_", "preview")))
    res = [r for r in (traiter(f, mode) for f in pages) if r]
    par = {l: [r for r in res if r[0] == l] for l in ("en", "fr", "es", "he")}
    if mode == "dry":
        for r in res: print(r[0], r[1])
    css_change = css(mode) if mode != "dry" else False
    print(mode, "| pages concernées par langue:", {l: len(v) for l, v in par.items()}, "| modifiées:", sum(1 for r in res if r[2]), "| styles.css modifié:", css_change)
