"""Phase 2 lot B1, tache 4 (03/11) : 404.html servie a toute profondeur d'URL.
Chemins ./ -> / ; memes feuilles que la page merci LV (styles, valora, valora-clair, valora-alterne, Jost, lv.css),
sans le bloc Valora en double ni valora-form.css ; plus de hreflang vers /merci/ ; langues vers / /fr/ /es/ /he/. Idempotent."""
import re, pathlib, io

R = pathlib.Path(__file__).parent
P = R / "404.html"
VALORA = ['<link rel="preload" href="/fonts/playfair-latin.woff2" as="font" type="font/woff2" crossorigin>',
          '<link rel="stylesheet" href="/valora-form.css">']


def main():
    t = io.open(P, encoding="utf-8", newline="").read()
    n = re.sub(r'((?:href|src)=")\./', r'\1/', t)
    n = re.sub(r'(srcset="[^"]*")', lambda m: re.sub(r'(^srcset="|,\s*)\./', r'\1/', m.group(1)), n)
    for v in ("/valora.css", "/valora-clair.css", "/valora-alterne.css"):
        tag = f'<link rel="stylesheet" href="{v}">'
        premier = n.find(tag)
        if premier >= 0:
            n = n[:premier + len(tag)] + n[premier + len(tag):].replace(tag, "")
    for tag in VALORA:
        n = n.replace(tag, "")
    n = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="https://mishpachatours\.com/(?:[a-z]{2}/)?merci/">\s*', "", n)
    n = re.sub(r'href="/((?:fr|es|he)/)?merci/"', lambda m: f'href="/{m.group(1) or ""}"', n)
    n = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', "\n\n", n)
    if n != t:
        io.open(P, "w", encoding="utf-8", newline="").write(n)
    reste = re.findall(r'(?:href|src)="\./|merci/|valora-form', n)
    print(f"404 : {'modifiee' if n != t else 'deja a jour'} ; restes ./, merci/, valora-form : {len(reste)} ;",
          "feuilles :", re.findall(r'<link rel="stylesheet" href="([^"]+)"', n))


if __name__ == "__main__":
    main()
