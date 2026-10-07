# -*- coding: utf-8 -*-
"""Genere le hub /jewish-lyon-guide/ et la page region /jewish-life-around-lyon/.
   Faits region : 06-reports/2026-10-06-base-factuelle-region.md (lignes O et S signalees).
   python _build_hub.py   (depuis site-v5/)"""
from _head import head_page, crumbs, webpage
import re, os, html, json, urllib.parse

CHECKED = "7 October 2026"
GEO = json.load(open("img/geo.json", encoding="utf-8"))
WA = "https://wa.me/33767711259?text="
def wa(t): return WA + urllib.parse.quote(t)
def gmaps(a): return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(a + ", France")
def carte(points, h=380, zoom=None):
    pts = [{"n": n, "a": a, "ll": GEO.get(a)} for n, a in points]; pts = [p for p in pts if p["ll"]]
    return f'<div class="carte-osm" data-points="{html.escape(json.dumps(pts, ensure_ascii=False), quote=True)}" style="height:{h}px"></div>'
LEAFLET = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
document.querySelectorAll(".carte-osm").forEach(el=>{const pts=JSON.parse(el.dataset.points);const m=L.map(el,{scrollWheelZoom:false});L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap contributors",maxZoom:19}).addTo(m);const g=L.featureGroup();pts.forEach(p=>{L.circleMarker(p.ll,{radius:9,color:"#1C1B1F",weight:2,fillColor:"#FCDE73",fillOpacity:1}).bindPopup("<b>"+p.n+"</b><br>"+p.a+"<br><a href=\\"https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(p.a+", France")+"\\" target=\\"_blank\\" rel=\\"noopener\\">Directions</a>").addTo(g)});g.addTo(m);m.fitBounds(g.getBounds().pad(0.15),{maxZoom:15})});
</script>"""
SHABBAT = """<div class="shabbat" id="shabbat"><p class="shabbat-titre">Shabbat in Lyon this week</p><p class="shabbat-corps">Candle lighting in Lyon falls as early as 16:30 in December and after 21:00 in June. <a href="https://www.hebcal.com/shabbat?geonameid=2996944" rel="noopener">This week's exact times on Hebcal</a>.</p></div>
<script>
fetch("https://www.hebcal.com/shabbat?cfg=json&geonameid=2996944&M=on&lg=en").then(r=>r.json()).then(d=>{const it=d.items;const c=it.find(i=>i.category==="candles"),h=it.find(i=>i.category==="havdalah"),p=it.find(i=>i.category==="parashat");const f=s=>new Date(s).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",timeZone:"Europe/Paris"});const dd=s=>new Date(s).toLocaleDateString("en-GB",{weekday:"long",day:"numeric",month:"long",timeZone:"Europe/Paris"});document.querySelector(".shabbat-corps").innerHTML=(p?"<b>"+p.title+"</b><br>":"")+(c?"Candle lighting: <b>"+f(c.date)+"</b>, "+dd(c.date)+"<br>":"")+(h?"Havdalah: <b>"+f(h.date)+"</b>, "+dd(h.date):"")+"<br><small>Source: Hebcal, Lyon</small>"}).catch(()=>{document.querySelector(".shabbat-corps").textContent="Times unavailable right now."});
</script>"""

home = open("index.html", encoding="utf-8").read()
head = home[:home.index("<main>")]; foot = home[home.index("</main>")+7:]
def rel(s):
    for a, b in [('href="img/','href="../img/'),('src="img/','src="../img/'),('src="fonts/','src="../fonts/'),('href="fonts/','href="../fonts/'),
                 ('href="styles.css"','href="../styles.css"'),('href="./"','href="../"'),('href="#tours"','href="../#tours"'),('href="#why"','href="../#why"'),
                 ('href="#before"','href="../#before"'),('href="#guide"','href="../#guide"'),('href="fr/"','href="../fr/"'),('href="es/"','href="../es/"'),
                 ('href="he/"','href="../he/"'),('href="credits.html"','href="../credits.html"'),('href="#book"','href="../#book"')]:
        s = s.replace(a, b)
    return s
def page(slug, title, desc, body):
    h = rel(head); h = re.sub(r"<title>.*?</title>", f"<title>{title} | Mishpacha Tours</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', h)
    h = head_page(h, f"/{slug}/", f"{title} | Mishpacha Tours", desc, [crumbs([(title, f"/{slug}/")]), webpage(f"/{slug}/", title, desc)])
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener","document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener").replace("</body>", LEAFLET + "\n</body>")
    os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html", "w", encoding="utf-8").write(h + body + f); print("ok", slug)
ticket = rel(home[home.index('<div class="ticket-zone"'):home.index('</main>')])

# ===================== HUB =====================
GROUPS = [
 ("Eat, pray, <i>sleep</i>", [
  ("kosher-restaurants-lyon/", "stock/stjean-5.jpg", "Kosher in Lyon", "36 certified restaurants, bakeries, butchers and caterers, on the map"),
  ("kosher-shabbat-meals-catering-lyon/", "stock/rose-3.jpg", "Shabbat meals and catering", "Seven certified caterers, Chabad tables, groceries for a Shabbat at home"),
  ("synagogues-lyon/", "c-synagogue-7.jpg", "Synagogues and prayer times", "The two main synagogues, 26 minyanim, candle-lighting times this week"),
  ("shabbat-in-lyon/", "synagogue-tilsitt-arche.jpg", "Shabbat in Lyon", "Where to pray, how to eat, what closes on Friday, how to plan it"),
  ("chabad-lyon/", "stock/boeuf-2.jpg", "Chabad houses", "Seven centres, a Shabbat table on request, a minyan near your hotel"),
  ("mikveh-lyon/", "stock/rose-7.jpg", "Mikveh", "Eight mikvaot in Lyon and Villeurbanne, with phones and how to book"),
  ("where-to-stay-lyon-jewish-travellers/", "stock/stjean-4.jpg", "Where to stay", "Three areas on foot from a synagogue, and what to ask a hotel for Shabbat"),
  ("jewish-cemetery-lyon/", "montluc-mur-des-fusilles.jpg", "The Jewish cemetery", "La Mouche, since 1795: hours, contact, finding a family grave"),
 ]),
 ("Places to <i>see</i>", [
  ("grande-synagogue-lyon/", "c-synagogue-4.jpg", "The Grande Synagogue", "Built 1864, closed to visitors outside the Heritage Days. We take you in"),
  ("rue-juiverie-lyon/", "c-juiverie-3.jpg", "Rue Juiverie", "The medieval Jewish quarter of Vieux Lyon, and rue Sainte-Catherine"),
  ("jewish-history-lyon/", "stock/juiverie-6.jpg", "Jewish history of Lyon", "From the Middle Ages to the Barbie trial and the community today"),
  ("chrd-lyon/", "stock/chrd-1.jpg", "The CHRD", "The Resistance and deportation museum, in the former Gestapo headquarters"),
  ("montluc-prison-lyon/", "c-montluc-1.jpg", "Montluc prison", "Where Jean Moulin and the children of Izieu were held. Free entry"),
  ("maison-izieu/", "c-izieu-8.jpg", "Maison d'Izieu", "The memorial to the 44 children, one hour from Lyon: hours, prices, our day"),
 ]),
 ("Plan the <i>trip</i>", [
  ("jewish-lyon-itinerary-2-days/", "stock/rose-6.jpg", "Two days in Jewish Lyon", "An itinerary built around kosher meals and Shabbat"),
  ("jewish-travel-lyon-faq/", "stock/traboule-1.jpg", "The honest FAQ", "Getting there, kosher, Shabbat, security, prayer, our tours: 19 answers"),
  ("is-lyon-safe-for-jewish-visitors/", "stock/stjean-6.jpg", "Is Lyon safe?", "Our security standard on every tour, the sourced facts, the practical steps"),
  ("jewish-life-around-lyon/", "stock/izieu-2.jpg", "Around Lyon and the Alps", "Grenoble, Annecy, Aix-les-Bains, Courchevel, Megève: where to pray and eat"),
  ("lyon-gateway-to-the-alps-kosher/", "stock/stjean-3.jpg", "Lyon, gateway to the Alps", "Drive times to the resorts, kosher shopping before you go up, the Stopover"),
  ("kosher-ski-holidays-french-alps/", "stock/boeuf-4.jpg", "Kosher ski holidays", "Resorts with a minyan or a Chabad house in winter, Shabbat on the slopes"),
  ("summer-in-the-alps-jewish-families/", "stock/izieu-1.jpg", "Summer in the Alps", "Annecy, Aix-les-Bains, Grenoble, Chamonix: a kosher summer in the mountains"),
  ("../tours/jewish-lyon/", "synagogue-tilsitt-galerie.jpg", "Inside the Grande Synagogue", "Closed to visitors outside the Heritage Days. The only tour that takes you in, by special authorisation"),
 ]),
]
def grille(items):
    return '<div class="hub-grille">' + "".join(f'''<a class="hub-carte" href="{u if u.startswith("../") else "../"+u}"><div class="photo"><img src="../img/{p}" alt="" loading="lazy"></div><div class="corps"><h3>{t}</h3><p>{d}</p><span class="btn-noir">Open</span></div></a>''' for u, p, t, d in items if os.path.isdir(u.replace("../","")) or u.startswith("../tours/")) + "</div>"
cards = "".join(f'<section class="ss wrap"><h2 class="centre">{h}</h2>{grille(items)}</section>' for h, items in GROUPS)
hub = f'''<main>
<section class="pratique-hero"><div class="wrap">
  <p class="fil"><a href="../">Home</a> / Jewish Lyon guide</p>
  <div class="pratique-tete"><div><h1>Jewish Lyon, <i>the complete guide</i></h1><p class="intro-fiche">Everything a Jewish traveller needs in Lyon and the Alps, kept by a guide who lives here: where to eat kosher, where to pray, when Shabbat comes in, who to call. Every address comes from the Beth Din, the Consistoire or the community itself, with a map and a phone number.</p>
  <ul class="chips"><li>21 guides, 80+ addresses</li><li>Maps and directions</li><li>Shabbat times, live</li><li>Checked {CHECKED}</li></ul></div>
  <img src="../img/illus/flat-jewish-lyon.png" alt="" width="700" height="700"></div>
</div></section>
<section class="ss wrap">{SHABBAT}</section>
{cards}
<section class="ss wrap"><h2 class="centre">Everything on one <i>map</i></h2>{carte([(n,a) for n,a in json.load(open("img/geo-all.json",encoding="utf-8"))],460)}<p class="carte-note">Kosher places, synagogues, Chabad houses and the cemetery, Lyon and Villeurbanne. Tap a marker for directions.</p></section>
<section class="ss wrap conseils"><h2>Before you <i>land</i></h2><ul>
<li><b>Where to stay.</b> The kosher life of Lyon is in Villeurbanne (Gratte-Ciel, rue Francis-de-Pressensé) and in the 6th arrondissement. A hotel there puts every restaurant and synagogue within walking distance of Shabbat. Our tours start in Vieux Lyon, 15 minutes away by metro.</li>
<li><b>Airports.</b> Lyon-Saint-Exupéry is 35 minutes from the centre by the Rhônexpress tram. Geneva is 2 hours by car and serves the Alps.</li>
<li><b>Security.</b> Every synagogue in France has a security check at the door: arrive early, bring ID. On our tours, routes and meeting points are chosen in advance. A professional escort is available on request.</li>
<li><b>Ask us.</b> Message us on WhatsApp before your trip. We answer the same day, never on Shabbat.</li>
</ul></section>
<section class="ss wrap cta-pratique"><div><h2>Planning a trip to Lyon?</h2><a class="btn-noir large" href="{wa("Hello, I am planning a trip to Lyon and I have a few questions. Dates: / Number of people:")}" rel="noopener"><svg><use href="#wa"/></svg>Ask on WhatsApp</a><p class="fiche-note">Same-day reply, never on Shabbat.</p></div></section>
{ticket}
</main>'''
page("jewish-lyon-guide", "Jewish Lyon, the complete guide", f"Kosher restaurants, synagogues, Chabad houses, the Jewish cemetery and Shabbat times in Lyon, plus the Alps. Maps, phones, directions. Checked {CHECKED}.", hub)

# ===================== REGION =====================
VILLES = [
 ("Grenoble", "1 h 15 from Lyon by train", [
   ("Synagogue Bar Yohaï (CIG)","4 rue des Bains, 38000 Grenoble","04 76 46 15 14","Consistoire regional"),
   ("Grande Synagogue consistoriale (ACJG Rachi)","11 rue André Maginot, 38000 Grenoble","04 76 87 02 80","Office open Monday and Thursday mornings"),
   ("Beth Habad de Grenoble, Rabbi Yhia Lahiany","10 rue Lazare Carnot, 38000 Grenoble","04 76 43 38 58","Also runs the Chabad network of the Alps: habadgrenoblealpes.com")]),
 ("Annecy", "1 h 45 from Lyon by car", [
   ("Centre communautaire israélite d'Annecy","18 rue de Narvik, 74000 Annecy","04 50 67 69 37","Rabbinical delegate Nephtaly Suissa"),
   ("Beth Habad d'Annemasse","17 rue du Clos Fleury, 74100 Annemasse","","The nearest Chabad house, 40 minutes from Annecy, by the Geneva border")]),
 ("Aix-les-Bains", "1 h 15 from Lyon by train", [
   ("Communauté israélite d'Aix-les-Bains","7 rue Paul Bonna, 73100 Aix-les-Bains","04 79 35 28 08","Synagogues, prayer times, a mikveh and kosher shops listed on ci-aixlesbains.fr: the best-equipped town in the Alps for an observant family")]),
 ("Chambéry", "1 h 20 from Lyon by train", [
   ("Synagogue de Chambéry","9 impasse Chardonnet, 73000 Chambéry","04 79 85 53 58","")]),
 ("Saint-Étienne", "50 minutes from Lyon by train", [
   ("Communauté de Saint-Étienne","34 rue d'Arcole, 42000 Saint-Étienne","04 77 33 56 31","Rabbinical delegate Michel Elharrar, 06 07 87 50 74")]),
 ("Valence", "1 h from Lyon by train", [
   ("Synagogue Hana, Chabad Loubavitch Valence","1 place du Colombier, 26000 Valence","04 75 43 34 43","Rabbinical delegate Menahem Mendel Bitton, 06 13 14 83 42")]),
 ("Vichy", "2 h from Lyon by train", [
   ("Association cultuelle israélite de Vichy","2 bis rue du Maréchal Foch, 03200 Vichy","04 70 59 82 33","Rabbinical delegate Daniel El Haddad")]),
 ("Clermont-Ferrand", "2 h 15 from Lyon by train", [
   ("Association cultuelle israélite","6 rue Blatin, 63000 Clermont-Ferrand","04 73 93 36 59","Rabbi Eyman Hagege, juif-clermont.org")]),
 ("Bourg-en-Bresse", "1 h from Lyon by train", [
   ("Communauté de Bourg-en-Bresse","1718 avenue de Lyon, 01960 Péronnas","","")]),
]
STATIONS = [
 ("Courchevel 1850","Synagogue at Hôtel Le Mont Charvin","389 rue des Tovets, 73120 Courchevel","06 20 60 72 58","Winter season only. Rabbi Daniel Belaïch. Help with kosher needs, wine and challot for Shabbat."),
 ("Megève","Chabad of the Alps, winter minyan","136 route Edmond de Rothschild, 74120 Megève","","Winter season. Contact habadalpes@yahoo.fr before you come: the venue has changed over the years."),
 ("Val Thorens, Les Menuires, Les Arcs","No permanent minyan published","","","Private operators organise kosher chalets and a minyan when numbers allow (skikosher.com). Supervision not published: ask them directly, and ask us."),
]
def lis(items, ville=True):
    return "".join(f'<li><b>{n}</b>{(" <small>"+d+"</small>") if d else ""}<span>{a}</span><span class="liens"><a class="go" href="{gmaps(a)}" target="_blank" rel="noopener">Map</a>{("<a href=\"tel:"+t.replace(" ","")+"\">"+t+"</a>") if t else ""}</span></li>' for n,a,t,d in items)
villes = "".join(f'<section class="groupe"><h2>{v} <small>{dist}</small></h2><ul class="liste-lieux">{lis(items)}</ul></section>' for v,dist,items in VILLES)
stations = "".join(f'<li><b>{s}</b> <small>{n}</small>{("<span>"+a+"</span>") if a else ""}<span class="liens">{("<a class=\"go\" href=\""+gmaps(a)+"\" target=\"_blank\" rel=\"noopener\">Map</a>") if a else ""}{("<a href=\"tel:"+t.replace(" ","")+"\">"+t+"</a>") if t else ""}</span><em>{d}</em></li>' for s,n,a,t,d in STATIONS)
allpts = [(n,a) for v,dist,items in VILLES for n,a,t,d in items] + [(n,a) for s,n,a,t,d in STATIONS if a]
region = f'''<main>
<section class="pratique-hero"><div class="wrap">
  <p class="fil"><a href="../">Home</a> / <a href="../jewish-lyon-guide/">Guide</a> / Around Lyon</p>
  <div class="pratique-tete"><div><h1>Jewish life around Lyon<br><i>Grenoble, Annecy, the Alps and the Auvergne</i></h1><p class="intro-fiche">Lyon is the gateway to the Alps. Within two hours you reach nine Jewish communities and, in winter, the minyanim of the ski resorts. Here is where to pray and who to call, town by town. Every address comes from the regional Consistoire or the community itself. Phone before you go: none of these pages shows a date.</p>
  <ul class="chips"><li>9 towns</li><li>3 ski resorts</li><li>Checked {CHECKED}</li></ul></div>
  <img src="../img/illus/flat-stopover.png" alt="" width="700" height="700"></div>
</div></section>
<section class="ss wrap"><h2 class="centre">The region on the <i>map</i></h2>{carte(allpts,460)}<p class="carte-note">Tap a marker for the address and directions.</p></section>
<div class="ss beige"><div class="wrap">{villes}</div></div>
<section class="ss wrap"><h2>Ski resorts in <i>winter</i></h2><p class="sous">Our Stopover tour is built for families on their way to the slopes: three hours in Jewish Lyon between the airport and the resort.</p><ul class="liste-lieux stations">{stations}</ul><p class="source">Sources: Consistoire régional de Lyon, chabad.org, ci-aixlesbains.fr, synalpes.wordpress.com, checked {CHECKED}. Kosher shops outside Lyon are not listed here: ask the local community. Villefranche-sur-Saône has no published address.</p></section>
<section class="ss wrap cta-pratique"><div><h2>Heading to the Alps through Lyon?</h2><a class="btn-noir large" href="{wa("Hello, we are travelling to the Alps through Lyon and would like to ask about the Stopover tour. Arrival time: / Onward departure time: / Number of people:")}" rel="noopener"><svg><use href="#wa"/></svg>Ask about the Stopover</a><p class="fiche-note">Same-day reply, never on Shabbat.</p></div></section>
{ticket}
</main>'''
page("jewish-life-around-lyon", "Jewish life around Lyon and in the Alps", f"Synagogues and Chabad houses in Grenoble, Annecy, Aix-les-Bains, Chambéry, Valence and Clermont-Ferrand, winter minyanim in Courchevel and Megève. Checked {CHECKED}.", region)
