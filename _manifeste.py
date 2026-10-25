# -*- coding: utf-8 -*-
"""Intro « manifeste » des pages noir et or (Moshé 20/10, planche v3, phrase b) : à gauche une phrase en grand, à droite trois lignes
(titre serif + détail) contre un filet or. Ordinateur en deux colonnes ; téléphone en une colonne, la phrase reprend le statement
(filet, bonhomme or lumière). Le paragraphe d'intro reste dans le HTML (p.dk-intro masqué sur les pages noir et or : Google le lit).
Pages : HIVER de _kit_wp.py (23 slugs), 4 langues. Textes FR/ES/HE dans _manifeste_trad.json. Idempotent, `--strip` retire.
À lancer après _intros_courtes.py et avant _mobile_alpes.py."""
import glob, io, json, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from _kit_wp import HIVER
from _lead import STATIONS
STRIP = "--strip" in sys.argv
LANGS = ("fr", "es", "he")
TRAD = json.load(open("_manifeste_trad.json", encoding="utf-8")) if os.path.exists("_manifeste_trad.json") else {}

# phrase b : « Ski by day. Come back to a set table, a minyan, and Shabbat ready. » ; par station : « Ski <station> by day. »
EN = dict(phrase="Ski by day. Come back to a set table, a minyan, and Shabbat ready.",
          phrase_station="Ski {x} by day. Come back to a set table, a minyan, and Shabbat ready.",
          lignes=[("A private chef, or meals delivered", "The kitchen is kashered, every meal of the week is taken care of."),
                  ("Shabbat and the holidays, ready", "Challot, wine, candles, and a minyan with a Sefer Torah on request."),
                  ("One written quote, the same day", "Your resort, your dates, your group. One contact from start to finish.")])
CHALETS = ("kosher-chalets", "kosher-chalet-les-deux-alpes", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-chalet-val-thorens")

def textes(lang, slug):
    t = EN if lang == "en" else TRAD.get(lang)
    if not t: return None
    if slug in STATIONS:
        phrase = t["phrase_station"].format(x=STATIONS[slug][1][lang])
    else:
        phrase = t["phrase"]
    return phrase, t["lignes"]

def bloc(phrase, lignes):
    col = "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in lignes)
    return f'<!--MANIFESTE--><div class="mf"><p class="mf-phrase">{phrase}</p><div class="mf-col">{col}</div></div><!--/MANIFESTE-->'

def page(path, lang, slug):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    s = re.sub(r"<!--MANIFESTE-->.*?<!--/MANIFESTE-->", "", s, flags=re.S)
    if not STRIP:
        t = textes(lang, slug)
        if not t: return "manque"
        m = re.search(r'(<section class="ss wrap lead-intro">.*?<div>)(<p)', s, re.S)
        if not m: return 0
        s = s[:m.end(1)] + bloc(*t) + s[m.end(1):]
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

CSS = """/* ===MANIFESTE=== */
body.kwp-hiver .lead-intro>div>p.dk-intro,body.kwp-hiver .lead-intro>div>p:not(.mf-phrase):not([class*=mf]),body.kwp-hiver .lead-intro>div>.dk-plus-lead{display:none}
body.kwp-hiver .lead-intro>div>.mf+p,body.kwp-hiver .lead-intro>div>.mf~.dk-plus{display:none}
.mf{display:grid;gap:28px}
body.kwp-hiver .lead-intro .mf-phrase,.lead-intro>div>p.mf-phrase{margin:0;font-family:Fraunces,Georgia,serif;font-weight:300;font-size:24px;line-height:1.25;color:#E3BE80;letter-spacing:-.005em}
.mf-col{display:grid;gap:18px;padding-inline-start:20px;border-inline-start:1px solid rgba(201,169,97,.45)}
.mf-col b{display:block;font-family:Fraunces,Georgia,serif;font-weight:300;font-size:19px;line-height:1.2;color:#E3BE80}
.mf-col span{display:block;margin-top:4px;font-size:14px;line-height:1.5;color:#C9D2D4}
@media (max-width:899px){body.kwp-hiver .lead-intro>div::before{display:none}body.kwp-hiver .lead-intro>.lead-mascotte{margin-bottom:14px}}
@media (min-width:900px){
 body.kwp-hiver .lead-intro{display:block;padding:40px 0 36px}
 body.kwp-hiver .lead-intro>.lead-mascotte{display:none}
 body.kwp-hiver .lead-intro>div{max-width:1200px;margin:0 auto}
 .mf{grid-template-columns:1.15fr 1fr;gap:64px;align-items:center}
 body.kwp-hiver .lead-intro .mf-phrase,.lead-intro>div>p.mf-phrase{font-size:44px;line-height:1.14;max-width:22ch}
 .mf-col{gap:24px;padding-inline-start:40px}
 .mf-col b{font-size:24px}
 .mf-col span{font-size:14.5px;margin-top:6px}
}
/* ===/MANIFESTE=== */"""

def css():
    p = "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
    s2 = re.sub(r"\n?/\* ===MANIFESTE=== \*/.*?/\* ===/MANIFESTE=== \*/\n?", "\n", s, flags=re.S)
    if not STRIP:
        i = s2.find("/* ===KIT-WP=== */")
        s2 = (s2[:i] + CSS + "\n" + s2[i:]) if i >= 0 else s2.rstrip("\n") + "\n" + CSS + "\n"
    if s2 != s: io.open(p, "w", encoding="utf-8", newline="\n").write(s2); return 1
    return 0

if __name__ == "__main__":
    n = css(); manque = []
    for slug in HIVER:
        for lang in ("en",) + LANGS:
            p = f"{slug}/index.html" if lang == "en" else f"{lang}/{slug}/index.html"
            if not os.path.exists(p): continue
            r = page(p, lang, slug)
            if r == "manque": manque.append(f"{lang}/{slug}")
            else: n += r
    print(f"_manifeste : {n} fichier(s) modifié(s)" + (f" ; traductions manquantes : {len(manque)}" if manque else ""), "(strip)" if STRIP else "")
