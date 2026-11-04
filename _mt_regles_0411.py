# -*- coding: utf-8 -*-
"""Règles de Moshé du 04/11 après-midi reportées sur le design v2 (HTML déjà passé par _mt_alpes / _mt_lyon). Idempotent.
 - classes `bande-pierre` et `pierre` renommées `bande-filet` et `filet` (plus aucune bande grise : blanc entre deux filets) ;
 - pages station, hub chalets et hubs Alpes : la section des cartes chalet (`kwp`) reçoit `kwp-noir` (une seule par page, hors accueil et hors fiches)."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
n_cl = n_noir = 0
for f in glob.glob("**/*.html", recursive=True):
    t = open(f, encoding="utf-8").read(); o = t
    if "MT-ALPES" not in t and "MT-LYON" not in t:
        continue
    def fix(m):
        toks = ["bande-filet" if c == "bande-pierre" else "filet" if c == "pierre" else c for c in m.group(1).split()]
        return 'class="' + " ".join(toks) + '"'
    t = re.sub(r'class="([^"]*\b(?:bande-)?pierre\b[^"]*)"', fix, t)
    b = re.search(r'<body[^>]*class="([^"]*)"', t)
    if b and re.search(r"\bmt-(station|hub|hubalps)\b", b.group(1)) and "kwp-noir" not in t:
        def noir(m):
            return m.group(0) if "kwp-accueil" in m.group(1).split() else '<section class="' + m.group(1) + ' kwp-noir"'
        t = re.sub(r'<section class="([^"]*\bkwp\b[^"]*)"', noir, t, count=1)
    if t != o:
        n_cl += o.count("pierre") != t.count("pierre"); n_noir += ("kwp-noir" in t and "kwp-noir" not in o)
        open(f, "w", encoding="utf-8", newline="").write(t)
print("pages avec classes renommées :", n_cl, "· pages passées en kwp-noir :", n_noir)
