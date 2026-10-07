# -*- coding: utf-8 -*-
"""Genere /merci/ (page d'arrivee apres le formulaire). python _build_merci.py (depuis site-v5/)"""
from _head import head_page
import re, os
home = open("index.html", encoding="utf-8").read()
head = home[:home.index("<main>")]; foot = home[home.index("</main>")+7:]
def rel(s):
    for a, b in [('href="img/','href="../img/'),('src="img/','src="../img/'),('src="fonts/','src="../fonts/'),('href="fonts/','href="../fonts/'),
                 ('href="styles.css"','href="../styles.css"'),('href="./"','href="../"'),('href="#tours"','href="../#tours"'),('href="#why"','href="../#why"'),
                 ('href="#before"','href="../#before"'),('href="#guide"','href="../#guide"'),('href="fr/"','href="../fr/"'),('href="es/"','href="../es/"'),
                 ('href="he/"','href="../he/"'),('href="credits.html"','href="../credits.html"'),('href="#book"','href="../#book"'),('href="jewish-lyon-guide/"','href="../jewish-lyon-guide/"')]:
        s = s.replace(a, b)
    return s
h = rel(head)
h = re.sub(r"<title>.*?</title>", "<title>Thank you | Mishpacha Tours, Jewish Tours of Lyon</title>", h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Your request has been received. We reply within one business day, never on Shabbat.">', h)
h = h.replace('<meta name="robots" content="noindex">', '<meta name="robots" content="noindex, follow">')
h = head_page(h, "/merci/", "Thank you | Mishpacha Tours", "Your request has been received.")
body = '''<main>
<section class="pratique-hero"><div class="wrap">
  <p class="fil"><a href="../">Home</a> / Thank you</p>
  <div class="pratique-tete"><div><h1>Thank you, <i>we have your request</i></h1>
  <p class="intro-fiche">We reply within one business day, and never on Shabbat or on a Jewish holiday. If your dates are close, the fastest way to reach us is WhatsApp.</p>
  <p><a class="btn-noir large" href="https://wa.me/33767711259?text=Hello%2C%20I%20just%20sent%20a%20booking%20request%20on%20the%20website." rel="noopener"><svg><use href="#wa"/></svg>Message us on WhatsApp</a></p>
  <p class="intro-fiche"><a href="../">Back to the tours</a></p></div>
  <img src="../img/illus/flat-jewish-lyon.png" alt="" width="700" height="700"></div>
</div></section>
</main>'''
f = rel(foot).replace("document.getElementById('chercheur').addEventListener","document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
os.makedirs("merci", exist_ok=True); open("merci/index.html", "w", encoding="utf-8").write(h + body + f); print("ok merci")
