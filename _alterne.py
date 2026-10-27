"""Alternance intelligente noir / blanc luxe sur toutes les pages Valora (Moshé 27/10 : « mettre en valeur
les call to action et ce qui demande du luxe »). Règle : REGLES-VALORA.md, section « Alternance ».

python _alterne.py           -> réécrit les pages (idempotent) + génère valora-alterne.css

- NOIR : bannières, barre de réservation, 4 visuels, cartes chalets (kwp*), « Le chalet en images »,
  étapes + leurs boutons, galerie villa, bloc final, encart d'appel Lyon, bande « Nous marchons dans ».
- BLANC (.clair, blanc pur The Row #FFFFFF) : tout le reste (information). Dans une suite de sections blanches,
  une sur deux prend .clair-2 (filet gris en haut) pour garder un rythme.
- Pages Lyon (valora-clair / valora-visite) : pas de .clair, leur thème clair passe du crème au blanc (CSS).
- Icônes : img/des/*.webp -> img/ico/or/*.svg (selon le texte de la ligne quand c'est évident),
  doré foncé sur blanc par content:url.
"""
import re, os
from pathlib import Path
from _theme_bc import Enfants, offset

ICI = Path(__file__).parent
NOIR = {"hero", "lead-hero3", "pratique-hero", "demande-hero", "ac-hero", "cherche-bar", "reve", "kwp",
        "kwp-mini", "kwp-hub", "kwp-accueil", "kwp-seul-bandeau", "chalet-images", "etapes", "cta-etapes",
        "lead-final", "ticket-zone", "cta-pratique", "galerie-wp", "bande", "fiche-hero"}
ICOS = {f[:-4] for f in os.listdir(ICI / "img/ico/or")}
PAR_TEXTE = [(r"(Surface|Superficie|שטח)", "x-ruler"), (r"(Chambres|Bedrooms|Habitaciones|חדרי)", "x-bed"),
             (r"(Salon|Living|Sal[oó]n|סלון)", "x-couch"), (r"(Salles? de bain|Bathrooms?|Baños?|חדרי רחצה)", "x-bathtub"),
             (r"(Extérieur|Outdoors?|Exterior|חוץ)", "x-tree"), (r"(Emplacement|Les vues|Location|The views|Ubicación|Las vistas|מיקום|הנוף)", "x-mountains"),
             (r"(Cuisine|Kitchen|Cocina|מטבח)", "chef-hat"), (r"(Salle à manger|Dining|Comedor|פינת אוכל|חדר אוכל)", "x-fork")]
CREME_BLANC = {"#f7f3ec": "#FFFFFF", "#f0e9dc": "#FFFFFF", "#fffdf9": "#FFFFFF", "#e6dccb": "#E8E8E8",
               "#f3ece0": "transparent", "#4a4640": "#4A4C50", "rgba(255,253,249,.97)": "rgba(255,255,255,.97)",
               "#faf7f0": "#FFFFFF", "#fbf8f3": "#FFFFFF", "#f3eee7": "#FFFFFF"}
LIENS = '<link rel="stylesheet" href="/valora-clair.css"><link rel="stylesheet" href="/valora-alterne.css">'


def icones(s):
    def rep(m):
        nom = m.group(2)
        suite = re.sub(r"<[^>]+>", " ", s[m.end():m.end() + 300]).strip()
        for motif, ico in PAR_TEXTE:
            if re.match(motif, suite):
                nom = ico
                break
        if nom not in ICOS:
            return m.group(0)
        return f'{m.group(1)}/img/ico/or/{nom}.svg"'
    return re.sub(r'(src=")/img/des/([\w-]+)\.webp"', rep, s)


def ajoute_classe(html, o, cls):
    fin = html.index(">", o)
    b = html[o:fin]
    m = re.search(r'class="([^"]*)"', b)
    if m:
        if cls in m.group(1).split():
            return html
        nb = b[:m.start(1)] + cls + " " + m.group(1) + b[m.end(1):]
    else:
        nb = b + f' class="{cls}"'
    return html[:o] + nb + html[fin:]


def traite(html):
    m = re.search(r'<body class="([^"]*)"', html)
    if not m or "valora" not in m.group(1).split():
        return html
    body = m.group(1).split()
    lyon = bool({"valora-clair", "valora-visite"} & set(body))
    if not lyon:
        p = Enfants(); p.feed(html)
        tons = []
        for pos, tag, cls in p.res:
            c = set(cls.split())
            tons.append((pos, "noir" if c & NOIR else "blanc"))
        marques = []
        run = 0
        for pos, ton in tons:
            if ton == "blanc":
                marques.append((pos, ["clair"] + (["clair-2"] if run % 2 == 1 else [])))
                run += 1
            else:
                run = 0
        for pos, classes in sorted(marques, key=lambda e: e[0], reverse=True):
            o = offset(html, pos)
            for c in reversed(classes):
                html = ajoute_classe(html, o, c)
    html = icones(html)
    m = re.search(r'<body class="([^"]*)"', html)
    if "theme-b" not in m.group(1).split():
        html = html.replace(m.group(0), f'<body class="{m.group(1)} theme-b"', 1)
    lien = '<link rel="stylesheet" href="/valora.css">'
    if "valora-alterne.css" not in html and lien in html:
        if "valora-clair.css" in html:
            html = html.replace('<link rel="stylesheet" href="/valora-clair.css">', LIENS, 1)
        else:
            html = html.replace(lien, lien + LIENS, 1)
    return html


def css():
    src = (ICI / "valora.css").read_text(encoding="utf-8")
    lyon = []
    for r in re.findall(r"[^{}]+\{[^{}]*\}", src):
        sel, decl = r.split("{", 1)
        if "@" in sel or not re.search(r"valora-(visite|clair)", sel):
            continue
        if not any(k in decl.lower().replace(" ", "") for k in CREME_BLANC):
            continue
        d = decl
        for a, b in CREME_BLANC.items():
            d = re.sub(re.escape(a).replace(r"\,", r",\s*"), b, d, flags=re.I)
        sels = ",".join(re.sub(r"(?<![\w-])body(?![\w-])", "body.theme-b", s.strip(), count=1)
                        if re.search(r"(?<![\w-])body(?![\w-])", s) else "body.theme-b " + s.strip()
                        for s in sel.split(","))
        lyon.append(sels + "{" + d)
    swap = []
    for k in sorted(ICOS):
        a = f'img[src="/img/ico/or/{k}.svg"]'
        swap.append(f'body.theme-b .clair {a},body.theme-b.valora-visite main section:not(.ticket-zone):not(.bande):not(.hero):not(.fiche-hero) {a},'
                    f'body.theme-b.valora-clair main section:not(.ticket-zone):not(.pratique-hero):not(.cta-pratique) {a}{{content:url(/img/ico/or-fonce/{k}.svg)}}')
    base = """/* GÉNÉRÉ par _alterne.py : ne pas modifier à la main. Alternance noir / blanc luxe (Moshé 27/10). */
body.valora.theme-b{--c-fond:#FFFFFF}
html body.valora.theme-b main>.clair:not(.clair-2):not(#z1):not(#z2):not(#z3):not(#z4){background:#FFFFFF !important;background-image:none !important;--v-fond:#FFFFFF}
/* sections blanches pleine largeur et collées (pas de bande sombre entre deux blancs) */
html body.valora.theme-b main>.clair:not(#z1):not(#z2):not(#z3):not(#z4){margin-top:0 !important;margin-bottom:0 !important;padding-top:56px !important;padding-bottom:56px !important;box-shadow:0 0 0 100vmax #FFFFFF !important;clip-path:inset(0 -100vmax) !important}
body.valora.theme-b main>.clair+:not(.clair){margin-top:0 !important;padding-top:56px}
@media (min-width:900px){html body.valora.theme-b main>.clair:not(#z1):not(#z2):not(#z3):not(#z4){padding-top:80px !important;padding-bottom:80px !important}}
/* suite de sections blanches : une sur deux en blanc pur, cartes gris très clair */
html body.valora.theme-b main>.clair.clair-2:not(#z1):not(#z2):not(#z3):not(#z4){--v-fond:#FFFFFF;background:#FFFFFF !important;background-image:none !important;border-top:1px solid #ECECEC !important}
/* cartes sur blanc pur (The Row) : filet gris très clair + ombre très douce */
html body.valora.theme-b main>.clair:not(#z1):not(#z2):not(#z3) :is(.dk-cartes>li,.liste-lieux>li,.dk-suite>li,.minyan-corps,.faq details,.hub-carte,.ac-van,.ac-lyon-liste>li,.shabbat,.dk-garanties,.dk-note,.conseils details){background:#FFFFFF !important;border:1px solid #E8E8E8 !important;box-shadow:0 6px 22px rgba(20,21,24,.05) !important}
html body.valora.theme-b.valora-visite main :is(.tuiles a,.tuile,.deux-cartes>*,.prix-table,.garanties-fiche li,.preuves li),html body.valora.theme-b.valora-clair main :is(.of-lyon a,.hub-carte,.liste-lieux>li,.dk-suite>li,.faq details){border:1px solid #E8E8E8 !important;box-shadow:0 6px 22px rgba(20,21,24,.05) !important}
/* petite voiture du bloc van (et icônes de bloc isolé) agrandies */
html body.valora.theme-b main .ac-van img[src*="/img/ico/"]{width:56px !important;height:56px !important;flex:0 0 56px !important}
@media (min-width:900px){html body.valora.theme-b main .ac-van img[src*="/img/ico/"]{width:64px !important;height:64px !important;flex-basis:64px !important}}
html body.valora.theme-b main .dk-note img[src*="/img/ico/"],html body.valora.theme-b main .shabbat img[src*="/img/ico/"]{width:40px !important;height:40px !important;flex-basis:40px !important}
/* Bloc Lyon de l'accueil, téléphone : titre et texte posés sur la photo (voile), la photo s'arrête avant les 3 points ; ordinateur inchangé */
@media (max-width:899px){
html body.valora #tours.ac-lyon .ac-lyon-grille{display:grid !important;grid-template-columns:1fr !important;gap:0 !important;padding:0 !important}
html body.valora #tours.ac-lyon .ac-lyon-grille>div:last-child{display:contents !important}
html body.valora #tours.ac-lyon .ac-lyon-photo{align-self:stretch !important;grid-row:1/3 !important;grid-column:1 !important;position:relative !important;aspect-ratio:auto !important;height:auto !important;min-height:0 !important;border-radius:22px !important;overflow:hidden !important;margin:0 !important}
html body.valora #tours.ac-lyon .ac-lyon-photo img{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;object-fit:cover !important;border-radius:0 !important}
html body.valora #tours.ac-lyon .ac-lyon-photo::after{content:"" !important;position:absolute !important;inset:0 !important;left:0 !important;bottom:0 !important;padding:0 !important;border-radius:0 !important;background:linear-gradient(180deg,rgba(20,21,24,.05) 0%,rgba(20,21,24,.55) 40%,rgba(20,21,24,.92) 100%) !important;backdrop-filter:none !important}
html body.valora:not(#z1):not(#z2):not(#z3):not(#z4) #tours.ac-lyon .ac-lyon-grille h2{grid-row:1 !important;grid-column:1 !important;position:relative;z-index:1;margin:0 !important;padding:190px 20px 0 !important;color:#FFFFFF !important;text-shadow:0 2px 14px rgba(0,0,0,.5)}
html body.valora:not(#z1):not(#z2):not(#z3):not(#z4) #tours.ac-lyon .ac-lyon-grille h2 i{background:linear-gradient(100deg,#F6DC8C,#E2B44A 45%,#C8902A) !important;-webkit-background-clip:text !important;background-clip:text !important;color:transparent !important;-webkit-text-fill-color:transparent !important}
html body.valora:not(#z1):not(#z2):not(#z3):not(#z4) #tours.ac-lyon .ac-lyon-grille>div:last-child>p:not(.ac-guide){grid-row:2 !important;grid-column:1 !important;position:relative;z-index:1;margin:0 !important;padding:12px 20px 26px !important;color:#F5F2EC !important}
html body.valora #tours.ac-lyon .ac-lyon-liste{grid-row:3 !important;margin-top:20px !important}
html body.valora #tours.ac-lyon .ac-boutons{grid-row:4 !important}
html body.valora #tours.ac-lyon .ac-guide{grid-row:5 !important}
}
/* FAQ sur blanc : marges intérieures */
html body.valora.theme-b main .clair:is(.faq) details,html body.valora.theme-b main .clair .faq details{border-radius:14px !important;margin-bottom:10px !important}
html body.valora.theme-b main .clair:is(.faq) summary,html body.valora.theme-b main .clair .faq summary{padding:16px 18px !important;gap:12px}
html body.valora.theme-b main .clair:is(.faq) details>*:not(summary),html body.valora.theme-b main .clair .faq details>*:not(summary){padding:0 18px 16px !important}
html[dir="rtl"] body.valora.theme-b main .clair:is(.faq) summary{padding:16px 18px !important}
/* Lyon : encart « voyage en préparation » = carte noire sur fond blanc (évite deux noirs collés avec le bloc final) */
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) .cta-pratique>div{background:#141518 !important;border-radius:22px !important;padding:32px 22px !important;text-align:center;box-shadow:0 14px 34px rgba(20,21,24,.18) !important}
/* Lyon : les appels à l'action (bloc final, encart « voyage en préparation ») passent en noir pour ressortir */
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) .ticket-zone{background:#141518 !important;background-image:none !important;box-shadow:0 0 0 100vmax #141518 !important;clip-path:inset(0 -100vmax) !important;padding-top:56px !important;padding-bottom:56px !important;margin-top:0 !important;margin-bottom:0 !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) :is(.ticket,.cta-carte,.cta-pratique-carte,.carte){background:#24272C !important;border:1px solid rgba(217,169,58,.32) !important;box-shadow:none !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) :is(h2,h3,p,li,span,small,label,b,strong){color:#F5F2EC !important;-webkit-text-fill-color:#F5F2EC !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) :is(p,small,li){color:#CFCAC1 !important;-webkit-text-fill-color:#CFCAC1 !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) :is(h2,h3) i{background:linear-gradient(100deg,#F6DC8C,#E2B44A 45%,#C8902A) !important;-webkit-background-clip:text !important;background-clip:text !important;color:transparent !important;-webkit-text-fill-color:transparent !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) a:not(.btn-noir):not(.pill):not([class*="btn"]){color:#F6DC8C !important;-webkit-text-fill-color:#F6DC8C !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) :is(.btn-noir,a[class*="btn"]){background:linear-gradient(100deg,#F6DC8C,#E2B44A 45%,#C8902A) !important;color:#141518 !important;-webkit-text-fill-color:#141518 !important;border:0 !important;border-radius:999px !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) .pill{background:transparent !important;border:1px solid #D9A93A !important;color:#F6DC8C !important;-webkit-text-fill-color:#F6DC8C !important;border-radius:999px !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) img[src*="picto-hassid"]{content:url(/img/picto-hassid-or-lumiere.svg) !important;filter:none !important}
html body.theme-b.valora:is(.valora-visite,.valora-clair):not(#z1):not(#z2):not(#z3):not(#z4) :is(.ticket-zone,.cta-pratique) svg{fill:currentColor}
/* boutons : pleins dorés arrondis, secondaires en contour arrondi (bannières des pages pratiques et sections blanches) */
html body.valora.theme-b:not(#z1):not(#z2) :is(.pratique-hero,.demande-hero,main>.clair) a.btn-noir:not(.hub-carte *):not(.kwp-carte *):not(.ac-van *),html body.valora.theme-b:not(#z1):not(#z2) .cta-hero .btn-noir{display:inline-flex !important;align-items:center !important;justify-content:center !important;gap:10px !important;min-height:46px !important;padding:12px 22px !important;border-radius:999px !important;background:linear-gradient(100deg,#F6DC8C,#E2B44A 45%,#C8902A) !important;color:#141518 !important;-webkit-text-fill-color:#141518 !important;border:0 !important;font:600 12px/1.25 Heebo,sans-serif !important;letter-spacing:.12em !important;text-transform:uppercase !important;text-decoration:none !important;box-shadow:none !important}
html body.valora.theme-b:not(#z1):not(#z2) :is(.pratique-hero,.demande-hero,main>.clair) .btn-noir svg{width:18px;height:18px;fill:currentColor}
html body.valora.theme-b:not(#z1):not(#z2) .pratique-hero .pill{display:inline-flex !important;align-items:center !important;justify-content:center !important;min-height:46px !important;padding:12px 22px !important;border-radius:999px !important;background:transparent !important;border:1px solid #D9A93A !important;color:#F6DC8C !important;-webkit-text-fill-color:#F6DC8C !important;font:600 12px/1.25 Heebo,sans-serif !important;letter-spacing:.12em !important;text-transform:uppercase !important}
html body.valora.theme-b.valora-clair:not(#z1):not(#z2) .pratique-hero .pill,html body.valora.theme-b:not(#z1):not(#z2) main>.clair .pill{border-color:#8A6416 !important;color:#8A6416 !important;-webkit-text-fill-color:#8A6416 !important;border-radius:999px !important}
html[dir="rtl"] body.valora.theme-b :is(.pratique-hero,main>.clair) :is(.btn-noir,.pill){letter-spacing:0 !important}
/* icônes au trait fin doré, sans cercle ni fond */
html body.valora.theme-b main img[src*="/img/ico/"]{background:none !important;padding:0 !important;border-radius:0 !important;box-shadow:none !important;border:0 !important;object-fit:contain !important;width:28px !important;height:28px !important;flex:0 0 28px !important}
html body.valora.theme-b main .etapes img[src*="/img/ico/"],html body.valora.theme-b main #how img[src*="/img/ico/"]{width:36px !important;height:36px !important;flex-basis:36px !important}
html body.valora.theme-b main .dk-h2img[src*="/img/ico/"]{width:44px !important;height:44px !important}
/* horaires de Chabbat dans une section blanche */
html body.valora.theme-b .clair .shabbat{background:#FFFFFF !important;border:1px solid #E8E8E8 !important;box-shadow:0 10px 28px rgba(20,21,24,.06) !important}
html body.valora.theme-b .clair .shabbat,html body.valora.theme-b .clair .shabbat *{color:#1C1D20 !important}
html body.valora.theme-b .clair .shabbat small,html body.valora.theme-b .clair .shabbat .doux,html body.valora.theme-b .clair .shabbat p{color:#4A4C50 !important}
html body.valora.theme-b .clair .shabbat h2 i,html body.valora.theme-b .clair .shabbat h3 i{color:#8A6416 !important;-webkit-text-fill-color:#8A6416 !important;background:none !important}
/* « + » de la FAQ en doré foncé sur blanc */
html body.valora.theme-b .clair.faq summary::after,html body.valora.theme-b .clair .faq summary::after,html body.valora.theme-b.valora-visite .faq summary::after,html body.valora.theme-b.valora-clair .faq summary::after{background:transparent !important;border:1px solid #8A6416 !important;color:#8A6416 !important}
/* bannière illustrée (van) : voile sombre pour lire le titre */
html body.valora.theme-b .lead-hero3-illus{position:relative}
html body.valora.theme-b .lead-hero3-illus::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(20,21,24,.35),rgba(20,21,24,.78));pointer-events:none}
html body.valora.theme-b .lead-hero3-illus>*:not(img){position:relative;z-index:2}
html body.valora.theme-b .lead-hero3-illus .lead3-bloc{background:rgba(20,21,24,.78) !important;backdrop-filter:blur(4px);border-radius:20px;padding:22px 18px !important;margin:0 16px !important}
"""
    (ICI / "valora-alterne.css").write_text(base + "/* icônes en doré foncé sur fond blanc */\n" + "\n".join(swap)
                                          + "\n/* Lyon : crème -> blanc luxe */\n" + "\n".join(lyon) + "\n", encoding="utf-8")
    return len(lyon)


def main():
    n = 0
    for f in ICI.rglob("*.html"):
        rel = f.relative_to(ICI).parts
        if rel[0] in ("preview", "node_modules") or rel[0].startswith(".") or "sections-a-valider" in rel:
            continue
        t = f.read_text(encoding="utf-8")
        t2 = traite(t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8", newline=""); n += 1
    print("pages :", n, "· règles Lyon :", css())


if __name__ == "__main__":
    main()
