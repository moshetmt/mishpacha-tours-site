# -*- coding: utf-8 -*-
"""Patch unique du 07/10 : cartes OSM, liens itineraire, Shabbat en direct, photos dans _build_pratique.py."""
s = open("_build_pratique.py", encoding="utf-8").read()
if "LEAFLET" in s:
    print("deja patche"); raise SystemExit

helpers = r'''
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
document.querySelectorAll(".carte-osm").forEach(el=>{const pts=JSON.parse(el.dataset.points);const m=L.map(el,{scrollWheelZoom:false});L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",{attribution:"&copy; OpenStreetMap &copy; CARTO",maxZoom:19}).addTo(m);const g=L.featureGroup();pts.forEach(p=>{L.circleMarker(p.ll,{radius:9,color:"#1C1B1F",weight:2,fillColor:"#FCDE73",fillOpacity:1}).bindPopup("<b>"+p.n+"</b><br>"+p.a+"<br><a href=\\"https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(p.a+", France")+"\\" target=\\"_blank\\" rel=\\"noopener\\">Directions</a>").addTo(g)});g.addTo(m);m.fitBounds(g.getBounds().pad(0.15),{maxZoom:15})});
</script>"""
SHABBAT = """<div class="shabbat" id="shabbat"><p class="shabbat-titre">Shabbat in Lyon this week</p><p class="shabbat-corps">Loading times…</p></div>
<script>
fetch("https://www.hebcal.com/shabbat?cfg=json&geonameid=2996944&M=on&lg=en").then(r=>r.json()).then(d=>{const it=d.items;const c=it.find(i=>i.category==="candles"),h=it.find(i=>i.category==="havdalah"),p=it.find(i=>i.category==="parashat");const f=s=>new Date(s).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",timeZone:"Europe/Paris"});const dd=s=>new Date(s).toLocaleDateString("en-GB",{weekday:"long",day:"numeric",month:"long",timeZone:"Europe/Paris"});document.querySelector(".shabbat-corps").innerHTML=(p?"<b>"+p.title+"</b><br>":"")+(c?"Candle lighting: <b>"+f(c.date)+"</b>, "+dd(c.date)+"<br>":"")+(h?"Havdalah: <b>"+f(h.date)+"</b>, "+dd(h.date):"")+"<br><small>Source: Hebcal, Lyon</small>"}).catch(()=>{document.querySelector(".shabbat-corps").textContent="Times unavailable right now."});
</script>"""
def photos(lst):
    figs = "".join(f'<figure{" class=\"large\"" if i == 0 else ""}><img src="../img/{p}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for i, (p, c) in enumerate(lst))
    return '<div class="ss wrap"><div class="mosaique" style="margin-top:0">' + figs + "</div></div>"
'''
s = s.replace('home = open("index.html"', helpers + '\nhome = open("index.html"', 1)

old1 = '''lis = "".join(f'<li><b>{n}</b>{(" <small>"+x+"</small>") if x else ""}<span>{a}</span>{("<a href=\\"tel:"+t.replace(" ","")+"\\">"+t+"</a>") if t else ""}</li>' for n,a,t,x in items)'''
new1 = '''lis = "".join(f'<li><b>{n}</b>{(" <small>"+x+"</small>") if x else ""}<span>{a}</span><span class="liens"><a class="go" href="{gmaps(a)}" target="_blank" rel="noopener">Map</a>{("<a href=\\"tel:"+t.replace(" ","")+"\\">"+t+"</a>") if t else ""}</span></li>' for n,a,t,x in items)'''
old2 = '''lis = "".join(f'<li><b>{n}</b><span>{a}</span>{("<a href=\\"tel:"+t.replace(" ","")+"\\">"+t+"</a>") if t else ""}</li>' for n,a,t in items)'''
new2 = '''lis = "".join(f'<li><b>{n}</b><span>{a}</span><span class="liens"><a class="go" href="{gmaps(a if "69" in a else a+", 69100 Villeurbanne")}" target="_blank" rel="noopener">Map</a>{("<a href=\\"tel:"+t.replace(" ","")+"\\">"+t+"</a>") if t else ""}</span></li>' for n,a,t in items)'''
assert old1 in s and old2 in s
s = s.replace(old1, new1).replace(old2, new2)

old3 = 'os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html","w",encoding="utf-8").write(h+body+f); print("ok",slug)'
assert old3 in s
s = s.replace(old3, 'f = f.replace("</body>", LEAFLET+"\\n</body>")\n    os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html","w",encoding="utf-8").write(h+body+f); print("ok",slug)')

# kosher
old4 = '<div class="ss beige"><div class="wrap">{groupes}<p class="source">Source: official list of certified establishments'
assert old4 in s
s = s.replace(old4, '''<section class="ss wrap"><h2 class="centre">All {total} places on the <i>map</i></h2>{carte([(n,a) for items in KOSHER.values() for n,a,t,x in items])}</section>
{photos([("stock/stjean-5.jpg","Vieux Lyon shopfronts"),("stock/boeuf-2.jpg","A quiet square, rue du Boeuf"),("stock/juiverie-7.jpg","Rue Juiverie"),("stock/rose-3.jpg","A traboule courtyard")])}
''' + old4)
# synagogues
old5 = '''<section class="ss wrap conseils">
  <h2>Shabbat in <i>Lyon</i></h2>'''
assert old5 in s
s = s.replace(old5, '<section class="ss wrap">{SHABBAT}</section>\n' + old5)
old6 = '<div class="ss beige"><div class="wrap"><h2 class="centre">Neighbourhood <i>minyanim</i></h2>'
assert old6 in s
s = s.replace(old6, '''<section class="ss wrap"><h2 class="centre">Every synagogue on the <i>map</i></h2>{carte([(s2['nom'],s2['adresse']) for s2 in SYN_MAIN]+[(n,(a if "69" in a else a+", 69100 Villeurbanne")) for v,items in SYN_AUTRES for n,a,t in items],420)}</section>
{photos([("c-synagogue-7.jpg","Grande Synagogue, quai Tilsitt"),("synagogue-tilsitt-arche.jpg","The holy ark"),("synagogue-tilsitt-galerie.jpg","The women's gallery"),("c-synagogue-4.jpg","The carved door")])}
''' + old6)
# chabad
old7 = '<section class="ss wrap"><div class="chabads">{cartes}</div>'
assert old7 in s
s = s.replace(old7, old7 + "{carte([(c['nom'],c['adresse']) for c in CHABAD],320)}")
# cimetiere
old8 = '''<section class="ss wrap conseils">
  <h2>Finding a <i>grave</i></h2>'''
assert old8 in s
s = s.replace(old8, '<section class="ss wrap">{carte([("Cimetière israélite de la Mouche","11 rue Abraham-Bloch, 69007 Lyon")],300)}</section>\n' + old8)
open("_build_pratique.py", "w", encoding="utf-8").write(s)
print("patche", s.count("carte("))
