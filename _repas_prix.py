# -*- coding: utf-8 -*-
"""Chiffres mis à jour le 30/10 (grille de Mendel des 28-29/10) ; le bloc en ligne et la FAQ prix sont tenus par _seo_semaine1.py.
Page des services Alpes, 4 langues : bloc « Repas livrés : les prix » (grille de Mendel du 26/10/2026, prix tels quels,
sans majoration, décision de Moshé), et FAQ (cacherout, livraison, prix) mise à jour dans le HTML et le JSON-LD.
Source : clients/mishpacha-tours/00-brief/2026-10-26-mendel-grille-repas-et-ads.md. Idempotent.
    python _repas_prix.py   (depuis site-v5/, puis python _agentic.py pour les index.md)"""
import re

WA = {
    "": "https://wa.me/33781823193?text=Hello%2C%20we%20are%20in%20the%20Alps%20and%20would%20like%20kosher%20meals%20delivered.%20Resort%3A%20/%20Dates%3A%20/%20Number%20of%20people%3A",
    "fr": "https://wa.me/33781823193?text=Bonjour%2C%20nous%20serons%20dans%20les%20Alpes%20et%20voudrions%20des%20repas%20casher%20livr%C3%A9s.%20Station%20%3A%20/%20Dates%20%3A%20/%20Nombre%20de%20personnes%20%3A",
    "es": "https://wa.me/33781823193?text=Hola%2C%20estaremos%20en%20los%20Alpes%20y%20querr%C3%ADamos%20comidas%20kosher%20a%20domicilio.%20Estaci%C3%B3n%3A%20/%20Fechas%3A%20/%20N%C3%BAmero%20de%20personas%3A",
    "he": "https://wa.me/33781823193?text=%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%A0%D7%94%D7%99%D7%94%20%D7%91%D7%90%D7%9C%D7%A4%D7%99%D7%9D%20%D7%95%D7%A0%D7%A9%D7%9E%D7%97%20%D7%9C%D7%90%D7%A8%D7%95%D7%97%D7%95%D7%AA%20%D7%9B%D7%A9%D7%A8%D7%95%D7%AA%20%D7%91%D7%9E%D7%A9%D7%9C%D7%95%D7%97.%20%D7%90%D7%AA%D7%A8%3A%20/%20%D7%AA%D7%90%D7%A8%D7%99%D7%9B%D7%99%D7%9D%3A%20/%20%D7%9E%D7%A1%D7%A4%D7%A8%20%D7%9E%D7%A9%D7%AA%D7%AA%D7%A4%D7%99%D7%9D%3A",
}
E = lambda s: f'<bdi dir="ltr">{s}</bdi>'

T = {
 "": dict(
  h2="Delivered meals: <i>the prices</i>",
  intro="Per person, per day. Starting prices, which depend on the resort and the season: you get the exact total in writing before you pay.",
  rows=[("Full board: breakfast, lunch and dinner", "from €78"), ("Dinner only: starter, main course, dessert", "from €28"),
        ("Shabbat: Friday night dinner", "€45"), ("Shabbat: Saturday lunch", "€40"), ("Seuda shlishit", "€30"),
        ("Delivery every two days, any resort in France", "€180 to €360"), ("Kashering the kitchen of the chalet you rent", "from €680"), ("Pizza night with a pizzaiolo, for groups", "€35 per person, from €400")],
  note="Children up to 5: about 30% less. Delivery is charged per trip; when several groups stay in the same resort the same week, they share it. Order by Wednesday evening, pay in full when you order. A plata or a kumkum can be bought for Shabbat. Kosher supervision: Beth Habad de Grenoble Alpes, Rav Yehia Lahiany.",
  btn="Order meals on WhatsApp",
  faq=[("Yes. Our team in the Alps cooks under the Chabad network of the Alps. The supervision details come in writing with your quote.",
        "Yes. The meals are prepared under the supervision of the Beth Habad de Grenoble Alpes, Rav Yehia Lahiany. The details come in writing with your quote."),
       ("Yes. The team delivers to a group for the week, in the resorts of the Grenoble side and in the Belleville valley. Send us the resort, the dates and the number of people.",
        "Yes, in every resort in France, every two days, from €180 to €350 per delivery depending on the resort. Send us the resort, the dates and the number of people."),
       ("No price list: a chalet with a chef for a week and a dozen meals delivered are not the same job. You receive a written quote before you commit to anything.",
        "Delivered meals start at €27 per person per day for dinner only and €75 for full board, plus delivery; Shabbat meals cost €35 to €45. A chalet with a private chef is quoted for your group. You receive a written quote before you commit to anything."),
       ("Strictly kosher: our team in the Alps cooks under the Chabad network of the Alps. The supervision details come in writing with your quote.",
        "Strictly kosher: the meals are prepared under the supervision of the Beth Habad de Grenoble Alpes, Rav Yehia Lahiany. The details come in writing with your quote.")]),
 "fr": dict(
  h2="Repas livrés : <i>les prix</i>",
  intro="Par personne et par jour. Ce sont des prix de départ, selon la station et la saison : vous recevez le total exact par écrit avant de payer.",
  rows=[("Formule complète : matin, midi et soir", "à partir de 78 €"), ("Soir seul : entrée, plat, dessert", "à partir de 28 €"),
        ("Chabbat : dîner du vendredi soir", "45 €"), ("Chabbat : déjeuner du samedi", "40 €"), ("Seouda chlichit", "30 €"),
        ("Livraison tous les deux jours, toute station française", "180 à 360 €"), ("Cachérisation de la cuisine du chalet que vous louez", "à partir de 680 €"), ("Soirée pizza avec un pizzaiolo, pour les groupes", "35 € par personne, à partir de 400 €")],
  note="Enfants jusqu’à 5 ans : environ 30 % de moins. La livraison se paie par passage ; quand plusieurs groupes séjournent dans la même station la même semaine, ils la partagent. Commande au plus tard le mercredi soir, paiement complet à la commande. Plata ou koumkoum en vente pour le Chabbat. Surveillance : Beth Habad de Grenoble Alpes, rav Yehia Lahiany.",
  btn="Commander les repas sur WhatsApp",
  faq=[("Oui. Notre équipe dans les Alpes cuisine sous l’autorité du réseau Chabad des Alpes. Le détail de la surveillance rabbinique vous est remis par écrit avec le devis.",
        "Oui. Les repas sont préparés sous la surveillance du Beth Habad de Grenoble Alpes, rav Yehia Lahiany. Le détail vous est remis par écrit avec le devis."),
       ("Oui. L’équipe livre un groupe pour la semaine, dans les stations du côté de Grenoble et dans la vallée des Belleville. Envoyez-nous la station, les dates et le nombre de personnes.",
        "Oui, dans toutes les stations françaises, tous les deux jours, de 180 à 350 € la livraison selon la station. Envoyez-nous la station, les dates et le nombre de personnes."),
       ("Pas de grille de prix : un chalet avec chef pour une semaine et une douzaine de repas livrés ne sont pas le même travail. Vous recevez un devis écrit avant de vous engager.",
        "Les repas livrés partent de 27 € par personne et par jour pour le soir seul et de 75 € pour la formule complète, plus la livraison ; les repas de Chabbat coûtent de 35 à 45 €. Un chalet avec chef privé se chiffre pour votre groupe. Vous recevez un devis écrit avant de vous engager.")]),
 "es": dict(
  h2="Comidas a domicilio: <i>los precios</i>",
  intro="Por persona y por día. Son precios de partida, según la estación y la temporada: recibe el total exacto por escrito antes de pagar.",
  rows=[("Pensión completa: desayuno, almuerzo y cena", "desde 78 €"), ("Solo cena: entrante, plato principal y postre", "desde 28 €"),
        ("Shabat: cena del viernes", "45 €"), ("Shabat: almuerzo del sábado", "40 €"), ("Seudá shlishit", "30 €"),
        ("Entrega cada dos días, cualquier estación de Francia", "de 180 a 360 €"), ("Kasherización de la cocina del chalé que alquila", "desde 680 €"), ("Noche de pizza con pizzaiolo, para grupos", "35 € por persona, desde 400 €")],
  note="Niños hasta 5 años: alrededor de un 30 % menos. La entrega se paga por viaje; cuando varios grupos están en la misma estación la misma semana, la comparten. Pedido a más tardar el miércoles por la noche, pago completo al hacer el pedido. Plata o kumkum a la venta para Shabat. Supervisión: Beth Habad de Grenoble Alpes, rav Yehia Lahiany.",
  btn="Pedir las comidas por WhatsApp",
  faq=[("Sí. Nuestro equipo en los Alpes cocina bajo la red Chabad de los Alpes. Los detalles de la supervisión se entregan por escrito con el presupuesto.",
        "Sí. Las comidas se preparan bajo la supervisión del Beth Habad de Grenoble Alpes, rav Yehia Lahiany. Los detalles se entregan por escrito con el presupuesto."),
       ("Sí. El equipo entrega a un grupo durante la semana, en las estaciones del lado de Grenoble y en el valle de Belleville. Envíenos la estación, las fechas y el número de personas.",
        "Sí, en todas las estaciones de Francia, cada dos días, de 180 a 350 € por entrega según la estación. Envíenos la estación, las fechas y el número de personas."),
       ("No hay lista de precios: un chalé con chef durante una semana y una docena de comidas entregadas no son el mismo trabajo. Recibe un presupuesto por escrito antes de comprometerse.",
        "Las comidas a domicilio parten de 27 € por persona y día para la cena y de 75 € para la pensión completa, más la entrega; las comidas de Shabat cuestan de 35 a 45 €. Un chalé con chef privado se presupuesta para su grupo. Recibe un presupuesto por escrito antes de comprometerse.")]),
 "he": dict(
  h2="ארוחות במשלוח: <i>המחירים</i>",
  intro="לאדם ליום. אלה מחירי פתיחה, לפי אתר הסקי והעונה: הסכום המדויק נשלח אליכם בכתב לפני התשלום.",
  rows=[("פנסיון מלא: בוקר, צהריים וערב", "החל מ־" + E("78 €")), ("ערב בלבד: מנה ראשונה, עיקרית וקינוח", "החל מ־" + E("28 €")),
        ("שבת: סעודת ליל שבת", E("45 €")), ("שבת: סעודת יום השבת", E("40 €")), ("סעודה שלישית", E("30 €")),
        ("משלוח כל יומיים, לכל אתר סקי בצרפת", E("180–360 €")), ("הכשרת המטבח בצ'אלה ששכרתם", "החל מ־" + E("680 €")), ("ערב פיצה עם פיצאיולו, לקבוצות", E("35 €") + " לאדם, החל מ־" + E("400 €"))],
  note="ילדים עד גיל 5: כ־30% פחות. המשלוח מחויב לפי נסיעה; כשכמה קבוצות שוהות באותו אתר באותו שבוע, הן מתחלקות בו. הזמנה עד יום רביעי בערב, תשלום מלא בעת ההזמנה. אפשר לרכוש פלטה או קומקום לשבת. השגחה: בית חב\"ד גרנובל אלפים, " + E("Rav Yehia Lahiany") + ".",
  btn="הזמינו ארוחות בוואטסאפ",
  faq=[("כן. הצוות שלנו באלפים מבשל תחת רשת חב״ד באלפים. פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר.",
        "כן. הארוחות מוכנות בהשגחת בית חב״ד גרנובל אלפים, " + E("Rav Yehia Lahiany") + ". הפרטים נמסרים בכתב יחד עם הצעת המחיר."),
       ("כן. הצוות מספק משלוחים לקבוצה לאורך השבוע, באתרי צד גרנובל ובעמק בלוויל. שלחו לנו את האתר, את התאריכים ואת מספר המשתתפים.",
        "כן, לכל אתרי הסקי בצרפת, כל יומיים, " + E("180–350 €") + " למשלוח לפי האתר. שלחו לנו את האתר, את התאריכים ואת מספר המשתתפים."),
       ("אין מחירון: צ'אלה עם שף לשבוע ותריסר ארוחות במשלוח אינם אותה עבודה. אתם מקבלים הצעת מחיר בכתב לפני שאתם מתחייבים לדבר.",
        "ארוחות במשלוח מתחילות ב־" + E("27 €") + " לאדם ליום לארוחת ערב בלבד וב־" + E("75 €") + " לפנסיון מלא, בתוספת משלוח; ארוחות שבת עולות " + E("35–45 €") + ". צ'אלה עם שף פרטי מתומחרת לפי הקבוצה. אתם מקבלים הצעת מחיר בכתב לפני שאתם מתחייבים לדבר.")]),
}

def bloc(l):
    t = T[l]
    # 26/10 Mendel : « trop linéaire », des photos par repas. Cartes avec photo pour les repas, lignes simples pour le reste.
    photos = {0: "petit-dej", 1: "diner", 2: "chabbat-soir", 3: "chabbat-midi", 4: "seouda", 7: "pizza"}
    cartes = "".join(
        f'<li class="rp-carte"><img src="/img/repas/{photos[i]}-480.webp" srcset="/img/repas/{photos[i]}-480.webp 480w, /img/repas/{photos[i]}-800.webp 800w" '
        f'sizes="(min-width:900px) 360px, (min-width:600px) 45vw, 90vw" alt="" width="800" height="600" loading="lazy" decoding="async">'
        f'<span>{a}</span><b>{b}</b></li>'
        for i, (a, b) in enumerate(t["rows"]) if i in photos)
    lis = "".join(f"<li><span>{a}</span><b>{b}</b></li>" for i, (a, b) in enumerate(t["rows"]) if i not in photos)
    return (f'<section class="ss wrap minyan-bh repas-prix" id="meal-prices"><div class="minyan-corps">'
            f'<h2>{t["h2"]}</h2><p>{t["intro"]}</p><ul class="rp-cartes">{cartes}</ul><div class="prix-table"><ul>{lis}</ul></div>'
            f'<p class="note">{t["note"]}</p>'
            f'<p class="cta-hero cta-bh"><a class="btn-noir" href="{WA[l]}" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg>{t["btn"]}</a></p>'
            f'</div></section>')

def plain(s):  # version texte pour le JSON-LD (sans bdi)
    return re.sub(r"<[^>]+>", "", s).replace('"', '\\"')

SUP = {
 "fr": ("Strictement casher : notre équipe dans les Alpes cuisine sous l’autorité du réseau Chabad des Alpes. Le détail de la surveillance rabbinique vous est remis par écrit avec le devis.",
        "Strictement casher : les repas sont préparés sous la surveillance du Beth Habad de Grenoble Alpes, rav Yehia Lahiany. Le détail vous est remis par écrit avec le devis."),
 "es": ("Estrictamente kosher: nuestro equipo en los Alpes cocina bajo la red Chabad de los Alpes. Los detalles de la supervisión se entregan por escrito con el presupuesto.",
        "Estrictamente kosher: las comidas se preparan bajo la supervisión del Beth Habad de Grenoble Alpes, rav Yehia Lahiany. Los detalles se entregan por escrito con el presupuesto."),
 "he": ("בהקפדה על כשרות: הצוות שלנו באלפים מבשל תחת רשת חב״ד באלפים. פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר.",
        "בהקפדה על כשרות: הארוחות מוכנות בהשגחת בית חב״ד גרנובל אלפים, " + E("Rav Yehia Lahiany") + ". הפרטים נמסרים בכתב יחד עם הצעת המחיר."),
}
for l in ("fr", "es", "he"):  # le JSON-LD FAQ des pages FR, ES, HE est resté en anglais : mêmes remplacements que l'anglais
    T[l]["faq"] = T[l]["faq"] + [SUP[l]] + T[""]["faq"][:3]

for l in T:
    p = (l + "/" if l else "") + "kosher-services-french-alps/index.html"
    h = open(p, encoding="utf-8").read()
    if 'id="meal-prices"' not in h:
        i = h.find('<section class="ss wrap etapes"')
        assert i > 0, p
        h = h[:i] + bloc(l) + " " + h[i:]
    n = 0
    for old, new in T[l]["faq"]:
        for o, nw in ((old, new), (old.replace('"', '\\"'), plain(new))):
            if o in h:
                k = h.count(o); h = h.replace(o, nw); n += k
    open(p, "w", encoding="utf-8").write(h)
    print(p, "bloc ok,", n, "remplacements FAQ")

css = open("styles.css", encoding="utf-8").read()
if "/* REPAS-PRIX */" not in css:
    css += """
/* REPAS-PRIX */ /* page des services Alpes : grille des repas livrés de Mendel (26/10) */
.repas-prix .prix-table ul{max-width:none;margin:28px 0 0;padding:4px 20px;background:transparent;border:1px solid rgba(201,169,97,.35)}
.repas-prix .prix-table li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 14px;align-items:baseline;color:inherit;border-color:rgba(201,169,97,.25)}
.repas-prix .prix-table li span{min-width:0;opacity:.9}
.repas-prix .prix-table li b{white-space:nowrap;font-size:18px;text-align:end;color:var(--jaune,#C9A961)}
.repas-prix .note{font-size:15px;opacity:.85}
@media (max-width:480px){.repas-prix .prix-table li{grid-template-columns:1fr}.repas-prix .prix-table li b{text-align:start}}
@media (min-width:900px){.repas-prix .prix-table li b{font-size:24px}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)

css = open("styles.css", encoding="utf-8").read()
if "/* REPAS-CARTES */" not in css:
    open("styles.css", "w", encoding="utf-8").write(css + """
/* REPAS-CARTES */ /* 26/10 Mendel : une photo par repas, cartes sur fond sombre */
.repas-prix .rp-cartes{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:1fr;gap:16px}
.repas-prix .rp-carte{display:grid;grid-template-columns:minmax(0,1fr);gap:4px;align-items:start;padding:0 0 16px;border:1px solid rgba(201,169,97,.3);overflow:hidden;background:rgba(250,247,240,.03)}
.repas-prix .rp-carte img{grid-column:1/-1;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;margin-bottom:12px}
.repas-prix .rp-carte span{padding-inline:16px;opacity:.92;font-size:15px;line-height:1.4}
.repas-prix .rp-carte b{padding-inline:16px;font-family:var(--titre);font-weight:300;font-size:19px;line-height:1.25;color:var(--jaune,#C9A961);text-align:start;text-wrap:balance}
@media (min-width:600px){.repas-prix .rp-cartes{grid-template-columns:repeat(2,1fr)}}
@media (min-width:900px){.repas-prix .rp-cartes{grid-template-columns:repeat(3,1fr);gap:20px}.repas-prix .rp-carte b{font-size:22px}}
.repas-prix .rp-cartes + .prix-table ul{margin-top:20px}
""")
