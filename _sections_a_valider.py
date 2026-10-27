"""Page de validation des sections (Moshé 27/10) : chaque type de section du site, une seule fois,
dans la version B alternée blanc luxe + icônes au trait fin doré.

python _sections_a_valider.py
-> fr/sections-a-valider/index.html (Alpes et commun) + fr/sections-a-valider/lyon/index.html (Lyon)
   + sections-a-valider.css. Noindex, hors sitemap, aucun lien depuis le site.
Le HTML des sections est copié des vraies pages ; rien n'est modifié ailleurs.
"""
import re, glob, os, html as H
from pathlib import Path
from _theme_bc import Enfants, offset

ICI = Path(__file__).parent
os.chdir(ICI)

def sections(page):
    h = open(page, encoding="utf-8").read()
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    p = Enfants(); p.feed(h)
    out = []
    for pos, tag, cls in p.res:
        o = offset(h, pos)
        depth = 0
        for m in re.finditer(r"<(/?)%s\b[^>]*>" % tag, h[o:]):
            depth += 1 if m.group(1) == "" else -1
            if depth == 0:
                out.append((cls, h[o:o + m.end()]))
                break
    return h, out

def trouve(page, test):
    _, secs = sections(page)
    for cls, s in secs:
        if test(cls, s):
            return s
    raise SystemExit(f"section introuvable dans {page}")

def nb_pages(test, zone):
    n, ex = 0, []
    for f in sorted(glob.glob("fr/**/index.html", recursive=True)):
        if "preview" in f or "sections-a-valider" in f:
            continue
        h = open(f, encoding="utf-8").read()
        b = re.search(r'<body class="([^"]*)"', h)
        lyon = bool(b and re.search(r"valora-(clair|visite)", b.group(1)))
        if (zone == "lyon") != lyon:
            continue
        _, secs = sections(f)
        if any(test(c, s) for c, s in secs):
            n += 1
            ex.append(f.replace("\\", "/").split("/")[1] if f.count("\\") + f.count("/") > 1 else "accueil")
    return n, ex

def c(*noms):
    return lambda cls, s: all(x in cls.split() for x in noms)

def c_has(nom, *dedans):
    return lambda cls, s: nom in cls.split() and all(d in s for d in dedans)

def sans(test, *exclus):
    return lambda cls, s: test(cls, s) and not any(e in cls.split() or e in s[:400] for e in exclus)

# (nom, noir|blanc, page exemple, test)
ALPES = [
    ("Bannière des pages Alpes (photo + titre centré)", "noir", "fr/kosher-val-thorens/index.html", c("lead-hero3")),
    ("Intro « Skiez le jour… » et 3 promesses", "blanc", "fr/kosher-val-thorens/index.html", c("lead-intro")),
    ("Offre « Où vous dormez, ce que vous mangez »", "blanc", "fr/kosher-chalet-les-deux-alpes/index.html", c("lead-offre")),
    ("Liste dépliable « Le chalet, en bref »", "blanc", "fr/kosher-chalet-les-deux-alpes/index.html", sans(c_has("conseils", "dk-cartes"), "dk-recit", "dk-note")),
    ("« Le chalet en images » (mosaïque + plein écran)", "noir", "fr/kosher-chalet-les-deux-alpes/index.html", c("chalet-images")),
    ("Récit « Shabbat et les fêtes au chalet »", "blanc", "fr/kosher-chalet-les-deux-alpes/index.html", c("dk-recit")),
    ("Horaires de Chabbat de la semaine", "blanc", "fr/kosher-chalet-les-deux-alpes/index.html", c("shabbat-bloc")),
    ("Étapes « Comment ça se passe » + boutons", "noir", "fr/kosher-chalet-les-deux-alpes/index.html", c("etapes")),
    ("Carte des lieux", "blanc", "fr/kosher-alpe-dhuez/index.html", lambda cls, s: "carte-osm" in s and set(cls.split()) <= {"ss", "wrap"}),
    ("Minyan et repas en station (Beth Habad)", "blanc", "fr/kosher-val-thorens/index.html", sans(c("minyan-bh"), "repas-prix")),
    ("Prix des repas livrés (cartes photo + tableau)", "blanc", "fr/kosher-services-french-alps/index.html", c("repas-prix")),
    ("Questions fréquentes (FAQ)", "blanc", "fr/kosher-chalet-les-deux-alpes/index.html", c("faq")),
    ("Cartes chalets en rangée (« Un chalet rien que pour vous ? »)", "noir", "fr/kosher-alpe-dhuez/index.html", c("kwp-mini")),
    ("Bloc final « Votre semaine casher, organisée »", "noir", "fr/kosher-val-thorens/index.html", c("lead-final")),
    ("« Pour aller plus loin » (liens vers d'autres pages)", "blanc", "fr/kosher-val-thorens/index.html", c_has("conseils", "dk-suite")),
    ("« Ce que comprend » / garanties", "blanc", "fr/kosher-vacation-french-alps/index.html", c_has("beige", "dk-garanties")),
    ("Note encadrée", "blanc", "fr/kosher-van-transfers/index.html", c("dk-note")),
    ("Page « Nos chalets » : les 5 cartes", "noir", "fr/kosher-chalets/index.html", c("kwp-hub")),
    ("Bannière des pages pratiques (à propos, contact)", "noir", "fr/about/index.html", c("pratique-hero")),
    ("Bannière illustrée (page van)", "noir", "fr/kosher-van-transfers/index.html", c("lead-hero3-illus")),
    ("Galerie de la villa de Saint-Tropez", "noir", "fr/kosher-villa-saint-tropez/index.html", c("galerie-wp")),
]
LYON = [
    ("Bannière des guides Lyon (avec pastilles)", "blanc", "fr/chabad-lyon/index.html", c("pratique-hero")),
    ("Les 5 offres Lyon (cartes)", "blanc", "fr/chabad-lyon/index.html", c("of-lyon")),
    ("Liste de lieux (adresses)", "blanc", "fr/chrd-lyon/index.html", c_has("beige", "liste-lieux")),
    ("Récit d'histoire", "blanc", "fr/chrd-lyon/index.html", c("dk-recit")),
    ("Étapes Lyon", "noir", "fr/chrd-lyon/index.html", c("etapes")),
    ("Carte de Lyon", "blanc", "fr/chabad-lyon/index.html", lambda cls, s: "carte-osm" in s and set(cls.split()) <= {"ss", "wrap"}),
    ("FAQ Lyon", "blanc", "fr/chrd-lyon/index.html", c("faq")),
    ("« Pour aller plus loin » Lyon", "blanc", "fr/chrd-lyon/index.html", c_has("conseils", "dk-suite")),
    ("Encart d'appel « Un voyage à Lyon en préparation »", "noir", "fr/chabad-lyon/index.html", c("cta-pratique")),
    ("Bloc final Lyon (ticket)", "noir", "fr/chabad-lyon/index.html", c("ticket-zone")),
    ("Visites : bannière avec réservation", "noir", "fr/jewish-lyon-tours/index.html", c("hero")),
    ("Visites : preuves (« La seule visite à l'intérieur… »)", "blanc", "fr/jewish-lyon-tours/index.html", c("preuves")),
    ("Visites : tuiles des 4 visites", "blanc", "fr/jewish-lyon-tours/index.html", c("tuiles")),
    ("Visites : bande « Nous marchons dans »", "noir", "fr/jewish-lyon-tours/index.html", c("bande")),
    ("Visites : citation de la guide", "blanc", "fr/jewish-lyon-tours/index.html", c("citation")),
    ("Visites : galerie « Les lieux où vous marcherez »", "blanc", "fr/jewish-lyon-tours/index.html", lambda cls, s: "lieux-galerie" in s),
    ("Visites : tableau des prix", "blanc", "fr/jewish-lyon-tours/index.html", c("prix-table")),
    ("Fiche visite : bannière", "noir", "fr/tours/izieu/index.html", c("fiche-hero")),
    ("Fiche visite : déroulé", "blanc", "fr/tours/izieu/index.html", c("deroule")),
    ("Fiche visite : Compris / Non compris", "blanc", "fr/tours/izieu/index.html", c_has("beige", "deux-cartes")),
    ("Fiche visite : garanties", "blanc", "fr/tours/izieu/index.html", c("garanties-fiche")),
    ("Guide Lyon : cartes de rubriques", "blanc", "fr/jewish-lyon-guide/index.html", lambda cls, s: "hub-grille" in s and set(cls.split()) <= {"ss", "wrap"}),
    ("Météo à Lyon (en direct)", "blanc", "fr/lyon-weather/index.html", c("meteo-live")),
]
DEJA = [
    ("Bannière d'accueil + barre de réservation", "noir", "fr/index.html", c("ac-hero")),
    ("Barre de réservation", "noir", "fr/index.html", c("cherche-bar")),
    ("4 visuels", "noir", "fr/index.html", c("reve")),
    ("Cartes chalets de l'accueil", "noir", "fr/index.html", c("kwp-accueil")),
    ("« Comment voulez-vous voyager » + stations + van", "blanc", "fr/index.html", c_has("beige", "hub-grille")),
    ("Étapes de l'accueil", "noir", "fr/index.html", c("etapes")),
    ("Bloc Lyon de l'accueil (mise en page A/B en attente)", "blanc", "fr/index.html", c("ac-lyon")),
    ("Bloc final « Parlez-nous de votre séjour »", "noir", "fr/index.html", c("ticket-zone")),
]

# Icônes au trait fin doré : fichier d'origine -> icône ; et selon le texte de la ligne quand c'est évident.
PAR_TEXTE = [(r"Surface", "x-ruler"), (r"Chambres", "x-bed"), (r"Salon", "x-couch"),
             (r"Salles? de bain", "x-bathtub"), (r"Extérieur", "x-tree"), (r"Emplacement|Les vues", "x-mountains"),
             (r"Cuisine", "chef-hat"), (r"Salle à manger", "x-fork")]

def icones(s):
    def rep(m):
        nom = m.group(2)
        suite = re.sub(r"<[^>]+>", " ", s[m.end():m.end() + 300]).strip()
        for motif, ico in PAR_TEXTE:
            if re.match(motif, suite):
                nom = ico
                break
        return f'{m.group(1)}/img/ico/or/{nom}.svg"'
    return re.sub(r'(src=")/img/des/([\w-]+)\.webp"', rep, s)

def marque_clair(s):
    o = s.index(">")
    t = s[:o]
    t = t.replace('class="', 'class="clair ', 1) if 'class="' in t else t + ' class="clair"'
    return t + s[o:]

MANQUE = []

def bloc(i, nom, ton, page, test, zone, clair):
    try:
        s = trouve(page, test)
    except SystemExit:
        MANQUE.append(nom)
        return ""
    n, ex = nb_pages(test, zone)
    s = icones(s)
    if clair and ton == "blanc":
        s = marque_clair(s)
    ex_txt = ", ".join(dict.fromkeys(ex))[:120]
    lab = (f'<div class="sav-label"><span class="sav-n">{i}</span> {H.escape(nom)} <span class="sav-ton sav-{ton}">{ton}</span>'
           f'<span class="sav-pages">apparaît sur {n} page{"s" if n > 1 else ""} (ex. {H.escape(ex_txt)})</span></div>')
    return lab + "\n" + s

def tete(page, titre, classes):
    h = open(page, encoding="utf-8").read()
    head = h[:h.index("</head>")]
    head = re.sub(r"<title>.*?</title>", f"<title>{titre}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="robots"[^>]*>', "", head)
    head = re.sub(r'<link rel="(canonical|alternate)"[^>]*>', "", head)
    head = head.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
    css = '<link rel="stylesheet" href="/valora.css">'
    add = ('<link rel="stylesheet" href="/valora-clair.css"><link rel="stylesheet" href="/valora-b.css">'
           '<link rel="stylesheet" href="/sections-a-valider.css">'
           '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">')
    head = head.replace(css, css + add, 1) if css in head else head + add
    scripts = set()
    for p in ("fr/index.html", "fr/kosher-chalet-les-deux-alpes/index.html", "fr/kosher-val-thorens/index.html",
              "fr/jewish-lyon-tours/index.html"):
        for m in re.finditer(r'<script[^>]*src="([^"]+)"[^>]*>\s*</script>', open(p, encoding="utf-8").read()):
            if not re.search(r"demande|plan|mesure|gtag|prix", m.group(1)):
                t = m.group(0)
                if "leaflet" in t:
                    t = re.sub(r"\s(defer|async)(?=[\s>])", "", t)
                scripts.add(t)
    for p in ("fr/kosher-alpe-dhuez/index.html", "fr/chabad-lyon/index.html"):
        for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", open(p, encoding="utf-8").read(), re.S):
            if "carte-osm" in m.group(1) or "L.map" in m.group(1):
                scripts.add(m.group(0))
    return head + f'</head>\n<body class="{classes}">', "\n".join(sorted(scripts))

INTRO = ('<div class="sav-intro"><h1>Sections à valider</h1><p>Chaque type de section du site, une seule fois, '
         'dans la version alternée noir et blanc luxe, avec les icônes au trait fin doré. Le numéro sert à me répondre '
         '(« 4 ok, 7 à revoir »).</p>{nav}</div>')

def page(dest, titre, classes, liste, deja, nav, zone):
    head, scripts = tete("fr/index.html", titre, classes)
    corps = [INTRO.format(nav=nav), "<main>"]
    for i, (nom, ton, p, t) in enumerate(liste, 1):
        corps.append(bloc(i, nom, ton, p, t, zone, zone == "alpes"))
    corps.append("</main>")
    if deja:
        corps.append('<details class="sav-deja"><summary>Déjà validé sur l\'accueil (replié)</summary><main>')
        for i, (nom, ton, p, t) in enumerate(deja, 1):
            corps.append(bloc(f"V{i}", nom, ton, p, t, "alpes", True))
        corps.append("</main></details>")
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    Path(dest).write_text(head + "\n" + "\n".join(corps) + "\n" + scripts + "\n</body></html>\n", encoding="utf-8")

CSS_LYON_BLANC = {"#f7f3ec": "#F7F7F7", "#f0e9dc": "#FFFFFF", "#fffdf9": "#FFFFFF", "#e6dccb": "#E6E6E3",
                  "#f3ece0": "transparent", "#4a4640": "#4A4C50", "rgba(255,253,249,.97)": "rgba(255,255,255,.97)"}

def css():
    src = open("valora.css", encoding="utf-8").read()
    lyon = []
    for r in re.findall(r"[^{}]+\{[^{}]*\}", src):
        sel, decl = r.split("{", 1)
        if not re.search(r"valora-(visite|clair)", sel):
            continue
        if not any(k in decl.lower() for k in CSS_LYON_BLANC):
            continue
        d = decl
        for a, b in CSS_LYON_BLANC.items():
            d = re.sub(re.escape(a), b, d, flags=re.I)
        lyon.append(sel.strip() + "{" + d)
    icos = sorted(f[:-4] for f in os.listdir("img/ico/or"))
    swap = []
    for k in icos:
        a = f'img[src="/img/ico/or/{k}.svg"]'
        swap.append(f'body.sav .clair {a},body.sav.valora-visite main section:not(.ticket-zone):not(.bande):not(.hero):not(.fiche-hero) {a},'
                    f'body.sav.valora-clair main section:not(.ticket-zone):not(.pratique-hero) {a}{{content:url(/img/ico/or-fonce/{k}.svg)}}')
    base = """/* GÉNÉRÉ par _sections_a_valider.py : page de validation des sections (Moshé 27/10). */
body.sav .sav-intro{max-width:none;margin:0;padding:32px 20px 12px;background:#141518;color:#f5f2ec}
body.sav .sav-intro h1{color:#f5f2ec !important}
body.sav .sav-intro h1{font-family:'Playfair Display',serif;font-weight:500;font-size:34px;margin:0 0 8px}
body.sav .sav-intro p{color:#cfcac1;font-size:15px;line-height:1.5;margin:0 0 12px}
body.sav .sav-intro a{color:#F6DC8C}
body.sav .sav-label{position:relative;z-index:5;display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:0;padding:12px 20px;background:#1F4FD1;color:#fff;font:600 14px/1.35 Heebo,sans-serif;letter-spacing:0;text-transform:none}
body.sav .sav-label .sav-n{display:inline-grid;place-items:center;min-width:30px;height:30px;padding:0 6px;border-radius:999px;background:#fff;color:#1F4FD1;font-weight:700}
body.sav .sav-ton{padding:2px 10px;border-radius:999px;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
body.sav .sav-noir{background:#141518;color:#fff}
body.sav .sav-blanc{background:#fff;color:#141518}
body.sav .sav-pages{flex-basis:100%;font-weight:400;font-size:12.5px;opacity:.9}
body.sav .sav-deja{margin-top:40px;border-top:4px solid #1F4FD1}
body.sav .sav-deja>summary{cursor:pointer;padding:18px 20px;background:#1F4FD1;color:#fff;font:600 16px Heebo,sans-serif}
body.sav main{display:block}
/* icônes au trait fin doré, sans cercle ni fond */
html body.sav.sav main img[src*="/img/ico/"]{background:none !important;padding:0 !important;border-radius:0 !important;box-shadow:none !important;border:0 !important;object-fit:contain !important;width:28px !important;height:28px !important;flex:0 0 28px !important}
html body.sav.sav main .etapes img[src*="/img/ico/"],html body.sav.sav main #how img[src*="/img/ico/"]{width:36px !important;height:36px !important;flex-basis:36px !important}
html body.sav.sav main .dk-h2img[src*="/img/ico/"]{width:44px !important;height:44px !important}
/* Horaires de Chabbat dans une section blanche : carte blanche lisible */
html body.sav.sav .clair .shabbat{background:#FFFFFF !important;border:1px solid #E6E6E3 !important;box-shadow:0 10px 28px rgba(20,21,24,.06) !important}
html body.sav.sav .clair .shabbat,html body.sav.sav .clair .shabbat *{color:#1C1D20 !important}
html body.sav.sav .clair .shabbat small,html body.sav.sav .clair .shabbat .doux,html body.sav.sav .clair .shabbat p{color:#4A4C50 !important}
html body.sav.sav .clair .shabbat h2 i,html body.sav.sav .clair .shabbat h3 i{color:#8A6416 !important;-webkit-text-fill-color:#8A6416 !important;background:none !important}
/* « + » de la FAQ en doré foncé sur blanc */
html body.sav.sav .clair.faq summary::after,html body.sav.sav .clair .faq summary::after,html body.sav.sav.valora-visite .faq summary::after{background:transparent !important;border:1px solid #8A6416 !important;color:#8A6416 !important}
/* Bannière illustrée (van) : voile sombre pour lire le titre */
html body.sav.sav .lead-hero3-illus{position:relative}
html body.sav.sav .lead-hero3-illus::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(20,21,24,.35),rgba(20,21,24,.78));pointer-events:none}
html body.sav.sav .lead-hero3-illus>*:not(img){position:relative;z-index:2}
html body.sav.sav .lead-hero3-illus .lead3-bloc{background:rgba(20,21,24,.78) !important;backdrop-filter:blur(4px);border-radius:20px;padding:22px 18px !important;margin:0 16px !important}
"""
    Path("sections-a-valider.css").write_text(base + "/* icônes en doré foncé sur fond blanc */\n" + "\n".join(swap)
                                              + "\n/* Lyon : crème -> blanc luxe (sur cette page seulement) */\n" + "\n".join(lyon) + "\n",
                                              encoding="utf-8")

if __name__ == "__main__":
    css()
    page("fr/sections-a-valider/index.html", "Sections à valider · Alpes", "valora theme-b sav", ALPES, DEJA,
         '<p><a href="/fr/sections-a-valider/lyon/">→ Partie Lyon (visites et guides)</a></p>', "alpes")
    page("fr/sections-a-valider/lyon/index.html", "Sections à valider · Lyon", "valora valora-visite sav", LYON, [],
         '<p><a href="/fr/sections-a-valider/">← Partie Alpes et commun</a></p>', "lyon")
    print("ok", len(ALPES), len(LYON), len(DEJA), "manque:", MANQUE)
