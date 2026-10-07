# Pages du guide : un module Python par page

Chaque fichier `_pages/<slug>.py` (slug = nom du dossier URL, kebab-case anglais) definit un dict `PAGE`.
Generation : `python _build_guide.py` (toutes) ou `python _build_guide.py <slug>` (une seule), depuis `site-v5/`.

```python
PAGE = dict(
  slug="grande-synagogue-lyon",
  title="Grande Synagogue of Lyon, quai Tilsitt",        # <title> sans le suffixe " | Mishpacha Tours", 45-60 caracteres
  desc="...",                                             # meta description 140-160 caracteres : un fait + une promesse
  h1="Grande Synagogue of Lyon", ital="inside the building closed to visitors",   # h1 en deux lignes, la seconde en italique
  intro="...",                                            # 2-3 phrases, l'essentiel pour un voyageur juif qui prepare son voyage
  chips=["Built 1864", "Quai Tilsitt, Lyon 2e", "Checked 7 October 2026"],        # 3-4 puces factuelles
  illus="line-synagogue.png",                             # une image de img/illus/ (flat-*.png ou line-*.png)
  crumb=("../jewish-lyon-guide/", "Jewish Lyon guide"),   # fil d'Ariane ; None pour about/contact/legal
  sections=[                                              # dans l'ordre d'affichage
    dict(type="text",   h2="History <i>in short</i>", html="<p>...</p><ul><li><b>Lead.</b> texte</li></ul>"),
    dict(type="beige",  h2="...", html="..."),            # meme chose sur fond beige
    dict(type="lieux",  h2="Where to pray", items=[("Nom", "adresse complete avec code postal et ville", "04 00 00 00 00" ou "", "note courte" ou "")], source="Source: ..."),
    dict(type="map",    h2="On the <i>map</i>", points=[("Nom", "adresse")], note="..."),  # adresses geocodees (cache img/geo.json, Nominatim sinon)
    dict(type="photos", items=[("stock/chrd-1.jpg", "legende"), ...]),                     # 4 images de img/, la premiere est grande
    dict(type="shabbat"),                                 # widget horaires de Shabbat en direct (Hebcal)
    dict(type="steps",  h2="How to <i>visit</i>", items=[("Titre", "texte"), ...]),
    dict(type="faq",    h2="Questions we get", items=[("Question ?", "Reponse en 1-3 phrases"), ...]),   # genere aussi le JSON-LD FAQPage
    dict(type="cta",    txt="Want to ...?", msg="Hello, I would like ... Dates: / Number of people:"),  # bouton WhatsApp pre-rempli
    "<section class='ss wrap'>html libre si besoin</section>",
  ],
  related=[("../tours/jewish-lyon/", "Jewish Lyon tour, 2h30"), ("../synagogues-lyon/", "Synagogues and Shabbat in Lyon")],
  source="Sources: memorializieu.eu, ...",                # phrase de sources en fin de page
  jsonld=None,                                            # dict schema.org supplementaire (TouristAttraction, Museum...) ou None
  ticket=True,                                            # False = pas de formulaire de reservation en bas
  VERIF=["fait X : source secondaire, a confirmer par telephone", ...],   # faits a relire par l'operateur (obligatoire, meme vide)
)
```

Regles de contenu, non negociables : anglais, voix directe, phrases courtes ; zero mention d'eglise ; jamais le mot Israel ni d'etoile de David ;
« strictly kosher », jamais « kosher-friendly » ; jamais « Israeli » (dire « Hebrew-speaking guests ») ; la guide n'a ni nom, ni visage, ni titre de fondatrice ;
chaque adresse et chaque horaire vient d'une source nommee, sinon « not published » ; les prix d'entree se citent avec la date de releve.
Pas de tiret cadratin. Pas d'adverbes de remplissage. Pas de « ce n'est pas X, c'est Y ». Liens internes relatifs depuis le sous-dossier (`../tours/izieu/`).
