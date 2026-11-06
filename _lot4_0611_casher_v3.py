# -*- coding: utf-8 -*-
"""Page casher /kosher-services-french-alps/ v3 (Moshé 06/11 2 h 40 : « ça manque de beauté et de luxe, l'expérience utilisateur
c'est de la merde » → recomposer, pas retoucher). 4 langues, idempotent (marqueur LOT4-MOM).
 - la liste en accordéon « Tous les services, une seule demande » et la grille de vignettes sont remplacées par « Votre journée » :
   4 moments en grandes photos réelles (matin : cuisine cachérisée ; journée : les pistes ; soir : la table dressée ; vendredi :
   Chabbat), 2 lignes chacun, les liens vers les 9 pages de service en texte sous chaque moment ;
 - « Quelle station, quel côté » : liste ouverte, plus d'accordéon ;
 - plus aucun accordéon à chevron sur les pages du lot (CSS LOT4-0611, `.dk-pli` ouvert).
Modèle : pages éditoriales Louis Vuitton (grande photo, légende courte, « Découvrir »). Depuis site-v5/ : python _lot4_0611_casher_v3.py"""
import html, io, json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
A, Z = "<!--LOT4-MOM-->", "<!--/LOT4-MOM-->"
LANGS = [("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")]
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def esc(s): return html.escape(s, quote=True)
def ltr(l, s):
    if l != "he": return s
    return re.sub(r"(?<![\w\"'=/])([A-Za-z][A-Za-z' .\-]*[A-Za-z]|\d[\d .:\-]*\d|\d)(?![\w\"'=/])", r'<span dir="ltr">\1</span>', s)

def lab(slug, l):
    if slug == "kosher-van-transfers": return {"en": "Private van transfers", "fr": "Transferts en van privé", "es": "Traslados en van privada", "he": "הסעות בוואן פרטי"}[l]
    if slug == "kosher-ski-holidays-french-alps": return {"en": "Kosher ski holidays", "fr": "Vacances au ski casher", "es": "Vacaciones de esquí kosher", "he": "חופשת סקי כשרה"}[l]
    t = json.load(open(f"_lot4_contenu/{slug}.json", encoding="utf-8"))[l]; return t["h1"]

PH = {"matin": ("/img/chalet/w/courchevel-cuisine-1", 1280, 859), "journee": ("/img/h/reve-ski", 1600, 1067),
      "soir": ("/img/chalet/w/valthorens-table", 1280, 859), "vendredi": ("/img/chalet/w/wp-salle-a-manger-1", 1280, 960)}
def img(k):
    b, w, h = PH[k]; ws = [640, 960, w]
    return f'<img src="{b}-960.webp" srcset="' + ", ".join(f"{b}-{x}.webp {x}w" for x in ws) + f'" sizes="(min-width:900px) 50vw, 100vw" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'

T = {
 "en": dict(h2=("Your day ", "in the resort"), sous="One request, and the week runs itself. Four moments, the services behind each.",
   mom=[("matin", "In the morning, the kitchen is already kosher", "Kashered before you arrive. A private chef cooks in the chalet, or hot meals arrive every two days.", ["private-kosher-chef-alps", "kosher-meals-delivered-alps", "private-kosher-chalet-alps"]),
        ("journee", "During the day, the slopes", "A private van to the resort, ski hire and a dog sled on request, all on one quote.", ["kosher-van-transfers", "kosher-ski-holidays-french-alps", "activities-alps-kosher-families"]),
        ("soir", "In the evening, the table is set", "Starter, main and dessert from 28 € per person, the full day from 78 €. Then the spa.", ["kosher-meals-delivered-alps", "spa-massage-alps"]),
        ("vendredi", "On Friday, Shabbat is ready", "Challot and wine delivered on Friday, dinner 45 €, lunch 40 €, and the nearest minyan for your dates.", ["shabbat-holiday-meals-alps", "minyan-sefer-torah-alps"])],
   wa="Order the meals on WhatsApp"),
 "fr": dict(h2=("Votre journée ", "en station"), sous="Une demande, et la semaine se déroule. Quatre moments, et les services derrière chacun.",
   mom=[("matin", "Le matin, la cuisine est déjà casher", "Cachérisée avant votre arrivée. Un chef privé cuisine au chalet, ou des repas chauds arrivent tous les deux jours.", ["private-kosher-chef-alps", "kosher-meals-delivered-alps", "private-kosher-chalet-alps"]),
        ("journee", "La journée, les pistes", "Un van privé jusqu'à la station, location de skis et traîneau à chiens sur demande, sur un seul devis.", ["kosher-van-transfers", "kosher-ski-holidays-french-alps", "activities-alps-kosher-families"]),
        ("soir", "Le soir, la table est dressée", "Entrée, plat, dessert à partir de 28 € par personne, la journée complète à partir de 78 €. Puis le spa.", ["kosher-meals-delivered-alps", "spa-massage-alps"]),
        ("vendredi", "Le vendredi, Chabbat est prêt", "Hallot et vin livrés le vendredi, dîner 45 €, déjeuner 40 €, et le minyan le plus proche pour vos dates.", ["shabbat-holiday-meals-alps", "minyan-sefer-torah-alps"])],
   wa="Commander les repas sur WhatsApp"),
 "es": dict(h2=("Su día ", "en la estación"), sous="Una solicitud, y la semana se organiza sola. Cuatro momentos, y los servicios detrás de cada uno.",
   mom=[("matin", "Por la mañana, la cocina ya es kosher", "Kasherizada antes de su llegada. Un chef privado cocina en el chalet, o llegan comidas calientes cada dos días.", ["private-kosher-chef-alps", "kosher-meals-delivered-alps", "private-kosher-chalet-alps"]),
        ("journee", "Durante el día, las pistas", "Una van privada hasta la estación, alquiler de esquís y trineo de perros bajo petición, en un solo presupuesto.", ["kosher-van-transfers", "kosher-ski-holidays-french-alps", "activities-alps-kosher-families"]),
        ("soir", "Por la noche, la mesa está puesta", "Entrante, plato y postre desde 28 € por persona, el día completo desde 78 €. Después, el spa.", ["kosher-meals-delivered-alps", "spa-massage-alps"]),
        ("vendredi", "El viernes, Shabat está listo", "Jalot y vino entregados el viernes, cena 45 €, almuerzo 40 €, y el minyán más cercano para sus fechas.", ["shabbat-holiday-meals-alps", "minyan-sefer-torah-alps"])],
   wa="Pedir las comidas por WhatsApp"),
 "he": dict(h2=("היום שלכם ", "באתר הסקי"), sous="בקשה אחת, והשבוע מתנהל מעצמו. ארבעה רגעים, והשירותים שמאחורי כל אחד.",
   mom=[("matin", "בבוקר, המטבח כבר כשר", "מוכשר לפני ההגעה שלכם. שף פרטי מבשל בצ'אלה, או ארוחות חמות מגיעות כל יומיים.", ["private-kosher-chef-alps", "kosher-meals-delivered-alps", "private-kosher-chalet-alps"]),
        ("journee", "ביום, המסלולים", "וואן פרטי עד אתר הסקי, השכרת סקי ומזחלת כלבים לפי בקשה, בהצעת מחיר אחת.", ["kosher-van-transfers", "kosher-ski-holidays-french-alps", "activities-alps-kosher-families"]),
        ("soir", "בערב, השולחן ערוך", "מנה ראשונה, עיקרית וקינוח החל מ-28 € לאדם, יום מלא החל מ-78 €. ואז הספא.", ["kosher-meals-delivered-alps", "spa-massage-alps"]),
        ("vendredi", "ביום שישי, שבת מוכנה", "חלות ויין מגיעים ביום שישי, ארוחת ערב 45 €, ארוחת צהריים 40 €, והמניין הקרוב ביותר לתאריכים שלכם.", ["shabbat-holiday-meals-alps", "minyan-sefer-torah-alps"])],
   wa="להזמין את הארוחות בוואטסאפ"),
}
n = 0
for l, pre in LANGS:
    p = f"{pre}kosher-services-french-alps/index.html"; s = rd(p); t = T[l]
    # 1. accordéon « Tous les services » + grille de vignettes → « Votre journée » (relance : le bloc marqué est réécrit en place)
    if A in s:
        i = s.find(A); j = s.find(Z) + len(Z)
    else:
        i = s.find('<section class="clair clair-2 ss wrap conseils">'); assert i > 0, p
        j = s.find('<section class="clair ss wrap minyan-bh repas-prix'); assert j > i, p
    ancien = s[i:j]
    wa = re.search(r"""["'](https://wa\.me/33781823193[^"']*)["']""", ancien) or re.search(r"""["'](https://wa\.me/33652092301[^"']*)["']""", ancien); assert wa, p
    moms = ""
    for k, h3, txt, liens in t["mom"]:
        li = " · ".join(f'<a href="/{pre}{sl}/">{ltr(l, esc(lab(sl, l)))}</a>' for sl in liens)
        moms += f'<article class="mom"><div class="mom-ph">{img(k)}</div><div class="mom-tx"><h3>{ltr(l, esc(h3))}</h3><p>{ltr(l, esc(txt))}</p><p class="mom-liens">{li}</p></div></article>'
    bloc = (f'{A}<section class="clair ss wrap moments"><h2>{esc(t["h2"][0])}<i>{esc(t["h2"][1])}</i></h2><p class="mom-sous">{ltr(l, esc(t["sous"]))}</p>{moms}'
            f'</section>{Z}')   # bouton WhatsApp retiré ici : il reste sous les prix
    s = s[:i] + bloc + s[j:]
    # 2. « Quelle station » : liste ouverte
    k0 = s.find('<div class="clair ss beige">'); k1 = s.find('</div></div>', k0)
    if k0 > 0: s = s[:k0] + s[k0:k1].replace('<ul class="dk-cartes">', '<ul class="dk-liste">') + s[k1:]
    wr(p, s); n += 1
print("page casher v3 :", n, "langues")
