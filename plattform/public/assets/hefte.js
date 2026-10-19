/* Arbeitshefte – Ausfuellen im Browser, automatisch speichern (localStorage), PDF ueber den Server.
   Dieselbe Datei laeuft auch serverseitig beim PDF-Export (?pdf=1): dort werden nur die Antworten eingesetzt. */
(function () {
  'use strict';
  var BASE = '/hefte';
  var root = document.documentElement;
  var HID = root.getAttribute('data-heft') || '';
  var KEY = 'hefte:v1:' + HID;
  var PDFMODE = /[?&]pdf=1/.test(location.search);
  var fields = [];
  var storageOk = true;
  var saveTimer = null;

  function meta(name) { var m = document.querySelector('meta[name="' + name + '"]'); return m ? m.content : ''; }
  function isEmpty(el) { return el.textContent.replace(/\s+/g, '') === ''; }

  /* ---------- Felder erkennen (Reihenfolge = Dokument, identisch im Browser und beim PDF-Export) ---------- */
  function collect() {
    var nodes = document.querySelectorAll('.namefields > div, table.fill td, .lines, ul.check > li');
    Array.prototype.forEach.call(nodes, function (el) {
      if (el.matches('.namefields > div')) {
        var v = document.createElement('div');
        v.className = 'nfv';
        v.setAttribute('aria-label', el.textContent.trim());
        el.insertBefore(v, el.firstChild);
        makeEditable(v);
        add(v, 'text');
      } else if (el.tagName === 'TD') {
        var table = el.closest('table');
        var kind = table.getAttribute('data-kind');
        var col = el.cellIndex;
        if (kind === 'quiz' && col > 0) {
          el.classList.add('tickcell');
          el.setAttribute('role', 'button'); el.tabIndex = 0;
          el.setAttribute('aria-label', col === 1 ? 'richtig' : 'falsch');
          add(el, 'quiz');
        } else if (kind === 'tick') {
          el.classList.add('tickcell');
          el.setAttribute('role', 'button'); el.tabIndex = 0;
          var th = table.rows[0] && table.rows[0].cells[col];
          el.setAttribute('aria-label', (th ? th.textContent.trim() : '') + ': vorhanden oder fehlt');
          add(el, 'tick');
        } else if (isEmpty(el) && !el.classList.contains('nr') && !el.classList.contains('case')) {
          el.classList.add('edit');
          var th2 = table.rows[0] && table.rows[0].cells[col];
          if (th2) el.setAttribute('aria-label', th2.textContent.trim());
          makeEditable(el);
          add(el, 'text');
        }
      } else if (el.classList.contains('lines')) {
        var w = document.createElement('div');
        w.className = 'write' + (el.classList.contains('full') ? ' full' : '');
        w.setAttribute('style', el.getAttribute('style') || '');
        var prev = el.previousElementSibling;
        if (prev && prev.classList.contains('lineslabel')) w.setAttribute('aria-label', prev.textContent.trim());
        el.parentNode.replaceChild(w, el);
        makeEditable(w);
        add(w, 'text');
      } else if (el.tagName === 'LI') {
        el.setAttribute('role', 'checkbox'); el.setAttribute('aria-checked', 'false'); el.tabIndex = 0;
        add(el, 'check');
      }
    });
    // breite Tabellen fuer das Handy seitlich wischbar machen
    Array.prototype.forEach.call(document.querySelectorAll('body.web > section table'), function (t) {
      var cols = t.rows[0] ? t.rows[0].cells.length : 0;
      if (cols >= 4) t.classList.add('wide');
      var wrap = document.createElement('div');
      wrap.className = 'tscroll';
      t.parentNode.insertBefore(wrap, t);
      wrap.appendChild(t);
    });
  }
  function add(el, type) { el.setAttribute('data-f', 'f' + fields.length); fields.push({ el: el, type: type }); }
  function makeEditable(el) {
    el.setAttribute('contenteditable', 'true');
    el.setAttribute('role', 'textbox');
    el.setAttribute('aria-multiline', 'true');
    el.spellcheck = true;
  }

  /* ---------- Werte lesen / setzen ---------- */
  function value(f) {
    if (f.type === 'text') return f.el.innerText.replace(/ /g, ' ').replace(/\s+$/, '');
    if (f.type === 'check') return f.el.classList.contains('done') ? '1' : '';
    return f.el.textContent.trim();
  }
  function set(f, v) {
    v = v == null ? '' : String(v);
    if (f.type === 'text') { f.el.textContent = v; }
    else if (f.type === 'check') { f.el.classList.toggle('done', v === '1'); f.el.setAttribute('aria-checked', v === '1' ? 'true' : 'false'); }
    else { f.el.textContent = v; f.el.classList.toggle('no', v === '✗'); }
  }
  function answers() {
    var a = {};
    fields.forEach(function (f, i) { var v = value(f); if (v) a['f' + i] = v; });
    return a;
  }
  function apply(a) {
    fields.forEach(function (f, i) { set(f, a && Object.prototype.hasOwnProperty.call(a, 'f' + i) ? a['f' + i] : ''); });
  }
  function nameValue() {
    var n = fields.length && fields[0].el.classList.contains('nfv') ? value(fields[0]) : '';
    return n.replace(/[^\wÄÖÜäöüß\- ]+/g, '').trim().replace(/\s+/g, '-').slice(0, 40);
  }

  /* ---------- Speichern ---------- */
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var d = JSON.parse(raw);
      return d && d.f ? d : null;
    } catch (e) { storageOk = false; return null; }
  }
  function save() {
    var a = answers();
    var n = Object.keys(a).length;
    try {
      if (n) localStorage.setItem(KEY, JSON.stringify({ v: 1, t: Date.now(), n: fields.length, f: a }));
      else localStorage.removeItem(KEY);
      storageOk = true;
      status(n ? 'ok' : '', n ? 'Gespeichert ' + time(new Date()) + ' · nur in diesem Browser' : 'Noch nichts eingetragen');
    } catch (e) {
      storageOk = false;
      status('warn', 'Speichern im Browser nicht möglich (privates Fenster?) – bitte als PDF oder Datei sichern.');
    }
  }
  function scheduleSave() { clearTimeout(saveTimer); saveTimer = setTimeout(save, 350); }
  function time(d) { return d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }); }
  function status(cls, text) {
    var s = document.getElementById('wb-status');
    if (!s) return;
    s.className = 'wb-status' + (cls ? ' ' + cls : '');
    s.textContent = text;
  }

  /* ---------- Bedienung ---------- */
  function bind() {
    document.addEventListener('input', function (e) { if (e.target.closest && e.target.closest('[data-f]')) scheduleSave(); });
    document.addEventListener('paste', function (e) {
      var el = e.target.closest && e.target.closest('[contenteditable]');
      if (!el) return;
      e.preventDefault();
      var text = (e.clipboardData || window.clipboardData).getData('text/plain') || '';
      if (!document.execCommand('insertText', false, text)) {
        var sel = window.getSelection();
        if (sel.rangeCount) { var r = sel.getRangeAt(0); r.deleteContents(); r.insertNode(document.createTextNode(text)); r.collapse(false); }
      }
      scheduleSave();
    });
    document.addEventListener('drop', function (e) { if (e.target.closest && e.target.closest('[contenteditable]')) e.preventDefault(); });
    document.addEventListener('click', function (e) {
      var li = e.target.closest && e.target.closest('ul.check > li[data-f]');
      if (li && !e.target.closest('a')) { toggleCheck(li); return; }
      var td = e.target.closest && e.target.closest('td.tickcell');
      if (td) toggleTick(td);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== ' ' && e.key !== 'Enter') return;
      var li = e.target.closest && e.target.closest('ul.check > li[data-f]');
      var td = e.target.closest && e.target.closest('td.tickcell');
      if (li && e.target === li) { e.preventDefault(); toggleCheck(li); }
      else if (td && e.target === td) { e.preventDefault(); toggleTick(td); }
    });
  }
  function fieldOf(el) { return fields[+el.getAttribute('data-f').slice(1)]; }
  function toggleCheck(li) { var f = fieldOf(li); set(f, value(f) ? '' : '1'); scheduleSave(); }
  function toggleTick(td) {
    var f = fieldOf(td);
    if (f.type === 'quiz') {
      var on = value(f) !== '✓';
      Array.prototype.forEach.call(td.parentNode.cells, function (c) { if (c !== td && c.classList.contains('tickcell')) set(fieldOf(c), ''); });
      set(f, on ? '✓' : '');
    } else {
      var order = ['', '✓', '✗'];
      set(f, order[(order.indexOf(value(f)) + 1) % 3]);
    }
    scheduleSave();
  }

  function extras() {
    // Kopieren-Knopf an jedem Prompt
    Array.prototype.forEach.call(document.querySelectorAll('.prompt'), function (p) {
      var lbl = p.querySelector('.lbl');
      if (!lbl) return;
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'copy'; b.textContent = 'Kopieren';
      b.addEventListener('click', function () {
        var c = p.cloneNode(true);
        var l = c.querySelector('.lbl'); if (l) l.remove();
        copyText(c.innerText.trim(), b);
      });
      lbl.appendChild(b);
    });
    // Kontrollloesung umdrehen
    Array.prototype.forEach.call(document.querySelectorAll('.solution'), function (s) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'sol-btn'; b.textContent = 'Lösung umdrehen';
      b.addEventListener('click', function () {
        var open = s.classList.toggle('open');
        b.textContent = open ? 'Wieder umdrehen' : 'Lösung umdrehen';
      });
      var tag = s.querySelector('.tag');
      if (tag) tag.insertAdjacentElement('afterend', b); else s.insertBefore(b, s.firstChild);
    });
  }
  function copyText(t, b) {
    function ok() { b.textContent = 'Kopiert ✓'; b.classList.add('done'); setTimeout(function () { b.textContent = 'Kopieren'; b.classList.remove('done'); }, 1600); }
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(t).then(ok, fallback); } else { fallback(); }
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = t; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); ok(); } catch (e) { b.textContent = 'Bitte markieren'; }
      ta.remove();
    }
  }

  /* ---------- Werkzeugleiste ---------- */
  function overlay(html) {
    var o = document.getElementById('wb-overlay');
    if (!o) { o = document.createElement('div'); o.id = 'wb-overlay'; o.setAttribute('role', 'dialog'); o.setAttribute('aria-modal', 'true'); document.body.appendChild(o); }
    if (html == null) { o.hidden = true; return o; }
    o.innerHTML = '<div class="ov">' + html + '</div>';
    o.hidden = false;
    return o;
  }
  function download(blob, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
  }
  function fileBase() { var n = nameValue(); return meta('heft-file') + (n ? '_' + n : ''); }
  function closeMenu() { var d = document.querySelector('.wb-more'); if (d) d.open = false; }

  function pdf() {
    closeMenu();
    save();
    overlay('<div class="spin"></div><b>PDF wird erstellt …</b><p>Das dauert etwa 10 Sekunden. Die Antworten werden dafür kurz an den Server geschickt und danach sofort verworfen.</p>');
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 90000);
    fetch(BASE + '/api/pdf', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ heft: HID, answers: answers() }), signal: ctrl ? ctrl.signal : undefined
    }).then(function (r) {
      if (!r.ok) return r.text().then(function (t) { throw new Error(t || ('Fehler ' + r.status)); });
      return r.blob();
    }).then(function (blob) {
      clearTimeout(timer);
      download(blob, fileBase() + '.pdf');
      var o = overlay('<b>Fertig ✓</b><p>Das PDF liegt im Download-Ordner.</p><div class="row"><button type="button" class="wb-primary" data-x="close">Schließen</button></div>');
      o.querySelector('[data-x=close]').onclick = function () { overlay(null); };
    }).catch(function (e) {
      clearTimeout(timer);
      var msg = String(e && e.message || e).slice(0, 200).replace(/[<>&]/g, '');
      var o = overlay('<b>Das PDF konnte gerade nicht erstellt werden.</b><p>' + msg + '</p><p>Alternative: „Drucken“ und im Druckfenster „Als PDF sichern“ wählen.</p>' +
        '<div class="row"><button type="button" class="wb-primary" data-x="print">Drucken</button><button type="button" data-x="retry">Nochmal versuchen</button><button type="button" data-x="close">Schließen</button></div>');
      o.querySelector('[data-x=print]').onclick = function () { overlay(null); window.print(); };
      o.querySelector('[data-x=retry]').onclick = pdf;
      o.querySelector('[data-x=close]').onclick = function () { overlay(null); };
    });
  }
  function exportJson() {
    closeMenu();
    var data = { heft: HID, v: 1, t: new Date().toISOString(), f: answers() };
    download(new Blob([JSON.stringify(data, null, 1)], { type: 'application/json' }), fileBase() + '_Antworten.json');
  }
  function importJson(file) {
    closeMenu();
    var rd = new FileReader();
    rd.onload = function () {
      try {
        var d = JSON.parse(rd.result);
        if (!d || !d.f) throw new Error('keine Antworten in der Datei');
        if (d.heft && d.heft !== HID) throw new Error('Die Datei gehört zu einem anderen Heft (' + d.heft + ').');
        if (Object.keys(answers()).length && !confirm('Die Datei ersetzt alle aktuellen Eingaben in diesem Heft. Fortfahren?')) return;
        apply(d.f); save();
        status('ok', 'Antworten aus Datei geladen · gespeichert ' + time(new Date()));
      } catch (e) { alert('Die Datei konnte nicht geladen werden: ' + e.message); }
    };
    rd.readAsText(file);
  }
  function reset() {
    closeMenu();
    if (!confirm('Alle Eingaben in diesem Heft löschen? Das lässt sich nicht rückgängig machen.')) return;
    apply({}); save();
  }
  function toolbar() {
    var q = function (id) { return document.getElementById(id); };
    if (q('wb-pdf')) q('wb-pdf').addEventListener('click', pdf);
    if (q('wb-export')) q('wb-export').addEventListener('click', exportJson);
    if (q('wb-import')) q('wb-import').addEventListener('change', function (e) { if (e.target.files[0]) importJson(e.target.files[0]); e.target.value = ''; });
    if (q('wb-print')) q('wb-print').addEventListener('click', function () { closeMenu(); window.print(); });
    if (q('wb-reset')) q('wb-reset').addEventListener('click', reset);
    if (q('wb-lrn')) q('wb-lrn').addEventListener('click', closeMenu);
    document.addEventListener('click', function (e) { var d = document.querySelector('.wb-more'); if (d && d.open && !d.contains(e.target)) d.open = false; });
  }

  /* ---------- Start ---------- */
  function start() {
    collect();
    window.HEFT = { ready: true, count: fields.length, apply: apply, answers: answers };
    if (PDFMODE) return;
    extras();
    bind();
    toolbar();
    var d = load();
    if (d) { apply(d.f); status('ok', 'Wiederhergestellt · zuletzt ' + new Date(d.t).toLocaleString('de-DE', { dateStyle: 'short', timeStyle: 'short' })); }
    else if (!storageOk) status('warn', 'Speichern im Browser nicht möglich (privates Fenster?) – bitte als PDF oder Datei sichern.');
    // Fortschritt fuer die Uebersicht vermerken (auch ohne Eingaben: Anzahl der Felder)
    try { if (!d) localStorage.setItem(KEY + ':n', String(fields.length)); } catch (e) { /* egal */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
