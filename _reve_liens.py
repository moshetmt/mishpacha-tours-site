# -*- coding: utf-8 -*-
"""Accueil, bande des 4 visuels « rêve » (Moshé 26/10/2026, « cliquable avec effet ») : chaque visuel devient un lien vers
la page qui en parle, avec un zoom doux de la photo et une flèche dans la légende au survol. 4 langues, idempotent.
    python _reve_liens.py   (depuis site-v5/)"""
import os, re
CIBLES = {"reve-table": "kosher-chalets", "reve-chef": "kosher-services-french-alps",
          "reve-ski": "kosher-ski-holidays-french-alps", "reve-traineau": "kosher-vacation-french-alps"}
n = 0
for l in ("", "fr", "es", "he"):
    p = (l + "/" if l else "") + "index.html"
    h = open(p, encoding="utf-8").read()
    if 'class="reve-lien"' in h:
        continue
    def lien(m):
        cle = m.group(2)
        cible = CIBLES[cle]
        assert os.path.exists((l + "/" if l else "") + cible + "/index.html"), (l, cible)
        return f'<a class="reve-lien" href="{"/" + l if l else ""}/{cible}/">{m.group(1)}</a>'
    h2 = re.sub(r'(<figure><img src="/?img/cartes/(reve-[a-z]+)\.webp".*?</figure>)', lien, h, flags=re.S)
    assert h2.count('class="reve-lien"') == 4, p
    open(p, "w", encoding="utf-8").write(h2); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* REVE-LIENS */" not in css:
    css += """
/* REVE-LIENS */ /* accueil : les 4 visuels sont des liens, zoom doux et flèche au survol (Moshé 26/10) */
.reve-grille .reve-lien{display:block;color:inherit;text-decoration:none;border-radius:inherit;-webkit-tap-highlight-color:transparent}
.reve-grille .reve-lien img{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.reve-grille .reve-lien figcaption::after{content:"→";display:inline-block;margin-inline-start:8px;transition:transform .3s ease}
[dir=rtl] .reve-grille .reve-lien figcaption::after{content:"←"}
.reve-grille .reve-lien:focus-visible{outline:2px solid var(--jaune,#C9A961);outline-offset:3px}
@media (hover:hover){
  .reve-grille .reve-lien:hover img{transform:scale(1.06)}
  .reve-grille .reve-lien:hover figcaption::after{transform:translateX(4px)}
  [dir=rtl] .reve-grille .reve-lien:hover figcaption::after{transform:translateX(-4px)}
}
.reve-grille .reve-lien:active figure{transform:scale(.98);transition:transform .15s ease}
@media (prefers-reduced-motion:reduce){.reve-grille .reve-lien img,.reve-grille .reve-lien figcaption::after{transition:none}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
