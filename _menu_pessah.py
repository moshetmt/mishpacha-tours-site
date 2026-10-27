"""Ajoute « Pessah dans les Alpes » au menu plein écran (#panneau) et au menu ordinateur (nav.liens), avant « Été ».
Idempotent. python _menu_pessah.py"""
import re
from pathlib import Path

ICI = Path(__file__).parent
TXT = {
    "": ("Pesach in the Alps", "A chalet koshered for Pesach, Seder and meals"),
    "fr": ("Pessah dans les Alpes", "Chalet cachérisé pour Pessah, sedarim et repas"),
    "es": ("Pésaj en los Alpes", "Chalé kosherizado para Pésaj, Séder y comidas"),
    "he": ("פסח באלפים", "צ'אלה כשרה לפסח, ליל הסדר והארוחות"),
}

n = 0
for f in ICI.rglob("index.html"):
    rel = f.relative_to(ICI).parts
    if rel[0] in ("preview", "node_modules") or "sections-a-valider" in rel:
        continue
    lang = rel[0] if rel[0] in ("fr", "es", "he") else ""
    pref = f"/{lang}" if lang else ""
    h = f.read_text(encoding="utf-8")
    if 'id="panneau"' not in h:
        continue
    titre, desc = TXT[lang]
    lien = f"{pref}/kosher-pesach-french-alps/"
    ete = f'<a href="{pref}/summer-in-the-alps-jewish-families/">'
    o = h
    i = h.find('id="panneau"')
    j = h.find("</nav>", i)
    zone = h[i:j]
    if lien not in zone and ete in zone:
        zone = zone.replace(ete, f'<a href="{lien}">{titre}<small>{desc}</small></a> ' + ete, 1)
        h = h[:i] + zone + h[j:]
    m = re.search(r'<nav class="liens".*?</nav>', h, re.S)
    if m and lien not in m.group() and ete in m.group():
        nz = m.group().replace(ete, f'<a href="{lien}">{titre.split()[0]}</a>' + ete, 1)
        h = h[:m.start()] + nz + h[m.end():]
    if h != o:
        f.write_text(h, encoding="utf-8", newline="")
        n += 1
print("pages modifiées :", n)
