# -*- coding: utf-8 -*-
PAGE = dict(
  slug="about",
  title="About Mishpacha Tours, Jewish Tours of Lyon",
  desc="Private Jewish tours of Lyon led by a Jewish, observant, state-licensed guide. Strictly kosher, shomer shabbat, prices per group. Who we are and how we work.",
  h1="About Mishpacha Tours",
  ital="a Jewish guide, for Jewish travellers",
  intro="Mishpacha means family. We guide Jewish travellers through Lyon the way you would show your own city to cousins from abroad: in private, at your pace, with nothing about kashrut or Shabbat to explain first.",
  chips=["Licensed guide-conférencier", "Jewish and observant", "English, French, Spanish", "Lyon, France"],
  illus="line-storyteller.png",
  crumb=None,
  sections=[
    dict(type="text", h2="Who guides <i>you</i>", html="""<p>Your guide is Jewish, observant and a member of the Lyon Jewish community. She holds the guide-conférencier card, the French state licence required to guide inside monuments and museums. She lives in Lyon and has walked these streets for years, with her own family and with visitors.</p>
<ul>
<li><b>Tours in English, French or Spanish.</b> Hebrew-speaking guests are guided in English; we say so plainly on every page.</li>
<li><b>Private only.</b> Your group, from one to ten people, never joined to strangers.</li>
<li><b>Shomer shabbat.</b> No tours on Saturday or on Jewish holidays. Friday tours end well before candle lighting.</li>
<li><b>Strictly kosher.</b> No stop involves non-kosher food. We know the certified places and tell you where they are.</li>
</ul>"""),
    dict(type="beige", h2="What we <i>believe</i> a Jewish tour should be", html="""<p>Most city tours of Lyon are excellent, and none of them is built for you. They stop where you cannot eat, run on Saturday, and tell the Jewish story of the city as a footnote. We turn it around: the Jewish story is the spine, the kosher map is in our pocket, and the day is planned around your calendar.</p>
<p>That is why we are the only tour that takes you inside the Grande Synagogue of Lyon, closed to visitors outside the Heritage Days, subject to the opening hours and security clearance of the day. And why the Memory tours visit the CHRD and Montluc on separate days, each with the time it deserves.</p>"""),
    dict(type="text", h2="Safety, <i>said plainly</i>", html="""<p>Many of our guests ask about it before anything else, and they are right to. We work in private groups, choose routes and meeting points in advance and keep them discreet. On any tour, a professional security escort is available on request, priced separately on quote. Your guide is part of the community and knows the city as it is today, not as a brochure describes it.</p>"""),
    dict(type="steps", h2="How a booking <i>works</i>", items=[
      ("Message us", "WhatsApp or the form: your dates, the number of people and your language. We answer the same day, never on Shabbat."),
      ("We confirm in writing", "Date, start time, meeting point in Vieux Lyon and the price for your group, in one message."),
      ("Meet your guide", "She waits at the agreed spot. Free cancellation up to 24 hours before the start time."),
    ]),
    dict(type="faq", h2="Questions we get", items=[
      ("Why do you not show your guide's face or name?", "For her privacy and safety. You will know who she is when we confirm your booking, and you will recognise her at the meeting point."),
      ("Are you a travel agency?", "No. We sell guided tours only. We do not book hotels, flights or transport, and we tell you when we recommend a van or a driver so you can book it yourself."),
      ("Do you take groups from synagogues or federations?", "Yes, up to ten people per guide. For larger groups, write to us and we organise several guides on the same day."),
      ("Can we tip?", "Tips are never expected and always welcome."),
    ]),
    dict(type="cta", txt="Want to talk before you book?", msg="Hello, I have a question about Mishpacha Tours. Dates: / Number of people: / Preferred language:"),
  ],
  related=[("../tours/jewish-lyon/", "Jewish Lyon, the 2h30 walk"), ("../jewish-lyon-guide/", "The complete Jewish Lyon guide"), ("../contact/", "Contact us")],
  jsonld={"@context": "https://schema.org", "@type": "TourOperator", "name": "Mishpacha Tours", "alternateName": "Mishpacha Tours - Jewish Tours of Lyon", "url": "https://mishpachatours.com/", "email": "contact@mishpachatours.com", "telephone": "+33767711259", "areaServed": "Lyon, France", "availableLanguage": ["en", "fr", "es"], "address": {"@type": "PostalAddress", "addressLocality": "Lyon", "addressCountry": "FR"}},
  VERIF=[],
)
