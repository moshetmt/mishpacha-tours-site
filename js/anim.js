/* Micro-animations Mishpacha Tours (_animations.py). Rien ne part d'un survol seul. */
(function(){
'use strict';
var D=document,R=D.documentElement;
var reduce=matchMedia('(prefers-reduced-motion: reduce)');
var RTL=(R.getAttribute('dir')||'ltr')==='rtl';
var LANG=(R.lang||'en').slice(0,2);
var path=location.pathname.replace(/index\.html$/,'').replace(/\/?$/,'/').replace(/^\/(fr|es|he)\//,'/');
var EASE='cubic-bezier(0.32,0.72,0,1)';
var TXT={en:{c:'Close',p:'Previous photo',n:'Next photo',d:'Photos'},fr:{c:'Fermer',p:'Photo précédente',n:'Photo suivante',d:'Photos'},es:{c:'Cerrar',p:'Foto anterior',n:'Foto siguiente',d:'Fotos'},he:{c:'סגירה',p:'התמונה הקודמת',n:'התמונה הבאה',d:'תמונות'}};
var L10=TXT[LANG]||TXT.en;
R.classList.add('anim-js');
R.classList.remove('anim-vis-on');
/* la visionneuse ne doit jamais laisser html en overflow:hidden (navigateurs integres, cache de navigation) */
function resetVis(){R.classList.remove('anim-vis-on');if(window.__animVisFin)window.__animVisFin()}
['pagehide','pageshow','popstate','hashchange'].forEach(function(ev){addEventListener(ev,resetVis)});
D.addEventListener('touchstart',function(){},{passive:true});

/* 13. bouton Plan your trip flottant a gauche du WhatsApp (Moshe 19/10) : texte et lien repris du menu, donc dans la langue de la page */
(function(){
  var wa=D.querySelector('.wa-flottant');if(!wa||D.getElementById('formDemande'))return;
  var src=D.querySelector('.nav .liens a[href$="plan-your-trip/"]');if(!src)return;
  var a=D.createElement('a');a.className='pyt-flottant';a.href=src.getAttribute('href');a.textContent=src.textContent.trim();
  wa.parentNode.insertBefore(a,wa);
})();

/* 6. bouton WhatsApp flottant */
(function(){
  if(!D.querySelector('.wa-flottant'))return;
  R.classList.add('wa-cache');
  function chk(){if(scrollY>=innerHeight){R.classList.add('wa-vu');removeEventListener('scroll',chk)}}
  chk();addEventListener('scroll',chk,{passive:true});
})();

/* 9. trait des etapes */
(function(){
  var b=D.querySelector('#how.etapes');if(!b)return;
  if(!('IntersectionObserver' in window)){b.classList.add('trait-vu');return}
  var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){b.classList.add('trait-vu');o.disconnect()}})},{threshold:.3});
  o.observe(b.querySelector('ol')||b);
})();

/* 10. flocons (pages d'hiver, en continu, Moshe 15/10) */
(function(){
  if(reduce.matches)return;
  if(!/^\/kosher-(alpe-dhuez|annecy|chamonix|courchevel|grenoble|la-plagne|les-arcs|les-deux-alpes|megeve|val-disere|val-thorens|zermatt|st-moritz|crans-montana|cervinia|courmayeur|cortina|ski-holidays-french-alps|chalet-les-deux-alpes)\/$/.test(path))return;
  var hero=D.querySelector('.lead-hero3');if(!hero)return;
  
  var c=D.createElement('div');c.className='anim-neige';c.setAttribute('aria-hidden','true');
  var h=hero.offsetHeight+30;
  for(var i=0;i<24;i++){
    var f=D.createElement('i'),s=4+Math.random()*5;
    f.style.cssText='--x:'+(Math.random()*100).toFixed(1)+'%;--s:'+s.toFixed(1)+'px;--d:'+(-Math.random()*9).toFixed(2)+'s;--t:'+(7+Math.random()*4).toFixed(2)+'s;--o:'+(0.45+Math.random()*0.35).toFixed(2)+';--dx:'+((Math.random()-.5)*60).toFixed(0)+'px;--h:'+h+'px';
    c.appendChild(f);
  }
  hero.appendChild(c);
  
})();

/* 7. listes d'adresses liees aux marqueurs Leaflet */
(function(){
  var conts=[].slice.call(D.querySelectorAll('.carte-osm[data-points]'));
  if(!conts.length||!window.L||!L.Map)return;
  var maps=[],o=L.Map.prototype.invalidateSize;
  L.Map.prototype.invalidateSize=function(){if(maps.indexOf(this)<0)maps.push(this);return o.apply(this,arguments)};
  dispatchEvent(new Event('resize'));
  function norm(s){return (s||'').toLowerCase().replace(/\s+/g,' ').trim()}
  var items=[].slice.call(D.querySelectorAll('li,article')).filter(function(e){return !e.closest('.pied,header,.panneau,.carte-osm,nav')});
  var pris=[];
  function carte(c){return maps.filter(function(m){return m.getContainer()===c})[0]}
  function aller(c,p,essai){
    var m=carte(c);
    if(!m){if(!essai){dispatchEvent(new Event('resize'));requestAnimationFrame(function(){requestAnimationFrame(function(){aller(c,p,1)})})}return}
    var mk=null;
    m.eachLayer(function(l){if(l.getLatLng&&l.getPopup&&l.getPopup()){var ll=l.getLatLng();if(Math.abs(ll.lat-p.ll[0])<1e-6&&Math.abs(ll.lng-p.ll[1])<1e-6&&!mk)mk=l}});
    if(!mk)return;
    var r=c.getBoundingClientRect();
    if(r.top<0||r.bottom>innerHeight)c.scrollIntoView({block:'center',behavior:reduce.matches?'auto':'smooth'});
    var z=Math.max(m.getZoom(),15),done=false;
    function ouvre(){if(done)return;done=true;mk.openPopup()}
    if(reduce.matches){m.setView(p.ll,z,{animate:false});ouvre();return}
    m.once('moveend',ouvre);setTimeout(ouvre,1100);
    m.flyTo(p.ll,z,{duration:.8});
  }
  conts.forEach(function(c){
    var pts;try{pts=JSON.parse(c.dataset.points)}catch(e){return}
    pts.forEach(function(p){
      var rue=norm((p.a||'').split(',')[0]),nom=norm(p.n);if(!rue)return;
      var cand=items.filter(function(e){return pris.indexOf(e)<0&&norm(e.textContent).indexOf(rue)>-1});
      var avec=cand.filter(function(e){return norm(e.textContent).indexOf(nom)>-1});
      if(avec.length)cand=avec;
      cand.sort(function(a,b){return a.textContent.length-b.textContent.length});
      var li=cand[0];if(!li)return;
      pris.push(li);li.classList.add('anim-carte-lien');li.setAttribute('tabindex','0');
      li.addEventListener('click',function(e){if(e.target.closest('a,button'))return;aller(c,p)});
      li.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&e.target===li){e.preventDefault();aller(c,p)}});
    });
  });
})();

/* 2. galerie du chalet */
(function(){
  if(path!=='/kosher-chalet-les-deux-alpes/')return;
  var th=[].slice.call(D.querySelectorAll('.lead-offre .lead-cartes img'));
  var n=th.length;if(!n)return;
  var cur=0,ouvert=false,ferme=false,W=0,H=0,dx=0,dy=0,sens=RTL?-1:1;
  var v,fond,stage,btnX,btnG,btnD,cpt,slides=[],g=null;
  function el(t,c){var e=D.createElement(t);if(c)e.className=c;return e}
  function fleche(dir){return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="'+(dir<0?'M15 5l-7 7 7 7':'M9 5l7 7-7 7')+'"/></svg>'}
  th.forEach(function(t,i){
    var b=t.closest('figure'),cap=b&&b.querySelector('figcaption b');
    t.classList.add('anim-zoom');t.setAttribute('tabindex','0');t.setAttribute('role','button');
    if(cap)t.setAttribute('aria-label',cap.textContent);
    t.addEventListener('click',function(){ouvrir(i)});
    t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();ouvrir(i)}});
  });
  function build(){
    if(v)return;
    v=el('div','anim-vis');v.hidden=true;v.setAttribute('role','dialog');v.setAttribute('aria-modal','true');v.setAttribute('aria-label',L10.d);
    fond=el('div','anim-vis-fond');stage=el('div','anim-vis-piste');
    th.forEach(function(t){var s=el('div','anim-vis-s'),im=el('img');im.alt=t.alt||'';im.src=t.currentSrc||t.src;im.draggable=false;s.appendChild(im);stage.appendChild(s);slides.push({s:s,im:im,w:+t.getAttribute('width')||0,h:+t.getAttribute('height')||0})});
    btnX=el('button','anim-vis-x');btnX.type='button';btnX.setAttribute('aria-label',L10.c);btnX.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    btnG=el('button','anim-vis-g');btnD=el('button','anim-vis-d');btnG.type=btnD.type='button';
    btnG.innerHTML=fleche(-1);btnD.innerHTML=fleche(1);
    btnG.setAttribute('aria-label',RTL?L10.n:L10.p);btnD.setAttribute('aria-label',RTL?L10.p:L10.n);
    cpt=el('div','anim-vis-cpt');cpt.setAttribute('aria-live','polite');
    v.appendChild(fond);v.appendChild(stage);v.appendChild(btnG);v.appendChild(btnD);v.appendChild(btnX);v.appendChild(cpt);
    D.body.appendChild(v);
    btnX.addEventListener('click',fermer);
    btnG.addEventListener('click',function(){aller(cur+(RTL?1:-1))});
    btnD.addEventListener('click',function(){aller(cur+(RTL?-1:1))});
    stage.addEventListener('pointerdown',down);stage.addEventListener('pointermove',move);stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);
    D.addEventListener('keydown',touche);
    addEventListener('resize',function(){if(ouvert){layout();place(false)}});
  }
  function layout(){
    W=innerWidth;H=innerHeight;var pad=W<700?0:48,bas=W<700?56:0;
    slides.forEach(function(o,i){
      var nw=th[i].naturalWidth||o.w||1,nh=th[i].naturalHeight||o.h||1;
      var k=Math.min((W-2*pad)/nw,(H-2*pad-bas)/nh,2);
      o.im.style.width=Math.round(nw*k)+'px';o.im.style.height=Math.round(nh*k)+'px';
    });
  }
  function place(anim){
    stage.style.cursor=g?'grabbing':'';
    slides.forEach(function(o,j){
      o.s.style.transition=(anim&&!reduce.matches)?(anim==='ressort'?'transform 350ms cubic-bezier(0.34,1.56,0.64,1)':'transform 300ms '+EASE):'none';
      o.s.style.transform='translate3d('+((j-cur)*W*sens+dx)+'px,0,0)';
    });
  }
  function majUI(){
    cpt.textContent=(cur+1)+' / '+n;
    var gauche=RTL?cur<n-1:cur>0,droite=RTL?cur>0:cur<n-1;
    btnG.setAttribute('aria-disabled',gauche?'false':'true');btnD.setAttribute('aria-disabled',droite?'false':'true');
    th.forEach(function(t,k){t.style.visibility=(ouvert&&k===cur)?'hidden':''});
  }
  function depuis(im,t){
    var f=im.getBoundingClientRect(),r=t.getBoundingClientRect();
    var nw=im.naturalWidth||1,nh=im.naturalHeight||1,s=Math.max(r.width/nw,r.height/nh),iw=nw*s,ih=nh*s;
    var cx=(1-r.width/iw)/2*100,cy=(1-r.height/ih)/2*100;
    return {transform:'translate('+((r.left+r.width/2)-(f.left+f.width/2))+'px,'+((r.top+r.height/2)-(f.top+f.height/2))+'px) scale('+(iw/f.width)+')',clipPath:'inset('+cy+'% '+cx+'% '+cy+'% '+cx+'%)'};
  }
  function ouvrir(i){
    build();cur=i;ouvert=true;ferme=false;dx=dy=0;
    v.hidden=false;R.classList.add('anim-vis-on');layout();place(false);
    var im=slides[i].im;
    if(!reduce.matches){
      var a=depuis(im,th[i]);
      im.animate([a,{transform:'none',clipPath:'inset(0% 0% 0% 0%)'}],{duration:300,easing:EASE});
      fond.animate([{opacity:0},{opacity:1}],{duration:300,easing:EASE});
      [cpt,btnX,btnG,btnD].forEach(function(e){e.animate([{opacity:0},{opacity:1}],{duration:300,easing:EASE})});
    }
    majUI();btnX.focus({preventScroll:true});
  }
  function fin(){
    v.hidden=true;R.classList.remove('anim-vis-on');ouvert=false;ferme=false;
    [fond,cpt,btnX,btnG,btnD].concat(slides.map(function(o){return o.im})).forEach(function(e){e.getAnimations().forEach(function(a){a.cancel()});});
    slides.forEach(function(o){o.im.style.transform='';o.im.style.transition=''});
    fond.style.opacity='';majUI();
    var t=th[cur];t.focus({preventScroll:true});
  }
  window.__animVisFin=function(){if(!v||!ouvert)return;th.forEach(function(x){x.style.visibility=''});fin()};
  function fermer(){
    if(!ouvert||ferme)return;ferme=true;
    var im=slides[cur].im,t=th[cur],r=t.getBoundingClientRect();
    var vis=r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth;
    var dep=im.style.transform||'none',op=fond.style.opacity===''?1:+fond.style.opacity;
    th.forEach(function(x,k){if(k!==cur)x.style.visibility=''});
    if(reduce.matches){fin();return}
    im.style.transform='';var a=vis?depuis(im,t):null;
    var anim;
    if(a){anim=im.animate([{transform:dep,clipPath:'inset(0% 0% 0% 0%)'},a],{duration:300,easing:EASE,fill:'forwards'})}
    else{anim=im.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'})}
    fond.style.opacity='';fond.animate([{opacity:op},{opacity:0}],{duration:300,easing:EASE,fill:'forwards'});
    [cpt,btnX,btnG,btnD].forEach(function(e){e.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'})});
    th[cur].style.visibility='hidden';
    anim.onfinish=function(){th[cur].style.visibility='';fin()};
  }
  function aller(k){
    if(k<0||k>=n||k===cur){dx=0;place('ressort');return}
    cur=k;dx=0;place(true);majUI();
  }
  function touche(e){
    if(!ouvert)return;
    if(e.key==='Escape'){e.preventDefault();fermer()}
    else if(e.key==='ArrowRight'){e.preventDefault();aller(cur+(RTL?-1:1))}
    else if(e.key==='ArrowLeft'){e.preventDefault();aller(cur+(RTL?1:-1))}
    else if(e.key==='Tab'){
      var f=[btnX,btnG,btnD].filter(function(b){return b.offsetParent!==null});
      var i=f.indexOf(D.activeElement);
      e.preventDefault();
      if(e.shiftKey)f[(i<=0?f.length:i)-1].focus();else f[(i+1)%f.length].focus();
    }
  }
  function down(e){
    if(!ouvert||ferme||e.target.closest('button')||(e.pointerType==='mouse'&&e.button!==0))return;
    g={id:e.pointerId,x0:e.clientX,y0:e.clientY,ax:null,pts:[{x:e.clientX,y:e.clientY,t:e.timeStamp}]};
    try{stage.setPointerCapture(e.pointerId)}catch(_){}
  }
  function move(e){
    if(!g||e.pointerId!==g.id)return;
    var ddx=e.clientX-g.x0,ddy=e.clientY-g.y0;
    if(!g.ax){if(Math.abs(ddx)<8&&Math.abs(ddy)<8)return;g.ax=Math.abs(ddx)>Math.abs(ddy)?'x':'y'}
    g.pts.push({x:e.clientX,y:e.clientY,t:e.timeStamp});if(g.pts.length>8)g.pts.shift();
    if(reduce.matches)return;
    if(g.ax==='x'){
      var step=sens===1?(ddx<0?1:-1):(ddx>0?1:-1),ok=cur+step>=0&&cur+step<n;
      dx=ok?ddx:ddx*.3;place(false);
    }else{
      dy=Math.max(0,ddy);var im=slides[cur].im;
      im.style.transform='translate3d(0,'+dy+'px,0) scale('+(1-Math.min(dy/H,1)*.25)+')';
      fond.style.opacity=String(1-Math.min(dy/(H*.6),1));
    }
  }
  function vit(axe){
    var p=g.pts,l=p[p.length-1],f=p[0];
    for(var i=0;i<p.length;i++){if(l.t-p[i].t<=100){f=p[i];break}}
    return (l[axe]-f[axe])/Math.max(1,l.t-f.t);
  }
  function up(e){
    if(!g||e.pointerId!==g.id)return;
    var s=g;try{stage.releasePointerCapture(e.pointerId)}catch(_){}
    if(s.ax==='x'){
      var ddx=e.clientX-s.x0,vx=vit('x'),vite=Math.abs(vx)>.11,loin=Math.abs(ddx)>W*.25;
      var sg=vite?Math.sign(vx):Math.sign(ddx),step=sens===1?(sg<0?1:-1):(sg>0?1:-1);
      g=null;
      if((vite||loin)&&cur+step>=0&&cur+step<n)aller(cur+step);
      else{dx=0;place(cur+step<0||cur+step>=n?'ressort':true)}
    }else if(s.ax==='y'){
      var ddy=e.clientY-s.y0,vy=vit('y');g=null;
      if(ddy>H*.12||(vy>.11&&ddy>20))fermer();
      else{
        dy=0;var im=slides[cur].im;
        if(!reduce.matches){im.animate([{transform:im.style.transform||'none'},{transform:'none'}],{duration:250,easing:EASE});}
        im.style.transform='';fond.style.opacity='';
      }
    }else g=null;
    place(false);
  }
})();

/* 12. bandeau vert de reassurance : sur telephone, cache au chargement (il cachait l'en-tete, Moshe 15/10),
   il apparait en haut une fois qu'on a defile, et disparait quand on revient tout en haut. */
(function(){
  var st=D.querySelector('.strip');if(!st)return;
  var mq=matchMedia('(max-width:699px)'),on=false;
  function f(){
    if(!mq.matches){if(on){on=false;R.classList.remove('strip-vis');}return;}
    var v=(window.scrollY||R.scrollTop)>220;
    if(v!==on){on=v;R.classList.toggle('strip-vis',v);}
    if(on)R.style.setProperty('--strip-h',st.offsetHeight+'px');
  }
  addEventListener('scroll',f,{passive:true});
  if(mq.addEventListener)mq.addEventListener('change',f);
  f();
})();

})();
