/* Seite der Schulungsleitung: Anmelden, Fragen sehen (aktualisiert sich alle 15 s), beantworten, erledigen, loeschen. */
(function () {
  'use strict';
  var BASE = '/hefte';
  var NAMES = { carmen: 'Carmen', ingo: 'Ingo', tabea: 'Tabea' };
  var K = window.KURS || {};
  var filter = 'offen', person = '', all = [], known = null, timer = null, drafts = {};
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function api(method, url, body) {
    return fetch(BASE + url, { method: method, credentials: 'same-origin', headers: body ? { 'Content-Type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { if (!r.ok) return r.text().then(function (t) { var e = new Error(t || ('Fehler ' + r.status)); e.status = r.status; throw e; }); return r.json(); });
  }
  function toast(t) { if (K.toast) K.toast(t); }
  function seen() { try { return JSON.parse(localStorage.getItem('kurs:v1:dz-seen') || '[]'); } catch (e) { return []; } }
  function markSeen(id) { try { var s = seen(); if (s.indexOf(id) < 0) { s.push(id); localStorage.setItem('kurs:v1:dz-seen', JSON.stringify(s.slice(-2000))); } } catch (e) { /* egal */ } }

  function showLogin(msg) {
    $('#dz-board').hidden = true;
    var f = $('#dz-login'); f.hidden = false;
    if (msg) { var e = $('.dz-err', f); e.hidden = false; e.textContent = msg; }
    $('#dz-pw').focus();
  }
  function showBoard() {
    $('#dz-login').hidden = true; $('#dz-board').hidden = false;
    load();
    clearInterval(timer);
    timer = setInterval(function () { if (!document.hidden) load(); }, 15000);
  }
  function load() {
    api('GET', '/api/dozent/fragen').then(function (list) {
      var ids = list.map(function (q) { return q.id; });
      if (known) {
        var neu = list.filter(function (q) { return known.indexOf(q.id) < 0 && q.status === 'offen'; });
        neu.forEach(function (q) {
          try { if (window.Notification && Notification.permission === 'granted') new Notification('Neue Frage von ' + (NAMES[q.person] || q.person), { body: q.label + (q.text ? '\n„' + q.text + '“' : ''), tag: 'kurs-' + q.id }); } catch (e) { /* egal */ }
        });
        if (neu.length) toast(neu.length === 1 ? 'Neue Frage von ' + (NAMES[neu[0].person] || neu[0].person) : neu.length + ' neue Fragen');
      }
      known = ids; all = list; render();
      $('#dz-updated').textContent = 'Stand ' + new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' · aktualisiert sich alle 15 Sekunden';
    }).catch(function (e) { if (e.status === 401) { clearInterval(timer); showLogin('Bitte neu anmelden.'); } });
  }
  function counts() {
    var base = all.filter(function (q) { return !person || q.person === person; });
    $('[data-c="offen"]').textContent = base.filter(function (q) { return q.status === 'offen'; }).length;
    $('[data-c="beantwortet"]').textContent = base.filter(function (q) { return q.status !== 'offen'; }).length;
    $('[data-c="alle"]').textContent = base.length;
  }
  function render() {
    counts();
    var ul = $('#dz-list');
    // Entwuerfe offener Antwortfelder retten
    $$('textarea[data-id]', ul).forEach(function (t) { drafts[t.getAttribute('data-id')] = t.value; });
    var focusId = document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute('data-id');
    ul.innerHTML = '';
    var s = seen();
    var list = all.filter(function (q) {
      if (person && q.person !== person) return false;
      if (filter === 'offen') return q.status === 'offen';
      if (filter === 'beantwortet') return q.status !== 'offen';
      return true;
    });
    $('#dz-empty').hidden = !!list.length;
    list.forEach(function (q) {
      var li = el('li', 'dz-item' + (q.status === 'offen' && s.indexOf(q.id) < 0 ? ' neu' : '')); li.id = 'q-' + q.id;
      var h = el('div', 'dz-head');
      h.appendChild(el('span', 'dz-who', NAMES[q.person] || q.person));
      if (q.tag) h.appendChild(el('span', 'dz-tag', 'Tag ' + q.tag));
      h.appendChild(el('span', 'dz-st ' + q.status, q.status === 'offen' ? 'offen' : q.status === 'beantwortet' ? 'beantwortet' : 'erledigt'));
      h.appendChild(el('span', 'dz-time', new Date(q.ts).toLocaleString('de-DE', { weekday: 'short', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })));
      li.appendChild(h);
      var w = el('p', 'dz-where');
      if (q.url && q.url.indexOf(BASE + '/') === 0) { var a = el('a', '', q.label); a.href = q.url; a.target = '_blank'; a.rel = 'noopener'; w.appendChild(a); }
      else w.textContent = q.label;
      li.appendChild(w);
      li.appendChild(el('p', 'dz-text' + (q.text ? '' : ' empty'), q.text || 'Ohne eigenen Text – nur als unklar markiert.'));
      if (q.antwort) { var g = el('div', 'dz-given'); g.appendChild(el('b', '', 'Deine Antwort')); g.appendChild(document.createTextNode(q.antwort)); li.appendChild(g); }
      var ans = el('div', 'dz-ans');
      var ta = el('textarea'); ta.setAttribute('data-id', q.id); ta.maxLength = 2000;
      ta.placeholder = q.antwort ? 'Antwort ändern …' : 'Antwort schreiben – erscheint bei ' + (NAMES[q.person] || q.person) + ' direkt auf der Seite.';
      ta.value = drafts[q.id] != null ? drafts[q.id] : '';
      ta.setAttribute('aria-label', 'Antwort an ' + (NAMES[q.person] || q.person));
      ans.appendChild(ta);
      var acts = el('div', 'dz-acts');
      var send = el('button', 'btn primary', q.antwort ? 'Antwort ändern' : 'Antwort senden'); send.type = 'button';
      send.onclick = function () {
        var t = ta.value.trim(); if (!t) { ta.focus(); return; }
        send.disabled = true;
        api('POST', '/api/dozent/fragen/' + q.id, { antwort: t, status: 'beantwortet' }).then(function () { delete drafts[q.id]; markSeen(q.id); toast('Antwort gesendet.'); load(); })
          .catch(function (e) { send.disabled = false; toast(e.message); });
      };
      acts.appendChild(send);
      var done = el('button', 'btn', q.status === 'offen' ? 'Erledigt (im Kurs geklärt)' : 'Wieder öffnen'); done.type = 'button';
      done.onclick = function () { api('POST', '/api/dozent/fragen/' + q.id, { status: q.status === 'offen' ? 'erledigt' : 'offen' }).then(function () { markSeen(q.id); load(); }).catch(function (e) { toast(e.message); }); };
      acts.appendChild(done);
      var del = el('button', 'btn del', 'Löschen'); del.type = 'button';
      del.onclick = function () { if (!confirm('Diese Frage endgültig löschen?')) return; api('DELETE', '/api/dozent/fragen/' + q.id).then(function () { load(); }).catch(function (e) { toast(e.message); }); };
      acts.appendChild(del);
      ans.appendChild(acts); li.appendChild(ans);
      li.addEventListener('click', function () { if (li.classList.contains('neu')) { li.classList.remove('neu'); markSeen(q.id); } });
      ul.appendChild(li);
    });
    if (focusId) { var f = $('textarea[data-id="' + focusId + '"]', ul); if (f) { f.focus(); f.setSelectionRange(f.value.length, f.value.length); } }
    if (location.hash.indexOf('#q-') === 0) { var t = document.getElementById(location.hash.slice(1)); if (t) { t.scrollIntoView({ block: 'center' }); history.replaceState(null, '', location.pathname); } }
  }

  function start() {
    K = window.KURS || K;
    $('#dz-login').addEventListener('submit', function (e) {
      e.preventDefault();
      var b = $('button', e.target); b.disabled = true;
      api('POST', '/api/dozent/login', { passwort: $('#dz-pw').value }).then(function () { $('#dz-pw').value = ''; showBoard(); })
        .catch(function (err) { showLogin(err.status === 429 ? 'Zu viele Versuche – bitte in ein paar Minuten nochmal.' : err.status === 503 ? err.message : 'Das Passwort stimmt nicht.'); })
        .then(function () { b.disabled = false; });
    });
    $$('[data-f]').forEach(function (b) { b.addEventListener('click', function () { filter = b.getAttribute('data-f'); $$('[data-f]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); render(); }); });
    $$('[data-p]').forEach(function (b) { b.addEventListener('click', function () { person = b.getAttribute('data-p'); $$('[data-p]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); render(); }); });
    $('#dz-logout').addEventListener('click', function () { api('POST', '/api/dozent/logout', {}).then(function () { clearInterval(timer); showLogin(); }); });
    var nb = $('#dz-notify');
    function nstate() {
      if (!window.Notification) { nb.hidden = true; return; }
      nb.textContent = Notification.permission === 'granted' ? 'Browser-Benachrichtigungen sind an' : Notification.permission === 'denied' ? 'Benachrichtigungen im Browser blockiert' : 'Browser-Benachrichtigungen an';
      nb.disabled = Notification.permission !== 'default';
    }
    nb.addEventListener('click', function () { Notification.requestPermission().then(nstate); });
    nstate();
    if (location.hash.indexOf('#q-') === 0) filter = 'alle', $$('[data-f]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-f') === 'alle')); });
    api('GET', '/api/dozent/status').then(function (s) { if (s.dozent) showBoard(); else showLogin(); }).catch(function () { showLogin(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
