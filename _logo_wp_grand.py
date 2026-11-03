# -*- coding: utf-8 -*-
"""Logo Winter Prestige en grand sur les pages Alpes (Mendel Attal, 03/11/2026). Idempotent : un bloc deja pose n'est pas repose.
   PERIMETRE (meme regle que _og_wp.py) : <body> avec la classe kwp-hiver ou kwp-ete, ou HTML contenant <!--KIT-WP:hero-->.
   1. Signature « A Winter Prestige chalet » (flocon wp-flocon-or.svg + texte) sous le H1 du heros des pages chalet
      (dossiers kosher-chalet-*/ et kosher-slope-chalet-*/, 4 langues), bloc <!--LOGO-WP:sign-->...<!--/LOGO-WP:sign-->.
   2. Pied de page : « with Winter Prestige » en texte devient le logo wp-long-or.svg precede de with / avec / con / עם,
      bloc <!--LOGO-WP:pied-->...<!--/LOGO-WP:pied-->. Le logo Mishpacha Tours reste en premier.
   3. En-tete co-marque (demande Moshe 03/11) : filet dore + flocon + « WINTER PRESTIGE / Powered by Mishpacha Tours » a droite du logo
      Mishpacha Tours, bloc <!--LOGO-WP:entete--> (HTML present des le chargement ; mini script inline : animation une fois par visite, cle
      sessionStorage wpEntete, jamais si prefers-reduced-motion cote CSS).
   4. Le CSS (heros ordinateur plus large, signature, pied) est dans lv.css, bloc ===LOGO-WP-2026-11-03===.
   Python systeme, depuis site-v5/ : python _logo_wp_grand.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LANGS = ("fr", "es", "he")
SIGNATURE = {"en": "A Winter Prestige chalet", "fr": "Un chalet Winter Prestige", "es": "Un chalet Winter Prestige", "he": "צ'אלה של Winter Prestige"}
AVEC = {"en": "with", "fr": "avec", "es": "con", "he": "עם"}
SUFFIXE = {"en": " · with Winter Prestige", "fr": " · avec Winter Prestige", "es": " · con Winter Prestige", "he": " · עם Winter Prestige"}

def lang_slug(rel):
    p = rel.split("/")[:-1]
    lang = p[0] if p and p[0] in LANGS else "en"
    return lang, "-".join(p[1:] if lang != "en" else p)

def dans_perimetre(h):
    """kwp-hiver / kwp-ete, ou bloc KIT-WP:hero. Exclu : le bloc porte le logo Summer Prestige (villa de Saint-Tropez, /img/sp-)."""
    b = re.search(r"<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->", h, re.S)
    if b and "/img/sp-" in b.group(0): return False
    return bool(re.search(r'<body[^>]*class="[^"]*kwp-(hiver|ete)', h)) or "<!--KIT-WP:hero-->" in h

def est_chalet(slug):
    return slug.startswith(("kosher-chalet-", "kosher-slope-chalet-"))

def main():
    cnt = {"sign": {}, "pied": {}, "entete": {}}
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        if rel.startswith("_") or rel == "index.html": continue
        h = open(f, encoding="utf-8").read()
        if not dans_perimetre(h): continue
        lang, slug = lang_slug(rel)
        n = h
        if est_chalet(slug) and "<!--LOGO-WP:sign-->" not in n:
            bloc = ('<!--LOGO-WP:sign--><div class="wp-signature"><img src="/img/wp-flocon-or.svg" alt="" width="28" height="28">'
                    f'<span>{SIGNATURE[lang]}</span></div><!--/LOGO-WP:sign-->')
            n2 = re.sub(r'(<section class="hero.*?</h1>)', lambda m: m.group(1) + bloc, n, count=1, flags=re.S)
            if n2 != n: n = n2; cnt["sign"][lang] = cnt["sign"].get(lang, 0) + 1
        if "<!--LOGO-WP:pied-->" not in n:
            def pied(m):
                texte = m.group(2)
                if not texte.endswith(SUFFIXE[lang].strip(" ")) and SUFFIXE[lang] not in texte: return m.group(0)
                base = texte.replace(SUFFIXE[lang], "")
                return (m.group(1) + '<!--LOGO-WP:pied--><small>' + base + '</small><span class="wp-pied"><em>' + AVEC[lang] +
                        '</em><span class="wp-pied-logo"><img src="/img/wp-long-or.svg" alt="Winter Prestige" width="172" height="61"></span></span><!--/LOGO-WP:pied--></p>')
            n2 = re.sub(r'(<p class="logo-pied">.*?<span class="mot"[^>]*>[^<]*</span>)<small>([^<]*)</small></p>', pied, n, count=1, flags=re.S)
            if n2 != n: n = n2; cnt["pied"][lang] = cnt["pied"].get(lang, 0) + 1
        if "<!--LOGO-WP:entete-->" not in n:
            bloc = ('<!--LOGO-WP:entete--><script>try{if(!sessionStorage.getItem("wpEntete")){sessionStorage.setItem("wpEntete","1");document.documentElement.classList.add("wp-anim")}}catch(e){}</script>'
                    '<div class="wp-entete"><img src="/img/wp-flocon-or.svg" alt="" width="34" height="34"><span class="wp-e-txt"><b translate="no">Winter Prestige</b><small translate="no">Powered by Mishpacha Tours</small></span></div><!--/LOGO-WP:entete-->')
            n2 = re.sub(r'(<header class="nav">\s*<a class="logo".*?</a>)', lambda m: m.group(1) + bloc, n, count=1, flags=re.S)
            if n2 != n: n = n2; cnt["entete"][lang] = cnt["entete"].get(lang, 0) + 1
        if n != h: open(f, "w", encoding="utf-8", newline="").write(n)
    print("signatures posees :", cnt["sign"], "| pieds de page :", cnt["pied"], "| en-tetes :", cnt["entete"])

if __name__ == "__main__": main()
