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
            "kosher-megeve": "Megève", "kosher-val-disere": "Val d'Isère", "kosher-val-thorens": "Val Thorens"}
SKI = "Ski holiday with a chalet"
CIBLES = {"kosher-chalet-les-deux-alpes": {"i": "a", "lieu": "Les Deux Alpes", "voyage": SKI},
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
    corps = re.sub(r'(href="[^"#?]*plan-your-trip/)(\?[^"#]*)?(#[^"]*)?"', lambda m: m.group(1) + query(c) + (m.group(3) or "") + '"', s[a:b])
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
JS = ("/*prefill*/document.getElementById('chercheur').addEventListener('submit',function(e){e.preventDefault();var f=e.target,o=f.voyage.options[f.voyage.selectedIndex],"
      "q=['i='+o.getAttribute('data-i')],v=o.getAttribute('data-voyage'),n=function(x){var m=/^\\s*(\\d{1,2})/.exec(x||'');return m?m[1]:''},a=n(f.adultes.value),c=n(f.enfants.value),"
      "d=/(\\d{4}-\\d\\d-\\d\\d)\\D+(\\d{4}-\\d\\d-\\d\\d)/.exec(f.dates.value);if(v)q.push('voyage='+encodeURIComponent(v));if(a)q.push('adultes='+a);if(c)q.push('enfants='+c);"
      "if(d){q.push('arrivee='+d[1]);q.push('depart='+d[2])}location.href='PRE/plan-your-trip/?'+q.join('&')});/*/prefill*/")

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
    js = JS.replace("PRE", "" if lang == "en" else "/" + lang)
    if "/*prefill*/" in s: s = re.sub(r"/\*prefill\*/.*?/\*/prefill\*/", lambda k: js, s, count=1, flags=re.S)
    else: s = re.sub(r"document\.getElementById\('chercheur'\)\.addEventListener\('submit',e=>\{.*?\}\);", lambda k: js, s, count=1, flags=re.S)
    if s != o: io.open(path, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

if __name__ == "__main__":
    n = 0
    for l in ("",) + tuple(x + "/" for x in LANGS):
        lang = l.rstrip("/") or "en"
        for slug, c in CIBLES.items():
            p = l + slug + "/index.html"
            if os.path.exists(p): n += page(p, slug, lang, c)
        if lang != "he": n += accueil(l + "index.html", lang)
    print(n, "pages modifiees")
