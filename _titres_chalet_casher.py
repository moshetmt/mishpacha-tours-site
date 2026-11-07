# -*- coding: utf-8 -*-
"""02/11 (brief 00-brief/2026-11-02-pages-chalet-casher-stations-brief.md) : « kosher chalet » dans le title et le H1 des
8 pages chalet et des 4 pages station qui ont des chalets (Courchevel, Les Deux Alpes, Val Thorens, Megève), 4 langues.
Les pages station deviennent les pages « chalet casher <station> » (Search Console 90 j : rien à protéger sur leurs requêtes).

1. <title>, og:title, twitter:title : l'ancien title (lu dans la page) est remplacé partout où il figure (html, md, _pages/*.py).
2. H1 : écrit dans TITRES de _titres_courts.py (sinon la passe suivante l'annulerait), puis _titres_courts.page() pose le H1.
3. llms.txt : texte du lien des pages EN.
Idempotent.   python _titres_chalet_casher.py [--dry]   (depuis site-v5/)"""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
import _titres_courts as tc
tc.DRY = DRY
SUFFIXE = " | Mishpacha Tours"

# slug -> {langue: (title sans suffixe, h1 blanc, h1 doré)}
T = {
 "kosher-chalet-courchevel": {
  "en": ("Kosher Chalet Flocon Doré, Courchevel", "Kosher chalet Flocon Doré", "Courchevel, 5 suites, heated pools"),
  "fr": ("Chalet casher Flocon Doré, Courchevel", "Chalet casher Flocon Doré", "Courchevel, 5 suites, piscines chauffées"),
  "es": ("Chalet kosher Flocon Doré, Courchevel", "Chalet kosher Flocon Doré", "Courchevel, 5 suites, piscinas"),
  "he": ("צ'אלה כשרה פלוקון דורה, קורשבל: בריכות ושף", "צ'אלה כשרה פלוקון דורה", "קורשבל, 5 סוויטות, בריכות מחוממות")},
 "kosher-chalet-courchevel-aurore-boreale": {
  "en": ("Kosher Chalet Aurore Boréale, Courchevel", "Kosher chalet Aurore Boréale", "Courchevel, three suites, heated pool"),
  "fr": ("Chalet casher Aurore Boréale, Courchevel", "Chalet casher Aurore Boréale", "Courchevel, trois suites, piscine chauffée"),
  "es": ("Chalet kosher Aurore Boréale, Courchevel", "Chalet kosher Aurore Boréale", "Courchevel, tres suites, piscina"),
  "he": ("צ'אלה כשרה אורור בוראל, קורשבל: סוויטות ובריכה", "צ'אלה כשרה אורור בוראל", "קורשבל, שלוש סוויטות, בריכה מחוממת")},
 "kosher-chalet-courchevel-renard-argente": {
  "en": ("Kosher Chalet Renard Argenté, Courchevel", "Kosher chalet Renard Argenté", "Courchevel, two suites, Nordic bath"),
  "fr": ("Chalet casher Renard Argenté, Courchevel", "Chalet casher Renard Argenté", "Courchevel, deux suites, bain nordique"),
  "es": ("Chalet kosher Renard Argenté, Courchevel", "Chalet kosher Renard Argenté", "Courchevel, dos suites, baño nórdico"),
  "he": ("צ'אלה כשרה רנאר ארז'נטה, קורשבל: אמבט נורדי", "צ'אלה כשרה רנאר ארז'נטה", "קורשבל, שתי סוויטות, אמבט נורדי")},
 "kosher-chalet-les-deux-alpes": {
  "en": ("Kosher Chalet King David, Les Deux Alpes", "Kosher chalet King David", "Les Deux Alpes, 300 m², private chef"),
  "fr": ("Chalet casher King David, Les Deux Alpes", "Chalet casher King David", "Les Deux Alpes, 300 m², chef privé"),
  "es": ("Chalet kosher King David, Les Deux Alpes", "Chalet kosher King David", "Les Deux Alpes, 300 m², chef privado"),
  "he": ("צ'אלה כשרה קינג דייוויד, לה דז אלפ: שף פרטי", "צ'אלה כשרה קינג דייוויד", 'לה דז אלפ, 300 מ"ר, שף פרטי')},
 "kosher-slope-chalet-les-deux-alpes": {
  "en": ("Kosher Chalet Rochebrune, Les Deux Alpes", "Kosher chalet Rochebrune", "Les Deux Alpes, skis on at the door"),
  "fr": ("Chalet casher Rochebrune, Les Deux Alpes", "Chalet casher Rochebrune", "Les Deux Alpes, à une minute des pistes"),
  "es": ("Chalet kosher Rochebrune, Les Deux Alpes", "Chalet kosher Rochebrune", "Les Deux Alpes, esquís en la puerta"),
  "he": ("צ'אלה כשרה רושברון, לה דז אלפ: סקי מהדלת", "צ'אלה כשרה רושברון", "לה דז אלפ, סקי מהדלת")},
 "kosher-chalet-val-thorens": {
  "en": ("Kosher Chalet Belle Étoile, Val Thorens", "Kosher chalet Belle Étoile", "Val Thorens, ski in, ski out"),
  "fr": ("Chalet casher Belle Étoile, Val Thorens", "Chalet casher Belle Étoile", "Val Thorens, à une minute des pistes"),
  "es": ("Chalet kosher Belle Étoile, Val Thorens", "Chalet kosher Belle Étoile", "Val Thorens, esquís en la puerta"),
  "he": ("צ'אלה כשרה בל אטואל, ואל טורנס: סקי מהדלת", "צ'אלה כשרה בל אטואל", "ואל טורנס, דקה מהמסלולים")},
 "kosher-chalet-les-menuires": {
  "en": ("Kosher Chalet Aigle Royal, Les Ménuires", "Kosher chalet Aigle Royal", "Les Ménuires, seven suites, spa"),
  "fr": ("Chalet casher Aigle Royal, Les Ménuires", "Chalet casher Aigle Royal", "Les Ménuires, sept suites, spa"),
  "es": ("Chalet kosher Aigle Royal, Les Ménuires", "Chalet kosher Aigle Royal", "Les Ménuires, siete suites, spa"),
  "he": ("צ'אלה כשרה אגל רויאל, לה מנואר: ספא וסוויטות", "צ'אלה כשרה אגל רויאל", "לה מנואר, שבע סוויטות, ספא")},
 "kosher-chalet-megeve": {
  "en": ("Kosher Chalet Loup Blanc, near Megève", "Kosher chalet Loup Blanc", "near Megève, facing Mont Blanc"),
  "fr": ("Chalet casher Loup Blanc, près de Megève", "Chalet casher Loup Blanc", "près de Megève, face au Mont-Blanc"),
  "es": ("Chalet kosher Loup Blanc, cerca de Megève", "Chalet kosher Loup Blanc", "cerca de Megève, frente al Mont Blanc"),
  "he": ("צ'אלה כשרה לו בלאן, ליד מג'ב: שף ושבת", "צ'אלה כשרה לו בלאן", "ליד מג'ב, מול המון בלאן")},
 # ---- pages station = pages « chalet casher <station> »
 "kosher-courchevel": {
  "en": ("Kosher Chalets in Courchevel: Chef, Shabbat, Minyan", "Kosher chalets in Courchevel", "1850 and Les 3 Vallées"),
  "fr": ("Chalets casher à Courchevel : chef, repas, Shabbat, minyan", "Chalets casher à Courchevel", "1850 et Les 3 Vallées"),
  "es": ("Chalets kosher en Courchevel: chef, Shabat, minián", "Chalets kosher en Courchevel", "1850 y Les 3 Vallées"),
  "he": ("צ'אלות כשרות בקורשבל: שף פרטי, שבת ומניין", "צ'אלות כשרות בקורשבל", "קורשבל 1850 וכפריה, בשלושת העמקים")},
 "kosher-les-deux-alpes": {
  "en": ("Kosher Chalets in Les Deux Alpes: Chef, Shabbat, Minyan", "Kosher chalets in Les Deux Alpes", "the glacier resort, at 1,650 m"),
  "fr": ("Chalets casher aux Deux Alpes : chef, repas, Shabbat, minyan", "Chalets casher aux Deux Alpes", "la station du glacier, à 1 650 m"),
  "es": ("Chalets kosher en Les Deux Alpes: chef, Shabat, minián", "Chalets kosher en Les Deux Alpes", "la estación del glaciar, a 1.650 m"),
  "he": ("צ'אלות כשרות בלה דז אלפ: שף פרטי, שבת ומניין", "צ'אלות כשרות בלה דז אלפ", "אתר הקרחון, בגובה 1,650 מ'")},
 "kosher-val-thorens": {
  "en": ("Kosher Chalet in Val Thorens: Chef, Shabbat, Minyan", "Kosher chalet in Val Thorens", "Europe's highest resort"),
  "fr": ("Chalet casher à Val Thorens : chef, repas, Shabbat, minyan", "Chalet casher à Val Thorens", "la plus haute d’Europe"),
  "es": ("Chalet kosher en Val Thorens: chef, comidas, Shabat, minián", "Chalet kosher en Val Thorens", "la más alta de Europa"),
  "he": ("צ'אלה כשרה בוואל טורנס: שף פרטי, שבת ומניין", "צ'אלה כשרה בוואל טורנס", "בגובה 2,300 מ', האתר הגבוה באירופה")},
 "kosher-megeve": {
  "en": ("Kosher Chalet near Megève: Chef, Shabbat, Minyan", "Kosher chalet near Megève", "445 km of linked pistes"),
  "fr": ("Chalet casher près de Megève : chef, repas, Shabbat, minyan", "Chalet casher près de Megève", "445 km de pistes reliées"),
  "es": ("Chalet kosher cerca de Megève: chef, Shabat, minián", "Chalet kosher cerca de Megève", "445 km de pistas"),
  "he": ("צ'אלה כשרה ליד מג'ב: שף פרטי, שבת ומניין", "צ'אלה כשרה ליד מג'ב", '445 ק"מ של מסלולים מחוברים')},
}

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    if not DRY: io.open(p, "w", encoding="utf-8", newline="").write(s)

def url(slug, l): return f"/{slug}/" if l == "en" else f"/{l}/{slug}/"

# 1. titles : l'ancien title de chaque page (lu dans sa page) est remplacé dans ses propres fichiers (index.html, index.md),
#    et pour l'EN aussi dans _pages/<slug>.py (EN et ES ont parfois le même ancien title : jamais de remplacement global).
n_tit = n_anc = 0
for slug, langs in T.items():
    for l, (titre, _, _) in langs.items():
        d = url(slug, l).strip("/")
        ancien = re.search(r"<title>(.*?)</title>", rd(d + "/index.html"), re.S).group(1).replace(SUFFIXE, "").strip()
        if ancien == titre: continue
        n_anc += 1
        for f in [d + "/index.html", d + "/index.md"] + ([f"_pages/{slug}.py"] if l == "en" else []):
            if not os.path.exists(f): continue
            s = rd(f); t = s.replace(ancien + SUFFIXE, titre + SUFFIXE).replace(f'"{ancien}"', f'"{titre}"')
            if t != s: wr(f, t); n_tit += 1
print(f"titles : {n_anc} page(s) à retitrer, {n_tit} fichier(s)")

# 2. H1 : TITRES de _titres_courts.py, puis pose
src = rd("_titres_courts.py"); crlf = "\r\n" in src; src = src.replace("\r\n", "\n"); src2 = src
q = lambda x: '"' + x.replace('"', '\\"') + '"'
for slug, langs in T.items():
    for l, (_, blanc, dore) in langs.items():
        u = url(slug, l); ligne = f'  "{u}": ({q(blanc)}, {q(dore)}),'
        m = re.search(r'^  "' + re.escape(u) + r'": \(.*\),$', src2, re.M)
        if m: src2 = src2[:m.start()] + ligne + src2[m.end():]
        else:
            i = src2.index("\n}\n\n# Générateurs de traductions")
            src2 = src2[:i] + "\n" + ligne + src2[i:]
        tc.TITRES[u] = (blanc, dore)
if src2 != src: wr("_titres_courts.py", src2.replace("\n", "\r\n") if crlf else src2); print("_titres_courts.py : TITRES mis à jour")
n_h1 = sum(tc.page(url(s, l), b, d) for s, langs in T.items() for l, (_, b, d) in langs.items())
print(f"H1 : {n_h1} fichier(s)")

# 3. llms.txt : texte du lien des pages EN
s = rd("llms.txt"); t = s
for slug, langs in T.items():
    t = re.sub(r"\[[^\]]*\]\(https://mishpachatours\.com/" + re.escape(slug) + r"/\)",
               lambda _: f"[{langs['en'][0]}](https://mishpachatours.com/{slug}/)", t)
if t != s: wr("llms.txt", t); print("llms.txt mis à jour")
print("(dry)" if DRY else "fait")
