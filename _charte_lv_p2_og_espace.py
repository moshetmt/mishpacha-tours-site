"""Phase 2 lot B1, tache 6 (03/11) : image de partage WhatsApp de l'Espace Mendel (og-alpes-v4, choix de Moshe).
Copie vers img/og-espace.jpg et balises og/twitter dans espace/index.html (la page n'en avait aucune). Idempotent."""
import pathlib, io, shutil, re
from PIL import Image

R = pathlib.Path(__file__).parent
SRC = R.parent.parent / "06-reports" / "2026-11-03-image-partage" / "og-alpes-v4.jpg"
DST = R / "img" / "og-espace.jpg"
URL = "https://mishpachatours.com/img/og-espace.jpg"


def main():
    copie = not DST.exists() or DST.read_bytes() != SRC.read_bytes()
    if copie:
        shutil.copyfile(SRC, DST)
    w, h = Image.open(DST).size
    p = R / "espace" / "index.html"
    t = io.open(p, encoding="utf-8", newline="").read()
    bloc = ('<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="Espace Mendel · Winter Prestige">\n'
            f'<meta property="og:image" content="{URL}">\n'
            f'<meta property="og:image:width" content="{w}">\n'
            f'<meta property="og:image:height" content="{h}">\n'
            '<meta property="og:image:type" content="image/jpeg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{URL}">\n')
    n = re.sub(r'(?:<meta (?:property|name)="(?:og|twitter):[^"]+" content="[^"]*">\n)+', "", t)
    n = n.replace("<style>", bloc + "<style>", 1)
    if n != t:
        io.open(p, "w", encoding="utf-8", newline="").write(n)
    print(f"og espace : image {'copiee' if copie else 'deja la'} ({w}x{h}), page {'modifiee' if n != t else 'deja a jour'}")


if __name__ == "__main__":
    main()
