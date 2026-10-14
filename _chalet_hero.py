# -*- coding: utf-8 -*-
"""Page chalet (4 langues) : bannière photo plein cadre avec le logo Winter Prestige or, à la place du logo seul sur fond vide
(opérateur 14/10 : « Bannière de Winter, c'est de la merde »). La galerie de 9 photos est retirée par _sans_mosaique.py
(« Galerie photo horrible »). Idempotent. À relancer après toute régénération de la page chalet, avant _decor.py."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
SLUG = 'kosher-chalet-les-deux-alpes'
BTN = {'en': 'Ask on WhatsApp', 'fr': 'Écrire sur WhatsApp', 'es': 'Escribir por WhatsApp', 'he': 'לכתוב בוואטסאפ'}
ALT = {'en': 'The chalet in Les Deux Alpes under a blue sky, the morning after a snowfall',
       'fr': 'Le chalet aux Deux Alpes sous un ciel bleu, le lendemain d\'une chute de neige',
       'es': 'El chalet en Les Deux Alpes bajo un cielo azul, la mañana después de una nevada',
       'he': 'השאלה בלה דז אלפ תחת שמיים כחולים, בבוקר שאחרי השלג'}
for lang in ('en', 'fr', 'es', 'he'):
    p = os.path.join(ICI, *( [SLUG] if lang == 'en' else [lang, SLUG]), 'index.html')
    s = io.open(p, encoding='utf8', newline='').read()
    if 'hero-photo' in s:
        continue
    m = re.search(r'<section class="pratique-hero">(.*?)</section>', s, re.S)
    if not m:
        print(lang, 'pas de pratique-hero'); continue
    bloc = m.group(1)
    fil = re.search(r'<p class="fil">.*?</p>', bloc, re.S).group(0)
    h1 = re.search(r'<h1>.*?</h1>', bloc, re.S).group(0)
    intro = re.search(r'<p class="intro-fiche[^"]*">(.*?)</p>', bloc, re.S).group(1)
    intro = re.sub(r'<[^>]+>', '', intro)
    intro = intro.split('. ')[0].rstrip('.') + '.'
    pre = '../' if lang == 'en' else '/'
    wa = re.search(r'href="(https://wa\.me/33652092301[^"]*)"', s)
    href = wa.group(1) if wa else 'https://wa.me/33652092301'
    hero = f'''<section class="hero hero-photo">
  <img src="{pre}img/chalet/wp-ext-bleu.jpg" alt="{ALT[lang]}" width="1800" height="1350" fetchpriority="high">
  <div class="hero-texte wrap">
    {fil}
    <img class="hero-logo" src="{pre}img/logo-winter-prestige-or.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="1144" height="328">
    {h1}
    <a class="btn-hero" href="{href}" rel="noopener"><svg aria-hidden="true" focusable="false"><use href="#wa"/></svg>{BTN[lang]}</a>
  </div>
</section>'''
    s = s[:m.start()] + hero + s[m.end():]
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print(lang, 'ok')
