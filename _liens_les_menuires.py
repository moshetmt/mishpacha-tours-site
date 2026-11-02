# -*- coding: utf-8 -*-
"""02/11 : liens entrants vers la page station /kosher-les-menuires/ (créée par _station_les_menuires.py).
1. Pied de toutes les pages, liste « Resorts » : Les Ménuires après Val Thorens (même libellé latin dans les 4 langues,
   comme les autres stations du pied).
2. « Nearby resorts » de Val Thorens et de Courchevel (4 langues) : Les Ménuires en premier, ancre « chalet casher ».
Idempotent.   python _liens_les_menuires.py [--dry]   (depuis site-v5/)"""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
S = "kosher-les-menuires"
assert os.path.exists(f"{S}/index.html"), "page station absente : lancer _station_les_menuires.py"
ANCRE = {"": "Kosher chalet in Les Ménuires", "fr/": "Chalet casher aux Ménuires", "es/": "Chalet kosher en Les Ménuires",
         "he/": "צ'אלה כשרה בלה מנואר"}

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    if not DRY: io.open(p, "w", encoding="utf-8", newline="").write(s)

# 1. pied
n = 0
for p in glob.glob("**/index.html", recursive=True) + ["_gabarit.html"]:
    if p.startswith(("_brouillons", "_candidats")) or not os.path.exists(p): continue
    s = rd(p)
    m = re.search(r'(<details class="pied-stations">.*?</details>)', s, re.S)
    if not m or f'/{S}/"' in m.group(1): continue
    bloc = re.sub(r'(<a href="(/(?:fr/|es/|he/)?)kosher-val-thorens/">Val Thorens</a><br>)',
                  lambda x: x.group(1) + f'<a href="{x.group(2)}{S}/">Les Ménuires</a><br>', m.group(1), count=1)
    if bloc != m.group(1): wr(p, s[:m.start()] + bloc + s[m.end():]); n += 1
print(f"pied : {n} page(s)")

# 2. stations voisines
n = 0
for l, ancre in ANCRE.items():
    for voisine, modele in (("kosher-val-thorens", "kosher-courchevel"), ("kosher-courchevel", "kosher-val-thorens")):
        p = f"{l}{voisine}/index.html"; s = rd(p)
        m = re.search(r'<section[^>]*id="voisines".*?</section>', s, re.S)
        if not m or f"{S}/" in m.group(0): continue
        li = re.search(r'<li>(?:(?!</li>).)*?href="\.\./' + modele + r'/">.*?</li>', m.group(0), re.S)
        assert li, p
        neuf = re.sub(r'href="\.\./' + modele + r'/">[^<]*</a>', f'href="../{S}/">{ancre}</a>', li.group(0))
        i = m.start() + m.group(0).index("<li>")
        wr(p, s[:i] + neuf + s[i:]); n += 1
print(f"stations voisines : {n} page(s)")
print("(dry)" if DRY else "fait")

# 3. /alps/ (4 langues) : pastille « Les Ménuires » après Val Thorens (Moshé 02/11)
n = 0
for l, nom in (("", "Les Ménuires"), ("fr/", "Les Ménuires"), ("es/", "Les Ménuires"), ("he/", "לה מנואר")):
    p = f"{l}alps/index.html"; s = rd(p)
    m = re.search(r'<ul class="kwp-pastilles">.*?</ul>', s, re.S)
    if not m or f"{S}/" in m.group(0): continue
    ul = re.sub(r'(<li><a href="((?:\.\./|/(?:fr/|es/|he/)?))kosher-val-thorens/">[^<]*</a></li>)',
                lambda x: x.group(1) + f'<li><a href="{x.group(2)}{S}/">{nom}</a></li>', m.group(0), count=1)
    if ul != m.group(0): wr(p, s[:m.start()] + ul + s[m.end():]); n += 1
print(f"/alps/ : {n} page(s)")
