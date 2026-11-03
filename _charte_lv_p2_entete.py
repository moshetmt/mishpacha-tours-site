"""Phase 2 lot B1, tache 1 (03/11) : en-tete transparent sur toute page a heros.
Remplace le script /*LV-ENTETE*/ existant, sinon l'ajoute avant </body>. Idempotent.
Exclus : pages des articles Lyon (pratique-hero, lot B2), espace/ (appli Mendel)."""
import re, pathlib, io

R = pathlib.Path(__file__).parent
SEL = '.ac-hero,.lv-hero-photo,main>section.hero:not(.lead-hero3-illus)'
JS = ('<script>/*LV-ENTETE*/(function(){var b=document.body;if(!document.querySelector("' + SEL + '"))return;'
      'b.classList.add("lv-transp");var f=function(){b.classList.toggle("lv-plein",window.scrollY>60)};'
      'window.addEventListener("scroll",f,{passive:true});f()})();</script>')
ANCIEN = re.compile(r'<script>/\*LV-ENTETE\*/.*?</script>', re.S)


def pages():
    for p in sorted(R.rglob("index.html")):
        rel = p.relative_to(R).parts
        if any(x.startswith("_") for x in rel) or rel[0] in ("espace", "preview"):
            continue
        yield p


def main():
    modif = deja = exclu = detecte = 0
    hors_main = []
    for p in list(pages()) + [R / "404.html"]:
        t = io.open(p, encoding="utf-8", newline="").read()
        if "pratique-hero" in t:
            exclu += 1
            continue
        if ANCIEN.search(t):
            n = ANCIEN.sub(lambda m: JS, t, count=1)
        else:
            n = t.replace("</body>", JS + "</body>", 1)
        # controle du selecteur : heros enfant direct de <main> ?
        m = re.search(r'<section class="(hero[^"]*)"', n)
        if m and ("ac-hero" in m.group(1) or "lead-hero3-illus" not in m.group(1)):
            avant = n[:m.start()]
            j = avant.rfind("<main")
            entre = re.sub(r'<!--.*?-->', '', avant[avant.find(">", j) + 1:] if j >= 0 else "x<div", flags=re.S)
            if j < 0 or re.search(r'<(div|section|article)\b', entre):
                hors_main.append(str(p.relative_to(R)))
            else:
                detecte += 1
        if n != t:
            io.open(p, "w", encoding="utf-8", newline="").write(n)
            modif += 1
        else:
            deja += 1
    print(f"entete : {modif} pages modifiees, {deja} deja a jour, {exclu} exclues (pratique-hero)")
    print(f"heros detectes par main>section.hero ou .ac-hero : {detecte} ; heros hors <main> direct : {len(hors_main)} {hors_main[:10]}")


if __name__ == "__main__":
    main()
