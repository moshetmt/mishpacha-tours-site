"""Socle du système de design v2 (DESIGN-SITE.md) : une feuille mt.css, body.mt, logos et icônes en trop retirés.
Usage : python _mt_socle.py [--racine <dossier>] [page.html ...]
Idempotent : le marqueur <!--MT-V2--> dans le head empêche tout second passage. Ne supprime ni texte, ni SEO, ni JSON-LD."""
import os, re, sys, pathlib, argparse, collections

ICI = pathlib.Path(__file__).parent
MARQUE = "<!--MT-V2-->"
MARQUE2 = "<!--MT-V2B-->"  # 2e passe (04/11, correctifs de la relecture) : lien d'évitement, 404, polices du premier écran
EVITE = {"en": "Skip to content", "fr": "Aller au contenu", "es": "Ir al contenido", "he": "דלג לתוכן"}
FEUILLES = {"styles.css", "lv.css", "lv-chalet.css", "valora-form.css", "wp-v3.css"}
EXCLUS = {"img", "fonts", "video", "catalogues", "css", "js", "apps-script", "espace"}
BOUTONS = {"btn", "lc-btn", "of-btn", "pill", "lc-noir", "lc-blanc", "lc-cta"}
EYEBROW = {"lv-eyebrow", "lc-ref", "lv-lc-eti", "lv-reassure"}


def attr(tag, nom):
    m = re.search(r'\b' + nom + r'="([^"]*)"', tag)
    return m.group(1) if m else ""


def garder_lien(tag, he):
    """False si le <link> du head doit disparaître."""
    href, rel = attr(tag, "href"), attr(tag, "rel")
    base = href.split("?")[0].rsplit("/", 1)[-1]
    if "fonts.googleapis.com" in href or "fonts.gstatic.com" in href:
        return False
    if rel == "stylesheet" and (base in FEUILLES or base.startswith("valora")):
        return False
    if rel == "preload" and re.search(r"/(playfair|fraunces|heebo-latin|heebo-hebrew)[^/]*\.woff2", "/" + href.lstrip("/")):
        return False
    return True


def icones(inner, c, cle):
    """Retire img et svg d'un bouton sauf le picto WhatsApp (qui reçoit data-wa). Garde tout si le bouton n'aurait plus de texte."""
    def svg(m):
        s = m.group(0)
        if 'href="#wa"' in s:
            return s if "data-wa" in s else s.replace("<svg", "<svg data-wa", 1)
        c[cle] += 1
        return ""
    def img(m):
        c[cle] += 1
        return ""
    avant = dict(c)
    neuf = re.sub(r"<svg\b[^>]*>.*?</svg>", svg, inner, flags=re.S)
    neuf = re.sub(r"<img\b[^>]*>", img, neuf)
    if not re.sub(r"<[^>]*>", "", neuf).strip() and re.sub(r"<[^>]*>", "", inner).strip() == "" and neuf != inner:
        c.clear(); c.update(avant); c["icone_seule_gardee"] += 1
        return inner
    return neuf


def boutons(mid, c):
    def f(m):
        tag, nom, cls = m.group(1), m.group(2), set(attr(m.group(1), "class").split())
        est = nom == "button" and "menu" not in cls
        est = est or any(x == "btn" or x.startswith("btn-") or x in BOUTONS for x in cls)
        if not est:
            return m.group(0)
        return tag + icones(m.group(3), c, "icone_bouton") + "</" + nom + ">"
    mid = re.sub(r"(<(a|button)\b[^>]*>)(.*?)</\2>", f, mid, flags=re.S)
    def cta(m):
        return m.group(1) + re.sub(r"(<a\b[^>]*>)(.*?)</a>", lambda a: a.group(1) + icones(a.group(2), c, "icone_bouton") + "</a>", m.group(2), flags=re.S) + "</p>"
    return re.sub(r'(<p\b[^>]*class="[^"]*\bcta-hero\b[^"]*"[^>]*>)(.*?)</p>', cta, mid, flags=re.S)


def classe(tag_open, ajout):
    if re.search(r'\bclass="', tag_open):
        return re.sub(r'class="([^"]*)"', lambda m: 'class="' + ajout + " " + m.group(1) + '"', tag_open, count=1)
    return tag_open[:-1] + ' class="' + ajout + '">'


def traiter(html, c):
    ih = html.find("</head>")
    ib = html.find("<body")
    if ih < 0 or ib < 0 or MARQUE in html:
        return None
    head, reste = html[:ih], html[ih:]
    he = re.search(r"<html[^>]*\blang=\"he\"", html[:400]) is not None
    # (a) head : feuilles, polices externes, blocs de charte
    n0 = len(head)
    for deb, fin, cle in (("<!--CHARTE-LV-->", "<!--/CHARTE-LV-->", "bloc_charte_lv"), ("<!--LV-CHALET-V1-css-->", "<!--/LV-CHALET-V1-css-->", "bloc_lv_chalet")):
        head, k = re.subn(re.escape(deb) + ".*?" + re.escape(fin), "", head, flags=re.S)
        c[cle] += k
    def lien(m):
        if garder_lien(m.group(0), he):
            return m.group(0)
        c["link_head"] += 1
        return ""
    head = re.sub(r"<link\b[^>]*>", lien, head)
    if c.get("_aucune_feuille") is None and "mt.css" in head:
        return None
    # (b) feuille unique + préchargement de la police du premier écran
    police = "mt-heebo-300-hebrew.woff2" if he else "mt-jost-300-latin.woff2"
    head += MARQUE + '<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/' + police + '"><link rel="stylesheet" href="/mt.css">\n'
    html = head + reste
    # (c) body.mt
    ib = html.find("<body")
    ie = html.find(">", ib) + 1
    html = html[:ib] + classe(html[ib:ie], "mt") + html[ie:]
    # région du contenu : entre l'en-tête et le pied
    ie = html.find(">", html.find("<body")) + 1
    r0 = html.find("</header>")
    r0 = r0 + 9 if r0 > 0 else ie
    r1 = html.rfind("<footer")
    if r1 < r0:
        r1 = len(html)
    av, mid, ap = html[:r0], html[r0:r1], html[r1:]
    # lockup co-marqué cliquable : lien vers l'accueil de la langue
    m = re.search(r'<html[^>]*lang="(\w+)"', html[:400])
    langue = m.group(1) if m else "en"
    accueil = "/" if langue == "en" else "/" + langue + "/"
    def lien_wp(m):
        c["lockup_lien"] += 1
        return '<a class="wp-lien" href="' + accueil + '" aria-label="Mishpacha Tours, Winter Prestige">' + m.group(0) + "</a>"
    av = re.sub(r'<div class="wp-entete">.*?</div>', lien_wp, av, flags=re.S)
    # (d) logos en trop
    def retire(pat, cle, flags=re.S):
        nonlocal mid
        mid, k = re.subn(pat, "", mid, flags=flags)
        c[cle] += k
    retire(r'<div\b[^>]*class="[^"]*\bkwp-hero-wp(?:-tel)?\b[^"]*"[^>]*>.*?</div>', "logo_heros")
    retire(r'<div\b[^>]*class="[^"]*\bkwp-bandeau\b[^"]*"[^>]*>.*?</div>', "banniere_wp")
    retire(r'<(div|section|aside|p)\b[^>]*>\s*(?:<img\b[^>]*/img/wp-[^>]*>\s*)+</\1>', "banniere_wp")
    retire(r'<svg\b[^>]*class="[^"]*\bkwp-seau\b[^"]*"[^>]*>.*?</svg>', "sceau_carte")
    retire(r'<span\b[^>]*class="[^"]*\bwp-brille\b[^"]*"[^>]*>.*?</span>', "wp_brille")
    retire(r'<img\b[^>]*src="[^"]*/img/wp-[^"/]*\.svg[^"]*"[^>]*>', "logo_wp_contenu")
    retire(r'<img\b[^>]*src="[^"]*picto-hassid[^"]*"[^>]*>', "picto_marque_contenu")
    # (e) icônes dans les boutons
    mid = boutons(mid, c)
    # (f) suffixe « with Winter Prestige » du lieu
    mid, k = re.subn(r"\s*·\s*(?:with|con|avec|עם)\s+Winter Prestige(?=\s*<)", "", mid)
    c["suffixe_wp"] += k
    # (g) classes lib et acc
    def eyebrow(m):
        cls = set(attr(m.group(0), "class").split())
        if cls & EYEBROW and "lib" not in cls:
            c["classe_lib"] += 1
            return classe(m.group(0), "lib")
        return m.group(0)
    mid = re.sub(r"<(?:p|span|div)\b[^>]*class=\"[^\"]*\"[^>]*>", eyebrow, mid)
    def det(m):
        if "acc" in attr(m.group(0), "class").split():
            return m.group(0)
        c["classe_acc"] += 1
        return classe(m.group(0), "acc")
    mid = re.sub(r"<details\b[^>]*>", det, mid)
    return av + mid + ap


def passe2(html, c):
    """Lien d'évitement en premier enfant du body (id="contenu" sur main), ancien bandeau .strip retiré, polices 400 et 500 préchargées."""
    if MARQUE not in html or MARQUE2 in html:
        return None
    m = re.search(r'<html[^>]*lang="(\w+)"', html[:400])
    langue = m.group(1) if m else "en"
    html, k = re.subn(r'<div class="strip">.*?</div>\s*', "", html, count=1, flags=re.S)
    c["bandeau_strip_retire"] += k
    html, k = re.subn(r"<main(?=[\s>])(?![^>]*\sid=)", '<main id="contenu"', html, count=1)
    ib = html.find("<body")
    ie = html.find(">", ib) + 1
    if k:
        html = html[:ie] + '<a class="evite" href="#contenu">' + EVITE.get(langue, EVITE["en"]) + "</a>" + html[ie:]
        c["lien_evitement"] += 1
    # barre transparente dès le premier rendu : la classe que le JS posait après coup (et qui faisait sauter la page, CLS 0,114) est posée dans le HTML
    hero = re.search(r'class="[^"]*\b(?:ac-hero|lv-hero-photo)\b', html) or re.search(r'<main\b[^>]*>\s*(?:<!--.*?-->\s*)*<section\b[^>]*class="(?![^"]*lead-hero3-illus)[^"]*\bhero\b', html, flags=re.S)
    if hero:
        ib = html.find("<body")
        ie = html.find(">", ib) + 1
        html = html[:ib] + classe(html[ib:ie], "lv-transp") + html[ie:]
        c["barre_transparente_dans_le_html"] += 1
    polices = ["mt-heebo-400-hebrew.woff2"] if langue == "he" else ["mt-jost-400-latin.woff2", "mt-jost-500-latin.woff2"]
    pre = "".join('<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/' + f + '">' for f in polices)
    c["polices_prechargees"] += len(polices)
    return html.replace(MARQUE, MARQUE + MARQUE2 + pre, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=str(ICI))
    ap.add_argument("pages", nargs="*")
    a = ap.parse_args()
    racine = pathlib.Path(a.racine).resolve()
    if a.pages:
        pages = [pathlib.Path(p) if pathlib.Path(p).is_absolute() else racine / p for p in a.pages]
    else:
        pages = [racine / "404.html"]
        for d, sous, fich in os.walk(racine):
            sous[:] = [s for s in sous if not s.startswith("_") and s not in EXCLUS]
            if "index.html" in fich:
                pages.append(pathlib.Path(d) / "index.html")
        pages = [p for p in pages if p.exists()]
    c = collections.Counter()
    touchees = ignorees = 0
    for p in sorted(set(pages)):
        t = p.read_bytes().decode("utf-8")
        if not re.search(r'<link\b[^>]*href="[^"]*(?:styles|lv|valora)[a-z-]*\.css', t) and MARQUE not in t:
            ignorees += 1
            continue
        n = passe2(t, c) if MARQUE in t else traiter(t, c)
        if n is None:
            ignorees += 1
            continue
        p.write_bytes(n.encode("utf-8"))
        touchees += 1
    print(f"pages touchées : {touchees}, laissées telles quelles : {ignorees}")
    for k, v in sorted(c.items()):
        print(f"  {k:<22} {v}")


main()
