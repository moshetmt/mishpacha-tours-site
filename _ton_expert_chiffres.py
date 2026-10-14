# -*- coding: utf-8 -*-
"""Après _ton_expert.py : plus de « about / environ / unos / כ- » devant un chiffre (opérateur 14/10 : tout doit paraître sûr).
Texte visible, meta et JSON-LD des 4 langues. Idempotent."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
R = [(r'\bat about (?=\d)', 'at '), (r'\b[Aa]bout (?=\d)', ''), (r"\b[Ee]nviron (?=\d)", ''), (r'\b[Uu]nos (?=\d)', ''), (r'\b[Aa]proximadamente (?=\d)', ''), (r'(?<![\w-])כ-(?=\d)', ''), (r'\broughly (?=\d)', ''), (r'\baround (?=\d)', '')]
n = 0
for root, d, f in os.walk(ICI):
    if any(x in root for x in ('_candidats', '.git', '_pages', 'credits')):
        continue
    for nom in f:
        if nom != 'index.html':
            continue
        p = os.path.join(root, nom); s = io.open(p, encoding='utf8', newline='').read(); t = s
        for a, b in R:
            t = re.sub(a, b, t)
        if t != s:
            io.open(p, 'w', encoding='utf8', newline='').write(t); n += 1
print('pages corrigées :', n)
