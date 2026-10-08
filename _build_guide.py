# -*- coding: utf-8 -*-
"""Genere les pages du guide (lieux, pratique, Alpes, about, contact, legal) depuis _pages/*.py.
   Chaque module _pages/<slug>.py definit PAGE = dict(...), voir _pages/README.md.
   python _build_guide.py [slug ...]   (depuis site-v5/)"""
import re, os, html, json, glob, importlib.util, urllib.parse, urllib.request, time, sys
from _head import head_page, webpage, itemlist, place, ORG, sans_tel

CHECKED = "7 October 2026"
WA = "https://wa.me/33652092301?text="
def wa(t): return WA + urllib.parse.quote(t)
def gmaps(a): return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(a + ", France")

GEO_PATH = "img/geo.json"
GEO = json.load(open(GEO_PATH, encoding="utf-8"))
def geocode(addr):
    if addr in GEO: return GEO[addr]
    try:
        q = urllib.parse.quote(addr + ", France")
        req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={q}", headers={"User-Agent": "mishpachatours-build/1.0 (contact@mishpachatours.com)"})
        r = json.load(urllib.request.urlopen(req, timeout=20)); time.sleep(1.1)
        if r: GEO[addr] = [float(r[0]["lat"]), float(r[0]["lon"])]; return GEO[addr]
    except Exception as e: print("geocode KO", addr, e, file=sys.stderr)
    return None
def carte(points, h=380):
    pts = [{"n": n, "a": a, "ll": geocode(a)} for n, a in points]; pts = [p for p in pts if p["ll"]]
    if not pts: return ""
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
ticket = rel(home[home.index('<div class="ticket-zone"'):home.index('</main>')])

def lieux(items):
    """items = [(nom, adresse, tel, note)]"""
    out = []
    for n, a, t, x in items:
        tel = f'<a href="tel:{t.replace(" ", "")}">{t}</a>' if t else ""
        note = f" <small>{x}</small>" if x else ""
        out.append(f'<li><b>{n}</b>{note}<span>{a}</span><span class="liens"><a class="go" href="{gmaps(a)}" target="_blank" rel="noopener">Map</a>{tel}</span></li>')
    return '<ul class="liste-lieux">' + "".join(out) + "</ul>"
def photos(lst):
    figs = "".join(f'<figure{" class=\"large\"" if i == 0 else ""}><img src="../img/{p}" alt="{html.escape(c)}" loading="lazy"><figcaption>{c}</figcaption></figure>' for i, (p, c) in enumerate(lst))
    return '<div class="ss wrap"><div class="mosaique" style="margin-top:0">' + figs + "</div></div>"
def cta(txt, msg):
    return f'<section class="ss wrap cta-pratique"><div><h2>{txt}</h2><a class="btn-noir large" href="{wa(msg)}" rel="noopener"><svg><use href="#wa"/></svg>Ask on WhatsApp</a><p class="fiche-note">Same-day reply, never on Shabbat.</p></div></section>'
def strip(s): return re.sub("<[^>]+>", "", s)

def build(P):
    slug = P["slug"]; h1 = P["h1"]; crumb = P.get("crumb", ("../jewish-lyon-guide/", "Jewish Lyon guide"))
    chips = "".join(f"<li>{x}</li>" for x in P.get("chips", []))
    fil = '<p class="fil"><a href="../">Home</a> / ' + (f'<a href="{crumb[0]}">{crumb[1]}</a> / ' if crumb else "") + f'{h1}</p>'
    hero = (f'<section class="pratique-hero"><div class="wrap">{fil}\n'
            f'  <div class="pratique-tete"><div><h1>{h1}<br><i>{P["ital"]}</i></h1><p class="intro-fiche">{P["intro"]}</p><ul class="chips">{chips}</ul></div>\n'
            f'  <img src="../img/illus/{P.get("illus", "flat-jewish-lyon.png")}" alt="" width="700" height="700"></div>\n</div></section>')
    secs = ""
    for s in P.get("sections", []):
        if isinstance(s, str): secs += s; continue
        typ = s.get("type", "text")
        if typ == "text":
            secs += f'<section class="ss wrap conseils"><h2>{s["h2"]}</h2>{s["html"]}</section>'
        elif typ == "beige":
            secs += f'<div class="ss beige"><div class="wrap"><h2>{s["h2"]}</h2>{s["html"]}</div></div>'
        elif typ == "lieux":
            src = f'<p class="source">{s["source"]}</p>' if s.get("source") else ""
            secs += f'<div class="ss beige"><div class="wrap"><section class="groupe"><h2>{s["h2"]} <small>{len(s["items"])}</small></h2>{lieux(s["items"])}</section>{src}</div></div>'
        elif typ == "map":
            note = f'<p class="carte-note">{s["note"]}</p>' if s.get("note") else ""
            secs += f'<section class="ss wrap"><h2 class="centre">{s["h2"]}</h2>{carte(s["points"], s.get("h", 380))}{note}</section>'
        elif typ == "photos":
            secs += photos(s["items"])
        elif typ == "shabbat":
            secs += f'<section class="ss wrap">{SHABBAT}</section>'
        elif typ == "faq":
            d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in s["items"])
            secs += f'<section class="ss wrap faq"><h2>{s.get("h2", "Questions we get")}</h2>{d}</section>'
        elif typ == "steps":
            lis = "".join(f'<li><b>{i+1}</b><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(s["items"]))
            secs += f'<section class="ss wrap etapes"><h2>{s["h2"]}</h2><ol>{lis}</ol></section>'
        elif typ == "cta":
            secs += cta(s["txt"], s["msg"])
    if P.get("related"):
        secs += '<section class="ss wrap conseils"><h2>Keep <i>reading</i></h2><ul>' + "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in P["related"]) + "</ul></section>"
    if P.get("source"): secs += f'<section class="wrap"><p class="source">{P["source"]} Compiled by Mishpacha Tours from these sources. Checked {CHECKED}.</p></section>'
    body = f"<main>\n{hero}\n{secs}\n{ticket if P.get('ticket', True) else ''}\n</main>"
    h = rel(head)
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(P['title'])} | Mishpacha Tours</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(P["desc"])}">', h)
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://mishpachatours.com/"}]
    if crumb: crumbs.append({"@type": "ListItem", "position": 2, "name": crumb[1], "item": "https://mishpachatours.com/" + crumb[0].replace("../", "")})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": h1, "item": f"https://mishpachatours.com/{slug}/"})
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}]
    faqs = [s for s in P.get("sections", []) if isinstance(s, dict) and s.get("type") == "faq"]
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for f in faqs for q, a in f["items"]]})
    ld.append(webpage(f"/{slug}/", P["title"], P["desc"]))
    for s in P.get("sections", []):
        if isinstance(s, dict) and s.get("type") == "lieux" and any(re.search(r"\d{5}", a) for _, a, _, _ in s["items"]):
            ld.append(itemlist(s["h2"], [place(n, a, t, "Place", GEO.get(a)) for n, a, t, x in s["items"] if re.search(r"\d{5}", a)]))
    if P.get("jsonld"): ld.append(P["jsonld"])
    h = head_page(h, f"/{slug}/", f"{P['title']} | Mishpacha Tours", P["desc"], ld)
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener", "document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
    if "carte-osm" in secs: f = f.replace("</body>", LEAFLET + "\n</body>")
    page = sans_tel(h + body + f)
    if P.get("wa"):  # pages Alpes : WhatsApp de l'operateur + option Alpes dans le formulaire (decision 08/10)
        page = page.replace("wa.me/33652092301", "wa.me/" + P["wa"]).replace('<option value="Izieu">Izieu</option>', '<option value="Izieu">Izieu</option><option value="Alps - kosher services">Kosher services in the Alps</option>')
    os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html", "w", encoding="utf-8").write(page); print("ok", slug)

if __name__ == "__main__":
    only = sys.argv[1:]
    for path in sorted(glob.glob("_pages/*.py")):
        name = os.path.basename(path)[:-3]
        if only and name not in only: continue
        spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        build(mod.PAGE)
    json.dump(GEO, open(GEO_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
