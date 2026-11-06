# -*- coding: utf-8 -*-
"""05/11 (Moshe) : deux fautes de contenu corrigees tout de suite, avant la refonte des pages.
   1. Pessah : la photo d'ouverture montrait une table de Chabbat avec des hallot (hametz). Remplacee par la photo des Alpes (wp-soleil)
      en attendant la vraie banniere Pessah du lot de refonte. 4 langues.
   2. Ete : le tableau « Cette semaine, Shabbat dans les Alpes » (horaires des stations de ski) retire de la page ete. 4 langues.
   Idempotent : python _fautes_05_11.py (depuis site-v5/)."""
import re, pathlib
n = 0
for L in ("", "fr/", "es/", "he/"):
    f = pathlib.Path(f"{L}kosher-pesach-french-alps/index.html"); s = f.read_text(encoding="utf-8")
    t = s.replace("/img/h/reve-table-", "/img/h/wp-soleil-").replace("wp-soleil-2400.webp", "wp-soleil-1600.webp")
    if t != s: f.write_text(t, encoding="utf-8", newline="\n"); n += 1
    f = pathlib.Path(f"{L}summer-in-the-alps-jewish-families/index.html"); s = f.read_text(encoding="utf-8")
    t = re.sub(r'<section class="clair ss wrap shabbat-bloc">.*?</section>\n?', "", s, count=1, flags=re.S)
    if t != s: f.write_text(t, encoding="utf-8", newline="\n"); n += 1
print("pages corrigees :", n)
