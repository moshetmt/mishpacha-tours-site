# -*- coding: utf-8 -*-
# Page cible du mot-cle hebreu « טיסות לליון » (480 recherches/mois, etude du 08/10). L'EN est la source, la HE la cible.
PAGE = dict(
  slug="flights-to-lyon",
  title="Flights to Lyon and the road to the ski resorts",
  desc="Flights to Lyon-Saint-Exupéry, the airport for Val Thorens, Courchevel and Alpe d'Huez: direct flights from Tel Aviv, drive times to the resorts, kosher shopping, and what to do with three hours in Lyon.",
  h1="Flights to Lyon", ital="the airport for the French Alps, and what to do between the plane and the slopes",
  intro="Lyon-Saint-Exupéry is the airport for the Tarentaise and the Grenoble side: Val Thorens, Courchevel, Méribel, Alpe d'Huez and Les Deux Alpes are two to three hours away by road. Direct flights from Tel Aviv are operated by El Al and Transavia, one to two a week depending on the season, about four and a half hours. This page gives the flights, the drive times, where to buy kosher before you climb, and how to use a few spare hours in Lyon. We sell no flights and no transfers: we guide in Lyon, and our kosher team organises your week in the resort.",
  chips=["Direct flights from Tel Aviv: El Al, Transavia", "Val Thorens 2 h 30, Courchevel 2 h 10", "Kosher shops in Lyon, not at the airport", "Checked 8 October 2026"],
  illus="flat-stopover.png",
  crumb=("../alps/", "The French Alps, strictly kosher"),
  wa="33652092301",
  sections=[
    dict(type="text", h2="Direct flights <i>to Lyon</i>", html="""<ul>
<li><b>From Tel Aviv.</b> El Al and Transavia France fly non-stop to Lyon; route listings give El Al on Tuesdays, Thursdays and Sundays in season, and one to two flights a week in total depending on the month. Flight time about 4 h 30 to 5 h. Check the airlines' schedules for your dates: frequencies change by season.</li>
<li><b>From the United States and the United Kingdom.</b> No non-stop flight from New York; connect through Paris, Amsterdam or Frankfurt. From London, non-stop flights with several airlines.</li>
<li><b>Geneva instead of Lyon?</b> Geneva is closer for Megève, Chamonix and the Portes du Soleil. Lyon is closer for Val Thorens, Courchevel, Méribel, Alpe d'Huez and Les Deux Alpes, and it has certified kosher shops on the way.</li>
</ul>"""),
    dict(type="beige", h2="From the airport <i>to your resort</i>", html="""<p>Typical drive times from Lyon-Saint-Exupéry, without traffic, as listed by j2ski.com. On a Saturday in February, or in snow, add an hour or more.</p>
<ul>
<li><b>Chamonix, Méribel:</b> about 2 h</li>
<li><b>Courchevel, Megève, Les Gets, Les Deux Alpes:</b> about 2 h 10</li>
<li><b>Morzine, Alpe d'Huez:</b> about 2 h 20</li>
<li><b>Val Thorens:</b> about 2 h 30</li>
<li><b>Tignes, Val d'Isère:</b> about 2 h 40</li>
</ul>
<p>Shuttles run in winter from the airport (Altibus, Ben's Bus and others); private transfers take families door to door. Details, shuttle seasons and the kosher shopping list: <a href="../lyon-gateway-to-the-alps-kosher/">Lyon, the gateway to the Alps</a>.</p>"""),
    dict(type="text", h2="Three hours in Lyon <i>between the plane and the slopes</i>", html="""<p>Most flights from Tel Aviv land in the morning. Your transfer drops you in Vieux Lyon, your bags stay in the van, and you walk into the Jewish story of the city with your guide: rue Juiverie, then inside the Grande Synagogue on quai Tilsitt, closed to visitors outside the Heritage Days. Three hours later, you leave for the resort on schedule. 390 € per group of 1 to 5, in English, French or Spanish: <a href="../tours/stopover/">the Stopover</a>.</p>
<p>Before you climb, Lyon and Villeurbanne have certified kosher groceries and butchers; the resorts have almost none. What to buy and where: <a href="../lyon-gateway-to-the-alps-kosher/">kosher shopping in Lyon</a>. And in the resort itself, our kosher team delivers meals, sets Shabbat and builds a minyan: <a href="../alps/">the French Alps, strictly kosher</a>.</p>"""),
    dict(type="steps", h2="A typical <i>arrival</i>", items=[
      ("Land in the morning", "Send us your landing time and the time your transfer must leave. We build the three hours around it."),
      ("Shop and walk", "Kosher groceries in Lyon, then the Stopover tour in Vieux Lyon with the Grande Synagogue."),
      ("Drive up, set table", "Your transfer takes you to the resort; if you asked for it, meals or the chef are ready for your first evening."),
    ]),
    dict(type="text", h2="Shabbat <i>in Lyon</i>", html="""<p>If your flight lands on Friday, or you leave on Sunday, Lyon has seven Chabad houses, two historic synagogues and certified kosher restaurants for a Shabbat before or after the mountain: <a href="../shabbat-in-lyon/">Shabbat in Lyon</a>.</p>"""),
    dict(type="photos", items=[("stock/lyon-partdieu.jpg", "Lyon Part-Dieu"), ("c-synagogue-7.jpg", "The Grande Synagogue, quai Tilsitt"), ("stock/traboule-1.jpg", "A Renaissance gallery, rue Juiverie"), ("stock/alpes-ski.jpg", "A piste above Megève")]),
    dict(type="faq", h2="Flights to Lyon: <i>questions</i>", items=[
      ("Is there a direct flight from Tel Aviv to Lyon?", "Yes. El Al and Transavia France operate non-stop flights, one to two a week depending on the season, about 4 h 30. Check the airlines for your dates."),
      ("Which airport for Val Thorens?", "Lyon-Saint-Exupéry, about 2 h 30 by road. Geneva and Chambéry are alternatives; Lyon is the one with kosher shops on the way."),
      ("Can we buy kosher food at the airport?", "No. The certified shops are in Lyon and Villeurbanne, 30 minutes from the airport. Or ask us to deliver meals to your apartment in the resort."),
      ("What if our flight is delayed?", "Tell us your landing time and your onward departure time when you book the Stopover; we build the three hours around your schedule, and we shorten the walk if needed."),
      ("Do you sell flights or transfers?", "No. You book them yourself. We guide in Lyon, and our kosher team organises meals, Shabbat and a minyan in the resort."),
    ]),
    dict(type="cta", txt="Landing in Lyon on the way to the Alps?", msg="Hello, we land in Lyon on the way to the Alps. Landing time: / Resort: / Dates: / Number of people: / We would like (Stopover tour, kosher meals in the resort, chef, Shabbat):"),
  ],
  related=[("../tours/stopover/", "The Stopover, 3 hours in Jewish Lyon"), ("../lyon-gateway-to-the-alps-kosher/", "Lyon, the gateway to the Alps: drive times and shopping"), ("../alps/", "The French Alps, strictly kosher"), ("../kosher-vacation-french-alps/", "A kosher vacation in the French Alps"), ("../shabbat-in-lyon/", "Shabbat in Lyon")],
  source="Sources: flightconnections.com and lyonaeroports.com for the flights; j2ski.com and alps2alps.com for drive times.",
  jsonld=None,
  ticket=True,
  VERIF=["Flight frequencies TLV-LYS: flightconnections.com (El Al Tue/Thu/Sun) and lyonaeroports.com; sources disagree on weekly frequency (1 to 2); check before publication of any schedule.", "No non-stop New York-Lyon: as of October 2026, to re-check each season.", "Drive times: j2ski.com, alps2alps.com.", "'Most flights from Tel Aviv land in the morning': to confirm on the current schedule."],
)
