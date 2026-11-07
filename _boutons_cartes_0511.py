# -*- coding: utf-8 -*-
"""05/11 (Moshe, cartes « autres chalets » des fiches) : « je n'aime pas les fleches comme ca ; je veux un bouton, imagine une
   personne agee, est-ce qu'elle le verrait ? ... fond noir et petite fleche en dore ». La fleche ::after de .lc-aut (lv-chalet.css)
   devient un bouton noir de 44 px, coins 4 px, chevron or. Bloc CARTE-0511 de lv.css, remplace a chaque passage.
   python _boutons_cartes_0511.py"""
import re, pathlib
P = "html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7):not(#lv8):not(#lv9)"
CSS = f"""
/* ===CARTE-0511=== cartes « autres chalets » : bouton noir 44 px, chevron or (_boutons_cartes_0511.py) */
{P} main.lc .lc-aut::after{{content:"\\203A";position:absolute;inset-inline-end:14px;bottom:16px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0 0 3px;border-radius:4px;background:#111111;color:#C2A874;font-size:28px;line-height:1;font-weight:300;box-shadow:0 2px 6px rgba(0,0,0,.18)}}
{P} main.lc .lc-aut:is(:hover,:focus-visible)::after{{background:#000000;color:#E8D6A6}}
{P} main.lc .lc-aut :is(.lc-nom,.lc-lieu){{padding-inline-end:66px !important}}
html[dir="rtl"] {P} main.lc .lc-aut::after{{content:"\\2039"}}
/* ===/CARTE-0511=== */
"""
c = pathlib.Path("lv.css"); s = c.read_text(encoding="utf-8")
s = re.sub(r"\n/\* ===CARTE-0511===.*?/\* ===/CARTE-0511=== \*/\n", "", s, flags=re.S) + CSS
c.write_text(s, encoding="utf-8", newline="\n"); print("CARTE-0511 posé")
