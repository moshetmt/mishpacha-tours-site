# -*- coding: utf-8 -*-
"""Reconstruit le bloc JSON-LD FAQPage des pages fr/ es/ he/ a partir de la FAQ visible (sections .faq, <details><summary>).
Les pages EN ne sont pas touchees. Idempotent : une 2e passe ne change rien.
  python _faq_jsonld_i18n.py          : applique
  python _faq_jsonld_i18n.py --dry    : inventaire seulement
Si une page a un FAQPage mais aucune FAQ visible, le bloc FAQPage est retire (rien n'est invente)."""
import re, io, sys, json, glob, html, os

LANGS = ("fr", "es", "he")
DRY = "--dry" in sys.argv
LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
SEC = re.compile(r'<section[^>]*class="[^"]*\bfaq\b[^"]*"[^>]*>(.*?)</section>', re.S)
DET = re.compile(r"<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>", re.S)
EN = re.compile(r'"@type": "Question", "name": "(How |Can |Do |Is |What |Where |Are |When |Which |Why |Who )')
MARQUEURS = ('"How much', '"Can you', '"Do you')

def texte(h):
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"[ \t\r\n]+", " ", t).strip()   # l'espace insecable du francais est garde

def faq_visible(s):
    main = re.search(r"<main.*?</main>", s, re.S)
    zone = main.group(0) if main else s
    out = []
    for sec in SEC.findall(zone):
        for q, a in DET.findall(sec):
            out.append((texte(q), texte(a)))
    return out

def main():
    stats = {l: {"corrigees": 0, "retirees": 0, "ok": 0} for l in LANGS}
    avant = apres = 0
    for p in sorted(glob.glob("**/index.html", recursive=True)):
        p = p.replace("\\", "/"); lang = p.split("/")[0]
        if lang not in LANGS: continue
        s = io.open(p, encoding="utf-8", newline="").read()   # fins de ligne conservees
        if not any('"FAQPage"' in b for b in LD.findall(s)): continue
        avant += any(m in b for b in LD.findall(s) for m in MARQUEURS)
        faqs = faq_visible(s)
        def refaire(m):
            data = json.loads(m.group(1)); liste = isinstance(data, list); blocs = data if liste else [data]
            out = []
            for b in blocs:
                if b.get("@type") == "FAQPage":
                    if not faqs:
                        stats[lang]["retirees"] += 1; print("RETIRE", p); continue
                    b = dict(b); b["inLanguage"] = lang
                    b["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
                elif b.get("@type") == "WebPage" and b.get("inLanguage") != lang:
                    b = dict(b); b["inLanguage"] = lang; print("LANG  ", p, "WebPage.inLanguage ->", lang)
                out.append(b)
            if not out: return ""
            return f'<script type="application/ld+json">{json.dumps(out if liste else out[0], ensure_ascii=False)}</script>'
        s2 = LD.sub(lambda m: refaire(m) if '"FAQPage"' in m.group(1) else m.group(0), s)
        s2 = s2.replace('\n\n</head>', '\n</head>') if s2 != s else s2
        if s2 != s:
            stats[lang]["corrigees"] += 1
            if not DRY: io.open(p, "w", encoding="utf-8", newline="").write(s2)
        else:
            stats[lang]["ok"] += 1
        apres += any(m in b for b in LD.findall(s2) for m in MARQUEURS) or any(EN.search(b) for b in LD.findall(s2))
    for l in LANGS: print(l, stats[l])
    print("pages non EN avec marqueur anglais dans un JSON-LD : avant", avant, "apres", apres, "(dry)" if DRY else "")

if __name__ == "__main__":
    main()


# 31/10 : nom des blocs ItemList repris du h2 visible (Chabbat à Lyon, Été), 3 langues
ITEMLIST_NOMS = {('fr', 'shabbat-in-lyon'): 'Où prier', ('es', 'shabbat-in-lyon'): 'Dónde rezar', ('he', 'shabbat-in-lyon'): 'איפה מתפללים', ('fr', 'summer-in-the-alps-jewish-families'): 'Où prier et se renseigner', ('es', 'summer-in-the-alps-jewish-families'): 'Dónde rezar y consultar', ('he', 'summer-in-the-alps-jewish-families'): 'איפה מתפללים ומבררים'}
def itemlist_noms():
    k = 0
    for (d, slug), nom in ITEMLIST_NOMS.items():
        p = f"{d}/{slug}/index.html"; s = io.open(p, encoding="utf-8").read()
        n = re.sub(r'"@type": "ItemList", "name": "Where to pray( and ask)?"', f'"@type": "ItemList", "name": "{nom}"', s)
        if n != s: io.open(p, "w", encoding="utf-8", newline="
").write(n); k += 1
    print("ItemList traduits :", k)
if __name__ == "__main__":
    itemlist_noms()
