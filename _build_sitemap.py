# -*- coding: utf-8 -*-
"""sitemap.xml + robots.txt depuis les dossiers index.html presents. python _build_sitemap.py (depuis site-v5/)"""
import os, glob, datetime
BASE = "https://mishpachatours.com"
urls = ["/"]
for p in sorted(glob.glob("**/index.html", recursive=True)):
    d = os.path.dirname(p).replace("\\", "/")
    if not d or d.startswith("_") or "merci" in d.split("/"): continue
    if 'data-i18n="todo"' in open(p, encoding="utf-8").read(): continue   # page preparee, pas encore traduite
    urls.append("/" + d + "/")
today = datetime.date.today().isoformat()
def prio(u):
    if u == "/": return "1.0"
    if "/tours/" in u: return "0.9"
    return "0.7"
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
xml += [f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{prio(u)}</priority></url>" for u in urls]
xml.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(xml) + "\n")
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "CCBot", "meta-externalagent", "Amazonbot", "DuckAssistBot", "YouBot"]
rob = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
open("robots.txt", "w", encoding="utf-8").write(rob + f"User-agent: *\nAllow: /\nDisallow: /merci/\nSitemap: {BASE}/sitemap.xml\nLLMs: {BASE}/llms.txt\n")

# llms.txt : resume + une ligne par page (titre, description), pour les moteurs de reponse IA
import re, html
def meta(path):
    h = open(path, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", h, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', h)
    return html.unescape(t.group(1).strip()) if t else "", html.unescape(d.group(1)) if d else ""
GROUPS = [("Tours", lambda u: u.startswith("/tours/")),
          ("Practical guides: kosher, synagogues, Shabbat, Chabad, mikveh, hotels", lambda u: any(k in u for k in ("kosher", "synagogue", "shabbat", "chabad", "mikveh", "where-to-stay", "faq", "safe", "catering", "itinerary", "cemetery"))),
          ("Places and memory: Grande Synagogue, rue Juiverie, CHRD, Montluc, Izieu, history", lambda u: any(k in u for k in ("grande-synagogue", "juiverie", "history", "chrd", "montluc", "izieu"))),
          ("Alps and region", lambda u: any(k in u for k in ("alps", "ski", "around-lyon"))),
          ("About", lambda u: True)]
lines = ["# Mishpacha Tours, Jewish Tours of Lyon", "",
 "> Private, strictly kosher guided tours of Jewish Lyon, France, led by a Jewish, observant, state-licensed guide-conferencier. The only tour that goes inside the Grande Synagogue of Lyon (quai Tilsitt, 1864), by a special authorisation that Mishpacha Tours holds; the building is closed to visitors outside the Heritage Days. Five tours: Jewish Lyon (2.5 h), Memory CHRD, Memory Montluc and Neveh Shalom, Stopover (3 h, between the airport and the Alps), Izieu day trip. Tours in English, French or Spanish (Hebrew-speaking guests are guided in English), per group, never on Shabbat or Jewish holidays. Bookings by WhatsApp +33 7 67 71 12 59 or contact@mishpachatours.com.", "",
 "Key facts: tours priced per group (Jewish Lyon from 290 EUR for 1 to 4 people); free cancellation up to 24 hours before; every tour is run as a secured tour (private group, discreet routes fixed in advance, guide from the community) with a professional security escort on request, priced separately; the site also documents the kosher restaurants, synagogues, Chabad houses, mikvaot and Shabbat logistics of Lyon and Villeurbanne, and the Jewish communities and kosher options of the French Alps (Grenoble, Aix-les-Bains, Annecy, Courchevel, Megeve). Facts are sourced and dated on each page; verify hours and prices before travelling.", ""]
done = set()
for gname, test in GROUPS:
    items = [u for u in urls if u not in done and u != "/" and not u.startswith(("/fr/", "/es/", "/he/")) and test(u)]
    if not items: continue
    lines.append(f"## {gname}"); lines.append("")
    for u in items:
        done.add(u); t, d = meta(u.strip("/") + "/index.html")
        lines.append(f"- [{t.split(' | ')[0]}]({BASE}{u}): {d}")
    lines.append("")
lines.append("## Home"); lines.append(""); t, d = meta("index.html"); lines.append(f"- [{t.split(' | ')[0]}]({BASE}/): {d}")
lines += ["", "## Other languages", "", "The whole site exists in French (/fr/), Spanish (/es/) and Hebrew (/he/), same URLs under the language prefix; hreflang links on every page. Tours are guided in English, French or Spanish."]
open("llms.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(len(urls), "urls")
