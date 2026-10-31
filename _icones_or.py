# -*- coding: utf-8 -*-
"""Icônes dorées à la place des 14 dessins Gemini (`img/illus/w/*.webp`), décision Moshé du 30/10 :
une icône PAR CONTEXTE (le même dessin servait à 45 sujets différents), générées par Canva (jamais Gemini) dans le langage
calligraphique du flocon Winter Prestige (pleins et déliés, spirales ; le trait fin uniforme a été refusé par Moshé le 30/10),
recolorées en or Valora (#D9A93A) en local, posées en `img/illus/or/<cle>.webp` (700x700, fond transparent).

    python _icones_or.py recolorer   # PNG noirs de _icones_src/ -> img/illus/or/*.webp
    python _icones_or.py appliquer   # remplace les <img src="…/illus/w/…"> dans les 4 langues (idempotent)
    python _icones_or.py planche     # planche avant/après pour Moshé

PROMPTS : clé -> sujet (le préfixe STYLE est ajouté devant). CONTEXTES : (page EN, dessin, n-ième occurrence) -> clé ;
les copies fr/es/he ont la même structure, donc la même occurrence."""
import io, re, sys, glob, os
from PIL import Image

OR = (217, 169, 58)  # #D9A93A, l'or des icônes img/ico/or
STYLE = ("One single emblem made of calligraphic brush swashes, nothing else on the page. Strict rules: the object itself is formed by three to five "
         "long continuous strokes with thick-and-thin contrast, each stroke ending in a small spiral curl, exactly like a hand-lettered monogram; "
         "NO decorative frame, NO border ornaments, NO fleur-de-lis, NO leaves, NO symmetrical filigree around the subject; solid black on pure white; "
         "no outlines, no shading, no text, no letters; centered, generous margins, square. Subject: ")  # langage du flocon Winter Prestige (Moshé 30/10)

PROMPTS = {
  # accueil, 3 étapes
  "bulle-montagne":   "a rounded speech bubble with a small snow-capped mountain drawn inside it; nothing else.",
  "programme-jour":   "a single sheet of paper with a slightly curled bottom corner, showing four short horizontal lines as a day-by-day list and a small sun in the top corner.",
  "skieur":           "a skier gliding downhill seen from the side, knees bent, two poles, a scarf flowing behind, no facial features, on a short curved snow line.",
  # visites de Lyon, étapes et arguments
  "lettre-scellee":   "a closed envelope with a round wax seal in its centre.",
  "cle-ancienne":     "an old ornate key with a decorative bow, lying diagonally.",
  "traboule":         "a narrow vaulted stone passage seen from the front: a round arch, three steps going up inside, light at the end.",
  "bougie-memoire":   "a single memorial candle in a small plain glass, one quiet flame.",
  "archives":         "an open archive box with a few upright document folders and one small framed photograph leaning in front.",
  "fenetre-barreaux": "a small square prison window with four vertical bars and three rays of light coming through.",
  "valise-horloge":   "a classic travel suitcase standing upright, with a round clock face drawn on its side.",
  "avion-decolle":    "a small passenger airplane taking off along a dotted rising arc.",
  "avion-montagne":   "a passenger airplane coming in to land, with a range of three mountain peaks behind it.",
  "van":              "a minivan seen from the side on a straight road line, two mountain peaks in the background.",
  "meteo":            "a sun half hidden behind a cloud, with one snowflake below the cloud.",
  "carte-confluence": "a folded paper map with a location pin planted where two river lines meet.",
  "maison-izieu":     "a quiet country house with a tiled roof and shutters, a large tree beside it, one small bird in the sky.",
  "livre-guide":      "an open guidebook with a ribbon bookmark and a small location pin standing on the right page.",
  "itineraire-2-jours": "a dotted route line winding from bottom left to top right with two small flags planted along it.",
  "mikve":            "three steps descending into still water with two gentle ripple lines.",
  "mezouza":          "a door frame seen from the front with a small slanted mezuzah case fixed on the right post.",
  "cloche-repas":     "a serving cloche on a round plate, with a small hanging label tied to the handle.",
  "traiteur":         "a rectangular serving tray carrying three small covered dishes, with a ribbon bow on the front.",
  "chabbat":          "two tall Shabbat candlesticks with small flames, and beside them a kiddush wine cup; nothing else.",
  "chabbat-table":    "two Shabbat candlesticks with flames next to a loaf under a draped cloth with tassels, on a table line.",
  "synagogue":        "the front of a synagogue: a tall round-arched doorway, a round rose window above it, and twin rounded stone tablets at the very top; no cross.",
  "cimetiere":        "a rounded headstone with three small pebbles resting on its top edge, a slim cypress tree beside it.",
  "cle-serrure":      "a door keyhole plate with an old key placed just beside it.",
  "cadenas-document": "a closed padlock resting on a document sheet with three short text lines.",
  "plume-sceau":      "a quill pen laid across a sheet of paper that carries a round wax seal.",
  "contrat":          "a document sheet with a few short lines and a signature line at the bottom, a fountain pen beside it.",
  "appareil-photo":   "a classic rangefinder camera seen from the front, simple lens and viewfinder.",
  "liste-verifiee":   "a clipboard holding a sheet with three lines, each marked with a small check mark.",
  "moyen-age":        "a medieval stone tower with a narrow arched window and a small lantern hanging from an iron bracket.",
  "trois-quartiers":  "three small house rooftops side by side with a footpath line running in front of them.",
  "tram":             "the front of a modern tram with a signpost standing beside it.",
  "contact-trois":    "a telephone handset, an envelope and a speech bubble arranged together.",
}

# (page EN sans slash, dessin, n-ième occurrence dans la page à partir de 1) -> clé
CONTEXTES = {
  ("", "line-whatsapp", 1): "bulle-montagne", ("", "flat-kosher", 1): "programme-jour", ("", "flat-ski", 1): "skieur",
  ("jewish-lyon-tours", "flat-jewish-lyon", 1): "traboule", ("jewish-lyon-tours", "flat-memory", 1): "bougie-memoire",
  ("jewish-lyon-tours", "flat-stopover", 1): "valise-horloge", ("jewish-lyon-tours", "flat-izieu", 1): "maison-izieu",
  ("jewish-lyon-tours", "line-storyteller", 1): "cle-ancienne", ("jewish-lyon-tours", "line-synagogue", 1): "synagogue",
  ("jewish-lyon-tours", "line-shabbat", 1): "chabbat", ("jewish-lyon-tours", "line-private", 1): "cle-serrure",
  ("jewish-lyon-tours", "line-doorway", 1): "liste-verifiee", ("jewish-lyon-tours", "line-whatsapp", 1): "bulle-montagne",
  ("jewish-lyon-tours", "line-whatsapp", 2): "bulle-montagne", ("jewish-lyon-tours", "line-doorway", 2): "lettre-scellee",
  ("jewish-lyon-tours", "line-storyteller", 2): "cle-ancienne",
  ("jewish-cemetery-lyon", "flat-cemetery", 1): "cimetiere", ("chabad-lyon", "flat-chabad", 1): "mezouza",
  ("maison-izieu", "flat-izieu", 1): "maison-izieu", ("jewish-lyon-guide", "flat-jewish-lyon", 1): "livre-guide",
  ("jewish-lyon-itinerary-2-days", "flat-jewish-lyon", 1): "itineraire-2-jours", ("mikveh-lyon", "flat-jewish-lyon", 1): "mikve",
  ("synagogues-lyon", "flat-jewish-lyon", 1): "mezouza", ("things-to-do-in-lyon", "flat-jewish-lyon", 1): "livre-guide",
  ("kosher-restaurants-lyon", "flat-kosher", 1): "cloche-repas", ("kosher-shabbat-meals-catering-lyon", "flat-kosher", 1): "traiteur",
  ("chrd-lyon", "flat-memory", 1): "archives", ("montluc-prison-lyon", "flat-memory", 1): "fenetre-barreaux",
  ("flights-to-lyon", "flat-stopover", 1): "avion-decolle", ("jewish-life-around-lyon", "flat-stopover", 1): "carte-confluence",
  ("kosher-van-transfers", "flat-stopover", 1): "van", ("lyon-gateway-to-the-alps-kosher", "flat-stopover", 1): "avion-montagne",
  ("lyon-weather", "flat-stopover", 1): "meteo",
  ("credits", "line-doorway", 1): "appareil-photo", ("is-lyon-safe-for-jewish-visitors", "line-doorway", 1): "liste-verifiee",
  ("rue-juiverie-lyon", "line-doorway", 1): "moyen-age", ("terms", "line-doorway", 1): "contrat",
  ("legal", "line-private", 1): "plume-sceau", ("privacy", "line-private", 1): "cadenas-document",
  ("where-to-stay-lyon-jewish-travellers", "line-private", 1): "trois-quartiers",
  ("shabbat-in-lyon", "line-shabbat", 1): "chabbat-table", ("about", "line-storyteller", 1): "cle-ancienne",
  ("jewish-history-lyon", "line-storyteller", 1): "moyen-age", ("grande-synagogue-lyon", "line-synagogue", 1): "synagogue",
  ("contact", "line-whatsapp", 1): "contact-trois", ("jewish-travel-lyon-faq", "line-whatsapp", 1): "tram",
}

SRC, DST = "_icones_src", "img/illus/or"
IMG = re.compile(r'<img([^>]*?)src="((?:\.\./)?/?)img/illus/w/([a-z-]+)\.webp"([^>]*)>')

def recolorer():
    os.makedirs(DST, exist_ok=True)
    for p in sorted(glob.glob(f"{SRC}/*.png")):
        cle = os.path.splitext(os.path.basename(p))[0]
        if os.path.exists(f"{DST}/{cle}.webp"): continue
        im = Image.open(p).convert("L")
        # trait noir sur blanc -> alpha = noirceur ; marge recadrée puis carré 700 avec 8 % de marge
        a = im.point(lambda v: 255 - v); bb = a.point(lambda v: 255 if v > 40 else 0).getbbox()
        if bb: a = a.crop(bb)
        w, h = a.size; c = max(w, h); n = int(c * 1.16)
        out = Image.new("RGBA", (n, n), (0, 0, 0, 0)); col = Image.new("RGBA", a.size, OR + (255,)); col.putalpha(a)
        out.paste(col, ((n - w) // 2, (n - h) // 2), col); out = out.resize((700, 700), Image.LANCZOS)
        out.save(f"{DST}/{cle}.webp", "WEBP", quality=90, method=4); print("ok", cle)

def appliquer():
    k = 0; manque = set()
    for f in glob.glob("**/index.html", recursive=True):
        rel = f.replace("\\", "/"); d = rel.split("/")[0] if rel.count("/") >= 1 and rel.split("/")[0] in ("fr", "es", "he") else "."
        page = rel[len(d) + 1 if d != "." else 0:].replace("/index.html", "").replace("index.html", "")
        s = io.open(f, encoding="utf-8").read(); compteur = {}
        def rempl(m):
            dessin = m.group(3); compteur[dessin] = compteur.get(dessin, 0) + 1
            cle = CONTEXTES.get((page, dessin, compteur[dessin]))
            if not cle: manque.add((page, dessin, compteur[dessin])); return m.group(0)
            attrs = re.sub(r'\s(width|height)="\d+"', "", m.group(1) + m.group(4))
            return f'<img{attrs.rstrip()} src="{m.group(2)}img/illus/or/{cle}.webp" width="700" height="700" data-illus="{cle}">'
        n = IMG.sub(rempl, s)
        if n != s: io.open(f, "w", encoding="utf-8", newline="\n").write(n); k += 1
    print("pages modifiées :", k); print("contextes sans icône :", sorted(manque))

if __name__ == "__main__":
    {"recolorer": recolorer, "appliquer": appliquer}[sys.argv[1]]()
