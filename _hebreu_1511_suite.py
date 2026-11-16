# -*- coding: utf-8 -*-
"""Corrections d'hébreu du 15/11/2026, suite (rapport 06-reports/2026-11-15-relecture-hebreu-suite.md), ciblées, idempotentes.
19 paires exactes (S1-S13 : תחת השלג, K1-K4 : קומותיים, M1-M2 : מטבח נפרד), appliquées à site-v5 et apps-script.
Exclus : _hebreu_1511.py et ce script (chaînes « avant » volontaires), apps-script/Mendel.gs (régénéré par mendel/build.py).
Lancer depuis site-v5 : python _hebreu_1511_suite.py   (ajouter --a-blanc pour compter sans écrire)"""
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINES = [ICI, ICI.parent / "apps-script"]
EXCLUS = {"_hebreu_1511.py", "_hebreu_1511_suite.py", "Mendel.gs"}
A_BLANC = "--a-blanc" in sys.argv

PAIRES = [
 ("S1", "צ'אלה רושברון בלה דז אלפ תחת השלג", "צ'אלה רושברון המושלגת בלה דז אלפ"),
 ("S2", "הצ'אלה בקורשבל תחת השלג", "הצ'אלה המושלגת בקורשבל"),
 ("S3", "צ'אלה בל אטואל בואל טורנס תחת השלג", "צ'אלה בל אטואל המושלגת בואל טורנס"),
 ("S4", "צ'אלה אגל רויאל בלה מנואר תחת השלג", "צ'אלה אגל רויאל המושלגת בלה מנואר"),
 ("S5", "צ'אלה אורור בוראל בקורשבל, הבריכה תחת השלג", "צ'אלה אורור בוראל בקורשבל, הבריכה בנוף מושלג"),
 ("S6", "צ'אלה רנאר ארז'נטה בקורשבל תחת השלג", "צ'אלה רנאר ארז'נטה המושלגת בקורשבל"),
 ("S7", "צ'אלה {_TG_HE} בטין תחת השלג", "צ'אלה {_TG_HE} המושלגת בטין"),
 ("S8", "צ'אלה אטואל פולר בטין תחת השלג", "צ'אלה אטואל פולר המושלגת בטין"),
 ("S9", "הצ'אלה תחת השלג, חמישים מטר מהמסלולים", "הצ'אלה המושלגת, חמישים מטר מהמסלולים"),
 ("S10", "הצ'אלה תחת השלג, מעל ואל טורנס", "הצ'אלה המושלגת, מעל ואל טורנס"),
 ("S11", 'f"{ro} בלה דז אלפ תחת השלג"', 'f"{ro} המושלגת בלה דז אלפ"'),
 ("S12", 'f"{be} בואל טורנס תחת השלג"', 'f"{be} המושלגת בואל טורנס"'),
 ("S13", "ג'קוזי חיצוני תחת השלג, סאונה עם מקלחת משלה", "ג'קוזי חיצוני בלב השלג, סאונה עם מקלחת משלה"),
 ("K1", "ומיטות קומותיים לשני ילדים", "ומיטות קומתיים לשני ילדים"),
 ("K2", "חדר ילדים ובו מיטות קומותיים", "חדר ילדים ובו מיטות קומתיים"),
 ("K3", "חדר ילדים צמוד ובו מיטות קומותיים", "חדר ילדים צמוד ובו מיטות קומתיים"),
 ("K4", "חדר ילדים צמוד עם מיטות קומותיים", "חדר ילדים צמוד עם מיטות קומתיים"),
 ("M1", "פינת אוכל עם שולחן גדול, ומטבח נפרד.", "פינת אוכל עם שולחן גדול, ומטבח סגור."),
 ("M2", "אח, פינת ספרייה בחלון בולט ושולחן אוכל ל-15 אורחים, עם מטבח נפרד עם אי מרכזי ומרפסת.", "אח, פינת ספרייה בחלון בולט, שולחן אוכל ל-15 אורחים, מטבח עם אי מרכזי ומרפסת."),
]
EXT = {".py", ".html", ".md", ".json", ".xml", ".txt", ".js", ".csv", ".gs"}
SKIP = {"node_modules", ".git", ".vercel"}

totaux = {k: 0 for k, _, _ in PAIRES}
touches = []
for racine in RACINES:
    for p in sorted(racine.rglob("*")):
        if not p.is_file() or p.suffix not in EXT or p.name in EXCLUS:
            continue
        if SKIP & set(p.parts):
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
            touches.append((p.relative_to(ICI.parent).as_posix(), fait))
            if not A_BLANC:
                p.write_bytes(neuf.encode("utf-8"))
for f, d in touches:
    print(f, d)
print("TOTAUX", totaux, "occurrences", sum(totaux.values()), "fichiers", len(touches), "(à blanc)" if A_BLANC else "")
