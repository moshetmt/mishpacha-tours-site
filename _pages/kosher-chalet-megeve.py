# -*- coding: utf-8 -*-
# Chalet près de Megève (Mont Blanc valley), page créée le 20/10 (Moshé : « ajoute le chalet Megève sur le site »).
# Source : PDF « configuration twin » de l'agence (16/10, 00-brief/references/2026-10-16-megeve-bibi/) et vocaux de Mendel du 16/10.
# Jamais le nom du chalet, de l'agence ni de Saint-Gervais (décision 16/10) ; photos re-rendues par Gemini (introuvables).
PAGE = dict(
  slug="kosher-chalet-megeve",
  title="Kosher Chalet near Megève, 10 Bedrooms, Mont Blanc",
  desc="A kosher chalet near Megève facing Mont Blanc: ten twin bedrooms, two attic rooms, an adjoining apartment, sauna and jacuzzi. Chef, Shabbat and minyan. One written quote.",
  h1="The Mont Blanc Chalet, near Megève", ital="10 twin bedrooms, sauna and jacuzzi facing Mont Blanc",
  intro="A large chalet in the Mont Blanc valley, a few minutes from Megève, built for several families at once. Ten twin bedrooms, two attic rooms and an adjoining apartment with its own front door. A sauna and a jacuzzi facing Mont Blanc, a shuttle at the foot of the chalet every twenty minutes to the lifts. Our team koshers the kitchen, a chef cooks or kosher meals are delivered, and Shabbat comes with a minyan on request. One request, one written quote.",
  chips=["10 twin bedrooms + 2 attic rooms", "Adjoining apartment", "Sauna, jacuzzi, Mont Blanc", "On written quote"],
  illus="flat-ski.png",
  crumb=("../kosher-chalets/", "Our kosher chalets"),
  wa="33652092301",
  sections=[
    # galerie : posée juste avant le pied par _kit_wp.py (KIT-WP:galerie), jamais sous la bannière (Moshé 19/10)
    dict(type="text", h2="The chalet, <i>in short</i>", html="""<ul>
<li><b>Ground floor.</b> A lounge with a bar, one dining room for everyone, the kitchen we kosher, a ski room, and one twin bedroom at ground level.</li>
<li><b>The apartment.</b> Adjoining the chalet, with its own front door: a living room, its own kitchen, one twin bedroom and one bunk bedroom. Ideal for a family that wants its own space.</li>
<li><b>First floor.</b> Seven twin bedrooms, each with its own shower room, around a wide landing that opens onto a terrace.</li>
<li><b>Under the roof.</b> Two attic rooms, for the teenagers or the staff.</li>
<li><b>Wellness.</b> A sauna and a jacuzzi facing Mont Blanc.</li>
<li><b>Getting to the slopes.</b> A shuttle stops at the foot of the chalet every twenty minutes; the lifts are six to eight minutes away.</li>
<li><b>Kitchen.</b> Kashered by our team before you arrive, included. A chef cooks in the chalet, or kosher meals arrive ready to reheat.</li>
</ul>
<p>Every bedroom has twin beds, so each family arranges its beds as it needs. Availability is confirmed for your dates with each request.</p>"""),
    dict(type="beige", h2="Shabbat <i>in the chalet</i>", html="""<p>The chef prepares the Shabbat meals and the holidays in the chalet, or the meals arrive before candle lighting. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your group, Shacharis takes place in your living room.</p>
<p>Strictly kosher, everything served is Chalav Yisrael. The supervision details come in writing with your quote.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us", "Your dates, the number of families and what you want. By WhatsApp or with the form at the bottom of this page. Hebrew-speaking guests are welcome."),
      ("We check the chalet", "Our team in the Alps confirms the chalet for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote for the whole stay, before you commit to anything."),
    ]),
    dict(type="beige", h2="Getting <i>there</i>", html="""<ul>
<li><b>From Geneva airport.</b> About 1 h 15 by road. Lyon-Saint-Exupéry, about 2 h 15.</li>
<li><b>Transfers.</b> Vans with car seats from the airport to the chalet and back, on quote.</li>
<li><b>Land in Lyon with a few hours to spare?</b> <a href="../tours/stopover/">The Stopover</a>: a private 3 hour tour of Jewish Lyon between the plane and the road.</li>
</ul>"""),
    dict(type="faq", h2="The Mont Blanc Chalet: <i>questions</i>", items=[
      ("How much does it cost?", "The price depends on your dates, the number of people and the services you choose. You receive a written quote before you commit to anything."),
      ("How many people can stay?", "Ten twin bedrooms and two attic rooms, plus the apartment: three or four families under one roof, each with its own bedrooms."),
      ("Is the apartment separate?", "It adjoins the chalet and has its own front door, living room and kitchen. One family can have it to itself."),
      ("Who cooks the meals?", "A chef cooks kosher meals in the chalet, or ready meals are delivered. Our team kashers the kitchen before you arrive."),
      ("Is there a minyan?", "We bring the bochurim and a Sefer Torah to the chalet for Shabbat, on request. Tell us your dates early."),
      ("How do we get to the slopes?", "A shuttle stops at the foot of the chalet every twenty minutes; the lifts are six to eight minutes away."),
    ]),
    dict(type="cta", txt="The Mont Blanc Chalet for your dates?", msg="Hello, we would like the kosher chalet near Megève. Dates: / Number of families:"),
  ],
  related=[("../kosher-chalets/", "Our kosher chalets"), ("../kosher-megeve/", "Kosher in Megève"), ("../kosher-chalet-les-deux-alpes/", "Our chalet in Les Deux Alpes"), ("../kosher-services-french-alps/", "Kosher services in the Alps")],
  source="Sources: our team in the Alps (document and messages of 16/10/2026) for the chalet, the shuttle and the services.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher chalet near Megève", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": {"@type": "Place", "name": "Megève"}, "serviceType": "Kosher chalet with chef or delivered meals, Shabbat and minyan near Megève", "url": "https://mishpachatours.com/kosher-chalet-megeve/"},
  ticket=True,
  VERIF=[
    "Ground floor (lounge and bar, dining room, kitchen, ski room, twin bedroom), apartment (living room, kitchen, twin + bunk bedrooms), 7 twin bedrooms with shower rooms on the first floor around a landing with terrace, 2 attic rooms: agency PDF « configuration twin » of 16/10/2026.",
    "Sauna, jacuzzi facing Mont Blanc, shuttle every 20 min at the foot of the chalet, lifts 6 to 8 min, minyan on request: Mendel, 16/10/2026 (messages and voice notes), no written contract.",
    "Geneva 1 h 15, Lyon 2 h 15: estimates, not measured. Capacity in guests not stated by the agency: the page says « three or four families ».",
  ],
)
