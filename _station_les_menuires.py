# -*- coding: utf-8 -*-
"""Page station « chalet casher aux Ménuires » /kosher-les-menuires/ en 4 langues, 02/11/2026.

Clonage de la page station Val Thorens publiée dans chaque langue (toutes les passes déjà posées : charte Valora, en-tête,
Shabbat, formulaire, vidéo), puis remplacement du contenu propre à la station. Jamais d'édition HTML à la main.
Idempotent : relancer réécrit les 4 pages et leurs index.md à l'identique (date figée), sitemap et llms.txt vérifient leur marque.

Faits sourcés (relevés le 02/11/2026) :
- saison du domaine 5 décembre 2026 au 18 avril 2027, village à 1 850 m : https://www.lesmenuires.com/
- office de tourisme, 1269 avenue de la Croisette, 73440 Les Belleville, « au cœur des 3 Vallées » : https://lesmenuires.com/en/tourist-office
- Moûtiers à 27 km, cars réguliers Altibus vers gares et aéroports : https://lesmenuires.com/en/access-transportation
- coordonnées : OpenStreetMap (village 45.3243, 6.5389 ; office 45.3230, 6.5377) ; Hebcal accepte 45.3236 / 6.5394
- pas de minyan permanent publié : _build_hub.py (« Val Thorens, Les Menuires, Les Arcs »)
Pas de durée de route depuis Lyon (aucune source primaire) ; pas de Ben's Bus (non vérifié pour Les Ménuires).
Ne touche que kosher-les-menuires/ (4 langues, html + md), sitemap.xml et llms.txt. Lancer depuis site-v5 : python _station_les_menuires.py"""
import io
import json
import os
import re
import urllib.parse as U
from markdownify import markdownify as md

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SLUG, MODELE = "kosher-les-menuires", "kosher-val-thorens"
BASE = "https://mishpachatours.com"
DATE = "2026-11-02"
LAT, LON = 45.3236, 6.5394
LANGS = {"en": "", "fr": "fr/", "es": "es/", "he": "he/"}


def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)


def sub1(motif, rempl, s, flags=re.S):
    """Remplacement regex qui doit trouver exactement une occurrence."""
    r, n = re.subn(motif, rempl, s, flags=flags)
    assert n == 1, (motif[:80], n)
    return r


T = {
 "en": dict(
  title="Kosher Chalet in Les Ménuires: Chef, Shabbat, Minyan | Mishpacha Tours",
  desc="Kosher chalet in Les Ménuires, at the heart of Les 3 Vallées: private chef, delivered meals, Shabbat, holidays and a minyan. One written quote.",
  h1=("Kosher chalet in Les Ménuires", "the heart of Les 3 Vallées"),
  hero="Les Ménuires sits at 1,850 m in the Belleville valley, at the heart of Les 3 Vallées.",
  saison=("21 November 2026 to 2 May 2027", "5 December 2026 to 18 April 2027"),
  kwp=("Our chalet", "in Les Ménuires"),
  casher=[("house", "No permanent minyan.", "No permanent minyan is published in Les Ménuires: prayers depend on the families in the resort that week."),
          ("snowflake", "Les 3 Vallées.", "From Les Ménuires you ski across Les 3 Vallées, as far as Val Thorens, Méribel and Courchevel."),
          ("scroll-text", "Organised for you.", "A private chef, delivered meals, Shabbat, and a minyan with a Sefer Torah depending on the number of families, arranged for your week.")],
  route="By road to Moûtiers, then 27 km up the Belleville valley to the resort. Allow extra time on a Saturday in February or in snow.",
  navette="Altibus runs regular buses from the airports and from Moûtiers station; details on {a}. Transfers can be part of a tailor-made stay, on quote.",
  note="The Les Ménuires tourist office, at La Croisette, in the centre of the resort.",
  noms=[("Val Thorens", "Les Ménuires")],
  vt=("Kosher Courchevel", "Kosher Val Thorens"),
  llms="Kosher Chalet in Les Ménuires: Chef, Shabbat, Minyan"),
 "fr": dict(
  title="Chalet casher aux Ménuires : chef, repas, Shabbat, minyan | Mishpacha Tours",
  desc="Chalet casher aux Ménuires, au cœur des 3 Vallées : chef privé, repas livrés, Shabbat, fêtes et minyan avec Sefer Torah. Un seul devis écrit.",
  h1=("Chalet casher aux Ménuires", "au cœur des 3 Vallées"),
  hero="Les Ménuires se trouvent à 1 850 m, dans la vallée des Belleville, au cœur des 3 Vallées.",
  saison=("du 21 novembre 2026 au 2 mai 2027", "du 5 décembre 2026 au 18 avril 2027"),
  kwp=("Notre chalet", "aux Ménuires"),
  casher=[("house", "Pas de minyan permanent.", "Aucun minyan permanent n’est publié aux Ménuires : les prières dépendent des familles présentes en station cette semaine-là."),
          ("snowflake", "Les 3 Vallées.", "Depuis Les Ménuires, vous skiez sur tout le domaine des 3 Vallées, jusqu’à Val Thorens, Méribel et Courchevel."),
          ("scroll-text", "Organisé pour vous.", "Chef privé, repas livrés, Shabbat, et un minyan avec Sefer Torah selon le nombre de familles, organisés pour votre semaine.")],
  route="Par la route jusqu’à Moûtiers, puis 27 km de montée dans la vallée des Belleville jusqu’à la station. Prévoyez plus de temps un samedi de février ou sous la neige.",
  navette="Des cars réguliers Altibus relient la station aux aéroports et à la gare de Moûtiers ; le détail est sur {a}. Les transferts peuvent s’ajouter à un séjour sur mesure, sur devis.",
  note="L’office de tourisme des Ménuires, à La Croisette, au centre de la station.",
  noms=[("Se rendre à <i>Val Thorens</i>", "Se rendre <i>aux Ménuires</i>"), ("à Val Thorens", "aux Ménuires"),
        ("de Val Thorens", "des Ménuires"), ("Val Thorens", "Les Ménuires")],
  vt=("Courchevel casher", "Val Thorens casher")),
 "es": dict(
  title="Chalet kosher en Les Ménuires: chef, Shabat, minián | Mishpacha Tours",
  desc="Chalet kosher en Les Ménuires, en el corazón de Les 3 Vallées: chef privado, comidas entregadas, Shabat, fiestas y minián. Un presupuesto por escrito.",
  h1=("Chalet kosher en Les Ménuires", "en el corazón de Les 3 Vallées"),
  hero="Les Ménuires se encuentra a 1.850 m en el valle de Les Belleville, en el corazón de Les 3 Vallées.",
  saison=("del 21 de noviembre de 2026 al 2 de mayo de 2027", "del 5 de diciembre de 2026 al 18 de abril de 2027"),
  kwp=("Nuestro chalet", "en Les Ménuires"),
  casher=[("house", "Sin minián permanente.", "No hay ningún minián permanente publicado en Les Ménuires: los rezos dependen de las familias presentes en la estación esa semana."),
          ("snowflake", "Les 3 Vallées.", "Desde Les Ménuires se esquía por todo Les 3 Vallées, hasta Val Thorens, Méribel y Courchevel."),
          ("scroll-text", "Organizado para ustedes.", "Chef privado, comidas entregadas, Shabat y un minián con Sefer Torá según el número de familias, organizados para su semana.")],
  route="Por carretera hasta Moûtiers y luego 27 km de subida por el valle de Les Belleville hasta la estación. Cuente más tiempo un sábado de febrero o con nieve.",
  navette="Los autobuses regulares de Altibus enlazan la estación con los aeropuertos y con la estación de tren de Moûtiers; los detalles están en {a}. Los traslados pueden formar parte de una estancia a medida, con presupuesto.",
  note="La oficina de turismo de Les Ménuires, en La Croisette, en el centro de la estación.",
  noms=[("Val Thorens", "Les Ménuires")],
  vt=("Courchevel kosher", "Val Thorens kosher")),
 "he": dict(
  title="צ'אלה כשרה בלה מנואר: שף פרטי, שבת ומניין | Mishpacha Tours",
  desc="צ'אלה כשרה בלה מנואר, בלב שלושת העמקים: שף פרטי, ארוחות במשלוח, שבת, חגים, מניין וספר תורה. הצעת מחיר אחת בכתב.",
  h1=("צ'אלה כשרה בלה מנואר", "בלב שלושת העמקים"),
  hero="לה מנואר שוכנת בגובה 1,850 מ', בלב שלושת העמקים.",
  saison=("מ-21 בנובמבר 2026 עד 2 במאי 2027", "מ-5 בדצמבר 2026 עד 18 באפריל 2027"),
  kwp=("הצ'אלה שלנו", "בלה מנואר"),
  casher=[("house", "אין מניין קבוע.", "בלה מנואר לא מתפרסם מניין קבוע: התפילות תלויות במשפחות שנמצאות באתר באותו שבוע."),
          ("snowflake", "שלושת העמקים.", "מלה מנואר גולשים לכל רחבי שלושת העמקים, עד ואל טורנס וקורשבל."),
          ("scroll-text", "הכל מאורגן.", "שף פרטי, ארוחות במשלוח, שבת, ומניין עם ספר תורה לפי מספר המשפחות, מסודרים לשבוע שלכם.")],
  route="בכביש עד מוטייה (Moûtiers), ומשם 27 ק\"מ של עלייה בעמק עד האתר. הוסיפו זמן בשבת של פברואר או בשלג.",
  navette="Altibus מפעילה אוטובוסים סדירים משדות התעופה ומתחנת הרכבת של מוטייה; הפרטים בעמוד {a}. הסעות יכולות להיכלל בשהייה בהתאמה אישית, בהצעת מחיר.",
  note="לשכת התיירות של לה מנואר, ברובע La Croisette במרכז האתר.",
  noms=[("בוואל טורנס", "בלה מנואר"), ("בואל טורנס", "בלה מנואר"), ("לוואל טורנס", "ללה מנואר"), ("לואל טורנס", "ללה מנואר"),
        ("ואל טורנס", "לה מנואר"), ("Val Thorens", "Les Ménuires")],
  vt=("כשר בקורשבל", "כשר בוואל טורנס")),
}
SUFFIXE = " | Mishpacha Tours"


def carte_aigle(pre):
    """Carte kwp de l'Aigle Royal telle qu'elle existe dans /kosher-chalets/ de la même langue (avec son data-prix-tpl)."""
    s = rd(f"{pre}kosher-chalets/index.html")
    a = [x for x in re.findall(r'<article class="kwp-carte".*?</article>', s, re.S) if "kosher-chalet-les-menuires/" in x]
    assert len(a) == 1 and "data-prix-tpl" in a[0], pre
    return a[0]


def page(lang, pre):
    t = T[lang]
    s = rd(f"{pre}{MODELE}/index.html")
    # 0. segments site-wide laissés tels quels : menu des chalets, pied (liste des stations), liste H de la vue de transition
    gardes = []
    def garder(m):
        gardes.append(m.group(0)); return f"\x00{len(gardes) - 1}\x00"
    s = s.replace('"kosher-val-thorens","kosher-alpe-dhuez"', '"kosher-val-thorens","kosher-les-menuires","kosher-alpe-dhuez"', 1) \
        if '"kosher-les-menuires"' not in s else s
    assert '"kosher-les-menuires"' in s
    for motif in (r'<!--KIT-WP:vt-->.*?<!--/KIT-WP:vt-->', r'<div class="nav-ch-menu">.*?<a class="nav-ch-tous"[^>]*>[^<]*</a></div>',
                  r'<footer class="pied">.*?</footer>'):
        s, n = re.subn(motif, garder, s, flags=re.S); assert n == 1, motif

    # 1. adresse de la page (canonical, hreflang, JSON-LD, sélecteurs de langue)
    s = s.replace(f"{MODELE}/", f"{SLUG}/")
    # 2. le nom de la station, en clair et dans les messages WhatsApp encodés (lieu= reste en lettres latines)
    for old, new in t["noms"]:
        s = s.replace(U.quote(old, safe=""), U.quote(new, safe="")).replace(old, new)

    # 3. en-tête : title, description, og, JSON-LD
    titre = t["title"]; court = titre.replace(SUFFIXE, "")
    s = sub1(r"<title>.*?</title>", f"<title>{titre}</title>", s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', s)
    og = re.search(r'<meta property="og:title" content="([^"]*)">', s).group(1)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titre if SUFFIXE in og else court}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{t["desc"]}">', s)
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    ld = json.loads(m.group(2))
    for o in ld:
        if o["@type"] == "WebPage":
            o.update(name=court, description=t["desc"], dateModified=DATE)
        if o["@type"] == "Service":
            o["areaServed"] = {"@type": "Place", "name": "Les Ménuires",
                               "address": {"@type": "PostalAddress", "addressLocality": "Les Belleville", "postalCode": "73440",
                                           "addressRegion": "Savoie", "addressCountry": "FR"},
                               "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON}}
    s = s[:m.start(2)] + json.dumps(ld, ensure_ascii=False) + s[m.end(2):]

    # 4. héros : photo (pas de photo de la station : le chalet Aigle Royal sous la neige), H1, phrase d'altitude
    s = sub1(r'<img src="/img/h/st-val-thorens-960\.webp"[^>]*fetchpriority="high">',
             '<img src="/img/h/aigle-exterieur-neige-960.webp" srcset="/img/h/aigle-exterieur-neige-640.webp 640w, '
             '/img/h/aigle-exterieur-neige-960.webp 960w, /img/h/aigle-exterieur-neige-1067.webp 1067w" sizes="100vw" alt="" '
             'width="1067" height="800" fetchpriority="high">', s)
    s = sub1(r"<h1>.*?</h1>(\s*)<p>.*?</p>", f"<h1>{t['h1'][0]}<br><i>{t['h1'][1]}</i></h1>\\1<p>{t['hero']}</p>", s)
    # 5. saison (lesmenuires.com)
    assert s.count(t["saison"][0]) == 1, lang
    s = s.replace(t["saison"][0], t["saison"][1])
    # 6. carte chalet : l'Aigle Royal seul (sans la marque KIT-WP:vth, que _kit_wp.py remplirait avec Belle Étoile)
    s = sub1(r"<!--KIT-WP:vth-->.*?<!--/KIT-WP:vth-->",
             lambda _: f'<section class="ss wrap kwp"><h2>{t["kwp"][0]} <i>{t["kwp"][1]}</i></h2>'
                       f'<div class="kwp-cartes">{carte_aigle(pre)}</div></section>', s)
    # 7. « Casher aux Ménuires » : faits de Val Thorens (hôtel d'été, Orelle, PlanetSKI) remplacés
    lis = "".join(f'\n<li><img class="dk dk-ico dk-des" src="/img/ico/or/{ico}.svg" alt="" width="96" height="96" loading="lazy"><b>{b}</b> {p}</li>'
                  for ico, b, p in t["casher"]) + "\n"
    s = sub1(r'(<div class="clair clair-2 ss beige"><div class="wrap"><h2 class="dk-h2">.*?</h2><ul class="dk-cartes">).*?(</ul>)',
             lambda m: m.group(1) + lis + m.group(2), s)
    # 8. Shabbat : coordonnées des Ménuires
    s = sub1(r"latitude=45\.2978&longitude=6\.5838", f"latitude={LAT}&longitude={LON}", s)
    # 9. accès : route par Moûtiers, cars Altibus (le lien vers la page Lyon, porte des Alpes, est conservé)
    def acces(m):
        b1 = re.search(r"<b>.*?</b>", m.group(2)).group(0)
        b2 = re.search(r"<b>.*?</b>", m.group(3)).group(0)
        a = re.search(r'<a href="[^"]*lyon-gateway-to-the-alps-kosher/">.*?</a>', m.group(3)).group(0)
        i1 = re.match(r"<li>(<img[^>]*>)", m.group(2)).group(1)
        i2 = re.match(r'<li class="dk-lien1">(<img[^>]*>)', m.group(3)).group(1)
        return (m.group(1) + f"<li>{i1}{b1} {t['route']}</li>\n"
                + f'<li class="dk-lien1">{i2}{b2} {t["navette"].format(a=a)}</li>\n')
    s = sub1(r'(<div class="clair ss beige"><div class="wrap"><h2>[^\n]*?</h2><ul class="dk-cartes">\n)(<li>.*?</li>\n)(<li class="dk-lien1">.*?</li>\n)', acces, s)
    # 10. carte : office de tourisme des Ménuires
    pts = [{"n": "Office de tourisme des Ménuires", "a": "1269 avenue de la Croisette, 73440 Les Belleville", "ll": [45.323, 6.537686]}]
    s = sub1(r'data-points="[^"]*"', 'data-points="' + json.dumps(pts, ensure_ascii=False).replace('"', "&quot;") + '"', s)
    s = sub1(r'<p class="carte-note">[^<]*</p>', f'<p class="carte-note">{t["note"]}</p>', s)
    # 11. stations voisines : Val Thorens, Courchevel, toutes les stations (pas de page Méribel sur le site)
    def voisines(m):
        lis = re.findall(r"<li>.*?</li>", m.group(2), re.S)
        cou = [x for x in lis if "kosher-courchevel/" in x]; tout = [x for x in lis if "/alps/" in x]
        assert len(cou) == 1 and len(tout) == 1 and t["vt"][0] in cou[0], lang
        vt = cou[0].replace("kosher-courchevel/", "kosher-val-thorens/").replace(t["vt"][0], t["vt"][1])
        for x in (vt, cou[0]):
            assert os.path.exists(f"{pre}{re.search(r'kosher-[a-z-]+/', x).group(0)}index.html")
        return m.group(1) + vt + cou[0] + tout[0] + m.group(3)
    s = sub1(r'(<section class="clair ss wrap conseils" id="voisines">.*?<ul class="dk-suite">)(.*?)(</ul></section>)', voisines, s)

    for i, g in enumerate(gardes):
        s = s.replace(f"\x00{i}\x00", g)
    os.makedirs(f"{pre}{SLUG}", exist_ok=True)
    wr(f"{pre}{SLUG}/index.html", s)
    ecrire_md(f"{pre}{SLUG}/index.html")
    print("page", f"{pre}{SLUG}/index.html")


def ecrire_md(p):
    """index.md : même code que _agentic.py, section 3 (boucle « index.md par page »), pour cette seule page
    (_agentic.py en entier réécrirait tous les index.md, 404.html et vercel.json)."""
    def meta(h, name):
        r = re.search(rf'<meta name="{name}" content="([^"]*)"', h); return r.group(1) if r else ""
    d = os.path.dirname(p).replace("\\", "/")
    h = open(p, encoding="utf-8").read()
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {meta(h, 'description')}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    open(os.path.join(os.path.dirname(p), "index.md"), "w", encoding="utf-8").write(out)


def sitemap_llms():
    # sitemap : 4 lignes à leur place alphabétique, comme _stations_verbier.py §16 (_build_sitemap.py redaterait les 270 URL)
    s = rd("sitemap.xml"); lignes = s.split("\n")
    for pre in LANGS.values():
        loc = f"{BASE}/{pre}{SLUG}/"
        if f"<loc>{loc}</loc>" in s: continue
        urls = [i for i, x in enumerate(lignes) if "<loc>" in x]
        i = next((i for i in urls if re.search(r"<loc>([^<]*)</loc>", lignes[i]).group(1) > loc), urls[-1] + 1)
        lignes.insert(i, f"  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><priority>0.7</priority></url>"); s = "\n".join(lignes)
        print("sitemap", loc)
    wr("sitemap.xml", s)
    # llms.txt : une ligne après la station Val Thorens
    s = rd("llms.txt")
    if f"({BASE}/{SLUG}/)" not in s:
        lignes = s.split("\n")
        i = next(i for i, x in enumerate(lignes) if f"({BASE}/{MODELE}/)" in x)
        lignes.insert(i + 1, f"- [{T['en']['llms']}]({BASE}/{SLUG}/): {T['en']['desc']}")
        wr("llms.txt", "\n".join(lignes)); print("llms.txt")


for lang, pre in LANGS.items():
    page(lang, pre)
sitemap_llms()
print("done")
