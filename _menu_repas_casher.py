# -*- coding: utf-8 -*-
"""05/11 (Mendel, audio relaye par Moshe) : l'entree de menu « Chef & Shabbat » devient « Repas casher et chef » dans les 4 langues.
   Ne touche que les liens du menu vers /kosher-services-french-alps/ (en-tete et panneau telephone), jamais le contenu des pages.
   Idempotent : python _menu_repas_casher.py (depuis site-v5/). _zones.py porte deja les nouveaux libelles."""
import re, pathlib
NOUV = {"": ("Chef & Shabbat", "Kosher meals & chef"), "fr": ("Chef & Chabbat", "Repas casher et chef"),
        "es": ("Chef y Shabat", "Comidas kosher y chef"), "he": ("שף ושבת", "ארוחות כשרות ושף")}
n = 0
for f in pathlib.Path(".").rglob("index.html"):
    lang = f.parts[0] if f.parts[0] in ("fr", "es", "he") else ""
    vieux, neuf = NOUV[lang]
    pre = f"/{lang}" if lang else ""
    s = f.read_text(encoding="utf-8")
    t = re.sub(r'(<a href="' + re.escape(pre) + r'/kosher-services-french-alps/"[^>]*>)' + "(?:&|&amp;)".join(re.escape(x) for x in vieux.split("&")) + r'(?=<|\s*<)',
               lambda m: m.group(1) + neuf.replace("&", "&amp;"), s)
    if t != s: f.write_text(t, encoding="utf-8", newline="\n"); n += 1
print("pages modifiees :", n)
