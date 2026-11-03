/* Präsenter-Modus: Folien mit Erklärungen direkt an den Begriffen.
   Schrittfolge je Folie: Folie → Einfach gesagt → Begriffe (mit Scheinwerfer) → Aus der Akte → Hinweis → Frage an die Runde → nächste Folie.
   Referentenansicht (zweites Fenster) läuft über BroadcastChannel synchron und zeigt die Sprechernotizen. */
(function () {
  'use strict';
  var FRAMES = JSON.parse(document.getElementById('p-daten').textContent);
  var app = document.getElementById('p-app');
  var KENNUNG = app.getAttribute('data-tag');
  var REF = /[?&]ansicht=referent/.test(location.search);
  var kanal = 'BroadcastChannel' in window ? new BroadcastChannel('praes:' + KENNUNG) : null;
  var f = 0, s = 0, erklaeren = true, start = Date.now();
  function $(q, e) { return (e || document).querySelector(q); }
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function de(n, d) { return Number(n).toLocaleString('de-DE', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }

  /* Schritte einer Folie */
  function schritte(fr) {
    var out = [{ a: 'folie' }];
    if (!erklaeren) return out;
    if (fr.kern) out.push({ a: 'kern' });
    fr.orte.forEach(function (o, i) { out.push({ a: 'ort', i: i }); });
    if (fr.fun) out.push({ a: 'fun' });
    if (fr.hinweis) out.push({ a: 'hinweis' });
    if (fr.frage) out.push({ a: 'frage' });
    return out;
  }
  function melden() { if (kanal) kanal.postMessage({ f: f, s: s, erklaeren: erklaeren }); try { localStorage.setItem('praes:' + KENNUNG, JSON.stringify({ f: f, s: s })); } catch (e) { /* egal */ } if (!REF) try { history.replaceState(null, '', '#' + FRAMES[f].id + (s ? '.' + s : '')); } catch (e) { /* Safari begrenzt sehr schnelle Wechsel */ } }
  function geh(nf, ns, still) {
    f = Math.max(0, Math.min(FRAMES.length - 1, nf));
    var n = schritte(FRAMES[f]).length;
    s = ns === 'ende' ? n - 1 : Math.max(0, Math.min(n - 1, ns || 0));
    malen();
    if (!still) melden();
  }
  function vor() { if (s < schritte(FRAMES[f]).length - 1) geh(f, s + 1); else if (f < FRAMES.length - 1) geh(f + 1, 0); }
  function zurueck() { if (s > 0) geh(f, s - 1); else if (f > 0) geh(f - 1, 'ende'); }

  /* Aufbau Hauptfenster */
  var ui = {};
  function knopf(text, titel, fn, cls) { var b = el('button', 'kn ' + (cls || ''), text); b.type = 'button'; b.title = titel; b.addEventListener('click', fn); return b; }
  function bauen() {
    var leiste = ui.leiste = el('div', 'leiste');
    ui.pos = el('span', 'pos'); ui.ti = el('span', 'ti');
    leiste.appendChild(ui.pos); leiste.appendChild(ui.ti);
    leiste.appendChild(knopf('←', 'Zurück (Pfeil links)', zurueck));
    leiste.appendChild(knopf('Weiter →', 'Weiter (Pfeil rechts, Leertaste)', vor, 'haupt'));
    ui.erk = knopf('Erklärungen', 'Erklärungen ein oder aus (E)', umschalten, 'opt'); ui.erk.setAttribute('aria-pressed', 'true'); leiste.appendChild(ui.erk);
    ui.liveKn = knopf('Live-Rechner', 'Auf der Folie mitmachen (L)', function () { liveUm(); }); leiste.appendChild(ui.liveKn);
    leiste.appendChild(knopf('Übersicht', 'Alle Folien (G)', rasterUm));
    leiste.appendChild(knopf('Referentenansicht', 'Notizen im zweiten Fenster (R)', refOeffnen, 'opt'));
    leiste.appendChild(knopf('Vollbild', 'Vollbild (F)', voll, 'opt'));
    leiste.appendChild(knopf('?', 'Tastenkürzel (H)', hilfeUm));
    var zur = el('a', 'kn', 'Schließen'); zur.href = zurueckAdresse(); leiste.appendChild(zur);
    app.appendChild(leiste);
    var buehne = el('div', 'buehne');
    ui.folie = el('div', 'folie'); ui.img = el('img'); ui.img.alt = ''; ui.folie.appendChild(ui.img);
    ui.marks = el('div'); ui.folie.appendChild(ui.marks);
    ui.spot = el('div', 'spot'); ui.folie.appendChild(ui.spot);
    ui.karte = el('div', 'karte'); ui.karte.setAttribute('aria-live', 'polite'); ui.folie.appendChild(ui.karte);
    ui.band = el('div', 'band'); ui.band.setAttribute('aria-live', 'polite'); ui.folie.appendChild(ui.band);
    ui.live = el('div', 'live'); ui.folie.appendChild(ui.live);
    ui.img.addEventListener('click', function (e) { if (e.detail) vor(); });
    buehne.appendChild(ui.folie); app.appendChild(buehne);
    ui.unter = el('div', 'unter'); app.appendChild(ui.unter);
    ablage();
    tipp();
    var wisch = null;
    ui.folie.addEventListener('touchstart', function (e) { wisch = e.changedTouches[0].clientX; }, { passive: true });
    ui.folie.addEventListener('touchend', function (e) { if (wisch === null) return; var dx = e.changedTouches[0].clientX - wisch; wisch = null; if (Math.abs(dx) > 45) { e.preventDefault(); if (dx < 0) vor(); else zurueck(); } });
    ui.ablauf = el('div', 'ablauf');
    FRAMES.forEach(function (fr, i) {
      var b = el('button', /^e/.test(fr.id) ? 'erinn' : ''); b.type = 'button'; b.title = fr.label + ': ' + fr.titel; b.setAttribute('aria-label', fr.label);
      b.addEventListener('click', function () { geh(i, 0); }); ui.ablauf.appendChild(b);
    });
    app.appendChild(ui.ablauf);
    ui.raster = el('div', 'raster');
    var kopf = el('h2', '', 'Alle Folien'); ui.raster.appendChild(kopf);
    var g = el('div', 'gitter');
    FRAMES.forEach(function (fr, i) {
      var b = el('button'); b.type = 'button'; var im = el('img'); im.loading = 'lazy'; im.src = fr.daumen; im.alt = ''; b.appendChild(im);
      var sp = el('span'); sp.appendChild(el('b', '', fr.label + ' ')); sp.appendChild(document.createTextNode(fr.titel)); b.appendChild(sp);
      b.addEventListener('click', function () { rasterUm(); geh(i, 0); }); g.appendChild(b);
    });
    ui.raster.appendChild(g); document.body.appendChild(ui.raster);
    ui.hilfe = el('div', 'hilfe'); ui.hilfe.innerHTML = '<div><h2>Tastenkürzel</h2><table>' + [['→ Leertaste Bild↓', 'Nächster Schritt (auch Presenter-Clicker)'], ['← Bild↑', 'Zurück'], ['↓ ↑', 'Direkt zur nächsten oder vorigen Folie'], ['E', 'Erklärungen ein oder aus'], ['L', 'Live-Rechner oder Mitmachen auf der Folie'], ['G', 'Übersicht aller Folien'], ['R', 'Referentenansicht mit Notizen'], ['F', 'Vollbild'], ['Esc', 'Erklärung schließen']].map(function (z) { return '<tr><td><kbd>' + z[0] + '</kbd></td><td>' + z[1] + '</td></tr>'; }).join('') + '</table><p style="margin:12px 0 0"><button class="kn haupt" type="button">Alles klar</button></p></div>';
    ui.hilfe.addEventListener('click', function (e) { if (e.target === ui.hilfe || e.target.tagName === 'BUTTON') hilfeUm(); });
    document.body.appendChild(ui.hilfe);
  }
  /* Auf dem Handy stehen Erklärung und Rechner gut lesbar unter der Folie */
  var ENG = window.matchMedia('(max-width:760px)');
  function ablage() {
    var ziel = ENG.matches ? ui.unter : ui.folie;
    [ui.karte, ui.band, ui.live].forEach(function (x) { if (x.parentNode !== ziel) ziel.appendChild(x); });
    if (ui.ablauf) document.documentElement.style.setProperty('--platz', (ui.leiste.offsetHeight + ui.ablauf.offsetHeight + 24) + 'px');
  }
  function tipp() {
    var gesehen = false;
    try { gesehen = !!localStorage.getItem('praes:tipp'); localStorage.setItem('praes:tipp', '1'); } catch (e) { /* egal */ }
    if (gesehen || location.hash) return;
    var t = el('div', 'tipp', '→ oder Klicker: nächster Schritt · E Erklärungen · L Mitmachen · R Notizen · ? Hilfe');
    ui.folie.appendChild(t);
    setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 7000);
  }
  function zurueckAdresse() {
    var p = ''; try { p = JSON.parse(localStorage.getItem('kurs:v1:person') || '""'); } catch (e) { /* egal */ }
    return p ? '/hefte/' + p + '/' + KENNUNG + '/' : '/hefte/';
  }

  /* Darstellung */
  function malen() {
    ablage();
    var fr = FRAMES[f], sch = schritte(fr), akt = sch[s] || sch[0];
    ui.pos.textContent = fr.label; ui.ti.textContent = fr.titel;
    if (ui.img.getAttribute('src') !== fr.bild) { ui.img.src = fr.bild; ui.img.classList.remove('wechsel'); void ui.img.offsetWidth; ui.img.classList.add('wechsel'); marks(fr); if (ui.live.classList.contains('an')) liveZu(); }
    Array.prototype.forEach.call(ui.marks.children, function (m, i) { m.classList.toggle('aktiv', akt.a === 'ort' && akt.i === i); });
    Array.prototype.forEach.call(ui.ablauf.children, function (b, i) { b.classList.toggle('fertig', i < f); b.classList.toggle('jetzt', i === f); });
    ui.liveKn.hidden = !fr.live; ui.liveKn.textContent = fr.liveName || 'Live-Rechner';
    ui.spot.classList.remove('an'); ui.karte.classList.remove('an'); ui.band.classList.remove('an', 'fr', 'hi', 'fu');
    if (akt.a === 'kern') band('Einfach gesagt', fr.kern, '');
    if (akt.a === 'fun') band('Aus der Akte', fr.fun, 'fu');
    if (akt.a === 'hinweis') band('Wichtig', fr.hinweis, 'hi');
    if (akt.a === 'frage') band('Frage an die Runde', fr.frage, 'fr');
    if (akt.a === 'ort') scheinwerfer(fr, akt.i);
    var vor = new Image(); if (FRAMES[f + 1]) vor.src = FRAMES[f + 1].bild;
  }
  function band(titel, text, cls) {
    ui.band.className = 'band an ' + cls; ui.band.innerHTML = '';
    ui.band.appendChild(el('b', '', titel)); ui.band.appendChild(document.createTextNode(text));
  }
  function marks(fr) {
    ui.marks.innerHTML = '';
    document.body.classList.toggle('aus', !erklaeren);
    fr.orte.forEach(function (o, i) {
      var m = el('button', 'mark neu'); m.type = 'button'; m.setAttribute('aria-label', 'Erklärung: ' + o.t);
      m.style.cssText = 'left:' + (o.x - .3) + '%;top:' + (o.y - .3) + '%;width:' + (o.w + .6) + '%;height:' + (o.h + .6) + '%';
      m.appendChild(el('i', '', String(i + 1)));
      m.addEventListener('click', function () { var idx = schritte(fr).findIndex(function (x) { return x.a === 'ort' && x.i === i; }); if (idx >= 0) geh(f, idx); });
      ui.marks.appendChild(m);
    });
  }
  function scheinwerfer(fr, i) {
    var o = fr.orte[i], pad = .5;
    ui.spot.style.left = (o.x - pad) + '%'; ui.spot.style.top = (o.y - pad) + '%';
    ui.spot.style.width = (o.w + pad * 2) + '%'; ui.spot.style.height = (o.h + pad * 2) + '%';
    ui.spot.classList.add('an');
    var k = ui.karte; k.innerHTML = '';
    k.appendChild(el('div', 'nr', 'Begriff ' + (i + 1) + ' von ' + fr.orte.length));
    k.appendChild(el('h3', '', o.t)); k.appendChild(el('p', '', o.e));
    if (o.b) { var b = el('div', 'bsp'); b.appendChild(el('b', '', 'Zum Beispiel')); b.appendChild(document.createTextNode(o.b)); k.appendChild(b); }
    // Karte frisch einblenden und neben den Begriff setzen
    k.classList.remove('an'); void k.offsetWidth; k.classList.add('an');
    if (ENG.matches) { k.style.left = k.style.top = ''; return; }
    var fw = ui.folie.clientWidth, fh = ui.folie.clientHeight, kw = k.offsetWidth, kh = k.offsetHeight, rand = fw * .012;
    var ox = o.x / 100 * fw, oy = o.y / 100 * fh, ow = o.w / 100 * fw, oh = o.h / 100 * fh;
    var unten = oy + oh + rand + kh + rand <= fh, oben = oy - rand - kh >= rand;
    var y = unten ? oy + oh + rand * 1.2 : oben ? oy - kh - rand * 1.2 : Math.max(rand, Math.min(fh - kh - rand, oy + oh / 2 - kh / 2));
    var x = Math.max(rand, Math.min(fw - kw - rand, ox + ow / 2 - kw / 2));
    if (!unten && !oben) x = ox + ow + rand + kw <= fw ? ox + ow + rand : Math.max(rand, ox - kw - rand);
    k.style.left = x + 'px'; k.style.top = y + 'px';
  }

  /* Live-Rechner */
  var BC = { a: 70, l: 300, i: 12000 }, SC = { n: 4, d: 4, e: 3, r: 4 };
  function regler(box, name, text, min, max, step, wert, einheit, fn) {
    var l = el('label'); l.appendChild(el('span', '', text)); var o = el('output'); l.appendChild(o);
    var r = el('input'); r.type = 'range'; r.min = min; r.max = max; r.step = step; r.value = wert;
    function zeigen() { o.textContent = de(r.value, step < 1 ? 1 : 0) + einheit; } zeigen();
    r.addEventListener('input', function () { zeigen(); fn(name, +r.value); }); r.addEventListener('keydown', function (e) { e.stopPropagation(); });
    l.appendChild(r); box.appendChild(l);
  }
  function erg(box, w, t, cls) { var d = el('div', cls || ''); d.appendChild(el('b', '', w)); d.appendChild(el('span', '', t)); box.appendChild(d); }
  function liveBc() {
    var L = ui.live; L.innerHTML = ''; L.appendChild(el('h3', '', 'Live: Was passiert, wenn …?'));
    var aus = el('div', 'erg');
    function rechne() {
      var h = Math.round(800 * BC.a / 100 * 3.5 / 60), br = h * 45, ne = br - BC.l, am = ne > 0 ? BC.i / ne : null;
      aus.innerHTML = '';
      erg(aus, am ? 'rund ' + de(am) + ' Monate' : 'nie', 'Amortisation', 'gross ' + (am && am <= 24 ? '' : 'warn'));
      erg(aus, de(h) + ' Std.', 'Ersparnis / Monat'); erg(aus, de(br) + ' €', 'Bruttonutzen'); erg(aus, de(ne) + ' €', 'Nettonutzen'); erg(aus, de((ne * 12 - BC.i) / BC.i * 100, 1) + ' %', 'ROI nach 12 Monaten');
      erg(aus, de((ne * 36 - BC.i) / BC.i * 100, 1) + ' %', 'ROI nach 36 Monaten'); erg(aus, de(BC.i + BC.l * 36) + ' €', 'TCO über 3 Jahre');
    }
    function set(n, v) { BC[n] = v; rechne(); }
    regler(L, 'a', 'Automatisierbarer Anteil', 0, 100, 5, BC.a, ' %', set);
    regler(L, 'l', 'Laufende Kosten / Monat', 0, 1500, 50, BC.l, ' €', set);
    regler(L, 'i', 'Investition', 2000, 40000, 1000, BC.i, ' €', set);
    L.appendChild(aus); rechne();
    L.appendChild(el('p', '', 'Basis: 800 Vorgänge, 3,5 Min. gespart, 45 € Stundensatz.'));
  }
  function liveScoring() {
    var L = ui.live; L.innerHTML = ''; L.appendChild(el('h3', '', 'Live: Punkte vergeben'));
    var aus = el('div', 'erg');
    function rechne() {
      var t = SC.n * .4 + SC.d * .25 + SC.e * .2 + SC.r * .15, w = SC.n + SC.d, a = 12 - SC.e - SC.r;
      var feld = w >= 7 ? (a <= 5 ? 'Sofort starten' : 'Planen, in Etappen') : (a <= 5 ? 'Nebenbei' : 'Streichen');
      aus.innerHTML = '';
      erg(aus, feld, 'Feld in der Matrix', 'gross');
      erg(aus, de(t, 2), 'Gewichtete Punktzahl'); erg(aus, w + ' / ' + a, 'Wert / Aufwand');
    }
    function set(n, v) { SC[n] = v; rechne(); }
    regler(L, 'n', 'Nutzen (40 %)', 1, 5, 1, SC.n, '', set); regler(L, 'd', 'Datenverfügbarkeit (25 %)', 1, 5, 1, SC.d, '', set);
    regler(L, 'e', 'Einfachheit (20 %)', 1, 5, 1, SC.e, '', set); regler(L, 'r', 'Risikoarmut (15 %)', 1, 5, 1, SC.r, '', set);
    L.appendChild(aus); rechne();
  }
  /* Mitmachen auf der Folie: Daten kommen aus dem Bau (fr.liveDaten) */
  function liveSpiel(fr) {
    var d = fr.liveDaten, L = ui.live, i = 0, ok = 0, n = d.karten.length;
    L.innerHTML = ''; L.appendChild(el('h3', '', d.titel));
    var feld = el('div'); L.appendChild(feld);
    function zeigen() {
      feld.innerHTML = '';
      if (i >= n) {
        var rang = d.raenge.filter(function (r) { return ok / n >= r[0]; })[0];
        feld.appendChild(el('p', 'sp-erg', ok + ' von ' + n + ' richtig')); feld.appendChild(el('p', 'sp-rang', 'Dienstgrad der Runde: ' + rang[1]));
        feld.appendChild(knopf('Nochmal', '', function () { i = 0; ok = 0; zeigen(); }));
        return;
      }
      var k = d.karten[i], opts = el('div', 'sp-opt');
      feld.appendChild(el('p', 'sp-z', 'Karte ' + (i + 1) + ' von ' + n + ': erst abstimmen, dann klicken')); feld.appendChild(el('p', 'sp-t', k.t));
      (k.o || d.optionen).forEach(function (o) {
        var b = knopf(o, 'Antwort wählen', function () {
          var tr = o === k.r; if (tr) ok++;
          Array.prototype.forEach.call(opts.children, function (x) { x.disabled = true; if (x.textContent === k.r) x.classList.add('richtig'); });
          if (!tr) b.classList.add('falsch');
          feld.appendChild(el('p', 'sp-w', k.w));
          var nx = knopf(i + 1 < n ? 'Nächste Karte →' : 'Auswertung →', '', function () { i++; zeigen(); }, 'haupt'); feld.appendChild(nx); nx.focus({ preventScroll: true });
        }, 'sp-b');
        opts.appendChild(b);
      });
      feld.appendChild(opts);
    }
    zeigen();
  }
  var BINGO_AN = [], LINIEN = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  function liveBingo(fr) {
    var L = ui.live; L.innerHTML = ''; L.appendChild(el('h3', '', 'Alarmsatz-Bingo der Runde'));
    var g = el('div', 'lv-bingo'), info = el('p', 'sp-w', 'Sobald jemand einen Satz sagt: antippen.');
    fr.liveDaten.forEach(function (d, i) {
      var b = knopf((d.f ? '★ ' : '') + d.a, 'Satz markieren', function () {
        var p = BINGO_AN.indexOf(i); if (p >= 0) BINGO_AN.splice(p, 1); else BINGO_AN.push(i);
        b.setAttribute('aria-pressed', String(p < 0));
        var bingo = LINIEN.some(function (l) { return l.indexOf(i) >= 0 && l.every(function (x) { return BINGO_AN.indexOf(x) >= 0; }); });
        info.textContent = p >= 0 ? 'Zurückgenommen.' : (bingo ? 'BINGO! ' : '') + 'Rückfrage: ' + d.b;
      }, 'lv-z');
      b.setAttribute('aria-pressed', String(BINGO_AN.indexOf(i) >= 0));
      g.appendChild(b);
    });
    L.appendChild(g); L.appendChild(info);
    L.appendChild(knopf('Neue Runde', '', function () { BINGO_AN = []; liveBingo(fr); }));
  }
  var BH = { a: 12, w1: 1.5, w2: 2, w3: .5, w4: 1 };
  function liveBahnen() {
    var L = ui.live; L.innerHTML = ''; L.appendChild(el('h3', '', 'Live: Wo sind die Tage hin?'));
    var aus = el('div', 'erg');
    function rechne() {
      var w = BH.w1 + BH.w2 + BH.w3 + BH.w4, t = w + BH.a / 480;
      aus.innerHTML = '';
      erg(aus, de(t, 1) + ' Tage', 'Durchlaufzeit', 'gross warn');
      erg(aus, de(BH.a) + ' Min.', 'Bearbeitungszeit');
      erg(aus, BH.a && w ? '1 zu ' + de(w * 480 / BH.a) : '–', 'Arbeit zu Warten (8-Stunden-Tag)');
    }
    function set(n, v) { BH[n] = v; rechne(); }
    regler(L, 'a', 'Arbeit, gesamt', 0, 12, 1, BH.a, ' Min.', set);
    regler(L, 'w1', 'Warten: zur Buchhaltung', 0, 5, .5, BH.w1, ' Tage', set);
    regler(L, 'w2', 'Warten: zur Fachabteilung', 0, 5, .5, BH.w2, ' Tage', set);
    regler(L, 'w3', 'Warten: zur Teamleitung', 0, 5, .5, BH.w3, ' Tage', set);
    regler(L, 'w4', 'Warten: zurück zur Buchhaltung', 0, 5, .5, BH.w4, ' Tage', set);
    L.appendChild(aus); rechne();
    L.appendChild(el('p', '', 'Zieh die Arbeit auf 0: Die Tage bleiben. Zieh eine Übergabe auf 0: Die Tage schmelzen.'));
  }
  function liveZiel(fr) {
    var L = ui.live, B = fr.liveDaten.bausteine, an = B.map(function () { return true; }); L.innerHTML = ''; L.appendChild(el('h3', '', 'Was passiert ohne diesen Baustein?'));
    var knoepfe = el('div', 'sp-opt'), satz = el('p', 'lv-satz'), info = el('p', 'sp-w');
    function zeigen() {
      satz.textContent = '';
      B.forEach(function (x, i) { var t = (i >= 3 ? ', ' : i ? ' ' : '') + x[1]; if (an[i]) satz.appendChild(document.createTextNode(t)); else satz.appendChild(el('s', '', t)); });
      satz.appendChild(document.createTextNode('.'));
      var weg = B.filter(function (x, i) { return !an[i]; });
      info.textContent = weg.length ? weg[weg.length - 1][2] : 'Alle fünf da: Das lässt sich in sechs Monaten prüfen.';
    }
    B.forEach(function (x, i) {
      var b = knopf(x[0], 'Baustein ein oder aus', function () { an[i] = !an[i]; b.setAttribute('aria-pressed', String(an[i])); zeigen(); }, 'sp-b');
      b.setAttribute('aria-pressed', 'true'); knoepfe.appendChild(b);
    });
    L.appendChild(knoepfe); L.appendChild(satz); L.appendChild(info); zeigen();
  }
  var AUFW = { b: 5000 };
  function liveAufwand() {
    var L = ui.live; L.innerHTML = ''; L.appendChild(el('h3', '', 'Live: Was kostet es wirklich?'));
    var aus = el('div', 'erg');
    function rechne() {
      var von = AUFW.b / .3, bis = AUFW.b / .2;
      aus.innerHTML = '';
      erg(aus, 'rund ' + de(Math.round(von / 1000) * 1000) + ' bis ' + de(Math.round(bis / 1000) * 1000) + ' €', 'Gesamtaufwand, wenn der Bau 20–30 % ist', 'gross warn');
      erg(aus, de(Math.round((von - AUFW.b) / 1000) * 1000) + ' €', 'mindestens nicht im Angebot'); erg(aus, de(Math.round((bis - AUFW.b) / 1000) * 1000) + ' €', 'höchstens nicht im Angebot');
    }
    regler(L, 'b', 'Preis im Angebot, nur der Bau', 1000, 40000, 500, AUFW.b, ' €', function (n, v) { AUFW.b = v; rechne(); });
    L.appendChild(aus); rechne();
    L.appendChild(el('p', '', 'Grobe Rechnung mit den Anteilen von Folie 36.'));
  }
  function liveZu() { ui.live.classList.remove('an', 'breit'); ui.liveKn.setAttribute('aria-pressed', 'false'); }
  function liveUm() {
    var fr = FRAMES[f];
    if (!fr.live) return;
    if (ui.live.classList.contains('an')) return liveZu();
    var tools = { bc: liveBc, scoring: liveScoring, spiel: liveSpiel, bingo: liveBingo, bahnen: liveBahnen, ziel: liveZiel, aufwand: liveAufwand };
    tools[fr.live](fr);
    if (fr.live === 'spiel' || fr.live === 'ziel' || fr.live === 'bingo') ui.live.classList.add('breit');
    ui.live.classList.add('an'); ui.liveKn.setAttribute('aria-pressed', 'true');
  }

  /* Steuerung */
  function umschalten() { erklaeren = !erklaeren; ui.erk.setAttribute('aria-pressed', String(erklaeren)); document.body.classList.toggle('aus', !erklaeren); geh(f, 0); }
  function rasterUm() { ui.raster.classList.toggle('an'); }
  function hilfeUm() { ui.hilfe.classList.toggle('an'); }
  function voll() { if (document.fullscreenElement) document.exitFullscreen(); else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(function () {}); }
  function refOeffnen() { window.open(location.pathname + '?ansicht=referent', 'praes-referent', 'width=1100,height=760'); setTimeout(melden, 900); }
  var idle;
  function wachheit() { document.body.classList.add('zeigen'); clearTimeout(idle); idle = setTimeout(function () { document.body.classList.remove('zeigen'); }, 2200); }
  function tasten(e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if ((k === ' ' || k === 'Enter') && e.target.closest && e.target.closest('.live')) return;
    if (k === 'Escape') { if (ui.hilfe && ui.hilfe.classList.contains('an')) return hilfeUm(); if (ui.raster && ui.raster.classList.contains('an')) return rasterUm(); if (ui.live && ui.live.classList.contains('an')) return liveZu(); if (s) geh(f, 0); return; }
    if (k === 'ArrowRight' || k === ' ' || k === 'PageDown' || k === 'Enter') { e.preventDefault(); vor(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); zurueck(); }
    else if (k === 'ArrowDown') { e.preventDefault(); geh(f + 1, 0); } else if (k === 'ArrowUp') { e.preventDefault(); geh(f - 1, 0); }
    else if (k === 'Home') geh(0, 0); else if (k === 'End') geh(FRAMES.length - 1, 0);
    else if (/^[eE]$/.test(k) && ui.erk) umschalten(); else if (/^[lL]$/.test(k) && ui.live) liveUm(); else if (/^[gG]$/.test(k) && ui.raster) rasterUm();
    else if (/^[rR]$/.test(k) && !REF) refOeffnen(); else if (/^[fF]$/.test(k)) voll(); else if ((/^[hH?]$/).test(k) && ui.hilfe) hilfeUm();
  }

  /* Referentenansicht */
  function refBauen() {
    document.body.classList.add('ref');
    var kopf = el('div', 'leiste');
    ui.pos = el('span', 'pos'); ui.ti = el('span', 'ti'); ui.uhr = el('span', 'ref-uhr', '0:00');
    kopf.appendChild(ui.pos); kopf.appendChild(ui.ti); kopf.appendChild(ui.uhr);
    kopf.appendChild(knopf('←', 'Zurück', zurueck)); kopf.appendChild(knopf('Weiter →', 'Weiter', vor, 'haupt'));
    app.appendChild(kopf);
    var r = el('div', 'ref-raster'), li = el('div'), re = el('div');
    ui.schritt = el('div', 'ref-box'); ui.schritt.appendChild(el('h3', '', 'Gerade auf der Folie')); ui.schrittText = el('p'); ui.schritt.appendChild(ui.schrittText);
    var nz = el('div', 'ref-box ref-notiz'); nz.appendChild(el('h3', '', 'Sprechernotiz')); ui.notiz = el('p'); nz.appendChild(ui.notiz);
    var kl = el('div', 'ref-box'); kl.appendChild(el('h3', '', 'Jetzt und danach')); var g = el('div', 'ref-kl'); ui.jetzt = el('img'); ui.nach = el('img'); ui.jetzt.alt = ''; ui.nach.alt = ''; g.appendChild(ui.jetzt); g.appendChild(ui.nach); kl.appendChild(g);
    li.appendChild(ui.schritt); li.appendChild(nz); li.appendChild(kl);
    var ab = el('div', 'ref-box'); ab.appendChild(el('h3', '', 'Ablauf dieser Folie')); ui.liste = el('ol', 'ref-liste'); ab.appendChild(ui.liste); re.appendChild(ab);
    r.appendChild(li); r.appendChild(re); app.appendChild(r);
    setInterval(function () { var m = Math.floor((Date.now() - start) / 1000); ui.uhr.textContent = Math.floor(m / 60) + ':' + ('0' + (m % 60)).slice(-2); }, 1000);
    malen = refMalen;
  }
  function textVon(fr, st) { return st.a === 'folie' ? 'Nur die Folie' : st.a === 'kern' ? 'Einfach gesagt: ' + fr.kern : st.a === 'fun' ? 'Aus der Akte: ' + fr.fun : st.a === 'hinweis' ? 'Wichtig: ' + fr.hinweis : st.a === 'frage' ? 'Frage an die Runde: ' + fr.frage : fr.orte[st.i].t + ': ' + fr.orte[st.i].e + (fr.orte[st.i].b ? ' Zum Beispiel: ' + fr.orte[st.i].b : ''); }
  function refMalen() {
    var fr = FRAMES[f], sch = schritte(fr);
    ui.pos.textContent = fr.label; ui.ti.textContent = fr.titel; ui.notiz.textContent = fr.notiz || 'Keine Notiz zu dieser Folie.';
    ui.schrittText.textContent = textVon(fr, sch[s] || sch[0]);
    ui.jetzt.src = fr.daumen; ui.nach.src = (FRAMES[f + 1] || fr).daumen;
    ui.liste.innerHTML = '';
    sch.forEach(function (st, i) {
      var li = el('li'), b = el('button', '', st.a === 'ort' ? (st.i + 1) + '. ' + fr.orte[st.i].t : st.a === 'folie' ? 'Folie' : st.a === 'kern' ? 'Einfach gesagt' : st.a === 'fun' ? 'Aus der Akte' : st.a === 'hinweis' ? 'Wichtig' : 'Frage an die Runde');
      b.type = 'button'; if (i === s) b.setAttribute('aria-current', 'true');
      b.addEventListener('click', function () { geh(f, i); }); li.appendChild(b); ui.liste.appendChild(li);
    });
  }

  /* Start */
  function startPos() {
    var m = /^#(e?\d+)(?:\.(\d+))?$/.exec(location.hash);
    if (m) { var i = FRAMES.findIndex(function (x) { return x.id === m[1]; }); if (i >= 0) return [i, +(m[2] || 0)]; }
    try { var g = JSON.parse(localStorage.getItem('praes:' + KENNUNG)); if (g && REF) return [g.f, g.s]; } catch (e) { /* egal */ }
    return [0, 0];
  }
  if (REF) refBauen(); else bauen();
  document.addEventListener('keydown', tasten);
  if (!REF) {
    document.addEventListener('mousemove', wachheit);
    document.addEventListener('fullscreenchange', function () { document.body.classList.toggle('voll', !!document.fullscreenElement); setTimeout(malen, 120); });
    window.addEventListener('resize', function () { malen(); });
    window.addEventListener('hashchange', function () { var p = startPos(); if (p[0] !== f || p[1] !== s) geh(p[0], p[1], true); });
  }
  if (kanal) kanal.onmessage = function (e) { var d = e.data; if (typeof d.erklaeren === 'boolean' && d.erklaeren !== erklaeren) { erklaeren = d.erklaeren; if (ui.erk) { ui.erk.setAttribute('aria-pressed', String(erklaeren)); document.body.classList.toggle('aus', !erklaeren); } } geh(d.f, d.s, true); };
  var p = startPos();
  geh(p[0], p[1], true);
  window.PRAES = { frames: FRAMES, pos: function () { return [f, s]; }, geh: geh, vor: vor };
})();
