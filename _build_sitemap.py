# -*- coding: utf-8 -*-
"""sitemap.xml + robots.txt depuis les dossiers index.html presents. python _build_sitemap.py (depuis site-v5/)"""
import os, glob, datetime
BASE = "https://mishpachatours.com"
EXCL = {"merci", "fr", "es", "he"}
urls = ["/"]
for p in sorted(glob.glob("**/index.html", recursive=True)):
    d = os.path.dirname(p).replace("\\", "/")
    if not d or d.startswith("_") or d.split("/")[0] in EXCL: continue
    urls.append("/" + d + "/")
today = datetime.date.today().isoformat()
def prio(u):
    if u == "/": return "1.0"
    if u.startswith("/tours/"): return "0.9"
    return "0.7"
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
xml += [f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{prio(u)}</priority></url>" for u in urls]
xml.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(xml) + "\n")
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /merci/\nSitemap: {BASE}/sitemap.xml\n")
print(len(urls), "urls")
