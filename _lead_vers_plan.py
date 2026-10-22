# -*- coding: utf-8 -*-
"""Petit formulaire de la section lead-final -> /plan-your-trip/ prérempli (Moshé 22/10 : « j'en ai marre de recevoir
des messages à moitié faits », plus de WhatsApp depuis ce formulaire). Formulaire GET natif : arrivee, depart (dates),
adultes, enfants + les paramètres du lien « Plan your stay » de la page (i, lieu, voyage), que _prefill pose déjà.
Idempotent. À lancer après _lead.py, _prefill.py et _panneau_wa_alpes.py (ils réécrivent ce formulaire).
    python _lead_vers_plan.py [--dry]"""
import glob, html, os, re, sys
from urllib.parse import parse_qsl
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv

T = {"arr": {"en": "Arrival", "fr": "Arrivée", "es": "Llegada", "he": "הגעה"},
     "dep": {"en": "Departure", "fr": "Départ", "es": "Salida", "he": "עזיבה"},
     "date_van": {"en": "Date of the ride", "fr": "Date du trajet", "es": "Fecha del trayecto", "he": "תאריך הנסיעה"},
     "ad": {"en": "Adults", "fr": "Adultes", "es": "Adultos", "he": "מבוגרים"},
     "pass": {"en": "Passengers", "fr": "Passagers", "es": "Pasajeros", "he": "נוסעים"},
     "enf": {"en": "Children", "fr": "Enfants", "es": "Niños", "he": "ילדים"},
     "btn": {"en": "Continue my request", "fr": "Continuer ma demande", "es": "Continuar mi solicitud", "he": "המשך לתכנון הטיול"},
     "small": {"en": "Two more minutes on the next page, then a day-by-day programme the same day. Never on Shabbat.",
               "fr": "Encore deux minutes sur la page suivante, puis un programme jour par jour le jour même. Jamais pendant Chabbat.",
               "es": "Dos minutos más en la página siguiente y le enviamos un programa día a día el mismo día. Nunca en Shabat.",
               "he": "עוד שתי דקות בעמוד הבא, ואנחנו שולחים תוכנית יום אחר יום באותו יום. לא בשבת."}}

FORM_RE = re.compile(r'<form class="chercheur lead-form[^"]*"[^>]*>.*?</form>(\s*<script>document\.querySelectorAll\(\'\.lead-form\'\).*?</script>)?', re.S)
LIEN_RE = re.compile(r'href="(?:/(?:fr|es|he))?/plan-your-trip/\?([^"#]+)"')

def langue(p):
    m = re.match(r"(fr|es|he)[\\/]", p)
    return m.group(1) if m else "en"

def form(lang, params, van):
    pre = "" if lang == "en" else f"/{lang}"
    caches = "".join(f'<input type="hidden" name="{html.escape(k)}" value="{html.escape(v)}">' for k, v in params if k in ("i", "lieu", "voyage"))
    if van:
        duo1 = f'<label><span>{T["date_van"][lang]}</span><input name="arrivee" type="date"></label><label><span>{T["pass"][lang]}</span><input name="adultes" type="number" inputmode="numeric" min="1" max="99" placeholder="4"></label>'
        duo2 = ""
    else:
        duo1 = f'<label><span>{T["arr"][lang]}</span><input name="arrivee" type="date"></label><label><span>{T["dep"][lang]}</span><input name="depart" type="date"></label>'
        duo2 = f'<div class="duo"><label><span>{T["ad"][lang]}</span><input name="adultes" type="number" inputmode="numeric" min="1" max="99" placeholder="6"></label><label><span>{T["enf"][lang]}</span><input name="enfants" type="number" inputmode="numeric" min="0" max="99" placeholder="2"></label></div>'
    return (f'<form class="chercheur lead-form lead-plan" action="{pre}/plan-your-trip/" method="get">{caches}'
            f'<div class="duo">{duo1}</div>{duo2}'
            f'<button type="submit">{T["btn"][lang]}</button><small>{T["small"][lang]}</small></form>')

n = 0
for p in sorted(glob.glob("**/index.html", recursive=True)):
    if p.startswith(("preview", "_")): continue
    s = open(p, encoding="utf-8", newline="").read()
    i = s.find('<section class="ss lead-final"')
    if i < 0: continue
    j = s.find("</section>", i)
    bloc = s[i:j]
    m = FORM_RE.search(bloc)
    if not m: continue
    lang = langue(p)
    van = "kosher-van-transfers" in p.replace("\\", "/")
    lien = LIEN_RE.search(s[s.find("<main"):] if "<main" in s else s)
    params = parse_qsl(html.unescape(lien.group(1))) if lien else [("i", "c" if van else "a")]
    neuf = form(lang, params, van)
    if m.group(0) == neuf: continue
    s2 = s[:i] + bloc[:m.start()] + neuf + bloc[m.end():] + s[j:]
    n += 1
    if not DRY: open(p, "w", encoding="utf-8", newline="").write(s2)
print(("à changer" if DRY else "changés"), n)
