# -*- coding: utf-8 -*-
"""Lot 3, chalets (retours de Moshé du 05/11, n° 12 à 16), 4 langues. Idempotent : marqueur LOT3-0611 dans le HTML,
bloc /* ===LOT3-0611=== */ dans lv.css. Ne touche ni CACH-0511 ni CARTE-0511.

    python _lot3_0611.py            # applique
    python _lot3_0611.py --etat     # compte seulement

Page /kosher-chalets/ : manifeste « Skiez le jour… » retiré (n° 12), barre de zones + fiches groupées par zone (n° 13),
bandeau Winter Prestige retiré (n° 14), « Comment ça marche » en section noire Vous · Nous · Ensemble (n° 13, 16).
Fiches chalet : « · Certifié cacher » retiré de la ligne du lieu (badge juste au-dessus), « Comment ça marche » au même dessin.
Pages station sans chalet : la liste des 8 chalets devient « nos chalets les plus proches » (2 chalets + lien vers la zone), n° 15.
Pages station avec chalet : rien (elles ne montrent déjà que leurs chalets). Aucune URL ne bouge.
Si _kit_wp.py est relancé un jour, relancer ce script après."""
import glob, io, json, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ETAT = "--etat" in sys.argv
LANGS = (("en", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/"))

# ---------------------------------------------------------------- zones
ZONES = {   # ordre d'affichage ; stations : (slug station, nom par langue)
    "3v": dict(nom={"en": "Les 3 Vallées", "fr": "Les 3 Vallées", "es": "Les 3 Vallées", "he": "<bdi dir=\"ltr\">Les 3 Vallées</bdi>"},
               stations=[("kosher-courchevel", {"en": "Courchevel", "fr": "Courchevel", "es": "Courchevel", "he": "קורשבל"}),
                         ("kosher-val-thorens", {"en": "Val Thorens", "fr": "Val Thorens", "es": "Val Thorens", "he": "ואל טורנס"}),
                         ("kosher-les-menuires", {"en": "Les Ménuires", "fr": "Les Ménuires", "es": "Les Ménuires", "he": "לה מנואר"})]),
    "da": dict(nom={"en": "Les Deux Alpes", "fr": "Les Deux Alpes", "es": "Les Deux Alpes", "he": "לה דז אלפ"},
               stations=[("kosher-les-deux-alpes", {"en": "Les Deux Alpes", "fr": "Les Deux Alpes", "es": "Les Deux Alpes", "he": "לה דז אלפ"}),
                         ("kosher-alpe-dhuez", {"en": "Alpe d'Huez", "fr": "Alpe d'Huez", "es": "Alpe d'Huez", "he": "אלפ ד'הואז"})]),
    "me": dict(nom={"en": "Mont-Blanc", "fr": "Mont-Blanc", "es": "Mont-Blanc", "he": "מון בלאן"},   # 11/11 : « Mont-Blanc » (Megève, Saint-Gervais, Les Houches), ex « Megève »
               stations=[("kosher-megeve", {"en": "Megève", "fr": "Megève", "es": "Megève", "he": "מג'ב"}),
                         ("kosher-chamonix", {"en": "Chamonix", "fr": "Chamonix", "es": "Chamonix", "he": "שמוני"})]),
    "ti": dict(nom={"en": "Tignes, Val d'Isère", "fr": "Tignes, Val d'Isère", "es": "Tignes, Val d'Isère", "he": "טין, ואל ד'יזר"},
               stations=[("kosher-tignes", {"en": "Tignes", "fr": "Tignes", "es": "Tignes", "he": "טין"}),
                         ("kosher-val-disere", {"en": "Val d'Isère", "fr": "Val d'Isère", "es": "Val d'Isère", "he": "ואל ד'יזר"})]),
}
def zone_du_chalet(href):
    s = href.strip("/").split("/")[-1]
    if "tignes" in s: return "ti"
    if "deux-alpes" in s: return "da"
    if "megeve" in s or "saint-gervais" in s or "les-houches" in s: return "me"
    if "courchevel" in s or "val-thorens" in s or "menuires" in s: return "3v"
    return None

T = {
    "en": dict(tous="All", zones="Chalets by area", stations="Resorts:", vous="You", nous="We", ens="Together",
               proches="Our nearest chalets", loin="Our kosher chalets in the French Alps", tousz="All our chalets, by area"),
    "fr": dict(tous="Tous", zones="Chalets par zone", stations="Stations :", vous="Vous", nous="Nous", ens="Ensemble",
               proches="Nos chalets les plus proches", loin="Nos chalets casher dans les Alpes françaises", tousz="Tous nos chalets, par zone"),
    "es": dict(tous="Todos", zones="Chalés por zona", stations="Estaciones:", vous="Usted", nous="Nosotros", ens="Juntos",
               proches="Nuestros chalés más cercanos", loin="Nuestros chalés kosher en los Alpes franceses", tousz="Todos nuestros chalés, por zona"),
    "he": dict(tous="הכל", zones="צ'אלות לפי אזור", stations="אתרים:", vous="אתם", nous="אנחנו", ens="יחד",
               proches="הצ'אלות הקרובות ביותר שלנו", loin="הצ'אלות הכשרות שלנו באלפים הצרפתיים", tousz="כל הצ'אלות שלנו, לפי אזור"),
}
# intro ES : comptait les chalets (« dos en Les Deux Alpes, uno en… »), règle « jamais le nombre de chalets »
INTRO_ES = "Nuestros chalés, con todo lo kosher resuelto: Les Deux Alpes, Courchevel, cerca de Megève y Val Thorens."

# stations sans chalet : (zone de la page des chalets ou None, [chalets à montrer, par slug])
PROCHES = {
    "kosher-alpe-dhuez": ("da", ["kosher-chalet-les-deux-alpes", "kosher-slope-chalet-les-deux-alpes"]),
    "kosher-grenoble": ("da", ["kosher-chalet-les-deux-alpes", "kosher-slope-chalet-les-deux-alpes"]),
    "kosher-val-disere": ("3v", ["kosher-chalet-val-thorens", "kosher-chalet-les-menuires"]),
    "kosher-les-arcs": ("3v", ["kosher-chalet-courchevel", "kosher-chalet-les-menuires"]),
    "kosher-la-plagne": ("3v", ["kosher-chalet-courchevel", "kosher-chalet-les-menuires"]),
    "kosher-chamonix": ("me", ["kosher-chalet-megeve", "kosher-chalet-courchevel"]),
    "kosher-annecy": ("me", ["kosher-chalet-megeve", "kosher-chalet-courchevel"]),
}
LOIN = ["kosher-chalet-megeve", "kosher-chalet-courchevel"]   # Suisse, Italie, ailleurs : pas de « plus proche » honnête

SRC_MINI = "_lot3_mini_src.json"   # vignettes kwp-v d'origine, par langue, relevées à la première passe

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def pfx(lang): return "" if lang == "en" else "/" + lang

def cm(lang, items, noir):
    """items = [(titre, texte)] ×3 → Vous · Nous · Ensemble"""
    t = T[lang]; k = (t["vous"], t["nous"], t["ens"]); cls = ("l3-cm-vous", "l3-cm-nous", "l3-cm-fin")
    return ('<div class="l3-cm' + (" l3-cm-noir" if noir else "") + '">' +
            "".join(f'<div class="l3-cm-c {c}"><span class="l3-cm-k">{kk}</span><h3>{a}</h3><p>{b}</p></div>' for c, kk, (a, b) in zip(cls, k, items)) + "</div>")

# ---------------------------------------------------------------- CSS
CSS = r"""/* ===LOT3-0611=== lot 3 chalets (_lot3_0611.py, 06/11) : zones, « Comment ça marche » Vous · Nous · Ensemble, chalets proches */
.l3-chips{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px 0 14px;margin:0 0 6px;-webkit-overflow-scrolling:touch}
.l3-chips::-webkit-scrollbar{display:none}
.l3-chips{-webkit-mask-image:linear-gradient(to right,#000 calc(100% - 36px),transparent);mask-image:linear-gradient(to right,#000 calc(100% - 36px),transparent)}
html[dir=rtl] .l3-chips{-webkit-mask-image:linear-gradient(to left,#000 calc(100% - 36px),transparent);mask-image:linear-gradient(to left,#000 calc(100% - 36px),transparent)}
@media (min-width:600px){.l3-chips,html[dir=rtl] .l3-chips{-webkit-mask-image:none;mask-image:none}}
html body.lv .l3-chip{flex:none;display:inline-flex;align-items:center;height:40px;padding:0 16px;border:1px solid #111111;border-radius:4px;background:#FFFFFF;color:#111111;font-family:var(--lv-sans,Jost,sans-serif);font-weight:500;font-size:11px;line-height:1;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;transition:transform 160ms cubic-bezier(.23,1,.32,1),background-color 160ms ease,color 160ms ease,border-color 160ms ease}
html body.lv .l3-chip:active{transform:scale(.97)}
html body.lv .l3-chip.is-on{background:#111111;color:#FFFFFF}
@media (hover:hover) and (pointer:fine){html body.lv .l3-chip:not(.is-on):hover{border-color:#7A6440;color:#7A6440}}
html[dir=rtl] body.lv .l3-chip{letter-spacing:0;font-size:14px}
.l3-zone{padding-top:26px;scroll-margin-top:96px}
.l3-zone+.l3-zone{margin-top:44px;border-top:1px solid #E6E6E6}
.l3-zone-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 18px;margin:0 0 18px}
.l3-zone-t h2{margin:0}
html body.lv .l3-zone-t p{margin:0;font-size:13px;letter-spacing:.04em;color:#4A4A4A}
html body.lv .l3-zone-t p a{color:#7A6440;text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(122,100,64,.45)}
.l3-hub.is-filtre .l3-zone:not(.is-vu){display:none}
.l3-hub.is-filtre .l3-zone.is-vu{border-top:0;margin-top:0}
.l3-cm{display:grid;grid-template-columns:1fr;row-gap:22px;margin:28px 0 0}
.l3-cm-c{position:relative;padding:18px 0 0;border-top:1px solid #E6E6E6}
.l3-cm-vous{width:88%}
.l3-cm-nous{width:88%;margin-inline-start:auto;padding-inline-start:18px;border-inline-start:1px solid #A88F5E}
.l3-cm-fin{border-top:1px solid #A88F5E;padding-top:22px}
html body.lv .l3-cm-k{display:block;margin:0 0 8px;font-family:var(--lv-sans,Jost,sans-serif);font-size:11px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:#7A6440}
html[dir=rtl] body.lv .l3-cm-k{letter-spacing:0;font-size:13px}
html body.lv .l3-cm h3{margin:0 0 8px;font-family:var(--lv-sans,Jost,sans-serif);font-size:18px;font-weight:400;letter-spacing:.02em;line-height:1.3;text-transform:none;color:#111111}
html body.lv .l3-cm p{margin:0;font-size:15px;line-height:1.55;color:#333333;max-width:none}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm-c{border-top-color:rgba(255,255,255,.24)}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm-nous{border-inline-start-color:#C2A874}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm-fin{border-top-color:#C2A874}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm-k{color:#C2A874 !important;-webkit-text-fill-color:#C2A874 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm h3{color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir .l3-cm p{color:#E6E6E6 !important;-webkit-text-fill-color:#E6E6E6 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir{padding-top:56px !important;padding-bottom:56px !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.l3-noir+div.cta-etapes{padding-top:28px !important}
@media (min-width:800px){
  .l3-cm{grid-template-columns:1fr 1fr;column-gap:56px;row-gap:28px;max-width:1000px;margin-left:auto;margin-right:auto}
  .l3-cm-vous,.l3-cm-nous{width:auto;margin-inline-start:0;padding-inline-start:0;border-inline-start:0}
  .l3-cm-nous::before{content:"";position:absolute;inset-inline-start:-28px;top:18px;bottom:0;border-inline-start:1px solid #A88F5E}
  .l3-noir .l3-cm-nous::before{border-inline-start-color:#C2A874}
  .l3-cm-fin{grid-column:1/-1;text-align:center;padding-top:28px}
  html body.lv .l3-cm-fin h3{font-size:22px;font-weight:300;letter-spacing:.06em;text-transform:uppercase}
  html body.lv .l3-cm-fin p{max-width:58ch;margin-left:auto;margin-right:auto}
}
.l3-proches .kwp-mini-v{margin-top:18px}
html body.lv .l3-tous{margin:18px 0 0;font-size:14px}
html body.lv .l3-tous a{color:#111111;text-decoration:underline;text-underline-offset:3px;text-decoration-color:#A88F5E}
html body.lv .l3-tous a::after{content:"\203A";margin-inline-start:6px;color:#7A6440}
html[dir=rtl] body.lv .l3-tous a::after{content:"\2039"}
@media (prefers-reduced-motion:reduce){html body.lv .l3-chip{transition:background-color 160ms ease,color 160ms ease}}
/* --- v3 luxe (consigne de Moshé du 06/11, 2 h 40 : « ça manque de beauté et de luxe ») : fiches sans cadre ni pictos ni bouton, photos pleine largeur sur téléphone,
   onglets texte au lieu de puces, « Ce que comprend » et FAQ ouverts sans chevron, fiche chalet : accordéons ouverts, bouton catalogue à sa taille, WhatsApp en lien --- */
html body.lv .l3-chips{gap:26px;padding:6px 0 10px;margin:0 0 4px;-webkit-mask-image:none;mask-image:none;flex-wrap:wrap}
html body.lv .l3-chip{height:auto;padding:0 0 7px;border:0;border-bottom:1px solid transparent;border-radius:0;background:transparent;color:#4A4A4A;letter-spacing:.2em;transition:color 160ms ease,border-color 160ms ease}
html body.lv .l3-chip:active{transform:none;color:#111111}
html body.lv .l3-chip.is-on{background:transparent;color:#111111;border-bottom-color:#A88F5E}
@media (hover:hover) and (pointer:fine){html body.lv .l3-chip:not(.is-on):hover{color:#111111;border-color:transparent}}
.l3-zone{padding-top:40px}
.l3-zone+.l3-zone{margin-top:64px;border-top:0}
.l3-zone-t{flex-direction:column;align-items:flex-start;gap:6px;margin:0 0 28px}
html body.lv .l3-zone-t p{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#6B6B6B}
html body.lv .l3-zone-t p a{color:#7A6440;text-decoration-color:rgba(122,100,64,.35)}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-cartes{gap:56px 36px}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-carte{border:0 !important;background:transparent !important;box-shadow:none !important;padding:0 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-photo img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:0 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-corps{padding:0 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-carte{display:block !important;grid-row:auto !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-corps{display:block !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) :is(.kwp-carte h3,.kwp-chiffres,.kwp-prix,.kwp-pied){padding-inline:0 !important;margin-inline:0 !important;text-align:start !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-carte h3{margin:20px 0 0 !important;font-family:var(--lv-sans,Jost,sans-serif) !important;font-size:14px !important;font-weight:400 !important;letter-spacing:.18em !important;text-transform:uppercase !important;line-height:1.5}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-carte h3 a{text-decoration:none !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres{display:block !important;margin:8px 0 0 !important;padding:0 !important;font-size:14px !important;line-height:1.6;letter-spacing:.02em;color:#4A4A4A !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres li{display:inline !important;margin:0 !important;padding:0 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres li+li::before{content:" \00B7 ";color:#A88F5E}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres svg{display:none !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres span{display:inline !important;color:inherit !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres b{display:inline !important;font-weight:400 !important;color:#111111 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-chiffres b::after{content:" "}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) :is(.kwp-lieu,.kwp-dispo,.kwp-casher,.kwp-pied img){display:none !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-prix{margin:10px 0 0 !important;font-size:15px !important;font-weight:300 !important;letter-spacing:.02em;color:#111111 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-pied{display:block !important;margin:14px 0 0 !important;padding:0 !important;border:0 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-pied .btn-noir{display:inline !important;width:auto !important;background:transparent !important;color:#111111 !important;-webkit-text-fill-color:#111111 !important;border:0 !important;border-radius:0 !important;padding:0 0 4px !important;margin:0 !important;font-size:11px !important;letter-spacing:.2em !important;text-transform:uppercase;text-decoration:underline !important;text-underline-offset:6px;text-decoration-color:#A88F5E !important;text-decoration-thickness:1px;box-shadow:none !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-pied .btn-noir::after{content:"\203A";margin-inline-start:8px;color:#7A6440}
html[dir=rtl] body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-pied .btn-noir::after{content:"\2039"}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.kwp-noir :is(.kwp-chiffres,.kwp-chiffres span){color:#D9D9D9 !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.kwp-noir :is(.kwp-chiffres b,.kwp-prix,.kwp-pied .btn-noir){color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important}
html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.kwp-noir .kwp-pied .btn-noir::after,html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main section.kwp-noir .kwp-chiffres li+li::before{color:#C2A874}
@media (max-width:699.98px){
  html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .l3-hub .kwp-photo{width:100vw;margin-inline:calc(50% - 50vw)}
  html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .l3-hub .kwp-cartes{gap:64px}
  html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .l3-hub .kwp-carte{overflow:visible !important}
}
@media (min-width:1000px){html body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) .kwp-cartes.kwp-six{grid-template-columns:repeat(2,minmax(0,1fr));gap:64px 56px}}
/* « Ce que comprend chaque séjour » : ouvert, sans cadre ni chevron (le script mobile-alpes replie les cartes à partir de la 3e) */
html.mob-alpes body.l3-luxe .dk-cartes>li.dk-pli>b{cursor:default;padding-inline-end:0}
html.mob-alpes body.l3-luxe .dk-cartes>li.dk-pli>b::after{display:none}
html.mob-alpes body.l3-luxe .dk-cartes>li.dk-pli:not(.dk-ouvert)>.dk-corps{display:block}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes>li{border:0 !important;padding:0 !important;background:transparent !important;display:block !important;min-height:0 !important}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes{gap:26px 48px !important;margin-top:28px}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes>li>b{display:block;margin:0 0 6px;font-family:var(--lv-sans,Jost,sans-serif);font-size:12px !important;font-weight:400;letter-spacing:.16em;text-transform:uppercase;color:#111111;line-height:1.5}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes>li,html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes>li .dk-corps{font-size:15px;line-height:1.6;color:#4A4A4A}
@media (min-width:700px){html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .beige .dk-cartes{grid-template-columns:repeat(2,minmax(0,1fr)) !important;max-width:900px}}
/* FAQ de la page des chalets : questions ouvertes, sans « + » ni filets */
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq details{border:0 !important;padding:0 !important;margin:0 !important}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq details+details{margin-top:30px !important}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq details:first-of-type{margin-top:28px !important}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq summary{pointer-events:none;cursor:default;padding:0 !important;font-family:var(--lv-sans,Jost,sans-serif);font-size:12px !important;font-weight:400 !important;letter-spacing:.16em;text-transform:uppercase;line-height:1.5;color:#111111}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq summary::after{display:none !important}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .faq details p{padding:8px 0 0 !important;margin:0;font-size:15px;line-height:1.6;color:#4A4A4A;opacity:1 !important;max-width:62ch}
/* fiche chalet : bouton du catalogue à sa taille, WhatsApp en lien, accordéons ouverts en sections */
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-btn.lc-cta{display:inline-flex !important;width:auto !important;padding:15px 26px !important;margin:0 16px 0 0 !important;vertical-align:middle}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-btn.lc-wa{display:inline-flex !important;width:auto !important;background:transparent !important;border:0 !important;padding:15px 0 !important;margin:0 !important;color:#111111 !important;text-decoration:underline !important;text-underline-offset:5px;text-decoration-color:#A88F5E !important;text-decoration-thickness:1px;vertical-align:middle}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-btn.lc-wa:hover{background:transparent !important;color:#7A6440 !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-accordeons{border-top:0 !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc details.lc-plis{border:0 !important;padding:0 0 8px !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc details.lc-plis>summary{pointer-events:none;cursor:default;padding:40px 0 12px !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc details.lc-plis:first-of-type>summary{padding-top:8px !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc details.lc-plis>summary::after{display:none !important}
html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-t{font-size:12px !important;font-weight:400 !important;letter-spacing:.2em !important;text-transform:uppercase !important;line-height:1.5 !important}
html[dir=rtl] body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main.lc .lc-t,html[dir=rtl] body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.faq summary,.beige .dk-cartes>li>b),html[dir=rtl] body.valora.lv.wp-nav:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main :is(.l3-hub,section.kwp-noir) :is(.kwp-carte h3,.kwp-pied .btn-noir){letter-spacing:0 !important;font-size:15px !important}
/* stations : vignettes des chalets proches sans cadre */
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .l3-proches .kwp-v{border:0 !important;gap:18px}
html body.lv.l3-luxe:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12) main .l3-proches .kwp-v b{font-weight:400;font-size:15px;letter-spacing:.04em}
/* ===/LOT3-0611=== */
"""
JS = ("<script>(function(){var h=document.querySelector('.l3-hub');if(!h)return;var cs=h.querySelectorAll('.l3-chip');"
      "function on(z){h.classList.toggle('is-filtre',!!z);h.querySelectorAll('.l3-zone').forEach(function(g){g.classList.toggle('is-vu',!z||g.getAttribute('data-zone')===z)});"
      "cs.forEach(function(c){c.classList.toggle('is-on',(c.getAttribute('data-zone')||'')===(z||''))})}"
      "cs.forEach(function(c){c.addEventListener('click',function(e){e.preventDefault();on(c.getAttribute('data-zone')||'');"
      "try{history.replaceState(null,'',c.getAttribute('href'))}catch(x){}})});"
      "var z=location.hash.replace('#zone-','');if(z&&h.querySelector('.l3-zone[data-zone=\"'+z+'\"]'))on(z)})();</script>")

def css():
    p = "lv.css"; s = rd(p)
    bloc = CSS.strip("\n") + "\n"
    n = re.sub(r"/\* ===LOT3-0611===.*?/\* ===/LOT3-0611=== \*/\n", lambda m: bloc, s, count=1, flags=re.S)
    if n == s and "===LOT3-0611===" not in s: n = s.rstrip("\n") + "\n\n" + bloc
    if n != s and not ETAT: wr(p, n)
    return n != s

# ---------------------------------------------------------------- page des chalets
def hub(lang, pf):
    p = f"{pf}kosher-chalets/index.html"; s = rd(p); o = s; t = T[lang]
    # n° 12 : manifeste retiré, intro ES sans compte
    s = re.sub(r'\n?<section class="clair ss wrap lead-intro">[\s\S]*?</section>', "", s, count=1)
    if lang == "es": s = re.sub(r'(<div class="bn-intro wrap"><p>)[^<]*(</p></div>)', lambda m: m.group(1) + INTRO_ES + m.group(2), s, count=1)
    # n° 13 et 14 : section des cartes regroupée par zone, bandeau WP retiré
    i = s.find('<section class="ss wrap kwp kwp-hub'); j = s.find("</section>", i)
    assert i > 0 and j > i, p
    sec = s[i:j]
    cartes = re.findall(r'<article class="kwp-carte[^"]*">[\s\S]*?</article>', sec)
    groupes = {}
    for c in cartes:
        href = re.search(r'<h3><a href="([^"]*)"', c).group(1)
        groupes.setdefault(zone_du_chalet(href), []).append(c)
    sans = groupes.pop(None, [])
    chips = f'<a class="l3-chip is-on" href="#chalets" data-zone="">{t["tous"]}</a>' + "".join(
        f'<a class="l3-chip" href="#zone-{z}" data-zone="{z}">{ZONES[z]["nom"][lang]}</a>' for z in ZONES if z in groupes)
    blocs = ""
    for z in ZONES:
        if z not in groupes: continue
        liens = " · ".join(f'<a href="{pfx(lang)}/{slug}/">{nom[lang]}</a>' for slug, nom in ZONES[z]["stations"] if os.path.exists(f"{pf}{slug}/index.html"))
        blocs += (f'<div class="l3-zone is-vu" id="zone-{z}" data-zone="{z}"><div class="l3-zone-t"><h2>{ZONES[z]["nom"][lang]}</h2>'
                  f'<p>{t["stations"]} {liens}</p></div><div class="kwp-cartes kwp-six">{"".join(groupes[z])}</div></div>')
    if sans: blocs += f'<div class="l3-zone is-vu" data-zone="autres"><div class="kwp-cartes kwp-six">{"".join(sans)}</div></div>'
    neuf = (f'<section class="ss wrap kwp kwp-hub l3-hub" id="chalets"><!--LOT3-0611--><nav class="l3-chips" aria-label="{t["zones"]}">{chips}</nav>'
            f'{blocs}{JS}<!--/LOT3-0611-->')
    s = s[:i] + neuf + s[j:]
    # n° 13 (page blanche) et n° 16 : « Comment ça marche » en section noire, Vous · Nous · Ensemble
    m = re.search(r'<section class="ss wrap etapes(?: kwp-noir l3-noir)?"><h2>(.*?)</h2>(?:<ol>([\s\S]*?)</ol>|<div class="l3-cm[\s\S]*?</div></div>)</section>', s)
    assert m, p + " etapes"
    if m.group(2):
        items = [(re.search(r"<h3>(.*?)</h3>", li).group(1), re.search(r"<p>(.*?)</p>", li).group(1))
                 for li in re.findall(r"<li>[\s\S]*?</li>", m.group(2))]
        assert len(items) == 3, p
        s = s.replace(m.group(0), f'<section class="ss wrap etapes kwp-noir l3-noir"><h2>{m.group(1)}</h2>{cm(lang, items, True)}</section>', 1)
    if s != o and not ETAT: wr(p, s)
    return s != o

# ---------------------------------------------------------------- fiches chalet
def fiche(lang, pf, p):
    s = rd(p); o = s
    s = re.sub(r'<span class="cach-ref">[^<]*</span>', "", s)   # « · Certifié cacher » : le badge est juste au-dessus
    m = re.search(r'<ol class="lc-et">([\s\S]*?)</ol>', s)
    if m:
        items = []
        for li in re.findall(r"<li>([\s\S]*?)</li>", m.group(1)):
            b = re.match(r"<b>(.*?)</b>\s*([\s\S]*)", li); items.append((b.group(1), b.group(2).strip()))
        if len(items) == 3: s = s.replace(m.group(0), "<!--LOT3-0611-->" + cm(lang, items, False), 1)
    if s != o and not ETAT: wr(p, s)
    return s != o

# ---------------------------------------------------------------- stations sans chalet
def vignettes_src():
    src = json.load(io.open(SRC_MINI, encoding="utf-8")) if os.path.exists(SRC_MINI) else {}
    changed = False
    for lang, pf in LANGS:
        if lang in src and len(src[lang]) >= 8: continue
        for p in glob.glob(f"{pf}kosher-*/index.html"):
            s = rd(p)
            m = re.search(r"<!--KIT-WP:mini-->([\s\S]*?)<!--/KIT-WP:mini-->", s)
            if not m or "LOT3-0611" in m.group(1): continue
            vs = re.findall(r'<a class="kwp-v" href="([^"]*)">[\s\S]*?</a>', m.group(1))
            if len(vs) >= 8:
                src[lang] = {href.strip("/").split("/")[-1]: html for href, html in
                             zip(vs, re.findall(r'<a class="kwp-v" href="[^"]*">[\s\S]*?</a>', m.group(1)))}
                changed = True; break
    if changed and not ETAT: io.open(SRC_MINI, "w", encoding="utf-8").write(json.dumps(src, ensure_ascii=False, indent=0))
    return src

def station(lang, pf, p, src):
    slug = p.replace("\\", "/").split("/")[-2]
    s = rd(p); o = s; t = T[lang]
    m = re.search(r"<!--KIT-WP:mini-->[\s\S]*?<!--/KIT-WP:mini-->", s)
    if not m or lang not in src: return False
    zone, chalets = PROCHES.get(slug, (None, LOIN))
    titre = t["proches"] if slug in PROCHES else t["loin"]
    vs = "".join(src[lang][c] for c in chalets if c in src[lang])
    if not vs: return False
    lien = f'{pfx(lang)}/kosher-chalets/' + (f"#zone-{zone}" if zone else "#chalets")
    neuf = (f'<!--KIT-WP:mini--><section class="ss wrap kwp kwp-mini l3-proches"><!--LOT3-0611--><h2>{titre}</h2><div class="kwp-mini-v">{vs}</div>'
            f'<p class="l3-tous"><a href="{lien}">{t["tousz"]}</a></p></section><!--/KIT-WP:mini-->')
    s = s.replace(m.group(0), neuf, 1)
    if s != o and not ETAT: wr(p, s)
    return s != o

# ---------------------------------------------------------------- v3 luxe (06/11, 2 h 40)
def luxe(p):
    """classe body l3-luxe ; page des chalets : FAQ ouverte ; fiche chalet : accordéons ouverts. Idempotent."""
    s = rd(p); o = s
    if "l3-luxe" not in s.split("<main", 1)[0]:
        s = re.sub(r'<body class="', '<body class="l3-luxe ', s, count=1) if '<body class="' in s else s.replace("<body", '<body class="l3-luxe"', 1)
    if p.replace("\\", "/").endswith("kosher-chalets/index.html"):   # glob rend des antislashs sous Windows
        s = re.sub(r'(<section class="clair[^"]*faq[^"]*">)([\s\S]*?)(</section>)',
                   lambda m: m.group(1) + m.group(2).replace("<details>", "<details open>") + m.group(3), s, count=1)
    s = s.replace('<details class="lc-plis">', '<details class="lc-plis" open>')
    # fiche : les photos avant les textes (blocs de texte sans photo = ce qui tue le luxe)
    a = s.find('<div class="lc-bas-photos">'); b = s.find('<div class="lc-bas-autres">'); c = s.find('<div class="lc-bas">')
    if 0 < c < a < b and '<div class="lc-bas">\n  <div class="lc-bas-photos">' not in s:
        bloc = s[a:b]
        s = s[:a] + s[b:]
        s = s.replace('<div class="lc-bas">', '<div class="lc-bas">\n  ' + bloc.rstrip() + "\n", 1)
    if s != o and not ETAT: wr(p, s)
    return s != o

# ---------------------------------------------------------------- main
n = {"css": css(), "hub": 0, "fiches": 0, "stations": 0}
src = vignettes_src()
for lang, pf in LANGS:
    n["hub"] += hub(lang, pf)
    for p in glob.glob(f"{pf}kosher-*chalet*/index.html"):
        if p.endswith("kosher-chalets/index.html"): continue
        n["fiches"] += fiche(lang, pf, p)
    for p in glob.glob(f"{pf}kosher-*/index.html"):
        if "chalet" in p: continue
        n["stations"] += station(lang, pf, p, src)
    n["luxe"] = n.get("luxe", 0) + sum(luxe(p) for p in glob.glob(f"{pf}kosher-*/index.html"))
print(("état :" if ETAT else "modifié :"), n)
