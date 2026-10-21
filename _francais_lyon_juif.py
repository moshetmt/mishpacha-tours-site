"""Menu et pied FR : « Lyon juif » (pas français, Moshé 21/10) devient « Visite juive à Lyon ». Idempotent, après _zones.py.
python _francais_lyon_juif.py [--dry]"""
import pathlib, re, sys

ICI = pathlib.Path(__file__).parent

# Moshé 21/10 : seulement les libellés du menu et du pied ; titres, h1, meta, JSON-LD et texte courant inchangés (SEO)
SOURCES = ["_zones.py"]
REMPLACEMENTS = [
    (">Lyon juif</a>", ">Visite juive à Lyon</a>"),
    (">Guide du Lyon juif</a>", ">Guide juif de Lyon</a>"),
    ("<p>Lyon juif<br>", "<p>Visite juive à Lyon<br>"),
    (">Le guide complet du Lyon juif</a>", ">Le guide juif complet de Lyon</a>"),
    (">visite Lyon juif</a>", ">visite juive à Lyon</a>"),
    ('"Hiver", "Été", "Lyon juif"', '"Hiver", "Été", "Visite juive à Lyon"'),
    ('"Stations", "Guide du Lyon juif"', '"Stations", "Guide juif de Lyon"'),
]


def traiter(f, dry):
    s = f.read_text(encoding="utf-8")
    n = s
    for a, b in REMPLACEMENTS:
        n = n.replace(a, b)
    if n != s:
        if not dry:
            f.write_text(n, encoding="utf-8")
        return 1
    return 0


def main():
    dry = "--dry" in sys.argv
    fichiers = [ICI / s for s in SOURCES] + sorted((ICI / "fr").rglob("*.html"))
    touches = sum(traiter(f, dry) for f in fichiers)
    restes = [(f.relative_to(ICI), m) for f in fichiers for m in re.findall(r">[^<>]{0,30}Lyon juif[^<>]{0,10}</a>|<p>Lyon juif<br>", f.read_text(encoding="utf-8"))]
    print(f"{touches} fichiers modifiés, {len(restes)} restes")
    for r in restes[:30]:
        print("  ", r)


if __name__ == "__main__":
    main()
