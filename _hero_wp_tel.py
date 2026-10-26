# -*- coding: utf-8 -*-
"""Bannières des pages Alpes et été sur téléphone (Moshé, 26/10/2026, capture iPhone de la page des services) : le logo
Winter Prestige (ou Summer Prestige) prenait le haut du cadre sombre et le cadre cachait la photo. Sur téléphone, le logo
passe en haut de la photo, en petit ; le cadre ne garde que le texte. Ordinateur inchangé. Idempotent, toutes les pages.
    python _hero_wp_tel.py   (depuis site-v5/)"""
import glob, re
n = 0
for p in glob.glob("**/index.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    if "kwp-hero-wp-tel" in h or 'class="kwp-hero-wp"' not in h:
        continue
    m = re.search(r'<div class="kwp-hero-wp"><img src="([^"]+)"[^>]*?width="(\d+)" height="(\d+)"', h)
    s = re.search(r'<section class="hero lead-hero3[^"]*">', h)
    if not (m and s):
        continue
    copie = f'<div class="kwp-hero-wp-tel" aria-hidden="true" style="--logo:url({m.group(1)})"><img src="{m.group(1)}" alt="" width="{m.group(2)}" height="{m.group(3)}"></div>'
    h = h[:s.end()] + copie + h[s.end():]
    open(p, "w", encoding="utf-8").write(h); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* HERO-WP-TEL */" not in css:
    css += """
/* HERO-WP-TEL */ /* téléphone : logo WP en haut de la photo, plus grand, avec un reflet qui passe (Moshé 26/10) */
.kwp-hero-wp-tel{display:none}
@media (max-width:899.98px){
  .lead-hero3 .kwp-hero-wp-tel{display:block;position:absolute;z-index:3;top:22px;inset-inline-start:16px;width:min(300px,80vw);pointer-events:none;filter:drop-shadow(0 2px 10px rgba(0,0,0,.65))}
  .lead-hero3 .kwp-hero-wp-tel::before{content:"";position:absolute;inset:-40px -48px;z-index:-1;background:radial-gradient(closest-side,rgba(12,12,14,.32),rgba(12,12,14,.12) 60%,rgba(12,12,14,0))}
  .lead-hero3 .kwp-hero-wp-tel img{display:block;width:100%;height:auto}
  .lead-hero3 .kwp-hero-wp-tel::after{content:"";position:absolute;inset:0;background:linear-gradient(105deg,transparent 40%,rgba(255,244,214,.95) 50%,transparent 60%) no-repeat;background-size:250% 100%;background-position:120% 0;-webkit-mask:var(--logo) center/100% 100% no-repeat;mask:var(--logo) center/100% 100% no-repeat;animation:wp-reflet 7s ease-in-out 1.2s infinite}
  .lead-hero3:has(.kwp-hero-wp-tel) .lead3-bloc .kwp-hero-wp{display:none}
  .lead-hero3:has(.kwp-hero-wp-tel) .lead3-bloc h1{margin-top:0}
  .lead-hero3.has-gal .kwp-hero-wp-tel{top:70px}
}
@keyframes wp-reflet{0%{background-position:120% 0}22%,100%{background-position:-20% 0}}
@media (prefers-reduced-motion:reduce){.lead-hero3 .kwp-hero-wp-tel::after{animation:none;display:none}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
