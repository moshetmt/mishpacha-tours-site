# -*- coding: utf-8 -*-
PAGE = dict(
  slug="chrd-lyon",
  title="CHRD Lyon: Resistance and deportation museum, visit",
  desc="The CHRD in Lyon, in the former Gestapo headquarters: what you see, the Jewish history it tells, hours, prices, tram access and our private guided visit.",
  h1="The CHRD in Lyon", ital="the Resistance and deportation museum, in the former Gestapo headquarters",
  intro="The Centre d'histoire de la résistance et de la déportation stands in the former military medical school of Lyon, where Klaus Barbie's Gestapo had its headquarters. It tells the story of Lyon at war: Resistance, repression, deportation and the persecution of the Jews. It is open Wednesday to Sunday.",
  chips=["14 avenue Berthelot, 69007 Lyon", "Open Wednesday to Sunday", "Tram T2, Centre Berthelot", "Checked 7 October 2026"],
  illus="flat-memory.png",
  crumb=("../jewish-lyon-guide/", "Jewish Lyon guide"),
  sections=[
    dict(type="text", h2="What you <i>see</i>",
      html="<p>The building is part of the story. It housed the École du service de santé militaire, and under the Occupation it became the seat of the Gestapo in Lyon, under Klaus Barbie. The museum has been installed there since the 1990s.</p>"
           "<p>The permanent exhibition follows the six years of war in Lyon through objects, photographs, archives and recorded testimonies. It covers daily life under the Occupation, the antisemitic policies, the Resistance and the repression. It also includes reconstructions, among them a resistance fighter's apartment with its clandestine printing press.</p>"),
    dict(type="beige", h2="The Jewish <i>dimension</i>",
      html="<p>Jewish history runs through the visit. These are the threads your guide follows.</p>"
           "<ul><li><b>Persecution and deportation.</b> The exhibition shows the antisemitic policies of the Occupation years and the deportation that followed.</li>"
           "<li><b>Izieu.</b> The museum presents testimonies from the Barbie trial of 1987, among them the account of the head of the children's home of Izieu. Our page on the <a href='../maison-izieu/'>Maison d'Izieu</a> tells that story.</li>"
           "<li><b>Rue Sainte-Catherine.</b> On 9 February 1943, Barbie's men arrested 86 people at the UGIF office, 12 rue Sainte-Catherine, in the 1st arrondissement. Your guide links this raid to the museum's account of the Gestapo in Lyon. The street is also on our <a href='../tours/jewish-lyon/'>Jewish Lyon tour</a>.</li>"
           "<li><b>Witnesses.</b> The exhibition draws on testimonies and objects given by former resistance fighters and deportees.</li></ul>"),
    dict(type="photos", items=[("c-chrd-1.jpg", "The CHRD, avenue Berthelot"), ("stock/chrd-1.jpg", "A reconstructed apartment, Lyon in the war"), ("stock/chrd-3.jpg", "Reconstruction of the Croix-Rousse square"), ("stock/chrd-4.jpg", "The staging of the Lyon in the war exhibition"), ("stock/chrd-7.jpg", "A liaison agent's satchel, Génération 40 collection")]),
    dict(type="lieux", h2="Hours, prices and <i>access</i>", items=[
      ("Centre d'histoire de la résistance et de la déportation", "14 avenue Berthelot, 69007 Lyon", "04 72 73 99 00",
       "Wednesday to Sunday 10:00 to 18:00. Ticket office closes at 17:15. On the first Wednesday of the month the museum opens at 11:00. Permanent exhibition: 6 € full rate, 4 € reduced rate (ages 18 to 25 and some museum cards), free under 18. With a temporary exhibition: 8 € and 6 €. Audioguide 1 €. Guided tours cost 2 € to 6 € per person on top of the entry. Tram T2 to Centre Berthelot, metro A to Perrache or metro B to Jean Macé."),
    ], source="Source: chrd.lyon.fr, practical information page, read on 7 October 2026. Hours and prices change: check before you go."),
    dict(type="map", h2="On the <i>map</i>", points=[("CHRD", "14 avenue Berthelot, 69007 Lyon")], note="1 place on the map. Tap the marker for the address and directions."),
    dict(type="steps", h2="How to <i>visit</i>", items=[
      ("Pick a day the museum is open", "The museum is closed on Monday and Tuesday. We do not guide on Shabbat or on Jewish holidays, so our visits run from Wednesday to Friday morning, or on Sunday."),
      ("Book a private guide", "The museum sells guided tours, and group visits need a reservation. Our private visit follows the Jewish history of Lyon through the exhibition and answers your questions on the spot. See the <a href='../tours/memory-chrd/'>Memory: CHRD tour</a>."),
      ("Allow your time", "The museum publishes no recommended duration. Our visit takes about 2 hours 30. We plan the pace with your group, and with children in particular."),
      ("Keep it on its own day", "We never combine the CHRD and the <a href='../montluc-prison-lyon/'>Montluc memorial</a> on the same day. Each carries enough history for a full visit."),
    ]),
    dict(type="faq", h2="Questions <i>we get</i>", items=[
      ("Can we do the CHRD and Montluc on the same day?", "No. We book them as two separate visits on two different days. Each one carries enough history and weight on its own."),
      ("How long does a visit take?", "The museum publishes no duration. Our private visit takes about 2 hours 30."),
      ("Is the CHRD suitable for children?", "The museum publishes no recommended age on the pages we read, and admission is free under 18. Tell us the ages in your group and we adapt the route and the words."),
      ("Can I visit in English?", "Our private visit runs in English, French or Spanish. The languages of the museum's own guided tours are not published: ask the museum."),
      ("How do I get there?", "Take tram T2 to Centre Berthelot. Metro A to Perrache and metro B to Jean Macé also serve the area. The museum lists a car park, LPA Berthelot, and a Vélo'v station at Centre Berthelot."),
    ]),
    dict(type="cta", txt="Want a private visit of the CHRD?", msg="Hello, I would like to ask about the Memory tour, CHRD. Dates: / Number of people: / Preferred language:"),
  ],
  related=[("../tours/memory-chrd/", "Memory: the CHRD, private visit"), ("../montluc-prison-lyon/", "Montluc prison memorial in Lyon"), ("../maison-izieu/", "Maison d'Izieu"), ("../jewish-history-lyon/", "Jewish history of Lyon")],
  source="Sources: chrd.lyon.fr; lyon.fr (page on the CHRD); Mémorial de la Shoah and en.wikipedia.org (rue Sainte-Catherine roundup).",
  jsonld={"@context": "https://schema.org", "@type": "Museum", "name": "Centre d'histoire de la résistance et de la déportation",
          "url": "https://www.chrd.lyon.fr/", "telephone": "+33 4 72 73 99 00",
          "address": {"@type": "PostalAddress", "streetAddress": "14 avenue Berthelot", "postalCode": "69007", "addressLocality": "Lyon", "addressCountry": "FR"}},
  ticket=True,
  VERIF=[
    "Prices from chrd.lyon.fr practical page, 7 October 2026: 6 / 4 permanent, 8 / 6 combined with a temporary exhibition, audioguide 1 €, guided tours 2-6 € per person plus entry, free under 18, reduced 18-25. lyon.fr shows 8 / 6 as the base price in one search snippet: the official page and lyon.fr's own page agree on 6 / 4. Prices change.",
    "Hours: Wed-Sun 10:00-18:00, ticket office closes 17:15 (chrd.lyon.fr). First-of-month exception conflicts: chrd.lyon.fr says first Wednesday at 11:00, lyon.fr says first Friday at 10:30. The official site is used. Closure of 7 October 2026 morning (notice on the homepage) is not repeated.",
    "Phone 04 72 73 99 00: lyon.fr / tourism listings (secondary). Not read on chrd.lyon.fr.",
    "Access T2 Centre Berthelot, metro A Perrache, metro B Jean Macé, LPA Berthelot, Vélo'v: chrd.lyon.fr practical page and lyon.fr.",
    "Gestapo headquarters under Barbie in the former École du service de santé militaire: chrd.lyon.fr homepage ('ancien siège de la Gestapo') and lyon.fr. 'Since the 1990s': secondary sources (inauguration 1992), exact date not stated.",
    "Exhibition content (antisemitic policies, Resistance, repression, resistance fighter's apartment with printing press, objects and testimonies of former resistance fighters and deportees, Barbie trial testimonies including the head of the Izieu home): secondary summaries (lyon.fr, CHRD press material found by search). Not read on the current permanent-exhibition page (404). To confirm with the museum, and confirm that the current layout still has these elements.",
    "Rue Sainte-Catherine: 9 February 1943, 86 arrested, UGIF office at 12 rue Sainte-Catherine, Barbie: Mémorial de la Shoah and en.wikipedia (secondary). The sentence saying our guide links it to the museum is our tour design, not a museum claim.",
    "Recommended duration, age recommendation and languages of the museum's guided tours: not published. Our 2h30: the Memory tour page.",
    "'Closed on Monday and Tuesday' is deduced from 'Wednesday to Sunday'. Our visit days (Wednesday to Friday morning, Sunday) follow the operator rule 'no tour on Shabbat or holidays'. Operator to confirm.",
    "Photos: stock/chrd-7.jpg is the satchel of liaison agent Andrée Merle (Commons title), not a deportee's. The Memory tour page /tours/memory-montluc-neveh-shalom/ captions it 'A deportee's satchel, CHRD': wrong, to correct. CHRD photos credits in CREDITS.md (CC0 and CC BY-SA 4.0, Pierre Verrier for chrd-1, 3 and 4 of stock).",
  ],
)
