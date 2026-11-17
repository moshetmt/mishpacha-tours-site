/* Mesure GA4 + conversions Google Ads avec consentement (15/10, Ads le 19/10).
   gtag.js ne se charge qu'apres un "Accept" : aucun hit avant.
   ===== A REMPLIR PAR L'OPERATEUR (procedure : 06-reports/2026-10-19-mesure-conversions-ads.md) =====
   Tant que ADS.id est vide, aucune balise Ads n'est chargee et aucune conversion Ads n'est envoyee. */
(function () {
  var ADS = {
    id: 'AW-18513655242',     // ID de conversion du compte 950-679-6570, forme AW-1234567890
    lead: 'tQXdCJb14KMdEMrr__tE',   // etiquette de l'action « Demande envoyee », forme AbC_dEfGhIjKl (sans l'ID, sans le slash)
    wa: 'bs0kCK-f2KMdEMrr__tE'      // etiquette de l'action « Clic WhatsApp »
  };
  var EC = true; // conversions ameliorees : telephone/e-mail du formulaire envoyes hachees (SHA-256 par gtag), seulement apres Accept
  /* ===== fin de la zone a remplir ===== */
  var ID = 'G-MJSV60Z8FG', KEY = 'mt-consent', DUREE = 15552000000, LEAD = 'mt-lead'; // 6 mois
  var AWOK = /^AW-\d{6,}$/.test(ADS.id);
  var T = {
    en: ['Cookies to measure visits and ads.', 'Accept', 'Refuse', 'Privacy'],
    fr: ['Cookies de mesure des visites et annonces.', 'Accepter', 'Refuser', 'Confidentialité'],
    es: ['Cookies para medir visitas y anuncios.', 'Aceptar', 'Rechazar', 'Privacidad'],
    he: ['עוגיות למדידת ביקורים ופרסומות.', 'לאשר', 'לסרב', 'פרטיות']
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
    if (AWOK) gtag('config', ADS.id, { allow_ad_personalization_signals: false }); // mesure des conversions seulement, pas de remarketing
  }
  function effacerCookies() {
    var h = location.hostname.split('.'), doms = [location.hostname, '.' + location.hostname];
    if (h.length > 2) doms.push('.' + h.slice(-2).join('.'));
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n === '_ga' || n.indexOf('_ga_') === 0 || n.indexOf('_gcl_') === 0) doms.forEach(function (d) {
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=' + d;
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      });
    });
  }
  function appliquer(c) {
    gtag('consent', 'update', { ad_storage: c, analytics_storage: c, ad_user_data: c, ad_personalization: c });
    granted = c === 'granted';
    if (granted) { charger(); leadMerci(); } else { if (loaded) effacerCookies(); try { sessionStorage.removeItem(LEAD); } catch (e) {} }
  }

  /* evenements du formulaire : objets {event:...} pousses dans dataLayer, relayes vers gtag.
     generate_lead n'est PAS envoye depuis la page du formulaire (la redirection vers /merci/ peut couper le hit) :
     un drapeau est pose en sessionStorage, la page /merci/ l'envoie une seule fois puis l'efface. */
  var OK = { form_start: 1, form_step: 1 };
  function relais(o) {
    if (!o || Object.prototype.toString.call(o) !== '[object Object]' || o.__r) return;
    if (o.event === 'generate_lead') { o.__r = 1; poserLead(o); return; }
    if (!granted || !OK[o.event]) return;
    o.__r = 1;
    var p = { lang: lang };
    ['branch', 'step', 'step_index'].forEach(function (k) { if (o[k] !== undefined) p[k] = o[k]; });
    gtag('event', o.event, p);
  }
  function e164() {
    var fm = window.MT_FORM || document, i = fm.querySelector('[name=indicatif]'), t = fm.querySelector('[name=tel]');   // accueil : deux formulaires courts
    var c = i ? String(i.value).replace(/\D/g, '') : '', n = t ? String(t.value).replace(/\D/g, '') : '';
    if (!c || n.length < 6) return '';
    if (c !== '39') n = n.replace(/^0+/, '');
    return '+' + c + n;
  }
  function poserLead(o) {
    if (lire() === 'denied') return;
    var d = { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8), t: Date.now(), branch: o.branch || '', budget: String(o.budget || '').slice(0, 40) };
    if (granted && EC) {
      var m = document.querySelector('[name=email]'); d.ph = e164(); d.em = m ? String(m.value).trim().toLowerCase() : '';
    }
    try { sessionStorage.setItem(LEAD, JSON.stringify(d)); } catch (e) { if (granted) envoyerLead(d); }
  }
  function envoyerLead(d) {
    var u = {};
    if (AWOK && EC) {
      if (d.ph) u.phone_number = d.ph;
      if (d.em && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.em)) u.email = d.em;
      if (u.phone_number || u.email) gtag('set', 'user_data', u);
    }
    gtag('event', 'generate_lead', { lang: lang, branch: d.branch, budget: d.budget, transaction_id: d.id });
    if (AWOK && ADS.lead) gtag('event', 'conversion', { send_to: ADS.id + '/' + ADS.lead, transaction_id: d.id });
  }
  function leadMerci() {
    if (!granted || !/\/(merci|contact-quick\/thanks)\/?$/.test(location.pathname)) return;
    var d = null;
    try { d = JSON.parse(sessionStorage.getItem(LEAD) || 'null'); sessionStorage.removeItem(LEAD); } catch (e) {}
    if (d && d.id && Date.now() - d.t < 1800000) envoyerLead(d);
  }

  var dl = window.dataLayer, push0 = dl.push;
  dl.push = function () {
    var r = push0.apply(dl, arguments);
    for (var i = 0; i < arguments.length; i++) relais(arguments[i]);
    return r;
  };
  function rejouer() { for (var i = 0; i < dl.length; i++) relais(dl[i]); }

  var waT = 0;
  function emplacement(a) {
    if (!a || !a.closest) return 'script';
    if (a.closest('.wa-flottant')) return 'floating';
    if (a.closest('#panneau')) return 'menu';
    if (a.closest('.nav,header')) return 'header';
    if (a.closest('footer,.pied')) return 'footer';
    return 'content';
  }
  function wa(a, href) {
    if (!granted || Date.now() - waT < 1000) return;
    waT = Date.now();
    if (/33781823193/.test(href || '')) { // Beth Habad (minyan, repas en station) : pas une demande Mishpacha, ni conversion ni whatsapp_click
      gtag('event', 'beth_habad_click', { page: location.pathname, lang: lang, link_location: emplacement(a), transport_type: 'beacon' });
      return;
    }
    var apres = /\/(merci|contact-quick\/thanks)\/?$/.test(location.pathname); // bouton de la page merci : apres la demande, pas une conversion
    gtag('event', 'whatsapp_click', { page: location.pathname, lang: lang, link_location: apres ? 'merci' : emplacement(a),
      offre: (a && a.getAttribute && a.getAttribute('data-offre')) || undefined, transport_type: 'beacon' });
    if (AWOK && ADS.wa && !apres) gtag('event', 'conversion', { send_to: ADS.id + '/' + ADS.wa, transport_type: 'beacon' });
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('wa.me') > -1) wa(a, h);
    else if (granted && /^mailto:/i.test(h)) gtag('event', 'email_click', { page: location.pathname, lang: lang, transport_type: 'beacon' });
    else if (granted && /^tel:/i.test(h)) gtag('event', 'phone_click', { page: location.pathname, lang: lang, transport_type: 'beacon' });
  }, true);
  var open0 = window.open;
  window.open = function (u) { if (u && String(u).indexOf('wa.me') > -1) wa(null, String(u)); return open0.apply(window, arguments); };

  /* banniere */
  /*LOT1-1611*/
  /* le bandeau masque reste masque (attribut hidden + display:none inline important) ; classe cb-on sur <html> et variables --cb-h / --cb-push
     pour que le premier ecran du heros remonte de la place du bandeau tant qu'il est affiche */
  function mesurer() {
    var d = document.documentElement;
    if (!bar || bar.hidden) return;
    d.style.setProperty('--cb-h', bar.offsetHeight + 'px');
    d.style.setProperty('--cb-push', '0px');
    var top = bar.getBoundingClientRect().top, bas = 0;
    var hero = document.querySelector('main>section.hero,main>section.lv-hero-photo,main>section.lv-hero-station');
    if (hero) hero.querySelectorAll('a,button,h1,h2,p,small').forEach(function (e) {
      var r = e.getBoundingClientRect();
      if (r.width && r.height && r.bottom <= window.innerHeight + 1 && r.bottom > bas) bas = r.bottom;
    });
    d.style.setProperty('--cb-push', Math.max(0, Math.ceil(bas + 12 - top)) + 'px');
    /* fiche chalet (pas de heros plein ecran) : sur telephone et tablette, la galerie raccourcit pour que les boutons du premier ecran restent au-dessus du bandeau */
    d.style.setProperty('--cb-gal', '0px');
    var g = document.querySelector('.lc-galerie');
    if (!hero && g && window.innerWidth < 900) {
      var gh = g.getBoundingClientRect().height, pb = 0;
      document.querySelectorAll('main a.btn-noir,main a.pill,main a[href*="wa.me"],main button').forEach(function (e) {
        if (e.closest('.cb,.barre-basse,.nav,.lc-galerie')) return;
        var r = e.getBoundingClientRect();
        if (r.width && r.height && r.top < window.innerHeight && r.bottom > top - 12 && r.bottom + 12 - top > pb) pb = r.bottom + 12 - top;
      });
      d.style.setProperty('--lc-gh', gh + 'px');
      d.style.setProperty('--cb-gal', Math.max(0, Math.min(Math.ceil(pb), gh - 170)) + 'px');
    }
  }
  function poser(on) {
    var d = document.documentElement;
    if (on) { d.classList.add('cb-on'); mesurer(); }
    else { d.classList.remove('cb-on'); d.style.removeProperty('--cb-h'); d.style.removeProperty('--cb-push'); d.style.removeProperty('--cb-gal'); d.style.removeProperty('--lc-gh'); }
  }
  function cacher() { bar.hidden = true; bar.style.setProperty('display', 'none', 'important'); poser(false); }
  window.addEventListener('resize', mesurer);
  function montrer() {
    if (bar) { bar.hidden = false; bar.style.removeProperty('display'); poser(true); return; }
    bar = document.createElement('div');
    bar.className = 'cb';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'Cookies');
    var p = document.createElement('p');
    p.appendChild(document.createTextNode(tx[0] + ' '));
    var a = document.createElement('a'); a.href = pre + '/privacy/'; a.textContent = tx[3]; p.appendChild(a);
    var d = document.createElement('div'); d.className = 'cb-b';
    [['granted', tx[1]], ['denied', tx[2]]].forEach(function (b) {
      var x = document.createElement('button'); x.type = 'button'; x.textContent = b[1];
      x.addEventListener('click', function () { ecrire(b[0]); appliquer(b[0]); if (b[0] === 'granted') rejouer(); cacher(); });
      d.appendChild(x);
    });
    bar.appendChild(p); bar.appendChild(d);
    document.body.appendChild(bar);
    poser(true);
  }
  document.addEventListener('click', function (e) {
    var c = e.target && e.target.closest && e.target.closest('[data-cookies]');
    if (c) { e.preventDefault(); montrer(); }
  });
  var c0 = lire();
  if (c0) { appliquer(c0); if (c0 === 'granted') rejouer(); } else montrer();
})();
