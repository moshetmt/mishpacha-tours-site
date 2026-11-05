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
# v3 du 05/11 (Moshe : « on dirait pas une hashgaha ») : composition d'une vraie teouda (cadre double, ב״ה, titre du document,
# phrase d'attestation, tampon rond, ligne du rav). Aucune signature, aucun numero, aucune date : rien d'invente.
DOC = {"": "Kashrut certificate", "fr": "Certificat de cacherout", "es": "Certificado de kashrut", "he": "תעודת כשרות"}
ATT = {"": "The meals of your stay are prepared under the hashgacha of", "fr": "Les repas de votre séjour sont préparés sous la hashgaha du",
       "es": "Las comidas de su estancia se preparan bajo la hashgajá del", "he": "ארוחות החופשה שלכם מוכנות בהשגחת"}
TAMPON = {"": "BETH HABAD · GRENOBLE-ALPES · HASHGACHA · ", "fr": "BETH HABAD · GRENOBLE-ALPES · HASHGAHA · ",
          "es": "BETH HABAD · GRENOBLE-ALPES · HASHGAJÁ · ", "he": "BETH HABAD · GRENOBLE-ALPES · HASHGACHA · "}  # anneau en latin partout : WebKit inverse l'hebreu sur un textPath

def tampon(lang):  # « כשר » au centre en HTML (le texte SVG hebreu sortait a l'envers sous WebKit)
    return ('<span class="cach-tampon-w"><svg class="cach-tampon" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="cach-cercle" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0"/></defs>'
            '<circle cx="60" cy="60" r="57" fill="none" stroke="#A88F5E" stroke-width="1.6"/><circle cx="60" cy="60" r="35" fill="none" stroke="#A88F5E" stroke-width="1"/>'
            f'<text direction="ltr" font-family="Jost,system-ui,sans-serif" font-size="10.5" letter-spacing="1.6" fill="#7A6440"><textPath href="#cach-cercle" textLength="272">{TAMPON[lang]}</textPath></text>'
            '</svg><span class="cach-kasher" dir="rtl" lang="he" aria-hidden="true">כשר</span></span>')
CSS = f"""
/* CACH-0511 : sceau de cacherout (_sceau_cacherout.py) ; 05/11 v2 (Moshe : « mise en page degueulasse, logo pas mis en valeur ») :
   certificat centre + badge rond « Certifie par » en haut a droite de la photo d'ouverture */
{P} .cach{{position:relative;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;text-align:center;max-width:440px;margin:34px auto !important;padding:34px 24px 26px !important;background:#FFFFFF;border:1px solid #A88F5E;outline:1px solid #A88F5E;outline-offset:-7px;border-radius:0;box-shadow:0 10px 30px rgba(0,0,0,.06)}}
{P} .cach-logo{{display:block;width:150px;height:auto;margin:12px auto 14px}}
{P} main .cach .cach-bh{{position:absolute;top:14px;right:16px;font-size:12px;line-height:1;color:#7A6440 !important;letter-spacing:0}}
{P} main .cach .cach-doc{{display:block;margin:8px 0 0;padding:0 0 12px;font-family:'Jost',system-ui,sans-serif;font-size:19px;font-weight:300;line-height:1.25;letter-spacing:.14em;text-transform:uppercase;color:#111111 !important;background:linear-gradient(#A88F5E,#A88F5E) bottom center/40px 1px no-repeat}}
{P} main .cach .cach-att{{display:block;margin:0 0 4px;font-size:13px;font-weight:300;line-height:1.45;color:#5E5E5E !important}}
{P} main .cach .cach-pied{{display:flex;align-items:center;justify-content:center;gap:18px;margin:18px 0 0;padding:16px 0 0;border-top:1px solid #E6E6E6;width:100%}}
{P} main .cach .cach-tampon-w{{position:relative;display:block;flex:none;width:84px;height:84px;transform:rotate(-8deg)}}
{P} main .cach .cach-tampon{{display:block;width:84px;height:84px}}
{P} main .cach .cach-kasher{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:19px;line-height:1;letter-spacing:0;color:#7A6440 !important}}
{P} main .cach .cach-sign{{display:flex;flex-direction:column;align-items:center;min-width:120px;padding:22px 0 0;border-bottom:1px solid #111111}}
{P} main .cach .cach-sign .cach-r{{margin:0 0 6px;font-style:italic}}
html[dir="rtl"] {P} main .cach .cach-doc{{letter-spacing:0}}
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
    pied = (f'<span class="cach-pied">{tampon(lang)}' +
            (f'<span class="cach-sign"><span class="cach-r">{RAV[lang]}</span></span>' if RAV[lang] else '') + '</span>')
    return (f'{A}<div class="cach" role="note"><span class="cach-bh" aria-hidden="true">ב״ה</span><span class="cach-t">{t}</span>'
            f'<span class="cach-doc">{DOC[lang]}</span>'
            f'<img class="cach-logo" src="/img/logo-bh-or-600.webp" srcset="/img/logo-bh-or-300.webp 300w, /img/logo-bh-or-600.webp 600w" sizes="(min-width:900px) 170px, 150px" alt="{alt}" width="600" height="480" loading="lazy">'
            f'<span class="cach-att">{ATT[lang]}</span><span class="cach-h">{h}</span><span class="cach-p">{pts}</span>{pied}</div>{Z}')

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
