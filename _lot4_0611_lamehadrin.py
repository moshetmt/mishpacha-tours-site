# -*- coding: utf-8 -*-
"""Règle de Moshé du 06/11/2026 à 2 h (« pas jamais lamehadrin, c'est lamehadrin ») : la cacherout est lamehadrin et s'écrit.
Idempotent. Depuis site-v5/ : python _lot4_0611_lamehadrin.py
 1. Ligne du certificat (lot 1, _sceau_cacherout.py) : « Cacher lamehadrin, certifié par le Beth Habad de Grenoble-Alpes, Rav Yehia
    Lahiany » (formule A choisie par Moshé), 4 langues ; le script du sceau est modifié puis relancé sur toutes les pages.
 2. Hébreu : le retrait du 30/10 (_retouches_30_10.py : « כשר למהדרין » → « שומר כשרות », « כשרות למהדרין » → « בהקפדה על כשרות »)
    est annulé sur les pages he/ et dans les générateurs ; les deux paires sont retirées de _retouches_30_10.py.
 3. Catalogues (apps-script/Mendel.gs) : même formule ; les 39 PDF sont à régénérer par la session qui publie."""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

# 1. formule du certificat dans le script du sceau
SCEAU = [("Certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany", "Kosher lamehadrin, certified by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany"),
         ("Certifié cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany", "Cacher lamehadrin, certifié par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany"),
         ("Certificado kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany", "Kosher lamehadrín, certificado por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany"),
         ('"he": ("", "בית חב״ד גרנובל-אלפים", "ארוחות חלב ישראל · שירות שומר שבת", "בהשגחת בית חב״ד גרנובל-אלפים"', '"he": ("", "בית חב״ד גרנובל-אלפים", "ארוחות חלב ישראל · שירות שומר שבת", "כשר למהדרין בהשגחת בית חב״ד גרנובל-אלפים"'),
         ('OR = {"": "Certified kosher by Beth Habad Grenoble‑Alpes", "fr": "Certifié cacher par le Beth Habad de Grenoble‑Alpes",', 'OR = {"": "Kosher lamehadrin, certified by Beth Habad Grenoble‑Alpes", "fr": "Cacher lamehadrin, certifié par le Beth Habad de Grenoble‑Alpes",'),
         ('"es": "Certificado kosher por el Beth Habad Grenoble‑Alpes", "he": "בהשגחת בית חב״ד גרנובל-אלפים"}   # ligne d\'or', '"es": "Kosher lamehadrín, certificado por el Beth Habad Grenoble‑Alpes", "he": "כשר למהדרין בהשגחת בית חב״ד גרנובל-אלפים"}   # ligne d\'or')]
s = rd("_sceau_cacherout.py"); n = 0
for a, b in SCEAU:
    if a in s: s = s.replace(a, b); n += 1
wr("_sceau_cacherout.py", s); print("sceau : remplacements", n, "(0 = déjà fait)")
assert "Cacher lamehadrin" in s

# 3. catalogues
g = rd("../apps-script/Mendel.gs"); m = 0
for a, b in SCEAU[:3]:
    if a in g: g = g.replace(a, b); m += 1
wr("../apps-script/Mendel.gs", g); print("Mendel.gs :", m)

# 2. hébreu
HE = [("בהקפדה על כשרות", "כשרות למהדרין"), ("שומר כשרות", "כשר למהדרין")]
r = rd("_retouches_30_10.py")
r = r.replace(', ("כשרות למהדרין", "בהקפדה על כשרות"), ("כשר למהדרין", "שומר כשרות")]', "]   # 06/11 : lamehadrin rétabli (_lot4_0611_lamehadrin.py)")
wr("_retouches_30_10.py", r)
k = 0
for p in glob.glob("he/**/index.html", recursive=True) + [f for f in glob.glob("_*.py") if f not in ("_lot4_0611_lamehadrin.py", "_retouches_30_10.py")] + ["../apps-script/Mendel.gs", "llms.txt"]:
    if not os.path.exists(p): continue
    t = rd(p); t0 = t
    for a, b in HE: t = t.replace(a, b)
    if t != t0: wr(p, t); k += 1
print("hébreu rétabli :", k, "fichier(s)")
os.system("python _sceau_cacherout.py")
