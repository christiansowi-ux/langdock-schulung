/* Weiterleitung alter Adressen: Ziel aus data-weiter, Parameter und Sprungmarke bleiben erhalten. */
(function () {
  var t = document.body && document.body.getAttribute('data-weiter');
  if (t) location.replace(t + location.search + location.hash);
})();
