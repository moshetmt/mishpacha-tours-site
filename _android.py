# -*- coding: utf-8 -*-
"""Capture Android de Mendel (26/10/2026, Chrome Android 360 px, page EN traduite par Chrome) :
la marque traduite en « circuits mishpacha » recouvre le bouton de langue, les champs date sont rognés
(« dd/mm/yy »), le texte du bouton doré de la barre basse déborde. Idempotent, toutes les pages.
    python _android.py   (depuis site-v5/)"""
import glob, re
n = 0
for p in glob.glob("**/*.html", recursive=True) + ["_gabarit.html"]:
    h = open(p, encoding="utf-8").read()
    h2 = h.replace('<span class="mot">mishpacha tours</span>', '<span class="mot" translate="no">mishpacha tours</span>')
    if h2 != h: open(p, "w", encoding="utf-8").write(h2); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* ANDROID-26-10 */" not in css:
    css += """
/* ANDROID-26-10 */ /* retours Mendel sur Chrome Android 360 px */
/* 1. La marque ne se traduit pas (translate="no") et ne touche jamais le bouton de langue. */
@media (max-width:899.98px){.nav .logo{min-width:0;flex:0 1 auto}.nav .logo .mot{white-space:nowrap}}
@media (max-width:399.98px){.nav .logo .mot{font-size:24px}.nav .logo{gap:6px}}
/* 2. Champs date : Chrome Android affiche « jj/mm/aaaa » plus un picto, trop large pour 133 px. */
@media (max-width:480px){
  #chercheur input[type=date],.lead-plan input[type=date],.cherche-bar .chercheur input[type=date]{padding-inline:10px;font-size:15px;font-variant-numeric:tabular-nums}
  #chercheur input[type=date]::-webkit-calendar-picker-indicator,.lead-plan input[type=date]::-webkit-calendar-picker-indicator{width:16px;height:16px;margin:0;padding:0}
}
/* 3. Barre basse : le bouton doré prend plus de place et son texte peut passer sur deux lignes. */
.barre-basse{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}
.barre-basse a{min-width:0;padding:0 8px;font-size:11px;letter-spacing:.1em;white-space:normal;text-align:center;line-height:1.2}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
