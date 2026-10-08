# -*- coding: utf-8 -*-
PAGE = dict(
  slug="contact",
  title="Contact Mishpacha Tours, WhatsApp or email",
  desc="Book a private Jewish tour of Lyon or ask a question. WhatsApp +33 7 67 71 12 59, email contact@mishpachatours.com. Same-day reply, never on Shabbat.",
  h1="Contact us",
  ital="same-day reply, never on Shabbat",
  intro="WhatsApp is the fastest way to reach us. Send your dates, the number of people and your language, and we answer in writing with a start time, a meeting point and the price for your group.",
  chips=["WhatsApp +33 7 67 71 12 59", "contact@mishpachatours.com", "English, French, Spanish"],
  illus="line-whatsapp.png",
  crumb=None,
  sections=[
    dict(type="text", h2="Three ways to <i>reach us</i>", html="""<ul>
<li><b>WhatsApp.</b> <a href="https://wa.me/33652092301?text=Hello%2C%20I%20would%20like%20to%20ask%20about%20a%20private%20Jewish%20tour%20of%20Lyon.%20Dates%3A%20%2F%20Number%20of%20people%3A%20%2F%20Preferred%20language%3A" rel="noopener">+33 7 67 71 12 59</a>. Messages only, any language; we reply in English, French or Spanish.</li>
<li><b>Email.</b> <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>. Best for groups, agencies and hotels.</li>
<li><b>The form below.</b> Tour, dates, number of people, language and a way to reach you. We write back within one business day.</li>
</ul>
<p>We do not answer from Friday afternoon to Saturday night, nor on Jewish holidays. A message sent on Friday evening is answered on Sunday.</p>"""),
    dict(type="beige", h2="Where we <i>meet</i>", html="""<p>City tours start in Vieux Lyon, at a spot we confirm in writing. The Memory tours start at the museum or memorial of the day. The Izieu day starts where your van picks you up. We never publish meeting points online.</p>"""),
    dict(type="faq", h2="Before you write", items=[
      ("How far ahead should I book?", "A week is comfortable in winter. From May to October, and around the Jewish holidays, two to three weeks. Last-minute requests are welcome; we tell you quickly if the date is free."),
      ("Can you help with kosher food, Shabbat or a hotel?", "Yes, within reason. We point you to the certified kosher places, the synagogues and the caterers who deliver, and we tell you which areas are practical for Shabbat. We do not book on your behalf."),
      ("Do you work with travel agents and hotels?", "Yes. Write to contact@mishpachatours.com for net rates on the Stopover and on group days."),
    ]),
  ],
  related=[("../about/", "About Mishpacha Tours"), ("../jewish-travel-lyon-faq/", "Jewish travel to Lyon, the FAQ"), ("../jewish-lyon-guide/", "The complete Jewish Lyon guide")],
  jsonld={"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Mishpacha Tours", "url": "https://mishpachatours.com/contact/"},
  VERIF=[],
)
