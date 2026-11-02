# -*- coding: utf-8 -*-
"""Décisions de Moshé du 02/11/2026, 4 langues, pages ET sources (_pages/*.py, _build_*.py). Idempotent.
    python _fix_i18n_2026_11_02_b.py          : applique et écrit le journal E:/tmp-zones-apres/journal_b.txt
    python _fix_i18n_2026_11_02_b.py --sec    : montre, n'écrit rien
1. Durée : Jewish Lyon, Mémoire CHRD et Mémoire Montluc + Neveh Shalom passent de 2 h 30 à 2 h (décision du 26/10,
   01-emails/2026-10-26-fiches-ota/guide-getyourguide.md). Un « 2 h 30 » est laissé quand son voisinage parle de route,
   d'aéroport, de train ou d'une station (temps de trajet), ou d'une autre visite (Izieu, Stopover).
2. Rabbin Daniel Belaïch : plus jamais présenté comme contact (ETAT, 15/10 : ne pas le contacter) ; mail, nom et
   invitations à lui écrire retirés ; le fait (office Chabad l'hiver à Courchevel et Megève) reste."""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEC = "--sec" in sys.argv
JOURNAL = []

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# ---------- 1. durée ----------
NB = r"[ \u00a0]"
MOTIFS = [  # (motif, remplacement) ; une fonction quand l'anglais demande « 2-hour » devant un nom
    (re.compile(r"2 hours 30 minutes"), "2 hours"),
    (re.compile(r"2 hours 30"), "2 hours"),
    (re.compile(r"two and a half hours"), "two hours"),
    (re.compile(r"2\.5 hours"), "2 hours"),
    (re.compile(r"deux heures et demie"), "deux heures"),
    (re.compile(r"dos horas y media"), "dos horas"),
    (re.compile(r"2,5 horas"), "2 horas"),
    (re.compile(r"שעתיים וחצי"), "שעתיים"),
    (re.compile(r"d’2" + NB + r"h" + NB + r"30"), lambda m: "de 2" + m.group(0)[3] + "h"),
    (re.compile(r"2,5" + NB + r"h\b"), lambda m: "2" + m.group(0)[3] + "h"),
    (re.compile(r"\(2\.5 h\)"), "(2 h)"),                 # libellé du formulaire (valeur envoyée à la feuille)
    (re.compile(r"Jewish Lyon 2\.5 h\b"), "Jewish Lyon 2 h"),   # llms.txt et _build_sitemap.py
    (re.compile(r"\(2\.5 שעות\)"), "(שעתיים)"),
    (re.compile(r"(?<![\d:])2h30\b|(?<![\d:])2" + NB + r"h" + NB + r"30\b"), "DUREE"),
]
NOM_EN = re.compile(r"[ \u00a0](walk|walking|visit|city|Jewish|tour|private)\b")
HORS = re.compile(r"road|par la route|de route|route\.svg|carretera|by car|traffic|tráfico|circulation|\bkm\b|airport|aéroport|aeropuerto|Saint-Exup|Exupéry|"
                  r"Geneva|Genève|Ginebra|Gen[eè]ve|Malpensa|Innsbruck|Zurich|Val Thorens|Morzine|Alpe d'Huez:|train|tren|"
                  r"Méribel|j2ski|Alps2Alps|transfer|sites give|skiresort|luxury-travel|brief's|"
                  r"\b[1-4] h (?:0\d|1\d|2\d|4\d|5\d)\b|\b2 h (?:to|à|a)\b|"   # une autre durée de trajet juste à côté (2 h 15 à 2 h 30)
                  r"כביש|בנסיעה|נמל התעופה|שדה תעופה|ז'נבה|מג'נבה|ממילאנו|אינסברוק|ברכבת|פקקים|ואל טורנס|אקזופרי", re.I)
ANGLAIS = lambda chemin: not re.match(r"(fr|es|he)[\\/]", chemin)

def duree(chemin, s):
    def sub(motif, rempl, s):
        def f(m):
            av, ap = s[max(0, m.start() - 110):m.start()], s[m.end():m.end() + 60]
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", av + "«" + m.group(0) + "»" + ap))
            if HORS.search(av[-110:] + ap):
                JOURNAL.append(f"LAISSÉ  {chemin} | {ctx} | trajet ou autre visite"); return m.group(0)
            if rempl == "DUREE":
                sp = "\u00a0" if "\u00a0" in m.group(0) else " "
                autre = chemin.endswith(".py") and re.search(r"[àéèçñáíóú’]|[֐-׿]", av[-80:] + ap)   # texte traduit dans un script
                if not ANGLAIS(chemin) or autre:
                    n = "2" + sp + "h"
                else:
                    n = "2-hour" if NOM_EN.match(ap) else "2 hours"
            else:
                n = rempl(m) if callable(rempl) else rempl
            JOURNAL.append(f"MODIFIÉ {chemin} | {ctx} → {n}"); return n
        return motif.sub(f, s)
    for motif, rempl in MOTIFS:
        s = sub(motif, rempl, s)
    return s

# ---------- 2. Belaïch ----------
B = []   # (fichier, avant, après)
def R(fichiers, avant, apres):
    for f in fichiers.split(): B.append((f, avant, apres))

H, P = "index.html index.md", "_pages/"
# jewish-life-around-lyon
for l, a1, b1, a2, b2 in (
    ("", "Winter season only. Rabbi Daniel Belaïch. Help with kosher needs, wine and challot for Shabbat.", "Winter season only.",
         "Winter season. Contact habadalpes@yahoo.fr before you come: the venue has changed over the years.", "Winter season. The venue has changed over the years: ask us before you come."),
    ("fr/", "Saison d’hiver uniquement. Rabbin Daniel Belaïch. Aide pour les besoins casher, le vin et les challot du Shabbat.", "Saison d’hiver uniquement.",
            "Saison d’hiver. Contactez habadalpes@yahoo.fr avant de venir : le lieu a changé au fil des ans.", "Saison d’hiver. Le lieu a changé au fil des ans : demandez-nous avant de venir."),
    ("es/", "Solo en temporada de invierno. Rabino Daniel Belaïch. Ayuda con las necesidades kosher, vino y jalot para Shabat.", "Solo en temporada de invierno.",
            "Temporada de invierno. Contacte con habadalpes@yahoo.fr antes de ir: el lugar ha cambiado con los años.", "Temporada de invierno. El lugar ha cambiado con los años: pregúntenos antes de ir."),
    ("he/", "עונת החורף בלבד. הרב דניאל בלעיש (Daniel Belaïch). עזרה בצרכי כשרות, יין וחלות לשבת.", "עונת החורף בלבד.",
            "עונת החורף. פנו אל habadalpes@yahoo.fr לפני שאתם מגיעים: המקום השתנה עם השנים.", "עונת החורף. המקום השתנה עם השנים: שאלו אותנו לפני שאתם מגיעים.")):
    for x in H.split():
        R(f"{l}jewish-life-around-lyon/{x}", a1, b1); R(f"{l}jewish-life-around-lyon/{x}", a2, b2)
R("_build_hub.py", "Winter season only. Rabbi Daniel Belaïch. Help with kosher needs, wine and challot for Shabbat.", "Winter season only.")
R("_build_hub.py", "Winter season. Contact habadalpes@yahoo.fr before you come: the venue has changed over the years.", "Winter season. The venue has changed over the years: ask us before you come.")

# kosher-courchevel
for l, a, b in (
    ("", "Rabbi Daniel Belaïch holds services at the Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, during the winter season. He writes that he helps with kosher needs, wine and challot for Shabbat.",
         "Services are held at the Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, during the winter season."),
    ("fr/", "Le rabbin Daniel Belaïch dirige des offices à l’Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, pendant la saison d’hiver. Il écrit qu’il aide pour les besoins casher, le vin et les challot de Shabbat.",
            "Des offices ont lieu à l’Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, pendant la saison d’hiver."),
    ("es/", "El rabino Daniel Belaïch dirige los oficios en el Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, durante la temporada de invierno. Escribe que ayuda con las necesidades kosher, el vino y las jalot para Shabat.",
            "Hay oficios en el Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, durante la temporada de invierno."),
    ("he/", "הרב דניאל בלאיש מקיים תפילות במלון Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, בעונת החורף. הוא כותב שהוא מסייע בצרכים כשרים, ביין ובחלות לשבת.",
            "בעונת החורף מתקיימות תפילות במלון Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel.")):
    for x in H.split(): R(f"{l}kosher-courchevel/{x}", a, b)
R(P + "kosher-courchevel.py", "Rabbi Daniel Belaïch holds services at the Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, during the winter season. He writes that he helps with kosher needs, wine and challot for Shabbat.",
  "Services are held at the Hôtel Le Mont Charvin, 389 rue des Tovets, 73120 Courchevel, during the winter season.")

# kosher-ski-holidays-french-alps
SKI = {
    "": [(", run by Rabbi Daniel Belaïch.", "."),
         ("In winter, Rabbi Daniel Belaïch runs Chabad services in Courchevel 1850 and Megève.", "In winter, Chabad services are held in Courchevel 1850 and Megève."),
         (" Both are run by Rabbi Daniel Belaïch (habadalpes@yahoo.fr).", ""),
         ("Synagogue at Hôtel Le Mont Charvin, Rabbi Daniel Belaïch", "Synagogue at Hôtel Le Mont Charvin"),
         ("Chabad of the Alps in Megève, Rabbi Daniel Belaïch", "Chabad of the Alps in Megève"),
         ("Winter. habadalpes@yahoo.fr. Venue: confirm before you come", "Winter. Venue: confirm with us before you come")],
    "fr/": [(", assuré par le rabbin Daniel Belaïch.", "."),
            ("En hiver, le rabbin Daniel Belaïch assure des offices Chabad à Courchevel 1850 et à Megève.", "En hiver, des offices Chabad ont lieu à Courchevel 1850 et à Megève."),
            (" Les deux sont assurés par le rabbin Daniel Belaïch (habadalpes@yahoo.fr).", ""),
            ("Synagogue de l’hôtel Le Mont Charvin, rabbin Daniel Belaïch", "Synagogue de l’hôtel Le Mont Charvin"),
            ("Chabad des Alpes à Megève, rabbin Daniel Belaïch", "Chabad des Alpes à Megève"),
            ("Hiver. habadalpes@yahoo.fr. Lieu : à confirmer avant de venir", "Hiver. Lieu : à confirmer avec nous avant de venir")],
    "es/": [(", dirigido por el rabino Daniel Belaïch.", "."),
            ("En invierno, el rabino Daniel Belaïch dirige los servicios de Chabad en Courchevel 1850 y en Megève.", "En invierno hay servicios de Chabad en Courchevel 1850 y en Megève."),
            (" Ambos los dirige el rabino Daniel Belaïch (habadalpes@yahoo.fr).", ""),
            ("Sinagoga en el Hôtel Le Mont Charvin, rabino Daniel Belaïch", "Sinagoga en el Hôtel Le Mont Charvin"),
            ("Chabad de los Alpes en Megève, rabino Daniel Belaïch", "Chabad de los Alpes en Megève"),
            ("Invierno. habadalpes@yahoo.fr. Local: confirme antes de ir", "Invierno. Local: confírmelo con nosotros antes de ir")],
    "he/": [(", בניהול הרב דניאל בלאיש.", "."),
            ("בחורף מפעיל הרב דניאל בלאיש (Daniel Belaïch) שירותי חב״ד בקורשבל 1850 (Courchevel) ובמג'ב (Megève).", "בחורף מתקיימים שירותי חב״ד בקורשבל 1850 (Courchevel) ובמג'ב (Megève)."),
            ("<p>את שניהם מפעיל הרב דניאל בלאיש (habadalpes@yahoo.fr).</p>", "<p>בשני אתרים יש שירות חב״ד בחורף.</p>"),
            ("בית כנסת במלון Le Mont Charvin, הרב דניאל בלאיש", "בית כנסת במלון Le Mont Charvin"),
            ("חב״ד האלפים במג'ב, הרב דניאל בלאיש", "חב״ד האלפים במג'ב"),
            ("חורף. habadalpes@yahoo.fr. המקום: אשרו לפני שאתם מגיעים", "חורף. המקום: אשרו איתנו לפני שאתם מגיעים")],
}
for l, paires in SKI.items():
    for a, b in paires:
        for x in H.split(): R(f"{l}kosher-ski-holidays-french-alps/{x}", a, b)
    # noms anglais du bloc ItemList (JSON-LD), identiques dans les 4 langues
    for a, b in SKI[""][3:5]:
        R(f"{l}kosher-ski-holidays-french-alps/index.html", a, b)
R(P + "kosher-ski-holidays-french-alps.py", "In winter, Rabbi Daniel Belaïch runs Chabad services in Courchevel 1850 and Megève.", "In winter, Chabad services are held in Courchevel 1850 and Megève.")
R(P + "kosher-ski-holidays-french-alps.py", " Both are run by Rabbi Daniel Belaïch (habadalpes@yahoo.fr, 06 20 60 72 58).", "")
R(P + "kosher-ski-holidays-french-alps.py", "The rabbi writes that he helps with kosher needs, wine ", "Kosher needs, wine ")
R(P + "kosher-ski-holidays-french-alps.py", "Synagogue at Hôtel Le Mont Charvin, Rabbi Daniel Belaïch\", \"389 rue des Tovets, 73120 Courchevel\", \"06 20 60 72 58\"", "Synagogue at Hôtel Le Mont Charvin\", \"389 rue des Tovets, 73120 Courchevel\", \"\"")
R(P + "kosher-ski-holidays-french-alps.py", "Chabad of the Alps in Megève, Rabbi Daniel Belaïch\", \"136 route Edmond de Rothschild, 74120 Megève\", \"06 20 60 72 58\", \"Winter. habadalpes@yahoo.fr. Venue: confirm before you come\"",
  "Chabad of the Alps in Megève\", \"136 route Edmond de Rothschild, 74120 Megève\", \"\", \"Winter. Venue: confirm with us before you come\"")
R(P + "kosher-ski-holidays-french-alps.py", ", run by Rabbi Daniel Belaïch.", ".")

R("he/kosher-ski-holidays-french-alps/index.md", "את שניהם מפעיל הרב דניאל בלאיש (habadalpes@yahoo.fr).", "בשני אתרים יש שירות חב״ד בחורף.")

# français : espace insécable avant les deux-points
for x in H.split():
    R(f"fr/jewish-life-around-lyon/{x}", "Saison d’hiver. Contactez habadalpes@yahoo.fr avant de venir : le lieu a changé au fil des ans.", "Saison d’hiver. Le lieu a changé au fil des ans : demandez-nous avant de venir.")
    R(f"fr/kosher-ski-holidays-french-alps/{x}", "Hiver. habadalpes@yahoo.fr. Lieu : à confirmer avant de venir", "Hiver. Lieu : à confirmer avec nous avant de venir")
R(P + "kosher-ski-holidays-french-alps.py", "Rabbi Belaïch phone 06 20 60 72 58: synalpes. The base factuelle also gives 06 29 47 39 80, not published here.", "Chabad phone numbers (synalpes, base factuelle): not published here, contact not to be used (Moshé, 15/10).")

# summer-in-the-alps-jewish-families
ETE = {
    "": [("Nothing says they run in summer. Write to Rabbi Daniel Belaïch (habadalpes@yahoo.fr) before you count on one.", "Nothing says their winter Chabad services run in summer: ask us before you count on one."),
         ("Write to Rabbi Belaïch before you plan around one.", "Nothing says they do. Ask us before you plan around one.")],
    "fr/": [("Rien n’indique qu’ils fonctionnent l’été. Écrivez au rabbin Daniel Belaïch (habadalpes@yahoo.fr) avant de compter sur l’un d’eux.", "Rien n’indique que leurs offices Chabad d’hiver ont lieu l’été : demandez-nous avant de compter sur l’un d’eux."),
            ("Écrivez au rabbin Belaïch avant de bâtir un projet autour de l’un d’eux.", "Rien ne l’indique. Demandez-nous avant de bâtir un projet autour de l’un d’eux.")],
    "es/": [("Nada indica que funcionen en verano. Escriba al rabino Daniel Belaïch (habadalpes@yahoo.fr) antes de contar con uno.", "Nada indica que sus servicios de Chabad de invierno funcionen en verano: pregúntenos antes de contar con uno."),
            ("Escriba al rabino Belaïch antes de planificar en torno a uno.", "Nada lo indica. Pregúntenos antes de planificar en torno a uno.")],
    "he/": [("שום דבר לא מעיד שהם פועלים בקיץ. כתבו להרב דניאל בלעיש (Daniel Belaïch), habadalpes@yahoo.fr, לפני שאתם מסתמכים על אחד מהם.", "שום דבר לא מעיד ששירותי חב״ד של החורף פועלים שם בקיץ: שאלו אותנו לפני שאתם מסתמכים על אחד מהם."),
            ("כתבו להרב בלעיש לפני שאתם מתכננים סביב אחד מהם.", "שום דבר לא מעיד על כך. שאלו אותנו לפני שאתם מתכננים סביב אחד מהם.")],
}
for l, paires in ETE.items():
    for a, b in paires:
        for x in H.split(): R(f"{l}summer-in-the-alps-jewish-families/{x}", a, b)
R(P + "summer-in-the-alps-jewish-families.py", "Nothing says they run in summer. Write to Rabbi Daniel Belaïch (habadalpes@yahoo.fr) before you count on one.", "Nothing says they run in summer: ask us before you count on one.")
R(P + "summer-in-the-alps-jewish-families.py", "Write to Rabbi Belaïch before you plan around one.", "Ask us before you plan around one.")


def main():
    fichiers = sorted({p for p in glob.glob("**/index.html", recursive=True) if not p.startswith("_")}
                      | {p for p in glob.glob("**/index.md", recursive=True) if not p.startswith("_")}
                      | set(glob.glob("_pages/*.py")) | set(glob.glob("_build_*.py")) | set(glob.glob("_demande_*.py"))
                      | {"_chalet_aigle_royal.py", "_chalets_courchevel_lot2.py", "llms.txt"})
    touches, manques = [], []
    for p in fichiers:
        q = p.replace("\\", "/")
        s0 = rd(p); s = s0
        for f, a, b in B:
            if f == q:
                if a in s: s = s.replace(a, b); JOURNAL.append(f"BELAÏCH {q} | « {a[:90]} » → « {b[:90]} »")
                elif not (b and b in s): manques.append(f"{q} : « {a[:70]} »")
        s = duree(q, s)
        if s != s0:
            touches.append(q)
            if not SEC: wr(p, s)
    io.open(r"E:\tmp-zones-apres\journal_b.txt", "w", encoding="utf-8").write("\n".join(JOURNAL) + "\n")
    print(len(touches), "fichiers modifiés" + (" (essai)" if SEC else ""))
    for m in manques: print("MANQUE", m)
    print(sum(j.startswith("MODIFIÉ") for j in JOURNAL), "durées changées,", sum(j.startswith("LAISSÉ") for j in JOURNAL), "laissées,",
          sum(j.startswith("BELAÏCH") for j in JOURNAL), "passages Belaïch")


if __name__ == "__main__":
    main()
