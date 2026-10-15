# -*- coding: utf-8 -*-
"""Gabarit « bannière 3 » (validé le 14/10) posé sur les pages Alpes et la page van, 4 langues. Idempotent.
Bannière photo voilée + panneau de verre sombre, bande hassid + intro, cartes (Deux Alpes et chalet seulement),
contenu existant, section finale verte avec formulaire court. La CSS vit dans styles.css (bloc LEAD).
À lancer après _images_cartes.py et _kashrut.py, avant _ton_expert.py et _decor.py."""
import io, os, re, html
from PIL import Image
ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
LANGS = ('en', 'fr', 'es', 'he')

# 1. hassid du logo en deux couleurs (le SVG source utilise currentColor)
src = io.open('img/picto-hassid.svg', encoding='utf8').read()
for nom, col in (('vert', '#2D5132'), ('creme', '#FFFAED')):
    io.open(f'img/picto-hassid-{nom}.svg', 'w', encoding='utf8').write(src.replace('currentColor', col))

STATIONS = {
 'kosher-val-thorens': ('stock/st-val-thorens.jpg', dict(en='Val Thorens', fr='Val Thorens', es='Val Thorens', he='ואל טורנס')),
 'kosher-courchevel': ('stock/st-courchevel.jpg', dict(en='Courchevel', fr='Courchevel', es='Courchevel', he='קורשבל')),
 'kosher-megeve': ('stock/st-megeve.jpg', dict(en='Megève', fr='Megève', es='Megève', he="מז'ב")),
 'kosher-alpe-dhuez': ('stock/st-alpe-dhuez.jpg', dict(en="Alpe d'Huez", fr="L'Alpe d'Huez", es="Alpe d'Huez", he="אלפ ד'ואז")),
 'kosher-les-deux-alpes': ('chalet/wp-pistes-balcon.jpg', dict(en='Les Deux Alpes', fr='Les Deux Alpes', es='Les Deux Alpes', he='לה דז אלפ')),
 'kosher-grenoble': ('stock/st-grenoble.jpg', dict(en='Grenoble', fr='Grenoble', es='Grenoble', he='גרנובל')),
 'kosher-annecy': ('stock/annecy-lac.jpg', dict(en='Annecy', fr='Annecy', es='Annecy', he='אנסי')),
 'kosher-chamonix': ('stock/st-chamonix.jpg', dict(en='Chamonix', fr='Chamonix', es='Chamonix', he='שמוני')),
 'kosher-les-arcs': ('stock/st-les-arcs.jpg', dict(en='Les Arcs', fr='Les Arcs', es='Les Arcs', he='לז ארק')),
 'kosher-la-plagne': ('stock/st-la-plagne.jpg', dict(en='La Plagne', fr='La Plagne', es='La Plagne', he='לה פלאן')),
 'kosher-val-disere': ('stock/st-val-disere.jpg', dict(en="Val d'Isère", fr="Val d'Isère", es="Val d'Isère", he='ואל דיזר')),
}
# slug -> (photo, type, voyage EN)
PAGES = {s: (p, 'station', f"Kosher stay in {n['en']}") for s, (p, n) in STATIONS.items()}
PAGES.update({
 'kosher-services-french-alps': ('stock/st-val-thorens.jpg', 'alps', 'Kosher services in the Alps'),
 'alps': ('chalet/wp-soleil.jpg', 'alps', 'Kosher stay in the French Alps'),            # 15/10 Mendel : la piste brunâtre « fait de la peine », neige éclatante
 'kosher-ski-holidays-french-alps': ('chalet/wp-soleil.jpg', 'alps', 'Kosher ski holiday in the Alps'),
 'summer-in-the-alps-jewish-families': ('stock/annecy-ete.jpg', 'alps', 'Kosher summer in the Alps'),
 'kosher-vacation-french-alps': ('stock/annecy-lac.jpg', 'alps', 'Kosher vacation in the Alps'),
 'kosher-van-transfers': ('illus/flat-stopover.png', 'van', 'Van transfer'),
 'kosher-chalet-les-deux-alpes': ('chalet/wp-ext-bleu.jpg', 'chalet', 'Kosher chalet in Les Deux Alpes'),
})
OFFRE_SLUGS = ('kosher-les-deux-alpes', 'kosher-chalet-les-deux-alpes')
WP_SLUG = 'kosher-les-deux-alpes'

T = {
 'puces': {
  'en': ['Shomer Shabbat', 'Strictly kosher, Chalav Yisrael', 'Minyan on request'],
  'fr': ['Shomer Shabbat', "Strictement casher, 'Halav Israël", 'Minyan sur demande'],
  'es': ['Shomer Shabat', 'Estrictamente kosher, Chalav Yisrael', 'Minyan a petición'],
  'he': ['שומר שבת', 'שומר כשרות, חלב ישראל', 'מניין לפי בקשה']},   # 15/10 Mendel : tout est 'Halav Israël, c'est un argument
 'puces_van': {
  'en': ['Shomer Shabbat', 'Point A to point B', 'Quote on request'],
  'fr': ['Shomer Shabbat', 'Du point A au point B', 'Devis sur demande'],
  'es': ['Shomer Shabat', 'De A a B', 'Presupuesto a petición'],
  'he': ['שומר שבת', 'מנקודה א׳ לנקודה ב׳', 'הצעת מחיר לפי בקשה']},
 'btn': {'en': 'Plan my stay on WhatsApp', 'fr': 'Organiser mon séjour sur WhatsApp', 'es': 'Organizar mi estancia por WhatsApp', 'he': 'לתכנן את החופשה בוואטסאפ'},
 'btn_van': {'en': 'Request a van on WhatsApp', 'fr': 'Demander un van sur WhatsApp', 'es': 'Pedir una furgoneta por WhatsApp', 'he': 'להזמין ואן בוואטסאפ'},
 'dates': {'en': 'Dates', 'fr': 'Dates', 'es': 'Fechas', 'he': 'תאריכים'},
 'dates_ph': {'en': '9 to 14 December', 'fr': 'du 9 au 14 décembre', 'es': 'del 9 al 14 de diciembre', 'he': '9 עד 14 בדצמבר'},
 'adultes': {'en': 'Adults', 'fr': 'Adultes', 'es': 'Adultos', 'he': 'מבוגרים'},
 'adultes_van': {'en': 'Passengers', 'fr': 'Passagers', 'es': 'Pasajeros', 'he': 'נוסעים'},
 'enfants': {'en': 'Children and babies', 'fr': 'Enfants et bébés', 'es': 'Niños y bebés', 'he': 'ילדים ותינוקות'},
 'enfants_ph': {'en': '3, including a baby', 'fr': '3, dont un bébé', 'es': '3, con un bebé', 'he': '3, כולל תינוק'},
 'trajet': {'en': 'From and to', 'fr': 'De et vers', 'es': 'Desde y hasta', 'he': 'מאיפה ולאן'},
 'trajet_ph': {'en': 'Lyon airport to Courchevel', 'fr': "Aéroport de Lyon vers Courchevel", 'es': 'Aeropuerto de Lyon a Courchevel', 'he': 'נמל התעופה של ליון לקורשבל'},
 'submit': {'en': 'Get my {p} programme', 'fr': 'Recevoir mon programme {p}', 'es': 'Recibir mi programa {p}', 'he': 'לקבל את התוכנית שלי: {p}'},
 'submit_gen': {'en': 'Get my programme', 'fr': 'Recevoir mon programme', 'es': 'Recibir mi programa', 'he': 'לקבל את התוכנית שלי'},
 'submit_van': {'en': 'Get my van quote', 'fr': 'Recevoir mon devis van', 'es': 'Recibir mi presupuesto', 'he': 'לקבל הצעת מחיר לואן'},
 'small': {'en': 'Same-day reply, in English or Hebrew. Never on Shabbat.', 'fr': 'Réponse le jour même, en anglais ou en hébreu. Jamais pendant Shabbat.',
           'es': 'Respuesta el mismo día, en inglés o en hebreo. Nunca en Shabat.', 'he': 'תשובה באותו יום, באנגלית או בעברית. לא בשבת.'},
 'h2_place': {'en': '{p}: your week, <i>organised</i>.', 'fr': '{p} : votre semaine, <i>organisée</i>.', 'es': '{p}: su semana, <i>organizada</i>.', 'he': '{p}: השבוע שלכם, <i>מאורגן</i>.'},
 'h2_alps': {'en': 'Your kosher week in the Alps, <i>organised</i>.', 'fr': 'Votre semaine casher dans les Alpes, <i>organisée</i>.',
             'es': 'Su semana kosher en los Alpes, <i>organizada</i>.', 'he': 'השבוע הכשר שלכם באלפים, <i>מאורגן</i>.'},
 'h2_van': {'en': 'Your transfer, <i>organised</i>.', 'fr': 'Votre transfert, <i>organisé</i>.', 'es': 'Su traslado, <i>organizado</i>.', 'he': 'ההסעה שלכם, <i>מאורגנת</i>.'},
 'p_final': {'en': 'Tell us your dates. We send a day-by-day programme the same day.', 'fr': 'Donnez-nous vos dates. Nous envoyons un programme jour par jour le jour même.',
             'es': 'Díganos sus fechas. Enviamos un programa día a día el mismo día.', 'he': 'ספרו לנו את התאריכים. נשלח באותו יום תוכנית יום אחר יום.'},
 'p_final_van': {'en': 'Tell us where you start and where you go. We send a quote the same day.', 'fr': 'Dites-nous d\'où vous partez et où vous allez. Nous envoyons un devis le jour même.',
                 'es': 'Díganos de dónde sale y adónde va. Enviamos un presupuesto el mismo día.', 'he': 'ספרו לנו מאיפה יוצאים ולאן. נשלח הצעת מחיר באותו יום.'},
 'offre_h2': {'en': 'Where you sleep, what you eat, <i>where you ski</i>', 'fr': 'Où vous dormez, ce que vous mangez, <i>où vous skiez</i>',
              'es': 'Dónde duerme, qué come, <i>dónde esquía</i>', 'he': 'איפה ישנים, מה אוכלים, <i>איפה גולשים</i>'},
 'c1': {'en': ('Chalet or apartment', 'We find the place for your group, from a family chalet to several apartments in one residence.'),
        'fr': ('Chalet ou appartement', 'Nous trouvons le logement de votre groupe, du chalet familial à plusieurs appartements dans une même résidence.'),
        'es': ('Chalet o apartamento', 'Encontramos el alojamiento para su grupo, desde un chalet familiar hasta varios apartamentos en una misma residencia.'),
        'he': ("צ'אלה או דירה", "אנחנו מוצאים את המקום לקבוצה שלכם, מצ'אלה משפחתי ועד כמה דירות באותו בניין.")},
 'c2': {'en': ('Chef or delivered meals', 'A private kosher chef in your kitchen, or hot meals delivered to your door, Shabbat and holidays included.'),
        'fr': ('Chef ou repas livrés', 'Un chef casher privé dans votre cuisine, ou des repas chauds livrés à votre porte, Shabbat et fêtes compris.'),
        'es': ('Chef o comidas entregadas', 'Un chef kosher privado en su cocina, o comidas calientes entregadas en su puerta, Shabat y fiestas incluidos.'),
        'he': ('שף או ארוחות עד הבית', 'שף כשר פרטי במטבח שלכם, או ארוחות חמות עד הדלת, כולל שבת וחגים.')},
 'c3': {'en': ('Ski and the glacier', 'Passes, rental and lessons on request, in a resort that skis up to the glacier.'),
        'fr': ('Le ski et le glacier', "Forfaits, location et cours sur demande, dans une station où l'on skie jusqu'au glacier."),
        'es': ('Esquí y glaciar', 'Forfaits, alquiler y clases a petición, en una estación que llega hasta el glaciar.'),
        'he': ('סקי והקרחון', 'כרטיסי סקי, השכרה ושיעורים לפי בקשה, באתר שמגיעים בו בסקי עד הקרחון.')},
 'wp': {'en': ('A whole chalet with a private chef?', 'Our Winter Prestige chalet: six bedrooms, two minutes from the lifts, chef and minyan included. See the chalet'),
        'fr': ('Un chalet entier avec chef privé ?', 'Notre chalet Winter Prestige : six chambres, à deux minutes des remontées, chef et minyan compris. Voir le chalet'),
        'es': ('¿Un chalet entero con chef privado?', 'Nuestro chalet Winter Prestige: seis habitaciones, a dos minutos de los remontes, chef y minyan incluidos. Ver el chalet'),
        'he': ("צ'אלה שלם עם שף פרטי?", "צ'אלה Winter Prestige שלנו: שישה חדרי שינה, שתי דקות מהמעליות, שף ומניין כלולים. לצפות בצ'אלה")},
}
CARTES = {'kosher-les-deux-alpes': ('chalet/wp-allee.jpg', 'chalet/wp-table-fete.jpg', 'chalet/wp-soleil.jpg'),
          'kosher-chalet-les-deux-alpes': ('chalet/wp-allee.jpg', 'chalet/wp-table-fete.jpg', 'chalet/wp-pistes-balcon.jpg')}

JS = '''<script>document.querySelectorAll('.lead-form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var t='Hello, we are planning: '+f.voyage.value+'.';f.querySelectorAll('label').forEach(function(l){t+=' '+l.querySelector('span').textContent+': '+(l.querySelector('input').value||'/')+' /'});window.open('https://wa.me/33652092301?text='+encodeURIComponent(t),'_blank','noopener')})});</script>'''


def sect(s, debut):
    i = s.index(debut)
    prof = 0
    for m in re.finditer(r'<(/?)section\b[^>]*>', s[i:]):
        prof += -1 if m.group(1) else 1
        if prof == 0:
            return i, i + m.end()


def premiere_phrase(p_html):
    """(phrase du panneau en texte, reste de l'intro en html). Phrase longue : coupée à une virgule."""
    morceaux = re.split(r'(?<=[.!?])\s+(?=[^\s<])', p_html.strip(), maxsplit=1)
    prem = morceaux[0]
    reste = morceaux[1] if len(morceaux) > 1 else ''
    if '<' in prem:
        return re.sub(r'<[^>]+>', '', prem), p_html
    court = prem
    if len(prem) > 150:
        coupe = [m.start() for m in re.finditer(r'[,;:]\s', prem) if m.start() <= 150]
        court = (prem[:coupe[-1]] if coupe else prem).rstrip(' ,;:') + '.'
        reste = p_html  # phrase tronquée : l'intro complète reste dans la bande
    return court, reste


def traiter(slug, lang):
    p = os.path.join(*([slug] if lang == 'en' else [lang, slug]), 'index.html')
    s = io.open(p, encoding='utf8', newline='').read()
    if 'lead-hero3' in s:
        return 'déjà'
    photo, typ, voyage = PAGES[slug]
    a, b = sect(s, '<section class="pratique-hero">')
    ancien = s[a:b]
    fil = re.search(r'<p class="fil">.*?</p>', ancien, re.S).group(0).replace('class="fil"', 'class="fil lead-fil"', 1)
    h1 = re.search(r'<h1>(.*?)</h1>', ancien, re.S).group(1)
    pi = re.search(r'<p class="intro-fiche[^"]*">(.*?)</p>', ancien, re.S)
    intro = pi.group(1) if pi else ''
    wa = re.search(r'href="(https://wa\.me/33652092301[^"]*)"', ancien)
    href = wa.group(1) if wa else 'https://wa.me/33652092301'
    chips = re.findall(r'<li>(?:<svg class="dk[^>]*>.*?</svg>|<img class="dk[^>]*>)*(.*?)</li>', (re.search(r'<ul class="chips[^"]*">(.*?)</ul>', ancien, re.S) or [None, ''])[1], re.S)
    chips = [c for c in chips if not re.search(r'\d{4}\s*$|Checked|Vérifi|Verific|נבדק', c)]
    phrase, reste = premiere_phrase(intro)
    phrase = html.escape(phrase, quote=False)
    puces = T['puces_van' if typ == 'van' else 'puces'][lang]
    btn = T['btn_van' if typ == 'van' else 'btn'][lang]
    name = STATIONS[slug][1][lang] if slug in STATIONS else None
    if typ == 'chalet':
        name = STATIONS['kosher-les-deux-alpes'][1][lang]
    wp = ('<img class="lead3-wp" src="/img/logo-winter-prestige-or.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="260" height="92">' if typ == 'chalet' else '')
    w, h = Image.open('img/' + photo).size
    cls = 'hero lead-hero3' + (' lead-hero3-illus' if typ == 'van' else '')
    hero = f'''<section class="{cls}">
  <img src="/img/{photo}" alt="" width="{w}" height="{h}" fetchpriority="high">
  <div class="lead3-texte">
    {fil}
    <div class="lead3-bloc">
    {wp}<ul class="lead-puces">{''.join(f'<li>{x}</li>' for x in puces)}</ul>
    <h1>{h1}</h1>
    <p>{phrase}</p>
    <a class="btn-hero" href="{href}" rel="noopener"><svg><use href="#wa"/></svg>{btn}</a>
    </div><!-- _lead_retouches.py (15/10) met le formulaire en bouton principal et WhatsApp en lien : à relancer après ce script -->
  </div>
</section>
'''
    chips_html = ('<ul class="chips">' + ''.join(f'<li>{c}</li>' for c in chips) + '</ul>') if chips else ''
    corps_intro = f'<p>{reste}</p>' if reste else ''
    hero += f'''
<section class="ss wrap lead-intro"><img class="lead-mascotte" src="/img/picto-hassid-vert.svg" alt="" width="797" height="806" loading="lazy"><div>{corps_intro}{chips_html}</div></section>
'''
    if slug in OFFRE_SLUGS:
        c = [T['c1'][lang], T['c2'][lang], T['c3'][lang]]
        fig = ''.join(f'<figure><img src="/img/{ph}" alt="" loading="lazy" width="1600" height="1600"><figcaption><b>{t}</b>{d}</figcaption></figure>' for ph, (t, d) in zip(CARTES[slug], c))
        hero += f'''
<section class="ss wrap lead-offre">
  <h2>{T['offre_h2'][lang]}</h2>
  <div class="lead-cartes">{fig}</div>'''
        if slug == WP_SLUG:
            cible = '/kosher-chalet-les-deux-alpes/' if lang == 'en' else f'/{lang}/kosher-chalet-les-deux-alpes/'
            t, d = T['wp'][lang]
            hero += f'''
  <a class="lead-wp" href="{cible}"><img src="/img/logo-winter-prestige.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="260" height="92" loading="lazy"><span><b>{t}</b>{d}</span></a>'''
        hero += '\n</section>\n'
    s = s[:a] + hero + s[b:]
    # section finale
    a, b = sect(s, '<section class="ss wrap cta-pratique">')
    if typ == 'van':
        h2, pf, sub = T['h2_van'][lang], T['p_final_van'][lang], T['submit_van'][lang]
        champs = (T['dates'][lang], T['dates_ph'][lang], T['adultes_van'][lang], '4', T['trajet'][lang], T['trajet_ph'][lang])
    else:
        h2 = T['h2_place'][lang].format(p=name) if name else T['h2_alps'][lang]
        pf = T['p_final'][lang]
        sub = T['submit'][lang].format(p=name) if name else T['submit_gen'][lang]
        champs = (T['dates'][lang], T['dates_ph'][lang], T['adultes'][lang], '6', T['enfants'][lang], T['enfants_ph'][lang])
    final = f'''<section class="ss lead-final"><div class="wrap">
  <div class="lead-final-tete"><img class="lead-final-hassid" src="/img/picto-hassid-creme.svg" alt="" width="240" height="243" loading="lazy"><div><h2>{h2}</h2><p>{pf}</p></div></div>
  <form class="chercheur lead-form">
    <input type="hidden" name="voyage" value="{voyage}">
    <div class="duo">
      <label><span>{champs[0]}</span><input name="dates" type="text" placeholder="{champs[1]}"></label>
      <label><span>{champs[2]}</span><input name="adultes" type="text" inputmode="numeric" placeholder="{champs[3]}"></label>
    </div>
    <label><span>{champs[4]}</span><input name="enfants" type="text" placeholder="{champs[5]}"></label>
    <button type="submit"><svg><use href="#wa"/></svg>{sub}</button>
    <small>{T['small'][lang]}</small>
  </form>
  {JS}
</div></section>'''
    s = s[:a] + final + s[b:]
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    return 'ok'


if __name__ == '__main__':
    n = 0
    for slug in PAGES:
        for lang in LANGS:
            r = traiter(slug, lang)
            n += r == 'ok'
    print('pages transformées :', n)
