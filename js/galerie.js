/* Galerie plein ecran des pages chalet (22/10). Blocs et CSS poses par _galerie_chalets.py.
   Echap ferme ; l'adresse prend #photos a l'ouverture pour que le bouton retour du telephone ferme la galerie ; defilement de la page bloque. */
(function () {
  var g = document.getElementById('galerie');
  if (!g) return;
  var html = document.documentElement;
  var main = g.querySelector('.gal-main');
  var liens = [].slice.call(g.querySelectorAll('.gal-som a'));
  var reduit = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ouvert = false, pousse = false, retour = null;

  function ouvrir() {
    if (ouvert) return;
    ouvert = true;
    retour = document.activeElement;
    g.hidden = false;
    html.classList.add('gal-ouvert');
    if (location.hash !== '#photos') {
      try { history.pushState({ gal: 1 }, '', '#photos'); pousse = true; } catch (e) {}
    }
    g.scrollTop = 0;
    if (main) main.scrollTop = 0;
    try { g.focus({ preventScroll: true }); } catch (e) {}
    suivre();
  }

  function fermer(depuisHistorique) {
    if (!ouvert) return;
    ouvert = false;
    g.hidden = true;
    html.classList.remove('gal-ouvert');
    if (!depuisHistorique) {
      if (pousse) { pousse = false; history.back(); }
      else if (location.hash === '#photos') {
        try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
      }
    } else { pousse = false; }
    if (retour && retour.focus) { try { retour.focus({ preventScroll: true }); } catch (e) {} }
  }

  document.addEventListener('click', function (ev) {
    var t = ev.target.closest ? ev.target.closest('[data-gal-open],[data-gal-close],.gal-som a') : null;
    if (!t) return;
    if (t.hasAttribute('data-gal-open')) { ev.preventDefault(); ouvrir(); return; }
    if (t.hasAttribute('data-gal-close')) { ev.preventDefault(); fermer(false); return; }
    if (t.tagName === 'A' && g.contains(t)) {
      ev.preventDefault();
      var cible = g.querySelector(t.getAttribute('href'));
      if (cible) cible.scrollIntoView({ behavior: reduit ? 'auto' : 'smooth', block: 'start' });
    }
  });

  document.addEventListener('keydown', function (ev) {
    if (ouvert && (ev.key === 'Escape' || ev.key === 'Esc')) { ev.preventDefault(); fermer(false); }
  });

  window.addEventListener('popstate', function () {
    if (location.hash === '#photos') ouvrir(); else fermer(true);
  });

  /* sommaire : piece courante soulignee (ordinateur) */
  function suivre() {
    if (!main || !liens.length) return;
    var haut = main.getBoundingClientRect().top + 140, cur = 0;
    var pieces = main.querySelectorAll('.gal-piece');
    for (var i = 0; i < pieces.length; i++) { if (pieces[i].getBoundingClientRect().top <= haut) cur = i; }
    for (var j = 0; j < liens.length; j++) liens[j].setAttribute('aria-current', j === cur ? 'true' : 'false');
  }
  if (main) main.addEventListener('scroll', function () { if (ouvert) suivre(); }, { passive: true });

  if (location.hash === '#photos') ouvrir();
})();

/* « Le chalet en images » (27/10) : visionneuse photo par photo. Flèches, glisser au doigt, Échap, compteur 3/19. */
(function () {
  var sec = document.querySelector('.chalet-images');
  if (!sec) return;
  var tuiles = [].slice.call(sec.querySelectorAll('.ci-tuile'));
  var n = tuiles.length, cur = 0, retour = null, html = document.documentElement;
  var rtl = html.dir === 'rtl';
  var v = document.createElement('div');
  v.className = 'ci-vue'; v.hidden = true;
  v.setAttribute('role', 'dialog'); v.setAttribute('aria-modal', 'true'); v.tabIndex = -1;
  function bouton(cls, lab) { var b = document.createElement('button'); b.type = 'button'; b.className = cls; b.setAttribute('aria-label', lab); return b; }
  var bx = bouton('ci-x', sec.dataset.lFer), bp = bouton('ci-prv', sec.dataset.lPrv), bn = bouton('ci-nxt', sec.dataset.lNxt);
  bx.textContent = '×';
  var fig = document.createElement('figure'), img = document.createElement('img'), cap = document.createElement('figcaption');
  var cpt = document.createElement('span'), leg = document.createElement('span');
  cpt.className = 'ci-cpt'; leg.className = 'ci-leg';
  cap.appendChild(cpt); cap.appendChild(document.createTextNode(' ')); cap.appendChild(leg);
  fig.appendChild(img); fig.appendChild(cap);
  v.appendChild(bx); v.appendChild(bp); v.appendChild(fig); v.appendChild(bn);
  document.body.appendChild(v);

  function montrer(i) {
    cur = (i + n) % n;
    var src = tuiles[cur].querySelector('img');
    img.removeAttribute('srcset');
    if (src.getAttribute('srcset')) { img.setAttribute('srcset', src.getAttribute('srcset')); img.sizes = '100vw'; }
    img.src = src.getAttribute('src');
    img.alt = src.alt; leg.textContent = src.alt; cpt.textContent = (cur + 1) + '/' + n;
    v.setAttribute('aria-label', src.alt);
    [cur + 1, cur - 1].forEach(function (k) { var t = tuiles[(k + n) % n].querySelector('img'); if (t.loading === 'lazy') t.loading = 'eager'; });
  }
  function ouvrir(i) {
    retour = document.activeElement; v.hidden = false; html.classList.add('gal-ouvert');
    montrer(i); try { v.focus({ preventScroll: true }); } catch (e) {}
  }
  function fermer() {
    v.hidden = true; html.classList.remove('gal-ouvert');
    if (retour && retour.focus) { try { retour.focus({ preventScroll: true }); } catch (e) {} }
  }
  tuiles.forEach(function (t) { t.addEventListener('click', function () { ouvrir(+t.dataset.ci); }); });
  bx.addEventListener('click', fermer);
  bp.addEventListener('click', function () { montrer(cur - 1); });
  bn.addEventListener('click', function () { montrer(cur + 1); });
  v.addEventListener('click', function (e) { if (e.target === v) fermer(); });
  document.addEventListener('keydown', function (e) {
    if (v.hidden) return;
    if (e.key === 'Escape' || e.key === 'Esc') { e.preventDefault(); fermer(); }
    else if (e.key === 'ArrowRight') montrer(cur + (rtl ? -1 : 1));
    else if (e.key === 'ArrowLeft') montrer(cur + (rtl ? 1 : -1));
  });
  var x0 = null;
  v.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  v.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) montrer(cur + ((dx < 0) !== rtl ? 1 : -1));
  }, { passive: true });
})();
