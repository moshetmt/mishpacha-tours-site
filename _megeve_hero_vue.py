# -*- coding: utf-8 -*-
"""Fiche Loup Blanc : héros = vue Mont-Blanc depuis la terrasse du chalet (photo HD réelle du bien, miroir + recadrage, sans IA),
posée en 1re photo du rail des 4 langues ; l'ancien séjour passe en 2e, chargé en différé. Idempotent (stem megeve-vue-mont-blanc).
04/11/2026 : Moshé trouvait la préversion « pas très jolie » : la salle à manger aux chaises noires ouvrait la fiche."""
import os, re
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
SRC = os.path.join("..", "..", "00-brief", "references", "2026-10-16-megeve-bibi", "originaux-hd", "Chalet-Remy-St-Gervais-chalet-TERRASSE-SUD-3.jpg")
STEM = "megeve-vue-mont-blanc"; W, H = 1600, 964
im = ImageOps.mirror(ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")).rotate(0.3, Image.BICUBIC)
w, h = im.size; box = [int(w * .04), int(h * .05), int(w * .97), int(h * .97)]
bw, bh = box[2] - box[0], box[3] - box[1]
if bw / bh > W / H: nw = int(bh * W / H); box[0] += (bw - nw) // 2; box[2] = box[0] + nw
else: nh = int(bw * H / W); box[1] += (bh - nh) // 2; box[3] = box[1] + nh
im = im.crop(box).resize((W, H), Image.LANCZOS)
im.save(f"img/chalet/{STEM}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
def wp(d, ww, nom):
    x = min(ww, W); im.resize((x, round(H * x / W)), Image.LANCZOS).save(os.path.join(d, nom), "WEBP", quality=80, method=6)
for ww in (640, 960, 1600, 2400): wp("img/h", ww, f"{STEM}-{ww}.webp")
for ww in (640, 960, 1280): wp("img/chalet/w", ww, f"{STEM}-{ww}.webp")
for ww in (336, 672): wp("img/chalet/min", ww, f"{STEM}-{ww}.webp")
NEW = (f'<img src="/img/h/{STEM}-960.webp" srcset="/img/h/{STEM}-640.webp 640w, /img/h/{STEM}-960.webp 960w, /img/h/{STEM}-1600.webp 1600w, /img/h/{STEM}-2400.webp 2400w" '
       f'sizes="(min-width:900px) 58vw, 100vw" alt="{{alt}}" width="1264" height="848" fetchpriority="high" decoding="async">')
n = 0
for pg in ("kosher-chalet-megeve/index.html", "fr/kosher-chalet-megeve/index.html", "es/kosher-chalet-megeve/index.html", "he/kosher-chalet-megeve/index.html"):
    s = open(pg, encoding="utf-8").read()
    if STEM in s: print("déjà fait", pg); continue
    m = re.search(r'(<div class="lc-piste" id="lcPiste">)(<img src="/img/h/megeve-n0-apt-sejour-960\.webp"[^>]*?)( fetchpriority="high")([^>]*>)', s)
    assert m, pg
    alt = re.search(r'alt="([^"]*)"', m.group(2)).group(1)
    s = s[:m.start()] + m.group(1) + NEW.format(alt=alt) + m.group(2) + ' loading="lazy"' + m.group(4) + s[m.end():]
    cnt = len(re.findall(r'<img ', re.search(r'<div class="lc-piste" id="lcPiste">(.*?)<div class="lc-progres">', s, re.S).group(1)))
    s = re.sub(r'(id="lcBarre" style="width:)[0-9.]+%', lambda k: f"{k.group(1)}{100 / cnt:.3f}%", s)
    s = re.sub(r'(<span class="lc-compte" id="lcCompte" dir="ltr">1 / )\d+', lambda k: f"{k.group(1)}{cnt}", s)
    open(pg, "w", encoding="utf-8").write(s); n += 1; print(pg, "rail", cnt)
print("pages", n)
