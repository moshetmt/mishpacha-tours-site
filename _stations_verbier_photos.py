# -*- coding: utf-8 -*-
"""29/10 : photo Wikimedia Commons de Verbier (licence lue par l'API, CC BY-SA refusée car og:image),
bannière 1600 px (img/stock/st-verbier.jpg), carte du hub 900x600 (img/stock/hub-kosher-verbier.jpg),
crédits ajoutés à CREDITS.md et à la page /credits/ (EN). Idempotent. Python avec Pillow (python 3.11)."""
import json, urllib.request, urllib.parse, io, re, os, html
from PIL import Image, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "MishpachaTours/1.0 (contact@123digital.fr)"}
T = "File:Verbier Valais 029.JPG"
p = dict(action="query", format="json", prop="imageinfo", titles=T, iiprop="url|extmetadata", iiurlwidth=2000)
r = json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA), timeout=30))
ii = next(iter(r["query"]["pages"].values()))["imageinfo"][0]
md = ii["extmetadata"]; lic = md["License"]["value"]
assert "sa" not in lic.lower(), lic
art = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(T.replace(" ", "_"))
st, hub = "img/stock/st-verbier.jpg", "img/stock/hub-kosher-verbier.jpg"
if not (os.path.exists(st) and os.path.exists(hub)):
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read()))).convert("RGB")
    im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(st, "JPEG", quality=82, optimize=True, progressive=True)
    h = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    top = max(0, (h.height - 600) // 2)
    h.crop((0, top, 900, top + 600)).save(hub, "JPEG", quality=80, optimize=True, progressive=True)
    print("images", lic, art)
rows = [f"| {f} | {T} | {lic} | {art} | {url} |" for f in (st, hub)]
s = io.open("CREDITS.md", encoding="utf-8").read()
new = [x for x in rows if x.split(" | ")[0][2:] not in s]
if new:
    io.open("CREDITS.md", "w", encoding="utf-8", newline="\n").write(s.rstrip("\n") + "\n" + "\n".join(new) + "\n")
print("CREDITS.md +", len(new))
# page /credits/ EN : deux lignes après Crans-Montana, compteur +2
c = io.open("credits/index.html", encoding="utf-8").read()
if "st-verbier.jpg" not in c:
    li = "".join(f'<li><b>{html.escape(T.replace("File:", ""))}</b><span>{html.escape(f.replace("img/", ""))} · {html.escape(art)} · {html.escape(lic)}</span><span class="liens"><a class="go" href="{html.escape(url)}" target="_blank" rel="noopener">Source</a></span></li>' for f in (st, hub))
    m = re.search(r'stock/hub-kosher-crans-montana\.jpg · .*?</li>', c)
    assert m
    c = c[:m.end()] + li + c[m.end():]
    c = re.sub(r"(<h2>Photographs <small>)(\d+)(</small>)", lambda k: f"{k.group(1)}{int(k.group(2)) + 2}{k.group(3)}", c, 1)
    c = re.sub(r"(<li>)(\d+)( photographs</li>)", lambda k: f"{k.group(1)}{int(k.group(2)) + 2}{k.group(3)}", c, 1)
    io.open("credits/index.html", "w", encoding="utf-8", newline="\n").write(c); print("credits/index.html +2")
