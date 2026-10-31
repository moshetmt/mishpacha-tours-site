# -*- coding: utf-8 -*-
# 30/10 : page « Ailleurs sur demande » (Autriche, Amérique du Nord, toute station hors liste). Décision Moshé 30/10 :
# AUCUN MONTANT, AUCUN SEUIL DE BUDGET, jamais « à partir de », jamais « sur mesure » chiffré. Même interlocuteur WhatsApp.
PAGE = dict(
  slug="kosher-ski-anywhere",
  title="Kosher Ski Anywhere: Chef, Shabbat, Minyan",
  desc="Kitzbühel, St. Anton, Whistler, Aspen or any resort not on our list: tell us where, we organise a private kosher chef, Shabbat, minyan and transfers.",
  h1="Kosher ski, anywhere", ital="tell us where, we organise",
  intro="Austria, North America, or a resort we have not listed yet: the formula is the same. A private kosher chef travels with you and cooks in your chalet, Shabbat and the holidays are set, and we organise the minyan and the transfers, with the same WhatsApp contact as for the Alps.",
  chips=["Austria, North America, and beyond", "A private chef who travels with you", "Shabbat, holidays, minyan on request", "Checked 30 October 2026"],
  illus="flat-ski.png",
  crumb=("../alps/", "The Alps, strictly kosher"),
  wa="33652092301",
  sections=[
    dict(type="text", h2="What we organise <i>anywhere</i>", html="""<ul>
<li><b>A private kosher chef who travels with you.</b> Our team based in the Alps sends a chef to your chalet or apartment, makes the kitchen kosher and cooks every meal of the week on site. The kosher shopping travels with the chef or is bought from the nearest Jewish community.</li>
<li><b>Shabbat and the holidays.</b> Shabbat meals, challot and wine set before candle lighting; Hanukkah, Purim, Pesach or Sukkot in the mountains. Nothing is prepared on Shabbat or on a holiday.</li>
<li><b>A minyan.</b> Where a synagogue or a Chabad house exists in the resort, we give you the times. Where none does, a minyan is built from the families who write to us for the same week, with a Sefer Torah on request.</li>
<li><b>Transfers.</b> From the nearest airport to the door of the chalet, on days that respect Shabbat and the holidays.</li>
<li><b>The chalet or apartment.</b> We find it with you, or we work with the one you have already booked.</li>
<li><b>One contact.</b> The same WhatsApp number as for the Alps, from the first message to the last transfer.</li>
</ul>
<p>Strictly kosher. Our kosher team based in the Alps cooks under the Chabad network of the Alps. Detail of each service: <a href="../kosher-services-french-alps/">kosher services in the Alps</a>.</p>"""),
    dict(type="beige", h2="Where we <i>go</i>", html="""<ul>
<li><b>Austria.</b> Kitzbühel, St. Anton am Arlberg, Lech, Ischgl, Sölden, Saalbach: the kosher shops of Vienna and the Chabad houses of Austria help with the shopping; the chef does the rest.</li>
<li><b>North America.</b> Whistler, Aspen, Vail, Park City, Mont-Tremblant: a chalet, a chef and Shabbat with the same standard as in the Alps, with the kosher shopping bought locally.</li>
<li><b>The rest of Switzerland and Italy.</b> A resort not on our list, such as Andermatt, Engelberg, Laax or Madonna di Campiglio: same formula, chef and Shabbat.</li>
<li><b>Anywhere else.</b> Tell us the resort. If we cannot do it well, we say so.</li>
</ul>"""),
    dict(type="text", h2="Courchevel and the French Alps, <i>where everything is in place</i>", html="""<p>Before you fly further, look at what already exists in the French Alps. In <a href="../kosher-courchevel/">Courchevel</a>, <a href="../kosher-megeve/">Megève</a>, <a href="../kosher-val-thorens/">Val Thorens</a> and <a href="../kosher-les-deux-alpes/">Les Deux Alpes</a>, our <a href="../kosher-chalets/">private kosher chalets</a>, the chef, the delivered meals, the minyan with the Chabad network of the Alps and the transfers from Lyon and Geneva are already in place, season after season. Everything we organise elsewhere starts from there.</p>"""),
    dict(type="steps", h2="How it <i>works</i>", items=[
      ("Tell us where", "The resort, your dates, the number of people, where you sleep, and what you need: a chef, Shabbat, a holiday, a minyan, transfers. By WhatsApp or with the form at the bottom of this page."),
      ("We check and put it together", "We check with our team in the Alps what is possible for your dates and your resort: chef, kitchen, shopping, minyan, the chef's travel. One contact from start to finish."),
      ("You get one quote", "The price depends on the destination, the dates, the number of people and the menu. You receive a written quote before you commit to anything."),
    ]),
    dict(type="faq", h2="Kosher anywhere: <i>questions</i>", items=[
      ("Which destinations do you cover?", "Austria, North America and any ski resort not on our list, in addition to the resorts of France, Switzerland and Italy already on this site. Tell us the resort and we tell you what is feasible."),
      ("How does the kosher shopping work far from the Alps?", "Part of it travels with the chef, part is bought from the nearest kosher shop or Jewish community. We plan it before you leave, and the supervision details come with your quote."),
      ("Can you organise a minyan in a resort with no synagogue?", "A minyan depends on how many families are there that week. Give us your dates early and we group the families who write to us, with a Sefer Torah on request."),
      ("How much does it cost?", "It depends on the destination, the dates, the number of people and the menu. You receive a written quote before you commit. We publish no price."),
      ("Do you work in summer as well?", "Yes. Walking, lakes, festivals: the services are the same in summer, chef, Shabbat, holidays, minyan."),
      ("Who supervises the food?", "Our kosher team based in the Alps cooks under the Chabad network of the Alps. The supervision details come with your quote."),
    ]),
    dict(type="cta", txt="Kosher somewhere else this season?", msg="Hello, we are going to [resort], [country]. Dates: / Number of people: / We need (chef, Shabbat, holiday, minyan, transfers):"),
  ],
  related=[("../alps/", "The Alps, strictly kosher"), ("../kosher-services-french-alps/", "Kosher services in the Alps, in detail"), ("../kosher-courchevel/", "Kosher in Courchevel"), ("../kosher-chalets/", "Our private kosher chalets"), ("../kosher-ski-holidays-french-alps/", "Kosher ski holidays in the Alps"), ("../kosher-verbier/", "Kosher in Verbier"), ("../lyon-gateway-to-the-alps-kosher/", "Lyon, the gateway to the Alps")],
  source="Sources: our team in the Alps for the services. Resort names are examples, not partnerships.",
  jsonld={"@context": "https://schema.org", "@type": "Service", "name": "Kosher ski stays outside the Alps", "provider": {"@id": "https://mishpachatours.com/#organization"}, "areaServed": [{"@type": "Country", "name": "Austria"}, {"@type": "Country", "name": "Canada"}, {"@type": "Country", "name": "United States"}, {"@type": "Country", "name": "Switzerland"}, {"@type": "Country", "name": "Italy"}], "serviceType": "Private kosher chef who travels with the family, Shabbat and holiday meals, minyan and transfers in any ski resort", "url": "https://mishpachatours.com/kosher-ski-anywhere/"},
  ticket=True,
  VERIF=[
    "Decision Moshe 30/10 (after Mendel's audios): page with NO amount, NO budget threshold, no 'from', no priced 'tailor-made'. Mendel's '> 100 000 EUR' figure stays internal.",
    "Chabad houses in Austria: Vienna certain; Innsbruck and Salzburg not checked on 30/10, hence the generic wording 'the Chabad houses of Austria'. Kosher shops in Vienna: known (2nd district).",
    "North American and Austrian resort names are examples only, no partnership and no local kosher check done on 30/10.",
    "'Chef who travels with you' and the chef's travel in the quote: Mendel 30/10 ('il faut etre partout', chef at a cost), confirm with Mendel the way the chef's flights are handled before the first request."
  ],
)
