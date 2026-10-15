# -*- coding: utf-8 -*-
"""Accueil sur telephone (reproche du 15/10 : « trop de swipe et de scroll ») : les 4 portes en lignes compactes sans carrousel
ni bouton Open, les 3 etapes en lignes avec petit dessin. Bloc ===MOBILE=== dans styles.css. Idempotent. `--strip` retire."""
import io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
D, F = "/* ===MOBILE=== */", "/* ===/MOBILE=== */"
CSS = """
@media (max-width:699px){
#trips .ac-portes{grid-auto-flow:row;grid-template-columns:1fr;overflow:visible;margin:20px 0 0;padding:0;gap:10px}
#trips .ac-portes .hub-carte{display:grid;grid-template-columns:96px 1fr;border-radius:14px}
#trips .ac-portes .hub-carte .photo{aspect-ratio:auto;min-height:96px}
#trips .ac-portes .corps{position:relative;justify-content:center;padding-block:12px;padding-inline:14px 36px}
#trips .ac-portes .corps::after{content:"›";position:absolute;inset-inline-end:14px;top:50%;transform:translateY(-50%);font-size:28px;line-height:1;opacity:.45}
[dir=rtl] #trips .ac-portes .corps::after{content:"‹"}
#trips .ac-portes h3{font-size:19px;line-height:1.15}
#trips .ac-portes .hub-carte p{font-size:14px;line-height:1.35;margin:4px 0 0}
#trips .ac-portes .btn-noir{display:none}
#how.etapes ol{gap:18px;margin-top:22px;text-align:start}
#how.etapes ol li{display:grid;grid-template-columns:64px 1fr;column-gap:14px;align-items:start}
#how.etapes li img{width:64px;height:64px;margin:0;grid-row:1 / span 3}
#how.etapes li > span{font-size:20px;margin-top:0}
#how.etapes li p{margin:4px 0 0;max-width:none}
#how.etapes ol li:not(:last-child)::after{display:none}
}
"""
p = "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
s = re.sub(re.escape(D) + r".*?" + re.escape(F) + r"\n?", "", s, flags=re.S)
if "--strip" not in sys.argv: s = s.rstrip("\n") + "\n" + D + CSS + F + "\n"
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
