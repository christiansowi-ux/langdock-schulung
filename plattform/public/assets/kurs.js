/* Plattform-Seiten: Personenwahl, Kursuebersicht, Tagesseite (Reiter, Learnings, Lernkarten, Selbsttest, Folien, Videos). */
(function () {
  'use strict';
  var BASE = '/hefte';
  var root = document.documentElement;
  var PERSON = root.getAttribute('data-person') || '';
  var TAG = root.getAttribute('data-tag') || '';
  var PAGE = root.getAttribute('data-page') || '';
  root.classList.add('js');
  var K = window.KURS || {};
  var ls = K.ls || function () { return null; };
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function key(tag, what) { return 'kurs:v1:' + PERSON + ':t' + tag + ':' + what; }
  function typing(e) { var t = e.target; return t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)); }
  var ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>';
  var ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>';

  /* ---------- Fortschritt (Uebersicht und Tagesseite) ---------- */
  function progress(tag, total) {
    var sitzt = (ls(key(tag, 'sitzt')) || []).length;
    var test = ls(key(tag, 'test'));
    var heft = null, filled = 0, fields = 0;
    try {
      var raw = localStorage.getItem('hefte:v1:' + PERSON + '/tag-' + tag);
      if (raw) { heft = JSON.parse(raw); filled = heft && heft.f ? Object.keys(heft.f).length : 0; fields = heft.n || 0; }
      if (!fields) fields = +(localStorage.getItem('hefte:v1:' + PERSON + '/tag-' + tag + ':n') || 0);
    } catch (e) { /* kein Speicher */ }
    return {
      sitzt: sitzt, total: total,
      sitztTxt: sitzt + ' von ' + total,
      test: test, testTxt: test ? test.best + ' von ' + test.of + ' richtig' + (test.best === test.of ? ' ✓' : '') : 'noch offen',
      testPct: test ? test.best / test.of : 0,
      heftTxt: filled ? filled + (fields ? ' von ' + fields : '') + ' Feldern ausgefüllt' : 'noch nicht begonnen',
      heftPct: filled && fields ? Math.min(1, filled / fields) : (filled ? .05 : 0)
    };
  }
  function paint(scope, p) {
    function v(n, t) { $$('[data-v="' + n + '"]', scope).forEach(function (e) { e.textContent = t; }); }
    function m(n, x) { $$('[data-m="' + n + '"]', scope).forEach(function (e) { e.style.width = Math.round(x * 100) + '%'; }); }
    v('sitzt', p.sitztTxt); v('test', p.testTxt); v('heft', p.heftTxt);
    m('sitzt', p.total ? p.sitzt / p.total : 0); m('test', p.testPct); m('heft', p.heftPct);
  }

  /* ---------- Startseite ---------- */
  function indexPage() {
    var last = ls('kurs:v1:person');
    var names = K.names || {};
    $$('[data-pick]').forEach(function (a) {
      a.addEventListener('click', function () { ls('kurs:v1:person', a.getAttribute('data-pick')); });
      if (a.getAttribute('data-pick') === last) a.classList.add('last');
    });
    if (last && names[last] && !/wechseln=1/.test(location.search)) {
      var r = $('#resume'); r.hidden = false;
      r.appendChild(el('span', '', 'Zuletzt hier: '));
      r.lastChild.appendChild(el('b', '', names[last]));
      var a = el('a', 'btn primary', 'Weiter als ' + names[last] + ' →'); a.href = BASE + '/' + last + '/';
      r.appendChild(a);
    }
  }

  /* ---------- Kursuebersicht ---------- */
  function todayIso() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function overviewPage() {
    ls('kurs:v1:person', PERSON);
    var today = todayIso();
    $$('.station[data-date]').forEach(function (st) {
      if (st.getAttribute('data-date') === today) { st.classList.add('heute'); var c = $('.chip-heute', st); if (c) c.hidden = false; }
    });
    $$('.station').forEach(function (st) {
      var tag = st.getAttribute('data-tag');
      var total = +(($('[data-v="sitzt"]', st) || {}).textContent || '').replace(/.*von\s+/, '') || 0;
      var p = progress(tag, total);
      paint(st, p);
      if (p.total && p.sitzt === p.total && p.test && p.test.best === p.test.of) st.classList.add('done');
    });
    var box = $('#meine-fragen'); if (!box) return;
    function render() {
      var list = (K.mine ? K.mine() : []).filter(function (q) { return q.person === PERSON; }).slice().reverse();
      var ul = $('.qlist', box); ul.innerHTML = '';
      $('[data-empty]', box).hidden = !!list.length;
      list.slice(0, 30).forEach(function (q) {
        var li = el('li');
        var w = el('span', 'qw');
        var a = el('a', '', (q.tag ? 'Tag ' + q.tag + ' · ' : '') + new Date(q.ts).toLocaleString('de-DE', { weekday: 'short', hour: '2-digit', minute: '2-digit' }));
        if (q.url && q.url.indexOf(BASE + '/') === 0) a.href = q.url; w.appendChild(a); li.appendChild(w);
        li.appendChild(el('span', 'qt', q.label));
        if (q.text) li.appendChild(el('span', 'qw', '„' + q.text + '“'));
        var st = q.status || 'offen';
        li.appendChild(el('span', 'qs ' + st, st === 'beantwortet' ? 'Beantwortet' : st === 'erledigt' ? 'Geklärt' : 'Gemeldet – wartet auf Antwort'));
        if (q.antwort) { var d = el('div', 'qa'); d.appendChild(el('b', '', 'Antwort')); d.appendChild(document.createTextNode(q.antwort)); li.appendChild(d); }
        ul.appendChild(li);
      });
    }
    document.addEventListener('kurs:fragen', render);
    render();
  }

  /* ---------- Tagesseite ---------- */
  var tabs = [], panels = {};
  function showTab(id, focus) {
    if (!panels[id]) id = 'learnings';
    tabs.forEach(function (t) { var on = t.getAttribute('data-tab') === id; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
    Object.keys(panels).forEach(function (k) { panels[k].hidden = k !== id; });
    if (focus) { var nav = $('.tabs-wrap'); var y = nav.getBoundingClientRect().top + window.scrollY; if (window.scrollY > y) window.scrollTo(0, y); }
    document.dispatchEvent(new CustomEvent('kurs:tab', { detail: id }));
  }
  function dayTabs() {
    tabs = $$('[data-tab]');
    tabs.forEach(function (t) {
      panels[t.getAttribute('data-tab')] = document.getElementById(t.getAttribute('data-tab'));
      t.id = 'tab-' + t.getAttribute('data-tab');
      t.setAttribute('aria-controls', t.getAttribute('data-tab'));
      panels[t.getAttribute('data-tab')].setAttribute('aria-labelledby', t.id);
      t.addEventListener('click', function (e) { e.preventDefault(); var id = t.getAttribute('data-tab'); history.replaceState(null, '', '#' + id); showTab(id, true); });
      t.addEventListener('keydown', function (e) {
        var i = tabs.indexOf(t);
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); n.click(); }
        if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); var edge = tabs[e.key === 'Home' ? 0 : tabs.length - 1]; edge.focus(); edge.click(); }
      });
    });
    $$('[data-tab-go]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); history.replaceState(null, '', '#' + a.getAttribute('data-tab-go')); showTab(a.getAttribute('data-tab-go')); var nav = $('.tabs-wrap'); window.scrollTo({ top: nav.getBoundingClientRect().top + window.scrollY, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }); }); });
    function openHash() {
      var h = location.hash.slice(1), section = /^lrn-/.test(h) ? 'learnings' : /^einfach-/.test(h) ? 'einfach' : h;
      if (h && !panels[section]) return;
      showTab(section || 'learnings');
      if (section !== h) { var c = document.getElementById(h); if (c) { c.scrollIntoView({block:'start', behavior:'instant'}); c.tabIndex = -1; c.focus({preventScroll:true}); } }
    }
    showTab('learnings');
    openHash();
    window.addEventListener('hashchange', openHash);
  }

  function dayLearnings() {
    var cards = $$('.lcard');
    var total = cards.length;
    var sitzt = ls(key(TAG, 'sitzt')) || [];
    function refresh() { paint(document, progress(TAG, total)); }
    cards.forEach(function (c) {
      var id = c.getAttribute('data-lrn');
      var b = $('.lc-sitzt', c);
      function set(on) { b.setAttribute('aria-pressed', String(on)); c.classList.toggle('sitzt', on); }
      set(sitzt.indexOf(id) >= 0);
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true';
        sitzt = sitzt.filter(function (x) { return x !== id; }); if (on) sitzt.push(id);
        ls(key(TAG, 'sitzt'), sitzt); set(on); refresh();
        if (on && sitzt.length === total && K.toast) K.toast('Alle ' + total + ' Learnings sitzen. Stark!');
      });
    });
    var selBtn = $('[data-lernblatt-sel]');
    function picked() { return $$('.lc-pick input:checked').map(function (i) { return i.value; }); }
    $$('.lc-pick input').forEach(function (i) {
      i.addEventListener('change', function () { var n = picked().length; selBtn.disabled = !n; selBtn.textContent = n ? 'Auswahl als PDF (' + n + ')' : 'Auswahl als PDF'; });
    });
    if (selBtn) selBtn.addEventListener('click', function () { if (K.pdf) K.pdf(selBtn.getAttribute('data-lernblatt-sel'), picked()); });
    var exp = $('[data-act="expand"]');
    if (exp) exp.addEventListener('click', function () {
      var ds = $$('.lc-more'); var open = ds.some(function (d) { return !d.open; });
      ds.forEach(function (d) { d.open = open; }); exp.textContent = open ? 'Alle zuklappen' : 'Alle aufklappen';
    });
    $$('[data-folie]').forEach(function (a) {
      if (!a.closest('.lcard, .simple-slide')) return;
      a.addEventListener('click', function (e) { e.preventDefault(); history.replaceState(null, '', '?folie=' + a.getAttribute('data-folie') + '#folien'); showTab('folien', true); goSlide(+a.getAttribute('data-folie')); });
    });
    refresh();
  }

  /* Lernkarten */
  function dayDeck() {
    var host = $('[data-deck]'); if (!host) return;
    var src = $$('.karten-src li', host).map(function (li, i) { return { i: i, q: $('b', li).textContent, a: $('span', li).textContent }; });
    var store = key(TAG, 'karten');
    var ui = el('div', 'deck-ui'); host.innerHTML = ''; host.appendChild(ui);
    var order, pos, known, again, flipped;
    function start(list) { order = list.slice(); pos = 0; known = []; again = []; flipped = false; draw(); }
    function draw() {
      ui.innerHTML = '';
      if (pos >= order.length) return end();
      var c = order[pos];
      var top = el('div', 'deck-top');
      top.appendChild(el('span', '', 'Karte ' + (pos + 1) + ' von ' + order.length));
      top.appendChild(el('span', '', known.length + ' gewusst · ' + again.length + ' nochmal'));
      ui.appendChild(top);
      var pr = el('div', 'deck-prog'); var bar = el('i'); bar.style.width = (pos / order.length * 100) + '%'; pr.appendChild(bar); ui.appendChild(pr);
      var card = el('div', 'kcard' + (flipped ? ' flip' : '')); card.tabIndex = 0; card.setAttribute('role', 'button');
      card.setAttribute('aria-label', flipped ? 'Antwort: ' + c.a : 'Frage: ' + c.q + ' – zum Umdrehen tippen');
      var inner = el('div', 'kcard-in');
      var f = el('div', 'kface front'); f.appendChild(el('span', 'kl', 'Frage')); f.appendChild(el('div', 'kt', c.q)); f.appendChild(el('span', 'kh', 'Tippen oder Leertaste zum Umdrehen'));
      var b = el('div', 'kface back'); b.appendChild(el('span', 'kl', 'Antwort')); b.appendChild(el('div', 'kt', c.a)); b.appendChild(el('span', 'kh', 'Gewusst? Ehrlich einsortieren.'));
      inner.appendChild(f); inner.appendChild(b); card.appendChild(inner); ui.appendChild(card);
      card.addEventListener('click', flip);
      card.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); flip(); } });
      var btns = el('div', 'deck-btns');
      if (!flipped) {
        var fb = el('button', 'btn primary', 'Umdrehen'); fb.type = 'button'; fb.onclick = flip; btns.appendChild(fb);
      } else {
        var ag = el('button', 'btn again', 'Nochmal üben'); ag.type = 'button'; ag.onclick = function () { rate(false); };
        var ok = el('button', 'btn primary', 'Gewusst'); ok.type = 'button'; ok.onclick = function () { rate(true); };
        btns.appendChild(ag); btns.appendChild(ok);
      }
      btns.appendChild(el('span', 'sp'));
      var u = el('button', 'unklar', 'Unklar?'); u.type = 'button';
      u.setAttribute('data-unklar-ref', 't' + TAG + ':karte:' + (c.i + 1));
      u.setAttribute('data-unklar-label', 'Lernkarte ' + (c.i + 1) + ': ' + c.q);
      u.setAttribute('data-unklar-hash', '#karten');
      btns.appendChild(u);
      ui.appendChild(btns);
      var hint = el('p', 'kbd-hint'); hint.innerHTML = 'Tastatur: <kbd>Leertaste</kbd> umdrehen · <kbd>1</kbd> nochmal · <kbd>2</kbd> gewusst';
      ui.appendChild(hint);
      if (K.mark) K.mark();
    }
    function flip() {
      flipped = !flipped;
      var card = $('.kcard', ui); card.classList.toggle('flip', flipped);
      setTimeout(draw, 10);
    }
    function rate(ok) { (ok ? known : again).push(order[pos]); pos++; flipped = false; draw(); }
    function end() {
      var s = ls(store) || {}; s.known = known.map(function (c) { return c.i; }); s.t = Date.now(); ls(store, s);
      var box = el('div', 'deck-end');
      box.appendChild(el('h3', '', known.length === order.length ? 'Alle gewusst!' : known.length + ' von ' + order.length + ' gewusst'));
      box.appendChild(el('p', '', again.length ? 'Die ' + again.length + ' Karte' + (again.length === 1 ? '' : 'n') + ' zum Nachüben gleich noch einmal – so bleibt es hängen.' : 'Sehr gut. Morgen kurz wiederholen, dann sitzt es dauerhaft.'));
      var row = el('div', 'btnrow');
      if (again.length) { var a = el('button', 'btn primary', 'Nur die Nochmal-Karten (' + again.length + ')'); a.type = 'button'; var rest = again.slice(); a.onclick = function () { start(rest); }; row.appendChild(a); }
      var m = el('button', 'btn', 'Alle neu gemischt'); m.type = 'button'; m.onclick = function () { start(shuffle(src)); }; row.appendChild(m);
      box.appendChild(row); ui.appendChild(box);
    }
    function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    document.addEventListener('keydown', function (e) {
      if (panels.karten && panels.karten.hidden) return;
      if (typing(e) || e.ctrlKey || e.metaKey || e.altKey || $('.ux-dlg')) return;
      if (e.key === ' ' && pos < order.length) { e.preventDefault(); flip(); }
      else if (flipped && e.key === '1') rate(false);
      else if (flipped && e.key === '2') rate(true);
    });
    start(src);
  }

  /* Selbsttest */
  function dayQuiz() {
    var host = $('[data-quiz]'); if (!host) return;
    var qs = $$('.test-src > li', host).map(function (li, i) {
      var opts = $$('.to li', li);
      return { i: i, q: $('.tq', li).textContent, opts: opts.map(function (o) { return o.textContent; }),
        ok: opts.findIndex(function (o) { return o.hasAttribute('data-ok'); }), why: $('.tw', li).textContent.replace(/^Warum:\s*/, '') };
    });
    var store = key(TAG, 'test');
    var ui = el('div', 'quiz-ui'); host.innerHTML = ''; host.appendChild(ui);
    var pos, res;
    function start() { pos = 0; res = []; draw(); }
    function draw() {
      ui.innerHTML = '';
      if (pos >= qs.length) return end();
      var q = qs[pos];
      var dots = el('div', 'qdots'); dots.setAttribute('aria-hidden', 'true');
      qs.forEach(function (_, i) { dots.appendChild(el('i', i < pos ? (res[i] ? 'ok' : 'bad') : i === pos ? 'cur' : '')); });
      ui.appendChild(dots);
      var card = el('div', 'qcard');
      card.appendChild(el('p', 'qn', 'Frage ' + (pos + 1) + ' von ' + qs.length));
      card.appendChild(el('h3', '', q.q));
      var ul = el('ul', 'qopts');
      var btns = q.opts.map(function (o, j) {
        var li = el('li'), b = el('button', 'qopt'); b.type = 'button';
        b.appendChild(el('span', 'ql', 'ABC'[j])); b.appendChild(el('span', '', o));
        b.onclick = function () { answer(j); };
        li.appendChild(b); ul.appendChild(li); return b;
      });
      card.appendChild(ul);
      var why = el('div', 'qwhy'); why.hidden = true; why.setAttribute('aria-live', 'polite'); card.appendChild(why);
      var foot = el('div', 'qfoot');
      var u = el('button', 'unklar', 'Unklar?'); u.type = 'button';
      u.setAttribute('data-unklar-ref', 't' + TAG + ':test:' + (q.i + 1));
      u.setAttribute('data-unklar-label', 'Selbsttest Frage ' + (q.i + 1) + ': ' + q.q);
      u.setAttribute('data-unklar-hash', '#test');
      foot.appendChild(u); foot.appendChild(el('span', 'sp'));
      var next = el('button', 'btn primary', pos === qs.length - 1 ? 'Ergebnis ansehen' : 'Nächste Frage'); next.type = 'button'; next.hidden = true;
      next.onclick = function () { pos++; draw(); window.scrollTo({ top: $('.tabs-wrap').getBoundingClientRect().top + window.scrollY }); };
      foot.appendChild(next); card.appendChild(foot);
      ui.appendChild(card);
      if (K.mark) K.mark();
      function answer(j) {
        var right = j === q.ok; res[pos] = right;
        btns.forEach(function (b, k) { b.disabled = true; if (k === q.ok) b.classList.add('ok'); else if (k === j) b.classList.add('bad'); });
        why.hidden = false; why.className = 'qwhy ' + (right ? 'ok' : 'bad');
        why.innerHTML = ''; why.appendChild(el('b', '', right ? 'Richtig. ' : 'Nicht ganz. ')); why.appendChild(document.createTextNode(q.why));
        next.hidden = false; next.focus();
      }
    }
    function end() {
      var n = res.filter(Boolean).length;
      var s = ls(store) || { best: 0, of: qs.length };
      s.last = n; s.of = qs.length; s.best = Math.max(s.best || 0, n); s.t = Date.now(); ls(store, s);
      paint(document, progress(TAG, $$('.lcard').length));
      var card = el('div', 'qcard qresult');
      card.appendChild(el('p', 'qn', 'Ergebnis'));
      card.appendChild(el('div', 'big', n + ' / ' + qs.length));
      card.appendChild(el('p', '', n === qs.length ? 'Alles richtig – das sitzt.' : n >= qs.length - 2 ? 'Fast alles richtig. Die falschen Fragen stehen hier noch einmal mit Lösung.' : 'Guter Anfang. Die Learnings oben erklären jede Frage noch einmal in Ruhe.'));
      var wrong = qs.filter(function (_, i) { return !res[i]; });
      if (wrong.length) {
        var ul = el('ul');
        wrong.forEach(function (q) { var li = el('li'); li.appendChild(el('b', '', q.q + ' ')); li.appendChild(document.createTextNode('Richtig: ' + q.opts[q.ok] + ' – ' + q.why)); ul.appendChild(li); });
        card.appendChild(ul);
      }
      var row = el('div', 'btnrow');
      var again = el('button', 'btn primary', 'Nochmal machen'); again.type = 'button'; again.onclick = start; row.appendChild(again);
      var l = el('a', 'btn', 'Zu den Learnings'); l.href = '#learnings'; l.onclick = function (e) { e.preventDefault(); history.replaceState(null, '', '#learnings'); showTab('learnings', true); }; row.appendChild(l);
      card.appendChild(row); ui.appendChild(card);
    }
    start();
  }

  /* Folien */
  var goSlide = function () {};
  function dayViewer() {
    var host = $('[data-viewer]'); if (!host) return;
    var data = JSON.parse($('.v-data', host).textContent);
    var n = data.n, cur = 1;
    var stage = el('div', 'v-stage');
    var img = el('img'); img.alt = ''; img.width = 1600; img.height = Math.round(1600 / data.ratio); img.decoding = 'async';
    stage.appendChild(img);
    var prev = el('button', 'v-nav v-prev'); prev.type = 'button'; prev.innerHTML = ARROW_L; prev.setAttribute('aria-label', 'Vorherige Folie');
    var next = el('button', 'v-nav v-next'); next.type = 'button'; next.innerHTML = ARROW_R; next.setAttribute('aria-label', 'Nächste Folie');
    stage.appendChild(prev); stage.appendChild(next);
    var bar = el('div', 'v-bar');
    var count = el('span', 'v-count'); count.setAttribute('aria-live', 'polite');
    var links = el('div', 'v-links');
    var u = el('button', 'unklar', 'Unklar?'); u.type = 'button';
    var fs = el('button', 'btn ghost', 'Vollbild'); fs.type = 'button'; fs.style.padding = '8px 14px';
    bar.appendChild(count); bar.appendChild(links); bar.appendChild(u);
    if (host.requestFullscreen) bar.appendChild(fs);
    var strip = $('.v-strip', host);
    host.insertBefore(stage, strip); host.insertBefore(bar, strip);
    var thumbs = $$('.v-th', strip);
    thumbs.forEach(function (t) { t.addEventListener('click', function (e) { e.preventDefault(); go(+t.getAttribute('data-n')); }); });
    function src(i) { return BASE + '/folien/tag-' + data.tag + '/' + (i < 10 ? '0' : '') + i + '.jpg'; }
    function go(i) {
      cur = Math.max(1, Math.min(n, i || 1));
      img.src = src(cur); img.alt = 'Folie ' + cur + ' von ' + n;
      count.textContent = 'Folie ' + cur + ' / ' + n;
      prev.disabled = cur === 1; next.disabled = cur === n;
      thumbs.forEach(function (t) { var on = +t.getAttribute('data-n') === cur; t.classList.toggle('on', on); if (on) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
      var th = thumbs[cur - 1]; if (th) strip.scrollTo({ left: th.offsetLeft - strip.clientWidth / 2 + th.clientWidth / 2, behavior: 'smooth' });
      links.innerHTML = '';
      var ls2 = data.links[cur] || data.links[String(cur)] || [];
      if (ls2.length) {
        links.appendChild(el('span', 'lbl', 'Links:'));
        ls2.slice(0, 4).forEach(function (h) { var a = el('a', '', h.replace(/^https?:\/\/(www\.)?/, '')); a.href = h; a.target = '_blank'; a.rel = 'noopener'; a.title = h; links.appendChild(a); });
      }
      u.setAttribute('data-unklar-ref', 't' + data.tag + ':folie:' + cur);
      u.setAttribute('data-unklar-label', 'Folie ' + cur + ' von Tag ' + data.tag);
      u.setAttribute('data-unklar-hash', '?folie=' + cur + '#folien');
      if (K.mark) K.mark();
      [cur - 1, cur + 1].forEach(function (j) { if (j >= 1 && j <= n) { var p = new Image(); p.src = src(j); } });
    }
    goSlide = go;
    prev.onclick = function () { go(cur - 1); };
    next.onclick = function () { go(cur + 1); };
    fs.onclick = function () { if (document.fullscreenElement) document.exitFullscreen(); else host.requestFullscreen().catch(function () {}); };
    document.addEventListener('keydown', function (e) {
      if (panels.folien && panels.folien.hidden) return;
      if (typing(e) || $('.ux-dlg')) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); go(cur + 1); }
    });
    var x0 = null, y0 = null, swiped = false;
    stage.addEventListener('pointerdown', function (e) { x0 = e.clientX; y0 = e.clientY; swiped = false; });
    stage.addEventListener('pointerup', function (e) {
      if (x0 == null) return;
      var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { swiped = true; go(cur + (dx < 0 ? 1 : -1)); }
    });
    img.addEventListener('click', function (e) {
      if (swiped) { swiped = false; return; }
      var r = img.getBoundingClientRect(); go(cur + (e.clientX - r.left > r.width / 2 ? 1 : -1));
    });
    var m = location.search.match(/[?&]folie=(\d+)/);
    go(m ? +m[1] : (ls(key(data.tag, 'folie')) || data.start || 1));
    var saveT; img.addEventListener('load', function () { clearTimeout(saveT); saveT = setTimeout(function () { ls(key(data.tag, 'folie'), cur); }, 400); });
    // Videos: erst nach Klick laden (YouTube ohne Cookies)
    $$('.video[data-yt]').forEach(function (v) {
      var b = $('.v-load', v);
      b.addEventListener('click', function () {
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + v.getAttribute('data-yt') + '?autoplay=1&rel=0&cc_load_policy=1&hl=de&cc_lang_pref=de';
        f.title = $('.v-meta b', v).textContent; f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true;
        f.referrerPolicy = 'strict-origin-when-cross-origin';
        b.replaceWith(f);
      });
    });
  }

  function dayHeft() {
    var lg = $('[data-legacy]');
    if (lg) {
      try {
        var raw = localStorage.getItem('hefte:v1:' + lg.getAttribute('data-legacy'));
        var d = raw && JSON.parse(raw);
        if (d && d.f && Object.keys(d.f).length) lg.hidden = false;
      } catch (e) { /* egal */ }
    }
  }

  function dayPage() {
    ls('kurs:v1:person', PERSON);
    dayTabs();
    dayLearnings();
    dayDeck();
    dayQuiz();
    dayViewer();
    dayHeft();
    $$('.lc-thumb').forEach(function (t) {
      t.addEventListener('click', function () { history.replaceState(null, '', '?folie=' + t.getAttribute('data-folie') + '#folien'); showTab('folien', true); goSlide(+t.getAttribute('data-folie')); });
    });
    if (/[?&]folie=\d+/.test(location.search) && location.hash === '#folien') showTab('folien');
  }

  function start() {
    K = window.KURS || K; ls = K.ls || ls;
    if (PAGE === 'index') indexPage();
    else if (PAGE === 'overview') overviewPage();
    else if (PAGE === 'day') dayPage();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
