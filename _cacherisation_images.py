"""Cachérisation : photos réelles (Wikimedia Commons), carte rp-carte sur la page services (4 langues),
image sur la page Pessah (4 langues), crédits. Idempotent. Ne touche ni wp-v3.css ni le formulaire.
Usage : python _cacherisation_images.py [--planche]
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_candidats" / "cacherisation-2026-11-05"
OUT = ROOT / "img" / "cacherisation"
REPORT = ROOT.parents[1] / "06-reports" / "2026-11-05-cacherisation-images"
UA = {"User-Agent": "MishpachaToursBot/1.0 (moshe@123digital.fr)"}

# boîte de recadrage 4:3 : (x0, y0, largeur) en fractions de l'original
CAND = [
    dict(n=1, key="hagalah-bouillante", file="88737.jpg", title="File:88737 hagalah - koshering process of utensils PikiWiki Israel.jpg",
         box=(0.0, 0.31, 1.0), lic="CC BY 2.5", au="Lizi Shanan (PikiWiki Israel)", pub="Lizi Shanan", curid=121599865,
         titre=dict(en="Hagalah, utensils dipped in boiling water", fr="Hagalah, ustensiles plongés dans l'eau bouillante", es="Hagalah, utensilios sumergidos en agua hirviendo", he="הגעלת כלים, כלים מוטבלים במים רותחים"),
         note="Filet d'ustensiles descendu dans un fût d'eau bouillante, vapeur. Recadrage sous les visages : aucun visage, pas de texte, pas de marque."),
    dict(n=2, key="hagalah-chaudrons", file="31511.jpg", title="File:PikiWiki Israel 31511 Religion in Israel.JPG",
         box=(0.06, 0.31, 0.62), lic="CC BY 2.5", au="Udi Steinwell (PikiWiki Israel)", pub="Udi Steinwell", curid=25427425,
         titre=dict(en="Pots on the fire before Pesach", fr="Marmites sur le feu avant Pessah", es="Ollas al fuego antes de Pésaj", he="סירים על האש לפני פסח"),
         note="Marmites sur brûleurs à gaz dans une cour, aucune personne. Les chandeliers du mur sont hors cadre."),
    dict(n=3, key="rack-bidon", file="31375.jpg", title="File:PikiWiki Israel 31375 Cleansing of vessels in boiling water on the eve o.JPG",
         box=(0.15, 0.30, 0.63), lic="CC BY 2.5", au="Avishai Teicher (PikiWiki Israel)",
         note="ECARTEE : visage net d'un jeune, enfants dans la foule. Très parlante sinon."),
    dict(n=4, key="chalumeau-armee", file="kaschern.jpg", title="File:Kaschern von Küchengeräten.JPG",
         box=(0.0, 0.0, 1.0), lic="CC BY-SA 3.0", au="Feliks (Wikipédia allemand)",
         note="ECARTEE : uniformes militaires et bouteilles de gaz. Seul chalumeau du lot."),
]
CHOIX = {"services": "hagalah-bouillante", "pessah": "hagalah-chaudrons"}


def api(**p):
    p["format"] = "json"
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(
                "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA)))
        except Exception:
            time.sleep(2)


def telecharger(c):
    f = SRC / c["file"]
    if f.exists():
        return f
    r = api(action="query", titles=c["title"], prop="imageinfo", iiprop="url", iiurlwidth=3840)
    ii = list(r["query"]["pages"].values())[0]["imageinfo"][0]
    u = ii.get("thumburl") or ii["url"]
    SRC.mkdir(parents=True, exist_ok=True)
    f.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=UA)).read())
    return f


def recadrer(c):
    im = Image.open(telecharger(c)).convert("RGB")
    W, H = im.size
    x0, y0, w = c["box"]
    bw = int(w * W)
    bh = int(bw * 3 / 4)
    x = int(x0 * W)
    y = min(int(y0 * H), H - bh)
    return im.crop((x, y, x + bw, y + bh))


def fabriquer_webp():
    OUT.mkdir(parents=True, exist_ok=True)
    for c in CAND:
        if c["key"] not in CHOIX.values():
            continue
        im = recadrer(c)
        for w in (480, 800):
            im.resize((w, w * 3 // 4), Image.LANCZOS).save(OUT / f"{c['key']}-{w}.webp", "WEBP", quality=80, method=6)


def srcset(key):
    return (f'src="/img/cacherisation/{key}-480.webp" srcset="/img/cacherisation/{key}-480.webp 480w, '
            f'/img/cacherisation/{key}-800.webp 800w" ')


T = {
    "en": dict(label="Kashering the kitchen of the chalet you rent", prix="On request",
               alt_s="Utensils lowered in a net into a drum of boiling water to kasher them (hagalat kelim)",
               alt_p="Pots of boiling water on gas burners in a yard, used to kasher utensils (hagalat kelim)",
               cap="Hagalat kelim: utensils kashered in boiling water before Pesach.", pdir=""),
    "fr": dict(label="Cachérisation de la cuisine du chalet que vous louez", prix="Sur demande",
               alt_s="Ustensiles plongés dans un filet au fond d'un fût d'eau bouillante pour les cachériser (hagalat kelim)",
               alt_p="Marmites d'eau bouillante sur des brûleurs à gaz, dans une cour, pour cachériser les ustensiles (hagalat kelim)",
               cap="Hagalat kelim : les ustensiles sont cachérisés dans l'eau bouillante avant Pessah.", pdir="fr/"),
    "es": dict(label="Kasherización de la cocina del chalé que alquila", prix="Bajo pedido",
               alt_s="Utensilios en una red sumergidos en un barril de agua hirviendo para kasherizarlos (hagalat kelim)",
               alt_p="Ollas de agua hirviendo sobre quemadores de gas, en un patio, para kasherizar los utensilios (hagalat kelim)",
               cap="Hagalat kelim: los utensilios se kasherizan en agua hirviendo antes de Pésaj.", pdir="es/"),
    "he": dict(label="הכשרת המטבח בצ'אלה ששכרתם", prix="לפי בקשה",
               alt_s="כלים ברשת מוטבלים בחבית מים רותחים כדי להכשיר אותם (הגעלת כלים)",
               alt_p="סירים עם מים רותחים על להבות גז בחצר, להכשרת כלים (הגעלת כלים)",
               cap="הגעלת כלים: הכלים מוכשרים במים רותחים לפני פסח.", pdir="he/"),
}
MARK_S = "<!--cach-carte-->"
MARK_P = "<!--cach-fig-->"


def patch_services(lang, t):
    f = ROOT / (t["pdir"] + "kosher-services-french-alps/index.html")
    s = f.read_text(encoding="utf8")
    if MARK_S in s:
        return "deja"
    carte = (f'{MARK_S}<li class="rp-carte"><img {srcset(CHOIX["services"])}sizes="(min-width:900px) 360px, (min-width:600px) 45vw, 90vw" '
             f'alt="{t["alt_s"]}" width="800" height="600" loading="lazy" decoding="async"><span>{t["label"]}</span><b>{t["prix"]}</b></li>')
    m = re.search(r'(<li class="rp-carte"><img[^>]*pizza-480[^>]*>.*?</li>)</ul>', s, re.S)
    assert m, lang
    s = s[:m.end(1)] + carte + s[m.end(1):]
    row = re.compile(r'<li><span>' + re.escape(t["label"]) + r'</span><b>' + re.escape(t["prix"]) + r'</b></li>')
    s, n = row.subn("", s, count=1)
    assert n == 1, (lang, "ligne du tableau introuvable")
    f.write_text(s, encoding="utf8")
    return "ok"


def patch_pessah(lang, t):
    f = ROOT / (t["pdir"] + "kosher-pesach-french-alps/index.html")
    s = f.read_text(encoding="utf8")
    if MARK_P in s:
        return "deja"
    i = s.find('class="mf-col"')
    j = s.find("<p>", s.find("</div></div></div>", i))
    k = s.find("</p>", j) + 4
    fig = (f'{MARK_P}<figure style="margin:24px 0 0;max-width:640px"><img {srcset(CHOIX["pessah"])}sizes="(min-width:900px) 640px, 90vw" '
           f'alt="{t["alt_p"]}" width="800" height="600" loading="lazy" decoding="async" '
           f'style="width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block"><figcaption style="margin-top:8px;font-size:14px;opacity:.85">{t["cap"]}</figcaption></figure>')
    s = s[:k] + fig + s[k:]
    f.write_text(s, encoding="utf8")
    return "ok"


def credits():
    retenues = [cd for cd in CAND if cd["key"] in CHOIX.values()]
    c = ROOT / "CREDITS.md"
    txt = c.read_text(encoding="utf8")
    if "Cachérisation (05/11/2026)" not in txt:
        lignes = ["", "## Cachérisation (05/11/2026)", "",
                  "Photos Wikimedia Commons, licence lue par l'API le 05/11/2026, recadrées en 4:3 et converties en WebP (aucune autre retouche). CC BY : crédit obligatoire, présent sur /credits/. Jamais en og:image.", "",
                  "| Fichier | Titre Commons | Licence | Auteur | Source |", "|---|---|---|---|---|"]
        for cd in retenues:
            lignes.append(f"| img/cacherisation/{cd['key']}-*.webp | {cd['title']} | {cd['lic']} | {cd['au']} | https://commons.wikimedia.org/wiki/{urllib.parse.quote(cd['title'].replace(' ', '_'), safe=':')} |")
        c.write_text(txt.rstrip("\n") + "\n" + "\n".join(lignes) + "\n", encoding="utf8")
    for pdir in ("", "fr/", "es/", "he/"):
        lang = pdir[:-1] or "en"
        p = ROOT / pdir / "credits" / "index.html"
        s = p.read_text(encoding="utf8")
        if "cacherisation/" in s:
            continue
        li = ""
        for cd in retenues:
            url = f"https://commons.wikimedia.org/w/index.php?curid={cd['curid']}"
            li += (f'<li><b>{cd["titre"][lang]}</b><span>cacherisation/{cd["key"]}.webp · {cd["pub"]} · {cd["lic"]}</span>'
                   f'<span class="liens"><a class="go" href="{url}" target="_blank" rel="noopener">Source</a></span></li>')
        m = re.search(r'(<h2>[^<]*<small>)(\d+)(</small></h2><ul class="liste-lieux">)', s)
        s = s[:m.start()] + m.group(1) + str(int(m.group(2)) + len(retenues)) + m.group(3) + li + s[m.end():]
        p.write_text(s, encoding="utf8")


def planche():
    REPORT.mkdir(parents=True, exist_ok=True)
    try:
        F = ImageFont.truetype("arial.ttf", 22)
        Fb = ImageFont.truetype("arialbd.ttf", 30)
        Fs = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        F = Fb = Fs = ImageFont.load_default()
    cw, ch = 640, 480
    cols, ph = 2, 480 + 170
    rows = (len(CAND) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (cw + 20) + 20, rows * (ph + 20) + 110), "white")
    d = ImageDraw.Draw(sh)
    d.text((20, 18), "Cachérisation : candidates (Wikimedia Commons), recadrées 4:3", font=Fb, fill="black")
    d.text((20, 58), "Retenues : 1 (page services) et 2 (page Pessah). 3 et 4 écartées, motif sous la photo.", font=F, fill="#444")
    for i, c in enumerate(CAND):
        x = 20 + (i % cols) * (cw + 20)
        y = 100 + (i // cols) * (ph + 20)
        sh.paste(recadrer(c).resize((cw, ch), Image.LANCZOS), (x, y))
        d.rectangle((x, y, x + 56, y + 56), fill="black")
        d.text((x + 18, y + 10), str(c["n"]), font=Fb, fill="white")
        yy = y + ch + 8
        d.text((x, yy), f"{c['lic']} · {c['au']}", font=F, fill="black")
        yy += 28
        d.text((x, yy), c["title"].replace("File:", "")[:70], font=Fs, fill="#333")
        yy += 24
        for ln in wrap(c["note"], 74)[:3]:
            d.text((x, yy), ln, font=Fs, fill="#666")
            yy += 22
    sh.save(REPORT / "planche.jpg", quality=88)


if __name__ == "__main__":
    fabriquer_webp()
    for lang, t in T.items():
        print(lang, "services", patch_services(lang, t), "pessah", patch_pessah(lang, t))
    credits()
    if "--planche" in sys.argv:
        planche()
