# -*- coding: utf-8 -*-
# Chalet de Val Thorens (3 Vallées), page créée le 22/10 (Moshé : « ajoute le chalet Val Thorens sur le site », cinquième chalet).
# Source : annonces Airbnb et allChalets lues le 22/10 (00-brief/references/2026-10-22-chalet-val-thorens-bennett/), photos re-rendues par Gemini.
# Jamais le nom du chalet, de l'hôte, de Saint-Martin-de-Belleville, ni « seul chalet privé de Val Thorens ». Prix : seulement le « à partir de » basse saison de la grille de Mendel (décision Moshé 30/10, _seo_semaine1.py).
# Nom affiché « The Val Thorens Chalet » et slug choisis par Claude, à confirmer par Moshé.
PAGE = dict(
  slug="kosher-chalet-val-thorens",
  title="Kosher Chalet in Val Thorens, Ski In Ski Out, 10 Guests",
  desc="A private kosher chalet in Val Thorens, south-facing with a ski path at the door: three en-suite bedrooms, up to 10 guests. Chef, Shabbat and minyan. One written quote.",
  h1="Chalet Belle Étoile, Val Thorens", ital="ski in, ski out, 3 suites",
  intro="A private wooden chalet above Val Thorens, in the 3 Valleys, facing south. A ski path starts at the door; the village is a few minutes on foot. 165 m², three en-suite bedrooms, up to 10 guests (8 adults). Chef or delivered meals, Shabbat and minyan.",
  chips=[],
  illus="flat-ski.png",
  crumb=("../kosher-chalets/", "Our kosher chalets"),
  wa="33652092301",
  sections=[
    # galerie : posée juste avant le pied par _kit_wp.py (KIT-WP:galerie), jamais sous la bannière (Moshé 19/10)
    dict(type="text", h2="The chalet, <i>in short</i>", html="""<ul>
<li><b>Location.</b> Above the village of Val Thorens, the highest resort in Europe, in a quiet area facing south. The centre and the restaurants are a few minutes on foot. A ski path starts in front of the door: good skiers ski back to the chalet, the others walk the last 100 metres.</li>
<li><b>The living floor.</b> 60 m² on the first floor: a lounge, a dining room with a table for ten, an open high-end kitchen, a rotating wood stove, wide south-facing windows and a balcony.</li>
<li><b>Three large bedrooms,</b> each with its own bathroom. The master suite of 28 m² under the roof, with a dressing room, a mezzanine, a balcony and a safe. A bedroom of 18 m² with two single beds, a bath, a shower and a south balcony. A bedroom of 15 m² with a double bed, a shower and a south balcony. Three bathrooms and one separate WC.</li>
<li><b>Ski room.</b> With boot warmers, at the door.</li>
<li><b>Comforts.</b> Wifi, a washing machine, a tumble dryer, a baby cot and a high chair.</li>
<li><b>Kitchen.</b> Kashered by our team before you arrive, included. A chef cooks in the chalet, or kosher meals arrive ready to reheat.</li>
</ul>
<p>The chalet welcomes up to 10 guests, 8 adults at most. Availability is confirmed for your dates with each request.</p>"""),
    dict(type="beige", h2="Shabbat <i>in the chalet</i>", html="""<p>The chef prepares the Shabbat meals and the holidays in the chalet, or the meals arrive before candle lighting. The dining table seats ten. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your group, Shacharis takes place in your living room.</p>
<p>Strictly kosher, everything served is Chalav Yisrael. The supervision details come in writing with your quote.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us", "Your dates, the number of guests and what you want. By WhatsApp or with the form at the bottom of this page. Hebrew-speaking guests are welcome."),
      ("We check the chalet", "Our team in the Alps confirms the chalet for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote for the whole stay, before you commit to anything."),
    ]),
    dict(type="beige", h2="Getting <i>there</i>", html="""<ul>
<li><b>From Geneva airport.</b> About 2 h 45 by road. Lyon-Saint-Exupéry, about 3 h.</li>
<li><b>Transfers.</b> Vans with car seats from Geneva or Lyon to the chalet and back, on quote.</li>
<li><b>Land in Lyon with a few hours to spare?</b> <a href="../tours/stopover/">The Stopover</a>: a private 3 hour tour of Jewish Lyon between the plane and the road.</li>
</ul>"""),
    dict(type="faq", h2="The Val Thorens Chalet: <i>questions</i>", items=[
      ("How much does it cost?", "<span data-prix-tpl='From €{ch5_basse_vente} per week'>From €9,500 per week</span> for the chalet. The final price depends on your dates, the number of people and the services you choose: you receive a written quote before you commit to anything. The stay is quoted and invoiced by our kosher team based in the Alps."),
      ("How many people can stay?", "Up to 10 guests, 8 adults at most, in three en-suite bedrooms: one large family, or two families with children."),
      ("Is it really ski in, ski out?", "A ski path starts in front of the door. Good skiers ski back to the chalet; for the others, the last 100 metres are on foot."),
      ("Can we walk to the restaurants?", "Yes. The village centre and the restaurants are a few minutes on foot from the chalet."),
      ("Who cooks the meals?", "A chef cooks kosher meals in the chalet, or ready meals are delivered. Our team kashers the kitchen before you arrive."),
      ("Is there a minyan?", "We bring the bochurim and a Sefer Torah to the chalet for Shabbat, on request. Tell us your dates early."),
    ]),
    dict(type="cta", txt="The Val Thorens Chalet for your dates?", msg="Hello, we would like the kosher chalet in Val Thorens. Dates: / Number of guests:"),
  ],
  related=[("../kosher-chalets/", "Our kosher chalets"), ("../kosher-val-thorens/", "Kosher in Val Thorens"), ("../kosher-chalet-courchevel/", "Our chalet in Courchevel"), ("../kosher-services-french-alps/", "Kosher services in the Alps")],
  source="Sources: our team in the Alps (listings read on 22/10/2026) for the chalet, the ski path and the services.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher chalet in Val Thorens", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": {"@type": "Place", "name": "Val Thorens"}, "serviceType": "Kosher chalet with chef or delivered meals, Shabbat and minyan in Val Thorens", "url": "https://mishpachatours.com/kosher-chalet-val-thorens/", "offers": {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": 9500, "priceCurrency": "EUR", "unitText": "week"}}},
  ticket=True,
  VERIF=[
    "165 m², living floor of 60 m², three en-suite bedrooms (28, 18 and 15 m²), ski room with boot warmers, wifi, washer, dryer, cot and high chair, ski path at the door, south-facing, quiet area a few minutes on foot from the centre: Airbnb and allChalets listings read on 22/10/2026, no written confirmation from the owner.",
    "Capacity: the listing says 10 guests with 8 adults at most. Page says « up to 10 guests (8 adults) ». A group of 10 adults does not fit (see the Bennett file).",
    "Geneva about 2 h 45 and Lyon about 3 h by road: estimates, not measured. Name « The Val Thorens Chalet » and slug chosen by Claude, to confirm by Moshé. Never the chalet's name, the host, Saint-Martin-de-Belleville, or any claim of being the only private chalet. Price: only the low-season « from » price of Mendel's grid (Moshé, 30/10).",
  ],
)
