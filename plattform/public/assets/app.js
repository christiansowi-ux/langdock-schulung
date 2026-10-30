/* Gemeinsam fuer alle Seiten: "Unklar?" melden (mit Antwort-Anzeige), Glocke der Schulungsleitung, Folien-Verweise,
   Learnings einzeln als PDF (Heft und Lernblatt). Beim serverseitigen PDF-Export (?pdf=1) nur die Lernblatt-Auswahl. */
(function () {
  'use strict';
  var BASE = '/hefte';
  var root = document.documentElement;
  var PERSON = root.getAttribute('data-person') || '';
  var TAG = root.getAttribute('data-tag') || '';
  var PAGE = root.getAttribute('data-page') || '';
  var PDFMODE = /[?&]pdf=1/.test(location.search);
  var NAMES = { carmen: 'Carmen', ingo: 'Ingo', tabea: 'Tabea' };
  var FKEY = 'kurs:v1:fragen';
  // Neue Adressen seit 30.10.2026: Modul 1 = Tag 1–19, Modul 2 = interne Tage 20–24 (Tag 1–5)
  function dayUrl(tag, person) { tag = +tag; return BASE + '/' + (person || PERSON) + '/' + (tag <= 19 ? 'modul-1/tag-' + tag : 'modul-2/tag-' + (tag - 19)) + '/'; }
  var BELL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 1 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>';

  /* ---------- Hilfen ---------- */
  function ls(k, v) {
    try {
      if (arguments.length === 1) { var r = localStorage.getItem(k); return r ? JSON.parse(r) : null; }
      if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
    return v;
  }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function api(method, url, body) {
    return fetch(BASE + url, {
      method: method, credentials: 'same-origin',
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      var ct = r.headers.get('Content-Type') || '';
      if (!r.ok) return r.text().then(function (t) { var e = new Error(t || ('Fehler ' + r.status)); e.status = r.status; throw e; });
      return ct.indexOf('json') >= 0 ? r.json() : r;
    });
  }
  var toastTimer;
  function toast(msg, action, ms) {
    var old = $('.ux-toast'); if (old) old.remove();
    clearTimeout(toastTimer);
    var t = el('div', 'ux-toast'); t.setAttribute('role', 'status');
    t.appendChild(el('span', '', msg));
    if (action) { var b = el('button', '', action.label); b.type = 'button'; b.onclick = function () { t.remove(); action.fn(); }; t.appendChild(b); }
    document.body.appendChild(t);
    toastTimer = setTimeout(function () { t.remove(); }, ms || 5200);
  }
  function download(blob, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
  }
  function timeAgo(ts) {
    var d = new Date(ts);
    return d.toLocaleString('de-DE', { weekday: 'short', hour: '2-digit', minute: '2-digit' });
  }

  /* ---------- Eigene Fragen ---------- */
  function mine() { return ls(FKEY) || []; }
  function saveMine(list) { ls(FKEY, list.slice(-200)); }
  function latestFor(ref) {
    var list = mine(), hit = null;
    for (var i = 0; i < list.length; i++) if (list[i].ref === ref && list[i].person === PERSON) hit = list[i];
    return hit;
  }
  function markButtons() {
    $$('.unklar[data-unklar-ref]').forEach(function (b) {
      var q = latestFor(b.getAttribute('data-unklar-ref'));
      b.classList.toggle('sent', !!q && q.status !== 'beantwortet');
      b.classList.toggle('answered', !!q && q.status === 'beantwortet');
      b.textContent = !q ? 'Unklar?' : q.status === 'beantwortet' ? 'Antwort da' : q.status === 'erledigt' ? 'Geklärt' : 'Gemeldet';
      b.title = !q ? 'Als unklar melden – die Schulungsleitung sieht es sofort' : q.status === 'beantwortet' ? 'Antwort lesen' : 'Schon gemeldet – noch einmal öffnen';
    });
  }
  var refreshing = false;
  function refreshMine(first) {
    var list = mine();
    if (!list.length || refreshing) { fire(); return; }
    refreshing = true;
    var ids = list.slice(-100).map(function (q) { return q.id; }).join(',');
    api('GET', '/api/fragen?ids=' + encodeURIComponent(ids)).then(function (res) {
      var byId = {}; (res || []).forEach(function (r) { byId[r.id] = r; });
      var fresh = [];
      list.forEach(function (q) {
        var r = byId[q.id];
        if (!r) { q.gone = true; return; }
        q.gone = false;
        if (r.status === 'beantwortet' && q.antwort !== r.antwort && !q.gelesen) fresh.push(q);
        q.status = r.status; q.antwort = r.antwort || ''; q.antwortTs = r.antwortTs || 0;
      });
      saveMine(list.filter(function (q) { return !q.gone; }));
      markButtons(); fire();
      var own = fresh.filter(function (q) { return q.person === PERSON || !PERSON; });
      if (own.length) toast('Neue Antwort der Schulungsleitung: „' + own[0].label.slice(0, 70) + '“', { label: 'Lesen', fn: function () { showAnswer(own[0]); } }, 9000);
    }).catch(function () { /* offline: spaeter nochmal */ }).then(function () { refreshing = false; });
  }
  function fire() { try { document.dispatchEvent(new CustomEvent('kurs:fragen')); } catch (e) { /* alt */ } }

  /* ---------- Dialog ---------- */
  function dialog(build) {
    var d = el('div', 'ux-dlg'); d.setAttribute('role', 'dialog'); d.setAttribute('aria-modal', 'true');
    var box = el('div', 'ux-box'); d.appendChild(box);
    var last = document.activeElement;
    function close() { d.remove(); document.removeEventListener('keydown', onKey); if (last && last.focus) last.focus(); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    d.addEventListener('mousedown', function (e) { if (e.target === d) close(); });
    document.addEventListener('keydown', onKey);
    build(box, close);
    document.body.appendChild(d);
    var f = box.querySelector('textarea, .ux-btn.primary, .ux-btn'); if (f) f.focus();
    return close;
  }
  function openUnklar(btn) {
    var ref = btn.getAttribute('data-unklar-ref'), label = btn.getAttribute('data-unklar-label') || ref;
    var q = latestFor(ref);
    if (q && q.status === 'beantwortet') return showAnswer(q);
    dialog(function (box, close) {
      var h = el('h2', '', q ? 'Schon gemeldet' : 'Was ist unklar?');
      var w = el('p', 'ux-where'); w.appendChild(document.createTextNode('Stelle: ')); w.appendChild(el('b', '', label));
      box.appendChild(h); box.appendChild(w);
      if (q) {
        box.appendChild(el('p', 'ux-mine', q.status === 'erledigt' ? 'Die Schulungsleitung hat das als geklärt markiert (z. B. im Kurs besprochen).' : 'Die Frage ist angekommen. Die Antwort erscheint hier und auf der eigenen Übersichtsseite.'));
        if (q.text) box.appendChild(el('p', 'ux-mine', '„' + q.text + '“'));
      }
      var lab = el('label', '', q ? 'Noch etwas ergänzen? (freiwillig)' : 'Was genau? (freiwillig)'); lab.htmlFor = 'ux-text';
      var ta = el('textarea'); ta.id = 'ux-text'; ta.maxLength = 1000;
      ta.placeholder = 'Zum Beispiel: Ich verstehe nicht, warum …';
      box.appendChild(lab); box.appendChild(ta);
      box.appendChild(el('p', 'ux-hint', 'Die Schulungsleitung sieht die Meldung sofort – mit Vornamen und dieser Stelle. Keine echten Kundendaten eintragen.'));
      var row = el('div', 'ux-row');
      var cancel = el('button', 'ux-btn', 'Abbrechen'); cancel.type = 'button'; cancel.onclick = close;
      var send = el('button', 'ux-btn primary', q ? 'Nochmal melden' : 'Als unklar melden'); send.type = 'button';
      send.onclick = function () {
        send.disabled = true; send.textContent = 'Wird gesendet …';
        api('POST', '/api/fragen', { person: PERSON, tag: +TAG || 0, ref: ref, label: label, text: ta.value.trim(), url: location.pathname + (btn.getAttribute('data-unklar-hash') || '') })
          .then(function (r) {
            var list = mine();
            list.push({ id: r.id, ref: ref, label: label, text: ta.value.trim(), person: PERSON, tag: +TAG || 0, ts: Date.now(), status: 'offen', url: location.pathname + (btn.getAttribute('data-unklar-hash') || '') });
            saveMine(list); markButtons(); fire(); close();
            toast('Ist angekommen – die Schulungsleitung sieht es jetzt.');
          })
          .catch(function (e) { send.disabled = false; send.textContent = 'Nochmal versuchen'; toast(String(e.message || e).slice(0, 160)); });
      };
      row.appendChild(cancel); row.appendChild(send); box.appendChild(row);
    });
  }
  function showAnswer(q) {
    dialog(function (box, close) {
      box.appendChild(el('h2', '', 'Antwort der Schulungsleitung'));
      var w = el('p', 'ux-where'); w.appendChild(document.createTextNode('Zu: ')); w.appendChild(el('b', '', q.label)); box.appendChild(w);
      if (q.text) box.appendChild(el('p', 'ux-mine', 'Eigene Frage: „' + q.text + '“'));
      var a = el('div', 'ux-answer'); a.appendChild(el('b', '', 'Antwort')); a.appendChild(document.createTextNode(q.antwort || '')); box.appendChild(a);
      var row = el('div', 'ux-row');
      var ok = el('button', 'ux-btn primary', 'Verstanden'); ok.type = 'button'; ok.onclick = close;
      row.appendChild(ok); box.appendChild(row);
      var list = mine(); list.forEach(function (x) { if (x.id === q.id) x.gelesen = true; }); saveMine(list);
    });
  }

  /* ---------- Heft: "Unklar?" an jedem Schritt ---------- */
  function heftButtons() {
    $$('.task, .zusatz').forEach(function (box) {
      var isZ = box.classList.contains('zusatz');
      var noEl = isZ ? null : box.querySelector('.task-no');
      var no = isZ ? box.getAttribute('data-zusatz') : (noEl ? noEl.textContent.replace(/\D+/g, '') : '');
      var title = box.querySelector('.task-head h3');
      var what = (isZ ? 'Zusatzaufgabe ' : 'Aufgabe ') + no;
      var steps = $$('.step-t', box).filter(function (s) { return s.closest('.task, .zusatz') === box; });
      if (!steps.length && title) steps = [null];
      steps.forEach(function (st) {
        var n = st ? (st.querySelector('.n') || {}).textContent : '';
        var id = 'u-' + (isZ ? 'z' : 'a') + no + (n ? 's' + n : '');
        var b = el('button', 'unklar', 'Unklar?'); b.type = 'button';
        b.setAttribute('data-unklar-ref', 't' + TAG + ':heft:' + id.slice(2));
        var stText = st ? st.cloneNode(true) : null;
        if (stText) $$('.n, .where, .unklar', stText).forEach(function (x) { x.remove(); });
        b.setAttribute('data-unklar-label', 'Arbeitsheft · ' + what + (title ? ' „' + title.textContent.trim() + '“' : '') + (n ? ' · Schritt ' + n + ': ' + stText.textContent.trim() : ''));
        b.setAttribute('data-unklar-hash', '#' + id);
        var host = st || box.querySelector('.task-head');
        host.id = host.id || id;
        host.appendChild(b);
      });
    });
  }

  /* ---------- Folien-Verweise ---------- */
  function frefLinks() {
    $$('.fref').forEach(function (s) {
      if (s.classList.contains('aus') || s.tagName === 'A') return;
      var n = s.getAttribute('data-folie') || (s.textContent.match(/\d+/) || [])[0];
      var sec = s.closest('[data-lrn-tag]');
      var tag = sec ? sec.getAttribute('data-lrn-tag') : TAG;
      if (!n || !tag || !PERSON || s.closest('.legend')) return;
      var a = el('a', s.className, s.textContent);
      a.href = dayUrl(tag) + '?folie=' + n + '#folien';
      a.title = 'Folie ' + n + ' ansehen';
      s.parentNode.replaceChild(a, s);
    });
  }

  /* ---------- Learnings als PDF ---------- */
  var pdfBusy = false;
  function lernblattPdf(key, ids) {
    if (pdfBusy) return;
    pdfBusy = true;
    toast('PDF wird erstellt – einen Moment …', null, 30000);
    var name = 'Learnings_' + key.replace(/[^\w-]+/g, '_');
    fetch(BASE + '/api/pdf', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ lernblatt: key, ids: ids || [] }) })
      .then(function (r) {
        if (!r.ok) return r.text().then(function (t) { throw new Error(t || ('Fehler ' + r.status)); });
        var cd = r.headers.get('Content-Disposition') || '';
        var m = cd.match(/filename="([^"]+)"/); if (m) name = m[1].replace(/\.pdf$/, '');
        return r.blob();
      })
      .then(function (b) { download(b, name + '.pdf'); toast('Fertig – das PDF liegt im Download-Ordner.'); })
      .catch(function (e) { toast('Das PDF ging gerade nicht: ' + String(e.message || e).slice(0, 120)); })
      .then(function () { pdfBusy = false; });
  }
  function heftLearnings() {
    var sec = $('.lrn-section'); if (!sec) return;
    var tag = sec.getAttribute('data-lrn-tag');
    var tools = $('.lrn-tools', sec);
    var items = $$('ol.lrn > li', sec);
    var txt = el('span', 'lt-txt', 'Einzelne Learnings anhaken und als eigenes Lernblatt speichern – oder alle auf einmal.');
    var all = el('button', 'primary', 'Alle als PDF'); all.type = 'button';
    var sel = el('button', '', 'Auswahl als PDF'); sel.type = 'button'; sel.disabled = true;
    tools.appendChild(txt); tools.appendChild(all); tools.appendChild(sel);
    function picked() { return items.filter(function (li) { return li.classList.contains('picked'); }).map(function (li) { return li.getAttribute('data-lrn'); }); }
    items.forEach(function (li, i) {
      var ctl = el('div', 'lrn-ctl');
      var lab = el('label'); var cb = el('input'); cb.type = 'checkbox';
      lab.appendChild(cb); lab.appendChild(document.createTextNode(' fürs Lernblatt'));
      cb.addEventListener('change', function () {
        li.classList.toggle('picked', cb.checked);
        var n = picked().length; sel.disabled = !n; sel.textContent = n ? 'Auswahl als PDF (' + n + ')' : 'Auswahl als PDF';
      });
      var b = el('button', 'unklar', 'Unklar?'); b.type = 'button';
      b.setAttribute('data-unklar-ref', 't' + tag + ':learning:' + li.getAttribute('data-lrn'));
      b.setAttribute('data-unklar-label', 'Learning ' + (i + 1) + ': ' + $('.lrn-satz', li).textContent);
      ctl.appendChild(lab); ctl.appendChild(b);
      $('.lrn-body', li).appendChild(ctl);
    });
    all.onclick = function () { lernblattPdf(PERSON + '/tag-' + tag, []); };
    sel.onclick = function () { lernblattPdf(PERSON + '/tag-' + tag, picked()); };
  }
  function lernblattFilter() {
    if (PAGE !== 'lernblatt') return;
    var m = location.search.match(/[?&]ids=([^&]*)/);
    var ids = m ? decodeURIComponent(m[1]).split(',').filter(Boolean) : [];
    if (ids.length) {
      $$('ol.lrn > li').forEach(function (li) { if (ids.indexOf(li.getAttribute('data-lrn')) < 0) li.classList.add('off'); });
      var s = $('.lb-sel'); if (s) { s.hidden = false; s.textContent = 'Ausgewählt: ' + ids.length + ' Learnings'; }
    }
    window.LERNBLATT = { ready: true, ids: ids };
  }

  /* ---------- Glocke der Schulungsleitung ---------- */
  function bell() {
    var slot = document.getElementById('dz-slot');
    if (!slot || PAGE === 'dozent') return;
    var lastCount = null, wrap = null;
    function render(st) {
      if (!st || !st.dozent) { if (wrap) { wrap.remove(); wrap = null; } return; }
      if (!wrap) {
        wrap = el('div', 'dz-bell');
        var b = el('button'); b.type = 'button'; b.setAttribute('aria-haspopup', 'true'); b.setAttribute('aria-expanded', 'false');
        b.innerHTML = BELL_SVG + '<span class="lbl">Fragen</span><span class="badge"></span>';
        var pop = el('div', 'dz-pop'); pop.hidden = true;
        b.onclick = function (e) { e.stopPropagation(); pop.hidden = !pop.hidden; b.setAttribute('aria-expanded', String(!pop.hidden)); };
        document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) { pop.hidden = true; b.setAttribute('aria-expanded', 'false'); } });
        wrap.appendChild(b); wrap.appendChild(pop); slot.appendChild(wrap);
      }
      var badge = $('.badge', wrap);
      badge.textContent = st.offen; badge.classList.toggle('zero', !st.offen);
      $('button', wrap).setAttribute('aria-label', st.offen + ' offene Fragen');
      var pop2 = $('.dz-pop', wrap); pop2.innerHTML = '';
      pop2.appendChild(el('h3', '', st.offen ? st.offen + ' offene Frage' + (st.offen === 1 ? '' : 'n') : 'Keine offenen Fragen'));
      var ul = el('ul');
      (st.neu || []).forEach(function (q) {
        var li = el('li'), a = el('a'); a.href = BASE + '/dozent/#q-' + q.id;
        var head = el('b', '', (NAMES[q.person] || q.person) + (q.tag ? ' · Tag ' + q.tag : ''));
        a.appendChild(head); a.appendChild(el('span', 'w', q.label + ' · ' + timeAgo(q.ts)));
        if (q.text) a.appendChild(el('span', 't', '„' + q.text.slice(0, 140) + '“'));
        li.appendChild(a); ul.appendChild(li);
      });
      pop2.appendChild(ul);
      var all = el('a', 'all', 'Alle Fragen beantworten →'); all.href = BASE + '/dozent/'; pop2.appendChild(all);
      if (lastCount != null && st.offen > lastCount) {
        wrap.classList.remove('ring'); void wrap.offsetWidth; wrap.classList.add('ring');
        var q0 = (st.neu || [])[0];
        toast('Neue Frage' + (q0 ? ' von ' + (NAMES[q0.person] || q0.person) + ': „' + q0.label.slice(0, 60) + '“' : ''), { label: 'Ansehen', fn: function () { location.href = BASE + '/dozent/'; } }, 9000);
        try { if (window.Notification && Notification.permission === 'granted' && q0) new Notification('Neue Frage von ' + (NAMES[q0.person] || q0.person), { body: q0.label + (q0.text ? '\n„' + q0.text + '“' : ''), tag: 'kurs-' + q0.id }); } catch (e) { /* egal */ }
      }
      document.title = document.title.replace(/^\(\d+\) /, '');
      if (st.offen) document.title = '(' + st.offen + ') ' + document.title;
      lastCount = st.offen;
    }
    function poll() { api('GET', '/api/dozent/status').then(render).catch(function () { /* offline */ }); }
    poll();
    setInterval(function () { if (!document.hidden) poll(); }, 20000);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) poll(); });
  }

  /* ---------- Lernheft: Uebungs-Prompts kopieren ---------- */
  function copyButtons(scope, sel) {
    [].forEach.call((scope || document).querySelectorAll(sel || '.ucode'), function (box) {
      var text = box.innerText.trim() || box.textContent.trim();
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'ucopy'; b.textContent = 'Kopieren';
      b.setAttribute('aria-label', 'Prompt kopieren');
      b.addEventListener('click', function () {
        function done() { b.textContent = 'Kopiert'; b.classList.add('done'); setTimeout(function () { b.textContent = 'Kopieren'; b.classList.remove('done'); }, 1800); }
        function fallback() {
          var t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
          document.body.appendChild(t); t.select();
          try { document.execCommand('copy'); done(); } catch (e) { /* nichts */ }
          document.body.removeChild(t);
        }
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
      });
      box.appendChild(b);
    });
  }

  window.KURS_COPY = copyButtons;  // auch fuer aufgaben.js

  /* ---------- Start ---------- */
  function start() {
    if (PDFMODE) { lernblattFilter(); return; }
    if (PAGE === 'heft') { heftButtons(); heftLearnings(); }
    if (PAGE === 'lernblatt') lernblattFilter();
    if (PAGE === 'lernheft') { copyButtons(); copyButtons(document, '.reg code'); }
    frefLinks();
    document.addEventListener('click', function (e) {
      var u = e.target.closest && e.target.closest('.unklar[data-unklar-ref]');
      if (u) { e.preventDefault(); if (!PERSON) return; openUnklar(u); return; }
      var lb = e.target.closest && e.target.closest('[data-lernblatt]');
      if (lb) { e.preventDefault(); lernblattPdf(lb.getAttribute('data-lernblatt'), []); return; }
      var here = e.target.closest && e.target.closest('[data-lernblatt-here]');
      if (here) { e.preventDefault(); lernblattPdf(here.getAttribute('data-lernblatt-here'), (window.LERNBLATT && window.LERNBLATT.ids) || []); }
    });
    markButtons();
    refreshMine(true);
    setInterval(function () { if (!document.hidden) refreshMine(); }, 45000);
    bell();
    window.KURS = { dayUrl: dayUrl, mine: mine, mark: markButtons, refresh: refreshMine, pdf: lernblattPdf, toast: toast, showAnswer: showAnswer, ls: ls, api: api, names: NAMES };
    fire();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
