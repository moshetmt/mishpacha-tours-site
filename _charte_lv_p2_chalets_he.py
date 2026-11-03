"""Phase 2 lot B1, tache 3 (03/11) : 4 fiches chalet HE dont le h2 « a lire aussi » contient le JS du formulaire
(<h2>document.querySelectorAll('.lead-form')... <i>להמשך</i></h2>).
Origine : traduction HE de he/kosher-chalet-val-thorens (commit 5e22364, segments decales : « Keep » a recu le texte du
<script>, « reading » le mot להמשך), puis clonage de cette page par _chalet_aigle_royal.py et _chalets_courchevel_lot2.py.
On remet le titre des fiches saines : להמשך <i>קריאה</i>. Le <script> n'est PAS remis : les formulaires lead-plan de ces
pages vont vers /he/plan-your-trip/ (comme sur les fiches HE saines et l'EN, qui n'ont pas ce script) ; il detournerait
l'envoi vers WhatsApp. Idempotent."""
import re, pathlib, io

R = pathlib.Path(__file__).parent
CASSE = re.compile(r"<h2>document\.querySelectorAll\('\.lead-form'\)\.forEach\(.*?\}\)\}\);\s*<i>להמשך</i></h2>", re.S)
BON = "<h2>להמשך <i>קריאה</i></h2>"
CASSE_MD = re.compile(r"^## document\.querySelectorAll\('\.lead-form'\).*?\*להמשך\*[ \t]*(?=\r?$)", re.M)
BON_MD = "## להמשך *קריאה*"


def main():
    modif = 0
    for p in sorted(list((R / "he").rglob("index.html")) + list((R / "he").rglob("index.md"))):
        t = io.open(p, encoding="utf-8", newline="").read()
        n = CASSE.sub(BON, t) if p.suffix == ".html" else CASSE_MD.sub(BON_MD, t)
        if n != t:
            io.open(p, "w", encoding="utf-8", newline="").write(n)
            modif += 1
            print("  repare :", p.relative_to(R))
    # controle : aucun <h2 de he/ (html et md) ne contient du JavaScript
    reste = []
    for p in list((R / "he").rglob("index.html")) + list((R / "he").rglob("index.md")):
        t = io.open(p, encoding="utf-8").read()
        for h in re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S) + re.findall(r"^##\s.*$", t, re.M):
            if re.search(r"function\(|document\.|\bvar ", h):
                reste.append(str(p.relative_to(R)))
    print(f"chalets HE : {modif} pages reparees ; h2 HE avec JavaScript restants : {len(reste)} {reste[:5]}")


if __name__ == "__main__":
    main()
