"""Contrôle phase 2b : bandeau du haut (.strip, ב״ה) et barre basse du téléphone.

python _controle_p2b.py <dossier_sortie> <etiquette> [--url BASE]
Sans --url : sert ce dossier en local (http.server). Captures WebKit 390 px (haut + bas de l'écran
après défilement) et Chromium 1440 px (haut), mesures dans <etiquette>.json.
"""
import json, pathlib, sys, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
from PIL import Image

ICI = pathlib.Path(__file__).resolve().parent
PAGES = [("accueil-en", "/"), ("accueil-fr", "/fr/"), ("accueil-es", "/es/"), ("accueil-he", "/he/"),
         ("courchevel-en", "/kosher-courchevel/"), ("courchevel-fr", "/fr/kosher-courchevel/"),
         ("courchevel-es", "/es/kosher-courchevel/"), ("courchevel-he", "/he/kosher-courchevel/"),
         ("chalet-en", "/kosher-chalet-courchevel/"), ("chalet-fr", "/fr/kosher-chalet-courchevel/"),
         ("chalet-es", "/es/kosher-chalet-courchevel/"), ("chalet-he", "/he/kosher-chalet-courchevel/")]
TEL = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
           user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
JS = r"""() => {
 const cs = e => getComputedStyle(e), R = e => e.getBoundingClientRect();
 const lum = c => { const v = (c.match(/[\d.]+/g)||[]).slice(0,3).map(Number).map(x => { x/=255; return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4); }); return .2126*v[0]+.7152*v[1]+.0722*v[2]; };
 const ratio = (a,b) => { const x = lum(a), y = lum(b); return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(2); };
 const o = {};
 const s = document.querySelector('.strip');
 if (s) {
  const bh = s.querySelector('.bh'), rg = document.createRange();
  const nodes = [...s.childNodes].filter(n => n !== bh);
  rg.setStartBefore(nodes[0]); rg.setEndAfter(nodes[nodes.length-1]);
  const rects = [...rg.getClientRects()].filter(r => r.width > 0);
  const tops = [...new Set(rects.map(r => Math.round(r.top)))];
  const tr = rg.getBoundingClientRect(), br = bh ? R(bh) : null;
  const a = s.querySelector('a');
  o.strip = {display: cs(s).display, h: Math.round(R(s).height), lignes: tops.length, fs: cs(s).fontSize, ls: cs(s).letterSpacing,
   color: cs(s).color, bg: cs(s).backgroundColor, contraste: ratio(cs(s).color, cs(s).backgroundColor),
   contraste_lien: a ? ratio(cs(a).color, cs(s).backgroundColor) : null,
   texte: [Math.round(tr.left), Math.round(tr.right)], bh: br ? [Math.round(br.left), Math.round(br.right)] : null,
   bh_a_droite: br ? br.left > innerWidth/2 : null, coupe: s.scrollWidth > s.clientWidth + 1,
   ecart_bh: br ? Math.round(Math.min(Math.abs(br.left - tr.right), Math.abs(tr.left - br.right))) : null,
   chevauche: br ? !(br.left >= tr.right || br.right <= tr.left) : null};
 }
 const b = document.querySelector('.barre-basse');
 if (b) {
  const as = [...b.querySelectorAll('a')];
  o.barre = {display: cs(b).display, rect: [Math.round(R(b).top), Math.round(R(b).bottom), Math.round(R(b).height)], vh: innerHeight,
   radius: cs(b).borderRadius, bg: cs(b).backgroundColor, padding: cs(b).padding, gap: cs(b).gap,
   liens: as.map(x => ({cls: x.className, w: Math.round(R(x).width), h: Math.round(R(x).height), radius: cs(x).borderRadius,
     bg: cs(x).backgroundColor, bgimg: cs(x).backgroundImage.slice(0,40), color: cs(x).color, shadow: cs(x).boxShadow,
     border: [cs(x).borderTopWidth, cs(x).borderRightWidth, cs(x).borderBottomWidth, cs(x).borderLeftWidth, cs(x).borderTopColor].join(' '),
     svg: x.querySelector('svg') ? cs(x.querySelector('svg')).fill : null}))};
 }
 return o;
}"""


def servir():
    class Muet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Muet, directory=str(ICI))
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}"


def main():
    out = pathlib.Path(sys.argv[1]); etq = sys.argv[2]; out.mkdir(parents=True, exist_ok=True)
    base = sys.argv[sys.argv.index("--url") + 1].rstrip("/") if "--url" in sys.argv else servir()
    res = {}
    with sync_playwright() as p:
        wk = p.webkit.launch()
        for nom, ch in PAGES:
            ctx = wk.new_context(**TEL); pg = ctx.new_page()
            r = pg.goto(base + ch, wait_until="domcontentloaded")
            if not r or r.status >= 400:
                res[nom] = {"erreur": r.status if r else None}; ctx.close(); continue
            pg.evaluate("document.querySelectorAll('#cb,.cb').forEach(e=>e.remove())"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"{nom}-{etq}-arrivee.png"), clip={"x": 0, "y": 0, "width": 390, "height": 110})
            for y in (300, 700, 1000):
                pg.evaluate(f"window.scrollTo(0,{y});window.dispatchEvent(new Event('scroll'))"); pg.wait_for_timeout(350)
            pg.wait_for_timeout(600)
            res[nom] = pg.evaluate(JS)
            f = out / f"{nom}-{etq}.png"; pg.screenshot(path=str(f))
            im = Image.open(f); w, h = im.size
            haut, bas = im.crop((0, 0, w, 240)), im.crop((0, h - 260, w, h))
            comb = Image.new("RGB", (w, 240 + 20 + 260), "white"); comb.paste(haut, (0, 0)); comb.paste(bas, (0, 260))
            comb.save(out / f"{nom}-{etq}-haut-bas.png"); f.unlink()
            ctx.close()
        wk.close()
        cr = p.chromium.launch(); ctx = cr.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page()
        for nom, ch in [("accueil-en", "/"), ("accueil-he", "/he/"), ("chalet-en", "/kosher-chalet-courchevel/"), ("chalet-he", "/he/kosher-chalet-courchevel/")]:
            pg.goto(base + ch, wait_until="domcontentloaded"); pg.mouse.wheel(0, 900); pg.wait_for_timeout(900)
            res[nom + "-pc"] = pg.evaluate(JS); pg.screenshot(path=str(out / f"{nom}-pc-{etq}.png"), clip={"x": 0, "y": 0, "width": 1440, "height": 160})
        cr.close()
    (out / f"{etq}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in res.items():
        s, b = v.get("strip", {}), v.get("barre", {})
        print(k, "| strip", s.get("display"), s.get("lignes"), "l", s.get("fs"), "c", s.get("contraste"), "bh-droite", s.get("bh_a_droite"),
              "écart", s.get("ecart_bh"), "chev", s.get("chevauche"), "| barre", b.get("radius"), [(l["w"], l["radius"], l["shadow"][:20]) for l in b.get("liens", [])])


if __name__ == "__main__":
    main()
