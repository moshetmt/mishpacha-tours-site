# -*- coding: utf-8 -*-
"""Genere les 4 pages pratiques (casher, synagogues, Chabad, cimetiere) de la v5.
   Source des faits : 06-reports/2026-09-08-base-factuelle-pages-plateforme.md (liste officielle Beth Din,
   sites officiels). Rien d'invente : une donnee absente ne s'ecrit pas.
   python _build_pratique.py   (depuis site-v5/)"""
from _head import head_page, crumbs, webpage, itemlist, place, sans_tel
import json as _geojson
GEO_CACHE = _geojson.load(open('img/geo.json', encoding='utf-8'))
def _full(a): return a if '69' in a else a + ', 69100 Villeurbanne'
import re, os, html, urllib.parse

WA = "https://wa.me/33767711259?text="
def wa(t): return WA + urllib.parse.quote(t)
CHECKED = "7 October 2026"

# ---------- 1. Casher : liste officielle Beth Din de Lyon uniquement ----------
KOSHER = {
 "Meat restaurants": [
  ("The Fifty and Five","8 rue Professeur-Weill, 69006 Lyon","06 46 40 68 34",""),
  ("Comptoir 43","43 rue Boileau, 69006 Lyon","06 27 12 50 51","grill"),
  ("Chez ViVi","39 avenue Marc-Sangnier, 69100 Villeurbanne","06 20 32 03 06",""),
  ("Jean Bomber","53 rue Pierre-Corneille, 69006 Lyon","",""),
  ("Le Namal","2 rue Baraban, 69006 Lyon","",""),
  ("Aroma","41 rue du 4-Août-1789, 69100 Villeurbanne","",""),
  ("Okami (formerly Bozen)","106 cours Vitton, 69006 Lyon","06 64 16 26 78","Asian"),
  ("Neshama Kitchen","10 rue Mulet, 69001 Lyon","07 68 00 74 31",""),
  ("O'Laffa","18 rue Louis-Goux, 69100 Villeurbanne","04 27 02 53 18","Middle Eastern grill"),
  ("La Casa Del Coco","20 B rue Faillebin, 69100 Villeurbanne","06 50 10 65 75","restaurant and caterer"),
  ("O'Sidney","324 rue Francis-de-Pressensé, 69100 Villeurbanne","04 72 16 08 35","restaurant and caterer"),
  ("La Darka","7 rue des Sports, 69003 Lyon","07 66 05 11 49","take-away and delivery"),
  ("Planet Sandwich","13 rue du Pérou, 69100 Villeurbanne","06 22 87 74 24","take-away and delivery"),
  ("Mika Sushi","49 rue Racine, 69100 Villeurbanne","","delivery only"),
 ],
 "Dairy restaurants and pizza": [
  ("Rose and Roses","21 rue Thomassin, 69002 Lyon","04 78 37 98 01",""),
  ("Le Raphaelo","25 rue Sully, 69006 Lyon","04 78 63 53 07",""),
  ("Pizza Cash","13 rue d'Inkermann, 69100 Villeurbanne","04 72 74 44 98","pizza"),
  ("Presto Pizza","61 rue Greuze, 69100 Villeurbanne","04 78 68 08 41","pizza"),
  ("Lippo","5 rue Malherbe, 69100 Villeurbanne","04 78 85 05 24","pizza"),
  ("Brooklyn","290 rue Francis-de-Pressensé, 69100 Villeurbanne","06 61 22 20 58","pizza"),
 ],
 "Bakeries": [
  ("La Galerie des Pains","30 rue Tronchet, 69006 Lyon","04 26 00 55 25","dairy"),
 ],
 "Butchers": [
  ("Eric Farache","28 rue Villeroy, 69003 Lyon","04 78 60 13 25",""),
  ("Maison William, Boucherie Dahan","50 rue Tête-d'Or, 69006 Lyon","04 78 24 10 10",""),
  ("L'Héritage","122 rue de Sèze, 69006 Lyon","04 78 65 78 20",""),
 ],
 "Groceries": [
  ("Hypercacher","17 rue Claudius-Pionchon, 69003 Lyon","04 78 85 00 80",""),
  ("Hypercacher Garibaldi","46 rue Garibaldi, 69006 Lyon","","opened 2026"),
  ("Lilly Market","140 rue Dedieu, 69100 Villeurbanne","04 78 03 24 79",""),
  ("Lilly Market Écully","6 avenue Raymond-de-Veyssière, 69130 Écully","04 72 48 82 44",""),
 ],
 "Caterers": [
  ("La Cerise sur le Gâteau","41 rue Alexandre-Boutin, 69100 Villeurbanne","04 26 18 33 11","pastry"),
  ("Philibert David","300 rue Francis-de-Pressensé, 69100 Villeurbanne","06 19 13 19 07",""),
  ("Samuel Califa, Le Vôtre","64 rue Docteur-Rollet, 69100 Villeurbanne","04 72 51 31 84",""),
 ],
}

# ---------- 2. Synagogues ----------
SYN_MAIN = [
 dict(nom="Grande Synagogue de Lyon", adresse="13 quai Tilsitt, 69002 Lyon", rite="Consistorial", aff="Consistoire de Lyon (ACIL)",
      horaires="Shacharit Sunday 8:00, weekdays 7:00. Mincha and Arvit 18:30.", tel="04 78 37 13 43",
      note="Closed to visitors outside the Heritage Days. Mishpacha Tours is the only tour that takes you inside, on the Jewish Lyon and Stopover tours.", photo="c-synagogue-7.jpg", lien="../tours/jewish-lyon/"),
 dict(nom="Neveh Chalom", adresse="317 rue Duguesclin, 69007 Lyon", rite="Sephardi", aff="Consistoire Israélite Sépharade de Lyon",
      horaires="Shacharit weekdays 7:00, Shabbat 8:30. Mincha weekdays 19:00, Shabbat 19:20.", tel="04 78 58 18 74",
      note="Beside the Institut culturel du judaïsme. The second synagogue we take you inside, on the Montluc and Neveh Shalom tour.", photo="synagogue-tilsitt-arche.jpg", lien="../tours/memory-montluc-neveh-shalom/"),
]
SYN_AUTRES = [
 ("Lyon",[("Montchat","22 cours du Docteur-Long, 69003","06 09 24 57 78"),("Beth-Habad Lyon 6","60 rue Crillon, 69006","06 25 30 90 38"),("Mizrahi","156 rue Cuvier, 69006","04 78 39 12 00"),("Chaare Tzedek","18 rue Saint-Mathieu, 69008","04 78 00 72 50"),("Patah Eliahou","3 impasse Professeur-Beauvisage, 69008","04 78 76 93 89"),("La Duchère, Rav Hida","501 avenue de la Sauvegarde, 69009","04 78 35 14 44")]),
 ("Villeurbanne",[("Beth-Menahem","293 rue Francis-de-Pressensé","04 78 68 02 03"),("Yeshiva Loubavitch","295 rue Francis-de-Pressensé","04 78 89 08 32"),("Beth Hamidrash","89 rue Magenta","04 78 79 92 58"),("Malherbe","4 rue Malherbe","04 78 84 04 32"),("Ysmah Lev","14 rue Pierre-Loti","04 72 80 99 53"),("Birkat Kohanim","19 rue Jean-Bourgey","04 78 68 18 75"),("Tal Orot","44 rue Hippolyte-Kahn","04 78 85 11 58"),("Hevrat Pinto","20 bis rue des Mûriers","04 78 03 89 14"),("Ohel Yaakov","26 rue Chevreul","04 78 84 09 55"),("Sidi Fredj Halimi","7 rue du Docteur-Frappaz","04 78 93 98 87"),("CERJ","80 rue Fontanières","04 78 84 30 14"),("Torat Emet","52 rue Hippolyte-Kahn","04 78 85 16 18"),("Em Habanim","6 rue d'Alsace","06 72 79 51 77"),("Merone","267 rue Francis-de-Pressensé","04 78 00 25 12"),("Malkhout David","13 bis rue Baudelaire","")]),
 ("Around Lyon",[("Caluire-et-Cuire","2 chemin des Bruyères, 69300","04 78 08 58 47"),("Saint-Fons","17 rue Albert-Thomas, 69190","04 78 67 39 78"),("Vénissieux","10 bis avenue de la Division-Leclerc, 69200","04 78 70 69 85"),("Bron","97 rue de la Pagère, 69500","04 78 41 88 33")]),
]

N_MINYANIM = sum(len(items) for v, items in SYN_AUTRES)

# ---------- 3. Chabad ----------
CHABAD = [
 dict(nom="Beth Habad Centre-Ville", adresse="10 rue Mulet, 69001 Lyon", rav="Rabbi Sender Gurewitz", tel="06 21 82 05 56", note="In the Presqu'île, a few minutes from Vieux Lyon and the Grande Synagogue."),
 dict(nom="Chabad Loubavitch Lyon 6", adresse="60 rue Crillon, 69006 Lyon", rav="Rabbi Mendel Nemanow", tel="06 29 89 19 97", note="In the 6th arrondissement, the neighbourhood of most kosher restaurants on the Lyon side."),
 dict(nom="Chabad Loubavitch Villeurbanne", adresse="295 rue Francis-de-Pressensé, 69100 Villeurbanne", rav="Rabbi Schneor Zalmen Gurewitz", tel="04 78 89 08 32", note="The heart of Jewish Villeurbanne: synagogue Beth-Menahem, yeshiva and school on the same street."),
 dict(nom="Chabad on Campus Lyon", adresse="10 promenade Léa-et-Napoléon-Bullukian, 69008 Lyon", rav="Rabbi Eliezer Gurewitz", tel="", note="For students and young travellers."),
 dict(nom="Beth Habad Charpennes", adresse="86 cours Émile-Zola, 69100 Villeurbanne", rav="Rabbi Haim-Hillel Zekri", tel="06 50 82 11 81", note="At the Charpennes end of Villeurbanne, by the metro, between the 6th arrondissement and Gratte-Ciel."),
 dict(nom="Beth Habad Lyon 3", adresse="119 rue Servient, 69003 Lyon", rav="Rabbi Eliezer (Lippe) Gurewitz", tel="06 19 18 02 67", note="In the 3rd arrondissement, between Part-Dieu station and the Hypercacher grocery of rue Claudius-Pionchon."),
 dict(nom="Beth Habad Écully", adresse="67 chemin du Tronchon, 69130 Écully", rav="Rabbi Lévy Gurewitz", tel="06 19 34 04 00", note="West of Lyon, near the Lilly Market grocery of Écully."),
]


import json as _json
GEO = _json.load(open("img/geo.json", encoding="utf-8"))
def gmaps(a): return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(a + ", France")
def carte(points, h=360):
    pts = [{"n": n, "a": a, "ll": GEO.get(a) or GEO.get(a + ", 69100 Villeurbanne")} for n, a in points]
    pts = [p for p in pts if p["ll"]]
    data = html.escape(_json.dumps(pts, ensure_ascii=False), quote=True)
    return f'<div class="carte-osm" data-points="{data}" style="height:{h}px"></div>\n<p class="carte-note">{len(pts)} places on the map. Tap a marker for the address and directions.</p>'
LEAFLET = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
document.querySelectorAll(".carte-osm").forEach(el=>{const pts=JSON.parse(el.dataset.points);const m=L.map(el,{scrollWheelZoom:false});L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap contributors",maxZoom:19}).addTo(m);const g=L.featureGroup();pts.forEach(p=>{L.circleMarker(p.ll,{radius:9,color:"#1C1B1F",weight:2,fillColor:"#FCDE73",fillOpacity:1}).bindPopup("<b>"+p.n+"</b><br>"+p.a+"<br><a href=\\"https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(p.a+", France")+"\\" target=\\"_blank\\" rel=\\"noopener\\">Directions</a>").addTo(g)});g.addTo(m);m.fitBounds(g.getBounds().pad(0.15),{maxZoom:15})});
</script>"""
SHABBAT = """<div class="shabbat" id="shabbat"><p class="shabbat-titre">Shabbat in Lyon this week</p><p class="shabbat-corps">Candle lighting in Lyon falls as early as 16:30 in December and after 21:00 in June. <a href="https://www.hebcal.com/shabbat?geonameid=2996944" rel="noopener">This week's exact times on Hebcal</a>.</p></div>
<script>
fetch("https://www.hebcal.com/shabbat?cfg=json&geonameid=2996944&M=on&lg=en").then(r=>r.json()).then(d=>{const it=d.items;const c=it.find(i=>i.category==="candles"),h=it.find(i=>i.category==="havdalah"),p=it.find(i=>i.category==="parashat");const f=s=>new Date(s).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",timeZone:"Europe/Paris"});const dd=s=>new Date(s).toLocaleDateString("en-GB",{weekday:"long",day:"numeric",month:"long",timeZone:"Europe/Paris"});document.querySelector(".shabbat-corps").innerHTML=(p?"<b>"+p.title+"</b><br>":"")+(c?"Candle lighting: <b>"+f(c.date)+"</b>, "+dd(c.date)+"<br>":"")+(h?"Havdalah: <b>"+f(h.date)+"</b>, "+dd(h.date):"")+"<br><small>Source: Hebcal, Lyon</small>"}).catch(()=>{document.querySelector(".shabbat-corps").textContent="Times unavailable right now."});
</script>"""
def photos(lst):
    figs = "".join(f'<figure{" class=\"large\"" if i == 0 else ""}><img src="../img/{p}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for i, (p, c) in enumerate(lst))
    return '<div class="ss wrap"><div class="mosaique" style="margin-top:0">' + figs + "</div></div>"

home = open("index.html", encoding="utf-8").read()
head = home[:home.index("<main>")]; foot = home[home.index("</main>")+7:]
def rel(s):
    for a,b in [('href="img/','href="../img/'),('src="img/','src="../img/'),('src="fonts/','src="../fonts/'),('href="fonts/','href="../fonts/'),
                ('href="styles.css"','href="../styles.css"'),('href="./"','href="../"'),('href="#tours"','href="../#tours"'),('href="#why"','href="../#why"'),
                ('href="#before"','href="../#before"'),('href="#guide"','href="../#guide"'),('href="fr/"','href="../fr/"'),('href="es/"','href="../es/"'),
                ('href="he/"','href="../he/"'),('href="credits.html"','href="../credits.html"'),('href="#book"','href="../#book"')]:
        s = s.replace(a,b)
    return s
def page(slug, title, desc, body, ld=None):
    h = rel(head)
    h = re.sub(r"<title>.*?</title>", f"<title>{title} | Mishpacha Tours</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', h)
    h = head_page(h, f"/{slug}/", f"{title} | Mishpacha Tours", desc, [crumbs([("Jewish Lyon guide", "/jewish-lyon-guide/"), (title, f"/{slug}/")]), webpage(f"/{slug}/", title, desc)] + (ld or []))
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener","document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
    f = f.replace("</body>", LEAFLET+"\n</body>")
    os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html","w",encoding="utf-8").write(sans_tel(h+body+f)); print("ok",slug)

def hero(illus, h1, ital, intro, chips):
    c = "".join(f"<li>{x}</li>" for x in chips)
    return f'''<section class="pratique-hero">
  <div class="wrap">
    <p class="fil"><a href="../">Home</a> / <a href="../#before">Before you come</a> / {h1}</p>
    <div class="pratique-tete">
      <div><h1>{h1}<br><i>{ital}</i></h1><p class="intro-fiche">{intro}</p><ul class="chips">{c}</ul></div>
      <img src="../img/illus/{illus}" alt="" width="700" height="700">
    </div>
  </div>
</section>'''

def cta(txt, msg):
    return f'''<section class="ss wrap cta-pratique"><div><h2>{txt}</h2><a class="btn-noir large" href="{wa(msg)}" rel="noopener"><svg><use href="#wa"/></svg>Ask on WhatsApp</a><p class="fiche-note">Same-day reply, never on Shabbat.</p></div></section>'''

ticket = home[home.index('<div class="ticket-zone"'):home.index('</main>')]
ticket = rel(ticket)

# ===== 1. Kosher =====
groupes = ""
for cat, items in KOSHER.items():
    lis = "".join(f'<li><b>{n}</b>{(" <small>"+x+"</small>") if x else ""}<span>{a}</span><span class="liens"><a class="go" href="{gmaps(a)}" target="_blank" rel="noopener">Map</a>{("<a href=\"tel:"+t.replace(" ","")+"\">"+t+"</a>") if t else ""}</span></li>' for n,a,t,x in items)
    groupes += f'<section class="groupe"><h2>{cat} <small>{len(items)}</small></h2><ul class="liste-lieux">{lis}</ul></section>'
total = sum(len(v) for v in KOSHER.values())
body = f'''<main>
{hero("flat-kosher.png","Kosher in Lyon",f"{total} certified places to eat and shop",f"The Beth Din de Lyon certifies {total} kosher restaurants, bakeries, butchers, groceries and caterers in Lyon, Villeurbanne and Écully, most of them in Villeurbanne and the 6th arrondissement. Vieux Lyon has none. Every address below is on the official list of the Beth Din de Lyon, the rabbinical court that supervises kashrut in Lyon, Villeurbanne and Écully. We list only what the Beth Din certifies: no self-declared places, no secondary directories. Call before you go: opening hours change, and most close for Shabbat from Friday afternoon.",["Beth Din de Lyon supervision","Lyon · Villeurbanne · Écully",f"List checked {CHECKED}"])}
<section class="ss wrap conseils">
  <h2>Good to <i>know</i></h2>
  <ul>
    <li><b>Where the food is.</b> Most kosher restaurants are in Villeurbanne (Gratte-Ciel, rue Francis-de-Pressensé) and in Lyon's 6th arrondissement. Vieux Lyon, where our tours start, has none: plan a 15-minute metro ride.</li>
    <li><b>Shabbat.</b> Everything closes Friday afternoon. For Shabbat meals, ask us when you book: we tell you which caterers deliver to your hotel and how to order in advance.</li>
    <li><b>Hechsher.</b> The Beth Din de Lyon is the supervising authority. A certificate is displayed inside each place. If you follow a specific standard, call the Beth Din: 04 12 04 05 15.</li>
  </ul>
</section>
<section class="ss wrap"><h2 class="centre">All {total} places on the <i>map</i></h2>{carte([(n,a) for items in KOSHER.values() for n,a,t,x in items])}</section>
{photos([("stock/stjean-5.jpg","Vieux Lyon shopfronts"),("stock/boeuf-2.jpg","A quiet square, rue du Boeuf"),("stock/juiverie-7.jpg","Rue Juiverie"),("stock/rose-3.jpg","A traboule courtyard")])}
<div class="ss beige"><div class="wrap">{groupes}<p class="source">Source: official list of certified establishments, Beth Din de Lyon, checked {CHECKED}. Places outside Lyon, Villeurbanne and Écully, and institutions that are not shops, are not listed. Tell us if something has changed.</p></div></div>
{cta("Planning your kosher days in Lyon?","Hello, I am planning a trip to Lyon and I would like a private tour with you. Dates: / Number of people:")}
{ticket}
</main>'''
page("kosher-restaurants-lyon","Kosher restaurants in Lyon and Villeurbanne",f"{total} kosher restaurants, bakeries, butchers, groceries and caterers in Lyon, Villeurbanne and Écully, all on the official Beth Din de Lyon list. Checked {CHECKED}.",body, [itemlist("Kosher places certified by the Beth Din de Lyon", [place(n, _full(a), t, "FoodEstablishment", GEO_CACHE.get(_full(a))) for items in KOSHER.values() for n, a, t, x in items])])

# ===== 2. Synagogues =====
cartes = "".join(f'''<article class="syn"><div class="photo"><img src="../img/{s['photo']}" alt="" loading="lazy"></div><div class="corps"><h2>{s['nom']}</h2><p class="adr">{s['adresse']}</p><dl><div><dt>Rite</dt><dd>{s['rite']}</dd></div><div><dt>Community</dt><dd>{s['aff']}</dd></div><div><dt>Prayer times</dt><dd>{s['horaires']}<br><small>Times change with the season. Check before you come.</small></dd></div><div><dt>Phone</dt><dd><a href="tel:{s['tel'].replace(' ','')}">{s['tel']}</a></dd></div></dl><p class="note-syn">{s['note']}</p><a class="btn-noir" href="{s['lien']}">See the tour</a></div></article>''' for s in SYN_MAIN)
habad_lis = "".join(f'<li><b>{c["nom"]}</b><span>{c["adresse"]}</span><span class="liens"><a class="go" href="{gmaps(c["adresse"])}" target="_blank" rel="noopener">Map</a>{("<a href=\"tel:"+c["tel"].replace(" ","")+"\">"+c["tel"]+"</a>") if c["tel"] else ""}</span></li>' for c in CHABAD)
autres = ""
for ville, items in SYN_AUTRES:
    lis = "".join(f'<li><b>{n}</b><span>{a}</span><span class="liens"><a class="go" href="{gmaps(a if "69" in a else a+", 69100 Villeurbanne")}" target="_blank" rel="noopener">Map</a>{("<a href=\"tel:"+t.replace(" ","")+"\">"+t+"</a>") if t else ""}</span></li>' for n,a,t in items)
    autres += f'<section class="groupe"><h2>{ville} <small>{len(items)}</small></h2><ul class="liste-lieux">{lis}</ul></section>'
body = f'''<main>
{hero("flat-jewish-lyon.png","Synagogues in Lyon","Where the community prays, and when Shabbat comes in",f"Lyon has seven Chabad houses, two large historic synagogues and {N_MINYANIM} neighbourhood minyanim, most of them in Villeurbanne. For prayer, a Shabbat meal or any question on the ground, start with a Chabad house: they welcome travellers every day. Visitors are welcome at prayer everywhere: arrive a few minutes early, have your ID with you, and expect a security check at the door, as in every synagogue in France today. For a minyan near your hotel, message us.",["7 Chabad houses first","2 historic synagogues",f"{N_MINYANIM} neighbourhood minyanim"])}
<section class="ss wrap"><h2 class="centre">Start with <i>Chabad</i></h2><p class="sous centre">Seven Chabad houses in Lyon, Villeurbanne and Écully welcome travellers every day: prayer, a Shabbat meal, kosher advice. Our first recommendation, before any other address.</p><ul class="liste-lieux">{habad_lis}</ul><p class="centre"><a href="../chabad-lyon/">Everything about Chabad in Lyon</a></p></section>
<section class="ss wrap"><h2 class="centre">The two <i>historic</i> synagogues</h2><div class="syns">{cartes}</div></section>
<section class="ss wrap">{SHABBAT}</section>
<section class="ss wrap conseils">
  <h2>Shabbat in <i>Lyon</i></h2>
  <ul>
    <li><b>Candle lighting.</b> Lyon's Shabbat times follow the sun: as early as 16:30 in December, after 21:00 in June. We send you the exact times for your dates when you book.</li>
    <li><b>Our tours and Shabbat.</b> We run Sunday to Friday morning, never on Shabbat or Jewish holidays. Friday tours end early enough to be home well before candle lighting.</li>
    <li><b>Hospitality.</b> For a Shabbat meal with the community, contact a Chabad house: see our <a href="../chabad-lyon/">Chabad in Lyon</a> page.</li>
  </ul>
</section>
<section class="ss wrap"><h2 class="centre">Every synagogue on the <i>map</i></h2>{carte([(s2['nom'],s2['adresse']) for s2 in SYN_MAIN]+[(n,(a if "69" in a else a+", 69100 Villeurbanne")) for v,items in SYN_AUTRES for n,a,t in items],420)}</section>
{photos([("c-synagogue-7.jpg","Grande Synagogue, quai Tilsitt"),("synagogue-tilsitt-arche.jpg","The holy ark"),("synagogue-tilsitt-galerie.jpg","The women's gallery"),("c-synagogue-4.jpg","The carved door")])}
<div class="ss beige"><div class="wrap"><h2 class="centre">Neighbourhood <i>minyanim</i></h2><p class="sous centre">Address and phone only. Rite and prayer times are not published online: call ahead.</p>{autres}<p class="source">Sources: official sites of the Grande Synagogue (consistoiredelyon.fr) and Neveh Chalom (nevehchalom.fr), City of Lyon, and the community directory of Habad Lyon, checked {CHECKED}.</p></div></div>
{cta("Want to see the Grande Synagogue from the inside?","Hello, I would like to book the Jewish Lyon tour, the one that goes inside the Grande Synagogue. Dates: / Number of people:")}
{ticket}
</main>'''
page("synagogues-lyon","Synagogues in Lyon, prayer times and Shabbat",f"Seven Chabad houses, the Grande Synagogue de Lyon, Neveh Chalom and {N_MINYANIM} minyanim in Lyon and Villeurbanne: addresses, prayer times. Checked {CHECKED}.",body, [itemlist("Synagogues and minyanim in Lyon and Villeurbanne", [place(s2["nom"], s2["adresse"], s2.get("tel", ""), ["Synagogue", "TouristAttraction"], GEO_CACHE.get(s2["adresse"])) for s2 in SYN_MAIN] + [place(n, _full(a), t, "Synagogue", GEO_CACHE.get(_full(a))) for v, items in SYN_AUTRES for n, a, t in items])])

# ===== 3. Chabad =====
cartes = "".join(f'''<article class="chabad"><h2>{c['nom']}</h2><p class="adr">{c['adresse']}</p><p class="rav">{c['rav']}</p>{("<a class=\"tel\" href=\"tel:"+c['tel'].replace(' ','')+"\">"+c['tel']+"</a>") if c['tel'] else ""}<p class="note-syn">{c['note']}</p></article>''' for c in CHABAD)
body = f'''<main>
{hero("flat-chabad.png","Chabad in Lyon","Seven Chabad houses, a Shabbat table always open","Lyon has seven Chabad centres: city centre, 3rd and 6th arrondissements, Villeurbanne, Charpennes, Écully and the university campus. Wherever you come from, you can call before Shabbat and ask for a meal or a minyan. Our guide is part of this community.",["7 Chabad houses","Shabbat meals on request","Lyon · Villeurbanne · Écully · Campus"])}
<section class="ss wrap"><div class="chabads">{cartes}</div>{carte([(c['nom'],c['adresse']) for c in CHABAD],320)}<p class="source">Source: chabad.org directory, checked {CHECKED}. Meal and class times are not published online: call each centre directly.</p></section>
<section class="ss wrap conseils">
  <h2>How it <i>works</i></h2>
  <ul>
    <li><b>Shabbat meals.</b> Tell us your dates and how many you are before Thursday: we put you in touch with the house nearest your hotel. There is no fixed price; a donation is customary.</li>
    <li><b>Mikveh.</b> Lyon and Villeurbanne have several mikvaot; addresses, phones and how to book are on our <a href="../mikveh-lyon/">mikveh page</a>.</li>
    <li><b>With Mishpacha.</b> Tell us when you book and we point you to the right centre for your dates and your neighbourhood.</li>
  </ul>
</section>
{cta("Need a Shabbat table in Lyon?","Hello, I would like to be put in touch with a Chabad house in Lyon for Shabbat. Dates: / Number of people:")}
{ticket}
</main>'''
page("chabad-lyon","Chabad houses in Lyon, Villeurbanne and Écully",f"The seven Chabad centres of Lyon and Villeurbanne, with addresses. Shabbat meals and minyan on request. Checked {CHECKED}.",body, [itemlist("Chabad houses in Lyon, Villeurbanne and Écully", [place(c["nom"], c["adresse"], c["tel"], "Place", GEO_CACHE.get(c["adresse"])) for c in CHABAD])])

# ===== 4. Cimetiere =====
body = f'''<main>
{hero("flat-cemetery.png","The Jewish cemetery of Lyon","La Mouche, in Gerland, since 1795","Lyon's Jewish cemetery is the cimetière israélite de la Mouche, in the Gerland district of the 7th arrondissement. It was founded in 1795 and holds more than 4,900 graves, a monument to the Jewish soldiers of France and a memorial to the deportation. It is managed by the Consistoire, not by the city.",["11 rue Abraham-Bloch, 69007 Lyon","Founded 1795","Managed by the Consistoire"])}
<section class="ss wrap"><div class="fiche-carte cim"><dl>
  <div><dt>Address</dt><dd>11 rue Abraham-Bloch, 69007 Lyon (Gerland)</dd></div>
  <div><dt>Opening hours</dt><dd>Sunday to Thursday 8:00 to 18:00<br>Friday 8:00 to 16:00<br>Closed on Shabbat and Jewish holidays</dd></div>
  <div><dt>Managed by</dt><dd>Consistoire de Lyon, 13 quai Tilsitt</dd></div>
  <div><dt>Phone</dt><dd><a href="tel:0478723134">04 78 72 31 34</a><br><a href="tel:0478371343">04 78 37 13 43</a></dd></div>
</dl></div></section>
<section class="ss wrap">{carte([("Cimetière israélite de la Mouche","11 rue Abraham-Bloch, 69007 Lyon")],300)}</section>
<section class="ss wrap conseils">
  <h2>Finding a <i>grave</i></h2>
  <ul>
    <li><b>Before you travel.</b> Call the Consistoire with the full name and, if you have it, the year of death. A catalogue of the graves was compiled in 2003.</li>
    <li><b>On the day.</b> Men cover their head. Bring a small stone to place on the grave. The cemetery is a 10-minute walk from the Debourg metro station (line B).</li>
    <li><b>With Mishpacha.</b> If a family grave is part of your trip, tell us: we add the visit to your Memory tour and help you prepare the search.</li>
  </ul>
</section>
<p class="wrap source">Sources: City of Lyon and Consistoire pages, checked {CHECKED}. There is no Jewish section in the Guillotière cemetery: La Mouche is the Jewish cemetery of Lyon.</p>
{cta("Looking for a family grave in Lyon?","Hello, I am looking for a family grave in the Jewish cemetery of Lyon. Name: / Year:")}
{ticket}
</main>'''
page("jewish-cemetery-lyon","The Jewish cemetery of Lyon (La Mouche)",f"Address, hours and contact of the cimetière israélite de la Mouche in Lyon, founded 1795, run by the Consistoire. How to find a family grave. Checked {CHECKED}.",body, [place("Cimetière israélite de la Mouche", "11 rue Abraham-Bloch, 69007 Lyon", "", "Cemetery", GEO_CACHE.get("11 rue Abraham-Bloch, 69007 Lyon"), **{"@context": "https://schema.org", "url": "https://mishpachatours.com/jewish-cemetery-lyon/"})])
