# -*- coding: utf-8 -*-
"""Genere /plan-your-trip/ (EN) et remplace le formulaire des copies fr/ es/ he/ : formulaire de demande EN ETAPES (14/10).
   python _build_demande.py (depuis site-v5/). Une question (ou un petit groupe) par ecran, des branches selon l'intention
   (sejour complet / j'ai deja mon logement / van / Lyon / fete / autre), barre de progression, recapitulatif, etat en sessionStorage.
   Envoi vers le meme Apps Script que les autres formulaires, MEMES champs et MEME format qu'avant (le 13/10) :
   colonnes tour / dates / personnes / langue / nom / contact, tout le reste concatene dans `message`.
   Les textes viennent de _demande_textes.py (page du 13/10, relue en 4 langues) et _demande_nouveaux.py (textes de l'11/10 : etapes).
   Les copies traduites gardent leur hero et leur pied ; seuls la section du formulaire et son script sont remplaces."""
from _head import head_page, webpage, crumbs, BASE
from _demande_nouveaux import t, LAB, LAB_NEW, JSX
import re, os, json, html, io

LANGS = ("en", "fr", "es", "he")
LOCALE = {"en": "en-GB", "fr": "fr-FR", "es": "es-ES", "he": "he-IL"}
MERCI = {"en": "/merci/", "fr": "/fr/merci/", "es": "/es/merci/", "he": "/he/merci/"}

# ---------------------------------------------------------------- page EN (tete, hero)
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
DESC = "One form for your whole trip: dates, family, chalet or hotel, chef and meals, Shabbat and minyan, transfers, ski, Lyon tours. You get a day-by-day programme with the price."
h = rel(head)
h = re.sub(r"<title>.*?</title>", "<title>" + TITLE + "</title>", h)
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', h)
h = head_page(h, P, TITLE.split(" | ")[0], DESC, [webpage(P, TITLE.split(" | ")[0], DESC), crumbs([("Plan your trip", P)])])

HERO_EN = '''<main>
<section class="pratique-hero"><div class="wrap">
  <p class="fil"><a href="../">Home</a> / Plan your trip</p>
  <div class="pratique-tete"><div><h1>Plan your <i>kosher trip</i></h1>
  <p class="intro-fiche">One form for everything: a stay in the Alps, a tour of Lyon, or both. Fill in what you know and skip the rest. You receive a day-by-day programme with the price, usually within one business day, never on Shabbat.</p>
  <p class="intro-fiche"><b>In a hurry?</b> <a href="https://wa.me/33652092301?text=Hello%2C%20we%20are%20planning%20a%20kosher%20trip.%20Dates%3A%20%2F%20Adults%3A%20%2F%20Children%3A" rel="noopener">Message us on WhatsApp</a> and we ask the questions ourselves.</p></div>
  <img class="hassid-grand" src="../img/picto-hassid.svg" alt="" width="68" height="95"></div>
</div></section>

'''

# ---------------------------------------------------------------- le formulaire, par langue
# Branches : a sejour complet, b j'ai deja mon logement, c van, d Lyon, e fete, f autre
PATHS = {
    "a": ["intention", "quoi", "dates", "groupe", "logement", "repas", "cacherout", "religieux", "transport", "ski", "lyon", "extras", "final"],
    "b": ["intention", "ou", "dates", "groupe", "religieux", "repas", "cacherout", "message", "final"],
    "c": ["intention", "trajet", "quand", "groupe", "bagages", "message", "final"],
    "d": ["intention", "lyon", "dates", "groupe", "message", "final"],
    "e": ["intention", "fete", "dates", "groupe", "logement", "repas", "cacherout", "religieux", "extras", "final"],
    "f": ["intention", "message", "dates", "groupe", "final"],
}
LAB_ORDER = ["voyage", "lieu", "adresse", "van_depart", "van_arrivee", "arrivee", "depart", "heure", "flexible", "adultes", "enfants", "bebes", "hommes", "bagages",
             "logement", "chambres", "logement_opt", "repas", "repas_jours", "cacherout", "cacherout_detail", "religieux", "rite", "aeroport", "vol", "transport",
             "ski", "niveau", "lyon", "langue_visite", "extras", "budget", "message", "ville", "urgence"]
INDICATIFS = '<option value="">{code}</option>' + "".join(f'<option value="{v}">{v} {c}</option>' for v, c in [
    ("+1", "US / CA"), ("+44", "UK"), ("+972", "IL"), ("+33", "FR"), ("+32", "BE"), ("+41", "CH"), ("+34", "ES"), ("+39", "IT"), ("+49", "DE"), ("+31", "NL"),
    ("+54", "AR"), ("+52", "MX"), ("+55", "BR"), ("+61", "AU"), ("+27", "ZA"), ("+7", "RU"), ("+380", "UA")])

def esc(s): return html.escape(s, quote=True)

def formulaire(lang):
    T = lambda s: t(s, lang)
    E = lambda s: esc(t(s, lang))
    IMG = "../img/" if lang == "en" else "/img/"
    def battr(b): return f' data-b="{b}"' if b else ""
    def chips(name, opts, multi=True, b=""):
        """opts : texte EN, ou (texte EN, branches, cle)."""
        typ = "checkbox" if multi else "radio"
        out = []
        for o in opts:
            en, ob, k = (o, "", "") if isinstance(o, str) else (o + ("", ""))[:3]
            kk = f' data-k="{k}"' if k else ""
            out.append(f'<label{battr(ob)}><input type="{typ}" name="{name}" value="{E(en)}"{kk}><span>{E(en)}</span></label>')
        return f'<div class="dm-chips"{battr(b)}>' + "".join(out) + "</div>"
    def champ(id_, name, label, typ="text", ph="", b="", extra=""):
        phh = f' placeholder="{E(ph)}"' if ph else ""
        return f'<div class="dm-champ"{battr(b)}><label for="{id_}">{E(label)}</label><input type="{typ}" id="{id_}" name="{name}"{phh}{extra}></div>'
    def zone(id_, name, label, ph, b=""):
        return f'<div class="dm-champ"{battr(b)}><label for="{id_}">{E(label)}</label><textarea id="{id_}" name="{name}" rows="3" placeholder="{E(ph)}"></textarea></div>'
    def compteur(name, label, b=""):
        return (f'<div class="dm-cpt"{battr(b)}><span class="lib" id="l-{name}">{E(label)}</span><div class="cpt">'
                f'<button type="button" class="moins" aria-label="{E("Fewer")}: {E(label)}">&#8722;</button>'
                f'<input type="number" id="c-{name}" name="{name}" min="0" max="99" value="0" inputmode="numeric" aria-labelledby="l-{name}">'
                f'<button type="button" class="plus" aria-label="{E("More")}: {E(label)}">+</button></div></div>')
    def ages(name, label, ph):
        return (f'<div class="dm-champ dm-ages cache" data-for="{name}"><label for="c-{name}_ages">{E(label)}</label>'
                f'<input type="text" id="c-{name}_ages" name="{name}_ages" placeholder="{E(ph)}"></div>')
    def etape(id_, titres, aide, corps, cls=""):
        """titres : texte EN, ou liste de (texte EN, branches)."""
        if isinstance(titres, str): titres = [(titres, "")]
        hs = "".join(f'<h2 tabindex="-1"{battr(b)}>{E(x)}</h2>' for x, b in titres)
        if isinstance(aide, str): aide = [(aide, "")]
        ps = "".join(f'<p{battr(b)}>{E(x)}</p>' for x, b in aide)
        return f'<div class="dm-bloc etape {cls}" id="e-{id_}" data-e="{id_}" role="group"><div class="dm-tete">{hs}{ps}</div>{corps}</div>\n'

    # ---- intention : grosses tuiles
    def tuile(val, icone, titre, sous, voyage):
        return (f'<label class="dm-tuile"><input type="radio" name="intention" value="{val}" data-voyage="{E(voyage)}">'
                f'<img src="{IMG}des/{icone}.webp" alt="" width="64" height="64" loading="lazy"><b>{E(titre)}</b><span>{E(sous)}</span></label>')
    tuiles = '<div class="dm-tuiles">' + "".join([
        tuile("a", "mountain-snow", "A full stay in the Alps", "Chalet, chef, Shabbat, minyan and transfers, all organised.", "A full stay in the Alps"),
        tuile("b", "house", "I already have my accommodation", "Minyan, Sefer Torah, Shabbat and meals where you stay.", "Services where we already stay (minyan, Sefer Torah, meals)"),
        tuile("c", "car", "A van transfer", "From point A to point B, with a driver.", "Van transfer, point A to point B"),
        tuile("d", "landmark", "A Jewish Lyon tour", "A guided walk in English, French or Spanish.", "Jewish Lyon tour"),
        tuile("e", "sparkles", "Pesach or a holiday", "A full programme for the holiday, at the kosher standard you keep.", "Holiday programme (Pesach or other)"),
        tuile("f", "message-circle", "Something else", "Tell us in your own words.", "Something else"),
    ]) + "</div>"
    hassid = f'<img class="dm-hassid" src="{IMG}picto-hassid-vert.svg" alt="" width="200" height="200">'
    S = []
    S.append(etape("intention", "What can we do for you?", "Pick the closest one. The next questions depend on it.",
                   '<div class="dm-accueil">' + tuiles + hassid + "</div>", "dm-intention"))
    # ---- a : sejour complet
    S.append(etape("quoi", "What kind of stay, and where?", "Tick everything that applies. A region is enough.",
                   chips("voyage", ["Ski holiday with a chalet", "Hanukkah in the Alps", "Pesach in the Alps", ("Summer in the Alps", "", "summer"), "Something else"]) +
                   champ("lieu-quoi", "lieu", "Resort, town or region you have in mind", ph="Courchevel, Les Deux Alpes, not sure yet")))
    # ---- b : j'ai deja mon logement
    S.append(etape("ou", "Where are you staying?", "The resort and the address of your chalet, apartment or hotel.",
                   champ("lieu-ou", "lieu", "Resort or town", ph="Morzine, Châtel, Les Deux Alpes") +
                   champ("adresse", "adresse", "Address or name of the accommodation", ph="Chalet Le Sapin, 12 route du Lac")))
    # ---- e : fete
    S.append(etape("fete", "Which holiday?", "Tick the holiday or holidays, and the place if you know it.",
                   chips("voyage", ["Pesach in the Alps", "Hanukkah in the Alps", "Sukkot", "Rosh Hashanah and Yom Kippur", "Purim", "Shavuot", "Another holiday"]) +
                   champ("lieu-fete", "lieu", "Resort, town or region you have in mind", ph="Courchevel, Les Deux Alpes, not sure yet")))
    # ---- dates (a b d e f)
    S.append(etape("dates", "When do you travel?", "Approximate is fine.",
                   '<div class="dm-duo">' + champ("arrivee", "arrivee", "Arrival", typ="date") + champ("depart", "depart", "Departure", typ="date") + "</div>" +
                   chips("flexible", ["Dates are flexible", "Dates are fixed", "We must be settled before Shabbat comes in"])))
    # ---- van : trajet, quand, bagages
    S.append(etape("trajet", "Where from, and where to?", "Address, airport, station or hotel. A town name is enough.",
                   champ("van_depart", "van_depart", "Pick-up point", ph="Lyon Saint-Exupéry airport") +
                   champ("van_arrivee", "van_arrivee", "Drop-off point", ph="Les Deux Alpes, chalet")))
    S.append(etape("quand", "When?", "Date and pick-up time. Add the flight if you land.",
                   '<div class="dm-duo">' + champ("arrivee-van", "arrivee", "Date", typ="date") + champ("heure", "heure", "Pick-up time", typ="time") + "</div>" +
                   champ("vol-van", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30")))
    S.append(etape("bagages", "Luggage and equipment", "Skis and baby seats change the vehicle we send.",
                   chips("bagages", ["Large suitcases", "Cabin bags only", "Skis or snowboards", "Baby seats or boosters", "Wheelchair or walker"])))
    # ---- groupe (tous)
    S.append(etape("groupe", "Who is coming?", "Children's ages help us choose rooms, ski school and cots.",
                   compteur("adultes", "Adults") + compteur("enfants", "Children") +
                   ages("enfants", "Ages of the children", "9 and 12") +
                   compteur("bebes", "Babies") + ages("bebes", "Ages of the babies", "10 months") +
                   compteur("hommes", "Men over bar mitzvah age, for the minyan", b="abe")))
    # ---- logement (a e)
    S.append(etape("logement", "Where would you like to sleep?", "Pick what suits you. We advise if you are not sure.",
                   chips("logement", ["A private chalet for our group", "Apartments in the same residence", "A hotel", "Advise me"]) +
                   champ("chambres", "chambres", "Bedrooms and bathrooms needed", ph="5 bedrooms, 3 bathrooms") +
                   chips("logement_opt", ["Close to the Beth Chabad or the shul", "Ski-in ski-out or very close to the slopes", "Daily cleaning", "Laundry"])))
    # ---- repas (a b e)
    S.append(etape("repas", "Which meals do you need?", "Our team cooks or delivers; tell us your standard.",
                   chips("repas", [("A private chef cooking in the chalet", "ae"), "Meals delivered every day", "Shabbat meals only", "Breakfast and dinner, lunch on the slopes",
                                   "Kosher groceries stocked before we arrive", ("No meals needed", "", "none")]) +
                   champ("repas_jours", "repas_jours", "Which days?", ph="Shabbat only, or every day from 25 July to 15 August")))
    S.append(etape("cacherout", "Your kashrut standard", "Tick what you keep. We follow it exactly.",
                   chips("cacherout", ["Chalav Yisrael", "Pas Yisrael", "Glatt / Beit Yosef", "Chassidic shechita", "Kitniyot-free (Pesach)", "Gluten-free or allergies"]) +
                   champ("cacherout_detail", "cacherout_detail", "Anything else about kashrut, allergies or preferences", ph="One vegetarian, nut allergy for a child")))
    S.append(etape("religieux", "Shabbat, prayer and holidays", "What do you need on site?",
                   chips("religieux", ["Minyan on Shabbat", "Minyan every day", "Sefer Torah in the chalet", "Shabbat candles, wine and challot provided", "Hot plate and urn for Shabbat",
                                       "Eruv or carrying advice", "Mikveh nearby", "Lulav, Chanukah menorah or other holiday items"]) +
                   champ("rite", "rite", "Nusach or community, if it matters for the minyan", ph="Chabad, Ashkenaz, Sefarad, Edot HaMizrach")))
    S.append(etape("transport", "Getting there and around", "We organise transfers from the airport and in the resort.",
                   chips("aeroport", ["Flying to Lyon", "Flying to Geneva", "Flying to Paris then train", "Arriving by car", "Not decided yet"], multi=False) +
                   champ("vol", "vol", "Flight numbers or landing times, if known", ph="Landing 11:40, departing 15:30") +
                   chips("transport", ["Private transfer airport to resort", "A van with driver during the stay", "A rental car", "Help with flights"])))
    S.append(etape("ski", "Ski and activities", "For winter stays.",
                   chips("ski", ["Ski passes", "Equipment rental delivered to the chalet", "Ski school for children", "Private instructor", "Non-skiers in the group",
                                 "Snowshoeing, sledging, dog sledding", "Spa, massage"]) +
                   champ("niveau", "niveau", "Ski levels in the group", ph="4 good skiers, 2 beginners, 2 children in ski school")))
    S.append(etape("lyon", "A visit in Lyon?", "Tick the visits that interest you. Tours are held in English, French or Spanish.",
                   chips("lyon", ["Jewish Lyon walk with the Grande Synagogue (2.5 h)", "Stopover (3 h) between flight and resort", "Memory: CHRD museum",
                                  "Memory: Montluc prison and Neveh Shalom", "Day trip to the Maison d'Izieu", "Kosher restaurant recommendations", "Shabbat in Lyon with a Chabad family"]) +
                   f'<p class="dm-sous">{E("Language of the visit")}</p>' + chips("langue_visite", ["English", "French", "Spanish"], multi=False)))
    S.append(etape("extras", "Extras and budget", "Everything here is optional.",
                   chips("extras", ["Babysitter", "Professional security escort (quoted separately)", "Birthday, bar or bat mitzvah, or simcha to celebrate", "Photographer",
                                    "Someone in the group with reduced mobility"], b="a") +
                   champ("budget", "budget", "Budget you have in mind (optional)", ph="Around 30 000 €, or no idea yet") +
                   zone("message-extras", "message", "Anything else we should know", "Last year we went to Switzerland. We want to be two minutes from the shul.")))
    S.append(etape("message", [("Anything else we should know?", "bcd"), ("Tell us what you have in mind", "f")],
                   [("Optional.", "bcd"), ("Write it the way you would say it. We take it from there.", "f")],
                   zone("message-bcd", "message", "Anything else we should know", "Anything that helps: a baby, a late arrival, a special diet.", b="bcd") +
                   zone("message-f", "message", "Tell us what you have in mind", "A bar mitzvah weekend in the Alps for 30 guests", b="f")))
    # ---- final : recapitulatif + contact
    contact = ('<div class="dm-duo">' + champ("nom", "nom", "Your name", extra=' autocomplete="name" required') + champ("ville", "ville", "Where you live", ph="Brooklyn, London, Tel Aviv") + "</div>" +
        f'<div class="dm-champ"><label for="f-tel">{E("WhatsApp number")}</label><div class="tel"><select id="f-indicatif" name="indicatif" aria-label="{E("Country code")}" required>'
        + INDICATIFS.replace("{code}", E("Code")) + '</select><input type="tel" id="f-tel" name="tel" inputmode="tel" autocomplete="tel-national" placeholder="212 555 0100" pattern="[0-9 ().-]{6,16}" required></div></div>' +
        champ("email", "email", "Email (optional)", typ="email", extra=' autocomplete="email"') +
        f'<p class="dm-sous">{E("Language we should answer in")}</p>' + chips("langue", ["English", "Hebrew", "French", "Spanish"], multi=False) +
        f'<p class="dm-sous">{E("How soon?")}</p>' + chips("urgence", ["No rush", "Within a week please", "Urgent, we travel soon"], multi=False))
    recap = (f'<div class="dm-recap"><img class="dm-hassid" src="{IMG}picto-hassid-vert.svg" alt="" width="200" height="200"><div><h3>{E("Your request so far")}</h3><ul id="dm-recap" class="dm-recap-liste"></ul></div></div>')
    S.append(etape("final", "Almost done", "Check your answers, then tell us how to reach you.", recap + contact +
                   f'<p class="dm-erreur" id="dm-erreur" hidden>{esc(JSX[lang]["err"])}</p>', "dm-contact"))

    wa = JSX[lang]["wa"]
    prog = (f'<div class="dm-prog" id="dm-prog" hidden><div class="dm-prog-txt" id="dm-prog-txt" aria-live="polite"></div>'
            f'<div class="dm-barre" id="dm-barre-c" role="progressbar" aria-label="{E("Progress")}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="dm-barre"></i></div></div>')
    nav = (f'<div class="dm-nav"><button type="button" class="dm-retour" id="dm-back" hidden>{E("Back")}</button>'
           f'<button type="button" class="btn-noir" id="dm-next" hidden>{E("Next")}</button>'
           f'<button type="submit" class="btn-noir" id="dm-send">{esc(JSX[lang]["envoyer"])}</button></div>'
           f'<p class="dm-petit" id="dm-petit"><small>{esc(JSX[lang]["petit"])}</small></p>')
    noscript = f'<noscript><p class="dm-noscript">{E("This form needs JavaScript. Write to us on WhatsApp instead.")} <a href="{wa}" rel="noopener">WhatsApp</a></p></noscript>'
    piege = {"en": "Company", "fr": "Société", "es": "Empresa", "he": "חברה"}[lang]
    return ('<section class="ss wrap demande" id="demande">\n<form id="formDemande" novalidate autocomplete="off">\n'
            f'  <div class="piege" aria-hidden="true"><label for="f-societe">{piege}</label><input type="text" id="f-societe" name="societe" tabindex="-1" autocomplete="off"></div>\n'
            f'  {noscript}\n  {prog}\n  ' + "  ".join(S) + f'  {nav}\n</form>\n</section>')

JS_TPL = r'''<script>
(function(){var f=document.getElementById('formDemande');if(!f)return;
var C=__CFG__;
var KEY='mt-demande-'+C.lang;
var ctrls=[].slice.call(f.querySelectorAll('input,select,textarea')).filter(function(e){return e.name!=='societe'});
ctrls.forEach(function(e){e.scr=e.closest('.etape').getAttribute('data-e')});
var etapes=[].slice.call(f.querySelectorAll('.etape'));
var prog=document.getElementById('dm-prog'),barre=document.getElementById('dm-barre'),barreC=document.getElementById('dm-barre-c'),ptxt=document.getElementById('dm-prog-txt');
var bBack=document.getElementById('dm-back'),bNext=document.getElementById('dm-next'),bSend=document.getElementById('dm-send'),petit=document.getElementById('dm-petit');
var cur='intention',ret='';
function branch(){var r=f.querySelector('input[name="intention"]:checked');return r?r.value:''}
function path(){var b=branch();if(!b)return ['intention'];var p=C.paths[b].slice();
 if(b==='a'){var v=ctrls.filter(function(e){return e.scr==='quoi'&&e.name==='voyage'&&e.checked});
  if(v.length&&v.every(function(e){return e.getAttribute('data-k')==='summer'}))p=p.filter(function(x){return x!=='ski'})}
 var r=ctrls.filter(function(e){return e.name==='repas'&&e.checked});
 if(r.length&&r.every(function(e){return e.getAttribute('data-k')==='none'}))p=p.filter(function(x){return x!=='cacherout'});
 return p}
function sync(){var b=branch(),p=path();
 [].forEach.call(f.querySelectorAll('[data-b]'),function(n){n.hidden=n.getAttribute('data-b').indexOf(b)<0});
 ctrls.forEach(function(e){var ok=p.indexOf(e.scr)>=0;
  if(ok){var n=e.parentNode;while(n&&n!==f){if(n.getAttribute&&n.getAttribute('data-b')&&n.getAttribute('data-b').indexOf(b)<0){ok=false;break}n=n.parentNode}}
  e.disabled=e.name==='intention'?false:!ok});
 [].forEach.call(f.querySelectorAll('.dm-ages'),function(w){var i=f.querySelector('input[name="'+w.getAttribute('data-for')+'"]');w.classList.toggle('cache',!(parseInt(i.value,10)>0))});
 return p}
function els(n){return ctrls.filter(function(e){return e.name===n&&!e.disabled})}
function raw(n){var a=els(n);if(!a.length)return '';var t=a[0].type;if(t==='checkbox'||t==='radio'){return a.filter(function(e){return e.checked}).map(function(e){return e.value}).join(', ')}return a[0].value.trim()}
function fdate(v){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(v);if(!m)return v;try{return new Date(+m[1],+m[2]-1,+m[3],12).toLocaleDateString(C.loc,{day:'numeric',month:'long',year:'numeric'})}catch(x){return v}}
function voyage(){var r=f.querySelector('input[name="intention"]:checked');var a=r?[r.getAttribute('data-voyage')]:[];
 els('voyage').forEach(function(e){if(e.checked&&a.indexOf(e.value)<0)a.push(e.value)});return a.join(', ')}
function val(n){
 if(n==='arrivee'||n==='depart'){var d=raw(n);return d?fdate(d):''}
 if(n==='adultes'||n==='hommes'){var x=parseInt(raw(n),10);return x>0?String(x):''}
 if(n==='enfants'||n==='bebes'){var y=parseInt(raw(n),10);if(!(y>0))return '';var g=raw(n+'_ages');return y+(g?' ('+g+')':'')}
 if(n==='voyage')return voyage();
 if(n==='logement'&&branch()==='b')return C.k.logementB;
 return raw(n)}
function screenOf(k){var e=els(k)[0];return e?e.scr:''}
function recap(){var ul=document.getElementById('dm-recap');ul.textContent='';var n=0;
 C.lab.forEach(function(kv){var k=kv[0],v=val(k);if(!v||screenOf(k)==='final')return;n++;
  var li=document.createElement('li'),a=document.createElement('span'),b=document.createElement('span');
  a.className='k';a.textContent=kv[1];b.className='v';b.textContent=v;li.appendChild(a);li.appendChild(b);
  var tg=k==='voyage'?'intention':screenOf(k);
  if(tg){var bt=document.createElement('button');bt.type='button';bt.className='dm-edit';bt.textContent=C.t.edit;bt.setAttribute('data-go',tg);li.appendChild(bt)}
  ul.appendChild(li)});
 if(!n){var li=document.createElement('li');li.className='vide';li.textContent=C.t.vide;ul.appendChild(li)}}
function save(){try{sessionStorage.setItem(KEY,JSON.stringify({c:cur,v:ctrls.map(function(e){return e.type==='checkbox'||e.type==='radio'?(e.checked?1:0):e.value})}))}catch(x){}}
function load(){try{var s=JSON.parse(sessionStorage.getItem(KEY)||'null');if(!s||!s.v||s.v.length!==ctrls.length)return;
 ctrls.forEach(function(e,i){if(e.type==='checkbox'||e.type==='radio')e.checked=!!s.v[i];else e.value=s.v[i]});cur=s.c||'intention'}catch(x){}}
function render(){var p=sync();if(p.indexOf(cur)<0)cur='intention';
 etapes.forEach(function(e){e.hidden=e.getAttribute('data-e')!==cur});
 var i=p.indexOf(cur),last=cur==='final',b=branch();
 bBack.hidden=i<=0;bNext.hidden=last;bSend.hidden=!last;petit.hidden=!last;bNext.disabled=(cur==='intention'&&!b);
 prog.hidden=p.length<2;ptxt.textContent=C.t.step.replace('{n}',i+1).replace('{t}',p.length);
 var pc=Math.round((i+1)/p.length*100);barre.style.width=pc+'%';barreC.setAttribute('aria-valuenow',pc);
 if(last)recap();
 save()}
function show(id,push,focus){var p=sync();if(p.indexOf(id)<0)id='intention';cur=id;if(id==='final')ret='';
 render();
 if(push){try{history.pushState({e:cur},'','#e-'+cur)}catch(x){}}
 if(focus){var h=document.querySelector('.etape[data-e="'+cur+'"] h2:not([hidden])');if(h)h.focus({preventScroll:true});
  var r=f.getBoundingClientRect();if(r.top<0||r.top>200)window.scrollTo({top:window.pageYOffset+r.top-90,behavior:'smooth'})}}
function next(){var p=path(),i=p.indexOf(cur);if(ret){var r=ret;ret='';show(r,true,true);return}if(i>=0&&i<p.length-1)show(p[i+1],true,true)}
function back(){ret='';var p=path(),i=p.indexOf(cur);if(i>0)show(p[i-1],true,true)}
bNext.addEventListener('click',next);bBack.addEventListener('click',back);
f.addEventListener('click',function(ev){
 var go=ev.target.closest&&ev.target.closest('.dm-edit');if(go){ret='final';show(go.getAttribute('data-go'),true,true);return}
 var bt=ev.target.closest&&ev.target.closest('.cpt button');if(!bt)return;
 var inp=bt.parentNode.querySelector('input'),v=parseInt(inp.value,10)||0;v+=bt.className==='plus'?1:-1;inp.value=Math.max(0,Math.min(99,v));
 inp.dispatchEvent(new Event('input',{bubbles:true}))});
function onchg(ev){var t=ev.target;
 if(t.name==='arrivee'&&t.type==='date'){[].forEach.call(f.querySelectorAll('input[name="depart"]'),function(x){x.min=t.value})}
 render();
 if(ev.type==='change'&&t.name==='intention'){setTimeout(next,220)}}
f.addEventListener('change',onchg);f.addEventListener('input',onchg);
window.addEventListener('popstate',function(ev){var id=ev.state&&ev.state.e;show(id||'intention',false,true)});
f.addEventListener('submit',function(ev){ev.preventDefault();
 if(cur!=='final'){next();return}
 if(f.elements.societe&&f.elements.societe.value){location.href=C.merci;return}
 var nom=val('nom'),tel=val('tel'),ind=val('indicatif');var err=document.getElementById('dm-erreur');
 if(!nom||!tel||!ind){err.hidden=false;err.scrollIntoView({behavior:'smooth',block:'center'});return}
 var parts=[];C.lab.forEach(function(kv){var v=val(kv[0]);if(v)parts.push(kv[1]+': '+v)});
 var dates=[val('arrivee'),val('depart')].filter(Boolean).join(C.k.datesj);
 var pers=val('adultes')?val('adultes')+C.k.adultes:'';if(val('enfants'))pers+=(pers?' + ':'')+val('enfants')+C.k.enfants;if(val('bebes'))pers+=(pers?' + ':'')+val('bebes')+C.k.bebes;
 var payload=JSON.stringify({tour:C.k.tour+(val('voyage')||C.k.none),dates:dates,personnes:pers,langue:val('langue'),nom:nom,contact:(ind+' '+tel.replace(/[^0-9]/g,'')).trim()+(val('email')?' / '+val('email'):''),message:parts.join(' | '),page:location.pathname,params:location.search});
 try{var u=window.MISHPACHA_ENDPOINT||'ENDPOINT_APPS_SCRIPT_A_POSER';if(navigator.sendBeacon){navigator.sendBeacon(u,new Blob([payload],{type:'text/plain;charset=UTF-8'}))}else{fetch(u,{method:'POST',mode:'no-cors',keepalive:true,body:payload})}}catch(e){}
 try{sessionStorage.removeItem(KEY)}catch(e){}
 location.href=C.merci});
load();f.classList.add('js');show(cur,false,false);try{history.replaceState({e:cur},'')}catch(x){}
})();
</script>'''

def js(lang):
    T = lambda s: t(s, lang)
    lab = dict(LAB[lang]); i = LANGS.index(lang)
    for k, v in LAB_NEW.items(): lab[k] = v[i]
    cfg = {"lang": lang, "loc": LOCALE[lang], "merci": MERCI[lang], "paths": PATHS,
           "lab": [[k, lab[k]] for k in LAB_ORDER],
           "k": {"tour": JSX[lang]["tour"], "none": JSX[lang]["none"], "datesj": JSX[lang]["datesj"], "adultes": JSX[lang]["adultes"], "enfants": JSX[lang]["enfants"],
                 "bebes": JSX[lang]["bebes"], "logementB": T("Already booked, I need services only")},
           "t": {"step": T("Step {n} of {t}"), "edit": T("Edit"), "vide": T("Nothing filled in yet.")}}
    assert set(LAB_ORDER) >= set(LAB[lang]), set(LAB[lang]) - set(LAB_ORDER)
    return JS_TPL.replace("__CFG__", json.dumps(cfg, ensure_ascii=False))

# ---------------------------------------------------------------- CSS (bloc delimite dans styles.css)
CSS_A, CSS_Z = "/* ===DEMANDE-ETAPES=== */", "/* ===/DEMANDE-ETAPES=== */"
CSS = CSS_A + """
.etape[hidden],[data-b][hidden],.cache{display:none!important}
.demande .piege{position:absolute;left:0;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
.demande form{max-width:760px}
.dm-prog,.dm-nav,.dm-petit{display:none}
.demande form.js .dm-prog{display:grid;gap:8px}
.demande form.js .dm-prog[hidden]{display:none}
.demande form.js .dm-nav{display:flex}
.demande form.js .dm-petit{display:block}
.demande form.js .dm-petit[hidden]{display:none}
.dm-prog-txt{font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.dm-barre{height:8px;border-radius:999px;background:rgba(28,27,31,.12);overflow:hidden}
.dm-barre i{display:block;height:100%;width:0;background:var(--vert);border-radius:999px;transition:width .25s}
.dm-bloc legend h2:focus{outline:none}
.etape{display:block}
.etape > .dm-tete{margin:0 0 20px}
.etape > .dm-tete h2{font-size:26px}
.etape > .dm-tete p{margin-top:4px;font-size:14px;opacity:.7}
.etape > * + *{margin-top:16px}
.dm-noscript{padding:14px 18px;border-radius:15px;background:var(--jaune);font-weight:600}
.dm-sous{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin:6px 0 -6px}
.dm-accueil{display:grid;gap:22px;align-items:center}
.dm-tuiles{display:grid;gap:12px}
.dm-tuile{position:relative;display:grid;grid-template-columns:64px 1fr;gap:2px 16px;align-items:center;min-height:88px;padding:14px 18px;border-radius:15px;border:1px solid rgba(28,27,31,.25);background:var(--creme);cursor:pointer}
.dm-tuile input{position:absolute;opacity:0;width:0;height:0}
.dm-tuile img{grid-row:1 / span 2;width:64px;height:64px;object-fit:contain}
.dm-tuile b{font-family:var(--titre);font-weight:400;font-size:20px;line-height:1.2;align-self:end}
.dm-tuile span{font-size:14px;line-height:1.35;opacity:.75;align-self:start}
.dm-tuile:has(input:checked){background:var(--jaune);border-color:var(--jaune)}
.dm-tuile:has(input:focus-visible){outline:3px solid var(--vert-c);outline-offset:2px}
.dm-hassid{display:block;width:200px;height:auto;margin:0 auto}
.dm-cpt{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:8px 0;border-bottom:1px solid rgba(28,27,31,.1)}
.dm-cpt .lib{font-weight:600;font-size:16px;line-height:1.3}
.cpt{display:flex;align-items:center;gap:6px;direction:ltr;flex:none}
.cpt button{width:48px;height:48px;border-radius:50%;border:1px solid rgba(28,27,31,.25);background:var(--creme);font-size:24px;line-height:1;cursor:pointer;color:var(--encre);padding:0}
.cpt button:hover{background:var(--jaune)}
.cpt input{width:56px;text-align:center;border:0;background:transparent;padding:0;font:inherit;font-size:22px;font-weight:600;color:var(--encre);-moz-appearance:textfield;appearance:textfield}
.cpt input::-webkit-outer-spin-button,.cpt input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.dm-champ input[type=date],.dm-champ input[type=time]{min-height:50px}
.dm-ages{padding-top:4px}
.dm-recap{display:grid;gap:18px;align-items:center}
.dm-recap h3{font-family:var(--titre);font-weight:400;font-size:22px;margin-bottom:8px}
.dm-recap-liste{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.dm-recap-liste li{display:grid;grid-template-columns:1fr auto;gap:0 12px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(28,27,31,.12)}
.dm-recap-liste .k{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;opacity:.7;grid-column:1}
.dm-recap-liste .v{grid-column:1;font-size:16px;line-height:1.35}
.dm-recap-liste .dm-edit{grid-column:2;grid-row:1 / span 2;min-height:44px;min-width:44px;padding:0 14px;border-radius:999px;border:1px solid rgba(28,27,31,.25);background:var(--blanc);font:inherit;font-size:14px;font-weight:600;cursor:pointer;color:var(--encre)}
.dm-recap-liste .dm-edit:hover{background:var(--jaune)}
.dm-recap-liste .vide{display:block;opacity:.7}
.dm-contact .dm-recap{padding-bottom:18px}
.dm-nav{max-width:760px;margin:80px auto 0;justify-content:space-between;align-items:center;gap:14px}
.dm-retour{min-height:54px;padding:0 28px;border-radius:999px;border:1px solid var(--encre);background:transparent;font:inherit;font-size:16px;font-weight:600;color:var(--encre);cursor:pointer}
.dm-retour:hover{background:var(--jaune);border-color:var(--jaune)}
.dm-nav .btn-noir{min-height:54px;padding:0 36px;font-size:16px;margin-inline-start:auto}
.dm-nav .btn-noir:disabled{opacity:.35;cursor:default}
.dm-nav [hidden]{display:none!important}
.dm-petit{max-width:760px;margin:80px auto 0;text-align:center;font-size:13px;opacity:.7}
.demande{padding-bottom:80px}
@media (min-width:700px){
  .dm-accueil{grid-template-columns:1fr 200px;gap:30px}
  .dm-intention .dm-tuiles{grid-column:1}
  .dm-intention .dm-hassid{grid-column:2;grid-row:1;align-self:end}
  .dm-recap{grid-template-columns:200px 1fr;gap:28px}
}
""" + CSS_Z

def update_css():
    c = open("styles.css", encoding="utf-8").read()
    if CSS_A in c:
        a = c.index(CSS_A); z = c.index(CSS_Z) + len(CSS_Z)
        c = c[:a] + CSS + c[z:]
    else:
        c = c.rstrip("\n") + "\n" + CSS + "\n"
    io.open("styles.css", "w", encoding="utf-8", newline="\n").write(c)

# ---------------------------------------------------------------- ecriture
if __name__ == "__main__":
    update_css()
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener", "document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
    f = f.replace('<script src="/config.js"></script>', '<script src="/config.js"></script>\n' + js("en"), 1)
    os.makedirs("plan-your-trip", exist_ok=True)
    io.open("plan-your-trip/index.html", "w", encoding="utf-8", newline="\n").write(h + HERO_EN + formulaire("en") + "\n</main>" + f)
    print("ok plan-your-trip")
    for lang in ("fr", "es", "he"):
        p = f"{lang}/plan-your-trip/index.html"
        s = io.open(p, encoding="utf-8").read()
        a = s.index('<section class="ss wrap demande" id="demande">'); b = s.index("</section>", a) + len("</section>")
        s = s[:a] + formulaire(lang) + s[b:]
        s, n = re.subn(r"<script>\n\(function\(\)\{var f=document.getElementById\('formDemande'\);if\(!f\)return;.*?</script>", lambda m: js(lang), s, count=1, flags=re.S)
        assert n == 1, p
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("ok", p)
