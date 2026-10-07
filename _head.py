# -*- coding: utf-8 -*-
"""Helper commun des generateurs : nettoie le head herite de l'accueil (canonical, og, JSON-LD)
   et pose canonical + Open Graph propres a la page."""
import re, html, json

OG_IMAGE = "https://mishpachatours.com/img/og-mishpacha-tours.jpg"

def clean(h):
    h = re.sub(r'<link rel="canonical"[^>]*>\n?', "", h)
    h = re.sub(r'<meta property="og:[^"]*"[^>]*>\n?', "", h)
    h = re.sub(r'<meta name="twitter:card"[^>]*>\n?', "", h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", h, flags=re.S)
    return h

def head_page(h, path, title, desc, ld=None):
    h = clean(h)
    og = (f'<link rel="canonical" href="https://mishpachatours.com{path}">\n'
          '<meta property="og:type" content="article">\n<meta property="og:site_name" content="Mishpacha Tours">\n'
          f'<meta property="og:title" content="{html.escape(title)}">\n<meta property="og:description" content="{html.escape(desc)}">\n'
          f'<meta property="og:image" content="{OG_IMAGE}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
          '<meta name="twitter:card" content="summary_large_image">\n')
    if ld: og += f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return h.replace("</head>", og + "</head>", 1)
