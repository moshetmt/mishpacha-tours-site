# -*- coding: utf-8 -*-
# 20/10 (C5) : mentions légales (LCEN). Éditeur = entreprise individuelle de la guide. Le marqueur {{SIREN}} est à remplacer par l'opérateur.
# Traductions fr/es/he et rendu des 4 sorties : _confidentialite_legal.py (même convention d'URL : /legal/, /fr/legal/, /es/legal/, /he/legal/).
PAGE = dict(
  slug="legal",
  title="Legal notice and publisher",
  desc="Legal notice of Mishpacha Tours: publisher, sole-trader status, SIREN, address in Lyon, publication director, contact and hosting provider of the website.",
  h1="Legal notice",
  ital="who runs this site",
  intro="This site is published by Mishpacha Tours, a sole-trader business based in Lyon. This page gives the identity of the publisher and of the hosting provider, and how to reach us.",
  chips=["Sole trader", "Lyon, France", "Hosted by Vercel"],
  illus="line-private.png",
  crumb=None,
  ticket=False,
  sections=[
    dict(type="text", h2="Who <i>publishes</i> this site", icos=["badge-check", "users", "file-text", "map-pin", "scroll-text", "info"], html="""<ul>
<li><b>Business name:</b> Mishpacha Tours</li>
<li><b>Run by:</b> Elisabeth Timsit, licensed guide-conférencière</li>
<li><b>SIREN:</b> {{SIREN}}</li>
<li><b>Address:</b> Lyon, France</li>
<li><b>Legal form:</b> sole trader (entreprise individuelle), no share capital</li>
<li><b>VAT:</b> not applicable, article 293 B of the French General Tax Code</li>
</ul>"""),
    dict(type="text", h2="Publication <i>director</i>", ico="users", html="""<p>Elisabeth Timsit.</p>"""),
    dict(type="text", h2="How to <i>reach us</i>", ico="message-circle", html="""<p>Through the <a href="../plan-your-trip/">request form</a> or by email at <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>.</p>"""),
    dict(type="text", h2="<i>Hosting</i>", ico="house", html="""<p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA.</p>"""),
    dict(type="text", h2="<i>Content</i> of the site", ico="book-open", html="""<p>The texts and the layout of this site belong to Mishpacha Tours. The credits for the photographs are listed on the <a href="../credits/">photo credits</a> page.</p>"""),
    dict(type="text", h2="Personal <i>data</i>", ico="shield-check", html="""<p>What we collect, why and for how long is explained in the <a href="../privacy/">privacy policy</a>.</p>"""),
  ],
  related=[("../privacy/", "Privacy"), ("../terms/", "Terms of booking")],
  VERIF=["SIREN : marqueur {{SIREN}} à remplacer dans _pages/legal.py et dans _confidentialite_legal.py (fr, es, he) puis relancer le script.", "Mention TVA « article 293 B du CGI » : valable pour la franchise en base de la micro-entreprise, à confirmer avec le statut réel."],
)
