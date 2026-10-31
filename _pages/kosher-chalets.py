# -*- coding: utf-8 -*-
# Page « Chalets » du menu (19/10, audit du parcours chalet). Les deux cartes et le bandeau sont posés par _kit_wp.py
# dans le marqueur KIT-WP:hub (après la section d'intro). Recherche Google « kosher chalet » ≈ 0 : page de navigation.
PAGE = dict(
  slug="kosher-chalets",
  title="Kosher Chalets in the Alps: Chef, Shabbat, Minyan",
  desc="Our kosher chalets in the Alps, in Les Deux Alpes, Courchevel, Megève and Val Thorens: a private chef, Shabbat and a minyan in the chalet. One request, one written quote.",
  h1="Our kosher chalets", ital="in Les Deux Alpes, Courchevel, Megève and Val Thorens",
  intro="Our chalets, everything kosher taken care of: Les Deux Alpes, Courchevel, near Megève, and Val Thorens with a ski path at the door. The kitchen is kashered, a chef cooks or meals are delivered, a minyan comes on request. One programme, one quote.",
  chips=["Les Deux Alpes and Courchevel", "Private chef or delivered meals", "Shabbat and minyan in the chalet", "Availability confirmed for your dates"],
  illus="flat-ski.png",
  crumb=("../alps/", "The Alps, strictly kosher"),
  wa="33652092301",
  sections=[
    dict(type="beige", h2="What every chalet stay <i>includes</i>", html="""<ul>
<li><b>A kosher kitchen.</b> Our team koshers the kitchen before you arrive. Everything served is Chalav Yisrael.</li>
<li><b>A private chef or delivered meals.</b> The chef cooks in the chalet, or ready meals arrive three times a week.</li>
<li><b>Shabbat and the holidays.</b> The meals are prepared, and a minyan with a Sefer Torah comes to the chalet on request.</li>
<li><b>Transfers.</b> From Lyon or Geneva airport to the chalet and back, with car seats.</li>
</ul>
<p>Already have a place to stay? <a href="../kosher-services-french-alps/">Kosher services in your resort</a>.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Choose a chalet", "Les Deux Alpes, Courchevel, Megève or Val Thorens; two families can take both chalets in Les Deux Alpes. Not sure? Tell us your dates and your group, we advise you."),
      ("We confirm the dates", "Our team in the Alps checks the chalet for your dates, then the chef, the transfers and the minyan."),
      ("You get one programme", "A day-by-day programme and one written quote, before you commit to anything."),
    ]),
    dict(type="faq", h2="Kosher chalets: <i>questions</i>", items=[
      ("Which chalet should we choose?", "In Les Deux Alpes, the 15-bed chalet has 6 bedrooms plus a nursery, two minutes from the slopes, and the Slope Chalet has 6 bedrooms and 13 beds with the skis on at the door; the two are five minutes apart, for four families. Courchevel has 5 en-suite bedrooms, heated pools and a private shuttle, in the 3 Valleys. Val Thorens has 3 en-suite bedrooms for up to 10 guests, with a ski path at the door, also in the 3 Valleys."),
      ("How much does a chalet cost?", "For a week in the chalet: Val Thorens <span data-prix-tpl='from €{ch5_basse_vente}'>from €9,500</span>, Les Deux Alpes <span data-prix-tpl='from €{ch2_basse_vente}'>from €13,000</span>, Courchevel <span data-prix-tpl='from €{ch3_basse_vente}'>from €17,500</span>, near Megève <span data-prix-tpl='from €{ch4_basse_vente}'>from €23,500</span>. The price for your dates and your services comes in one written quote. The stay is quoted and invoiced by our kosher team based in the Alps."),
      ("Are the chalets available for our dates?", "Availability is confirmed with each request. Send your dates and we check the same day."),
      ("Is everything strictly kosher?", "Yes. The kitchen is kashered by our team and everything served is Chalav Yisrael. The supervision details come in writing with your quote."),
      ("Can we have a minyan?", "Yes, on request: we bring the bochurim and a Sefer Torah to the chalet for Shabbat."),
    ]),
    dict(type="cta", txt="Which chalet for your dates?", msg="Hello, we are looking for a kosher chalet. Dates: / Number of people: / Les Deux Alpes, Courchevel, Megève or Val Thorens:"),
  ],
  related=[("../kosher-chalet-les-deux-alpes/", "The kosher chalet in Les Deux Alpes"), ("../kosher-slope-chalet-les-deux-alpes/", "The Slope Chalet in Les Deux Alpes"), ("../kosher-chalet-courchevel/", "The kosher chalet in Courchevel"), ("../kosher-chalet-megeve/", "The Mont Blanc Chalet near Megève"), ("../kosher-chalet-val-thorens/", "The Val Thorens Chalet"), ("../alps/", "The Alps, strictly kosher"), ("../kosher-services-french-alps/", "Kosher services in the Alps")],
  source="Sources: our team in the Alps (messages of 09/10, 14/10 and 16/10/2026).",
  jsonld={"@context": "https://schema.org", "@type": "ItemList", "name": "Kosher chalets in the Alps", "itemListElement": [
    {"@type": "ListItem", "position": 1, "url": "https://mishpachatours.com/kosher-chalet-les-deux-alpes/", "name": "Kosher chalet in Les Deux Alpes"},
    {"@type": "ListItem", "position": 2, "url": "https://mishpachatours.com/kosher-slope-chalet-les-deux-alpes/", "name": "The Slope Chalet in Les Deux Alpes"},
    {"@type": "ListItem", "position": 3, "url": "https://mishpachatours.com/kosher-chalet-courchevel/", "name": "Kosher chalet in Courchevel"},
    {"@type": "ListItem", "position": 4, "url": "https://mishpachatours.com/kosher-chalet-megeve/", "name": "Kosher chalet near Megève"},
    {"@type": "ListItem", "position": 5, "url": "https://mishpachatours.com/kosher-chalet-val-thorens/", "name": "Kosher chalet in Val Thorens"}]},
  ticket=True,
  VERIF=["Facts of each chalet: see the five chalet modules.", "Delivered meals three times a week: Mendel, 15/10/2026."],
)
