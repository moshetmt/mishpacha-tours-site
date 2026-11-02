# -*- coding: utf-8 -*-
"""Régénère l'index.md (version Markdown servie aux agents IA) des seules pages données, avec la méthode de _agentic.py § 3
(lancer _agentic.py en entier réécrirait les 300 pages et le 404).
    python _md_pages.py kosher-courchevel fr/kosher-courchevel ...   (depuis site-v5/)"""
import os, re, sys
from markdownify import markdownify as md

os.chdir(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://mishpachatours.com"

def meta(h, name):
    r = re.search(rf'<meta name="{name}" content="([^"]*)"', h); return r.group(1) if r else ""

for d in sys.argv[1:]:
    d = d.strip("/")
    h = open(os.path.join(d, "index.html"), encoding="utf-8").read()
    main = re.search(r"<main.*?</main>", h, re.S)
    body = main.group(0) if main else re.sub(r"<(header|footer|nav)\b.*?</\1>", "", h[h.find("<body"):], flags=re.S)
    body = re.sub(r"<(script|style|svg|noscript|form|select|button)\b.*?</\1>", "", body, flags=re.S)
    title = re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    url = BASE + "/" + (d + "/" if d else "")
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\((?!https?:|mailto:|tel:|#)([^)\s]*)\)", lambda mm: "](" + __import__("urllib.parse").parse.urljoin(url, mm.group(1)) + ")", text)  # 02/11 : lien relatif résolu depuis la page (../ en FR/ES/HE restait en EN)
    if not re.search(r"^# ", text, re.M): text = f"# {title}\n\n" + text
    out = (f"> {meta(h, 'description')}\n\nSource: {url} (HTML version). Every page of the site, one line each: {BASE}/llms.txt\n\n"
           f"{text}\n\n---\nMishpacha Tours · WhatsApp +33 6 52 09 23 01 · contact@mishpachatours.com · never on Shabbat or Jewish holidays.\n")
    p = os.path.join(d, "index.md")
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    if old != out: open(p, "w", encoding="utf-8", newline="\n").write(out); print("md", d)
