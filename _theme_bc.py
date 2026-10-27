"""Prépare une copie du site en version B (alterné) ou C (clair) pour une préversion.

python _theme_bc.py b <dossier_sortie>
python _theme_bc.py c <dossier_sortie>

- ajoute theme-b / theme-c sur <body> et les feuilles valora-clair.css + valora-<x>.css ;
- pose la classe .clair sur les sections de <main> (B : une sur deux ; C : toutes),
  sauf bannière, barre de réservation, bloc final (bande forte) et pages Lyon déjà claires.
Le dossier source n'est jamais modifié.
"""
import re, shutil, sys
from html.parser import HTMLParser
from pathlib import Path

ICI = Path(__file__).parent
SAUTE_SECTION = re.compile(r"(?<![-\w])(hero|cherche-bar|lead-final|ticket-zone)(?![-\w])")

class Enfants(HTMLParser):
    """Repère les balises ouvrantes des enfants directs de <main> (positions dans le texte)."""
    VIDES = {"img", "br", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "track"}
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.prof = None; self.pile = 0; self.res = []
    def handle_starttag(self, tag, attrs):
        if tag == "main" and self.prof is None:
            self.prof = 0; return
        if self.prof is None or tag in self.VIDES:
            return
        if self.pile == 0 and tag in ("section", "div"):
            self.res.append((self.getpos(), tag, dict(attrs).get("class", "")))
        self.pile += 1
    def handle_endtag(self, tag):
        if self.prof is None or tag in self.VIDES:
            return
        if tag == "main" and self.pile == 0:
            self.prof = None; return
        self.pile -= 1

def offset(texte, pos):
    l, c = pos
    lignes = texte.split("\n")
    return sum(len(x) + 1 for x in lignes[:l - 1]) + c

def traite(html, theme):
    m = re.search(r'<body class="([^"]*)"', html)
    if not m or "valora" not in m.group(1).split():
        return html
    classes = m.group(1).split()
    if "valora-clair" in classes or "valora-visite" in classes:
        lyon = True
    else:
        lyon = False
    p = Enfants(); p.feed(html)
    elig = [(pos, tag, cls) for pos, tag, cls in p.res
            if not SAUTE_SECTION.search(cls)]
    a_marquer = []
    if not lyon:
        for i, e in enumerate(elig):
            if theme == "c" or i % 2 == 1:
                a_marquer.append(e)
    for pos, tag, cls in sorted(a_marquer, key=lambda e: e[0], reverse=True):
        o = offset(html, pos)
        fin = html.index(">", o)
        balise = html[o:fin]
        if 'class="' in balise:
            nb = balise.replace('class="', 'class="clair ', 1)
        else:
            nb = balise + ' class="clair"'
        html = html[:o] + nb + html[fin:]
    html = html.replace(m.group(0), f'<body class="{m.group(1)} theme-{theme}"', 1)
    lien = '<link rel="stylesheet" href="/valora.css">'
    ajout = f'<link rel="stylesheet" href="/valora-clair.css"><link rel="stylesheet" href="/valora-{theme}.css">'
    if lien in html and "valora-clair.css" not in html:
        html = html.replace(lien, lien + ajout, 1)
    return html

def main():
    """N'écrit dans <sortie> que les pages modifiées (même chemin relatif)."""
    theme, sortie = sys.argv[1], Path(sys.argv[2])
    if sortie.exists():
        shutil.rmtree(sortie)
    n = 0
    for f in ICI.rglob("*.html"):
        rel = f.relative_to(ICI)
        if rel.parts[0] in ("preview", "node_modules") or rel.parts[0].startswith("."):
            continue
        t = f.read_text(encoding="utf-8")
        t2 = traite(t, theme)
        if t2 != t:
            d = sortie / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            d.write_text(t2, encoding="utf-8", newline=""); n += 1
    print(theme, n, "pages ->", sortie)

if __name__ == "__main__":
    main()
