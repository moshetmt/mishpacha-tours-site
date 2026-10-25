# -*- coding: utf-8 -*-
"""Lot 1 de la refonte luxe (décisions Moshé du 25/10) : un seul univers (ivoire, encre, or champagne), rectangles,
capitales espacées sur les boutons, fin de l'italique de titre, barre basse WhatsApp | Plan your trip sur téléphone
(remplace les deux boutons flottants), bandeau cookies en une ligne, Clarity derrière le consentement.
Bloc ===LUXE=== en FIN de styles.css (après tout le reste, il doit gagner), bloc ===LUXE=== en fin de js/anim.js,
bloc ===LUXE=== dans js/mesure.js. Idempotent. `--strip` retire tout. À lancer EN DERNIER de la chaîne."""
import io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STRIP = "--strip" in sys.argv
D, F = "/* ===LUXE=== */", "/* ===/LUXE=== */"
CLARITY_ID = ""  # identifiant du projet Clarity (clarity.microsoft.com), vide = rien ne se charge

def lire(p): return io.open(p, encoding="utf-8", newline="").read()
def ecrire(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def sans(s): return re.sub(re.escape(D) + r".*?" + re.escape(F) + r"\n?", "", s, flags=re.S)

# 1. CSS
css = sans(lire("styles.css"))
# Sélecteurs qui portent un rayon (hors 50 %) : on les repasse tous à 0, sans toucher aux ronds.
sels = []
for m in re.finditer(r"([^{}]+)\{([^{}]*border-radius:(?!50%)[^;}]+[^{}]*)\}", css):
    sel = " ".join(m.group(1).split())
    if sel.startswith("@") or sel in sels: continue
    sels.append(sel)
rayons = ",\n".join(sels)
BLOC = f"""
/* Tokens : un seul univers. */
:root{{--creme:#FAF7F0;--beige:#FAF7F0;--rose:#FAF7F0;--jaune:#C9A961;--vert:#141416;--vert-c:#141416;--encre:#141416;--rouge:#141416;--ecart:64px}}
@media (min-width:900px){{:root{{--ecart:120px}}}}
h1 i,h2 i,h3 i{{font-style:normal}}
/* Rectangles partout (les ronds à 50 % ne sont pas touchés). */
{rayons}{{border-radius:0}}
/* Boutons : capitales espacées, 48 px. */
.btn-noir,.btn-hero,.cta-hero,.cta-pratique,.cta-etapes,.nav .liens a.nav-cta,.panneau nav a.nav-cta,.pill-noir,.cb button,.demande button,.lead-final button,.lead-plan a,form button{{font-family:'Heebo',sans-serif;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;min-height:48px}}
.panneau nav a.nav-cta{{font-size:13px;padding:0 24px;min-height:56px}}
.nav .liens a{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:500}}
.nav .liens a.nav-cta{{background:transparent;border:1px solid var(--encre);color:var(--encre)}}
.nav .burger{{background:transparent;border:0}}
/* Langues en codes, plus de drapeaux (règle n° 1 : jamais le drapeau). */
.langue img{{display:none}}.langue .code{{display:inline}}
.langue summary{{background:transparent;border:1px solid var(--encre);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:500}}
.langue ul{{box-shadow:none;border:1px solid var(--encre)}}
/* Bande du haut et pied : encre. */
.strip{{background:var(--encre)}}
/* Bandeau cookies : une ligne, sans ombre, au-dessus de la barre basse. */
.cb{{left:0;right:0;bottom:0;max-width:none;border:0;border-top:1px solid rgba(20,20,22,.15);box-shadow:none;padding:8px 16px;font-size:12px;line-height:1.35;gap:6px 12px;flex-wrap:nowrap}}
.cb button{{min-width:0;min-height:32px;padding:0 10px;font-size:10px;letter-spacing:.1em}}
.cb-b{{display:flex;gap:6px;flex:none}}
@media (max-width:899px){{.cb{{bottom:56px}}.cb-b{{width:auto}}.cb p{{flex:1 1 auto;min-width:0}}}}
/* Menu plein écran (lot 2) : cinq entrées, sous-titre, bouton, contact, langues. */
.panneau{{background:var(--creme);padding:16px var(--pad) 32px;display:flex;flex-direction:column}}
.panneau[hidden]{{display:none}}
.panneau nav a{{font-size:32px;line-height:1.15;padding:14px 0;border-bottom:1px solid #E2DCCF}}
.panneau nav a small{{display:block;font-family:'Heebo',sans-serif;font-size:13px;font-weight:300;color:#6E6A62;letter-spacing:0;text-transform:none;margin-top:2px}}
.panneau nav a.nav-cta{{margin-top:28px;border:0;background:var(--jaune);color:var(--encre)}}
.panneau nav a.nav-cta-wa{{margin-top:10px;background:var(--encre);color:var(--creme)}}
.panneau-wa{{margin-top:24px;font-size:15px;font-weight:400}}
.panneau-wa svg{{width:20px;height:20px;fill:var(--encre)}}
.panneau-bas{{margin-top:8px;font-size:14px;color:#6E6A62;line-height:1.7}}
.panneau-bas a{{display:block;color:var(--encre);text-decoration:none}}
.panneau-langs{{display:flex;gap:20px;margin-top:14px;font-size:12px;letter-spacing:.14em;font-weight:500}}
.panneau-langs a{{display:inline;color:#6E6A62}}.panneau-langs a[aria-current]{{color:var(--encre)}}
.panneau-st,.panneau-sec{{display:none}}
.nav .menu{{width:auto;height:38px;padding:0 10px;background:transparent}}
.nav .menu span{{box-shadow:0 -5px 0 var(--encre),0 5px 0 var(--encre)}}
/* Pied : stations en liste texte (maillage). */
.pied-stations summary{{cursor:pointer;font-weight:500}}
.pied-stations p{{columns:2;column-gap:24px;margin-top:8px;font-size:14px;line-height:2}}
@media (min-width:900px){{.pied-stations p{{columns:3}}}}
/* Accueil (lot 3) : la photo, cinq mots, un bouton ; chercheur en barre dessous. */
.ac-hero{{min-height:calc(100svh - 116px);display:flex;align-items:flex-end}}
body:has(.cb) .ac-hero{{min-height:calc(100svh - 190px)}}
@media (min-width:900px){{.ac-hero{{min-height:calc(100vh - 72px)}}}}
.ac-hero > img{{opacity:1}}
.ac-hero::before{{background:linear-gradient(to top,rgba(10,10,12,.62) 0%,rgba(10,10,12,.18) 45%,rgba(10,10,12,0) 70%)}}
.ac-hero .hero-texte{{display:block;width:100%;padding:0 var(--pad) 84px}}
.ac-hero .hero-texte p.hero-sous{{display:block!important;margin-top:12px}}
.ac-hero .btn-hero{{width:auto}}
.ac-hero h1{{font-size:44px;line-height:1.08;max-width:10em}}
.ac-hero h1 i{{display:none}}
.ac-hero .hero-sous{{margin-top:12px;font-size:17px;max-width:22em;color:#F6F1E6}}
.ac-hero .btn-hero{{display:inline-flex;align-items:center;justify-content:center;margin-top:24px;height:48px;padding:0 24px;background:var(--creme);color:var(--encre);border:1px solid var(--creme);text-decoration:none;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500}}
.cherche-bar{{position:relative;z-index:3;margin-top:-56px}}
.cherche-bar .chercheur{{margin:0;padding:0;background:var(--blanc);border:1px solid #E2DCCF;gap:0;grid-template-columns:1fr}}
.cherche-bar .chercheur > label,.cherche-bar .chercheur .duo label{{border:0;border-bottom:1px solid #E2DCCF;padding:10px 16px;min-height:56px}}
.cherche-bar .chercheur .duo{{gap:0;grid-template-columns:1fr 1fr}}
.cherche-bar .chercheur .duo label:first-child{{border-right:1px solid #E2DCCF}}
.cherche-bar .chercheur label span{{font-size:10px;letter-spacing:.14em;color:#6E6A62;font-weight:500}}
.cherche-bar .chercheur button{{min-height:56px;border:0;background:var(--encre);color:var(--creme)}}
.cherche-bar .chercheur button svg{{display:none}}
.cherche-bar .chercheur small{{padding:10px 0;color:#6E6A62}}
@media (min-width:900px){{
  .ac-hero h1{{font-size:72px;max-width:12em}}
  .ac-hero .hero-texte{{padding:0 var(--pad) 120px}}
  .ac-hero .hero-sous{{font-size:20px}}
  .cherche-bar{{margin-top:-72px;max-width:1100px}}
  .cherche-bar .chercheur{{grid-template-columns:1.2fr 1.6fr 1.2fr 220px;align-items:stretch}}
  .cherche-bar .chercheur > label,.cherche-bar .chercheur .duo label{{border-bottom:0;border-right:1px solid #E2DCCF;min-height:72px}}
  .cherche-bar .chercheur .duo label:last-child{{border-right:1px solid #E2DCCF}}
  .cherche-bar .chercheur button{{min-height:72px}}
  .cherche-bar .chercheur small{{grid-column:1/-1;text-align:left;padding:8px 16px}}
}}
/* Accueil : les cinq chalets en rail qui glisse, téléphone et ordinateur (Moshé 25/10). */
#chalet .kwp-cartes.kwp-rail{{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:4px}}
#chalet .kwp-cartes.kwp-rail::-webkit-scrollbar{{display:none}}
#chalet .kwp-cartes.kwp-rail .kwp-carte{{flex:0 0 86%;scroll-snap-align:start;display:flex;flex-direction:column;grid-row:auto}}
#chalet .kwp-cartes.kwp-rail .kwp-corps{{display:block;padding:0 22px 22px}}
@media (min-width:900px){{
  #chalet .kwp-cartes.kwp-rail{{gap:24px;margin:24px calc(-1*var(--pad)) 0;padding:0 var(--pad) 4px;scroll-padding-inline:var(--pad)}}
  #chalet .kwp-cartes.kwp-rail .kwp-carte{{flex:0 0 380px}}
}}
/* Barre basse téléphone : WhatsApp | Plan your trip. */
.barre-basse{{display:none}}
@media (max-width:899px){{
  body{{padding-bottom:56px}}
  .wa-flottant,.pyt-flottant{{display:none!important}}
  .barre-basse{{position:fixed;left:0;right:0;bottom:0;z-index:60;display:grid;grid-template-columns:1fr 1fr;height:56px;border-top:1px solid rgba(255,255,255,.12)}}
  .barre-basse a{{display:flex;align-items:center;justify-content:center;gap:8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;text-decoration:none;overflow:hidden;white-space:nowrap}}
  .barre-basse .bb-wa{{background:var(--encre);color:var(--creme)}}
  .barre-basse .bb-wa svg{{width:20px;height:20px;fill:var(--creme);flex:none}}
  .barre-basse .bb-plan{{background:var(--jaune);color:var(--encre)}}
  body:has(#formDemande) .barre-basse{{display:none}}
}}
"""
if not STRIP: css = css.rstrip("\n") + "\n" + D + BLOC + F + "\n"
ecrire("styles.css", css)

# 2. JS : barre basse construite depuis le bouton WhatsApp et le bouton du menu (langue de la page).
JS = """
(function(){var D=document;if(D.getElementById('formDemande')||D.querySelector('.barre-basse'))return;
var wa=D.querySelector('.wa-flottant'),src=D.querySelector('.nav .liens a.nav-cta')||D.querySelector('.panneau nav a.nav-cta');if(!wa||!src)return;
var b=D.createElement('div');b.className='barre-basse';
var a1=D.createElement('a');a1.className='bb-wa';a1.href=wa.getAttribute('href');a1.rel='noopener';a1.innerHTML=(wa.querySelector('svg')||{outerHTML:''}).outerHTML+'<span>WhatsApp</span>';
var a2=D.createElement('a');a2.className='bb-plan';a2.href=src.getAttribute('href');a2.textContent=src.textContent.trim();
b.appendChild(a1);b.appendChild(a2);D.body.appendChild(b);})();
"""
anim = sans(lire("js/anim.js"))
if not STRIP: anim = anim.rstrip("\n") + "\n" + D + JS + F + "\n"
ecrire("js/anim.js", anim)

# 3. Clarity derrière le consentement (dans charger(), donc après Accept seulement).
mes = sans(lire("js/mesure.js"))
if not STRIP and CLARITY_ID:
    bloc = (D + "\n    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,'clarity','script','" + CLARITY_ID + "');\n    " + F + "\n")
    mes = mes.replace("    document.head.appendChild(s);\n", "    document.head.appendChild(s);\n" + bloc, 1)
ecrire("js/mesure.js", mes)
print("ok", "strip" if STRIP else f"{len(sels)} sélecteurs à rayon remis à 0, clarity={'oui' if CLARITY_ID else 'non'}")
