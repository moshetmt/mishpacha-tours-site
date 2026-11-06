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
    # 05/11 v4 (Moshe : « ca n'a pas trop de sens de dire Hashgaha, il faut bien utiliser la terminologie ») : « certifie cacher par »
    # points = ce qui qualifie les REPAS et le SERVICE, jamais pose a cote du rav (« Shomer Shabbat » pres du nom du rav laisserait
    # entendre qu'on certifie le rav lui-meme : malentendu enorme)
    "":   ("", "Beth Habad Grenoble‑Alpes", "Chalav Yisrael meals · Shomer Shabbat service", "Certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany", "Beth Habad Grenoble-Alpes"),
    "fr": ("", "Beth Habad de Grenoble‑Alpes", "Repas 'Halav Yisrael · Service shomer Chabbat", "Certifié cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany", "Beth Habad Grenoble-Alpes"),
    "es": ("", "Beth Habad Grenoble‑Alpes", "Comidas Jalav Yisrael · Servicio shomer Shabat", "Certificado kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany", "Beth Habad Grenoble-Alpes"),
    "he": ("", "בית חב״ד גרנובל-אלפים", "ארוחות חלב ישראל · שירות שומר שבת", "בהשגחת בית חב״ד גרנובל-אלפים", "בית חב״ד גרנובל-אלפים"),
}
RAV = {"": "Rav Yehia Lahiany", "fr": "Rav Yehia Lahiany", "es": "Rav Yehia Lahiany", "he": ""}   # 05/11 : oui de Moshe ; orthographe hebraique a fournir
REF = {"": "Certified kosher", "fr": "Certifié cacher", "es": "Certificado kosher", "he": "השגחת בית חב״ד"}
OR = {"": "Certified kosher by Beth Habad Grenoble‑Alpes", "fr": "Certifié cacher par le Beth Habad de Grenoble‑Alpes",
      "es": "Certificado kosher por el Beth Habad Grenoble‑Alpes", "he": "בהשגחת בית חב״ד גרנובל-אלפים"}   # ligne d'or en bas du certificat
A, Z = "<!--CACH-0511-->", "<!--/CACH-0511-->"
P = "html body.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9):not(#lv10):not(#lv11):not(#lv12):not(#lv13)"   # plus fort que les regles wp-v3 (11 :not) des pages Winter Prestige
CERT = {"": "Certified kosher by:", "fr": "Certifié cacher par :", "es": "Certificado kosher por:", "he": "בהשגחת:"}
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
/* CACH-0511 : sceau de cacherout (_sceau_cacherout.py) ; 05/11 v4 (Moshe) : certificat coupe avant le tampon, ligne d'or en bas,
   pose apres les accordeons des fiches chalet ; badge rond « Certifie cacher par : » plus discret sur la photo d'ouverture */
{P} .cach{{position:relative;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;text-align:center;max-width:440px;margin:34px auto !important;padding:32px 24px 0 !important;background:#FFFFFF;border:1px solid #A88F5E;outline:1px solid #A88F5E;outline-offset:-7px;border-radius:0;box-shadow:0 10px 30px rgba(0,0,0,.06);overflow:hidden}}
{P} .cach-logo{{display:block;width:130px;height:auto;margin:14px auto 12px}}
{P} main .cach .cach-bh{{position:absolute;top:14px;right:16px;font-size:12px;line-height:1;color:#7A6440 !important;letter-spacing:0}}
{P} main .cach .cach-doc{{display:block;margin:6px 0 0;padding:0 0 12px;font-family:'Jost',system-ui,sans-serif;font-size:18px;font-weight:300;line-height:1.25;letter-spacing:.14em;text-transform:uppercase;color:#111111 !important;background:linear-gradient(#A88F5E,#A88F5E) bottom center/40px 1px no-repeat}}
{P} main .cach .cach-p{{display:block;margin:0;font-size:13px;font-weight:300;line-height:1.45;letter-spacing:.02em;color:#5E5E5E !important}}
{P} main .cach .cach-or{{display:block;box-sizing:border-box;width:calc(100% - 14px);margin:20px 0 7px;padding:14px 16px 16px;border-top:1px solid #A88F5E;font-family:'Jost',system-ui,sans-serif;font-size:12px;font-weight:400;line-height:1.5;letter-spacing:.12em;text-transform:uppercase;color:#7A6440 !important}}
{P} main .cach .cach-or-r{{display:block;margin:2px 0 0;font-size:13px;letter-spacing:.06em;text-transform:none;color:#7A6440 !important}}
html[dir="rtl"] {P} main .cach :is(.cach-doc,.cach-or,.cach-or-r){{letter-spacing:0}}
{P} .lc-cach{{box-sizing:border-box;margin:30px 0 34px !important;padding:0 24px !important}}
{P} .lc-cach .cach{{margin:0 auto !important}}
{P} main .lc-ref .cach-ref{{color:#7A6440 !important;white-space:nowrap}}
{P} .cach-hero{{display:inline-block;margin:14px 0 0;padding:8px 0 0;border-top:1px solid #A88F5E;font-family:'Jost',system-ui,sans-serif;font-size:11px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:#FFFFFF !important;text-shadow:0 1px 8px rgba(0,0,0,.45)}}
{P} .dk-garanties .dk-g-logo{{display:none !important}}
{P} .lc-galerie{{position:relative}}
{P} .cach-bulle{{position:absolute;top:12px;right:12px;left:auto;z-index:6;box-sizing:border-box;width:92px;height:92px;border-radius:50%;background:rgba(255,255,255,.94);box-shadow:0 4px 14px rgba(0,0,0,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;pointer-events:none}}
{P} .cach-bulle::before{{content:"";position:absolute;inset:4px;border:1px solid #A88F5E;border-radius:50%}}
{P} .cach-bulle .cach-bulle-t{{display:block;max-width:64px;font-family:'Jost',system-ui,sans-serif;font-size:7.5px;font-weight:400;line-height:1.25;letter-spacing:.12em;text-align:center;text-transform:uppercase;color:#7A6440 !important;text-shadow:none}}
html[dir="rtl"] {P} .cach-bulle .cach-bulle-t{{font-size:10px;letter-spacing:0}}
{P} .cach-bulle img{{display:block;width:56px;height:auto;margin:0}}
/* 06/11 (Moshe : « le logo dans la banniere, mets-le en dore, avec un petit effet ») : logo et libelle remplis d'or brosse,
   un reflet lent passe toutes les 6 s ; fixe si l'utilisateur a coupe les animations */
{P} .cach-bulle .cach-bulle-logo{{display:block;width:56px;aspect-ratio:600/479;background:linear-gradient(100deg,#8C7448 0%,#D9C48E 13%,#F3E6BE 19%,#D9C48E 25%,#8C7448 33%,#7A6440 40%,#B89C62 70%,#9C8250 85%,#7A6440 100%) 100% 0/300% 100%;-webkit-mask:url(/img/logo-bh-or-600.webp) center/contain no-repeat;mask:url(/img/logo-bh-or-600.webp) center/contain no-repeat;animation:cach-reflet 6s ease-in-out infinite}}
{P} .cach-bulle .cach-bulle-t{{background:linear-gradient(100deg,#8C7448 0%,#D9C48E 13%,#F3E6BE 19%,#D9C48E 25%,#8C7448 33%,#7A6440 40%,#B89C62 70%,#9C8250 85%,#7A6440 100%) 100% 0/300% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent !important;animation:cach-reflet 6s ease-in-out infinite}}
@keyframes cach-reflet{{0%,55%{{background-position:100% 0}}85%,100%{{background-position:0 0}}}}
@media (prefers-reduced-motion:reduce){{ {P} .cach-bulle .cach-bulle-logo,{P} .cach-bulle .cach-bulle-t{{animation:none;background-position:50% 0}} }}
{P} section.hero .cach-bulle{{top:86px}}
@media (min-width:900px){{ {P} .cach-bulle{{width:112px;height:112px;top:18px;right:18px}} {P} section.hero .cach-bulle{{top:96px;right:28px}} {P} .cach-bulle img,{P} .cach-bulle .cach-bulle-logo{{width:70px}} {P} .cach-bulle .cach-bulle-t{{font-size:8.5px;max-width:78px}} {P} .cach-logo{{width:150px}} }}
/* /CACH-0511 */
"""

def bloc(lang):
    t, h, pts, _, alt = T[lang]
    # 05/11 v4 (Moshe) : coupe avant le tampon, sans tampon ni signature ; en bas, en or, « Certifie cacher par ..., Rav ... »
    rav = f'<span class="cach-or-r">{RAV[lang]}</span>' if RAV[lang] else ''
    return (f'{A}<div class="cach" role="note"><span class="cach-bh" aria-hidden="true">ב״ה</span>'
            f'<span class="cach-doc">{DOC[lang]}</span>'
            f'<img class="cach-logo" src="/img/logo-bh-or-600.webp" srcset="/img/logo-bh-or-300.webp 300w, /img/logo-bh-or-600.webp 600w" sizes="(min-width:900px) 150px, 130px" alt="{alt}" width="600" height="480" loading="lazy">'
            f'<span class="cach-p">{pts}</span><span class="cach-or">{OR[lang]}{rav}</span></div>{Z}')

def bulle(lang):
    return (f'{A}<div class="cach-bulle"><span class="cach-bulle-t">{CERT[lang]}</span>'
            f'<span class="cach-bulle-logo" role="img" aria-label="{T[lang][4]}"></span></div>{Z}')

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
    if 'class="lc-produit"' in t:  # fiche chalet : mention courte sur la ligne du lieu (premier ecran) ; certificat apres les accordeons
        # (05/11 v4, Moshe : « le certificat n'a rien a faire ici », sous les boutons du premier ecran)
        cert = A + '<div class="lc-cach">' + bloc(lang)[len(A):-len(Z)] + '</div>' + Z
        for ancre in ('<div class="lc-bas-photos">', '<div class="lc-bas-autres">'):
            if ancre in t:
                t = t.replace(ancre, cert + "\n  " + ancre, 1); break
        else:
            t = re.sub(r'(<a class="lc-btn lc-blanc lc-wa".*?</a>)', lambda m: m.group(1) + "\n     " + bloc(lang), t, count=1, flags=re.S)
        t = re.sub(r'(<p class="lc-ref">[^<]*)', lambda m: m.group(1) + f'{A}<span class="cach-ref"> · {REF[lang]}</span>{Z}', t, count=1)
    elif slug == "kosher-services-french-alps":
        # 05/11 soir (Moshe : « il y a deja marque certifie cacher en haut, pourquoi tu le rajoutes dans la banniere ») :
        # plus de ligne sous le titre, le badge rond suffit dans la banniere
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
