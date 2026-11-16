# -*- coding: utf-8 -*-
"""Retours de Moshé du 17/11 sur la préversion des bannières (captures iPhone) : textes illisibles, texte collé aux bords,
boutons de cartes pas alignés, autres chalets en pile sur téléphone. Scan des 363 pages : E:/taches/scan_defauts.py.

    python _lisible_1711.py

Cause des textes illisibles : valora-alterne.css (thème sombre abandonné le 30/10) force encore -webkit-text-fill-color
en clair sur .ticket-zone, .cta-pratique et .etapes ; la charte LV n'avait corrigé que `color`.
CSS seulement (bloc LIS-1711 de lv.css), aucun HTML touché. Idempotent."""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Q = "html body.lv" + "".join(f":not(#q{i})" for i in range(1, 17))
N = "#111111 !important;-webkit-text-fill-color:#111111 !important"
CSS = f"""/* ===LIS-1711=== lisibilité, cadres, alignement, rail des chalets (_lisible_1711.py) */
{Q} :is(.ticket-zone,.cta-pratique) :is(h2,h3,p,li,span,small,label,b,strong):not(.btn-noir):not(.btn-noir *):not(.lc-btn):not(.lc-btn *){{color:{N}}}
{Q} :is(.ticket-zone,.cta-pratique) :is(.fiche-note,small){{color:#5E5E5E !important;-webkit-text-fill-color:#5E5E5E !important}}
{Q} .ticket .wa,{Q} .ticket .wa *{{color:{N};text-decoration-color:#111111 !important}}
{Q} .ticket .wa svg{{fill:#111111 !important}}
{Q}.valora-visite section.beige.etapes :is(h2,h2 i,h3,li b,li span){{color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;background:none !important}}
{Q}.valora-visite section.beige.etapes :is(p,li p){{color:#CFCAC1 !important;-webkit-text-fill-color:#CFCAC1 !important}}
{Q} .garanties-fiche ul>li{{border:0 !important;border-bottom:1px solid #E8E8E8 !important;box-shadow:none !important;background:none !important;padding:16px 0 !important}}
{Q} .garanties-fiche ul>li:last-child{{border-bottom:0 !important}}
{Q} .of-carte .of-plus{{margin-top:auto !important}}
{Q} .of-carte .of-btn{{margin-top:12px !important}}
{Q} .of-carte>p{{margin-bottom:14px !important}}
@media (max-width:899.98px){{
{Q} main.lc .lc-autres{{display:flex !important;grid-template-columns:none !important;overflow-x:auto !important;overflow-y:hidden !important;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;gap:14px !important;margin:0 -20px !important;padding:0 20px 6px !important;scroll-padding-inline:20px;border-top:0 !important}}
{Q} main.lc .lc-autres::-webkit-scrollbar{{display:none}}
{Q} main.lc .lc-autres>.lc-aut{{flex:0 0 68% !important;max-width:300px;scroll-snap-align:start;grid-column:auto !important;border:0 !important;padding:0 0 4px !important;margin:0 !important}}
{Q} main.lc .lc-autres>.lc-aut img{{width:100% !important;height:auto !important;aspect-ratio:3/2;object-fit:cover}}
}}
/* ===/LIS-1711=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===LIS-1711===.*?/\* ===/LIS-1711=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("css ok")
