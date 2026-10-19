# -*- coding: utf-8 -*-
"""Liens preremplis vers /plan-your-trip/ (15/10). Idempotent. A lancer depuis site-v5/ apres _zones.py et _decor.py.
 (1) pages station, chalet, van, Lyon, tours, ete, ski : chaque lien vers /plan-your-trip/ du corps de page (entre <main> et <footer>)
     recoit ?i=...&lieu=...&voyage=... ; menu, panneau et pied restent generiques.
 (2) pages station : lien « Plan your stay in X » dans la section finale lead-final (avant le formulaire ; apres lui en hebreu,
     pour que le bouton WhatsApp passe en premier).
 (3) accueils EN, FR, ES : le chercheur ouvre le formulaire prerempli (hebreu : reste WhatsApp)."""
import io, os, re, glob
from urllib.parse import quote
os.chdir(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("fr", "es", "he")
STATIONS = {"kosher-alpe-dhuez": "Alpe d'Huez", "kosher-annecy": "Annecy", "kosher-chamonix": "Chamonix", "kosher-courchevel": "Courchevel",
            "kosher-grenoble": "Grenoble", "kosher-la-plagne": "La Plagne", "kosher-les-arcs": "Les Arcs", "kosher-les-deux-alpes": "Les Deux Alpes",
            "kosher-megeve": "Megève", "kosher-val-disere": "Val d'Isère", "kosher-val-thorens": "Val Thorens",
            "kosher-zermatt": "Zermatt", "kosher-st-moritz": "St. Moritz", "kosher-crans-montana": "Crans-Montana", "kosher-cervinia": "Cervinia", "kosher-courmayeur": "Courmayeur", "kosher-cortina": "Cortina d'Ampezzo"}
SKI = "Ski holiday with a chalet"
CIBLES = {"kosher-chalet-les-deux-alpes": {"i": "a", "lieu": "Les Deux Alpes", "voyage": SKI},
          "kosher-chalet-courchevel": {"i": "a", "lieu": "Courchevel", "voyage": SKI}, "kosher-chalets": {"i": "a", "voyage": SKI},
          "kosher-villa-saint-tropez": {"i": "a", "lieu": "Saint-Tropez", "voyage": "Summer in the Alps"},
          "kosher-van-transfers": {"i": "c"}, "jewish-lyon-tours": {"i": "d"},
          "summer-in-the-alps-jewish-families": {"i": "a", "voyage": "Summer in the Alps"},
          "kosher-ski-holidays-french-alps": {"i": "a", "voyage": SKI}}
for s in ("izieu", "jewish-lyon", "memory-chrd", "memory-montluc-neveh-shalom", "stopover"): CIBLES["tours/" + s] = {"i": "d"}
for k, v in STATIONS.items(): CIBLES[k] = {"i": "a", "lieu": v}
PLAN = {"en": "Plan your stay in {x}", "fr": "Préparer mon séjour : {x}", "es": "Planificar mi estancia: {x}", "he": "לתכנן את השהות: {x}"}

def query(c): return "?" + "&amp;".join(f"{k}={quote(v, safe='')}" for k, v in c.items())

def page(path, slug, lang, c):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    a, b = s.find("<main"), s.rfind("<footer")
    if a < 0 or b < 0: return 0
    # 19/10 : les cartes chalet (blocs KIT-WP de _kit_wp.py) gardent leur propre préremplissage (station du chalet), sinon va-et-vient
    morceaux = re.split(r"(<!--KIT-WP:(\w+)-->.*?<!--/KIT-WP:\2-->)", s[a:b], flags=re.S)
    corps = "".join(x if i % 3 == 1 else "" if i % 3 == 2 else
                    re.sub(r'(href="[^"#?]*plan-your-trip/)(\?[^"#]*)?(#[^"]*)?"', lambda m: m.group(1) + query(c) + (m.group(3) or "") + '"', x)
                    for i, x in enumerate(morceaux))
    corps = re.sub(r'\s*<p class="lead-plan">.*?</p>', "", corps, flags=re.S)
    if slug in STATIONS and 'class="ss lead-final"' in corps:
        h1 = re.search(r"<h1>([^<]*)", corps).group(1)
        nom = re.split(r",\s*", h1)[0].strip() if lang != "en" else STATIONS[slug]
        pre = "" if lang == "en" else "/" + lang
        p = f'\n  <p class="lead-plan"><a href="{pre}/plan-your-trip/{query(c)}">{PLAN[lang].format(x=nom)}</a></p>'
        if lang == "he": corps = re.sub(r'(<section class="ss lead-final">.*?</form>)', lambda m: m.group(1) + p, corps, count=1, flags=re.S)
        else: corps = re.sub(r'(<section class="ss lead-final">.*?</div>\s*</div>)(\s*<form)', lambda m: m.group(1) + p + m.group(2), corps, count=1, flags=re.S)
    s = s[:a] + corps + s[b:]
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

OPT = [("a", SKI), ("a", "Hanukkah in the Alps"), ("a", "Summer in the Alps"), ("b", ""), ("d", ""), ("f", "")]
LABEL = {"en": ("Plan my stay on WhatsApp", "Plan my stay"), "fr": ("Organiser mon séjour sur WhatsApp", "Organiser mon séjour"),
         "es": ("Planear mi estancia por WhatsApp", "Planear mi estancia")}
JS = ("/*prefill*/(function(){var f=document.getElementById('chercheur'),a0=f.arrivee,d0=f.depart,t=new Date(Date.now()-new Date().getTimezoneOffset()*6e4).toISOString().slice(0,10);"
      "if(a0){a0.min=t;d0.min=t;a0.addEventListener('change',function(){d0.min=a0.value||t;if(d0.value&&d0.value<a0.value)d0.value=''})}"
      "f.addEventListener('submit',function(e){e.preventDefault();var o=f.voyage.options[f.voyage.selectedIndex],"
      "q=['i='+o.getAttribute('data-i')],v=o.getAttribute('data-voyage'),n=function(x){var m=/^\\s*(\\d{1,2})/.exec(x||'');return m?m[1]:''},a=n(f.adultes.value),c=n(f.enfants.value);"
      "if(v)q.push('voyage='+encodeURIComponent(v));if(a)q.push('adultes='+a);if(c)q.push('enfants='+c);"
      "if(a0&&a0.value)q.push('arrivee='+a0.value);if(d0&&d0.value)q.push('depart='+d0.value);location.href='PRE/plan-your-trip/?'+q.join('&')})})();/*/prefill*/")
# Chercheur : deux vraies dates (calendrier du telephone) au lieu d'un texte libre perdu au preremplissage (Moshe, 15/10)
CH = {"en": ("Arrival", "Departure", "Adults", "Children", "6", "2"), "fr": ("Arrivée", "Départ", "Adultes", "Enfants", "6", "2"),
      "es": ("Llegada", "Salida", "Adultos", "Niños", "6", "2")}
def champs(lang):
    a, d, ad, en, pa, pe = CH[lang]
    return (f'<div class="duo"><label><span>{a}</span><input name="arrivee" type="date"></label><label><span>{d}</span><input name="depart" type="date"></label></div>'
            f'\n      <div class="duo"><label><span>{ad}</span><input name="adultes" type="text" inputmode="numeric" placeholder="{pa}"></label>'
            f'<label><span>{en}</span><input name="enfants" type="text" inputmode="numeric" placeholder="{pe}"></label></div>')
# Bas de l'accueil : le formulaire court repetait le chercheur, remplace par un bouton vers le formulaire complet (Moshe, 15/10)
BOUTON = {"en": "Plan your trip", "fr": "Préparer mon voyage", "es": "Planificar mi viaje", "he": "לתכנן את הטיול"}
def bas(s, lang):
    """Toutes les pages (15/10) : le ticket rose garde son titre et WhatsApp, le formulaire devient un bouton ;
    s'il y a deja la section verte lead-final, le ticket rose disparait et lead-final prend l'ancre #book."""
    pre = "" if lang == "en" else "/" + lang
    if 'class="ss lead-final"' in s:
        s = re.sub(r'\s*<div class="ticket-zone"[^>]*>.*?</form>.*?</div>\s*</div>', "", s, count=1, flags=re.S)
        if 'id="book"' not in s: s = s.replace('<section class="ss lead-final">', '<section class="ss lead-final" id="book">', 1)
        return s
    b = f'<p class="ticket-plan"><a class="btn-noir" href="{pre}/plan-your-trip/">{BOUTON[lang]}</a></p>'
    return re.sub(r'<form id="formReserver">.*?</form>(?:\s*<p class="ac-form-lien">.*?</p>)?', lambda m: b, s, count=1, flags=re.S)

def accueil(path, lang):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    m = re.search(r'(<select name="voyage">)(.*?)(</select>)', s, re.S)
    if not m: return 0
    ops = re.findall(r"<option[^>]*>([^<]*)</option>", m.group(2))
    if len(ops) != 6: return 0
    sel = m.group(1) + "".join(f'<option data-i="{i}"' + (f' data-voyage="{v}"' if v else "") + f">{t}</option>" for (i, v), t in zip(OPT, ops)) + m.group(3)
    s = s[:m.start()] + sel + s[m.end():]
    old, new = LABEL[lang]
    s = re.sub(r'(<button type="submit">)<svg><use href="#wa"/></svg>' + re.escape(old) + "</button>", lambda k: k.group(1) + new + "</button>", s, count=1)
    s = re.sub(r'(<form class="chercheur" id="chercheur">.*?</label>\s*)<div class="duo">.*?<input name="enfants"[^>]*></label>(?:</div>)?', lambda k: k.group(1) + champs(lang), s, count=1, flags=re.S)
    js = JS.replace("PRE", "" if lang == "en" else "/" + lang)
    if "/*prefill*/" in s: s = re.sub(r"/\*prefill\*/.*?/\*/prefill\*/", lambda k: js, s, count=1, flags=re.S)
    else: s = re.sub(r"document\.getElementById\('chercheur'\)\.addEventListener\('submit',e=>\{.*?\}\);", lambda k: js, s, count=1, flags=re.S)
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

if __name__ == "__main__":
    n = 0
    for p in glob.glob("**/index.html", recursive=True):   # bas de page d'abord, les liens recoivent ensuite leur preremplissage
        if p.startswith("_"): continue
        lang = p.split("\\")[0].split("/")[0]; lang = lang if lang in LANGS else "en"
        t = io.open(p, encoding="utf-8", newline="").read(); t2 = bas(t, lang)
        if t2 != t: io.open(p, "w", encoding="utf-8", newline="").write(t2); n += 1
    n = 0
    for l in ("",) + tuple(x + "/" for x in LANGS):
        lang = l.rstrip("/") or "en"
        for slug, c in CIBLES.items():
            p = l + slug + "/index.html"
            if os.path.exists(p): n += page(p, slug, lang, c)
        if lang != "he": n += accueil(l + "index.html", lang)

    print(n, "pages modifiees")
