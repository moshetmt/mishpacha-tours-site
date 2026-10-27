/* Vidéo de fond des héros intérieurs : <section class="hero lead-hero3" data-video="chalets">.
   La photo s'affiche d'abord ; la vidéo se charge après la page, jamais en économie de données ni en mouvement réduit. */
(function(){
var h=document.querySelector('.lead-hero3[data-video]');if(!h)return;
var c=navigator.connection||{};
if(c.saveData||/(^|-)2g$/.test(c.effectiveType||'')||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function go(){
  var t=matchMedia('(max-width:899.98px)').matches?'tel':'pc',n=h.getAttribute('data-video');
  var v=document.createElement('video');
  v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute('playsinline','');v.setAttribute('aria-hidden','true');v.tabIndex=-1;v.preload='auto';
  v.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease;pointer-events:none';
  var s=document.createElement('source');s.src='/img/video/'+n+'-'+t+'.mp4';s.type='video/mp4';v.appendChild(s);
  var img=h.querySelector(':scope > img');if(img)img.after(v);else h.prepend(v);
  v.addEventListener('playing',function(){v.style.opacity='1'},{once:true});
  var p=v.play();if(p&&p.catch)p.catch(function(){});
  if('IntersectionObserver'in window)new IntersectionObserver(function(e){e[0].isIntersecting?v.play().catch(function(){}):v.pause()}).observe(h);
}
if(document.readyState==='complete')setTimeout(go,300);else addEventListener('load',function(){setTimeout(go,300)});
})();
