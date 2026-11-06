# -*- coding: utf-8 -*-
"""05/11 : liens entrants vers la page station /kosher-avoriaz/ (créée par _station_avoriaz.py).
1. Pied de toutes les pages, liste « Resorts » : Avoriaz après Chamonix (même libellé latin dans les 4 langues).
2. « Nearby resorts » de Chamonix, Megève et Annecy (4 langues) : Avoriaz en premier.
3. /alps/ (4 langues) : pastille Avoriaz après Chamonix.
Ne touche ni /plan-your-trip/ ni les fichiers du formulaire. Idempotent.   python _liens_avoriaz.py [--dry]   (depuis site-v5/)"""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
S = "kosher-avoriaz"
assert os.path.exists(f"{S}/index.html"), "page station absente : lancer _station_avoriaz.py"
ANCRE = {"": "Kosher Avoriaz", "fr/": "Avoriaz casher", "es/": "Avoriaz kosher", "he/": "כשר באבוריאז"}
PASTILLE = {"": "Avoriaz", "fr/": "Avoriaz", "es/": "Avoriaz", "he/": "אבוריאז"}

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
    bloc = re.sub(r'(<a href="(/(?:fr/|es/|he/)?)kosher-chamonix/">Chamonix</a><br>)',
                  lambda x: x.group(1) + f'<a href="{x.group(2)}{S}/">Avoriaz</a><br>', m.group(1), count=1)
    if bloc != m.group(1): wr(p, s[:m.start()] + bloc + s[m.end():]); n += 1
print(f"pied : {n} page(s)")

# 2. stations voisines
n = 0
for l, ancre in ANCRE.items():
    for voisine in ("kosher-chamonix", "kosher-megeve", "kosher-annecy"):
        p = f"{l}{voisine}/index.html"; s = rd(p)
        m = re.search(r'<section[^>]*id="voisines".*?</section>', s, re.S)
        if not m or f"{S}/" in m.group(0): continue
        li = re.search(r'<li[^>]*>(?:(?!</li>).)*?href="\.\./kosher-[a-z-]+/">.*?</li>', m.group(0), re.S)
        assert li, p
        neuf = re.sub(r'href="\.\./kosher-[a-z-]+/">[^<]*</a>', f'href="../{S}/">{ancre}</a>', li.group(0), count=1)
        i = m.start() + m.group(0).index(li.group(0))
        wr(p, s[:i] + neuf + s[i:]); n += 1
print(f"stations voisines : {n} page(s)")

# 3. /alps/
n = 0
for l, nom in PASTILLE.items():
    p = f"{l}alps/index.html"; s = rd(p)
    m = re.search(r'<ul class="kwp-pastilles">.*?</ul>', s, re.S)
    if not m or f"{S}/" in m.group(0): continue
    ul = re.sub(r'(<li><a href="((?:\.\./|/(?:fr/|es/|he/)?))kosher-chamonix/">[^<]*</a></li>)',
                lambda x: x.group(1) + f'<li><a href="{x.group(2)}{S}/">{nom}</a></li>', m.group(0), count=1)
    if ul != m.group(0): wr(p, s[:m.start()] + ul + s[m.end():]); n += 1
print(f"/alps/ : {n} page(s)")
print("(dry)" if DRY else "fait")
