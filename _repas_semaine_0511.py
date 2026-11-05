# -*- coding: utf-8 -*-
"""Lot 1 du 05/11 (Moshé : « Shabbat au chalet » exclut les repas de semaine ; dire « repas au chalet ou livrés, la semaine et Chabbat »).
   1. Titre du bloc des fiches chalet et légende de la carte de l'accueil : « Repas au chalet ou livrés », 4 langues.
   2. Première phrase du bloc : semaine, Chabbat et fêtes, ou repas livrés ; pour Chabbat, avant l'allumage des bougies.
      Villa de Saint-Tropez : semaine ajoutée, sans livraison (non confirmée là-bas). Phrase du minyan inchangée.
   3. Pages qui portent le sceau CACH-0511 seulement : « le détail de la surveillance vous est remis par écrit » (contredit le sceau)
      devient le nom de la hashgaha. Les autres pages (Suisse, Italie...) gardent leur phrase : autre surveillance.
   Textes alternatifs des photos de table de Chabbat inchangés (ils décrivent la photo).
   Idempotent. Pages : index.html et index.md ; générateurs : _accueil_reve.py, _chalet_aigle_royal.py.
   python _repas_semaine_0511.py"""
import re, pathlib

TITRES = [  # (avant, après), seulement entre > < (h2, figcaption), en lien markdown [..] ou en titre markdown, ou dans une liste Python
    ("Chabbat au chalet", "Repas au chalet ou livrés"),
    ("Shabbat in the chalet", "Meals in the chalet or delivered"),
    ("Shabbat at the chalet", "Meals in the chalet or delivered"),
    ("Shabat en el chalet", "Comidas en el chalet o a domicilio"),
    ("Shabat en el chalé", "Comidas en el chalé o a domicilio"),
    ("שבת בצ'אלה", "ארוחות בצ'אלה או במשלוח"),
]
PHRASES = [
    (r"Le chef prépare au chalet les repas de Chabbat et des fêtes(?:, ou les repas arrivent avant l([’'])allumage des bougies)?\.",
     lambda m: f"Le chef prépare au chalet vos repas de la semaine, de Chabbat et des fêtes, ou vos repas sont livrés ; pour Chabbat, ils arrivent avant l{m.group(1) or chr(39)}allumage des bougies."),
    (r"The chef prepares the Shabbat meals and the holidays in the chalet(?:, or the meals arrive before candle lighting)?\.",
     lambda m: "The chef cooks your weekday, Shabbat and holiday meals in the chalet, or your meals are delivered; for Shabbat, they arrive before candle lighting."),
    (r"El chef prepara en el (chalet|chalé) las comidas de Shabat y de las fiestas(?:, o las comidas llegan antes del encendido de (?:las )?velas)?\.",
     lambda m: f"El chef prepara en el {m.group(1)} sus comidas de la semana, de Shabat y de las fiestas, o sus comidas llegan ya preparadas; para Shabat, antes del encendido de las velas."),
    (r"השף מכין בצ'אלה את סעודות השבת והחגים(?:, או שהארוחות מגיעות לפני הדלקת הנרות)?\.",
     lambda m: "השף מכין בצ'אלה את הארוחות שלכם בימי החול, בשבת ובחגים, או שהארוחות מגיעות אליכם במשלוח; לשבת הן מגיעות לפני הדלקת הנרות."),
    (r"Le chef prépare à la villa les repas de Chabbat et des fêtes\.", lambda m: "Le chef prépare à la villa vos repas de la semaine, de Chabbat et des fêtes."),
    (r"The chef prepares the Shabbat meals and the holidays (in|at) the villa\.", lambda m: f"The chef cooks your weekday, Shabbat and holiday meals {m.group(1)} the villa."),
    (r"El chef prepara en la villa las comidas de Shabat y de las fiestas\.", lambda m: "El chef prepara en la villa sus comidas de la semana, de Shabat y de las fiestas."),
    (r"השף מכין בווילה את סעודות השבת והחגים\.", lambda m: "השף מכין בווילה את הארוחות שלכם בימי החול, בשבת ובחגים."),
    # 05/11 soir (Moshe : « bien utiliser la terminologie ») : « la hashgaha est celle du » -> « certifie cacher par »
    (r"([Ll])a hashgaha est celle du Beth Habad de Grenoble-Alpes\.", lambda m: ("L" if m.group(1) == "L" else "l") + "a cuisine est certifiée cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"([Tt])he hashgacha is by Beth Habad Grenoble-Alpes\.", lambda m: ("T" if m.group(1) == "T" else "t") + "he kitchen is certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"([Ll])a hashgajá es del Beth Habad Grenoble-Alpes\.", lambda m: ("L" if m.group(1) == "L" else "l") + "a cocina está certificada kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"ההשגחה היא של בית חב״ד גרנובל-אלפים\.", lambda m: "המטבח בהשגחת בית חב״ד גרנובל-אלפים."),
    # RAV-0511 (Moshe 05/11 : « certifie par le Beth Habad de Grenoble, et la le nom du Rav, c'est toujours comme ca ») : pages deja reecrites
    (r"(certifiée cacher par le Beth Habad de Grenoble-Alpes|certified kosher by Beth Habad Grenoble-Alpes|certificada kosher por el Beth Habad Grenoble-Alpes)\.", lambda m: m.group(1) + ", Rav Yehia Lahiany."),
    # SHOMER-0511 : apres le nom du rav, « Shomer Shabbat : » devient « Service shomer Chabbat : » (le sujet est le service, jamais le rav)
    (r"Rav Yehia Lahiany\.((?:\s*<[^>]*>)*\s*)Shomer Shabbat :", lambda m: "Rav Yehia Lahiany." + m.group(1) + "Service shomer Chabbat :"),
    (r"Rav Yehia Lahiany\.((?:\s*<[^>]*>)*\s*)Shomer Shabbat:", lambda m: "Rav Yehia Lahiany." + m.group(1) + "Shomer Shabbat service:"),
    (r"Rav Yehia Lahiany\.((?:\s*<[^>]*>)*\s*)Shomer Shabat:", lambda m: "Rav Yehia Lahiany." + m.group(1) + "Servicio shomer Shabat:"),
]
SURV = [  # pages au sceau seulement
    (r"(?i)(t)he supervision details come in writing with your quote\.", lambda m: ("T" if m.group(1) == "T" else "t") + "he kitchen is certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"Le détail de la surveillance rabbinique vous est remis par écrit avec le devis\.", lambda m: "La cuisine est certifiée cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"le détail de la surveillance rabbinique vous est remis par écrit avec le devis\.", lambda m: "la cuisine est certifiée cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"([Ll])es détails de la surveillance figurent par écrit dans votre devis\.", lambda m: ("L" if m.group(1) == "L" else "l") + "a cuisine est certifiée cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"([Ll])os detalles de la supervisión se entregan por escrito con el presupuesto\.", lambda m: ("L" if m.group(1) == "L" else "l") + "a cocina está certificada kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
    (r"פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר\.", lambda m: "המטבח בהשגחת בית חב״ד גרנובל-אלפים."),
]

def titres(t):
    for a, b in TITRES:
        e = re.escape(a)
        t = re.sub(r"(?<=>)" + e + r"(?=<)", b, t)            # <h2 class="lc-t">..</h2>, <figcaption>..</figcaption>
        t = re.sub(r"(?<=\[)" + e + r"(?=\])", b, t)          # [..](url) en markdown
        t = re.sub(r"(?m)^(#+ )" + e + r"\s*$", lambda m: m.group(1) + b, t)
        t = re.sub(r'(?<=cap=\[")' + e + r'(?=")', b, t)     # _accueil_reve.py
    return t

def phrases(t, table):
    for r, f in table:
        t = re.sub(r, f, t)
    return t

n = 0
S = pathlib.Path(".")
for f in list(S.rglob("index.html")) + list(S.rglob("index.md")):
    s = f.read_text(encoding="utf-8")
    t = phrases(titres(s), PHRASES)
    html = f.with_name("index.html")
    if html.exists() and "<!--CACH-0511-->" in html.read_text(encoding="utf-8"):
        t = phrases(t, SURV)
    if t != s:
        f.write_text(t, encoding="utf-8", newline="\n"); n += 1
for g in ("_accueil_reve.py", "_chalet_aigle_royal.py"):
    f = S / g; s = f.read_text(encoding="utf-8"); t = phrases(titres(s), PHRASES)
    if t != s:
        f.write_text(t, encoding="utf-8", newline="\n"); n += 1
print("fichiers modifiés :", n)
