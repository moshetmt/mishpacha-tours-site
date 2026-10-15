# -*- coding: utf-8 -*-
"""Controle (15/10) : dans une meme section, une icone ne sert qu'une fois. Liste les repetitions. python _controle_icones.py [-v]"""
import glob, io, re, sys, os
from bs4 import BeautifulSoup
os.chdir(os.path.dirname(os.path.abspath(__file__)))
EXCL = ("dk-fleche", "dk-coche", "dk-sep")

def noms(sec):
    out = []
    for t in sec.find_all(["img", "svg"]):
        cl = t.get("class") or []
        if "dk" not in cl or any(c in cl for c in EXCL): continue
        if t.name == "img":
            m = re.search(r"/img/des/([\w-]+)\.webp", t.get("src", ""))
            if m: out.append(m.group(1))
        else:
            u = t.find("use")
            if u: out.append(u.get("href", "").split("#")[-1])
    return out

def repetitions(path):
    soup = BeautifulSoup(io.open(path, encoding="utf-8").read(), "lxml")
    res = []
    for sec in soup.select("main section, main div.ss, section.ss"):
        if sec.find_parent(["section"]) is not None and sec.name == "section" and sec.find_parent("section").get("class") and "ss" in sec.find_parent("section").get("class"): continue
        n = noms(sec); d = sorted({x for x in n if n.count(x) > 1})
        if d: res.append((" ".join(sec.get("class") or []), (sec.find("h2") or sec.find("h1") or sec).get_text(" ", strip=True)[:50], d))
    return res

if __name__ == "__main__":
    tot = 0
    for p in sorted(glob.glob("**/index.html", recursive=True)):
        if p.startswith("_"): continue
        for cl, h, d in repetitions(p):
            tot += 1; print(p, "|", h, "|", d)
    print(tot, "repetition(s)")
