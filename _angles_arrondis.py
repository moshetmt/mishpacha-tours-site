# -*- coding: utf-8 -*-
"""« J'aime pas que ce soit tout carré » (Moshé 27/10/2026) : la règle « Rectangles partout » de la refonte luxe forçait
border-radius:0 sur les cartes, boutons, champs, photos et panneaux. Elle passe à un arrondi doux et unique (--rayon,
12 px ; 10 px pour les boutons et les champs). Les ronds à 50 % ne sont pas touchés. Idempotent.
    python _angles_arrondis.py   (depuis site-v5/)"""
css = open("styles.css", encoding="utf-8").read()
if "/* ANGLES-ARRONDIS */" not in css:
    i = css.index("/* Rectangles partout")
    j = css.index(".gal-btn{border-radius:0}", i)
    css = css[:j] + ".gal-btn{border-radius:var(--rayon)}" + css[j + len(".gal-btn{border-radius:0}"):]
    css += """
/* ANGLES-ARRONDIS */ /* 27/10 Moshé : plus de carrés, un arrondi doux partout */
:root{--rayon:12px;--rayon-btn:10px}
.btn-noir,.btn-hero,.cta-hero .btn-noir,.nav .liens a.nav-cta,.panneau nav a.nav-cta,.pill-noir,.cb button,.of-btn,.gal-btn,.pyt-flottant,
.barre-basse a,#chercheur input,#chercheur select,#chercheur button,.lead-final .chercheur input,.lead-final button,.demande button,form button,
.langue summary,.langue ul{border-radius:var(--rayon-btn)}
.kwp-carte,.carte,.of-carte,.hub-carte,.rp-carte,.dk-cartes>li,.minyan-corps,.prix-table ul,.mosaique figure,.reve-grille figure,
.lead3-bloc,.chercheur,.ticket,.kwp-photo,.photo-cit,.carte-osm,.dk-note p{border-radius:var(--rayon);overflow:hidden}
.reve-grille .reve-lien{border-radius:var(--rayon)}
.barre-basse{border-radius:var(--rayon) var(--rayon) 0 0;overflow:hidden}
.barre-basse a{border-radius:0}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
    print("arrondis ajoutés")
else:
    print("déjà fait")
