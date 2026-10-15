/* Mesure GA4 avec consentement (15/10). gtag.js ne se charge qu'apres un "Accept" : aucun hit avant. */
(function () {
  var ID = 'G-MJSV60Z8FG', KEY = 'mt-consent', DUREE = 15552000000; // 6 mois
  var T = {
    en: ['We use cookies to measure visits and improve the site.', 'Accept', 'Refuse', 'Privacy'],
    fr: ['Nous utilisons des cookies pour mesurer les visites et améliorer le site.', 'Accepter', 'Refuser', 'Confidentialité'],
    es: ['Usamos cookies para medir las visitas y mejorar el sitio.', 'Aceptar', 'Rechazar', 'Privacidad'],
    he: ['אנו משתמשים בעוגיות כדי למדוד ביקורים ולשפר את האתר.', 'לאשר', 'לסרב', 'פרטיות']
  };
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  if (!T[lang]) lang = 'en';
  var pre = lang === 'en' ? '' : '/' + lang;
  var tx = T[lang];
  window.dataLayer = window.dataLayer || [];
  var gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  var granted = false, loaded = false, bar = null;

  function lire() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (v && v.t && Date.now() - v.t < DUREE && (v.c === 'granted' || v.c === 'denied')) return v.c;
    } catch (e) {}
    return '';
  }
  function ecrire(c) { try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {} }
  function charger() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(s);
    gtag('config', ID, { cookie_expires: 34128000 });
  }
  function effacerCookies() {
    var h = location.hostname.split('.'), doms = [location.hostname, '.' + location.hostname];
    if (h.length > 2) doms.push('.' + h.slice(-2).join('.'));
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n === '_ga' || n.indexOf('_ga_') === 0) doms.forEach(function (d) {
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=' + d;
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      });
    });
  }
  function appliquer(c) {
    gtag('consent', 'update', { ad_storage: c, analytics_storage: c, ad_user_data: c, ad_personalization: c });
    granted = c === 'granted';
    if (granted) charger(); else if (loaded) effacerCookies();
  }

  /* evenements du formulaire : objets {event:...} pousses dans dataLayer, relayes vers gtag */
  var OK = { form_start: 1, form_step: 1, generate_lead: 1 };
  function relais(o) {
    if (!granted || !o || Object.prototype.toString.call(o) !== '[object Object]' || !OK[o.event]) return;
    var p = { lang: lang };
    ['branch', 'step', 'step_index', 'budget'].forEach(function (k) { if (o[k] !== undefined) p[k] = o[k]; });
    gtag('event', o.event, p);
  }
  var dl = window.dataLayer, push0 = dl.push;
  dl.push = function () {
    var r = push0.apply(dl, arguments);
    for (var i = 0; i < arguments.length; i++) relais(arguments[i]);
    return r;
  };
  function rejouer() { for (var i = 0; i < dl.length; i++) relais(dl[i]); }

  function wa() {
    if (granted) gtag('event', 'whatsapp_click', { page: location.pathname, lang: lang, transport_type: 'beacon' });
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href*="wa.me"]');
    if (a) wa();
  }, true);
  var open0 = window.open;
  window.open = function (u) { if (u && String(u).indexOf('wa.me') > -1) wa(); return open0.apply(window, arguments); };

  /* banniere */
  function montrer() {
    if (bar) { bar.hidden = false; return; }
    bar = document.createElement('div');
    bar.className = 'cb' + (/\/plan-your-trip\/?$/.test(location.pathname) ? ' cb-haut' : '');
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'Cookies');
    var p = document.createElement('p');
    p.appendChild(document.createTextNode(tx[0] + ' '));
    var a = document.createElement('a'); a.href = pre + '/privacy/'; a.textContent = tx[3]; p.appendChild(a);
    var d = document.createElement('div'); d.className = 'cb-b';
    [['granted', tx[1]], ['denied', tx[2]]].forEach(function (b) {
      var x = document.createElement('button'); x.type = 'button'; x.textContent = b[1];
      x.addEventListener('click', function () { ecrire(b[0]); appliquer(b[0]); if (b[0] === 'granted') rejouer(); bar.hidden = true; });
      d.appendChild(x);
    });
    bar.appendChild(p); bar.appendChild(d);
    document.body.appendChild(bar);
  }
  document.addEventListener('click', function (e) {
    var c = e.target && e.target.closest && e.target.closest('[data-cookies]');
    if (c) { e.preventDefault(); montrer(); }
  });
  var c0 = lire();
  if (c0) { appliquer(c0); if (c0 === 'granted') rejouer(); } else montrer();
})();
