# -*- coding: utf-8 -*-
PAGE = dict(
  slug="privacy",
  title="Privacy policy, Mishpacha Tours",
  desc="What Mishpacha Tours collects when you book a tour, why, for how long, and your rights under the GDPR. No advertising cookies, no tracking.",
  h1="Privacy",
  ital="what we keep, and why",
  intro="We collect what we need to answer you and to run your tour, nothing else. This page says what that is, where it is stored and how to have it deleted.",
  chips=["GDPR", "No advertising cookies", "Data kept 3 years"],
  illus="line-private.png",
  crumb=None,
  ticket=False,
  sections=[
    dict(type="text", h2="Who is <i>responsible</i>", html="""<p>Mishpacha Tours, a sole-trader business registered in Lyon, France. Contact: <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>, WhatsApp +33 7 67 71 12 59.</p>"""),
    dict(type="text", h2="What we <i>collect</i>", html="""<ul>
<li><b>When you send the booking form:</b> the tour, your dates, the number of people, the language, your name, and an email address or WhatsApp number. The form writes a line in a private Google Sheet and sends us an email. Legal basis: steps prior to a contract.</li>
<li><b>When you write on WhatsApp or by email:</b> your messages and your number or address, kept in those services under their own terms.</li>
<li><b>When you visit the site:</b> nothing from us. The site sets no cookies and runs no analytics or advertising scripts. Our hosting provider (Vercel) keeps standard server logs for security. Map pages load tiles from OpenStreetMap and Shabbat times from Hebcal; those services see your IP address when the page loads.</li>
</ul>"""),
    dict(type="text", h2="How long, and <i>who sees it</i>", html="""<p>Booking requests and correspondence are kept for three years after the last exchange, then deleted. Nobody outside Mishpacha Tours sees them, except the services named above that store them on our behalf (Google, WhatsApp, Vercel). We never sell or share your details, and we never send newsletters.</p>"""),
    dict(type="text", h2="Your <i>rights</i>", html="""<p>You can ask what we hold about you, have it corrected or deleted, or object to its use. Write to <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>; we answer within one month. You can also lodge a complaint with the CNIL, the French data protection authority, at cnil.fr.</p>"""),
  ],
  related=[("../terms/", "Terms of booking"), ("../credits/", "Photo credits")],
  VERIF=["Statut juridique et mention d'immatriculation (SIREN) à compléter quand l'opérateur les transmet."],
)
