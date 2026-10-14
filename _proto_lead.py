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
HERO = f'''<section class="hero lead-hero3">
  <img src="/img/chalet/wp-pistes-balcon.jpg" alt="The slopes and the lifts of Les Deux Alpes under a blue sky" width="1600" height="1600" fetchpriority="high">
  <div class="lead3-texte">
    <p class="fil lead-fil"><a href="../../">Home</a> / <a href="../../alps/">The French Alps</a> / Les Deux Alpes</p>
    <div class="lead3-bloc">
    <ul class="lead-puces"><li>Shomer Shabbat</li><li>Strictly kosher</li><li>Minyan on request</li></ul>
    <h1>Strictly kosher<br>in Les Deux Alpes.</h1>
    <p>Your accommodation, a chef or delivered meals, Shabbat and minyan, organised for you.</p>
    <a class="btn-hero" href="https://wa.me/33652092301?text=Hello%2C%20we%20are%20planning%20a%20kosher%20stay%20in%20Les%20Deux%20Alpes.%20Dates%3A%20%2F%20Adults%3A%20%2F%20Children%3A" rel="noopener"><svg><use href="#wa"/></svg>Plan my stay on WhatsApp</a>
    </div>
  </div>
</section>

<section class="ss wrap lead-intro"><img class="lead-mascotte" src="/img/illus/flat-ski.png" alt="" width="700" height="700" loading="lazy"><p>{intro}</p></section>

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
.lead-hero3{position:relative;height:100dvh;min-height:560px;max-height:920px;overflow:hidden;background:#1C1B1F}
.lead-hero3 > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 12%;opacity:.74;filter:saturate(.85)}
.lead-hero3::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,22,.10) 0%,rgba(20,19,22,.38) 45%,rgba(20,19,22,.90) 100%)}
.lead3-texte{position:absolute;left:0;right:0;bottom:0;z-index:1;padding:0 24px 52px;color:#FFFAED;max-width:1248px;margin:0 auto}
.lead3-texte .lead-fil{margin-bottom:18px;opacity:.95;text-shadow:0 1px 8px rgba(0,0,0,.6)}
.lead3-bloc{display:inline-block;max-width:760px;padding:28px 32px 32px;border-radius:24px;background:rgba(20,19,22,.62);backdrop-filter:blur(12px) saturate(.9);-webkit-backdrop-filter:blur(12px) saturate(.9);border:1px solid rgba(255,250,237,.18)}
.lead3-texte h1{font-family:Fraunces,serif;font-weight:300;font-size:clamp(42px,6vw,84px);line-height:.98;letter-spacing:-.015em;margin-top:18px;color:#FFFAED;text-wrap:balance}
.lead3-texte p{margin-top:16px;font-size:clamp(17px,1.5vw,21px);line-height:1.45;max-width:34em;color:#F6EFE0}
.lead3-texte h1,.lead3-texte p{text-shadow:none}
.lead-puces li{background:rgba(20,19,22,.42);border:1px solid rgba(255,250,237,.5);color:#FFFAED}
.btn-hero{display:inline-flex;align-items:center;gap:10px;margin-top:26px;min-height:54px;padding:0 24px;border-radius:999px;background:var(--jaune);color:var(--encre);font-weight:600;font-size:16px;text-decoration:none}
.btn-hero svg{width:20px;height:20px;fill:currentColor}
@media (min-width:900px){.lead3-texte{padding-bottom:72px}}
@media (max-width:899px){.lead3-bloc{padding:20px 20px 24px;border-radius:18px}.lead-hero3 > img{object-position:50% 0;opacity:.68}.lead-hero3::before{background:linear-gradient(180deg,rgba(20,19,22,.12) 0%,rgba(20,19,22,.45) 40%,rgba(20,19,22,.94) 100%)}.lead3-texte{padding-bottom:88px}}
.lead-hero3 .lead-fil a{color:inherit}
.lead-fil{font-size:13px;opacity:.85;margin-bottom:14px}.lead-fil a{color:inherit}
.lead-puces{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;list-style:none;padding:0}
.lead-puces li{background:rgba(255,250,237,.16);border:1px solid rgba(255,250,237,.45);border-radius:999px;padding:6px 14px;font-size:14px;font-weight:600}
.lead-intro{display:grid;gap:18px;align-items:center;justify-items:center;text-align:center}
.lead-intro .lead-mascotte{width:260px;height:auto}
.lead-intro p{max-width:640px;font-size:17px;line-height:1.6}
.lead-offre h2{text-align:center}
.lead-cartes{display:grid;gap:18px;margin-top:28px}
.lead-cartes figure{margin:0;background:var(--blanc);border-radius:15px;overflow:hidden}
.lead-cartes img{width:100%;aspect-ratio:4/3;height:auto;object-fit:cover;display:block}
.lead-cartes figcaption{padding:16px 18px 20px;font-size:15px;line-height:1.5}
.lead-cartes figcaption b{display:block;font-size:18px;margin-bottom:4px}
.lead-wp{display:grid;gap:16px;align-items:center;margin-top:28px;padding:22px 26px;background:var(--blanc);border-radius:15px;color:inherit;text-decoration:none}
.lead-wp img{width:170px;height:auto}
.lead-wp span{font-size:15px;line-height:1.5}.lead-wp b{display:block;font-size:18px;margin-bottom:4px}
.lead-final{background:var(--vert);color:var(--creme);text-align:center}
.lead-final .chercheur{max-width:520px;margin:26px auto 0;text-align:start}
@media (min-width:900px){
  .lead-intro{grid-template-columns:320px 1fr;text-align:start;justify-items:start}
  .lead-intro .lead-mascotte{width:320px}
  .lead-cartes{grid-template-columns:repeat(3,1fr)}
  .lead-wp{grid-template-columns:200px 1fr;gap:24px}.lead-wp img{width:200px}
}
</style>
</head>''', 1)
JS = '''<script>document.querySelectorAll('.lead-form').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const t=`Hello, we are planning: ${f.voyage.value}. Dates: ${f.dates.value||'/'} / Adults: ${f.adultes.value||'/'} / Children and babies: ${f.enfants.value||'/'}`;window.open('https://wa.me/33652092301?text='+encodeURIComponent(t),'_blank','noopener')}));</script>
</body>'''
src = src.replace('</body>', JS, 1)
out = os.path.join(ICI, 'preview', 'lead-les-deux-alpes')
os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(src)
print('ok', len(src))
