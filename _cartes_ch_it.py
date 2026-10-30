# -*- coding: utf-8 -*-
"""Carte des 6 stations suisses et italiennes (19/10, audit mobile : « On the map » vide). _build_guide.py ajoutait « , France »
à l'adresse pour la géolocaliser, donc aucune carte n'était rendue (corrigé dans _build_guide.py, coordonnées dans img/geo.json).
Ici on pose le cadre de carte et Leaflet dans les pages existantes, 4 langues, sans régénérer. Idempotent."""
import glob, html, io, json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from _build_guide import LEAFLET, geocode
import importlib.util
SLUGS = ("kosher-st-moritz", "kosher-zermatt", "kosher-crans-montana", "kosher-verbier", "kosher-cervinia", "kosher-courmayeur", "kosher-cortina")
LANGS = ("", "fr/", "es/", "he/")

def points(slug):
    spec = importlib.util.spec_from_file_location(slug, f"_pages/{slug}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for sec in m.PAGE["sections"]:
        if isinstance(sec, dict) and sec.get("type") == "map":
            return [{"n": n, "a": a, "ll": geocode(a)} for n, a in sec["points"]]
    return []

n = 0
for slug in SLUGS:
    pts = [p for p in points(slug) if p["ll"]]
    if not pts: print("sans coordonnées :", slug); continue
    div = f'<div class="carte-osm" data-points="{html.escape(json.dumps(pts, ensure_ascii=False), quote=True)}" style="height:380px"></div>'
    for l in LANGS:
        p = f"{l}{slug}/index.html"
        s = io.open(p, encoding="utf-8", newline="").read(); o = s
        if 'class="carte-osm"' not in s:
            s = s.replace('<p class="carte-note">', div + '<p class="carte-note">', 1)
        if "leaflet.min.js" not in s:
            i = s.find('<script src="/js/anim.js"')
            if i < 0: i = s.find("</body>")
            s = s[:i] + LEAFLET + "\n" + s[i:]
        if s != o: io.open(p, "w", encoding="utf-8", newline="").write(s); n += 1
print("_cartes_ch_it :", n, "page(s) modifiée(s)")
