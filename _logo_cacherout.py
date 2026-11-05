# -*- coding: utf-8 -*-
"""05/11 (Mendel, audio relaye par Moshe : « la ou tu as mis la hashgacha, mets le logo du Beth Habad de Grenoble, ca rassure les gens »).
   Pose le logo du Beth Habad Grenoble-Alpes sous la ligne de cacherout (icone sceau) du bloc « Strictly kosher » des pages Alpes, 4 langues.
   Logo nettoye (fond retire, marges egales) : 00-brief/references/2026-10-14-logo-kashrut-beth-habad-grenoble-alpes/propre/.
   Idempotent : python _logo_cacherout.py (depuis site-v5/)."""
import re, pathlib
TIT = {"": "Hashgacha", "fr": "Hashgaha", "es": "Hashgajá", "he": "השגחה"}
ALT = {"": "Beth Habad Grenoble-Alpes", "fr": "Beth Habad Grenoble-Alpes", "es": "Beth Habad Grenoble-Alpes", "he": "בית חב״ד גרנובל-אלפים"}
CSS = ("\n/* LOGO-BH-0511 : logo du Beth Habad Grenoble-Alpes sous la ligne de cacherout (_logo_cacherout.py) */\n"
       ".dk-garanties .dk-g-logo{display:block;margin:12px 0 4px;padding-inline-start:44px}\n.dk-garanties .dk-g-logo img{display:block;width:150px;height:auto}\n"
       "html[dir=rtl] .dk-garanties .dk-g-logo img{margin-inline-start:0}\n/* /LOGO-BH-0511 */\n")
n = 0
for f in pathlib.Path(".").rglob("index.html"):
    s = f.read_text(encoding="utf-8")
    if "seal-check.svg" not in s: continue
    lang = f.parts[0] if f.parts[0] in ("fr", "es", "he") else ""
    img = f'<span class="dk-g dk-g-logo"><span class="dk-g-logo-t">{TIT[lang]}</span><img src="/img/logo-beth-habad-grenoble-alpes.webp" alt="{ALT[lang]}" width="300" height="240" loading="lazy"></span>'
    s = re.sub(r' <span class="dk-g dk-g-logo">(?:<span class="dk-g-logo-t">[^<]*</span>)?<img[^>]*></span>', '', s)  # repose a neuf (idempotent)
    t, k = re.subn(r'(<span class="dk-g dk-g-ligne"><img class="dk dk-gico ico-fin" src="/img/ico/fin/seal-check.svg"[^>]*>.*?</span>)', lambda m: m.group(1) + " " + img, s, count=1, flags=re.S)
    if k: f.write_text(t, encoding="utf-8", newline="\n"); n += 1
c = pathlib.Path("lv.css"); cs = c.read_text(encoding="utf-8")
if "LOGO-BH-0511" not in cs: c.write_text(cs + CSS, encoding="utf-8", newline="\n")
print("pages :", n)
