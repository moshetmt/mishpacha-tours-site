# -*- coding: utf-8 -*-
"""Lisibilité du site par les agents IA (audit « Is Agentic » du 25/10/2026, 75/100) :
1. JSON-LD de l'accueil : TravelAgency + Organization, contactPoint, adresse (4 langues).
2. 404.html (gabarit de la page merci) et 404.md.
3. Un index.md à côté de chaque index.html (contenu de <main> en Markdown), servi quand Accept: text/markdown.
4. vercel.json en « routes » : négociation Markdown avant le système de fichiers, 404 Markdown après, Vary: Accept partout.
    python _agentic.py   (depuis site-v5/, puis python _build_sitemap.py)"""
import glob, json, os, re
from markdownify import markdownify as md

BASE = "https://mishpachatours.com"

# 1. JSON-LD Organization
OLD_TYPE = '"@type": "TravelAgency", "@id": "https://mishpachatours.com/#organization"'
NEW_TYPE = '"@type": ["TravelAgency", "Organization"], "@id": "https://mishpachatours.com/#organization"'
OLD_TEL = '"telephone": "+33652092301",'
CONTACT = ('"telephone": "+33652092301", "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", '
           '"telephone": "+33652092301", "email": "contact@mishpachatours.com", "availableLanguage": ["en", "fr", "he", "es"], '
           '"contactOption": "TollFree"}],')
for p in ["index.html", "fr/index.html", "es/index.html", "he/index.html"]:
    h = open(p, encoding="utf-8").read()
    if OLD_TYPE in h:
        h = h.replace(OLD_TYPE, NEW_TYPE, 1).replace(OLD_TEL, CONTACT.replace(', "contactOption": "TollFree"', ""), 1)
        open(p, "w", encoding="utf-8").write(h); print("JSON-LD Organization", p)
    else:
        print("JSON-LD deja fait ou introuvable", p)

# 2. 404.html depuis la page merci (meme gabarit, chemins ramenes a la racine)
m = open("merci/index.html", encoding="utf-8").read()
m = m.replace('href="../', 'href="./').replace('src="../', 'src="./')
m = re.sub(r'<link rel="canonical"[^>]*>\s*', "", m)
m = re.sub(r"<title>.*?</title>", "<title>Page not found | Mishpacha Tours</title>", m, flags=re.S)
m = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="This page does not exist. Find the kosher Alps, Jewish Lyon tours and practical guides from the home page."', m)
m = m.replace("<a href=\"./\">Home</a> / Thank you", "<a href=\"./\">Home</a> / Page not found")
m = re.sub(r"<h1>.*?</h1>", "<h1>Page not found, <i>let us point you the right way</i></h1>", m, flags=re.S)
m = re.sub(r'<p class="intro-fiche">We reply within.*?</p>', '<p class="intro-fiche">This address does not exist or has moved. The home page lists every tour, chalet and guide; the sitemap and llms.txt list every page.</p>', m, flags=re.S)
m = re.sub(r'<p style="margin-top:40px">.*?</p>', '<p style="margin-top:40px"><a class="btn-noir large" href="./">Back to the home page</a></p>', m, flags=re.S)
m = m.replace('<a href="./">Back to the tours</a>', '<a href="./sitemap.xml">Sitemap</a> · <a href="./llms.txt">llms.txt</a> · <a href="https://wa.me/33652092301" rel="noopener">WhatsApp</a>')
open("404.html", "w", encoding="utf-8").write(m); print("404.html")
open("404.md", "w", encoding="utf-8").write(
    "# Page not found (404)\n\nThis address does not exist on mishpachatours.com, or the page has moved.\n\n"
    f"- Home: {BASE}/\n- Every page, one line each: {BASE}/llms.txt\n- Sitemap: {BASE}/sitemap.xml\n"
    f"- Contact: WhatsApp +33 6 52 09 23 01, contact@mishpachatours.com\n"); print("404.md")

# 3. index.md par page
def meta(h, name):
    r = re.search(rf'<meta name="{name}" content="([^"]*)"', h); return r.group(1) if r else ""
n = 0
for p in sorted(glob.glob("**/index.html", recursive=True)):
    d = os.path.dirname(p).replace("\\", "/")
    if d.startswith(("_", "preview")) or "merci" in d.split("/"): continue
    h = open(p, encoding="utf-8").read()
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)\.?/?([^)]*)\)", lambda mm: "](" + BASE + "/" + mm.group(1).lstrip("./") + ")", text)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {meta(h, 'description')}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    open(os.path.join(os.path.dirname(p), "index.md"), "w", encoding="utf-8").write(out); n += 1
print(n, "index.md")

# 4. vercel.json : routes (ordre maitrise ; les rewrites ne passent qu'apres le systeme de fichiers)
MD = [{"type": "header", "key": "accept", "value": ".*text/markdown.*"}]
routes = [
    {"src": "/(.*)", "has": [{"type": "host", "value": "mishpacha-tours-site.vercel.app"}], "status": 308, "headers": {"Location": "https://mishpachatours.com/$1"}},
    {"src": "/(.*)", "headers": {"X-Content-Type-Options": "nosniff", "Vary": "Accept"}, "continue": True},
    {"src": "/", "has": MD, "dest": "/index.md"},
    {"src": "/((?:[^./]+/)*[^./]+)/?", "has": MD, "dest": "/$1/index.md", "check": True},
    {"handle": "filesystem"},
    {"src": "/(.*)", "has": MD, "dest": "/404.md", "status": 404},
    {"src": "/(.*)", "dest": "/404.html", "status": 404},
]
json.dump({"$schema": "https://openapi.vercel.sh/vercel.json", "routes": routes}, open("vercel.json", "w", encoding="utf-8"), indent=2)
print("vercel.json")
