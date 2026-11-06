# -*- coding: utf-8 -*-
"""Mendel (02/11) : jamais « skis aux pieds » ni « ski-in ski-out » (mot bloquant de qa_site). Passation du 05/11 : à retirer sur tout
le site avant la publication groupée. Remplacement par « à une minute des pistes » (proposition de la passation), 4 langues,
pages + JSON des pages de service + générateurs. Idempotent. Depuis site-v5/ : python _lot4_0611_pistes.py"""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
REP = [
 ("ski-in ski-out chalet", "chalet a minute from the slopes"), ("ski-in/ski-out chalet", "chalet a minute from the slopes"),
 ("Ski-in ski-out chalet", "Chalet a minute from the slopes"), ("ski-in ski-out access", "access a minute from the slopes"),
 ("ski-in ski-out", "a minute from the slopes"), ("ski-in/ski-out", "a minute from the slopes"), ("Ski In Ski Out", "a Minute from the Slopes"),
 ("ski in ski out", "a minute from the slopes"), ("Ski in ski out", "A minute from the slopes"),
 ("Skis aux pieds", "À une minute des pistes"), ("skis aux pieds", "à une minute des pistes"),
 ("¿Es realmente esquí a pie de puerta?", "¿Está realmente a un minuto de las pistas?"),
 ("esquí a pie de puerta", "a un minuto de las pistas"), ("Esquí a pie de puerta", "A un minuto de las pistas"),
 ("a pie de pista", "a un minuto de las pistas"), ("סקי עד הדלת", "דקה מהמסלולים"),
]
fichiers = [p for p in glob.glob("**/index.html", recursive=True) if not p.startswith(("_brouillons", "_candidats"))]
fichiers += glob.glob("**/index.md", recursive=True) + glob.glob("_lot4_contenu/*.json") + [f for f in glob.glob("_*.py") if f != "_lot4_0611_pistes.py"] + ["llms.txt"]
n = 0
for p in fichiers:
    if not os.path.exists(p): continue
    s = io.open(p, encoding="utf-8", newline="").read(); s0 = s
    for a, b in REP: s = s.replace(a, b)
    if s != s0: io.open(p, "w", encoding="utf-8", newline="").write(s); n += 1
print("fichiers corrigés :", n)
reste = 0
for p in fichiers:
    if os.path.exists(p) and re.search(r"skis aux pieds|ski[- ]in[ /-]*ski[- ]out|esquí a pie|a pie de pista|סקי עד הדלת", io.open(p, encoding="utf-8").read(), re.I): reste += 1; print("reste :", p)
print("fichiers avec un mot interdit :", reste)
