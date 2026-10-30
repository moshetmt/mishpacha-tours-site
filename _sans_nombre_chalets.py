# -*- coding: utf-8 -*-
"""Règle Moshé du 28/10 : jamais le nombre de chalets, dans aucune langue.
Idempotent. Passe sur toutes les pages (index.html + index.md) et sur les générateurs
qui portent ces textes (_kit_wp.py, _zones.py, _pages/kosher-chalets.py). À relancer après toute régénération."""
import io, re, glob

REMPL = [
  # EN
  ("See the five chalets", "See the chalets"),
  ("Five kosher chalets", "Our kosher chalets"),
  ("Cinq chalets casher", "Nos chalets casher"),
  ("Cinco chalets kosher", "Nuestros chalets kosher"),
  ("Our five chalets, private chef", "Our chalets, private chef"),
  ("Five chalets, everything kosher taken care of: two in Les Deux Alpes, one in Courchevel, one near Megève, one in Val Thorens with a ski path at the door.",
   "Our chalets, everything kosher taken care of: Les Deux Alpes, Courchevel, near Megève, and Val Thorens with a ski path at the door."),
  ("Five chalets, everything kosher taken care of: two in Les Deux Alpes, one in Courchevel, one near Megève.",
   "Our chalets, everything kosher taken care of: Les Deux Alpes, Courchevel and near Megève."),
  # FR
  ("Voir les cinq chalets", "Voir les chalets"),
  ("Nos cinq chalets avec chef privé", "Nos chalets avec chef privé"),
  ("Cinq chalets privés, strictement casher", "Des chalets privés, strictement casher"),
  ("Cinq chalets casher", "Des chalets casher"),
  ("Cinq chalets strictement casher dans les Alpes", "Des chalets strictement casher dans les Alpes"),
  ("Cinq chalets, tout le casher pris en charge : deux aux Deux Alpes, un à Courchevel, un près de Megève, un à Val Thorens avec un chemin skieur à la porte.",
   "Nos chalets, tout le casher pris en charge : aux Deux Alpes, à Courchevel, près de Megève et à Val Thorens avec un chemin skieur à la porte."),
  ("Cinq chalets, tout le casher pris en charge : deux aux Deux Alpes, un à Courchevel, un près de Megève.",
   "Nos chalets, tout le casher pris en charge : aux Deux Alpes, à Courchevel et près de Megève."),
  # ES
  ("Ver los cinco chalets", "Ver los chalets"),
  ("Nuestros cinco chalets con chef privado", "Nuestros chalets con chef privado"),
  ("Cinco chalets privados, estrictamente kosher", "Chalets privados, estrictamente kosher"),
  ("Cinco chalets kosher", "Chalets kosher"),
  ("Cinco chalets estrictamente kosher en los Alpes", "Chalets estrictamente kosher en los Alpes"),
  # HE
  ("לראות את חמש הצ'אלות", "לראות את הצ'אלות"),
  ("חמש הצ'אלות שלנו עם שף פרטי", "הצ'אלות שלנו עם שף פרטי"),
  ("חמש צ'אלות פרטיות, בהקפדה על כשרות", "צ'אלות פרטיות, בהקפדה על כשרות"),
  ("חמש צ'אלות כשרות באלפים", "צ'אלות כשרות באלפים"),
  ("<i>חמש צ'אלות כשרות</i>", "<i>צ'אלות כשרות</i>"),
  ("חמש צ'אלות כשרות", "צ'אלות כשרות"),
  ("חמש צ'אלות שבהן כל מה שקשור לכשרות מסודר: שתיים בלה דז אלפ, אחת בקורשבל, אחת ליד מג'ב ואחת בואל טורנס, עם שביל סקי ליד הדלת.",
   "הצ'אלות שלנו, שבהן כל מה שקשור לכשרות מסודר: בלה דז אלפ, בקורשבל, ליד מג'ב ובואל טורנס, עם שביל סקי ליד הדלת."),
  ("חמש צ'אלות שבהן כל מה שקשור לכשרות מסודר: שתיים בלה דז אלפ, אחת בקורשבל, אחת ליד מג'ב.",
   "הצ'אלות שלנו, שבהן כל מה שקשור לכשרות מסודר: בלה דז אלפ, בקורשבל וליד מג'ב."),
]
# ES : intro du hub, formulations variables
REGEX = [
  (re.compile(r"Cinco chalets, todo lo kosher[^:]*: dos en Les Deux Alpes, uno en Courchevel, uno cerca de Megève, uno en Val Thorens([^.]*)\."),
   r"Nuestros chalets, todo lo kosher resuelto: Les Deux Alpes, Courchevel, cerca de Megève y Val Thorens\1."),
  (re.compile(r"Cinco chalets, todo lo kosher[^:]*: dos en Les Deux Alpes, uno en Courchevel, uno cerca de Megève\."),
   "Nuestros chalets, todo lo kosher resuelto: Les Deux Alpes, Courchevel y cerca de Megève."),
]

def passe(p):
    s = io.open(p, encoding="utf-8").read(); n = s
    for a, b in REMPL: n = n.replace(a, b)
    for r, b in REGEX: n = r.sub(b, n)
    if n != s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(n); return 1
    return 0

if __name__ == "__main__":
    fichiers = [f for f in glob.glob("**/index.html", recursive=True) + glob.glob("**/index.md", recursive=True) if not f.startswith("_")]
    fichiers += ["_kit_wp.py", "_zones.py", "_pages/kosher-chalets.py"]
    k = sum(passe(f) for f in fichiers)
    print("fichiers modifies :", k)
    reste = []
    for f in fichiers:
        s = io.open(f, encoding="utf-8").read()
        for m in re.finditer(r"[Ff]ive chalets|[Cc]inq chalets|[Cc]inco chalets|cinq chalets|cinco chalets|חמש (?:ה)?צ'אלות|חמש הצ'אלות", s):
            reste.append((f, s[max(0, m.start()-40):m.end()+40].replace("\n", " ")))
    print("restes :", len(reste))
    for r in reste[:20]: print("  ", r)
