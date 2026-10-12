#!/bin/bash
# usage: gen.sh fichier-liste   (lignes "nom|sujet")
D=clients/mishpacha-tours/03-website/site-v5/_candidats/spots-2026-10-12
REF=clients/mishpacha-tours/03-website/site-v5/img/illus/flat-kosher.png
ST="Using exactly the same flat illustration style, colour palette and paper texture as the reference image (flat shapes, no outlines, no gradients, warm cream, mustard yellow, deep green, salmon pink, black), draw ONE single small object centred on a plain pure white background, no text, no letters, no numbers, no six-pointed star, no cross, generous margin. Object: "
while IFS='|' read -r n s; do
  [ -f "$D/$n.png" ] && continue
  python scripts/gemini_image.py "$ST$s" "$D/$n.png" --ref $REF --model gemini-3.1-flash-image 2>&1 | tail -1
done < "$1"
