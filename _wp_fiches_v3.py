# -*- coding: utf-8 -*-
"""Pages Alpes gérées par Winter Prestige (body.wp-nav, 140 pages) aux couleurs WP, retour Moshé du 04/11/2026 :
- pied de page : lockup Winter Prestige « powered by Mishpacha Tours » en or à la place du bloc Mishpacha, colonnes Lyon (Tours,
  When we run, Good to know : visites et conditions de Lyon, libellés anglais sur les pages FR/ES/HE) retirées, Contact traduit ;
- fiches chalet (32) : bouton « Plan your stay » (barre collante et héros) → « Request the catalogue » vers le PDF du chalet
  (ES → EN, pas de catalogue ES), flocon WP dans la barre collante ;
- feuille wp-v3.css (flocon WP à la place du bonhomme dans les boutons Plan your trip) liée après lv.css.
Le zoom du rail est dans _animations.py (sélecteur .lc-piste img). Idempotent (marqueur WP-V3)."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CAT = {"kosher-chalet-les-deux-alpes": "king-david", "kosher-slope-chalet-les-deux-alpes": "rochebrune", "kosher-chalet-courchevel": "flocon-dore",
       "kosher-chalet-val-thorens": "belle-etoile", "kosher-chalet-megeve": "loup-blanc", "kosher-chalet-les-menuires": "aigle-royal",
       "kosher-chalet-courchevel-aurore-boreale": "aurore-boreale", "kosher-chalet-courchevel-renard-argente": "renard-argente"}
TXT = {"en": "Request the catalogue", "fr": "Demander le catalogue", "es": "Solicitar el catálogo", "he": "לקבלת הקטלוג"}
CONTACT = {"en": "Contact", "fr": "Contact", "es": "Contacto", "he": "צור קשר"}
PB = {"en": "Powered by", "fr": "Propulsé par", "es": "Impulsado por", "he": "מופעל על ידי"}
n_pied = n_fiche = n_css = 0
for f in sorted(glob.glob("**/index.html", recursive=True)):
    f = f.replace("\\", "/")
    s = open(f, encoding="utf-8").read()
    if not re.search(r'<body[^>]*class="[^"]*\bwp-nav\b', s): continue
    o = s; lang = f.split("/")[0] if f.split("/")[0] in ("fr", "es", "he") else "en"
    parts = f.split("/"); slug = parts[-2] if len(parts) > 1 else ""
    # 1. feuille CSS
    if "wp-v3.css" not in s: s = s.replace('<link rel="stylesheet" href="/lv.css">', '<link rel="stylesheet" href="/lv.css"><link rel="stylesheet" href="/wp-v3.css">', 1); n_css += 1
    # 2. pied de page
    if "WP-V3:pied" not in s:
        i = s.find("<footer"); j = s.find("</footer>"); pied = s[i:j]
        pied2 = re.sub(r'<p class="logo-pied">.*?</p>',
            f'<!--WP-V3:pied--><p class="logo-pied wp-v3"><a href="/kosher-chalets/"><img src="/img/wp-long-or-powered.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="320" height="113"></a></p>'
            f'<p class="wp-v3-pb">{PB[lang]} <a href="{"/" if lang == "en" else "/" + lang + "/"}">Mishpacha Tours</a></p><!--/WP-V3:pied-->', pied, count=1, flags=re.S)
        ds = re.findall(r"<details[^>]*>.*?</details>", pied2, re.S)
        for d in ds:
            lab = re.search(r"<summary>([^<]+)</summary>", d).group(1)
            if lab in ("Tours", "When we run", "Good to know"): pied2 = pied2.replace(d, "", 1)
            elif lab == "Contact" and CONTACT[lang] != "Contact": pied2 = pied2.replace(d, d.replace("<summary>Contact</summary>", f"<summary>{CONTACT[lang]}</summary>", 1), 1)
        s = s[:i] + pied2 + s[j:]; n_pied += 1
    # 3. fiches chalet
    if slug in CAT and "WP-V3:fiche" not in s and 'class="lc-colle"' in s:
        pdf = f"/catalogues/{CAT[slug]}-{'en' if lang == 'es' else lang}.pdf"
        s = re.sub(r'<a class="lc-btn lc-noir lc-cta" id="lcCta" href="[^"]*">[^<]*</a>',
                   f'<a class="lc-btn lc-noir lc-cta" id="lcCta" href="{pdf}" target="_blank" rel="noopener">{TXT[lang]}</a>', s, count=1)
        s = re.sub(r'<a class="lc-btn lc-noir lc-mini" href="[^"]*" tabindex="-1">[^<]*</a>',
                   f'<a class="lc-btn lc-noir lc-mini" href="{pdf}" target="_blank" rel="noopener" tabindex="-1">{TXT[lang]}</a>', s, count=1)
        s = s.replace('<div class="lc-colle" id="lcColle" aria-hidden="true"><div>', '<div class="lc-colle" id="lcColle" aria-hidden="true"><!--WP-V3:fiche--><img class="lc-fl" src="/img/wp-flocon-or.svg" alt="" width="26" height="26"><div>', 1)
        assert "WP-V3:fiche" in s and TXT[lang] in s, f
        n_fiche += 1
    if s != o: open(f, "w", encoding="utf-8").write(s)
print("css liée :", n_css, "| pieds refaits :", n_pied, "| fiches :", n_fiche)
