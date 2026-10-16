# -*- coding: utf-8 -*-
"""Lot du 16/10 : photos Wikimedia Commons des 6 stations suisses et italiennes (licence lue par l'API),
bannière 1600 px (img/stock/st-<station>.jpg) et carte du hub 900x600 (img/stock/hub-kosher-<station>.jpg), crédits ajoutés à CREDITS.md."""
import json, urllib.request, urllib.parse, io, re, subprocess, os
UA = {"User-Agent": "MishpachaTours/1.0 (contact@123digital.fr)"}
PICK = {"zermatt": "File:Zermatt (132078539).jpeg", "st-moritz": "File:Lake St. Moritz in winter.jpg",
        "crans-montana": "File:Crans Montana Valais Suisse 20190316.jpg", "cervinia": "File:Skigebiet am Plateau Rosa Breuil-Cervinia-2.jpg",
        "courmayeur": "File:Mont Blanc depuis Val Ferret.jpg", "cortina": "File:Cortina d'Ampezzo - Comune di Cortina d'Ampezzo - 2023-09-27 15-35-37 012.jpg"}
def api(**p):
    p.update(action="query", format="json")
    r = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA)
    return json.load(urllib.request.urlopen(r, timeout=30))
info = api(prop="imageinfo", titles="|".join(PICK.values()), iiprop="url|extmetadata", iiurlwidth=2000)["query"]["pages"]
by = {p["title"]: p["imageinfo"][0] for p in info.values()}
rows = []
for k, t in PICK.items():
    ii = by[t]; md = ii["extmetadata"]; lic = md["License"]["value"]
    art = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
    tmp = f"img/stock/_tmp-{k}.jpg"
    open(tmp, "wb").write(urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read())
    subprocess.run(["magick", tmp, "-auto-orient", "-resize", "1600x", "-strip", "-quality", "82", f"img/stock/st-{k}.jpg"], check=True)
    subprocess.run(["magick", tmp, "-auto-orient", "-resize", "900x", "-gravity", "center", "-extent", "900x600", "-strip", "-quality", "80", f"img/stock/hub-kosher-{k}.jpg"], check=True)
    os.remove(tmp)
    url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_"))
    for f in (f"img/stock/st-{k}.jpg", f"img/stock/hub-kosher-{k}.jpg"):
        rows.append(f"| {f} | {t} | {lic} | {art} | {url} |")
    print(k, lic, art)
s = io.open("CREDITS.md", encoding="utf-8").read()
new = [r for r in rows if r.split(" | ")[0][2:] not in s]
if new:
    io.open("CREDITS.md", "w", encoding="utf-8", newline="\n").write(s.rstrip("\n") + "\n" + "\n".join(new) + "\n")
print("CREDITS.md +", len(new))
