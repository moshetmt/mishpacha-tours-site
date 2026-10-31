# -*- coding: utf-8 -*-
"""Passe visuelle (12/10) : pictos, cartes, tuiles. A lancer EN DERNIER, apres tous les builds et les traductions.
  python _decor.py            : toutes les pages, 4 langues
  python _decor.py alps       : une page (et ses 3 copies traduites)
  python _decor.py --strip    : retire toute la decoration (retour au HTML des builders)
Regle : aucun noeud texte n'est modifie, supprime ou deplace. La passe ajoute des classes dk-*, des <svg class="dk">,
des <img class="dk" alt=""> et des <span class="dk-sep"> autour de separateurs existants. Idempotente (strip puis pose).
Le choix du picto se fait sur le texte ANGLAIS et s'applique par position aux copies fr/ es/ he/.
`python _decor.py --check` compare le texte visible, les titres, les liens et le JSON-LD avant/apres : doit sortir 0 ecart.
"""
import os, re, io, sys, glob, html

LANGS = ("fr", "es", "he")
MORE = {"en": "Read more", "fr": "Lire la suite", "es": "Leer más", "he": "להמשך קריאה"}

# mot-cle anglais (dans le titre en gras, puis dans tout le li) -> picto Lucide de _decor_src/
ICO = [
  (r"grenoble side", "snowflake"), (r"courchevel side", "mountain-snow"),
  (r"by road|by car", "car"), (r"by train|tgv|ter|rail", "ticket"), (r"paris", "map-pin"),
  (r"saint-exup|airport|flight|fly|plane|geneva", "plane"), (r"shuttle|bus|transfer|by road|drive", "car"),
  (r"chef|kitchen", "chef-hat"), (r"meals? delivered|delivered meals|catering|restaurant|food|eat", "utensils"),
  (r"shabbat|candle", "flame"), (r"holiday|hanukkah|purim|pesach|festival", "sparkles"),
  (r"minyan|sefer|torah|pray|synagogue|shul", "scroll-text"), (r"tailor|a to z|whole stay|stay", "luggage"),
  (r"chalet|apartment|accommodation|hotel|sleep|where to stay", "house"),
  (r"resort by resort|by resort", "map-pin"), (r"other resort|elsewhere", "route"),
  (r"grenoble|courchevel|side|valley|mountain|alps|resort", "mountain-snow"),
  (r"ski|winter|snow|piste", "snowflake"), (r"summer|lake|hike", "sun"),
  (r"safe|security|escort|guard", "shield-check"), (r"flight|airport|fly|land", "plane"),
  (r"drive|car|transfer|road|taxi", "car"), (r"shop|grocer|supermarket|bakery", "shopping-basket"),
  (r"whatsapp|ask|contact|tell us", "message-circle"), (r"quote|price|cost|invoice", "file-text"),
  (r"group|famil|people|private", "users"), (r"date|when|season|calendar|open|hours", "calendar-days"),
  (r"time|hour|minutes|how long", "clock"), (r"history|museum|memorial|read|book", "book-open"),
  (r"visit|tour|walk", "footprints"), (r"ticket|entry|admission", "ticket"), (r"language|english|hebrew", "languages"),
]
LIENS = [(r"ski", "snowflake"), (r"summer|lake", "sun"), (r"stopover|3 hours", "clock"), (r"landing|flight|airport", "plane"), (r"gateway|drive", "car"),
  (r"chalet", "house"), (r"services", "chef-hat"), (r"shabbat meals|catering|restaurant", "utensils"), (r"shabbat", "flame"), (r"grande synagogue|synagogue", "landmark"),
  (r"safe", "shield-check"), (r"where to stay|hotel", "bed-double"), (r"mikveh", "waves"), (r"cemetery", "trees"), (r"chabad", "heart-handshake"),
  (r"faq|question", "info"), (r"itinerary|2 days", "route"), (r"history|juiverie", "book-open"), (r"izieu|montluc|chrd|memory", "scroll-text"),
  (r"vacation", "luggage"), (r"tour|walk", "footprints"), (r"guide", "map-pin"), (r"alps|val |courchevel|meg|huez|grenoble|annecy|chamonix|arcs|plagne|zermatt|moritz|crans|verbier|gstaad|davos|anywhere|cervinia|courmayeur|cortina", "mountain-snow")]
PREUVES = ["landmark", "badge-check", "utensils", "lock", "users", "calendar-x"]
# illustration posee a cote d'un h2 (jamais celle du hero de la page)
H2ILLUS = [(r"kosher|service|meal", "flat-kosher"), (r"safe", "line-private"), (r"shabbat", "line-shabbat"),
           (r"winter|summer|ski|resort", "flat-ski"), (r"lyon|stopover|land", "flat-stopover")]

# pages Alpes et van : le hassid du logo (dessin de marque) remplace toutes les illustrations posees a cote des h2
HASSID_PAGES = {"kosher-val-thorens", "kosher-courchevel", "kosher-megeve", "kosher-alpe-dhuez", "kosher-les-deux-alpes", "kosher-grenoble", "kosher-annecy",
                "kosher-chamonix", "kosher-les-arcs", "kosher-la-plagne", "kosher-val-disere", "kosher-services-french-alps", "alps", "kosher-ski-holidays-french-alps",
                "summer-in-the-alps-jewish-families", "kosher-vacation-french-alps", "kosher-van-transfers", "kosher-chalet-les-deux-alpes", "kosher-chalets", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-chalet-val-thorens",
                "kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana", "kosher-cervinia", "kosher-verbier", "kosher-gstaad", "kosher-davos", "kosher-ski-anywhere", "kosher-courmayeur", "kosher-cortina"}

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def txt(s): return html.unescape(re.sub("<[^>]+>", " ", s)).lower()

def sprite():
    out = []
    for f in sorted(glob.glob("_decor_src/*.svg")):
        s = rd(f); inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
        out.append(f'<symbol id="{os.path.basename(f)[:-4]}" viewBox="0 0 24 24">{inner}</symbol>')
    wr("img/pictos.svg", '<svg xmlns="http://www.w3.org/2000/svg">' + "".join(out) + "</svg>")

def vignettes():
    from PIL import Image
    os.makedirs("img/illus/v", exist_ok=True)
    for f in glob.glob("img/illus/*.png"):
        d = "img/illus/v/" + os.path.basename(f)[:-4] + ".webp"
        if not os.path.exists(d):
            im = Image.open(f).convert("RGBA"); im.thumbnail((240, 240)); im.save(d, "WEBP", quality=82)

DES = {os.path.basename(f)[:-5] for f in glob.glob("img/des/*.webp")}
def ico(name, cls="dk dk-ico"):
    """Mini-dessin (img/des/<nom>.webp, choix operateur du 12/10) pour les cartes ; picto au trait pour les coches et les fleches."""
    if "dk-ico" in cls and name in DES:
        return f'<img class="{cls} dk-des" src="/img/des/{name}.webp" alt="" width="96" height="96" loading="lazy">'
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="/img/pictos.svg#{name}"/></svg>'
def dessins():
    """_candidats/spots-*/<nom>.png (fond blanc) -> img/des/<nom>.webp 192 px, fond rendu transparent."""
    from PIL import Image, ImageDraw
    os.makedirs("img/des", exist_ok=True)
    for f in glob.glob("_candidats/spots-*/*.png"):
        n = os.path.basename(f)[:-4]; d = f"img/des/{n}.webp"
        if n.startswith("spot-") or os.path.exists(d): continue
        rgb = Image.open(f).convert("RGB"); w, h = rgb.size; M = (255, 0, 255)
        for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
            if rgb.getpixel(xy) != M and min(rgb.getpixel(xy)) > 225: ImageDraw.floodfill(rgb, xy, M, thresh=28)  # le fond part des bords : le blanc INTERIEUR du dessin reste
        im = Image.open(f).convert("RGBA"); im.putalpha(Image.eval(Image.frombytes("L", (w, h), bytes(0 if p == M else 255 for p in rgb.getdata())), lambda v: v))
        bb = im.getbbox(); im = im.crop(bb) if bb else im
        c = Image.new("RGBA", (max(im.size),) * 2, (0, 0, 0, 0)); c.paste(im, ((c.width - im.width) // 2, (c.height - im.height) // 2))
        c.resize((192, 192), Image.LANCZOS).save(d, "WEBP", quality=88)
def choisir(lead, tout):
    for src in (lead, tout):
        for pat, name in ICO:
            if re.search(pat, src): return name
    return "check"

# Regle (15/10) : dans une meme section, un mini-dessin ne sert qu'une fois. A la 2e occurrence : une alternative du meme sujet, puis le fonds commun.
ALT = {
  "plane": ["plane-landing", "clock", "landmark", "route", "map-pin", "luggage"],
  "plane-landing": ["plane", "clock", "route"],
  "car": ["bus", "route", "map-pin", "clock", "footprints", "luggage"],
  "bus": ["car", "ticket", "route"],
  "route": ["compass", "map-pin", "car", "footprints"],
  "check": ["badge-check", "info", "book-open", "sparkles", "heart-handshake"],
  "badge-check": ["check", "shield-check", "sparkles"],
  "scroll-text": ["book-open", "landmark", "languages", "file-text", "users"],
  "mountain-snow": ["cable-car", "snowflake", "trees", "map-pin", "route", "sun"],
  "snowflake": ["cable-car", "mountain-snow", "sparkles", "house", "sun"],
  "cable-car": ["mountain-snow", "snowflake", "ticket"],
  "flame": ["wine", "sparkles", "sun", "heart-handshake", "badge-check"],
  "wine": ["flame", "sparkles", "utensils"],
  "users": ["heart-handshake", "message-circle", "house", "languages", "sparkles"],
  "house": ["bed-double", "luggage", "map-pin", "trees"],
  "bed-double": ["house", "luggage", "lock"],
  "utensils": ["chef-hat", "croissant", "shopping-basket", "wine"],
  "chef-hat": ["utensils", "croissant", "wine"],
  "croissant": ["utensils", "shopping-basket", "chef-hat"],
  "shopping-basket": ["croissant", "utensils", "chef-hat"],
  "calendar-days": ["calendar-x", "clock", "file-text", "ticket", "info"],
  "calendar-x": ["calendar-days", "clock", "info"],
  "footprints": ["compass", "map-pin", "route", "book-open"],
  "compass": ["footprints", "map-pin", "route"],
  "book-open": ["scroll-text", "landmark", "file-text", "info"],
  "map-pin": ["compass", "route", "footprints", "landmark"],
  "clock": ["calendar-days", "ticket", "route", "info"],
  "sun": ["trees", "waves", "sparkles", "mountain-snow"],
  "trees": ["sun", "waves", "mountain-snow", "footprints"],
  "waves": ["sun", "trees", "snowflake"],
  "info": ["message-circle", "book-open", "file-text", "languages"],
  "landmark": ["book-open", "scroll-text", "map-pin", "badge-check"],
  "message-circle": ["heart-handshake", "users", "info", "languages"],
  "heart-handshake": ["users", "message-circle", "sparkles", "badge-check"],
  "shield-check": ["lock", "badge-check", "users"],
  "lock": ["shield-check", "badge-check", "bed-double"],
  "file-text": ["scroll-text", "book-open", "info", "ticket"],
  "languages": ["message-circle", "users", "book-open"],
  "sparkles": ["flame", "sun", "heart-handshake", "badge-check"],
  "ticket": ["calendar-days", "file-text", "bus"],
}
COMMUN = ["info", "book-open", "clock", "map-pin", "route", "landmark", "badge-check", "file-text", "users", "sparkles", "house", "luggage",
          "calendar-days", "message-circle", "footprints", "heart-handshake", "languages", "scroll-text", "compass", "check", "trees", "ticket", "wine"]
def unique(name, used):
    """name si libre dans la section, sinon la premiere alternative libre (sujet voisin, puis fonds commun). Rend aussi `used` mis a jour."""
    for c in [name] + ALT.get(name, []) + COMMUN:
        if c in DES and c not in used:
            used.add(c); return c
    return name

def strip(h):
    h = re.sub(r'<(svg|script|button) class="dk[^"]*"[^>]*>.*?</\1>', "", h, flags=re.S)
    h = re.sub(r'<img class="dk[^"]*"[^>]*>', "", h)
    h = re.sub(r'<span class="dk-g[a-z0-9 -]*">(.*?)</span>(?=\s|</p>)', r"\1", h, flags=re.S)
    h = re.sub(r'<span class="dk-sep">(.*?)</span>', r"\1", h, flags=re.S)
    h = re.sub(r' class="((?:dk-[a-z0-9-]+ ?)+)"', "", h)
    h = re.sub(r'class="([^"]*?)((?: dk-[a-z0-9-]+)+)"', r'class="\1"', h)
    return h

LI = re.compile(r"<li>(.*?)</li>", re.S)
UL = re.compile(r"<ul>(.*?)</ul>", re.S)
SEC = re.compile(r'(<section class="ss wrap conseils">|<div class="ss beige"><div class="wrap">)(<h2>(.*?)</h2>)(.*?)(?=</section>|</div></div>)', re.S)

TRAIL = re.compile(r"</ul>\s*<p>((?:(?!</p>).)*)</p>\s*$", re.S)
def phrases(p):
    return re.split(r"(?<=\.)\s+(?![^<]*>)", p.strip())
def garanties(corps, n, noms=()):
    """Paragraphe final « Strictement casher. ... » : une phrase par ligne, avec mini-dessin. Le texte reste identique (spans seulement)."""
    m = TRAIL.search(corps)
    if not m or len(phrases(m.group(1))) != n: return corps
    ph = phrases(m.group(1)); out = []
    for i, t in enumerate(ph):
        if i == 0: out.append(f'<span class="dk-g dk-g-tete">{t}</span>'); continue
        name = noms[i - 1] if i - 1 < len(noms) else ("file-text" if "<a " in t else ("badge-check" if i == 1 else "flame"))
        out.append(f'<span class="dk-g dk-g-ligne"><img class="dk dk-gico" src="/img/des/{name}.webp" alt="" width="96" height="96" loading="lazy">{t}</span>')
    return corps[:m.start()] + '</ul><p class="dk-garanties">' + " ".join(out) + "</p>" + corps[m.end():]

def plan(en, page_dir=""):
    """Depuis la page anglaise : pour chaque section texte, la liste des pictos par li, l'illustration du h2, le type."""
    hero = (re.search(r'img/illus/(?:w/)?([a-z-]+)\.(?:png|webp)', en) or [None, ""])[1]
    P = []
    for m in SEC.finditer(en):
        h2, corps = txt(m.group(3)), m.group(4)
        u = UL.search(corps); lis = LI.findall(u.group(1)) if u else []
        suite = bool(lis) and all(re.fullmatch(r"\s*<a [^>]+>.*?</a>\s*", x, re.S) for x in lis)
        vigs = []
        for x in (lis if suite else []):  # un picto par tuile, jamais deux fois le meme dans la liste
            t = txt(x); c = [n for pat, n in LIENS if re.search(pat, t)] + ["mountain-snow", "book-open", "map-pin", "footprints", "landmark", "info"]
            vigs.append(next(n for n in c if n not in vigs))
        icos = []; liens = []; used = set(); gnoms = []
        gm0 = TRAIL.search(corps)
        if lis and not suite and gm0 and txt(gm0.group(1)).startswith("strictly kosher"):  # les dessins des garanties comptent dans la section
            for i, t in enumerate(phrases(gm0.group(1))[1:], 1):
                gnoms.append(unique("file-text" if "<a " in t else ("badge-check" if i == 1 else "flame"), used))
        for x in lis:
            g = re.findall(r"</a>([^<]*)(?=<a )", x)
            liens.append(len(re.findall(r"<a ", x)) >= 3 and len(g) == len(re.findall(r"<a ", x)) - 1 and all(len(t) <= 8 for t in g))
            b = re.match(r"\s*<b>(.*?)</b>", x, re.S)
            icos.append(unique(choisir(txt(b.group(1)) if b else "", txt(x)), used))
        il = next((n for pat, n in H2ILLUS if re.search(pat, h2) and n != hero), "") if (lis and not suite) else ""
        ps = re.findall(r'<p>(.*?)</p>', corps, re.S)
        recit = (not lis) and len(ps) >= 2 and bool(re.fullmatch(r'(\s*<p>.*?</p>\s*)+', corps, re.S))
        gm = TRAIL.search(corps)
        gar = len(phrases(gm.group(1))) if (lis and not suite and gm and txt(gm.group(1)).startswith("strictly kosher")) else 0
        P.append(dict(garant=gar, gnoms=gnoms, nb=len(lis), recit=recit, np=len(ps), plier=recit and sum(len(txt(x)) for x in ps) > 450, rico=(lambda n: "book-open" if n == "check" else n)(choisir(h2, "")), liens=liens, boite=(not lis and bool(re.fullmatch(r"\s*<p>.*?</p>\s*", corps, re.S)) and corps.count("<p") == 1 and len(txt(corps)) <= 700), icos=icos, suite=suite, vigs=vigs, illus=il, note=choisir(h2, txt(corps)) if not lis else ""))
    m = re.search(r'<p class="intro-fiche">(.*?)</p>', en, re.S)
    return P, bool(m and len(txt(m.group(1))) > 320)

VUES = set()
def vignette(href, page_dir):
    """Vignette d'une page liee : sa premiere photo, sinon l'illustration de son hero. Jamais deux fois la meme dans une liste."""
    from PIL import Image, ImageOps
    cible = os.path.normpath(os.path.join(page_dir, href.split("#")[0], "index.html"))
    try: t = strip(rd(cible))
    except OSError: t = ""
    c = re.findall(r'img/((?:stock/|c-)[\w-]+\.jpe?g|illus/(?:w/)?[a-z-]+\.(?:png|webp))', t.split("<main", 1)[-1]) or ["illus/flat-jewish-lyon.png"]
    c = [re.sub(r"^illus/w/([a-z-]+)\.webp$", r"illus/\1.png", x) for x in c]   # 21/10 : _images_legeres.py pointe les illustrations sur illus/w/*.webp, les originaux PNG restent la source
    photos = []  # les photos des pages ne collent pas toujours au sujet (traboule sur la page ski) : on prend le dessin du hero
    c = [x for x in c if x.startswith("illus")] or ["illus/flat-jewish-lyon.png"]
    src = (photos or c)[0]
    nom = re.sub(r"[^a-z0-9]+", "-", src.rsplit(".", 1)[0]); d = f"img/v/{nom}.webp"
    if not os.path.exists(d):
        os.makedirs("img/v", exist_ok=True)
        im = Image.open("img/" + src).convert("RGB") if not src.endswith("png") else Image.open("img/" + src).convert("RGBA")
        ImageOps.fit(im, (160, 160)).save(d, "WEBP", quality=80)
    return "/" + d

def decorer(h, plan_en, page_dir, lang):
    P, replier = plan_en
    n = [0]
    def sec(m):
        i = n[0]; n[0] += 1
        p = P[i] if i < len(P) else dict(nb=-1, recit=False, np=0, plier=False, rico="info", boite=False, icos=[], suite=False, vigs=[], illus="", note="check")
        ouv, h2, corps = m.group(1), m.group(2), m.group(4)
        u = UL.search(corps)
        if u and p.get("nb") != len(LI.findall(u.group(1))): return m.group(0)  # copie traduite qui a diverge : on ne touche pas
        if not u:  # section a paragraphes seuls : note avec picto
            if p.get("recit") and corps.count("<p>") == p["np"]:  # recit : un fil, un paragraphe par pastille, la suite repliee sur mobile
                o2 = ouv.replace('conseils"', 'conseils dk-recit"').replace('"ss beige"', '"ss beige dk-recit"')
                c2 = corps.replace("<p>", "<p>" + ico(p["rico"], "dk dk-ico dk-ico-recit"), 1)
                if p["plier"]:
                    c2 = c2.replace("</p>", "</p>" + f'<button class="dk dk-plus dk-plus-recit" type="button" aria-expanded="false" onclick="this.parentElement.classList.add(\'dk-ouvert\');this.remove()">{MORE[lang]}</button>', 1)
                return o2 + h2 + c2
            if not p.get("boite"): return m.group(0)
            if corps.count("<p>") != 1: return m.group(0)
            return ouv.replace('conseils"', 'conseils dk-note"').replace('"ss beige"', '"ss beige dk-note"') + h2 + corps.replace("<p>", "<p>" + ico(p["note"] or "info", "dk dk-ico dk-ico-note"), 1)
        k = [0]
        def li(x):
            j = k[0]; k[0] += 1; c = x.group(1)
            c = re.sub(r'^(<b>[^<]*</b>),\s*(\w)', lambda q: q.group(1) + ' ' + q.group(2).upper(), c)   # titre de carte suivi de « , on the lake » : la virgule ouvrait la ligne (15/10)
            if p["suite"]:
                v = p["vigs"][j] if j < len(p.get("vigs", [])) else "book-open"
                return f'<li>{ico(v, "dk dk-ico dk-vigico")}{c}{ico("arrow-right", "dk dk-fleche")}</li>'
            name = p["icos"][j] if j < len(p["icos"]) else "check"
            nb = len(re.findall(r"<a ", c))
            if j < len(p.get("liens", [])) and p["liens"][j] and len(re.findall(r"</a>[^<]*(?=<a )", c)) == nb - 1:
                c = re.sub(r"(</a>)([^<]*)(?=<a )", r'\1<span class="dk-sep">\2</span>', c)
                c = re.sub(r"(</a>)([^<]+)$", lambda q: q.group(1) + '<span class="dk-sep dk-suite-txt">' + q.group(2) + "</span>", c)
                return f'<li class="dk-liens">{ico(name)}{c}</li>'
            return ('<li class="dk-lien1">' if nb else '<li>') + ico(name) + c + '</li>'
        nli = len(LI.findall(u.group(1)))
        corps2 = corps[:u.start()] + "<ul>" + LI.sub(li, u.group(1)) + "</ul>" + corps[u.end():]
        if p["suite"]: cls = "dk-suite"
        else:
            multi = len(re.findall(r"<a ", u.group(1))) >= 3
            cls = "dk-cartes" + (" dk-rail" if nli >= 4 and not multi else "")
        corps2 = corps2.replace("<ul>", f'<ul class="{cls}">', 1)
        if p.get("garant"): corps2 = garanties(corps2, p["garant"], p.get("gnoms", ()))
        if p["illus"]:
            h2 = h2.replace("<h2>", f'<h2 class="dk-h2"><img class="dk dk-h2img" src="{'/img/picto-hassid-vert.svg' if page_dir in HASSID_PAGES else '/img/illus/v/' + p['illus'] + '.webp'}" alt="" width="120" height="120" loading="lazy">', 1)
        return ouv + h2 + corps2
    h = SEC.sub(sec, h)
    # bande de preuves (accueil, tours)
    def preuves(m):
        k = [0]
        def li(x):
            j = k[0]; k[0] += 1
            return "<li>" + ico(PREUVES[j % len(PREUVES)]) + x.group(1) + "</li>"
        return m.group(1).replace('class="preuves"', 'class="preuves dk-preuves"') + LI.sub(li, m.group(2)) + m.group(3)
    h = re.sub(r'(<section class="preuves">\s*<ul>)(.*?)(</ul>)', preuves, h, flags=re.S)
    # puces du hero : coche
    h = re.sub(r'<ul class="chips">(.*?)</ul>', lambda m: '<ul class="chips dk-chips">' + LI.sub(lambda x: "<li>" + ico("check", "dk dk-coche") + x.group(1) + "</li>", m.group(1)) + "</ul>", h, flags=re.S)
    # intro longue : repliee sur mobile, bouton pour tout lire (le texte reste entier dans le HTML)
    m = re.search(r'<p class="intro-fiche">(.*?)</p>', h, re.S)
    if m and replier:
        h = h.replace(m.group(0), m.group(0).replace('class="intro-fiche"', 'class="intro-fiche dk-intro"') +
            f'<button class="dk dk-plus" type="button" aria-expanded="false" onclick="this.previousElementSibling.classList.add(\'dk-ouvert\');this.remove()">{MORE[lang]}</button>', 1)
    return h

def cibles(only):
    en = [p.replace("\\", "/") for p in glob.glob("**/index.html", recursive=True)]
    en = [p for p in en if not p.startswith("_") and p.split("/")[0] not in LANGS]
    if only: en = [p for p in en if os.path.dirname(p) in only or (p == "index.html" and "home" in only)]
    return en

def empreinte(h):
    """Ce que Google lit : texte visible, titres, liens, title/description, JSON-LD."""
    b = re.sub(r"<(script|style)[^>]*>.*?</\1>", lambda m: m.group(0) if "ld+json" in m.group(0) else "", h, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", re.sub(r'<script type="application/ld\+json">.*?</script>', "", b, flags=re.S)))).strip()
    return dict(texte=t, hn=re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", re.sub(r'<img class="dk[^>]*>', "", h), re.S), liens=re.findall(r'<a [^>]*href="([^"]+)"', h),
                meta=re.findall(r"<title>.*?</title>|<meta name=\"description\"[^>]*>|<link rel=\"canonical\"[^>]*>", h),
                ld=re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_strip, check = "--strip" in sys.argv, "--check" in sys.argv
    if not do_strip and not check: sprite(); dessins(); DES.update(os.path.basename(f)[:-5] for f in glob.glob("img/des/*.webp"))
    nb = ecarts = 0
    for p in cibles(args):
        d = os.path.dirname(p)
        en_nu = strip(rd(p)); P = plan(en_nu, d)
        for lang, path in [("en", p)] + [(l, f"{l}/{p}") for l in LANGS]:
            if not os.path.exists(path): continue
            brut = rd(path); nu = strip(brut)
            neuf = nu if do_strip else decorer(nu, P, d, lang)
            if check:
                a, b = empreinte(nu), empreinte(neuf)
                a["texte"], b["texte"] = re.sub(r"\s+", "", a["texte"]), re.sub(r"\s+", "", b["texte"])
                b["texte"] = b["texte"].replace(re.sub(r"\s+", "", MORE[lang]), "", 1) if "dk-plus" in neuf else b["texte"]
                for k in a:
                    if a[k] != b[k]: ecarts += 1; print("ECART", path, k)
            elif neuf != brut: wr(path, neuf)
            nb += 1
    print(("verifie" if check else "retire" if do_strip else "decore"), nb, "fichiers", f"- {ecarts} ecart(s)" if check else "")
