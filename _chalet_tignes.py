# -*- coding: utf-8 -*-
"""Chalet de Tignes (Espace Killy), clé ch9, 02/11/2026 : deux chalets mitoyens qui communiquent, loués ensemble, 9 suites, jusqu'à
21 personnes, deux jacuzzis extérieurs, à une minute des pistes (Mendel 02/11 : PAS skis aux pieds). Même moteur que _chalet_aigle_royal.py et _chalets_courchevel_lot2.py (clone
de la page Val Thorens publiée), carte et menu posés après le dernier chalet (Renard Argenté). Idempotent.
Nom commercial : _chalet_tignes_nom.py (une constante). Photos : _chalet_tignes_photos.py doit avoir tourné.
🛑 Jamais le nom d'origine des deux chalets, de l'exploitant, de la piste ni du quartier de la station (liste dans 00-brief, hors site).
Pas de page station Tignes : aucun Beth Habad ni minyan local promis, seul le bloc casher standard du gabarit. Prix « Sur demande »
tant que la ligne ch9 de la grille de Mendel est vide. Hébreu à faire relire (skill relecture-hebreu) avant mise en ligne.
Lancer depuis site-v5 : python _chalet_tignes.py"""
import html as H
import re
import sys
from pathlib import Path

PAGE_SEUL = "--page" in sys.argv   # avant l'import de A, qui vide sys.argv
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import _chalet_aigle_royal as A   # noqa: E402  (page(), jsonld(), index_md(), webp(), K, G)
from _chalet_tignes_nom import NOM, NOM_HE   # noqa: E402

K, G = A.K, A.G
LANGS = A.LANGS
pfx = A.pfx
SLUG, CH, CLE = "kosher-chalet-tignes", "ch9", "tg"
COORD = "latitude=45.4683&longitude=6.9056"   # Tignes, Shabbat Hebcal
CUISINE = {l: A.TX[l]["bref"][-1] for l in LANGS}   # ligne « cuisine casher » commune (chef-hat)
_LISTE = ICI.parents[1] / "00-brief" / "references" / "2026-11-02-chalet-tignes" / "interdits.txt"   # hors du dépôt public du site
INTERDITS = re.compile(r"(" + "|".join(l.strip() for l in _LISTE.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")) + r")", re.I)

PRIX = {"en": ("From €{%s_basse_vente} per week", "Price on request"), "fr": ("À partir de {%s_basse_vente} € la semaine", "Prix sur demande"),
        "es": ("Desde {%s_basse_vente} € por semana", "Precio a consultar"), "he": ("החל מ־<bdi dir='ltr'>{%s_basse_vente} €</bdi> לשבוע", "מחיר לפי בקשה")}

T = {
 "en": dict(
  title=f"Kosher Chalet {NOM}, Tignes",
  desc=f"Chalet {NOM} in Tignes, Espace Killy: two adjoining luxury kosher chalets for up to 21 guests, nine suites, two outdoor jacuzzis, one minute from the slopes.",
  ital="Tignes, nine suites, one minute from the slopes", hero="Two adjoining chalets in Tignes, at the heart of the Espace Killy, one minute from the slopes.",
  intro="Two adjoining chalets that connect inside, taken together: nine suites, each with its own shower room, for up to 21 guests. The slopes are one minute away on foot. Two outdoor jacuzzis facing the peaks, two living rooms with a fireplace. A private chef, Shabbat and minyan, arranged for you.",
  bref=[("map-pin", "One minute from the slopes.", "In Tignes, at the heart of the Espace Killy. The slopes are less than a minute on foot from the chalet."),
        ("house", "Two chalets that connect.", "Two adjoining chalets, connected inside and taken together: each family has its own chalet, and everyone meets at the table. Three floors in each."),
        ("bed-double", "Nine suites,", "nine shower rooms, up to 21 guests, each suite with a balcony or the terrace. A family suite with a bunk room for the children, a master suite under the roof with an extra single bed."),
        ("waves", "Two jacuzzis.", "Two outdoor jacuzzis facing the peaks, for the end of the ski day."),
        ("x-couch", "Two living rooms, two tables.", "In each chalet, an open living room with a fireplace and corner sofas, a fitted kitchen and a table for twelve.")],
  apres="The two chalets welcome up to 21 guests together. Availability is confirmed for your dates with each request.",
  shabbat="The chef prepares the Shabbat and holiday meals in the chalet, or the meals arrive before candle lighting. Two tables for twelve, one in each chalet. A private minyan and a Sefer Torah on request: tell us your dates early.",
  acces="<b>From Lyon-Saint-Exupéry.</b> About 2 h 45 by road. Geneva, about 2 h 45 to 3 h.",
  faq=[("How many guests?", "Up to 21 guests in nine suites, each with its own shower room: several families together, each in its own chalet, connected inside."),
       ("How far are the slopes?", "Less than a minute on foot from the chalet."),
       ("Can we rent only one of the two chalets?", "The two chalets are rented together, for one group. Each has its own kitchen, its own living room and its own table for twelve.")],
  alt=f"Chalet {NOM}", vt_lien="Chalet Flocon Doré, Courchevel", suite_noms=[("kosher-val-thorens/", "kosher-val-disere/"), ("Val Thorens", "Val d'Isère")],
  noms=[("Chalet Belle Étoile", f"Chalet {NOM}"), ("Belle Étoile", NOM), ("Val Thorens", "Tignes")],
  web=f"Luxury kosher chalet in Tignes, up to 21 guests, nine suites, two jacuzzis",
  ld_desc="Two adjoining private kosher chalets in Tignes, Espace Killy, rented together: nine suites with shower rooms for up to 21 guests, two outdoor jacuzzis, the slope less than a minute away. Chef or delivered meals, Shabbat and minyan."),
 "fr": dict(
  title=f"Chalet casher {NOM}, Tignes",
  desc=f"Le Chalet {NOM} à Tignes, Espace Killy : deux chalets casher de luxe mitoyens pour 21 personnes, neuf suites, deux jacuzzis extérieurs, à une minute des pistes.",
  ital="Tignes, neuf suites, à une minute des pistes", hero="Deux chalets mitoyens à Tignes, au cœur de l'Espace Killy, à une minute des pistes.",
  intro="Deux chalets mitoyens qui communiquent, loués ensemble : neuf suites, chacune avec sa salle de douche, jusqu'à 21 personnes. Les pistes sont à une minute à pied. Deux jacuzzis extérieurs face aux sommets, deux salons avec cheminée. Chef privé, Chabbat et minyan, organisés pour vous.",
  bref=[("map-pin", "À une minute des pistes.", "À Tignes, au cœur de l'Espace Killy. Les pistes sont à moins d'une minute à pied du chalet."),
        ("house", "Deux chalets qui communiquent.", "Deux chalets mitoyens, reliés de l'intérieur et loués ensemble : chaque famille a son chalet, tout le monde se retrouve à table. Trois niveaux dans chacun."),
        ("bed-double", "Neuf suites,", "neuf salles de douche, jusqu'à 21 personnes, chaque suite avec son balcon ou la terrasse. Une suite familiale avec chambre d'enfants à lits superposés, une suite parentale sous les toits avec un lit simple en plus."),
        ("waves", "Deux jacuzzis.", "Deux jacuzzis extérieurs face aux sommets, pour la fin de la journée de ski."),
        ("x-couch", "Deux salons, deux tables.", "Dans chaque chalet, un salon ouvert avec cheminée et canapés d'angle, une cuisine équipée et une table de douze couverts.")],
  apres="Les deux chalets accueillent ensemble jusqu'à 21 personnes. La disponibilité est confirmée pour vos dates à chaque demande.",
  shabbat="Le chef prépare au chalet les repas de Chabbat et des fêtes, ou les repas arrivent avant l'allumage des bougies. Deux tables de douze couverts, une dans chaque chalet. Minyan privé et Séfer Torah sur demande : donnez-nous vos dates tôt.",
  acces="<b>Depuis Lyon-Saint-Exupéry.</b> Environ 2 h 45 par la route. Depuis Genève, environ 2 h 45 à 3 h.",
  faq=[("Combien de personnes ?", "Jusqu'à 21 personnes dans neuf suites, chacune avec sa salle de douche : plusieurs familles ensemble, chacune dans son chalet, reliés de l'intérieur."),
       ("Les pistes sont-elles loin ?", "À moins d'une minute à pied du chalet."),
       ("Peut-on louer un seul des deux chalets ?", "Les deux chalets se louent ensemble, pour un seul groupe. Chacun a sa cuisine, son salon et sa table de douze couverts.")],
  alt=f"Le Chalet {NOM}", vt_lien="Chalet Flocon Doré, Courchevel", suite_noms=[("kosher-val-thorens/", "kosher-val-disere/"), ("Val Thorens", "Val d’Isère")],
  noms=[("Chalet Belle Étoile", f"Chalet {NOM}"), ("Belle Étoile", NOM), ("Val Thorens", "Tignes")],
  web=f"Chalet casher de luxe à Tignes, 21 personnes, neuf suites, deux jacuzzis",
  ld_desc="Deux chalets casher privés et mitoyens à Tignes, Espace Killy, loués ensemble : neuf suites avec salle de douche pour 21 personnes, deux jacuzzis extérieurs, la piste à moins d'une minute. Chef ou repas livrés, Chabbat et minyan."),
 "es": dict(
  title=f"Chalet kosher {NOM}, Tignes",
  desc=f"Chalet {NOM} en Tignes, Espace Killy: dos chalets kosher de lujo contiguos para 21 personas, nueve suites, dos jacuzzis exteriores, a un minuto de las pistas.",
  ital="Tignes, nueve suites, a un minuto de las pistas", hero="Dos chalets contiguos en Tignes, en el corazón del Espace Killy, a un minuto de las pistas.",
  intro="Dos chalets contiguos que se comunican por dentro, alquilados juntos: nueve suites, cada una con su ducha, hasta 21 personas. Las pistas están a un minuto a pie. Dos jacuzzis exteriores frente a las cumbres, dos salones con chimenea. Chef privado, Shabat y minyán, organizados para usted.",
  bref=[("map-pin", "A un minuto de las pistas.", "En Tignes, en el corazón del Espace Killy. Las pistas están a menos de un minuto a pie del chalet."),
        ("house", "Dos chalets comunicados.", "Dos chalets contiguos, unidos por dentro y alquilados juntos: cada familia tiene su chalet y todos se reúnen en la mesa. Tres plantas en cada uno."),
        ("bed-double", "Nueve suites,", "nueve baños con ducha, hasta 21 personas, cada suite con balcón o terraza. Una suite familiar con dormitorio infantil con literas, una suite principal bajo el tejado con una cama individual adicional."),
        ("waves", "Dos jacuzzis.", "Dos jacuzzis exteriores frente a las cumbres, para el final del día de esquí."),
        ("x-couch", "Dos salones, dos mesas.", "En cada chalet, un salón abierto con chimenea y sofás rinconeros, una cocina equipada y una mesa para doce.")],
  apres="Los dos chalets reciben juntos hasta 21 personas. La disponibilidad se confirma para sus fechas con cada solicitud.",
  shabbat="El chef prepara en el chalet las comidas de Shabat y de las fiestas, o las comidas llegan antes del encendido de las velas. Dos mesas para doce, una en cada chalet. Minyán privado y Séfer Torá bajo petición: indíquenos sus fechas con tiempo.",
  acces="<b>Desde Lyon-Saint-Exupéry.</b> Unas 2 h 45 por carretera. Desde Ginebra, unas 2 h 45 a 3 h.",
  faq=[("¿Cuántas personas?", "Hasta 21 personas en nueve suites, cada una con su ducha: varias familias juntas, cada una en su chalet, unidos por dentro."),
       ("¿Están lejos las pistas?", "A menos de un minuto a pie del chalet."),
       ("¿Se puede alquilar uno solo de los dos chalets?", "Los dos chalets se alquilan juntos, para un solo grupo. Cada uno tiene su cocina, su salón y su mesa para doce.")],
  alt=f"El Chalet {NOM}", vt_lien="Chalet Flocon Doré, Courchevel", suite_noms=[("kosher-val-thorens/", "kosher-val-disere/"), ("Val Thorens", "Val d'Isère")],
  noms=[("Chalet Belle Étoile", f"Chalet {NOM}"), ("Belle Étoile", NOM), ("Val Thorens", "Tignes")],
  web=f"Chalet kosher de lujo en Tignes, 21 personas, nueve suites, dos jacuzzis",
  ld_desc="Dos chalets kosher privados y contiguos en Tignes, Espace Killy, alquilados juntos: nueve suites con ducha para 21 personas, dos jacuzzis exteriores, la pista a menos de un minuto. Chef o comidas a domicilio, Shabat y minyán."),
 "he": dict(
  title=f"צ'אלה כשרה {NOM_HE}, טין: דקה מהמסלולים",
  desc=f"צ'אלה {NOM_HE} בטין, באזור הסקי של טין וואל דיזר: שתי צ'אלות כשרות יוקרתיות וצמודות לעד 21 אורחים, תשע סוויטות, שני ג'קוזי חיצוניים, דקה מהמסלולים.",
  ital="טין, תשע סוויטות, דקה מהמסלולים", hero="שתי צ'אלות צמודות בטין, בלב אזור הסקי של טין וואל דיזר, דקה מהמסלולים.",
  intro="שתי צ'אלות צמודות עם מעבר פנימי ביניהן, המושכרות יחד: תשע סוויטות, לכל אחת חדר מקלחת משלה, לעד 21 אורחים. המסלולים במרחק דקה הליכה. שני ג'קוזי חיצוניים מול הפסגות, שני סלונים עם אח. שף פרטי, שבת ומניין: הכל מאורגן.",
  bref=[("map-pin", "דקה מהמסלולים.", "בטין, באזור הסקי המשותף לטין ולואל דיזר. המסלולים במרחק פחות מדקה הליכה מהצ'אלה."),
        ("house", "שתי צ'אלות מחוברות.", "שתי צ'אלות צמודות, מחוברות מבפנים ומושכרות יחד: לכל משפחה צ'אלה משלה, וכולם נפגשים סביב השולחן. שלוש קומות בכל אחת."),
        ("bed-double", "תשע סוויטות,", "תשעה חדרי מקלחת, עד 21 אורחים, ולכל סוויטה מרפסת או יציאה למרפסת הגדולה. סוויטה משפחתית עם חדר ילדים ובו מיטות קומותיים, וסוויטת הורים בעליית הגג עם מיטת יחיד נוספת."),
        ("waves", "שני ג'קוזי.", "שני ג'קוזי חיצוניים מול הפסגות, לסוף יום הסקי."),
        ("x-couch", "שני סלונים, שני שולחנות.", "בכל צ'אלה סלון פתוח עם אח וספות פינתיות, מטבח מאובזר ושולחן ל-12 סועדים.")],
  apres="שתי הצ'אלות מארחות יחד עד 21 אורחים. הזמינות מאושרת לתאריכים שלכם בכל פנייה.",
  shabbat="השף מכין בצ'אלה את סעודות השבת והחגים, או שהארוחות מגיעות לפני הדלקת הנרות. שני שולחנות ל-12 סועדים, אחד בכל צ'אלה. מניין פרטי וספר תורה לפי בקשה: ספרו לנו את התאריכים מוקדם.",
  acces="<b>מנמל התעופה ליון-סנט-אקזופרי.</b> כשלוש שעות פחות רבע בנסיעה. מז'נבה, כשלוש שעות.",
  faq=[("כמה אורחים?", "עד 21 אורחים בתשע סוויטות, לכל אחת חדר מקלחת משלה: כמה משפחות יחד, כל אחת בצ'אלה שלה, עם מעבר פנימי ביניהן."),
       ("המסלולים רחוקים?", "פחות מדקה הליכה מהצ'אלה."),
       ("אפשר לשכור רק אחת משתי הצ'אלות?", "שתי הצ'אלות מושכרות יחד, לקבוצה אחת. לכל אחת מטבח, סלון ושולחן ל-12 סועדים משלה.")],
  alt="הצ'אלה בטין", vt_lien="צ'אלה פלוקון דורה, קורשבל", suite_noms=[("kosher-val-thorens/", "kosher-val-disere/"), ("בואל טורנס", "בואל דיזר"), ("ואל טורנס", "ואל דיזר")],
  noms=[("בל אטואל", NOM_HE), ("בואל טורנס", "בטין"), ("ואל טורנס", "טין"), ('value="Val Thorens"', 'value="Tignes"'), ("מג'נבה", "מז'נבה")],   # champ caché du formulaire, en latin
  web="צ'אלה כשרה יוקרתית בטין, עד 21 אורחים, תשע סוויטות, שני ג'קוזי",
  ld_desc="שתי צ'אלות כשרות פרטיות וצמודות בטין, באזור הסקי של טין וואל דיזר, המושכרות יחד: תשע סוויטות עם חדר מקלחת לעד 21 אורחים, שני ג'קוזי חיצוניים, והמסלול במרחק פחות מדקה. שף או ארוחות במשלוח, שבת ומניין."),
}


def tx():
    out = {}
    for l in LANGS:
        t = dict(T[l])
        t.update(bref=t["bref"] + [CUISINE[l]], shabbat=t["shabbat"], prix=(PRIX[l][0] % CH, PRIX[l][1]),
                 voisin="kosher-chalet-courchevel", lieu_q="Tignes", svc="Tignes")
        out[l] = t
    return out


def regler():
    A.SLUG, A.GC = SLUG, G.CHALETS[SLUG]
    A.HERO = A.GC["hero"]
    A.STEMS = A.ORDRE = [s for _, _, ss in A.GC["pieces"] for s in ss]
    A.TX = tx()
    A.COORD_AR = COORD
    A.DIM = {s: A.webp(s) for s in A.STEMS}


def carte(lang):
    return K.carte(lang, CLE).replace('<p class="kwp-dispo">', f'<p class="kwp-prix" data-prix-tpl="{A.attr_(PRIX[lang][0] % CH)}">{PRIX[lang][1]}</p><p class="kwp-dispo">', 1)


def apres_derniere_carte(bloc, lang):
    """La carte se pose après celle du Renard Argenté (dernier chalet), sinon en fin de rangée."""
    lien = f'href="{pfx(lang)}/kosher-chalet-courchevel-renard-argente/"'
    i = bloc.find(lien)
    while i >= 0 and bloc.rfind('<article class="kwp-carte', 0, i) < bloc.rfind("</article>", 0, i):
        i = bloc.find(lien, i + 1)
    if i < 0:
        j = bloc.rfind("</article>") + len("</article>")
    else:
        j = bloc.find("</article>", i) + len("</article>")
    return bloc[:j] + carte(lang) + bloc[j:]


def brancher():
    n = 0
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = (r[len(lang) + 1:] if lang != "en" else r)[: -len("index.html")].strip("/")
        s = A.lire(p); o = s
        s = A.retirer(s, lang, SLUG)
        # menu « Chalets » : après le Renard Argenté
        if f'class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"' not in s:
            k = [u for u, _ in K.CH_URL].index(SLUG)
            b, d = K.NAV_CH[lang][2][k]
            nav = (f'<a class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"><img src="{K.CH_URL[k][1]}" alt="" width="96" height="64" loading="lazy">'
                   f'<span><b>{H.escape(b, quote=False)}</b>{H.escape(d, quote=False)}</span></a>')
            s = re.sub(rf'(<a class="nav-ch-v" href="{pfx(lang)}/kosher-chalet-courchevel-renard-argente/">.*?</a>)', lambda m: m.group(1) + nav, s, count=1, flags=re.S)
        # liste des pages hiver (fondu entre chartes)
        if f'"{SLUG}"' not in s:
            s = s.replace('"kosher-chalet-courchevel-renard-argente"];', f'"kosher-chalet-courchevel-renard-argente","{SLUG}"];')
        # cartes : accueil, hub, /alps/ et ski (« duo »)
        for nom in ("accueil", "hub", "duo"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{pfx(lang)}/{SLUG}/"' not in m.group(0):
                s = s[:m.start()] + apres_derniere_carte(m.group(0), lang) + s[m.end():]
        # bandes « un chalet entier ? »
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug != SLUG:   # toujours reposée : la vignette Tignes suit le texte de _zones.py
            sauf = slug if slug in [u for u, _ in K.CH_URL] else None
            s = s[:m.start()] + K.bloc("mini", K.mini(lang, sauf)) + s[m.end():]
        n += A.ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = A.lire(p); o = s
    if f"/{SLUG}/" not in s:
        for lang in ("", "fr/", "es/", "he/"):
            m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}kosher-chalet-courchevel-renard-argente/</loc>.*?</url>", s, flags=re.S)
            if m:
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>2026-11-02</lastmod>", m.group(0).replace("kosher-chalet-courchevel-renard-argente", SLUG))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
    n = A.ecrire(p, s, o)
    p = ICI / "llms.txt"; s = A.lire(p); o = s
    lignes = [l for l in s.split("\n") if f"/{SLUG}/" not in l]
    i = next(k for k, l in enumerate(lignes) if "/kosher-chalet-courchevel-renard-argente/" in l)
    lignes.insert(i + 1, f"- [Kosher Chalet {NOM}, Tignes]({A.BASE}/{SLUG}/): two adjoining private kosher chalets in Tignes (Espace Killy) rented together, up to 21 guests, nine suites with shower rooms, two outdoor jacuzzis, one minute from the slopes; price on request.")
    return n + A.ecrire(p, "\n".join(lignes), o)


def sans_minyan_station(dst):
    """Retire le bloc « A minyan in the resort » (Beth Habad des Alpes en station) : rien de publié à Tignes, on ne promet
    que le minyan privé au chalet (bloc Shabbat et FAQ)."""
    s = A.lire(dst); o = s
    s = re.sub(r'<section class="clair ss wrap minyan-bh">.*?</section>', "", s, count=1, flags=re.S)
    A.ecrire(dst, s, o)


def controle():
    """Aucun nom interdit dans les pages du chalet et leur index.md."""
    for lang in LANGS:
        for f in ("index.html", "index.md"):
            p = ICI / (SLUG if lang == "en" else f"{lang}/{SLUG}") / f
            m = INTERDITS.search(A.lire(p))
            assert not m, (p, m and m.group(0))


if __name__ == "__main__":
    regler()
    for lang in LANGS:
        dst = A.page(lang)
        sans_minyan_station(dst)
        A.index_md(dst)
        print("page", dst.relative_to(ICI))
    controle()
    if not PAGE_SEUL:
        print("pages branchées :", brancher())
        print("sitemap + llms :", sitemap_llms())
