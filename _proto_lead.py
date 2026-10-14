# -*- coding: utf-8 -*-
"""Prototype « page de lead » sur Les Deux Alpes (14/10), en aperçu non indexé : /preview/lead-les-deux-alpes/.
Modèle validé par la recherche (06-reports/2026-10-14-modeles-de-pages-recherche.md) :
bannière photo plein écran + promesse + formulaire court visible sans scroller, preuves, ce qu'on organise (photos),
étapes, offre chalet, minyan, Chabbat, FAQ, formulaire répété. Le texte SEO de la page actuelle est gardé.
Pas de mosaïque en bas de page."""
import io, os, re
ICI = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(ICI, 'kosher-les-deux-alpes', 'index.html'), encoding='utf8').read()

def sect(s, debut):
    i = s.index(debut)
    prof, k = 0, i
    for m in re.finditer(r'<(/?)section\b[^>]*>', s[i:]):
        prof += -1 if m.group(1) else 1
        if prof == 0:
            return i, i + m.end()

# 1. bannière
a, b = sect(src, '<section class="pratique-hero">')
ancien = src[a:b]
intro = re.search(r'<p class="intro-fiche[^"]*">(.*?)</p>', ancien, re.S).group(1)
FORM = '''<form class="chercheur lead-form">
      <input type="hidden" name="voyage" value="Kosher stay in Les Deux Alpes">
      <div class="duo">
        <label><span>Dates</span><input name="dates" type="text" placeholder="9 to 14 December"></label>
        <label><span>Adults</span><input name="adultes" type="text" inputmode="numeric" placeholder="6"></label>
      </div>
      <label><span>Children and babies</span><input name="enfants" type="text" placeholder="3, including a baby"></label>
      <button type="submit"><svg><use href="#wa"/></svg>Get my Deux Alpes programme</button>
      <small>Same-day reply, in English or Hebrew. Never on Shabbat.</small>
    </form>'''
HERO = f'''<section class="hero ac-hero lead-hero">
  <img src="/img/stock/st-les-deux-alpes.jpg" alt="Les Deux Alpes, the resort and its slopes under the snow" width="1600" height="1067" fetchpriority="high">
  <div class="hero-texte">
    <p class="fil lead-fil"><a href="../../">Home</a> / <a href="../../alps/">The French Alps</a> / Les Deux Alpes</p>
    <h1>Strictly kosher in Les Deux Alpes.<br><i>Your accommodation, a chef or delivered meals, Shabbat and minyan, organised for you.</i></h1>
    <ul class="lead-puces"><li>Shomer Shabbat</li><li>Strictly kosher</li><li>One request, one programme</li></ul>
    {FORM}
  </div>
  <img class="lead-mascotte" src="/img/illus/flat-ski.png" alt="" width="700" height="700">
</section>

<section class="ss lead-preuves"><div class="wrap">
  <div><b>Chalets and apartments</b><span>for one family or a whole group, near the lifts</span></div>
  <div><b>Minyan</b><span>with a Sefer Torah, for Shabbat and holidays</span></div>
  <div><b>1 programme</b><span>day by day, before you pay anything</span></div>
</div></section>

<section class="ss wrap lead-intro"><p>{intro}</p></section>

<section class="ss wrap lead-offre">
  <h2>Where you sleep, what you eat, <i>where you ski</i></h2>
  <div class="lead-cartes">
    <figure><img src="/img/chalet/wp-allee.jpg" alt="A chalet in Les Deux Alpes between two walls of snow" loading="lazy" width="1600" height="1600"><figcaption><b>Chalet or apartment</b>We find the place for your group, from a family chalet to several apartments in one residence.</figcaption></figure>
    <figure><img src="/img/chalet/wp-table-fete.jpg" alt="A festive kosher table set in the chalet" loading="lazy" width="1600" height="1600"><figcaption><b>Chef or delivered meals</b>A private kosher chef in your kitchen, or hot meals delivered to your door, Shabbat and holidays included.</figcaption></figure>
    <figure><img src="/img/chalet/wp-pistes-balcon.jpg" alt="The slopes of Les Deux Alpes seen from the chalet balcony" loading="lazy" width="1600" height="1600"><figcaption><b>Ski and the glacier</b>Passes, rental and lessons on request, in a resort that skis up to the glacier.</figcaption></figure>
  </div>
  <a class="lead-wp" href="../../kosher-chalet-les-deux-alpes/"><img src="/img/logo-winter-prestige.svg" alt="Winter Prestige, powered by Mishpacha Tours" width="260" height="92" loading="lazy"><span><b>A whole chalet with a private chef?</b>Our Winter Prestige chalet: six bedrooms, two minutes from the lifts, chef and minyan included. See the chalet</span></a>
</section>'''
src = src[:a] + HERO + src[b:]

# 2. CTA final : formulaire répété à la place du simple bouton
a, b = sect(src, '<section class="ss wrap cta-pratique">')
src = src[:a] + f'''<section class="ss lead-final"><div class="wrap">
  <h2>Your week in Les Deux Alpes, <i>organised</i>.</h2>
  <p>Tell us your dates. We send a day-by-day programme the same day.</p>
  {FORM}
</div></section>''' + src[b:]

# 3. « Keep reading » et sources gardés ; aperçu non indexé, canonique vers la vraie page
src = src.replace('<meta name="robots" content="index, follow">', '')
src = re.sub(r'(<head[^>]*>)', r'\1\n<meta name="robots" content="noindex, nofollow">', src, count=1)
src = src.replace('="../', '="../../')
src = src.replace('</head>', '''<style>
.lead-hero{min-height:0}
.lead-hero .hero-texte{display:block!important;max-width:620px;margin-inline-end:auto;grid-template-columns:none!important}
.lead-hero .hero-texte > *{grid-column:auto!important}
.lead-fil{font-size:13px;opacity:.85;margin-bottom:14px}.lead-fil a{color:inherit}
.lead-puces{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;list-style:none;padding:0}
.lead-puces li{background:rgba(255,250,237,.16);border:1px solid rgba(255,250,237,.45);border-radius:999px;padding:6px 14px;font-size:14px;font-weight:600}
.lead-mascotte{position:absolute!important;inset:auto 150px 0 auto!important;width:420px!important;height:auto!important;object-fit:contain!important;z-index:2;filter:drop-shadow(0 10px 24px rgba(0,0,0,.35))}
section.ss.lead-preuves{padding:44px 0 12px!important}
section.ss.lead-intro{padding-top:20px!important}
.lead-preuves .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;text-align:center}
.lead-preuves b{display:block;font-family:Fraunces,serif;font-size:30px;line-height:1.1}
.lead-preuves span{display:block;font-size:15px;opacity:.75;margin-top:4px}
.lead-intro p{max-width:760px;margin:0 auto;font-size:18px;line-height:1.6}
.lead-offre h2{text-align:center}
.lead-cartes{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}
.lead-cartes figure{margin:0;background:var(--blanc);border-radius:15px;overflow:hidden}
.lead-cartes img{width:100%;aspect-ratio:4/3;height:auto;object-fit:cover;display:block}
.lead-cartes figcaption{padding:16px 18px 20px;font-size:15px;line-height:1.5}
.lead-cartes figcaption b{display:block;font-size:18px;margin-bottom:4px}
.lead-wp{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:center;margin-top:28px;padding:22px 26px;background:var(--blanc);border-radius:15px;color:inherit;text-decoration:none}
.lead-wp img{width:200px;height:auto}
.lead-wp span{font-size:15px;line-height:1.5}.lead-wp b{display:block;font-size:18px;margin-bottom:4px}
@media (max-width:899px){.lead-wp{grid-template-columns:1fr}.lead-wp img{width:160px}}
.lead-final{background:var(--vert);color:var(--creme);text-align:center}
.lead-final .chercheur{max-width:520px;margin:26px auto 0;text-align:start}
@media (max-width:899px){.lead-preuves .wrap,.lead-cartes{grid-template-columns:1fr}.lead-mascotte{position:static!important;display:block;width:230px!important;margin:-12px auto 0;filter:none}.lead-hero{min-height:0}}
</style>
</head>''', 1)
JS = '''<script>document.querySelectorAll('.lead-form').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const t=`Hello, we are planning: ${f.voyage.value}. Dates: ${f.dates.value||'/'} / Adults: ${f.adultes.value||'/'} / Children and babies: ${f.enfants.value||'/'}`;window.open('https://wa.me/33652092301?text='+encodeURIComponent(t),'_blank','noopener')}));</script>
</body>'''
src = src.replace('</body>', JS, 1)
out = os.path.join(ICI, 'preview', 'lead-les-deux-alpes')
os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(src)
print('ok', len(src))
