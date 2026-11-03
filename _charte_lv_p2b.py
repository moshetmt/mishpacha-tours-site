"""Phase 2b (03/11) : phrase courte du bandeau .strip, une ligne sur téléphone, 4 langues.

python _charte_lv_p2b.py [--sec]   (idempotent ; --sec = compte sans écrire)
Ne touche que le contenu de <div class="strip"> ; le ב״ה et le lien restent.
"""
import re, sys, pathlib

ICI = pathlib.Path(__file__).resolve().parent
PHRASES = {
    # Alpes
    "Strictly kosher stays in the Alps, one day-by-day programme.": "Strictly kosher stays in the Alps.",
    "Strictly kosher holidays in the Alps and Lyon, shomer shabbat.": "Strictly kosher stays in the Alps.",
    "Séjours strictement casher dans les Alpes, un programme jour par jour.": "Casher strict dans les Alpes.",
    "Séjours strictement casher dans les Alpes et à Lyon, shomer shabbat.": "Casher strict dans les Alpes.",
    "Estancias estrictamente kosher en los Alpes, un programa día a día.": "Kosher estricto en los Alpes.",
    "Vacaciones estrictamente kosher en los Alpes y Lyon, shomer Shabat.": "Kosher estricto en los Alpes.",
    "חופשות כשרות באלפים, תוכנית מפורטת יום אחר יום.": "חופשות כשרות באלפים.",
    "חופשות כשרות באלפים ובליון. שומר כשרות · שומר שבת.": "חופשות כשרות באלפים.",
    # Lyon
    "Visites privées, du dimanche au vendredi matin.": "Visites privées, dimanche au vendredi matin.",
    ">Check a date on WhatsApp.<": ">Check a date.<",
    ">Vérifier une date sur WhatsApp.<": ">Vérifier une date.<",
    ">Consulte una fecha por WhatsApp.<": ">Consulte una fecha.<",
    ">בדיקת תאריך בוואטסאפ.<": ">בדיקת תאריך.<",
}
STRIP = re.compile(r'<div class="strip">.*?</div>', re.S)


def corrige(bloc):
    for a, b in PHRASES.items():
        bloc = bloc.replace(a, b)
    return bloc


def main():
    sec = "--sec" in sys.argv
    n = 0
    for f in sorted(ICI.rglob("*.html")):
        s = f.read_bytes().decode("utf-8")  # octets bruts : fins de ligne conservées
        t = STRIP.sub(lambda m: corrige(m.group(0)), s)
        if t != s:
            n += 1
            if not sec:
                f.write_bytes(t.encode("utf-8"))
    print(("à modifier" if sec else "modifiées"), n, "pages")


if __name__ == "__main__":
    main()
