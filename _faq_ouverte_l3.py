# -*- coding: utf-8 -*-
"""Correctif en ligne du 08/11/2026 (Moshé : « c'est quoi cette zone non cliquable », FAQ de la page Pessah).
La passe luxe du lot 3 (classe body `l3-luxe`, 168 pages) rend les questions de la FAQ ouvertes sans « + » : son CSS coupe le
toucher sur `summary` et cache le signe, mais son script ne posait `open` que sur les pages chalet. Sur 124 pages (stations en
4 langues, Pessah…), les questions restaient fermées et inertes. Ici : `open` sur chaque <details> de la section FAQ des pages
`l3-luxe`. Idempotent. Depuis site-v5/ : python _faq_ouverte_l3.py"""
import glob, io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
n = m = 0
for p in glob.glob("**/index.html", recursive=True):
    if p.startswith("_"): continue
    s = io.open(p, encoding="utf-8", newline="").read()
    body = re.search(r'<body class="([^"]*)"', s)
    if not body or "l3-luxe" not in body.group(1): continue
    def faq(sec):
        global m
        new, k = re.subn(r'<details(?![^>]*\bopen\b)((?:\s[^>]*)?)>', r'<details open\1>', sec.group(0)); m += k; return new
    s2 = re.sub(r'<section class="[^"]*\bfaq\b[^"]*"[^>]*>.*?</section>', faq, s, flags=re.S)
    if s2 != s: io.open(p, "w", encoding="utf-8", newline="").write(s2); n += 1
print(f"pages corrigées : {n}, questions ouvertes : {m}")
