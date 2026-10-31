# -*- coding: utf-8 -*-
"""30/10 : photos Wikimedia Commons de Gstaad, Davos et de la page « Ailleurs » (licence lue par l'API, CC BY-SA refusée car
og:image ; jamais Gemini, jamais Pexels pour les stations), bannière 1600 px (img/stock/st-<x>.jpg, recadrée en 3:2 quand la
photo est trop carrée), carte du hub 900x600 (img/stock/hub-<slug>.jpg), crédits ajoutés à CREDITS.md (après les lignes
Verbier) et aux 4 pages /credits/ (même mécanique que _stations_verbier_photos.py). Idempotent. py -3.14 depuis site-v5."""
import json, urllib.request, urllib.parse, io, re, os, html
from PIL import Image, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "MishpachaTours/1.0 (contact@123digital.fr)"}
PHOTOS = [  # titre Commons, bannière, carte du hub, haut du recadrage (fraction de la hauteur) quand la photo est trop carrée
  ("File:Gstaad. Palace Hotel from The Promenade, Switzerland - panoramio.jpg", "img/stock/st-gstaad.jpg", "img/stock/hub-kosher-gstaad.jpg", 0.04),
  ("File:Weissfluhjoch-2010.jpg", "img/stock/st-davos.jpg", "img/stock/hub-kosher-davos.jpg", 0.5),
  ("File:St. Johann in Tirol Winter 2015.JPG", "img/stock/st-anywhere.jpg", "img/stock/hub-kosher-ski-anywhere.jpg", 0.5),
]
LANGS = {".": ("Photographs", "Source"), "fr": ("Photographies", "Source"), "es": ("Fotografías", "Fuente"), "he": ("צילומים", "מקור")}
rows, lis = [], []
for T, st, hub, top in PHOTOS:
    p = dict(action="query", format="json", prop="imageinfo", titles=T, iiprop="url|extmetadata", iiurlwidth=2000)
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA), timeout=30))
    ii = next(iter(r["query"]["pages"].values()))["imageinfo"][0]
    md = ii["extmetadata"]; lic = md["License"]["value"]
    assert "sa" not in lic.lower() and "gfdl" not in lic.lower(), (T, lic)
    art = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
    url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(T.replace(" ", "_"))
    if not (os.path.exists(st) and os.path.exists(hub)):
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read()))).convert("RGB")
        if im.width / im.height < 1.45:   # trop carrée pour une bannière : 3:2
            nh = round(im.width / 1.5); y = max(0, min(im.height - nh, round((im.height - nh) * top if top < 0.5 else (im.height - nh) * 0.5)))
            im = im.crop((0, y, im.width, y + nh))
        im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(st, "JPEG", quality=82, optimize=True, progressive=True)
        h = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        t = max(0, (h.height - 600) // 2)
        h.crop((0, t, 900, t + 600)).save(hub, "JPEG", quality=80, optimize=True, progressive=True)
        print("images", st, lic, art)
    rows += [f"| {f} | {T} | {lic} | {art} | {url} |" for f in (st, hub)]
    lis += [(T, f, art, lic, url) for f in (st, hub)]
# CREDITS.md : après les deux lignes Verbier (section du 29/10), jamais en fin de fichier (la section Icônes or y est)
s = io.open("CREDITS.md", encoding="utf-8").read()
new = [x for x in rows if x.split(" | ")[0][2:] not in s]
if new:
    anc = "| img/stock/hub-kosher-verbier.jpg |"; i = s.find("\n", s.find(anc)) + 1; assert i > 0
    io.open("CREDITS.md", "w", encoding="utf-8", newline="\n").write(s[:i] + "\n".join(new) + "\n" + s[i:])
print("CREDITS.md +", len(new))
# pages /credits/ (4 langues) : après la ligne hub-kosher-verbier, compteur du titre + nombre de lignes ajoutées
for d, (h2, src) in LANGS.items():
    p = f"{d}/credits/index.html".replace("./", "")
    c = io.open(p, encoding="utf-8").read()
    add = "".join(f'<li><b>{html.escape(T.replace("File:", ""))}</b><span>{html.escape(f.replace("img/", ""))} · {html.escape(art)} · {html.escape(lic)}</span><span class="liens"><a class="go" href="{html.escape(url)}" target="_blank" rel="noopener">{src}</a></span></li>'
                  for T, f, art, lic, url in lis if f.replace("img/", "") not in c)
    if not add: print("ok   ", p); continue
    m = re.search(r'stock/hub-kosher-verbier\.jpg · .*?</li>', c); assert m, p
    c = c[:m.end()] + add + c[m.end():]
    n = add.count("<li>")
    c = re.sub(r"(<h2>" + re.escape(h2) + r" <small>)(\d+)(</small>)", lambda k: f"{k.group(1)}{int(k.group(2)) + n}{k.group(3)}", c, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(c); print(p, "+", n)
