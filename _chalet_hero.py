# -*- coding: utf-8 -*-
"""Page chalet (4 langues) : bannière photo plein cadre avec le logo Winter Prestige or, à la place du logo seul sur fond vide
(opérateur 14/10 : « Bannière de Winter, c'est de la merde »). La galerie de 9 photos est retirée par _sans_mosaique.py
(« Galerie photo horrible »). Idempotent. À relancer après toute régénération de la page chalet, avant _decor.py."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
SLUG = 'kosher-chalet-les-deux-alpes'
BTN = {'en': 'Ask on WhatsApp', 'fr': 'Écrire sur WhatsApp', 'es': 'Escribir por WhatsApp', 'he': 'לכתוב בוואטסאפ'}
INTRO = {'en': 'A chalet of 300 m² in Les Deux Alpes, 6 bedrooms and 16 beds, 2 minutes from the slopes: private kosher chef or delivered meals, Shabbat and the holidays organised, a minyan on request.',
         'fr': 'Un chalet de 300 m² aux Deux Alpes, 6 chambres et 16 lits, à 2 minutes des pistes : chef privé casher ou repas livrés, Chabbat et fêtes organisés, minyan sur demande.',
         'es': 'Un chalet de 300 m² en Les Deux Alpes, 6 habitaciones y 16 camas, a 2 minutos de las pistas: chef privado kosher o comidas entregadas, Shabat y fiestas organizados, minyan a petición.',
         'he': 'שאלה של 300 מ"ר בלה דז אלפ, 6 חדרי שינה ו-16 מיטות, 2 דקות מהמסלולים: שף כשר פרטי או ארוחות עד הבית, שבת וחגים מאורגנים, מניין לפי בקשה.'}
ALT = {'en': 'The chalet in Les Deux Alpes under a blue sky, the morning after a snowfall',
       'fr': 'Le chalet aux Deux Alpes sous un ciel bleu, le lendemain d\'une chute de neige',
       'es': 'El chalet en Les Deux Alpes bajo un cielo azul, la mañana después de una nevada',
       'he': 'השאלה בלה דז אלפ תחת שמיים כחולים, בבוקר שאחרי השלג'}
for lang in ('en', 'fr', 'es', 'he'):
    p = os.path.join(ICI, *( [SLUG] if lang == 'en' else [lang, SLUG]), 'index.html')
    s = io.open(p, encoding='utf8', newline='').read()
    if 'tete-photo' in s:
        continue
    m = re.search(r'<section class="(?:pratique-hero|hero hero-photo)">(.*?)</section>', s, re.S)
    if not m:
        print(lang, 'pas de pratique-hero'); continue
    bloc = m.group(1)
    fil = re.search(r'<p class="fil">.*?</p>', bloc, re.S).group(0)
    h1 = re.search(r'<h1>.*?</h1>', bloc, re.S).group(0)
    mi = re.search(r'<p class="intro-fiche[^"]*">(.*?)</p>', bloc, re.S)
    intro = re.sub(r'<[^>]+>', '', mi.group(1)) if mi else INTRO[lang]
    pre = '../' if lang == 'en' else '/'
    wa = re.search(r'href="(https://wa\.me/33652092301[^"]*)"', s)
    href = wa.group(1) if wa else 'https://wa.me/33652092301'
    hero = f'''<section class="pratique-hero"><div class="wrap">{fil}
  <div class="pratique-tete tete-photo"><div><img class="ac-wp" src="{pre}img/logo-winter-prestige.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="260" height="92">{h1}<p class="intro-fiche">{intro}</p><a class="btn-noir large" href="{href}" rel="noopener"><svg><use href="#wa"/></svg>{BTN[lang]}</a></div>
  <img class="photo-hero" src="{pre}img/chalet/wp-ext-bleu.jpg" alt="{ALT[lang]}" width="1800" height="1200" fetchpriority="high"></div>
</div></section>'''
    s = s[:m.start()] + hero + s[m.end():]
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print(lang, 'ok')
