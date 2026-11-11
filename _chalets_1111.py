# -*- coding: utf-8 -*-
"""Deux chalets neufs du 11/11/2026 au format LV-CHALET-V2 : A = Saint-Gervais Mont-Blanc (ch12), B = Courchevel 1850 (ch13).
Même procédé que _chalet_tignes_lv.py (clone de la fiche Val Thorens ACTUELLE : tête, en-tête, pied et formulaire courants, corps d'avant
la phase 3, puis transformation de la phase 3 et retouches du 04/11), appliqué à deux chalets. Noms : _chalets_1111_noms.py
(provisoires, une constante par chalet) ; textes : _chalets_1111_textes.py ; photos : _chalets_1111_photos.py (à lancer avant).
La chaîne idempotente globale est cassée : ce script ne lance ni _zones, ni _kit_wp, ni _galerie_chalets, ni _contacts_bh_hebcal.
Idempotent : relancer réécrit les pages et ne duplique rien (menu, cartes, bandes, sitemap, llms.txt) ; l'image de partage n'est refaite
que si elle manque (Chromium n'est pas déterministe).
Lancer depuis site-v5 : python _chalets_1111.py [--page]   (--page : les 4+4 pages seulement, sans rien brancher)"""
import io
import pathlib
import re
import subprocess
import sys

PAGE_SEUL = "--page" in sys.argv
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import _chalet_aigle_royal as A   # noqa: E402  (page(), jsonld(), index_md(), webp(), K, G)
from _chalets_1111_noms import CH, ORDRE_CLES   # noqa: E402
import _chalets_1111_textes as TT   # noqa: E402

K, G = A.K, A.G
LANGS, pfx, MODELE = A.LANGS, A.pfx, A.MODELE
SRC_AVANT_P3 = "a8e477b^"
DATE = "2026-11-11"
CTA = {"en": "Request the catalogue", "fr": "Demander le catalogue", "es": "Solicitar el catálogo", "he": "לקבלת הקטלוג"}
PRIX = {"en": ("From €{%s_basse_vente} per week", "Price on request"), "fr": ("À partir de {%s_basse_vente} € la semaine", "Prix sur demande"),
        "es": ("Desde {%s_basse_vente} € por semana", "Precio a consultar"), "he": ("החל מ־<bdi dir='ltr'>{%s_basse_vente} €</bdi> לשבוע", "מחיר לפי בקשה")}
VOISIN = {"a": ("kosher-chalet-megeve", 3), "b": ("kosher-chalet-courchevel", 2)}   # chalet proposé dans « À lire aussi » et son rang dans le menu
STATION = {"a": [("kosher-val-thorens/", "kosher-chamonix/"), ("Val Thorens", "Chamonix"), ("בואל טורנס", "בשמוני"), ("ואל טורנס", "שמוני")],
           "b": [("kosher-val-thorens/", "kosher-courchevel/"), ("Val Thorens", "Courchevel"), ("בואל טורנס", "בקורשבל"), ("ואל טורנס", "קורשבל")]}
SLUGS = [CH[k]["slug"] for k in ORDRE_CLES]
DERNIER_AVANT = "kosher-chalet-tignes"   # les deux chalets se posent après lui (menu, hiver, cartes)


# ---------------------------------------------------------------- textes -> moteur
def tx(cle):
    c, out = CH[cle], {}
    for l in LANGS:
        t = TT.T[cle][l]
        nom = c["nom_he"] if l == "he" else c["nom"]
        vi, rang = VOISIN[cle]
        vt = K.NAV_CH[l][2][rang][0].replace(" · ", ", ")
        noms = ([("בל אטואל", nom), ("בואל טורנס", "ב" + c["lieu_he"]), ("ואל טורנס", c["lieu_he"]), ("מג'נבה", "מז'נבה")] if l == "he"
                else [("Chalet Belle Étoile", "Chalet " + nom), ("Belle Étoile", nom), ("Val Thorens", c["lieu"])])
        cuisine = TT.CUISINE_A[l] if cle == "a" else A.TX[l]["bref"][-1]
        out[l] = dict(title=t["title"], desc=t["desc"], ital=t["ital"], hero=t["hero"], intro=t["intro"],
                      bref=[t["loc"]] + t["bref"] + [cuisine], apres=t["apres"] + " " + TT.DISPO[l], shabbat=TT.SHABBAT[l], acces=TT.ACCES[l],
                      prix=(PRIX[l][0] % c["ch"], PRIX[l][1]), faq=[t["faq"][0], t["pistes"], t["faq"][1]], alt=t["alt"],
                      vt_lien=vt, voisin=vi, noms=noms, suite_noms=STATION[cle], web=t["web"], ld_desc=t["ld_desc"],
                      lieu_q=c["lieu_q"], svc=c["svc"])
    return out


def regler(cle):
    c = CH[cle]
    A.SLUG, A.GC = c["slug"], G.CHALETS[c["slug"]]
    A.HERO = A.GC["hero"]
    A.STEMS = A.ORDRE = [s for _, _, ss in A.GC["pieces"] for s in ss]
    A.TX = tx(cle)
    A.COORD_AR = c["coord"]
    A.DIM = {s: A.webp(s) for s in A.STEMS}


# ---------------------------------------------------------------- clonage (comme _chalet_tignes_lv.py)
def git_show(chemin):
    pref = subprocess.run(["git", "-C", str(ICI), "rev-parse", "--show-prefix"], capture_output=True, text=True, check=True).stdout.strip()
    r = subprocess.run(["git", "-C", str(ICI), "show", f"{SRC_AVANT_P3}:{pref}{chemin}"], capture_output=True, check=True)
    return r.stdout.decode("utf-8")


def p3():
    src = (ICI / "_charte_lv_p3_chalets.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
    ns = {"__file__": str(ICI / "_charte_lv_p3_chalets.py")}
    exec(compile(src, "_charte_lv_p3_chalets", "exec"), ns)
    return ns


class _IO:
    def __init__(self, composee):
        self.composee = composee

    def open(self, f, *a, **k):
        if str(f).replace("\\", "/") in self.composee:
            return io.StringIO(self.composee[str(f).replace("\\", "/")])
        return io.open(f, *a, **k)

    def __getattr__(self, n):
        return getattr(io, n)


def source_composee(lang):
    p = (MODELE if lang == "en" else f"{lang}/{MODELE}") + "/index.html"
    cur = A.lire(ICI / p)
    old = git_show(p)
    i0, i1 = cur.find("<main"), cur.find("<footer")
    j0, j1 = old.find("<main>"), old.find("<footer")
    assert min(i0, i1, j0, j1) > 0, lang
    return str(ICI / p).replace("\\", "/"), cur[:i0] + old[j0:j1] + cur[i1:]


def sans_minyan_station(dst):
    """A : pas de page station, aucun minyan de station promis (bloc « A minyan in the resort » retiré)."""
    s = A.lire(dst); o = s
    s = re.sub(r'<section class="clair ss wrap minyan-bh">.*?</section>', "", s, count=1, flags=re.S)
    A.ecrire(dst, s, o)


def poser_pages(cle):
    regler(cle)
    A.io = _IO(dict(source_composee(l) for l in LANGS))
    try:
        for lang in LANGS:
            dst = A.page(lang)
            if cle == "a":
                sans_minyan_station(dst)
            print("page", dst.relative_to(ICI))
    finally:
        A.io = io


def retouches(s, lang, cat):
    plan = f"{pfx(lang)}/plan-your-trip/?i=a&amp;catalogue={cat}"
    s = s.replace('id="lcColle" aria-hidden="true"><div>', 'id="lcColle" aria-hidden="true"><!--WP-V3:fiche--><img class="lc-wpfl" src="/img/wp-flocon-brosse-fonce.svg" alt="" width="26" height="26"><div>', 1)
    s, n1 = re.subn(r'<a class="lc-btn lc-noir lc-cta" id="lcCta" href="[^"]*">[^<]*</a>', f'<a class="lc-btn lc-noir lc-cta" id="lcCta" href="{plan}">{CTA[lang]}</a>', s, count=1)
    s, n2 = re.subn(r'<a class="lc-btn lc-noir lc-mini" href="[^"]*" tabindex="-1">[^<]*</a>', f'<a class="lc-btn lc-noir lc-mini" href="{plan}" tabindex="-1">{CTA[lang]}</a>', s, count=1)
    assert n1 == n2 == 1, (lang, n1, n2)
    return s


def photos_pleine_largeur(s):
    a = s.find('<div class="lc-photos">')
    if a < 0:
        return s
    b = s.find('<div class="lc-duo">', a); c = s.find("</div>", b) + 6
    tete, duo, queue = s[a:b], s[b:c], s[c:]
    fin = queue.find("</div>")
    queue = queue[:fin].replace("(min-width:900px) 40vw", "(min-width:900px) 92vw") + queue[fin:]
    return s[:a] + tete.replace("(min-width:900px) 40vw", "(min-width:900px) 92vw") + duo + queue


def og(s, slug):
    u = f"{A.BASE}/img/og/{slug}.jpg"
    return re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + u + m.group(2), s)


def transformer(cle, ns):
    c = CH[cle]
    for lang in LANGS:
        dst = ICI / (c["slug"] if lang == "en" else f"{lang}/{c['slug']}") / "index.html"
        s = A.lire(dst)
        if "<!--LV-CHALET-V2-->" in s:
            s_new = s
        else:
            s_new, n = ns["transforme"](s, c["slug"])
            s_new = retouches(s_new, lang, c["catalogue"])
            s_new = photos_pleine_largeur(s_new)
            s_new = s_new.replace('<img class="lead-final-hassid" src="/img/picto-hassid-creme.svg" alt="" width="240" height="243"',
                                  '<img class="lead-final-hassid wp-fl-final" src="/img/wp-flocon-brosse-fonce.svg" alt="" width="240" height="240"')
            print("fiche LV", dst.relative_to(ICI), n, "photos")
        s_new = og(s_new, c["slug"])
        A.ecrire(dst, s_new, s)


# ---------------------------------------------------------------- branchement
def carte(lang, cle):
    c = CH[cle]
    tpl, repli = PRIX[lang][0] % c["ch"], PRIX[lang][1]
    return K.carte(lang, c["cle"]).replace('<p class="kwp-dispo">', f'<p class="kwp-prix" data-prix-tpl="{A.attr_(tpl)}">{repli}</p><p class="kwp-dispo">', 1)


def apres_carte(bloc, lang, slug, html_neuf):
    """Pose html_neuf juste après la carte (article) qui pointe vers slug ; sinon en fin de bloc."""
    lien = f'href="{pfx(lang)}/{slug}/"'
    i = bloc.find(lien)
    while i >= 0 and bloc.rfind('<article class="kwp-carte', 0, i) < bloc.rfind("</article>", 0, i):
        i = bloc.find(lien, i + 1)
    j = (bloc.find("</article>", i) if i >= 0 else bloc.rfind("</article>") - len("</article>") + 1) + len("</article>")
    return bloc[:j] + html_neuf + bloc[j:]


def carte_dans_zone(bloc, zone, html_neuf):
    """Hub : la carte se pose à la fin de sa zone (data-zone), pas à la fin du bloc."""
    debut = re.compile(r'<div class="l3-zone(?: [^"]*)?" id="zone-')
    a = bloc.find(f'id="zone-{zone}"')
    assert a >= 0, zone
    suite = debut.search(bloc, a)
    fin_zone = suite.start() if suite else len(bloc)
    fin = bloc.rfind("</article>", a, fin_zone)
    assert fin > 0, zone
    fin += len("</article>")
    return bloc[:fin] + html_neuf + bloc[fin:]


H2_ME = {"en": ("Our chalets", "near Megève"), "fr": ("Nos chalets", "près de Megève"), "es": ("Nuestros chalets", "cerca de Megève"), "he": ("הצ'אלות שלנו", "ליד מג'ב")}
H2_CO = {"en": ("Our chalets", "in Courchevel"), "fr": ("Nos chalets", "à Courchevel"), "es": ("Nuestros chalets", "en Courchevel"), "he": ("הצ'אלות שלנו", "בקורשבל")}


def vignette_mini(lang, cle):
    slug = CH[cle]["slug"]
    return re.search(rf'<a class="kwp-v" href="{pfx(lang)}/{slug}/">.*?</a>', K.mini(lang, None), flags=re.S).group(0)


def nav_item(lang, cle):
    slug = CH[cle]["slug"]
    k = [u for u, _ in K.CH_URL].index(slug)
    b, d = K.NAV_CH[lang][2][k]
    return (f'<a class="nav-ch-v" href="{pfx(lang)}/{slug}/"><img src="{K.CH_URL[k][1]}" alt="" width="96" height="64" loading="lazy">'
            f'<span><b>{A.H.escape(b, quote=False)}</b>{A.H.escape(d, quote=False)}</span></a>')


def brancher():
    n = 0
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = (r[len(lang) + 1:] if lang != "en" else r)[: -len("index.html")].strip("/")
        s = A.lire(p); o = s
        for sl in SLUGS:
            s = A.retirer(s, lang, sl)
        # menu « Chalets » : après Tignes, A puis B
        nav = "".join(nav_item(lang, k) for k in ORDRE_CLES)
        s = re.sub(rf'(<a class="nav-ch-v" href="{pfx(lang)}/{DERNIER_AVANT}/">.*?</a>)', lambda m: m.group(1) + nav, s, count=1, flags=re.S)
        # liste des pages hiver (fondu entre chartes)
        for sl in SLUGS:
            if f'"{sl}"' not in s:
                s = s.replace(f'"{DERNIER_AVANT}"];', f'"{DERNIER_AVANT}","{sl}"];') if sl == SLUGS[0] else s.replace(f'"{SLUGS[0]}"];', f'"{SLUGS[0]}","{sl}"];')
        # cartes : accueil et /alps/ (« duo ») après Tignes ; hub par zone ; Courchevel (B) ; Megève (A)
        for nom in ("accueil", "duo"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{pfx(lang)}/{SLUGS[0]}/"' not in m.group(0):
                b = apres_carte(m.group(0), lang, DERNIER_AVANT, carte(lang, "a") + carte(lang, "b"))
                s = s[:m.start()] + b + s[m.end():]
        m = re.search(r"<!--KIT-WP:hub-->.*?<!--/KIT-WP:hub-->", s, flags=re.S)
        if m and f'href="{pfx(lang)}/{SLUGS[0]}/"' not in m.group(0):
            b = carte_dans_zone(m.group(0), "me", carte(lang, "a"))
            b = carte_dans_zone(b, "3v", carte(lang, "b"))
            s = s[:m.start()] + b + s[m.end():]
        m = re.search(r"<!--KIT-WP:co-->.*?<!--/KIT-WP:co-->", s, flags=re.S)
        if m and f'href="{pfx(lang)}/{CH["b"]["slug"]}/"' not in m.group(0):
            b = apres_carte(m.group(0), lang, "kosher-chalet-courchevel-renard-argente", carte(lang, "b"))
            b = re.sub(r"<h2>.*?</h2>", f"<h2>{H2_CO[lang][0]} <i>{H2_CO[lang][1]}</i></h2>", b, count=1, flags=re.S)
            s = s[:m.start()] + b + s[m.end():]
        m = re.search(r"<!--KIT-WP:me-->.*?<!--/KIT-WP:me-->", s, flags=re.S)
        if m and f'href="{pfx(lang)}/{CH["a"]["slug"]}/"' not in m.group(0):
            b = apres_carte(m.group(0), lang, "kosher-chalet-megeve", carte(lang, "a")).replace("kwp-cartes kwp-seule", "kwp-cartes")
            b = re.sub(r"<h2>.*?</h2>", f"<h2>{H2_ME[lang][0]} <i>{H2_ME[lang][1]}</i></h2>", b, count=1, flags=re.S)
            s = s[:m.start()] + b + s[m.end():]
        # bandes « chalets proches » : la vignette de A là où figure Megève, celle de B là où figure Courchevel (flocon doré)
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug not in SLUGS:
            bloc = m.group(0)
            for cle, voisin in (("a", "kosher-chalet-megeve"), ("b", "kosher-chalet-courchevel")):
                if f'href="{pfx(lang)}/{voisin}/"' in bloc and f'href="{pfx(lang)}/{CH[cle]["slug"]}/"' not in bloc:
                    j = bloc.find("</div>", bloc.find('class="kwp-mini-v'))
                    bloc = bloc[:j] + vignette_mini(lang, cle) + bloc[j:]
            s = s[:m.start()] + bloc + s[m.end():]
        n += A.ecrire(p, s, o)
    return n


def carte_lc(lang, cle):
    slug = CH[cle]["slug"]
    m = re.search(rf'<a class="kwp-v" href="{pfx(lang)}/{slug}/"><img src="([^"]+)"[^>]*><span><b>([^<]*)</b>', K.mini(lang, None))
    img, nom = m.group(1), A.H.unescape(m.group(2))
    nm, _, pl = nom.partition(" · ")
    return (f'<a class="lc-aut" href="{pfx(lang)}/{slug}/"><img src="{img}" alt="" width="336" height="224" loading="lazy">'
            f'<span class="lc-nom">{nm}</span><span class="lc-lieu">{pl}</span></a>')


def autres_fiches():
    """Vignettes de A et B à la fin de la rangée « autres chalets » de chaque fiche (la fiche de A ne reçoit que B, et inversement)."""
    n = 0
    for p in sorted(list(ICI.glob("kosher-*chalet-*/index.html")) + list(ICI.glob("*/kosher-*chalet-*/index.html"))):
        r = p.relative_to(ICI).as_posix()
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        s = A.lire(p); o = s
        i = s.find('<div class="lc-autres">')
        if i < 0:
            continue
        for sl in SLUGS:
            s = re.sub(rf'<a class="lc-aut" href="{pfx(lang)}/{sl}/">.*?</a>', "", s, flags=re.S)
        i = s.find('<div class="lc-autres">'); j = s.find("</div>", i)
        neuf = "".join(carte_lc(lang, k) for k in ORDRE_CLES if CH[k]["slug"] != p.parent.name)
        s = s[:j] + neuf + s[j:]
        n += A.ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = A.lire(p); o = s
    ancre = DERNIER_AVANT
    for sl in SLUGS:
        if f"/{sl}/" in s:
            continue
        for lang in ("", "fr/", "es/", "he/"):
            m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}{ancre}/</loc>.*?</url>", s, flags=re.S)
            if m:
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{DATE}</lastmod>", m.group(0).replace(ancre, sl))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
        ancre = sl
    n = A.ecrire(p, s, o)
    p = ICI / "llms.txt"; s = A.lire(p); o = s
    lignes = [l for l in s.split("\n") if not any(f"/{sl}/" in l for sl in SLUGS)]
    i = next(k for k, l in enumerate(lignes) if f"/{DERNIER_AVANT}/" in l)
    ajout = [f"- [Kosher Chalet {CH['a']['nom']}, Saint-Gervais Mont-Blanc]({A.BASE}/{SLUGS[0]}/): private kosher chalet in Saint-Gervais Mont-Blanc, up to 16 guests, eight bedrooms with bathrooms, indoor heated pool, sauna, cinema room, two kitchens; price on request.",
             f"- [Kosher Chalet {CH['b']['nom']}, Courchevel 1850]({A.BASE}/{SLUGS[1]}/): private kosher chalet in Courchevel 1850, up to 10 guests, five bedrooms, stone hot tub and hammam; price on request."]
    lignes[i + 1:i + 1] = ajout
    return n + A.ecrire(p, "\n".join(lignes), o)


def rendre_og(cle):
    """og:image 1200x630 (même gabarit que les autres fiches, _og_lv.py), seulement si elle manque (Chromium n'est pas déterministe)."""
    c = CH[cle]
    dest = ICI / "img" / "og" / f"{c['slug']}.jpg"
    if dest.exists():
        return
    import tempfile
    import _og_lv as O
    from playwright.sync_api import sync_playwright
    ph = O.photo_fiche(A.lire(ICI / c["slug"] / "index.html"))
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        O.svg_brosses(tmp)
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": O.W, "height": O.H}, device_scale_factor=1)
        nb = O.rendre_wp(pg, c["slug"], ph, tmp, str(dest))
        b.close()
    t = ICI / "_og_lv_tmp.html"
    if t.exists():
        t.unlink()
    print("og", dest.relative_to(ICI), nb, "octets")


INTERDITS_FICHIER = next((ICI.parents[1] / "00-brief" / "references").glob("2026-11-11-chalets-*")) / "interdits.txt"
RESTES_MODELE = ("Val Thorens", "Belle Étoile", "Tignes", "Étoile Polaire", "valthorens", "ואל טורנס", "בל אטואל", "טין", "אטואל פולר", "165 m", "ski aux pieds", "ski-in", "skis aux pieds")


def controle():
    """Aucun mot interdit (liste hors site), aucun reste du modèle (hors menu, bandes et pied) dans les pages et index.md des deux chalets."""
    mots = [l.strip() for l in INTERDITS_FICHIER.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    rx = re.compile(r"(" + "|".join(re.escape(m) for m in mots) + r")", re.I)
    for cle in ORDRE_CLES:
        c = CH[cle]
        for lang in LANGS:
            for f in ("index.html", "index.md"):
                p = ICI / (c["slug"] if lang == "en" else f"{lang}/{c['slug']}") / f
                h = A.lire(p)
                m = rx.search(h)
                assert not m, (p, m and m.group(0))
                if f == "index.html":
                    corps = h[h.find("<main"):h.find("<!--KIT-WP:mini-->") if "<!--KIT-WP:mini-->" in h else h.find("<footer")]
                    corps = re.sub(r'<a class="lc-aut".*?</a>', "", corps, flags=re.S)
                    corps = re.sub(r'<nav .*?</nav>', "", corps, flags=re.S)
                    for r_ in RESTES_MODELE:
                        trouve = re.search(r"(?<![֐-׿])טין(?![֐-׿])", corps) if r_ == "טין" else (r_ in corps)
                        if trouve:
                            i = corps.find(r_)
                            print("RESTE", p.relative_to(ICI), r_, "::", corps[max(0, i - 60):i + 60].replace("\n", " "))


if __name__ == "__main__":
    for cle in ORDRE_CLES:
        poser_pages(cle)
    if not PAGE_SEUL:
        print("pages branchées :", brancher())
    ns = p3()
    for cle in ORDRE_CLES:
        regler(cle)
        transformer(cle, ns)
    if not PAGE_SEUL:
        print("autres fiches :", autres_fiches())
        print("sitemap + llms :", sitemap_llms())
    for cle in ORDRE_CLES:
        for lang in LANGS:
            A.index_md(ICI / (CH[cle]["slug"] if lang == "en" else f"{lang}/{CH[cle]['slug']}") / "index.html")
    if not PAGE_SEUL:
        for cle in ORDRE_CLES:
            regler(cle)
            rendre_og(cle)
    controle()
