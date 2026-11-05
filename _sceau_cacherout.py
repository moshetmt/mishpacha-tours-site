# -*- coding: utf-8 -*-
"""05/11 (Moshe : « la cacherout, c'est une proposition de valeur hyper importante, il faut la mettre en valeur, visible des
   le premier instant » ; Mendel : « mets le logo du Beth Habad de Grenoble, ca rassure les gens »).
   Sceau de cacherout = un bloc unique : logo du Beth Habad Grenoble-Alpes + « Hashgaha » + nom + 'Halav Israel · Shomer Shabbat,
   entre deux filets d'or brosse. Pose :
     - fiche chalet : sous le prix et les chiffres, avant « Demander le catalogue » ;
     - page services : une ligne « Hashgaha · Beth Habad Grenoble-Alpes » dans le heros (premier ecran), le sceau sous le heros ;
     - pages station et Alpes : le sceau remplace le logo seul pose sous la ligne de cacherout (_logo_cacherout.py).
   Tout est entre marqueurs <!--CACH-0511--> ... <!--/CACH-0511--> et remplace a chaque passage (idempotent).
   python _sceau_cacherout.py [fichiers...]   (sans argument : toutes les pages concernees)"""
import re, sys, pathlib

T = {  # titre, nom, points, ligne du heros, texte alternatif
    "":   ("Hashgacha", "Beth Habad Grenoble‑Alpes", "Chalav Yisrael · Shomer Shabbat", "Hashgacha · Beth Habad Grenoble-Alpes", "Beth Habad Grenoble-Alpes"),
    "fr": ("Hashgaha", "Beth Habad de Grenoble‑Alpes", "'Halav Yisrael · Shomer Shabbat", "Hashgaha · Beth Habad Grenoble-Alpes", "Beth Habad Grenoble-Alpes"),
    "es": ("Hashgajá", "Beth Habad Grenoble‑Alpes", "Jalav Yisrael · Shomer Shabat", "Hashgajá · Beth Habad Grenoble-Alpes", "Beth Habad Grenoble-Alpes"),
    "he": ("השגחה", "בית חב״ד גרנובל-אלפים", "חלב ישראל · שומר שבת", "השגחה · בית חב״ד גרנובל-אלפים", "בית חב״ד גרנובל-אלפים"),
}
RAV = {"": "Rav Yehia Lahiany", "fr": "Rav Yehia Lahiany", "es": "Rav Yehia Lahiany", "he": ""}   # 05/11 : oui de Moshe ; orthographe hebraique a fournir
REF = {"": "Hashgacha Beth Habad", "fr": "Hashgaha Beth Habad", "es": "Hashgajá Beth Habad", "he": "השגחת בית חב״ד"}
A, Z = "<!--CACH-0511-->", "<!--/CACH-0511-->"
P = "html body.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12):not(#lv13)"   # plus fort que les regles wp-v3 (11 :not) des pages Winter Prestige
CERT = {"": "Certified by", "fr": "Certifié par", "es": "Certificado por", "he": "בהשגחת"}
CSS = f"""
/* CACH-0511 : sceau de cacherout (_sceau_cacherout.py) ; 05/11 v2 (Moshe : « mise en page degueulasse, logo pas mis en valeur ») :
   certificat centre + badge rond « Certifie par » en haut a droite de la photo d'ouverture */
{P} .cach{{display:flex;flex-direction:column;align-items:center;text-align:center;max-width:420px;margin:30px auto !important;padding:26px 16px 24px !important;border:0;background:linear-gradient(#A88F5E,#A88F5E) top center/56px 1px no-repeat,linear-gradient(#A88F5E,#A88F5E) bottom center/56px 1px no-repeat}}
{P} .cach-logo{{display:block;width:150px;height:auto;margin:12px auto 14px}}
{P} main .cach .cach-t{{display:block;margin:0;font-family:'Jost',system-ui,sans-serif;font-size:11px;font-weight:400;line-height:1.2;letter-spacing:.24em;text-transform:uppercase;color:#7A6440 !important}}
{P} main .cach .cach-h{{display:block;margin:0;font-family:'Jost',system-ui,sans-serif;font-size:18px;font-weight:400;line-height:1.3;color:#111111 !important}}
{P} main .cach .cach-r{{display:block;margin:3px 0 0;font-family:'Jost',system-ui,sans-serif;font-size:14px;font-weight:300;line-height:1.35;color:#111111 !important}}
{P} main .cach .cach-p{{display:block;margin:8px 0 0;font-size:13px;font-weight:300;line-height:1.45;letter-spacing:.02em;color:#5E5E5E !important}}
{P} .lc-produit .cach{{margin:26px auto 8px !important}}
{P} main .lc-ref .cach-ref{{color:#7A6440 !important;white-space:nowrap}}
{P} .cach-hero{{display:inline-block;margin:14px 0 0;padding:8px 0 0;border-top:1px solid #A88F5E;font-family:'Jost',system-ui,sans-serif;font-size:11px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:#FFFFFF !important;text-shadow:0 1px 8px rgba(0,0,0,.45)}}
{P} .dk-garanties .dk-g-logo{{display:none !important}}
{P} .lc-galerie{{position:relative}}
{P} .cach-bulle{{position:absolute;top:14px;right:14px;left:auto;z-index:6;box-sizing:border-box;width:112px;height:112px;border-radius:50%;background:#FFFFFF;box-shadow:0 8px 24px rgba(0,0,0,.24),0 1px 3px rgba(0,0,0,.14);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;pointer-events:none}}
{P} .cach-bulle::before{{content:"";position:absolute;inset:5px;border:1px solid #A88F5E;border-radius:50%}}
{P} .cach-bulle .cach-bulle-t{{display:block;font-family:'Jost',system-ui,sans-serif;font-size:8.5px;font-weight:400;line-height:1;letter-spacing:.18em;text-transform:uppercase;color:#7A6440 !important;text-shadow:none}}
{P} .cach-bulle img{{display:block;width:74px;height:auto;margin:0}}
{P} section.hero .cach-bulle{{top:86px}}
@media (min-width:900px){{ {P} .cach-bulle{{width:140px;height:140px;top:20px;right:20px}} {P} section.hero .cach-bulle{{top:96px;right:28px}} {P} .cach-bulle img{{width:94px}} {P} .cach-bulle .cach-bulle-t{{font-size:10px}} {P} .cach-logo{{width:170px}} }}
/* /CACH-0511 */
"""

def bloc(lang):
    t, h, pts, _, alt = T[lang]
    return (f'{A}<div class="cach" role="note"><span class="cach-t">{t}</span>'
            f'<img class="cach-logo" src="/img/logo-bh-or-600.webp" srcset="/img/logo-bh-or-300.webp 300w, /img/logo-bh-or-600.webp 600w" sizes="(min-width:900px) 170px, 150px" alt="{alt}" width="600" height="480" loading="lazy">'
            f'<span class="cach-h">{h}</span>' + (f'<span class="cach-r">{RAV[lang]}</span>' if RAV[lang] else '') + f'<span class="cach-p">{pts}</span></div>{Z}')

def bulle(lang):
    return (f'{A}<div class="cach-bulle"><span class="cach-bulle-t">{CERT[lang]}</span>'
            f'<img src="/img/logo-bh-or-300.webp" srcset="/img/logo-bh-or-300.webp 300w, /img/logo-bh-or-600.webp 600w" sizes="(min-width:900px) 94px, 74px" alt="{T[lang][4]}" width="600" height="480"></div>{Z}')

def hero(lang):
    return f'{A}<p class="cach-hero">{T[lang][3]}</p>{Z}'

def poser(f):
    s = f.read_text(encoding="utf-8")
    lang = f.parts[0] if f.parts[0] in ("fr", "es", "he") else ""
    t = re.sub(r"(?:\n[ ]*)?" + re.escape(A) + r".*?" + re.escape(Z), "", s, flags=re.S)  # retire l'ancien sceau, puis repose
    slug = f.parent.name
    if 'class="lc-galerie"' in t:  # badge rond en haut a droite de la photo d'ouverture des fiches
        t = t.replace('<div class="lc-galerie">', '<div class="lc-galerie">' + bulle(lang), 1)
    elif re.search(r'<section class="hero[ "]', t) and ("seal-check.svg" in t or slug == "kosher-services-french-alps"):
        t = re.sub(r'(<section class="hero[^"]*"[^>]*>)', lambda m: m.group(1) + bulle(lang), t, count=1)
    if 'class="lc-produit"' in t:  # fiche chalet : mention courte sur la ligne du lieu (premier ecran), sceau apres les boutons
        t = re.sub(r'(<a class="lc-btn lc-blanc lc-wa".*?</a>)', lambda m: m.group(1) + "\n     " + bloc(lang), t, count=1, flags=re.S)
        t = re.sub(r'(<p class="lc-ref">[^<]*)', lambda m: m.group(1) + f'{A}<span class="cach-ref"> · {REF[lang]}</span>{Z}', t, count=1)
    elif slug == "kosher-services-french-alps":
        t = re.sub(r'(<h1>[^<]*<br><i>[^<]*</i></h1>)', lambda m: m.group(1) + hero(lang), t, count=1)
        if '<div class="bn-intro wrap">' in t:
            t = re.sub(r'(<div class="bn-intro wrap">)', lambda m: m.group(1) + bloc(lang), t, count=1)
        else:  # hebreu : pas de bloc d'introduction sous la banniere, le sceau va juste apres le fil d'Ariane
            t = re.sub(r'(<div class="bn-fil wrap">.*?</div>)', lambda m: m.group(1) + A + '<div class="wrap">' + bloc(lang)[len(A):-len(Z)] + '</div>' + Z, t, count=1, flags=re.S)
    elif "seal-check.svg" in t and "dk-garanties" in t:  # station, Alpes (le logo seul de _logo_cacherout.py est retire)
        t = re.sub(r' <span class="dk-g dk-g-logo">(?:<span class="dk-g-logo-t">[^<]*</span>)?<img[^>]*></span>', '', t)
        t = re.sub(r'(<p class="dk-garanties">.*?</p>)', lambda m: m.group(1) + bloc(lang), t, count=1, flags=re.S)
    if t != s:
        f.write_text(t, encoding="utf-8", newline="\n")
        return 1
    return 0

def main():
    fs = [pathlib.Path(x) for x in sys.argv[1:]] or [p for p in pathlib.Path(".").rglob("index.html")]
    n = sum(poser(f) for f in fs)
    c = pathlib.Path("lv.css"); cs = c.read_text(encoding="utf-8")
    cs = re.sub(r"\n/\* CACH-0511 .*?/\* /CACH-0511 \*/\n", "", cs, flags=re.S) + CSS
    c.write_text(cs, encoding="utf-8", newline="\n")
    print("pages modifiees :", n)

main()
