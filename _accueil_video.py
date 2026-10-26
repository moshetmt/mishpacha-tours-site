# -*- coding: utf-8 -*-
"""Accueil, 4 langues : petite vidéo muette en boucle dans la bannière (Moshé 26/10/2026, idée du client).
Montage de 6 plans Mixkit (licence gratuite, usage commercial, sans mention) : img/video/accueil-pc.* (1280x720) et
accueil-tel.* (720x1280), AV1 en WebM puis H.264 en MP4. La photo actuelle reste l'image principale (LCP) ; la vidéo n'est
demandée qu'après le chargement de la page, jamais si le visiteur a réduit les animations ou active l'économie de données,
et se met en pause hors de l'écran. Idempotent.
    python _accueil_video.py   (depuis site-v5/)"""
import re
VIDEO = '<video class="ac-video" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>'
JS = """<script>/* ACCUEIL-VIDEO */(function(){var v=document.querySelector('.ac-video');if(!v)return;
var c=navigator.connection||{};if(c.saveData||/(^|-)2g$/.test(c.effectiveType||'')||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function go(){var t=matchMedia('(max-width:899.98px)').matches?'tel':'pc',b='/img/video/accueil-'+t;
var saf=/^((?!chrome|chromium|crios|android).)*safari/i.test(navigator.userAgent);
var s2=document.createElement('source');s2.src=b+'.mp4';s2.type='video/mp4';v.appendChild(s2);v.load();
v.addEventListener('playing',function(){v.classList.add('on')},{once:true});var p=v.play();if(p&&p.catch)p.catch(function(){});
if('IntersectionObserver'in window)new IntersectionObserver(function(e){e[0].isIntersecting?v.play().catch(function(){}):v.pause()}).observe(v);}
if(document.readyState==='complete')setTimeout(go,300);else addEventListener('load',function(){setTimeout(go,300)});})();</script>"""
n = 0
for l in ("", "fr", "es", "he"):
    p = (l + "/" if l else "") + "index.html"
    h = open(p, encoding="utf-8").read()
    if "ac-video" in h:
        continue
    m = re.search(r'(<section class="hero ac-hero">\s*<img[^>]*>)', h)
    assert m, p
    h = h[:m.end()] + VIDEO + h[m.end():]
    h = h.replace("</body>", JS + "</body>", 1)
    open(p, "w", encoding="utf-8").write(h); n += 1
css = open("styles.css", encoding="utf-8").read()
if "/* ACCUEIL-VIDEO */" not in css:
    css += """
/* ACCUEIL-VIDEO */ /* vidéo muette de la bannière d'accueil, posée sur la photo, fondu à l'entrée (Moshé 26/10) */
.ac-hero > .ac-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease;pointer-events:none}
.ac-hero > .ac-video.on{opacity:1}
@media (prefers-reduced-motion:reduce){.ac-hero > .ac-video{display:none}}
"""
    open("styles.css", "w", encoding="utf-8").write(css)
print(n, "pages")
