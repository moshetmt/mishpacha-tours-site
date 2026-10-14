# -*- coding: utf-8 -*-
"""Logo de cacherout (Beth Habad Grenoble-Alpes, reçu le 14/10) sur les pages Deux Alpes (station, 4 langues) et le prototype.
Posé dans le bloc minyan (.minyan-bh). Idempotent."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
TXT = {'en': 'Kashrut under the supervision of the Beth Habad Grenoble-Alpes',
       'fr': 'Cacherout sous la supervision du Beth Habad Grenoble-Alpes',
       'es': 'Kashrut bajo la supervisión del Beth Habad Grenoble-Alpes',
       'he': 'כשרות בפיקוח בית חב"ד גרנובל-אלפים'}
PAGES = [('en', 'kosher-les-deux-alpes/index.html'), ('fr', 'fr/kosher-les-deux-alpes/index.html'),
         ('es', 'es/kosher-les-deux-alpes/index.html'), ('he', 'he/kosher-les-deux-alpes/index.html'),
         ('en', 'preview/lead-les-deux-alpes/index.html')]
for lang, rel in PAGES:
    p = os.path.join(ICI, rel); s = io.open(p, encoding='utf8', newline='').read()
    if 'kashrut-badge' in s: continue
    pre = '../' if (lang == 'en' and not rel.startswith('preview')) else ('../../' if rel.startswith('preview') else '/')
    badge = f'<div class="kashrut-badge"><img src="{pre}img/logo-kashrut-beth-habad-grenoble-alpes.png" alt="" width="600" height="470" loading="lazy"><span>{TXT[lang]}</span></div>'
    m = re.search(r'(<section class="ss wrap minyan-bh">.*?)(</section>)', s, re.S)
    assert m, rel
    s = s[:m.end(1)] + badge + s[m.end(1):]
    io.open(p, 'w', encoding='utf8', newline='').write(s); print(rel, 'ok')
