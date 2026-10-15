# -*- coding: utf-8 -*-
"""Cherche des photos Wikimedia Commons par sujet, licence libre vérifiée (pas de NC/ND), 4 candidates par sujet."""
import json, re, sys, os, urllib.request, urllib.parse
UA = {"User-Agent": "mishpacha-tours/1.0 (contact@mishpachatours.com)"}
ICI = os.path.dirname(os.path.abspath(__file__))
SUJETS = {
    "juiverie": "rue Juiverie Lyon",
    "vieux-lyon": "Vieux Lyon rue Saint-Jean",
    "traboule": "traboule Lyon",
    "tilsitt": "Grande synagogue de Lyon quai Tilsitt",
    "chrd": "Centre d'histoire de la résistance et de la déportation Lyon",
    "montluc": "prison de Montluc Lyon",
    "izieu": "Maison d'Izieu",
    "saone": "quais de Saône Lyon Vieux Lyon",
    "bouchon": "bouchon lyonnais rue",
}
def get(params):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
credits = {}
for cle, q in SUJETS.items():
    r = get({"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6,
             "gsrlimit": 12, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1600})
    n = 0
    for pg in sorted((r.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 99)):
        ii = pg["imageinfo"][0]; m = ii.get("extmetadata", {})
        lic = m.get("LicenseShortName", {}).get("value", "")
        if not any(k in lic for k in ("CC BY", "CC0", "Public domain", "CC-BY")) or "NC" in lic or "ND" in lic:
            continue
        if ii["width"] < 1200 or ii["width"] < ii["height"]:
            continue
        n += 1
        f = f"{cle}-{n}.jpg"
        open(os.path.join(ICI, f), "wb").write(urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read())
        credits[f] = {"titre": pg["title"], "page": ii["descriptionurl"], "licence": lic,
                      "auteur": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip()[:80]}
        if n == 6:
            break
    print(cle, n)
json.dump(credits, open(os.path.join(ICI, "credits.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
