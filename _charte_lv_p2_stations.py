"""Phase 2 lot B1, tache 2 (03/11) : heros des 19 pages station x 4 langues comme l'accueil (lv-hero-station, CSS lot A).
Liste = STATIONS de _zones.py + Les Menuires, sans Annecy (video ete), Grenoble (ville) ni « Anywhere on request ».
Garde image/srcset, data-video, fil d'Ariane, bloc WP, h1, sous-titre ; retire boutons et kwp-hero-wp-tel. Idempotent.
Passe aussi video-pages.js sur .lv-hero-station[data-video]."""
import re, pathlib, io

R = pathlib.Path(__file__).parent
SLUGS = ["kosher-les-deux-alpes", "kosher-courchevel", "kosher-val-thorens", "kosher-les-menuires", "kosher-megeve",
         "kosher-alpe-dhuez", "kosher-val-disere", "kosher-les-arcs", "kosher-la-plagne", "kosher-chamonix",
         "kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana", "kosher-verbier", "kosher-gstaad", "kosher-davos",
         "kosher-cervinia", "kosher-courmayeur", "kosher-cortina"]
EYEBROW = {"en": "The Alps", "fr": "Les Alpes", "es": "Los Alpes", "he": "האלפים"}
# mention reprise telle quelle de l'accueil de chaque langue (.lv-reassure)
REASSURE = {"en": "Strictly kosher · Shomer Shabbat", "fr": "Strictement casher · Chomer Chabbat",
            "es": "Estrictamente kosher · Shomer Shabat", "he": "שומר כשרות · שומר שבת"}


def bloc_section(t, debut):
    prof = 0
    for m in re.finditer(r'<(/?)section\b[^>]*>', t[debut:]):
        prof += -1 if m.group(1) else 1
        if prof == 0:
            return debut + m.end()


def traiter(p, lang):
    t = io.open(p, encoding="utf-8", newline="").read()
    if "lv-hero-station" in t:
        return "deja"
    m = re.search(r'<section class="hero lead-hero3" data-video="([^"]+)">', t)
    if not m:
        return "absent"
    fin = bloc_section(t, m.start())
    h = t[m.start():fin]
    h_sans_tel = re.sub(r'<div class="kwp-hero-wp-tel".*?</div>', '', h, count=1, flags=re.S)
    img = re.search(r'<img [^>]*fetchpriority="high"[^>]*>', h_sans_tel)
    fil = re.search(r'<p class="fil[^"]*">(.*?)</p>', h, re.S)
    wp = re.search(r'<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->', h, re.S)
    h1 = re.search(r'<h1>.*?</h1>', h, re.S)
    sous = re.search(r'</h1>\s*<p>(.*?)</p>', h, re.S)
    if not (img and fil and h1 and sous):
        return "incomplet " + ",".join(k for k, v in (("img", img), ("fil", fil), ("h1", h1), ("sous", sous)) if not v)
    lignes = [f'<section class="hero ac-hero lv-hero-station" data-video="{m.group(1)}">',
              "  " + img.group(0),
              '  <div class="hero-texte">',
              f'    <p class="fil">{fil.group(1)}</p>']
    if wp:
        lignes.append("    " + wp.group(0))
    lignes += [f'    <p class="lv-eyebrow">{EYEBROW[lang]}</p>',
               "    " + h1.group(0),
               f'    <p class="hero-sous">{sous.group(1)}</p>',
               f'    <p class="lv-reassure">{REASSURE[lang]}</p>',
               "  </div>",
               "</section>"]
    n = t[:m.start()] + "\n".join(lignes) + t[fin:]
    io.open(p, "w", encoding="utf-8", newline="").write(n)
    return "modifie"


def video_js():
    p = R / "video-pages.js"
    t = io.open(p, encoding="utf-8", newline="").read()
    n = t.replace("querySelector('.lead-hero3[data-video]')", "querySelector('.lead-hero3[data-video],.lv-hero-station[data-video]')")
    if n != t:
        io.open(p, "w", encoding="utf-8", newline="").write(n)
        return "modifie"
    return "deja" if ".lv-hero-station[data-video]" in t else "SELECTEUR INTROUVABLE"


def main():
    bilan = {}
    for slug in SLUGS:
        for lang in ("en", "fr", "es", "he"):
            p = R / slug / "index.html" if lang == "en" else R / lang / slug / "index.html"
            r = traiter(p, lang) if p.exists() else "fichier absent"
            bilan.setdefault(r, []).append(f"{lang}/{slug}")
    for k, v in bilan.items():
        print(f"stations {k} : {len(v)}" + ("" if k in ("modifie", "deja") else f" {v}"))
    print("video-pages.js :", video_js())


if __name__ == "__main__":
    main()
