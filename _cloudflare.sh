#!/bin/bash
# Construction Cloudflare Pages (18/11/2026, compte Vercel gelé).
# Copie le site dans _site sans les fichiers de travail (tout ce qui commence par _ à la racine),
# comme le faisait le .vercelignore. Réglages Cloudflare : commande « bash _cloudflare.sh », dossier « _site ».
set -e
rm -rf _site
mkdir _site
for f in *; do
  case "$f" in
    _*|apps-script|README.md|CREDITS.md|vercel.json) continue ;;
  esac
  cp -r "$f" _site/
done
cp _headers _site/_headers
echo "Fichiers servis : $(find _site -type f | wc -l)"
