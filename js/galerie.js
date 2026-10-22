/* Galerie plein ecran des pages chalet (22/10). Blocs et CSS poses par _galerie_chalets.py.
   Echap ferme ; l'adresse prend #photos a l'ouverture pour que le bouton retour du telephone ferme la galerie ; defilement de la page bloque. */
(function () {
  var g = document.getElementById('galerie');
  if (!g) return;
  var html = document.documentElement;
  var rail = document.querySelector('.gal-rail');
  var cpt = document.querySelector('.gal-cpt');
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
    var t = ev.target.closest ? ev.target.closest('[data-gal-open],[data-gal-close],.gal-rail,.gal-som a') : null;
    if (!t) return;
    if (t.hasAttribute('data-gal-open') || t.classList.contains('gal-rail')) { ev.preventDefault(); ouvrir(); return; }
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

  /* telephone : compteur du rail */
  if (rail && cpt) {
    var n = rail.children.length, att = false;
    rail.addEventListener('scroll', function () {
      if (att) return;
      att = true;
      requestAnimationFrame(function () {
        att = false;
        var w = rail.clientWidth || 1;
        var i = Math.min(n - 1, Math.max(0, Math.round(Math.abs(rail.scrollLeft) / w)));
        cpt.textContent = (i + 1) + '/' + n;
      });
    }, { passive: true });
  }

  if (location.hash === '#photos') ouvrir();
})();
