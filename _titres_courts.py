# -*- coding: utf-8 -*-
"""Titres (h1) courts sur téléphone. Contrôle du 30/10 (scripts/verif_appareils.py, mesures.csv) : 210 contrôles où le h1
dépassait 4 lignes à 360 px (Android) ou 390 px (iPhone), surtout FR et ES, parce que la ligne dorée était trop longue.
Chaque h1 = ligne blanche + <br><i>ligne dorée</i> (thème Valora). Objectif mesuré : 4 lignes au plus sur les deux téléphones,
chaque couple ci-dessous a été mesuré dans Chromium 360 px et WebKit 390 px avant d'être retenu.
Règles : sens conservé, registre luxe sobre, langue du dossier, jamais un nombre de chalets, jamais « Israel », jamais de tiret
cadratin ; hébreu selon le lexique de relecture-hebreu (מג'ב, קורמאיור, jamais למהדרין ni מורת דרך). Les noms de chalets choisis
par Mendel (King David, Rochebrune, Flocon Doré, Loup Blanc, Belle Étoile) restent en ligne blanche, seule la dorée raccourcit.

Passe aussi sur /jewish-lyon-tours/ (4 langues) : le bloc OFFRES-LYON s'était posé au-dessus du héros (son formulaire de
recherche était pris pour le formulaire de demande), le titre partait sous le premier écran et le bandeau cookies le
recouvrait au contrôle ; le bloc repasse sous le héros (et _offres_lyon.py ignore désormais le formulaire du héros).

Idempotent. Écrit index.html + index.md des pages listées, puis h1=/ital= dans les générateurs : _pages/<slug>.py (EN),
_build_tours.py (tours EN), _van_textes.py et _verbier_i18n.py (FR, ES). À lancer EN DERNIER, après _retouches_30_10.py
(noms des chalets) et _offres_lyon.py.
    python _titres_courts.py [--dry]      (depuis site-v5/)"""
import glob, html, io, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
DRY = "--dry" in sys.argv

# page -> (ligne blanche, ligne dorée)
TITRES = {
  # ---- EN
  "/alps/": ("The Alps, strictly kosher", "winter ski, summer lakes"),
  "/chrd-lyon/": ("The CHRD in Lyon", "Resistance and deportation museum"),
  "/flights-to-lyon/": ("Flights to Lyon", "the airport for the French Alps"),
  "/is-lyon-safe-for-jewish-visitors/": ("Is Lyon safe for Jewish visitors?", "a straight answer, and what we do"),
  "/jewish-life-around-lyon/": ("Jewish life around Lyon", "Grenoble, Annecy, the Alps"),
  "/jewish-lyon-itinerary-2-days/": ("Jewish Lyon in two days", "around Shabbat and kosher meals"),
  "/jewish-lyon-tours/": ("The only tour inside the Grande Synagogue of Lyon.", "Private, strictly kosher, shaped by you."),
  "/kosher-alpe-dhuez/": ("Alpe d'Huez, strictly kosher", "Isère, at 1,860 m"),
  "/kosher-cervinia/": ("Cervinia, strictly kosher", "under the Matterhorn"),
  "/kosher-chamonix/": ("Chamonix, strictly kosher", "under Mont Blanc"),
  "/kosher-cortina/": ("Cortina d'Ampezzo", "strictly kosher, the Dolomites"),
  "/kosher-courchevel/": ("Courchevel, strictly kosher", "1850 and Les 3 Vallées"),
  "/kosher-crans-montana/": ("Crans-Montana", "strictly kosher, above the Rhône"),
  "/kosher-la-plagne/": ("La Plagne, strictly kosher", "11 villages, one request"),
  "/kosher-les-arcs/": ("Les Arcs, strictly kosher", "four villages, linked to La Plagne"),
  "/kosher-les-deux-alpes/": ("Les Deux Alpes", "strictly kosher, glacier at 1,650 m"),
  "/kosher-megeve/": ("Megève, strictly kosher", "445 km of linked pistes"),
  "/kosher-services-french-alps/": ("Kosher services in the Alps", "chalet, chef, Shabbat, minyan"),
  "/kosher-shabbat-meals-catering-lyon/": ("Kosher catering in Lyon", "Shabbat meals, who cooks"),
  "/kosher-ski-holidays-french-alps/": ("Kosher ski holidays", "in the Alps: where to pray, who to call"),
  "/kosher-st-moritz/": ("St. Moritz, strictly kosher", "in the Engadine"),
  "/kosher-vacation-french-alps/": ("A kosher vacation in the Alps", "you choose, we handle kosher"),
  "/kosher-val-disere/": ("Val d'Isère, strictly kosher", "1,850 m, linked to Tignes"),
  "/kosher-val-thorens/": ("Val Thorens, strictly kosher", "Europe's highest resort"),
  "/kosher-van-transfers/": ("Private van transfers", "never on Shabbat"),
  "/kosher-villa-saint-tropez/": ("Villa in Saint-Tropez", "kosher, on the water, private beach"),
  "/kosher-zermatt/": ("Zermatt, strictly kosher", "under the Matterhorn, car-free"),
  "/lyon-gateway-to-the-alps-kosher/": ("Lyon, gateway to the Alps", "for the Jewish traveller"),
  "/montluc-prison-lyon/": ("Montluc memorial", "where the Gestapo held Jews in Lyon"),
  "/synagogues-lyon/": ("Synagogues in Lyon", "Where the community prays"),
  "/tours/jewish-lyon/": ("Jewish Lyon", "A private walk, inside the Grande Synagogue"),
  "/tours/memory-chrd/": ("Memory: the CHRD", "The Resistance museum, privately"),
  "/tours/memory-montluc-neveh-shalom/": ("Memory: Montluc and Neveh Shalom", "Memorial, then synagogue"),
  "/where-to-stay-lyon-jewish-travellers/": ("Where to stay in Lyon", "for a traveller who keeps Shabbat"),
  # ---- FR
  "/fr/about/": ("Mishpacha Tours", "une guide juive, pour des voyageurs juifs"),
  "/fr/alps/": ("Les Alpes, strictement casher", "ski l’hiver, lacs l’été"),
  "/fr/chabad-lyon/": ("Chabad à Lyon", "Huit maisons, une table de Shabbat"),
  "/fr/chrd-lyon/": ("Le CHRD à Lyon", "le musée de la Résistance et de la déportation"),
  "/fr/flights-to-lyon/": ("Vols vers Lyon", "l’aéroport des Alpes françaises"),
  "/fr/grande-synagogue-lyon/": ("Grande Synagogue de Lyon", "à l’intérieur d’un édifice fermé"),
  "/fr/is-lyon-safe-for-jewish-visitors/": ("Lyon est-elle sûre ?", "visiteurs juifs : une réponse directe"),
  "/fr/jewish-cemetery-lyon/": ("Le cimetière juif de Lyon", "La Mouche, depuis 1795"),
  "/fr/jewish-life-around-lyon/": ("La vie juive autour de Lyon", "Grenoble, Annecy, les Alpes"),
  "/fr/jewish-lyon-itinerary-2-days/": ("Le patrimoine juif de Lyon", "deux jours, repas casher et Shabbat"),
  "/fr/jewish-lyon-tours/": ("Dans la Grande Synagogue de Lyon.", "La seule visite qui vous y fait entrer. Privée, strictement casher, construite avec vous."),
  "/fr/kosher-alpe-dhuez/": ("L’Alpe d’Huez", "strictement casher, Isère, 1 860 m"),
  "/fr/kosher-chalet-les-deux-alpes/": ("Chalet King David, Les Deux Alpes", "300 m², chef privé"),
  "/fr/kosher-chalet-megeve/": ("Chalet Loup Blanc, près de Megève", "10 chambres face au Mont-Blanc"),
  "/fr/kosher-chalets/": ("Nos chalets casher", "Deux Alpes, Courchevel, Megève, Val Thorens"),
  "/fr/kosher-chamonix/": ("Chamonix, strictement casher", "au pied du Mont-Blanc"),
  "/fr/kosher-courchevel/": ("Courchevel", "strictement casher, Les 3 Vallées"),
  "/fr/kosher-crans-montana/": ("Crans-Montana", "strictement casher, au-dessus du Rhône"),
  "/fr/kosher-grenoble/": ("Grenoble, strictement casher", "la base des stations de l’Isère"),
  "/fr/kosher-la-plagne/": ("La Plagne, strictement casher", "11 villages, une seule demande"),
  "/fr/kosher-les-arcs/": ("Les Arcs, strictement casher", "quatre villages, reliés à La Plagne"),
  "/fr/kosher-les-deux-alpes/": ("Les Deux Alpes", "strictement casher, glacier à 1 650 m"),
  "/fr/kosher-megeve/": ("Megève, strictement casher", "445 km de pistes reliées"),
  "/fr/kosher-restaurants-lyon/": ("Casher à Lyon", "31 adresses certifiées, table et courses"),
  "/fr/kosher-services-french-alps/": ("Services casher dans les Alpes", "chalet, chef, repas, Shabbat"),
  "/fr/kosher-shabbat-meals-catering-lyon/": ("Traiteurs casher", "à Lyon, repas de Shabbat, qui cuisine"),
  "/fr/kosher-ski-holidays-french-alps/": ("Vacances au ski casher", "dans les Alpes : où prier, qui appeler"),
  "/fr/kosher-st-moritz/": ("Saint-Moritz, strictement casher", "en Engadine"),
  "/fr/kosher-vacation-french-alps/": ("Vacances casher", "dans les Alpes, le casher pris en charge"),
  "/fr/kosher-val-disere/": ("Val d’Isère, strictement casher", "1 850 m, relié à Tignes"),
  "/fr/kosher-val-thorens/": ("Val Thorens, strictement casher", "la plus haute d’Europe"),
  "/fr/kosher-van-transfers/": ("Transferts en van privé", "jamais le Shabbat"),
  "/fr/kosher-verbier/": ("Verbier, strictement casher", "le balcon des 4 Vallées"),
  "/fr/kosher-villa-saint-tropez/": ("Villa à Saint-Tropez", "casher, les pieds dans l’eau, plage privée"),
  "/fr/kosher-zermatt/": ("Zermatt, strictement casher", "au pied du Cervin, sans voitures"),
  "/fr/lyon-gateway-to-the-alps-kosher/": ("Lyon, la porte des Alpes", "pour le voyageur juif"),
  "/fr/montluc-prison-lyon/": ("Mémorial de Montluc", "où la Gestapo détenait les Juifs"),
  "/fr/tours/jewish-lyon/": ("Visite juive à Lyon", "Un parcours privé, jusque dans la Grande Synagogue"),
  "/fr/tours/memory-chrd/": ("Mémoire : le CHRD", "Visite privée du musée de la Résistance"),
  "/fr/tours/memory-montluc-neveh-shalom/": ("Mémoire : Montluc et Neveh Shalom", "Mémorial, puis synagogue"),
  "/fr/tours/stopover/": ("Escale à Lyon", "Trois heures dans les lieux juifs de Lyon"),
  # ---- ES
  "/es/alps/": ("Los Alpes kosher", "esquí en invierno, lagos en verano"),
  "/es/chabad-lyon/": ("Chabad en Lyon", "Ocho casas, una mesa de Shabat abierta"),
  "/es/chrd-lyon/": ("El CHRD en Lyon", "el museo de la Resistencia y la deportación"),
  "/es/flights-to-lyon/": ("Vuelos a Lyon", "el aeropuerto de los Alpes franceses"),
  "/es/grande-synagogue-lyon/": ("Gran Sinagoga de Lyon", "el interior de un edificio cerrado"),
  "/es/is-lyon-safe-for-jewish-visitors/": ("¿Es Lyon segura?", "para visitantes judíos, una respuesta directa"),
  "/es/jewish-life-around-lyon/": ("Vida judía cerca de Lyon", "Grenoble, Annecy, los Alpes"),
  "/es/jewish-lyon-itinerary-2-days/": ("Lyon judío en dos días", "comidas kosher y Shabat"),
  "/es/jewish-lyon-tours/": ("Dentro de la Gran Sinagoga de Lyon.", "La única visita que le lleva al interior. Privada, estrictamente kosher, a su medida."),
  "/es/kosher-alpe-dhuez/": ("Alpe d'Huez", "estrictamente kosher, Isère, 1.860 m"),
  "/es/kosher-annecy/": ("Annecy", "estrictamente kosher, el lago y los Aravis"),
  "/es/kosher-cervinia/": ("Cervinia", "estrictamente kosher, al pie del Cervino"),
  "/es/kosher-chalet-courchevel/": ("Chalet Flocon Doré, Courchevel", "5 suites, piscinas, chef privado"),
  "/es/kosher-chalet-megeve/": ("Chalet Loup Blanc, cerca de Megève", "10 habitaciones, Mont Blanc"),
  "/es/kosher-chalets/": ("Nuestros chalés kosher", "Les Deux Alpes, Courchevel, Megève"),
  "/es/kosher-chamonix/": ("Chamonix", "estrictamente kosher, al pie del Mont Blanc"),
  "/es/kosher-cortina/": ("Cortina d'Ampezzo", "estrictamente kosher, los Dolomitas"),
  "/es/kosher-courchevel/": ("Courchevel", "estrictamente kosher, Les 3 Vallées"),
  "/es/kosher-courmayeur/": ("Courmayeur", "estrictamente kosher, Mont Blanc italiano"),
  "/es/kosher-crans-montana/": ("Crans-Montana", "estrictamente kosher, sobre el Ródano"),
  "/es/kosher-grenoble/": ("Grenoble", "estrictamente kosher, puerta del Isère"),
  "/es/kosher-la-plagne/": ("La Plagne", "estrictamente kosher, 11 pueblos"),
  "/es/kosher-les-arcs/": ("Les Arcs", "estrictamente kosher, cuatro pueblos"),
  "/es/kosher-les-deux-alpes/": ("Les Deux Alpes", "estrictamente kosher, glaciar a 1.650 m"),
  "/es/kosher-megeve/": ("Megève", "estrictamente kosher, 445 km de pistas"),
  "/es/kosher-services-french-alps/": ("Servicios kosher", "en los Alpes: chalé, chef, comidas, Shabat"),
  "/es/kosher-shabbat-meals-catering-lyon/": ("Catering kosher", "en Lyon: comidas de Shabat, quién cocina"),
  "/es/kosher-ski-holidays-french-alps/": ("Esquí kosher", "en los Alpes: dónde rezar, a quién llamar"),
  "/es/kosher-slope-chalet-les-deux-alpes/": ("Chalet Rochebrune, Les Deux Alpes", "6 habitaciones, esquís en la puerta"),
  "/es/kosher-st-moritz/": ("St. Moritz", "estrictamente kosher, en la Engadina"),
  "/es/kosher-vacation-french-alps/": ("Vacaciones kosher", "en los Alpes, todo lo kosher resuelto"),
  "/es/kosher-val-disere/": ("Val d'Isère", "estrictamente kosher, unida a Tignes"),
  "/es/kosher-val-thorens/": ("Val Thorens", "estrictamente kosher, la más alta de Europa"),
  "/es/kosher-van-transfers/": ("Traslados en van privado", "nunca en Shabat"),
  "/es/kosher-verbier/": ("Verbier", "estrictamente kosher, 4 Vallées"),
  "/es/kosher-villa-saint-tropez/": ("Villa en Saint-Tropez", "kosher, junto al mar, playa privada"),
  "/es/kosher-zermatt/": ("Zermatt", "estrictamente kosher, al pie del Cervino"),
  "/es/lyon-gateway-to-the-alps-kosher/": ("Lyon, puerta de los Alpes", "para el viajero judío"),
  "/es/montluc-prison-lyon/": ("Memorial de Montluc", "donde la Gestapo retuvo a judíos"),
  "/es/synagogues-lyon/": ("Sinagogas en Lyon", "Dónde reza la comunidad, el Shabat"),
  "/es/tours/jewish-lyon/": ("Lyon judío", "Un paseo privado, con entrada a la Gran Sinagoga"),
  "/es/tours/memory-chrd/": ("Memoria: el CHRD", "Visita privada al museo de la Resistencia"),
  "/es/tours/memory-montluc-neveh-shalom/": ("Memoria: Montluc y Neveh Shalom", "Memorial, luego sinagoga"),
  "/es/tours/stopover/": ("Escala en Lyon", "Tres horas en el Lyon judío, el traslado espera"),
  "/es/where-to-stay-lyon-jewish-travellers/": ("Dónde alojarse en Lyon", "para quien guarda el Shabat"),
  # ---- HE
  "/he/montluc-prison-lyon/": ("אתר הזיכרון בכלא מונלוק", "המקום שבו כלא הגסטאפו יהודים"),
  "/he/tours/memory-montluc-neveh-shalom/": ("זיכרון: מונלוק ונווה שלום", "אתר הזיכרון, ואחריו בית הכנסת השני"),
}

# Générateurs de traductions : (fichier, ancien couple exact) -> nouveau couple de TITRES. Les anciens couples ne sont là que
# pour reconnaître la ligne ; une fois remplacés, la passe ne trouve plus rien (idempotent).
GEN_TRAD = {
  "_van_textes.py": {"/fr/kosher-van-transfers/": ("Transferts en van privé", "d'un point A à un point B, jamais le Shabbat"),
                     "/es/kosher-van-transfers/": ("Traslados en van privado", "de un punto A a un punto B, nunca en Shabat")},
  "_verbier_i18n.py": {"/fr/kosher-verbier/": ("Verbier, strictement casher", "sur le balcon ensoleillé des 4 Vallées"),
                       "/es/kosher-verbier/": ("Verbier, estrictamente kosher", "en el balcón soleado de los 4 Vallées")},
}
LYON = ["jewish-lyon-tours", "fr/jewish-lyon-tours", "es/jewish-lyon-tours", "he/jewish-lyon-tours"]
H1 = re.compile(r"<h1>.*?</h1>", re.S)
MD = re.compile(r"^# .*$", re.M)
PAIR = re.compile(r'h1=(["\'])(?:(?!\1).)*\1,\s*ital=(["\'])(?:(?!\2).)*\2')
DEB, FIN = "<!-- OFFRES-LYON -->", "<!-- /OFFRES-LYON -->"


def rd(p): return io.open(p, encoding="utf-8").read()


def wr(p, s):
    if DRY: return
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def esc(t): return html.escape(t, quote=False)


def page(u, blanc, dore):
    """index.html + index.md de la page u. Retourne le nombre de fichiers modifiés."""
    n = 0
    d = u.strip("/")
    h = os.path.join(d, "index.html")
    if os.path.exists(h):
        s = rd(h); t = H1.sub(lambda _: f"<h1>{esc(blanc)}<br><i>{esc(dore)}</i></h1>", s, count=1)
        if t != s: wr(h, t); n += 1
    m = os.path.join(d, "index.md")
    if os.path.exists(m):
        s = rd(m); t = MD.sub(lambda _: f"# {blanc} *{dore}*", s, count=1)
        if t != s: wr(m, t); n += 1
    return n


def pair(blanc, dore):
    q = lambda t: '"' + t.replace('"', '\\"') + '"'
    return f"h1={q(blanc)}, ital={q(dore)}"


def generateurs():
    """h1=/ital= des générateurs EN (_pages/<slug>.py, _build_tours.py) et des générateurs de traductions."""
    n = 0
    for u, (blanc, dore) in TITRES.items():
        if re.match(r"/(fr|es|he)/", u): continue
        slug = u.strip("/")
        if slug.startswith("tours/"):
            f = "_build_tours.py"
            if not os.path.exists(f): continue
            s = rd(f); m = re.search(r'dict\(slug="' + re.escape(slug[6:]) + r'"', s)
            if not m: print("  générateur sans entrée :", f, slug); continue
            mp = PAIR.search(s, m.end())
            if not mp: continue
            t = s[:mp.start()] + pair(blanc, dore) + s[mp.end():]
        else:
            f = os.path.join("_pages", slug + ".py")
            if not os.path.exists(f): continue
            s = rd(f); mp = PAIR.search(s)
            if not mp: print("  générateur sans h1= :", f); continue
            t = s[:mp.start()] + pair(blanc, dore) + s[mp.end():]
        if t != s: wr(f, t); n += 1; print("  générateur", f)
    for f, anciens in GEN_TRAD.items():
        if not os.path.exists(f): continue
        s = rd(f); t = s
        for u, (ob, od) in anciens.items():
            t = t.replace(pair(ob, od), pair(*TITRES[u]))
        if t != s: wr(f, t); n += 1; print("  générateur", f)
    return n


def heros_lyon():
    """Bloc OFFRES-LYON sous le héros de /jewish-lyon-tours/ (4 langues) : le titre revient dans le premier écran."""
    n = 0
    for d in LYON:
        h = os.path.join(d, "index.html")
        if not os.path.exists(h): continue
        s = rd(h)
        i, j, k = s.find(DEB), s.find(FIN), s.find('<section class="hero">')
        if i < 0 or k < 0 or i > k: continue
        bloc = s[i:j + len(FIN)]
        s2 = s[:i] + s[j + len(FIN):].lstrip("\r\n")
        k = s2.find('<section class="hero">'); e = s2.find("</section>", k) + len("</section>")
        s2 = s2[:e] + "\n\n" + bloc + s2[e:]
        if s2 != s: wr(h, s2); n += 1; print("  héros Lyon :", h)
    return n


if __name__ == "__main__":
    pages = sum(page(u, b, d) for u, (b, d) in TITRES.items())
    gens = generateurs()
    lyon = heros_lyon()
    print(f"{'(dry) ' if DRY else ''}{pages} fichier(s) de page, {gens} générateur(s), {lyon} héros Lyon")
