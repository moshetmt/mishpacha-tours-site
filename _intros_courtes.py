# -*- coding: utf-8 -*-
"""Pose les intros courtes (19/10, Moshé : « un gros pavé qu'il faut swiper ») dans les pages à bannière 3, 4 langues, sans régénérer.
Source EN = clé intro des modules _pages/<slug>.py ; FR/ES/HE = _intros_courtes_trad.json {lang: {slug: texte}} (agents de traduction).
Pour chaque page : première phrase (premiere_phrase de _lead.py) dans le panneau de la bannière, le reste dans la bande lead-intro.
Idempotent. À lancer avant _mobile_alpes.py. Usage : python _intros_courtes.py [slug ...]"""
import glob, html, importlib.util, io, json, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from _lead import premiere_phrase
LANGS = ("fr", "es", "he")
TRAD = json.load(open("_intros_courtes_trad.json", encoding="utf-8")) if os.path.exists("_intros_courtes_trad.json") else {}

def intro_en(slug):
    p = f"_pages/{slug}.py"
    if not os.path.exists(p): return None
    spec = importlib.util.spec_from_file_location(slug, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.PAGE.get("intro")

def poser(path, intro):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    if "lead-hero3" not in s: return 0
    phrase, reste = premiere_phrase(intro)
    phrase = html.escape(phrase, quote=False)
    m = re.search(r'(<div class="lead3-bloc">.*?<h1>.*?</h1>\s*<p>)(.*?)(</p>)', s, re.S)
    if not m: return 0
    s = s[:m.start(2)] + phrase + s[m.end(2):]
    m = re.search(r'(<section class="ss wrap lead-intro">.*?<div><p[^>]*>)(.*?)(</p>)', s, re.S)
    if not m: return 0
    s = s[:m.start(2)] + (reste or intro) + s[m.end(2):]
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

if __name__ == "__main__":
    only = set(sys.argv[1:])
    n = 0; manque = []
    for p in sorted(glob.glob("**/index.html", recursive=True)):
        p = p.replace("\\", "/")
        parts = p.split("/")
        if parts[0].startswith("_") or "preview" in parts: continue
        lang = parts[0] if parts[0] in LANGS else "en"
        slug = "/".join(parts[1:-1] if lang != "en" else parts[:-1])
        if not slug or (only and slug not in only): continue
        en = intro_en(slug)
        if not en: continue
        intro = en if lang == "en" else TRAD.get(lang, {}).get(slug)
        if not intro: manque.append(f"{lang}/{slug}"); continue
        n += poser(p, intro)
    print(f"_intros_courtes : {n} page(s) modifiée(s)" + (f" ; traductions manquantes : {len(manque)} ({', '.join(manque[:6])}…)" if manque else ""))
