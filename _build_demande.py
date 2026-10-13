# -*- coding: utf-8 -*-
"""Genere /plan-your-trip/ : le formulaire complet de demande (sejours Alpes + visites de Lyon), lien a partager.
   python _build_demande.py (depuis site-v5/). Envoi vers le meme Apps Script que les autres formulaires :
   colonnes tour / dates / personnes / langue / nom / contact, tout le reste concatene dans `message`."""
from _head import head_page, webpage, crumbs, BASE
import re, os, json
home = open("_gabarit.html", encoding="utf-8").read()
head = home[:home.index("<main>")]; foot = home[home.index("</main>")+7:]
def rel(s):
    for a, b in [('href="img/','href="../img/'),('src="img/','src="../img/'),('src="fonts/','src="../fonts/'),('href="fonts/','href="../fonts/'),
                 ('href="styles.css"','href="../styles.css"'),('href="./"','href="../"'),('href="#tours"','href="../#tours"'),('href="#why"','href="../#why"'),
                 ('href="#before"','href="../#before"'),('href="#guide"','href="../#guide"'),('href="fr/"','href="../fr/"'),('href="es/"','href="../es/"'),
                 ('href="he/"','href="../he/"'),('href="credits.html"','href="../credits.html"'),('href="#book"','href="#demande"'),('href="jewish-lyon-guide/"','href="../jewish-lyon-guide/"')]:
        s = s.replace(a, b)
    return s
P = "/plan-your-trip/"
TITLE = "Plan your kosher trip to the Alps or Lyon | Mishpacha Tours"
DESC = "One form for your whole trip: dates, family, chalet or hotel, chef and meals, Shabbat and minyan, transfers, ski, tours of Lyon. You get a day-by-day programme with the price."
h = rel(head)
h = re.sub(r"<title>.*?</title>", "<title>" + TITLE + "</title>", h)
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', h)
h = head_page(h, P, TITLE.split(" | ")[0], DESC, [webpage(P, TITLE.split(" | ")[0], DESC), crumbs([("Plan your trip", P)])])

def chips(name, opts, multi=True):
    t = "checkbox" if multi else "radio"
    return '<div class="dm-chips">' + "".join(f'<label><input type="{t}" name="{name}" value="{o}"><span>{o}</span></label>' for o in opts) + "</div>"
def champ(id_, label, typ="text", ph="", req=False, extra=""):
    r = " required" if req else ""
    return f'<div class="dm-champ"><label for="{id_}">{label}</label><input type="{typ}" id="{id_}" name="{id_}" placeholder="{ph}"{r}{extra}></div>'
def zone(id_, label, ph=""):
    return f'<div class="dm-champ"><label for="{id_}">{label}</label><textarea id="{id_}" name="{id_}" rows="3" placeholder="{ph}"></textarea></div>'
def bloc(id_, titre, sous, corps, cls=""):
    return f'<fieldset class="dm-bloc {cls}" id="{id_}"><legend><h2>{titre}</h2><p>{sous}</p></legend>{corps}</fieldset>'

body = f'''<main>
<section class="pratique-hero"><div class="wrap">
  <p class="fil"><a href="../">Home</a> / Plan your trip</p>
  <div class="pratique-tete"><div><h1>Plan your <i>kosher trip</i></h1>
  <p class="intro-fiche">One form for everything: a stay in the Alps, a tour of Lyon, or both. Fill in what you know and skip the rest. You receive a day-by-day programme with the price, usually within one business day, never on Shabbat.</p>
  <p class="intro-fiche"><b>In a hurry?</b> <a href="https://wa.me/33652092301?text=Hello%2C%20we%20are%20planning%20a%20kosher%20trip.%20Dates%3A%20%2F%20Adults%3A%20%2F%20Children%3A" rel="noopener">Message us on WhatsApp</a> and we ask the questions ourselves.</p></div>
  <img class="hassid-grand" src="../img/picto-hassid.svg" alt="" width="68" height="95"></div>
</div></section>

<section class="ss wrap demande" id="demande">
<form id="formDemande" novalidate>
  <div class="piege" aria-hidden="true"><label for="f-societe">Company</label><input type="text" id="f-societe" name="societe" tabindex="-1" autocomplete="off"></div>

  {bloc("b-voyage", "1. Your trip", "Tick everything that applies.",
    chips("voyage", ["Ski holiday with a chalet", "Kosher meals in a resort I already booked", "Hanukkah in the Alps", "Pesach in the Alps", "Summer in the Alps", "Jewish Lyon tour", "Stopover in Lyon between the airport and the resort", "Something else"]) +
    champ("lieu", "Resort, town or region you have in mind", ph="Courchevel, Les Deux Alpes, not sure yet"))}

  {bloc("b-dates", "2. Dates", "Approximate is fine.",
    '<div class="dm-duo">' + champ("arrivee", "Arrival", ph="9 December 2026") + champ("depart", "Departure", ph="14 December 2026") + '</div>' +
    chips("flexible", ["Dates are flexible", "Dates are fixed", "We must be settled before Shabbat comes in"]))}

  {bloc("b-groupe", "3. Who is coming", "Children's ages help us choose rooms, ski school and cots.",
    '<div class="dm-trio">' + champ("adultes", "Adults", ph="6", extra=' inputmode="numeric"') + champ("enfants", "Children (ages)", ph="2 (9 and 12)") + champ("bebes", "Babies (cots needed)", ph="1 (10 months)") + '</div>' +
    champ("hommes", "Men over bar mitzvah age, for the minyan", ph="4", extra=' inputmode="numeric"'))}

  {bloc("b-logement", "4. Accommodation", "Where would you like to sleep?",
    chips("logement", ["A private chalet for our group", "Apartments in the same residence", "A hotel", "Already booked, I need services only", "Advise me"]) +
    champ("chambres", "Bedrooms and bathrooms needed", ph="5 bedrooms, 3 bathrooms") +
    chips("logement_opt", ["Close to the Beth Chabad or the shul", "Ski-in ski-out or very close to the slopes", "Daily cleaning", "Laundry"]))}

  {bloc("b-repas", "5. Meals and kashrut", "Our team cooks or delivers; tell us your standard.",
    chips("repas", ["A private chef cooking in the chalet", "Meals delivered every day", "Shabbat meals only", "Breakfast and dinner, lunch on the slopes", "Kosher groceries stocked before we arrive"]) +
    chips("cacherout", ["Chalav Yisrael", "Pas Yisrael", "Glatt / Beit Yosef", "Chassidic shechita", "Kitniyot-free (Pesach)", "Gluten-free or allergies"]) +
    champ("cacherout_detail", "Anything else about kashrut, allergies or preferences", ph="One vegetarian, nut allergy for a child"))}

  {bloc("b-religieux", "6. Shabbat, prayer and holidays", "What do you need on site?",
    chips("religieux", ["Minyan on Shabbat", "Minyan every day", "Sefer Torah in the chalet", "Shabbat candles, wine and challot provided", "Hot plate and urn for Shabbat", "Eruv or carrying advice", "Mikveh nearby", "Lulav, Chanukah menorah or other holiday items"]) +
    champ("rite", "Nusach or community, if it matters for the minyan", ph="Chabad, Ashkenaz, Sefarad, Edot HaMizrach"))}

  {bloc("b-transport", "7. Getting there and around", "We organise transfers from the airport and in the resort.",
    chips("aeroport", ["Flying to Lyon", "Flying to Geneva", "Flying to Paris then train", "Arriving by car", "Not decided yet"], multi=False) +
    champ("vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30") +
    chips("transport", ["Private transfer airport to resort", "A van with driver during the stay", "A rental car", "Help with flights"]))}

  {bloc("b-ski", "8. Ski and activities", "For winter stays.",
    chips("ski", ["Ski passes", "Equipment rental delivered to the chalet", "Ski school for children", "Private instructor", "Non-skiers in the group", "Snowshoeing, sledging, dog sledding", "Spa, massage"]) +
    champ("niveau", "Ski levels in the group", ph="4 good skiers, 2 beginners, 2 children in ski school"))}

  {bloc("b-lyon", "9. Lyon", "If you pass through Lyon, or come for the city itself.",
    chips("lyon", ["Jewish Lyon walk with the Grande Synagogue (2.5 h)", "Stopover (3 h) between flight and resort", "Memory: CHRD museum", "Memory: Montluc prison and Neveh Shalom", "Day trip to the Maison d'Izieu", "Kosher restaurant recommendations", "Shabbat in Lyon with a Chabad family"]) +
    chips("langue_visite", ["English", "French", "Spanish"], multi=False))}

  {bloc("b-extras", "10. Extras and comfort", "Optional.",
    chips("extras", ["Babysitter", "Professional security escort (quoted separately)", "Birthday, bar or bat mitzvah, or simcha to celebrate", "Photographer", "Someone in the group with reduced mobility"]) +
    champ("budget", "Budget you have in mind (optional)", ph="Around 30 000 €, or no idea yet") +
    zone("message", "Anything else we should know", "Last year we went to Switzerland. We want to be two minutes from the shul."))}

  {bloc("b-contact", "11. How to reach you", "We answer on WhatsApp first.",
    '<div class="dm-duo">' + champ("nom", "Your name", req=True, extra=' autocomplete="name"') + champ("ville", "Where you live", ph="Brooklyn, London, Tel Aviv") + '</div>' +
    '<div class="dm-champ"><label for="f-tel">WhatsApp number</label><div class="tel"><select id="f-indicatif" name="indicatif" aria-label="Country code" required><option value="">Code</option><option value="+1">+1 US / CA</option><option value="+44">+44 UK</option><option value="+972">+972 IL</option><option value="+33">+33 FR</option><option value="+32">+32 BE</option><option value="+41">+41 CH</option><option value="+34">+34 ES</option><option value="+39">+39 IT</option><option value="+49">+49 DE</option><option value="+31">+31 NL</option><option value="+54">+54 AR</option><option value="+52">+52 MX</option><option value="+55">+55 BR</option><option value="+61">+61 AU</option><option value="+27">+27 ZA</option><option value="+7">+7 RU</option><option value="+380">+380 UA</option></select><input type="tel" id="f-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="212 555 0100" pattern="[0-9 ().-]{{6,16}}" required></div></div>' +
    champ("email", "Email (optional)", typ="email", extra=' autocomplete="email"') +
    chips("langue", ["English", "Hebrew", "French", "Spanish"], multi=False) +
    chips("urgence", ["No rush", "Within a week please", "Urgent, we travel soon"], multi=False), "dm-contact")}

  <p class="dm-erreur" id="dm-erreur" hidden>Please add your name and WhatsApp number so we can answer.</p>
  <div class="dm-envoi"><button class="btn-noir large" type="submit">Send my request</button><small>You receive a day-by-day programme with the price. No payment on this page.</small></div>
</form>
</section>
</main>'''

JS = '''<script>
(function(){var f=document.getElementById('formDemande');if(!f)return;
var LAB={voyage:'Trip',lieu:'Resort or place',arrivee:'Arrival',depart:'Departure',flexible:'Dates',adultes:'Adults',enfants:'Children',bebes:'Babies',hommes:'Men for minyan',logement:'Accommodation',chambres:'Rooms',logement_opt:'Accommodation options',repas:'Meals',cacherout:'Kashrut',cacherout_detail:'Kashrut details',religieux:'Religious needs',rite:'Nusach',aeroport:'Airport',vol:'Flights',transport:'Transport',ski:'Ski',niveau:'Ski levels',lyon:'Lyon',langue_visite:'Tour language',extras:'Extras',budget:'Budget',message:'Message',ville:'Lives in',urgence:'Urgency'};
function val(n){var els=f.querySelectorAll('[name="'+n+'"]');if(!els.length)return '';if(els[0].type==='checkbox'||els[0].type==='radio'){var v=[];els.forEach(function(e){if(e.checked)v.push(e.value)});return v.join(', ')}return els[0].value.trim()}
f.addEventListener('submit',function(ev){ev.preventDefault();
if(f.elements.societe&&f.elements.societe.value){location.href='/merci/';return}
var nom=val('nom'),tel=val('tel'),ind=val('indicatif');var err=document.getElementById('dm-erreur');
if(!nom||!tel||!ind){err.hidden=false;err.scrollIntoView({behavior:'smooth',block:'center'});return}
var parts=[];Object.keys(LAB).forEach(function(k){var v=val(k);if(v)parts.push(LAB[k]+': '+v)});
var dates=[val('arrivee'),val('depart')].filter(Boolean).join(' to ');
var pers=val('adultes')?val('adultes')+' adults':'';if(val('enfants'))pers+=(pers?' + ':'')+val('enfants')+' children';if(val('bebes'))pers+=(pers?' + ':'')+val('bebes')+' babies';
var payload=JSON.stringify({tour:'FULL REQUEST: '+(val('voyage')||'not specified'),dates:dates,personnes:pers,langue:val('langue'),nom:nom,contact:(ind+' '+tel.replace(/[^0-9]/g,'')).trim()+(val('email')?' / '+val('email'):''),message:parts.join(' | '),page:location.pathname,params:location.search});
try{var u=window.MISHPACHA_ENDPOINT||'ENDPOINT_APPS_SCRIPT_A_POSER';if(navigator.sendBeacon){navigator.sendBeacon(u,new Blob([payload],{type:'text/plain;charset=UTF-8'}))}else{fetch(u,{method:'POST',mode:'no-cors',keepalive:true,body:payload})}}catch(e){}
location.href='/merci/'})})();
</script>'''
f = rel(foot).replace("document.getElementById('chercheur').addEventListener", "document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
f = f.replace('<script src="/config.js"></script>', '<script src="/config.js"></script>\n' + JS, 1)
os.makedirs("plan-your-trip", exist_ok=True); open("plan-your-trip/index.html", "w", encoding="utf-8").write(h + body + f); print("ok plan-your-trip")
