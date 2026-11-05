# -*- coding: utf-8 -*-
"""Fiche du chalet de Tignes (ch9, « Étoile Polaire ») au format des fiches chalet actuelles (charte LV, fiche produit), 05/11/2026.
Remplace _chalet_tignes.py comme générateur de page : les textes, la carte et le menu viennent toujours de ce module, mais la page
est posée par clonage de la fiche Val Thorens ACTUELLE (tête, en-tête, pied et formulaire courants) avec le corps de la fiche d'avant
la phase 3 (a8e477b^, la source que _charte_lv_p3_chalets.py sait transformer), puis passée à la transformation de la phase 3 et
aux retouches des 04/11 (flocon WP, bouton catalogue, tailles de photos, flocon du formulaire). Contrôle du procédé : la même chaîne
appliquée à Val Thorens redonne la fiche en ligne, aux retouches du 04/11 près.

La chaîne idempotente globale est cassée : ce script ne lance ni _zones, ni _kit_wp, ni _galerie_chalets, ni _contacts_bh_hebcal.
Idempotent : relancer réécrit les 4 pages et ne duplique rien ailleurs (menu, cartes, bandes, sitemap, llms.txt).
Lancer depuis site-v5 : python _chalet_tignes_lv.py [--page]   (--page : les 4 pages seulement, sans rien brancher)"""
import io
import pathlib
import re
import subprocess
import sys

PAGE_SEUL = "--page" in sys.argv
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import _chalet_tignes as T   # noqa: E402  (textes, moteur réglé sur Tignes, carte, menu, bandes ; importe _chalet_aigle_royal comme A)

A, K, G = T.A, T.K, T.G
LANGS, SLUG, NOM, NOM_HE, pfx = T.LANGS, T.SLUG, T.NOM, T.NOM_HE, T.pfx
MODELE = A.MODELE
SRC_AVANT_P3 = "a8e477b^"            # dernière version de la fiche Val Thorens avant la transformation de la phase 3
CAT = "etoile-polaire"               # clé du catalogue (PDF catalogues/etoile-polaire-*), paramètre ?catalogue=
DATE = "2026-11-05"
CTA = {"en": "Request the catalogue", "fr": "Demander le catalogue", "es": "Solicitar el catálogo", "he": "לקבלת הקטלוג"}


def git_show(chemin):
    pref = subprocess.run(["git", "-C", str(ICI), "rev-parse", "--show-prefix"], capture_output=True, text=True, check=True).stdout.strip()
    r = subprocess.run(["git", "-C", str(ICI), "show", f"{SRC_AVANT_P3}:{pref}{chemin}"], capture_output=True, check=True)
    return r.stdout.decode("utf-8")


def p3():
    """Fonctions de la phase 3 (le script lance main() à l'import : on l'exécute sans cette dernière ligne)."""
    src = (ICI / "_charte_lv_p3_chalets.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
    ns = {"__file__": str(ICI / "_charte_lv_p3_chalets.py")}
    exec(compile(src, "_charte_lv_p3_chalets", "exec"), ns)
    return ns


class _IO:
    """Remplace io pour A.page() : la lecture de la fiche Val Thorens renvoie la source composée, le reste passe tel quel."""
    def __init__(self, composee):
        self.composee = composee

    def open(self, f, *a, **k):
        if str(f).replace("\\", "/") in self.composee:
            return io.StringIO(self.composee[str(f).replace("\\", "/")])
        return io.open(f, *a, **k)

    def __getattr__(self, n):
        return getattr(io, n)


def source_composee(lang):
    """Tête, en-tête et pied de la fiche Val Thorens actuelle + corps d'avant la phase 3."""
    p = (MODELE if lang == "en" else f"{lang}/{MODELE}") + "/index.html"
    cur = A.lire(ICI / p)
    old = git_show(p)
    i0, i1 = cur.find("<main"), cur.find("<footer")
    j0, j1 = old.find("<main>"), old.find("<footer")
    assert min(i0, i1, j0, j1) > 0, lang
    return str(ICI / p).replace("\\", "/"), cur[:i0] + old[j0:j1] + cur[i1:]


def poser_pages():
    """Étape 1 : les 4 pages au format d'avant la phase 3, tête courante, textes de Tignes."""
    T.regler()
    A.io = _IO(dict(source_composee(l) for l in LANGS))
    try:
        for lang in LANGS:
            dst = A.page(lang)
            T.sans_minyan_station(dst)
            print("page", dst.relative_to(ICI))
    finally:
        A.io = io


def retouches(s, lang):
    """Retouches du 04/11 que la phase 3 ne porte pas (_wp_fiches_v3.py, _retours_04_11.py), posées comme sur Val Thorens."""
    plan = f"{pfx(lang)}/plan-your-trip/?i=a&amp;catalogue={CAT}"
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
    fin = queue.find("</div>")   # fin de la section lc-photos : la 4e photo, si elle existe, suit la paire
    queue = queue[:fin].replace("(min-width:900px) 40vw", "(min-width:900px) 92vw") + queue[fin:]
    return s[:a] + tete.replace("(min-width:900px) 40vw", "(min-width:900px) 92vw") + duo + queue


def og(s):
    u = f"{A.BASE}/img/og/{SLUG}.jpg"
    return re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + u + m.group(2), s)


def transformer():
    """Étape 3 : phase 3 (fiche produit LV) sur les 4 pages, puis retouches du 04/11."""
    ns = p3()
    for lang in LANGS:
        dst = ICI / (SLUG if lang == "en" else f"{lang}/{SLUG}") / "index.html"
        s = A.lire(dst)
        if "<!--LV-CHALET-V2-->" in s:
            s_new = s
        else:
            s_new, n = ns["transforme"](s, SLUG)
            s_new = retouches(s_new, lang)
            s_new = photos_pleine_largeur(s_new)
            s_new = s_new.replace('<img class="lead-final-hassid" src="/img/picto-hassid-creme.svg" alt="" width="240" height="243"',
                                  '<img class="lead-final-hassid wp-fl-final" src="/img/wp-flocon-brosse-fonce.svg" alt="" width="240" height="240"')
            print("fiche LV", dst.relative_to(ICI), n, "photos")
        s_new = og(s_new)
        A.ecrire(dst, s_new, s)


def carte_lc(lang):
    """Vignette « autres chalets » des fiches actuelles (a.lc-aut), même découpe que la phase 3."""
    m = re.search(rf'<a class="kwp-v" href="{pfx(lang)}/{SLUG}/"><img src="([^"]+)"[^>]*><span><b>([^<]*)</b>', K.mini(lang, None))
    img, nom = m.group(1), A.H.unescape(m.group(2))
    nm, _, pl = nom.partition(" · ")
    return (f'<a class="lc-aut" href="{pfx(lang)}/{SLUG}/"><img src="{img}" alt="" width="336" height="224" loading="lazy">'
            f'<span class="lc-nom">{nm}</span><span class="lc-lieu">{pl}</span></a>')


def autres_fiches():
    """Vignette de Tignes à la fin de la rangée « autres chalets » des 32 fiches actuelles (4 langues) ; retirée puis reposée."""
    n = 0
    for p in sorted(list(ICI.glob("kosher-*chalet-*/index.html")) + list(ICI.glob("*/kosher-*chalet-*/index.html"))):
        r = p.relative_to(ICI).as_posix()
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        if p.parent.name == SLUG:
            continue
        s = A.lire(p); o = s
        s = re.sub(rf'<a class="lc-aut" href="{pfx(lang)}/{SLUG}/">.*?</a>', "", s, flags=re.S)
        i = s.find('<div class="lc-autres">')
        if i < 0:
            continue
        j = s.find("</div>", i)
        s = s[:j] + carte_lc(lang) + s[j:]
        n += A.ecrire(p, s, o)
    return n


def vignette_mini(lang):
    return re.search(rf'<a class="kwp-v" href="{pfx(lang)}/{SLUG}/">.*?</a>', K.mini(lang, None), flags=re.S).group(0)


def brancher():
    """Menu, liste hiver, cartes (accueil, hub, /alps/, ski) et bandes des stations. Comme T.brancher, mais les bandes « un chalet
    entier ? » ne sont pas régénérées (le texte de _zones.py a dérivé de celui des pages en ligne) : seule la vignette de Tignes
    y est ajoutée. Menu et cartes se posent en fin de liste (Tignes est le dernier chalet de CH_URL ; le menu en ligne ne suit pas l'ordre du hub)."""
    n = 0
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = (r[len(lang) + 1:] if lang != "en" else r)[: -len("index.html")].strip("/")
        s = A.lire(p); o = s
        s = A.retirer(s, lang, SLUG)
        if f'class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"' not in s:
            k = [u for u, _ in K.CH_URL].index(SLUG)
            b, d = K.NAV_CH[lang][2][k]
            nav = (f'<a class="nav-ch-v" href="{pfx(lang)}/{SLUG}/"><img src="{K.CH_URL[k][1]}" alt="" width="96" height="64" loading="lazy">'
                   f'<span><b>{A.H.escape(b, quote=False)}</b>{A.H.escape(d, quote=False)}</span></a>')
            s = re.sub(rf'(<a class="nav-ch-v" href="{pfx(lang)}/kosher-chalet-les-menuires/">.*?</a>)', lambda m: m.group(1) + nav, s, count=1, flags=re.S)
        if f'"{SLUG}"' not in s:
            s = s.replace('"kosher-chalet-courchevel-renard-argente"];', f'"kosher-chalet-courchevel-renard-argente","{SLUG}"];')
        for nom in ("accueil", "hub", "duo"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{pfx(lang)}/{SLUG}/"' not in m.group(0):
                bloc = m.group(0); j = bloc.rfind("</article>") + len("</article>")
                s = s[:m.start()] + bloc[:j] + T.carte(lang) + bloc[j:] + s[m.end():]
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug != SLUG and f'href="{pfx(lang)}/{SLUG}/"' not in m.group(0):
            bloc = m.group(0); j = bloc.find("</div>", bloc.find('class="kwp-mini-v'))
            s = s[:m.start()] + bloc[:j] + vignette_mini(lang) + bloc[j:] + s[m.end():]
        n += A.ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = A.lire(p); o = s
    if f"/{SLUG}/" not in s:
        for lang in ("", "fr/", "es/", "he/"):
            m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}kosher-chalet-courchevel-renard-argente/</loc>.*?</url>", s, flags=re.S)
            if m:
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{DATE}</lastmod>", m.group(0).replace("kosher-chalet-courchevel-renard-argente", SLUG))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
    n = A.ecrire(p, s, o)
    return n + T.sitemap_llms()


def rendre_og():
    """og:image 1200x630 de la fiche, même gabarit que les autres fiches (_og_lv.py), photo = héros de la page."""
    dest = ICI / "img" / "og" / f"{SLUG}.jpg"
    import tempfile
    import _og_lv as O
    from playwright.sync_api import sync_playwright
    ph = O.photo_fiche(A.lire(ICI / SLUG / "index.html"))
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        O.svg_brosses(tmp)
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": O.W, "height": O.H}, device_scale_factor=1)
        n = O.rendre_wp(pg, SLUG, ph, tmp, str(dest))
        b.close()
    t = ICI / "_og_lv_tmp.html"
    if t.exists():
        t.unlink()
    print("og", dest.relative_to(ICI), n, "octets")


if __name__ == "__main__":
    poser_pages()
    if not PAGE_SEUL:
        print("pages branchées :", brancher())
    transformer()
    if not PAGE_SEUL:
        print("autres fiches :", autres_fiches())
        print("sitemap + llms :", sitemap_llms())
    for lang in LANGS:
        A.index_md(ICI / (SLUG if lang == "en" else f"{lang}/{SLUG}") / "index.html")
    T.controle()
