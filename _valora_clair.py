"""Génère valora-clair.css : la version claire (crème) des composants Valora, appliquée
aux sections marquées .clair (versions B « alterné » et C « clair » de Moshé, 27/10).

Principe : on relit valora.css et valora-form.css, on garde chaque règle qui pose une
couleur, on la re-cible sous .clair et on convertit ses couleurs (fond sombre -> crème,
texte clair -> encre, doré clair -> doré foncé lisible). Ainsi « l'intérieur des cases »
suit automatiquement : toute couleur posée par Valora a sa version claire.

Usage : python _valora_clair.py   (réécrit valora-clair.css, idempotent)
"""
import re
from pathlib import Path

ICI = Path(__file__).parent
SOURCES = ["valora.css", "valora-form.css"]
SORTIE = ICI / "valora-clair.css"

# Blanc retenu (Moshé 27/10 : « pas crème, un blanc luxe ») : Le Collectionist #F7F7F7 (relevé sur
# lecollectionist.com le 27/10), cartes blanches #FFFFFF à ombre douce et filet gris très clair.
FOND = "#F7F7F7"
FOND_ALT = "#F7F7F7"
CARTE = "#FFFFFF"
OMBRE = "0 1px 2px rgba(20,21,24,.04),0 10px 28px rgba(20,21,24,.06)"
ENCRE = "#1C1D20"
DOUX = "#4A4C50"
DOUX2 = "#6B6E73"
OR_FONCE = "#8A6416"      # doré lisible sur crème (contraste 4,9:1 sur #F3EEE7)
OR_FILET = "#9C7424"
GRAD_TEXTE = "linear-gradient(100deg,#B5852A,#7E5410)"

# Zones qui restent sombres : jamais re-ciblées.
EXCLUS = re.compile(r"\.nav\b|\.panneau|footer|\.pied\b|\.barre-basse|\.hero\b|ac-hero|lead-hero3|"
                    r"\.cb\b|header|\.strip|valora-clair|valora-visite|\.ticket|lead-final|"
                    r"reve-carte|\.reve\b|kwp-photo|kwp-seau|::selection")

def hexn(h):
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h

def rgb_of(tok):
    tok = tok.strip().lower()
    if tok.startswith("#"):
        h = hexn(tok)
        if len(h) == 7:
            return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)), 1.0
        return None
    m = re.match(r"rgba?\(([^)]*)\)", tok)
    if m:
        p = [x.strip() for x in m.group(1).replace("/", ",").split(",")]
        try:
            r, g, b = (float(x) for x in p[:3])
            a = float(p[3]) if len(p) > 3 else 1.0
            return (r, g, b), a
        except ValueError:
            return None
    if tok in ("#fff", "white"):
        return (255, 255, 255), 1.0
    return None

def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def est_dore(c):
    r, g, b = c
    return r > 150 and g > 100 and b < 150 and r - b > 60

COULEUR = re.compile(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)|\bwhite\b")

def conv(tok, prop):
    v = rgb_of(tok)
    if not v:
        return None
    c, a = v
    L = lum(c)
    fond = prop.startswith("background") or prop in ("--v-fond", "--v-carte")
    bord = prop.startswith("border") or prop.startswith("outline") or prop == "--v-trait"
    if fond:
        if L < 0.08:                        # fond sombre
            if a < 0.6:
                return f"rgba(28,29,32,{min(a, .08):.2f})"
            return CARTE if L > 0.012 else FOND
        if est_dore(c) and a < 0.5:          # voile doré léger
            return f"rgba(138,100,22,{a:.2f})"
        if L > 0.7 and a < 0.3:             # voile crème sur sombre
            return f"rgba(28,29,32,{max(a / 2, .04):.2f})"
        return None
    if bord:
        if est_dore(c):
            return "rgba(28,29,32,.09)" if a < 1 else OR_FILET
        if L > 0.6:
            return f"rgba(28,29,32,{min(max(a, .10), .25):.2f})"
        if L < 0.08 and a >= 0.6:
            return "rgba(28,29,32,.18)"
        return None
    # texte, remplissages
    if est_dore(c):
        return OR_FONCE
    if L > 0.6:
        if L > 0.8:
            return ENCRE if a > 0.7 else f"rgba(28,29,32,{a:.2f})"
        return DOUX if L > 0.45 else DOUX2
    if 0.3 < L <= 0.6:
        return DOUX2
    return None

PROPS = re.compile(r"^(color|background|background-color|background-image|border(-[a-z-]+)?|outline(-color)?|"
                   r"fill|stroke|-webkit-text-fill-color|text-decoration-color|caret-color|accent-color|"
                   r"box-shadow|--[a-z][a-z0-9-]*)$")

def conv_decl(prop, val):
    prop = prop.strip().lower()
    if not PROPS.match(prop):
        return None
    if prop == "box-shadow":
        return None
    imp = " !important" if "!important" in val else ""
    v = val.replace("!important", "").strip()
    if "gradient" in v:
        # dégradé doré en texte (background-clip:text) : version foncée ; boutons dorés : inchangés
        return None
    if prop in ("color", "-webkit-text-fill-color", "fill") and v.lower() in ("transparent",):
        return None
    if prop in ("color", "-webkit-text-fill-color", "fill"):
        c = rgb_of(v) if COULEUR.fullmatch(v) else None
        if c and lum(c[0]) < 0.05:
            return None          # texte déjà foncé (bouton doré, etc.) : on n'y touche pas
    pconv = prop
    if prop.startswith("--") and not prop.startswith("--v-"):
        toks = [rgb_of(t) for t in COULEUR.findall(v)]
        toks = [t for t in toks if t]
        if not toks:
            return None
        pconv = "background" if any(lum(c) < 0.08 and a >= 0.6 for c, a in toks) else "color"
    chang = [False]
    def rep(m):
        n = conv(m.group(0), pconv)
        if n is None:
            return m.group(0)
        chang[0] = True
        return n
    nv = COULEUR.sub(rep, v)
    if "var(--v-" in v and prop in ("color", "background", "background-color"):
        chang[0] = chang[0] or False
    if not chang[0]:
        return None
    return f"{prop}:{nv}{imp}"

def decoupe_selecteurs(s):
    out, prof, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            prof += 1
        elif ch in ")]":
            prof -= 1
        if ch == "," and prof == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out

TETE = re.compile(r"^((?:html[^\s>]*\s+)?body[^\s>]*)\s*(.*)$", re.S)

def recible(sel):
    sel = sel.strip()
    if EXCLUS.search(sel):
        return []
    m = TETE.match(sel)
    if m:
        tete, reste = m.group(1), m.group(2).strip()
    else:
        tete, reste = "body.valora", sel
    reste = re.sub(r"^main\s+", "", reste)
    if not reste or reste == "main":
        return []
    sc = ".clair:not(#z1):not(#z2):not(#z3)"
    out = [f"{tete} {sc} {reste}"]
    # variante où la section elle-même porte .clair : on accroche .clair au 1er composé
    m2 = re.match(r"([^\s>+~]+)(.*)$", reste, re.S)
    if m2 and not m2.group(1).startswith(":"):
        premier = m2.group(1)
        pseudo = re.search(r"::?[a-z-]+(\(.*\))?$", premier)
        if pseudo and not premier.startswith(("#", ".", "[")):
            pass
        elif "::" not in premier:
            out.append(f"{tete} {premier}{sc}{m2.group(2)}")
    return out

def regles(css):
    """Renvoie une liste (prelude_media_ou_None, selecteurs, declarations)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i, n, res = 0, len(css), []
    def bloc(start, media):
        j = start
        while j < n:
            k = css.find("{", j)
            if k < 0:
                return n
            fin_media = css.find("}", j)
            if media and 0 <= fin_media < k:
                return fin_media + 1
            pre = css[j:k].strip()
            if pre.startswith("@media") or pre.startswith("@supports"):
                j = bloc(k + 1, pre)
                continue
            if pre.startswith("@"):
                # @font-face, @keyframes : on saute le bloc entier (gère un niveau d'imbrication)
                d, q = 1, k + 1
                while q < n and d:
                    if css[q] == "{": d += 1
                    elif css[q] == "}": d -= 1
                    q += 1
                j = q
                continue
            e = css.find("}", k)
            res.append((media, pre, css[k + 1:e]))
            j = e + 1
        return n
    bloc(0, None)
    return res

def genere():
    lignes = [
        "/* GÉNÉRÉ par _valora_clair.py : ne pas modifier à la main. Version claire des composants Valora",
        "   pour les sections .clair (versions B et C, Moshé 27/10). Blanc Le Collectionist #F7F7F7. */",
        f"body.valora .clair{{--v-fond:{FOND};--v-carte:{CARTE};--v-texte:{ENCRE};--v-doux:{DOUX};--v-or:{OR_FONCE};--v-or-clair:{OR_FONCE};--v-trait:rgba(28,29,32,.12);background:{FOND} !important;color:{ENCRE}}}",
        f"body.valora .clair.beige,body.valora .clair .beige{{background:{FOND_ALT} !important}}",
    ]
    FIN = [
        "/* Filets de sécurité : titres, mots dorés et textes dans les sections claires */",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) :is(h1,h2,h3,h4,h5,.dk-h2):not(.reve *){{color:{ENCRE} !important}}",
        f"body.valora .clair:not(#z1):not(#z2):not(#z3):not(#z4) :is(h1,h2,h3,h4) i{{background:{GRAD_TEXTE} !important;-webkit-background-clip:text !important;background-clip:text !important;color:transparent !important;-webkit-text-fill-color:transparent !important}}",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) :is(p,li,dd,dt,td,th,small,figcaption,blockquote,.sous):not(.reve *){{color:{DOUX} !important}}",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) :is(p,li,dd,td) :is(b,strong){{color:{ENCRE} !important}}",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) :is(summary,label,dt,.sh-d,.sh-ville,b,strong):not(.reve *):not([class*=btn] *):not(button *){{color:{ENCRE} !important}}",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) span:not(.reve *):not([class*=btn] *):not(button *):not(.pill *):not([class*=photo] *):not([class*=tag]){{color:inherit !important}}",
        f"body.valora .clair:not(.reve):not(#z1):not(#z2):not(#z3):not(#z4) a:not([class*=btn]):not(.pill):not(.reve *):not([class*=carte]):not([class*=photo] *){{color:{ENCRE}}}",
        f"body.valora .clair:not(#z1):not(#z2):not(#z3):not(#z4) :is(.shabbat,.sh-moments,.sh-moment){{color:{ENCRE} !important}}",
        f"body.valora .clair:not(#z1):not(#z2):not(#z3):not(#z4) .sh-moment{{background:{CARTE} !important;border:1px solid rgba(28,29,32,.10)}}",
        f"body.valora .clair:not(#z1):not(#z2):not(#z3):not(#z4) a.pill,body.valora .clair:not(#z1):not(#z2):not(#z3):not(#z4) .pill{{color:{ENCRE} !important;border-color:rgba(28,29,32,.55) !important;background:transparent !important}}",
    ]
    vus = set()
    for src in SOURCES + ["styles.css"]:
        for media, pre, decl in regles((ICI / src).read_text(encoding="utf-8")):
            if src == "styles.css" and "hiver" not in pre:
                continue
            ds = []
            for d in decl.split(";"):
                if ":" not in d:
                    continue
                p, v = d.split(":", 1)
                c = conv_decl(p, v)
                if c:
                    ds.append(c)
            # titres en dégradé doré clair -> dégradé foncé
            if "background-clip:text" in decl.replace(" ", "") and "F6DC8C" in decl.upper():
                ds.append(f"background:{GRAD_TEXTE} !important;-webkit-background-clip:text !important;background-clip:text !important;color:transparent !important;-webkit-text-fill-color:transparent !important")
            if not ds:
                continue
            # bouton à fond sombre ou doré plein : il reste tel quel (texte compris) sur fond crème
            if re.search(r"btn|pill|button|bouton|cta|submit", pre, re.I):
                fonds = [d for d in decl.split(";") if re.match(r"\s*background(-color)?\s*:", d)]
                if any(conv_decl(*d.split(":", 1)) for d in fonds):
                    continue
            # fond d'une section entière (id, .ss, .beige) : crème de section, pas couleur de carte
            dernier = re.split(r"[\s>+~]+", decoupe_selecteurs(pre)[-1].strip())[-1]
            if re.search(r"#|\.ss|\.beige|^section", dernier):
                ds = [d.replace(CARTE, FOND_ALT) if d.startswith("background") else d for d in ds]
            if any(d.startswith("background") and CARTE in d for d in ds) and not re.search(r"#|\.ss|\.beige|^section", dernier):
                ds.append(f"box-shadow:{OMBRE}")
            sels = []
            for s in decoupe_selecteurs(pre):
                sels += recible(s)
            if not sels:
                continue
            r = ",".join(sels) + "{" + ";".join(ds) + "}"
            if media:
                r = media + "{" + r + "}"
            if r not in vus:
                vus.add(r); lignes.append(r)
    lignes += FIN
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(len(lignes), "règles ->", SORTIE.name)

if __name__ == "__main__":
    genere()
