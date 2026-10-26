# -*- coding: utf-8 -*-
"""Ordinateur : même reflet doré que sur téléphone sur le logo Winter Prestige (ou Summer Prestige) du cadre de la bannière
(Moshé, 26/10/2026). L'image est enveloppée dans un <span class="wp-brille"> qui porte la forme du logo en masque.
Idempotent, toutes les pages, à relancer après _kit_wp.py.
    python _hero_wp_pc.py   (depuis site-v5/)"""
import glob, re
n = 0
for p in glob.glob("**/index.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    h2 = re.sub(r'<div class="kwp-hero-wp">(<img src="([^"]+)"[^>]*>)</div>',
                lambda m: f'<div class="kwp-hero-wp"><span class="wp-brille" style="--logo:url({m.group(2)})">{m.group(1)}</span></div>', h)
    if h2 != h:
        open(p, "w", encoding="utf-8").write(h2); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* HERO-WP-PC */" not in css:
    css += """
/* HERO-WP-PC */ /* ordinateur : reflet doré sur le logo du cadre (Moshé 26/10), même animation que le téléphone */
.lead-hero3 .lead3-bloc .kwp-hero-wp .wp-brille{position:relative;display:block;width:100%;max-width:280px;margin-inline-start:-6px}
.lead-hero3 .lead3-bloc .kwp-hero-wp .wp-brille img{width:100%;max-width:100%;margin:0}
@media (min-width:900px){
  .lead-hero3 .lead3-bloc .kwp-hero-wp .wp-brille::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(105deg,transparent 40%,rgba(255,244,214,.95) 50%,transparent 60%) no-repeat;background-size:250% 100%;background-position:120% 0;-webkit-mask:var(--logo) center/100% 100% no-repeat;mask:var(--logo) center/100% 100% no-repeat;animation:wp-reflet 7s ease-in-out 1.2s infinite}
}
@media (prefers-reduced-motion:reduce){.lead-hero3 .lead3-bloc .kwp-hero-wp .wp-brille::after{animation:none;display:none}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
