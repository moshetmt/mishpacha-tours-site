# -*- coding: utf-8 -*-
"""Dégraissage des 4 accueils (14/10) : hero, portes (+ stations en ligne), chalet, comment ça marche, Lyon, formulaire.
Retire preuves, stations, saisons, pourquoi, FAQ. La phrase Atout France de la FAQ passe sous « Comment ça marche »."""
import re, io

FICHIERS = ["index.html", "fr/index.html", "es/index.html", "he/index.html"]

def section(html, motif):
    """Retourne (debut, fin) de la <section ...motif...>...</section> (pas de sections imbriquées)."""
    m = re.search(r'<section[^>]*' + motif + r'[^>]*>.*?</section>\n?', html, re.S)
    return m

for f in FICHIERS:
    html = io.open(f, encoding="utf-8").read()
    orig = html

    # 1. stations : récupérer le libellé (h2 sans <i>) et la liste, puis retirer la section
    m = section(html, 'id="resorts"')
    h2 = re.search(r'<h2>(.*?)</h2>', m.group(0), re.S).group(1)
    libelle = re.sub(r'</?i>', '', h2).strip()
    ul = re.search(r'<ul class="ac-stations">.*?</ul>', m.group(0), re.S).group(0)
    html = html.replace(m.group(0), '')

    # 2. phrase Atout France = première réponse de la FAQ
    m = section(html, 'id="faq"')
    atout = re.search(r'<details><summary>[^<]*</summary><p>(.*?)</p></details>', m.group(0), re.S).group(1)
    html = html.replace(m.group(0), '')

    # 3. retirer preuves, saisons, pourquoi
    for motif in ('class="ac-preuves"', 'id="seasons"', 'id="why"'):
        m = section(html, motif)
        html = html.replace(m.group(0), '')

    # 4. stations en une ligne sous les portes
    ligne = '    <p class="ac-stations-ligne" id="resorts"><b>' + libelle + '</b></p>\n    ' + ul.replace('class="ac-stations"', 'class="ac-stations compacte"') + '\n'
    html = html.replace('    </div>\n  </div>\n</section>\n\n<section class="ss wrap ac-chalet"', '    </div>\n' + ligne + '  </div>\n</section>\n\n<section class="ss wrap ac-chalet"', 1)
    assert 'ac-stations-ligne' in html, f

    # 5. phrase Atout France sous les 3 étapes
    html = re.sub(r'(</ol>\n)(  </div>\n</section>\n+<section class="ss beige ac-lyon")', r'\1    <p class="ac-atout">' + atout.replace('\\', '\\\\') + r'</p>\n\2', html, count=1)
    assert 'ac-atout' in html, f

    html = re.sub(r'\n{3,}', '\n\n', html)
    # 6. menu : l'ancre #resorts existe toujours (sur la ligne de stations)
    assert html != orig
    io.open(f, "w", encoding="utf-8", newline="\n").write(html)
    print(f, len(orig), "->", len(html), "sections :", len(re.findall(r'<section', html)))
