# -*- coding: utf-8 -*-
"""Carte des numéros, mentions Hebcal et Grenoble dans les pages EN (sorties HTML)."""
import os, re, io, collections, sys
PAT = {
    'moshe': re.compile(r'33652092301|6 52 09 23 01'),
    'guide': re.compile(r'33767711259|7 67 71 12 59'),
    'mendel': re.compile(r'33781823193|7 81 82 31 93'),
    'hebcal': re.compile(r'[Hh]ebcal'),
    'grenoble': re.compile(r'Grenoble'),
}
c = collections.defaultdict(list)
for root, d, f in os.walk('.'):
    r = root.replace(os.sep, '/')
    if any(x in r for x in ('_candidats', '.git', '_pages', '/fr', '/es', '/he')):
        continue
    for n in f:
        if n.endswith('.html'):
            p = (r + '/' + n)[2:]
            s = io.open(p, encoding='utf8', errors='ignore').read()
            for k, rx in PAT.items():
                m = len(rx.findall(s))
                if m:
                    c[k].append(f'{p}({m})')
for k, v in c.items():
    print(f'== {k} : {len(v)} pages EN')
    print('   ' + ' '.join(v))
