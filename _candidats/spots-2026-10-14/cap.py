import sys
from playwright.sync_api import sync_playwright
from pathlib import Path
import http.server, threading, functools, os
root = Path(sys.argv[1]).resolve(); path = sys.argv[2]; out = sys.argv[3]
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch()
    for nom, vp, dpr in (('d', {'width':1440,'height':900}, 1), ('m', {'width':390,'height':844}, 2)):
        pg = b.new_page(viewport=vp, device_scale_factor=dpr)
        pg.goto('http://127.0.0.1:8765/' + path.lstrip('/'), wait_until='networkidle'); pg.wait_for_timeout(1500)
        for y in range(0, 12000, 600): pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(60)
        pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{out}-{nom}.png', full_page=True); pg.close()
    b.close()
srv.shutdown()
