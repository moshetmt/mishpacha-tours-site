# -*- coding: utf-8 -*-
"""Contrôle de structure : compare, pour chaque fiche neuve et chaque langue, la suite des balises et des attributs structurels avec la fiche
de Val Thorens (même langue), hors contenu. Garde : nom de balise, class, id, open, loading, sizes, type, rel, role, aria-*, noms des data-* (pas leurs valeurs),
href des feuilles de style et src des scripts. Ignore : textes, alt, src/srcset des images, liens, largeurs, hauteurs. Les répétitions consécutives
identiques (photos du rail, questions) sont repliées en une seule ligne. Sortie : tout écart, par page. Usage : python _chalets_1111_structure.py [--ecarts-seulement]"""
import difflib
import pathlib
import re
import sys
from html.parser import HTMLParser

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from _chalets_1111_noms import CH, ORDRE_CLES  # noqa: E402

GARDE = {"class", "id", "open", "loading", "sizes", "type", "rel", "role", "dir", "lang", "tabindex", "decoding", "fetchpriority", "defer", "async", "media"}
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "path", "circle", "rect", "use", "stop", "image"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def jeton(self, tag, attrs):
        a = []
        for k, v in attrs:
            if k in GARDE or k.startswith("aria-"):
                a.append(f'{k}="{v}"' if v is not None else k)
            elif k.startswith("data-"):
                a.append(k)
            elif tag == "link" and k == "href" and (v or "").endswith(".css"):
                a.append(f'href="{(v or "").split("?")[0]}"')
            elif tag == "script" and k == "src":
                a.append(f'src="{(v or "").split("?")[0]}"')
            elif tag == "meta" and k in ("name", "property", "http-equiv"):
                a.append(f'{k}="{v}"')
        return "<" + tag + (" " + " ".join(sorted(a)) if a else "") + ">"

    def handle_starttag(self, tag, attrs):
        self.out.append(self.jeton(tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.out.append(self.jeton(tag, attrs))

    def handle_endtag(self, tag):
        if tag not in VOID:
            self.out.append(f"</{tag}>")


def normaliser(h, ref):
    """Val Thorens porte DEUX fois le bloc « The chalet in pictures » (défaut du site en ligne, issu d'un double passage de _lot3_0611.py) : on compare
    à une seule copie, comme sur les fiches neuves. Le défaut de Val Thorens n'est pas touché."""
    if ref:
        m = [x.start() for x in re.finditer('<div class="lc-bas-photos">', h)]
        if len(m) == 2:
            fin = h.find('<div class="lc-bas-autres">', m[1])
            h = h[:m[1]] + h[fin:]
    return h


def replier(out):
    """Replie les répétitions consécutives d'un même jeton ou d'un même groupe de 2 à 6 jetons (cartes, items de liste, photos, questions)."""
    chg = True
    while chg:
        chg = False
        for n in range(1, 7):
            i = 0
            res = []
            while i < len(out):
                if i + 2 * n <= len(out) and out[i:i + n] == out[i + n:i + 2 * n]:
                    j = i + n
                    while j + n <= len(out) and out[j:j + n] == out[i:i + n]:
                        j += n
                    res += out[i:i + n]; i = j; chg = True
                else:
                    res.append(out[i]); i += 1
            out = res
    return out


def suite(path, ref=False):
    p = P()
    p.feed(normaliser(path.read_text(encoding="utf-8"), ref))
    return replier(p.out)


def main():
    seul = "--ecarts-seulement" in sys.argv
    total = 0
    for cle in ORDRE_CLES:
        for lang in ("en", "fr", "es", "he"):
            pre = "" if lang == "en" else f"{lang}/"
            ref = suite(ICI / f"{pre}kosher-chalet-val-thorens" / "index.html", True)
            neuf = suite(ICI / f"{pre}{CH[cle]['slug']}" / "index.html")
            d = [l for l in difflib.unified_diff(ref, neuf, "val-thorens", f"{CH[cle]['slug']}", n=0, lineterm="") if not l.startswith(("---", "+++", "@@"))]
            total += len(d)
            if d or not seul:
                print(f"== {lang} {CH[cle]['slug']} : {len(d)} écart(s), {len(neuf)} jetons contre {len(ref)}")
            for l in d:
                print("   ", l[:230])
    print("TOTAL écarts :", total)


if __name__ == "__main__":
    main()
