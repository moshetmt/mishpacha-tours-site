# -*- coding: utf-8 -*-
"""Décisions Moshé du 30/10 (audit du 29/10), idempotent, à relancer après toute régénération :
1. hébreu aligné sur ce que tapent les Israéliens : מג'ב (Megève), קורמאיור (Courmayeur) ; « למהדרין » interdit par le lexique ;
2. page été : titre « Your private kosher summer » (idée Moshé), 4 langues ;
3. fiches chalet : titre en 2 lignes, nom court en blanc + 4 mots dorés (noms choisis par Mendel le 30/10 à 1 h 04 : NOMS)."""
import io, re, glob

HEBREU = [("מז'ב", "מג'ב"), ("קורמאייר", "קורמאיור"), ("כשרות למהדרין", "בהקפדה על כשרות"), ("כשר למהדרין", "שומר כשרות")]

ETE = {  # dossier : (ligne blanche, ligne dorée)
  ".":  ("Your private kosher summer", "the Riviera, the lakes, the Alps"),
  "fr": ("Votre été casher, en privé", "la Riviera, les lacs, les Alpes"),
  "es": ("Su verano kosher, en privado", "la Riviera, los lagos, los Alpes"),
  "he": ("הקיץ הכשר שלכם, באופן פרטי", "הריביירה, האגמים, האלפים"),
}

NOMS = {  # slug : {langue : (nom, 4 mots dorés)}. Noms provisoires jusqu'au choix de Mendel.
  "kosher-chalet-les-deux-alpes": {
    ".":  ("Chalet King David, Les Deux Alpes", "300 m², 16 guests, private chef"),
    "fr": ("Chalet King David, Les Deux Alpes", "300 m², 16 couchages, chef privé"),
    "es": ("Chalet King David, Les Deux Alpes", "300 m², 16 plazas, chef privado"),
    "he": ("צ'אלה קינג דייוויד, לה דז אלפ", "300 מ\"ר, 16 אורחים, שף פרטי")},
  "kosher-slope-chalet-les-deux-alpes": {
    ".":  ("Chalet Rochebrune, Les Deux Alpes", "6 bedrooms, skis on at the door"),
    "fr": ("Chalet Rochebrune, Les Deux Alpes", "6 chambres, skis aux pieds"),
    "es": ("Chalet Rochebrune, Les Deux Alpes", "6 habitaciones, esquís en la puerta"),
    "he": ("צ'אלה רושברון, לה דז אלפ", "6 חדרים, סקי מהדלת")},
  "kosher-chalet-courchevel": {
    ".":  ("Chalet Flocon Doré, Courchevel", "5 suites, heated pools, private chef"),
    "fr": ("Chalet Flocon Doré, Courchevel", "5 suites, piscines chauffées, chef privé"),
    "es": ("Chalet Flocon Doré, Courchevel", "5 suites, piscinas climatizadas, chef privado"),
    "he": ("צ'אלה פלוקון דורה, קורשבל", "5 סוויטות, בריכות מחוממות, שף פרטי")},
  "kosher-chalet-megeve": {
    ".":  ("Chalet Loup Blanc, near Megève", "10 bedrooms facing Mont Blanc"),
    "fr": ("Chalet Loup Blanc, près de Megève", "10 chambres face au Mont-Blanc"),
    "es": ("Chalet Loup Blanc, cerca de Megève", "10 habitaciones frente al Mont Blanc"),
    "he": ("צ'אלה לו בלאן, ליד מג'ב", "10 חדרים מול המון בלאן")},
  "kosher-chalet-val-thorens": {
    ".":  ("Chalet Belle Étoile, Val Thorens", "ski in, ski out, 3 suites"),
    "fr": ("Chalet Belle Étoile, Val Thorens", "skis aux pieds, 3 suites"),
    "es": ("Chalet Belle Étoile, Val Thorens", "esquís en la puerta, 3 suites"),
    "he": ("צ'אלה בל אטואל, ואל טורנס", "סקי עד הדלת, 3 סוויטות")},
}

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
H1 = re.compile(r"<h1>.*?</h1>", re.S)

def h1(p, blanc, dore):
    s = rd(p); n = H1.sub(f"<h1>{blanc}<br><i>{dore}</i></h1>", s, count=1)
    if n != s: wr(p, n); return 1
    return 0

if __name__ == "__main__":
    k = 0
    # 1. hébreu, pages et générateurs
    fichiers = [f for f in glob.glob("he/**/index.html", recursive=True) + glob.glob("he/**/index.md", recursive=True)]
    fichiers += glob.glob("_*.py") + glob.glob("_pages/*.py")
    fichiers = [f for f in fichiers if f != "_retouches_30_10.py"]
    for f in fichiers:
        s = rd(f); n = s
        for a, b in HEBREU: n = n.replace(a, b)
        if n != s: wr(f, n); k += 1
    print("hébreu :", k, "fichiers")
    # 2. été
    k = sum(h1(f"{d}/summer-in-the-alps-jewish-families/index.html", *v) for d, v in ETE.items())
    pg = "_pages/summer-in-the-alps-jewish-families.py"; s = rd(pg)
    n = re.sub(r'h1="[^"]*", ital="[^"]*"', f'h1="{ETE["."][0]}", ital="{ETE["."][1]}"', s, count=1)
    if n != s: wr(pg, n); k += 1
    print("été :", k, "fichiers")
    # 3. chalets
    k = 0
    for slug, langs in NOMS.items():
        for d, (blanc, dore) in langs.items():
            k += h1(f"{d}/{slug}/index.html", blanc, dore)
        pg = f"_pages/{slug}.py"; s = rd(pg)
        n = re.sub(r'h1="[^"]*", ital="[^"]*"', f'h1="{langs["."][0]}", ital="{langs["."][1]}"', s, count=1)
        if n != s: wr(pg, n); k += 1
    print("chalets :", k, "fichiers")
    reste = [f for f in glob.glob("**/index.html", recursive=True) if any(a in rd(f) for a, _ in HEBREU)]
    print("restes hébreu :", len(reste), reste[:5])
