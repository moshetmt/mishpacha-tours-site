# -*- coding: utf-8 -*-
"""Applique les titles et descriptions du CSV d'audit (04-ads-data/2026-10-13-titles-metas-proposes.csv)
   dans les sorties HTML (EN + HE) ET dans les sources (_pages/*.py, _build_*.py) quand la chaine actuelle s'y trouve.
   Met a jour og:title, og:description et le WebPage du JSON-LD EN. python _appliquer_titles.py"""
import csv, io, re, json, glob, html, os
CSV = "../../04-ads-data/2026-10-13-titles-metas-proposes.csv"
GARDER = {("/", "he")}   # title HE de l'accueil garde (choix du 13/10 : nom complet du massif)
rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
SRC = {p: io.open(p, encoding="utf-8").read() for p in glob.glob("_pages/*.py") + glob.glob("_build_*.py")}
touch_src = set(); nb = 0; manq = []
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
for r in rows:
    if r["a_changer"] == "non": continue
    page, lang = r["page"], r["lang"]
    f = ("" if lang == "en" else lang + "/") + page.strip("/") + ("/" if page != "/" else "") + "index.html"
    if not os.path.exists(f): manq.append(f); continue
    h = rd(f); o = h
    t_old, t_new, d_old, d_new = r["title_actuel"], r["title_propose"], r["desc_actuelle"], r["desc_proposee"]
    if (page, lang) in GARDER: t_new = t_old
    if "titre" in r["a_changer"] and t_new != t_old:
        h = re.sub(r"<title>.*?</title>", "<title>" + html.escape(t_new, quote=False) + "</title>", h, count=1, flags=re.S)
        h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(t_new.split(" | ")[0])}">', h, count=1)
    if "desc" in r["a_changer"] and d_new:
        if re.search(r'<meta name="description" content="[^"]*">', h):
            h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(d_new)}">', h, count=1)
        else:
            h = h.replace("<title>", f'<meta name="description" content="{html.escape(d_new)}">\n<title>', 1)
        h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(d_new)}">', h, count=1)
    if lang == "en":
        def ld_fix(m):
            try: data = json.loads(m.group(1))
            except Exception: return m.group(0)
            lst = data if isinstance(data, list) else [data]
            for d in lst:
                if d.get("@type") == "WebPage":
                    if "titre" in r["a_changer"]: d["name"] = t_new.split(" | ")[0]
                    if "desc" in r["a_changer"] and d_new: d["description"] = d_new
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
        h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld_fix, h, count=1, flags=re.S)
        # sources
        for p, s in SRC.items():
            s2 = s
            if "titre" in r["a_changer"] and t_old in s2: s2 = s2.replace(t_old, t_new)
            if "desc" in r["a_changer"] and d_old and d_old in s2: s2 = s2.replace(d_old, d_new)
            if s2 != s: SRC[p] = s2; touch_src.add(p)
    if h != o: wr(f, h); nb += 1
for p in touch_src: wr(p, SRC[p])
print(nb, "pages modifiees ;", len(touch_src), "sources :", sorted(touch_src)); print("manquantes :", manq)
