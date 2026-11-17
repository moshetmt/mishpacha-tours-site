# -*- coding: utf-8 -*-
"""Bannières à la même taille partout (Moshé, 16/11 : « les bannières ne sont jamais à la même taille, sur tel, tablette ou web »).
Mesure du 16/11 sur les 363 pages en ligne : E:/taches/bannieres-mish.csv.

    python _bannieres_1611.py

 - ordinateur : bannière à 100 % de l'écran sur toutes les pages « bn » (172 pages étaient à 85 %, accueil et stations à 100 %) ;
 - 20 fiches visite (/tours/…) : la photo devient la bannière plein écran avec le titre, comme le reste du site ;
   fil d'Ariane, texte et carte de prix passent dessous ;
 - fiches chalet : fil d'Ariane sur une ligne au téléphone (sur deux lignes il décalait la photo de 19 px sur 41 pages).
Idempotent (marqueur BN-1611)."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FICHE = re.compile(r'<section class="fiche-hero">\s*<div class="fiche-photo">(<img[^>]*>)(?:<span class="tag">(.*?)</span>)?</div>\s*'
                   r'<div class="fiche-texte">\s*(<p class="fil[^"]*">.*?</p>)\s*(<h1>.*?</h1>)', re.S)
n = 0
for f in sorted(glob.glob("**/index.html", recursive=True)):
    s = open(f, encoding="utf-8").read()
    if "BN-1611" in s: continue
    m = FICHE.search(s)
    if not m: continue
    img, tag, fil, h1 = m.groups()
    sur = f'<p class="lv-eyebrow">{tag}</p>' if tag else ""
    neuf = (f'<section class="hero">\n  {img}\n  <div class="hero-texte">{sur}{h1}</div>\n</section><!--BN-0511-->'
            f'<div class="bn-fil wrap">{fil}</div><!--BN-1611-->\n<section class="fiche-hero fiche-suite">\n  <div class="fiche-texte">')
    s = s[:m.start()] + neuf + s[m.end():]
    s = re.sub(r'<body class="', '<body class="bn ', s, count=1)
    open(f, "w", encoding="utf-8").write(s); n += 1
print("fiches visite passées au modèle bannière :", n)

P = "html body.lv.bn" + "".join(f":not(#b{i})" for i in range(1, 14))
H = f"{P} main>section:is(.lv-hero-station,.lead-hero3,.lv-hero-photo,.hero)"
LC = "html body.valora.lv" + "".join(f":not(#lv{i})" for i in range(1, 10)) + " main.lc .lc-fil"
CSS = f"""/* ===BN-1611=== bannières à la même taille partout (_bannieres_1611.py) */
@media (min-width:900px){{{H}{{height:100svh !important}}}}
{P} main>section.fiche-suite{{display:grid !important;grid-template-columns:1fr !important;grid-template-areas:none !important;gap:18px !important;max-width:1200px !important;margin:0 auto !important;padding:8px 20px 0 !important;align-items:start !important}}
{P} main>section.fiche-suite>:is(.fiche-texte,.fiche-carte){{grid-area:auto !important}}
{P} main>section.bn-fiche .hero-texte{{display:block !important}}
@media (min-width:900px){{{P} main>section.fiche-suite{{grid-template-columns:1.1fr .9fr !important;gap:24px 48px !important;padding:24px 56px 0 !important}}}}
@media (max-width:899.98px){{{LC}{{white-space:nowrap !important;overflow:hidden !important;text-overflow:ellipsis !important}}}}
/* ===/BN-1611=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===BN-1611===.*?/\* ===/BN-1611=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("css ok")
