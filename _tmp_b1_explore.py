import re, pathlib
R = pathlib.Path(__file__).parent
t = (R/"404.html").read_text(encoding="utf-8"); m = (R/"merci/index.html").read_text(encoding="utf-8")
print(len(t))
pat = r'<link[^>]*>|<script[^>]*src="[^"]*"|href="[^"]*merci[^"]*"|(?:src|href|srcset)="\./[^"]*"|<body[^>]*>|<button[^>]*>|<details class="langue"'
for x in re.findall(pat, t): print("404:", x[:160])
print("--- merci")
for x in re.findall(r'<link rel="stylesheet"[^>]*>|<script[^>]*src="[^"]*"|<body[^>]*>|<button[^>]*>', m): print("merci:", x[:160])
i = t.find("<nav"); print(t[i:i+1500])
print("--- 404 inline scripts:", [s[:120] for s in re.findall(r"<script>(.*?)</script>", t, re.S)])
print("--- merci inline scripts:", [s[:120] for s in re.findall(r"<script>(.*?)</script>", m, re.S)])
md = (R/"404.md").read_text(encoding="utf-8"); print("--- md", md[:1200])
v = (R/"vercel.json").read_text(encoding="utf-8"); print([l for l in v.splitlines() if "404" in l or "status" in l][:10])
