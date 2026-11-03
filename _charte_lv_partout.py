# -*- coding: utf-8 -*-
"""Charte « Louis Vuitton » sur toutes les pages du site (Moshé 02/11, 22 h 30 : « je valide, on peut appliquer à toutes les pages »). Idempotent.

Ce que l'accueil EN validé a de plus que les autres pages, et que ce script reporte :
  1. dans <head> : Jost + Suez One (Google Fonts) puis /lv.css, posés juste après la dernière feuille valora*.css (bloc <!--CHARTE-LV-->) ;
  2. sur <body> : la classe « lv » après « valora ». Toute la charte vit dans lv.css, active seulement sur body.valora.lv :
     en-tête noir 64 px (burger blanc, langue sur téléphone, logo picto + « mishpacha tours » en Suez One), titres en Jost,
     sceau Winter Prestige en verre fumé, barre basse et bouton flottant avec le bonhomme, pied noir au filet d'or, cookies, boutons droits ;
  3. rien d'autre : aucun texte, aucun lien, aucun JSON-LD, aucun hreflang, aucun data-prix-tpl n'est touché.
     L'en-tête, le pied et le <head> de chaque page restent les siens ; les formulaires de fin de page gardent leur rôle
     (lead-plan des pages Alpes : préremplit /plan-your-trip/ ; ticket des pages Lyon) et prennent l'habillage LV par lv.css.

Exclus : /espace/ (outil de Mendel, hors charte du site), /_*/ (brouillons, sources). Pages sans valora*.css (44) : lv.css après styles.css.
Déjà en charte (inchangées si on relance) : accueil EN, /merci/ et /plan-your-trip/ des 4 langues, /contact-quick/.
Les accueils FR, ES et HE reçoivent en plus la structure de l'accueil EN par _accueils_lv.py (à lancer après ce script).

Usage (depuis site-v5/) : python _charte_lv_partout.py            toutes les pages
                          python _charte_lv_partout.py --sec      compte sans écrire
                          python _charte_lv_partout.py a/index.html b/index.html
"""
import glob
import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
BLOC = ('<!--CHARTE-LV--><link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Suez+One&display=swap">'
        '<link rel="stylesheet" href="/lv.css"><!--/CHARTE-LV-->')
EXCLUS = re.compile(r"^(?:(?:fr|es|he)/)?(?:espace/|_)")


def transformer(html):
    """Renvoie (html, motif). Idempotent : relancé sur une page déjà en charte, rend le même texte."""
    sans = re.sub(r"<!--CHARTE-LV-->.*?<!--/CHARTE-LV-->", "", html, flags=re.S)
    liens = list(re.finditer(r'<link rel="stylesheet" href="/?valora[^"]*\.css">', sans))
    if not liens:   # 44 pages (chalets, hub, Pessah, services, à propos...) n'ont que styles.css : lv.css se pose après
        liens = list(re.finditer(r'<link rel="stylesheet" href="(?:\.\./)*/?styles\.css">', sans))
    if not liens or '<body class="' not in sans:
        return html, "sans feuille du site"
    fin = liens[-1].end()
    out = sans[:fin] + BLOC + sans[fin:]

    def corps(m):
        classes = m.group(1).split()
        if "lv" not in classes:
            classes.insert(classes.index("valora") + 1 if "valora" in classes else 0, "lv")
        return '<body class="' + " ".join(classes) + '"'
    out = re.sub(r'<body class="([^"]*)"', corps, out, count=1)
    return out, ("modifiée" if out != html else "déjà à jour")


def pages():
    os.chdir(ICI)
    ps = sorted(p.replace("\\", "/") for p in glob.glob("**/index.html", recursive=True))
    ps += ["404.html"]
    return [p for p in ps if not EXCLUS.match(p)]


if __name__ == "__main__":
    sec = "--sec" in sys.argv
    cibles = [a for a in sys.argv[1:] if not a.startswith("--")] or pages()
    os.chdir(ICI)
    bilan = {}
    for p in cibles:
        s = io.open(p, encoding="utf-8", newline="").read()
        n, motif = transformer(s)
        bilan.setdefault(motif, []).append(p)
        if n != s and not sec:
            io.open(p, "w", encoding="utf-8", newline="").write(n)
    for motif, l in bilan.items():
        print(f"{motif} : {len(l)}" + ("  " + ", ".join(l[:12]) if motif != "modifiée" and motif != "déjà à jour" else ""))
