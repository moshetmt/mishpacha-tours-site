# -*- coding: utf-8 -*-
"""Controle des correctifs « Is Agentic » sur un deploiement.   python _test_agentic.py https://mishpachatours.com
Verifie : 404 HTML et Markdown, negociation Markdown sur l'accueil et une page, Vary: Accept, llms.txt, JSON-LD Organization."""
import json, re, sys, urllib.request, urllib.error
B = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://mishpachatours.com"
ok = True
def get(path, accept):
    req = urllib.request.Request(B + path, headers={"Accept": accept, "User-Agent": "Mozilla/5.0 agentic-check"})
    try: r = urllib.request.urlopen(req, timeout=30); return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
def check(nom, cond, detail=""):
    global ok; ok &= bool(cond); print(("OK  " if cond else "KO  ") + nom, detail)

s, h, b = get("/__agentic-probe-zz9", "text/html"); check("404 HTML statut", s == 404, s); check("404 HTML corps", "Page not found" in b)
s, h, b = get("/__agentic-probe-zz9", "text/markdown"); check("404 MD statut", s == 404, s)
check("404 MD type", h.get("Content-Type", "").startswith("text/markdown"), h.get("Content-Type")); check("404 MD corps >= 20 car + lien", len(b) >= 20 and "llms.txt" in b)
s, h, b = get("/", "text/markdown"); check("Accueil MD statut", s == 200, s)
check("Accueil MD type", h.get("Content-Type", "").startswith("text/markdown"), h.get("Content-Type")); check("Accueil MD Vary", "accept" in h.get("Vary", "").lower(), h.get("Vary")); check("Accueil MD corps", b.startswith(("# ", "> ")))
s, h, b = get("/", "text/html"); check("Accueil HTML type", h.get("Content-Type", "").startswith("text/html"), h.get("Content-Type")); check("Accueil HTML Vary", "accept" in h.get("Vary", "").lower(), h.get("Vary"))
ld = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S)]
org = [o for blk in ld for o in (blk if isinstance(blk, list) else [blk]) if "Organization" in (o.get("@type") if isinstance(o.get("@type"), list) else [o.get("@type")])]
check("JSON-LD Organization", bool(org)); check("JSON-LD contactPoint + address", bool(org) and org[0].get("contactPoint") and org[0].get("address", {}).get("@type") == "PostalAddress")
s, h, b = get("/tours/jewish-lyon/", "text/markdown"); check("Page MD", s == 200 and h.get("Content-Type", "").startswith("text/markdown"), (s, h.get("Content-Type")))
s, h, b = get("/llms.txt", "text/plain"); check("llms.txt when-to-use", "## When to use" in b)
print("FIN", "TOUT OK" if ok else "DES KO")
sys.exit(0 if ok else 1)
