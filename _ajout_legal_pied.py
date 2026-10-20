# -*- coding: utf-8 -*-
"""20/10 (C5) : lien « Legal notice / Mentions légales » dans la ligne légale du pied, 4 langues, juste après « Terms ».
   Idempotent. A relancer depuis site-v5/ si un builder régénère un pied sans le lien. Cible aussi _gabarit.html et index.html (sources des pieds)."""
import re, io, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
LIEN = {"en": ("/legal/", "Legal notice"), "fr": ("/fr/legal/", "Mentions légales"), "es": ("/es/legal/", "Aviso legal"), "he": ("/he/legal/", "מידע משפטי")}
def patch(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    lang = path.replace("\\", "/").split("/")[0]; lang = lang if lang in ("fr", "es", "he") else "en"
    href, txt = LIEN[lang]
    if f'<a href="{href}">' in s: return 0
    n, k = re.subn(r'(<p class="legal">.*?<a href="/(?:(?:fr|es|he)/)?terms/">[^<]*</a>)', lambda m: m.group(1) + f'<a href="{href}">{txt}</a>', s, count=1, flags=re.S)
    if k: io.open(path, "w", encoding="utf-8", newline="").write(n)
    return k
if __name__ == "__main__":
    fichiers = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith(("_", "preview/"))] + ["_gabarit.html"]
    print(sum(patch(p) for p in fichiers), "pieds modifies sur", len(fichiers))
