# -*- coding: utf-8 -*-
"""Lot 2, accueil : retours 6 à 11 de Moshé du 05/11 (plan 06-reports/2026-11-05-retours-site-crm/plan.md, stratégie
06-reports/2026-11-06-lot2-accueil/plan-lot2.md). Les 4 accueils (/, /fr/, /es/, /he/). Idempotent : marqueur LOT2-0611 dans
le HTML, bloc /* ===LOT2-0611=== */ remplacé à chaque passage en fin de lv.css.

    python _lot2_0611.py

 6. bannière plein écran (100 svh, 560 px mini), photo et vidéo en couverture, en-tête transparent dessus (LV-ENTETE) ;
 7. les 4 carrés sous la bannière : plus de flèche blanche, carré noir 44 px à chevron or (même langage que CARTE-0511),
    légende blanche sur un voile du bas renforcé ;
 8. les 4 carrés mènent à la page de tous les services (/kosher-services-french-alps/, dans la langue de la page) ;
 9. air sous le dernier contenu quand la barre du bas (transparente depuis le 04/11) le recouvre : pied de page et fin du
    rail des chalets sur téléphone ; air autour du prix des cartes chalet ;
10. « Comment souhaitez-vous voyager » : rail horizontal de 5 cartes hautes (photo 4:5, titre sous la photo sur blanc,
    chevron or sur la photo), 5 colonnes sur ordinateur ; photos en grand (img/h/) ;
11. « Comment ça marche » : texte blanc pur sur un voile plus sombre (contraste mesuré par _mesure_contraste.py),
    étapes en escalier sur téléphone (picto à gauche, à droite, à gauche, filet d'or), 3 colonnes reliées par un filet
    sur ordinateur."""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PAGES = ["index.html", "fr/index.html", "es/index.html", "he/index.html"]
GRAND = {  # photo des cartes « voyager » -> versions larges de img/h/ (largeur, hauteur de la 960)
    "reve-ski": (960, 640), "wp-ext-bleu": (960, 720), "reve-table": (960, 644), "reve-chef": (960, 644), "annecy-lac": (960, 640)}

n = 0
for f in PAGES:
    s = open(f, encoding="utf-8").read(); o = s
    pf = "" if f == "index.html" else f.split("/")[0] + "/"
    # 8. les 4 carrés -> page de tous les services
    s = re.sub(r'(<a class="reve-lien" href=")[^"]*(")', lambda m: f"{m.group(1)}/{pf}kosher-services-french-alps/{m.group(2)}", s)
    if "<!--LOT2-0611-->" not in s:
        s = s.replace('<section class="ss reve">', '<section class="ss reve"><!--LOT2-0611-->', 1)
    # 10. photos des cartes « voyager » en grand
    for nom, (w, h) in GRAND.items():
        for base in ("img/cartes/", "/img/cartes/"):
            s = s.replace(f'<img src="{base}{nom}.webp" alt="" loading="lazy">',
                          f'<img src="/img/h/{nom}-960.webp" srcset="/img/h/{nom}-640.webp 640w, /img/h/{nom}-960.webp 960w, /img/h/{nom}-1600.webp 1600w" sizes="(min-width:900px) 240px, 78vw" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">')
    if s != o: open(f, "w", encoding="utf-8", newline="\n").write(s); n += 1
print("accueils modifiés :", n)

P = "html body.lv" + "".join(f":not(#l{i})" for i in range(1, 15))
R = "html[dir=\"rtl\"] body.lv" + "".join(f":not(#l{i})" for i in range(1, 15))
HERO = f"{P} main>section.ac-hero"
CARRE = ("content:\"\\203A\";position:absolute;inset-inline-end:10px;bottom:10px;margin:0 !important;box-sizing:border-box;display:flex;align-items:center;"
         "justify-content:center;width:44px;height:44px;padding:0 0 3px;border-radius:4px;background:#111111;color:#C2A874;font:300 28px/1 'Jost',sans-serif;"
         "letter-spacing:0;box-shadow:0 2px 6px rgba(0,0,0,.18);transform:none !important;transition:background .15s ease,color .15s ease,transform .12s ease;opacity:1")
CSS = f"""/* ===LOT2-0611=== accueil, retours 6 à 11 de Moshé du 05/11 (_lot2_0611.py) */
/* 6. bannière plein écran */
{HERO}{{height:100svh !important;min-height:560px !important;max-height:none !important;padding:0 !important;margin:0 !important;overflow:hidden !important;display:flex !important;flex-direction:column !important;justify-content:flex-end !important}}
{HERO}>:is(img,video.ac-video){{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;max-width:none !important;object-fit:cover !important;border-radius:0 !important;transform:none !important}}
{HERO}>img{{z-index:0 !important}}
{HERO}>video.ac-video{{z-index:0 !important}}
{HERO}::before{{z-index:1 !important}}
{HERO} .hero-texte{{position:relative !important;z-index:2 !important}}
/* 7. les 4 carrés (crible luxe du 06/11, 2 h 40 : « grandes photos pleine largeur, une idée par écran ») : rail de 4 grandes photos 4:5,
   légende en capitales SOUS la photo sur blanc, carré noir à chevron or sur la photo ; 4 colonnes sur ordinateur */
{P} main>section.reve{{padding-top:28px !important;padding-bottom:8px !important}}
{P} .reve-grille{{display:flex !important;grid-template-columns:none !important;gap:12px !important;overflow-x:auto !important;overflow-y:hidden !important;scroll-snap-type:x mandatory !important;margin:0 auto !important;padding:0 var(--pad,20px) 6px !important;scroll-padding-inline:var(--pad,20px) !important;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
{P} .reve-grille::-webkit-scrollbar{{display:none}}
{P} .reve-grille .reve-lien{{flex:0 0 84% !important;max-width:320px;scroll-snap-align:start;display:block !important;border-radius:0 !important;-webkit-tap-highlight-color:transparent}}
{P} .reve-grille figure{{position:relative !important;margin:0 !important;aspect-ratio:auto !important;height:auto !important;overflow:visible !important;background:#FFFFFF !important;padding:0 0 64px !important;box-sizing:border-box}}
{P} .reve-grille figure img{{position:static !important;display:block !important;width:100% !important;height:auto !important;aspect-ratio:4/5 !important;object-fit:cover !important;background:#111111;transform:none !important}}
{P} .reve-grille figcaption{{position:absolute !important;left:0 !important;right:0 !important;bottom:0 !important;height:64px !important;box-sizing:border-box;padding:14px 0 0 !important;margin:0 !important;font:300 15px/1.3 'Jost',system-ui,sans-serif !important;letter-spacing:.08em !important;text-transform:uppercase !important;color:#111111 !important;-webkit-text-fill-color:#111111 !important;background:none !important;text-shadow:none !important;text-align:start;text-wrap:balance}}
{R} .reve-grille figcaption{{letter-spacing:0 !important}}
{P} .reve-grille .reve-lien figcaption::after{{display:none !important;content:none !important}}
{P} .reve-grille figure::after{{{CARRE};bottom:74px;box-shadow:0 0 0 1px rgba(255,255,255,.3),0 2px 6px rgba(0,0,0,.18)}}
{R} .reve-grille figure::after{{content:"\\2039"}}
{P} .reve-grille .reve-lien:is(:hover,:focus-visible) figure::after{{background:#000000;color:#E8D6A6}}
{P} .reve-grille .reve-lien:active figure::after{{transform:scale(.96) !important}}
{P} .reve-grille .reve-lien:focus-visible{{outline:2px solid #111111;outline-offset:3px}}
@media (min-width:900px){{
{P} main>section.reve{{padding-top:40px !important}}
{P} .reve-grille{{display:grid !important;grid-template-columns:repeat(4,minmax(0,1fr)) !important;gap:22px !important;overflow:visible !important;margin:0 auto !important;padding:0 var(--pad,20px) !important;scroll-snap-type:none !important}}
{P} .reve-grille .reve-lien{{flex:none !important;max-width:none}}
{P} .reve-grille figcaption{{font-size:14px !important}}
}}
/* 9. air sous le dernier contenu quand la barre du bas le recouvre (téléphone), air autour du prix des cartes chalet */
@media (max-width:899.98px){{
{P}.bb-on footer.pied{{padding-bottom:calc(96px + env(safe-area-inset-bottom)) !important}}
{P} .kwp-accueil .kwp-tous{{padding-bottom:12px !important}}
{P} .kwp-carte .kwp-prix{{margin:14px 0 6px !important}}
{P} main>section.kwp:last-of-type,{P} main>section.kwp-liste{{padding-bottom:calc(72px + env(safe-area-inset-bottom)) !important}}
}}
/* 10. « Comment souhaitez-vous voyager » : rail de cartes hautes, titre sous la photo */
{P} #trips .ac-portes{{display:flex !important;grid-template-columns:none !important;grid-auto-flow:row !important;gap:12px !important;overflow-x:auto !important;overflow-y:hidden !important;scroll-snap-type:x mandatory !important;margin:24px calc(var(--pad,20px) * -1) 0 !important;padding:0 var(--pad,20px) 6px !important;scroll-padding-inline:var(--pad,20px) !important;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
{P} #trips .ac-portes::-webkit-scrollbar{{display:none}}
{P} #trips .ac-portes .hub-carte{{flex:0 0 78% !important;max-width:300px;display:flex !important;flex-direction:column !important;grid-template-columns:none !important;position:relative !important;padding:0 !important;margin:0 !important;border:0 !important;border-radius:0 !important;background:transparent !important;box-shadow:none !important;scroll-snap-align:start;color:#111111 !important;-webkit-tap-highlight-color:transparent}}
{P} #trips .ac-portes .hub-carte .photo{{position:relative !important;width:100% !important;height:auto !important;min-height:0 !important;aspect-ratio:4/5 !important;border-radius:0 !important;overflow:hidden !important;background:#111111 !important}}
{P} #trips .ac-portes .hub-carte .photo img{{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;object-fit:cover !important;transition:transform .6s cubic-bezier(.2,.7,.2,1)}}
{P} #trips .ac-portes .hub-carte:hover .photo img{{transform:scale(1.04)}}
{P} #trips .ac-portes .hub-carte .photo::after{{{CARRE}}}
{R} #trips .ac-portes .hub-carte .photo::after{{content:"\\2039"}}
{P} #trips .ac-portes .hub-carte:is(:hover,:focus-visible) .photo::after{{background:#000000;color:#E8D6A6}}
{P} #trips .ac-portes .hub-carte:active .photo::after{{transform:scale(.96) !important}}
{P} #trips .ac-portes .hub-carte .corps{{position:static !important;display:block !important;padding:14px 0 0 !important;justify-content:flex-start !important}}
{P} #trips .ac-portes .hub-carte .corps::after{{display:none !important;content:none !important}}
{P} #trips .ac-portes .hub-carte h3{{margin:0 !important;font:300 15px/1.3 'Jost',system-ui,sans-serif !important;letter-spacing:.08em !important;text-transform:uppercase !important;color:#111111 !important;-webkit-text-fill-color:#111111 !important;text-wrap:balance}}
{P} #trips .ac-portes .hub-carte p{{margin:6px 0 0 !important;font:300 14px/1.5 'Jost',system-ui,sans-serif !important;letter-spacing:0 !important;color:#5E5E5E !important;-webkit-text-fill-color:#5E5E5E !important;opacity:1 !important;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
{R} #trips .ac-portes .hub-carte h3{{letter-spacing:0 !important}}
{P} #trips .ac-portes .hub-carte .btn-noir{{display:none !important}}
{P} #trips .ac-portes .hub-carte:focus-visible{{outline:2px solid #111111;outline-offset:3px}}
{P} #trips .ac-stations-ligne{{margin-top:36px !important}}
{P} #trips .ac-stations a{{font-size:12px !important;letter-spacing:.12em !important}}
{P} #trips .ac-portes .hub-carte p,{P} #trips .sous{{text-wrap:pretty}}
@media (min-width:900px){{
{P} #trips .ac-portes{{display:grid !important;grid-template-columns:repeat(5,minmax(0,1fr)) !important;gap:22px !important;overflow:visible !important;margin:32px 0 0 !important;padding:0 !important;scroll-snap-type:none !important}}
{P} #trips .ac-portes .hub-carte{{flex:none !important;max-width:none}}
{P} #trips .ac-portes .hub-carte h3{{font-size:14px !important}}
{P} #trips .ac-portes .hub-carte p{{font-size:13.5px !important}}
}}
/* 11. « Comment ça marche » (crible luxe du 06/11 : une seule section noire par page, beaucoup de blanc) : fond blanc, pictos noirs,
   libellés en capitales fines, filets d'or ; en escalier sur téléphone, 3 colonnes reliées par un filet sur ordinateur */
{P} main>section#how{{background:#FFFFFF !important;background-image:none !important;border-top:0 !important;box-shadow:none !important;clip-path:none !important}}
{P} main>section#how :is(h2,h2 i,h2 em,li span){{color:#111111 !important;-webkit-text-fill-color:#111111 !important}}
{P} main>section#how .lv-eyebrow{{color:#A88F5E !important;-webkit-text-fill-color:#A88F5E !important}}
{P} main>section#how :is(p,.sous,ol li p){{color:#5E5E5E !important;-webkit-text-fill-color:#5E5E5E !important;font-weight:300 !important;opacity:1 !important;text-shadow:none !important;text-wrap:pretty}}
{P} main>section#how ol li img{{filter:none !important}}
{P} main>section#how ol li>b{{display:flex;align-items:center;gap:10px;color:#111111 !important;-webkit-text-fill-color:#111111 !important;font:400 11px/1.3 'Jost',system-ui,sans-serif !important;letter-spacing:.22em !important;text-transform:uppercase !important}}
{P} main>section#how ol li>b::before{{content:"";flex:none;width:22px;height:1px;background:#A88F5E}}
{R} main>section#how ol li>b{{letter-spacing:0 !important}}
@media (max-width:899.98px){{
{P} main>section#how ol{{display:grid !important;grid-template-columns:minmax(0,1fr) !important;gap:0 !important;margin-top:26px !important;text-align:start !important}}
{P} main>section#how ol li{{display:grid !important;grid-template-columns:96px minmax(0,1fr) !important;grid-template-rows:auto auto auto !important;column-gap:16px !important;align-items:start !important;padding:0 !important;margin:0 !important}}
{P} main>section#how ol li img{{grid-column:1 !important;grid-row:1 / span 3 !important;align-self:start !important;justify-self:center !important;--lv-h:78px}}
{P} main>section#how ol li :is(b,span,p){{grid-column:2 !important}}
{P} main>section#how ol li:nth-child(2){{grid-template-columns:minmax(0,1fr) 96px !important;text-align:end !important}}
{P} main>section#how ol li:nth-child(2) img{{grid-column:2 !important;transform:scaleX(-1) !important}}
{R} main>section#how ol li:nth-child(2) img{{transform:none !important}}
{P} main>section#how ol li:nth-child(2) :is(b,span,p){{grid-column:1 !important;text-align:end !important;margin-inline-start:auto !important}}
{P} main>section#how ol li:nth-child(2)>b{{justify-content:flex-end}}
{P} main>section#how ol li::after{{display:none !important;content:none !important}}
{P} main>section#how ol li+li{{position:relative !important;margin-top:0 !important;padding-top:56px !important}}
{P} main>section#how ol li+li::before{{content:"";position:absolute;top:8px;left:50%;width:1px;height:40px;margin-left:-.5px;background:linear-gradient(180deg,rgba(168,143,94,.15),#A88F5E 50%,rgba(168,143,94,.15))}}
{P} main>section#how ol li p{{margin:6px 0 0 !important;font-size:14.5px !important;line-height:1.5 !important;max-width:none !important}}
{P} main>section#how ol li>span{{font-size:19px !important;line-height:1.2 !important}}
}}
@media (min-width:900px){{
{P} main>section#how ol{{position:relative;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:48px !important;max-width:1040px !important;margin-left:auto !important;margin-right:auto !important}}
{P} main>section#how ol::before{{content:"";position:absolute;left:10%;right:10%;top:150px;height:1px;background:linear-gradient(90deg,rgba(168,143,94,0),#A88F5E 18%,#A88F5E 82%,rgba(168,143,94,0));pointer-events:none}}
{P} main>section#how ol li{{text-align:center !important}}
{P} main>section#how ol li>b{{justify-content:center;margin-top:18px !important}}
{P} main>section#how ol li>b::before{{display:none}}
{P} main>section#how ol li p{{max-width:30em !important;margin-left:auto !important;margin-right:auto !important}}
}}
/* ===/LOT2-0611=== */
"""
c = "lv.css"
s = open(c, encoding="utf-8").read()
s = re.sub(r"\n?/\* ===LOT2-0611===.*?/\* ===/LOT2-0611=== \*/\n", "", s, flags=re.S).rstrip("\n") + "\n" + CSS
open(c, "w", encoding="utf-8", newline="\n").write(s); print("LOT2-0611 posé dans lv.css")
