# -*- coding: utf-8 -*-
"""Chalet « Aigle Royal », Les Ménuires (3 Vallées), septième chalet, 02/11/2026 (Moshé : « ajouter au site, choisir les meilleures
photos et ajouter au CRM aussi »). Brief : 00-brief/2026-11-02-chalet-aigle-royal-brief.md.

Pourquoi un générateur par clonage : la chaîne idempotente (_zones, _kit_wp, _galerie_chalets, _contacts_bh_hebcal…) ne repasse plus
proprement sur le HTML actuel (test du 02/11 : _zones réécrit 292 pages, trois scripts plantent). Ce script part donc de la page
Val Thorens publiée dans chaque langue (toutes les passes déjà appliquées : charte, en-tête, formulaire, Shabbat, galerie), remplace
le contenu propre au chalet, puis branche le chalet ailleurs (menu Chalets, hub, accueil, /alps/, ski, station Val Thorens, bandes
« Prefer a whole chalet? », sitemap, llms.txt). Idempotent : relancer réécrit la page et ne duplique rien ailleurs.

🛑 Jamais le vrai nom du chalet, du hameau, le numéro d'enregistrement ni le site du propriétaire. Prix « Sur demande » tant que la
ligne ch6 de la grille de Mendel est vide (js/prix.js remplace le texte quand la clé ch6_basse_vente existe et est publique).
Ensuite : _aigle_royal_photos.py doit avoir tourné (img/chalet/aigle-*.jpg). Lancer depuis site-v5 : python _chalet_aigle_royal.py"""
import html as H
import io
import json
import re
import sys
import urllib.parse as U
from pathlib import Path
from PIL import Image

ICI = Path(__file__).resolve().parent
sys.argv = sys.argv[:1]
sys.path.insert(0, str(ICI))
import _kit_wp as K          # noqa: E402  (cartes, bandes mini : l'Aigle Royal y est déclaré sous la clé « ar »)
import _galerie_chalets as G  # noqa: E402  (galerie plein écran)

SLUG, MODELE = "kosher-chalet-les-menuires", "kosher-chalet-val-thorens"
BASE = "https://mishpachatours.com"
LANGS = ("en", "fr", "es", "he")
pfx = lambda l: "" if l == "en" else f"/{l}"
GC = G.CHALETS[SLUG]
HERO = GC["hero"]
STEMS = [s for _, _, ss in GC["pieces"] for s in ss]
ORDRE = STEMS   # ordre de la grille « en images » : celui des pièces

# ---------------------------------------------------------------- textes
TX = {
 "en": dict(
  title="Chalet Aigle Royal, kosher, Les Ménuires",
  desc="Chalet Aigle Royal in Les Ménuires, 3 Valleys: a private kosher chalet for 15 guests, 7 en-suite bedrooms, outdoor jacuzzi and sauna. Chef, Shabbat, minyan.",
  ital="7 bedrooms, jacuzzi and sauna",
  hero="A large wooden chalet in a quiet hamlet of Les Ménuires, in the 3 Valleys.",
  intro="A chairlift 230 metres away takes you up to the slopes in 7 minutes; a blue run brings you back to the chalet. Seven bedrooms, each with its own shower room, up to 15 guests. Outdoor jacuzzi, sauna, south balcony. Chef or delivered meals, Shabbat and minyan.",
  bref=[("map-pin", "Location.", "In a quiet hamlet just below Les Ménuires, in the 3 Valleys and their 600 km of slopes. A four-seat chairlift 230 metres from the door takes you up to the resort in 7 minutes; at the end of the day, a blue run brings you back to the chalet."),
        ("x-couch", "The living floor.", "On the first floor, a 50 m² living room with an open kitchen, a dining table for the whole group and a balcony facing south. Two bedrooms on the same floor."),
        ("bed-double", "Seven bedrooms,", "each with its own shower room and WC. Two on the ground floor, two on the first floor, three under the roof: a double, a twin and a triple. Two baby cots."),
        ("waves", "Jacuzzi and sauna.", "An outdoor jacuzzi, a sauna with its own shower, and a 20 m² games and TV lounge for the children."),
        ("snowflake", "Ski room.", "A large ski room with boot dryers, and a laundry room."),
        ("check", "Comforts.", "Built in 2006, renovated in 2022. Beds made on arrival, final cleaning included. Two parking spaces at the door, free public parking 50 metres away."),
        ("chef-hat", "Kitchen.", "Kashered by our team before you arrive, included. A chef cooks in the chalet, or kosher meals arrive ready to reheat.")],
  apres="The chalet welcomes up to 15 guests. Stays run from Sunday to Sunday. Availability is confirmed for your dates with each request.",
  shabbat="The chef prepares the Shabbat meals and the holidays in the chalet, or the meals arrive before candle lighting. The dining table seats the whole group. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your group, Shacharis takes place in your living room.",
  acces="<b>From Geneva airport.</b> About 2 h 30 by road. Lyon-Saint-Exupéry, about 2 h 45.",
  prix=("From €{ch6_basse_vente} per week", "Price on request"),
  faq=[("How many people can stay?", "Up to 15 guests in seven bedrooms, each with its own shower room and WC: two or three families together, or one large family with the grandparents. Two baby cots."),
       ("How do we get to the slopes?", "A four-seat chairlift 230 metres from the chalet takes you up to Les Ménuires in 7 minutes. At the end of the day, a blue run brings you back to the chalet."),
       ("Is there a jacuzzi and a sauna?", "Yes: an outdoor jacuzzi, a sauna with its own shower, and a games and TV lounge.")],
  alt="Chalet Aigle Royal", vt_lien="Chalet Belle Étoile, Val Thorens",
  noms=[("Chalet Belle Étoile", "Chalet Aigle Royal"), ("Belle Étoile", "Aigle Royal"), ("Val Thorens", "Les Ménuires")],
  web="Kosher chalet in Les Ménuires, 15 guests, jacuzzi and sauna",
  ld_desc="A private kosher chalet in Les Ménuires, in the 3 Valleys: seven en-suite bedrooms, up to 15 guests, outdoor jacuzzi and sauna, chairlift 230 m away. Chef or delivered meals, Shabbat and minyan."),
 "fr": dict(
  title="Chalet Aigle Royal, casher, Les Ménuires",
  desc="Le Chalet Aigle Royal aux Ménuires, 3 Vallées : chalet casher privé pour 15 personnes, 7 chambres avec salle d'eau, jacuzzi extérieur et sauna. Chef, Chabbat, minyan.",
  ital="7 chambres, jacuzzi et sauna",
  hero="Un grand chalet en bois dans un hameau tranquille des Ménuires, aux 3 Vallées.",
  intro="Un télésiège à 230 mètres vous monte sur les pistes en 7 minutes ; une piste bleue vous ramène au chalet. Sept chambres, chacune avec sa salle d'eau, jusqu'à 15 personnes. Jacuzzi extérieur, sauna, balcon plein sud. Chef ou repas livrés, Chabbat et minyan.",
  bref=[("map-pin", "Situation.", "Dans un hameau tranquille juste en dessous des Ménuires, au cœur des 3 Vallées et de leurs 600 km de pistes. Un télésiège quatre places, à 230 mètres de la porte, monte à la station en 7 minutes ; le soir, une piste bleue vous ramène au chalet."),
        ("x-couch", "L'étage de vie.", "Au premier étage, un séjour de 50 m² avec cuisine ouverte, une table pour tout le groupe et un balcon plein sud. Deux chambres au même étage."),
        ("bed-double", "Sept chambres,", "chacune avec sa salle d'eau et ses WC. Deux au rez-de-chaussée, deux au premier étage, trois sous le toit : une double, une à deux lits, une à trois lits. Deux lits bébé."),
        ("waves", "Jacuzzi et sauna.", "Un jacuzzi extérieur, un sauna avec sa douche, et un salon de jeux et de télévision de 20 m² pour les enfants."),
        ("snowflake", "Local à skis.", "Un grand local à skis avec sèche-chaussures, et une buanderie."),
        ("check", "Confort.", "Construit en 2006, rénové en 2022. Lits faits à l'arrivée, ménage de fin de séjour inclus. Deux places de parking devant la porte, parking public gratuit à 50 mètres."),
        ("chef-hat", "Cuisine.", "Cachérisée par notre équipe avant votre arrivée, incluse. Un chef cuisine au chalet, ou des repas casher arrivent prêts à réchauffer.")],
  apres="Le chalet accueille jusqu'à 15 personnes. Les séjours vont du dimanche au dimanche. La disponibilité est confirmée pour vos dates à chaque demande.",
  shabbat="Le chef prépare au chalet les repas de Chabbat et des fêtes, ou les repas arrivent avant l'allumage des bougies. La table accueille tout le groupe. Pour un minyan, nous amenons les ba'hourim et un Séfer Torah : avec les hommes de votre groupe, Cha'harit a lieu dans votre salon.",
  acces="<b>Depuis l'aéroport de Genève.</b> Environ 2 h 30 de route. Lyon-Saint-Exupéry, environ 2 h 45.",
  prix=("À partir de {ch6_basse_vente} € la semaine", "Prix sur demande"),
  faq=[("Combien de personnes peuvent séjourner ?", "Jusqu'à 15 personnes dans sept chambres, chacune avec sa salle d'eau et ses WC : deux ou trois familles ensemble, ou une grande famille avec les grands-parents. Deux lits bébé."),
       ("Comment rejoint-on les pistes ?", "Un télésiège quatre places, à 230 mètres du chalet, monte aux Ménuires en 7 minutes. En fin de journée, une piste bleue vous ramène au chalet."),
       ("Y a-t-il un jacuzzi et un sauna ?", "Oui : un jacuzzi extérieur, un sauna avec sa douche, et un salon de jeux et de télévision.")],
  alt="Le Chalet Aigle Royal", vt_lien="Chalet Belle Étoile, Val Thorens",
  noms=[("Chalet Belle Étoile", "Chalet Aigle Royal"), ("Belle Étoile", "Aigle Royal"), ("à Val Thorens", "aux Ménuires"), ("À Val Thorens", "Aux Ménuires"),
        ("de Val Thorens", "des Ménuires"), ("Val Thorens", "Les Ménuires")],
  web="Chalet casher aux Ménuires, 15 personnes, jacuzzi et sauna",
  ld_desc="Un chalet casher privé aux Ménuires, aux 3 Vallées : sept chambres avec salle d'eau, jusqu'à 15 personnes, jacuzzi extérieur et sauna, télésiège à 230 m. Chef ou repas livrés, Chabbat et minyan."),
 "es": dict(
  title="Chalet Aigle Royal, kosher, Les Ménuires",
  desc="Chalet Aigle Royal en Les Ménuires, 3 Valles: chalet kosher privado para 15 personas, 7 habitaciones con baño, jacuzzi exterior y sauna. Chef, Shabat, minyán.",
  ital="7 habitaciones, jacuzzi y sauna",
  hero="Un gran chalet de madera en una aldea tranquila de Les Ménuires, en los 3 Valles.",
  intro="Un telesilla a 230 metros le sube a las pistas en 7 minutos; una pista azul le devuelve al chalet. Siete habitaciones, cada una con su baño, hasta 15 personas. Jacuzzi exterior, sauna, balcón orientado al sur. Chef o comidas a domicilio, Shabat y minyán.",
  bref=[("map-pin", "Ubicación.", "En una aldea tranquila justo debajo de Les Ménuires, en los 3 Valles y sus 600 km de pistas. Un telesilla de cuatro plazas, a 230 metros de la puerta, sube a la estación en 7 minutos; por la tarde, una pista azul le devuelve al chalet."),
        ("x-couch", "La planta principal.", "En el primer piso, un salón de 50 m² con cocina abierta, una mesa para todo el grupo y un balcón orientado al sur. Dos habitaciones en la misma planta."),
        ("bed-double", "Siete habitaciones,", "cada una con su baño y aseo. Dos en la planta baja, dos en el primer piso y tres bajo el tejado: una doble, una con dos camas y una con tres camas. Dos cunas."),
        ("waves", "Jacuzzi y sauna.", "Un jacuzzi exterior, una sauna con su ducha y una sala de juegos y televisión de 20 m² para los niños."),
        ("snowflake", "Guardaesquís.", "Un gran guardaesquís con secadores de botas, y un lavadero."),
        ("check", "Comodidades.", "Construido en 2006 y renovado en 2022. Camas hechas a la llegada, limpieza final incluida. Dos plazas de aparcamiento delante de la puerta y aparcamiento público gratuito a 50 metros."),
        ("chef-hat", "Cocina.", "Kosherizada por nuestro equipo antes de su llegada, incluida. Un chef cocina en el chalet, o las comidas kosher llegan listas para calentar.")],
  apres="El chalet recibe hasta 15 personas. Las estancias van de domingo a domingo. La disponibilidad se confirma para sus fechas con cada solicitud.",
  shabbat="El chef prepara en el chalet las comidas de Shabat y de las fiestas, o las comidas llegan antes del encendido de las velas. La mesa acoge a todo el grupo. Para un minyán, traemos a los bojurim y un Séfer Torá: con los hombres de su grupo, Shajarit se reza en su salón.",
  acces="<b>Desde el aeropuerto de Ginebra.</b> Unas 2 h 30 por carretera. Lyon-Saint-Exupéry, unas 2 h 45.",
  prix=("Desde {ch6_basse_vente} € por semana", "Precio a consultar"),
  faq=[("¿Cuántas personas pueden alojarse?", "Hasta 15 personas en siete habitaciones, cada una con su baño y aseo: dos o tres familias juntas, o una gran familia con los abuelos. Dos cunas."),
       ("¿Cómo se llega a las pistas?", "Un telesilla de cuatro plazas, a 230 metros del chalet, sube a Les Ménuires en 7 minutos. Al final del día, una pista azul le devuelve al chalet."),
       ("¿Hay jacuzzi y sauna?", "Sí: un jacuzzi exterior, una sauna con su ducha y una sala de juegos y televisión.")],
  alt="El Chalet Aigle Royal", vt_lien="Chalet Belle Étoile, Val Thorens",
  noms=[("Chalet Belle Étoile", "Chalet Aigle Royal"), ("Belle Étoile", "Aigle Royal"), ("Val Thorens", "Les Ménuires")],
  web="Chalet kosher en Les Ménuires, 15 personas, jacuzzi y sauna",
  ld_desc="Un chalet kosher privado en Les Ménuires, en los 3 Valles: siete habitaciones con baño, hasta 15 personas, jacuzzi exterior y sauna, telesilla a 230 m. Chef o comidas a domicilio, Shabat y minyán."),
 "he": dict(
  title="צ'אלה אגל רויאל, לה מנואר: כשרה, ג'קוזי וסאונה",
  desc="צ'אלה אגל רויאל בלה מנואר, בשלושת העמקים: צ'אלה כשרה פרטית ל-15 אורחים, 7 חדרי שינה עם חדר מקלחת, ג'קוזי חיצוני וסאונה. שף, שבת ומניין.",
  ital="7 חדרים, ג'קוזי וסאונה",
  hero="צ'אלה גדולה מעץ בכפר קטן ושקט של לה מנואר, בשלושת העמקים.",
  intro="רכבל כיסאות במרחק 230 מטר מעלה אתכם למסלולים תוך 7 דקות, ומסלול כחול מחזיר אתכם לצ'אלה. שבעה חדרי שינה, לכל אחד חדר מקלחת משלו, עד 15 אורחים. ג'קוזי חיצוני, סאונה ומרפסת הפונה דרומה. שף או ארוחות במשלוח, שבת ומניין.",
  bref=[("map-pin", "מיקום.", "בכפר קטן ושקט ממש מתחת ללה מנואר, בשלושת העמקים, עם 600 קילומטרים של מסלולים. רכבל כיסאות בן ארבעה מושבים, 230 מטר מהדלת, מעלה לאתר תוך 7 דקות; בסוף היום, מסלול כחול מחזיר אתכם לצ'אלה."),
        ("x-couch", "קומת המגורים.", "בקומה הראשונה, סלון בן 50 מ״ר עם מטבח פתוח, שולחן אוכל לכל הקבוצה ומרפסת הפונה דרומה. שני חדרי שינה באותה קומה."),
        ("bed-double", "שבעה חדרי שינה,", "לכל אחד חדר מקלחת ושירותים משלו. שניים בקומת הקרקע, שניים בקומה הראשונה ושלושה בעליית הגג: חדר זוגי, חדר עם שתי מיטות וחדר עם שלוש מיטות. שתי מיטות תינוק."),
        ("waves", "ג'קוזי וסאונה.", "ג'קוזי חיצוני, סאונה עם מקלחת משלה, וחדר משחקים וטלוויזיה בן 20 מ״ר לילדים."),
        ("snowflake", "חדר סקי.", "חדר סקי גדול עם מייבשי נעלי סקי, וחדר כביסה."),
        ("check", "נוחות.", "נבנתה ב-2006 ושופצה ב-2022. המיטות מוצעות בהגעה, וניקיון סופי כלול. שני מקומות חניה מול הדלת, וחניון ציבורי חינם במרחק 50 מטר."),
        ("chef-hat", "מטבח.", "מוכשר בידי הצוות שלנו לפני שתגיעו, כלול במחיר. שף מבשל בצ'אלה, או שארוחות כשרות מגיעות מוכנות לחימום.")],
  apres="הצ'אלה מארחת עד 15 אורחים. השהייה מיום ראשון עד יום ראשון. הזמינות מאושרת לתאריכים שלכם בכל פנייה.",
  shabbat="השף מכין בצ'אלה את סעודות השבת והחגים, או שהארוחות מגיעות לפני הדלקת הנרות. שולחן האוכל מתאים לכל הקבוצה. למניין אנחנו מביאים בחורים וספר תורה: עם הגברים של הקבוצה שלכם, תפילת שחרית נערכת בסלון שלכם.",
  acces="<b>מנמל התעופה של ג'נבה.</b> כשעתיים וחצי בנסיעה. מנמל התעופה ליון-סנט-אקזופרי, כשלוש שעות פחות רבע.",
  prix=("החל מ־<bdi dir='ltr'>{ch6_basse_vente} €</bdi> לשבוע", "מחיר לפי בקשה"),
  faq=[("כמה אנשים יכולים להתארח?", "עד 15 אורחים בשבעה חדרי שינה, לכל אחד חדר מקלחת ושירותים משלו: שתיים-שלוש משפחות יחד, או משפחה גדולה עם הסבים והסבתות. שתי מיטות תינוק."),
       ("איך מגיעים למסלולים?", "רכבל כיסאות בן ארבעה מושבים, 230 מטר מהצ'אלה, מעלה ללה מנואר תוך 7 דקות. בסוף היום, מסלול כחול מחזיר אתכם לצ'אלה."),
       ("יש ג'קוזי וסאונה?", "כן: ג'קוזי חיצוני, סאונה עם מקלחת משלה, וחדר משחקים וטלוויזיה.")],
  alt="הצ'אלה בלה מנואר", vt_lien="צ'אלה בל אטואל, ואל טורנס",
  noms=[("בל אטואל", "אגל רויאל"), ("בואל טורנס", "בלה מנואר"), ("ואל טורנס", "לה מנואר")],
  web="צ'אלה כשרה בלה מנואר, 15 אורחים, ג'קוזי וסאונה",
  ld_desc="צ'אלה כשרה פרטית בלה מנואר, בשלושת העמקים: שבעה חדרי שינה עם חדר מקלחת, עד 15 אורחים, ג'קוזי חיצוני וסאונה, רכבל במרחק 230 מטר. שף או ארוחות במשלוח, שבת ומניין."),
}
import _chalets_textes_luxe as LUXE   # noqa: E402  (Moshé 02/11 : « on est une entreprise de luxe »)
LUXE.appliquer(TX, LUXE.AR)
for _l in TX:
    K.T[_l]["ar"]["s"] = LUXE.CARTE_AR[_l]
SUFFIXE = " | Mishpacha Tours"
VOILE = ('<style id="voile-heros">.lead-hero3::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;'
         'background:linear-gradient(180deg,rgba(17,17,17,.72) 0%,rgba(17,17,17,.6) 38%,rgba(17,17,17,.45) 70%,rgba(17,17,17,.4) 100%)}</style>')
attr_ = lambda v: H.escape(v, quote=False).replace('"', "&quot;")   # apostrophes en clair, comme le reste du site
COORD_VT, COORD_AR = "latitude=45.2978&longitude=6.5838", "latitude=45.3236&longitude=6.5389"   # Les Ménuires (station), Shabbat Hebcal


# ---------------------------------------------------------------- images
def webp(stem):
    src = ICI / "img" / "chalet" / f"{stem}.jpg"
    im = Image.open(src).convert("RGB")
    sorties = {ICI / "img" / "chalet" / "w" / f"{stem}-{w}.webp": w for w in (640, 960, 1280)}
    sorties.update({ICI / "img" / "chalet" / "min" / f"{stem}-{w}.webp": w for w in (336, 672)})
    if stem == HERO:
        sorties.update({ICI / "img" / "h" / f"{stem}-{w}.webp": w for w in (640, 960, im.width)})
    for d, w in sorties.items():
        if d.exists() and d.stat().st_mtime >= src.stat().st_mtime:
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        w = min(w, im.width)   # jamais d'agrandissement : le fichier « -1280 » garde la taille d'origine
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(d, "WEBP", quality=80, method=6)
    return im.size


DIM = {s: webp(s) for s in STEMS}


# ---------------------------------------------------------------- page du chalet
def remplace_noms(x, lang):
    for a, b in TX[lang]["noms"]:
        x = x.replace(a, b)
    return x


def wa_liens(x, lang):
    """Messages WhatsApp encodés : on décode, on change les noms, on réencode."""
    def f(m):
        t = U.unquote(m.group(2))
        t2 = remplace_noms(t, lang)
        return m.group(1) + (U.quote(t2, safe="/") if t2 != t else m.group(2))
    return re.sub(r'(wa\.me/\d+\?text=)([^"\'&]+)', f, x)


def grille(lang, h_modele):
    """Section « Le chalet en images » : même balisage que celle de Val Thorens."""
    a = h_modele.find('<section class="ss wrap chalet-images"')
    b = h_modele.find("</section>", a) + len("</section>")
    s = h_modele[a:b]
    n = len(ORDRE)
    tete = s[: s.find('<div class="ci-grille"')]
    aria = re.search(r'aria-label="([^"]*?)1([^"]*?)13"', s)
    tout = re.search(r'(class="ci-tout"[^>]*>)([^<]*)<', s).group(2).replace("13", str(n))
    nom = TX[lang]["alt"]
    btns = []
    for i, st in enumerate(ORDRE):
        piece = next(G.PIECE[pk][lang] for _, pk, ss in GC["pieces"] if st in ss)
        w, hh = DIM[st]
        taille = "(min-width:900px) 50vw, 100vw" if i == 0 else "(min-width:900px) 25vw, 50vw"
        cache = " hidden" if i >= 8 else ""
        alt = f"{nom}, {piece if lang == 'he' else piece[0].lower() + piece[1:]}"
        btns.append(f'<button type="button" class="ci-tuile"{cache} data-ci="{i}" aria-label="{aria.group(1)}{i + 1}{aria.group(2)}{n}">'
                    f'<img alt="{H.escape(alt)}" sizes="{taille}" loading="lazy" src="/img/chalet/w/{st}-960.webp" '
                    f'srcset="/img/chalet/w/{st}-640.webp 640w, /img/chalet/w/{st}-960.webp {min(960, w)}w, /img/chalet/{st}.jpg {w}w" '
                    f'width="{w}" height="{hh}" decoding="async"></button>')
    return (tete + f'<div class="ci-grille" data-n="{n}">' + "".join(btns) + "</div>"
            f'<p class="ci-pied"><button type="button" class="ci-tout" data-gal-open aria-haspopup="dialog" aria-controls="galerie">{tout}</button></p></section>')


def remplace_section(h, debut, html_neuf):
    a = h.find(debut)
    assert a >= 0, debut
    b = h.find("</section>", a) + len("</section>")
    return h[:a] + html_neuf + h[b:]


def page(lang):
    t = TX[lang]
    src = ICI / (MODELE if lang == "en" else f"{lang}/{MODELE}") / "index.html"
    h = io.open(src, encoding="utf-8", newline="").read()
    i_main, i_fin = h.find("<main>"), h.find("<footer")
    tete, main, pied = h[:i_main], h[i_main:i_fin], h[i_fin:]

    # --- tête : title, description, canonical, og, hreflang, JSON-LD
    titre = t["title"] + SUFFIXE
    tete = re.sub(r"<title>.*?</title>", f"<title>{H.escape(titre, quote=False)}</title>", tete, flags=re.S)
    for attr, val in (('name="description"', t["desc"]), ('property="og:title"', titre), ('property="og:description"', t["desc"])):
        tete = re.sub(rf'(<meta {attr} content=")[^"]*(")', lambda m: m.group(1) + attr_(val) + m.group(2), tete)
    tete = re.sub(r'(<link rel="(?:canonical|alternate)"[^>]*href="[^"]*/)' + MODELE + '/', r"\g<1>" + SLUG + "/", tete)
    tete = re.sub(r'(<meta property="og:url" content="[^"]*/)' + MODELE + '/', r"\g<1>" + SLUG + "/", tete)
    # sélecteur de langue (en-tête et panneau)
    langues = lambda m: re.sub(r'(href="(?:/(?:fr|es|he))?/)' + MODELE + '/"', r'\g<1>' + SLUG + '/"', m.group(0))
    tete = re.sub(r'<details class="langue">.*?</details>', langues, tete, flags=re.S)   # seulement le sélecteur de langue,
    tete = re.sub(r'<div class="panneau-langs">.*?</div>', langues, tete, flags=re.S)   # jamais le lien Belle Étoile du menu

    # voile sombre en haut du héros : la photo a un ciel clair, le fil d'Ariane tombait à 1,4:1 (qa_site du 02/11) ;
    # dégradé léger sans cadre ni pastille, comme décidé par Moshé le 01/11 pour les héros des Alpes
    if 'id="voile-heros"' not in tete:
        tete = tete.replace("</head>", VOILE + "\n</head>", 1)

    # --- contenu
    mini_a = main.find("<!--KIT-WP:mini-->"); mini_b = main.find("<!--/KIT-WP:mini-->") + len("<!--/KIT-WP:mini-->")
    mini_vt = main[mini_a:mini_b]
    main = main[:mini_a] + "@@MINI@@" + main[mini_b:]
    suite_a = main.find('<section class="clair ss wrap conseils"><h2>', main.find('<section class="ss lead-final"'))
    suite_b = main.find("</section>", suite_a) + len("</section>")
    suite = main[suite_a:suite_b]
    main = main[:suite_a] + "@@SUITE@@" + main[suite_b:]

    # héros
    main = re.sub(r'<img src="/img/h/valthorens-exterieur-neige-960\.webp"[^>]*>',
                  f'<img src="/img/h/{HERO}-960.webp" srcset="/img/h/{HERO}-640.webp 640w, /img/h/{HERO}-960.webp 960w, /img/h/{HERO}-{DIM[HERO][0]}.webp {DIM[HERO][0]}w" sizes="100vw" alt="" width="{DIM[HERO][0]}" height="{DIM[HERO][1]}" fetchpriority="high">', main, count=1)
    main = re.sub(r"(<h1>[^<]*<br><i>)[^<]*(</i></h1>)", lambda m: m.group(1) + H.escape(t["ital"], quote=False) + m.group(2), main, count=1)
    main = re.sub(r'(</h1>\s*<p>)[^<]*(</p>)', lambda m: m.group(1) + H.escape(t["hero"], quote=False) + m.group(2), main, count=1)
    # intro (après le manifeste) et rappel dans le bloc Shabbat
    main = re.sub(r'(<!--/MANIFESTE--><p>)[^<]*(</p>)', lambda m: m.group(1) + H.escape(t["intro"], quote=False) + m.group(2), main, count=1)
    main = re.sub(r'(<p class="sh-sur">)[^<]*(</p>)', lambda m: m.group(1) + H.escape(t["intro"], quote=False) + m.group(2), main, count=1)
    # en bref
    a = main.find('<section class="clair clair-2 ss wrap conseils">')
    h2 = re.search(r"<h2>.*?</h2>", main[a:]).group(0)
    lis = "\n".join(f'<li><img class="dk dk-ico dk-des" src="/img/ico/or/{ic}.svg" alt="" width="96" height="96" loading="lazy"><b>{H.escape(b, quote=False)}</b> {H.escape(x, quote=False)}</li>'
                    for ic, b, x in t["bref"])
    main = remplace_section(main, '<section class="clair clair-2 ss wrap conseils">',
                            f'<section class="clair clair-2 ss wrap conseils">{h2}<ul class="dk-cartes dk-rail">\n{lis}\n</ul>\n<p>{H.escape(t["apres"], quote=False)}</p></section>')
    # grille de photos
    main = remplace_section(main, '<section class="ss wrap chalet-images"', grille(lang, h))
    # Shabbat au chalet : le premier paragraphe (taille de la table)
    main = re.sub(r'(<div class="clair ss beige dk-recit"><div class="wrap"><h2>.*?</h2><p><img[^>]*>)[^<]*(</p>)',
                  lambda m: m.group(1) + H.escape(t["shabbat"], quote=False) + m.group(2), main, count=1, flags=re.S)
    # accès : la première ligne (temps de route)
    main = re.sub(r'(<li><img class="dk dk-ico dk-des" src="/img/ico/or/plane\.svg"[^>]*>).*?(</li>)', lambda m: m.group(1) + t["acces"] + m.group(2), main, count=1, flags=re.S)
    # Shabbat Hebcal : coordonnées des Ménuires
    main = main.replace(COORD_VT, COORD_AR)
    # FAQ : prix sur demande, questions 2 à 4 propres au chalet, 5 et 6 gardées
    a = main.find('<section class="clair clair-2 ss wrap faq">'); b = main.find("</section>", a)
    faq = main[a:b]
    det = re.findall(r"<details>.*?</details>", faq, flags=re.S)
    assert len(det) == 6, len(det)
    tpl, repli = t["prix"]
    d0 = re.sub(r"<span data-prix-tpl='[^']*'>.*?</span>", f"<span data-prix-tpl=\"{attr_(tpl)}\">{repli}</span>", det[0], count=1, flags=re.S)
    neuves = [f"<details><summary>{H.escape(q, quote=False)}</summary><p>{H.escape(r, quote=False)}</p></details>" for q, r in t["faq"]]
    faq_neuve = faq[: faq.find("<details>")] + d0 + "".join(neuves) + det[4] + det[5] + faq[faq.rfind("</details>") + len("</details>"):]
    main = main[:a] + faq_neuve + main[b:]
    # noms et liens WhatsApp
    main = wa_liens(main, lang)
    main = remplace_noms(main, lang)
    main = main.replace("lieu=Val%20Thorens", "lieu=" + t.get("lieu_q", "Les%20M%C3%A9nuires"))

    # « À lire aussi » : le chalet de Val Thorens (même domaine) à la place de Courchevel
    voisin = t.get("voisin", MODELE)   # chalet voisin proposé dans « À lire aussi » (Aigle Royal : Belle Étoile ; Courchevel : Flocon Doré)
    suite = re.sub(r'<a href="(?:\.\./|/(?:fr|es|he)/)kosher-chalet-courchevel/">[^<]*</a>',
                   lambda m: m.group(0).split('"')[0] + '"' + m.group(0).split('"')[1].replace("kosher-chalet-courchevel", voisin) + '">' + H.escape(t["vt_lien"], quote=False) + "</a>", suite, count=1)
    for a, b in t.get("suite_noms", []):   # station proposée (lot 2 : Courchevel au lieu de Val Thorens)
        suite = suite.replace(a, b)
    main = main.replace("@@SUITE@@", suite)
    # bande « un chalet entier ? » : les autres chalets, dont Belle Étoile
    main = main.replace("@@MINI@@", K.bloc("mini", K.mini(lang, SLUG)))

    # --- galerie plein écran (après </main>) et après-pied
    pied = re.sub(r"<!--GALERIE:overlay-->.*?<!--/GALERIE:overlay-->", lambda m: G.bloc_overlay(lang, GC), pied, flags=re.S)
    if "<!--GALERIE:overlay-->" not in pied:
        main = re.sub(r"<!--GALERIE:overlay-->.*?<!--/GALERIE:overlay-->", lambda m: G.bloc_overlay(lang, GC), main, flags=re.S)
    pied = wa_liens(pied, lang)

    h = tete + main + pied
    h = jsonld(h, lang)
    # contrôles : aucun reste de Val Thorens hors menu, bandes et pied
    corps = h[h.find("<main>"):h.find("<!--KIT-WP:mini-->")]
    for mot in ("Val Thorens", "Belle Étoile", "valthorens", "ואל טורנס", "בל אטואל", "ch5_"):
        assert mot not in corps, (lang, mot, corps[max(0, corps.find(mot) - 120):corps.find(mot) + 60])
    for interdit in ("Cabri", "Bettaix", "lerefugeducabri"):
        assert interdit.lower() not in h.lower(), interdit
    dst = ICI / (SLUG if lang == "en" else f"{lang}/{SLUG}") / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    io.open(dst, "w", encoding="utf-8", newline="").write(h)
    return dst


def texte(x):
    return H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).strip()


def jsonld(h, lang):
    t = TX[lang]
    url = f"{BASE}{pfx(lang)}/{SLUG}/"
    def f(m):
        d = json.loads(m.group(1))
        lst = d if isinstance(d, list) else [d]
        out = []
        for x in lst:
            ty = x.get("@type")
            if ty == "BreadcrumbList":
                x["itemListElement"][-1]["name"] = texte(re.search(r'<p class="fil lead-fil">.*?/[^/]*/\s*([^<]*)</p>', h, re.S).group(1))
                x["itemListElement"][-1]["item"] = url
            elif ty == "FAQPage":
                faq = h[h.find('<section class="clair clair-2 ss wrap faq">'):]
                faq = faq[:faq.find("</section>")]
                x["mainEntity"] = [{"@type": "Question", "name": texte(q), "acceptedAnswer": {"@type": "Answer", "text": texte(r)}}
                                   for q, r in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", faq, flags=re.S)]
            elif ty == "WebPage":
                x.update({"@id": url, "url": url, "name": t["web"], "description": t["ld_desc"]})
            elif ty == "Service":
                lieu = t.get("svc", "Les Ménuires")
                x.update({"name": f"Kosher chalet in {lieu}", "areaServed": {"@type": "Place", "name": lieu},
                          "serviceType": f"Kosher chalet with chef or delivered meals, Shabbat and minyan in {lieu}", "url": url})
                x.pop("offers", None)   # prix sur demande : aucun montant tant que Mendel n'a pas rempli la grille
            out.append(x)
        return '<script type="application/ld+json">' + json.dumps(out if isinstance(d, list) else out[0], ensure_ascii=False) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', f, h, flags=re.S)


# ---------------------------------------------------------------- branchements ailleurs
def lire(p):
    return io.open(p, encoding="utf-8", newline="").read()


def ecrire(p, s, o):
    if s != o:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
        return 1
    return 0


def carte_ar(lang):
    """Carte du chalet (kit Winter Prestige) avec la ligne de prix branchée sur la grille."""
    c = K.carte(lang, "ar")
    tpl, repli = TX[lang]["prix"]
    return c.replace('<p class="kwp-dispo">', f'<p class="kwp-prix" data-prix-tpl="{attr_(tpl)}">{repli}</p><p class="kwp-dispo">', 1)


def carte_vth_fin(s):
    """Fin de la carte Val Thorens dans un bloc (l'Aigle Royal se pose juste après)."""
    i = s.find('href="/kosher-chalet-val-thorens/"') if 'href="/kosher-chalet-val-thorens/"' in s else -1
    return i


def apres_carte_vth(bloc, lang):
    lien = f'href="{pfx(lang)}/{MODELE}/"'
    i = bloc.find(lien)
    while i >= 0 and bloc.rfind('<article class="kwp-carte', 0, i) < 0:
        i = bloc.find(lien, i + 1)
    j = bloc.find("</article>", i) + len("</article>")
    return bloc[:j] + carte_ar(lang) + bloc[j:]


def retirer(s, lang, slug):
    """Enlève l'entrée de menu et les cartes déjà posées pour ce chalet (relancer met le texte à jour)."""
    p = pfx(lang)
    s = re.sub(rf'<a class="nav-ch-v" href="{p}/{slug}/">.*?</a>', "", s, flags=re.S)
    return re.sub(rf'<article class="kwp-carte[^"]*">(?:(?!</article>).)*?href="{p}/{slug}/"(?:(?!</article>).)*?</article>', "", s, flags=re.S)


def brancher():
    n = 0
    nav_tpl = {}
    for lang in LANGS:
        nav = (K.NAV_CH[lang][2][[u for u, _ in K.CH_URL].index(SLUG)][0], LUXE.NAV_AR[lang])
        nav_tpl[lang] = (f'<a class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"><img src="/img/chalet/min/{HERO}-336.webp" alt="" width="96" height="64" loading="lazy">'
                         f'<span><b>{H.escape(nav[0], quote=False)}</b>{H.escape(nav[1], quote=False)}</span></a>')
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = r[len(lang) + 1:] if lang != "en" else r
        slug = slug[: -len("index.html")].strip("/")
        s = lire(p); o = s
        s = retirer(s, lang, SLUG)
        # menu « Chalets » de l'en-tête
        if f'class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"' not in s:
            s = re.sub(rf'(<a class="nav-ch-v" href="{pfx(lang)}/{MODELE}/">.*?</a>)', lambda m: m.group(1) + nav_tpl[lang], s, count=1, flags=re.S)
        # liste des pages hiver (fondu entre chartes)
        s = s.replace('"kosher-chalet-val-thorens"];', '"kosher-chalet-val-thorens","kosher-chalet-les-menuires"];')
        # cartes : accueil, hub, /alps/, ski, station Val Thorens
        for nom in ("accueil", "hub", "duo", "vth"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{pfx(lang)}/{SLUG}/"' not in m.group(0):
                b = apres_carte_vth(m.group(0), lang)
                b = b.replace("kwp-cartes kwp-cinq", "kwp-cartes kwp-six").replace("kwp-cartes kwp-seule", "kwp-cartes")
                if nom == "vth":
                    b = re.sub(r"<h2>.*?</h2>", f"<h2>{K.VTH_H2[lang][0]} <i>{K.VTH_H2[lang][1]}</i></h2>", b, count=1, flags=re.S)
                s = s[:m.start()] + b + s[m.end():]
        # hub : même voile en haut du héros (fil d'Ariane à 4,2:1 au qa_site du 02/11)
        if slug == "kosher-chalets" and 'id="voile-heros"' not in s:
            s = s.replace("</head>", VOILE + "\n</head>", 1)
        # bande « un chalet entier ? » des stations et des autres chalets
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug != SLUG and f'href="{pfx(lang)}/{SLUG}/"' not in m.group(0):
            sauf = slug if slug in [u for u, _ in K.CH_URL] else None
            s = s[:m.start()] + K.bloc("mini", K.mini(lang, sauf)) + s[m.end():]
        n += ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = lire(p); o = s
    if f"/{SLUG}/" not in s:
        m = re.search(r"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/kosher-chalet-val-thorens/</loc>.*?</url>", s, flags=re.S)
        assert m, "Val Thorens absent du sitemap"
        bloc = m.group(0).replace(MODELE, SLUG)
        bloc = re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>2026-11-02</lastmod>", bloc)
        s = s[:m.end()] + "\n" + bloc + s[m.end():]
        for lang in ("fr", "es", "he"):
            m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}/kosher-chalet-val-thorens/</loc>.*?</url>", s, flags=re.S)
            if m:
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>2026-11-02</lastmod>", m.group(0).replace(MODELE, SLUG))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
    n = ecrire(p, s, o)
    p = ICI / "llms.txt"; s = lire(p); o = s
    if f"/{SLUG}/" not in s:
        lignes = s.split("\n")
        i = next(k for k, l in enumerate(lignes) if f"/{MODELE}/" in l)
        lignes.insert(i + 1, f"- [Chalet Aigle Royal, kosher, Les Ménuires]({BASE}/{SLUG}/): private kosher chalet in Les Ménuires (3 Valleys), 15 guests, 7 en-suite bedrooms, outdoor jacuzzi and sauna, chairlift 230 m away; price on request.")
        s = "\n".join(lignes)
    return n + ecrire(p, s, o)


def index_md(p):
    """Version Markdown servie aux agents IA (Accept: text/markdown), même recette que _agentic.py."""
    from markdownify import markdownify as md
    h = lire(p)
    d = p.parent.relative_to(ICI).as_posix()
    body = re.search(r"<main.*?</main>", h, re.S).group(0)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    desc = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    url = f"{BASE}/{d}/"
    text = re.sub(r"\n{3,}", "\n\n", md(body, heading_style="ATX", strip=["img"], bullets="-")).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M):
        text = f"# {title}\n\n" + text
    out = (f"> {desc}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    open(p.parent / "index.md", "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    for lang in LANGS:
        dst = page(lang)
        index_md(dst)
        print("page", dst.relative_to(ICI))
    print("pages branchées :", brancher())
    print("sitemap + llms :", sitemap_llms())
