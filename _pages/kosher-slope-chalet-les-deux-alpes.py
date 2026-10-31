# -*- coding: utf-8 -*-
# Second chalet des Deux Alpes (13 places, ski aux pieds), « The Slope Chalet », page créée le 20/10 (Moshé : « et au site aussi »).
# Source : annonces les2alpes.com et Airbnb du 20/10 (liens de Mendel), références dans 00-brief/references/2026-10-20-chalet-2-deux-alpes/.
# Ni nom du chalet, ni numéro, ni adresse ; photos retouchées (miroir, recadrage, étalonnage) pour ne pas retrouver l'annonce.
PAGE = dict(
  slug="kosher-slope-chalet-les-deux-alpes",
  title="Kosher Chalet in Les Deux Alpes, Ski In Ski Out, 13 Beds",
  desc="A kosher ski-in ski-out chalet in Les Deux Alpes: 6 bedrooms, 13 beds, a fireplace, a south-facing terrace. Chef or delivered meals, Shabbat and minyan. One written quote.",
  h1="Chalet Rochebrune, Les Deux Alpes", ital="6 bedrooms, skis on at the door",
  intro="A 165 m² chalet in Les Deux Alpes, fifty metres from the slopes: you put your skis on at the door. Six bedrooms and 13 beds, a living room with a fireplace, a south-facing terrace. Our team koshers the kitchen, a chef cooks or kosher meals are delivered, and Shabbat comes with a minyan on request. Five minutes on foot from our other chalet, for a group of two families. One request, one written quote.",
  chips=["6 bedrooms, 13 beds", "Skis on at the door", "Fireplace, south terrace", "On written quote"],
  illus="flat-ski.png",
  crumb=("../kosher-chalets/", "Our kosher chalets"),
  wa="33652092301",
  sections=[
    # galerie : posée juste avant le pied par _kit_wp.py (KIT-WP:galerie), jamais sous la bannière (Moshé 19/10)
    dict(type="text", h2="The chalet, <i>in short</i>", html="""<ul>
<li><b>Bedrooms.</b> Six bedrooms for 13 guests: a bedroom with a large double bed that splits into twins, a twin bedroom, two double bedrooms, a bedroom with three single beds, and bunk beds for two kids.</li>
<li><b>Bathrooms.</b> A bathroom with a tub, a shower room, two separate toilets.</li>
<li><b>Living.</b> A living room with a fireplace, a dining table for everyone, an equipped kitchen, a smart TV and Wi-Fi.</li>
<li><b>Outside.</b> A south-west terrace and a garden, a barbecue, a garage and two parking spaces. A laundry with a washing machine and a boot dryer.</li>
<li><b>Location.</b> Les Deux Alpes, at 1,650 m. The slopes are fifty metres away, the ski school meeting point three hundred, the shops and the shuttle stop a hundred.</li>
<li><b>With our other chalet.</b> Five minutes on foot from <a href="../kosher-chalet-les-deux-alpes/">our 15-bed chalet</a>: two families in each house, dinner together in one.</li>
<li><b>Kitchen.</b> Kashered by our team before you arrive, included. A chef cooks in the chalet, or kosher meals arrive ready to reheat.</li>
</ul>
<p>Beds made on arrival in winter, linen and towels included. Availability is confirmed for your dates with each request.</p>"""),
    dict(type="beige", h2="Shabbat <i>in the chalet</i>", html="""<p>The chef prepares the Shabbat meals and the holidays in the chalet, or the meals arrive before candle lighting. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your group, Shacharis takes place in your living room.</p>
<p>Strictly kosher, everything served is Chalav Yisrael. The supervision details come in writing with your quote.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us", "Your dates, the number of people and what you want. By WhatsApp or with the form at the bottom of this page. Hebrew-speaking guests are welcome."),
      ("We check the chalet", "Our team in the Alps confirms the chalet for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote for the whole stay, before you commit to anything."),
    ]),
    dict(type="beige", h2="Getting <i>there</i>", html="""<ul>
<li><b>From Lyon-Saint-Exupéry.</b> About 2 h 30 by road. Geneva, about 3 h. Grenoble, about 1 h 30.</li>
<li><b>Transfers.</b> Vans with car seats from the airport to the chalet and back, on quote.</li>
<li><b>In the resort.</b> The shuttle stop is a hundred metres from the door; the shuttle from Grenoble stops there too.</li>
<li><b>Land in Lyon with a few hours to spare?</b> <a href="../tours/stopover/">The Stopover</a>: a private 3 hour tour of Jewish Lyon between the plane and the road.</li>
</ul>"""),
    dict(type="faq", h2="The Slope Chalet: <i>questions</i>", items=[
      ("How much does it cost?", "<span data-prix-tpl='From €{ch2_basse_vente} per week'>From €13,000 per week</span> for the chalet. The final price depends on your dates, the number of people and the services you choose: you receive a written quote before you commit to anything. The stay is quoted and invoiced by our kosher team based in the Alps."),
      ("How many people can stay?", "Six bedrooms and 13 beds, for two families or one large family."),
      ("Can two families take both chalets?", "Yes. Our 15-bed chalet is five minutes on foot. Four families, two houses, one chef for the dinners together."),
      ("Who cooks the meals?", "A chef cooks kosher meals in the chalet, or ready meals are delivered. Our team kashers the kitchen before you arrive."),
      ("Is there a minyan?", "We bring the bochurim and a Sefer Torah to the chalet for Shabbat, on request. Tell us your dates early."),
      ("How far are the slopes?", "Fifty metres: you put your skis on at the door. The ski school meeting point is three hundred metres away."),
    ]),
    dict(type="cta", txt="The Slope Chalet for your dates?", msg="Hello, we would like the Slope Chalet in Les Deux Alpes. Dates: / Number of people:"),
  ],
  related=[("../kosher-chalets/", "Our kosher chalets"), ("../kosher-chalet-les-deux-alpes/", "Our 15-bed chalet in Les Deux Alpes"), ("../kosher-les-deux-alpes/", "Kosher in Les Deux Alpes"), ("../kosher-services-french-alps/", "Kosher services in the Alps")],
  source="Sources: our team in the Alps (links of 20/10/2026) for the chalet and its layout.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher ski-in ski-out chalet in Les Deux Alpes", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": {"@type": "Place", "name": "Les Deux Alpes"}, "serviceType": "Kosher chalet with chef or delivered meals, Shabbat and minyan in Les Deux Alpes", "url": "https://mishpachatours.com/kosher-slope-chalet-les-deux-alpes/", "offers": {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": 13000, "priceCurrency": "EUR", "unitText": "week"}}},
  ticket=True,
  VERIF=[
    "165 m², 13 guests, bed plan (160 or 2x80, 2x90, 140, 3x90, 140 + 2 bunk beds 90), bathroom with tub + shower room + 2 WC, fireplace, terrace south-west, garden, barbecue, garage, 2 parking, laundry, boot dryer, smart TV, Wi-Fi, 50 to 300 m from the slopes, ski school 300 m, shops 100 m, shuttle 100 m, beds made on arrival in winter: resort booking listing read on 20/10/2026.",
    "6 bedrooms, 3 bathrooms, 50 m from the slopes, south terrace: Airbnb listing read on 20/10/2026 (the resort listing counts 5 bedrooms plus the bunk beds, and 2 bathrooms plus 2 WC; page follows the resort listing for bathrooms).",
    "Five minutes on foot from the 15-bed chalet: Mendel, 19/10/2026 (fiche Bibi), not measured.",
    "Lyon 2 h 30, Geneva 3 h, Grenoble 1 h 30: estimates, not measured.",
  ],
)
