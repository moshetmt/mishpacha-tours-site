# -*- coding: utf-8 -*-
"""Lot 4 contenu (retours 17 à 21 de Moshé du 05/11/2026) : bloc CSS unique ===LOT4-0611=== en fin de lv.css.
Idempotent : le bloc est remplacé à chaque passage. Ne s'applique qu'aux pages portant la classe body « l4 »
(posée par _lot4_0611_pages.py et _lot4_0611_services.py).
  - rythme vertical sur téléphone : 64 + 64 px entre deux sections → 40 + 40 (n° 17) ;
  - liste des prix de la page services : lignes compactes, une seule photo (n° 17) ;
  - titre de la carte en capitales fines Jost comme les autres titres (n° 17) ;
  - dessins hassid retirés des titres et du bloc final des pages sans Winter Prestige (été, Lyon) (n° 19) ;
  - page Lyon : voir la section n° 19 Lyon plus bas ;
  - pages de service : voir la section n° 20.
python _lot4_0611_css.py   (depuis site-v5/)"""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = "html body.lv.l4" + "".join(f":not(#q{i})" for i in range(1, 15))     # plus fort que tout bloc antérieur (14 :not)
OR = "#A88F5E"; ORF = "#7A6440"
FILET = "linear-gradient(100deg,#8F7646,#D2BC8C 45%,#A88F5E 55%,#8F7646)"
CSS = f"""/* ===LOT4-0611=== lot 4 contenu, retours 17 à 21 du 05/11 (_lot4_0611_css.py) */
/* n° 17 : rythme vertical sur téléphone */
@media (max-width:899.98px){{
{P} main>section.ss,{P} main>div.ss{{padding-top:40px !important;padding-bottom:40px !important}}
{P} main>section.lead-intro{{padding-top:28px !important}}
{P} main>div.cta-etapes{{margin:0 !important;padding-bottom:40px !important}}
{P} main>div.cta-etapes .cta-hero{{margin:0 !important}}
{P} main .ss h2{{margin-top:0 !important}}
{P} main>section.lead-final{{padding-top:40px !important;padding-bottom:40px !important}}
{P} .bn-intro{{padding-bottom:0 !important}}
}}
/* n° 17 : prix en lignes, une seule photo */
@media (max-width:899.98px){{
{P} .repas-prix .rp-cartes{{display:block !important;margin:20px 0 0 !important}}
{P} .repas-prix .rp-carte{{display:grid !important;grid-template-columns:minmax(0,1fr) auto !important;gap:2px 14px !important;align-items:baseline !important;padding:12px 0 !important;border:0 !important;border-bottom:1px solid rgba(168,143,94,.35) !important;background:transparent !important}}
{P} .repas-prix .rp-carte img{{display:none !important}}
{P} .repas-prix .rp-carte:first-child img{{display:block !important;grid-column:1/-1 !important;aspect-ratio:3/2 !important;margin:0 0 10px !important}}
{P} .repas-prix .rp-carte span{{padding:0 !important;font-size:15px !important}}
{P} .repas-prix .rp-carte b{{padding:0 !important;font-size:17px !important;color:{ORF} !important;white-space:nowrap}}
{P} .repas-prix .prix-table ul{{margin-top:8px !important;padding:0 !important;border:0 !important}}
{P} .repas-prix .prix-table li{{padding:12px 0 !important;border-bottom:1px solid rgba(168,143,94,.35) !important;grid-template-columns:minmax(0,1fr) auto !important}}
{P} .repas-prix .prix-table li b{{text-align:end !important;color:{ORF} !important;font-size:17px !important}}
{P} .repas-prix .note{{margin-top:18px !important}}
}}
/* n° 17 : titre de carte comme les autres titres */
{P} h2.carte-titre{{font-weight:300 !important;text-transform:uppercase !important;letter-spacing:.06em !important;font-size:22px !important;line-height:1.25 !important;margin-bottom:20px !important}}
/* n° 19 : dessins hassid retirés des titres (pages sans Winter Prestige : le flocon WP reste), du pied et du bloc final */
{P}:not(.wp-nav) .dk-h2img,{P} .forme-pied,{P} main .marcheur{{display:none !important}}
{P}:not(.wp-nav) main>section.lead-final .lead-final-hassid{{display:none !important}}
{P}:not(.wp-nav) .lead-final-tete{{display:block !important}}
{P}:not(.wp-nav) .lead-final-tete>div{{max-width:30em;margin:0 auto}}
/* n° 19 Lyon (body.l4-lyon) : pastilles, cadres, dessins Gemini et icônes bleues retirés ; rails coupés remis en grille ; une section noire */
{P}.l4-lyon .filtres{{display:none !important}}
{P}.l4-lyon #tours .rail{{display:grid !important;grid-template-columns:1fr !important;gap:28px !important;overflow:visible !important;padding:0 20px !important;scroll-snap-type:none !important}}
{P}.l4-lyon #tours .rail>.carte{{width:auto !important;min-width:0 !important;max-width:none !important;flex:none !important;border:0 !important;box-shadow:none !important;border-radius:4px !important;background:transparent !important}}
{P}.l4-lyon #tours .carte .tag{{display:none !important}}
{P}.l4-lyon #tours .carte .prix b{{font-weight:500 !important}}
{P}.l4-lyon #tours .carte .detail{{border-radius:4px !important}}
{P}.l4-lyon .tuiles{{grid-template-columns:1fr !important;gap:0 !important;padding-top:8px !important}}
{P}.l4-lyon .tuiles>a{{display:block !important;border:0 !important;border-top:1px solid rgba(168,143,94,.35) !important;border-radius:0 !important;box-shadow:none !important;background:transparent !important;padding:18px 0 !important;text-align:start !important}}
{P}.l4-lyon .tuiles>a img{{display:none !important}}
{P}.l4-lyon .tuiles>a h3{{font-family:Jost,sans-serif !important;font-weight:400 !important;text-transform:uppercase !important;letter-spacing:.06em !important;font-size:14px !important;margin:0 0 4px !important}}
{P}.l4-lyon .tuiles>a p{{margin:0 !important;opacity:.8}}
{P}.l4-lyon .bande{{display:none !important}}
{P}.l4-lyon #alps .hub-carte .btn-noir,{P}.l4-lyon #alps .hub-carte span.btn-noir{{display:none !important}}
{P}.l4-lyon #why .pourquoi img{{display:none !important}}
{P}.l4-lyon #why .pourquoi>div{{border:0 !important;box-shadow:none !important;padding:16px 0 !important;border-top:1px solid rgba(168,143,94,.35) !important}}
{P}.l4-lyon .citation .photo-cit p{{font-family:Jost,sans-serif !important;font-style:normal !important;font-weight:300 !important;text-transform:uppercase !important;letter-spacing:.08em !important;font-size:18px !important;color:#fff !important;line-height:1.3 !important}}
{P}.l4-lyon .citation .photo-cit p i{{font-style:normal !important;color:inherit !important;font-weight:300 !important}}
@media (max-width:899.98px){{
{P}.l4-lyon .citation{{display:block !important}}
{P}.l4-lyon .citation .photo-cit p{{position:static !important;color:#111 !important;margin:14px 0 0 !important;padding:0 !important;text-shadow:none !important}}
{P}.l4-lyon .citation blockquote{{margin:24px 0 0 !important;padding:0 !important;max-width:100% !important;width:auto !important}}
{P}.l4-lyon .citation blockquote p{{font-size:17px !important}}
{P}.l4-lyon #why .pourquoi>div{{display:block !important}}
{P}.l4-lyon #why .pourquoi>div h3{{margin:0 0 6px !important}}
{P}.l4-lyon #how ol li{{display:block !important;padding:18px 0 !important;border-top:1px solid rgba(255,255,255,.18) !important}}
{P}.l4-lyon #how ol li b{{display:block !important;margin:0 0 6px !important}}
{P}.l4-lyon #how ol li span{{display:block !important;margin:0 0 8px !important;font-size:17px !important}}
}}
{P}.l4-lyon .citation .pill-noir{{background:transparent !important;border:0 !important;padding:0 !important;color:{ORF} !important;text-transform:uppercase !important;letter-spacing:.1em !important;font-size:12px !important;font-weight:500 !important;border-radius:0 !important}}
{P}.l4-lyon .citation blockquote p{{font-family:Jost,sans-serif !important;font-weight:300 !important;font-size:19px !important;line-height:1.5 !important}}
{P}.l4-lyon .citation .signature{{font-family:Jost,sans-serif !important;font-weight:400 !important;text-transform:uppercase !important;letter-spacing:.08em !important;font-size:13px !important;color:#111 !important}}
{P}.l4-lyon #how{{background:#111 !important;background-image:none !important;color:#fff !important}}
{P}.l4-lyon #how::before,{P}.l4-lyon #how::after{{display:none !important}}
{P}.l4-lyon #how ol li img{{display:none !important}}
{P}.l4-lyon #how ol li b{{color:{OR} !important}}
{P}.l4-lyon #how ol li span,{P}.l4-lyon #how ol li p,{P}.l4-lyon #how h2,{P}.l4-lyon #how .sous{{color:#fff !important;opacity:1 !important}}
{P}.l4-lyon #places .lieux-galerie{{display:grid !important;grid-template-columns:1fr 1fr !important;gap:12px !important;overflow:visible !important;padding:0 !important}}
{P}.l4-lyon #places .lieux-galerie figure{{width:auto !important;min-width:0 !important;max-width:none !important;flex:none !important;margin:0 !important}}
{P}.l4-lyon #places .lieux-galerie img{{width:100% !important;height:auto !important;aspect-ratio:4/5 !important;object-fit:cover !important;border-radius:4px !important}}
{P}.l4-lyon .ticket .wa{{color:{ORF} !important;text-decoration-color:{OR} !important}}
{P}.l4-lyon .ticket-hassid{{display:none !important}}
{P}.l4-lyon .of-lyon .of-plus{{border-radius:4px !important;text-transform:uppercase !important;letter-spacing:.1em !important;font-size:12px !important}}
{P}.l4-lyon .of-lyon .of-grille{{grid-auto-flow:row !important;grid-auto-columns:auto !important;grid-template-columns:1fr !important;gap:24px !important;margin-inline:0 !important;padding-inline:0 !important;overflow:visible !important;scroll-snap-type:none !important}}
{P}.l4-lyon .of-lyon .of-carte{{border:0 !important;box-shadow:none !important;padding:20px 0 0 !important;border-top:1px solid rgba(168,143,94,.35) !important;border-radius:0 !important;background:transparent !important}}
{P}.l4-lyon #tours .carte .detail{{text-transform:uppercase !important;letter-spacing:.1em !important;font-size:12px !important;font-weight:500 !important}}
{P}.l4-lyon .hero .chercheur{{border-radius:4px !important;box-shadow:none !important}}
{P}.l4-lyon .hero .chercheur button{{border-radius:4px !important}}
@media (min-width:900px){{
{P}.l4-lyon #tours .rail{{grid-template-columns:repeat(3,minmax(0,1fr)) !important;padding:0 !important}}
{P}.l4-lyon #places .lieux-galerie{{grid-template-columns:repeat(4,minmax(0,1fr)) !important}}
{P}.l4-lyon .tuiles{{grid-template-columns:repeat(2,minmax(0,1fr)) !important;column-gap:40px !important}}
}}
/* n° 20 : grille de cartes photo des 9 services sur la page casher (Moshé 06/11 : « toujours un peu vide ») */
{P} .svc-grille{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 12px;margin-top:22px}}
{P} .svc-carte{{display:block;text-decoration:none !important;color:#111 !important;border:0 !important;background:transparent !important}}
{P} .svc-carte img{{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:4px;margin:0 0 8px}}
{P} .svc-carte .svc-t{{display:block;font-family:Jost,sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.06em;font-size:12.5px;line-height:1.3}}
{P} .svc-carte .svc-s{{display:block;font-size:13px;line-height:1.35;opacity:.75;margin-top:2px}}
@media (min-width:900px){{
{P} .svc-grille{{grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 24px}}
{P} .svc-carte .svc-t{{font-size:14px}}
{P} .svc-carte .svc-s{{font-size:15px}}
}}
/* ===/LOT4-0611=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===LOT4-0611===.*?/\* ===/LOT4-0611=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("lv.css : bloc LOT4-0611 écrit,", CSS.count("\n"), "lignes")
