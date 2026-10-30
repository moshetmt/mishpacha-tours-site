# -*- coding: utf-8 -*-
"""30/10 : branche Gstaad (Berne), Davos (Grisons) et la page « Ailleurs sur demande » partout où figure Verbier (même
mécanique que _stations_verbier.py du 29/10) : générateurs (hub, zones, lead, prefill, décor, cartes, Hebcal, animations,
kit WP, carte CH/IT, /alps/, compte des stations du menu, manifeste chef seul, bloc Beth Habad sans repas livrés pour la
Suisse et l'ailleurs), puis, dans les pages déjà en ligne, les couches posées par édition HTML (pastilles de /alps/, tables
de Shabbat multi-stations, carte du hub /jewish-lyon-guide/, sitemap, llms.txt) et la correction Verbier « plus de livraison ».
Idempotent : chaque patch vérifie sa marque avant d'écrire. Lancer depuis site-v5 avec py -3.14, APRÈS _build_guide.py et
les traductions, AVANT _stations_suisse_chaine.py."""
import io, os, re, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# slug, noms EN/FR/ES/HE, geonameid, lat, lon, photo, (titre de carte, texte de carte), slug après lequel on s'insère
ST = [
  dict(s="kosher-gstaad", en="Gstaad", fr="Gstaad", es="Gstaad", he="גשטאד", geo=2660461, lat=46.47215, lon=7.28685,   # hebcal.com 30/10 (2660486 du brief : inconnu)
       carte=("Kosher in Gstaad", "The Saanenland and Glacier 3000, winter and summer: private chef, Shabbat, holidays, minyan"), apres="kosher-verbier",
       llms="- [Kosher Gstaad: Private Chef and Shabbat](https://mishpachatours.com/kosher-gstaad/): Kosher Gstaad, Saanenland, winter and summer: a private chef cooks in your chalet, kosher shopping brought in, Shabbat, holidays, minyan and Sefer Torah. One quote.\n"),
  dict(s="kosher-davos", en="Davos", fr="Davos", es="Davos", he="דאבוס", geo=2661039, lat=46.80429, lon=9.83723,   # hebcal.com 30/10, 1 560 m
       carte=("Kosher in Davos", "The highest town in the Alps, Parsenn and Jakobshorn, winter and summer: private chef, Shabbat, holidays, minyan"), apres="kosher-gstaad",
       llms="- [Kosher Davos: Private Chef and Shabbat](https://mishpachatours.com/kosher-davos/): Kosher Davos, Grisons, at 1,560 m, winter and summer: a private chef cooks in your chalet, kosher shopping brought in, Shabbat, holidays, minyan and Sefer Torah. One quote.\n"),
  dict(s="kosher-ski-anywhere", en="Anywhere on request", fr="Ailleurs, sur demande", es="Otro destino, a petición", he="יעד אחר, לפי בקשה", geo=None,
       carte=("Kosher ski, anywhere", "Austria, North America or any resort not on our list: a private chef who travels with you, Shabbat, minyan, transfers"), apres="kosher-cortina",
       llms="- [Kosher Ski Anywhere: Chef, Shabbat, Minyan](https://mishpachatours.com/kosher-ski-anywhere/): Kitzbühel, St. Anton, Whistler, Aspen or any ski resort not on our list: tell us where, we organise a private kosher chef, Shabbat, holidays, minyan and transfers.\n"),
]
STATIONS = [x for x in ST if x["geo"]]          # Gstaad, Davos : vraies stations (Hebcal, carte, hassid)
SANS_LIVRAISON = ("kosher-verbier", "kosher-gstaad", "kosher-davos", "kosher-ski-anywhere")   # Mendel 30/10 : chef privé seulement
VERBIER_CARTE = ("The 4 Vallées above the Rhône valley, winter and summer: chef, meals, Shabbat, holidays, minyan",
                 "The 4 Vallées above the Rhône valley, winter and summer: private chef, Shabbat, holidays, minyan")

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def patch(path, anchor, add, check, avant=False):
    s = rd(path)
    if check in s.replace("\r\n", "\n"): print("ok   ", path, check[:40]); return
    if anchor not in s and "\r\n" in s:   # fichiers en CRLF
        anchor, add = anchor.replace("\n", "\r\n"), add.replace("\n", "\r\n")
    assert anchor in s, (path, anchor)
    wr(path, s.replace(anchor, (add + anchor) if avant else (anchor + add), 1)); print("patch", path, check[:40])
def remplace(path, old, new):
    s = rd(path)
    if new in s: print("ok   ", path, new[:40]); return
    assert old in s, (path, old)
    wr(path, s.replace(old, new)); print("patch", path, new[:40])

# 1. hub /jewish-lyon-guide/ : cartes (générateur) ; texte Verbier sans « meals »
remplace("_build_hub.py", VERBIER_CARTE[0], VERBIER_CARTE[1])
patch("_build_hub.py", '  ("kosher-verbier/", "stock/alpes-ski.jpg", "Kosher in Verbier", "' + VERBIER_CARTE[1] + '"),\n',
      "".join(f'  ("{x["s"]}/", "stock/alpes-ski.jpg", "{x["carte"][0]}", "{x["carte"][1]}"),\n' for x in STATIONS), '("kosher-gstaad/"')
patch("_build_hub.py", '  ("kosher-cortina/", "stock/alpes-ski.jpg", "Kosher in Cortina d\'Ampezzo", "The Dolomites, winter and summer: chef, meals, Shabbat, holidays, minyan"),\n',
      f'  ("kosher-ski-anywhere/", "stock/alpes-ski.jpg", "{ST[2]["carte"][0]}", "{ST[2]["carte"][1]}"),\n', '("kosher-ski-anywhere/"')
# 2. zones : ALPES, stations du menu et du pied (Gstaad et Davos après Verbier, l'ailleurs en fin de liste), compte des stations
patch("_zones.py", '"kosher-cervinia", "kosher-verbier",', ' "kosher-gstaad", "kosher-davos", "kosher-ski-anywhere",', '"kosher-gstaad", "kosher-davos", "kosher-ski-anywhere",')
# la page Pessah (SEO semaine 1) n'était pas connue de _zones : sans cette ligne, une passe globale lui met la baseline de Lyon
patch("_zones.py", '"kosher-ski-holidays-french-alps", "kosher-vacation-french-alps",', ' "kosher-pesach-french-alps",', '"kosher-pesach-french-alps"')
patch("_zones.py", '("Verbier", "kosher-verbier"),', ' ("Gstaad", "kosher-gstaad"), ("Davos", "kosher-davos"),', '("Gstaad", "kosher-gstaad")')
patch("_zones.py", '("Cortina d\'Ampezzo", "kosher-cortina")', ', ("Anywhere on request", "kosher-ski-anywhere")', '("Anywhere on request", "kosher-ski-anywhere")')
patch("_zones.py", "def pied_stations(lang, pre):\n",
      'AILLEURS = {"en": "Anywhere on request", "fr": "Ailleurs, sur demande", "es": "Otro destino, a petición", "he": "יעד אחר, לפי בקשה"}   # 30/10, libellé par langue\n',
      "AILLEURS = {", avant=True)
remplace("_zones.py", '''"<br>".join(f'<a href="{pre}/{slug}/">{nom}</a>' for nom, slug in STATIONS)''',
         '''"<br>".join(f'<a href="{pre}/{slug}/">{AILLEURS[lang] if slug == "kosher-ski-anywhere" else nom}</a>' for nom, slug in STATIONS)''')
remplace("_zones.py", "Eighteen resorts in France", "Twenty resorts in France")
remplace("_zones.py", "Dix-huit stations en France", "Vingt stations en France")
remplace("_zones.py", "Dieciocho estaciones en Francia", "Veinte estaciones en Francia")
remplace("_zones.py", "שמונה־עשר אתרי סקי", "עשרים אתרי סקי")
# 3. lead : photo de bannière + nom par langue ; l'ailleurs en page de type « alps »
patch("_lead.py", " 'kosher-verbier': ('stock/st-verbier.jpg', dict(en=\"Verbier\", fr=\"Verbier\", es=\"Verbier\", he='ורבייה')),\n",
      "".join(f" '{x['s']}': ('stock/st-{x['en'].lower()}.jpg', dict(en=\"{x['en']}\", fr=\"{x['fr']}\", es=\"{x['es']}\", he='{x['he']}')),\n" for x in STATIONS), "'kosher-gstaad'")
patch("_lead.py", " 'kosher-services-french-alps': ('stock/st-val-thorens.jpg', 'alps', 'Kosher services in the Alps'),\n",
      " 'kosher-ski-anywhere': ('stock/st-anywhere.jpg', 'alps', 'Kosher stay, any resort'),   # 30/10\n", "'kosher-ski-anywhere'")
# 4. prefill
patch("_prefill.py", '"kosher-verbier": "Verbier",', ' "kosher-gstaad": "Gstaad", "kosher-davos": "Davos",', '"kosher-gstaad"')
remplace("_prefill.py", '"kosher-ski-holidays-french-alps": {"i": "a", "voyage": SKI}}', '"kosher-ski-holidays-french-alps": {"i": "a", "voyage": SKI}, "kosher-ski-anywhere": {"i": "a", "voyage": SKI}}')
# 5. decor : hassid + icône montagne
patch("_decor.py", '"kosher-cervinia", "kosher-verbier",', ' "kosher-gstaad", "kosher-davos", "kosher-ski-anywhere",', '"kosher-gstaad"')
remplace("_decor.py", "|crans|verbier|cervinia|", "|crans|verbier|gstaad|davos|anywhere|cervinia|")
# 6. photo de la carte de hub
patch("_images_cartes.py", "    'kosher-verbier': 'stock/hub-kosher-verbier.jpg',\n", "".join(f"    '{x['s']}': 'stock/hub-{x['s']}.jpg',\n" for x in ST), "'kosher-gstaad'")
# 7. Hebcal (geonameid), table de Shabbat (coordonnées), bloc Beth Habad sans repas livrés
patch("_contacts_bh_hebcal.py", '    "kosher-verbier": (2658168, dict(en="Verbier", fr="Verbier", es="Verbier", he="ורבייה")),\n',
      "".join(f'    "{x["s"]}": ({x["geo"]}, dict(en="{x["en"]}", fr="{x["fr"]}", es="{x["es"]}", he="{x["he"]}")),\n' for x in STATIONS), '"kosher-gstaad": (2660461')
patch("_contacts_bh_hebcal.py", '"kosher-verbier": (46.1002, 7.22651, "Europe/Zurich"),', "".join(f' "{x["s"]}": ({x["lat"]}, {x["lon"]}, "Europe/Zurich"),' for x in STATIONS), '"kosher-gstaad": (46.47215')
remplace("_contacts_bh_hebcal.py", '    meals = slug != "kosher-services-french-alps"  # la page services a deja son bouton repas vers le Beth Habad',
         '    meals = slug not in SANS_LIVRAISON  # la page services a deja son bouton repas ; Suisse et ailleurs : chef privé seulement (Mendel 30/10)')
patch("_contacts_bh_hebcal.py", "def bloc_minyan(h, lang, slug):\n",
      'SANS_LIVRAISON = {"kosher-services-french-alps", ' + ", ".join(f'"{s}"' for s in SANS_LIVRAISON) + "}   # 30/10 : plus de livraison au-delà de 3 h de Grenoble\n", "SANS_LIVRAISON = {", avant=True)
# 8. flocons (générateur et js)
for f in ("_animations.py", "js/anim.js"):
    remplace(f, "|crans-montana|verbier|cervinia|", "|crans-montana|verbier|gstaad|davos|ski-anywhere|cervinia|")
# 9. kit WP : liste HIVER (via STATIONS_SANS_CHALET) et pastilles FR/ES/HE (Suisse, puis un groupe « ailleurs »)
patch("_kit_wp.py", '                        "kosher-verbier",\n', "".join(f'                        "{x["s"]}",\n' for x in ST), '"kosher-gstaad",\n')
for lang, aill, sur in (("fr", "Ailleurs", "Sur demande"), ("es", "Otro destino", "A petición"), ("he", "יעד אחר", "לפי בקשה")):
    s = rd("_kit_wp.py")
    m = re.search(r'"' + lang + r'": \[\([^\n]*?\("kosher-verbier", "[^"]+"\)', s); assert m, lang
    if '("kosher-gstaad"' not in s[m.start():s.find("\n", m.start())]:
        s = s[:m.end()] + f', ("kosher-gstaad", "Gstaad"), ("kosher-davos", "Davos")' + s[m.end():]; wr("_kit_wp.py", s); print("patch _kit_wp.py", lang, "Gstaad Davos")
    s = rd("_kit_wp.py")
    i = s.find(f'"{lang}": [("'); j = s.find("\n", s.find('("kosher-cortina", ', i))
    ligne = s[i:j]
    if "kosher-ski-anywhere" not in ligne:
        assert ligne.endswith(")])],"), ligne[-30:]
        s = s[:i] + ligne[:-2] + f', ("{aill}", [("kosher-ski-anywhere", "{sur}")])],' + s[j:]; wr("_kit_wp.py", s); print("patch _kit_wp.py", lang, "ailleurs")
# 10. carte Leaflet des stations CH/IT
remplace("_cartes_ch_it.py", '"kosher-verbier", "kosher-cervinia"', '"kosher-verbier", "kosher-gstaad", "kosher-davos", "kosher-cervinia"')
# 11. module /alps/ (pour un futur build)
patch("_pages/alps.py", '<a href="../kosher-verbier/">Verbier</a>', ', <a href="../kosher-gstaad/">Gstaad</a>, <a href="../kosher-davos/">Davos</a>', '../kosher-gstaad/')
patch("_pages/alps.py", '<a href="../kosher-cortina/">Cortina d\'Ampezzo</a>', '. Elsewhere on request: <a href="../kosher-ski-anywhere/">Austria, North America, any resort</a>', '../kosher-ski-anywhere/')
# 11 bis. manifeste : première ligne « chef privé » sans repas livrés sur les pages sans livraison
patch("_manifeste.py", "def textes(lang, slug):\n",
      'CHEF_SEUL = {' + ", ".join(f'"{s}"' for s in SANS_LIVRAISON if s != "kosher-services-french-alps") + '}   # 30/10 : plus de livraison au-delà de 3 h de Grenoble\n'
      'LIGNES_CHEF = {"en": ("A private chef in your chalet", "The kitchen is kashered, the chef cooks every meal of the week on site."),\n'
      '               "fr": ("Un chef privé dans votre chalet", "La cuisine est cachérisée, le chef cuisine sur place tous les repas de la semaine."),\n'
      '               "es": ("Un chef privado en su chalé", "La cocina se kosheriza y el chef cocina allí mismo todas las comidas de la semana."),\n'
      '               "he": ("שף פרטי בצ\'אלה שלכם", "המטבח מוכשר, והשף מבשל במקום כל ארוחה בשבוע.")}\n', "CHEF_SEUL = {", avant=True)
remplace("_manifeste.py", '    return phrase, t["lignes"]', '    lignes = [LIGNES_CHEF[lang]] + list(t["lignes"][1:]) if slug in CHEF_SEUL else t["lignes"]\n    return phrase, lignes')

# ---------- pages en ligne : couches sans générateur ----------
PRE = {"": "..", "fr/": "/fr", "es/": "/es", "he/": "/he"}
def nom(x, l): return x[l.rstrip("/") or "en"]
# 12. pastilles de /alps/ (KIT-WP:stations, posées une seule fois par _kit_wp.py)
for l, pre in PRE.items():
    p = f"{l}alps/index.html"; s = rd(p)
    for x in ST:
        bloc = s.split("<!--KIT-WP:stations-->")[1].split("<!--/KIT-WP:stations-->")[0]
        if f"/{x['s']}/" in bloc: print("ok   ", p, x["s"]); continue
        m = re.search(r'<li><a href="[^"]*' + x["apres"] + r'/">[^<]*</a></li>', s[s.find("<!--KIT-WP:stations-->"):]); assert m, (p, x["s"])
        i = s.find("<!--KIT-WP:stations-->") + m.end()
        href = m.group(0).split('"')[1].replace(x["apres"], x["s"])
        s = s[:i] + f'<li><a href="{href}">{nom(x, l)}</a></li>' + s[i:]; wr(p, s); print("patch", p, x["s"])
# 13. tables de Shabbat multi-stations : Gstaad et Davos après Verbier
ROW = re.compile(r'<tr data-q="latitude=46\.1002&amp;longitude=7\.22651&amp;tzid=Europe/Zurich" data-tz="Europe/Zurich"><td><a href="([^"]*)kosher-verbier/">[^<]*</a></td><td></td><td></td></tr>')
for p in sorted(glob.glob("**/index.html", recursive=True)):
    p = p.replace(os.sep, "/")
    if p.startswith("_"): continue
    s = rd(p); m = ROW.search(s)
    if not m: continue
    l = p.split("/")[0] + "/" if p.split("/")[0] in ("fr", "es", "he") else ""
    add = ""
    for x in STATIONS:
        if f'{x["s"]}/">' in s[m.end():m.end() + 800]: continue
        add += (f'<tr data-q="latitude={x["lat"]}&amp;longitude={x["lon"]}&amp;tzid=Europe/Zurich" data-tz="Europe/Zurich">'
                f'<td><a href="{m.group(1)}{x["s"]}/">{nom(x, l)}</a></td><td></td><td></td></tr>')
    if add: wr(p, s[:m.end()] + add + s[m.end():]); print("shabbat", p)
# 14. carte du hub /jewish-lyon-guide/ (EN seulement, comme Verbier ; régénérer le hub ferait perdre les CTA) + texte Verbier
p = "jewish-lyon-guide/index.html"; s = rd(p)
s = s.replace(VERBIER_CARTE[0], VERBIER_CARTE[1])
for x in ST:
    if f'href="../{x["s"]}/"' in s: continue
    m = re.search(r'<a class="hub-carte" href="\.\./' + x["apres"] + r'/">.*?</a>', s, re.S); assert m, x["s"]
    carte = (f'<a class="hub-carte" href="../{x["s"]}/"><div class="photo"><img src="../img/stock/hub-{x["s"]}.jpg" alt="" loading="lazy"></div>'
             f'<div class="corps"><h3>{x["carte"][0]}</h3><p>{x["carte"][1]}</p><span class="btn-noir">Open</span></div></a>')
    s = s[:m.end()] + carte + s[m.end():]; print("hub", x["s"])
if s != rd(p): wr(p, s)
# 15. sitemap (ordre alphabétique, date du jour) et llms.txt, sans relancer _build_sitemap.py (il redate les 270 URL)
s = rd("sitemap.xml"); lignes = s.split("\n")
for x in ST:
    for l in ("", "fr/", "es/", "he/"):
        loc = f"https://mishpachatours.com/{l}{x['s']}/"
        if f"<loc>{loc}</loc>" in s: continue
        new = f"  <url><loc>{loc}</loc><lastmod>2026-10-30</lastmod><priority>0.7</priority></url>"
        urls = [i for i, x2 in enumerate(lignes) if "<loc>" in x2]
        i = next((i for i in urls if re.search(r"<loc>([^<]*)</loc>", lignes[i]).group(1) > loc), urls[-1] + 1)
        lignes.insert(i, new); s = "\n".join(lignes)
if s != rd("sitemap.xml"): wr("sitemap.xml", s); print("patch sitemap.xml")
remplace("llms.txt", "Kosher Verbier, Valais, in winter and summer: private chef in your chalet, delivered meals, Shabbat, holidays, minyan and Sefer Torah. One written quote.",
         "Kosher Verbier, Valais, winter and summer: a private chef cooks in your chalet, kosher shopping brought in, Shabbat, holidays, minyan and Sefer Torah. One quote.")
s = rd("llms.txt")
for x in ST:
    if f"/{x['s']}/)" in s: continue
    anc = f"(https://mishpachatours.com/{x['apres']}/)"; i = s.find("\n", s.find(anc)) + 1; assert i > 0, x["s"]
    s = s[:i] + x["llms"] + s[i:]; print("llms", x["s"])
if s != rd("llms.txt"): wr("llms.txt", s)
print("done")
