# -*- coding: utf-8 -*-
"""Formulaire court /contact-quick/ et sa page merci /contact-quick/thanks/ (EN seulement, 31/10, decision Moshe :
   capter le lead « comme Clim69 », puis envoyer au client le lien du tunnel complet /plan-your-trip/ prerempli).
   python _build_contact_quick.py (depuis site-v5/), puis python _charte_lv.py contact-quick/index.html contact-quick/thanks/index.html

   Coquille = /merci/ (en-tete, pied, feuilles valora). Envoi vers le meme Apps Script que le tunnel, memes noms de champs
   (tour, dates, personnes, langue, nom, contact, message, message_en, page, params) + source=court et lead=<id>.
   Aucune donnee personnelle dans l'adresse de la page merci (sessionStorage) ; dans le lien vers le tunnel, prenom et
   numero passent apres le # (jamais envoyes a GA4, qui ne lit pas le fragment)."""
import re, os, html

H = open("merci/index.html", encoding="utf-8").read()
TUNNEL = open("plan-your-trip/index.html", encoding="utf-8").read()
OPTIONS = re.search(r'<select id="f-indicatif"[^>]*>(.*?)</select>', TUNNEL, re.S).group(1)
WA = "https://wa.me/33652092301?text=" + "Hello%2C%20we%20are%20planning%20a%20kosher%20holiday."
SVG_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg>'


def coquille(chemin, titre, desc, corps):
    i, j = H.index("<main>"), H.index("</main>") + 7
    tete, pied = H[:i], H[j:]
    tete = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", tete)
    tete = re.sub(r"<title>.*?</title>", "<title>" + titre + "</title>", tete)
    tete = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + desc + '">', tete)
    tete = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + titre, tete)
    tete = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + desc, tete)
    tete = tete.replace("https://mishpachatours.com/merci/", "https://mishpachatours.com" + chemin)
    page = tete + corps + pied
    page = page.replace('href="../', 'href="/').replace('src="../', 'src="/')   # chemins absolus : la page merci est a 2 niveaux
    d = chemin.strip("/")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="").write(page)
    print("ok", chemin)


# ---------------------------------------------------------------- formulaire court
FORM = f'''<main>
<section class="court" id="court"><div class="court-col">
  <p class="lv-eyebrow">Alps · Lyon</p>
  <h1>Plan your kosher stay</h1>
  <p class="court-sous">Leave your WhatsApp number. We call you back with ideas and prices.</p>
  <form id="formCourt" novalidate autocomplete="on">
    <div class="piege" aria-hidden="true"><label for="c-societe">Company</label><input type="text" id="c-societe" name="societe" tabindex="-1" autocomplete="off"></div>
    <div class="court-champ"><label for="c-prenom">First name</label><input id="c-prenom" name="prenom" autocomplete="given-name" required></div>
    <div class="court-champ"><label for="c-tel">WhatsApp number</label><div class="court-tel"><select id="c-indicatif" name="indicatif" aria-label="Country code" required>{OPTIONS}</select><input type="tel" id="c-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="52 123 4567" required></div></div>
    <div class="court-duo"><div class="court-champ"><label for="c-ou">Where and when?</label><input id="c-ou" name="ou" placeholder="Courchevel, 17 to 24 Jan"></div>
    <div class="court-champ"><label for="c-n">How many?</label><input id="c-n" name="n" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="3" placeholder="8"></div></div>
    <p class="court-facult">Optional: where, when and how many.</p>
    <p class="court-erreur" id="c-erreur" role="alert" hidden>Please add your first name and your WhatsApp number.</p>
    <button type="submit" class="court-envoyer" id="c-envoyer">Send</button>
    <p class="court-note">We answer the same day, never on Shabbat.</p>
    <a class="court-wa" href="{WA}" rel="noopener">{SVG_WA}<span>Or write to us on WhatsApp</span></a>
  </form>
  <noscript><p class="court-note">This form needs JavaScript. <a href="{WA}" rel="noopener">Write to us on WhatsApp</a>.</p></noscript>
</div></section>
</main>'''

JS_FORM = r'''<script>/*CONTACT-QUICK*/(function(){var f=document.getElementById('formCourt');if(!f)return;
var q;try{q=new URLSearchParams(location.search)}catch(x){q=null}
function p(k){var v=q&&q.get(k);return v?v.replace(/[\u0000-\u001f<>]/g,'').trim().slice(0,80):''}
/* indicatif : region de la langue du navigateur, sinon la langue seule */
var R={US:'+1',CA:'+1',GB:'+44',IL:'+972',FR:'+33',BE:'+32',CH:'+41',ES:'+34',IT:'+39',DE:'+49',NL:'+31',AR:'+54',MX:'+52',BR:'+55',AU:'+61',ZA:'+27',RU:'+7',UA:'+380'},
    L={he:'+972',iw:'+972',fr:'+33',es:'+34',it:'+39',de:'+49',nl:'+31',ru:'+7',uk:'+380',pt:'+55'};
var sel=f.indicatif;function poser(v){if(v&&!sel.value&&[].some.call(sel.options,function(o){return o.value===v}))sel.value=v}
(navigator.languages||[navigator.language||'']).forEach(function(l){var m=/^([a-z]{2,3})(?:-([A-Z]{2}))?/i.exec(l||'');if(!m)return;poser(m[2]?R[m[2].toUpperCase()]:'');poser(L[m[1].toLowerCase()])});
if(!sel.value){var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(x){}poser(/Jerusalem|Tel_Aviv/.test(tz)?'+972':/^America\/(New_York|Chicago|Denver|Los_Angeles|Toronto|Montreal)/.test(tz)?'+1':/London/.test(tz)?'+44':/Paris/.test(tz)?'+33':'')}
/* prerempli depuis l'accueil : voyage et dates -> « Where and when? », adultes + enfants -> « How many of you? » */
/* une ligne courte : « Ski and chalet, Courchevel, 17 to 24 Jan 2027 » */
function dt(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);return m?new Date(+m[1],+m[2]-1,+m[3],12):null}
function fm(x,o){try{return x.toLocaleDateString('en-GB',o)}catch(e){return ''}}
var A=dt(p('arrivee')),Dd=dt(p('depart')),per='';
if(A&&Dd){per=A.getFullYear()!==Dd.getFullYear()?fm(A,{day:'numeric',month:'short',year:'numeric'})+' to '+fm(Dd,{day:'numeric',month:'short',year:'numeric'}):
 A.getMonth()!==Dd.getMonth()?fm(A,{day:'numeric',month:'short'})+' to '+fm(Dd,{day:'numeric',month:'short',year:'numeric'}):A.getDate()+' to '+fm(Dd,{day:'numeric',month:'short',year:'numeric'})}
else if(A)per=fm(A,{day:'numeric',month:'short',year:'numeric'});
var COURT={'Ski holiday with a chalet':'Ski and chalet','Hanukkah in the Alps':'Hanukkah in the Alps','Summer in the Alps':'Summer in the Alps'};
var vy=p('voyage'),vy=COURT[vy]||vy||{b:'Kosher meals in my resort',c:'Van transfer',d:'Jewish Lyon tour',e:'Holiday programme'}[p('i')]||'',li=p('lieu'),ou=[vy,li,per].filter(Boolean).join(', ');
if(ou&&!f.ou.value)f.ou.value=ou;
var n=(parseInt(p('adultes'),10)||0)+(parseInt(p('enfants'),10)||0);if(n>0&&!f.n.value)f.n.value=String(n);
var dl=window.dataLayer=window.dataLayer||[],sent=false,err=document.getElementById('c-erreur'),b=document.getElementById('c-envoyer');
f.addEventListener('input',function(ev){var t=ev.target;if(t.getAttribute('aria-invalid')==='true'&&(t.value||'').trim())t.setAttribute('aria-invalid','false')});
f.addEventListener('submit',function(ev){ev.preventDefault();if(sent)return;
 if(f.societe.value){location.href='/contact-quick/thanks/';return}
 var pre=f.prenom.value.trim(),ind=sel.value,tel=f.tel.value.replace(/[^0-9]/g,''),manque=[];
 if(!pre)manque.push(f.prenom);if(!ind)manque.push(sel);if(tel.length<6)manque.push(f.tel);
 [f.prenom,sel,f.tel].forEach(function(e){e.setAttribute('aria-invalid',manque.indexOf(e)>=0?'true':'false')});
 if(manque.length){err.hidden=false;manque[0].focus();return}
 err.hidden=true;
 if(ind!=='+39')tel=tel.replace(/^0+/,'');
 var ouV=f.ou.value.trim().slice(0,200),nV=f.n.value.replace(/[^0-9]/g,'').slice(0,3),
     lead='q'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),
     parts=['Trip: Quick request (short form)'];if(ouV)parts.push('Where and when: '+ouV);if(nV)parts.push('Guests: '+nV);parts.push('Source: short form, ref '+lead);
 var payload=JSON.stringify({tour:'Quick request',dates:'',personnes:nV?nV+' guests':'',langue:'English',nom:pre,contact:(ind+' '+tel).trim(),
   message:parts.join(' | '),message_en:parts.join(' | '),nuits:'',page:location.pathname,params:location.search,source:'court',lead:lead});
 sent=true;var lab=b.textContent;b.disabled=true;b.textContent='Sending';
 var fini=false,ok=function(){if(fini)return;fini=true;
   try{sessionStorage.setItem('mt-court',JSON.stringify({lead:lead,prenom:pre,wa:(ind+tel).replace(/[^0-9]/g,''),q:location.search}))}catch(x){}
   dl.push({event:'generate_lead',branch:'court'});location.href='/contact-quick/thanks/'},
  ko=function(){if(fini)return;fini=true;sent=false;b.disabled=false;b.textContent=lab;
   var t='Hello, I am '+pre+'. '+(ouV?ouV+'. ':'')+(nV?nV+' guests.':'');
   err.hidden=false;err.innerHTML='';err.appendChild(document.createTextNode('Your request did not go through. Send it on WhatsApp in one tap: '));
   var a=document.createElement('a');a.href='https://wa.me/33652092301?text='+encodeURIComponent(t);a.rel='noopener';a.textContent='Send on WhatsApp';err.appendChild(a);dl.push({event:'form_error'})};
 setTimeout(ko,20000);
 try{fetch(window.MISHPACHA_ENDPOINT,{method:'POST',body:payload}).then(function(r){return r.json()}).then(function(j){j&&j.ok?ok():ko()})['catch'](ko)}catch(x){ko()}});
})();</script>'''

# ---------------------------------------------------------------- page merci
MERCI = f'''<main>
<section class="court court-merci"><div class="court-col">
  <p class="lv-eyebrow">Request received</p>
  <h1 id="m-titre">Thank you</h1>
  <p class="court-sous">We answer you on WhatsApp the same day, never on Shabbat or on a Jewish holiday.</p>
  <p class="court-sous">Two minutes now help us prepare a precise programme with the price: dates, chalet, meals, minyan.</p>
  <a class="court-envoyer" id="m-plan" href="/plan-your-trip/">Complete your trip details</a>
  <a class="court-wa" href="https://wa.me/33652092301?text=Hello%2C%20I%20just%20sent%20a%20request%20on%20the%20website." rel="noopener">{SVG_WA}<span>Write to us on WhatsApp</span></a>
  <p class="court-note"><a href="/">Back to the home page</a></p>
</div></section>
</main>'''

JS_MERCI = r'''<script>/*CONTACT-QUICK-MERCI*/(function(){var s=null;try{s=JSON.parse(sessionStorage.getItem('mt-court')||'null')}catch(x){}
if(!s)return;var h=document.getElementById('m-titre'),a=document.getElementById('m-plan');
if(s.prenom)h.textContent='Thank you, '+s.prenom;
/* lien vers le tunnel complet : parametres non personnels en requete (lead, type, lieu, dates, groupe), prenom et numero apres le # */
var q=new URLSearchParams(s.q||''),o=new URLSearchParams();o.set('lead',s.lead||'');
['i','voyage','lieu','arrivee','depart','adultes','enfants'].forEach(function(k){if(q.get(k))o.set(k,q.get(k))});
var fr=new URLSearchParams();if(s.prenom)fr.set('prenom',s.prenom);if(s.wa)fr.set('wa',s.wa);
a.href='/plan-your-trip/?'+o.toString()+'#'+fr.toString()})();</script>'''

CSS = '''<style>/*CONTACT-QUICK*/
.court{background:#fff;padding:14px 16px 32px}
.court-col{max-width:440px;margin:0 auto}
.court h1{font:300 23px/1.2 'Jost',system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em;margin:4px 0 6px;color:#111}
.court .lv-eyebrow{font:400 11px/1 'Jost',system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#5B3A29;margin:0}
.court-sous{font:300 15px/1.45 'Jost',system-ui,sans-serif;color:#444;margin:0 0 14px}
.court-champ{margin:0 0 10px}
.court-champ label{display:block;font:400 11px/1.4 'Jost',system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#111;margin:0 0 4px}
.court-champ label small{letter-spacing:.06em;text-transform:none;color:#6B6B6B;font-weight:300;margin-left:6px}
.court input,.court select{width:100%;height:46px;border:1px solid #CFCFCF;border-radius:4px;background:#fff;color:#111;font:300 16px/1 'Jost',system-ui,sans-serif;padding:0 12px;-webkit-appearance:none;appearance:none;box-sizing:border-box}
.court select{background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23111' stroke-width='1.2'/%3E%3C/svg%3E") no-repeat right 10px center;padding-right:28px}
.court input:focus,.court select:focus{outline:none;border-color:#111}
.court [aria-invalid=true]{border-color:#9B1C1C}
.court-tel{display:grid;grid-template-columns:118px 1fr;gap:8px}
.court-duo{display:grid;grid-template-columns:1fr 84px;gap:8px}
.court-duo .court-champ{margin:0}
.court-duo{margin:0 0 10px}
.court-envoyer{display:flex;align-items:center;justify-content:center;width:100%;height:52px;margin:6px 0 0;background:#111;color:#fff;border:1px solid #111;border-radius:4px;font:400 13px/1 'Jost',system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;cursor:pointer;text-decoration:none}
.court-envoyer:disabled{opacity:.6}
.court-note{font:300 13px/1.5 'Jost',system-ui,sans-serif;color:#6B6B6B;margin:10px 0 0;text-align:center}
.court-note a{color:#111}
.court-wa{display:flex;align-items:center;justify-content:center;gap:8px;margin:14px 0 0;color:#111;font:400 12px/1 'Jost',system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:underline;text-underline-offset:4px}
.court-wa svg{width:18px;height:18px;fill:currentColor}
.court-facult{font:300 12px/1.4 'Jost',system-ui,sans-serif;color:#6B6B6B;margin:-4px 0 10px}
.court-erreur{font:400 14px/1.4 'Jost',system-ui,sans-serif;color:#9B1C1C;margin:0 0 8px}
.court-erreur a{color:#111;font-weight:500}
.court .piege{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.court-merci .court-envoyer{margin-top:24px}
@media (min-width:900px){.court{padding:72px 16px 96px}.court h1{font-size:32px}}
</style>'''


coquille("/contact-quick/", "Plan your kosher stay | Mishpacha Tours",
         "Leave your first name and WhatsApp number. We call you back the same day with ideas and prices, never on Shabbat.",
         CSS + FORM + JS_FORM)
coquille("/contact-quick/thanks/", "Thank you | Mishpacha Tours",
         "Your request has been received. We answer on WhatsApp the same day, never on Shabbat.",
         CSS + MERCI + JS_MERCI)
