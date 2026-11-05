# -*- coding: utf-8 -*-
"""Titre du bloc Chabbat (100 pages + générateur _contacts_bh_hebcal.py) : la paracha reste dans le titre en toute circonstance
(contrôle du 05/11 sur 6 dates simulées) :
 - samedi soir après la havdala : titre = paracha de la semaine suivante (avant : « Shavua tov in Courchevel », sans paracha) ;
 - semaine sans paracha (Chabbat de fête, ex. Pessah) : le nom de la fête du samedi, sans numéro ni « (CH''M) » : « Shabbat Pesach in Courchevel ».
Idempotent (marqueur PARACHA-V2)."""
import glob, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NM = (r'nm=(x.p?x.p.title.replace(/^\S+\s+/,""):((x.it||[]).filter(function(i){return i.category==="holiday"&&x.h&&i.date.slice(0,10)===x.h.date.slice(0,10)})[0]||{title:""})'
      r'.title.replace(/\s*\([^)]*\)/g,"").replace(/:.*$/,"").replace(/\s+[IVX]+$/,"").replace(/\s+\S׳$/,"")).replace(/[֑-ׇ̲]/g,"").replace(/[<>&]/g,"").trim()/*PARACHA-V2*/,Q=')
n = 0
for f in glob.glob("**/index.html", recursive=True) + ["_contacts_bh_hebcal.py"]:
    s = open(f, encoding="utf-8").read()
    if "PARACHA-V2" in s or "function rendre(x,etat)" not in s: continue
    o = s
    s = s.replace("return{c:it.find(function(i){return i.category===\"candles\"})", "return{it:it,c:it.find(function(i){return i.category===\"candles\"})", 1)
    s, k1 = re.subn(r'nm=x\.p\?x\.p\.title.*?:"",Q=', lambda m: NM, s, count=1)
    s, k2 = re.subn(r'\s*else if\(etat==="apres"\)ti\.textContent=C\.tov\}', "}", s, count=1)
    assert k1 == 1 and k2 == 1 and "return{it:it," in s, (f, k1, k2)
    open(f, "w", encoding="utf-8").write(s); n += 1
print("titres Chabbat mis à jour :", n)
