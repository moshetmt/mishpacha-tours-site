# -*- coding: utf-8 -*-
"""Genere les 5 fiches tours de la v5 a partir de l'accueil (nav, pied, styles) et des donnees ci-dessous.
   python _build_tours.py   (depuis site-v5/)"""
import re, os, html

WA = "https://wa.me/33767711259?text="
def wa(txt): return WA + html.escape(__import__('urllib.parse').parse.quote(txt))

TOURS = [
 dict(slug="jewish-lyon", tag="City walk", h1="Jewish Lyon", ital="A private walk through the Jewish story of Lyon, inside the Grande Synagogue",
   photo="synagogue-tilsitt-arche.jpg", lieu="Vieux Lyon and quai Tilsitt", duree="2 hours 30 minutes", format="On foot, private group",
   prix="290 €", prix2="per group, 1 to 4 people", prix3="+35 € per extra person, 5th to 10th",
   intro="Rue Juiverie and medieval Old Lyon, the Grande Synagogue on quai Tilsitt from the inside, and rue Sainte-Catherine: two and a half hours on foot with a guide who is part of the community she shows you. The Grande Synagogue is closed to visitors outside the Heritage Days. This is the only tour that takes you inside.",
   wa="Hello, I would like to ask about the Jewish Lyon tour. Dates: / Number of people: / Preferred language:",
   etapes=[("Rue Juiverie","We start in rue Juiverie and the medieval streets of Vieux Lyon, where Lyon's Jewish community lived before the expulsions of the Middle Ages."),
           ("The Grande Synagogue, from the inside","From rue Juiverie we walk to the Grande Synagogue on quai Tilsitt and go inside: the Ark of the Law, the arcades of the women's gallery, a working synagogue that is closed to visitors outside the Heritage Days. Entry depends on opening hours and on security clearance on the day; your guide confirms before the walk begins."),
           ("Rue Sainte-Catherine","We finish on rue Sainte-Catherine, where the wartime story of Lyon's Jews meets the story of the Resistance, and where your guide answers the questions the walk has raised.")],
   inclus=["A private guide for 2 hours 30 minutes, in English, French or Spanish.","Entry to the Grande Synagogue on quai Tilsitt, subject to opening hours and security clearance on the day.","The walking route through Vieux Lyon and rue Sainte-Catherine."],
   exclus=["Meals and drinks.","Transport to the meeting point.","A security escort. Available on request on any tour, priced separately, quote on demand."],
   faq=[("Is the Grande Synagogue always open when I book?","Entry depends on the synagogue's opening hours and on security clearance on the day. Your guide checks and confirms with you before the walk begins."),
        ("In which language is the tour guided?","English, French or Spanish. We do not run tours in Hebrew: Hebrew-speaking guests are guided in English. Tell us your preferred language when you book."),
        ("Can I cancel if my plans change?","Yes, free cancellation up to 24 hours before the start time."),
        ("Is a security escort available?","Yes, on request, on any tour. It is priced separately and quoted on demand, never included in the tour price.")],
   photos=[("c-synagogue-7.jpg","Grande Synagogue, quai Tilsitt"),("synagogue-tilsitt-galerie.jpg","The women's gallery"),("c-juiverie-3.jpg","Rue Juiverie"),("stock/juiverie-6.jpg","Rue Juiverie, looking down"),("stock/juiverie-3.jpg","A Renaissance plaque, rue Juiverie"),("stock/stecath-1.jpg","Rue Sainte-Catherine"),("stock/stecath-6.jpg","Rue Sainte-Catherine today")]),
 dict(slug="memory-chrd", tag="Memory", h1="Memory: the CHRD", ital="A private visit of the Centre d'histoire de la résistance et de la déportation",
   photo="c-chrd-1.jpg", lieu="Lyon 7e", duree="About 2 hours 30 minutes", format="Museum visit, private group",
   prix="290 €", prix2="per group, 1 to 4 people", prix3="+35 € per extra person, 5th to 10th. Booked separately from the Montluc and Neveh Shalom visit.",
   intro="Your guide walks you through Lyon's Centre d'histoire de la résistance et de la déportation, housed in the former Gestapo headquarters, with the Jewish dimension of that history at the centre of the visit. This booking is never combined with the Montluc and Neveh Shalom visit on the same day.",
   wa="Hello, I would like to ask about the Memory tour, CHRD booking. Dates: / Number of people: / Preferred language:",
   etapes=[("Meeting and introduction","Your guide meets your group and sets the history of Lyon under the Occupation before you go in."),
           ("Inside the CHRD","The permanent exhibition on the Resistance and the deportation from Lyon, with your guide's commentary on the Jewish dimension of that history throughout."),
           ("Time to talk","We close with time for your questions, at the pace your group needs.")],
   inclus=["A private guide, about 2 hours 30 minutes, in English, French or Spanish.","Guiding through the CHRD exhibition, with the Jewish dimension of the history explained throughout."],
   exclus=["The CHRD entry ticket, paid on site.","Transport to the museum.","A security escort. Available on request on any tour, priced separately, quote on demand."],
   faq=[("How long does this visit last?","About 2 hours 30 minutes. The exact timing is confirmed once your group size and the CHRD's hours on the day are set."),
        ("Is the museum entry ticket included?","No, the CHRD entry ticket is paid on site. Your guide tells you the current rate before you go in."),
        ("Can I combine this with the Montluc and Neveh Shalom visit on the same day?","No. The two Memory visits are booked separately and never run on the same day: each one carries enough history and emotional weight on its own."),
        ("Can I cancel if my plans change?","Yes, free cancellation up to 24 hours before the start time.")],
   photos=[("c-chrd-1.jpg","The CHRD entrance"),("stock/chrd-1.jpg","A 1940s kitchen, reconstructed"),("stock/chrd-3.jpg","The posters of the Occupation"),("stock/chrd-4.jpg","The permanent exhibition"),("stock/chrd-7.jpg","A deportee's satchel")]),
 dict(slug="memory-montluc-neveh-shalom", tag="Memory", h1="Memory: Montluc and Neveh Shalom", ital="The Montluc memorial, then the second synagogue we take you inside",
   photo="c-montluc-1.jpg", lieu="Lyon 3e", duree="About 2 hours 30 minutes", format="On foot, private group",
   prix="290 €", prix2="per group, 1 to 4 people", prix3="+35 € per extra person, 5th to 10th. Booked separately from the CHRD visit.",
   intro="The Montluc prison memorial, then Neveh Shalom, the second synagogue your guide takes you inside, and the Institut culturel du judaïsme next door: memory and living Jewish life on the same walk. This booking is never combined with the CHRD visit on the same day.",
   wa="Hello, I would like to ask about the Memory tour, Montluc and Neveh Shalom booking. Dates: / Number of people: / Preferred language:",
   etapes=[("Montluc prison memorial","The fort where the Gestapo held resistance fighters and Jews before deportation. Your guide covers this history plainly, at the pace your group needs."),
           ("Neveh Shalom synagogue","From Montluc we walk to Neveh Shalom, the second synagogue your guide takes you inside, alongside the Grande Synagogue on quai Tilsitt."),
           ("Institut culturel du judaïsme","Next door to Neveh Shalom: living Jewish life in Lyon, seen right after the history of Montluc.")],
   inclus=["A private guide, about 2 hours 30 minutes, in English, French or Spanish.","The walking route from Montluc to Neveh Shalom and the Institut culturel du judaïsme.","Entry inside Neveh Shalom, the second synagogue we take you into."],
   exclus=["Montluc memorial entry.","Transport to the memorial.","A security escort. Available on request on any tour, priced separately, quote on demand."],
   faq=[("How long does this visit last?","About 2 hours 30 minutes. Your guide confirms the exact timing once your group size is set."),
        ("Can I combine this with the CHRD visit on the same day?","No. The two Memory visits are booked separately and never run on the same day."),
        ("Do we go inside Neveh Shalom?","Yes. It is the second synagogue we take you inside, alongside the Grande Synagogue on quai Tilsitt."),
        ("Can I cancel if my plans change?","Yes, free cancellation up to 24 hours before the start time.")],
   photos=[("c-montluc-1.jpg","Montluc, the cell gallery"),("montluc-mur-des-fusilles.jpg","Montluc, the wall"),("synagogue-tilsitt-arche.jpg","Inside a Lyon synagogue"),("c-synagogue-4.jpg","The synagogue door"),("stock/chrd-7.jpg","A deportee's satchel, CHRD")]),
 dict(slug="stopover", tag="City walk", h1="Stopover", ital="Three hours in Jewish Lyon while your transfer waits",
   photo="c-traboule-1.jpg", lieu="Vieux Lyon", duree="3 hours", format="On foot, private group, for families driving on to the Alps",
   prix="390 €", prix2="per group, 1 to 5 people", prix3="+35 € per extra person, 6th to 10th. Tour operators and kosher hotels: net rates on request.",
   intro="Your own transport drops you in Vieux Lyon and picks you up at the same spot three hours later. Your bags stay in the van; you walk into the Jewish story of Lyon and into the Grande Synagogue on quai Tilsitt, closed to visitors outside the Heritage Days.",
   wa="Hello, I would like to ask about the Stopover tour. Arrival time: / Onward departure time: / Number of people: / Preferred language:",
   etapes=[("Drop-off in Vieux Lyon","Your own transport, van or private transfer, drops you at the meeting point in Vieux Lyon. Your bags stay inside; you carry nothing."),
           ("Vieux Lyon on foot","We walk through the Jewish story of the medieval old town, the same ground covered on the Jewish Lyon tour, at a pace built for three hours."),
           ("The Grande Synagogue","We go inside the Grande Synagogue on quai Tilsitt. Entry depends on opening hours and on security clearance on the day; your guide confirms before the walk begins."),
           ("Pick-up, on schedule","We finish at the time you give us, so your transfer leaves for the resort on schedule.")],
   inclus=["3 hours of private guiding, in English, French or Spanish.","Entry to the Grande Synagogue on quai Tilsitt, subject to opening hours and security clearance on the day.","Drop-off and pick-up at the same meeting point in Vieux Lyon."],
   exclus=["Airport pick-up. Available on request, as a paid add-on, quote on demand.","Transport to or from the resort.","A security escort. Available on request on any tour, priced separately, quote on demand."],
   faq=[("Where do we meet, and what happens to our bags?","We meet at a set point in Vieux Lyon. Your bags stay in your van or transfer; you carry nothing for the three hours."),
        ("What if our flight lands late?","Tell us your arrival time and your onward departure time when you book. We build the three hours around your schedule so you leave for the resort on time."),
        ("Is airport pick-up included?","No, it is available on request as a paid add-on, quote on demand."),
        ("Can I cancel if my plans change?","Yes, free cancellation up to 24 hours before the start time.")],
   photos=[("c-traboule-1.jpg","Vieux Lyon, the Tour Rose"),("stock/rose-3.jpg","A traboule courtyard"),("stock/stjean-5.jpg","Rue Saint-Jean shopfronts"),("stock/boeuf-2.jpg","A quiet square, rue du Boeuf"),("c-synagogue-7.jpg","Grande Synagogue"),("synagogue-tilsitt-galerie.jpg","The women's gallery"),("stock/stjean-4.jpg","A Renaissance doorway")]),
 dict(slug="izieu", tag="Day trip", h1="Izieu", ital="A full day at the Maison d'Izieu, one hour from Lyon",
   photo="c-izieu-8.jpg", lieu="Izieu, Ain", duree="Full day", format="Day trip, van and driver arranged separately",
   prix="from 990 €", prix2="quote on request", prix3="The price depends on the vehicle and the number of guests.",
   intro="Your guide's own account of Izieu unfolds on the road and through the rest of the day; the house itself is visited with a memorial mediator, as the Maison d'Izieu requires.",
   wa="Hello, I would like a quote for the Izieu day trip. Dates: / Number of people: / Preferred language:",
   etapes=[("The road to Izieu","About an hour from Lyon by van. Your guide's own commentary on the story of Izieu begins on the drive out."),
           ("The house, with a memorial mediator","The Maison d'Izieu itself is only visited accompanied by a mediator from the memorial, for about an hour to an hour and fifteen minutes. Your guide accompanies the group through this part rather than leading it."),
           ("The memorial's guided tour, in context","English-language guided visits of the memorial require advance booking and a minimum of 6 people, including 2 adults and 2 children over 8. We arrange this booking for you and plan around it if your group is smaller."),
           ("The rest of the day","Your guide's own account continues around the visit and on the road back, filling the day beyond the mediator-led hour.")],
   inclus=["A full-day private guide, in English, French or Spanish.","Your guide's own narration on the drive and throughout the day.","Coordination of the memorial's mediator-led visit and its 6-person minimum for English tours."],
   exclus=["Van and driver. Arranged and billed separately, quote on request.","Maison d'Izieu memorial entry, billed directly by the memorial: 12 € full rate, 5 € ages 8 to 25, free under 8 (rates checked 9 August 2026).","A security escort. Available on request on any tour, priced separately, quote on demand."],
   faq=[("Can we visit the house without booking ahead?","No. The Maison d'Izieu is only accessible with a memorial mediator on a booked guided visit, and the memorial requires 6 people minimum for the English tour, including 2 adults and 2 children over 8. We handle this booking and adjust the plan if your group is smaller."),
        ("Is transport included?","No. Van and driver are arranged and billed separately: we do not sell transport as part of a package."),
        ("How much is memorial entry?","Rates checked on 9 August 2026: 12 € full rate, 5 € for ages 8 to 25, free under 8. The memorial bills entry directly."),
        ("Can I cancel if my plans change?","Yes, free cancellation up to 24 hours before departure.")],
   photos=[("c-izieu-8.jpg","Maison d'Izieu"),("maison-izieu-volets.jpg","The blue shutters"),("c-izieu-4.jpg","The house and its grounds"),("stock/izieu-3.jpg","The classroom"),("stock/izieu-2.jpg","The staircase"),("stock/izieu-1.jpg","The corridor")]),
]

home = open("index.html", encoding="utf-8").read()
head = home[:home.index("<main>")]
foot = home[home.index("</main>")+7:]

def rel(s):  # chemins relatifs depuis tours/<slug>/
    s = s.replace('href="img/', 'href="../../img/').replace('src="img/', 'src="../../img/').replace('src="fonts/', 'src="../../fonts/')
    s = s.replace('href="fonts/', 'href="../../fonts/').replace('href="styles.css"', 'href="../../styles.css"').replace('href="./"', 'href="../../"')
    s = s.replace('href="#tours"', 'href="../../#tours"').replace('href="#why"', 'href="../../#why"').replace('href="#before"', 'href="../../#before"').replace('href="#guide"', 'href="../../#guide"')
    s = s.replace('href="fr/"', 'href="../../fr/"').replace('href="es/"', 'href="../../es/"').replace('href="he/"', 'href="../../he/"').replace('href="credits.html"', 'href="../../credits.html"')
    return s

def carte_autre(t):
    return f'''<a class="carte autre" href="../{t['slug']}/"><div class="photo"><img src="../../img/{t['photo']}" alt="" loading="lazy"><span class="tag">{t['tag']}</span></div><div class="corps"><h3>{t['h1']}</h3><p class="ital">{t['ital']}</p><p class="prix"><b>{t['prix']}</b> <span>{t['prix2']}</span></p></div></a>'''

for t in TOURS:
    autres = "".join(carte_autre(o) for o in TOURS if o["slug"] != t["slug"])
    etapes = "".join(f'<li><b>{i+1}</b><div><h3>{a}</h3><p>{b}</p></div></li>' for i,(a,b) in enumerate(t["etapes"]))
    inclus = "".join(f"<li>{x}</li>" for x in t["inclus"]); exclus = "".join(f"<li>{x}</li>" for x in t["exclus"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in t["faq"])
    photos = "".join(f'<figure{" class=\"large\"" if i==0 else ""}><img src="../../img/{p}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for i,(p,c) in enumerate(t["photos"]))
    h = rel(head)
    h = re.sub(r"<title>.*?</title>", f"<title>{t['h1']} | Mishpacha Tours, Jewish Tours of Lyon</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(t["ital"])}. Private, strictly kosher, {t["prix"]} {t["prix2"]}. Book on WhatsApp.">', h)
    body = f'''<main>
<section class="fiche-hero">
  <div class="fiche-photo"><img src="../../img/{t['photo']}" alt="" fetchpriority="high"><span class="tag">{t['tag']}</span></div>
  <div class="fiche-texte">
    <p class="fil"><a href="../../">Home</a> / <a href="../../#tours">Tours</a> / {t['h1']}</p>
    <h1>{t['h1']}<br><i>{t['ital']}</i></h1>
    <p class="intro-fiche">{t['intro']}</p>
  </div>
  <aside class="fiche-carte">
    <dl>
      <div><dt>Where</dt><dd>{t['lieu']}</dd></div>
      <div><dt>Duration</dt><dd>{t['duree']}</dd></div>
      <div><dt>Format</dt><dd>{t['format']}</dd></div>
      <div><dt>Language</dt><dd>English, French or Spanish</dd></div>
    </dl>
    <p class="fiche-prix"><b>{t['prix']}</b><span>{t['prix2']}</span><small>{t['prix3']}</small></p>
    <a class="btn-noir large" href="{wa(t['wa'])}" rel="noopener"><svg><use href="#wa"/></svg>Ask on WhatsApp</a>
    <p class="fiche-note">Same-day reply, never on Shabbat. Free cancellation up to 24 hours before the start time.</p>
  </aside>
</section>

<section class="ss wrap deroule">
  <h2>How the tour <i>unfolds</i></h2>
  <ol>{etapes}</ol>
</section>

<section class="ss beige">
  <div class="wrap inclus">
    <h2 class="centre">Know before you <i>go</i></h2>
    <div class="deux-cartes">
      <div><h3>Included</h3><ul>{inclus}</ul></div>
      <div><h3>Not included</h3><ul>{exclus}</ul></div>
    </div>
  </div>
</section>

<section class="ss wrap" id="places">
  <h2 class="centre">Places you will <i>stand</i> in</h2>
  <div class="mosaique">{photos}</div>
</section>

<section class="ss wrap garanties-fiche">
  <h2>How we move through <i>Lyon</i></h2>
  <ul>
    <li><b>Private groups only.</b> Your booking is never joined to strangers.</li>
    <li><b>Discreet routes.</b> Routes and meeting points are chosen in advance and kept discreet.</li>
    <li><b>Known in the places we visit.</b> Your guide is a member of the Lyon Jewish community.</li>
    <li><b>Security escort on request.</b> On any tour, priced separately, quote on demand. Never included in the tour price.</li>
  </ul>
</section>

<section class="ss wrap faq">
  <h2 class="centre">Questions before you <i>book</i></h2>
  {faq}
</section>

<section class="ss beige">
  <div class="wrap centre"><h2>Other <i>Mishpacha</i> tours</h2></div>
  <div class="rail autres">{autres}</div>
</section>

<div class="ticket-zone" id="book">
  <div class="ticket">
    <h2>Ready to <i>book</i> {t['h1']}?</h2>
    <form id="formReserver">
      <div class="piege" aria-hidden="true"><label for="f-societe">Company</label><input type="text" id="f-societe" name="societe" tabindex="-1" autocomplete="off"></div>
      <input type="hidden" name="tour" value="{t['h1']}">
      <div><label for="f-dates">Dates</label><input type="text" id="f-dates" name="dates" placeholder="12 to 15 October" required></div>
      <div><label for="f-personnes">Number of people</label><input type="text" id="f-personnes" name="personnes" inputmode="numeric" required></div>
      <div><label for="f-langue">Tour language</label><select id="f-langue" name="langue" required><option value="">Choose a language</option><option>English</option><option>French</option><option>Spanish</option></select></div>
      <div><label for="f-nom">Your name</label><input type="text" id="f-nom" name="nom" autocomplete="name" required></div>
      <div><label for="f-contact">Email or WhatsApp number</label><input type="text" id="f-contact" name="contact" required></div>
      <div class="envoi"><span>Send my request</span><button class="rond" type="submit" aria-label="Send my request"><svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>
    </form>
    <a class="wa" href="{wa(t['wa'])}" rel="noopener"><svg><use href="#wa"/></svg>Or message us on WhatsApp</a>
  </div>
</div>
</main>'''
    f = rel(foot).replace("document.getElementById('chercheur').addEventListener", "document.getElementById('chercheur')&&document.getElementById('chercheur').addEventListener")
    f = f.replace("document.querySelectorAll('.filtres button')", "document.querySelectorAll('.filtres button')")
    os.makedirs(f"tours/{t['slug']}", exist_ok=True)
    open(f"tours/{t['slug']}/index.html", "w", encoding="utf-8").write(h + body + f)
    print("ok", t["slug"])
