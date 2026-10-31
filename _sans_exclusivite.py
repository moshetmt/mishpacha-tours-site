# -*- coding: utf-8 -*-
"""Pages hébreu : retire les prétentions d'exclusivité (היחיד, היחידים, הבלעדי) interdites par le lexique
(relecture-hebreu §4 contrôle 1), 
EXCEPTION (Moshé 30/10) : « le seul tour qui entre dans la Grande Synagogue » est un fait (personne d'autre n'a le droit à Lyon),
la formule היחיד reste sur ce point ; seules les prétentions sur la villa de Saint-Tropez sont retirées.
Patche he/**/index.html et le jumeau index.md. python _sans_exclusivite.py (depuis site-v5/), relecture du 30/10/2026."""
import io, glob

# (avant, après, occurrences attendues html + md)
REMPLACEMENTS = [
    ('זו הווילה היחידה להשכרה בסן טרופה עם חוף חול פרטי ומוסך סירות משלה, עם רמפת הורדה למים.',
     'וילה להשכרה בסן טרופה, עם חוף חול פרטי ומוסך סירות משלה ורמפת הורדה למים.', 2),
    ('ומוסך סירות עם רמפת הורדה משלו, היחידים להשכרה בסן טרופה.',
     'ומוסך סירות עם רמפת הורדה משלו.', 2),
]

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)

if __name__ == "__main__":
    fichiers = glob.glob("he/**/index.html", recursive=True) + glob.glob("he/**/index.md", recursive=True)
    vus = [0] * len(REMPLACEMENTS); touches = []
    for f in fichiers:
        s = rd(f); n = s
        for i, (a, b, _) in enumerate(REMPLACEMENTS):
            c = n.count(a)
            if c: vus[i] += c; n = n.replace(a, b)
        if n != s: wr(f, n); touches.append(f)
    for (a, b, att), c in zip(REMPLACEMENTS, vus):
        if c != att: print(f"ECART {c} != {att} : {a[:50]}")
    print(sum(vus), "occurrences remplacées dans", len(touches), "fichiers :", ", ".join(sorted(touches)))
