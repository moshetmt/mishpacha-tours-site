# -*- coding: utf-8 -*-
"""Tunnel /plan-your-trip/ (4 langues) : lit prenom et wa venus du formulaire court ou du lien envoye par Mendel (31/10)
   et remplit le dernier ecran (prenom, indicatif, numero). Idempotent, a relancer apres _build_demande.py.
   python _prefill_court.py (depuis site-v5/)

   Lien attendu : /plan-your-trip/?lead=<id>&i=a&lieu=...#prenom=<prenom>&wa=<chiffres E.164 sans +>
   Prenom et numero voyagent apres le # (GA4 ne lit pas le fragment) ; ils sont aussi acceptes dans la requete.
   Le # est efface de la barre d'adresse des la lecture. Ne remplace jamais un champ deja rempli."""
import re

PAGES = ["plan-your-trip/index.html", "fr/plan-your-trip/index.html", "es/plan-your-trip/index.html", "he/plan-your-trip/index.html"]
JS = r'''<!--PREFILL-COURT--><script>(function(){var f=document.getElementById('formDemande');if(!f)return;
var h={};(location.hash||'').replace(/^#/,'').split('&').forEach(function(kv){var i=kv.indexOf('=');if(i>0)try{h[kv.slice(0,i)]=decodeURIComponent(kv.slice(i+1).replace(/\+/g,' '))}catch(x){}});
var q;try{q=new URLSearchParams(location.search)}catch(x){q=null}
function g(k){var v=h[k]||(q&&q.get(k))||'';return String(v).replace(/[\u0000-\u001f<>]/g,'').trim().slice(0,60)}
var pre=g('prenom'),wa=g('wa').replace(/[^0-9]/g,'');if(!pre&&!wa)return;
var P=f.elements.prenom,I=f.elements.indicatif,T=f.elements.tel;
if(pre&&P&&!P.value)P.value=pre;
if(wa&&I&&T&&!T.value){var best='';[].forEach.call(I.options,function(o){var c=o.value.replace(/[^0-9]/g,'');if(c&&wa.indexOf(c)===0&&c.length>best.length)best=c});
 if(best){I.value='+'+best;T.value=wa.slice(best.length)}else T.value=wa}
f.dispatchEvent(new Event('input',{bubbles:true}));
if(h.prenom||h.wa){try{history.replaceState(history.state,'',location.pathname+location.search)}catch(x){}}})();</script><!--/PREFILL-COURT-->'''

for p in PAGES:
    s = open(p, encoding="utf-8").read()
    s2 = re.sub(r"<!--PREFILL-COURT-->.*?<!--/PREFILL-COURT-->", "", s, flags=re.S)
    i = s2.rindex("</body>")
    s2 = s2[:i] + JS + s2[i:]
    if s2 != s:
        open(p, "w", encoding="utf-8", newline="").write(s2)
    print(p, "ok" if s2 != s else "deja a jour")
