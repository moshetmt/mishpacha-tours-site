# -*- coding: utf-8 -*-
"""Decision operateur du 15/10 : Atout France ne contraint plus rien. Retire la phrase « Stays, transfers and meals are organised and
   invoiced by our kosher team based in the Alps; Mishpacha Tours sells its guided tours in Lyon. » (4 langues) des sorties, des
   modules _pages/*.py, de _build_sitemap.py et de llms.txt. Retire aussi les paragraphes de sources vides (« , , . ») laisses par
   _ton_expert.py. Idempotent : python _sans_atout.py (depuis site-v5/), a relancer apres toute regeneration."""
import io, re, glob

PHRASE = re.compile(
    r"\s*(?:Stays, transfers and meals are organised and invoiced by (?:a|our) kosher team based in the Alps[^.]*?; ?Mishpacha Tours sells its guided tours in Lyon\."
    r"|Las estancias, los traslados y las comidas[^.]*?Mishpacha Tours vende sus visitas guiadas en Lyon\."
    r"|Séjours, transferts et repas sont organisés et facturés[^.]*?Mishpacha Tours vend ses visites guidées à Lyon\."
    r"|(?:לינה|שהייה), הסעות וארוחות מאורגנות ומחויבות[^.]*?Mishpacha Tours מוכרת את הסיורים המודרכים שלה בליון\.)")
P_VIDE = re.compile(r"\s*<p>(?:\s*<a [^>]*>\s*</a>\s*,?\s*)+\.?\s*</p>")
P_NU = re.compile(r"<p>\s*</p>")

def nettoyer(s, html):
    s = PHRASE.sub("", s)
    if html:
        s = P_VIDE.sub("", s)
        s = P_NU.sub("", s)
    return s

if __name__ == "__main__":
    n = 0
    for p in sorted(glob.glob("**/index.html", recursive=True) + glob.glob("_pages/*.py") + ["_build_sitemap.py", "llms.txt"]):
        s = io.open(p, encoding="utf-8").read()
        t = nettoyer(s, p.endswith(".html"))
        if t != s:
            io.open(p, "w", encoding="utf-8", newline="\n").write(t); n += 1
    print("fichiers modifies :", n)
