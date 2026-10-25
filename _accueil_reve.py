# -*- coding: utf-8 -*-
"""Accueil « qui fait rêver » (Moshé, 25/10/2026, après l'audio de Mendel). Idempotent, 4 langues.
1. Héros : la table de Chabbat (Gemini n° 7) remplace la façade du chalet ; titre et chercheur inchangés.
2. Bande de 4 visuels sous le chercheur : table, chef, ski (Pexels 15318901), chiens de traîneau (Pexels 5619157, n° 7 ; le 36152836 montrait un dossard de course).
3. Cartes « How do you want to travel » : ski et repas prennent les visuels ski et chef.
Fichiers : img/reve/*.jpg (sources), img/h/reve-*-{640,960,1600,2400}.webp, img/cartes/reve-*.webp.
    python _accueil_reve.py   (depuis site-v5/)"""
import re
L = {"": dict(pref="", alt="A Shabbat table set in the chalet, with the Alps through the window", cap=["Shabbat at the chalet", "Your private chef", "On the slopes", "Dog sledding"]),
     "fr/": dict(pref="/", alt="Une table de Chabbat dressée dans le chalet, les Alpes par la fenêtre", cap=["Chabbat au chalet", "Votre chef privé", "Sur les pistes", "Chiens de traîneau"]),
     "es/": dict(pref="/", alt="Una mesa de Shabat puesta en el chalet, con los Alpes por la ventana", cap=["Shabat en el chalet", "Su chef privado", "En las pistas", "Trineo de perros"]),
     "he/": dict(pref="/", alt="שולחן שבת ערוך בצ'אלה, האלפים מבעד לחלון", cap=["שבת בצ'אלה", "השף הפרטי שלכם", "על המסלולים", "מזחלת כלבים"])}
ORDRE = ["table", "chef", "ski", "traineau"]
for lang, d in L.items():
    p = f"{lang}index.html"; h = open(p, encoding="utf-8").read(); P = d["pref"]
    # 1. héros
    hero = (f'<img src="{P}img/h/reve-table-960.webp" srcset="{P}img/h/reve-table-640.webp 640w, {P}img/h/reve-table-960.webp 960w, {P}img/h/reve-table-1600.webp 1600w, {P}img/h/reve-table-2400.webp 2400w" '
            f'sizes="100vw" alt="{d["alt"]}" width="2400" height="1610" fetchpriority="high">')
    h, n1 = re.subn(r'(<section class="hero ac-hero">\s*)<img [^>]*fetchpriority="high">', lambda m: m.group(1) + hero, h, count=1)
    # 2. bande (supprimée puis reposée, pour rester idempotent)
    h = re.sub(r'\s*<!--REVE--><section class="ss reve">.*?</section><!--/REVE-->', "", h, flags=re.S)
    figs = "".join(f'<figure><img src="{P}img/cartes/reve-{k}.webp" alt="" width="704" height="{"1056" if k == "traineau" else "470"}" loading="lazy" decoding="async"><figcaption>{c}</figcaption></figure>' for k, c in zip(ORDRE, d["cap"]))
    bande = f'<!--REVE--><section class="ss reve"><div class="wrap reve-grille">{figs}</div></section><!--/REVE-->'
    h, n2 = re.subn(r'(<!--/LUXE-HERO-->)', lambda m: m.group(1) + " " + bande, h, count=1)
    # 3. cartes voyager
    h, n3 = re.subn(r'(<a class="hub-carte" href="/(?:[a-z]{2}/)?kosher-ski-holidays-french-alps/"><div class="photo"><img src=")[^"]*(")', lambda m: f'{m.group(1)}{P}img/cartes/reve-ski.webp{m.group(2)}', h, count=1)
    h, n4 = re.subn(r'(<a class="hub-carte" href="/(?:[a-z]{2}/)?kosher-services-french-alps/"><div class="photo"><img src=")[^"]*(")', lambda m: f'{m.group(1)}{P}img/cartes/reve-chef.webp{m.group(2)}', h, count=1)
    open(p, "w", encoding="utf-8").write(h); print(p, "héros", n1, "bande", n2, "cartes", n3, n4)
css = open("styles.css", encoding="utf-8").read()
if ".reve-grille" not in css:
    css += """
/* Accueil « rêve » (25/10) : bande de 4 visuels sous le chercheur */
body:has(.ac-hero) .ss.reve{margin-top:0;padding:14px 0 0;background:var(--creme,#FAF6F0)}
.reve-grille{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.reve-grille figure{margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;background:#1C1B1F}
.reve-grille img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.reve-grille figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;color:#FFFAED;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;background:linear-gradient(180deg,rgba(20,19,22,0),rgba(20,19,22,.72))}
@media (min-width:900px){.reve-grille{grid-template-columns:repeat(4,1fr);gap:14px}.reve-grille figure{aspect-ratio:3/4}.reve-grille figcaption{font-size:13px;padding:44px 18px 16px}}
"""
    open("styles.css", "w", encoding="utf-8").write(css); print("css ajoutée")
