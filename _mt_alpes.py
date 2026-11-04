"""Pages Alpes du système de design v2 (DESIGN-SITE.md §4) : accueil, stations, fiches chalet, hub chalets, services, Pessah/été/villa/van.
Usage : python _mt_alpes.py [--racine <dossier>] [page.html ...]   (à lancer APRÈS _mt_socle.py)
Idempotent : le marqueur <!--MT-ALPES--> dans le head empêche tout second passage. Ne supprime aucun texte, ni SEO, ni JSON-LD, ni data-prix-tpl, ni id d'ancre.
Ne lance ni _build_i18n.py, ni _zones.py, ni _kit_wp.py."""
import os, re, sys, pathlib, argparse, collections

ICI = pathlib.Path(__file__).parent
MARQUE = "<!--MT-ALPES-->"
LANGS = ["", "fr/", "es/", "he/"]
STATIONS = ["alpe-dhuez", "annecy", "cervinia", "chamonix", "cortina", "courchevel", "courmayeur", "crans-montana", "davos", "grenoble",
            "gstaad", "la-plagne", "les-arcs", "les-deux-alpes", "les-menuires", "megeve", "st-moritz", "val-disere", "val-thorens", "verbier", "zermatt"]
SLUGS = {"accueil": [""], "station": ["kosher-" + s for s in STATIONS],
         "hubalps": ["alps", "kosher-ski-anywhere", "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps"],
         "hub": ["kosher-chalets"], "services": ["kosher-services-french-alps"],
         "divers": ["kosher-pesach-french-alps", "summer-in-the-alps-jewish-families", "kosher-villa-saint-tropez", "kosher-van-transfers"]}
CHALETS = ["kosher-chalet-courchevel", "kosher-chalet-courchevel-aurore-boreale", "kosher-chalet-courchevel-renard-argente", "kosher-chalet-les-deux-alpes",
           "kosher-chalet-les-menuires", "kosher-chalet-megeve", "kosher-chalet-val-thorens", "kosher-slope-chalet-les-deux-alpes"]

# --- libellés nouveaux, 4 langues (en, fr, es, he) -----------------------------------------------
L = {
    "guide": ("Guide to", "Guide de", "Guía de", "מדריך: "),
    "guide0": ("Guide", "Guide", "Guía", "מדריך"),
    "wa": ("WhatsApp", "WhatsApp", "WhatsApp", "וואטסאפ"),
    "casher": ("Strictly kosher · Chalav Yisrael · Shomer Shabbat", "Strictement casher · Chalav Yisrael · Chomer Chabbat",
               "Estrictamente kosher · Chalav Yisrael · Shomer Shabat", "שומר כשרות · חלב ישראל · שומר שבת"),
    "f_route": ("from {c} airport", "depuis l'aéroport de {c}", "desde el aeropuerto de {c}", "מנמל התעופה של {c}"),
    "f_meals": ("Meals", "Repas", "Comidas", "ארוחות"),
    "f_meals_l": ("delivered in the resort", "livrés en station", "entregadas en la estación", "במשלוח"),
    "f_bh_l": ("minyan and meals, on WhatsApp", "minyan et repas, sur WhatsApp", "minyan y comidas, por WhatsApp", "מניין וארוחות בוואטסאפ"),
    "f_bh_l0": ("minyan, on WhatsApp", "minyan, sur WhatsApp", "minyan, por WhatsApp", "מניין בוואטסאפ"),
    "f_bh": ("Beth Habad", "Beth Habad", "Beth Habad", "בית חב״ד"),
    "f_sh": ("Shabbat", "Shabbat", "Shabat", "שבת"),
    "f_sh_l": ("candle lighting and Havdalah", "allumage des bougies et Havdalah", "encendido de velas y Havdalá", "הדלקת נרות והבדלה"),
    "min": ("min", "min", "min", "דק׳"),
}
CITES = {"lyon": ("Lyon", "Lyon", "Lyon", "ליון"), "geneva": ("Geneva", "Genève", "Ginebra", "ז'נבה"), "zurich": ("Zurich", "Zurich", "Zúrich", "ציריך"),
         "turin": ("Turin", "Turin", "Turín", "טורינו"), "venice": ("Venice", "Venise", "Venecia", "ונציה"), "nice": ("Nice", "Nice", "Niza", "ניס")}
LI = {"en": 0, "fr": 1, "es": 2, "he": 3}

# --- découpage HTML ------------------------------------------------------------------------------
VOID = {"img", "br", "input", "hr", "meta", "link", "source", "track", "wbr", "col", "area", "base", "embed", "param"}
TOK = re.compile(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<(/?)([a-zA-Z][\w-]*)\b[^>]*?(/?)>", re.S)


def split_blocks(m):
    out, pos, depth, start = [], 0, 0, None
    for t in TOK.finditer(m):
        s = t.group(0)
        if depth == 0 and t.start() > pos:
            gap = m[pos:t.start()]
            if gap.strip():
                out.append(("raw", gap.strip()))
            pos = t.start()
        if s.startswith("<!--") or s.startswith("<script") or s.startswith("<style"):
            if depth == 0:
                out.append(("raw", s)); pos = t.end()
            continue
        close, tag, selfc = t.group(1), t.group(2).lower(), t.group(3)
        if tag in VOID or selfc:
            if depth == 0:
                out.append(("raw", s)); pos = t.end()
            continue
        if not close:
            if depth == 0:
                start = t.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append(("el", m[start:t.end()])); pos = t.end()
    return out


def head_of(el):
    t = re.match(r"<(\w+)([^>]*)>", el)
    c = re.search(r'class="([^"]*)"', t.group(2))
    i = re.search(r'\bid="([^"]*)"', t.group(2))
    return t.group(1), (c.group(1).split() if c else []), (i.group(1) if i else "")


def inner(el):
    a = el.find(">") + 1
    b = el.rfind("</")
    return el[a:b]


def open_tag(el):
    return re.match(r"<\w+[^>]*>", el).group(0)


def with_classes(el, add=(), rem=()):
    tag = open_tag(el)
    cl = head_of(el)[1]
    cl = [c for c in cl if c not in rem] + [c for c in add if c not in cl]
    if re.search(r'class="[^"]*"', tag):
        new = re.sub(r'class="[^"]*"', 'class="' + " ".join(cl) + '"', tag, count=1) if cl else re.sub(r'\s*class="[^"]*"', "", tag, count=1)
    else:
        new = tag[:-1] + ' class="' + " ".join(cl) + '">'
    return new + el[len(tag):]


def plain(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()


def h2_of(h):
    m = re.search(r"<h2\b[^>]*>(.*?)</h2>", h, re.S)
    return m


class U:
    def __init__(self, pre, html, post):
        self.pre, self.html, self.post = pre, html, post
        if html:
            self.tag, self.cls, self.id = head_of(html)
        else:
            self.tag, self.cls, self.id = "", [], ""
        self.kind = self.classify()

    def classify(self):
        c, h = set(self.cls), self.html
        if not h:
            return "raw"
        if self.tag == "script":
            return "raw"
        if "hero" in c:
            return "hero"
        if "lead-intro" in c:
            return "intro"
        if "kwp" in c or "galerie-wp" in c:
            return "kwp"
        if "shabbat-bloc" in c:
            return "shabbat"
        if "repas-prix" in c:
            return "prix"
        if "minyan-bh" in c:
            return "minyan"
        if "faq" in c:
            return "faq"
        if self.id == "book" or "lead-final" in c or "ticket-zone" in c:
            return "book"
        if self.id == "voisines":
            return "voisines"
        if "cta-etapes" in c:
            return "cta"
        if "etapes" in c:
            return "etapes"
        if "carte-osm" in h:
            return "map"
        if "dk-suite" in h and "<h2" in h and not re.search(r"<p>[^<]{40}", h):
            return "liens"
        return "bloc"

    def out(self):
        return (self.pre + "\n" if self.pre else "") + self.html + ("\n" + self.post if self.post else "")


def units(m):
    bl = split_blocks(m)
    out, i = [], 0
    while i < len(bl):
        k, b = bl[i]
        if k == "raw" and re.match(r"<!--KIT-WP:[^>]*-->$", b) and i + 2 < len(bl) and bl[i + 1][0] == "el" and bl[i + 2][0] == "raw" and "/KIT-WP" in bl[i + 2][1]:
            out.append(U(b, bl[i + 1][1], bl[i + 2][1])); i += 3; continue
        if k == "el":
            out.append(U("", b, ""))
        else:
            u = U("", "", ""); u.pre = b; u.kind = "raw"; out.append(u)
        i += 1
    return out


# --- briques ---------------------------------------------------------------------------------------
def sec(classes, body, wrap=True):
    inner_ = f'<div class="wrap">{body}</div>' if wrap == "div" else body
    cl = "ss " + ("wrap " if wrap is True else "") + classes
    return f'<section class="{cl.strip()}">{inner_}</section>'


def cta_bh(h, lg):
    """Lien WhatsApp du Beth Habad (texte long sur deux lignes) -> une ligne de texte + bouton secondaire « WhatsApp »."""
    def f(m):
        a = m.group(2)
        if "class='btn-noir'" not in a and 'class="btn-noir"' not in a:
            return m.group(0)
        href = re.search(r"href=(['\"])(.*?)\1", a).group(2)
        svg = re.search(r"<svg\b.*?</svg>", a, re.S)
        txt = plain(re.sub(r"<svg\b.*?</svg>", "", a, flags=re.S))
        wa = L["wa"][lg]
        svg = svg.group(0) if svg else ""
        if svg and "data-wa" not in svg:
            svg = svg.replace("<svg", "<svg data-wa", 1)
        op = m.group(1) if "cta-bh" in m.group(1) else re.sub(r"class=(['\"])", lambda q: "class=" + q.group(1) + "cta-bh ", m.group(1), count=1)
        return f'{op}<span class="bh-txt">{txt}</span><a class="pill" href="{href}" rel="noopener" aria-label="{txt}">{svg}{wa}</a></p>'
    return re.sub(r'(<p\b[^>]*class=[\'"][^\'"]*\bcta-(?:bh|hero)\b[^\'"]*[\'"][^>]*>)(<a\b[^>]*33781823193.*?</a>)</p>', f, h, flags=re.S)


def ltr(b):
    return f'<span dir="ltr">{b}</span>' if re.search(r"\d", b) and not re.search(r"[֐-׿]", b) else b


def route(racine, slug, lg):
    """(temps, ville) lus dans la page EN : « From Geneva airport: ... 1 h 15 to 1 h 30 ... »."""
    p = racine / slug / "index.html"
    if not p.exists():
        return None
    t = p.read_text(encoding="utf-8")
    for h2 in re.finditer(r"<h2\b[^>]*>(?:<img[^>]*>)?\s*Getting to.*?</h2>(.*?)(?=</section>|</div>\s*</div>)", t, re.S):
        li = re.search(r"<li\b[^>]*>(.*?)</li>", h2.group(1), re.S)
        if not li:
            continue
        s = plain(li.group(1))
        tm = re.search(r"(\d+) h(?: (\d{2}))?|(\d+) minutes", s)
        if not tm:
            return None
        ville = next((k for k, n in (("lyon", "Lyon"), ("geneva", "Geneva"), ("zurich", "Z"), ("turin", "Turin"), ("venice", "Venice"), ("nice", "Nice")) if s.startswith("From " + n) or ("From " + n) in s[:30]), None)
        if not ville:
            return None
        temps = f"{tm.group(1)} h" + (f" {tm.group(2)}" if tm.group(2) else "") if tm.group(1) else f"{tm.group(3)} {L['min'][lg]}"
        return temps, ville
    return None


def faits_station(us, racine, slug, lg):
    cells = []
    r = route(racine, slug, lg) if slug else None
    if r:
        cells.append((r[0], L["f_route"][lg].format(c=CITES[r[1]][lg])))
    allh = " ".join(u.html for u in us)
    nbh = allh.count("cta-bh")
    if nbh >= 2:
        cells.append((L["f_meals"][lg], L["f_meals_l"][lg]))
    if nbh >= 1:
        cells.append((L["f_bh"][lg], L[("f_bh_l" if nbh >= 2 else "f_bh_l0")][lg]))
    if any(u.kind == "shabbat" for u in us):
        cells.append((L["f_sh"][lg], L["f_sh_l"][lg]))
    if len(cells) < 2:
        return ""
    lis = "".join(f"<li><b>{ltr(b) if lg == 3 else b}</b>{l}</li>" for b, l in cells[:4])
    return f'<section class="ss wrap faits-bloc"><ul class="faits">{lis}</ul></section>'


def photo_ed(nom, lg):
    return (f'<div class="ed-photo"><img src="/img/h/{nom}-960.webp" srcset="/img/h/{nom}-640.webp 640w, /img/h/{nom}-960.webp 960w, /img/h/{nom}-1600.webp 1600w" '
            f'sizes="(min-width:960px) 50vw, 100vw" alt="" width="960" height="644" loading="lazy" decoding="async"></div>')


def to_ed(u, nom, n, lg):
    body = inner(u.html)
    m = re.fullmatch(r'\s*<div class="wrap">(.*)</div>\s*', body, re.S)
    body = m.group(1) if m else body
    img = "<img" in re.sub(r"<img[^>]*(?:ico|picto)[^>]*>", "", body)
    photo = "" if img else photo_ed(nom, lg)
    cl = f"ss wrap ed ed-{n}" + (" ed-img" if img else "")
    return f'<section class="{cl}">{photo}<div class="ed-texte">{body}</div></section>'


def to_acc(u, titre_defaut=""):
    body = u.html
    m = h2_of(inner(body))
    if m:
        titre = f"<h2{m.group(0)[3:m.group(0).find('>')]}>{m.group(1)}</h2>"
        titre = re.sub(r"<img[^>]*>", "", titre)
        rest = inner(body)[:m.start()] + inner(body)[m.end():]
    else:
        titre, rest = f"<h2>{titre_defaut}</h2>", inner(body)
    mm = re.fullmatch(r'\s*<div class="wrap">(.*)</div>\s*', rest, re.S)
    rest = mm.group(1) if mm else rest
    return f'<details class="acc"><summary>{titre}</summary><div class="acc-corps">{rest}</div></details>'


def liste_liens(u):
    return with_classes(u.html, add=["liens", "wrap"], rem=["beige", "clair-2", "clair"])


def clean(u):
    if u.html:
        u.html = with_classes(u.html, rem=["beige", "clair-2"])
    return u


def extraire_kit(u):
    """Un bloc qui porte des cartes chalet <!--KIT-WP:x-->…<!--/KIT-WP:x--> : les cartes deviennent leur section."""
    m = re.search(r"(<!--KIT-WP:(\w+)-->)(.*?)(<!--/KIT-WP:\2-->)", u.html, re.S)
    if not m or u.kind in ("kwp",):
        return None
    u.html = u.html[:m.start()] + u.html[m.end():]
    return U(m.group(1), f'<section class="ss wrap kwp">{m.group(3)}</section>', m.group(4))


def kwp_unit(u):
    h = u.html
    cl = head_of(h)[1]
    if "kwp-diapo" in cl or "galerie-wp" in cl:
        return u
    if "kwp-accueil" in cl:
        ident = f' id="{u.id}"' if u.id else ""
        u.html = f'<section class="ss kwp kwp-accueil bande-encre"{ident}><div class="wrap">{inner(h)}</div></section>'
        return u
    u.html = with_classes(h, rem=["clair", "clair-2", "beige"])
    return u


# --- composition par type ---------------------------------------------------------------------------
def recompose(us, typ, lg, racine, slug):
    us = [clean(u) for u in us]
    for u in list(us):
        if u.kind == "bloc":
            k = extraire_kit(u)
            if k:
                us.insert(us.index(u) + 1, k)
    by = collections.defaultdict(list)
    for u in us:
        by[u.kind].append(u)
    for u in by["kwp"]:
        kwp_unit(u)
    out = []
    pris = set()

    def add(u):
        if u is not None and id(u) not in pris:
            pris.add(id(u)); out.append(u.out() if isinstance(u, U) else u)

    hero = by["hero"][:1]
    for u in hero:
        add(u)
    if typ in ("station", "hubalps", "divers", "hub"):
        f = faits_station(us, racine, slug, lg) if typ != "hub" else ""
        if f:
            out.append(f)
    for u in by["intro"]:
        u.html = with_classes(u.html, rem=["clair"]); add(u)
    kw = by["kwp"]
    if typ == "services":
        for u in by["bloc"][:1]:
            u.html = with_classes(u.html, add=["svc"]); add(u)
        for u in by["prix"]:
            body = inner(u.html)
            body = re.sub(r'<ul class="rp-cartes">', '<ul class="rp-cartes prix">', body)
            body = re.sub(r'(<div class="prix-table[^"]*">)<ul>', r'\1<ul class="prix">', body)
            u.html = f'<section class="ss bande-pierre repas-prix" id="meal-prices"><div class="wrap">{body}</div></section>'
            add(u)
    elif typ == "hub":
        for u in kw:
            add(u)
        for u in by["bloc"]:
            u.html = with_classes(u.html, add=["svc"], rem=["clair", "beige"]); add(u)
        for u in by["etapes"]:
            add(u)
        for u in by["cta"]:
            add(u)
    else:
        for u in kw:
            add(u)
    if typ in ("station", "hubalps", "divers"):
        blocs = by["bloc"]
        nb = 2 if typ == "station" else 1
        eds = blocs[:nb]
        names = ["reve-chef", "reve-table"]
        for i, u in enumerate(eds):
            out.append(to_ed(u, names[i], i + 1, lg)); pris.add(id(u))
        reste = blocs[nb:]
        items = [to_acc(u) for u in reste]
        for u in by["etapes"]:
            items.append(to_acc(u))
        for u in by["minyan"]:
            items.append(to_acc(u))
        if typ == "station":
            ville = re.search(r'name="lieu" value="([^"]*)"', " ".join(u.html for u in by["book"]))
            titre = (L["guide"][lg] + ("" if lg == 3 else " ") if ville else L["guide0"][lg])
            titre = (titre + ville.group(1)) if ville else titre
            if lg == 3 and ville:
                titre = L["guide"][lg] + f'<span dir="ltr">{ville.group(1)}</span>'
        else:
            titre = L["guide0"][lg]
        if items:
            out.append(f'<section class="ss wrap guide"><h2>{titre}</h2>{"".join(items)}</section>')
        for u in by["etapes"] + by["minyan"] + blocs:
            pris.add(id(u))
        for u in by["cta"]:
            add(u)
        for u in by["shabbat"]:
            u.html = with_classes(u.html, rem=["clair", "clair-2"]); add(u)
        for u in by["voisines"]:
            u.html = liste_liens(u); add(u)
        for u in by["liens"]:
            u.html = liste_liens(u); add(u)
        for u in by["faq"]:
            u.html = with_classes(u.html, rem=["clair", "clair-2"]); add(u)
        for u in by["map"]:
            add(u)
    elif typ in ("services", "hub"):
        if typ == "services":
            blocs = [u for u in by["bloc"][1:]]
            items = [to_acc(u) for u in blocs] + [to_acc(u) for u in by["etapes"]]
            if items:
                out.append(f'<section class="ss wrap guide">{"".join(items)}</section>')
            for u in blocs + by["etapes"]:
                pris.add(id(u))
            for u in by["cta"]:
                add(u)
            for u in by["map"]:
                add(u)
            for u in by["minyan"]:
                u.html = with_classes(u.html, rem=["clair", "clair-2"]); add(u)
        else:
            for u in by["map"] + by["minyan"] + by["shabbat"]:
                add(u)
        for u in by["faq"]:
            u.html = with_classes(u.html, rem=["clair", "clair-2"]); add(u)
    if typ != "station" and typ in ("hubalps", "divers"):
        pass
    for u in by["book"]:
        add(u)
    for u in by["liens"] + by["voisines"]:
        if id(u) not in pris:
            u.html = liste_liens(u); add(u)
    for u in us:
        if id(u) not in pris and u.kind != "hero":
            add(u)
    return "\n".join(out)


def accueil(us):
    out = []
    for u in us:
        u = clean(u)
        if u.kind == "kwp":
            kwp_unit(u)
        out.append(u.out())
    return "\n".join(out)


# --- fiche chalet ---------------------------------------------------------------------------------
def faits_chalet(racine, pref, slug, lg):
    p = racine / pref / "kosher-chalets" / "index.html"
    if not p.exists():
        return ""
    t = p.read_text(encoding="utf-8")
    for a in re.finditer(r'<article class="kwp-carte">.*?</article>', t, re.S):
        s = a.group(0)
        if f"/{slug}/" not in s:
            continue
        lis = re.findall(r"<li>\s*<svg.*?</svg>\s*<span><b>(.*?)</b>(.*?)</span></li>", s, re.S)
        if len(lis) >= 3:
            return '<ul class="faits lc-faits">' + "".join(f"<li><b>{ltr(b) if lg == 3 else b}</b>{l}</li>" for b, l in lis[:4]) + "</ul>"
    return ""


def chalet(main, racine, pref, slug, lg):
    f = faits_chalet(racine, pref, slug, lg)
    if f:
        main = re.sub(r'(<p class="[^"]*\blc-chiffres\b[^"]*"[^>]*>)', f + r"\1", main, count=1)
    ligne = f'<p class="lc-casher">{L["casher"][lg]}</p>'
    main, n = re.subn(r'(<p class="lc-prix"[^>]*>.*?</p>)', r"\1" + ligne.replace("\\", "\\\\"), main, count=1, flags=re.S)
    main = re.sub(r'class="([^"]*)\b(?:clair-2|beige)\b([^"]*)"', lambda m: 'class="' + re.sub(r"\s+", " ", m.group(1) + m.group(2)).strip() + '"', main)
    main = re.sub(r'(<a class="lc-btn lc-blanc lc-wa"[^>]*>)(?!<svg)', r'\1<svg data-wa viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg>', main)
    return main, bool(f), n


# --- page ------------------------------------------------------------------------------------------
LEAFLET = re.compile(r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet/[^"]*">\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet/[^"]*"></script>\s*<script>\s*document\.querySelectorAll\("\.carte-osm"\).*?</script>', re.S)
MOB = re.compile(r"<!--MOB-ALPES--><script data-mob-alpes>.*?</script>", re.S)


def page(html, typ, racine, pref, slug, c):
    if MARQUE in html or "<!--MT-V2-->" not in html:
        return None
    lg = LI[(re.search(r'<html[^>]*\blang="(\w\w)', html) or [0, "en"])[1]]
    a = html.find("<main")
    a2 = html.find(">", a) + 1
    b = html.rfind("</main>")
    mhead, m, mtail = html[:a2], html[a2:b], html[b:]
    if typ == "chalet":
        m, okf, okc = chalet(m, racine, pref, slug, lg)
        c["chalet_faits"] += okf; c["chalet_ligne_casher"] += okc
    else:
        us = units(m)
        m = "\n" + (accueil(us) if typ == "accueil" else recompose(us, typ, lg, racine, slug)) + "\n"
    m = cta_bh(m, lg)
    c["cta_bh"] += m.count('class="bh-txt"')
    m, k = re.subn(r"(<h[123]\b[^>]*>(?:(?!</h[123]>).)*?)</i>([?.!:])", r"\1\2</i>", m, flags=re.S)
    c["ponctuation_dans_i"] += k
    html = mhead + m + mtail
    html, k = LEAFLET.subn('<script src="/js/mt-carte.js" defer></script>', html)
    c["leaflet_paresseux"] += k
    html, k = re.subn(r"<style[^>]*>\s*\.lead-hero3::after\{[^}]*\}\s*</style>\s*", "", html)
    c["style_voile_hero_retire"] += k
    html, k = MOB.subn("", html)
    c["script_mob_alpes_retire"] += k
    html = html.replace("</head>", MARQUE + "</head>", 1)
    ib = html.find("<body")
    ie = html.find(">", ib) + 1
    html = html[:ib] + with_classes(html[ib:ie], add=["mt-alpes", "mt-" + typ]) + html[ie:]
    c["pages_" + typ] += 1
    return html


# --- 2e passe (04/11, correctifs de la relecture) ---------------------------------------------------
MARQUE2 = "<!--MT-ALPES-2-->"
# ligne de supervision, reprise mot pour mot de la page services de chaque langue
SURV = ("Kosher supervision: Beth Habad de Grenoble Alpes, Rav Yehia Lahiany.", "Surveillance : Beth Habad de Grenoble Alpes, rav Yehia Lahiany.",
        "Supervisión: Beth Habad de Grenoble Alpes, rav Yehia Lahiany.", 'השגחה: בית חב"ד גרנובל אלפים, <bdi dir="ltr">Rav Yehia Lahiany</bdi>.')
LIEU = {"kosher-chalet-courchevel": "Courchevel", "kosher-chalet-courchevel-aurore-boreale": "Courchevel", "kosher-chalet-courchevel-renard-argente": "Courchevel",
        "kosher-chalet-les-deux-alpes": "Les Deux Alpes", "kosher-chalet-les-menuires": "Les Ménuires", "kosher-chalet-val-thorens": "Val Thorens"}


def page2(html, typ, pref, slug, c):
    """Ouverture « Ski by day » retirée des stations et des fiches ; fiche : ligne de supervision, nom du chalet dans le message WhatsApp et dans les liens Plan your trip."""
    from urllib.parse import quote
    if MARQUE not in html or MARQUE2 in html or typ not in ("station", "chalet"):
        return None
    lg = LI[(re.search(r'<html[^>]*\blang="(\w\w)', html) or [0, "en"])[1]]
    neuf = html
    if typ == "station":
        neuf, k = re.subn(r'<!--MANIFESTE-->(?=\s*<div class="mf">).*?<!--/MANIFESTE-->\s*', "", neuf, flags=re.S)
        c["ouverture_station_retiree"] += k
    else:
        neuf, k1 = re.subn(r'\s*<p class="lc-note"[^>]*>.*?</p>', "", neuf, count=1, flags=re.S)
        neuf, k2 = re.subn(r'\s*<ul class="lc-assure"[^>]*>.*?</ul>', "", neuf, count=1, flags=re.S)
        c["ouverture_fiche_retiree"] += k1 and k2
        nom = re.search(r'<div class="lc-colle"[^>]*>(?:<!--[^>]*-->)?<div><b>(.*?)</b>', neuf, re.S)
        if nom:
            nom = plain(nom.group(1))
            neuf, k = re.subn(r'(<p class="lc-casher">.*?</p>)', lambda m: m.group(1) + f'<p class="lc-surv">{SURV[lg]}</p>', neuf, count=1, flags=re.S)
            c["fiche_ligne_supervision"] += k

            def wa(m):
                h = m.group(2)
                if "text=" not in h or quote(nom) in h:
                    return m.group(0)
                c["fiche_wa_avec_nom"] += 1
                return m.group(1) + re.sub(r"(text=[^&\"]*?\.%20)", lambda q: q.group(1) + quote(nom) + ".%20", h, count=1) + '"'
            neuf = re.sub(r'(<a class="lc-btn lc-blanc lc-wa"[^>]*href=")([^"]*)"', wa, neuf)
            lieu = LIEU.get(slug)
            q = "?i=a" + (f"&amp;lieu={quote(lieu)}&amp;voyage=Ski%20holiday%20with%20a%20chalet" if lieu else "") + f"&amp;chalet={quote(nom)}"
            neuf, k = re.subn(r'(class="nav-cta" href="[^"?]*plan-your-trip/)"', lambda m: m.group(1) + q + '"', neuf)
            neuf, k2 = re.subn(r'(<a href="[^"?]*plan-your-trip/)"( class="nav-cta")', lambda m: m.group(1) + q + '"' + m.group(2), neuf)
            c["fiche_liens_plan_avec_nom"] += k + k2
    if neuf == html:
        return None
    c["pages2_" + typ] += 1
    return neuf.replace(MARQUE, MARQUE + MARQUE2, 1)


def cibles(racine):
    out = []
    for pref in LANGS:
        for typ, slugs in SLUGS.items():
            for s in slugs:
                out.append((racine / pref / s / "index.html", typ, pref, s))
        for s in CHALETS:
            out.append((racine / pref / s / "index.html", "chalet", pref, s))
    return [x for x in out if x[0].exists()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=str(ICI))
    ap.add_argument("pages", nargs="*")
    a = ap.parse_args()
    racine = pathlib.Path(a.racine).resolve()
    cs = cibles(racine)
    if a.pages:
        veut = {(pathlib.Path(p) if pathlib.Path(p).is_absolute() else racine / p).resolve() for p in a.pages}
        cs = [x for x in cs if x[0].resolve() in veut]
    c = collections.Counter()
    ignorees = 0
    for p, typ, pref, slug in cs:
        t = p.read_bytes().decode("utf-8")
        n = page(t, typ, racine, pref, slug, c) if MARQUE not in t else page2(t, typ, pref, slug, c)
        if n is None:
            ignorees += 1
            continue
        p.write_bytes(n.encode("utf-8"))
    print(f"pages restructurées : {sum(v for k, v in c.items() if k.startswith('pages_'))}, corrigées (2e passe) : {sum(v for k, v in c.items() if k.startswith('pages2_'))}, laissées telles quelles : {ignorees}")
    for k, v in sorted(c.items()):
        print(f"  {k:<26} {v}")


main()
