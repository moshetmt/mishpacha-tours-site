# -*- coding: utf-8 -*-
"""QA locale : liens internes cassés, images manquantes, mots interdits, title/description, canonical. python _qa.py (depuis site-v5/)"""
import re, os, glob, html
INTERDITS = [r"\bchurch", r"\bIsrael\b", r"\bIsraeli", r"kosher-friendly", r"\bfounder", "—", r"מורת דרך", r"כשר למהדרין"]
pages = sorted(p for p in glob.glob("**/index.html", recursive=True) if not p.startswith("_"))
pass
err = 0
for p in pages:
    s = open(p, encoding="utf-8").read(); d = os.path.dirname(p)
    for m in re.finditer(r'(?:href|src)="([^"#]+)"', s):
        u = m.group(1)
        if u.startswith(("http", "mailto:", "tel:", "data:")): continue
        u = u.split("?")[0]
        if u.startswith("/"): path = u.lstrip("/")
        else: path = os.path.normpath(os.path.join(d, u)).replace("\\", "/")
        if u.endswith("/") or u == "./" or u == "": path = path.rstrip("/") + "/index.html" if path not in ("", ".") else "index.html"
        if not os.path.exists(path) and path.split("/")[0] not in ("fr", "es", "he"):
            print(f"LIEN  {p}: {u} -> {path}"); err += 1
    for pat in INTERDITS:
        for m in re.finditer(pat, re.sub(r"<script.*?</script>", "", s, flags=re.S)):
            print(f"MOT   {p}: {m.group(0)!r} ...{s[max(0,m.start()-50):m.end()+30]!r}"); err += 1
    t = re.search(r"<title>(.*?)</title>", s); dsc = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t or not (30 <= len(html.unescape(t.group(1))) <= 70): print(f"TITLE {p}: {t.group(1) if t else 'absent'} ({len(t.group(1)) if t else 0})")
    if not dsc or not (90 <= len(dsc.group(1)) <= 170): print(f"DESC  {p}: {len(dsc.group(1)) if dsc else 'absent'}")
    c = re.findall(r'rel="canonical" href="([^"]*)"', s)
    if len(c) != 1 or not c[0].endswith("/" + d.replace("\\", "/") + ("/" if d else "")) and p != "credits.html": print(f"CANON {p}: {c}")
    for s2 in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S):
        import json
        try: json.loads(s2)
        except Exception as e: print(f"LD    {p}: {e}"); err += 1
print(len(pages), "pages,", err, "erreurs bloquantes")
