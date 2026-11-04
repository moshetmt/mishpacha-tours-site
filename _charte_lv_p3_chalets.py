"""Charte LV phase 3 : fiches chalet façon fiche produit Louis Vuitton (maquette-chalet-lv, validée par Moshé le 03/11).
Réécrit le <main> des 32 fiches kosher-*chalet-*/ (4 langues). Idempotent : marqueur <!--LV-CHALET-V1--> ; second passage = 0 fichier changé.
Écrit aussi lv-chalet.css (jamais lv.css). Usage : python _charte_lv_p3_chalets.py [--dry]"""
import re, sys, glob, pathlib
from urllib.parse import urlencode
from bs4 import BeautifulSoup, NavigableString

ROOT = pathlib.Path(__file__).resolve().parent
MARQ = "<!--LV-CHALET-V2-->"
CSS_LINK = '<!--LV-CHALET-V1-css--><link rel="stylesheet" href="/lv-chalet.css?v=2"><!--/LV-CHALET-V1-css-->'
# photos écartées (rien de non casher visible) : bouteilles de mousseux et flûtes sur la table, vu le 03/11
EXCLURE = {"kosher-slope-chalet-les-deux-alpes": {"slope-salon-canape", "slope-salon-baie", "slope-sejour-table"}}
CTA_EN = "Plan your stay"
WA_SVG = '<svg class="lc-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/></svg>'

CSS_SRC = r"""/* Fiches chalet façon fiche produit LV (phase 3, 03/11). Généré par _charte_lv_p3_chalets.py, ne pas éditer à la main. */
@@{background:#fff !important;color:#111 !important;font-family:'Jost','Heebo',sans-serif;font-weight:300;letter-spacing:.01em;padding:0 !important;--filet:#E6E6E6;--gris:#5E5E5E;--or:#7A6440;--filet-or:linear-gradient(100deg,#8F7646,#D2BC8C 45%,#A88F5E 55%,#8F7646)}
@@ :is(p,li,div,span,b,small,summary,h1,h2,i){-webkit-text-fill-color:currentColor !important}
@@ .lc-fil{padding:14px 20px 12px !important;margin:0 !important;font-size:13px !important;line-height:1.5 !important;color:var(--gris) !important;text-align:start !important;background:none !important;opacity:1 !important}
@@ .lc-fil a{color:var(--gris) !important;text-decoration:underline !important;text-underline-offset:3px}
@@ .lc-galerie{position:relative;background:#FFFFFF}
@@ .lc-piste{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch}
@@ .lc-piste::-webkit-scrollbar{display:none}
@@ .lc-piste img{flex:0 0 100%;width:100%;height:auto;max-width:none !important;aspect-ratio:4/3;object-fit:cover;scroll-snap-align:start;display:block;border-radius:0 !important;filter:none !important;margin:0 !important}
@@ .lc-progres{height:2px;background:var(--filet)}
@@ .lc-progres i{display:block;height:2px;background:#111;transition:transform .2s}
@@ .lc-compte{position:absolute;inset-inline-end:14px;bottom:16px;background:rgba(255,255,255,.92);color:#111;font-size:12px;padding:4px 8px;border-radius:4px}
@@ .lc-produit{padding:24px 20px 8px}
@@ .lc-ref{margin:0 !important;font-size:12px !important;letter-spacing:.24em !important;text-transform:uppercase;color:var(--or) !important}
@@ h1.lc-h1{margin:8px 0 8px !important;padding:0 !important;font-size:clamp(22px,2.2vw,30px) !important;line-height:1.25 !important;font-weight:300 !important;color:#111 !important;text-align:start !important;max-width:none !important;width:auto !important}
@@ h1.lc-h1 i{display:block !important;margin-top:8px;font-size:.52em !important;letter-spacing:.14em !important;color:var(--gris) !important}
@@ h1.lc-h1::after{content:"";display:block;width:36px;height:1px;margin-top:16px;background:var(--filet-or)}
@@ .lc-prix{margin:14px 0 4px !important;font-size:16px !important;color:#111 !important}
@@ .lc-chiffres{margin:0 0 22px !important;font-size:14px !important;color:var(--gris) !important}
@@ .lc-btn{display:flex !important;align-items:center;justify-content:center;gap:10px;width:100%;margin:0 0 12px !important;padding:17px !important;border-radius:4px !important;font:400 16px 'Jost','Heebo',sans-serif !important;letter-spacing:.02em !important;text-transform:none !important;text-decoration:none !important;box-shadow:none !important;min-height:48px}
@@ .lc-noir{background:#111 !important;color:#fff !important;border:1px solid #111 !important}
@@ .lc-noir:hover{background:#fff !important;color:#111 !important}
@@ .lc-blanc{background:#fff !important;color:#111 !important;border:1px solid #111 !important}
@@ .lc-blanc:hover{background:#111 !important;color:#fff !important}
@@ .lc-ico{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.2;flex:none}
@@ .lc-note{margin:22px 0 12px !important;font-size:15px !important;line-height:1.6 !important;color:var(--gris) !important}
@@ .lc-desc{margin:0 0 14px !important;font-size:15px !important;line-height:1.65 !important;color:var(--gris) !important}
@@ .lc-assure{margin:10px 0 0;padding:0;list-style:none}
@@ .lc-assure li{padding:12px 0;border-top:1px solid var(--filet);font-size:14px;line-height:1.55;color:var(--gris);background:none !important}
@@ .lc-assure b{display:block;font-weight:400;color:#111;font-size:15px}
@@ .lc-accordeons{margin:30px 20px 0;border-top:1px solid var(--filet)}
@@ details.lc-plis{border:0 !important;border-bottom:1px solid var(--filet) !important;border-radius:0 !important;background:none !important;padding:0 !important;margin:0 !important}
@@ details.lc-plis>summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 0;cursor:pointer;background:none !important;border:0 !important;min-height:48px}
@@ details.lc-plis>summary::-webkit-details-marker{display:none}
@@ details.lc-plis>summary::after{content:"+";font-size:22px;font-weight:300;line-height:1;width:auto;height:auto;border:0 !important;background:none !important;color:#111 !important;position:static;transform:none}
@@ details.lc-plis[open]>summary::after{content:"\2212"}
@@ .lc-t{margin:0 !important;padding:0 !important;font-size:16px !important;line-height:1.35 !important;letter-spacing:.01em !important;text-transform:none !important;font-weight:300 !important;color:#111 !important;text-align:start !important}
@@ .lc-t::after{display:none !important}
@@ .lc-corps{padding:0 0 22px;font-size:15px;line-height:1.65;color:var(--gris)}
@@ .lc-corps :is(p,li,span,div,b){color:inherit}
@@ .lc-corps p{margin:0 0 12px}
@@ .lc-corps ul,@@ .lc-corps ol{margin:0;padding:0;list-style:none}
@@ .lc-corps li{padding:7px 0;border:0 !important;background:none !important}
@@ .lc-corps b{font-weight:400;color:#111 !important}
@@ .lc-corps ol{list-style:decimal;padding-inline-start:22px}
@@ .lc-corps a{color:#111 !important;text-decoration:underline;text-underline-offset:4px}
@@ .lc-bas{margin:0 auto}
@@ .lc-h2{margin:48px 20px 18px !important;padding:0 !important;text-align:start !important}
@@ .lc-bas-photos .lc-photos img,@@ .lc-photos img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;margin:0 0 4px;border-radius:0 !important}
@@ .lc-duo{display:grid;grid-template-columns:1fr;gap:4px}
@@ .lc-aut:last-child:nth-child(odd){grid-column:1/-1}
@@ .lc-bas-autres{margin-top:88px;padding-top:4px;border-top:1px solid var(--filet)}
@@ .lc-aut .lc-nom,@@ .lc-aut .lc-lieu{padding-inline-end:40px !important}
@@ .lc-aut::after{content:"\203A";position:absolute;inset-inline-end:16px;bottom:24px;font-size:26px;line-height:1;font-weight:300;color:#111}
@R@ .lc-aut::after{content:"\2039"}
@@ .lc-duo img{aspect-ratio:4/3 !important;margin:0 !important}
@@ .lc-autres{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--filet)}
@@ .lc-aut{position:relative;display:block;text-decoration:none !important;border-bottom:1px solid var(--filet);border-inline-end:1px solid var(--filet);color:#111 !important}
@@ .lc-aut:nth-child(2n){border-inline-end:0}
@@ .lc-aut img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#FFFFFF;border-radius:0 !important}
@@ .lc-nom{display:block;padding:14px 14px 2px;font-size:15px;line-height:1.35;color:#111 !important}
@@ .lc-lieu{display:block;padding:0 14px 18px;font-size:14px;color:var(--gris) !important}
@@ .lc-fleches{margin:18px 20px 0}
@@ .lc-fleches .lc-h2{margin:48px 0 8px !important}
@@ .lc-fl{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:1px solid var(--filet);text-decoration:none !important;font-size:16px;color:#111 !important}
@@ .lc-fl::after{content:"\203A";font-size:24px;font-weight:300}
@R@ .lc-fl::after{content:"\2039"}
@@ .lc-colle{position:fixed;top:0;left:0;right:0;z-index:70;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;background:#fff;border-bottom:1px solid var(--filet);transform:translateY(-110%);visibility:hidden;transition:transform .3s,visibility 0s .3s}
@@ .lc-colle.on{transform:none;visibility:visible;transition:transform .3s,visibility 0s}
@@ .lc-colle b{display:block;font-weight:400;font-size:15px;color:#111}
@@ .lc-colle small{font-size:13px;color:var(--gris)}
@@ .lc-mini{width:auto !important;margin:0 !important;padding:12px 18px !important;font-size:15px !important;white-space:nowrap}
@media(min-width:900px){
@@ .lc-fil{padding:18px 56px 14px !important}
@@ .lc-haut{display:grid;grid-template-columns:1.4fr 1fr;max-width:1440px;margin:0 auto;align-items:start}
@@ .lc-piste img{aspect-ratio:4/3;height:auto}
@@ .lc-produit{padding:40px 56px 0;position:sticky;top:24px}
@@ .lc-accordeons{max-width:880px;margin:48px auto 0;padding:0 56px}
@@ .lc-bas{max-width:1440px}
@@ .lc-h2{margin:64px 56px 22px !important}
@@ .lc-photos{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:0 56px}
@@ .lc-photos>img{grid-column:1/-1;aspect-ratio:2/1;margin:0}
@@ .lc-aut:last-child:nth-child(odd){grid-column:auto}
@@ .lc-duo{grid-column:span 2;grid-template-columns:1fr 1fr}
@@ .lc-duo img{aspect-ratio:4/3 !important}
@@ .lc-autres{grid-template-columns:repeat(4,1fr);margin:0 56px}
@@ .lc-aut:nth-child(2n){border-inline-end:1px solid var(--filet)}
@@ .lc-aut:nth-child(4n){border-inline-end:0}
@@ .lc-fleches{max-width:880px;margin:18px auto 0;padding:0 56px}
@@ .lc-fleches .lc-h2{margin-inline:0 !important}
@@ .lc-colle{padding:12px 56px}
}
"""

def stem(src):
    b = src.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return re.sub(r"-\d{3,4}$", "", b)

def propre(el):
    """Fragment nettoyé : plus de classes ni d'ids, plus d'images, de svg ni de scripts."""
    for t in el.find_all(["img", "svg", "script", "button"]): t.decompose()
    for t in el.find_all(True):
        for a in ("class", "style", "id"): t.attrs.pop(a, None)
    for t in el.find_all(["li", "p", "span", "div"]):
        if not t.get_text(strip=True) and not t.find(True): t.decompose()
    return el

def inner(el):
    return "".join(str(c) for c in el.contents)

def titre(h2):
    return re.sub(r"\s+", " ", h2.get_text("")).strip()

def acc(t, corps):
    return f'<details class="lc-plis"><summary><h2 class="lc-t">{t}</h2></summary><div class="lc-corps">{corps}</div></details>'

def transforme(src, slug):
    m = re.search(r"<main>(.*?)</main>", src, re.S)
    if not m: raise SystemExit("pas de <main> : " + slug)
    d = BeautifulSoup(m.group(1), "html.parser")
    kids = [c for c in d.contents if getattr(c, "name", None)]
    hero = d.find("section", class_="hero")
    fil = hero.select_one(".lead-fil")
    nomlieu = fil.get_text(" ", strip=True).split(" / ")[-1]
    nom, _, lieu = nomlieu.rpartition(",")
    nom, lieu = nom.strip(), lieu.strip()
    h1html = inner(hero.find("h1"))
    hero_img = hero.find("img", attrs={"fetchpriority": True}) or hero.select("img")[-1]
    form = d.select_one("form.lead-plan")
    action = form["action"]
    hid = {i["name"]: i.get("value", "") for i in form.select("input[type=hidden]")}
    wa = None
    for a in hero.select("a[href*='wa.me/33652092301']"):
        wa = a["href"]; break
    if not wa: wa = d.select_one(".cta-etapes a[href*='wa.me/33652092301']")["href"]
    hb = hero.select_one("a.btn-hero")
    plan = hb["href"] if hb and "plan-your-trip" in hb["href"] else action + ("?" + urlencode(hid) if hid else "")
    plan = plan.replace("&amp;", "&").replace("&", "&amp;")
    full = BeautifulSoup(src, "html.parser")
    cta = CTA_EN if full.html.get("lang") == "en" else full.select_one(".nav-cta").get_text(strip=True)
    prix = str(d.select_one("span[data-prix-tpl]"))
    chiffres = ""
    for a in full.select(".nav-ch-v"):
        if a["href"].rstrip("/").rsplit("/", 1)[-1] == slug:
            sub = a.find("span"); b = sub.find("b")
            if b: b.extract()
            chiffres = sub.get_text(" ", strip=True)
    intro = d.select_one(".lead-intro")
    phrase = intro.select_one(".mf-phrase")
    col = intro.select_one(".mf-col")
    desc = ""
    for p in intro.select("div > p"):
        if "mf-phrase" in (p.get("class") or []): continue
        p["class"] = ["lc-desc"]; desc += str(p)
    note = f'<p class="lc-note">{inner(phrase)}</p>' if phrase else ""
    items = ""
    if col:
        items = '<ul class="lc-assure">' + "".join(f"<li><b>{c.find('b').get_text(strip=True)}</b>{c.find('span').get_text(strip=True)}</li>" for c in col.find_all("div", recursive=False)) + "</ul>"
    ex = EXCLURE.get(slug, set())
    rail, vus = [], set()
    def ajoute(img, alt=None):
        s = img["src"]; st = stem(s)
        if st in vus or st in ex: return
        vus.add(st)
        rail.append((s, img.get("srcset", ""), (alt if alt is not None else img.get("alt", "")).replace('"', "&quot;")))
    ajoute(hero_img, alt=nom)
    for im in d.select(".chalet-images .ci-tuile img"): ajoute(im)
    n = len(rail)
    def tag(r, i=None, sizes="(min-width:900px) 58vw, 100vw"):
        s, ss, alt = r
        srcset = f' srcset="{ss}" sizes="{sizes}"' if ss else ""
        pos = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
        return f'<img src="{s}"{srcset} alt="{alt}" width="1264" height="848" {pos} decoding="async">'
    rail_html = "".join(tag(r, i) for i, r in enumerate(rail))
    h2_img = titre(d.select_one(".chalet-images h2"))
    picks = sorted(set(i for i in (1, n // 3, (2 * n) // 3, n - 2) if 0 < i < n))
    photos = ""
    if len(picks) >= 3:
        pc = lambda i: tag(rail[i], sizes="(min-width:900px) 40vw, 100vw")
        photos = f'<div class="lc-bas-photos"><h2 class="lc-h2">{h2_img}</h2><div class="lc-photos">{pc(picks[0])}<div class="lc-duo">{pc(picks[1])}{pc(picks[2])}</div>' + (pc(picks[3]) if len(picks) > 3 else "") + '</div></div>'
    accs, fleches, autres, garde, lead_final = [], "", "", [], ""
    for c in kids:
        cl = set(c.get("class") or [])
        if c is hero or "lead-intro" in cl or "chalet-images" in cl: continue
        if cl & {"cta-etapes", "minyan-bh", "shabbat-bloc", "kwp-seul-bandeau"}: continue
        if "lead-final" in cl: lead_final = re.search(r'<section class="ss lead-final".*?</section>', m.group(1), re.S).group(0); continue
        if c.select_one(".carte-osm"): garde.append(("carte", str(c))); continue
        if c.select_one("p.source"): garde.append(("source", str(c))); continue
        if "kwp-mini" in cl:
            cards = []
            for a in c.select("a.kwp-v"):
                nm, _, pl = a.find("b").get_text(strip=True).partition(" · ")
                cards.append(f'<a class="lc-aut" href="{a["href"]}"><img src="{a.find("img")["src"]}" alt="" width="336" height="224" loading="lazy"><span class="lc-nom">{nm}</span><span class="lc-lieu">{pl}</span></a>')
            autres = f'<div class="lc-bas-autres"><h2 class="lc-h2">{titre(c.find("h2"))}</h2><div class="lc-autres">{"".join(cards)}</div></div>'
            continue
        if c.select_one("ul.dk-suite"):
            lis = "".join(f'<a class="lc-fl" href="{li.find("a")["href"]}">{li.find("a").get_text(strip=True)}</a>' for li in c.select("ul.dk-suite li"))
            fleches = f'<div class="lc-fleches"><h2 class="lc-h2">{titre(c.find("h2"))}</h2>{lis}</div>'
            continue
        h2 = c.find("h2")
        if "faq" in cl:
            qa = "".join(f"<li><b>{x.find('summary').get_text(strip=True)}</b> {inner(propre(x.find('p')))}</li>" for x in c.find_all("details"))
            accs.append(acc(titre(h2), f'<ul class="lc-faq">{qa}</ul>')); continue
        if "etapes" in cl:
            li = "".join(f"<li><b>{x.find('h3').get_text(strip=True)}</b> {inner(propre(x.find('p')))}</li>" for x in c.select("ol > li"))
            accs.append(acc(titre(h2), f'<ol class="lc-et">{li}</ol>')); continue
        if "lead-offre" in cl:
            li = "".join(f"<li><b>{f.find('b').get_text(strip=True)}</b> {''.join(str(t) for t in f.find('figcaption').contents if isinstance(t, NavigableString))}</li>" for f in c.select("figure"))
            accs.append(acc(titre(h2), f'<ul class="lc-liste">{li}</ul>')); continue
        if h2 is None: raise SystemExit(f"bloc inconnu {slug}: {sorted(cl)}")
        t = titre(h2); h2.decompose()
        accs.append(acc(t, inner(propre(c))))
    if not lead_final: raise SystemExit("formulaire lead-final absent : " + slug)
    sticky = f'<div class="lc-colle" id="lcColle" aria-hidden="true"><div><b>{nom}</b><small>{prix}</small></div><a class="lc-btn lc-noir lc-mini" href="{plan}" tabindex="-1">{cta}</a></div>'
    out = f'''{MARQ}{sticky}
<div class="lc-fil fil">{inner(fil)}</div>
<div class="lc-haut">
  <div class="lc-galerie"><div class="lc-piste" id="lcPiste">{rail_html}</div><div class="lc-progres"><i id="lcBarre" style="width:{100 / n:.3f}%"></i></div><span class="lc-compte" id="lcCompte" dir="ltr">1 / {n}</span></div>
  <div class="lc-produit">
    <p class="lc-ref">{lieu}</p>
    <h1 class="lc-h1">{h1html}</h1>
    <p class="lc-prix">{prix}</p>
    <p class="lc-chiffres">{chiffres}</p>
    <a class="lc-btn lc-noir lc-cta" id="lcCta" href="{plan}">{cta}</a>
    <a class="lc-btn lc-blanc lc-wa" href="{wa}" rel="noopener">{WA_SVG}WhatsApp</a>
    {note}{desc}{items}
  </div>
</div>
<div class="lc-bas">
  <div class="lc-accordeons">{"".join(accs)}</div>
  {"".join(h for k, h in garde if k == "carte")}
  {photos}
  {autres}
</div>
{lead_final}
{fleches}
{"".join(h for k, h in garde if k == "source")}
<script>
(function(){{var p=document.getElementById('lcPiste'),b=document.getElementById('lcBarre'),c=document.getElementById('lcCompte');if(!p)return;var n=p.children.length,rtl=getComputedStyle(p).direction==='rtl';
p.addEventListener('scroll',function(){{var i=Math.round(Math.abs(p.scrollLeft)/p.clientWidth);b.style.transform='translateX('+(rtl?-i:i)*100+'%)';c.textContent=(i+1)+' / '+n}},{{passive:true}});
var s=document.getElementById('lcColle');if(s){{var f=function(){{var on=window.scrollY>480;s.classList.toggle('on',on);s.setAttribute('aria-hidden',on?'false':'true');s.querySelector('a').tabIndex=on?0:-1}};window.addEventListener('scroll',f,{{passive:true}});f()}}}})();
</script>
'''
    new = src[:m.start()] + '<main class="lc">' + out + "</main>" + src[m.end():]
    new = re.sub(r"<!--GALERIE:overlay-->.*?<!--/GALERIE:overlay-->\s*", "", new, flags=re.S)
    new = new.replace("<!--/CHARTE-LV-->", "<!--/CHARTE-LV-->" + CSS_LINK, 1)
    return new, n

def css():
    P = "html body.valora.lv" + "".join(f":not(#lv{i})" for i in range(1, 9)) + " main.lc"
    R = P.replace("html body", 'html[dir="rtl"] body', 1)
    return CSS_SRC.replace("@R@", R).replace("@@", P)

def main():
    dry = "--dry" in sys.argv
    fs = sorted(glob.glob(str(ROOT / "kosher-*chalet-*/index.html")) + glob.glob(str(ROOT / "*/kosher-*chalet-*/index.html")))
    chg = tot = 0
    for f in fs:
        p = pathlib.Path(f); s = p.read_text(encoding="utf-8"); tot += 1
        if MARQ in s: continue
        new, n = transforme(s, p.parent.name)
        chg += 1
        print(f"{p.relative_to(ROOT).parent} : {n} photos")
        if not dry: p.write_text(new, encoding="utf-8", newline="")
    cp = ROOT / "lv-chalet.css"; nc = css()
    if not cp.exists() or cp.read_text(encoding="utf-8") != nc:
        if not dry: cp.write_text(nc, encoding="utf-8", newline="")
        print("lv-chalet.css écrit")
    print(f"{chg} fiche(s) modifiée(s) sur {tot}")

main()
