# -*- coding: utf-8 -*-
"""Retours de Moshé du 17/11 (après la mise en ligne des bannières) :
 1. carte « Table de Chabbat » sans icône (pain retiré le 03/11, jamais remplacé) : flamme (bougies) ;
 2. texte « trop pâle » sur tout le site : gris du texte courant foncés, épaisseur 300 -> 400 ;
 3. fiche visite « trop blanche » : « Déroulement de la visite » devient la section noire de la page ;
 4. encart de cacherout : le gros bloc devient une ligne fine (« Cacher lamehadrin », Beth Habad de Grenoble-Alpes,
    Rav Yehia Lahiany), sous les boutons sur les fiches chalet, à la place du bloc ailleurs ; plus de « Repas 'Halav
    Yisrael · Service shomer Chabbat » (Moshé : la surveillance de Grenoble le dit déjà) ;
 5. sceau rond de la photo refait en verre fumé.

    python _retours_1711.py

Idempotent (marqueurs RET-1711, bloc RET-1711 de lv.css)."""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

BLOC = re.compile(r'<!--CACH-0511--><div class="lc-cach"><div class="cach" role="note">.*?</div></div><!--/CACH-0511-->', re.S)
BLOC2 = re.compile(r'(?:<!--CACH-0511-->)?<div class="cach" role="note">.*?<span class="cach-or">.*?</span>(?:</span>)?</div>(?:<!--/CACH-0511-->)?', re.S)
OR = re.compile(r'<span class="cach-or">(.*?)(?:<span class="cach-or-r">(.*?)</span>)?</span>(?:</span>)?</div>', re.S)
ICO = '<img class="of-ico ico-fin" src="/img/ico/fin/flame.svg" alt="" width="28" height="28" loading="lazy">'

def signature(bloc):
    m = OR.search(bloc)
    if not m: return None
    txt, rav = m.group(1).strip(), (m.group(2) or "").strip()
    if "למהדרין" in txt and "," not in txt: tete, suite = "כשר למהדרין", txt.replace("כשר למהדרין", "", 1).strip()
    else:
        tete, _, suite = txt.partition(","); suite = suite.strip()
        if suite: suite = suite[0].upper() + suite[1:]
    if suite and rav: suite += ", "
    return f'<!--RET-1711--><p class="cach-sig"><img src="/img/logo-bh-or-300.webp" alt="" width="300" height="240" loading="lazy"><span><b>{tete.strip()}</b>{suite}{rav}</span></p>'

n_ico = n_ch = n_aut = 0; titres = set(); rates = []
for f in sorted(glob.glob("**/index.html", recursive=True)):
    s = open(f, encoding="utf-8").read(); o = s
    # 1. icône manquante
    for m in re.finditer(r'<article class="of-carte of-sans-ico" role="listitem"><h3>(.*?)</h3>', s):
        titres.add(m.group(1)[:40])
    s, k = re.subn(r'<article class="of-carte of-sans-ico" role="listitem"><h3>', '<article class="of-carte" role="listitem">' + ICO + '<h3>', s); n_ico += k
    # 4. encart
    if "RET-1711" not in s:
        m = BLOC.search(s)
        if m and 'class="lc-btn lc-blanc lc-wa"' in s:
            sig = signature(m.group(0))
            if sig:
                s = s.replace(m.group(0), "", 1)
                s = re.sub(r'(<a class="lc-btn lc-blanc lc-wa".*?</a>)', lambda x: x.group(1) + "\n    " + sig, s, count=1, flags=re.S); n_ch += 1
        else:
            m = BLOC2.search(s)
            if m:
                sig = signature(m.group(0))
                if sig: s = s.replace(m.group(0), sig, 1); n_aut += 1
                else: rates.append(f)
            elif 'class="cach"' in s: rates.append(f)
    if s != o: open(f, "w", encoding="utf-8").write(s)
print("icônes remises :", n_ico, sorted(titres)[:8])
print("encart en ligne fine : fiches chalet", n_ch, "| autres pages", n_aut, "| non traitées", rates[:6])

# 2. gris du texte courant (feuilles en vigueur et restes Valora encore chargés)
GRIS = {"#4A4C50": "#2E2E2E", "#5E5E5E": "#333333", "#6B6B6B": "#3A3A3A"}
for css in ("lv.css", "lv-chalet.css", "styles.css", "wp-v3.css", "valora.css", "valora-alterne.css", "valora-clair.css"):
    if not os.path.exists(css): continue
    t = open(css, encoding="utf-8").read(); o = t
    for a, b in GRIS.items(): t = t.replace(a, b)
    if t != o: open(css, "w", encoding="utf-8").write(t)

Q = "html body.lv" + "".join(f":not(#r{i})" for i in range(1, 18))
D = f"{Q}.valora-visite main>section.deroule"
OR_ = "linear-gradient(100deg,#8C7448 0%,#D9C48E 13%,#F3E6BE 19%,#D9C48E 25%,#8C7448 33%,#7A6440 40%,#B89C62 70%,#9C8250 85%,#7A6440 100%)"
CSS = f"""/* ===RET-1711=== texte plus lisible, déroulé en noir, cacherout en ligne fine, sceau en verre fumé (_retours_1711.py) */
{Q} main :is(p,li,dd,dt,small):not(.lv-eyebrow):not(.hero-sous):not(.lv-reassure){{font-weight:400 !important}}
{Q} main .deroule li p{{opacity:1 !important}}
{D}{{background:#111111 !important;box-shadow:0 0 0 100vmax #111111 !important;clip-path:inset(0 -100vmax) !important;max-width:none !important;padding-top:56px !important;padding-bottom:56px !important;margin-top:48px !important}}
{D} :is(h2,h2 i,h3){{color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;background:none !important}}
{D} li p{{color:#D9D9D9 !important;-webkit-text-fill-color:#D9D9D9 !important}}
{D} li>b{{background:#C2A874 !important;color:#111111 !important;-webkit-text-fill-color:#111111 !important;border:0 !important}}
@media (min-width:900px){{{D}>*{{max-width:820px;margin-left:auto !important;margin-right:auto !important}}}}
{Q} main .cach-sig{{display:flex !important;align-items:center;gap:14px;margin:22px 0 4px !important;padding:16px 0 0 !important;border-top:1px solid #A88F5E;text-align:start;max-width:520px}}
{Q} main :is(section,div.wrap)>.cach-sig{{margin:28px auto !important;padding:16px 20px 0 !important}}
{Q} main .cach-sig img{{flex:0 0 46px;width:46px !important;height:auto !important;margin:0 !important}}
{Q} main .cach-sig span{{display:block;font:400 13px/1.5 'Jost',system-ui,sans-serif !important;color:#7A6440 !important;-webkit-text-fill-color:#7A6440 !important;letter-spacing:.02em}}
{Q} main .cach-sig b{{display:block;margin:0 0 3px;font:500 10.5px/1.5 'Jost',system-ui,sans-serif !important;letter-spacing:.16em;text-transform:uppercase;color:#111111 !important;-webkit-text-fill-color:#111111 !important}}
html[dir="rtl"] body.lv main .cach-sig b{{letter-spacing:0 !important;font-size:13px !important}}
{Q} .cach-bulle{{width:84px !important;height:84px !important;background:rgba(17,17,17,.58) !important;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:none !important}}
{Q} .cach-bulle::before{{inset:3px !important;border:1px solid rgba(217,196,142,.75) !important}}
{Q} .cach-bulle .cach-bulle-t{{background:none !important;-webkit-background-clip:border-box !important;background-clip:border-box !important;color:#E8D6A6 !important;-webkit-text-fill-color:#E8D6A6 !important;font-size:6.5px !important;letter-spacing:.14em !important;max-width:58px !important}}
{Q} .cach-bulle .cach-bulle-logo{{width:46px !important;background:{OR_} 50% 0/300% 100% !important;animation:none !important}}
@media (min-width:900px){{{Q} .cach-bulle{{width:100px !important;height:100px !important}}{Q} .cach-bulle .cach-bulle-logo{{width:56px !important}}{Q} .cach-bulle .cach-bulle-t{{font-size:7.5px !important;max-width:70px !important}}}}
/* ===/RET-1711=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===(RET|ENC)-1711===.*?/\* ===/(RET|ENC)-1711=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("css ok")
