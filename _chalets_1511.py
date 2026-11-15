# -*- coding: utf-8 -*-
"""Chalets Cachemire (ch16, clé « e ») et Onyx (ch17, clé « f »), Courchevel 1850, 15/11/2026, au format LV-CHALET-V2 : même procédé que _chalets_1111.py
(qu'on importe et dont on réutilise les fonctions), mais ne pose QUE ces deux chalets : les pages de Crystal, Mont d'Or, Althéa et Neige Éternelle ne sont pas
refaites, on leur ajoute seulement le menu, la carte, la vignette « autres chalets », le sitemap. Idempotent (relancer retire puis repose ses propres ajouts).

RENOMMER un chalet (ex. Cachemire en Saphir) : changer `nom` et `nom_he` de CH["e"] dans _chalets_1111_noms.py (un seul endroit par chalet ; ni les URL ni les noms
de fichiers ne contiennent le nom), puis, depuis site-v5 :
    1. supprimer img/og/<slug>.jpg (l'image de partage ne se refait que si elle manque), puis  python _chalets_1511.py
    2. (apps-script/mendel)  python _chalets_1111_devis.py ; python build.py ; python catalogue_chalet.py ch16 en|fr|he  (ch17 pour Onyx)
    3. relire le texte hébreu du nouveau nom (nom_he) ; chercher l'ancien nom ailleurs dans le dépôt (grep) : rapports et ETAT.md seulement.
Photos : python _chalets_1111_photos.py e f (à lancer avant). Textes : _chalets_1111_textes.py (T["e"], T["f"]).
Lancer depuis site-v5 : python _chalets_1511.py [--page]   (--page : les pages seulement, sans rien brancher)"""
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
PAGE_SEUL = "--page" in sys.argv   # avant les imports (l'un d'eux réécrit sys.argv)
import _chalets_1111 as M   # noqa: E402

A, K = M.A, M.K
KEYS = ("e", "f")
SL = {k: M.CH[k]["slug"] for k in KEYS}
B_SLUG = M.CH["b"]["slug"]      # Mont d'Or, premier chalet de Courchevel 1850
D_SLUG = M.CH["d"]["slug"]      # dernier chalet posé le 11/11 (le menu et les listes se prolongent après lui)
DATE = "2026-11-15"
M.DATE = DATE


def IDX(slug):
    return [u for u, _ in K.CH_URL].index(slug)


# réglages propres à ces chalets dans les dictionnaires de _chalets_1111 (lus par tx(), regler(), carte()...)
M.VOISIN["e"] = (B_SLUG, IDX(B_SLUG))            # « À lire aussi » : Cachemire -> Mont d'Or
M.VOISIN["f"] = (SL["e"], IDX(SL["e"]))          # Onyx -> Cachemire (chaîne Onyx > Cachemire > Mont d'Or ; vignettes croisées sur toutes les fiches)
for _k in KEYS:
    M.STATION[_k] = M.STATION["b"]               # station proposée : Courchevel, comme Mont d'Or
    M.ZONE_HUB[_k] = "3v"                        # zone du hub : Les 3 Vallées, comme Mont d'Or
TOUS = tuple(M.ORDRE_CLES) + KEYS                # a, b, c, d, e, f


def chaine(bloc, lang, f_carte):
    """Pose les cartes (ou vignettes) de KEYS absentes d'un bloc, chacune après la précédente, la première après Mont d'Or."""
    ancre = B_SLUG
    for k in KEYS:
        if f'href="{A.pfx(lang)}/{SL[k]}/"' not in bloc:
            bloc = M.apres_carte(bloc, lang, ancre, f_carte(lang, k))
        ancre = SL[k]
    return bloc


def brancher():
    n = 0
    nav = {l: "".join(M.nav_item(l, k) for k in KEYS) for l in A.LANGS}
    for p in sorted(ICI.glob("**/index.html")):
        r = p.relative_to(ICI).as_posix()
        if r.startswith(("_", "preview/")):
            continue
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        slug = (r[len(lang) + 1:] if lang != "en" else r)[: -len("index.html")].strip("/")
        s = A.lire(p); o = s
        for k in KEYS:
            s = A.retirer(s, lang, SL[k])
        s = re.sub(rf'(<a class="nav-ch-v" href="{A.pfx(lang)}/{D_SLUG}/">.*?</a>)', lambda m: m.group(1) + nav[lang], s, count=1, flags=re.S)
        s = re.sub(rf'"{D_SLUG}"(?:,"{SL["e"]}")?(?:,"{SL["f"]}")?\]', f'"{D_SLUG}","{SL["e"]}","{SL["f"]}"]', s)   # liste des pages hiver
        for nom in ("accueil", "duo", "co", "hub"):
            m = re.search(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->", s, flags=re.S)
            if m and f'href="{A.pfx(lang)}/{B_SLUG}/"' in m.group(0):
                s = s[:m.start()] + chaine(m.group(0), lang, M.carte) + s[m.end():]
        m = re.search(r"<!--KIT-WP:mini-->.*?<!--/KIT-WP:mini-->", s, flags=re.S)
        if m and slug not in M.SLUGS and slug not in SL.values():
            bloc = m.group(0)
            for k in KEYS:
                bloc = re.sub(rf'<a class="kwp-v" href="{A.pfx(lang)}/{SL[k]}/">.*?</a>', "", bloc, flags=re.S)
            if f'<a class="kwp-v" href="{A.pfx(lang)}/{B_SLUG}/">' in bloc:
                i = bloc.find(f'<a class="kwp-v" href="{A.pfx(lang)}/{B_SLUG}/">')
                j = bloc.find("</a>", i) + len("</a>")
                bloc = bloc[:j] + "".join(M.vignette_mini(lang, k) for k in KEYS) + bloc[j:]
            s = s[:m.start()] + bloc + s[m.end():]
        n += A.ecrire(p, s, o)
    return n


def autres_fiches():
    """Vignettes de E et F à la fin de la rangée « autres chalets » de chaque fiche ; les fiches de E et F reçoivent aussi les autres chalets."""
    n = 0
    for p in sorted(list(ICI.glob("kosher-*chalet-*/index.html")) + list(ICI.glob("*/kosher-*chalet-*/index.html"))):
        r = p.relative_to(ICI).as_posix()
        lang = r.split("/")[0] if r.split("/")[0] in ("fr", "es", "he") else "en"
        s = A.lire(p); o = s
        if '<div class="lc-autres">' not in s:
            continue
        propre = next((k for k in KEYS if p.parent.name == SL[k]), None)
        cles = [k for k in TOUS if k != propre] if propre else list(KEYS)
        for k in (TOUS if propre else KEYS):
            s = re.sub(rf'<a class="lc-aut" href="{A.pfx(lang)}/{M.CH[k]["slug"]}/">.*?</a>', "", s, flags=re.S)
        i = s.find('<div class="lc-autres">'); j = s.find("</div>", i)
        s = s[:j] + "".join(M.carte_lc(lang, k) for k in cles) + s[j:]
        n += A.ecrire(p, s, o)
    return n


def sitemap_llms():
    p = ICI / "sitemap.xml"; s = A.lire(p); o = s
    ancre = D_SLUG
    for k in KEYS:
        if f"/{SL[k]}/" not in s:
            for lang in ("", "fr/", "es/", "he/"):
                m = re.search(rf"<url>(?:(?!</url>).)*?<loc>https://mishpachatours\.com/{lang}{ancre}/</loc>.*?</url>", s, flags=re.S)
                assert m, (lang, ancre, "absent du sitemap")
                bloc = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{DATE}</lastmod>", m.group(0).replace(ancre, SL[k]))
                s = s[:m.end()] + "\n" + bloc + s[m.end():]
        ancre = SL[k]
    n = A.ecrire(p, s, o)
    p = ICI / "llms.txt"; s = A.lire(p); o = s
    lignes = [l for l in s.split("\n") if not any(f"/{SL[k]}/" in l for k in KEYS)]
    i = next(q for q, l in enumerate(lignes) if f"/{D_SLUG}/" in l)
    c, f = M.CH["e"], M.CH["f"]
    lignes[i + 1:i + 1] = [
        f"- [Kosher Family Chalet {c['nom']}, Courchevel 1850]({A.BASE}/{SL['e']}/): private kosher family chalet in Courchevel 1850 near the slopes, up to 10 guests (eight in four double rooms, two in a children's room with bunk beds), five bedrooms, hammam, two fireplaces, lift; price on request.",
        f"- [Luxury Kosher Chalet {f['nom']}, Courchevel 1850]({A.BASE}/{SL['f']}/): private luxury kosher chalet in Courchevel 1850 at the foot of the slopes, up to 12 guests, six double bedrooms with bathrooms, heated indoor pool, hammam, cinema, gym and massage room; price on request."]
    return n + A.ecrire(p, "\n".join(lignes), o)


def controle():
    """Aucun mot interdit (union des deux listes interdits.txt), aucun reste du modèle dans les pages et index.md de E et F."""
    mots = []
    for f in (M.INTERDITS_FICHIER, next((ICI.parents[1] / "00-brief" / "references").glob("2026-11-15-chalets-courchevel")) / "interdits.txt"):
        mots += [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    # « 10 pers » (nom de l'annonce d'origine) attrapait « 10 personnes » : borne de mot
    mots = [r"10 pers\b" if m == "10 pers" else re.escape(m) for m in dict.fromkeys(mots)]
    rx = re.compile("(" + "|".join(mots) + ")", re.I)
    bad = 0
    for k in KEYS:
        slug = SL[k]
        for lang in A.LANGS:
            for f in ("index.html", "index.md"):
                p = ICI / (slug if lang == "en" else f"{lang}/{slug}") / f
                h = A.lire(p)
                corps = h[h.find("<main"):h.find("<!--KIT-WP:mini-->") if "<!--KIT-WP:mini-->" in h else h.find("<footer")] if f == "index.html" else h
                for mm in rx.finditer(corps):
                    print("INTERDIT", p.relative_to(ICI), mm.group(0)); bad += 1
                if f == "index.html":
                    corps = re.sub(r'<a class="lc-aut".*?</a>', "", corps, flags=re.S)
                    corps = re.sub(r"<nav .*?</nav>", "", corps, flags=re.S)
                    for r_ in M.RESTES_MODELE:
                        trouve = re.search(r"(?<![֐-׿])טין(?![֐-׿])", corps) if r_ == "טין" else (r_ in corps)
                        if trouve:
                            i = corps.find(r_)
                            print("RESTE", p.relative_to(ICI), r_, "::", corps[max(0, i - 60):i + 60].replace("\n", " ")); bad += 1
    print("controle : ", "OK" if not bad else f"{bad} point(s)")


if __name__ == "__main__":
    for k in KEYS:
        M.poser_pages(k)
    if not PAGE_SEUL:
        print("pages branchées :", brancher())
    ns = M.p3()
    for k in KEYS:
        M.regler(k)
        M.transformer(k, ns)
    if not PAGE_SEUL:
        print("autres fiches :", autres_fiches())
        print("sitemap + llms :", sitemap_llms())
    for k in KEYS:
        for lang in A.LANGS:
            A.index_md(ICI / (SL[k] if lang == "en" else f"{lang}/{SL[k]}") / "index.html")
    if not PAGE_SEUL:
        for k in KEYS:
            M.regler(k)
            M.rendre_og(k)
    controle()
