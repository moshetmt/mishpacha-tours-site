# -*- coding: utf-8 -*-
"""CSS du menu a 4 entrees (15/10) : bouton jaune de l'en-tete, ligne de liens secondaires du panneau mobile,
colonne « Explore » du pied et lien du formulaire en fin de page station. Bloc ===MENU=== dans styles.css. Idempotent. `--strip` retire."""
import io, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
D, F = "/* ===MENU=== */", "/* ===/MENU=== */"
CSS = """
.nav .liens a.nav-cta{display:inline-flex;align-items:center;min-height:44px;padding:0 22px;border-radius:999px;background:var(--jaune);color:var(--encre);font-weight:600;white-space:nowrap}
@media (min-width:900px){.nav .liens{align-items:center}}
.panneau nav a.nav-cta{display:flex;justify-content:center;align-items:center;margin-top:24px;padding:16px 24px;border:0;border-radius:999px;background:var(--jaune);font-size:22px;font-weight:600}
.panneau-sec{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:22px}
.panneau-sec a{font-size:15px;line-height:1.4;text-decoration:underline;text-underline-offset:3px;opacity:.8}
@media (min-width:900px){.pied .cols{grid-template-columns:repeat(5,1fr)}}
.lead-plan{margin:18px 0 0;text-align:center}
.lead-plan a{color:var(--creme);font-weight:600;font-size:16px;text-decoration:underline;text-underline-offset:3px}
"""
p = "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
s = re.sub(re.escape(D) + r".*?" + re.escape(F) + r"\n?", "", s, flags=re.S)
if "--strip" not in sys.argv: s = s.rstrip("\n") + "\n" + D + CSS + F + "\n"
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
