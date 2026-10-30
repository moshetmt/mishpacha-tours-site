# -*- coding: utf-8 -*-
"""30/10 : chaîne idempotente limitée aux pages Gstaad, Davos, « Ailleurs sur demande » (et Verbier avec --verbier, rebâtie
sans livraison), 4 langues. Depuis Valora, _contacts_bh_hebcal, _kit_wp et _galerie_chalets plantent en global : ici chaque
script tourne sur mes pages seulement (fonctions appelées directement, ou module lancé avec glob restreint), sauf _zones
(menus et pied : listes de stations) et _kit_wp.transition (script des transitions, liste HIVER) qui passent sur toutes les
pages, comme pour Verbier le 29/10. Ordre : zones, lead, Hebcal, lead_vers_plan, manifeste, mobile, décor, prefill, mesure,
animations, kit WP, carte CH/IT, sans nombre de chalets, lexique hébreu, couches Valora, index.md, images légères, JSON-LD i18n.
    py -3.14 _stations_suisse_chaine.py [--verbier]     (depuis site-v5, après _stations_suisse.py et _stations_suisse_photos.py)"""
import glob, io, os, re, runpy, subprocess, sys
from pathlib import Path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SLUGS = ["kosher-gstaad", "kosher-davos", "kosher-ski-anywhere"] + (["kosher-verbier"] if "--verbier" in sys.argv else [])
sys.argv = [sys.argv[0]]
LANGS = ("", "fr/", "es/", "he/")
MINE = [f"{l}{s}/index.html" for s in SLUGS for l in LANGS]
EXTRA = [f"{l}{s}/index.html" for s in ("jewish-lyon-guide", "alps", "kosher-ski-holidays-french-alps", "summer-in-the-alps-jewish-families") for l in LANGS]
EXTRA = [p for p in EXTRA if os.path.exists(p)]
PY = sys.executable
def norm(p): return p.replace("\\", "/")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
_orig = glob.glob
def restreint(fn, pages):
    """Exécute fn avec glob.glob limité à `pages` pour les motifs index.html / index.md (les autres motifs passent)."""
    ok = set(pages)
    def mien(pattern, **kw):
        out = _orig(pattern, **kw)
        return [p for p in out if norm(p) in ok] if ("index.html" in pattern or "index.md" in pattern) else out
    glob.glob = mien
    try: return fn()
    finally: glob.glob = _orig
def run(*args): print(">>", *args); subprocess.run([PY, *args], check=True)
def lang_de(p): return p.split("/")[0] if p.split("/")[0] in ("fr", "es", "he") else "en"
def slug_de(p): return p.split("/")[-2]

tous = [norm(p) for p in _orig("**/index.html", recursive=True) if not norm(p).startswith("_")]
# 1. menus, pied et listes de stations sur TOUTES les pages ; script des transitions (liste HIVER)
import _zones, _kit_wp
print("_zones :", sum(_zones.traiter(p) for p in tous), "pages")
run("_menu_pessah.py")   # _zones ne connaît pas l'entrée Pessah du menu (SEO semaine 1) : la reposer tout de suite
print("_kit_wp transition :", sum(_kit_wp.transition(Path(p)) for p in tous), "pages")
# 2. bannière 3 (lead) puis blocs Shabbat et Beth Habad (minyan seul : SANS_LIVRAISON)
import _lead as L, _contacts_bh_hebcal as BH
for p in MINE: print(p, "lead :", L.traiter(slug_de(p), lang_de(p)))
print("_contacts_bh_hebcal :", sum(BH.traiter(p) for p in MINE), "pages")
restreint(lambda: runpy.run_path("_lead_vers_plan.py", run_name="__main__"), MINE)
import _ton_expert as TE   # ton expert : bloc « Sources » et béquilles retirés (texte, meta, JSON-LD), comme sur Verbier le 29/10
n = 0
for p in MINE:
    s = rd(p); t = TE.process_ld(TE.process_meta(TE.process_html(s, lang_de(p), p), lang_de(p), p), lang_de(p), p)
    if t != s: wr(p, t); n += 1
print("_ton_expert :", n, "pages")
# 3. manifeste (chef seul), passe mobile, décor, préremplissage, mesure, animations
import _manifeste as M, _mobile_alpes as MA
print("_manifeste :", sum(M.page(p, lang_de(p), slug_de(p)) == 1 for p in MINE), "pages")
print("_mobile_alpes :", sum(MA.page(p) for p in MINE), "pages")
run("_decor.py", *SLUGS)
import _prefill as PF, _mesure as ME, _animations as AN
n = 0
for p in MINE:
    t = rd(p); t2 = PF.bas(t, lang_de(p))
    if t2 != t: wr(p, t2); n += 1
    n += PF.page(p, slug_de(p), lang_de(p), PF.CIBLES[slug_de(p)])
print("_prefill :", n)
print("_mesure :", sum(ME.page(p, False) for p in MINE), "pages")
n = 0
for p in MINE:
    s = rd(p)
    if AN.TAG not in s: wr(p, s.replace("</body>", AN.TAG + "</body>", 1)); n += 1
print("_animations :", n, "pages")
# 4. kit Winter Prestige (hiver, mini, pastilles), carte Leaflet CH/IT, règle « jamais le nombre de chalets », lexique hébreu
n = 0
for p in MINE: n += _kit_wp.page(slug_de(p), lang_de(p)); n += _kit_wp.transition(Path(p))
print("_kit_wp :", n)
run("_cartes_ch_it.py")
import _sans_nombre_chalets as SN, _retouches_30_10 as R
print("_sans_nombre_chalets :", sum(SN.passe(p) for p in MINE))
n = 0
for p in MINE:
    if not p.startswith("he/"): continue
    s = rd(p); t = s
    for a, b in R.HEBREU: t = t.replace(a, b)
    if t != s: wr(p, t); n += 1
print("lexique hébreu :", n, "pages")
# 5. couches Valora posées à la main le 28/10 sur les pages station (data-video, sans-wp, polices, vidéo, config), recopiées
#    depuis Crans-Montana, même langue (étape 13 de _stations_verbier.py) ; champ caché « lieu » du formulaire final
NOM_EN = {"kosher-gstaad": "Gstaad", "kosher-davos": "Davos", "kosher-verbier": "Verbier"}
for p in MINE:
    l = p[:3] if lang_de(p) != "en" else ""
    ref = rd(f"{l}kosher-crans-montana/index.html"); s = rd(p); o = s
    if 'data-video="stations"' not in s:
        s = s.replace('<section class="hero lead-hero3">', '<section class="hero lead-hero3" data-video="stations">', 1)
    mb = re.search(r'<body class="([^"]*)"', ref).group(1).split()
    b = re.search(r'<body(?: class="([^"]*)")?', s)
    cl = (b.group(1) or "").split()
    for c in mb:
        if c not in cl: cl.append(c)
    s = s[:b.start()] + f'<body class="{" ".join(cl)}"' + s[b.end():]
    for tag in re.findall(r'<link rel="preload" href="/fonts/[^"]+"[^>]*>|<link rel="stylesheet" href="/valora[^"]*\.css">', ref):
        if tag not in s: s = s.replace("</head>", tag + "\n</head>", 1)
    for js in ("/config.js", "/video-pages.js"):
        tag = re.search(r'<script src="' + re.escape(js) + r'"[^>]*></script>', ref)
        if tag and js not in s: s = s.replace("</body>", tag.group(0) + "\n</body>", 1)
    for tag in re.findall(r'<link rel="preload" href="/fonts/[^"]+"[^>]*>\n?', s):   # polices préchargées : mêmes que Crans-Montana
        if tag.strip() not in ref: s = s.replace(tag, "", 1)
    if 'name="lieu"' not in s and slug_de(p) in NOM_EN:
        s = s.replace('<input type="hidden" name="i" value="a">', f'<input type="hidden" name="i" value="a"><input type="hidden" name="lieu" value="{NOM_EN[slug_de(p)]}">', 1)
    if l:   # libellé du panneau WhatsApp du menu, traduit à la main sur les autres pages : repris de Crans-Montana
        lab = re.search(r'<a class="panneau-wa"[^>]*>(?:<svg>.*?</svg>)?([^<]*)</a>', ref, re.S)
        if lab: s = re.sub(r'(<a class="panneau-wa"[^>]*>(?:<svg>.*?</svg>)?)WhatsApp, same-day reply(</a>)', lambda k: k.group(1) + lab.group(1) + k.group(2), s, count=1, flags=re.S)
    if l == "he/" and slug_de(p) == "kosher-verbier":   # préfixes devant un nom qui commence par ו : la lettre se double
        s = re.sub(r"(?<![א-ת])([בלמ])ורבייה", r"\1וורבייה", s)
    if s != o: wr(p, s); print("valora", p)
import _alterne as AL   # alternance noir / blanc Valora (classes clair / clair-2 sur les sections), sans régénérer valora-alterne.css
n = 0
for p in MINE:
    s = rd(p); t = AL.traite(s)
    if t != s: wr(p, t); n += 1
print("_alterne :", n, "pages")
# 5 bis. liens WhatsApp génériques du menu et du bouton flottant (repris de Crans-Montana) : plus de « repas livrés » sur ces pages
import urllib.parse
LIVR = ("delivered meals, ", "repas livrés, ", "comidas entregadas, ", "ארוחות במשלוח, ", "ארוחות משלוח, ")
def sans_livraison(m):
    t = urllib.parse.unquote(m.group(2)); t2 = t
    for x in LIVR: t2 = t2.replace(x, "")
    if t2 == t: return m.group(0)
    q = urllib.parse.quote(t2, safe="/")
    if urllib.parse.quote(t, safe="/") != m.group(2): q = urllib.parse.quote(t2)   # même style d'encodage que l'original
    return m.group(1) + q
n = 0
for p in MINE:
    s = rd(p); t = re.sub(r'(wa\.me/\d+\?text=)([^"\']+)', sans_livraison, s)
    if t != s: wr(p, t); n += 1
print("WhatsApp sans livraison :", n, "pages")
# 6. index.md (Markdown servi aux agents), 404.html régénéré depuis la page merci, images légères (WebP) EN DERNIER
restreint(lambda: runpy.run_path("_agentic.py", run_name="__main__"), MINE + EXTRA)
import _images_legeres as IL
restreint(IL.main, MINE + EXTRA)
run("_build_i18n.py", "ld")
run("_build_i18n.py", "check")
print("chaîne terminée :", SLUGS)
