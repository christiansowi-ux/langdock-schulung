/* Aufgabengenerator: freiwillige Uebungsaufgaben aus dem Lernstoff, im Browser zufaellig gemischt.
   Daten: aufgaben.json (aus _quellen/aufgaben.py). Eine Aufgabe = Muster x Firma x Seed; die Nummer (z. B. t6-fehler.w2.4711)
   baut genau dieselbe Aufgabe wieder auf (?aufgabe=...). Zwei Modi: Kurzaufgaben (5-10 Min) und Deep Learn (60 Min, 5 Etappen,
   Stunden-Uhr, Etappen abhaken). Fortschritt nur im Browser (localStorage). */
(function () {
  'use strict';
  var root = document.documentElement;
  var PERSON = root.getAttribute('data-person') || '';
  var BASE = '/hefte';
  var DATA = null, loading = null, cur = null, recent = [], tick = null;
  var DICE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
    + '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><circle cx="8.5" cy="8.5" r="1.3" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.3" fill="currentColor"/>'
    + '<circle cx="15.5" cy="8.5" r="1.3" fill="currentColor"/><circle cx="8.5" cy="15.5" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/></svg>';

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* privat */ } }
  function key(what) { return 'aufg:v1:' + PERSON + ':' + what; }

  /* ---------- Zufall mit Seed (gleiche Nummer = gleiche Aufgabe) ---------- */
  function rng(seed) {
    var a = seed >>> 0;
    return function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function euro(c) { return (c / 100).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €'; }
  function zahl(n) { return n.toLocaleString('de-DE'); }
  function mmss(ms) { var s = Math.max(0, Math.floor(ms / 1000)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }

  /* ---------- Rechenaufgaben: Zahlen aus dem Seed, Loesung wird mitgerechnet ---------- */
  function rechnen(kind, r, lage, b, s) {
    if (kind === 'kunden') {
      var n = pick(r, [120, 160, 200, 240, 280, 320, 360, 400]), p = pick(r, [10, 15, 20, 25]), q = pick(r, [5, 10, 15, 20]);
      if (q === p) q = p - 5;
      var pn = n * p / 100, qn = n * q / 100, res = n - pn + qn;
      s.r_frage = lage.firma + ' hat ' + zahl(n) + ' ' + lage.kunden_wort + '. ' + p + ' % davon hören in diesem Jahr auf, und ' + q
        + ' % (gerechnet von den ' + zahl(n) + ') kommen neu dazu. Wie viele sind es am Ende des Jahres?';
      s.r_weg = p + ' % von ' + zahl(n) + ' sind ' + zahl(pn) + ', ' + q + ' % von ' + zahl(n) + ' sind ' + zahl(qn) + '. Rechnung: '
        + zahl(n) + ' − ' + zahl(pn) + ' + ' + zahl(qn) + ' = ' + zahl(res) + '. Richtig ist also: ' + zahl(res) + '.';
    } else if (kind === 'vram') {
      var pb = pick(r, [7, 8, 13, 24, 32, 70]), gpu = pick(r, [12, 16, 24, 48, 80]);
      var gb = function (v) { return v.toLocaleString('de-DE', { maximumFractionDigits: 1 }); };
      var need = [[16, pb * 2], [8, pb], [4, pb * 0.5]];
      var fits = need.filter(function (x) { return x[1] * 1.2 <= gpu; }).map(function (x) { return x[0] + ' Bit'; });
      s.r_frage = 'Ein Sprachmodell hat ' + pb + ' Milliarden Parameter. Wie viel Grafikspeicher brauchen allein die Gewichte in 16, 8 und 4 Bit – und in welcher '
        + 'Variante passt es auf eine Grafikkarte mit ' + gpu + ' GB? Faustregel: 16 Bit ≈ 2 GB je Milliarde Parameter, für den Betrieb rund 20 % Puffer einplanen.';
      s.r_weg = need.map(function (x) { return x[0] + ' Bit: ' + gb(x[1]) + ' GB (mit Puffer ' + gb(x[1] * 1.2) + ' GB)'; }).join(' · ') + '. '
        + (fits.length ? 'Auf ' + gpu + ' GB passt: ' + fits.join(', ') + '.' : 'Auf ' + gpu + ' GB passt keine Variante – mehrere Grafikkarten oder ein kleineres Modell nötig.');
    } else if (kind === 'kosten') {
      var np = pick(r, [50, 100, 150, 200, 300]), seat = pick(r, [20, 25, 30, 40]), kap = pick(r, [60000, 90000, 120000]);
      var strom = pick(r, [2000, 3000, 5000]), pers = pick(r, [15000, 25000, 40000]);
      var a1 = np * seat * 12, abschr = Math.round(kap / 3), b1 = abschr + strom + pers, be = Math.ceil(b1 / (seat * 12));
      var eur = function (v) { return zahl(v) + ' €'; };
      s.r_frage = 'Angenommen, bei ' + lage.firma + ' sollen ' + zahl(np) + ' Personen KI nutzen. Weg A: eine Managed-Plattform für ' + seat + ' € pro Person und Monat. '
        + 'Weg B: eigene Server für ' + eur(kap) + ' (über 3 Jahre abgeschrieben), dazu ' + eur(strom) + ' Strom und ' + eur(pers) + ' Personal pro Jahr. '
        + 'Welcher Weg ist pro Jahr günstiger – und ab wie vielen Personen lohnt sich Weg B? (Alle Zahlen ausgedacht.)';
      s.r_weg = 'Weg A: ' + zahl(np) + ' × ' + seat + ' € × 12 = ' + eur(a1) + ' pro Jahr. Weg B: Abschreibung ' + eur(kap) + ' ÷ 3 = ' + eur(abschr) + '; '
        + eur(abschr) + ' + ' + eur(strom) + ' + ' + eur(pers) + ' = ' + eur(b1) + ' pro Jahr. Günstiger: ' + (a1 < b1 ? 'Weg A (Managed)' : a1 > b1 ? 'Weg B (eigene Server)' : 'beide gleich') + '. '
        + 'Break-Even: ' + eur(b1) + ' ÷ (' + seat + ' € × 12) = ab ' + zahl(be) + ' Personen lohnt sich Weg B.';
    } else if (kind === 'rabatt') {
      var x = b.rabatt, c = pick(r, x.cents), m = pick(r, x.mengen);
      var sub = m * c, rate = m >= x.s2 ? x.r2 : (m >= x.s1 ? x.r1 : 0);
      var minus = Math.round(sub * rate / 100), after = sub - minus, fee = after >= x.frei ? 0 : x.fee, total = after + fee;
      s.r_frage = x.einzel + ' kostet ' + euro(c) + '. Ab ' + zahl(x.s1) + ' ' + x.mass + ' gibt es ' + x.r1 + ' % Rabatt, ab ' + zahl(x.s2) + ' ' + x.mass + ' '
        + x.r2 + ' % (es zählt nur die höhere Stufe). Dazu kommen ' + euro(x.fee) + ' ' + x.fee_wofuer + ' – diese Kosten entfallen, wenn der Betrag nach Rabatt mindestens '
        + euro(x.frei) + ' beträgt. Was kostet eine Bestellung von ' + zahl(m) + ' ' + x.mass + '?';
      s.r_weg = zahl(m) + ' × ' + euro(c) + ' = ' + euro(sub) + '. '
        + (rate ? 'Ab ' + zahl(rate === x.r2 ? x.s2 : x.s1) + ' ' + x.mass + ' gilt ' + rate + ' % Rabatt: ' + euro(sub) + ' − ' + euro(minus) + ' = ' + euro(after) + '. '
          : 'Unter ' + zahl(x.s1) + ' ' + x.mass + ' gibt es keinen Rabatt. ')
        + (fee ? euro(after) + ' liegt unter ' + euro(x.frei) + ', also kommen ' + euro(fee) + ' dazu. ' : euro(after) + ' erreicht ' + euro(x.frei) + ', die Zusatzkosten entfallen. ')
        + 'Ergebnis: ' + euro(total) + '.';
    }
  }

  /* ---------- Eine Aufgabe zusammenbauen ---------- */
  function musterById(id) {
    if (id.indexOf('dl-') === 0) {
      var d = DATA.deep.filter(function (x) { return x.id === id; })[0];
      return d && DATA.tage[String(d.tag)] ? { m: d, tag: String(d.tag), deep: true, key: id } : null;
    }
    var g = id.split('~');
    var m = (g.length > 1 ? DATA.generisch : DATA.muster).filter(function (x) { return x.id === g[0]; })[0];
    if (!m) return null;
    var tag = g.length > 1 ? g[1] : String(m.tag);
    return DATA.tage[tag] ? { m: m, tag: tag, gen: g.length > 1, key: id } : null;
  }
  function build(code) {
    var parts = String(code || '').split('.');
    if (parts.length !== 3) return null;
    var mm = musterById(parts[0]);
    var lage = DATA.lagen.filter(function (l) { return l.id === parts[1]; })[0];
    var seed = parseInt(parts[2], 10);
    if (!mm || !lage || !(seed > 0)) return null;
    var r = rng(seed), b = DATA.bereiche[lage.bereich], s = {};
    Object.keys(b).forEach(function (k) { if (typeof b[k] === 'string') s[k] = b[k]; });
    Object.keys(lage).forEach(function (k) { if (typeof lage[k] === 'string') s[k] = lage[k]; });
    s.fakten = lage.fakten.join(', ');
    s.notizen_liste = lage.notizen.map(function (x) { return '- ' + x; }).join('\n');
    s.doc = 'Infoblatt ' + lage.firma + ' (Stand: Januar 2026)\nAngebot: ' + lage.leistung + '\nPreis: ' + lage.preis + '\nDauer: ' + lage.lieferzeit + '\nVorteil: ' + lage.vorteil;
    var T = DATA.tage[mm.tag];
    s.tag = mm.tag; s.tagtitel = T.titel;
    var li = Math.floor(r() * T.learnings.length);
    s.satz = T.learnings[li][1]; s.lrn_nr = String(li + 1);
    if (mm.m.rechnen) rechnen(mm.m.rechnen, r, lage, b, s);
    var learn = mm.deep ? mm.m.learn : (mm.gen ? [[mm.tag, T.learnings[li][0]]] : mm.m.learn.map(function (id) { return [mm.tag, id]; }));
    return { code: code, m: mm.m, tag: mm.tag, key: mm.key, deep: !!mm.deep, lage: lage, bereich: b, s: s, learn: learn };
  }
  function fill(t, s) { return String(t || '').replace(/\{(\w+)\}/g, function (all, k) { return Object.prototype.hasOwnProperty.call(s, k) ? s[k] : all; }); }

  /* ---------- Widget ---------- */
  function W() { return $('[data-aufg]'); }
  function mode() { var b = $('.aufg-mode [aria-pressed="true"]', W()); return b ? b.getAttribute('data-mode') : 'kurz'; }
  function setMode(m) {
    var w = W();
    $$('.aufg-mode [data-mode]', w).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-mode') === m)); });
    w.classList.toggle('is-deep', m === 'deep');
    $('.aufg-dauer', w).disabled = m === 'deep';
  }
  function settings() {
    var w = W(), mine = DATA.personen[PERSON] || 'druck';
    var ber = $('.aufg-bereich', w).value, dauer = $('.aufg-dauer', w).value;
    var days;
    var chips = $$('.aufg-days input', w);
    if (chips.length) days = chips.filter(function (c) { return c.checked; }).map(function (c) { return c.value; });
    else {
      var here = w.getAttribute('data-tag'), fr = $('.aufg-frueher', w);
      days = fr && fr.checked ? Object.keys(DATA.tage).filter(function (d) { return +d <= +here; }) : [here];
    }
    days = days.filter(function (d) { return DATA.tage[d]; });
    return { bereiche: ber === 'mein' ? [mine] : (ber === 'alle' ? Object.keys(DATA.bereiche) : [ber]), dauer: dauer, days: days, mode: mode() };
  }
  function candidates(st) {
    var list = [];
    if (st.mode === 'deep') {
      // Deep Learn: nur Aufgaben der gewaehlten Tage - auf der Tagesseite also nur die des Tages (mit Haken auch fruehere)
      var here = W().getAttribute('data-tag');
      DATA.deep.forEach(function (d) { if (st.days.indexOf(String(d.tag)) >= 0) list.push({ id: d.id, m: d, w: String(d.tag) === here ? 4 : 1 }); });
      return list;
    }
    st.days.forEach(function (d) {
      var spec = DATA.muster.filter(function (m) { return String(m.tag) === d; });
      spec.forEach(function (m) { list.push({ id: m.id, m: m, w: 1 }); });
      DATA.generisch.forEach(function (g) { list.push({ id: g.id + '~' + d, m: g, w: spec.length >= 3 ? 0.2 : 1 }); });
    });
    if (st.dauer) list = list.filter(function (c) { return String(c.m.dauer) === st.dauer; });
    return list;
  }
  function doneMap() { return lsGet(key('done'), {}); }
  function roll(sameMuster) {
    var st = settings(), done = doneMap();
    var lagen = DATA.lagen.filter(function (l) { return st.bereiche.indexOf(l.bereich) >= 0; });
    var mid;
    if (sameMuster && cur) mid = cur.key;
    else {
      var c = candidates(st);
      if (!c.length) { renderEmpty(st); return; }
      var total = 0;
      c.forEach(function (x) {
        x.ww = x.w * (done[x.id] ? 1 : 3) * (recent.indexOf(x.id) >= 0 && c.length > recent.length ? 0.04 : 1);
        total += x.ww;
      });
      var t = Math.random() * total;
      for (var i = 0; i < c.length; i++) { t -= c[i].ww; if (t <= 0) { mid = c[i].id; break; } }
      if (!mid) mid = c[c.length - 1].id;
    }
    var pool = lagen.filter(function (l) { return !cur || l.id !== cur.lage.id || lagen.length < 2; });
    var lage = pool[Math.floor(Math.random() * pool.length)];
    var seed = 1 + Math.floor(Math.random() * 9998);
    show(mid + '.' + lage.id + '.' + seed, true);
  }
  function renderEmpty(st) {
    stopTick();
    var card = $('.aufg-card', W());
    card.textContent = '';
    card.appendChild(el('p', 'aufg-leer', st.mode === 'deep' ? 'Für die gewählten Tage gibt es noch keine Deep-Learn-Aufgabe – bitte einen späteren Tag wählen.'
      : 'Für diese Auswahl gibt es keine Aufgabe – bitte einen Tag oder eine andere Dauer wählen.'));
    stats();
  }
  function show(code, push) {
    var a = build(code);
    if (!a) { roll(false); return; }
    var here = W().getAttribute('data-tag');
    if (here && settings().days.indexOf(a.tag) < 0) {
      if (!push) { location.replace(BASE + '/' + PERSON + '/tag-' + a.tag + '/?aufgabe=' + encodeURIComponent(code) + '#aufgaben'); return; }
      roll(false); return;
    }
    if (a.deep !== (mode() === 'deep')) setMode(a.deep ? 'deep' : 'kurz');
    cur = a;
    recent = [a.key].concat(recent.filter(function (x) { return x !== a.key; })).slice(0, 4);
    stopTick();
    if (a.deep) renderDeep(a); else renderKurz(a);
    if (push) {
      var u = location.pathname + '?aufgabe=' + encodeURIComponent(code) + (W().hasAttribute('data-tag') ? '#aufgaben' : '');
      try { history.replaceState(null, '', u); } catch (e) { /* egal */ }
    }
  }

  /* ---------- Bausteine der Karte ---------- */
  function head(card, a, kicker, s) {
    var h = el('div', 'aufg-head');
    var k = el('p', 'aufg-kicker');
    kicker.filter(Boolean).forEach(function (x, i) {
      if (i) k.appendChild(el('span', 'sep', ' · '));
      k.appendChild(el('span', i === 0 && a.deep ? 'deep' : '', x));
    });
    h.appendChild(k);
    h.appendChild(el('h3', 'aufg-title', a.m.titel));
    h.appendChild(el('p', 'aufg-ziel', fill(a.m.ziel, s)));
    card.appendChild(h);
  }
  function lageBox(card, a, s) {
    var lage = el('div', 'aufg-lage');
    lage.appendChild(el('b', '', 'Die Lage'));
    lage.appendChild(el('p', '', fill(a.m.lage, s)));
    lage.appendChild(el('p', 'aufg-firma', a.lage.firma + ' – ' + a.lage.was + '. (ausgedacht)'));
    card.appendChild(lage);
  }
  function steps(list, s) {
    var ol = el('ol', 'aufg-steps');
    list.forEach(function (st) {
      var li = el('li');
      li.appendChild(el('p', '', fill(st.t, s)));
      if (st.p) li.appendChild(el('div', 'aprompt', fill(st.p, s)));
      ol.appendChild(li);
    });
    return ol;
  }
  function unklarBtn(a, refTail, label) {
    var ux = el('button', 'unklar', 'Unklar?');
    ux.type = 'button';
    ux.setAttribute('data-unklar-ref', 't' + a.tag + ':' + refTail);
    ux.setAttribute('data-unklar-label', label);
    ux.setAttribute('data-unklar-hash', '?aufgabe=' + a.code + (W().hasAttribute('data-tag') ? '#aufgaben' : ''));
    return ux;
  }
  function foot(card, a) {
    var f = el('div', 'aufg-foot');
    if (a.learn.length) {
      var lp = el('p', 'aufg-lrn');
      lp.appendChild(document.createTextNode('Passt zu: '));
      var first = true;
      a.learn.forEach(function (pair) {
        var t = String(pair[0]), id = pair[1], T = DATA.tage[t];
        if (!T) return;
        var idx = -1;
        T.learnings.forEach(function (l, j) { if (l[0] === id) idx = j; });
        if (idx < 0) return;
        if (!first) lp.appendChild(document.createTextNode(' · '));
        first = false;
        var link = el('a', '', (t !== a.tag || a.deep ? 'Tag ' + t + ', ' : '') + 'Learning ' + (idx + 1) + ': ' + T.learnings[idx][1]);
        link.href = BASE + '/' + PERSON + '/tag-' + t + '/#lrn-' + id;
        link.setAttribute('data-lrn', id);
        link.setAttribute('data-lrn-tag', t);
        lp.appendChild(link);
      });
      f.appendChild(lp);
    }
    var btns = el('div', 'aufg-btns');
    var db = el('button', 'chipbtn aufg-done');
    db.type = 'button';
    db.innerHTML = '<span class="ck" aria-hidden="true"></span>';
    db.appendChild(document.createTextNode(a.deep ? 'Ganze Aufgabe geschafft' : 'Geschafft'));
    db.setAttribute('aria-pressed', String(!!doneMap()[a.key]));
    db.addEventListener('click', function () {
      var d = doneMap();
      if (d[a.key]) delete d[a.key]; else d[a.key] = Date.now();
      lsSet(key('done'), d);
      db.setAttribute('aria-pressed', String(!!d[a.key]));
      stats();
    });
    btns.appendChild(db);
    var other = el('button', 'btn ghost aufg-other', 'Gleiche Aufgabe, andere Firma');
    other.type = 'button';
    other.addEventListener('click', function () { roll(true); });
    btns.appendChild(other);
    btns.appendChild(unklarBtn(a, (a.deep ? 'deep:' : 'aufgabe:') + a.key.replace('~', '-'),
      (a.deep ? 'Deep Learn' : 'Aufgabe') + ' (Tag ' + a.tag + '): ' + a.m.titel + ' · ' + a.lage.firma));
    f.appendChild(btns);
    var cp = el('p', 'aufg-code');
    cp.appendChild(document.createTextNode('Aufgabe Nr. '));
    cp.appendChild(el('code', '', a.code));
    cp.appendChild(document.createTextNode(' – mit dieser Nummer bekommt jede Person genau dieselbe Aufgabe.'));
    f.appendChild(cp);
    card.appendChild(f);
  }
  function finish(card) {
    if (window.KURS_COPY) window.KURS_COPY(card, '.aprompt');
    if (window.KURS && window.KURS.mark) window.KURS.mark();
    stats();
  }

  /* ---------- Kurzaufgabe ---------- */
  function renderKurz(a) {
    var card = $('.aufg-card', W()), s = a.s, m = a.m;
    card.textContent = '';
    card.classList.remove('deep');
    head(card, a, ['Tag ' + a.tag, m.dauer + ' Min', a.bereich.name, m.id.charAt(0) === 'g' ? 'aus den Learnings' : null], s);
    lageBox(card, a, s);
    card.appendChild(steps(m.schritte, s));
    var ach = el('div', 'aufg-achten');
    ach.appendChild(el('b', '', 'Darauf achten'));
    ach.appendChild(el('p', '', fill(m.achten, s)));
    card.appendChild(ach);
    [['noch', 'Noch eine Runde'], ['loesung', 'Auflösung']].forEach(function (x) {
      if (!m[x[0]]) return;
      var d = el('details', 'aufg-mehr');
      d.appendChild(el('summary', '', x[1]));
      d.appendChild(el('p', '', fill(m[x[0]], s)));
      card.appendChild(d);
    });
    foot(card, a);
    finish(card);
  }

  /* ---------- Deep Learn: 5 Etappen, Stunden-Uhr, Etappen abhaken ---------- */
  function baseKey(a) { return a.key + '.' + a.lage.id; }
  function etDone(a) { return (lsGet(key('etappen'), {})[baseKey(a)] || []); }
  function setEtDone(a, list) { var all = lsGet(key('etappen'), {}); if (list.length) all[baseKey(a)] = list; else delete all[baseKey(a)]; lsSet(key('etappen'), all); }
  function stopTick() { if (tick) { clearInterval(tick); tick = null; } }

  function renderDeep(a) {
    var card = $('.aufg-card', W()), s = a.s, m = a.m;
    card.textContent = '';
    card.classList.add('deep');
    head(card, a, ['Deep Learn', '60 Min', 'Tag ' + a.tag, a.bereich.name], s);
    var erg = el('div', 'aufg-ergebnis');
    erg.appendChild(el('b', '', 'Am Ende liegt vor'));
    erg.appendChild(el('p', '', fill(m.ergebnis, s)));
    card.appendChild(erg);
    lageBox(card, a, s);

    // Fahrplan + Uhr
    var plan = el('div', 'aufg-plan');
    var bar = el('ol', 'aufg-fahrplan');
    m.etappen.forEach(function (e, i) {
      var li = el('li');
      li.setAttribute('data-et', i);
      var ln = el('a', '', '');
      ln.href = '#etappe-' + (i + 1);
      ln.appendChild(el('b', '', String(i + 1)));
      ln.appendChild(el('span', '', e.titel));
      ln.appendChild(el('small', '', e.min + ' Min'));
      li.appendChild(ln);
      bar.appendChild(li);
    });
    plan.appendChild(bar);
    var uhr = el('div', 'aufg-uhr');
    var startB = el('button', 'btn primary aufg-uhr-start', 'Stunde starten'); startB.type = 'button';
    var resetB = el('button', 'btn ghost aufg-uhr-reset', 'Uhr zurücksetzen'); resetB.type = 'button';
    var info = el('span', 'aufg-uhr-info');
    info.setAttribute('aria-live', 'polite');
    var prog = el('span', 'aufg-uhr-bar'); prog.appendChild(el('i'));
    uhr.appendChild(startB); uhr.appendChild(resetB); uhr.appendChild(info); uhr.appendChild(prog);
    plan.appendChild(uhr);
    card.appendChild(plan);

    var cum = [], acc = 0;
    m.etappen.forEach(function (e) { cum.push(acc); acc += e.min; });
    m.etappen.forEach(function (e, i) {
      var sec = el('section', 'aufg-etappe');
      sec.id = 'etappe-' + (i + 1);
      sec.setAttribute('data-et', i);
      var hd = el('div', 'et-head');
      hd.appendChild(el('span', 'et-no', String(i + 1)));
      var ht = el('div', 'et-t');
      ht.appendChild(el('small', '', 'Etappe ' + (i + 1) + ' · ' + e.min + ' Minuten · ' + (i ? 'ab Minute ' + cum[i] : 'zum Start')));
      ht.appendChild(el('h4', '', fill(e.titel, s)));
      hd.appendChild(ht);
      sec.appendChild(hd);
      sec.appendChild(steps(e.schritte, s));
      var ch = el('div', 'aufg-achten');
      ch.appendChild(el('b', '', 'Zwischencheck'));
      ch.appendChild(el('p', '', fill(e.check, s)));
      sec.appendChild(ch);
      var ef = el('div', 'et-foot');
      var lab = el('label', 'et-done');
      var cb = el('input'); cb.type = 'checkbox';
      cb.checked = etDone(a).indexOf(i) >= 0;
      cb.addEventListener('change', function () {
        var l = etDone(a).filter(function (x) { return x !== i; });
        if (cb.checked) l.push(i);
        setEtDone(a, l.sort());
        paint();
      });
      lab.appendChild(cb);
      lab.appendChild(document.createTextNode(' Etappe ' + (i + 1) + ' erledigt'));
      ef.appendChild(lab);
      ef.appendChild(unklarBtn(a, 'deep:' + a.key + ':e' + (i + 1), 'Deep Learn (Tag ' + a.tag + '): ' + m.titel + ' · Etappe ' + (i + 1) + ': ' + e.titel));
      sec.appendChild(ef);
      card.appendChild(sec);
    });

    var ab = el('div', 'aufg-abschluss');
    ab.appendChild(el('b', '', 'Fertig, wenn …'));
    var ul = el('ul');
    m.abschluss.forEach(function (x) { ul.appendChild(el('li', '', fill(x, s))); });
    ab.appendChild(ul);
    card.appendChild(ab);
    if (m.bonus) {
      var d = el('details', 'aufg-mehr');
      d.appendChild(el('summary', '', 'Bonus, wenn noch Zeit ist'));
      d.appendChild(el('p', '', fill(m.bonus, s)));
      card.appendChild(d);
    }
    foot(card, a);

    function clock() { var c = lsGet(key('uhr'), null); return c && c.k === baseKey(a) ? c : null; }
    function paint() {
      var done = etDone(a), c = clock(), now = -1;
      if (c) {
        var mins = (Date.now() - c.start) / 60000;
        for (var i = 0; i < cum.length; i++) if (mins >= cum[i]) now = i;
        while (now >= 0 && now < cum.length && done.indexOf(now) >= 0) now++;   // schon erledigt -> naechste offene
        if (now >= cum.length) { now = -1; for (var j = 0; j < cum.length; j++) if (done.indexOf(j) < 0) { now = j; break; } }
        var over = mins >= 60;
        var dran = done.length === cum.length ? 'alle Etappen erledigt' : 'jetzt dran: Etappe ' + (now + 1);
        info.textContent = over ? 'Die Stunde ist um (' + mmss(Date.now() - c.start) + ') – ' + dran + '.'
          : mmss(Date.now() - c.start) + ' von 60:00 · ' + dran;
        prog.firstChild.style.width = Math.min(100, mins / 60 * 100) + '%';
      } else {
        info.textContent = done.length ? done.length + ' von 5 Etappen erledigt' : 'Uhr starten, Etappe für Etappe abarbeiten – die Zeiten sind nur ein Rahmen.';
        prog.firstChild.style.width = (done.length / m.etappen.length * 100) + '%';
      }
      startB.hidden = !!c; resetB.hidden = !c;
      $$('[data-et]', card).forEach(function (x) {
        var i = +x.getAttribute('data-et');
        x.classList.toggle('done', done.indexOf(i) >= 0);
        x.classList.toggle('now', i === now && done.indexOf(i) < 0);
      });
    }
    startB.addEventListener('click', function () { lsSet(key('uhr'), { k: baseKey(a), start: Date.now() }); paint(); stopTick(); tick = setInterval(paint, 1000); });
    resetB.addEventListener('click', function () { lsSet(key('uhr'), null); stopTick(); paint(); });
    paint();
    if (clock()) tick = setInterval(paint, 1000);
    finish(card);
  }

  function stats() {
    var w = W(), out = $('.aufg-stat', w);
    if (!out || !DATA) return;
    var st = settings(), done = doneMap();
    var c = candidates({ days: st.days, dauer: '', mode: st.mode });
    var n = c.filter(function (x) { return done[x.id]; }).length;
    if (st.mode === 'deep') {
      out.textContent = n ? n + ' von ' + c.length + ' Deep-Learn-Aufgaben geschafft' + (n === c.length ? ' – alle!' : '.')
        : c.length + ' Deep-Learn-Aufgaben zur Auswahl – je etwa eine Stunde, alles in Langdock.';
    } else {
      out.textContent = n ? n + ' von ' + c.length + ' Aufgaben ausprobiert' + (n === c.length ? ' – alle! Würfeln geht trotzdem weiter.' : '.')
        : c.length + ' verschiedene Aufgaben, jede mit 12 möglichen Firmen.';
    }
  }

  /* ---------- Start ---------- */
  function load() {
    if (DATA) return Promise.resolve(DATA);
    if (!loading) {
      var src = W().getAttribute('data-src');
      loading = fetch(src, { credentials: 'same-origin' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (d) { DATA = d; return d; });
    }
    return loading;
  }
  var started = false;
  function start() {
    if (started || !W()) return;
    started = true;
    var w = W();
    load().then(function () {
      var mine = DATA.personen[PERSON];
      var opt = $('.aufg-bereich option[value="mein"]', w);
      if (opt && mine) opt.textContent = 'Mein Bereich (' + DATA.bereiche[mine].name + ')';
      var saved = lsGet(key('opts'), {});
      if (saved.bereich && $('.aufg-bereich option[value="' + saved.bereich + '"]', w)) $('.aufg-bereich', w).value = saved.bereich;
      if (saved.dauer != null) $('.aufg-dauer', w).value = saved.dauer;
      setMode(saved.mode === 'deep' ? 'deep' : 'kurz');
      var chips = $$('.aufg-days input', w), savedDays = lsGet(key('days'), null);
      if (chips.length && savedDays && savedDays.length) chips.forEach(function (c) { c.checked = savedDays.indexOf(c.value) >= 0; });
      function save() {
        var o = lsGet(key('opts'), {});
        o.bereich = $('.aufg-bereich', w).value; o.dauer = $('.aufg-dauer', w).value; o.mode = mode();
        lsSet(key('opts'), o);
        if (chips.length) lsSet(key('days'), chips.filter(function (c) { return c.checked; }).map(function (c) { return c.value; }));
      }
      $$('select, input', $('.aufg-ctl', w)).forEach(function (x) { x.addEventListener('change', function () { save(); roll(false); }); });
      $$('.aufg-mode [data-mode]', w).forEach(function (b) {
        b.addEventListener('click', function () {
          if (b.getAttribute('aria-pressed') === 'true') return;
          setMode(b.getAttribute('data-mode')); cur = null; save(); roll(false);
        });
      });
      $('.aufg-roll', w).addEventListener('click', function () { roll(false); });
      var m = /[?&]aufgabe=([\w~.\-]+)/.exec(location.search);
      if (m) show(decodeURIComponent(m[1]), false); else roll(false);
      w.classList.add('ready');
    }).catch(function () {
      $('.aufg-card', w).textContent = 'Die Aufgaben konnten nicht geladen werden. Bitte die Seite neu laden.';
    });
  }
  // Links zu Learnings derselben Tagesseite: Reiter wechseln statt neu laden
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.aufg-lrn a[data-lrn]');
    if (!a) return;
    var here = root.getAttribute('data-tag');
    if (!here || a.getAttribute('data-lrn-tag') !== here) return;
    e.preventDefault();
    location.hash = 'learnings';
    setTimeout(function () {
      var c = document.getElementById('lrn-' + a.getAttribute('data-lrn'));
      if (c) { c.scrollIntoView({ block: 'center' }); c.classList.remove('flash'); void c.offsetWidth; c.classList.add('flash'); }
    }, 80);
  });
  // Fahrplan-Links: zur Etappe scrollen, ohne den Reiter-Anker (#aufgaben) zu verlieren
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.aufg-fahrplan a');
    if (!a) return;
    e.preventDefault();
    var t = document.getElementById(a.getAttribute('href').slice(1));
    if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  function init() {
    // Uebersicht: nur Zaehler
    var cnt = $('[data-aufg-count]');
    if (cnt) {
      var n = Object.keys(doneMap()).length;
      cnt.textContent = n ? n + (n === 1 ? ' Aufgabe' : ' Aufgaben') + ' geschafft' : 'noch keine Aufgabe geschafft';
    }
    var w = W();
    if (!w) return;
    $('.aufg-roll', w).innerHTML = DICE + '<span>Neue Aufgabe würfeln</span>';
    var panel = w.closest('.tpanel');
    if (!panel || !panel.hidden) start();
    document.addEventListener('kurs:tab', function (e) { if (e.detail === 'aufgaben') start(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
