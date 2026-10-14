# -*- coding: utf-8 -*-
"""Mini-dessins img/des/*.webp à surface visuelle égale (reproche du 14/10 : « tailles pas similaires, ça fait pas pro »).
Chaque dessin est rogné à son contenu, puis mis à l'échelle pour que racine(l x h) = CIBLE px, sans dépasser 192 px,
et recentré sur un carré transparent de 192 px. Sauvegarde des originaux dans _candidats/des-avant-2026-10-14/.
Avec --menorah : remplace sparkles.webp par la menorah Habad régénérée (bras droits)."""
import os, sys, shutil, subprocess, math
ICI = os.path.dirname(os.path.abspath(__file__))
DES = os.path.join(ICI, 'img', 'des')
SAUV = os.path.join(ICI, '_candidats', 'des-avant-2026-10-14')
CIBLE, BOITE = 150, 192

def mesure(f):
    out = subprocess.run(['magick', f, '-trim', '-format', '%w %h', 'info:'], capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])

os.makedirs(SAUV, exist_ok=True)
if '--menorah' in sys.argv:
    src = os.path.join(ICI, '_candidats', 'spots-2026-10-14', 'menorah-2.png')
    shutil.copy(os.path.join(DES, 'sparkles.webp'), os.path.join(SAUV, 'sparkles-ancienne-menorah.webp'))
    subprocess.run(['magick', src, '-fuzz', '8%', '-transparent', 'white', '-trim', '+repage',
                    '-resize', f'{BOITE}x{BOITE}', '-gravity', 'center', '-background', 'none',
                    '-extent', f'{BOITE}x{BOITE}', '-quality', '90', os.path.join(DES, 'sparkles.webp')], check=True)

for n in sorted(os.listdir(DES)):
    if not n.endswith('.webp'):
        continue
    f = os.path.join(DES, n)
    s = os.path.join(SAUV, n)
    if not os.path.exists(s):
        shutil.copy(f, s)
    w, h = mesure(s if n != 'sparkles.webp' or '--menorah' not in sys.argv else f)
    k = min(CIBLE / math.sqrt(w * h), BOITE / max(w, h))
    nw, nh = max(1, round(w * k)), max(1, round(h * k))
    base = f if (n == 'sparkles.webp' and '--menorah' in sys.argv) else s
    subprocess.run(['magick', base, '-trim', '+repage', '-resize', f'{nw}x{nh}!', '-gravity', 'center',
                    '-background', 'none', '-extent', f'{BOITE}x{BOITE}', '-quality', '90', f], check=True)
    print(f'{n}: {w}x{h} -> {nw}x{nh}')
