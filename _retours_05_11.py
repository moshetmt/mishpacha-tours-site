# -*- coding: utf-8 -*-
"""Retours de Moshé du 05/11/2026 sur les pages station (captures iPhone). Idempotent, marqueur RET-0511.
 - carte : le filet doré passe sous « ON THE MAP » (surtitre), au-dessus du nom de la zone ;
 - Chabbat : plus de guillemets autour de la paracha, le nom est souligné d'or (« Shabbat Chayei Sara in Courchevel »).
Le script Hebcal des 100 pages (et son générateur _contacts_bh_hebcal.py) écrit le nom dans <span class="sh-paracha">."""
import glob, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = 'ti.innerHTML=C.mot+(nm?" <span style=\\"white-space:nowrap\\">"+Q[0]+nm+Q[1]+"</span>":"");'
B = 'ti.innerHTML=C.mot+(nm?" <span class=\\"sh-paracha\\">"+nm+"</span>":"");'
n = 0
for f in glob.glob("**/index.html", recursive=True) + ["_contacts_bh_hebcal.py"]:
    s = open(f, encoding="utf-8").read()
    if A in s:
        open(f, "w", encoding="utf-8").write(s.replace(A, B)); n += 1
print("titres Chabbat sans guillemets :", n)
P = "html body.lv" + "".join(f":not(#c{i})" for i in range(1, 14))
OR = "linear-gradient(100deg,#8F7646,#D2BC8C 45%,#A88F5E 55%,#8F7646)"
CSS = f"""/* ===RET-0511=== retours de Moshé du 05/11 (_retours_05_11.py) */
{P} h2.carte-titre::after{{display:none !important}}
{P} .carte-sur::after{{content:"";display:block;width:56px;height:1.5px;margin:12px auto 14px;background:{OR}}}
{P} .sh-paracha{{white-space:nowrap;text-decoration:underline;text-decoration-color:#A88F5E;text-decoration-thickness:2px;text-underline-offset:.16em;text-decoration-skip-ink:none}}
/* ===/RET-0511=== */
"""
lv = open("lv.css", encoding="utf-8").read()
lv = re.sub(r"/\* ===RET-0511===.*?/\* ===/RET-0511=== \*/\n", "", lv, flags=re.S)
open("lv.css", "w", encoding="utf-8").write(lv.rstrip("\n") + "\n" + CSS)
print("css ok")
