# -*- coding: utf-8 -*-
# Villa Beach à Saint-Tropez (Summer Prestige), page créée le 19/10 sur le texte du gestionnaire et le vocal de Moshé
# (00-brief/references/2026-10-19-villa-beach-st-tropez/, 02-meetings/2026-10-19-audio-moshe-villa-beach-st-tropez.md).
# Nom « Villa Beach » affiché (Moshé 19/10 « oui »), passe par Mendel sous la marque Summer Prestige, chef, Chabbat et minyan comme dans les Alpes.
# Jamais le clocher (église), jamais de prix ; la cave à vins reste hors page ; œuvres d'art = filtrer les très jeunes enfants (en interne, pas sur la page).
PAGE = dict(
  slug="kosher-villa-saint-tropez",
  title="Kosher Villa in Saint-Tropez, Private Beach",
  desc="Villa Beach, a kosher villa on the water in Saint-Tropez: private sand beach, boat garage, 5 bedrooms for 12 guests, heated pool, private chef, Shabbat and a minyan. One written quote.",
  h1="A kosher villa on the water in Saint-Tropez", ital="private beach, boat, chef and Shabbat",
  intro="Villa Beach sits with its feet in the water, in the gulf of Saint-Tropez. It is the only villa for rent in Saint-Tropez with a private sand beach and its own boat garage with a launching ramp. Five bedrooms and five bathrooms for 12 guests, a heated pool and a jacuzzi in the garden, a hammam and a sauna over the sea. Our team koshers the kitchen, a private chef cooks every meal, and Shabbat is kept in the villa with a minyan if you wish.",
  chips=["5 bedrooms, 12 guests", "Private sand beach, boat garage", "Heated pool, jacuzzi", "On written quote"],
  illus="flat-stopover.png",
  crumb=("../summer-in-the-alps-jewish-families/", "Summer"),
  wa="33652092301",
  sections=[
    # galerie : posée sous la bannière par _kit_wp.py (KIT-WP:galerie)
    dict(type="text", h2="The villa, <i>in short</i>", html="""<ul>
<li><b>Three houses.</b> The main villa, a guest house across the garden and the caretaker's lodge: 520 m² of house on 1 600 m² of land, 12 guests in five bedrooms with five bathrooms.</li>
<li><b>Sea view.</b> The four bedrooms of the main villa look at the sea. A vast living room and a very large panoramic terrace overlook the water and the village of Saint-Tropez.</li>
<li><b>Wellness.</b> A heated 25 m² pool and a jacuzzi in the garden, a hammam and a sauna over the sea.</li>
<li><b>The beach.</b> A private sand beach at the foot of the villa and a boat garage with its own launching ramp, the only ones for rent in Saint-Tropez.</li>
<li><b>Quiet.</b> The villa is calm: the only sound is the sea. A concierge is on site all year.</li>
<li><b>Kitchen.</b> Kashered by our team before you arrive, included. A private chef cooks every meal.</li>
</ul>
<p>Availability is confirmed for your dates with each request.</p>"""),
    dict(type="beige", h2="Shabbat <i>by the sea</i>", html="""<p>The chef prepares the Shabbat meals and the holidays in the villa. For a minyan, we bring the bochurim and a Sefer Torah: with the men of your family, the minyan is at home, on the terrace over the water. The synagogue of Saint-Tropez is a walk of about 30 to 40 minutes along the sea, for those who prefer to go.</p>
<p>Strictly kosher, everything served is Chalav Yisrael. The supervision details come in writing with your quote. Summer weeks and Pesach are both possible: tell us your dates.</p>"""),
    dict(type="text", h2="The sea, <i>from the garden</i>", html="""<ul>
<li><b>Your own boat.</b> A rigid inflatable boat is at your disposal, with access to the pontoon. The port of Saint-Tropez is three minutes away by boat.</li>
<li><b>On the water.</b> Pedal boat, canoe, paddle board, Seabob and snorkelling masks are in the boat garage, ready to use.</li>
<li><b>Under the water.</b> The villa faces a marine reserve: Mediterranean fish a few metres from the beach. This corner of the gulf is known for its calm sea.</li>
<li><b>Around.</b> A sailing club 500 metres away. Bicycles take you along the protected cycle path to the port of Saint-Tropez in eight minutes.</li>
</ul>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us", "Your dates, the number of people and what you want. By WhatsApp or with the form at the bottom of this page. Hebrew-speaking guests are welcome."),
      ("We check the villa", "Our team confirms the villa for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote for the whole stay, before you commit to anything."),
    ]),
    dict(type="beige", h2="Getting <i>there</i>", html="""<ul>
<li><b>From Nice airport.</b> About 1 h 30 to 2 h by road, depending on the season. Toulon-Hyères airport, about 1 h.</li>
<li><b>Transfers.</b> Vans with car seats from the airport to the villa and back, on quote.</li>
<li><b>By boat.</b> From the pontoon of the villa, the port of Saint-Tropez is three minutes away.</li>
</ul>"""),
    dict(type="faq", h2="Villa Beach: <i>questions</i>", items=[
      ("How much does it cost?", "The price depends on your dates, the number of people and the services you choose. You receive a written quote before you commit to anything."),
      ("How many people can stay?", "Five bedrooms and five bathrooms, for 12 guests, between the main villa and the guest house."),
      ("Who cooks the meals?", "A private chef cooks kosher meals at the villa. Our team kashers the kitchen before you arrive."),
      ("Is there a minyan?", "We bring the bochurim and a Sefer Torah to the villa for Shabbat, on request. The synagogue of Saint-Tropez is also within walking distance along the sea."),
      ("Is the beach really private?", "Yes. A private sand beach at the foot of the villa, with a boat garage and a launching ramp. The sea in front of the villa is a marine reserve."),
      ("Can we come for Pesach?", "Yes. Pesach and the summer weeks are both possible. Tell us your dates early."),
    ]),
    dict(type="cta", txt="Villa Beach in Saint-Tropez?", msg="Hello, we would like the kosher villa in Saint-Tropez. Dates: / Number of people:"),
  ],
  related=[("../summer-in-the-alps-jewish-families/", "Summer in the Alps"), ("../kosher-chalets/", "Our kosher chalets in the Alps"), ("../kosher-van-transfers/", "Van transfers"), ("../plan-your-trip/", "Plan your trip")],
  source="Sources: the villa's manager (description received on 19/10/2026) and our team (same day) for the houses, the beach and the services.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher villa in Saint-Tropez", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": {"@type": "Place", "name": "Saint-Tropez, France"}, "description": "Villa Beach, a kosher villa on the water in Saint-Tropez: private beach, boat garage, five bedrooms for 12 guests, private chef, Shabbat and minyan. Written quote.", "url": "https://mishpachatours.com/kosher-villa-saint-tropez/"},
  ticket=True,
  VERIF=[
    "Private beach, boat garage and ramp, 25 m² heated pool, jacuzzi, hammam and sauna, 5 bedrooms / 5 bathrooms / 12 guests, 520 m² on 1 600 m², marine reserve, sailing club 500 m, bikes 8 min to the port: manager's description received on 19/10/2026, no written contract.",
    "Synagogue of Saint-Tropez at 30 to 40 min on foot along the sea, concierge all year, terrace about 300 m², art works inside (filter families with very young children), Pesach possible: Moshé's voice note of 19/10/2026.",
    "Nice 1 h 30 to 2 h, Toulon-Hyères 1 h: estimates, not measured.",
    "The manager's text mentions the hotel Cheval Blanc 5 min by bike: left out (no third-party names).",
  ],
)
