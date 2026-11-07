# -*- coding: utf-8 -*-
"""Tignes, passation du 05/11 (point 2) et relais du 07/11 (étape 4) : le Chalet Étoile Polaire se loue en entier OU par moitié
(Grande Ourse, quatre suites ; Petite Ourse, cinq suites), décision de Moshé du 02/11 déjà appliquée au devis et aux catalogues
(apps-script/mendel/chalets_tignes.py) ; la page disait encore « loués ensemble, pour un seul groupe ». Et « deux jacuzzis » retiré :
Mendel n'a pas confirmé le jacuzzi de la Grande Ourse (seule la Petite Ourse en a un, annonce) ; on écrit « un jacuzzi ».
Capacités 11 et 10 lits non confirmées : on ne les écrit pas. 4 langues, HTML + JSON-LD + index.md + générateur + llms.txt.
Idempotent. Depuis site-v5/ : python _lot4_0711_tignes.py"""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
REP = [
 # FAQ « un seul des deux chalets ? » : réponse
 ("The two chalets are rented together, for one group", "Yes: the whole Chalet Étoile Polaire, or one of the two chalets on its own, Grande Ourse (four suites) or Petite Ourse (five suites)"),
 ("Les deux chalets se louent ensemble, pour un seul groupe", "Oui : le Chalet Étoile Polaire en entier, ou un seul des deux chalets, la Grande Ourse (quatre suites) ou la Petite Ourse (cinq suites)"),
 ("Los dos chalets se alquilan juntos, para un solo grupo", "Sí: el Chalet Étoile Polaire entero, o uno solo de los dos chalets, Grande Ourse (cuatro suites) o Petite Ourse (cinco suites)"),
 ("שתי הצ'אלות מושכרות יחד, לקבוצה אחת", "כן: צ'אלה אטואל פולר בשלמותה, או אחת משתי הצ'אלות בנפרד, גרנד אורס (ארבע סוויטות) או פטיט אורס (חמש סוויטות)"),
 # « loués ensemble » ailleurs sur la page
 (", rented together:", ", rented whole or by half:"), ("connected inside and taken together:", "connected inside, rented whole or by half:"),
 ("that connect inside, taken together:", "that connect inside, rented whole or by half:"),
 ("loués ensemble :", "loués en entier ou par moitié :"), ("reliés de l'intérieur et loués ensemble :", "reliés de l'intérieur, loués en entier ou par moitié :"),
 ("alquilados juntos:", "alquilados enteros o por mitad:"), ("unidos por dentro y alquilados juntos:", "unidos por dentro, alquilados enteros o por mitad:"),
 ("ומושכרות יחד:", "ומושכרות בשלמותן או בנפרד:"), ("המושכרות יחד:", "המושכרות בשלמותן או בנפרד:"),
 # jacuzzis : un seul confirmé (Petite Ourse)
 ("Two outdoor jacuzzis facing the peaks", "An outdoor jacuzzi facing the peaks"), ("two outdoor jacuzzis", "an outdoor jacuzzi"),
 ("Two jacuzzis.", "Jacuzzi."), ("two jacuzzis", "a jacuzzi"),
 ("Deux jacuzzis extérieurs face aux sommets", "Un jacuzzi extérieur face aux sommets"), ("deux jacuzzis extérieurs", "un jacuzzi extérieur"),
 ("Deux jacuzzis.", "Jacuzzi."), ("deux jacuzzis", "un jacuzzi"), ("Le Chalet Étoile Polaire, jacuzzis", "Le Chalet Étoile Polaire, jacuzzi"),
 ("Dos jacuzzis exteriores frente a las cumbres", "Un jacuzzi exterior frente a las cumbres"), ("dos jacuzzis exteriores", "un jacuzzi exterior"),
 ("Dos jacuzzis.", "Jacuzzi."), ("dos jacuzzis", "un jacuzzi"), ("El Chalet Étoile Polaire, jacuzzis", "El Chalet Étoile Polaire, jacuzzi"),
 ("שני ג'קוזי חיצוניים", "ג'קוזי חיצוני"), ("שני ג'קוזי", "ג'קוזי"),
]
fichiers = glob.glob("**/kosher-chalet-tignes/index.html", recursive=True) + glob.glob("**/kosher-chalet-tignes/index.md", recursive=True)
fichiers += ["_chalet_tignes.py", "llms.txt"]
n = 0
for p in fichiers:
    if not os.path.exists(p): continue
    s = io.open(p, encoding="utf-8", newline="").read(); s0 = s
    for a, b in REP: s = s.replace(a, b)
    if s != s0: io.open(p, "w", encoding="utf-8", newline="").write(s); n += 1; print("corrigé :", p)
print("fichiers corrigés :", n)
reste = [p for p in glob.glob("**/*.html", recursive=True) + glob.glob("**/*.md", recursive=True) + ["llms.txt"]
         if not p.startswith(("_brouillons", "_candidats")) and os.path.exists(p)
         and re.search(r"two (outdoor )?jacuzzis|deux jacuzzis|dos jacuzzis|שני ג'קוזי|rented together, for one group|louent ensemble, pour un seul|alquilan juntos, para un solo", io.open(p, encoding="utf-8").read(), re.I)]
print("fichiers où il reste « deux jacuzzis » ou « un seul groupe » :", len(reste), reste[:10])
