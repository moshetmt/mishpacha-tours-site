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
REF = {"": "Hashgacha Beth Habad", "fr": "Hashgaha Beth Habad", "es": "Hashgajá Beth Habad", "he": "השגחת בית חב״ד"}
A, Z = "<!--CACH-0511-->", "<!--/CACH-0511-->"
P = "html body.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9)"
CSS = f"""
/* CACH-0511 : sceau de cacherout (_sceau_cacherout.py) */
{P} .cach{{display:flex;align-items:center;gap:18px;margin:22px 0;padding:16px 0;border-top:1px solid #A88F5E;border-bottom:1px solid #A88F5E;background:transparent}}
{P} .cach-logo{{display:block;flex:none;width:104px;height:auto;margin:0}}
{P} .cach-logo-c{{display:none}}
{P} .cach.cach--couleur .cach-logo-o{{display:none}}
{P} .cach.cach--couleur .cach-logo-c{{display:block}}
{P} .cach-txt{{min-width:0}}
{P} main .cach .cach-t{{display:block;margin:0 0 6px;font-family:'Jost',system-ui,sans-serif;font-size:11px;font-weight:400;line-height:1.2;letter-spacing:.22em;text-transform:uppercase;color:#7A6440 !important}}
{P} main .cach .cach-h{{display:block;margin:0;font-family:'Jost',system-ui,sans-serif;font-size:17px;font-weight:400;line-height:1.3;color:#111111 !important}}
{P} main .cach .cach-p{{display:block;margin:6px 0 0;font-size:13px;font-weight:300;line-height:1.45;color:#5E5E5E !important}}
{P} .lc-produit .cach{{margin:22px 0 6px}}
{P} main .lc-ref .cach-ref{{color:#7A6440 !important;white-space:nowrap}}
{P} .cach-hero{{display:inline-block;margin:14px 0 0;padding:8px 0 0;border-top:1px solid #A88F5E;font-family:'Jost',system-ui,sans-serif;font-size:11px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:#FFFFFF !important;text-shadow:0 1px 8px rgba(0,0,0,.45)}}
{P} .dk-garanties .dk-g-logo{{display:none !important}}
@media (min-width:900px){{ {P} .cach-logo{{width:120px}} {P} main .cach .cach-h{{font-size:18px}} }}
/* /CACH-0511 */
"""

def bloc(lang):
    t, h, pts, _, alt = T[lang]
    return (f'{A}<div class="cach" role="note">'
            f'<img class="cach-logo cach-logo-o" src="/img/logo-bh-or-600.webp" srcset="/img/logo-bh-or-300.webp 300w, /img/logo-bh-or-600.webp 600w" sizes="(min-width:900px) 120px, 104px" alt="{alt}" width="600" height="480" loading="lazy">'
            f'<img class="cach-logo cach-logo-c" src="/img/logo-bh-couleur-600.webp" srcset="/img/logo-bh-couleur-300.webp 300w, /img/logo-bh-couleur-600.webp 600w" sizes="(min-width:900px) 120px, 104px" alt="" width="600" height="480" loading="lazy" aria-hidden="true">'
            f'<div class="cach-txt"><span class="cach-t">{t}</span><span class="cach-h">{h}</span><span class="cach-p">{pts}</span></div></div>{Z}')

def hero(lang):
    return f'{A}<p class="cach-hero">{T[lang][3]}</p>{Z}'

def poser(f):
    s = f.read_text(encoding="utf-8")
    lang = f.parts[0] if f.parts[0] in ("fr", "es", "he") else ""
    t = re.sub(r"(?:\n[ ]*)?" + re.escape(A) + r".*?" + re.escape(Z), "", s, flags=re.S)  # retire l'ancien sceau, puis repose
    slug = f.parent.name
    if 'class="lc-produit"' in t:  # fiche chalet : mention courte sur la ligne du lieu (premier ecran), sceau apres les boutons
        t = re.sub(r'(<a class="lc-btn lc-blanc lc-wa".*?</a>)', lambda m: m.group(1) + "\n     " + bloc(lang), t, count=1, flags=re.S)
        t = re.sub(r'(<p class="lc-ref">[^<]*)', lambda m: m.group(1) + f'{A}<span class="cach-ref"> · {REF[lang]}</span>{Z}', t, count=1)
    elif slug == "kosher-services-french-alps":
        t = re.sub(r'(<h1>[^<]*<br><i>[^<]*</i></h1>)', lambda m: m.group(1) + hero(lang), t, count=1)
        t = re.sub(r'(<div class="bn-intro wrap">)', lambda m: m.group(1) + bloc(lang), t, count=1)
    elif "seal-check.svg" in t and "dk-garanties" in t:  # station, Alpes
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
