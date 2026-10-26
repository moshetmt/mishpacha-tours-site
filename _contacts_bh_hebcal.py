# -*- coding: utf-8 -*-
"""Contacts, Beth Habad, Hebcal : post-traitement idempotent des sorties HTML des 4 langues (ordres operateur du 14/10).
  python _contacts_bh_hebcal.py   : apres les builds et _zones.py, AVANT _decor.py (relancer _decor.py ensuite). Peut tourner deux fois.
1. Aucun numero de telephone dans le texte visible ni dans les meta (le JSON-LD n'est pas touche). Les liens wa.me / tel: gardent leur href.
2. Bloc « Minyan » (+ « repas livres ») vers le WhatsApp du Beth Habad (33781823193) sur les pages Alpes ; tout le reste du WhatsApp = operateur.
3. Plus de Grenoble sur les pages Deux Alpes (reseau Chabad « cote Grenoble », parquet de Grenoble).
4. Plus de renvoi vers Hebcal dans le texte visible : encadre d'horaires de Shabbat affiche en direct (API JSON Hebcal, geonameid par station).
Les pages ne sont pas regenerees : les sources _pages/*.py et _gabarit.html portent encore l'ancien texte, donc ce script doit passer apres tout build.
"""
import glob, io, json, os, re, urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
LANGS = ("fr", "es", "he")
WA_BH = "33781823193"

# ---------------------------------------------------------------- 1. numeros
NUM = r"\+33 6 52 09 23 01"
OUVRIR = {"en": "Open the chat", "fr": "Ouvrir la conversation", "es": "Abrir el chat", "he": "פתחו שיחה"}
N3 = r"0[1-9](?: \d\d){4}"  # numeros francais de tiers (restaurants, delegues, Beth Din, memoriaux)


def sans_numeros(h, lang):
    def seg(t):
        t = re.sub(r"(WhatsApp|וואטסאפ)(?:[\s‎‏\xa0]|&nbsp;)*" + NUM, r"\1", t, flags=re.I)
        t = re.sub(r">" + NUM + "</a>", ">" + OUVRIR[lang] + "</a>", t)
        t = re.sub(r"[‎‏]?" + NUM, "WhatsApp", t)
        # Beth Habad de Grenoble (page ski) : le numero et « appelez les deux »
        t = re.sub(r"(habadgrenoblealpes\.com)\.[^<]*?04 85 02 84 47[^<]*(</small>)", r"\1\2", t)
        # numeros de tiers
        t = re.sub(r",\s*" + N3 + r"\)", ")", t)
        t = re.sub(r"\s*\(" + N3 + r"\)", "", t)
        t = re.sub(r",\s*" + N3 + r"(?=[,<.])", "", t)
        t = re.sub(r"\s*:\s+" + N3 + r"(?=\.)", "", t)
        t = re.sub(r"\s+(?:on|en el|al|au)\s+" + N3, "", t)
        t = re.sub(r"\s+ב-" + N3, "", t)
        t = re.sub(r"(?<=[֐-׿])\s+" + N3, "", t)
        return t
    return segments(h, seg)


def segments(h, f):
    """Applique f aux parties hors <script> (JSON-LD et JS intacts)."""
    p = re.split(r"(<script\b.*?</script>)", h, flags=re.S)
    return "".join(x if i % 2 else f(x) for i, x in enumerate(p))


# ---------------------------------------------------------------- 3. Grenoble (pages Deux Alpes)
GRENOBLE = [
    ("the Chabad network of the Alps on the Grenoble side", "the Beth Habad of the Alps"),
    ("the Grenoble prosecutor's office", "the prosecutor's office"),
    ("le réseau Chabad des Alpes, côté Grenoble", "le Beth Habad des Alpes"),
    ("au parquet de Grenoble", "au parquet"),
    ("la red Chabad de los Alpes en el lado de Grenoble", "el Beth Habad de los Alpes"),
    ("a la fiscalía de Grenoble", "a la fiscalía"),
    ("רשת חב״ד באלפים בצד גרנובל", "בית חב״ד באלפים"),
    ("לפרקליטות גרנובל", "לפרקליטות"),
]


def sans_grenoble(h):
    return segments(h, lambda t: _rep(t, GRENOBLE))


def _rep(t, table):
    for a, b in table:
        t = t.replace(a, b)
    return t


# ---------------------------------------------------------------- 4. Hebcal
PLACES = {  # slug : (geonameid, {lang: nom})
    "kosher-alpe-dhuez": (3013022, dict(en="Alpe d'Huez", fr="Alpe d’Huez", es="Alpe d'Huez", he="אלפ ד'ואז")),
    "kosher-annecy": (3037543, dict(en="Annecy", fr="Annecy", es="Annecy", he="אנסי")),
    "kosher-chalet-les-deux-alpes": (6354942, dict(en="Les Deux Alpes", fr="Les Deux Alpes", es="Les Deux Alpes", he="לה דז אלפ")),
    "kosher-slope-chalet-les-deux-alpes": (6354942, dict(en="Les Deux Alpes", fr="Les Deux Alpes", es="Les Deux Alpes", he="לה דז אלפ")),
    "kosher-chamonix": (3027301, dict(en="Chamonix", fr="Chamonix", es="Chamonix", he="שמוני")),
    "kosher-courchevel": (3023065, dict(en="Courchevel", fr="Courchevel", es="Courchevel", he="קורשבל")),
    "kosher-chalet-courchevel": (3023065, dict(en="Courchevel", fr="Courchevel", es="Courchevel", he="קורשבל")),
    "kosher-grenoble": (3014728, dict(en="Grenoble", fr="Grenoble", es="Grenoble", he="גרנובל")),
    "kosher-la-plagne": (2996874, dict(en="La Plagne", fr="La Plagne", es="La Plagne", he="לה פלאן")),
    "kosher-les-arcs": (3030949, dict(en="Les Arcs", fr="Les Arcs", es="Les Arcs", he="לז ארק")),
    "kosher-les-deux-alpes": (6354942, dict(en="Les Deux Alpes", fr="Les Deux Alpes", es="Les Deux Alpes", he="לה דז אלפ")),
    "kosher-megeve": (2994768, dict(en="Megève", fr="Megève", es="Megève", he="מז'ב")),
    "kosher-chalet-megeve": (2994768, dict(en="Megève", fr="Megève", es="Megève", he="מז'ב")),
    "kosher-val-disere": (2971074, dict(en="Val d'Isère", fr="Val d’Isère", es="Val d'Isère", he="ואל דיזר")),
    "kosher-val-thorens": (6544556, dict(en="Val Thorens", fr="Val Thorens", es="Val Thorens", he="ואל טורנס")),
    "kosher-chalet-val-thorens": (6544556, dict(en="Val Thorens", fr="Val Thorens", es="Val Thorens", he="ואל טורנס")),
    "kosher-zermatt": (2657928, dict(en="Zermatt", fr="Zermatt", es="Zermatt", he="צרמט")),
    "kosher-st-moritz": (2658813, dict(en="St. Moritz", fr="Saint-Moritz", es="St. Moritz", he="סנט מוריץ")),
    "kosher-crans-montana": (6559506, dict(en="Crans-Montana", fr="Crans-Montana", es="Crans-Montana", he="קראן מונטנה")),
    "kosher-cervinia": (6534766, dict(en="Cervinia", fr="Cervinia", es="Cervinia", he="צרביניה")),
    "kosher-courmayeur": (3177872, dict(en="Courmayeur", fr="Courmayeur", es="Courmayeur", he="קורמאייר")),
    "kosher-cortina": (3177952, dict(en="Cortina d'Ampezzo", fr="Cortina d'Ampezzo", es="Cortina d'Ampezzo", he="קורטינה")),
    # pages multi-stations : Albertville, au centre des Alpes
    "kosher-ski-holidays-french-alps": (3038266, dict(en="the Alps", fr="les Alpes", es="los Alpes", he="האלפים")),
    "summer-in-the-alps-jewish-families": (3038266, dict(en="the Alps", fr="les Alpes", es="los Alpes", he="האלפים")),
}
MULTI = {"kosher-ski-holidays-french-alps", "summer-in-the-alps-jewish-families"}
LYON = {"shabbat-in-lyon", "synagogues-lyon", "jewish-lyon-guide"}
LYON_GID = 2996944
# 19/10 : un horaire = un lieu. Coordonnees du centre de chaque station (le geonameid tombait parfois sur le village
# de vallee : Macot pour La Plagne, Bourg-Saint-Maurice pour Les Arcs, Valtournenche pour Cervinia, Huez pour l'Alpe).
COORDS = {  # slug : (latitude, longitude, tzid)
    "kosher-courchevel": (45.4154, 6.6364, "Europe/Paris"), "kosher-val-thorens": (45.2978, 6.5838, "Europe/Paris"), "kosher-chalet-val-thorens": (45.2978, 6.5838, "Europe/Paris"),
    "kosher-megeve": (45.8569, 6.6178, "Europe/Paris"), "kosher-chalet-megeve": (45.8569, 6.6178, "Europe/Paris"), "kosher-alpe-dhuez": (45.0909, 6.0710, "Europe/Paris"),
    "kosher-les-deux-alpes": (45.0116, 6.1255, "Europe/Paris"), "kosher-chalet-les-deux-alpes": (45.0116, 6.1255, "Europe/Paris"), "kosher-slope-chalet-les-deux-alpes": (45.0116, 6.1255, "Europe/Paris"),
    "kosher-chalet-courchevel": (45.4154, 6.6364, "Europe/Paris"),
    "kosher-chamonix": (45.9237, 6.8694, "Europe/Paris"), "kosher-annecy": (45.8992, 6.1294, "Europe/Paris"),
    "kosher-grenoble": (45.1885, 5.7245, "Europe/Paris"), "kosher-la-plagne": (45.5070, 6.6780, "Europe/Paris"),
    "kosher-les-arcs": (45.5726, 6.8279, "Europe/Paris"), "kosher-val-disere": (45.4481, 6.9800, "Europe/Paris"),
    "kosher-zermatt": (46.0200, 7.7486, "Europe/Zurich"), "kosher-st-moritz": (46.4994, 9.8433, "Europe/Zurich"),
    "kosher-crans-montana": (46.3132, 7.4791, "Europe/Zurich"), "kosher-cervinia": (45.9336, 7.6297, "Europe/Rome"),
    "kosher-courmayeur": (45.7966, 6.9689, "Europe/Rome"), "kosher-cortina": (46.5369, 12.1390, "Europe/Rome"),
}
STATIONS = [s for s in COORDS if s not in ("kosher-chalet-les-deux-alpes", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-chalet-val-thorens")]  # tableau des pages multi-stations
REPLI = {"en": "Candle lighting falls as early as 16:30 in December and after 21:00 in June.",  # Lyon seulement
         "fr": "L’allumage des bougies tombe dès 16:30 en décembre et après 21:00 en juin.",
         "es": "El encendido de velas cae hacia las 16:30 en diciembre y después de las 21:00 en junio.",
         "he": "הדלקת הנרות חלה כבר ב-16:30 בדצמבר, ואחרי 21:00 ביוני."}
REPLI_ST = {"en": "Times calculated for the coordinates of {}.", "fr": "Horaires calculés aux coordonnées de {}.",
            "es": "Horarios calculados para las coordenadas de {}.", "he": "הזמנים מחושבים לפי הקואורדינטות של {}."}
NOTE = {"en": "Each resort has its own times: they are calculated for its coordinates, resort by resort.",
        "fr": "Chaque station a ses horaires : ils sont calculés aux coordonnées de la station, une par une.",
        "es": "Cada estación tiene sus propios horarios: se calculan para sus coordenadas, una por una.",
        "he": "לכל אתר זמנים משלו: הם מחושבים לפי הקואורדינטות של כל אתר בנפרד."}
COL = {"en": "Resort", "fr": "Station", "es": "Estación", "he": "אתר"}
# encadre v2 (15/10) : maquette scratchpad/test-compte-a-rebours.html, section « Apres »
SH = {  # mot Shabbat, preposition + ville, sur-titre, libelles, etats
    "en": dict(mot="Shabbat", vil="in {}", sur="This week", cand="Candle lighting", hav="Havdalah", loc="en-GB", paix="Shabbat Shalom",
               tov="Shavua tov", suiv="Next Shabbat", rep="We answer messages after Havdalah."),
    "fr": dict(mot="Shabbat", vil="à {}", sur="Cette semaine", cand="Allumage des bougies", hav="Havdala", loc="fr-FR", paix="Shabbat Shalom",
               tov="Shavoua tov", suiv="Prochain Shabbat", rep="Nous répondons aux messages après la havdala."),
    "es": dict(mot="Shabat", vil="en {}", sur="Esta semana", cand="Encendido de velas", hav="Havdalá", loc="es-ES", paix="Shabat Shalom",
               tov="Shavua tov", suiv="Próximo Shabat", rep="Respondemos a los mensajes después de la havdalá."),
    "he": dict(mot="שבת", vil="ב{}", sur="השבוע", cand="הדלקת נרות", hav="הבדלה", loc="he-IL", paix="שבת שלום",
               tov="שבוע טוב", suiv="השבת הבאה", rep="נענה להודעות אחרי ההבדלה."),
}
MULTI_NOM = {"en": "in the Alps", "fr": "dans les Alpes", "es": "en los Alpes", "he": "באלפים"}
LYON_NOM = dict(en="Lyon", fr="Lyon", es="Lyon", he="ליון")

# phrases mixtes a recoudre a la main (le reste des phrases « Hebcal » est supprime)
SPECIAL = [
    # page ski : on garde la consigne « demandez les horaires des offices »
    (r"Look it up for your resort with Hebcal, and ask your Chabad", "Ask your Chabad", True),
    (r"Consultez-le pour votre station avec Hebcal, et demandez les horaires des offices", "Demandez les horaires des offices", True),
    (r"Consúltela para su estación con Hebcal y pida a su contacto de Chabad", "Pida a su contacto de Chabad", True),
    (r"בדקו אותו לאתר שלכם ב-Hebcal, ושאלו את איש הקשר", "שאלו את איש הקשר", True),
    # shabbat-in-lyon
    (r", from Hebcal for Lyon", " for Lyon", False), (r", from Hebcal\.", ".", False),
    (r", d’après Hebcal pour Lyon", " pour Lyon", False), (r", d’après Hebcal\.", ".", False),
    (r", según Hebcal para Lyon", " para Lyon", False), (r", según Hebcal\.", ".", False),
    (r", מתוך Hebcal עבור ליון", " עבור ליון", False), (r", מתוך Hebcal\.", ".", False),
    (r",\s*hebcal\.com", "", False),  # liste de sources
]


SVG_ENTREE = ('<svg viewBox="0 0 72 48" aria-hidden="true"><defs><clipPath id="sh-sol"><rect width="72" height="34"/></clipPath>'
              '<radialGradient id="sh-lueur" cx=".5" cy="1" r=".55"><stop offset="0" stop-color="#E8875A" stop-opacity=".9"/>'
              '<stop offset="1" stop-color="#E8875A" stop-opacity="0"/></radialGradient></defs>'
              '<rect class="sh-ciel" width="72" height="34" fill="url(#sh-lueur)" opacity="0"/><g clip-path="url(#sh-sol)"><g class="sh-soleil">'
              '<circle cx="36" cy="24" r="9" fill="#FCDE73"/><g stroke="#FCDE73" stroke-width="2" stroke-linecap="round">'
              '<path d="M36 9v-4M24 14l-3-3M48 14l3-3M19 24h-4M53 24h4"/></g></g></g><path d="M6 34h60" stroke="#FFFAED" stroke-width="2" stroke-linecap="round"/>'
              '<path d="M14 40h44M24 45h24" stroke="#FFFAED" stroke-width="2" stroke-linecap="round" opacity=".35"/></svg>')
SVG_SORTIE = ('<svg viewBox="0 0 72 48" aria-hidden="true"><g class="sh-lune"><path d="M40 8a15 15 0 1 0 14 22A12 12 0 0 1 40 8z" fill="#FFFAED"/></g>'
              '<g fill="#FCDE73"><path class="sh-etoile sh-e1" d="M14 10l1.4 3 3 1.4-3 1.4L14 19l-1.4-3.2-3-1.4 3-1.4z"/>'
              '<path class="sh-etoile sh-e2" d="M60 6l1 2.2 2.2 1-2.2 1-1 2.2-1-2.2-2.2-1 2.2-1z"/>'
              '<path class="sh-etoile sh-e3" d="M24 30l1 2.2 2.2 1-2.2 1-1 2.2-1-2.2-2.2-1 2.2-1z"/></g></svg>')
CSS_DEB, CSS_FIN = "/* SHABBAT v2 (15/10) */", "/* fin SHABBAT v2 */"
CSS_SH = CSS_DEB + r"""
.shabbat .sh-tete{display:flex;flex-direction:column;align-items:flex-start;gap:14px}
.sh-sur{margin:0 0 4px;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.7}
.sh-gros{margin:0;font-family:var(--titre);font-weight:700;font-size:34px;line-height:1.08}
.sh-ville{color:var(--jaune)}
.sh-des{flex:none;width:150px;height:auto;order:-1}
.sh-moments{display:grid;gap:10px;margin-top:18px}
.sh-moment{display:grid;grid-template-columns:72px 1fr;gap:14px;align-items:center;background:rgba(255,250,237,.06);border-radius:12px;padding:10px 14px 10px 10px}
.sh-moment[hidden],.sh-moments[hidden]{display:none}
.sh-moment svg{width:72px;height:48px;display:block}
.sh-moment b{display:block;font-family:var(--titre);font-weight:700;font-size:26px;line-height:1.1;font-variant-numeric:tabular-nums}
.sh-moment span{font-size:14px;opacity:.75}
.sh-soleil{transform-box:view-box}
.sh-lune,.sh-etoile{transform-box:fill-box;transform-origin:center}
@media (prefers-reduced-motion:no-preference){
 .sh-soleil{animation:sh-coucher 7s cubic-bezier(.45,0,.55,1) infinite}
 .sh-ciel{animation:sh-soir 7s cubic-bezier(.45,0,.55,1) infinite}
 .sh-lune{animation:sh-lever 7s cubic-bezier(.45,0,.55,1) infinite}
 .sh-etoile{animation:sh-scintille 7s ease-in-out infinite}
 .sh-e2{animation-delay:.6s}.sh-e3{animation-delay:1.2s}
}
@keyframes sh-coucher{0%{transform:translateY(-10px)}55%,80%{transform:translateY(14px)}100%{transform:translateY(-10px)}}
@keyframes sh-soir{0%{opacity:0}55%,80%{opacity:1}100%{opacity:0}}
@keyframes sh-lever{0%{transform:translateY(12px);opacity:.2}45%,85%{transform:translateY(0);opacity:1}100%{transform:translateY(12px);opacity:.2}}
@keyframes sh-scintille{0%,30%{opacity:0;transform:scale(.4)}50%,85%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.4)}}
@media (min-width:900px){.shabbat .sh-tete{flex-direction:row;align-items:center;justify-content:space-between}.sh-des{order:0;width:220px}.sh-gros{font-size:52px}.sh-moments{grid-template-columns:1fr 1fr}}
.sh-dates{margin:18px 0 6px;font-size:14px;opacity:.75}
.sh-table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
.sh-table th{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.7;text-align:start;padding:8px 6px}
.sh-table td{padding:9px 6px;border-top:1px solid rgba(255,250,237,.12);font-size:16px}
.sh-table td+td,.sh-table th+th{text-align:end;width:24%}
.sh-table td+td{white-space:nowrap}
.sh-table th{line-height:1.3;vertical-align:bottom}
.sh-table td b{font-family:var(--titre);font-weight:700;font-size:17px}
@media (min-width:600px){.sh-table td b{font-size:20px}}
.sh-table a{color:inherit;text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(255,250,237,.35)}
""" + CSS_FIN


def poser_css_et_dessin():
    c = io.open("styles.css", encoding="utf-8").read()
    if CSS_DEB in c:
        c2 = re.sub(re.escape(CSS_DEB) + r".*?" + re.escape(CSS_FIN), lambda m: CSS_SH, c, flags=re.S)
    else:
        c2 = c.rstrip("\n") + "\n\n" + CSS_SH + "\n"
    if c2 != c:
        io.open("styles.css", "w", encoding="utf-8", newline="\n").write(c2)
    if not os.path.exists("img/des/_shabbat-tete.webp"):  # hallot + vin, rogne au contenu (le mini-dessin carre garde des bandes vides)
        from PIL import Image
        im = Image.open("img/des/shabbat-a.webp").convert("RGBA")
        im = im.crop(im.getbbox())
        im = im.resize((360, round(360 * im.height / im.width)), Image.LANCZOS)
        im.save("img/des/_shabbat-tete.webp", "WEBP", quality=88)


JS_SH = r"""<script data-shabbat>
(function(){var C=__CFG__;var Z=C.tz,U="https://www.hebcal.com/shabbat?cfg=json&"+C.q+"&M=on&lg="+C.lg;
var B=document.getElementById("shabbat");if(!B)return;
function $(s){return B.querySelector(s)}
function f(s){return new Date(s).toLocaleTimeString(C.loc,{hour:"2-digit",minute:"2-digit",timeZone:Z})}
function dd(s){return new Date(s).toLocaleDateString(C.loc,{weekday:"long",day:"numeric",month:"short",timeZone:Z})}
function lire(d){var it=d.items||[];return{c:it.find(function(i){return i.category==="candles"}),h:it.find(function(i){return i.category==="havdalah"}),p:it.find(function(i){return i.category==="parashat"})}}
function rendre(x,etat){var e=$("#m-entree"),s=$("#m-sortie"),ti=$(".sh-tt"),co=$(".shabbat-corps"),pa=x.p?"<small>"+x.p.title+"</small>":"",n=C.note?"<br><small>"+C.note+"</small>":"";
e.hidden=false;s.hidden=false;$(".sh-moments").hidden=false;ti.textContent=C.mot;
if(x.c){e.querySelector(".sh-d").textContent=(etat==="apres"?C.suiv+" \u00b7 ":"")+dd(x.c.date);(e.querySelector("b")||e.querySelector(".sh-d").insertAdjacentElement("afterend",document.createElement("b"))).textContent=f(x.c.date)}else e.hidden=true;
if(x.h){s.querySelector(".sh-d").textContent=dd(x.h.date);(s.querySelector("b")||s.querySelector(".sh-d").insertAdjacentElement("afterend",document.createElement("b"))).textContent=f(x.h.date)}else s.hidden=true;
co.innerHTML=pa+n;
if(etat==="pendant"){ti.textContent=C.paix;e.hidden=true;co.innerHTML=C.rep+"<br>"+pa+n}
else if(etat==="apres")ti.textContent=C.tov}
fetch(U).then(function(r){return r.json()}).then(function(d){var x=lire(d);if(!x.c&&!x.h)return;var t=new Date();
if(x.c&&x.h&&t>=new Date(x.h.date)){var j=new Date(t.getTime()+864e5).toLocaleDateString("sv-SE",{timeZone:Z});
return fetch(U+"&dt="+j).then(function(r){return r.json()}).then(function(d2){var y=lire(d2);rendre(y.c||y.h?y:x,"apres")})}
rendre(x,x.c&&x.h&&t>=new Date(x.c.date)?"pendant":"avant")}).catch(function(){})})();
</script>"""


# pages multi-stations (19/10) : une ligne par station, chacune calculee a ses coordonnees
JS_MULTI = r"""<script data-shabbat>
(function(){var C=__CFG__;var B=document.getElementById("shabbat");if(!B)return;
var R=[].slice.call(B.querySelectorAll("tr[data-q]"));if(!R.length)return;
function u(r,dt){return "https://www.hebcal.com/shabbat?cfg=json&"+r.getAttribute("data-q")+"&M=on&lg="+C.lg+(dt?"&dt="+dt:"")}
function f(s,z){return new Date(s).toLocaleTimeString(C.loc,{hour:"2-digit",minute:"2-digit",timeZone:z})}
function dd(s,z){return new Date(s).toLocaleDateString(C.loc,{weekday:"long",day:"numeric",month:"short",timeZone:z})}
function lire(d){var it=d.items||[];return{c:it.find(function(i){return i.category==="candles"}),h:it.find(function(i){return i.category==="havdalah"})}}
function tout(dt){return Promise.all(R.map(function(r){return fetch(u(r,dt)).then(function(x){return x.json()}).then(lire).catch(function(){return{}})}))}
function rendre(L,etat){var z=R[0].getAttribute("data-tz"),p=null;
R.forEach(function(r,i){var x=L[i]||{},td=r.querySelectorAll("td");if(!p&&x.c&&x.h)p=x;
td[1].innerHTML=x.c?"<b>"+f(x.c.date,r.getAttribute("data-tz"))+"</b>":"";td[2].innerHTML=x.h?"<b>"+f(x.h.date,r.getAttribute("data-tz"))+"</b>":""});
if(!p)return;var d=B.querySelector(".sh-dates");d.textContent=(etat==="apres"?C.suiv+" · ":"")+dd(p.c.date,z)+" → "+dd(p.h.date,z);d.hidden=false;
var ti=B.querySelector(".sh-tt");ti.textContent=etat==="pendant"?C.paix:etat==="apres"?C.tov:C.mot;
if(etat==="pendant")B.querySelector(".shabbat-corps").innerHTML=C.rep+"<br><small>"+C.note+"</small>"}
tout().then(function(L){var t=new Date(),x=L.filter(function(y){return y.c&&y.h})[0];if(!x)return;
if(t>=new Date(x.h.date)){var j=new Date(t.getTime()+864e5).toLocaleDateString("sv-SE",{timeZone:"Europe/Paris"});return tout(j).then(function(L2){rendre(L2,"apres")})}
rendre(L,t>=new Date(x.c.date)?"pendant":"avant")})})();
</script>"""


def requete(slug):
    if slug in COORDS:
        la, lo, tz = COORDS[slug]
        return "latitude=%s&longitude=%s&tzid=%s" % (la, lo, tz), tz
    return "geonameid=%d" % LYON_GID, "Europe/Paris"


def script_shabbat(lang, slug, multi):
    t = SH[lang]
    q, tz = requete(slug)
    cfg = dict(q=q, tz=tz, lg=lang, loc=t["loc"], mot=t["mot"], paix=t["paix"], tov=t["tov"], suiv=t["suiv"], rep=t["rep"],
               note=NOTE[lang] if multi else "")
    return (JS_MULTI if multi else JS_SH).replace("__CFG__", json.dumps(cfg, ensure_ascii=False))


def tableau_stations(lang):
    t, pre = SH[lang], ("" if lang == "en" else "/" + lang)
    lignes = "".join('<tr data-q="%s" data-tz="%s"><td><a href="%s/%s/">%s</a></td><td></td><td></td></tr>'
                     % (requete(s)[0].replace("&", "&amp;"), requete(s)[1], pre, s, PLACES[s][1][lang]) for s in STATIONS)
    return ('<p class="sh-dates" hidden></p><table class="sh-table"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>'
            '<tbody>%s</tbody></table>') % (COL[lang], t["cand"], t["hav"], lignes)


def fin_section(h, idx):
    """Fin de la section de premier niveau qui contient la position idx."""
    ops = list(re.finditer(r'<section class="ss [^"]*">|<div class="ss beige[^"]*">', h[:idx]))
    if not ops:
        return idx
    o = ops[-1]
    tag = "section" if o.group(0).startswith("<section") else "div"
    depth, pos = 0, o.start()
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), h[pos:]):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return pos + m.end()
    return idx


BLOC = re.compile(r"<(p|li)(\s[^>]*)?>(.*?)</\1>", re.S)


def vide(s):
    s = re.sub(r'<img class="dk[^>]*>|<svg class="dk.*?</svg>|<button class="dk.*?</button>', "", s, flags=re.S)
    return not re.sub(r"<[^>]+>|\s|&nbsp;", "", s)


def sans_hebcal(h, slug):
    """Supprime toute phrase de paragraphe ou de puce qui renvoie vers Hebcal. Rend (html, position apres le premier bloc touche)."""
    ancre = [None]
    for rx, b, ancrer in SPECIAL:
        h2 = re.sub(rx, b, h)
        if ancrer and h2 != h:
            m = re.search(re.escape(b), h2)
            ancre[0] = m.end() if m else None
        h = h2
    out, last = [], 0
    for m in BLOC.finditer(h):
        inner = m.group(3)
        if "hebcal" not in inner.lower():
            continue
        parts = re.split(r"((?<=\.)\s+(?![^<]*>)|(?<=</b>)\s+)", inner)
        ph, seps = parts[0::2], parts[1::2]
        keep = [i for i, t in enumerate(ph) if "hebcal" not in t.lower()]
        new = ""
        for n, i in enumerate(keep):
            new += (seps[i - 1] if n and i > 0 and i - 1 < len(seps) and keep[n - 1] == i - 1 else (" " if n else "")) + ph[i]
        out.append(h[last:m.start()])
        out.append("" if vide(new) else "<%s%s>%s</%s>" % (m.group(1), m.group(2) or "", new.strip(), m.group(1)))
        last = m.end()
        if ancre[0] is None:
            ancre[0] = sum(len(x) for x in out)
    out.append(h[last:])
    return "".join(out), ancre[0]


def bloc_shabbat(lang, slug, gid, multi):
    t = SH[lang]
    if slug in LYON:
        vil = t["vil"].format(LYON_NOM[lang])
    elif multi:
        vil = MULTI_NOM[lang]
    else:
        vil = t["vil"].format(PLACES[slug][1][lang])
    if slug in LYON:
        corps = REPLI[lang]
    elif multi:
        corps = NOTE[lang]
    else:
        corps = REPLI_ST[lang].format(PLACES[slug][1][lang])
    tete = ('<section class="ss wrap shabbat-bloc"><div class="shabbat" id="shabbat">'
            '<div class="sh-tete"><div><p class="sh-sur">%s</p><p class="sh-gros"><span class="sh-tt">%s</span><br><span class="sh-ville">%s</span></p></div>'
            '<img class="sh-des" src="/img/des/_shabbat-tete.webp" alt="" width="360" height="187" loading="lazy"></div>') % (t["sur"], t["mot"], vil)
    if multi:
        corps_html = tableau_stations(lang)
    else:
        corps_html = ('<div class="sh-moments" hidden>'
                      '<div class="sh-moment" id="m-entree">%s<div><span class="sh-d"></span><b></b><span>%s</span></div></div>'
                      '<div class="sh-moment" id="m-sortie">%s<div><span class="sh-d"></span><b></b><span>%s</span></div></div></div>'
                      ) % (SVG_ENTREE, t["cand"], SVG_SORTIE, t["hav"])
    return tete + corps_html + '<p class="shabbat-corps">%s</p></div>\n%s</section>\n' % (corps, script_shabbat(lang, slug, multi))


def encadre(h, lang, slug, ancre):
    if slug in LYON:
        gid, multi = LYON_GID, False
    elif slug in PLACES:
        gid, multi = PLACES[slug][0], slug in MULTI
    else:
        return h
    bloc = bloc_shabbat(lang, slug, gid, multi)
    rx = re.compile(r'<section class="ss wrap(?: shabbat-bloc)?"><div class="shabbat" id="shabbat">.*?</section>\n?', re.S)   # aussi l'ancien encadre des pages de Lyon (15/10)
    if 'id="shabbat"' in h:
        return rx.sub(lambda m: bloc, h, count=1)
    if ancre:
        i = fin_section(h, ancre)
        return h[:i] + "\n" + bloc + h[i:]
    i = h.index('<section class="ss wrap faq">')
    return h[:i] + bloc + h[i:]


# ---------------------------------------------------------------- 2. Beth Habad : minyan public et repas livres
MINYAN = {
    "en": dict(h2="A minyan in the <i>resort</i>", p="Shabbat and weekday prayers with the Beth Habad of the Alps: tell them your dates.",
               b="Minyan: WhatsApp the Beth Habad", h3="Kosher meals delivered",
               p2="Kosher meals brought to your accommodation in the resort, ordered through the Beth Habad of the Alps. Give them your dates and the number of people.",
               b2="Kosher meals delivered: WhatsApp the Beth Habad",
               m="Hello, we would like to join a minyan in the Alps. Resort: {} / Dates: / Number of people:",
               m2="Hello, we are in the Alps and would like kosher meals delivered. Resort: {} / Dates: / Number of people:"),
    "fr": dict(h2="Un minyan en <i>station</i>", p="Prières de Shabbat et de semaine avec le Beth Habad des Alpes : indiquez-leur vos dates.",
               b="Minyan : écrire au Beth Habad sur WhatsApp", h3="Repas casher livrés",
               p2="Des repas casher livrés à votre hébergement en station, commandés auprès du Beth Habad des Alpes. Indiquez-leur vos dates et le nombre de personnes.",
               b2="Repas casher livrés : écrire au Beth Habad sur WhatsApp",
               m="Bonjour, nous aimerions participer à un minyan dans les Alpes. Station : {} / Dates : / Nombre de personnes :",
               m2="Bonjour, nous sommes dans les Alpes et aimerions des repas casher livrés. Station : {} / Dates : / Nombre de personnes :"),
    "es": dict(h2="Un minián en la <i>estación</i>", p="Oraciones de Shabat y de entre semana con el Beth Habad de los Alpes: indíqueles sus fechas.",
               b="Minián: escribir al Beth Habad por WhatsApp", h3="Comidas kosher a domicilio",
               p2="Comidas kosher entregadas en su alojamiento en la estación, encargadas al Beth Habad de los Alpes. Indíqueles sus fechas y el número de personas.",
               b2="Comidas kosher a domicilio: escribir al Beth Habad por WhatsApp",
               m="Hola, nos gustaría participar en un minián en los Alpes. Estación: {} / Fechas: / Número de personas:",
               m2="Hola, estamos en los Alpes y nos gustaría que nos entregaran comidas kosher. Estación: {} / Fechas: / Número de personas:"),
    "he": dict(h2="מניין <i>באתר</i>", p="תפילות שבת וימי חול עם בית חב״ד באלפים: מסרו להם את התאריכים.",
               b="מניין: כתבו לבית חב״ד בוואטסאפ", h3="ארוחות כשרות במשלוח",
               p2="ארוחות כשרות מגיעות אל מקום הלינה שלכם באתר, בהזמנה דרך בית חב״ד באלפים. מסרו להם את התאריכים ואת מספר האנשים.",
               b2="ארוחות כשרות במשלוח: כתבו לבית חב״ד בוואטסאפ",
               m="שלום, נשמח להצטרף למניין באלפים. אתר: {} / תאריכים: / מספר אנשים:",
               m2="שלום, אנחנו באלפים ונשמח לקבל ארוחות כשרות במשלוח. אתר: {} / תאריכים: / מספר אנשים:"),
}
PAGES_BH = {"alps", "kosher-services-french-alps", "kosher-ski-holidays-french-alps", "kosher-vacation-french-alps",
            "lyon-gateway-to-the-alps-kosher", "summer-in-the-alps-jewish-families", "kosher-chalet-les-deux-alpes"} | {
    s for s in PLACES if s not in MULTI}
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg>'


def bloc_minyan(h, lang, slug):
    if 'class="ss wrap minyan-bh"' in h:
        return h
    t = MINYAN[lang]
    lieu = PLACES[slug][1][lang] if slug in PLACES and slug not in MULTI else ""
    url = lambda m: "https://wa.me/%s?text=%s" % (WA_BH, urllib.parse.quote(m.format(lieu).replace(" Station : / ", " ").replace(" Resort: / ", " ")
                                                                           if not lieu else m.format(lieu), safe=""))
    btn = lambda href, txt: '<p class="cta-hero cta-bh"><a class="btn-noir" href="%s" rel="noopener">%s%s</a></p>' % (href, WA_SVG, txt)
    meals = slug != "kosher-services-french-alps"  # la page services a deja son bouton repas vers le Beth Habad
    b = ('<section class="ss wrap minyan-bh"><div class="minyan-corps"><h2>%s</h2><p>%s</p>%s'
         % (t["h2"], t["p"], btn(url(t["m"]), t["b"])))
    if meals:
        b += '<h3>%s</h3><p>%s</p>%s' % (t["h3"], t["p2"], btn(url(t["m2"]), t["b2"]))
    b += "</div></section>\n"
    i = h.index('<section class="ss wrap faq">')
    return h[:i] + b + h[i:]


# ---------------------------------------------------------------- orchestration
def traiter(path):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    slug = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    h0 = io.open(p, encoding="utf-8").read()
    h = sans_numeros(h0, lang)
    if slug in ("kosher-les-deux-alpes", "kosher-chalet-les-deux-alpes"):
        h = sans_grenoble(h)
    if slug != "privacy":
        h, ancre = sans_hebcal(h, slug)
        if slug in PLACES or slug in LYON:
            h = encadre(h, lang, slug, ancre)
    if slug in PAGES_BH:
        h = bloc_minyan(h, lang, slug)
    if h != h0:
        io.open(p, "w", encoding="utf-8", newline="\n").write(h)
        return 1
    return 0


if __name__ == "__main__":
    poser_css_et_dessin()
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    n = sum(traiter(p) for p in pages)
    t = io.open("llms.txt", encoding="utf-8").read()
    t2 = re.sub(r"WhatsApp\s*" + NUM, "WhatsApp", t)
    if t2 != t:
        io.open("llms.txt", "w", encoding="utf-8", newline="\n").write(t2)
        n += 1
    print(n, "fichiers modifies sur", len(pages) + 1)
