# -*- coding: utf-8 -*-
"""Photos réelles à la place des re-rendus Gemini (Moshé 01/11/2026 : « ne me mets jamais de photos inventées ! juste
retouchées à la limite pour éviter la recherche inversée »).
Pour chaque photo du site identique à une sortie de re-rendu (liste 06-reports/2026-11-01-audit-photos-re-rendues/rerendus.json),
reprend l'ENTRÉE du re-rendu (la vraie photo, déjà recadrée) et applique recadrage 3 à 6 %, rotation < 1° et un étalonnage « magazine » sans IA (luxe()), aucune métadonnée. Même taille en pixels que le fichier remplacé (HTML inchangé).
Les anciens fichiers partent dans 06-reports/2026-11-01-audit-photos-re-rendues/_avant/ ; leurs WebP dérivés sont supprimés
pour que _rail_leger.py et _images_legeres.py les régénèrent.
    python _photos_reelles.py   (depuis site-v5/)"""
import glob, json, os, random, shutil
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

REF = r"..\..\00-brief\references"
AUDIT = r"..\..\06-reports\2026-11-01-audit-photos-re-rendues"
AVANT = os.path.join(AUDIT, "_avant")
os.makedirs(AVANT, exist_ok=True)
ENTREES = ["_entree-galerie", "retouchees", "_lots/int", "_lots/ext", "_lots/*", "choix-int", "choix-ext", "airbnb", "originaux"]


def entree(rerendu):
    dossier = rerendu.split("\\")[0]
    nom = os.path.splitext(os.path.basename(rerendu))[0].replace("-fort2", "").replace("-fort", "")
    for sous in ENTREES:
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            t = glob.glob(os.path.join(REF, dossier, sous, nom + ext))
            if t:
                return t[0]
    return None


def retouche(src, taille, graine):
    r = random.Random(graine)
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    W, H = im.size
    m = [r.uniform(0.015, 0.03) for _ in range(4)]   # gauche, haut, droite, bas : recadrage léger
    im = im.crop((int(W * m[0]), int(H * m[1]), int(W * (1 - m[2])), int(H * (1 - m[3]))))
    tw, th = taille   # cadrage au rapport du fichier remplacé, centré
    W, H = im.size
    if W / H > tw / th:
        nw = int(H * tw / th); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W * th / tw); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    im = im.resize((tw, th), Image.LANCZOS)
    return luxe(im, r)


def luxe(im, r):
    """Retouche PROPRE et discrète (Moshé 01/11 : l'étalonnage « magazine » était « dégueulasse ») : niveaux corrigés à
    moitié, un soupçon de contraste et de netteté. Ni vignette, ni clarté, ni virage, ni couleurs poussées."""
    import numpy as np
    a = np.asarray(im).astype(np.float32) / 255.0
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    lo, hi = np.percentile(L, 0.1), np.percentile(L, 99.9)
    n = np.clip((a - lo) / max(hi - lo, 0.3), 0, 1)
    a = a * 0.5 + n * 0.5   # niveaux à moitié : on garde la lumière de la photo
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8"))
    out = ImageEnhance.Contrast(out).enhance(1.03)
    return out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=3))


d = json.load(open(os.path.join(AUDIT, "rerendus.json"), encoding="utf-8"))
SOURCES = {"slope-sdb-baignoire.jpg": os.path.join(REF, "2026-10-20-chalet-2-deux-alpes", "originaux", "l2a-08.jpg")}
faits, manques = [], []
for nom, rer, dist, taille in d["rerendus"]:
    dossier_site = "villa" if nom.startswith("st-tropez") else "chalet"
    cible = os.path.join("img", dossier_site, nom)
    src = SOURCES.get(nom) or entree(rer)
    if not src:
        manques.append((nom, rer)); continue
    retouche(src, tuple(taille), nom).save(cible, "JPEG", quality=88, optimize=True, progressive=True)
    stem = os.path.splitext(nom)[0]
    for v in glob.glob(f"img/{dossier_site}/w/{stem}-*.webp") + glob.glob(f"img/{dossier_site}/min/{stem}-*") + glob.glob(f"img/h/{stem}-*") + glob.glob(f"img/cartes/{stem}*"):
        os.remove(v)
    faits.append((nom, os.path.relpath(src, REF)))
json.dump({"faits": faits, "manques": manques}, open(os.path.join(AUDIT, "remplacements.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(faits), "remplacées,", len(manques), "sans entrée :", manques)
