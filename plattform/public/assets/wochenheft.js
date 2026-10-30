/* Modul 2 · Woche 1: Learning Hub und Wochenheft.
   Zeitfresser-Rechner, Steckbriefe, Stufen/Ausschluss, Entscheidungstreppe, Kopieren der Make-Vorlagen,
   Fortschritt. Speicher nur in diesem Browser unter kurs:m2w1:<person>:<feld>. */
(function () {
  'use strict';
  var root = document.documentElement;
  var PERSON = root.getAttribute('data-person') || 'gast';
  var PREFIX = 'kurs:m2w1:' + PERSON + ':';
  var storageOk = true;
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function get(k, def) {
    try { var v = localStorage.getItem(PREFIX + k); return v === null ? def : JSON.parse(v); } catch (e) { storageOk = false; return def; }
  }
  function set(k, v) {
    try { localStorage.setItem(PREFIX + k, JSON.stringify(v)); } catch (e) { storageOk = false; warnStorage(); }
  }
  function warnStorage() {
    $$('.tool-h span').forEach(function (s) { s.textContent = 'Speichern in diesem Browser ist gesperrt – bitte am Ende herunterladen.'; });
  }
  function num(v) { var n = parseFloat(String(v || '').replace(',', '.')); return isFinite(n) ? n : 0; }
  function fmt(n) { return Math.round(n).toLocaleString('de-DE'); }

  /* ---------- Felder mit data-save ---------- */
  function initSaves() {
    $$('[data-save]').forEach(function (f) {
      var k = f.getAttribute('data-save');
      var v = get(k, null);
      if (f.type === 'checkbox') f.checked = !!v; else if (v !== null) f.value = v;
      var t;
      function save() {
        clearTimeout(t);
        t = setTimeout(function () {
          set(k, f.type === 'checkbox' ? f.checked : f.value);
          // gleiche Felder auf derselben Seite angleichen
          $$('[data-save="' + k + '"]').forEach(function (o) { if (o !== f) { if (o.type === 'checkbox') o.checked = f.checked; else o.value = f.value; } });
          refresh();
        }, 250);
      }
      f.addEventListener('input', save); f.addEventListener('change', save);
    });
  }

  /* ---------- Kopieren ---------- */
  function legacyCopy(text) {
    var ta = el('textarea'), ok = false; ta.value = text; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.focus(); ta.select(); ta.setSelectionRange(0, text.length);
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function copyText(text) {
    // Erst die Zwischenablage-Schnittstelle, sonst der klassische Weg – beides noch innerhalb des Klicks.
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { if (!legacyCopy(text)) throw new Error('copy'); });
    }
    return legacyCopy(text) ? Promise.resolve() : Promise.reject(new Error('copy'));
  }
  // Vorlagen vorab laden: Die Zwischenablage (v. a. Safari am Mac) verlangt das Kopieren direkt im Klick.
  var cache = {};
  function load(url) {
    if (!cache[url]) cache[url] = fetch(url, { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) { cache[url] = t; return t; }, function (e) { delete cache[url]; throw e; });
    return cache[url];
  }
  function initCopy() {
    var btns = $$('[data-copy-url]');
    function pre(b) { load(b.getAttribute('data-copy-url')).catch(function () {}); }
    if ('IntersectionObserver' in window) {
      // erst laden, wenn der Knopf sichtbar wird – keine abgebrochenen Anfragen beim schnellen Seitenwechsel
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); pre(e.target); } }); }, { rootMargin: '400px 0px' });
      btns.forEach(function (b) { io.observe(b); });
    } else if (btns.length) setTimeout(function () { btns.forEach(pre); }, 800);
    btns.forEach(function (b) {
      var label = b.textContent;
      function say(t) { b.textContent = t; setTimeout(function () { b.textContent = label; }, 4000); }
      b.addEventListener('click', function () {
        var url = b.getAttribute('data-copy-url'), text = cache[url];
        var job = typeof text === 'string' ? copyText(text) : load(url).then(copyText);
        job.then(function () { say('Kopiert ✓ – in Make: Rechtsklick → Paste'); })
          .catch(function () { say('Kopieren ging nicht – bitte „JSON herunterladen“'); });
      });
    });
  }

  /* ---------- Zeitfresser-Rechner ---------- */
  var DEMO = [
    { t: 'Rechnungsdaten abtippen', h: 60, m: 12, s: 2, f: 'm' },
    { t: 'Monatsbericht formatieren', h: 2, m: 45, s: 3, f: 'h' },
    { t: 'Anfragen ins Postfach-Ordner sortieren', h: 180, m: 3, s: 1, f: 'n' },
    { t: 'Termine aus Mails in den Kalender übertragen', h: 40, m: 4, s: 2, f: 'm' }
  ];
  function initZeitfresser() {
    $$('[data-tool="zeitfresser"]').forEach(function (tool) {
      var table = $('.zf-table', tool), top = $('.zf-top', tool);
      var rows = get('zeitfresser', null) || [{ t: '', h: '', m: '', s: '', f: '' }];
      function save() { set('zeitfresser', rows); refresh(); }
      function draw() {
        table.innerHTML = '';
        var head = el('div', 'zf-row kopf');
        ['Tätigkeit', 'pro Monat', 'Min. je Vorgang', 'Systeme', 'Fehler', 'Min. / Monat', ''].forEach(function (h) { head.appendChild(el('span', '', h)); });
        table.appendChild(head);
        var ranked = rows.map(function (r, i) { return { i: i, v: num(r.h) * num(r.m) }; }).filter(function (x) { return x.v > 0; })
          .sort(function (a, b) { return b.v - a.v; }).slice(0, 3).map(function (x) { return x.i; });
        rows.forEach(function (r, i) {
          var row = el('div', 'zf-row' + (ranked.indexOf(i) >= 0 ? ' top' : '')); row.setAttribute('role', 'row');
          function inp(key, type, label, w) {
            var x = el('input'); x.type = type; x.value = r[key]; x.setAttribute('aria-label', label + ' (Zeile ' + (i + 1) + ')');
            if (type === 'number') { x.min = '0'; x.inputMode = 'decimal'; }
            x.placeholder = w || '';
            x.addEventListener('input', function () { r[key] = x.value; min.textContent = fmt(num(r.h) * num(r.m)); save(); paintTop(); markTop(); });
            row.appendChild(x);
          }
          inp('t', 'text', 'Tätigkeit', 'z. B. Angebote abtippen'); inp('h', 'number', 'Häufigkeit pro Monat', 'pro Monat'); inp('m', 'number', 'Minuten je Vorgang', 'Minuten');
          inp('s', 'number', 'Anzahl Systeme', 'Systeme');
          var sel = el('select'); sel.setAttribute('aria-label', 'Fehleranfälligkeit (Zeile ' + (i + 1) + ')');
          [['', 'Fehler?'], ['n', 'niedrig'], ['m', 'mittel'], ['h', 'hoch']].forEach(function (o) { var op = el('option', '', o[1]); op.value = o[0]; sel.appendChild(op); });
          sel.value = r.f || ''; sel.addEventListener('change', function () { r.f = sel.value; save(); }); row.appendChild(sel);
          var min = el('span', 'zf-min', fmt(num(r.h) * num(r.m))); min.setAttribute('aria-label', 'Minuten pro Monat'); row.appendChild(min);
          var del = el('button', 'zf-del', '×'); del.type = 'button'; del.setAttribute('aria-label', 'Zeile ' + (i + 1) + ' löschen');
          del.addEventListener('click', function () { rows.splice(i, 1); if (!rows.length) rows.push({ t: '', h: '', m: '', s: '', f: '' }); save(); draw(); });
          row.appendChild(del);
          table.appendChild(row);
        });
        paintTop();
      }
      function markTop() {
        var ranked = rows.map(function (r, i) { return { i: i, v: num(r.h) * num(r.m) }; }).filter(function (x) { return x.v > 0; })
          .sort(function (a, b) { return b.v - a.v; }).slice(0, 3).map(function (x) { return x.i; });
        $$('.zf-row:not(.kopf)', table).forEach(function (row, i) { row.classList.toggle('top', ranked.indexOf(i) >= 0); });
      }
      function paintTop() {
        var list = rows.map(function (r) { return { t: r.t || '(ohne Namen)', v: num(r.h) * num(r.m) }; }).filter(function (x) { return x.v > 0; })
          .sort(function (a, b) { return b.v - a.v; });
        top.innerHTML = '';
        if (!list.length) { top.textContent = 'Trage Häufigkeit und Minuten ein – die Top 3 erscheinen hier.'; return; }
        top.appendChild(el('span', '', 'Deine Top 3 nach Minuten pro Monat:'));
        var ol = el('ol');
        list.slice(0, 3).forEach(function (x) { ol.appendChild(el('li', '', x.t + ' – ' + fmt(x.v) + ' Min. (' + (x.v / 60).toLocaleString('de-DE', { maximumFractionDigits: 1 }) + ' Std.)' + (x.v >= 600 ? ' · Top-Kandidat' : ''))); });
        top.appendChild(ol);
      }
      $('[data-zf-add]', tool).addEventListener('click', function () { rows.push({ t: '', h: '', m: '', s: '', f: '' }); save(); draw(); var ins = $$('.zf-row:last-child input', table); if (ins[0]) ins[0].focus(); });
      $('[data-zf-sort]', tool).addEventListener('click', function () { rows.sort(function (a, b) { return num(b.h) * num(b.m) - num(a.h) * num(a.m); }); save(); draw(); });
      $('[data-zf-demo]', tool).addEventListener('click', function () {
        var empty = rows.every(function (r) { return !r.t && !r.h && !r.m; });
        if (!empty && !window.confirm('Beispielzeilen unten anhängen?')) return;
        rows = (empty ? [] : rows).concat(DEMO.map(function (d) { return Object.assign({}, d); })); save(); draw();
      });
      draw();
    });
  }

  /* ---------- Steckbriefe ---------- */
  var NUTZEN_ZAHL = /\d/;
  var NUTZEN_EINHEIT = /(stunde|std|minute|min\b|euro|€|prozent|%|fälle|vorgänge|anfragen|tage?\b|personen)/i;
  var NUTZEN_ZEIT = /(pro|je|im|in der|im|\/)\s*(monat|woche|jahr|tag|quartal)|monatlich|wöchentlich|jährlich|täglich/i;
  function initSteckbrief() {
    $$('[data-tool="steckbrief"]').forEach(function (tool) {
      var tabs = $$('.sb-tab', tool);
      tabs.forEach(function (t) {
        t.addEventListener('click', function () {
          tabs.forEach(function (o) { o.setAttribute('aria-pressed', String(o === t)); });
          $$('[data-sb-pane]', tool).forEach(function (p) { p.hidden = p.getAttribute('data-sb-pane') !== t.getAttribute('data-sb'); });
        });
      });
      $$('[data-sb-pane]', tool).forEach(function (pane) {
        var f = $('[data-nutzen]', pane), out = $('.sb-check', pane);
        function check() {
          var v = f.value.trim();
          if (!v) { out.textContent = ''; out.className = 'sb-check'; return; }
          var miss = [];
          if (!NUTZEN_ZAHL.test(v)) miss.push('Zahl');
          if (!NUTZEN_EINHEIT.test(v)) miss.push('Einheit (z. B. Stunden)');
          if (!NUTZEN_ZEIT.test(v)) miss.push('Zeitraum (z. B. pro Monat)');
          out.textContent = miss.length ? 'Nutzen-Check: Noch ergänzen: ' + miss.join(', ') + '.' : 'Nutzen-Check: Zahl, Einheit und Zeitraum sind da ✓';
          out.className = 'sb-check ' + (miss.length ? 'warn' : 'ok');
        }
        f.addEventListener('input', check); check();
      });
    });
  }

  /* ---------- Stufen und Ausschluss ---------- */
  function paintStufen() {
    $$('[data-tool="stufen"] .st-col').forEach(function (col) {
      var k = col.getAttribute('data-st');
      var name = get('sb' + k + '-name', '');
      $$('[data-sb-name="' + k + '"]').forEach(function (s) { s.textContent = name ? '· ' + name : ''; });
      var ok = 0; for (var i = 1; i <= 5; i++) if (get('st' + k + '-k' + i, false)) ok++;
      var std = get('st' + k + '-standard', ''), aus = get('st' + k + '-ausnahme', ''), zeit = get('st' + k + '-zeit', false);
      var msg = [], warn = false;
      if (std !== '' && aus !== '' && +aus > +std) { msg.push('Ausnahme höher als Standardfall? Meist ist es umgekehrt.'); warn = true; }
      if (std === '2' && !zeit) { msg.push('Ohne Zeit und Information zum Widersprechen ist Stufe 2 faktisch höher.'); warn = true; }
      if (std === '4') { msg.push('Stufe 4: Geht es um Entscheidungen über Menschen? Dann nicht zulässig.'); warn = true; }
      msg.push(ok === 5 ? 'Alle fünf Ausschlusskriterien bestanden ✓' : ok + ' von 5 Ausschlusskriterien abgehakt.');
      var out = $('.st-result', col); out.textContent = msg.join(' '); out.className = 'st-result ' + (ok === 5 && !warn ? 'ok' : 'warn');
    });
  }

  /* ---------- Entscheidungstreppe ---------- */
  function initTreppe() {
    $$('[data-tool="treppe"]').forEach(function (tool) {
      var steps = JSON.parse(tool.getAttribute('data-steps')), stage = $('.tr-stage', tool);
      function show(i) {
        stage.innerHTML = '';
        if (i >= steps.length) {
          var r = el('div', 'tr-res'); r.appendChild(el('b', '', 'Use-Case neu definieren'));
          r.appendChild(el('span', '', 'Dreimal Nein: Der Use-Case ist noch nicht scharf beschrieben. Zurück zum Auslöser und zum Steckbrief.'));
          stage.appendChild(r); stage.appendChild(restart()); return;
        }
        stage.appendChild(el('p', 'tr-step', 'Frage ' + (i + 1) + ' von ' + steps.length));
        stage.appendChild(el('p', 'tr-q', steps[i][0]));
        var row = el('div', 'btnrow');
        var ja = el('button', 'btn primary', 'Ja'); ja.type = 'button';
        var nein = el('button', 'btn', 'Nein'); nein.type = 'button';
        ja.addEventListener('click', function () {
          stage.innerHTML = '';
          var r = el('div', 'tr-res'); r.appendChild(el('b', '', steps[i][1])); r.appendChild(el('span', '', steps[i][2] + ' Hier stehen bleiben.'));
          stage.appendChild(r); stage.appendChild(restart()); r.setAttribute('tabindex', '-1'); r.focus();
        });
        nein.addEventListener('click', function () { show(i + 1); var b = $('.btn', stage); if (b) b.focus(); });
        row.appendChild(ja); row.appendChild(nein); stage.appendChild(row);
      }
      function restart() { var b = el('button', 'btn ghost', 'Neuen Fall prüfen'); b.type = 'button'; b.style.marginTop = '12px'; b.addEventListener('click', function () { show(0); }); return b; }
      show(0);
    });
  }

  /* ---------- Export ---------- */
  var FELDER = [['name', 'Name'], ['eigentuemer', 'Verantwortlich'], ['problem', 'Problem'], ['ausloeser', 'Auslöser'], ['input', 'Input'],
    ['verarbeitung', 'System übernimmt'], ['output', 'Output'], ['volumen', 'Volumen'], ['nutzen', 'Nutzen'], ['richtig_wenn', 'Richtig, wenn'], ['nicht_dabei', 'Nicht dabei']];
  var STUFEN = ['0 Manuell', '1 Assistenz', '2 Human-in-the-Loop', '3 Semi-Autonom', '4 Autonom'];
  var KRIT = ['Datenzugriff', 'Verantwortliche Person', 'Rechtlich zulässig', 'Richtiger Output definierbar', 'Prozess stabil'];
  function exportMd() {
    var L = ['# Meine Use-Case-Arbeit · Modul 2 · 30.10.2026', '', 'Person: ' + PERSON + ' · nur erfundene oder freigegebene Angaben', '', '## 1 Zeitfresser', '',
      '| Tätigkeit | pro Monat | Min. | Systeme | Fehler | Min./Monat |', '|---|---|---|---|---|---|'];
    (get('zeitfresser', []) || []).forEach(function (r) { if (r.t || r.h) L.push('| ' + [r.t, r.h, r.m, r.s, r.f, fmt(num(r.h) * num(r.m))].join(' | ') + ' |'); });
    L.push('', '## 2 Schmerz-Interview', '');
    for (var q = 1; q <= 4; q++) L.push(q + '. ' + (get('interview-' + q, '') || '–'));
    L.push('Markiert: ' + (get('interview-markiert', '') || '–'));
    for (var k = 1; k <= 3; k++) {
      L.push('', '## 3 Steckbrief ' + k, '');
      FELDER.forEach(function (f, i) { L.push((i + 1) + '. **' + f[1] + ':** ' + (get('sb' + k + '-' + f[0], '') || '(offen)')); });
      var s = get('st' + k + '-standard', ''), a = get('st' + k + '-ausnahme', '');
      L.push('', 'Stufe Standardfall: ' + (s !== '' ? STUFEN[+s] : '–') + ' · Ausnahme: ' + (a !== '' ? STUFEN[+a] : '–'));
      L.push('Begründung: ' + (get('st' + k + '-warum', '') || '–'));
      L.push('Ausschlusskriterien bestanden: ' + KRIT.filter(function (_, i) { return get('st' + k + '-k' + (i + 1), false); }).join(', '));
      L.push('Einwände: ' + (get('st' + k + '-einwaende', '') || '–'));
    }
    var blob = new Blob([L.join('\n')], { type: 'text/markdown;charset=utf-8' });
    var a = el('a'); a.href = URL.createObjectURL(blob); a.download = 'Use-Case-Arbeit_' + PERSON + '_2026-10-30.md';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  /* ---------- Fortschritt ---------- */
  function refresh() {
    var done = 0; for (var i = 1; i <= 9; i++) if (get('vorlage-a' + i, false)) done++;
    $$('[data-vorlagen-count]').forEach(function (e) { e.textContent = done; });
    $$('[data-vorlagen-meter]').forEach(function (e) { e.style.width = Math.round(done / 9 * 100) + '%'; });
    var filled = 0;
    try {
      for (var j = 0; j < localStorage.length; j++) {
        var key = localStorage.key(j);
        if (key.indexOf(PREFIX) === 0 && !/vorlage-a|zeitfresser/.test(key)) { var v = JSON.parse(localStorage.getItem(key)); if (v && v !== '') filled++; }
      }
      filled += (get('zeitfresser', []) || []).filter(function (r) { return r.t && num(r.h) && num(r.m); }).length;
    } catch (e) { /* kein Speicher */ }
    $$('[data-labor-count]').forEach(function (e) { e.textContent = filled; });
    paintStufen();
  }

  /* ---------- Hub: Start-Reiter, Filter, Suche, Sprungziele ---------- */
  function initHub() {
    var start = $('[data-tab="start"]');
    // Sprungziele innerhalb eines Reiters (z. B. #vorlage-a3 aus den Tagesseiten): Reiter öffnen, dann hinscrollen
    function deepLink() {
      var h = location.hash.slice(1), target = h && document.getElementById(h);
      if (!target || target.classList.contains('tpanel')) return;
      var panel = target.closest('.tpanel'), tab = panel && $('[data-tab="' + panel.id + '"]');
      if (!tab) return;
      if (panel.hidden) { tab.click(); history.replaceState(null, '', '#' + h); }
      function go() { target.scrollIntoView({ block: 'start', behavior: 'instant' }); }
      setTimeout(go, 120); setTimeout(go, 700);
    }
    if (start) { setTimeout(deepLink, 0); window.addEventListener('hashchange', function () { setTimeout(deepLink, 0); }); }
    $$('[data-jump]').forEach(function (a) {
      a.addEventListener('click', function () {
        var id = a.getAttribute('data-jump');
        setTimeout(function () { var t = document.getElementById(id); if (t) t.scrollIntoView({ block: 'start', behavior: 'instant' }); }, 120);
      });
    });
    $$('[data-day-filter]').forEach(function (b, _, all) {
      b.addEventListener('click', function () {
        var d = b.getAttribute('data-day-filter');
        all.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        $$('.lcard[data-day]').forEach(function (c) { c.hidden = !!d && c.getAttribute('data-day') !== d; });
      });
    });
    var s = $('[data-words-search]');
    if (s) s.addEventListener('input', function () {
      var q = s.value.trim().toLowerCase();
      $$('.words .word').forEach(function (w) { w.hidden = !!q && w.textContent.toLowerCase().indexOf(q) < 0; });
    });
  }

  /* ---------- Leseseite: aktuelles Kapitel markieren ---------- */
  function initNav() {
    var links = $$('.rd-nav a[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting && map[e.target.id]) { links.forEach(function (a) { a.classList.remove('on'); }); map[e.target.id].classList.add('on'); } });
    }, { rootMargin: '-20% 0px -70% 0px' });
    $$('.kapitel[id]').forEach(function (k) { io.observe(k); });
  }

  function init() {
    try { localStorage.setItem(PREFIX + 'probe', '1'); localStorage.removeItem(PREFIX + 'probe'); } catch (e) { storageOk = false; }
    initSaves(); initCopy(); initZeitfresser(); initSteckbrief(); initTreppe(); initHub(); initNav();
    $$('[data-export]').forEach(function (b) { b.addEventListener('click', exportMd); });
    if (!storageOk) warnStorage();
    refresh();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
