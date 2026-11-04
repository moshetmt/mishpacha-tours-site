"""Pages Lyon, formulaire et lecture du système de design v2 : pose les classes et restructure le <main>.
Idempotent (marqueur <!--MT-LYON-->). Se lance APRÈS _mt_socle.py.
Usage : python _mt_lyon.py [--racine DOSSIER] [pages...]   (pages relatives à la racine, par défaut tout le périmètre)
Aucun texte supprimé ; SEO, JSON-LD, name/id, lang/dir, ancres intacts. Aucun libellé nouveau (compteurs en CSS)."""
import re, sys, pathlib, collections

MARK = "<!--MT-LYON-->"
LANGS = ["", "fr/", "es/", "he/"]
ARTICLES = """chabad-lyon chrd-lyon grande-synagogue-lyon is-lyon-safe-for-jewish-visitors jewish-cemetery-lyon jewish-history-lyon
jewish-lyon-guide jewish-lyon-itinerary-2-days jewish-travel-lyon-faq kosher-restaurants-lyon kosher-shabbat-meals-catering-lyon lyon-weather
maison-izieu montluc-prison-lyon rue-juiverie-lyon shabbat-in-lyon synagogues-lyon things-to-do-in-lyon where-to-stay-lyon-jewish-travellers
mikveh-lyon flights-to-lyon jewish-life-around-lyon lyon-gateway-to-the-alps-kosher""".split()
TOURS = "izieu jewish-lyon memory-chrd memory-montluc-neveh-shalom stopover".split()
PAGES = "about contact credits legal privacy terms merci".split()


def perimetre():
    out = []
    for l in LANGS:
        out += [f"{l}jewish-lyon-tours/index.html", f"{l}plan-your-trip/index.html", f"{l}404.html"]
        out += [f"{l}tours/{t}/index.html" for t in TOURS]
        out += [f"{l}{a}/index.html" for a in ARTICLES + PAGES]
    return out


def type_de(rel, main):
    r = re.sub(r"^(fr|es|he)/", "", rel)
    if r == "plan-your-trip/index.html": return "form"
    if r == "jewish-lyon-tours/index.html": return "visite"
    if r.startswith("tours/"): return "tour"
    if r.split("/")[0] in ARTICLES and "lv-hero-photo" in main: return "art"
    if r == "404.html" or r.split("/")[0] in PAGES: return "page"
    return None


def ltr(txt):
    """chiffres, montants et heures en dir=ltr (pages hébreu)."""
    pat = re.compile(r"[+\-−]?\d[\d.,   ]*\d?\s?€|€\s?\d[\d.,]*|\b\d{1,2}[:h]\d{2}\b")
    return pat.sub(lambda m: f'<span dir="ltr">{m.group(0).strip()}</span>' + (" " if m.group(0).endswith(" ") else ""), txt)


def traiter(html, rel, stats):
    m = re.search(r"<main\b[^>]*>.*?</main>", html, re.S)
    if not m or MARK in m.group(0): return None
    main = m.group(0)
    t = type_de(rel, main)
    if not t: return None
    ouv = re.match(r"<main\b[^>]*>", main).group(0)
    corps = main[len(ouv):]
    n = stats[t]

    # tarifs (visite) et inclus (tour) : l'unique bande pierre de la page
    if t == "visite":
        corps, k = re.subn(r'(<section class="[^"]*prix-table[^"]*)(">\s*<h2.*?</h2>\s*)<ul>', r'\1 pierre\2<ul class="prix">', corps, flags=re.S)
        n["tarifs_en_liste_de_prix"] += k
        # le chercheur quitte le héros : il devient une section sous la photo
        f = re.search(r'<form class="chercheur".*?</form>', corps, re.S)
        h = re.search(r'<section class="hero"', corps)
        if f and h:
            corps = corps.replace(f.group(0), "", 1)
            fin = corps.index("</section>", h.start()) + len("</section>")
            corps = corps[:fin] + f'\n<section class="ss wrap l-cherche">{f.group(0)}</section>' + corps[fin:]
            n["chercheur_sorti_du_heros"] += 1
    if t == "tour":
        corps, k = re.subn(r'<section class="ss( beige)?">(\s*<div class="wrap inclus">)', r'<section class="ss pierre">\2', corps)
        n["inclus_en_bande_pierre"] += k

    # titres longs : 24 px sur téléphone (4 lignes au plus)
    def h1(mm):
        txt = re.sub(r"<[^>]+>", "", re.split(r"<br|<i>", mm.group(2))[0]).strip()
        if len(txt) > 28:
            n["titres_longs_reduits"] += 1
            return f'<h1{mm.group(1)} class="long">{mm.group(2)}</h1>'
        return mm.group(0)
    corps = re.sub(r"<h1((?:(?!class)[^>])*)>(.*?)</h1>", h1, corps, count=1, flags=re.S)

    # un seul fond teinté : beige et clair-2 disparaissent
    def classes(mm):
        toks = mm.group(1).split()
        new = [x for x in toks if x not in ("beige", "clair-2")]
        if len(new) != len(toks): n["fonds_teintes_retires"] += 1
        return 'class="' + " ".join(new) + '"'
    corps = re.sub(r'class="([^"]*)"', classes, corps)

    # offres Lyon : juste avant le contact (#book)
    o = re.search(r"<!-- OFFRES-LYON -->.*?<!-- /OFFRES-LYON -->\n?", corps, re.S)
    z = re.search(r'<div class="ticket-zone"', corps)
    if o and z:
        bloc = o.group(0)
        avant = corps[:o.start()] + corps[o.end():]
        z2 = re.search(r'<div class="ticket-zone"', avant)
        nouveau = avant[:z2.start()] + bloc + "\n" + avant[z2.start():]
        if nouveau != corps:
            corps = nouveau
            n["offres_deplacees_avant_le_contact"] += 1

    # articles : l'encadré « visiter » (points pratiques) en accordéon
    if t == "art":
        def acc(mm):
            ouv_s, inner = mm.group(1), mm.group(2)
            h2 = re.match(r"\s*(<h2\b.*?</h2>)(.*)$", inner, re.S)
            if not h2 or "dk-cartes" not in inner or "dk-suite" in inner: return mm.group(0)
            reste = h2.group(2)
            hors_liste = re.sub(r"<ul\b.*?</ul>", "", reste, flags=re.S)
            if len(re.findall(r"<p\b", hors_liste)) > 2: return mm.group(0)
            n["encadres_visiter_en_accordeon"] += 1
            ouv_s = ouv_s.replace('class="', 'class="l-acc ', 1)
            return f'{ouv_s}<details class="acc"><summary>{h2.group(1)}</summary>{reste}</details></section>'
        corps = re.sub(r'(<section class="[^"]*\bconseils\b[^"]*">)(.*?)</section>', acc, corps, flags=re.S)

    # styles en ligne retirés (hauteur de carte, marges du 404)
    def style(mm):
        if "--photo" in mm.group(1): return mm.group(0)
        n["styles_en_ligne_retires"] += 1
        return ""
    corps = re.sub(r'\sstyle="([^"]*)"', style, corps)

    # hébreu : montants, heures en dir=ltr
    if rel.startswith("he/"):
        parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", corps, flags=re.S)
        for i, p in enumerate(parts):
            if i % 2 == 0:
                new = re.sub(r">([^<>]+)<", lambda mm: ">" + ltr(mm.group(1)) + "<", p)
                n["nombres_en_ltr"] += len(re.findall(r'dir="ltr"', new)) - len(re.findall(r'dir="ltr"', p))
                parts[i] = new
        corps = "".join(parts)

    cl = {"visite": "xl", "tour": "xl", "art": "xl lr la", "page": "xl lr lp", "form": "lf"}[t]
    ouv2 = '<main class="%s">' % cl
    n["pages"] += 1
    return html[:m.start()] + ouv2 + MARK + corps + html[m.end():]


def main():
    a = sys.argv[1:]
    racine = pathlib.Path(__file__).parent
    if "--racine" in a:
        i = a.index("--racine"); racine = pathlib.Path(a[i + 1]); a = a[:i] + a[i + 2:]
    pages = a or perimetre()
    stats = collections.defaultdict(lambda: collections.Counter())
    vus = 0
    for rel in pages:
        p = racine / rel
        if not p.is_file(): continue
        vus += 1
        h = p.read_text(encoding="utf-8")
        r = traiter(h, rel.replace("\\", "/"), stats)
        if r and r != h: p.write_text(r, encoding="utf-8", newline="")
    print(f"_mt_lyon : {vus} pages lues dans {racine}")
    total = 0
    for t in ("visite", "tour", "art", "form", "page"):
        c = stats[t]
        total += c["pages"]
        print(f"  {t:7s} {c['pages']:3d} pages" + "".join(f" | {k} {v}" for k, v in sorted(c.items()) if k != "pages"))
    print(f"  total   {total} pages restructurées")


if __name__ == "__main__":
    main()
