# -*- coding: utf-8 -*-
"""Assemble les 8 pages (things-to-do-in-lyon, lyon-weather) x (en, fr, es, he), puis passes ciblees. Lancer depuis n'importe ou.
   python lyon_assemble.py [build|passes|all]"""
import os, re, io, sys, html, json, subprocess, importlib.util
SITE = r"C:\projet site\ads-os\clients\mishpacha-tours\03-website\site-v5"
SP = r"C:/Users/moche/AppData/Local/Temp/claude/C--projet-site-ads-os/519d5c51-7e1d-4c7a-90dc-24830ae876ed/scratchpad"
os.chdir(SITE); sys.path.insert(0, SITE)
SLUGS = ["things-to-do-in-lyon", "lyon-weather"]
LANGS = ("fr", "es", "he")
SIB = "where-to-stay-lyon-jewish-travellers"
RTL_STYLE = None

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

def load_pages(slug):
    sp = importlib.util.spec_from_file_location("p_" + slug.replace("-", "_"), f"_pages/{slug}.py")
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return {"en": m.PAGE, "fr": m.PAGE_FR, "es": m.PAGE_ES, "he": m.PAGE_HE}

def build():
    subprocess.run([sys.executable, "_build_guide.py", *SLUGS], check=True)
    import _build_i18n as I
    import _build_guide as bg
    # ---------- EN : chips vides retirees, hreflang + selecteur (comme prepare)
    en_prep = {}
    for slug in SLUGS:
        p = f"{slug}/index.html"; h = rd(p)
        h = h.replace('<ul class="chips"></ul>', "")
        # bouton WhatsApp flottant : message de la page (comme les autres pages du guide), place apres le bloc Leaflet comme sur ces pages
        fl = re.search(r'<a class="wa-flottant" href="[^"]*"([^>]*)>.*?</a>\s*', h, re.S)
        cta_en = [s_ for s_ in load_pages(slug)["en"]["sections"] if isinstance(s_, dict) and s_.get("type") == "cta"][0]["msg"]
        fl_new = re.sub(r'(<a class="wa-flottant" href=")[^"]*(")', lambda m: m.group(1) + bg.wa(cta_en) + m.group(2), fl.group(0), count=1)
        h = h.replace(fl.group(0), "", 1).replace("</body>", fl_new.rstrip() + "\n</body>", 1)
        h = I.strip_alt(h).replace("</head>", I.alternates(slug) + "</head>", 1)
        h = I.selector(h, slug, "en")
        wr(p, h); en_prep[slug] = h
    # ---------- fr / es / he
    for slug in SLUGS:
        pages = load_pages(slug); en = en_prep[slug]
        for lang in LANGS:
            P = dict(pages[lang]); tmp = f"{SP}/render/{lang}/{slug}"; P["slug"] = tmp
            os.makedirs(tmp, exist_ok=True)
            bg.build(P)
            t = rd(tmp + "/index.html")
            main = t[t.index("<main>") + 6:t.index('<div class="ticket-zone"')]
            main = main.replace('<ul class="chips"></ul>', "")
            main = I.absolutize(main, slug)
            for q in I.LOT:
                qp = f"/{q}/" if q else "/"
                main = re.sub(r'href="' + re.escape(qp) + r'(#[^"]*)?"', lambda m: f'href="/{lang}{qp}{m.group(1) or ""}"', main)
            sib = rd(f"{lang}/{SIB}/index.html")
            sm = sib[sib.index("<main>"):sib.index("</main>")]
            # chaines en dur de _build_guide.py, reprises de la page sœur dans la meme langue
            hero_sib = re.search(r'<p class="cta-hero">.*?<svg[^>]*><use href="#wa"/></svg>(.*?)</a><a class="pill" href="#book">(.*?)</a>', sm, re.S)
            cta_sib = re.search(r'<svg><use href="#wa"/></svg>([^<]*)</a><p class="fiche-note">(.*?)</p>', sm, re.S)
            kr_sib = re.search(r'<h2>([^<]*<i>[^<]*</i>)</h2><ul class="dk-suite"', sm)
            home_sib = re.search(r'<p class="fil"><a href="[^"]*">([^<]*)</a>', sm)
            main = main.replace("</svg>Ask on WhatsApp</a><a class=\"pill\" href=\"#book\">Get a quote</a>", "</svg>" + hero_sib.group(1) + "</a><a class=\"pill\" href=\"#book\">" + hero_sib.group(2) + "</a>")
            main = main.replace("</svg>Ask on WhatsApp</a><p class=\"fiche-note\">Same-day reply, never on Shabbat.</p>", "</svg>" + cta_sib.group(1) + "</a><p class=\"fiche-note\">" + cta_sib.group(2) + "</p>")
            main = main.replace("<h2>Keep <i>reading</i></h2>", "<h2>" + kr_sib.group(1) + "</h2>")
            main = re.sub(r'(<p class="fil"><a href="[^"]*">)Home(</a>)', lambda m: m.group(1) + home_sib.group(1) + m.group(2), main, count=1)
            # tete : copie EN preparee comme _build_i18n.prepare
            h = I.absolutize(en, slug)
            d = I.LANGS[lang][3]
            h = re.sub(r"<html[^>]*>", f'<html lang="{lang}"' + (' dir="rtl"' if d == "rtl" else "") + ">", h, count=1)
            h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{I.BASE}/{lang}/{slug}/">', h)
            h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{I.BASE}/{lang}/{slug}/">', h)
            h = re.sub(r'<meta property="og:locale" content="[^"]*">', "", h)
            h = h.replace('<meta property="og:type"', f'<meta property="og:locale" content="{I.LANGS[lang][2]}">\n<meta property="og:type"', 1)
            h = I.selector(h, slug, lang)
            if d == "rtl": h = h.replace("</head>", I.RTL + "</head>", 1)
            head = h[:h.index("<body")]
            tt = html.escape(P["title"] + " | Mishpacha Tours", quote=True); dd = html.escape(P["desc"], quote=True)
            head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{tt}</title>", head, count=1, flags=re.S)
            head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + tt + m.group(2), head, count=1)
            head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + dd + m.group(2), head, count=1)
            head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + dd + m.group(2), head, count=1)
            pre = sib[sib.index("<body"):sib.index("<main>")].replace(f"/{SIB}/", f"/{slug}/")
            ticket = sib[sib.index('<div class="ticket-zone"'):sib.index("</main>")]
            post = sib[sib.index("</main>"):].replace(f"/{SIB}/", f"/{slug}/")
            if "carte-osm" not in main:   # pas de carte : pas de Leaflet
                post = re.sub(r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet[^>]*>\s*<script src="https://cdnjs[^>]*leaflet[^>]*></script>\s*<script>\s*document\.querySelectorAll\("\.carte-osm"\).*?</script>\s*', "", post, flags=re.S)
            cta_l = [s_ for s_ in P["sections"] if isinstance(s_, dict) and s_.get("type") == "cta"][0]["msg"]
            post = re.sub(r'(<a class="wa-flottant" href=")[^"]*(")', lambda m: m.group(1) + bg.wa(cta_l) + m.group(2), post, count=1)
            DIR = {"fr": "Itinéraire", "es": "Cómo llegar", "he": "הוראות הגעה"}
            post = post.replace("Directions</a>", DIR[lang] + "</a>")
            page = head + pre + "<main>" + chr(10) + main + ticket + post
            ld = I.localize_ld(en, page, lang, slug)
            fq = [s_ for s_ in P["sections"] if isinstance(s_, dict) and s_.get("type") == "faq"][0]["items"]
            mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', ld, re.S); data = json.loads(mm.group(1))
            for b in data:
                if b.get("@type") == "FAQPage":
                    b["mainEntity"] = [{"@type": "Question", "name": bg.strip(q), "acceptedAnswer": {"@type": "Answer", "text": bg.strip(a_)}} for q, a_ in fq]
            ld = ld[:mm.start(1)] + json.dumps(data, ensure_ascii=False) + ld[mm.end(1):]
            wr(f"{lang}/{slug}/index.html", ld)
            print("assemble", lang, slug)

def passes():
    import _zones, _contacts_bh_hebcal as CH, _decor as D, _prefill as PF, _mesure as ME, _kit_wp as KW, _offres_lyon as OF, _ajout_legal_pied as AL
    CH.LYON.add("lyon-weather")
    paths = [f"{l}{s}/index.html" for s in SLUGS for l in ("", "fr/", "es/", "he/")]
    for p in paths:
        AL.patch(p)
    for p in paths: _zones.traiter(p)
    for p in paths: CH.traiter(p)
    # decor : plan depuis l'anglais nu, applique aux 4 langues
    for slug in SLUGS:
        en_nu = D.strip(rd(f"{slug}/index.html")); Pl = D.plan(en_nu, slug)
        for lang, path in [("en", f"{slug}/index.html")] + [(l, f"{l}/{slug}/index.html") for l in LANGS]:
            nu = D.strip(rd(path)); wr(path, D.decorer(nu, Pl, slug, lang))
    for p in paths:
        lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
        t = io.open(p, encoding="utf-8", newline="").read(); t2 = PF.bas(t, lang)
        if t2 != t: io.open(p, "w", encoding="utf-8", newline="").write(t2)
        slug = [s for s in SLUGS if p.endswith(s + "/index.html")][0]
        PF.page(p, slug, lang, {"i": "d"})
    for p in paths: ME.page(p, False)
    TAG = '<script src="/js/anim.js" defer></script>'
    for p in paths:
        s = io.open(p, encoding="utf-8", newline="").read()
        if TAG not in s:
            io.open(p, "w", encoding="utf-8", newline="").write(s.replace("</body>", TAG + "</body>", 1))
    for p in paths: KW.transition(p)
    for p in paths: print(OF.traiter(p, "pose"))
    # fins de ligne : CRLF comme les pages voisines
    for p in paths:
        b = io.open(p, "rb").read().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        io.open(p, "wb").write(b)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("build", "all"): build()
    if cmd in ("passes", "all"): passes()
