# -*- coding: utf-8 -*-
"""Corrections d'hébreu du 15/11/2026 (relecture Opus, hors lot), ciblées, idempotentes.
Remplace dans les sources (.py) ET dans les sorties (html, md, json, xml, txt) de site-v5 : chaque remplacement est une
phrase exacte, jamais un mot isolé hors contexte, sauf קומותיים (fautif partout).
  A. קומותיים -> קומתיים (lits superposés, duel de קומה)
  B. מטבח נפרד -> מטבח סגור (Mont d'Or, une cuisine fermée) ; neutre à Neige Éternelle (fiche contradictoire)
  C. תחת השלג -> המושלגת (alt de Mont d'Or, copié sur l'accueil et les hubs)
Lancer depuis site-v5 : python _hebreu_1511.py   (ajouter --a-blanc pour compter sans écrire)"""
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
A_BLANC = "--a-blanc" in sys.argv

PAIRES = [
    ("A", "קומותיים", "קומתיים"),
    ("B1", "פינת אוכל עם שולחן גדול, ומטבח נפרד.", "פינת אוכל עם שולחן גדול, ומטבח סגור."),
    ("B2", "בחלון בולט ושולחן אוכל ל-15 אורחים, עם מטבח נפרד עם אי מרכזי ומרפסת",
           "בחלון בולט, שולחן אוכל ל-15 אורחים, מטבח עם אי מרכזי ומרפסת"),
    ("C1", "צ'אלה מון ד'אור בקורשבל 1850 תחת השלג", "צ'אלה מון ד'אור המושלגת בקורשבל 1850"),
    ("C2", 'alt=f"צ\'אלה {HB} בקורשבל 1850 תחת השלג"', 'alt=f"צ\'אלה {HB} המושלגת בקורשבל 1850"'),
]
EXT = {".py", ".html", ".md", ".json", ".xml", ".txt", ".js", ".csv"}

totaux = {k: 0 for k, _, _ in PAIRES}
touches = []
for p in sorted(ICI.rglob("*")):
    if not p.is_file() or p.suffix not in EXT or p.name == Path(__file__).name:
        continue
    if "node_modules" in p.parts or ".git" in p.parts or ".vercel" in p.parts:
        continue
    try:
        t = p.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        continue
    neuf, fait = t, {}
    for k, avant, apres in PAIRES:
        n = neuf.count(avant)
        if n:
            neuf = neuf.replace(avant, apres)
            fait[k] = n
            totaux[k] += n
    if fait:
        touches.append((p.relative_to(ICI).as_posix(), fait))
        if not A_BLANC:
            p.write_bytes(neuf.encode("utf-8"))
for f, d in touches:
    print(f, d)
print("TOTAUX", totaux, "fichiers", len(touches), "(à blanc)" if A_BLANC else "")
