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
GROUPS = [("Alps: kosher holidays, chalet, resorts", lambda u: any(k in u for k in ("alps", "ski", "chalet", "kosher-val", "kosher-courchevel", "kosher-megeve", "kosher-alpe", "kosher-les-", "kosher-la-", "kosher-chamonix", "kosher-annecy", "kosher-grenoble", "kosher-services", "kosher-vacation", "flights"))),
          ("Jewish Lyon tours", lambda u: u.startswith("/tours/") or u == "/jewish-lyon-tours/"),
          ("Practical guides: kosher, synagogues, Shabbat, Chabad, mikveh, hotels", lambda u: any(k in u for k in ("kosher", "synagogue", "shabbat", "chabad", "mikveh", "where-to-stay", "faq", "safe", "catering", "itinerary", "cemetery"))),
          ("Places and memory: Grande Synagogue, rue Juiverie, CHRD, Montluc, Izieu, history", lambda u: any(k in u for k in ("grande-synagogue", "juiverie", "history", "chrd", "montluc", "izieu"))),
          ("Alps and region", lambda u: any(k in u for k in ("alps", "ski", "around-lyon"))),
          ("About", lambda u: True)]
lines = ["# Mishpacha Tours, kosher holidays in the French Alps and Lyon", "",
 "> Strictly kosher holidays in the French Alps and Lyon, shomer shabbat. A chalet in Les Deux Alpes (seven bedrooms and a baby room, 15 to 16 guests, two minutes from the slopes) with a private kosher chef and daily cleaning; kosher meals, Shabbat, holidays and a minyan with a Sefer Torah arranged in the ski resorts (Les Deux Alpes, Courchevel, Val Thorens, Megeve, Alpe d'Huez, Val d'Isere, Les Arcs, La Plagne, Chamonix, Annecy, Grenoble); private transfers from Lyon or Geneva; every request answered with a day-by-day programme, price at the end. Stays, transfers and meals are organised and invoiced by a kosher team based in the Alps, part of the Chabad network of the Alps; Mishpacha Tours sells its guided tours in Lyon. Requests by WhatsApp +33 6 52 09 23 01 (answered in English, Hebrew, French or Spanish) or contact@mishpachatours.com.", "",
 "Jewish Lyon: private, strictly kosher guided tours led by a Jewish, observant, state-licensed guide-conferencier, including the only tour that goes inside the Grande Synagogue of Lyon (quai Tilsitt, 1864) by a special authorisation that Mishpacha Tours holds. Five tours (Jewish Lyon 2.5 h, Memory CHRD, Memory Montluc and Neveh Shalom, Stopover 3 h between the airport and the Alps, Izieu day trip), guided in English, French or Spanish, priced per group (from 290 EUR for 1 to 4 people), free cancellation up to 24 hours before, never on Shabbat or Jewish holidays, security escort on request. The site also documents the kosher restaurants, synagogues, Chabad houses, mikvaot and Shabbat logistics of Lyon and Villeurbanne. Facts are sourced and dated on each page; verify hours and prices before travelling.", ""]
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
