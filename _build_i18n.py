# -*- coding: utf-8 -*-
"""Traductions FR / ES / HE.
  python _build_i18n.py prepare   : (re)cree fr/ es/ he/ a partir de TOUTES les pages anglaises (chemins absolus,
                                    lang/dir, canonical, hreflang, selecteur de langue, redirection /merci/),
                                    SANS ecraser un fichier deja traduit (sauf --force) ; ajoute les hreflang aux pages EN.
  python _build_i18n.py ld        : regenere le JSON-LD de chaque page traduite a partir du JSON-LD anglais et du texte traduit
                                    (title, description, FAQ, fil d'Ariane, inLanguage, URL de la langue). A lancer apres toute traduction.
  python _build_i18n.py check     : compare la structure des balises EN / traduit et signale l'anglais residuel.
  python _build_i18n.py repair    : repare les meta content prefixees (bug corrige le 07/10).
A lancer apres chaque build (les builders regenerent les pages EN sans hreflang). Les traducteurs ne touchent pas au JSON-LD.
"""
import os, re, io, sys, html, json, glob

BASE = "https://mishpachatours.com"
LANGS = {"fr": ("Français", "fr", "fr_FR", "ltr"), "es": ("Español", "es", "es_ES", "ltr"), "he": ("עברית", "il", "he_IL", "rtl")}
FORCE = "--force" in sys.argv

def lot():
    pages = [""]
    for p in sorted(glob.glob("**/index.html", recursive=True)):
        d = os.path.dirname(p).replace("\\", "/")
        if not d or d.startswith("_") or d.split("/")[0] in LANGS: continue
        pages.append(d)
    return pages
LOT = lot()

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def strip(s): return html.unescape(re.sub("<[^>]+>", "", s)).strip()

def absolutize(h, page):
    """Chemins relatifs -> absolus depuis la racine du site (href et src seulement)."""
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|mailto:|tel:|#|/|data:|javascript:)", url): return m.group(0)
        parts = [p for p in page.split("/") if p] if page else []
        u = url
        while u.startswith("../"): u = u[3:]; parts = parts[:-1]
        if u.startswith("./"): u = u[2:]
        new = "/" + "/".join(parts + ([u] if u else []))
        return f'{attr}={q}{new}{q}'
    return re.sub(r'\b(href|src)=(["\'])([^"\']*)\2', fix, h)

def alternates(page):
    p = f"/{page}/" if page else "/"
    out = [f'<link rel="alternate" hreflang="en" href="{BASE}{p}">', f'<link rel="alternate" hreflang="x-default" href="{BASE}{p}">']
    for l in LANGS: out.append(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}{p}">')
    return "\n".join(out) + "\n"

def strip_alt(h): return re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', "", h)

def selector(h, page, lang):
    """Reecrit le <details class="langue"> : liens vers la meme page dans chaque langue."""
    p = f"/{page}/" if page else "/"
    def link(l): return p if l == "en" else f"/{l}{p}"
    names = {"en": ("English", "gb", "", "")}
    for l, (n, flag, _, d) in LANGS.items(): names[l] = (n, flag, f' lang="{l}"', f' dir="{d}"' if d == "rtl" else "")
    cur_name, cur_flag = names[lang][0], names[lang][1]
    items = []
    for l in ["en", "fr", "es", "he"]:
        n, flag, la, d = names[l]
        cur = ' aria-current="true"' if l == lang else ""
        items.append(f'<li><a href="{link(l)}"{cur}{la}{d}><img class="drapeau" src="/img/flags/{flag}.svg" alt="" width="20" height="20">{n}</a></li>')
    new = (f'<details class="langue">\n      <summary aria-label="Language: {cur_name}"><img class="drapeau" src="/img/flags/{cur_flag}.svg" alt="" width="20" height="20"><span class="code">{lang.upper()}</span></summary>\n      <ul>\n        '
           + "\n        ".join(items) + "\n      </ul>\n    </details>")
    return re.sub(r'<details class="langue">.*?</details>', new, h, flags=re.S)

RTL = "<style>html[dir=rtl]{overflow-x:hidden}[dir=rtl] h1,[dir=rtl] h2,[dir=rtl] h3,[dir=rtl] .ital,[dir=rtl] em{font-family:'Heebo',sans-serif;font-style:normal}[dir=rtl] .langue ul{left:0;right:auto}[dir=rtl] .ticket h2{text-align:right}[dir=rtl] .rail{scroll-padding-right:var(--pad)}</style>\n"

def prepare():
    for page in LOT:
        src = (page + "/" if page else "") + "index.html"
        if not os.path.exists(src): print("absent", src); continue
        en = rd(src)
        en2 = strip_alt(en)
        en2 = en2.replace("</head>", alternates(page) + "</head>", 1)
        en2 = selector(en2, page, "en")
        if en2 != en: wr(src, en2); print("hreflang", src)
        for lang, (name, flag, locale, d) in LANGS.items():
            dst = f"{lang}/{src}"
            if os.path.exists(dst) and not FORCE:
                t = rd(dst); t2 = selector(strip_alt(t).replace("</head>", alternates(page) + "</head>", 1), page, lang)
                if t2 != t: wr(dst, t2)
                continue
            h = absolutize(en2, page)
            p = f"/{page}/" if page else "/"
            h = re.sub(r"<html[^>]*>", f'<html lang="{lang}"' + (' dir="rtl"' if d == "rtl" else "") + ">", h, 1)
            h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE}/{lang}{p}">', h)
            h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{BASE}/{lang}{p}">', h)
            h = re.sub(r'<meta property="og:locale" content="[^"]*">', "", h)
            h = h.replace('<meta property="og:type"', f'<meta property="og:locale" content="{locale}">\n<meta property="og:type"', 1)
            for q in LOT:
                qp = f"/{q}/" if q else "/"
                h = re.sub(r'href="' + re.escape(qp) + r'(#[^"]*)?"', lambda m: f'href="/{lang}{qp}{m.group(1) or ""}"', h)
            h = h.replace("location.href='/merci/'", f"location.href='/{lang}/merci/'")
            h = selector(h, page, lang)
            if d == "rtl": h = h.replace("</head>", RTL + "</head>", 1)
            h = h.replace("<body", "<body data-i18n=\"todo\"", 1)   # marqueur retire par le traducteur
            wr(dst, h); print("prepare", dst)

def localize_ld(en, tr, lang, page):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', en, re.S)
    if not m: return tr
    data = json.loads(m.group(1)); blocks = data if isinstance(data, list) else [data]
    tm = re.search(r"<title>(.*?)</title>", tr, re.S); title = html.unescape(tm.group(1).split(" | ")[0].strip()) if tm else None
    dm = re.search(r'<meta name="description" content="([^"]*)"', tr); desc = html.unescape(dm.group(1)) if dm else None
    faqs = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p>", tr, re.S)
    fm = re.search(r'<p class="fil">(.*?)</p>', tr, re.S); fil = [strip(x) for x in fm.group(1).split(" / ")] if fm else []
    def urls(o):
        if isinstance(o, dict): return {k: urls(v) for k, v in o.items()}
        if isinstance(o, list): return [urls(v) for v in o]
        if isinstance(o, str) and o.startswith(BASE + "/") and not o.startswith(BASE + "/img/") and not o.startswith(BASE + "/#"):
            return BASE + f"/{lang}" + o[len(BASE):]
        return o
    out = []
    for b in blocks:
        b = dict(b); t = b.get("@type")
        if t == "WebPage":
            b["inLanguage"] = lang
            if title: b["name"] = title
            if desc: b["description"] = desc
        elif t == "FAQPage" and faqs and len(faqs) == len(b.get("mainEntity", [])):
            b["mainEntity"] = [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]
        elif t == "BreadcrumbList" and fil and len(fil) == len(b.get("itemListElement", [])):
            b["itemListElement"] = [dict(it, name=n) for it, n in zip(b["itemListElement"], fil)]
        elif t in ("TouristTrip", "TravelAgency"):
            if t == "TouristTrip" and title: b["name"] = title
            if desc: b["description"] = desc
        out.append(urls(b))
    js = json.dumps(out if isinstance(data, list) else out[0], ensure_ascii=False)
    tag = f'<script type="application/ld+json">{js}</script>'
    if re.search(r'<script type="application/ld\+json">.*?</script>', tr, re.S):
        return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: tag, tr, count=1, flags=re.S)
    return tr.replace("</head>", tag + "\n</head>", 1)

def ld():
    n = 0
    for page in LOT:
        src = (page + "/" if page else "") + "index.html"
        if not os.path.exists(src): continue
        en = rd(src)
        for lang in LANGS:
            dst = f"{lang}/{src}"
            if not os.path.exists(dst): continue
            t = rd(dst)
            if 'data-i18n="todo"' in t: continue
            t2 = localize_ld(en, t, lang, page)
            if t2 != t: wr(dst, t2); n += 1
    print(n, "JSON-LD localises")

def repair():
    """Repare les meta content prefixees par un chemin (bug d'absolutize corrige le 07/10)."""
    for lang in LANGS:
        for page in LOT:
            dst = f"{lang}/" + (page + "/" if page else "") + "index.html"
            if not os.path.exists(dst): continue
            t = rd(dst)
            t2 = re.sub(r'content="/(?:tours/[^/"]+/|merci/|contact/|about/)?(?!/)', 'content="', t)
            if t2 != t: wr(dst, t2); print("repare", dst)

def tags(h):
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style>(?:html)?\[dir=rtl\].*?</style>", "", h, flags=re.S)
    h = re.sub(r'<meta property="og:locale"[^>]*>', "", h)
    return re.findall(r"<(/?[a-zA-Z0-9]+)", h)

RESIDU = ["Free cancellation", "Ask on WhatsApp", "Full details", "Your guide", "Check availability", "Prices per group", "Loading times",
          "Candle lighting in Lyon falls", "Compiled by Mishpacha Tours", "Tap a marker", "Keep reading", "Same-day reply", "Checked 7 October", "Questions we get"]

def check():
    bad = 0
    for page in LOT:
        src = (page + "/" if page else "") + "index.html"
        if not os.path.exists(src): continue
        en = rd(src); te = tags(en)
        for lang in LANGS:
            dst = f"{lang}/{src}"
            if not os.path.exists(dst): print("MANQUE", dst); bad += 1; continue
            t = rd(dst)
            if 'data-i18n="todo"' in t: print("NON TRADUIT", dst); bad += 1; continue
            tt = tags(t)
            if tt != te:
                bad += 1
                i = next((k for k in range(min(len(te), len(tt))) if te[k] != tt[k]), min(len(te), len(tt)))
                print(f"STRUCTURE {dst}: {len(te)} balises EN, {len(tt)} traduit, divergence vers la balise {i} ({te[i:i+3]} / {tt[i:i+3]})")
            if f'<html lang="{lang}"' not in t: print("LANG", dst); bad += 1
            if f'href="{BASE}/{lang}/' not in t: print("CANONICAL", dst); bad += 1
            if "location.href='/merci/'" in t: print("MERCI EN", dst); bad += 1
            if "application/ld+json" in en and (f'"inLanguage": "{lang}"' not in t and "TravelAgency" not in en): print("LD NON LOCALISE", dst); bad += 1
            txt = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", t, flags=re.S)
            for w in ["Israel", "church", "kosher-friendly", "Israeli"]:
                if re.search(r"\b" + w + r"\b", txt): print("INTERDIT", w, dst); bad += 1
            if "—" in txt: print("TIRET CADRATIN", dst); bad += 1
            left = [w for w in RESIDU if w in txt]
            if left: print("ANGLAIS RESIDUEL", dst, left); bad += 1
    print(bad, "problemes")
    return bad

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    {"prepare": prepare, "check": check, "repair": repair, "ld": ld}[cmd]()
