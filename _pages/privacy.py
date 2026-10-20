# -*- coding: utf-8 -*-
# 20/10 (C3) : texte aligné sur le vrai comportement (GA4 + Google Ads après « Accept » seulement) et sur le formulaire (données de santé et de pratique religieuse, art. 9 RGPD).
# La section « Cookies and measurement » est posée par _mesure.py (PRIV). Traductions fr/es/he et rendu des 4 sorties : _confidentialite_legal.py.
PAGE = dict(
  slug="privacy",
  title="Privacy policy, Mishpacha Tours",
  desc="What Mishpacha Tours collects through the request form, why, who receives it, for how long, and your rights under the GDPR. Cookies only with your consent.",
  h1="Privacy",
  ital="what we keep, and why",
  intro="We collect what we need to answer you and to run your tour, nothing else. This page says what that is, where it is stored and how to have it deleted.",
  chips=["GDPR", "Cookies only with your consent", "Data kept 3 years"],
  illus="line-private.png",
  crumb=None,
  ticket=False,
  sections=[
    dict(type="text", h2="Who is <i>responsible</i>", ico="message-circle", html="""<p>Mishpacha Tours, a sole-trader business run by the guide in Lyon, France. Contact: <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>, or the request form. Business details are in the <a href="../legal/">legal notice</a>.</p>"""),
    dict(type="text", h2="What we <i>collect</i>", icos=["calendar-days", "lock", "message-circle", "calendar-x"], html="""<ul>
<li><b>When you send the request form:</b> the trip or tour you want, your dates, the number of people, the language, your name, your phone or WhatsApp number, and your email address if you give one. The form also asks for details that help us prepare your quote: dietary needs and allergies, the ages of your children, your level of religious observance (minyan and kashrut) and your budget. The form writes a line in a private Google Sheet and sends us an email.</li>
<li><b>Legal basis:</b> steps prior to a contract for the booking details. For allergies and dietary needs (health data) and for religious observance, we rely on your explicit consent (article 9.2.a of the GDPR), given by ticking the box under the Send button of the form. Without that consent the form cannot be sent.</li>
<li><b>When you write on WhatsApp or by email:</b> your messages and your number or address, kept in those services under their own terms.</li>
<li><b>When you visit the site:</b> before you press Accept, nothing from us: no cookie and no third-party script. After Accept, Google Analytics and Google Ads load, as described in the section Cookies and measurement below. Our hosting provider (Vercel) keeps standard server logs for security. Map pages load tiles from OpenStreetMap and Shabbat times from Hebcal; those services see your IP address when the page loads.</li>
</ul>"""),
    dict(type="text", h2="Who <i>receives</i> it", ico="users", html="""<p>For a stay in the Alps, we pass your request to the service provider in the Alps who prepares the quote (chalet, chef, minyan, transfers). This provider receives your answers, including diet and religious observance, and uses them only to build your quote. Besides the provider, only the services that store the data for us see it (Google, WhatsApp, Vercel). We never sell or share your details, and we never send newsletters.</p>"""),
    dict(type="text", h2="How long <i>we keep it</i>", ico="clock", html="""<p>Requests and correspondence, including the answers on diet and religious observance, are kept for three years after our last exchange, then deleted.</p>"""),
    dict(type="text", h2="Your <i>rights</i>", ico="message-circle", html="""<p>You can ask what we hold about you, have it corrected or deleted, or object to its use. You can withdraw your consent at any time by writing to <a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>; we then delete the answers on health and religious observance, and what was done before is not affected. We answer within one month. You can also lodge a complaint with the CNIL, the French data protection authority, at cnil.fr.</p>"""),
  ],
  related=[("../terms/", "Terms of booking"), ("../credits/", "Photo credits")],
  VERIF=["Durée de conservation des réponses sensibles (allergies, pratique religieuse) : 3 ans comme le reste, à confirmer par l'opérateur (une durée plus courte est défendable).", "Statut juridique : les mentions d'immatriculation sont dans la page /legal/ (SIREN à compléter)."],
)
