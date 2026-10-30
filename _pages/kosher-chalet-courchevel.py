# -*- coding: utf-8 -*-
# Chalet de Courchevel (Winter Prestige), page créée le 19/10 (audit du parcours chalet, décision Moshé « page dédiée »).
# Ni nom du chalet, ni hameau, ni surface (ETAT 16/10) ; photos d'origine (décision du 18/10).
PAGE = dict(
  slug="kosher-chalet-courchevel",
  title="Kosher Chalet in Courchevel, Pools and Chef",
  desc="A kosher chalet in the heart of Courchevel: 5 en-suite bedrooms, heated pools and hammam, a private chef, Shabbat and a minyan. One written quote.",
  h1="Chalet Flocon Doré, Courchevel", ital="5 suites, heated pools, private chef",
  intro="A chalet in the heart of Courchevel, in the 3 Valleys. Five en-suite bedrooms for 10 to 14 guests, heated pools, a hammam and a private shuttle to the lifts. Our team koshers the kitchen, a private chef cooks every meal, and Shabbat comes with a minyan and a Sefer Torah. One request, one written quote.",
  chips=["5 en-suite bedrooms, 10 to 14 guests", "Heated pools, hammam", "Private shuttle to the lifts", "On written quote"],
  illus="flat-ski.png",
  crumb=("../kosher-chalets/", "Our kosher chalets"),
  wa="33652092301",
  sections=[
    # galerie : posée sous la bannière par _kit_wp.py (KIT-WP:galerie), une mosaïque de bas de page serait retirée par _sans_mosaique
    dict(type="text", h2="The chalet, <i>in short</i>", html="""<ul>
<li><b>Bedrooms.</b> Five bedrooms, each with its own bathroom, on three floors. One bedroom for each couple, 10 to 14 guests.</li>
<li><b>Location.</b> The heart of Courchevel, in the 3 Valleys. The slopes are five to six minutes on foot.</li>
<li><b>Shuttle.</b> A private shuttle runs from 9 am to 6 pm and drops you at the foot of the lifts.</li>
<li><b>Wellness.</b> A heated pool indoors and outdoors, a hammam, a relaxation area and a gym.</li>
<li><b>Art.</b> An artist's chalet: every room is dressed with a unique work of art chosen by the owner. One bedroom all white, like a snowfield; another dark, with tapestry on the walls and ski scenes. An old family farm reworked into a few chalets.</li>
<li><b>Also.</b> A large living room with a fireplace, a dining room, a home cinema, a ski room, private parking and a south-facing terrace.</li>
<li><b>Kitchen.</b> Kashered by our team before you arrive, included. A private chef cooks every meal.</li>
</ul>
<p>Availability is confirmed for your dates with each request.</p>"""),
    dict(type="beige", h2="Shabbat <i>in the chalet</i>", html="""<p>The chef prepares the Shabbat meals and the holidays in the chalet. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your family, Shacharis takes place in your living room.</p>
<p>Strictly kosher, everything served is Chalav Yisrael. The supervision details come in writing with your quote.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us", "Your dates, the number of people and what you want. By WhatsApp or with the form at the bottom of this page. Hebrew-speaking guests are welcome."),
      ("We check the chalet", "Our team in the Alps confirms the chalet for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote for the whole stay, before you commit to anything."),
    ]),
    dict(type="beige", h2="Getting <i>there</i>", html="""<ul>
<li><b>From Lyon-Saint-Exupéry.</b> About 2 h 15 to 2 h 30 by road. Geneva, about 2 h 30.</li>
<li><b>Transfers.</b> Vans with car seats from the airport to the chalet and back, on quote.</li>
<li><b>Land in Lyon with a few hours to spare?</b> <a href="../tours/stopover/">The Stopover</a>: a private 3 hour tour of Jewish Lyon between the plane and the road.</li>
</ul>"""),
    dict(type="faq", h2="The Courchevel chalet: <i>questions</i>", items=[
      ("How much does it cost?", "<span data-prix-tpl='From €{ch3_basse_vente} per week'>From €17,500 per week</span> for the chalet. The final price depends on your dates, the number of people and the services you choose: you receive a written quote before you commit to anything. The stay is quoted and invoiced by our kosher team based in the Alps."),
      ("How many people can stay?", "Five en-suite bedrooms, for 10 to 14 guests."),
      ("Who cooks the meals?", "A private chef cooks kosher meals at the chalet. Our team kashers the kitchen before you arrive."),
      ("Is there a minyan?", "We bring the bochurim and a Sefer Torah to the chalet for Shabbat, on request. Tell us your dates early."),
      ("How do we get to the slopes?", "On foot in five to six minutes, or with the private shuttle from 9 am to 6 pm."),
    ]),
    dict(type="cta", txt="The kosher chalet in Courchevel?", msg="Hello, we would like the kosher chalet in Courchevel. Dates: / Number of people:"),
  ],
  related=[("../kosher-chalets/", "Our kosher chalets"), ("../kosher-chalet-les-deux-alpes/", "The kosher chalet in Les Deux Alpes"), ("../kosher-courchevel/", "Kosher in Courchevel"), ("../kosher-services-french-alps/", "Kosher services in the Alps")],
  source="Sources: our team in the Alps (messages of 16/10/2026) for the chalet, the shuttle and the services.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher chalet in Courchevel", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": {"@type": "Place", "name": "Courchevel"}, "serviceType": "Kosher chalet with private chef, Shabbat and minyan in Courchevel", "url": "https://mishpachatours.com/kosher-chalet-courchevel/", "offers": {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": 17500, "priceCurrency": "EUR", "unitText": "week"}}},
  ticket=True,
  VERIF=[
    "5 en-suite bedrooms, 10 to 14 guests, heated pool indoors and outdoors, hammam, gym, private shuttle 9 am to 6 pm, centre of Courchevel: messages of 16/10/2026 (Mendel), no written contract.",
    "Home cinema, ski room, private parking, south-facing terrace, slopes 5 to 6 min on foot: listing read on 16/10/2026, to confirm with the owner.",
    "Lyon 2 h 15 to 2 h 30, Geneva 2 h 30: estimates, not measured.",
    "Artist's chalet, one artwork per room chosen by the owner, white bedroom / dark tapestried bedroom, ski scenes, former family farm turned into a few chalets: Moshé's voice note of 19/10/2026 relaying the owner's description, no written source.",
  ],
)
