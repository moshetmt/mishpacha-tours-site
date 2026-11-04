/* Cartes OpenStreetMap des pages Alpes : Leaflet ne se charge que lorsque la carte approche de l'écran (DESIGN-SITE §6). */
(function () {
  var c = [].slice.call(document.querySelectorAll('.carte-osm[data-points]')), go = false;
  if (!c.length) return;
  var CDN = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.';
  function init() {
    c.forEach(function (el) {
      var m = L.map(el, { scrollWheelZoom: false }), g = L.featureGroup();
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors', maxZoom: 19 }).addTo(m);
      JSON.parse(el.dataset.points).forEach(function (p) {
        L.circleMarker(p.ll, { radius: 9, color: '#111111', weight: 2, fillColor: '#FFFFFF', fillOpacity: 1 })
          .bindPopup('<b>' + p.n + '</b><br>' + p.a + '<br><a href="https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(p.a + ', France') + '" target="_blank" rel="noopener">Directions</a>').addTo(g);
      });
      g.addTo(m); m.fitBounds(g.getBounds().pad(0.15), { maxZoom: 15 });
    });
    document.dispatchEvent(new Event('mt-leaflet'));
  }
  function charger() {
    if (go) return; go = true;
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = CDN + 'css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = CDN + 'js'; s.onload = init; document.head.appendChild(s);
  }
  if (!('IntersectionObserver' in window)) return charger();
  var o = new IntersectionObserver(function (e) { if (e.some(function (x) { return x.isIntersecting; })) { o.disconnect(); charger(); } }, { rootMargin: '400px' });
  c.forEach(function (el) { o.observe(el); });
})();
