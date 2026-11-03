"""Mesures Playwright des fiches chalet (avant/apres charte LV phase 3). Usage : python _charte_lv_p3_chalets_mesures.py avant|apres"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8080"
RAP = pathlib.Path(__file__).resolve().parents[2] / "06-reports/2026-11-03-charte-lv-phase3/chalets"
FICHES = {"belle-etoile-EN": "/kosher-chalet-val-thorens/", "courchevel-HE": "/he/kosher-chalet-courchevel/",
          "megeve-FR": "/fr/kosher-chalet-megeve/", "aigle-royal-ES": "/es/kosher-chalet-les-menuires/"}
VUES = {"mob": (390, 844), "pc": (1440, 900)}
mode = sys.argv[1]
RAP.mkdir(parents=True, exist_ok=True)
res = {}
with sync_playwright() as p:
    for nav in ("chromium", "webkit"):
        br = getattr(p, nav).launch()
        for vue, (w, h) in VUES.items():
            ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            for nom, url in FICHES.items():
                pg = ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
                pg.goto(BASE + url, wait_until="networkidle"); pg.wait_for_timeout(600)
                r = {"hauteur": pg.evaluate("document.documentElement.scrollHeight"), "erreurs_js": errs}
                if nav == "chromium":
                    f = RAP / f"{mode}-{nom}-{vue}"
                    if vue == "mob":
                        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(300)
                        # force lazy images
                        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(800)
                        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
                        pg.screenshot(path=str(f) + ".jpg", full_page=True, type="jpeg", quality=55)
                    else:
                        pg.screenshot(path=str(f) + ".jpg", type="jpeg", quality=70)
                if mode == "apres":
                    rtl = pg.evaluate("getComputedStyle(document.documentElement).direction") == "rtl"
                    r["rail"] = pg.evaluate("""()=>{const p=document.querySelector('.lc-piste');if(!p)return null;
                      return {n:p.children.length,snap:getComputedStyle(p).scrollSnapType,sw:p.scrollWidth,cw:p.clientWidth}}""")
                    if r["rail"]:
                        pg.evaluate("document.querySelector('.lc-piste').scrollBy({left:%d*document.querySelector('.lc-piste').clientWidth,behavior:'instant'})" % (-2 if rtl else 2))
                        pg.wait_for_timeout(700)
                        r["rail_defile"] = pg.evaluate("document.querySelector('.lc-compte').textContent")
                        r["rail_sl"] = pg.evaluate("Math.round(document.querySelector('.lc-piste').scrollLeft)")
                    pg.evaluate("window.scrollTo(0,600)"); pg.wait_for_timeout(700)
                    r["colle_visible"] = pg.evaluate("(()=>{const c=document.querySelector('.lc-colle');if(!c)return null;const b=c.getBoundingClientRect();return b.top>=-1&&b.bottom>0})()")
                    r["cta"] = pg.evaluate("!!document.querySelector('.lc-cta')")
                    r["wa"] = pg.evaluate("!!document.querySelector('.lc-wa[href*=\"wa.me\"]')")
                    r["form_names"] = pg.evaluate("[...document.querySelectorAll('form.lead-plan [name]')].map(e=>e.name)")
                    r["h2_js"] = pg.evaluate("[...document.querySelectorAll('h2')].filter(h=>/function\s*\(|=>|var |document\./.test(h.textContent)).length")
                res[f"{nav}-{vue}-{nom}"] = r
                pg.close()
            ctx.close()
        br.close()
(RAP / f"mesures-{mode}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: v["hauteur"] for k, v in res.items()}, indent=0))
