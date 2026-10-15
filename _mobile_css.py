# -*- coding: utf-8 -*-
"""Accueil sur telephone (reproche du 15/10 : « trop de swipe et de scroll ») : les 4 portes en lignes compactes sans carrousel
ni bouton Open, les 3 etapes en lignes avec petit dessin. Bloc ===MOBILE=== dans styles.css. Idempotent. `--strip` retire."""
import io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
D, F = "/* ===MOBILE=== */", "/* ===/MOBILE=== */"
CSS = """
#chercheur{gap:12px;padding:16px}
#chercheur label{border:0;border-radius:0;padding:0;display:grid;gap:5px;min-width:0}
#chercheur label span{opacity:.8}
#chercheur input,#chercheur select{box-sizing:border-box;width:100%;min-width:0;min-height:46px;padding:10px 14px;background:var(--creme);border:1px solid rgba(28,27,31,.2);border-radius:12px;font-size:16px;text-align:start}
#chercheur select{padding-inline-end:38px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231C1B1F' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:18px;background-position:right 12px center}
[dir=rtl] #chercheur select{background-position:left 12px center}
#chercheur input[type=date]{-webkit-appearance:none;appearance:none;display:block;line-height:24px}
#chercheur input[type=date]::-webkit-date-and-time-value{text-align:start}
#chercheur .duo{grid-template-columns:1fr 1fr;gap:12px}
.ticket-plan{margin:22px 0 0}
.ticket-zone{margin-bottom:48px}   /* le pied n a plus 170 px de marge haute : le ticket ne deborde plus dessus (15/10) */
.ticket-plan .btn-noir{display:flex;justify-content:center;align-items:center;min-height:52px;font-size:16px}
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
