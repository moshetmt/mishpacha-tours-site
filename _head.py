# -*- coding: utf-8 -*-
"""Helper commun des generateurs : nettoie le head herite de l'accueil (canonical, og, JSON-LD, hreflang)
   et pose canonical + Open Graph + JSON-LD propres a la page. Entite unique : ORG (@id), referencee partout."""
import re, html, json

BASE = "https://mishpachatours.com"
OG_IMAGE = BASE + "/img/og-mishpacha-tours.jpg"
ORG = BASE + "/#organization"
DATE = "2026-10-07"   # dateModified declaree (= date de verification des pages)

def clean(h):
    h = re.sub(r'<link rel="canonical"[^>]*>\n?', "", h)
    h = re.sub(r'<meta property="og:[^"]*"[^>]*>\n?', "", h)
    h = re.sub(r'<meta name="twitter:card"[^>]*>\n?', "", h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", h, flags=re.S)
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', "", h)
    return h

def strip(s): return html.unescape(re.sub("<[^>]+>", "", s))

def addr(a):
    m = re.match(r"^(.*?),\s*(\d{5})\s*(.*)$", a.strip())
    if not m: return {"@type": "PostalAddress", "streetAddress": a, "addressCountry": "FR"}
    return {"@type": "PostalAddress", "streetAddress": m.group(1), "postalCode": m.group(2), "addressLocality": m.group(3) or "Lyon", "addressCountry": "FR"}

def place(name, a, tel="", typ="Place", geo=None, **k):
    p = {"@type": typ, "name": strip(name), "address": addr(a)}
    if tel: p["telephone"] = "+33" + re.sub(r"\D", "", tel)[1:]
    if geo: p["geo"] = {"@type": "GeoCoordinates", "latitude": geo[0], "longitude": geo[1]}
    p.update(k); return p

def itemlist(name, items):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": strip(name),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}

def crumbs(items):
    """items = [(name, path)] apres Home."""
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    lst += [{"@type": "ListItem", "position": i + 2, "name": strip(n), "item": BASE + p} for i, (n, p) in enumerate(items)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

def faqpage(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def webpage(path, title, desc, lang="en"):
    return {"@context": "https://schema.org", "@type": "WebPage", "@id": BASE + path, "url": BASE + path, "name": strip(title), "description": strip(desc),
            "inLanguage": lang, "dateModified": DATE, "author": {"@id": ORG}, "publisher": {"@id": ORG},
            "isPartOf": {"@type": "WebSite", "url": BASE + "/", "name": "Mishpacha Tours"}}

def head_page(h, path, title, desc, ld=None):
    h = clean(h)
    og = (f'<link rel="canonical" href="{BASE}{path}">\n'
          '<meta property="og:type" content="article">\n<meta property="og:site_name" content="Mishpacha Tours">\n'
          f'<meta property="og:title" content="{html.escape(title)}">\n<meta property="og:description" content="{html.escape(desc)}">\n'
          f'<meta property="og:image" content="{OG_IMAGE}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
          '<meta name="twitter:card" content="summary_large_image">\n')
    if ld: og += f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return h.replace("</head>", og + "</head>", 1)
