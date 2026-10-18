# -*- coding: utf-8 -*-
"""Kit Winter Prestige sur les pages hiver et Alpes (19/10, planche v7 validée : 00-brief/kit-winter-prestige/).
Idempotent : chaque bloc vit entre <!--KIT-WP:x--> et <!--/KIT-WP:x-->, le CSS entre /* ===KIT-WP=== */ et /* ===/KIT-WP=== */.
A lancer depuis site-v5/ APRES _prefill.py (il pose ses propres liens pré-remplis), avant _build_sitemap.py.
  - /kosher-les-deux-alpes/ : carte du chalet des Deux Alpes à la place de l'encart lead-wp (fin de lead-offre)
  - /kosher-courchevel/     : section « notre chalet à Courchevel » avec la carte Courchevel, après lead-intro
  - /alps/, /kosher-ski-holidays-french-alps/ : les deux cartes + bandeau, avant lead-final
  - /kosher-chalet-les-deux-alpes/ : bandeau « In partnership with Winter Prestige », avant lead-final
Règle de signature (ETAT 18/10) : support Mishpacha = « In partnership with Winter Prestige », jamais « exclusif ».
Photos d'origine (Courchevel : originaux du 16/10, redimensionnés seulement). Usage : python _kit_wp.py [racine]"""
import io, os, re, sys, shutil, subprocess
from pathlib import Path
ICI = Path(__file__).resolve().parent
RACINE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ICI
KIT = ICI.parents[1] / "00-brief" / "kit-winter-prestige" / "logos"
COURCH = ICI.parents[1] / "00-brief" / "references" / "2026-10-16-chalet-sisimiut-courchevel" / "originaux"

# ---------- fichiers servis ----------
def fichiers():
    img = RACINE / "img"
    for src, dst in [("winter-prestige-symbole-or-aere.svg", "wp-flocon-or.svg"), ("winter-prestige-symbole-noir-aere.svg", "wp-flocon-noir.svg"),
                     ("winter-prestige-long-or-sans-powered-honneur.svg", "wp-long-or.svg"),
                     ("winter-prestige-long-noir-sans-powered-honneur.svg", "wp-long-noir.svg")]:
        shutil.copyfile(KIT / src, img / dst)
    dst = img / "chalet" / "courchevel-ext.jpg"
    if not dst.exists():
        subprocess.run(["magick", str(COURCH / "gal-40209.jpg"), "-resize", "1600x>", "-strip", "-quality", "84", str(dst)], check=True)

# ---------- textes ----------
T = {
 "en": dict(avec="with Winter Prestige", part="In partnership with", dispo="Availability confirmed for your dates with each request.",
            btn="Check my dates", deux="Our two kosher chalets", deux_i="in the Alps", co_h2="Our chalet", co_h2_i="in Courchevel",
            da=dict(lieu="Les Deux Alpes", t="Our kosher chalet, at the foot of the slopes", alt="The chalet in Les Deux Alpes under a blue sky",
                    s=[("300 m²", "private chalet"), ("6 + 1", "bedrooms + nursery"), ("Up to 16", "guests"), ("2 min", "to the slopes")],
                    k="<b>Strictly kosher.</b> Chef or delivered meals, everything served is Chalav Yisrael."),
            co=dict(lieu="Courchevel", t="A kosher chalet in the heart of Courchevel", alt="The chalet in Courchevel under snow",
                    s=[("5", "en-suite bedrooms"), ("10 to 14", "guests"), ("2 pools", "heated, in and out"), ("Private shuttle", "to the slopes")],
                    k="<b>Strictly kosher.</b> Chalet koshered for you, chef or delivered meals, everything served is Chalav Yisrael."),
            seau="STRICTLY KOSHER · CHALAV YISRAEL · SHOMER SHABBAT ·"),
 "fr": dict(avec="avec Winter Prestige", part="En partenariat avec", dispo="Disponibilité confirmée pour vos dates à chaque demande.",
            btn="Vérifier mes dates", deux="Nos deux chalets casher", deux_i="dans les Alpes", co_h2="Notre chalet", co_h2_i="à Courchevel",
            da=dict(lieu="Les Deux Alpes", t="Notre chalet casher, au pied des pistes", alt="Le chalet des Deux Alpes sous le ciel bleu",
                    s=[("300 m²", "chalet privé"), ("6 + 1", "chambres + chambre bébé"), ("Jusqu’à 16", "personnes"), ("2 min", "des pistes")],
                    k="<b>Strictement casher.</b> Chef ou plats livrés, tout ce qui est servi est Chalav Yisrael."),
            co=dict(lieu="Courchevel", t="Un chalet casher au cœur de Courchevel", alt="Le chalet de Courchevel sous la neige",
                    s=[("5", "chambres en suite"), ("10 à 14", "personnes"), ("2 piscines", "chauffées, dedans et dehors"), ("Navette privée", "vers les pistes")],
                    k="<b>Strictement casher.</b> Chalet cachérisé pour vous, chef ou plats livrés, tout ce qui est servi est Chalav Yisrael."),
            seau="STRICTEMENT CASHER · CHALAV YISRAEL · SHOMER SHABBAT ·"),
 "es": dict(avec="con Winter Prestige", part="En colaboración con", dispo="Disponibilidad confirmada para sus fechas en cada solicitud.",
            btn="Consultar mis fechas", deux="Nuestros dos chalets kosher", deux_i="en los Alpes", co_h2="Nuestro chalet", co_h2_i="en Courchevel",
            da=dict(lieu="Les Deux Alpes", t="Nuestro chalet kosher, al pie de las pistas", alt="El chalet de Les Deux Alpes bajo el cielo azul",
                    s=[("300 m²", "chalet privado"), ("6 + 1", "habitaciones + cuarto del bebé"), ("Hasta 16", "personas"), ("2 min", "de las pistas")],
                    k="<b>Estrictamente kosher.</b> Chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            co=dict(lieu="Courchevel", t="Un chalet kosher en el corazón de Courchevel", alt="El chalet de Courchevel bajo la nieve",
                    s=[("5", "habitaciones con baño"), ("De 10 a 14", "personas"), ("2 piscinas", "climatizadas, interior y exterior"), ("Lanzadera privada", "a las pistas")],
                    k="<b>Estrictamente kosher.</b> Chalet kosherizado para ustedes, chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            seau="ESTRICTAMENTE KOSHER · CHALAV YISRAEL · SHOMER SHABAT ·"),
 # hébreu : jamais « ישראל » (règle n° 1), donc pas de Chalav Yisrael ; lexique de la charte (שומר כשרות)
 "he": dict(avec="עם Winter Prestige", part="בשיתוף עם", dispo="הזמינות מאושרת לתאריכים שלכם בכל פנייה.",
            btn="לבדוק את התאריכים", deux="שתי הצ'אלות הכשרות שלנו", deux_i="באלפים", co_h2="הצ'אלה שלנו", co_h2_i="בקורשבל",
            da=dict(lieu="לה דז אלפ", t="הצ'אלה הכשרה שלנו, למרגלות המסלולים", alt="הצ'אלה בלה דז אלפ תחת שמיים כחולים",
                    s=[("300 מ\"ר", "צ'אלה פרטית"), ("6 + 1", "חדרי שינה + חדר תינוק"), ("עד 16", "אורחים"), ("2 דק'", "מהמסלולים")],
                    k="<b>שומר כשרות.</b> שף בצ'אלה או ארוחות במשלוח."),
            co=dict(lieu="קורשבל", t="צ'אלה כשרה בלב קורשבל", alt="הצ'אלה בקורשבל תחת השלג",
                    s=[("5", "חדרי שינה עם חדר רחצה"), ("10 עד 14", "אורחים"), ("2 בריכות", "מחוממות, בפנים ובחוץ"), ("הסעה פרטית", "למסלולים")],
                    k="<b>שומר כשרות.</b> הצ'אלה מוכשרת עבורכם, שף או ארוחות במשלוח."),
            seau="STRICTLY KOSHER · SHOMER SHABBAT · STRICTLY KOSHER · SHOMER SHABBAT ·"),
}
PICTOS = {
 "maison": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "lit": '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M12 4v6"/><path d="M2 18h20"/>',
 "gens": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "pistes": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/><path d="M4.14 15.08c2.62-1.57 5.24-1.43 7.86.42 2.74 1.94 5.49 2 8.23.19"/>',
 "eau": '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>',
 "navette": '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
}
CHALETS = {
 "da": dict(img="/img/chalet/wp-ext-bleu.jpg", w=1600, h=1067, pictos=["maison", "lit", "gens", "pistes"], lien="/kosher-chalet-les-deux-alpes/",
            q="?i=a&amp;lieu=Les%20Deux%20Alpes&amp;voyage=Ski%20holiday%20with%20a%20chalet"),
 "co": dict(img="/img/chalet/courchevel-ext.jpg", w=1600, h=1067, pictos=["lit", "gens", "eau", "navette"], lien=None,
            q="?i=a&amp;lieu=Courchevel&amp;voyage=Ski%20holiday%20with%20a%20chalet"),
}

def pfx(lang): return "" if lang == "en" else f"/{lang}"

def seau(lang, cle):
    i = f"kwp-anneau-{cle}"
    return (f'<svg class="kwp-seau" viewBox="0 0 200 200" aria-hidden="true" focusable="false">'
            f'<defs><path id="{i}" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>'
            f'<circle cx="100" cy="100" r="97" fill="#141416" stroke="#C9A961" stroke-width="3"/>'
            f'<circle cx="100" cy="100" r="58" fill="none" stroke="#C9A961" stroke-width="1.5" opacity=".6"/>'
            f'<text fill="#C9A961" font-family="Heebo,sans-serif" font-weight="700" font-size="13" letter-spacing="2" direction="ltr">'
            f'<textPath href="#{i}" textLength="458" lengthAdjust="spacing">{T[lang]["seau"]}</textPath></text>'
            f'<image href="/img/wp-flocon-or.svg" x="56" y="56" width="88" height="88"/></svg>')

def carte(lang, cle):
    t, c, d = T[lang], CHALETS[cle], T[lang][cle]
    puces = "".join(f'<li><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{PICTOS[p]}</svg><span><b>{a}</b>{b}</span></li>'
                    for p, (a, b) in zip(c["pictos"], d["s"]))
    titre = f'<a href="{pfx(lang)}{c["lien"]}">{d["t"]}</a>' if c["lien"] else d["t"]
    return (f'<article class="kwp-carte"><div class="kwp-photo"><img src="{c["img"]}" alt="{d["alt"]}" width="{c["w"]}" height="{c["h"]}" loading="lazy">'
            f'{seau(lang, cle)}</div><div class="kwp-corps"><div class="kwp-lieu">{d["lieu"]} · {t["avec"]}</div><h3>{titre}</h3>'
            f'<ul class="kwp-chiffres">{puces}</ul><p class="kwp-casher">{d["k"]}</p><p class="kwp-dispo">{t["dispo"]}</p>'
            f'<div class="kwp-pied"><img src="/img/wp-flocon-noir.svg" alt="Winter Prestige" title="Winter Prestige" width="46" height="46" loading="lazy">'
            f'<a class="btn-noir" href="{pfx(lang)}/plan-your-trip/{c["q"]}">{t["btn"]}</a></div></div></article>')

# Moshé 19/10 : « pas en partenariat avec, plutôt en dessous powered by » (remplace « In partnership with » du kit v7)
POWERED = "Powered by Mishpacha Tours"

def bandeau(lang):
    return (f'<div class="kwp-bandeau"><img src="/img/wp-long-or.svg" alt="Winter Prestige" width="300" height="96" loading="lazy">'
            f'<span>{POWERED}</span></div>')

def bloc(nom, html): return f"<!--KIT-WP:{nom}-->{html}<!--/KIT-WP:{nom}-->"

def poser(s, nom, html, avant=None, apres=None):
    s = re.sub(rf"<!--KIT-WP:{nom}-->.*?<!--/KIT-WP:{nom}-->\n", "", s, flags=re.S)
    b = bloc(nom, html)
    if avant:
        i = s.find(avant); assert i >= 0, (nom, avant)
        return s[:i] + b + "\n" + s[i:]
    i = s.find(apres); assert i >= 0, (nom, apres)
    j = s.find("</section>", i) + len("</section>")
    return s[:j] + b + "\n" + s[j:]

def page(slug, lang):
    p = RACINE / (slug if lang == "en" else f"{lang}/{slug}") / "index.html"
    s = io.open(p, encoding="utf-8", newline="").read(); o = s; t = T[lang]
    if slug == "kosher-les-deux-alpes":
        s = re.sub(r'\s*<a class="lead-wp".*?</a>', "", s, flags=re.S)
        i = s.find('<section class="ss wrap lead-offre">'); assert i >= 0
        s = re.sub(r"<!--KIT-WP:da-->.*?<!--/KIT-WP:da-->\n", "", s, flags=re.S)
        j = s.find("</section>", i)
        s = s[:j] + bloc("da", f'<div class="kwp-cartes kwp-seule">{carte(lang, "da")}</div>') + "\n" + s[j:]
    elif slug == "kosher-courchevel":
        s = poser(s, "co", f'<section class="ss wrap kwp"><h2>{t["co_h2"]} <i>{t["co_h2_i"]}</i></h2>'
                           f'<div class="kwp-cartes kwp-seule">{carte(lang, "co")}</div></section>', apres='<section class="ss wrap lead-intro"')
    elif slug in ("alps", "kosher-ski-holidays-french-alps"):
        s = poser(s, "duo", f'<section class="ss wrap kwp"><h2>{t["deux"]} <i>{t["deux_i"]}</i></h2>'
                            f'<div class="kwp-cartes">{carte(lang, "da")}{carte(lang, "co")}</div>{bandeau(lang)}</section>',
                  avant='<section class="ss lead-final"')
    elif slug == "kosher-chalet-les-deux-alpes":
        s = poser(s, "bandeau", f'<section class="ss wrap kwp kwp-seul-bandeau">{bandeau(lang)}</section>', avant='<section class="ss lead-final"')
    if slug in HIVER:
        s = hiver(s, lang)
    if s != o: io.open(p, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

# ---------- pages hiver et Alpes en mixte (réunion du 19/10) ----------
# Contenu aux couleurs du kit v7 (noir, or, givre) et logo Winter Prestige en grand dans la bannière ;
# menu, pied, formulaire lead-final et boutons restent Mishpacha. Signature : « In partnership with ».
HIVER = ["alps"]

def hiver(s, lang):
    s = re.sub(r"<body(?![^>]*kwp-hiver)([^>]*)>", lambda m: '<body class="kwp-hiver"%s>' % m.group(1)
               if "class=" not in m.group(1) else m.group(0).replace('class="', 'class="kwp-hiver '), s, count=1)
    s = re.sub(r"<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->", "", s, flags=re.S)
    i = s.find('<div class="lead3-bloc">')
    if i >= 0:
        i += len('<div class="lead3-bloc">')
        s = s[:i] + bloc("hero", f'<div class="kwp-hero-wp"><img src="/img/wp-long-or.svg" alt="Winter Prestige" width="300" height="96">'
                                 f'<span>{POWERED}</span></div>') + s[i:]
    return s

CSS = """/* ===KIT-WP=== */
.kwp-cartes{display:grid;gap:24px;margin-top:24px}
.kwp-seule{max-width:460px}
.kwp-carte{background:#fff;border-radius:15px;overflow:hidden;box-shadow:0 1px 0 rgba(28,27,31,.08);display:flex;flex-direction:column}
.kwp-photo{position:relative;aspect-ratio:3/2}
.kwp-photo>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.kwp-seau{position:absolute;inset-inline-end:14px;bottom:-34px;width:88px;height:88px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.18))}
.kwp-corps{padding:22px 22px 24px;display:flex;flex-direction:column;flex:1}
.kwp-lieu{font-size:12px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--vert,#2D5132)}
.kwp-carte h3{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:24px;line-height:1.15;margin:6px 0 16px;padding-inline-end:80px}
.kwp-carte h3 a{color:inherit;text-decoration:none}
.kwp-chiffres{display:grid;grid-template-columns:1fr 1fr;gap:12px 14px;margin:0;padding:0;list-style:none}
.kwp-chiffres li{display:flex;gap:10px;align-items:center;font-size:14px;line-height:1.25}
.kwp-chiffres svg{flex:none;width:22px;height:22px;stroke:var(--vert,#2D5132);fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.kwp-chiffres b{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:17px}
.kwp-casher{margin:18px 0 0;padding:12px 14px;background:var(--creme,#FFFAED);border-radius:10px;font-size:14px}
.kwp-casher b{font-weight:500}
.kwp-dispo{font-size:13px;color:#5A6068;margin:12px 0 0}
.kwp-pied{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:auto;padding-top:16px;border-top:1px solid #E2DCCF}
.kwp-corps .kwp-dispo+.kwp-pied{margin-top:18px}
.kwp-pied img{width:46px;height:46px}
.kwp-bandeau{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;margin-top:28px;padding:22px 24px;border-radius:12px;background:#141416;color:#C9D2D4}
.kwp-bandeau span{font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase}
.kwp-bandeau img{height:96px;width:auto}
.kwp-seul-bandeau .kwp-bandeau{margin-top:0}
@media (max-width:599px){.kwp-bandeau{padding:18px 16px}.kwp-bandeau img{height:72px}.kwp-carte h3{font-size:21px}}
@media (min-width:900px){.kwp-cartes{grid-template-columns:repeat(2,minmax(0,460px))}.kwp-seule{grid-template-columns:minmax(0,460px)}}
/* pages hiver et Alpes (19/10) : noir #141416, or #C9A961, or lumière #E3BE80, givre #C9D2D4, clair #FAF7F0 */
body.kwp-hiver{background:#141416}
.kwp-hero-wp{display:flex;flex-direction:column;align-items:flex-start;gap:2px;direction:ltr;margin:0 0 18px;padding-bottom:18px;border-bottom:1px solid rgba(201,169,97,.45)}
.kwp-hero-wp span{font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#C9D2D4;white-space:nowrap;margin-top:-6px;margin-left:calc(min(100%,340px)*.3)}
@media (max-width:420px){.kwp-hero-wp span{font-size:11px;letter-spacing:.12em}}
@media (min-width:900px){.kwp-hero-wp span{font-size:13px;margin-top:-14px;margin-left:calc(min(100%,520px)*.3)}}
[dir=rtl] .kwp-hero-wp{align-items:flex-end}
.kwp-hero-wp img{width:100%;max-width:340px;height:auto;display:block;margin-inline-start:-8px}
@media (min-width:900px){.kwp-hero-wp img{max-width:520px}}
.kwp-hiver .lead3-bloc{background:rgba(20,20,22,.82);border-color:rgba(201,169,97,.45)}
.kwp-hiver .lead3-texte h1{color:#FAF7F0}
.kwp-hiver .lead3-texte h1 i{color:#E3BE80}
.kwp-hiver .lead-puces li{border-color:rgba(201,169,97,.55);color:#E3BE80}
.kwp-hiver main>:not(.lead-final,.lead-hero3){color:#C9D2D4}
.kwp-hiver main>:not(.lead-final,.lead-hero3) :is(h2,h3){color:#E3BE80}
.kwp-hiver main>:not(.lead-final,.lead-hero3) h2 i{color:#C9A961}
.kwp-hiver main>:not(.lead-final,.lead-hero3,.kwp) a:not(.btn-noir):not(.btn-hero){color:#E3BE80}
.kwp-hiver .kwp-carte{color:var(--encre)}
.kwp-hiver .dk-g-tete{color:#E3BE80}
.kwp-hiver main>:not(.lead-final,.lead-hero3) .pill{color:#FAF7F0;border-color:rgba(201,169,97,.55)}
.kwp-lieu{padding-inline-end:96px}
.kwp-hiver .ss.beige{background:#141416;border-block:1px solid rgba(201,169,97,.3)}
.kwp-hiver :is(.dk-cartes>li,.beige .dk-cartes>li,.dk-note p,.beige.dk-note p,.dk-suite>li,.chips li,.minyan-corps,.shabbat){background:rgba(250,247,240,.05);color:#C9D2D4;border:1px solid rgba(201,169,97,.28)!important}
.kwp-hiver .dk-cartes>li>b,.kwp-hiver .conseils b{color:#FAF7F0}
.kwp-hiver .conseils ul,.kwp-hiver .conseils li,.kwp-hiver .faq details{border-color:rgba(201,169,97,.28)}
.kwp-hiver .faq summary{color:#FAF7F0}
.kwp-hiver .faq summary::after{background:#C9A961;color:#141416}
.kwp-hiver .dk-fleche,.kwp-hiver .dk-coche{color:#C9A961}
.kwp-hiver .etapes ol>li>b{color:#C9A961}
.kwp-hiver .lead-mascotte{content:url(/img/picto-hassid-creme.svg)}
.kwp-hiver .dk-h2img[src*="hassid"]{content:url(/img/wp-flocon-or.svg)}
.kwp-hiver main>:not(.lead-final,.lead-hero3) .btn-noir{background:var(--jaune);color:var(--encre)}
.kwp-hiver main>:not(.lead-final,.lead-hero3) .btn-noir svg{fill:var(--encre)}
.kwp-hiver main>:not(.lead-final,.lead-hero3) .kwp-carte :is(h3,h3 a,b){color:var(--encre)}
.kwp-hiver main>:not(.lead-final,.lead-hero3) .kwp-carte .btn-noir{background:var(--encre);color:#fff}
.kwp-hiver .kwp-bandeau{border:1px solid rgba(201,169,97,.45)}
/* toutes les pages : la dernière section ne colle plus au pied (Moshé 19/10, « tronqué ») */
main>.ss:last-child:not(.lead-final){padding-bottom:72px}
/* ===/KIT-WP=== */"""

def css():
    p = RACINE / "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
    s2 = re.sub(r"\n?/\* ===KIT-WP=== \*/.*?/\* ===/KIT-WP=== \*/", "", s, flags=re.S).rstrip("\n") + "\n" + CSS + "\n"
    if s2 != s: io.open(p, "w", encoding="utf-8", newline="").write(s2); return 1
    return 0

if __name__ == "__main__":
    fichiers(); n = css()
    for slug in dict.fromkeys(("kosher-les-deux-alpes", "kosher-courchevel", "alps", "kosher-ski-holidays-french-alps", "kosher-chalet-les-deux-alpes", *HIVER)):
        for lang in T: n += page(slug, lang)
    print(f"_kit_wp : {n} fichier(s) modifié(s)")
