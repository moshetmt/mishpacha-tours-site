/* Formulaire court de l'accueil EN (heros et section Contact, v9 du 31/10, decision Moshe).
   Chaque <form class="form-court"> : prenom et WhatsApp obligatoires, « Where and when? » facultatif.
   Envoi au meme Apps Script que le tunnel (source=court, lead=<id>) ; on reste sur la page jusqu'a la reponse,
   puis /contact-quick/thanks/ (prenom et numero en sessionStorage, jamais dans l'adresse). */
(function () {
  var forms = [].slice.call(document.querySelectorAll('form.form-court'));
  if (!forms.length) return;
  var R = { US: '+1', CA: '+1', GB: '+44', IL: '+972', FR: '+33', BE: '+32', CH: '+41', ES: '+34', IT: '+39', DE: '+49', NL: '+31',
            AR: '+54', MX: '+52', BR: '+55', AU: '+61', ZA: '+27', RU: '+7', UA: '+380' },
      L = { he: '+972', iw: '+972', fr: '+33', es: '+34', it: '+39', de: '+49', nl: '+31', ru: '+7', uk: '+380', pt: '+55' };
  function devine(sel) {
    function poser(v) { if (v && !sel.value && [].some.call(sel.options, function (o) { return o.value === v; })) sel.value = v; }
    (navigator.languages || [navigator.language || '']).forEach(function (l) {
      var m = /^([a-z]{2,3})(?:-([A-Z]{2}))?/i.exec(l || ''); if (!m) return;
      poser(m[2] ? R[m[2].toUpperCase()] : ''); poser(L[m[1].toLowerCase()]);
    });
    if (!sel.value) {
      var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (x) {}
      poser(/Jerusalem|Tel_Aviv/.test(tz) ? '+972' : /^America\/(New_York|Chicago|Denver|Los_Angeles|Toronto|Montreal)/.test(tz) ? '+1' :
            /London/.test(tz) ? '+44' : /Paris/.test(tz) ? '+33' : '');
    }
  }
  var dl = window.dataLayer = window.dataLayer || [];
  forms.forEach(function (f) {
    var sel = f.elements.indicatif, err = f.querySelector('.fc-erreur'), b = f.querySelector('button[type=submit]'), sent = false;
    // 03/11 : textes des accueils FR/ES/HE lus dans data-* (l'EN n'en a pas et garde l'anglais)
    var T = function (k, d) { return f.getAttribute('data-' + k) || d; };
    devine(sel);
    f.addEventListener('input', function (ev) { var t = ev.target; if (t.getAttribute('aria-invalid') === 'true' && (t.value || '').trim()) t.setAttribute('aria-invalid', 'false'); });
    function dire(txt, lien) {
      err.hidden = false; err.textContent = txt;
      if (lien) { var a = document.createElement('a'); a.href = lien; a.rel = 'noopener'; a.textContent = T('msg-wa', 'Send on WhatsApp'); err.appendChild(document.createTextNode(' ')); err.appendChild(a); }
    }
    f.addEventListener('submit', function (ev) {
      ev.preventDefault(); if (sent) return;
      if (f.elements.societe && f.elements.societe.value) { location.href = '/contact-quick/thanks/'; return; }
      var pre = f.elements.prenom.value.trim(), ind = sel.value, tel = f.elements.tel.value.replace(/[^0-9]/g, ''), manque = [];
      if (!pre) manque.push(f.elements.prenom); if (!ind) manque.push(sel); if (tel.length < 6) manque.push(f.elements.tel);
      [f.elements.prenom, sel, f.elements.tel].forEach(function (e) { e.setAttribute('aria-invalid', manque.indexOf(e) >= 0 ? 'true' : 'false'); });
      if (manque.length) { dire(T('msg-manque', 'Please add your first name and your WhatsApp number.')); manque[0].focus(); return; }
      err.hidden = true;
      if (ind !== '+39') tel = tel.replace(/^0+/, '');
      var ou = (f.elements.ou.value || '').trim().slice(0, 200), ou_ = f.getAttribute('data-ou') || 'home',
          lead = 'q' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
          parts = ['Trip: Quick request (short form)'];
      if (ou) parts.push('Where and when: ' + ou);
      parts.push('Source: short form, home page (' + ou_ + '), ref ' + lead);
      var payload = JSON.stringify({ tour: 'Quick request', dates: '', personnes: '', langue: T('langue', 'English'), nom: pre, contact: (ind + ' ' + tel).trim(),
        message: parts.join(' | '), message_en: parts.join(' | '), nuits: '', page: location.pathname, params: '?form=' + ou_, source: 'court', lead: lead });
      sent = true; var lab = b.textContent; b.disabled = true; b.textContent = T('msg-envoi', 'Sending');
      var fini = false,
          ok = function () {
            if (fini) return; fini = true;
            try { sessionStorage.setItem('mt-court', JSON.stringify({ lead: lead, prenom: pre, wa: (ind + tel).replace(/[^0-9]/g, ''), q: '' })); } catch (x) {}
            window.MT_FORM = f; dl.push({ event: 'generate_lead', branch: 'court' });
            location.href = '/contact-quick/thanks/';
          },
          ko = function () {
            if (fini) return; fini = true; sent = false; b.disabled = false; b.textContent = lab;
            var t = T('msg-salut', 'Hello, I am') + ' ' + pre + '.' + (ou ? ' ' + ou + '.' : '');
            dire(T('msg-ko', 'Your request did not go through.'), 'https://wa.me/33652092301?text=' + encodeURIComponent(t));
            dl.push({ event: 'form_error' });
          };
      setTimeout(ko, 20000);
      try { fetch(window.MISHPACHA_ENDPOINT, { method: 'POST', body: payload }).then(function (r) { return r.json(); }).then(function (j) { j && j.ok ? ok() : ko(); })['catch'](ko); } catch (x) { ko(); }
    });
  });
})();
