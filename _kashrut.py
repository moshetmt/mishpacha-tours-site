# -*- coding: utf-8 -*-
"""Logo de la hashgaha (Beth Habad Grenoble-Alpes, reçu le 14/10) à la place du picto générique de la ligne « Strictly kosher »
des pages Deux Alpes (4 langues), avec le nom du Beth Habad dans la phrase et dans la FAQ JSON-LD. Idempotent.
À lancer APRES _decor.py (il lit son balisage et _decor efface le logo)."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
LOGO = 'img/logo-kashrut-beth-habad-grenoble-alpes.png'
TXT = {'en': 'Kashrut under the supervision of the Beth Habad Grenoble-Alpes. The supervision details come in writing with your quote.',
       'fr': 'Cacherout sous la surveillance du Beth Habad Grenoble-Alpes. Le détail de la surveillance rabbinique vous est remis par écrit avec le devis.',
       'es': 'Kashrut bajo la supervisión del Beth Habad Grenoble-Alpes. Los detalles de la supervisión se entregan por escrito con el presupuesto.',
       'he': 'כשרות בהשגחת בית חב״ד גרנובל-אלפים. פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר.'}
ALT = 'Beth Habad Grenoble-Alpes'
FAQ_OLD = 'Our team in the Alps cooks under the Chabad network of the Alps. Ask for the supervision details in writing with your quote.'
FAQ_NEW = 'Our team in the Alps cooks under the supervision of the Beth Habad Grenoble-Alpes. The supervision details come in writing with your quote.'
PAGES = [('en', 'kosher-les-deux-alpes/index.html'), ('fr', 'fr/kosher-les-deux-alpes/index.html'),
         ('es', 'es/kosher-les-deux-alpes/index.html'), ('he', 'he/kosher-les-deux-alpes/index.html')]
RX = re.compile(r'(<span class="dk-g dk-g-ligne">)<img class="dk dk-gico" src="([^"]*?)img/des/badge-check\.webp"[^>]*>[^<]*(</span>)')
for lang, rel in PAGES:
    p = os.path.join(ICI, rel); s = io.open(p, encoding='utf8', newline='').read()
    # ancien badge séparé (première pose du 14/10) retiré
    s = re.sub(r'<div class="kashrut-badge">.*?</div>', '', s, count=1, flags=re.S)
    s, k = RX.subn(lambda m: f'{m.group(1)}<img class="dk dk-gico hashgaha" src="{m.group(2)}{LOGO}" alt="{ALT}" width="600" height="470" loading="lazy">{TXT[lang]}{m.group(3)}', s, count=1)
    s = s.replace(FAQ_OLD, FAQ_NEW)
    io.open(p, 'w', encoding='utf8', newline='').write(s); print(rel, 'logo' if k else 'déjà posé')
