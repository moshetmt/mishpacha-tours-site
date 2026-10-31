# -*- coding: utf-8 -*-
"""Suite des retouches de l'audit du 29/10 (Moshé 30/10), idempotent :
1. fil d'Ariane de la page été : plus de « Jewish Lyon guide » entre Accueil et Été (visible + JSON-LD), 4 langues ;
2. page crédits FR/ES/HE alignée sur EN : les photos des stations (Wikimedia) manquaient depuis le 45e titre ;
   doublons retirés partout, compteur du titre recalculé, libellé du lien Source dans la langue."""
import io, re, glob

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)

ETE = "summer-in-the-alps-jewish-families/index.html"
LANGS = {".": ("Photographs", "Source"), "fr": ("Photographies", "Source"), "es": ("Fotografías", "Fuente"), "he": ("צילומים", "מקור")}
LI = re.compile(r"<li><b>(.*?)</b><span>(.*?)</span><span class=\"liens\">(.*?)</span></li>", re.S)

def fil_ete():
    k = 0
    for d in LANGS:
        p = f"{d}/{ETE}"; s = rd(p)
        n = re.sub(r'(<p class="fil lead-fil">\s*<a href="[^"]*">[^<]*</a>) / <a href="[^"]*jewish-lyon-guide/">[^<]*</a>', r"\1", s, count=1)
        n = re.sub(r'\{"@type": "ListItem", "position": 2, "name": "[^"]*", "item": "[^"]*jewish-lyon-guide/"\}, \{"@type": "ListItem", "position": 3,',
                   '{"@type": "ListItem", "position": 2,', n, count=1)
        if n != s: wr(p, n); k += 1
    print("fil été :", k, "fichiers")

def credits():
    en = rd("credits/index.html"); en_li = LI.findall(en)
    vus, base = set(), []
    for nom, meta, liens in en_li:
        cle = (nom, meta.split(" · ")[0])
        if cle in vus: continue
        vus.add(cle); base.append((nom, meta, liens))
    for d, (titre, src) in LANGS.items():
        p = f"{d}/credits/index.html"; s = rd(p); lis = LI.findall(s)
        locaux, cles = [], set()
        for nom, meta, liens in lis:
            cle = meta.split(" · ")[0]
            if cle in cles: continue
            cles.add(cle); locaux.append((nom, meta, liens))
        for nom, meta, liens in base:
            cle = meta.split(" · ")[0]
            if cle in cles: continue
            cles.add(cle); locaux.append((nom, meta, re.sub(r">Source<", f">{src}<", liens)))
        html = "".join(f'<li><b>{n}</b><span>{m}</span><span class="liens">{l}</span></li>' for n, m, l in locaux)
        m = re.search(r'(<ul class="liste-lieux">).*?(</ul>)', s, re.S)
        n = s[:m.start()] + m.group(1) + html + m.group(2) + s[m.end():]
        n = re.sub(rf"({re.escape(titre)} <small>)\d+(</small>)", rf"\g<1>{len(locaux)}\g<2>", n, count=1)
        if n != s: wr(p, n)
        print(d, "crédits :", len(lis), "->", len(locaux))

SUISSE = ["kosher-verbier", "kosher-gstaad", "kosher-davos", "kosher-ski-anywhere"]
LIVRE = [", delivered meals", ", repas livrés", ", comidas entregadas", ", comida entregada", ", entrega de comidas", ", comidas a domicilio", ", ארוחות משלוח", ", משלוח ארוחות"]

def suisse_sans_livraison():
    # formule chef seulement au-delà de 3 h (Mendel 30/10) : la carte « Chef & Shabbat » ne promet plus de repas livrés sur ces pages
    k = 0
    for d in LANGS:
        for slug in SUISSE:
            p = f"{d}/{slug}/index.html"
            try: s = rd(p)
            except OSError: continue
            n = s
            for a in LIVRE: n = n.replace(a, "")
            if n != s: wr(p, n); k += 1
    print("pages suisses sans livraison :", k)

ALT_SYNAGOGUE = {".": "The women's gallery and chandeliers inside the Grande Synagogue of Lyon",
    "fr": "La galerie des femmes et les lustres à l'intérieur de la Grande Synagogue de Lyon",
    "es": "La galería de mujeres y las lámparas en el interior de la Gran Sinagoga de Lyon",
    "he": "עזרת הנשים והנברשות בתוך בית הכנסת הגדול של ליון"}
HERO_LYON = re.compile(r'<img src="/img/h/c-juiverie-5-960\.webp" srcset="[^"]*" sizes="100vw" alt="[^"]*" width="1200" height="1600" fetchpriority="high">')

def heros_lyon_tours():
    # 31/10 (Moshé « improvise ») : le premier écran de la page des visites montre l'intérieur de la Grande Synagogue, la preuve du « seul tour qui entre », au lieu de la rue sombre
    k = 0
    for d, alt in ALT_SYNAGOGUE.items():
        p = f"{d}/jewish-lyon-tours/index.html"; s = rd(p)
        n = HERO_LYON.sub(f'<img src="/img/h/synagogue-tilsitt-galerie-960.webp" srcset="/img/h/synagogue-tilsitt-galerie-640.webp 640w, /img/h/synagogue-tilsitt-galerie-960.webp 960w, /img/h/synagogue-tilsitt-galerie-1000.webp 1000w" sizes="100vw" alt="{alt}" width="1000" height="1000" fetchpriority="high">', s, count=1)
        if n != s: wr(p, n); k += 1
    print("héros Lyon tours :", k, "pages")

if __name__ == "__main__":
    fil_ete(); credits(); suisse_sans_livraison(); heros_lyon_tours()
