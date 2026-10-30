# -*- coding: utf-8 -*-
"""29/10 : branche Verbier (Valais) partout où figure Crans-Montana : générateurs (hub, zones, lead, prefill, décor, cartes,
Hebcal, animations, kit WP, carte, /alps/, compte des stations du menu) puis, dans les pages déjà en ligne, les couches que
seule une édition HTML a posées (Valora : data-video, sans-wp, polices, video-pages.js ; pastilles de /alps/).
Idempotent : chaque patch vérifie sa marque avant d'écrire. Lancer depuis site-v5 avec py -3.14."""
import io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S, EN, FR, ES, HE, GEO = "kosher-verbier", "Verbier", "Verbier", "Verbier", "ורבייה", 2658168   # geonames.org/2658168 (2658123 = Villeneuve)
LAT, LON = 46.1002, 7.22651   # hebcal.com, geonameid 2658168
CARTE = ("Kosher in Verbier", "The 4 Vallées above the Rhône valley, winter and summer: chef, meals, Shabbat, holidays, minyan")

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def patch(path, anchor, add, check, avant=False):
    s = rd(path)
    if check in s.replace("\r\n", "\n"): print("ok   ", path); return
    if anchor not in s and "\r\n" in s:   # fichiers en CRLF
        anchor, add = anchor.replace("\n", "\r\n"), add.replace("\n", "\r\n")
    assert anchor in s, (path, anchor)
    wr(path, s.replace(anchor, (add + anchor) if avant else (anchor + add), 1)); print("patch", path)
def remplace(path, old, new):
    s = rd(path)
    if new in s: print("ok   ", path); return
    assert old in s, (path, old)
    wr(path, s.replace(old, new)); print("patch", path)

# 1. hub /jewish-lyon-guide/ : carte après Crans-Montana
patch("_build_hub.py", '  ("kosher-crans-montana/", "stock/alpes-ski.jpg", "Kosher in Crans-Montana", "The sunny plateau of the Valais, two hours from Geneva: chef, meals, Shabbat, holidays, minyan"),\n',
      f'  ("{S}/", "stock/alpes-ski.jpg", "{CARTE[0]}", "{CARTE[1]}"),\n', f'"{S}/"')
# 2. zones : ALPES, stations du pied, compte des stations dans le menu plein écran
patch("_zones.py", '"kosher-crans-montana", "kosher-cervinia",', f' "{S}",', f'"{S}",', avant=False)
patch("_zones.py", '("Crans-Montana", "kosher-crans-montana"),', f' ("{EN}", "{S}"),', f'("{EN}", "{S}")')
remplace("_zones.py", "Seventeen resorts in France", "Eighteen resorts in France")
remplace("_zones.py", "Dix-sept stations en France", "Dix-huit stations en France")
remplace("_zones.py", "Diecisiete estaciones en Francia", "Dieciocho estaciones en Francia")
remplace("_zones.py", "שבעה־עשר אתרי סקי", "שמונה־עשר אתרי סקי")
# 3. lead : photo de bannière + nom par langue
patch("_lead.py", " 'kosher-crans-montana': ('stock/st-crans-montana.jpg', dict(en=\"Crans-Montana\", fr=\"Crans-Montana\", es=\"Crans-Montana\", he='קראן מונטנה')),\n",
      f" '{S}': ('stock/st-verbier.jpg', dict(en=\"{EN}\", fr=\"{FR}\", es=\"{ES}\", he='{HE}')),\n", f"'{S}'")
# 4. prefill
patch("_prefill.py", '"kosher-crans-montana": "Crans-Montana",', f' "{S}": "{EN}",', f'"{S}"')
# 5. decor : hassid + icône montagne
patch("_decor.py", '"kosher-crans-montana", "kosher-cervinia",', f' "{S}",', f'"{S}"')
remplace("_decor.py", "|crans|cervinia|", "|crans|verbier|cervinia|")
# 6. photo de la carte de hub
patch("_images_cartes.py", "    'kosher-crans-montana': 'stock/hub-kosher-crans-montana.jpg',\n", f"    '{S}': 'stock/hub-{S}.jpg',\n", f"'{S}'")
# 7. Hebcal (geonameid) et table de Shabbat (coordonnées)
patch("_contacts_bh_hebcal.py", '    "kosher-crans-montana": (6559506, dict(en="Crans-Montana", fr="Crans-Montana", es="Crans-Montana", he="קראן מונטנה")),\n',
      f'    "{S}": ({GEO}, dict(en="{EN}", fr="{FR}", es="{ES}", he="{HE}")),\n', f'"{S}": ({GEO}')
patch("_contacts_bh_hebcal.py", '    "kosher-crans-montana": (46.3132, 7.4791, "Europe/Zurich"),', f' "{S}": ({LAT}, {LON}, "Europe/Zurich"),', f'"{S}": ({LAT}')
# 8. flocons (générateur et js)
for f in ("_animations.py", "js/anim.js"):
    remplace(f, "|crans-montana|cervinia|", "|crans-montana|verbier|cervinia|")
# 9. kit WP : liste HIVER (via STATIONS_SANS_CHALET) et pastilles FR/ES/HE
patch("_kit_wp.py", '"kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana",\n', f'                        "{S}",\n', f'"{S}",\n                        "kosher-cervinia"')
for lang, nom in (("fr", FR), ("es", ES), ("he", HE)):
    s = rd("_kit_wp.py")
    m = re.search(r'"' + lang + r'": \[\([^\n]*?\("kosher-crans-montana", "[^"]+"\)', s)
    assert m, lang
    if f'("{S}", "{nom}")' not in s[m.start():s.find("\n", m.start())]:
        s = s[:m.end()] + f', ("{S}", "{nom}")' + s[m.end():]; wr("_kit_wp.py", s); print("patch _kit_wp.py", lang)
# 10. carte Leaflet des stations CH/IT
remplace("_cartes_ch_it.py", '"kosher-crans-montana", "kosher-cervinia"', f'"kosher-crans-montana", "{S}", "kosher-cervinia"')
# 11. module /alps/ (pour un futur build)
patch("_pages/alps.py", '<a href="../kosher-crans-montana/">Crans-Montana</a>', f', <a href="../{S}/">{EN}</a>', f'../{S}/')

# ---------- pages en ligne : couches sans générateur ----------
PRE = {"": "..", "fr/": "/fr", "es/": "/es", "he/": "/he"}
NOMS = {"": EN, "fr/": FR, "es/": ES, "he/": HE}
# 12. pastilles de /alps/ (KIT-WP:stations, posées une seule fois par _kit_wp.py)
for l, pre in PRE.items():
    p = f"{l}alps/index.html"; s = rd(p)
    if f"/{S}/" in s.split("<!--KIT-WP:stations-->")[1].split("<!--/KIT-WP:stations-->")[0]: print("ok   ", p); continue
    m = re.search(r'<li><a href="[^"]*kosher-crans-montana/">[^<]*</a></li>', s[s.find("<!--KIT-WP:stations-->"):])
    assert m, p
    i = s.find("<!--KIT-WP:stations-->") + m.end()
    href = m.group(0).split('"')[1].replace("kosher-crans-montana", S)
    s = s[:i] + f'<li><a href="{href}">{NOMS[l]}</a></li>' + s[i:]; wr(p, s); print("patch", p)
# 13. couches Valora posées à la main le 28/10 sur les pages station (86b635d data-video, 065d101 sans-wp, polices, vidéo, config)
#     recopiées depuis Crans-Montana, même langue, sur la page Verbier seulement
for l in PRE:
    p, ref = f"{l}{S}/index.html", rd(f"{l}kosher-crans-montana/index.html")
    if not os.path.exists(p): print("absent", p); continue
    s = rd(p); o = s
    if 'data-video="stations"' not in s:
        s = s.replace('<section class="hero lead-hero3">', '<section class="hero lead-hero3" data-video="stations">', 1)
    mb = re.search(r'<body class="([^"]*)"', ref).group(1).split()
    b = re.search(r'<body(?: class="([^"]*)")?', s)
    cl = (b.group(1) or "").split()
    for c in mb:
        if c not in cl: cl.append(c)
    s = s[:b.start()] + f'<body class="{" ".join(cl)}"' + s[b.end():]
    for tag in re.findall(r'<link rel="preload" href="/fonts/[^"]+"[^>]*>|<link rel="stylesheet" href="/valora[^"]*\.css">', ref):
        if tag not in s: s = s.replace("</head>", tag + "\n</head>", 1)
    for js in ("/config.js", "/video-pages.js"):
        tag = re.search(r'<script src="' + re.escape(js) + r'"[^>]*></script>', ref)
        if tag and js not in s: s = s.replace("</body>", tag.group(0) + "\n</body>", 1)
    for tag in re.findall(r'<link rel="preload" href="/fonts/[^"]+"[^>]*>\n?', s):   # polices préchargées : mêmes que Crans-Montana
        if tag.strip() not in ref: s = s.replace(tag, "", 1)
    if 'name="lieu"' not in s:   # _prefill pose le lien après _lead_vers_plan : champ caché du formulaire final
        s = s.replace('<input type="hidden" name="i" value="a">', f'<input type="hidden" name="i" value="a"><input type="hidden" name="lieu" value="{EN}">', 1)
    if l:   # libellé du panneau WhatsApp du menu, traduit à la main sur les autres pages : repris de Crans-Montana
        lab = re.search(r'<a class="panneau-wa"[^>]*>(?:<svg>.*?</svg>)?([^<]*)</a>', ref, re.S)
        if lab: s = re.sub(r'(<a class="panneau-wa"[^>]*>(?:<svg>.*?</svg>)?)WhatsApp, same-day reply(</a>)', lambda k: k.group(1) + lab.group(1) + k.group(2), s, count=1, flags=re.S)
    if l == "he/":   # préfixes devant un nom qui commence par ו : la lettre se double (בוורבייה, לוורבייה)
        s = re.sub(r"(?<![א-ת])([בלמ])ורבייה", r"\1וורבייה", s)
    if s != o: wr(p, s); print("valora", p)
    else: print("ok   ", p)
# 14. tables de Shabbat multi-stations (ski, été, ... : _contacts_bh_hebcal.py ne tourne plus en entier depuis Valora)
import glob
ROW = re.compile(r'<tr data-q="latitude=46\.3132&amp;longitude=7\.4791&amp;tzid=Europe/Zurich" data-tz="Europe/Zurich"><td><a href="([^"]*)kosher-crans-montana/">[^<]*</a></td><td></td><td></td></tr>')
for p in sorted(glob.glob("**/index.html", recursive=True)):
    p = p.replace(os.sep, "/")
    if p.startswith("_"): continue
    s = rd(p); m = ROW.search(s)
    if not m or f"{S}/\">" in s[m.end():m.end() + 400]: continue
    l = p.split("/")[0] + "/" if p.split("/")[0] in ("fr", "es", "he") else ""
    row = (f'<tr data-q="latitude={LAT}&amp;longitude={LON}&amp;tzid=Europe/Zurich" data-tz="Europe/Zurich">'
           f'<td><a href="{m.group(1)}{S}/">{NOMS[l]}</a></td><td></td><td></td></tr>')
    wr(p, s[:m.end()] + row + s[m.end():]); print("shabbat", p)
# 15. carte du hub /jewish-lyon-guide/ (EN seulement, comme Crans-Montana ; régénérer le hub ferait perdre les CTA)
p = "jewish-lyon-guide/index.html"; s = rd(p)
if f'href="../{S}/"' not in s:
    m = re.search(r'<a class="hub-carte" href="\.\./kosher-crans-montana/">.*?</a>', s, re.S); assert m
    carte = (f'<a class="hub-carte" href="../{S}/"><div class="photo"><img src="../img/stock/hub-{S}.jpg" alt="" loading="lazy"></div>'
             f'<div class="corps"><h3>{CARTE[0]}</h3><p>{CARTE[1]}</p><span class="btn-noir">Open</span></div></a>')
    wr(p, s[:m.end()] + carte + s[m.end():]); print("hub", p)
# 16. sitemap (ordre alphabétique, date du jour) et llms.txt, sans relancer _build_sitemap.py (il redate les 270 URL)
s = rd("sitemap.xml"); lignes = s.split("\n")
for l in ("", "fr/", "es/", "he/"):
    loc = f"https://mishpachatours.com/{l}{S}/"
    if f"<loc>{loc}</loc>" in s: continue
    new = f"  <url><loc>{loc}</loc><lastmod>2026-10-29</lastmod><priority>0.7</priority></url>"
    urls = [i for i, x in enumerate(lignes) if "<loc>" in x]
    i = next((i for i in urls if re.search(r"<loc>([^<]*)</loc>", lignes[i]).group(1) > loc), urls[-1] + 1)
    lignes.insert(i, new); s = "\n".join(lignes)
wr("sitemap.xml", s)
patch("llms.txt", "(https://mishpachatours.com/kosher-crans-montana/): Kosher Crans-Montana, Valais, in winter and summer: private chef in your chalet, delivered meals, Shabbat, holidays, minyan and Sefer Torah. One quote.\n",
      f"- [Kosher Verbier: Private Chef, Shabbat and Minyan](https://mishpachatours.com/{S}/): Kosher Verbier, Valais, in winter and summer: private chef in your chalet, delivered meals, Shabbat, holidays, minyan and Sefer Torah. One written quote.\n",
      f"/{S}/)")
print("done")
