"""Pose la charte « Louis Vuitton » (lv.css + Jost) sur une liste de pages. Idempotent.

Usage : python _charte_lv.py            (pages de PAGES)
        python _charte_lv.py fr/index.html he/index.html ...
Ajoute, après la dernière feuille valora*.css, le lien Google Fonts de Jost puis /lv.css,
et passe <body class="valora ..."> en "valora lv ...". Ne touche à aucun texte.
"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).parent
PAGES = ["index.html"]  # aperçu du 30/10 : accueil EN seulement (Moshé)

BLOC = ('<!--CHARTE-LV--><link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap">'
        '<link rel="stylesheet" href="/lv.css"><!--/CHARTE-LV-->')


def poser(chemin: Path) -> str:
    html = chemin.read_text(encoding="utf-8")
    avant = html
    html = re.sub(r"<!--CHARTE-LV-->.*?<!--/CHARTE-LV-->", "", html, flags=re.S)
    liens = list(re.finditer(r'<link rel="stylesheet" href="/?valora[^"]*\.css">', html))
    if not liens:
        return "SANS valora.css, ignorée"
    fin = liens[-1].end()
    html = html[:fin] + BLOC + html[fin:]

    def corps(m):
        classes = m.group(1).split()
        if "valora" in classes and "lv" not in classes:
            classes.insert(classes.index("valora") + 1, "lv")
        return '<body class="' + " ".join(classes) + '"'
    html = re.sub(r'<body class="([^"]*)"', corps, html, count=1)
    if html == avant:
        return "déjà à jour"
    chemin.write_text(html, encoding="utf-8", newline="")
    return "modifiée"


if __name__ == "__main__":
    for p in (sys.argv[1:] or PAGES):
        print(p, ":", poser(ICI / p))
