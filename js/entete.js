/* entete.js : comportement de l'en-tete unique (header.mt-tete), 16/11/2026.
   Panneau du burger (aria-expanded, piege de focus, Echap, inert sur la page), selecteur de langue (clic dehors, Echap),
   menu des chalets (Echap, aria-expanded), et garde d'ajustement : si l'en-tete ne tient pas dans la largeur (traduction
   automatique, libelle plus long, police de repli), il passe seul en mode compact puis retire le bouton. */
(function () {
  'use strict';
  var D = document, B = D.body, H = D.querySelector('.mt-tete');
  if (!H) return;
  var burger = H.querySelector('.mt-burger'), pan = D.getElementById('panneau'),
      lang = H.querySelector('.mt-langue'), ch = H.querySelector('.mt-ch'),
      corps = H.querySelector('.mt-corps'), lienCh = H.querySelector('.mt-ch-lien');
  var large = matchMedia('(min-width:1280px)');
  var FOC = 'a[href],button:not([disabled]),summary,[tabindex]:not([tabindex="-1"])';
  var inertes = [];

  function visibles(racine) {
    return [].slice.call(racine.querySelectorAll(FOC)).filter(function (x) {
      return x.getClientRects().length && getComputedStyle(x).visibility !== 'hidden';
    });
  }

  /* ---------- panneau ---------- */
  function ouvert() { return pan && !pan.hidden; }
  function ouvrir() {
    if (!pan || ouvert()) return;
    if (lang) lang.open = false;
    pan.style.top = Math.max(0, Math.round(H.getBoundingClientRect().bottom)) + 'px';
    pan.hidden = false;
    burger.setAttribute('aria-expanded', 'true');
    H.setAttribute('data-menu', 'ouvert');
    B.classList.add('menu-ouvert');
    [].forEach.call(B.children, function (n) {
      if (n === H || n === pan || n.tagName === 'SCRIPT' || n.tagName === 'SVG' || n.tagName === 'svg' || n.hasAttribute('inert')) return;
      n.setAttribute('inert', ''); inertes.push(n);
    });
    var f = visibles(pan)[0]; if (f) f.focus({ preventScroll: true });
  }
  function fermer(retour) {
    if (!pan || !ouvert()) return;
    pan.hidden = true;
    pan.style.top = '';
    burger.setAttribute('aria-expanded', 'false');
    H.removeAttribute('data-menu');
    B.classList.remove('menu-ouvert');
    inertes.forEach(function (n) { n.removeAttribute('inert'); }); inertes = [];
    if (retour) burger.focus({ preventScroll: true });
  }
  if (burger && pan) {
    burger.addEventListener('click', function () { ouvert() ? fermer(true) : ouvrir(); });
    pan.addEventListener('click', function (ev) { if (ev.target.closest('a')) fermer(false); });
    large.addEventListener && large.addEventListener('change', function () { if (large.matches) fermer(false); });
  }

  /* ---------- langue ---------- */
  if (lang) {
    D.addEventListener('pointerdown', function (ev) { if (lang.open && !lang.contains(ev.target)) lang.open = false; });
  }

  /* ---------- menu des chalets ---------- */
  function majCh() {
    if (!ch || !lienCh) return;
    var o = !ch.hasAttribute('data-ferme') && (ch.matches(':hover') || ch.matches(':focus-within'));
    lienCh.setAttribute('aria-expanded', o ? 'true' : 'false');
  }
  if (ch) {
    ['mouseenter', 'mouseleave', 'focusin', 'focusout'].forEach(function (t) {
      ch.addEventListener(t, function () {
        if (t === 'mouseenter') ch.removeAttribute('data-ferme');      /* une nouvelle entree du pointeur rouvre le menu */
        if (t === 'mouseleave' || t === 'focusout') setTimeout(function () { if (!ch.matches(':hover') && !ch.matches(':focus-within')) ch.removeAttribute('data-ferme'); majCh(); }, 0);
        else majCh();
      });
    });
  }

  /* ---------- clavier ---------- */
  D.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') {
      if (ouvert()) { fermer(true); ev.preventDefault(); return; }
      if (lang && lang.open) { lang.open = false; lang.querySelector('summary').focus(); ev.preventDefault(); return; }
      if (ch && lienCh && lienCh.getAttribute('aria-expanded') === 'true') {
        ch.setAttribute('data-ferme', ''); lienCh.setAttribute('aria-expanded', 'false');
        if (ch.contains(D.activeElement)) lienCh.focus();
        ev.preventDefault();
      }
      return;
    }
    if (ev.key === 'Tab' && ouvert()) {
      var liste = visibles(H).concat(visibles(pan));
      if (!liste.length) return;
      /* le piege mene le focus lui-meme : il ne depend pas de l'ordre de tabulation du navigateur (Safari saute les liens) */
      var i = liste.indexOf(D.activeElement);
      var n = ev.shiftKey ? (i <= 0 ? liste.length - 1 : i - 1) : (i < 0 || i === liste.length - 1 ? 0 : i + 1);
      liste[n].focus(); ev.preventDefault();
    }
  });

  /* ---------- garde d'ajustement : l'en-tete tient, ou il se simplifie ---------- */
  function tient() { return corps.scrollWidth <= corps.clientWidth + 1; }
  function ajuster() {
    H.removeAttribute('data-compact'); H.removeAttribute('data-nocta'); H.removeAttribute('data-nowa');
    if (!tient()) H.setAttribute('data-nowa', '');                       /* 1. le second bouton WhatsApp (hebreu) cede d'abord */
    if (large.matches && !tient()) H.setAttribute('data-compact', '');   /* 2. puis la navigation complete cede au burger */
    if (!tient()) H.setAttribute('data-nocta', '');                      /* 3. puis le bouton Plan your trip */
  }
  var t = 0;
  function planifier() { clearTimeout(t); t = setTimeout(ajuster, 60); }
  addEventListener('resize', planifier);
  addEventListener('load', ajuster);
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(ajuster);
  if (window.MutationObserver) new MutationObserver(planifier).observe(corps, { childList: true, subtree: true, characterData: true });
  ajuster();
  H.setAttribute('data-pret', '');
})();
