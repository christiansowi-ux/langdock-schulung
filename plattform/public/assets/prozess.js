/* Modul 2 · Tag 7: Tatort Prozess. Stand von Montag, Mini-Spiele, Alarmsatz-Bingo, Interview-Mitschrift, SIPOC, Bahnen mit Skizze, SOP, Zielsatz, Scope, Kriterien, Akte.
   Felder mit data-save speichert wochenheft.js (kurs:m2w1:<person>:<feld>). Zeilen, die sich ändern (Mitschrift, Bahnen, SOP), speichert diese Datei selbst unter demselben Präfix.
   Verhältnis Arbeit zu Warten: Arbeitstag = 8 Stunden, wie im Lernheft angegeben. */
(function () {
  'use strict';
  var PERSON = document.documentElement.getAttribute('data-person') || 'gast';
  var PREFIX = 'kurs:m2w1:' + PERSON + ':';
  var ARBEITSTAG = 480;
  function $(s, e) { return (e || document).querySelector(s); }
  function $$(s, e) { return Array.prototype.slice.call((e || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function get(k, def) { try { var v = localStorage.getItem(PREFIX + k); return v === null ? def : JSON.parse(v); } catch (e) { return def; } }
  function set(k, v) { try { localStorage.setItem(PREFIX + k, JSON.stringify(v)); } catch (e) { /* Speichern gesperrt: Export bleibt möglich */ } }
  function num(v) { var n = parseFloat(String(v == null ? '' : v).replace(',', '.')); return isFinite(n) ? n : 0; }
  function de(n, d) { return Number(n).toLocaleString('de-DE', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function setVal(f, v) { f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }
  function val(k) { var f = $('[data-save="' + k + '"]'); return f ? (f.type === 'checkbox' ? f.checked : f.value) : get(k, ''); }
  function tage(n) { return de(n, n % 1 ? 1 : 0) + (n === 1 ? ' Tag' : ' Tage'); }
  function knopf(text, cls, fn) { var b = el('button', cls, text); b.type = 'button'; b.addEventListener('click', fn); return b; }
  function belegt(frage, hat) { return !hat || window.confirm(frage); }

  function konfetti() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var box = el('div', 'konfetti'), farben = ['#05dbba', '#05614c', '#f6cf09', '#0d0d0d', '#c7e5dc'];
    box.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 46; i++) {
      var s = el('i');
      s.style.left = (Math.random() * 100) + '%'; s.style.background = farben[i % farben.length];
      s.style.animationDelay = (Math.random() * .35) + 's'; s.style.animationDuration = (1 + Math.random() * .9) + 's';
      box.appendChild(s);
    }
    document.body.appendChild(box);
    setTimeout(function () { box.remove(); }, 2400);
  }

  function stand(name, ok, text) {
    $$('[data-stand="' + name + '"]').forEach(function (p) {
      p.textContent = text; p.className = 'stand ' + (ok ? 'ok' : '');
      if (ok) p.appendChild(el('span', 'stempel', 'Geprüft'));
    });
  }

  /* ---------- Alarmsätze: gleiche Rückfragen wie auf Folie 16, dazu „wir“ und „man“ aus Folie 14 ---------- */
  var ALARM = [
    [/normalerweise|in der regel|meistens|grundsätzlich/i, '„normalerweise“', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?'],
    [/sieht man|merkt man|erkennt man/i, '„das sieht man“', 'Woran genau? Nenne mir drei Merkmale.'],
    [/macht (die|der|das) |die kollegin|der kollege/i, '„das macht die Kollegin“', 'Nach welchen Kriterien? Was passiert im Urlaub?'],
    [/eigentlich|immer gleich/i, '„eigentlich immer gleich“', 'Zeig mir die letzten fünf Fälle.'],
    [/(^|[\s,.])(wir|man)($|[\s,.])/i, '„wir“ oder „man“', 'Wer genau?']
  ];
  function alarme(zeilen, liste) {
    if (!liste) return;
    liste.innerHTML = '';
    zeilen.forEach(function (t, i) {
      ALARM.forEach(function (a) {
        if (!a[0].test(t)) return;
        var li = el('li');
        li.appendChild(el('b', '', 'Alarm in Zeile ' + (i + 1) + ': ' + a[1] + '. '));
        li.appendChild(document.createTextNode('Frag nach: ' + a[2]));
        liste.appendChild(li);
      });
    });
  }

  /* ---------- Stand von Montag ---------- */
  function montag() {
    var box = $('[data-tool="montag"] .ft-liste'); if (!box) return;
    box.innerHTML = '';
    var h = get('haupt', ''), name = h ? (get('bw' + h + '-name', '') || 'Kandidat ' + h) : '';
    function karte(t, x) { var k = el('div', 'ft-karte'); k.appendChild(el('b', '', t)); k.appendChild(el('span', '', x)); box.appendChild(k); }
    var v = num(get('bc-volumen', '')), m = num(get('bc-zeit', '')), a = num(get('bc-anteil', '')), r = num(get('bc-rest', '')), s = num(get('bc-satz', '')), f = num(get('bc-fehler', ''));
    var inv = 0, lauf = 0, i;
    for (i = 1; i <= 7; i++) inv += num(get('bc-e' + i, ''));
    for (i = 1; i <= 6; i++) lauf += num(get('bc-l' + i, ''));
    var netto = Math.round(v * a / 100 * Math.max(m - r, 0) / 60) * s + f - lauf;
    var wahl = get('ent-wahl', '');
    if (name) karte(name, 'dein Haupt-Use-Case');
    if (wahl) karte(wahl, 'deine Empfehlung');
    if (v && s) karte(netto > 0 ? 'rund ' + de(inv / netto) + ' Monate' : 'nie', 'Amortisation deiner Rechnung');
    if (!name && !wahl && !(v && s)) {
      var p = el('p', '', 'In diesem Browser ist vom Montag noch nichts gespeichert. Trage es im Rechen-Labor von Tag 6 nach oder nimm eines der Beispiele aus diesem Heft.');
      var l = el('a', '', ' Zum Rechen-Labor →'); l.href = '/hefte/' + PERSON + '/modul-2/tag-6/#labor'; p.appendChild(l);
      box.appendChild(p);
    }
  }

  /* ---------- Mini-Spiele ---------- */
  function spiel(box) {
    var d = JSON.parse($('.sp-daten', box).textContent), feld = $('.sp-feld', box), id = box.getAttribute('data-spiel'), i = 0, ok = 0, n = d.karten.length;
    function start() { i = 0; ok = 0; zeigen(); }
    function ende() {
      feld.innerHTML = '';
      var q = ok / n, rang = d.raenge.filter(function (r) { return q >= r[0]; })[0];
      var bester = Math.max(get('t7-spiel-' + id, 0), ok);
      set('t7-spiel-' + id, bester);
      feld.appendChild(el('p', 'sp-erg', ok + ' von ' + n + ' richtig'));
      feld.appendChild(el('p', 'sp-rang', 'Dienstgrad: ' + rang[1]));
      feld.appendChild(el('p', '', rang[2]));
      if (bester > ok) feld.appendChild(el('p', 'sp-z', 'Dein Bestwert: ' + bester + ' von ' + n));
      feld.appendChild(knopf('Nochmal spielen', 'btn', start));
      if (ok === n) konfetti();
      alles();
    }
    function zeigen() {
      feld.innerHTML = '';
      if (i >= n) return ende();
      var k = d.karten[i], opts = el('div', 'sp-opt'), weiter = el('div', 'sp-weiter');
      feld.appendChild(el('p', 'sp-z', 'Karte ' + (i + 1) + ' von ' + n + ' · ' + ok + ' richtig'));
      feld.appendChild(el('p', 'sp-t', k.t));
      (k.o || d.optionen).forEach(function (o) {
        opts.appendChild(knopf(o, 'sp-b', function (ev) {
          var treffer = o === k.r;
          if (treffer) ok++;
          $$('.sp-b', opts).forEach(function (b) { b.disabled = true; if (b.textContent === k.r) b.classList.add('richtig'); });
          if (!treffer) ev.currentTarget.classList.add('falsch');
          weiter.appendChild(el('p', 'sp-w ' + (treffer ? 'ok' : 'warn'), (treffer ? 'Richtig. ' : 'Nicht ganz. ') + k.w));
          var n2 = knopf(i + 1 < n ? 'Nächste Karte →' : 'Auswertung →', 'btn primary', function () { i++; zeigen(); });
          weiter.appendChild(n2); n2.focus({ preventScroll: true });
        }));
      });
      feld.appendChild(opts); feld.appendChild(weiter);
    }
    start();
  }

  /* ---------- Alarmsatz-Bingo ---------- */
  var LINIEN = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  function bingoMalen() {
    var an = get('t7-bingo', []);
    $$('[data-tool="bingo"]').forEach(function (tool) {
      var daten = JSON.parse($('.bg-daten', tool).textContent), feld = $('[data-bingo]', tool);
      feld.innerHTML = '';
      daten.forEach(function (d, i) {
        var b = knopf((d.f ? '★ ' : '') + d.a, 'bg-z', function () {
          var aktuell = get('t7-bingo', []), pos = aktuell.indexOf(i), vorher = linien(aktuell);
          if (pos >= 0) aktuell.splice(pos, 1); else aktuell.push(i);
          set('t7-bingo', aktuell);
          bingoMalen();
          $$('[data-tool="bingo"] .bg-frage').forEach(function (p) { p.textContent = pos >= 0 ? 'Zurückgenommen.' : 'Rückfrage: ' + d.b; });
          if (linien(aktuell) > vorher) { $$('[data-tool="bingo"] .bg-frage').forEach(function (p) { p.textContent = 'BINGO! Drei Alarmsätze in einer Reihe. Rückfrage zum letzten: ' + d.b; }); konfetti(); }
        });
        b.setAttribute('aria-pressed', String(an.indexOf(i) >= 0));
        feld.appendChild(b);
      });
    });
  }
  function linien(an) { return LINIEN.filter(function (l) { return l.every(function (x) { return an.indexOf(x) >= 0; }); }).length; }

  /* ---------- Stoppuhr ---------- */
  function uhr(box) {
    var gesamt = +box.getAttribute('data-uhr') * 60, rest = gesamt, t = null, z = $('.uhr-z', box), info = $('.uhr-t', box), los = $('[data-uhr-los]', box);
    function zeigen() { z.textContent = Math.floor(rest / 60) + ':' + ('0' + (rest % 60)).slice(-2); }
    function halt() { clearInterval(t); t = null; los.textContent = 'Weiter'; }
    los.addEventListener('click', function () {
      if (t) return halt();
      if (!rest) rest = gesamt;
      info.textContent = ''; box.classList.remove('uhr-ende');
      los.textContent = 'Pause';
      t = setInterval(function () {
        rest--; zeigen();
        if (rest <= 0) { halt(); los.textContent = 'Nochmal'; box.classList.add('uhr-ende'); info.textContent = box.getAttribute('data-uhr-text'); }
      }, 1000);
    });
    $('[data-uhr-neu]', box).addEventListener('click', function () { clearInterval(t); t = null; rest = gesamt; los.textContent = 'Start'; info.textContent = ''; box.classList.remove('uhr-ende'); zeigen(); });
  }

  /* ---------- Interview-Mitschrift ---------- */
  var runde = 1;
  function msDaten() { var d = get('t7-ms', null); return d && d[1] ? d : { 1: { fall: '', z: [] }, 2: { fall: '', z: [] } }; }
  var MS_BSP = { fall: 'Rechnung 0815 vom Büromaterial-Lieferanten, gestern', z: [
    { h: 'Mail öffnen und Rechnung sichten', s: 'Mailprogramm', e: 'Ist das überhaupt eine Rechnung für uns?' },
    { h: 'Betrag und Lieferant prüfen', s: 'Buchhaltungssoftware', e: 'Passt der Lieferant? Das sieht man dann schon.' },
    { h: 'An die Fachabteilung weiterleiten', s: 'Mailprogramm', e: 'Wer ist zuständig? Normalerweise Alex.' },
    { h: 'Freigabe eintragen, wenn sie zurückkommt', s: 'Buchhaltungssoftware', e: 'Fehlt was? Dann fragen wir nach.' }] };
  function msMalen() {
    var tool = $('[data-tool="mitschrift"]'); if (!tool) return;
    var d = msDaten(), r = d[runde], box = $('.ms-zeilen', tool), fall = $('[data-ms-fall]', tool);
    while (r.z.length < 3) r.z.push({ h: '', s: '', e: '' });
    fall.value = r.fall || '';
    box.innerHTML = '';
    r.z.forEach(function (z, i) {
      var zeile = el('div', 'ms-zeile');
      [['h', 'Handlung'], ['s', 'System'], ['e', 'Entscheidung']].forEach(function (f) {
        var inp = el('input'); inp.type = 'text'; inp.value = z[f[0]] || ''; inp.placeholder = f[1]; inp.setAttribute('aria-label', f[1] + ', Zeile ' + (i + 1));
        inp.addEventListener('input', function () { var aktuell = msDaten(); aktuell[runde].z[i] = aktuell[runde].z[i] || { h: '', s: '', e: '' }; aktuell[runde].z[i][f[0]] = inp.value; set('t7-ms', aktuell); msAlarm(); alles(); });
        zeile.appendChild(inp);
      });
      zeile.appendChild(knopf('×', 'zeile-weg', function () { var a = msDaten(); while (a[runde].z.length < r.z.length) a[runde].z.push({ h: '', s: '', e: '' }); a[runde].z.splice(i, 1); set('t7-ms', a); msMalen(); alles(); }));
      zeile.lastChild.setAttribute('aria-label', 'Zeile ' + (i + 1) + ' löschen');
      box.appendChild(zeile);
    });
    $$('[data-ms-runde]', tool).forEach(function (b) { var an = +b.getAttribute('data-ms-runde') === runde; b.setAttribute('aria-pressed', String(an)); b.className = 'btn' + (an ? ' primary' : ' ghost'); });
    msAlarm();
  }
  function msAlarm() {
    var tool = $('[data-tool="mitschrift"]'); if (!tool) return;
    var z = msDaten()[runde].z;
    alarme(z.map(function (x) { return [x.h, x.s, x.e].join(' '); }), $('.alarm-liste', tool));
  }
  function msVoll(r) { return msDaten()[r].z.filter(function (x) { return x.h && x.h.trim(); }).length; }
  function msInit() {
    var tool = $('[data-tool="mitschrift"]'); if (!tool) return;
    $('[data-ms-fall]', tool).addEventListener('input', function (e) { var a = msDaten(); a[runde].fall = e.target.value; set('t7-ms', a); });
    $$('[data-ms-runde]', tool).forEach(function (b) { b.addEventListener('click', function () { runde = +b.getAttribute('data-ms-runde'); $('.ms-vorlesen', tool).hidden = true; msMalen(); }); });
    $('[data-ms-plus]', tool).addEventListener('click', function () { var a = msDaten(); while (a[runde].z.length < 3) a[runde].z.push({ h: '', s: '', e: '' }); a[runde].z.push({ h: '', s: '', e: '' }); set('t7-ms', a); msMalen(); });
    $('[data-ms-bsp]', tool).addEventListener('click', function () {
      var a = msDaten();
      if (!belegt('Diese Runde durch das Beispiel ersetzen?', a[runde].z.some(function (x) { return x.h; }))) return;
      a[runde] = JSON.parse(JSON.stringify(MS_BSP)); set('t7-ms', a); msMalen(); alles();
    });
    $('[data-ms-vorlesen]', tool).addEventListener('click', function () {
      var ol = $('.ms-vorlesen', tool); ol.innerHTML = '';
      msDaten()[runde].z.filter(function (x) { return x.h; }).forEach(function (x) {
        ol.appendChild(el('li', '', x.h + (x.s ? ' (in: ' + x.s + ')' : '') + (x.e ? '. Entscheidung: ' + x.e : '')));
      });
      ol.hidden = !ol.children.length || !ol.hidden;
    });
    msMalen();
  }

  /* ---------- SIPOC ---------- */
  function sipoc() {
    var tool = $('[data-tool="sipoc"]');
    if (tool) {
      var i = String(val('t7-sipoc-i')).trim(), o = String(val('t7-sipoc-o')).trim(), box = $('.absperr', tool), innen = el('p');
      box.innerHTML = '';
      innen.appendChild(el('b', '', 'Der Prozess beginnt hier: ')); innen.appendChild(document.createTextNode(i || 'noch offen'));
      innen.appendChild(el('br'));
      innen.appendChild(el('b', '', 'Der Prozess endet hier: ')); innen.appendChild(document.createTextNode(o || 'noch offen'));
      box.appendChild(innen);
    }
    return sipocStand();
  }
  function sipocStand() {
    var fehlt = ['s', 'i', 'p', 'o', 'c'].filter(function (k) { return !String(val('t7-sipoc-' + k)).trim(); }).length;
    var schritte = String(val('t7-sipoc-p')).split('\n').filter(function (x) { return x.trim(); }).length;
    var ok = !fehlt && schritte >= 5 && schritte <= 7;
    stand('sipoc', ok, ok ? 'Fertig: Anfang und Ende stehen fest.' : fehlt ? 'Noch ' + fehlt + ' Spalten offen.' : schritte + ' Hauptschritte. Die Folie empfiehlt fünf bis sieben.');
    return ok;
  }

  /* ---------- Bahnen ---------- */
  var BH_BSP = { bahnen: ['Lieferant', 'Buchhaltung', 'Fachabteilung', 'Teamleitung', ''], z: [
    { n: 'Rechnung senden', b: 1, a: 'start', m: '0', w: '' }, { n: 'Rechnung sichten', b: 2, a: 'task', m: '2', w: '1.5' }, { n: 'Betrag + Lieferant prüfen', b: 2, a: 'task', m: '3', w: '' },
    { n: 'Sachlich prüfen', b: 3, a: 'task', m: '3', w: '2' }, { n: 'Bestellbezug bestätigen', b: 3, a: 'task', m: '1', w: '' }, { n: 'Betrag über 1.000 €?', b: 4, a: 'raute', m: '1', w: '0.5' },
    { n: 'Freigeben', b: 4, a: 'mensch', m: '1', w: '' }, { n: 'Freigabe erfassen', b: 2, a: 'task', m: '1', w: '1' }] };
  var ARTEN = [['task', 'Aufgabe'], ['mensch', 'Mensch entscheidet'], ['raute', 'Entscheidung'], ['start', 'Start']];
  function bahnName(i) { return String(val('t7-bahn-' + i) || '').trim(); }
  function bhZeilen() { return get('t7-bahnen', []); }
  function bhSumme(z, ohne, ohneArbeit) {
    var m = 0, w = 0, ueb = [];
    z.forEach(function (s, i) {
      if (!ohneArbeit) m += num(s.m);
      var wechsel = i > 0 && +s.b !== +z[i - 1].b;
      if (wechsel) ueb.push({ i: i, von: bahnName(z[i - 1].b) || 'Bahn ' + z[i - 1].b, nach: bahnName(s.b) || 'Bahn ' + s.b, w: num(s.w), leer: !String(s.w == null ? '' : s.w).trim() });
      if (!(ohne && ohne.indexOf(i) >= 0)) w += num(s.w);
    });
    return { m: m, w: w, ueb: ueb, tage: w + m / ARBEITSTAG, verh: m ? Math.round(w * ARBEITSTAG / m) : 0 };
  }
  function bhMalen() {
    var tool = $('[data-tool="bahnen"]'); if (!tool) return;
    var box = $('.bh-zeilen', tool), z = bhZeilen();
    box.innerHTML = '';
    z.forEach(function (s, i) {
      var zeile = el('div', 'bh-zeile');
      var n = el('input'); n.type = 'text'; n.value = s.n || ''; n.placeholder = 'Schritt ' + (i + 1); n.setAttribute('aria-label', 'Schritt ' + (i + 1));
      n.addEventListener('input', function () { bhSet(i, 'n', n.value); });
      var b = el('select'); b.setAttribute('aria-label', 'Bahn von Schritt ' + (i + 1));
      [1, 2, 3, 4, 5].forEach(function (k) { var o = el('option', '', bahnName(k) || 'Bahn ' + k); o.value = k; if (+s.b === k) o.selected = true; b.appendChild(o); });
      b.addEventListener('change', function () { bhSet(i, 'b', +b.value); });
      var a = el('select'); a.setAttribute('aria-label', 'Art von Schritt ' + (i + 1));
      ARTEN.forEach(function (x) { var o = el('option', '', x[1]); o.value = x[0]; if ((s.a || 'task') === x[0]) o.selected = true; a.appendChild(o); });
      a.addEventListener('change', function () { bhSet(i, 'a', a.value); });
      var m = el('input'); m.type = 'number'; m.min = 0; m.step = 'any'; m.value = s.m == null ? '' : s.m; m.placeholder = 'Min.'; m.setAttribute('aria-label', 'Arbeit in Minuten, Schritt ' + (i + 1));
      m.addEventListener('input', function () { bhSet(i, 'm', m.value); });
      var w = el('input'); w.type = 'number'; w.min = 0; w.step = 'any'; w.value = s.w == null ? '' : s.w; w.placeholder = 'Tage'; w.setAttribute('aria-label', 'Warten davor in Tagen, Schritt ' + (i + 1));
      w.addEventListener('input', function () { bhSet(i, 'w', w.value); });
      var weg = knopf('×', 'zeile-weg', function () { var a2 = bhZeilen(); a2.splice(i, 1); set('t7-bahnen', a2); bhMalen(); alles(); });
      weg.setAttribute('aria-label', 'Schritt ' + (i + 1) + ' löschen');
      [n, b, a, m, w, weg].forEach(function (x) { zeile.appendChild(x); });
      box.appendChild(zeile);
    });
  }
  function bhSet(i, k, v) { var z = bhZeilen(); z[i][k] = v; set('t7-bahnen', z); bhAus(); alles(); }
  var SVGNS = 'http://www.w3.org/2000/svg';
  function sv(t, a, x) { var e = document.createElementNS(SVGNS, t); for (var k in a) e.setAttribute(k, a[k]); if (x != null) e.textContent = x; return e; }
  function umbruch(t, max) {
    var out = [], z = '';
    String(t).split(/\s+/).forEach(function (w) { if ((z + ' ' + w).trim().length > max && z) { out.push(z); z = w; } else z = (z + ' ' + w).trim(); });
    if (z) out.push(z);
    return out.slice(0, 3);
  }
  function bhSkizze(box, z) {
    box.innerHTML = '';
    if (!z.length) { box.appendChild(el('p', 'bh-leer', 'Sobald du Schritte einträgst, zeichnet sich hier dein Ablauf. Oder lade den Fall Rechnung 0815.')); return; }
    var benutzt = []; z.forEach(function (s) { if (benutzt.indexOf(+s.b) < 0) benutzt.push(+s.b); }); benutzt.sort();
    var L = 104, SP = 130, H = 98, O = 8, W = L + SP * (z.length + 1) + 24, G = O + H * benutzt.length + 8;
    var svg = sv('svg', { width: W, height: G, viewBox: '0 0 ' + W + ' ' + G, role: 'img', 'aria-label': 'Ablauf in Bahnen mit ' + z.length + ' Schritten' });
    var defs = sv('defs'), pf = sv('marker', { id: 'bh-pf', markerWidth: 7, markerHeight: 7, refX: 6, refY: 3, orient: 'auto' }); pf.appendChild(sv('path', { d: 'M0 0L6 3L0 6z', fill: '#05614c' })); defs.appendChild(pf); svg.appendChild(defs);
    benutzt.forEach(function (b, i) {
      var y = O + H * i;
      svg.appendChild(sv('rect', { x: 0, y: y, width: W, height: H, fill: i % 2 ? '#f4f6f5' : '#ffffff', stroke: '#dfe5e2' }));
      umbruch(bahnName(b) || 'Bahn ' + b, 12).forEach(function (zt, k, alle) { svg.appendChild(sv('text', { x: 10, y: y + H / 2 - (alle.length - 1) * 8 + k * 16 + 5, 'font-size': 13.5, 'font-weight': 700, fill: '#0f1513' }, zt)); });
    });
    function pos(i) { var s = z[i]; return { x: L + 18 + SP * i, y: O + H * benutzt.indexOf(+s.b) + H / 2 }; }
    var bw = 108, bh = 50;
    z.forEach(function (s, i) {
      var p = pos(i);
      if (i > 0) {
        var q = pos(i - 1), x1 = q.x + bw, x2 = p.x, wechsel = p.y !== q.y;
        svg.appendChild(sv('path', { d: wechsel ? 'M' + x1 + ' ' + q.y + 'H' + (x1 + 12) + 'V' + p.y + 'H' + x2 : 'M' + x1 + ' ' + q.y + 'H' + x2, fill: 'none', stroke: wechsel ? '#05614c' : '#8d9692', 'stroke-width': wechsel ? 2 : 1.4, 'marker-end': 'url(#bh-pf)' }));
        if (num(s.w)) {
          var t = 'Ø ' + tage(num(s.w)), tw = t.length * 6.8 + 14;
          var gx = p.x - 2, gy = p.y - bh / 2 - 22;
          svg.appendChild(sv('rect', { x: gx, y: gy, rx: 10, width: tw, height: 20, fill: '#05614c' }));
          svg.appendChild(sv('text', { x: gx + tw / 2, y: gy + 14, 'font-size': 12, 'font-weight': 700, fill: '#ffffff', 'text-anchor': 'middle' }, t));
        }
      }
      var cx = p.x + bw / 2;
      if (s.a === 'raute') svg.appendChild(sv('polygon', { points: cx + ',' + (p.y - 27) + ' ' + (p.x + bw) + ',' + p.y + ' ' + cx + ',' + (p.y + 27) + ' ' + p.x + ',' + p.y, fill: '#fff', stroke: '#0f1513', 'stroke-width': 1.4 }));
      else if (s.a === 'start') svg.appendChild(sv('rect', { x: p.x, y: p.y - bh / 2, rx: bh / 2, width: bw, height: bh, fill: '#fff', stroke: '#0f1513', 'stroke-width': 1.4 }));
      else svg.appendChild(sv('rect', { x: p.x, y: p.y - bh / 2, rx: 9, width: bw, height: bh, fill: '#fff', stroke: '#0f1513', 'stroke-width': 1.4 }));
      if (s.a === 'mensch') { svg.appendChild(sv('circle', { cx: p.x + 11, cy: p.y - bh / 2 + 9, r: 3.2, fill: '#05614c' })); svg.appendChild(sv('path', { d: 'M' + (p.x + 5) + ' ' + (p.y - bh / 2 + 19) + 'a6 6 0 0 1 12 0z', fill: '#05614c' })); }
      var zeilen = umbruch(s.n || 'Schritt ' + (i + 1), s.a === 'raute' ? 12 : 15);
      zeilen.forEach(function (zt, k) { svg.appendChild(sv('text', { x: cx, y: p.y - (zeilen.length - 1) * 7.5 + k * 15 + 4, 'font-size': 12.5, fill: '#0f1513', 'text-anchor': 'middle' }, zt)); });
    });
    var letzte = pos(z.length - 1), ex = letzte.x + SP;
    svg.appendChild(sv('path', { d: 'M' + (letzte.x + bw) + ' ' + letzte.y + 'H' + (ex - 2), fill: 'none', stroke: '#8d9692', 'stroke-width': 1.4, 'marker-end': 'url(#bh-pf)' }));
    svg.appendChild(sv('circle', { cx: ex + 13, cy: letzte.y, r: 12, fill: '#fff', stroke: '#05614c', 'stroke-width': 3.5 }));
    box.appendChild(svg);
    if (W > box.clientWidth) box.appendChild(el('p', 'bh-wisch', 'Seitlich wischen oder scrollen, dann siehst du den ganzen Ablauf.'));
  }
  var bhWas = { arbeit: false, weg: [] };
  function bhAus() {
    var tool = $('[data-tool="bahnen"]'); if (!tool) return;
    var z = bhZeilen(), s = bhSumme(z), aus = $('.bh-aus', tool), was = $('.bh-was', tool);
    bhSkizze($('.bh-skizze', tool), z);
    aus.innerHTML = '';
    if (!z.length) { was.hidden = true; return; }
    function kachel(w, t, cls) { var d = el('div', 'bc-kachel ' + (cls || '')); d.appendChild(el('b', '', w)); d.appendChild(el('span', '', t)); aus.appendChild(d); }
    kachel(de(s.m, s.m % 1 ? 1 : 0) + ' Minuten', 'Bearbeitungszeit gesamt');
    kachel(de(s.tage, 1) + ' Tage', 'Durchlaufzeit gesamt', 'warn');
    if (s.m && s.w) kachel('1 zu ' + de(s.verh), 'Minute Arbeit zu Minuten Warten (8-Stunden-Tag)', s.verh >= 50 ? 'warn' : 'gut');
    var gross = s.ueb.slice().sort(function (a, b) { return b.w - a.w; })[0];
    if (gross && gross.w) kachel(tage(gross.w), 'Größte Übergabe: ' + gross.von + ' → ' + gross.nach, 'gut');
    was.hidden = !s.ueb.length;
    var kn = $('.bh-kn', tool);
    kn.innerHTML = '';
    var a = knopf('Gesamte Arbeit automatisieren', 'sp-b', function () { bhWas.arbeit = !bhWas.arbeit; bhAus(); }); a.setAttribute('aria-pressed', String(bhWas.arbeit)); kn.appendChild(a);
    s.ueb.forEach(function (u) {
      var an = bhWas.weg.indexOf(u.i) >= 0;
      var b = knopf('Übergabe streichen: ' + u.von + ' → ' + u.nach, 'sp-b', function () { var p = bhWas.weg.indexOf(u.i); if (p >= 0) bhWas.weg.splice(p, 1); else bhWas.weg.push(u.i); bhAus(); });
      b.setAttribute('aria-pressed', String(an)); kn.appendChild(b);
    });
    var neu = bhSumme(z, bhWas.weg, bhWas.arbeit), e = $('.bh-was-e', tool);
    e.textContent = !bhWas.arbeit && !bhWas.weg.length ? 'Klick dich durch: Was bringt mehr, die Arbeit oder eine Übergabe?'
      : 'Durchlaufzeit: ' + de(s.tage, 1) + ' → ' + de(neu.tage, 1) + ' Tage. ' + (bhWas.arbeit && !bhWas.weg.length ? 'Gewonnen: gerade mal ' + de(s.m, s.m % 1 ? 1 : 0) + ' Minuten. Die Tage sind noch da.' : 'Das sind ' + de(s.tage ? (s.tage - neu.tage) / s.tage * 100 : 0) + ' % weniger.');
  }
  function bhFertig() {
    var z = bhZeilen(), s = bhSumme(z), offen = s.ueb.filter(function (u) { return u.leer; }).length;
    var ok = z.length >= 3 && s.m > 0 && s.ueb.length > 0 && !offen;
    stand('bahnen', ok, ok ? 'Fertig: Beide Summen stehen, jede Übergabe hat eine Zeit.' : !z.length ? 'Noch keine Schritte eingetragen.' : offen ? offen + ' Übergaben ohne Zeitangabe. Schätzen ist hier erlaubt.' : 'Trage die Arbeitsminuten und mindestens eine Übergabe ein.');
    return ok;
  }
  function bhInit() {
    var tool = $('[data-tool="bahnen"]'); if (!tool) return;
    $('[data-bh-plus]', tool).addEventListener('click', function () { var z = bhZeilen(), v = z[z.length - 1]; z.push({ n: '', b: v ? v.b : 1, a: 'task', m: '', w: '' }); set('t7-bahnen', z); bhMalen(); bhAus(); alles(); });
    $('[data-bh-bsp]', tool).addEventListener('click', function () {
      if (!belegt('Deine Schritte durch den Fall Rechnung 0815 ersetzen?', bhZeilen().length)) return;
      BH_BSP.bahnen.forEach(function (n, i) { setVal($('[data-save="t7-bahn-' + (i + 1) + '"]'), n); });
      set('t7-bahnen', JSON.parse(JSON.stringify(BH_BSP.z))); bhWas = { arbeit: false, weg: [] }; bhMalen(); bhAus(); alles();
    });
    $('[data-bh-ms]', tool).addEventListener('click', function () {
      var quellen = msDaten()[runde].z.filter(function (x) { return x.h && x.h.trim(); });
      if (!quellen.length) { window.alert('In dieser Runde der Mitschrift steht noch nichts. Fülle sie zuerst aus oder lade dort das Beispiel.'); return; }
      if (!belegt('Deine Schritte durch die Mitschrift ersetzen?', bhZeilen().length)) return;
      set('t7-bahnen', quellen.map(function (x) { return { n: x.h, b: 1, a: x.e && x.e.trim() ? 'mensch' : 'task', m: '', w: '' }; })); bhMalen(); bhAus(); alles();
    });
    tool.addEventListener('input', function (e) { if (e.target.hasAttribute('data-bahn')) { $$('.bh-zeile select:first-of-type', tool).forEach(function (sel) { var w = sel.value; Array.prototype.forEach.call(sel.options, function (o, i) { o.textContent = bahnName(i + 1) || 'Bahn ' + (i + 1); }); sel.value = w; }); bhAus(); } });
    bhMalen(); bhAus();
  }

  /* ---------- SOP ---------- */
  var SOP_BSP = [
    { r: 'Die Buchhaltung', h: 'sichtet die eingegangene Rechnung', s: 'Mailprogramm, Ordner „Eingang Rechnungen“', m: '' }, { r: 'Die Buchhaltung', h: 'gleicht Betrag und Lieferant mit der Bestellung ab', s: 'Buchhaltungssoftware', m: '' },
    { w: true, h: 'Wartezeit: Die Rechnung liegt im Schnitt 2 Tage im Postfach der Fachabteilung', r: '', s: '', m: '' }, { r: 'Die Fachabteilung', h: 'prüft die Rechnung sachlich und bestätigt den Bestellbezug', s: 'Mailprogramm', m: 'regel' },
    { w: true, h: 'Wartezeit: im Schnitt 0,5 Tage bis zur Teamleitung', r: '', s: '', m: '' }, { r: 'Die Teamleitung', h: 'gibt Rechnungen über 1.000 Euro frei', s: 'Mailprogramm', m: 'ausnahme' }];
  function sopZeilen() { return get('t7-sop', []); }
  function sopMalen() {
    var tool = $('[data-tool="sop"]'); if (!tool) return;
    var box = $('.sop-zeilen', tool), z = sopZeilen();
    box.innerHTML = '';
    z.forEach(function (s, i) {
      var zeile = el('div', 'sop-zeile' + (s.w ? ' warte' : ''));
      function feld(k, ph) {
        var f = el('input'); f.type = 'text'; f.value = s[k] || ''; f.placeholder = ph; f.setAttribute('aria-label', ph + ', Schritt ' + (i + 1));
        f.addEventListener('input', function () { var a = sopZeilen(); a[i][k] = f.value; set('t7-sop', a); sopAlarm(); alles(); });
        return f;
      }
      zeile.appendChild(s.w ? el('span', 'sop-w', 'Wartezeit') : feld('r', 'Rolle'));
      zeile.appendChild(feld('h', s.w ? 'Wo, und wie lange?' : 'Handlung'));
      zeile.appendChild(s.w ? el('span') : feld('s', 'System'));
      var m = el('select'); m.setAttribute('aria-label', 'Markierung, Schritt ' + (i + 1));
      [['', 'Keine Markierung'], ['regel', 'Fehlende Regel'], ['ausnahme', 'Fehlende Ausnahme']].forEach(function (x) { var o = el('option', '', x[1]); o.value = x[0]; if ((s.m || '') === x[0]) o.selected = true; m.appendChild(o); });
      m.addEventListener('change', function () { var a = sopZeilen(); a[i].m = m.value; set('t7-sop', a); alles(); });
      zeile.appendChild(m);
      var weg = knopf('×', 'zeile-weg', function () { var a = sopZeilen(); a.splice(i, 1); set('t7-sop', a); sopMalen(); alles(); });
      weg.setAttribute('aria-label', 'Schritt ' + (i + 1) + ' löschen');
      zeile.appendChild(weg);
      box.appendChild(zeile);
    });
    sopAlarm();
  }
  function sopAlarm() { var tool = $('[data-tool="sop"]'); if (tool) alarme(sopZeilen().map(function (x) { return [x.r, x.h].join(' '); }), $('.alarm-liste', tool)); }
  function sopFertig() {
    var z = sopZeilen(), schritte = z.filter(function (x) { return !x.w; }), offen = schritte.filter(function (x) { return !String(x.r || '').trim() || !String(x.h || '').trim() || !String(x.s || '').trim(); }).length;
    var regel = z.filter(function (x) { return x.m === 'regel'; }).length, aus = z.filter(function (x) { return x.m === 'ausnahme'; }).length;
    var ok = schritte.length >= 3 && !offen && !!val('t7-sop-ok');
    var t = !z.length ? 'Noch keine Schritte.' : schritte.length + ' Schritte, ' + (z.length - schritte.length) + ' Wartezeiten. ' + (offen ? offen + ' Schritte ohne Rolle, Handlung oder System. ' : 'Jeder Schritt hat Rolle und System. ') + 'Markierungen: ' + regel + ' fehlende Regeln, ' + aus + ' Ausnahmen. Beides wandert in Block 4.' + (val('t7-sop-ok') ? '' : ' Noch nicht gegengelesen.');
    stand('sop', ok, t);
    return ok;
  }
  function sopInit() {
    var tool = $('[data-tool="sop"]'); if (!tool) return;
    function neu(z) { set('t7-sop', z); sopMalen(); alles(); }
    $('[data-sop-plus]', tool).addEventListener('click', function () { var z = sopZeilen(); z.push({ r: '', h: '', s: '', m: '' }); neu(z); });
    $('[data-sop-warte]', tool).addEventListener('click', function () { var z = sopZeilen(); z.push({ w: true, r: '', h: '', s: '', m: '' }); neu(z); });
    $('[data-sop-bsp]', tool).addEventListener('click', function () { if (belegt('Deinen SOP durch das Beispiel ersetzen?', sopZeilen().length)) neu(JSON.parse(JSON.stringify(SOP_BSP))); });
    $('[data-sop-bahnen]', tool).addEventListener('click', function () {
      var quellen = bhZeilen();
      if (!quellen.length) { window.alert('In den Bahnen steht noch nichts. Fülle sie zuerst aus oder lade dort den Fall Rechnung 0815.'); return; }
      if (!belegt('Deinen SOP durch die Schritte aus den Bahnen ersetzen?', sopZeilen().length)) return;
      var z = [];
      quellen.forEach(function (s) {
        if (num(s.w)) z.push({ w: true, h: 'Wartezeit: im Schnitt ' + tage(num(s.w)) + ' vor „' + s.n + '“', r: '', s: '', m: '' });
        z.push({ r: bahnName(s.b), h: s.n, s: '', m: '' });
      });
      neu(z);
    });
    sopMalen();
  }

  /* ---------- Zielsatz ---------- */
  var ZIEL = ['anteil', 'fall', 'handlung', 'kennzahl', 'zeit'];
  var FEHLT = { anteil: 'Anteil oder Menge fehlt. „Mehr“ ist keine Zahl.', fall: 'Fallmenge fehlt. Alle? Wirklich alle? Auch die von 1987?', handlung: 'Handlung fehlt. Was soll eigentlich passieren?', kennzahl: 'Kennzahl fehlt. „Gefühlt besser“ zählt nicht.', zeit: 'Zeitpunkt fehlt. So kann das Projekt auch 2049 noch erfolgreich werden.' };
  var TECHNIK = /(^|[\s-])(ki|ai|gpt|chatgpt|claude|copilot|make|zapier|n8n|bot|chatbot|agent|workflow|automation|automatisierung)($|[\s-])/i;
  function zielSatz() { return ZIEL.map(function (k) { return String(val('t7-ziel-' + k)).trim(); }); }
  function ziel() {
    var tool = $('[data-tool="ziel"]');
    var w = zielSatz(), name = String(val('t7-ziel-name')).trim(), offen = [];
    ZIEL.forEach(function (k, i) { if (!w[i]) offen.push(FEHLT[k]); });
    if (w[0] && !/\d|jede|alle/i.test(w[0])) offen.push('Der Anteil braucht eine Zahl. „Viele“ kann in sechs Monaten alles heißen.');
    if (name && TECHNIK.test(name)) offen.push('Im Projektnamen steckt ein Technologiebegriff. Nenne lieber das Ergebnis, das Werkzeug kann sich ändern.');
    if (!name) offen.push('Projektname fehlt. Er darf ruhig Spaß machen, nur keine Technik enthalten.');
    if (tool) {
      var s = $('.ziel-satz', tool);
      s.textContent = w.some(Boolean) ? [w[0], w[1], w[2]].filter(Boolean).join(' ') + (w[3] ? ', ' + w[3] : '') + (w[4] ? ', ' + w[4] : '') + '.' : 'Hier setzt sich dein Zielsatz zusammen.';
      var ul = $('.ziel-fehlt', tool); ul.innerHTML = '';
      offen.forEach(function (t) { ul.appendChild(el('li', 'warn', t)); });
    }
    var ok = !offen.length;
    stand('ziel', ok, ok ? 'Fertig: Alle fünf Bausteine sind da.' : 'Noch ' + offen.length + (offen.length === 1 ? ' Punkt' : ' Punkte') + ' offen.');
    return ok;
  }

  /* ---------- Scope ---------- */
  var SCOPE_BSP = { 'in': 'Rechnungen unter 1.000 Euro\nRechnungen mit Bestellbezug\nEingang als PDF per E-Mail\nAbgleich von Betrag und Lieferant\nFreigabe ohne manuelle Prüfung\nProtokolleintrag je Freigabe',
    out: 'Rechnungen über 1.000 Euro\nProjektabrechnungen\nRechnungen ohne Bestellbezug\nAlles mit Klärungsvermerk\nPapierrechnungen\nHistorische Rechnungen',
    ann: [['Es kommen rund 800 Rechnungen pro Monat', 'Nutzen und Aufwand werden neu gerechnet'], ['Der Zugang zum Postfach steht bis zum Start', 'Der Zeitplan verschiebt sich'], ['Die PDF-Rechnungen sind maschinenlesbar', 'Die Erkennung braucht einen Zusatzschritt']] };
  function zeilenZahl(k) { return String(val(k)).split('\n').filter(function (x) { return x.trim(); }).length; }
  function scope() {
    var a = zeilenZahl('t7-in'), b = zeilenZahl('t7-out'), ann = [1, 2, 3].filter(function (i) { return String(val('t7-ann' + i)).trim() && String(val('t7-ann' + i + '-wenn')).trim(); }).length;
    $$('[data-scope-zahl="in"]').forEach(function (e) { e.textContent = a + ' von mindestens 6 Einträgen'; });
    $$('[data-scope-zahl="out"]').forEach(function (e) { e.textContent = b + ' von mindestens 6 Einträgen'; });
    var ok = a >= 6 && b >= 6 && ann === 3;
    stand('scope', ok, ok ? 'Fertig: Zwei Listen, drei Annahmen. Monat drei kann kommen.' : 'Noch offen: ' + [a < 6 ? 'In Scope' : '', b < 6 ? 'Out of Scope' : '', ann < 3 ? (3 - ann) + ' Annahmen' : ''].filter(Boolean).join(', ') + '.');
    return ok;
  }

  /* ---------- Erfolgskriterien ---------- */
  var KR_BSP = [['Bearbeitungszeit je Rechnung', '4,0 Minuten', '1,2 Minuten', 'Zeitmessung Stichprobe, 20 Fälle', 'Monat 1 und Monat 4'], ['Durchlaufzeit je Rechnung', '5,0 Tage', '1,5 Tage', 'Zeitstempel im System', 'monatlich'],
    ['Anteil ohne manuelle Prüfung', '0 Prozent', '70 Prozent', 'Freigabeprotokoll', 'monatlich'], ['Fehlerquote bei Freigaben', '1,8 Prozent', 'höchstens 1,8 Prozent', 'Nachprüfung Stichprobe', 'Monat 3']];
  var KR = ['name', 'heute', 'ziel', 'quelle', 'wann'];
  function krZeilen() { var out = []; for (var z = 1; z <= 5; z++) { var r = {}; KR.forEach(function (k) { r[k] = String(val('t7-kr' + z + '-' + k)).trim(); }); r.z = z; if (r.name) out.push(r); } return out; }
  function kriterien() {
    var r = krZeilen(), offen = [];
    if (r.length < 3) offen.push('Es braucht mindestens drei Kriterien, du hast ' + r.length + '.');
    if (!r.some(function (x) { return /durchlauf/i.test(x.name); })) offen.push('Mindestens ein Kriterium zur Durchlaufzeit fehlt. Hol es dir aus den Bahnen.');
    var ohne = r.filter(function (x) { return !x.heute; }).length;
    if (ohne) offen.push(ohne + (ohne === 1 ? ' Kriterium hat' : ' Kriterien haben') + ' keinen Wert heute. Unbekannt? Dann schreib rein, wie er erhoben wird und bis wann.');
    var luecke = r.filter(function (x) { return !x.ziel || !x.quelle || !x.wann; }).length;
    if (luecke) offen.push(luecke + ' Zeilen ohne Zielwert, Messquelle oder Zeitpunkt.');
    var tool = $('[data-tool="kriterien"]');
    if (tool) { var ul = $('.kr-fehlt', tool); ul.innerHTML = ''; offen.forEach(function (t) { ul.appendChild(el('li', 'warn', t)); }); }
    var ok = !offen.length;
    stand('kriterien', ok, ok ? 'Fertig: Ohne Spalte „heute“ kommt hier niemand durch.' : '');
    return ok;
  }
  function krInit() {
    var tool = $('[data-tool="kriterien"]'); if (!tool) return;
    $('[data-kr-bsp]', tool).addEventListener('click', function () {
      if (!belegt('Deine Kriterien durch das Beispiel ersetzen?', krZeilen().length)) return;
      for (var z = 1; z <= 5; z++) KR.forEach(function (k, i) { setVal($('[data-save="t7-kr' + z + '-' + k + '"]'), (KR_BSP[z - 1] || [])[i] || ''); });
    });
    $('[data-kr-bahnen]', tool).addEventListener('click', function () {
      var z = bhZeilen(), s = bhSumme(z);
      if (!z.length) { window.alert('In den Bahnen steht noch nichts. Fülle sie zuerst aus oder lade dort den Fall Rechnung 0815.'); return; }
      var frei = 0; for (var i = 5; i >= 1; i--) if (!String(val('t7-kr' + i + '-name')).trim()) frei = i;
      if (!frei) { window.alert('Alle fünf Zeilen sind belegt.'); return; }
      setVal($('[data-save="t7-kr' + frei + '-name"]'), 'Durchlaufzeit'); setVal($('[data-save="t7-kr' + frei + '-heute"]'), de(s.tage, 1) + ' Tage'); setVal($('[data-save="t7-kr' + frei + '-quelle"]'), 'Zeitstempel im System'); setVal($('[data-save="t7-kr' + frei + '-wann"]'), 'monatlich');
    });
  }

  /* ---------- Akte und Stand ---------- */
  function mitschriftFertig() {
    var ok = !!val('t7-ms1-ok') && !!val('t7-ms2-ok') && msVoll(1) >= 3 && msVoll(2) >= 3;
    var t = ok ? 'Fertig: Beide Runden vorgelesen und bestätigt.' : 'Runde 1: ' + msVoll(1) + ' Zeilen, Runde 2: ' + msVoll(2) + ' Zeilen. Fertig, wenn beide vorgelesen und bestätigt sind.';
    stand('mitschrift', ok, t);
    return ok;
  }
  function alles() {
    var st = { ms: mitschriftFertig(), si: sipoc(), bh: bhFertig(), sop: sopFertig(), zi: ziel(), sc: scope(), kr: kriterien() };
    var teile = [['Interviewmitschrift', st.ms], ['SIPOC', st.si], ['Ist-Prozess in Bahnen', st.bh], ['SOP', st.sop], ['Zielsatz', st.zi], ['Scope mit Annahmen', st.sc], ['Erfolgskriterien', st.kr]];
    var n = teile.filter(function (t) { return t[1]; }).length;
    $$('.akte-liste').forEach(function (ul) { ul.innerHTML = ''; teile.forEach(function (t) { ul.appendChild(el('li', t[1] ? 'ok' : '', (t[1] ? '✓ ' : '○ ') + t[0])); }); });
    $$('[data-stat-akte]').forEach(function (e) { e.textContent = n + ' von 7'; });
    var s = bhSumme(bhZeilen());
    $$('[data-stat-verh]').forEach(function (e) { e.textContent = s.m && s.w ? '1 zu ' + de(s.verh) : 'noch offen'; });
  }
  function exportMd() {
    var L = ['# Meine Ermittlungsakte · Modul 2 · Tag 7 · 03.11.2026', '', 'Person: ' + PERSON + ' · nur erfundene oder freigegebene Angaben', ''];
    var ms = msDaten();
    L.push('## 1. Interviewmitschrift', '');
    [1, 2].forEach(function (r) {
      L.push('### Runde ' + r + (ms[r].fall ? ': ' + ms[r].fall : ''), '', '| Handlung | System | Entscheidung |', '| --- | --- | --- |');
      ms[r].z.filter(function (x) { return x.h; }).forEach(function (x) { L.push('| ' + x.h + ' | ' + (x.s || '') + ' | ' + (x.e || '') + ' |'); });
      L.push('');
    });
    L.push('## 2. SIPOC', '', '- Lieferant: ' + val('t7-sipoc-s'), '- Input (Der Prozess beginnt hier): ' + val('t7-sipoc-i'), '- Prozess: ' + String(val('t7-sipoc-p')).split('\n').join(', '), '- Output (Der Prozess endet hier): ' + val('t7-sipoc-o'), '- Empfänger: ' + val('t7-sipoc-c'), '');
    var z = bhZeilen(), s = bhSumme(z);
    L.push('## 3. Ist-Prozess in Bahnen', '');
    z.forEach(function (x, i) { L.push((i + 1) + '. ' + (bahnName(x.b) || 'Bahn ' + x.b) + ': ' + x.n + ' (' + (x.m || 0) + ' Min.' + (num(x.w) ? ', davor ' + x.w + ' Tage Warten' : '') + ')'); });
    L.push('', 'Bearbeitungszeit gesamt: ' + de(s.m, s.m % 1 ? 1 : 0) + ' Minuten · Durchlaufzeit gesamt: ' + de(s.tage, 1) + ' Tage' + (s.verh ? ' · 1 zu ' + de(s.verh) : ''), '');
    L.push('## 4. SOP', '');
    sopZeilen().forEach(function (x, i) { L.push((i + 1) + '. ' + (x.w ? x.h : [x.r, x.h].filter(Boolean).join(' ') + (x.s ? ' (System: ' + x.s + ')' : '')) + (x.m === 'regel' ? ' [fehlende Regel]' : x.m === 'ausnahme' ? ' [fehlende Ausnahme]' : '')); });
    var w = zielSatz();
    L.push('', '## 5. Zielsatz', '', 'Projektname: ' + val('t7-ziel-name'), '', [w[0], w[1], w[2]].filter(Boolean).join(' ') + (w[3] ? ', ' + w[3] : '') + (w[4] ? ', ' + w[4] : '') + '.', '');
    L.push('## 6. Scope', '', '### In Scope', '');
    String(val('t7-in')).split('\n').filter(Boolean).forEach(function (x) { L.push('- ' + x); });
    L.push('', '### Out of Scope', '');
    String(val('t7-out')).split('\n').filter(Boolean).forEach(function (x) { L.push('- ' + x); });
    L.push('- Alles, was hier nicht ausdrücklich aufgeführt ist, gilt als außerhalb des Umfangs.', '', '### Annahmen', '');
    [1, 2, 3].forEach(function (i) { if (val('t7-ann' + i)) L.push('- ' + val('t7-ann' + i) + ' · Wenn nicht: ' + val('t7-ann' + i + '-wenn')); });
    L.push('', '## 7. Erfolgskriterien', '', '| Kriterium | Wert heute | Zielwert | Messquelle | Gemessen wann |', '| --- | --- | --- | --- | --- |');
    krZeilen().forEach(function (x) { L.push('| ' + [x.name, x.heute, x.ziel, x.quelle, x.wann].join(' | ') + ' |'); });
    var blob = new Blob([L.join('\n')], { type: 'text/markdown;charset=utf-8' });
    var a = el('a'); a.href = URL.createObjectURL(blob); a.download = 'Tag7-Ermittlungsakte_' + PERSON + '.md';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  function beispielFelder(attr, frage) {
    var felder = $$('[' + attr + ']').filter(function (f) { return f.getAttribute('data-bsp') !== null; });
    if (!belegt(frage, felder.some(function (f) { return f.value; }))) return;
    felder.forEach(function (f) { setVal(f, f.getAttribute('data-bsp')); });
  }
  function init() {
    montag();
    $$('[data-spiel]').forEach(spiel);
    bingoMalen();
    $$('[data-bg-neu]').forEach(function (b) { b.addEventListener('click', function () { set('t7-bingo', []); bingoMalen(); $$('[data-tool="bingo"] .bg-frage').forEach(function (p) { p.textContent = 'Neue Runde. Viel Spaß beim Zuhören.'; }); }); });
    $$('[data-uhr]').forEach(uhr);
    msInit(); bhInit(); sopInit(); krInit();
    var b;
    if ((b = $('[data-sipoc-bsp]'))) b.addEventListener('click', function () { beispielFelder('data-sipoc', 'Dein SIPOC durch das Beispiel ersetzen?'); alles(); });
    if ((b = $('[data-ziel-bsp]'))) b.addEventListener('click', function () { beispielFelder('data-ziel', 'Deine Bausteine durch das Beispiel ersetzen?'); var n = $('[data-ziel-name]'); if (n && !n.value) setVal(n, 'Rechnung in einem Tag'); alles(); });
    if ((b = $('[data-scope-bsp]'))) b.addEventListener('click', function () {
      if (!belegt('Deinen Scope durch das Beispiel ersetzen?', String(val('t7-in')).trim() || String(val('t7-out')).trim())) return;
      setVal($('[data-save="t7-in"]'), SCOPE_BSP['in']); setVal($('[data-save="t7-out"]'), SCOPE_BSP.out);
      SCOPE_BSP.ann.forEach(function (a, i) { setVal($('[data-save="t7-ann' + (i + 1) + '"]'), a[0]); setVal($('[data-save="t7-ann' + (i + 1) + '-wenn"]'), a[1]); });
      alles();
    });
    if ((b = $('[data-t7-export]'))) b.addEventListener('click', exportMd);
    document.addEventListener('input', alles);
    document.addEventListener('change', alles);
    alles();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
