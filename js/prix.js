/* Prix publics de la grille tarifaire (Apps Script, onglet « Grille Mendel », lignes cochées « Public » par Moshé).
   data-prix-tpl="à partir de {r_soir_vente} €" : remplacé seulement si toutes les clés existent et sont des nombres.
   data-prix="cle" : remplace le texte par la valeur. Sans réponse ou sans valeur : le texte d'origine reste. */
(function () {
  var URL = 'https://script.google.com/macros/s/AKfycbz9BOV80s-OY8i66FZsFM-zoD4icjchnWwckSBWVtcg7KzPq6xSgPqHF9D2NGP_M7KW/exec?prix=1';
  var els = document.querySelectorAll('[data-prix-tpl],[data-prix]');
  if (!els.length || !window.fetch) return;
  var ok = function (v) { return typeof v === 'string' && /^\d+([.,]\d+)?$/.test(v.trim()); };
  var fmt = function (v) { return v.trim().replace('.', ','); };
  var ctl = window.AbortController ? new AbortController() : null;
  if (ctl) setTimeout(function () { ctl.abort(); }, 6000);
  fetch(URL, ctl ? { signal: ctl.signal } : {}).then(function (r) { return r.json(); }).then(function (j) {
    var P = (j && j.prix) || {};
    els.forEach(function (el) {
      var tpl = el.getAttribute('data-prix-tpl');
      if (tpl) {
        var manque = false;
        var out = tpl.replace(/\{([\w.]+)\}/g, function (_, k) { if (!ok(P[k])) { manque = true; return ''; } return fmt(P[k]); });
        if (!manque) el.innerHTML = out;
      } else {
        var k = el.getAttribute('data-prix');
        if (ok(P[k])) el.textContent = fmt(P[k]);
      }
    });
  }).catch(function () {});
})();
