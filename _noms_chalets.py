# -*- coding: utf-8 -*-
"""Noms des chalets choisis par Mendel le 30/10 (dictionnaire NOMS de _retouches_30_10.py, translittérations hébraïques
reprises telles quelles), propagés partout où un chalet était désigné sans son nom : cartes (h3 de _kit_wp.py), menus et
bandes de vignettes (_zones.py), balises title, description et og: des 5 fiches, fil d'Ariane et JSON-LD BreadcrumbList,
liens texte vers les fiches, titres h2 des sections chalet des pages station, index.md jumeaux (régénérés comme _agentic.py).
Au passage : titres et descriptions ES trop longs (> 70 et > 170, liste de _qa.py), « Five private chalets » du menu EN,
« Cinco chalés » de la description ES du hub (règle du 28/10 : jamais un nombre de chalets).
Idempotent, à relancer après toute régénération :  python _noms_chalets.py   (depuis site-v5/).
Ne touche à aucun <h1> ni à css/styles.css. Imprime ce qui reste à la main."""
import io, re, glob, os, html as H
from markdownify import markdownify as md
from _retouches_30_10 import NOMS

os.chdir(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://mishpachatours.com"
LANGS = [".", "fr", "es", "he"]
SLUGS = list(NOMS)
MOI = {"_noms_chalets.py", "_retouches_30_10.py"}

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def nom(slug, d): return NOMS[slug][d][0]                       # « Chalet King David, Les Deux Alpes »
def court(slug, d): return nom(slug, d).split(",")[0]            # « Chalet King David »
def menu(slug, d): return nom(slug, d).replace(", ", " · ")      # « Chalet King David · Les Deux Alpes »
def pre(d): return "" if d == "." else f"/{d}"

DA, SL, CO, ME, VT = SLUGS

# 1. Anciennes désignations (texte exact d'un lien vers la fiche, ou h3 d'une carte « hub-carte ») -> nom complet.
ANCIENS = {
 (DA, "."): ["Our kosher chalet, at the foot of the slopes", "The kosher chalet in Les Deux Alpes", "Our 15-bed chalet in Les Deux Alpes",
             "Our chalet in Les Deux Alpes", "Kosher chalet in Les Deux Alpes"],
 (SL, "."): ["The Slope Chalet, skis on at the door"],
 (CO, "."): ["A kosher chalet in the heart of Courchevel", "The kosher chalet in Courchevel", "Our chalet in Courchevel"],
 (ME, "."): ["The Mont Blanc Chalet, for several families"],
 (VT, "."): ["The Val Thorens Chalet, skis on at the door"],
 (DA, "fr"): ["Notre chalet casher, au pied des pistes", "Le chalet casher aux Deux Alpes", "Notre chalet de 15 couchages aux Deux Alpes",
              "Notre chalet aux Deux Alpes", "Chalet casher aux Deux Alpes"],
 (SL, "fr"): ["Le chalet des pistes, skis aux pieds"],
 (CO, "fr"): ["Un chalet casher au cœur de Courchevel", "Le chalet casher à Courchevel", "Notre chalet à Courchevel"],
 (ME, "fr"): ["Le chalet du Mont Blanc, pour plusieurs familles"],
 (VT, "fr"): ["Le chalet de Val Thorens, skis aux pieds"],
 (DA, "es"): ["Nuestro chalet kosher, al pie de las pistas", "El chalé kosher en Les Deux Alpes", "Nuestro chalé de 15 camas en Les Deux Alpes",
              "Nuestro chalé en Les Deux Alpes", "Chalé kosher en Les Deux Alpes"],
 (SL, "es"): ["El chalet de las pistas, esquís puestos en la puerta"],
 (CO, "es"): ["Un chalet kosher en el corazón de Courchevel", "El chalé kosher en Courchevel", "Nuestro chalé en Courchevel"],
 (ME, "es"): ["El chalet del Mont Blanc, para varias familias"],
 (VT, "es"): ["El chalet de Val Thorens, esquís en la puerta"],
 (DA, "he"): ["הצ'אלה הכשרה שלנו, למרגלות המסלולים", "הצ'אלה הכשרה בלה דז אלפ", "הצ'אלה שלנו עם 15 המיטות בלה דז אלפ",
              "הצ'אלה שלנו בלה דז אלפ", "צ'אלה כשרה בלה דז אלפ"],
 (SL, "he"): ["צ'אלה המסלולים, נועלים מגלשיים בדלת"],
 (CO, "he"): ["צ'אלה כשרה בלב קורשבל", "הצ'אלה הכשרה בקורשבל", "הצ'אלה שלנו בקורשבל"],
 (ME, "he"): ["צ'אלה המון בלאן, לכמה משפחות"],
 (VT, "he"): ["הצ'אלה בואל טורנס, מגלשיים בדלת"],
}

# 2. Paires littérales (HTML, index.md et générateurs) : phrases en prose, h2 des sections station, alt des photos, menu EN, hub ES.
def paires(d):
    kd, ro, fd, lb, be = (court(s, d) for s in SLUGS)
    P = {
     ".": [("from <a href=\"../kosher-chalet-les-deux-alpes/\">our 15-bed chalet</a>", f"from <a href=\"../kosher-chalet-les-deux-alpes/\">{kd}</a>"),
           ("Our 15-bed chalet is five minutes on foot.", f"{kd} is five minutes on foot."),
           ("<b>A kosher chalet in Les Deux Alpes.</b>", f"<b>{nom(DA, d)}.</b>"),
           ("<h2>Our chalet <i>in Courchevel</i></h2>", f"<h2>{fd} <i>in Courchevel</i></h2>"),
           ("<h2>Our chalet <i>near Megève</i></h2>", f"<h2>{lb} <i>near Megève</i></h2>"),
           ("<h2>Our chalet <i>in Val Thorens</i></h2>", f"<h2>{be} <i>in Val Thorens</i></h2>"),
           ('co_h2="Our chalet"', f'co_h2="{fd}"'), ('me_h2="Our chalet"', f'me_h2="{lb}"'), ('vth_h2="Our chalet"', f'vth_h2="{be}"'),
           ("The Slope Chalet in Les Deux Alpes under snow", f"{ro} in Les Deux Alpes under snow"),
           ("The Val Thorens chalet under snow", f"{be} in Val Thorens under snow"),
           ("Five private chalets, strictly kosher", "Private chalets, strictly kosher")],
     "fr": [("de <a href=\"/fr/kosher-chalet-les-deux-alpes/\">notre chalet de 15 couchages</a>", f"du <a href=\"/fr/kosher-chalet-les-deux-alpes/\">{kd}</a>"),
            ("Notre chalet de 15 couchages est à cinq minutes à pied.", f"Le {kd} est à cinq minutes à pied."),
            ("<b>Un chalet casher aux Deux Alpes.</b>", f"<b>{nom(DA, d)}.</b>"),
            ("<h2>Notre chalet <i>à Courchevel</i></h2>", f"<h2>{fd} <i>à Courchevel</i></h2>"),
            ("<h2>Notre chalet <i>près de Megève</i></h2>", f"<h2>{lb} <i>près de Megève</i></h2>"),
            ("<h2>Notre chalet <i>à Val Thorens</i></h2>", f"<h2>{be} <i>à Val Thorens</i></h2>"),
            ('co_h2="Notre chalet"', f'co_h2="{fd}"'), ('me_h2="Notre chalet"', f'me_h2="{lb}"'), ('vth_h2="Notre chalet"', f'vth_h2="{be}"'),
            ("Le chalet des pistes aux Deux Alpes sous la neige", f"Le {ro} aux Deux Alpes sous la neige"),
            ("Le chalet de Val Thorens sous la neige", f"Le {be} à Val Thorens sous la neige")],
     "es": [("de <a href=\"/es/kosher-chalet-les-deux-alpes/\">nuestro chalet de 15 camas</a>", f"del <a href=\"/es/kosher-chalet-les-deux-alpes/\">{kd}</a>"),
            ("Nuestro chalé de 15 camas está a cinco minutos a pie.", f"El {kd} está a cinco minutos a pie."),
            ("<b>Un chalé kosher en Les Deux Alpes.</b>", f"<b>{nom(DA, d)}.</b>"),
            ("<h2>Nuestro chalet <i>en Courchevel</i></h2>", f"<h2>{fd} <i>en Courchevel</i></h2>"),
            ("<h2>Nuestro chalet <i>cerca de Megève</i></h2>", f"<h2>{lb} <i>cerca de Megève</i></h2>"),
            ("<h2>Nuestro chalet <i>en Val Thorens</i></h2>", f"<h2>{be} <i>en Val Thorens</i></h2>"),
            ('co_h2="Nuestro chalet"', f'co_h2="{fd}"'), ('me_h2="Nuestro chalet"', f'me_h2="{lb}"'), ('vth_h2="Nuestro chalet"', f'vth_h2="{be}"'),
            ("El chalet de las pistas en Les Deux Alpes bajo la nieve", f"El {ro} en Les Deux Alpes bajo la nieve"),
            ("El chalet de Val Thorens bajo la nieve", f"El {be} en Val Thorens bajo la nieve"),
            ("Cinco chalés kosher en los Alpes, en Les Deux Alpes, Courchevel, cerca de Megève y en Val Thorens: chef privado, Shabat y minyan en el chalé. Una solicitud, un presupuesto por escrito.",
             "Chalés kosher en los Alpes: Les Deux Alpes, Courchevel, cerca de Megève y Val Thorens. Chef privado, Shabat y minyan en el chalé. Un presupuesto por escrito.")],
     "he": [("מ<a href=\"/he/kosher-chalet-les-deux-alpes/\">הצ'אלה שלנו עם 15 המיטות</a>", f"מ<a href=\"/he/kosher-chalet-les-deux-alpes/\">{kd}</a>"),
            ("הצ'אלה שלנו עם 15 המיטות במרחק חמש דקות בהליכה.", f"{kd} במרחק חמש דקות בהליכה."),
            ("חמש דקות הליכה מהצ'אלה שלנו עם 15 המיטות", f"חמש דקות הליכה מ{kd}"),
            ("<b>צ'אלה כשרה בלה דז אלפ.</b>", f"<b>{nom(DA, d)}.</b>"),
            ("<h2>הצ'אלה שלנו <i>בקורשבל</i></h2>", f"<h2>{fd} <i>בקורשבל</i></h2>"),
            ("<h2>הצ'אלה שלנו <i>ליד מג'ב</i></h2>", f"<h2>{lb} <i>ליד מג'ב</i></h2>"),
            ("<h2>הצ'אלה שלנו <i>בואל טורנס</i></h2>", f"<h2>{be} <i>בואל טורנס</i></h2>"),
            ('co_h2="הצ\'אלה שלנו"', f'co_h2="{fd}"'), ('me_h2="הצ\'אלה שלנו"', f'me_h2="{lb}"'), ('vth_h2="הצ\'אלה שלנו"', f'vth_h2="{be}"'),
            ("צ'אלה המסלולים בלה דז אלפ תחת השלג", f"{ro} בלה דז אלפ תחת השלג"),
            ("הצ'אלה בואל טורנס תחת השלג", f"{be} בואל טורנס תחת השלג")],
    }
    return P[d]

# 2 bis. Anciens noms propres en prose, alt des galeries (_galerie_chalets.py), h2 et CTA des FAQ, hub : « quel chalet choisir ? »
def prose(d):
    kd, ro, fd, lb, be = (court(s, d) for s in SLUGS)
    P = {
     ".": [("The Slope Chalet", ro), ("the Slope Chalet", ro), ("The Mont Blanc Chalet", lb), ("the Mont Blanc Chalet", lb),
           ("The Val Thorens Chalet", be), ("the Val Thorens Chalet", be), ("the 15-bed chalet has", f"{kd} has"),
           ("The Courchevel chalet: <i>questions</i>", f"{fd}: <i>questions</i>"), ('faq"><h2>The kosher chalet: ', f'faq"><h2>{kd}: '),
           ('alt="Courchevel Chalet, ', f'alt="{fd}, '), ('alt="Les Deux Alpes Chalet, ', f'alt="{kd}, '),
           ('nom=t("Courchevel Chalet", "Chalet de Courchevel", "Chalé de Courchevel", "הצ\'אלה בקורשבל")', f'nom=t("{fd}", "{fd}", "{fd}", "{court(CO, "he")}")'),
           ('nom=t("Les Deux Alpes Chalet", "Chalet des Deux Alpes", "Chalé de Les Deux Alpes", "הצ\'אלה בלה דז אלפ")', f'nom=t("{kd}", "{kd}", "{kd}", "{court(DA, "he")}")')],
     "fr": [("Le chalet des pistes", f"Le {ro}"), ("le chalet des pistes", f"le {ro}"), ("Le chalet du Mont Blanc", f"Le {lb}"), ("le chalet du Mont Blanc", f"le {lb}"),
            ("Le chalet de Val Thorens", f"Le {be}"), ("le chalet de Val Thorens", f"le {be}"), ("le chalet de 15 lits compte", f"le {kd} compte"),
            ("Le chalet de Courchevel : <i>vos questions</i>", f"Le {fd} : <i>vos questions</i>"), ('faq"><h2>Le chalet casher : ', f'faq"><h2>Le {kd} : '),
            ('alt="Chalet de Courchevel, ', f'alt="{fd}, '), ('alt="Chalet des Deux Alpes, ', f'alt="{kd}, ')],
     "es": [("El chalet de las pistas", f"El {ro}"), ("el chalet de las pistas", f"el {ro}"), ("el chalé de las pistas", f"el {ro}"),
            ("El chalet del Mont Blanc", f"El {lb}"), ("el chalet del Mont Blanc", f"el {lb}"), ("El chalet de Val Thorens", f"El {be}"), ("el chalet de Val Thorens", f"el {be}"),
            ("el chalé de 15 camas tiene", f"el {kd} tiene"), ("El chalé de Courchevel: <i>preguntas</i>", f"El {fd}: <i>preguntas</i>"), ('faq"><h2>El chalé kosher: ', f'faq"><h2>El {kd}: '),
            ('alt="Chalé de Courchevel, ', f'alt="{fd}, '), ('alt="Chalé de Les Deux Alpes, ', f'alt="{kd}, '),
            ("Cinco chalés con todo lo kosher resuelto: dos en Les Deux Alpes, uno en Courchevel, uno cerca de Megève y uno en Val Thorens",
             "Nuestros chalés con todo lo kosher resuelto: Les Deux Alpes, Courchevel, cerca de Megève y Val Thorens")],
     "he": [("צ'אלה המסלולים", ro), ("צ'אלה המון בלאן", lb), ("צ'אלה מון בלאן", lb), ("לצ'אלה של 15 המיטות יש", f"ל{kd} יש"),
            ("הצ'אלה בואל טורנס: <i>שאלות</i>", f"{be}: <i>שאלות</i>"), ("הצ'אלה בקורשבל: <i>שאלות</i>", f"{fd}: <i>שאלות</i>"), ("הצ'אלה הכשרה: <i>שאלות</i>", f"{kd}: <i>שאלות</i>"),
            ('alt="הצ\'אלה בואל טורנס, ', f'alt="{be}, '), ('alt="הצ\'אלה בקורשבל, ', f'alt="{fd}, '), ('alt="הצ\'אלה בלה דז אלפ, ', f'alt="{kd}, '),
            ('"הצ\'אלה בואל טורנס")', f'"{be}")')],
    }
    return P[d]

# 3. Menu « Chalets » et bande de vignettes (_zones.py CHALETS, HTML <b>lieu</b>détail) : le nom passe en gras, le lieu derrière.
MENU = {".": [(DA, "Les Deux Alpes", "6 + 1 bedrooms"), (SL, "Les Deux Alpes · Slope Chalet", "6 bedrooms"), (CO, "Courchevel", "5 suites · heated"),
              (ME, "Near Megève", "10 twin"), (VT, "Val Thorens", "3 en-suite")],
        "fr": [(DA, "Les Deux Alpes", "6 + 1 chambres"), (SL, "Les Deux Alpes · chalet des pistes", "6 chambres"), (CO, "Courchevel", "5 suites · piscines"),
               (ME, "Près de Megève", "10 chambres"), (VT, "Val Thorens", "3 chambres")],
        "es": [(DA, "Les Deux Alpes", "6 + 1 habitaciones"), (SL, "Les Deux Alpes · chalet de las pistas", "6 habitaciones"), (CO, "Courchevel", "5 suites · piscinas"),
               (ME, "Cerca de Megève", "10 habitaciones"), (VT, "Val Thorens", "3 habitaciones")],
        "he": [(DA, "לה דז אלפ", "6 + 1 חדרים"), (SL, "לה דז אלפ · צ'אלה המסלולים", "6 חדרים"), (CO, "קורשבל", "5 סוויטות"),
               (ME, "ליד מג'ב", "10 חדרי"), (VT, "ואל טורנס", "3 חדרי")]}

# 4. Title (sans « | Mishpacha Tours », 18 caractères) et description des 5 fiches : title <= 60, description <= 155.
META = {
 DA: {".": ("Chalet King David, kosher, Les Deux Alpes", "Chalet King David in Les Deux Alpes: a 300 m² kosher chalet, 6 bedrooms, 16 beds, 2 minutes from the slopes. Private chef, Shabbat and holidays. One quote."),
      "fr": ("Chalet King David, casher, Les Deux Alpes", "Chalet King David aux Deux Alpes : chalet casher de 300 m², 6 chambres, 16 lits, à 2 minutes des pistes. Chef privé, Chabbat et fêtes. Un seul devis écrit."),
      "es": ("Chalet King David, kosher, Les Deux Alpes", "Chalet King David en Les Deux Alpes: chalet kosher de 300 m², 6 habitaciones, 16 camas, a 2 minutos de las pistas. Chef privado, Shabat y fiestas."),
      "he": ("צ'אלה קינג דייוויד, לה דז אלפ: כשרה, שף", "צ'אלה קינג דייוויד בלה דז אלפ: צ'אלה כשרה של 300 מ״ר, 6 חדרי שינה ו-16 מיטות, 2 דקות מהמסלולים. שף פרטי, שבת וחגים, שירות מא' ועד ת'. הצעת מחיר אחת בכתב.")},
 SL: {".": ("Chalet Rochebrune, kosher, Les Deux Alpes", "Chalet Rochebrune in Les Deux Alpes: a kosher ski-in ski-out chalet, 6 bedrooms, 13 beds, fireplace, south terrace. Chef, Shabbat and minyan. One quote."),
      "fr": ("Chalet Rochebrune, casher, Les Deux Alpes", "Chalet Rochebrune aux Deux Alpes : chalet casher skis aux pieds, 6 chambres, 13 couchages, cheminée, terrasse plein sud. Chef, Chabbat et minyan."),
      "es": ("Chalet Rochebrune, kosher, Les Deux Alpes", "Chalet Rochebrune en Les Deux Alpes: chalet kosher a pie de pista, 6 habitaciones, 13 camas, chimenea y terraza al sur. Chef, Shabat y minyán."),
      "he": ("צ'אלה רושברון, לה דז אלפ: כשרה, סקי מהדלת", "צ'אלה רושברון בלה דז אלפ: צ'אלה כשרה עם מגלשיים בדלת, 6 חדרי שינה, 13 מיטות, אח ומרפסת הפונה דרומה. שף או ארוחות במשלוח, שבת ומניין. הצעת מחיר בכתב.")},
 CO: {".": ("Chalet Flocon Doré, kosher, Courchevel", "Chalet Flocon Doré in Courchevel: a kosher chalet with 5 en-suite bedrooms, heated pools and hammam, private chef, Shabbat and minyan. One written quote."),
      "fr": ("Chalet Flocon Doré, casher, Courchevel", "Chalet Flocon Doré à Courchevel : chalet strictement casher, 5 chambres en suite, piscines chauffées et hammam, chef privé, Chabbat et minyan."),
      "es": ("Chalet Flocon Doré, kosher, Courchevel", "Chalet Flocon Doré en Courchevel: chalet kosher con 5 habitaciones con baño, piscinas climatizadas y hammam, chef privado, Shabat y minyán."),
      "he": ("צ'אלה פלוקון דורה, קורשבל: כשרה, בריכות", "צ'אלה פלוקון דורה בלב קורשבל: צ'אלה כשרה עם 5 חדרי שינה עם חדר רחצה, בריכות מחוממות וחמאם, שף פרטי, שבת ומניין. הצעת מחיר אחת בכתב.")},
 ME: {".": ("Chalet Loup Blanc, kosher, near Megève", "Chalet Loup Blanc near Megève, facing Mont Blanc: ten twin bedrooms, two attic rooms, an apartment, sauna and jacuzzi. Kosher chef, Shabbat, minyan."),
      "fr": ("Chalet Loup Blanc, casher, près de Megève", "Chalet Loup Blanc près de Megève, face au Mont Blanc : dix chambres twin, deux sous le toit, un appartement, sauna et jacuzzi. Chef, Chabbat, minyan."),
      "es": ("Chalet Loup Blanc, kosher, cerca de Megève", "Chalet Loup Blanc cerca de Megève, frente al Mont Blanc: diez habitaciones twin, dos buhardillas, un apartamento, sauna y jacuzzi. Chef, Shabat, minyán."),
      "he": ("צ'אלה לו בלאן, ליד מג'ב: כשרה, שף, שבת", "צ'אלה לו בלאן ליד מג'ב, מול המון בלאן: עשרה חדרי טווין, שני חדרי עליית גג, דירה צמודה, סאונה וג'קוזי. שף כשר, שבת ומניין. הצעת מחיר אחת בכתב.")},
 VT: {".": ("Chalet Belle Étoile, kosher, Val Thorens", "Chalet Belle Étoile in Val Thorens: a private kosher chalet, ski path at the door, 3 en-suite bedrooms, up to 10 guests. Chef, Shabbat, minyan."),
      "fr": ("Chalet Belle Étoile, casher, Val Thorens", "Chalet Belle Étoile à Val Thorens : chalet casher privé, chemin skieur à la porte, 3 chambres en suite, jusqu'à 10 personnes. Chef, Chabbat, minyan."),
      "es": ("Chalet Belle Étoile, kosher, Val Thorens", "Chalet Belle Étoile en Val Thorens: chalet kosher privado, pista en la puerta, 3 habitaciones con baño, hasta 10 personas. Chef, Shabat, minyán."),
      "he": ("צ'אלה בל אטואל, ואל טורנס: כשרה, סקי מהדלת", "צ'אלה בל אטואל בואל טורנס: צ'אלה כשרה פרטית, פונה דרומה, שביל סקי ליד הדלת, שלושה חדרי שינה עם חדר רחצה, עד 10 אורחים. שף, שבת ומניין.")},
}

# 5. Autres pages ES : title (avec suffixe) <= 70 une fois désentité, description <= 170 (liste _qa.py du 30/10). None = inchangé.
ES_META = {
 "alps": (None, "Estrictamente kosher en los Alpes: chef privado en su chalé, comidas a domicilio, Shabat y fiestas en la estación, minyan y Sefer Torá. Una solicitud, un presupuesto."),
 "chrd-lyon": ("CHRD Lyon: museo de la Resistencia, la visita", None),
 "credits": (None, "Fuente, autor y licencia de cada fotografía de mishpachatours.com. Imágenes de Wikimedia Commons con licencias CC0, CC BY y CC BY-SA."),
 "flights-to-lyon": ("Vuelos a Lyon y el camino a las estaciones de esquí", "Vuelos a Lyon-Saint-Exupéry, el aeropuerto de Val Thorens, Courchevel y Alpe d'Huez: vuelos directos desde Tel Aviv, trayectos hasta las estaciones y compras kosher."),
 "grande-synagogue-lyon": (None, "La Gran Sinagoga de Lyon, de 1864, está cerrada a los visitantes fuera de las Jornadas Europeas del Patrimonio. Cómo entrar, horarios de oración y dirección."),
 "": (None, "Esquí kosher y chalés con chef privado en los Alpes, Shabat y minyan en la estación, traslados y el patrimonio judío de Lyon. Una solicitud, un programa día a día."),
 "is-lyon-safe-for-jewish-visitors": ("¿Es seguro Lyon para los visitantes judíos?", "Cómo Mishpacha Tours protege sus visitas judías privadas por Lyon: itinerarios discretos, una guía de la comunidad, escolta bajo petición. Los hechos, con fuentes."),
 "jewish-life-around-lyon": (None, "Sinagogas y casas Chabad en Grenoble, Annecy, Aix-les-Bains, Chambéry, Valence y Clermont-Ferrand, minyanim de invierno en Courchevel y Megève. Direcciones y teléfonos."),
 "jewish-lyon-guide": (None, "Restaurantes kosher, sinagogas, casas Chabad, cementerio judío y horarios de Shabat en Lyon y en los Alpes. Mapas, teléfonos, indicaciones. Revisado en octubre de 2026."),
 "jewish-lyon-tours": ("Visitas judías de Lyon, privadas y kosher", "La única visita que entra en la Gran Sinagoga de Lyon. Visitas judías privadas con una guía judía, observante y titulada. Kosher, shomer Shabat, precio por grupo."),
 "jewish-travel-lyon-faq": ("Viaje judío a Lyon: preguntas frecuentes", "Diecinueve respuestas directas para un viajero judío a Lyon: cómo llegar, kosher, Shabat, seguridad, oración y nuestras visitas privadas. Revisado en octubre de 2026."),
 "kosher-alpe-dhuez": ("Kosher en Alpe d&#x27;Huez: chef, Shabat, minián", None),
 "kosher-les-deux-alpes": ("Kosher en Les Deux Alpes: chef, Shabat, minián", None),
 "kosher-restaurants-lyon": (None, "31 restaurantes, panaderías, carnicerías, tiendas y caterings kosher en Lyon, Villeurbanne y Écully, todos en la lista oficial del Beth Din de Lyon."),
 "kosher-shabbat-meals-catering-lyon": (None, "Seis caterings certificados por el Beth Din de Lyon, comidas de Shabat de Chabad y tiendas kosher para un Shabat en un apartamento. Cómo encargar antes de aterrizar."),
 "kosher-vacation-french-alps": (None, "Unas vacaciones kosher en los Alpes: su chalé o apartamento, nuestro chef, comidas a domicilio, Shabat, fiestas y un minián. Esquí en invierno, lagos en verano."),
 "kosher-val-disere": ("Kosher en Val d&#x27;Isère: chef, Shabat, minián", None),
 "kosher-villa-saint-tropez": (None, "Villa Beach, una villa kosher junto al mar en Saint-Tropez: playa privada, 5 habitaciones para 12 personas, piscina climatizada, chef privado, Shabat y minyan."),
 "mikveh-lyon": ("Mikve en Lyon y Villeurbanne: direcciones", "Ocho mikvaot en Lyon y Villeurbanne con direcciones y teléfonos. La Mikve Haya Mouchka, 60 rue Crillon, abre todas las noches. Cómo preguntar antes de viajar."),
 "montluc-prison-lyon": ("Memorial de Montluc, Lyon: visita e historia", None),
 "plan-your-trip": (None, "Un solo formulario para todo su viaje: fechas, familia, chalé u hotel, chef y comidas, Shabat y minyan, traslados, esquí, visitas de Lyon. Un programa día por día."),
 "rue-juiverie-lyon": ("Rue Juiverie, Lyon: el antiguo barrio judío medieval", None),
 "summer-in-the-alps-jewish-families": ("Verano kosher en los Alpes para familias judías", None),
 "terms": (None, "Cómo funciona la reserva de una visita judía privada por Lyon: precio por grupo, pago, cancelación gratuita hasta 24 horas antes, entradas aparte, sin visitas en Shabat."),
}
HUB_ES = "Nuestros chalés kosher"
SUFFIXE = " | Mishpacha Tours"

def controle_longueurs():
    for slug, L in META.items():
        for d, (t, desc) in L.items():
            assert len(t) + len(SUFFIXE) <= 60, f"title > 60 : {slug} {d} ({len(t) + len(SUFFIXE)})"
            assert len(desc) <= 155, f"description > 155 : {slug} {d} ({len(desc)})"
    for p, (t, desc) in ES_META.items():
        if t: assert len(H.unescape(t)) + len(SUFFIXE) <= 70, f"title ES > 70 : {p}"
        if desc: assert len(desc) <= 170, f"description ES > 170 : {p} ({len(desc)})"

def meta_page(s, titre, desc):
    """Remplace title, og:title, description et og:description (et la même chaîne dans le JSON-LD)."""
    if titre is not None:
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        if m and m.group(1) != titre + SUFFIXE: s = s.replace(m.group(1), titre + SUFFIXE)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', rf'\g<1>{titre + SUFFIXE}\2', s)
    if desc is not None:
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        if m and m.group(1) != desc: s = s.replace(m.group(1), desc)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', rf'\g<1>{desc}\2', s)
    return s

def liens(s, slug, d):
    """Texte exact d'un lien vers la fiche (ou h3 d'une carte hub-carte) parmi les anciennes désignations -> nom complet."""
    vieux = set(ANCIENS.get((slug, d), []))
    def r(m):
        return m.group(1) + nom(slug, d) + m.group(3) if m.group(2).strip() in vieux else m.group(0)
    s = re.sub(rf'(<a\b[^>]*href="[^"]*/{slug}/[^"]*"[^>]*>)([^<]+)(</a>)', r, s)
    s = re.sub(rf'(<a class="hub-carte" href="[^"]*/{slug}/">(?:(?!</a>).)*?<h3>)([^<]+)(</h3>)', r, s, flags=re.S)
    return s

def fil(s, slug, d):
    """Dernier maillon du fil d'Ariane et BreadcrumbList : nom complet. Répare le fil HE de Val Thorens et le maillon ES anglais."""
    s = s.replace('<a href="/he/">הסעות בוואן</a> וואטסאפ, מענה באותו יום <a href="/he/kosher-chalets/">', '<a href="/he/">דף הבית</a> / <a href="/he/kosher-chalets/">')
    if d == "es": s = re.sub(r'(<p class="fil lead-fil">.*?kosher-chalets/">)Our kosher chalets(</a>)', rf'\1{HUB_ES}\2', s)
    m = re.search(r'<p class="fil lead-fil">.*? / ([^<]+)</p>', s)
    if m and m.group(1) != nom(slug, d):
        s = s[:m.start(1)] + nom(slug, d) + s[m.end(1):]
    m = re.search(r'<p class="fil lead-fil">(.*?)</p>', s)
    if m:   # BreadcrumbList JSON-LD = les maillons du fil visible, dans la langue de la page (les copies portaient l'anglais)
        maillons = re.findall(r"<a [^>]*>([^<]*)</a>", m.group(1)) + [m.group(1).rsplit(" / ", 1)[-1]]
        for i, texte in enumerate(maillons, 1):
            s = re.sub(rf'("position": {i}, "name": ")[^"]*(")', lambda mm: mm.group(1) + texte + mm.group(2), s, count=1)
    return s

def index_md(p):
    """Même fabrication que _agentic.py (section 3) : index.md à côté de index.html."""
    h = rd(p); d = os.path.dirname(p).replace("\\", "/").lstrip("./")
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    dm = re.search(r'<meta name="description" content="([^"]*)"', h)
    out = (f"> {dm.group(1) if dm else ''}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    pm = os.path.join(os.path.dirname(p), "index.md")
    if not os.path.exists(pm) or rd(pm) != out: open(pm, "w", encoding="utf-8").write(out); return 1
    return 0

def page(p, d):
    s0 = s = rd(p); dossier = os.path.dirname(p).replace("\\", "/")
    if d != ".": dossier = dossier[len(d):].strip("/")
    for a, b in paires(d): s = s.replace(a, b)
    for slug, old, det in MENU[d]: s = s.replace(f"<b>{old}</b>{det}", f"<b>{menu(slug, d)}</b>{det}")
    for slug in SLUGS: s = liens(s, slug, d)
    for a, b in prose(d): s = s.replace(a, b)
    if dossier in SLUGS:
        s = meta_page(s, *META[dossier][d]); s = fil(s, dossier, d)
    if d == "es" and dossier in ES_META: s = meta_page(s, *ES_META[dossier])
    if s != s0: wr(p, s); return 1
    return 0

def generateurs():
    k = 0
    for f in glob.glob("_*.py") + glob.glob("_pages/*.py"):
        if os.path.basename(f) in MOI or f.endswith("_sans_nombre_chalets.py"): continue
        s0 = s = rd(f)
        for a, b in paires("."): s = s.replace(a, b)
        for d in LANGS:                                        # _kit_wp.py T[lang][cle]["t"] et alt, 4 langues
            for slug, lst in ((sl, l) for (sl, dd), l in ANCIENS.items() if dd == d):
                for v in lst: s = s.replace(f't="{v}"', f't="{nom(slug, d)}"')
            for a, b in paires(d): s = s.replace(a, b)
            for slug, old, det in MENU[d]: s = s.replace(f'("{old}", "{det}', f'("{menu(slug, d)}", "{det}')
        for slug in SLUGS: s = liens(s, slug, ".")
        for d in LANGS:
            for a, b in prose(d): s = s.replace(a, b)
        if os.path.basename(f) == "kosher-chalet-les-deux-alpes.py": s = s.replace('h2="The kosher chalet: ', f'h2="{court(DA, ".")}: ')
        if f.startswith("_pages") and os.path.basename(f)[:-3] in META:  # title/desc EN de la fiche
            t, desc = META[os.path.basename(f)[:-3]]["."]
            s = re.sub(r'title="[^"]*"', f'title="{t}"', s, count=1); s = re.sub(r'desc="[^"]*"', f'desc="{desc}"', s, count=1)
        if s != s0: wr(f, s); k += 1; print("  générateur :", f)
    return k

NOMS_CONNUS = {x for L in NOMS.values() for v in L.values() for x in (v[0], v[0].split(",")[0])}
NAV = {"EN", "FR", "ES", "HE", "English", "Français", "Español", "עברית", "דברו איתנו בוואטסאפ"}
VESTIGES = ["Slope Chalet", "Mont Blanc Chalet", "Val Thorens Chalet", "15-bed", "15 couchages", "15 camas", "15 המיטות",
            "chalet des pistes", "chalet de las pistas", "צ'אלה המסלולים", "chalet du Mont Blanc", "chalet del Mont Blanc", "צ'אלה המון בלאן",
            "Five private chalets", "Cinco chalés kosher en los Alpes"]
NOMBRES = re.compile(r"\b(five|cinq|cinco|5)\b[^<.]{0,20}chal|חמש[^<.]{0,12}צ'אל", re.I)

def reste():
    """Ce qui reste à la main : liens vers une fiche sans son nom, vestiges des anciens noms, nombre de chalets."""
    out = []
    for p in sorted(glob.glob("**/index.html", recursive=True)):
        if p.startswith("_"): continue
        s = rd(p); corps = re.sub(r"<script.*?</script>", "", s, flags=re.S)
        for m in re.finditer(r'<a\b[^>]*href="[^"]*/(kosher-(?:slope-)?chalet-[a-z-]+)/[^"]*"[^>]*>(.*?)</a>', s, re.S):
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
            avant = s[max(0, m.start() - 160):m.start()]                 # « <b>Chalet King David, Les Deux Alpes.</b> <a>300 m²…</a> »
            if txt in NAV or any(n in txt or n in avant for n in NOMS_CONNUS): continue
            out.append(f"LIEN  {p}: {m.group(1)} -> {txt[:70]!r}")
        for v in VESTIGES:
            n = corps.count(v)
            if n: out.append(f"VIEUX {p}: {v!r} x{n}")
        for m in NOMBRES.finditer(corps): out.append(f"NOMBRE {p}: {m.group(0)!r}")
    return out

if __name__ == "__main__":
    controle_longueurs()
    touches = {d: 0 for d in LANGS}; md_n = 0
    for d in LANGS:
        for p in sorted(glob.glob("**/index.html" if d == "." else f"{d}/**/index.html", recursive=True)):
            p = p.replace("\\", "/")
            if d == "." and p.split("/")[0] in ("fr", "es", "he", "_pages"): continue
            if page(p, d): touches[d] += 1; md_n += index_md(p)
    for slug in SLUGS:                                         # les .md des fiches portent encore l'ancien h1 : toujours refaits
        for d in LANGS: md_n += index_md(f"{d}/{slug}/index.html")
    print("pages modifiées :", {("en" if d == "." else d): n for d, n in touches.items()}, "· index.md refaits :", md_n)
    print("générateurs modifiés :", generateurs())
    r = reste()
    print("reste à la main :", len(r))
    for l in r: print(" ", l)
