# -*- coding: utf-8 -*-
"""Planche de bannières (14/10) : quatre modèles de hero pris dans les bibliothèques UI (Tailwind UI, Flowbite, Booking,
Aman/Black Tomato) montés avec les vrais contenus Mishpacha, pour que l'opérateur choisisse. Aperçu non indexé :
/preview/bannieres/. Le numéro choisi devient le gabarit de _proto_lead.py."""
import io, os
ICI = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(ICI, 'preview', 'lead-les-deux-alpes', 'index.html'), encoding='utf8').read()
head = src[:src.index('<main>')]
tail = src[src.index('</main>'):]
head = head.replace('<title>', '<title>Bannières · ').replace('lead-les-deux-alpes', 'bannieres')
FORM = '''<form class="chercheur lead-form">
  <input type="hidden" name="voyage" value="Kosher stay in Les Deux Alpes">
  <div class="duo"><label><span>Dates</span><input name="dates" type="text" placeholder="9 to 14 December"></label><label><span>Adults</span><input name="adultes" type="text" inputmode="numeric" placeholder="6"></label></div>
  <label><span>Children and babies</span><input name="enfants" type="text" placeholder="3, including a baby"></label>
  <button type="submit"><svg><use href="#wa"/></svg>Get my Deux Alpes programme</button>
  <small>Same-day reply, in English or Hebrew. Never on Shabbat.</small>
</form>'''
H1 = 'Strictly kosher in Les Deux Alpes.'
SUB = 'Your accommodation, a chef or delivered meals, Shabbat and minyan, organised for you.'
PH = '/img/chalet/wp-pistes-balcon.jpg'
PH2 = '/img/chalet/wp-ext-bleu.jpg'
KASH = '<img class="b-kash" src="/img/logo-kashrut-beth-habad-grenoble-alpes.png" alt="Kashrut under the Beth Habad Grenoble-Alpes" width="600" height="470">'

def etiq(n, nom, source):
    return f'<div class="b-etiq"><b>Bannière {n}</b> · {nom} <span>{source}</span></div>'

B1 = etiq(1, 'Photo pleine largeur, titre centré, carte de recherche posée dessous', 'Booking.com, Airbnb · « Hero with search »') + f'''
<section class="b1">
  <div class="b1-photo"><img src="{PH}" alt=""><div class="b1-voile"></div>
    <div class="b1-texte"><h1>{H1}</h1><p>{SUB}</p></div></div>
  <div class="b1-carte">{FORM}</div>
</section>'''

B2 = etiq(2, 'Deux colonnes, texte à gauche, photo à fond perdu à droite', 'Tailwind UI · « Split with image », Context Travel') + f'''
<section class="b2">
  <div class="b2-texte"><p class="fil">Home / The French Alps / Les Deux Alpes</p><h1>{H1}</h1><p>{SUB}</p>{FORM}{KASH}</div>
  <div class="b2-photo"><img src="{PH2}" alt=""></div>
</section>'''

B3 = etiq(3, 'Photo plein écran, titre en bas à gauche, bouton unique, chips', 'Aman, Black Tomato · « Editorial hero »') + f'''
<section class="b3">
  <img src="{PH}" alt="">
  <div class="b3-texte"><ul class="lead-puces"><li>Shomer Shabbat</li><li>Strictly kosher</li><li>Minyan on request</li></ul><h1>{H1}</h1><p>{SUB}</p>
    <a class="btn-hero" href="https://wa.me/33652092301"><svg><use href="#wa"/></svg>Plan my stay on WhatsApp</a></div>
</section>'''

B4 = etiq(4, 'Photo pleine largeur, carte en verre dépoli à droite', 'Flowbite · « Hero with glass card », Expedia') + f'''
<section class="b4">
  <img src="{PH2}" alt="">
  <div class="b4-grille"><div class="b4-texte"><h1>{H1}</h1><p>{SUB}</p>{KASH}</div><div class="b4-verre">{FORM}</div></div>
</section>'''

CSS = '''<style>
body{background:#FFFAED}
.b-etiq{max-width:1200px;margin:48px auto 10px;padding:0 16px;font-size:15px}.b-etiq b{font-size:18px}.b-etiq span{display:block;opacity:.65;font-size:13px}
.b-kash{width:110px;height:auto;margin-top:16px;display:block}
.chercheur{background:#fff;color:#1C1B1F;border-radius:15px;padding:12px;display:grid;gap:10px;max-width:520px}
.lead-form{margin-top:20px}
h1{font-family:Fraunces,serif;font-weight:300;letter-spacing:-.01em;line-height:1.05}
/* 1 */
.b1 .b1-photo{position:relative;height:62vh;min-height:420px;overflow:hidden}
.b1 .b1-photo img{width:100%;height:100%;object-fit:cover;display:block}
.b1-voile{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,22,.25),rgba(20,19,22,.55))}
.b1-texte{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:#fff;padding:24px;text-shadow:0 2px 16px rgba(0,0,0,.5)}
.b1-texte h1{font-size:clamp(34px,6vw,64px);max-width:16ch}.b1-texte p{margin-top:14px;font-size:18px;max-width:38em;color:#F6EFE0}
.b1-carte{max-width:760px;margin:-56px auto 0;padding:0 16px;position:relative}.b1-carte .chercheur{max-width:none;box-shadow:none;border:1px solid #E7E0D2}
/* 2 */
.b2{display:grid;background:#FFFAED}
.b2-texte{padding:40px 24px}.b2-texte h1{font-size:clamp(34px,4.4vw,56px);margin-top:14px}.b2-texte p{margin-top:14px;font-size:17px;max-width:34em}
.b2-photo img{width:100%;height:100%;min-height:360px;object-fit:cover;display:block}
@media(min-width:900px){.b2{grid-template-columns:1.05fr 1fr;min-height:640px}.b2-texte{padding:64px 56px 64px max(24px,calc((100vw - 1200px)/2))}}
/* 3 */
.b3{position:relative;height:88vh;min-height:520px;overflow:hidden;background:#1C1B1F}
.b3 > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.b3::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,22,0) 30%,rgba(20,19,22,.82) 100%)}
.b3-texte{position:absolute;left:0;right:0;bottom:0;padding:0 24px 48px;max-width:1200px;margin:0 auto;color:#fff;z-index:1}
.b3-texte h1{font-size:clamp(36px,6vw,72px);max-width:14ch;margin-top:16px}.b3-texte p{margin-top:12px;font-size:18px;max-width:40em;color:#F6EFE0}
.lead-puces{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.lead-puces li{background:rgba(255,250,237,.16);border:1px solid rgba(255,250,237,.45);border-radius:999px;padding:6px 14px;font-size:14px;font-weight:600}
.btn-hero{display:inline-flex;align-items:center;gap:10px;margin-top:22px;min-height:52px;padding:0 22px;border-radius:999px;background:#FCDE73;color:#1C1B1F;font-weight:600;text-decoration:none}.btn-hero svg{width:20px;height:20px;fill:currentColor}
@media(min-width:900px){.b3-texte{padding-left:max(24px,calc((100vw - 1200px)/2))}}
/* 4 */
.b4{position:relative;min-height:600px;overflow:hidden;background:#1C1B1F}
.b4 > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.b4::after{content:"";position:absolute;inset:0;background:rgba(20,19,22,.35)}
.b4-grille{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:48px 24px;display:grid;gap:28px;color:#fff;align-items:center;min-height:600px}
.b4-texte h1{font-size:clamp(34px,5vw,60px);text-shadow:0 2px 16px rgba(0,0,0,.45)}.b4-texte p{margin-top:14px;font-size:18px;color:#F6EFE0;max-width:34em}
.b4-verre{background:rgba(255,250,237,.78);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-radius:20px;padding:12px}.b4-verre .chercheur{background:transparent;padding:6px;max-width:none}
@media(min-width:900px){.b4-grille{grid-template-columns:1.1fr .9fr;gap:56px}}
</style>'''
page = head.replace('</head>', CSS + '\n</head>') + '<main>' + B1 + B2 + B3 + B4 + '\n<p style="text-align:center;padding:40px 16px">Quatre modèles, mêmes textes, mêmes photos. Le choix devient le gabarit des pages de lead.</p>\n' + tail
out = os.path.join(ICI, 'preview', 'bannieres'); os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(page)
print('ok')
