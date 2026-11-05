# -*- coding: utf-8 -*-
"""Bannières des pages à photo ou vidéo sur le modèle de l'accueil validé le 02/11 (« je valide, on peut appliquer à toutes les pages »),
retours de Moshé du 05/11 : « la bannière ne ressemble pas à celle de l'accueil, trop sombre, pas la bonne taille, trou blanc ».

    python _bannieres_accueil.py --pages kosher-courchevel,kosher-chalets,chabad-lyon,jewish-lyon-tours,kosher-van-transfers   # échantillon
    python _bannieres_accueil.py --tout                                                                                         # après le oui de Moshé

Sur chaque page traitée (classe body « bn ») :
 - bannière plein écran du téléphone (100svh), texte court centré en bas comme l'accueil (surtitre, titre, sous-titre en capitales, réassurance, bouton) ;
 - fil d'Ariane sorti de la bannière, posé sous elle sur fond blanc (comme les fiches chalet) ;
 - voile de l'accueil renforcé juste ce qu'il faut pour 4,5:1 sur la pire image (contrôle E:/taches/contraste_bn.py) ;
 - grand logo WP de la bannière retiré (l'en-tête le porte déjà, comme sur les stations) ;
 - page du van : l'illustration dorée (texte blanc illisible dessus) remplacée par une photo des Alpes.
Partout (sans classe) : sceau « Strictly kosher » des cartes chalet posé dans la photo comme sur l'accueil (il débordait de 26 px et se voyait coupé).
L'accueil n'est pas touché. Idempotent (marqueur BN-0511)."""
import re, glob, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FAMILLES = ("hero ac-hero lv-hero-station", "hero lead-hero3", "hero lead-hero3 lead-hero3-illus", "lv-hero-photo", "hero")
VAN_PHOTO = '<img alt="" fetchpriority="high" src="/img/h/st-val-thorens-960.webp" srcset="/img/h/st-val-thorens-640.webp 640w, /img/h/st-val-thorens-960.webp 960w, /img/h/st-val-thorens-1600.webp 1600w" sizes="100vw" width="1600" height="1067" class="bn-photo">'

def pages():
    if "--tout" in sys.argv:
        return sorted(f.replace("\\", "/") for f in glob.glob("**/index.html", recursive=True))
    i = sys.argv.index("--pages"); noms = sys.argv[i + 1].split(",")
    return [f"{pf}{n}/index.html" for n in noms for pf in ("", "fr/", "es/", "he/") if os.path.exists(f"{pf}{n}/index.html")]

n = 0
for f in pages():
    if f in ("index.html", "fr/index.html", "es/index.html", "he/index.html"): continue   # accueil validé : on n'y touche pas
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<main[^>]*>\s*<section class="([^"]*)"[^>]*>', s)
    if not m or m.group(1) not in FAMILLES or "BN-0511" in s: continue
    o = s
    s = re.sub(r'<body class="', '<body class="bn ', s, count=1) if re.search(r'<body class="', s) else s.replace("<body", '<body class="bn"', 1)
    i0 = m.start(1) - len('<section class="'); j0 = s.find("</section>", i0)
    hero = s[i0:j0]
    fil = re.search(r'<p class="fil[^"]*">.*?</p>', hero, re.S)
    if fil:
        hero = hero.replace(fil.group(0), "", 1)
        apres = f'<!--BN-0511--><div class="bn-fil wrap">{fil.group(0)}</div>'
    else:
        apres = "<!--BN-0511-->"
    if "lead-hero3-illus" in m.group(1):
        hero = re.sub(r'<img alt="" fetchpriority="high" src="/img/illus/or/van\.webp"[^>]*>', VAN_PHOTO, hero, count=1)
    s = s[:i0] + hero + "</section>" + apres + s[j0 + len("</section>"):]
    if s != o: open(f, "w", encoding="utf-8").write(s); n += 1
print("pages passées au modèle de l'accueil :", n)

P = "html body.lv.bn" + "".join(f":not(#b{i})" for i in range(1, 13))
H = f"{P} main>section:is(.lv-hero-station,.lead-hero3,.lv-hero-photo,.hero)"
VOILE = "linear-gradient(180deg,rgba(0,0,0,.30) 0,rgba(0,0,0,0) 120px),linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 34%,rgba(0,0,0,.30) 52%,rgba(0,0,0,.58) 72%,rgba(0,0,0,.66) 100%)"
CSS = f"""/* ===BN-0511=== bannières au modèle de l'accueil (_bannieres_accueil.py) */
html body.lv:not(#b1):not(#b2):not(#b3):not(#b4):not(#b5):not(#b6):not(#b7):not(#b8):not(#b9) .kwp-photo .kwp-seau{{bottom:12px !important;right:12px !important;width:64px !important;height:64px !important}}
{H}{{position:relative !important;height:100svh !important;min-height:560px !important;max-height:none !important;padding:0 !important;margin:0 !important;display:flex !important;flex-direction:column !important;justify-content:flex-end !important;align-items:center !important;overflow:hidden !important;background:#111111 !important;border:0 !important}}
{H}>:is(img,video,picture),{H} .lead3-photo,{H} img.bn-photo{{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;max-width:none !important;object-fit:cover !important;filter:none !important;border-radius:0 !important;z-index:0 !important;opacity:1 !important;transform:none !important}}
{H}::before{{content:"" !important;position:absolute !important;inset:0 !important;z-index:1 !important;pointer-events:none;background:{VOILE} !important;opacity:1 !important}}
{H}::after{{display:none !important}}
{H} :is(.hero-texte,.lead3-texte){{position:relative !important;z-index:2 !important;width:100% !important;max-width:720px !important;margin:0 auto !important;padding:0 24px 48px !important;text-align:center !important;box-sizing:border-box;background:none !important;inset:auto !important;transform:none !important}}
{H} .lead3-bloc{{background:none !important;padding:0 !important;margin:0 !important;max-width:none !important;border:0 !important;box-shadow:none !important;backdrop-filter:none !important;-webkit-backdrop-filter:none !important}}
{H} :is(.kwp-hero-wp,.kwp-hero-wp-tel){{display:none !important}}
{H} :is(.lv-eyebrow){{display:block;margin:0 0 14px !important;font:400 11px/1.3 'Jost',sans-serif !important;letter-spacing:.25em !important;text-transform:uppercase !important;color:#FFFFFF !important}}
{H} h1{{margin:0 !important;font:300 28px/1.2 'Jost',sans-serif !important;letter-spacing:.06em !important;text-transform:uppercase !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;text-wrap:balance;text-shadow:none !important}}
{H} h1 i{{display:block;margin-top:14px;font:400 12px/1.5 'Jost',sans-serif !important;font-style:normal !important;letter-spacing:.2em !important;text-transform:uppercase !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important}}
{H} :is(.hero-sous,.lead3-bloc>p,.hero-texte>p:not(.lv-eyebrow):not(.lv-reassure)){{margin:14px auto 0 !important;max-width:34ch;font:400 12px/1.5 'Jost',sans-serif !important;letter-spacing:.2em !important;text-transform:uppercase !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;text-shadow:none !important}}
{H} .lv-reassure{{margin:16px 0 0 !important;font:400 11px/1.3 'Jost',sans-serif !important;letter-spacing:.25em !important;text-transform:uppercase !important;color:#FFFFFF !important}}
{H} :is(.btn-hero,.lead3-btns .btn-hero){{display:inline-flex !important;align-items:center;justify-content:center;margin-top:22px !important;min-height:48px;padding:0 28px !important;border-radius:4px !important;background:#111111 !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;border:1px solid #111111 !important;font:400 12px/1 'Jost',sans-serif !important;letter-spacing:.2em !important;text-transform:uppercase !important}}
{H} .lead3-btns{{display:flex !important;flex-direction:column !important;align-items:center !important;gap:12px !important;margin:0 !important}}
{H} .lead3-wa{{color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-size:13px !important;text-decoration:underline !important;text-underline-offset:3px}}
{H} .lead3-wa svg{{fill:#FFFFFF !important}}
{H} form.chercheur{{margin:22px auto 0 !important;max-width:420px}}
{P} .bn-fil{{padding:14px 20px 0 !important}}
{P} .bn-fil .fil{{margin:0 !important;font:400 12px/1.5 'Jost',sans-serif !important;letter-spacing:.04em !important;color:#5E5E5E !important;-webkit-text-fill-color:#5E5E5E !important;text-align:start !important;text-shadow:none !important;background:none !important}}
{P} .bn-fil .fil a{{color:#111111 !important;-webkit-text-fill-color:#111111 !important;text-decoration:underline;text-underline-offset:3px}}
html[dir="rtl"] {P[5:]} :is(.lv-eyebrow,h1,h1 i,.hero-sous,.lv-reassure,.btn-hero){{letter-spacing:0 !important}}
@media (min-width:900px){{{H}{{height:85svh !important}}{H} :is(.hero-texte,.lead3-texte){{padding-bottom:72px !important}}{H} h1{{font-size:44px !important}}{P} .bn-fil{{padding:18px 56px 0 !important}}}}
/* ===/BN-0511=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===BN-0511===.*?/\* ===/BN-0511=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("css ok")
