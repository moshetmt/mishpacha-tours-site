# -*- coding: utf-8 -*-
"""Maquette de comparaison demandée par Mendel (vocal du 15/10 21 h 56) : l'accueil EN en noir, blanc et or (palette B du logo
Winter Prestige, 14/10), logo Winter Prestige devant, « powered by mishpacha tours » dessous. Sortie : preview/accueil-sombre/index.html,
noindex, hors sitemap. Rien ne change sur l'accueil réel."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(ICI, 'index.html'), encoding='utf8', newline='').read()
# chemins relatifs -> absolus (la maquette vit deux niveaux plus bas)
s = re.sub(r'(src|href)="(img/|styles\.css|js/)', r'\1="/\2', s)
s = s.replace('href="./"', 'href="/preview/accueil-sombre/"')
s = s.replace('<link rel="canonical"', '<meta name="robots" content="noindex, nofollow">\n<link rel="canonical"', 1)
# logo : Winter Prestige en or, Mishpacha en « powered by » dessous
s = s.replace('<img class="forme" src="/img/picto-hassid.svg" alt="" width="68" height="95"><span class="mot">mishpacha tours</span>',
              '<span class="wp-logo"><img src="/img/logo-winter-prestige-or.svg" alt="Winter Prestige" width="1144" height="328">'
              '<small>powered by <img src="/img/picto-hassid.svg" alt="" width="68" height="95"> mishpacha tours</small></span>', 1)
CSS = '''
<style id="maquette-sombre">
:root{--creme:#141416;--beige:#1C1B1F;--encre:#FAF7F0;--blanc:#232226;--jaune:#C9A961;--vert:#C9A961;--vert-c:#2A2A2E;--rose:#1F1E22;--or:#C9A961;--or-c:#E3C98A}
body{background:#141416;color:#FAF7F0}
.strip{background:#0C0C0E;color:#E3C98A;border-bottom:1px solid rgba(201,169,97,.35)}.strip a{color:#E3C98A}
.nav{background:#141416;border-bottom:1px solid rgba(201,169,97,.25)}
.nav .logo .wp-logo{display:flex;flex-direction:column;gap:2px}.nav .logo .wp-logo > img{height:30px;width:auto}
.nav .logo .wp-logo small{display:flex;align-items:center;gap:4px;font-size:10px;letter-spacing:.04em;color:#CFC8B8;font-weight:600}.nav .logo .wp-logo small img{height:14px;width:auto;filter:invert(1) brightness(1.4)}
.nav .liens a{color:#FAF7F0}.nav .menu{background:#C9A961}.nav .menu::before,.nav .menu span::before,.nav .menu span::after{background:#141416}
.nav-cta,.btn-noir,.chercheur button,.ticket .rond{background:#C9A961!important;color:#141416!important}.nav-cta{color:#141416}
.langue summary,.langue ul{background:#1C1B1F;color:#FAF7F0;border-color:rgba(201,169,97,.3)}
.hero{background:#000}.hero h1,.hero h1 i,.hero p{color:#FAF7F0}.hero h1 i{color:#E3C98A}
.chercheur{background:rgba(20,20,22,.78);color:#FAF7F0;border:1px solid rgba(201,169,97,.35);backdrop-filter:blur(10px)}
.chercheur label span,.chercheur small{color:#CFC8B8}.chercheur input,.chercheur select{background:#232226;color:#FAF7F0;border:1px solid rgba(201,169,97,.3)}
.beige{background:#1C1B1F}
h2,h3,.sous{color:#FAF7F0}h2 i,h1 i{color:#E3C98A}
.hub-carte,.carte,a.hub-carte{background:#232226;color:#FAF7F0;border:1px solid rgba(201,169,97,.22)}.hub-carte p,.carte p{color:#CFC8B8}
.ac-van{background:#1C1B1F;color:#FAF7F0;border:1px solid rgba(201,169,97,.35)}.ac-van img{filter:invert(.9)}
.ac-wp,.ac-chalet{color:#FAF7F0}
.ticket{background:#1C1B1F;color:#FAF7F0;border:1px solid rgba(201,169,97,.35)}.ticket h2{color:#FAF7F0}.ticket .wa{color:#E3C98A}
.ticket-hassid,.ac-lyon img.hassid,.pied img[src*='logo'],.pied img[src*='hassid'],.pied .logo img{filter:invert(1) brightness(1.2)}
footer,.pied{background:#0C0C0E;color:#CFC8B8}footer a{color:#E3C98A}
.pill{background:#232226;color:#FAF7F0;border:1px solid rgba(201,169,97,.3)}
.ac-etapes li b{color:#E3C98A}
.wa-flottant{background:#C9A961;color:#141416}
.consent,.cookie{background:#1C1B1F;color:#FAF7F0}
img[src$=".webp"],img[src*="/img/des/"]{filter:invert(.92) sepia(.6) saturate(2) hue-rotate(5deg) brightness(.95)}
</style>
</head>'''
s = s.replace('</head>', CSS, 1)
out = os.path.join(ICI, 'preview', 'accueil-sombre'); os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf8', newline='').write(s); print('ok preview/accueil-sombre')
