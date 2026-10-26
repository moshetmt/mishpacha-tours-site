# -*- coding: utf-8 -*-
"""Horaires de Chabbat qui ne s'affichaient plus (Moshé, 27/10/2026). Cause : l'emplacement de l'heure, un <b></b> vide
dans #m-entree et #m-sortie, a été retiré du HTML par un nettoyage, et le script n'avait plus où écrire l'heure.
Correctif : le script recrée le <b> s'il manque (toutes les pages, et le modèle _contacts_bh_hebcal.py). Idempotent.
    python _shabbat_heures.py   (depuis site-v5/)"""
import glob
REMPL = {
    'e.querySelector("b").textContent=': '(e.querySelector("b")||e.querySelector(".sh-d").insertAdjacentElement("afterend",document.createElement("b"))).textContent=',
    's.querySelector("b").textContent=': '(s.querySelector("b")||s.querySelector(".sh-d").insertAdjacentElement("afterend",document.createElement("b"))).textContent=',
}
n = 0
for p in glob.glob("**/index.html", recursive=True) + ["_contacts_bh_hebcal.py"]:
    h = open(p, encoding="utf-8").read()
    h2 = h
    for a, b in REMPL.items():
        h2 = h2.replace(a, b)
    if h2 != h:
        open(p, "w", encoding="utf-8").write(h2); n += 1
print(n, "fichiers")
