"""Concatène css/mt/*.css (ordre alphabétique) en mt.css. Usage : python _mt_build.py [--check]
--check : refuse si mt.css contient !important, un sélecteur #id (hors #panneau) ou dépasse 60 Ko."""
import sys, re, pathlib
ICI = pathlib.Path(__file__).parent
parts = sorted((ICI / "css/mt").glob("*.css"))
css = "\n".join(p.read_text(encoding="utf-8") for p in parts)
css = re.sub(r"\n\s*\n+", "\n", re.sub(r"/\*.*?\*/", "", css, flags=re.S)).strip() + "\n"  # commentaires retirés du fichier généré
out = ICI / "mt.css"
out.write_text(css, encoding="utf-8")
ko = len(css.encode()) / 1024
imp = css.count("!important")
ids = len(re.findall(r"(?<![\w-])#(?!panneau\b)[a-zA-Z][\w-]*\s*[{,.:\[\s>]", re.sub(r"#[0-9a-fA-F]{3,8}\b", "", css)))
print(f"mt.css : {len(parts)} partiels, {ko:.1f} Ko, {imp} !important, {ids} sélecteurs #id")
if "--check" in sys.argv and (imp or ids or ko > 60):
    sys.exit("mt.css hors budget (voir DESIGN-SITE.md §1 et §6)")
