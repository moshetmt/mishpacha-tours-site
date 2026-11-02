# -*- coding: utf-8 -*-
"""02/11 : liens de texte des pages FR/ES/HE qui menaient vers la page anglaise. La traduction n'a converti que les
href="..." (guillemets doubles) ; les href='/x/' (apostrophes) du texte restaient en anglais (271 liens relevés dans les
index.md). Chaque href='/x/' d'une page /<l>/ devient href='/<l>/x/' quand /<l>/x/ existe. Même chose pour les href="/x/" du <main> (39 liens).
Le sélecteur de langue (en-tête, attributs hreflang, lang) n'est pas touché. Idempotent.   python _liens_langue.py [--dry]   (depuis site-v5/)"""
import glob, io, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
A = re.compile(r"<a\b[^>]*>")
H = re.compile(r"href='/([^'#?]*)([#?][^']*)?'")

n_liens = n_pages = 0
for l in ("fr", "es", "he"):
    for p in glob.glob(f"{l}/**/index.html", recursive=True):
        s = io.open(p, encoding="utf-8", newline="").read()
        def balise(m):
            global n_liens
            t = m.group(0)
            if "hreflang" in t or " lang=" in t: return t
            def lien(h):
                global n_liens
                chemin = h.group(1)
                if chemin.startswith(("fr/", "es/", "he/")) or not os.path.exists(os.path.join(l, chemin, "index.html")): return h.group(0)
                n_liens += 1
                return f"href='/{l}/{chemin}{h.group(2) or ''}'"
            return H.sub(lien, t)
        t = A.sub(balise, s)
        # guillemets doubles : seulement dans <main> (le sélecteur de langue de l'en-tête écrit href="/x/" sans hreflang)
        m = re.search(r"<main.*?</main>", t, re.S)
        if m:
            def dbl(h):
                global n_liens
                ch = h.group(2)
                if ch.startswith(("fr/", "es/", "he/")) or not os.path.exists(os.path.join(l, ch, "index.html")): return h.group(0)
                n_liens += 1
                return f'{h.group(1)}href="/{l}/{ch}{h.group(3) or ""}"'
            corps = re.sub(r'(<a\b[^>]*?)href="/([^"#?]*)([#?][^"]*)?"', dbl, m.group(0))
            t = t[:m.start()] + corps + t[m.end():]
        if t != s:
            n_pages += 1
            if not DRY: io.open(p, "w", encoding="utf-8", newline="").write(t)
print(f"{'(dry) ' if DRY else ''}{n_liens} lien(s) sur {n_pages} page(s)")
