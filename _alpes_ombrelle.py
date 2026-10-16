# -*- coding: utf-8 -*-
"""Decision operateur du 16/10 : le site couvre les Alpes (France, Suisse, Italie). Les URL ne changent pas ; seule la formulation
   « ombrelle » change : « French Alps » / « Alpes françaises » / « Alpes franceses » / « האלפים הצרפתיים » deviennent « Alps » / « Alpes »
   / « Alpes » / « האלפים » quand le texte designe l'offre entiere. Les contextes qui parlent d'un lieu precis en France (LIEU) sont
   proteges par GARDER : famille qui skie dans les Alpes francaises et atterrit a Lyon, aeroport des Alpes francaises, « organise dans
   les Alpes francaises, a deux ou trois heures de Lyon », description de la page ete (Aix-les-Bains, Annecy, Grenoble).
   Ajoute aussi la phrase d'intro de /alps/ (4 langues + _pages/alps.py).
   Ne touche jamais aux URL ni aux href, sauf le texte du message WhatsApp encode dans wa.me/?text= (c'est du texte visible).
   Exclut les six pages en cours de build par une autre session (zermatt, st-moritz, crans-montana, cervinia, courmayeur, cortina).
   Idempotent : python _alpes_ombrelle.py [--dry] (depuis site-v5/)."""
import io, re, glob, os, sys

EXCLUES = ()  # lot du 16/10 integre, plus aucune exclusion

# Contextes LIEU : proteges (remplaces par un jeton le temps du passage).
GARDER = [
    r"ski in the French Alps land in Lyon", r"skient dans les Alpes françaises", r"esquían en los Alpes franceses", r"שגולשות באלפים הצרפתיים",
    r"airport for the French Alps", r"aéroport des Alpes françaises", r"aeropuerto de los Alpes franceses", r"שדה התעופה של האלפים הצרפתיים",
    r"organises in the French Alps, two to three hours", r"organise dans les Alpes françaises, à deux", r"organiza en los Alpes franceses, a dos",
    r"מארגנת באלפים הצרפתיים, שעתיים",
    r"summer in the French Alps: synagogues", r"été casher dans les Alpes françaises : synagogues", r"Verano kosher en los Alpes franceses: sinagogas",
    r"קיץ כשר באלפים הצרפתיים: בתי כנסת",
]
GARDER_RE = re.compile("|".join(GARDER))

# Dictionnaire de remplacements (ordre : du plus specifique au plus general).
REMPLACER = [
    ("French%20Alps", "Alps"),                       # texte du message WhatsApp encode
    ("Alpes%20fran%C3%A7aises", "Alpes"),
    ("Alpes%20franceses", "Alpes"),
    ("French Alps", "Alps"),                          # « Kosher French Alps: » -> « Kosher Alps: » ; « the French Alps » -> « the Alps »
    ("Alpes françaises", "Alpes"),
    ("Alpes franceses", "Alpes"),
]
HE = re.compile(r"(אלפים) הצרפתיים")                  # גם « באלפים הצרפתיים », « האלפים הצרפתיים »

# Phrase d'intro de /alps/ : inseree apres la 1re phrase de l'intro (le panneau du hero garde sa phrase d'accroche).
INTRO = {
    "en": "From the French resorts to Switzerland and Italy: one kosher team, one request, one quote.",
    "fr": "Des stations françaises à la Suisse et à l’Italie : une équipe casher, une demande, un devis.",
    "es": "De las estaciones francesas a Suiza e Italia: un equipo kosher, una solicitud, un presupuesto.",
    "he": "מאתרי הסקי בצרפת ועד שווייץ ואיטליה: צוות כשר אחד, פנייה אחת, הצעת מחיר אחת.",
}
PREMIERE = "You have your resort, your dates and your apartment or chalet."

def langue(p):
    p = p.replace("\\", "/")
    return p.split("/")[0] if p.split("/")[0] in ("fr", "es", "he") else "en"

def exclu(p):
    q = p.replace("\\", "/").split("/")
    return any(x in EXCLUES for x in q) or p.replace("\\", "/").endswith(tuple(f"_pages/{e}.py" for e in EXCLUES))

def ombrelle(s):
    """Retourne (texte, nombre de remplacements)."""
    gardes = []
    def mettre(m):
        gardes.append(m.group(0)); return f"\x00{len(gardes)-1}\x00"
    s = GARDER_RE.sub(mettre, s)
    n = 0
    for a, b in REMPLACER:
        s, k = re.subn(re.escape(a), b, s); n += k
    s, k = HE.subn(r"\1", s); n += k
    s = re.sub(r"\x00(\d+)\x00", lambda m: gardes[int(m.group(1))], s)
    return s, n

def ajouter_intro(p, s):
    """Phrase d'intro de /alps/ (page HTML, ou source _pages/alps.py)."""
    pn = p.replace("\\", "/")
    if pn == "_pages/alps.py":
        if INTRO["en"] in s: return s
        return s.replace(PREMIERE + " ", PREMIERE + " " + INTRO["en"] + " ", 1)
    if pn not in ("alps/index.html", "fr/alps/index.html", "es/alps/index.html", "he/alps/index.html"): return s
    L = langue(pn)
    if INTRO[L] in s: return s
    if L == "en":
        return s.replace(PREMIERE + " ", PREMIERE + " " + INTRO["en"] + " ", 1)
    marque = 'class="ss wrap lead-intro"'                 # fr / es / he : le corps de l'intro suit le <p> du panneau
    i = s.find(marque)
    j = s.find("<div><p>", i) if i >= 0 else -1
    if j < 0: return s
    j += len("<div><p>")
    return s[:j] + INTRO[L] + " " + s[j:]

def fichiers():
    sorties = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    sources = glob.glob("_pages/*.py") + glob.glob("_*.py") + ["_gabarit.html", "llms.txt"]
    sources = [p for p in sources if os.path.basename(p) != "_alpes_ombrelle.py"]
    return sorted(set(p for p in sorties + sources if os.path.exists(p) and not exclu(p)))

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    par_langue = {"en": 0, "fr": 0, "es": 0, "he": 0, "sources": 0}
    fich = 0; intros = 0
    for p in fichiers():
        s = io.open(p, encoding="utf-8").read()
        t, n = ombrelle(s)
        t2 = ajouter_intro(p, t)
        if t2 != t: intros += 1
        if t2 == s: continue
        fich += 1
        cle = "sources" if (not p.endswith("index.html") or p.startswith("_")) else langue(p)
        par_langue[cle] += n
        if dry: print(f"{p}: {n} remplacement(s)" + (" + intro" if t2 != t else ""))
        else: io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
    print(("[dry] " if dry else "") + f"fichiers modifies : {fich} ; intro /alps/ : {intros} ; remplacements par langue : {par_langue}")
