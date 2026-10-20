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
                     ("winter-prestige-long-noir-sans-powered-honneur.svg", "wp-long-noir.svg"),
                     ("winter-prestige-long-or-honneur.svg", "wp-long-or-powered.svg")]:
        shutil.copyfile(KIT / src, img / dst)
    dst = img / "chalet" / "courchevel-ext.jpg"
    if not dst.exists():
        subprocess.run(["magick", str(COURCH / "gal-40209.jpg"), "-resize", "1600x>", "-strip", "-quality", "84", str(dst)], check=True)

# ---------- textes ----------
T = {
 "en": dict(vi_h2="Our villa", vi_h2_i="in Saint-Tropez", avec="with Winter Prestige", part="In partnership with", dispo="Availability confirmed for your dates with each request.",
            btn="Check my dates", deux="Our kosher chalets", deux_i="in the Alps", co_h2="Our chalet", co_h2_i="in Courchevel", me_h2="Our chalet", me_h2_i="near Megève",
            da=dict(lieu="Les Deux Alpes", t="Our kosher chalet, at the foot of the slopes", alt="The chalet in Les Deux Alpes under a blue sky",
                    s=[("300 m²", "private chalet"), ("6 + 1", "bedrooms + nursery"), ("Up to 16", "guests"), ("2 min", "to the slopes")],
                    k="<b>Strictly kosher.</b> Chef or delivered meals, everything served is Chalav Yisrael."),
            co=dict(lieu="Courchevel", t="A kosher chalet in the heart of Courchevel", alt="The chalet in Courchevel under snow",
                    s=[("5", "en-suite bedrooms"), ("10 to 14", "guests"), ("2 pools", "heated, in and out"), ("Private shuttle", "to the slopes")],
                    k="<b>Strictly kosher.</b> Chalet koshered for you, chef or delivered meals, everything served is Chalav Yisrael."),
            sl=dict(lieu="Les Deux Alpes", t="The Slope Chalet, skis on at the door", alt="The Slope Chalet in Les Deux Alpes under snow",
                    s=[("6", "bedrooms"), ("Up to 13", "guests"), ("50 m", "to the slopes"), ("Fireplace", "and south terrace")],
                    k="<b>Strictly kosher.</b> Chalet koshered for you, chef or delivered meals, everything served is Chalav Yisrael."),
            me=dict(lieu="Near Megève", t="The Mont Blanc Chalet, for several families", alt="The living room of the chalet near Megève",
                    s=[("10 + 2", "twin bedrooms + attic rooms"), ("3 to 4", "families"), ("Sauna, jacuzzi", "facing Mont Blanc"), ("Shuttle", "every 20 min to the lifts")],
                    k="<b>Strictly kosher.</b> Chalet koshered for you, chef or delivered meals, everything served is Chalav Yisrael."),
            vi=dict(lieu="Saint-Tropez", t="Villa Beach, a kosher villa on the water", alt="Villa Beach in Saint-Tropez, the pool and the sea",
                    s=[("5", "bedrooms, 5 bathrooms"), ("12", "guests"), ("Private beach", "and boat garage"), ("3 houses", "villa, guest house, lodge")],
                    k="<b>Strictly kosher.</b> Villa koshered for you, private chef, everything served is Chalav Yisrael.", avec="with Summer Prestige"),
            seau="STRICTLY KOSHER · CHALAV YISRAEL · SHOMER SHABBAT ·"),
 "fr": dict(vi_h2="Notre villa", vi_h2_i="à Saint-Tropez", avec="avec Winter Prestige", part="En partenariat avec", dispo="Disponibilité confirmée pour vos dates à chaque demande.",
            btn="Vérifier mes dates", deux="Nos chalets casher", deux_i="dans les Alpes", co_h2="Notre chalet", co_h2_i="à Courchevel", me_h2="Notre chalet", me_h2_i="près de Megève",
            da=dict(lieu="Les Deux Alpes", t="Notre chalet casher, au pied des pistes", alt="Le chalet des Deux Alpes sous le ciel bleu",
                    s=[("300 m²", "chalet privé"), ("6 + 1", "chambres + chambre bébé"), ("Jusqu’à 16", "personnes"), ("2 min", "des pistes")],
                    k="<b>Strictement casher.</b> Chef ou plats livrés, tout ce qui est servi est 'Halav Yisrael."),
            co=dict(lieu="Courchevel", t="Un chalet casher au cœur de Courchevel", alt="Le chalet de Courchevel sous la neige",
                    s=[("5", "chambres en suite"), ("10 à 14", "personnes"), ("2 piscines", "chauffées, dedans et dehors"), ("Navette privée", "vers les pistes")],
                    k="<b>Strictement casher.</b> Chalet cachérisé pour vous, chef ou plats livrés, tout ce qui est servi est 'Halav Yisrael."),
            sl=dict(lieu="Les Deux Alpes", t="Le chalet des pistes, skis aux pieds", alt="Le chalet des pistes aux Deux Alpes sous la neige",
                    s=[("6", "chambres"), ("Jusqu’à 13", "personnes"), ("50 m", "des pistes"), ("Cheminée", "et terrasse plein sud")],
                    k="<b>Strictement casher.</b> Chalet cachérisé pour vous, chef ou plats livrés, tout ce qui est servi est 'Halav Yisrael."),
            me=dict(lieu="Près de Megève", t="Le chalet du Mont Blanc, pour plusieurs familles", alt="Le salon du chalet près de Megève",
                    s=[("10 + 2", "chambres twin + chambres sous le toit"), ("3 à 4", "familles"), ("Sauna, jacuzzi", "face au Mont Blanc"), ("Navette", "toutes les 20 min vers les pistes")],
                    k="<b>Strictement casher.</b> Chalet cachérisé pour vous, chef ou plats livrés, tout ce qui est servi est 'Halav Yisrael."),
            vi=dict(lieu="Saint-Tropez", t="Villa Beach, une villa casher les pieds dans l’eau", alt="Villa Beach à Saint-Tropez, la piscine et la mer",
                    s=[("5", "chambres, 5 salles de bain"), ("12", "personnes"), ("Plage privée", "et garage à bateau"), ("3 maisons", "villa, maison d’invités, loge")],
                    k="<b>Strictement casher.</b> Villa cachérisée pour vous, chef privé, tout ce qui est servi est 'Halav Yisrael.", avec="avec Summer Prestige"),
            seau="STRICTEMENT CASHER · CHALAV YISRAEL · SHOMER SHABBAT ·"),
 "es": dict(vi_h2="Nuestra villa", vi_h2_i="en Saint-Tropez", avec="con Winter Prestige", part="En colaboración con", dispo="Disponibilidad confirmada para sus fechas en cada solicitud.",
            btn="Consultar mis fechas", deux="Nuestros chalets kosher", deux_i="en los Alpes", co_h2="Nuestro chalet", co_h2_i="en Courchevel", me_h2="Nuestro chalet", me_h2_i="cerca de Megève",
            da=dict(lieu="Les Deux Alpes", t="Nuestro chalet kosher, al pie de las pistas", alt="El chalet de Les Deux Alpes bajo el cielo azul",
                    s=[("300 m²", "chalet privado"), ("6 + 1", "habitaciones + cuarto del bebé"), ("Hasta 16", "personas"), ("2 min", "de las pistas")],
                    k="<b>Estrictamente kosher.</b> Chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            co=dict(lieu="Courchevel", t="Un chalet kosher en el corazón de Courchevel", alt="El chalet de Courchevel bajo la nieve",
                    s=[("5", "habitaciones con baño"), ("De 10 a 14", "personas"), ("2 piscinas", "climatizadas, interior y exterior"), ("Lanzadera privada", "a las pistas")],
                    k="<b>Estrictamente kosher.</b> Chalet kosherizado para ustedes, chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            sl=dict(lieu="Les Deux Alpes", t="El chalet de las pistas, esquís puestos en la puerta", alt="El chalet de las pistas en Les Deux Alpes bajo la nieve",
                    s=[("6", "habitaciones"), ("Hasta 13", "personas"), ("50 m", "de las pistas"), ("Chimenea", "y terraza al sur")],
                    k="<b>Estrictamente kosher.</b> Chalet kosherizado para ustedes, chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            me=dict(lieu="Cerca de Megève", t="El chalet del Mont Blanc, para varias familias", alt="El salón del chalet cerca de Megève",
                    s=[("10 + 2", "habitaciones twin + buhardillas"), ("3 a 4", "familias"), ("Sauna, jacuzzi", "frente al Mont Blanc"), ("Lanzadera", "cada 20 min a las pistas")],
                    k="<b>Estrictamente kosher.</b> Chalet kosherizado para ustedes, chef o comidas a domicilio, todo lo que se sirve es Chalav Yisrael."),
            vi=dict(lieu="Saint-Tropez", t="Villa Beach, una villa kosher a pie de mar", alt="Villa Beach en Saint-Tropez, la piscina y el mar",
                    s=[("5", "habitaciones, 5 baños"), ("12", "personas"), ("Playa privada", "y garaje para barco"), ("3 casas", "villa, casa de invitados, caseta")],
                    k="<b>Estrictamente kosher.</b> Villa kosherizada para ustedes, chef privado, todo lo que se sirve es Chalav Yisrael.", avec="con Summer Prestige"),
            seau="ESTRICTAMENTE KOSHER · CHALAV YISRAEL · SHOMER SHABAT ·"),
 # hébreu : jamais « ישראל » (règle n° 1), donc pas de Chalav Yisrael ; lexique de la charte (שומר כשרות)
 "he": dict(vi_h2="הווילה שלנו", vi_h2_i="בסן טרופה", avec="עם Winter Prestige", part="בשיתוף עם", dispo="הזמינות מאושרת לתאריכים שלכם בכל פנייה.",
            btn="לבדוק את התאריכים", deux="הצ'אלות הכשרות שלנו", deux_i="באלפים", co_h2="הצ'אלה שלנו", co_h2_i="בקורשבל", me_h2="הצ'אלה שלנו", me_h2_i="ליד מז'ב",
            da=dict(lieu="לה דז אלפ", t="הצ'אלה הכשרה שלנו, למרגלות המסלולים", alt="הצ'אלה בלה דז אלפ תחת שמיים כחולים",
                    s=[("300 מ\"ר", "צ'אלה פרטית"), ("6 + 1", "חדרי שינה + חדר תינוק"), ("עד 16", "אורחים"), ("2 דק'", "מהמסלולים")],
                    k="<b>שומר כשרות.</b> שף בצ'אלה או ארוחות במשלוח."),
            co=dict(lieu="קורשבל", t="צ'אלה כשרה בלב קורשבל", alt="הצ'אלה בקורשבל תחת השלג",
                    s=[("5", "חדרי שינה עם חדר רחצה"), ("10 עד 14", "אורחים"), ("2 בריכות", "מחוממות, בפנים ובחוץ"), ("הסעה פרטית", "למסלולים")],
                    k="<b>שומר כשרות.</b> הצ'אלה מוכשרת עבורכם, שף או ארוחות במשלוח."),
            sl=dict(lieu="לה דז אלפ", t="צ'אלה המסלולים, נועלים מגלשיים בדלת", alt="צ'אלה המסלולים בלה דז אלפ תחת השלג",
                    s=[("6", "חדרי שינה"), ("עד 13", "אורחים"), ("50 מ'", "מהמסלולים"), ("אח", "ומרפסת דרומית")],
                    k="<b>שומר כשרות.</b> הצ'אלה מוכשרת עבורכם, שף או ארוחות במשלוח."),
            me=dict(lieu="ליד מז'ב", t="צ'אלה המון בלאן, לכמה משפחות", alt="הסלון של הצ'אלה ליד מז'ב",
                    s=[("10 + 2", "חדרי טווין + חדרי עליית גג"), ("3 עד 4", "משפחות"), ("סאונה, ג'קוזי", "מול המון בלאן"), ("הסעה", "כל 20 דק' למסלולים")],
                    k="<b>שומר כשרות.</b> הצ'אלה מוכשרת עבורכם, שף או ארוחות במשלוח."),
            vi=dict(lieu="סן טרופה", t="וילה ביץ׳, וילה כשרה על קו המים", alt="וילה ביץ׳ בסן טרופה, הבריכה והים",
                    s=[("5", "חדרי שינה, 5 חדרי רחצה"), ("12", "אורחים"), ("חוף פרטי", "ומוסך סירות"), ("3 בתים", "וילה, בית אורחים, בית השומר")],
                    k="<b>שומר כשרות.</b> הווילה מוכשרת עבורכם, שף פרטי.", avec="עם Summer Prestige"),
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
 "co": dict(img="/img/chalet/courchevel-ext.jpg", w=1264, h=848, pictos=["lit", "gens", "eau", "navette"], lien="/kosher-chalet-courchevel/",
            q="?i=a&amp;lieu=Courchevel&amp;voyage=Ski%20holiday%20with%20a%20chalet"),
 # 20/10 : second chalet des Deux Alpes, 13 places, ski aux pieds (liens de Mendel, photos retouchées)
 "sl": dict(img="/img/chalet/slope-facade.jpg", w=1264, h=848, pictos=["lit", "gens", "pistes", "maison"], lien="/kosher-slope-chalet-les-deux-alpes/",
            q="?i=a&amp;lieu=Les%20Deux%20Alpes&amp;voyage=Ski%20holiday%20with%20a%20chalet"),
 # 20/10 : chalet près de Megève (Mont Blanc), PDF agence du 16/10, photos re-rendues
 "me": dict(img="/img/chalet/megeve-n0-apt-sejour.jpg", w=1600, h=1067, pictos=["lit", "gens", "eau", "navette"], lien="/kosher-chalet-megeve/",
            q="?i=a&amp;lieu=Meg%C3%A8ve&amp;voyage=Ski%20holiday%20with%20a%20chalet"),
 # 19/10 : la villa de Saint-Tropez, marque d'été Summer Prestige (même équipe, même kit, logo soleil)
 "vi": dict(img="/img/villa/st-tropez-facade.jpg", w=1368, h=912, pictos=["lit", "gens", "eau", "maison"], lien="/kosher-villa-saint-tropez/",
            q="?i=a&amp;lieu=Saint-Tropez&amp;voyage=Summer%20in%20the%20Alps", marque="sp"),
}
MARQUE = {"wp": dict(nom="Winter Prestige", or_="/img/wp-flocon-or.svg", noir="/img/wp-flocon-noir.svg"),
          "sp": dict(nom="Summer Prestige", or_="/img/sp-symbole-or.svg", noir="/img/sp-symbole-noir.svg")}
def marque(cle): return MARQUE[CHALETS[cle].get("marque", "wp")]

def pfx(lang): return "" if lang == "en" else f"/{lang}"

def seau(lang, cle):
    i = f"kwp-anneau-{cle}"
    return (f'<svg class="kwp-seau" viewBox="0 0 200 200" aria-hidden="true" focusable="false">'
            f'<defs><path id="{i}" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>'
            f'<circle cx="100" cy="100" r="97" fill="#141416" stroke="#C9A961" stroke-width="3"/>'
            f'<circle cx="100" cy="100" r="58" fill="none" stroke="#C9A961" stroke-width="1.5" opacity=".6"/>'
            f'<text fill="#C9A961" font-family="Heebo,sans-serif" font-weight="700" font-size="13" letter-spacing="2" direction="ltr">'
            f'<textPath href="#{i}" textLength="458" lengthAdjust="spacing">{T[lang]["seau"]}</textPath></text>'
            f'<image href="{marque(cle)["or_"]}" x="56" y="56" width="88" height="88"/></svg>')

def carte(lang, cle):
    t, c, d = T[lang], CHALETS[cle], T[lang][cle]
    puces = "".join(f'<li><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{PICTOS[p]}</svg><span><b>{a}</b>{b}</span></li>'
                    for p, (a, b) in zip(c["pictos"], d["s"]))
    titre = f'<a href="{pfx(lang)}{c["lien"]}">{d["t"]}</a>' if c["lien"] else d["t"]
    return (f'<article class="kwp-carte{" kwp-sp" if CHALETS[cle].get("marque") == "sp" else ""}"><div class="kwp-photo"><img src="{c["img"]}" alt="{d["alt"]}" width="{c["w"]}" height="{c["h"]}" loading="lazy">'
            f'{seau(lang, cle)}</div><div class="kwp-corps"><div class="kwp-lieu">{d["lieu"]} · {d.get("avec", t["avec"])}</div><h3>{titre}</h3>'
            f'<ul class="kwp-chiffres">{puces}</ul><p class="kwp-casher">{d["k"]}</p><p class="kwp-dispo">{t["dispo"]}</p>'
            f'<div class="kwp-pied"><img src="{marque(cle)["noir"]}" alt="{marque(cle)["nom"]}" title="{marque(cle)["nom"]}" width="46" height="46" loading="lazy">'
            f'<a class="btn-noir" href="{pfx(lang)}/plan-your-trip/{c["q"]}">{t["btn"]}</a></div></div></article>')

# Moshé 19/10 : « pas en partenariat avec », « powered by » écrit juste sous « Winter Prestige », comme dans le logo d'origine
# (logo du kit avec la ligne dessinée dedans ; remplace « In partnership with » du kit v7)
POWERED = "Powered by Mishpacha Tours"

def bandeau(lang):
    return (f'<div class="kwp-bandeau"><img src="/img/wp-long-or-powered.svg" alt="Winter Prestige, {POWERED}" width="1222" height="430" loading="lazy"></div>')

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

# ---------- accès direct aux chalets (19/10, audit du parcours chalet, 06-reports/2026-10-19-information-architecture-chalets.md) ----------
from _zones import CHALETS as NAV_CH, CH_URL
STATIONS_SANS_CHALET = ["kosher-val-thorens", "kosher-alpe-dhuez", "kosher-val-disere", "kosher-les-arcs", "kosher-la-plagne",
                        "kosher-chamonix", "kosher-annecy", "kosher-grenoble", "kosher-zermatt", "kosher-st-moritz", "kosher-crans-montana",
                        "kosher-cervinia", "kosher-courmayeur", "kosher-cortina"]
ACC = {  # titre de la section accueil, porte « chalet » (h3, p), bande des stations (h2, italique)
 "en": dict(h2="Our kosher chalets", i="in the Alps", porte=("Our four chalets, private chef", "Les Deux Alpes, Courchevel or Megève: chef, Shabbat and minyan in the chalet."),
            mini=("Prefer a whole chalet?", "Four kosher chalets")),
 "fr": dict(h2="Nos chalets casher", i="dans les Alpes", porte=("Nos quatre chalets avec chef privé", "Les Deux Alpes, Courchevel ou Megève : chef, Chabbat et minyan au chalet."),
            mini=("Un chalet rien que pour vous ?", "Quatre chalets casher")),
 "es": dict(h2="Nuestros chalets kosher", i="en los Alpes", porte=("Nuestros cuatro chalets con chef privado", "Les Deux Alpes, Courchevel o Megève: chef, Shabat y minyan en el chalet."),
            mini=("¿Prefiere un chalet entero?", "Cuatro chalets kosher")),
 "he": dict(h2="הצ'אלות הכשרות שלנו", i="באלפים", porte=("ארבע הצ'אלות שלנו עם שף פרטי", "לה דז אלפ, קורשבל או מז'ב: שף, שבת ומניין בצ'אלה."),
            mini=("מעדיפים צ'אלה שלם?", "ארבע צ'אלות כשרות")),
}

GALERIE_CO = [("courchevel-piscine-ext", dict(en="The heated outdoor pool", fr="La piscine chauffée extérieure", es="La piscina exterior climatizada", he="הבריכה החיצונית המחוממת")),
              ("courchevel-salon-cheminee", dict(en="The living room and its fireplace", fr="Le salon et sa cheminée", es="El salón y su chimenea", he="הסלון והאח")),
              ("courchevel-salle-a-manger", dict(en="The dining room, for the Shabbat meals", fr="La salle à manger, pour les repas de Chabbat", es="El comedor, para las comidas de Shabat", he="פינת האוכל, לסעודות השבת")),
              ("courchevel-chambre", dict(en="One of the five en-suite bedrooms", fr="L'une des cinq chambres en suite", es="Una de las cinco habitaciones con baño", he="אחד מחמשת חדרי השינה עם חדר רחצה")),
              ("courchevel-piscine-int", dict(en="The indoor pool", fr="La piscine intérieure", es="La piscina interior", he="הבריכה המקורה")),
              ("courchevel-salon-lustre", dict(en="The lounge", fr="Le salon", es="El salón", he="הטרקלין"))]

DIAPO_JS = ("<script>(function(){var g=document.currentScript.previousElementSibling,f=[].slice.call(g.querySelectorAll('figure')),i=0,t,n=f.length;if(n<2)return;"
            "var red=matchMedia('(prefers-reduced-motion: reduce)').matches;function go(k){f[i].classList.remove('on');i=(k+n)%n;f[i].classList.add('on')}"
            "function arme(){clearTimeout(t);if(!red)t=setTimeout(function(){go(i+1);arme()},4500)}"
            "var x0=null;g.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;clearTimeout(t)},{passive:true});"
            "g.addEventListener('touchend',function(e){if(x0!==null){var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)go(i+(d<0?1:-1))}x0=null;arme()},{passive:true});"
            "g.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){go(i+(b.className.indexOf('suiv')>=0?1:-1));arme()})});"
            "f[0].classList.add('on');arme()})();</script>")
FLECHES = {"en": ("Previous photo", "Next photo"), "fr": ("Photo précédente", "Photo suivante"), "es": ("Foto anterior", "Foto siguiente"), "he": ("התמונה הקודמת", "התמונה הבאה")}

def diapo(lang, photos, dossier):
    """photos = [(fichier, légendes par langue)] ; légende dans alt et en texte masqué (Google), jamais affichée (Moshé 19/10)."""
    figs = "".join(f'<figure><img src="/img/{dossier}/{f}.jpg" alt="{c[lang]}" loading="{"eager" if i == 0 else "lazy"}" width="1500" height="1000"><figcaption class="sr-only">{c[lang]}</figcaption></figure>'
                   for i, (f, c) in enumerate(photos))
    a, b = FLECHES[lang]
    return (f'<section class="ss wrap galerie-wp kwp-diapo" aria-roledescription="carousel"><div class="kwp-diapo-cadre">{figs}'
            f'<button type="button" class="kwp-diapo-prec" aria-label="{a}">&#8249;</button><button type="button" class="kwp-diapo-suiv" aria-label="{b}">&#8250;</button></div>{DIAPO_JS}</section>')

GALERIE_SL = [("slope-facade", dict(en="The chalet under snow, fifty metres from the slopes", fr="Le chalet sous la neige, à cinquante mètres des pistes", es="El chalet bajo la nieve, a cincuenta metros de las pistas", he="הצ'אלה תחת השלג, חמישים מטר מהמסלולים")),
              ("slope-salon-canape", dict(en="The living room, open on the snow", fr="Le salon, ouvert sur la neige", es="El salón, abierto a la nieve", he="הסלון, פתוח אל השלג")),
              ("slope-sejour-table", dict(en="The dining table and the kitchen", fr="La table et la cuisine", es="La mesa y la cocina", he="שולחן האוכל והמטבח")),
              ("slope-chambre-double", dict(en="One of the double bedrooms", fr="L'une des chambres doubles", es="Una de las habitaciones dobles", he="אחד מחדרי השינה הזוגיים")),
              ("slope-chambre-double-2", dict(en="A second double bedroom", fr="Une deuxième chambre double", es="Una segunda habitación doble", he="חדר שינה זוגי נוסף")),
              ("slope-chambre-double-3", dict(en="Double bedroom, garden side", fr="Chambre double, côté jardin", es="Habitación doble, lado jardín", he="חדר שינה זוגי, לצד הגינה")),
              ("slope-chambre-sous-toit", dict(en="The bedroom under the roof", fr="La chambre sous le toit", es="La habitación bajo el tejado", he="חדר השינה בעליית הגג")),
              ("slope-salon-baie", dict(en="The living room and its bay window", fr="Le salon et sa baie vitrée", es="El salón y su ventanal", he="הסלון וחלון הראווה")),
              ("slope-sdb-baignoire", dict(en="The bathroom with a tub", fr="La salle de bain avec baignoire", es="El baño con bañera", he="חדר הרחצה עם אמבטיה"))]

GALERIE_ME = [("megeve-n0-apt-sejour", dict(en="The living room of the apartment", fr="Le séjour de l'appartement", es="El salón del apartamento", he="הסלון של הדירה")),
              ("megeve-n1-chambre-1", dict(en="One of the seven twin bedrooms on the first floor", fr="L'une des sept chambres twin du premier étage", es="Una de las siete habitaciones twin del primer piso", he="אחד משבעת חדרי הטווין בקומה הראשונה")),
              ("megeve-n1-chambre-2", dict(en="Twin bedroom, first floor", fr="Chambre twin, premier étage", es="Habitación twin, primer piso", he="חדר טווין, קומה ראשונה")),
              ("megeve-n1-chambre-3", dict(en="Twin bedroom with its shower room", fr="Chambre twin et sa salle d'eau", es="Habitación twin con su baño", he="חדר טווין עם חדר הרחצה שלו")),
              ("megeve-n0-chalet-chambre-twin", dict(en="The ground-floor twin bedroom", fr="La chambre twin du rez-de-chaussée", es="La habitación twin de la planta baja", he="חדר הטווין בקומת הקרקע")),
              ("megeve-n0-apt-chambre-twin", dict(en="The apartment's twin bedroom", fr="La chambre twin de l'appartement", es="La habitación twin del apartamento", he="חדר הטווין של הדירה")),
              ("megeve-n0-apt-chambre-superposes", dict(en="The apartment's bunk bedroom", fr="La chambre à lits superposés de l'appartement", es="La habitación con literas del apartamento", he="חדר המיטות הקומתיים של הדירה")),
              ("megeve-n1-chambre-5", dict(en="Twin bedroom, first floor", fr="Chambre twin, premier étage", es="Habitación twin, primer piso", he="חדר טווין, קומה ראשונה")),
              ("megeve-n2-chambre-1", dict(en="One of the two attic rooms", fr="L'une des deux chambres sous le toit", es="Una de las dos buhardillas", he="אחד משני חדרי עליית הגג"))]

def galerie_me(lang):
    return diapo(lang, GALERIE_ME, "chalet")

def galerie_sl(lang):
    return diapo(lang, GALERIE_SL, "chalet")

def galerie_co(lang):
    """Galerie du chalet de Courchevel sous la bannière, même balisage que celle des Deux Alpes (galerie-wp, épargnée par _sans_mosaique)."""
    return diapo(lang, GALERIE_CO, "chalet")

GALERIE_VI = [("facade", dict(en="The villa, the pool and the sea", fr="La villa, la piscine et la mer", es="La villa, la piscina y el mar", he="הווילה, הבריכה והים")),
              ("terrasse", dict(en="The terrace over the water", fr="La terrasse au-dessus de l'eau", es="La terraza sobre el agua", he="המרפסת מעל המים")),
              ("salon-cuisine", dict(en="The living room, open on the sea", fr="Le salon, ouvert sur la mer", es="El salón, abierto al mar", he="הסלון, פתוח אל הים")),
              ("chambre-vue-mer", dict(en="One of the four sea-view bedrooms", fr="L'une des quatre chambres vue mer", es="Una de las cuatro habitaciones con vista al mar", he="אחד מארבעת חדרי השינה עם נוף לים")),
              ("baie", dict(en="The gulf, from the terrace", fr="Le golfe, depuis la terrasse", es="El golfo, desde la terraza", he="המפרץ, מהמרפסת")),
              ("piscine", dict(en="The heated pool and the jacuzzi", fr="La piscine chauffée et le jacuzzi", es="La piscina climatizada y el jacuzzi", he="הבריכה המחוממת והג'קוזי")),
              ("veranda", dict(en="The glass lounge, the third living room", fr="La véranda, troisième salon", es="La galería acristalada, el tercer salón", he="המרפסת המזוגגת, הסלון השלישי")),
              ("hamac", dict(en="The pergola over the sea", fr="La pergola au-dessus de la mer", es="La pérgola sobre el mar", he="הפרגולה מעל הים")),
              ("garage-bateau", dict(en="The boat garage and its ramp", fr="Le garage à bateau et sa rampe", es="El garaje para barco y su rampa", he="מוסך הסירות והרמפה")),
              ("salle-de-bain-vue-mer", dict(en="The bathroom over the sea", fr="La salle de bain sur la mer", es="El baño sobre el mar", he="חדר הרחצה מעל הים")),
              ("salon-invites", dict(en="The guest house", fr="La maison d'invités", es="La casa de invitados", he="בית האורחים")),
              ("portail", dict(en="The gate", fr="Le portail", es="El portón", he="השער"))]

def galerie_vi(lang):
    return diapo(lang, [("st-tropez-" + f, c) for f, c in GALERIE_VI], "villa")

def hero_sp(s):
    """Logo Summer Prestige en grand dans la bannière (même place que le logo Winter des pages hiver), page crème."""
    s = re.sub(r"<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->", "", s, flags=re.S)
    s = re.sub(r'\s*<img class="lead3-wp"[^>]*>', "", s)
    i = s.find('<div class="lead3-bloc">'); assert i >= 0
    i += len('<div class="lead3-bloc">')
    return s[:i] + bloc("hero", f'<div class="kwp-hero-wp"><img src="/img/sp-long-or.svg" alt="Summer Prestige, {POWERED}" width="3334" height="824"></div>') + s[i:]

def lien_tous(lang): return f'<p class="kwp-tous"><a class="pill" href="{pfx(lang)}/kosher-chalets/">{NAV_CH[lang][1]}</a></p>'

def mini(lang, sauf=None):
    """Bande légère des pages station sans chalet et des pages chalet : deux vignettes vers les chalets."""
    a = ACC[lang]
    v = "".join(f'<a class="kwp-v" href="{pfx(lang)}/{u}/"><img src="{img}" alt="" width="160" height="107" loading="lazy"><span><b>{n}</b>{d}</span></a>'
                for (u, img), (n, d) in zip(CH_URL, NAV_CH[lang][2]) if u != sauf)
    n = sum(1 for u, _ in CH_URL if u != sauf)
    return (f'<section class="ss wrap kwp kwp-mini"><h2>{a["mini"][0]} <i>{a["mini"][1]}</i></h2><div class="kwp-mini-v{" kwp-trois" if n == 3 else ""}">{v}</div>{lien_tous(lang)}</section>')

def accueil(s, lang):
    """Les deux cartes juste sous le hero (à la place du bloc Deux Alpes du 3e écran) ; la porte « chalet » mène à /kosher-chalets/."""
    a = ACC[lang]
    s = re.sub(r'\n?<section class="ss wrap ac-chalet" id="chalet">.*?</section>', "", s, count=1, flags=re.S)
    s = poser(s, "accueil", f'<section class="ss wrap kwp kwp-accueil" id="chalet"><h2>{a["h2"]} <i>{a["i"]}</i></h2>'
                            f'<div class="kwp-cartes">{carte(lang, "da")}{carte(lang, "co")}</div>{lien_tous(lang)}</section>',
              avant='<section class="ss beige" id="trips">')
    s = re.sub(rf'<a class="hub-carte" href="{pfx(lang)}/kosher-chalet-les-deux-alpes/">(.*?)<h3>[^<]*</h3><p>[^<]*</p>',
               lambda m: f'<a class="hub-carte" href="{pfx(lang)}/kosher-chalets/">{m.group(1)}<h3>{a["porte"][0]}</h3><p>{a["porte"][1]}</p>', s, count=1, flags=re.S)
    return s

def page(slug, lang):
    p = RACINE / (slug if lang == "en" else f"{lang}/{slug}") / "index.html"
    s = io.open(p, encoding="utf-8", newline="").read(); o = s; t = T[lang]
    if slug == "":
        s = accueil(s, lang)
    elif slug == "kosher-chalets":
        s = poser(s, "hub", f'<section class="ss wrap kwp kwp-hub"><div class="kwp-cartes">{carte(lang, "da")}{carte(lang, "sl")}{carte(lang, "co")}{carte(lang, "me")}</div>{bandeau(lang)}</section>',
                  apres='<section class="ss wrap lead-intro"')
    elif slug == "kosher-villa-saint-tropez":
        s = poser(s, "galerie", galerie_vi(lang), avant='</main>')   # 19/10 Moshé : jamais sous la bannière, juste avant le pied
        s = hero_sp(s)
    elif slug == "summer-in-the-alps-jewish-families":
        s = poser(s, "vi", f'<section class="ss wrap kwp"><h2>{t["vi_h2"]} <i>{t["vi_h2_i"]}</i></h2>'
                           f'<div class="kwp-cartes kwp-seule">{carte(lang, "vi")}</div></section>', apres='<section class="ss wrap lead-intro"')
    elif slug == "kosher-chalet-courchevel":
        s = poser(s, "galerie", galerie_co(lang), avant='</main>')   # 19/10 Moshé : jamais sous la bannière, juste avant le pied
        s = poser(s, "bandeau", f'<section class="ss wrap kwp kwp-seul-bandeau">{bandeau(lang)}</section>', avant='<section class="ss lead-final"')
    elif slug == "kosher-slope-chalet-les-deux-alpes":   # 20/10, second chalet des Deux Alpes
        s = poser(s, "galerie", galerie_sl(lang), avant='</main>')
        s = poser(s, "bandeau", f'<section class="ss wrap kwp kwp-seul-bandeau">{bandeau(lang)}</section>', avant='<section class="ss lead-final"')
    elif slug == "kosher-chalet-megeve":   # 20/10, chalet du Mont Blanc près de Megève
        s = poser(s, "galerie", galerie_me(lang), avant='</main>')
        s = poser(s, "bandeau", f'<section class="ss wrap kwp kwp-seul-bandeau">{bandeau(lang)}</section>', avant='<section class="ss lead-final"')
    elif slug == "kosher-megeve":
        s = poser(s, "me", f'<section class="ss wrap kwp"><h2>{t["me_h2"]} <i>{t["me_h2_i"]}</i></h2>'
                           f'<div class="kwp-cartes kwp-seule">{carte(lang, "me")}</div></section>', apres='<section class="ss wrap lead-intro"')
    if slug in STATIONS_SANS_CHALET or slug in ("kosher-chalet-les-deux-alpes", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve"):
        s = poser(s, "mini", mini(lang, slug), avant='<section class="ss lead-final"')
    if slug == "kosher-les-deux-alpes":
        s = re.sub(r'\s*<a class="lead-wp".*?</a>', "", s, flags=re.S)
        i = s.find('<section class="ss wrap lead-offre">'); assert i >= 0
        s = re.sub(r"<!--KIT-WP:da-->.*?<!--/KIT-WP:da-->\n", "", s, flags=re.S)
        j = s.find("</section>", i)
        s = s[:j] + bloc("da", f'<div class="kwp-cartes">{carte(lang, "da")}{carte(lang, "sl")}</div>') + "\n" + s[j:]
    elif slug == "kosher-courchevel":
        s = poser(s, "co", f'<section class="ss wrap kwp"><h2>{t["co_h2"]} <i>{t["co_h2_i"]}</i></h2>'
                           f'<div class="kwp-cartes kwp-seule">{carte(lang, "co")}</div></section>', apres='<section class="ss wrap lead-intro"')
    elif slug in ("alps", "kosher-ski-holidays-french-alps"):
        s = poser(s, "duo", f'<section class="ss wrap kwp"><h2>{t["deux"]} <i>{t["deux_i"]}</i></h2>'
                            f'<div class="kwp-cartes">{carte(lang, "da")}{carte(lang, "sl")}{carte(lang, "co")}{carte(lang, "me")}</div>{bandeau(lang)}</section>',
                  apres='<section class="ss wrap lead-intro"')   # 19/10 : remonté juste après l'intro (9e écran -> 2e) ; 20/10 : 3 chalets
    elif slug == "kosher-chalet-les-deux-alpes":
        s = poser(s, "bandeau", f'<section class="ss wrap kwp kwp-seul-bandeau">{bandeau(lang)}</section>', avant='<section class="ss lead-final"')
    if slug in HIVER:
        s = hiver(s, lang)
    if s != o: io.open(p, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

# ---------- pages hiver et Alpes en mixte (réunion du 19/10) ----------
# Contenu aux couleurs du kit v7 (noir, or, givre) et logo Winter Prestige en grand dans la bannière ;
# menu, pied, formulaire lead-final et boutons restent Mishpacha. Signature : logo avec « Powered by Mishpacha Tours ».
# Moshé 19/10 « oui étends » : /alps/, les 17 pages station, services et ski.
HIVER = ["alps", "kosher-courchevel", "kosher-les-deux-alpes", "kosher-megeve", *STATIONS_SANS_CHALET, "kosher-services-french-alps", "kosher-ski-holidays-french-alps",
         "kosher-chalets", "kosher-chalet-les-deux-alpes", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve"]  # les pages chalet (Moshé 19/10 « oui »)
# pastilles FR/ES/HE : la Suisse et l'Italie manquaient aux traductions (Moshé 19/10 « oui ajoute »)
PAYS_ST = {
    "fr": [("En Suisse", [("kosher-zermatt", "Zermatt"), ("kosher-st-moritz", "Saint-Moritz"), ("kosher-crans-montana", "Crans-Montana")]),
           ("En Italie", [("kosher-cervinia", "Cervinia"), ("kosher-courmayeur", "Courmayeur"), ("kosher-cortina", "Cortina d’Ampezzo")])],
    "es": [("En Suiza", [("kosher-zermatt", "Zermatt"), ("kosher-st-moritz", "St. Moritz"), ("kosher-crans-montana", "Crans-Montana")]),
           ("En Italia", [("kosher-cervinia", "Cervinia"), ("kosher-courmayeur", "Courmayeur"), ("kosher-cortina", "Cortina d'Ampezzo")])],
    "he": [("בשוויץ", [("kosher-zermatt", "צרמט"), ("kosher-st-moritz", "סנט מוריץ"), ("kosher-crans-montana", "קראן מונטנה")]),
           ("באיטליה", [("kosher-cervinia", "צרביניה"), ("kosher-courmayeur", "קורמאייר"), ("kosher-cortina", "קורטינה")])],
}
PIED_WP = " · with Winter Prestige"  # pied des pages hiver : notre logo reste, la ligne nomme le partenaire (Moshé 19/10)

def hiver(s, lang):
    s = re.sub(r"<body(?![^>]*kwp-hiver)([^>]*)>", lambda m: '<body class="kwp-hiver"%s>' % m.group(1)
               if "class=" not in m.group(1) else m.group(0).replace('class="', 'class="kwp-hiver '), s, count=1)
    s = re.sub(r"<!--KIT-WP:hero-->.*?<!--/KIT-WP:hero-->", "", s, flags=re.S)
    s = re.sub(r'\s*<img class="lead3-wp"[^>]*>', "", s)  # petit logo de _lead.py : doublon du grand (pages chalet, 19/10)
    # galerie du chalet égarée avant <html> par l'ancienne ancre de _photos_winter_prestige.py : on la remet sous la bannière
    # (le doctype était même coupé en deux : « <!doctype », la galerie, puis « html> »)
    m = re.match(r"<!doctype\s*(<div class=\"ss wrap galerie-wp\">.*?</div></div>)\s*html>\s*", s, flags=re.S | re.I)
    if m:
        gal = m.group(1); s = "<!doctype html>\n" + s[m.end():]
        i = s.find("</section>", s.find('class="hero lead-hero3"')) + len("</section>")
        s = s[:i] + "\n" + gal + s[i:]
    i = s.find('<div class="lead3-bloc">')
    if i >= 0:
        i += len('<div class="lead3-bloc">')
        s = s[:i] + bloc("hero", f'<div class="kwp-hero-wp"><img src="/img/wp-long-or-powered.svg" alt="Winter Prestige, {POWERED}" width="1222" height="430"></div>') + s[i:]
    s = re.sub(r'(<p class="logo-pied">.*?<small>)([^<]*?)(?:' + re.escape(PIED_WP) + r')?(</small>)', lambda m: m.group(1) + m.group(2) + PIED_WP + m.group(3), s, count=1, flags=re.S)
    s = stations(s)
    i = s.find('<!--KIT-WP:stations-->')
    if i >= 0 and lang in PAYS_ST and "kosher-zermatt/" not in s[i:s.find('<!--/KIT-WP:stations-->', i)]:
        j = s.find('</ul>', s.find('class="kwp-pastilles"', i))
        ajout = "".join(f'<li class="kwp-pays">{pays}</li>' + "".join(f'<li><a href="{pfx(lang)}/{u}/">{n}</a></li>' for u, n in st)
                        for pays, st in PAYS_ST[lang])
        s = s[:j] + ajout + s[j:]
    return s

def stations(s):
    """Carte « Station par station » (liste de liens) + carte « Toute autre station » sortent de la grille :
    une bande pleine largeur de pastilles, l'autre carte en ligne dessous (Moshé 19/10, plus de carte orpheline)."""
    m = re.search(r'<li class="dk-lien1"><img[^>]*><b>([^<]*)</b>((?:(?!<a |<li).)*?)(<a (?:(?!<li).)*?)</li>\s*(<li><img[^>]*><b>([^<]*)</b>((?:(?!<li).)*?)</li>\s*)?(?=</ul>)', s, flags=re.S)
    if not m or m.group(3).count("<a ") < 6:
        return s
    morceaux = re.split(r"(<a [^>]*>[^<]*</a>)", m.group(3))
    pastilles = []
    for x in morceaux:
        if x.startswith("<a "):
            pastilles.append(f"<li>{x}</li>")
        elif re.sub(r"[\s,.;:،]", "", x):
            pastilles.append(f'<li class="kwp-pays">{x.strip(" ,.;:").strip()}</li>')
    autre = f'<p class="kwp-st-autre"><b>{m.group(5)}</b>{m.group(6)}</p>' if m.group(4) else ""
    bande = bloc("stations", f'<div class="kwp-stations"><p class="kwp-st-tete"><b>{m.group(1)}</b>{re.sub(r"<[^>]+>", "", m.group(2)).strip()}</p>'
                             f'<ul class="kwp-pastilles">{"".join(pastilles)}</ul>{autre}</div>')
    s = s[:m.start()] + s[m.end():]
    j = s.find("</ul>", m.start()) + len("</ul>")
    return s[:j] + bande + s[j:]

# ---------- fondu vert <-> noir entre les deux chartes (Moshé 19/10 « oui et inversement ») ----------
# Transition de page native (navigateurs récents) activée en CSS ; ce script l'annule quand on reste dans la même charte,
# donc rien au premier chargement ni entre deux pages Mishpacha ou deux pages hiver. Remplace, pour ce seul passage,
# la décision du 15/10 « plus de transition entre pages ».
def script_vt():
    slugs = ",".join(f'"{x}"' for x in HIVER)
    return ('<script data-kwp-vt>(function(){var H=[' + slugs + '];'
            r'function h(){var s=location.pathname.replace(/^\/(fr|es|he)\//,"/").split("/")[1]||"";return H.indexOf(s)>=0?"1":"0"}'
            'addEventListener("pageswap",function(){try{sessionStorage.setItem("mt-charte",h())}catch(e){}});'
            'addEventListener("pagereveal",function(e){if(!e.viewTransition)return;var p=null;try{p=sessionStorage.getItem("mt-charte")}catch(x){}'
            'if(p===null||p===h()){e.viewTransition.skipTransition();return}'
            'var r=document.documentElement;r.dataset.vt=h()==="1"?"hiver":"mishpacha";e.viewTransition.finished.then(function(){delete r.dataset.vt})})})();</script>')

def transition(p):
    s = io.open(p, encoding="utf-8", newline="").read(); o = s
    # 19/10 Moshé : plus de pastilles dans la bannière 3 (elles empilaient sur téléphone) ; _lead.py ne les rend plus, ici on nettoie l'existant
    s = re.sub(r'\s*<ul class="lead-puces">.*?</ul>', "", s, count=1, flags=re.S)
    s = re.sub(r"<!--KIT-WP:vt-->.*?<!--/KIT-WP:vt-->", "", s, flags=re.S)
    m = re.search(r'<link rel="stylesheet" href="[^"]*styles\.css">', s)
    if m:
        s = s[:m.end()] + bloc("vt", script_vt()) + s[m.end():]
    if s != o: io.open(p, "w", encoding="utf-8", newline="").write(s); return 1
    return 0

CSS = """/* ===KIT-WP=== */
.kwp-cartes{display:grid;gap:24px;margin-top:24px}
.kwp-diapo{margin-top:40px}
.kwp-diapo-cadre{position:relative;aspect-ratio:3/2;border-radius:15px;overflow:hidden;background:#ddd}
.kwp-diapo-cadre figure{position:absolute;inset:0;margin:0;opacity:0;transition:opacity 900ms ease}
.kwp-diapo-cadre figure.on{opacity:1}
.kwp-diapo-cadre img{display:block;width:100%;height:100%;object-fit:cover}
.kwp-diapo .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.kwp-diapo button{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border:0;border-radius:50%;background:rgba(20,20,22,.55);color:#fff;font-size:28px;line-height:1;cursor:pointer;display:none}
.kwp-diapo-prec{left:12px}.kwp-diapo-suiv{right:12px}
@media (hover:hover) and (pointer:fine){.kwp-diapo button{display:grid;place-items:center}}
@media (prefers-reduced-motion:reduce){.kwp-diapo-cadre figure{transition:none}}
.kwp .kwp-sp .btn-noir{--logo:url(img/sp-symbole-noir.svg)}   /* 19/10 : carte Summer Prestige, soleil sur le bouton au lieu du flocon */
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
.kwp-dispo{margin-bottom:18px!important}  /* pieds des deux cartes alignés en bas (Moshé 19/10 « c pas droit ») */
.kwp-pied img{width:46px;height:46px}
.kwp-bandeau{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;margin-top:28px;padding:22px 24px;border-radius:12px;background:#141416;color:#C9D2D4}
.kwp-bandeau span{font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase}
.kwp-bandeau img{width:100%;max-width:420px;height:auto}
.kwp-seul-bandeau .kwp-bandeau{margin-top:0}
@media (max-width:599px){.kwp-bandeau{padding:18px 16px}.kwp-carte h3{font-size:21px}}
@media (min-width:900px){.kwp-cartes{grid-template-columns:repeat(2,minmax(0,460px))}.kwp-seule{grid-template-columns:minmax(0,460px)}}
/* 20/10 Moshé « c'est pas droit » : les lignes des cartes (lieu, titre, chiffres, casher, dispo, pied) s'alignent d'une carte à l'autre (subgrid) */
@media (min-width:900px){.kwp-cartes{row-gap:0}.kwp-cartes .kwp-carte{display:grid;grid-template-rows:subgrid;grid-row:span 7}
.kwp-cartes .kwp-corps{display:contents}.kwp-cartes .kwp-corps>*{padding-inline:22px}.kwp-cartes .kwp-corps>h3{padding-inline:22px 80px}
.kwp-cartes .kwp-corps>.kwp-lieu{padding:22px 96px 0 22px}.kwp-cartes .kwp-corps>.kwp-chiffres{align-self:start}
.kwp-cartes .kwp-corps>.kwp-casher{margin-inline:22px;padding:12px 14px}.kwp-cartes .kwp-corps>.kwp-pied{padding-bottom:24px;margin-top:0;align-self:end}}
/* 20/10 : trois chalets, jamais de carte orpheline (règle du 19/10) */
@media (min-width:1000px){.kwp-cartes.kwp-trois{grid-template-columns:repeat(3,minmax(0,1fr))}.kwp-mini-v.kwp-trois{grid-template-columns:repeat(3,minmax(0,420px))}}
/* pages hiver et Alpes (19/10) : noir #141416, or #C9A961, or lumière #E3BE80, givre #C9D2D4, clair #FAF7F0 */
body.kwp-hiver{background:#141416}
.kwp-hero-wp{display:flex;flex-direction:column;align-items:flex-start;gap:2px;direction:ltr;margin:0 0 18px;padding-bottom:18px;border-bottom:1px solid rgba(201,169,97,.45)}
.kwp-hero-wp img{width:100%;max-width:360px;height:auto;display:block;margin-inline-start:-8px}
@media (min-width:900px){.kwp-hero-wp img{max-width:520px}}
[dir=rtl] .kwp-hero-wp{align-items:flex-end}
.kwp-hiver .lead3-bloc{background:rgba(20,20,22,.82);border-color:rgba(201,169,97,.45)}
.kwp-hiver .lead3-texte h1{color:#FAF7F0}
.kwp-hiver .lead3-texte h1 i{color:#E3BE80}
.kwp-hiver .lead-puces li{border-color:rgba(201,169,97,.55);color:#E3BE80}
.kwp-hiver main>:not(.lead-final,.lead-hero3){color:#C9D2D4}
.kwp-hiver main>:not(.lead-final,.lead-hero3) :is(h2,h3){color:#E3BE80}
.kwp-hiver main>:not(.lead-final,.lead-hero3) h2 i{color:#C9A961}
.kwp-hiver main>:not(.lead-final,.lead-hero3,.kwp) a:not(.btn-noir):not(.btn-hero){color:#E3BE80}
.kwp-hiver .kwp-carte{color:var(--encre)}
.kwp-hiver .mosaique figcaption{color:var(--encre)}
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
/* pages hiver : une seule largeur (1200 px, même bord gauche), cartes en colonnes égales, stations en pastilles (19/10) */
@media (min-width:900px){
 .kwp-hiver main>.ss.conseils,.kwp-hiver main>.ss.faq,.kwp-hiver main>.conseils:has(.dk-rail){max-width:1200px}
 .kwp-hiver .dk-cartes:not(.dk-rail){grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
}
.kwp-stations{margin-top:12px;padding:22px 24px;border-radius:15px;border:1px solid rgba(201,169,97,.28);background:rgba(250,247,240,.05)}
.kwp-st-tete b{display:block;margin-bottom:4px;font-family:var(--titre);font-weight:300;font-size:21px;line-height:1.15;color:#FAF7F0}
.kwp-pastilles{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:14px 0 0;padding:0}
.kwp-pastilles a{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;border:1px solid rgba(201,169,97,.5);color:#E3BE80!important;text-decoration:none;font-size:15px}
.kwp-pastilles a:hover{background:#C9A961;color:#141416!important}
.kwp-pays{flex-basis:100%;margin-top:8px;font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#C9D2D4}
.kwp-st-autre{margin:18px 0 0;padding-top:16px;border-top:1px solid rgba(201,169,97,.2)}
.kwp-st-autre b{color:#FAF7F0}
/* toutes les pages : la dernière section ne colle plus au pied (Moshé 19/10, « tronqué ») */
main>.ss:last-child:not(.lead-final){padding-bottom:72px}
/* toutes les pages : le bloc vert du formulaire avait 0 px de marge, bonhomme coupé en haut, carte collée en bas (Moshé 19/10) */
.lead-final{padding:48px 0 56px}
@media (min-width:900px){.lead-final{padding:72px 0 80px}}
/* accès direct aux chalets (19/10) : carte entièrement cliquable, bande des stations, accueil */
.kwp-carte{position:relative;transition:box-shadow .2s,transform .2s}
.kwp-carte h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.kwp-carte .kwp-pied .btn-noir{position:relative;z-index:2}
@media (hover:hover){.kwp-carte:hover{box-shadow:0 10px 30px rgba(28,27,31,.14);transform:translateY(-2px)}}
.kwp-carte h3 a:focus-visible{outline:none}.kwp-carte:has(h3 a:focus-visible){outline:3px solid var(--jaune);outline-offset:3px}
.kwp-tous{margin:22px 0 0}
.kwp-accueil{padding-top:40px}
.kwp-mini-v{display:grid;gap:12px;margin-top:18px}
.kwp-v{display:flex;gap:14px;align-items:center;padding:10px;border-radius:14px;background:#fff;border:1px solid #E2DCCF;text-decoration:none;color:var(--encre)}
.kwp-v img{width:112px;height:75px;object-fit:cover;border-radius:10px;flex:none}
.kwp-v b{display:block;font-family:var(--titre);font-weight:600;font-size:18px;line-height:1.2}
.kwp-v span{font-size:14px;line-height:1.35;color:#5A6068}
@media (min-width:700px){.kwp-mini-v{grid-template-columns:repeat(2,minmax(0,420px))}}
/* menu : entrée Chalets (posée par _zones.py), aperçu des deux chalets au survol sur ordinateur, vignettes visibles dans le panneau */
.nav-ch{position:relative}
.nav-ch-menu{display:none}
.nav-ch-v{display:flex;gap:12px;align-items:center;text-decoration:none;color:var(--encre)}
.nav-ch-v img{width:84px;height:56px;object-fit:cover;border-radius:8px;flex:none}
.nav-ch-v b{display:block;font-weight:600;font-size:15px}
.nav-ch-v span{font-size:13px;line-height:1.35;color:#5A6068}
.nav-ch-tous{font-size:14px;font-weight:600;text-decoration:underline;text-underline-offset:3px}
@media (min-width:900px){
 .nav .liens .nav-ch{display:flex;align-items:center;align-self:stretch}
 .nav .liens .nav-ch-menu{position:absolute;top:100%;inset-inline-start:-18px;z-index:50;width:340px;padding:14px;border-radius:14px;background:#fff;box-shadow:0 16px 40px rgba(28,27,31,.18);flex-direction:column;gap:10px}
 .nav .liens .nav-ch:hover .nav-ch-menu,.nav .liens .nav-ch:focus-within .nav-ch-menu{display:flex}
 .nav .liens .nav-ch-v{padding:6px;border-radius:10px}.nav .liens .nav-ch-v:hover{background:var(--creme)}
 .nav .liens .nav-ch-tous{padding:4px 6px}
}
.panneau .nav-ch{border-bottom:1px solid rgba(28,27,31,.2);padding-bottom:16px}
.panneau nav .nav-ch>a.nav-ch-lien{border-bottom:0;padding-bottom:10px}
.panneau .nav-ch-menu{display:grid;gap:10px}
.panneau nav .nav-ch-menu a{display:flex;padding:0;border:0;font-family:inherit;font-weight:400;font-size:15px}
.panneau nav .nav-ch-menu a.nav-ch-tous{display:none}
/* fondu entre la charte Mishpacha et la charte hiver (19/10) : le script data-kwp-vt l'annule hors changement de charte */
@view-transition{navigation:auto}
/* l'ancienne page s'efface sur le fond de la charte d'arrivée (noir en entrant, vert en revenant), puis la nouvelle apparaît */
html[data-vt=hiver]::view-transition{background:#141416}
html[data-vt=mishpacha]::view-transition{background:#2D5132}
::view-transition-old(root){animation:kwp-vt-sort .3s cubic-bezier(.4,0,1,1) both}
::view-transition-new(root){animation:kwp-vt-entre .35s cubic-bezier(0,0,.2,1) .25s both}
@keyframes kwp-vt-sort{to{opacity:0}}
@keyframes kwp-vt-entre{from{opacity:0}}
.nav{view-transition-name:mt-nav}
@media (prefers-reduced-motion:reduce){@view-transition{navigation:none}}
/* ===/KIT-WP=== */"""

def css():
    p = RACINE / "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
    s2 = re.sub(r"\n?/\* ===KIT-WP=== \*/.*?/\* ===/KIT-WP=== \*/", "", s, flags=re.S).rstrip("\n") + "\n" + CSS + "\n"
    if s2 != s: io.open(p, "w", encoding="utf-8", newline="").write(s2); return 1
    return 0

if __name__ == "__main__":
    fichiers(); n = css()
    for slug in dict.fromkeys(("kosher-les-deux-alpes", "kosher-courchevel", "kosher-megeve", "alps", "kosher-ski-holidays-french-alps", "kosher-chalet-les-deux-alpes",
                               "", "kosher-chalets", "kosher-chalet-courchevel", "kosher-slope-chalet-les-deux-alpes", "kosher-chalet-megeve", "kosher-villa-saint-tropez", "summer-in-the-alps-jewish-families",
                               *STATIONS_SANS_CHALET, *HIVER)):
        for lang in T: n += page(slug, lang)
    for f in sorted(RACINE.glob("**/index.html")):
        r = f.relative_to(RACINE).as_posix()
        if not r.startswith(("_", "preview/")):
            n += transition(f)
    print(f"_kit_wp : {n} fichier(s) modifié(s)")
