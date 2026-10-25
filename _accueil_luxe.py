# -*- coding: utf-8 -*-
"""Lot 3 de la refonte luxe (décisions Moshé du 25/10, question 3 = A) : sur les 4 accueils, le héros ne garde que la photo,
cinq mots, une phrase et un bouton ; le chercheur (le même formulaire, mêmes champs, même préremplissage) descend juste sous
la photo, en barre. Idempotent (marqueurs LUXE-HERO) ; `--strip` remet le formulaire dans le héros tel qu'il était.
À lancer après _zones.py et _prefill.py, avant _luxe.py."""
import io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STRIP = "--strip" in sys.argv
T = {"en": ("Kosher holidays in the Alps.", "Private chalet, private chef, Shabbat and minyan. Organised for you.", "Find your chalet"),
     "fr": ("Vacances casher dans les Alpes.", "Chalet privé, chef privé, Chabbat et minyan. Tout est organisé pour vous.", "Trouver votre chalet"),
     "es": ("Vacaciones kosher en los Alpes.", "Chalet privado, chef privado, Shabat y minyán. Todo organizado para usted.", "Encontrar su chalet"),
     "he": ("חופשת סקי כשרה באלפים.", "צ'אלה פרטית, שף פרטי, שבת ומניין. הכול מאורגן בשבילכם.", "למצוא את הצ'אלה שלכם")}
A, B = "<!--LUXE-HERO-->", "<!--/LUXE-HERO-->"
n_mod = 0
for lang in ("en", "fr", "es", "he"):
    p = "index.html" if lang == "en" else f"{lang}/index.html"
    pre = "" if lang == "en" else "/" + lang
    s = io.open(p, encoding="utf-8").read(); h = s
    if A in s:  # retour à l'état d'origine conservé dans le marqueur
        orig = re.search(re.escape(A) + r"<!--(.*?)-->" + r".*?" + re.escape(B), s, flags=re.S)
        s = s.replace(orig.group(0), orig.group(1).replace("--&gt;", "-->"), 1)
    if not STRIP:
        m = re.search(r'(<div class="hero-texte">)(.*?)(</div>\s*</section>)', s, flags=re.S)
        form = re.search(r'<form class="chercheur".*?</form>', m.group(2), flags=re.S).group(0)
        h1, sous, btn = T[lang]
        texte = f'\n    <h1>{h1}</h1>\n    <p class="hero-sous">{sous}</p>\n    <a class="btn-hero" href="{pre}/kosher-chalets/">{btn}</a>\n  '
        barre = f'\n<section class="cherche-bar wrap" aria-label="Plan your stay">{form}</section>'
        nouveau = m.group(1) + texte + m.group(3) + barre
        s = s.replace(m.group(0), A + "<!--" + m.group(0).replace("-->", "--&gt;") + "-->" + nouveau + B, 1)
    if s != h:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s); n_mod += 1
print("accueil luxe :", n_mod, "fichiers modifiés", "(strip)" if STRIP else "")
