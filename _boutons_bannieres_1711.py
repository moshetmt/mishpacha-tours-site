# -*- coding: utf-8 -*-
"""Un bouton dans chaque bannière (Moshé, 17/11 : « il n'y a pas de bouton sur les bannières des fiches visite, de Lyon »).
Relevé : 192 bannières sans bouton (92 pages Lyon, 80 stations, 20 fiches visite) ; les 84 autres en ont un.

    python _boutons_bannieres_1711.py

 - fiche visite : le bouton WhatsApp de sa carte de prix ;
 - page Lyon : le bouton WhatsApp déjà présent sous la bannière ;
 - station : le bouton « Personnaliser mon séjour » de l'en-tête (formulaire).
Idempotent (marqueur BTN-1711). Le style vient du bloc BN-0511 (.btn-hero)."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FAM = {"hero", "ac-hero", "lv-hero-station", "lead-hero3", "lv-hero-photo"}
sans_svg = lambda t: re.sub(r"<svg.*?</svg>", "", t, flags=re.S).strip()
n = {"visite": 0, "lyon": 0, "station": 0}; rates = []
for f in sorted(glob.glob("**/index.html", recursive=True)):
    s = open(f, encoding="utf-8").read()
    i = s.find("<main")
    if i < 0 or "BTN-1711" in s: continue
    m = re.compile(r'<section class="([^"]*)"[^>]*>').search(s, i)
    if not m or m.start() - i > 400 or not (FAM & set(m.group(1).split())): continue
    k = s.find("</section>", m.end()); hero = s[m.end():k]
    if "btn-hero" in hero or "<form" in hero or "<button" in hero: continue
    cls = m.group(1).split()
    if "bn-fiche" in cls:
        a = re.search(r'<a class="btn-noir large" href="([^"]+)"[^>]*>(.*?)</a>', s, re.S); type_ = "visite"
    elif "lv-hero-photo" in cls:
        a = re.search(r'<p class="cta-hero"><a class="btn-noir" href="([^"]+)"[^>]*>(.*?)</a>', s, re.S); type_ = "lyon"
    else:
        a = re.search(r'<a class="nav-cta" href="([^"]+)"[^>]*>(.*?)</a>', s, re.S); type_ = "station"
    j = hero.rfind("</h1>")
    if not a or j < 0: rates.append(f); continue
    ext = ' rel="noopener"' if a.group(1).startswith("http") else ""
    bouton = f'<!--BTN-1711--><a class="btn-hero" href="{a.group(1)}"{ext}>{sans_svg(a.group(2))}</a>'
    hero = hero[:j + 5] + bouton + hero[j + 5:]
    open(f, "w", encoding="utf-8").write(s[:m.end()] + hero + s[k:]); n[type_] += 1
print("boutons ajoutés :", n, "| non traitées :", rates[:8])
