/* Modul 2 · Tag 6: Scoring, Matrix, Business Case, Szenarien, Empfehlung.
   Felder mit data-save speichert wochenheft.js (kurs:m2w1:<person>:<feld>); hier wird nur gerechnet und angezeigt.
   Rechenweg wie Folie 19: Ersparnis wird auf ganze Stunden gerundet. */
(function () {
  'use strict';
  var PERSON = document.documentElement.getAttribute('data-person') || 'gast';
  var PREFIX = 'kurs:m2w1:' + PERSON + ':';
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function get(k, def) { try { var v = localStorage.getItem(PREFIX + k); return v === null ? def : JSON.parse(v); } catch (e) { return def; } }
  function num(v) { var n = parseFloat(String(v == null ? '' : v).replace(',', '.')); return isFinite(n) ? n : 0; }
  function de(n, d) { return Number(n).toLocaleString('de-DE', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function setVal(f, v) { f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }
  function val(k) { var f = $('[data-save="' + k + '"]'); return f ? f.value : get(k, ''); }

  var KRIT = ['n', 'd', 'e', 'r'], NAMEN = { n: 'Nutzen', d: 'Datenverfügbarkeit', e: 'Einfachheit', r: 'Risikoarmut' };
  var FELD = {
    sofort: ['Sofort starten', 'Hier liegt das Erstprojekt.'], planen: ['Planen und in Etappen schneiden', 'Nicht als Ganzes beauftragen.'],
    nebenbei: ['Nebenbei', 'Kein Projekt, kein Budget, kein Fahrplan.'], streichen: ['Streichen', 'Ein Ergebnis, kein Scheitern.']
  };

  /* ---------- Freitag ---------- */
  function freitag() {
    var box = $('.ft-liste'); if (!box) return;
    box.innerHTML = '';
    var n = 0;
    [1, 2, 3].forEach(function (k) {
      var name = get('sb' + k + '-name', '');
      if (!name) return;
      n++;
      var nutzen = get('sb' + k + '-nutzen', '');
      var karte = el('div', 'ft-karte');
      karte.appendChild(el('b', '', k + '. ' + name));
      karte.appendChild(el('span', '', nutzen ? 'Nutzen: ' + nutzen : 'Nutzenfeld noch offen'));
      box.appendChild(karte);
    });
    if (!n) {
      var p = el('p', '', 'In diesem Browser sind noch keine Steckbriefe gespeichert. Trage sie im Use-Case-Labor von Tag 5 nach oder nimm eines der Beispiele aus diesem Heft.');
      var a = el('a', '', ' Zum Use-Case-Labor →'); a.href = '/hefte/' + PERSON + '/modul-2/tag-5/#labor'; p.appendChild(a);
      box.appendChild(p);
    }
  }

  /* ---------- Scoring ---------- */
  function gewichte() { var g = {}; KRIT.forEach(function (c) { g[c] = num(val('gw-' + c)); }); return g; }
  function bewertung(k) {
    var p = {}, voll = true;
    KRIT.forEach(function (c) { p[c] = num(val('bw' + k + '-' + c)); if (!p[c]) voll = false; });
    return { name: val('bw' + k + '-name') || ('Kandidat ' + k), p: p, voll: voll };
  }
  function scoring() {
    var tool = $('[data-tool="scoring"]');
    var g = gewichte(), summe = g.n + g.d + g.e + g.r;
    var gs = $('.gw-summe', tool);
    if (gs) { gs.textContent = summe === 100 ? 'Summe: 100 % ✓' : 'Summe: ' + de(summe) + ' %. Es müssen genau 100 % sein.'; gs.className = 'gw-summe ' + (summe === 100 ? 'ok' : 'warn'); }
    var saetze = 0;
    [1, 2, 3].forEach(function (k) {
      var b = bewertung(k), out = $('[data-bw-summe="' + k + '"]');
      KRIT.forEach(function (c) { if (val('bw' + k + '-' + c + '-warum').trim()) saetze++; });
      if (!out) return;
      if (b.voll) {
        var t = KRIT.reduce(function (s, c) { return s + b.p[c] * g[c] / 100; }, 0);
        out.textContent = 'Gewichtete Punktzahl: ' + de(t, 2);
        out.className = 'bw-summe ok';
      } else { out.textContent = 'Noch nicht alle vier Punkte vergeben.'; out.className = 'bw-summe'; }
    });
    var stand = tool && $('.bw-stand', tool);
    if (stand) { stand.textContent = saetze + ' von 12 Begründungssätzen geschrieben' + (saetze === 12 ? ' ✓' : '. Eine Zahl ohne Satz zählt nicht.'); stand.className = 'bw-stand ' + (saetze === 12 ? 'ok' : ''); }
  }
  var BSP = [['Druckanfragen vorsortieren', 4, 4, 3, 4], ['Angebote automatisch versenden', 5, 2, 2, 1], ['Monatsbericht formatieren', 2, 3, 5, 5]];
  var BSP_W = { n: 'Spart laut Zählung viele Stunden im Monat.', d: 'Die Daten liegen vor, sind aber nicht einheitlich.', e: 'Überschaubar viele Systeme und Sonderfälle.', r: 'Fehler fallen auf und lassen sich korrigieren.' };
  function beispielScoring() {
    var belegt = [1, 2, 3].some(function (k) { return val('bw' + k + '-n'); });
    if (belegt && !window.confirm('Deine Punkte durch das Beispiel ersetzen?')) return;
    BSP.forEach(function (b, i) {
      var k = i + 1;
      setVal($('[data-save="bw' + k + '-name"]'), b[0]);
      KRIT.forEach(function (c, j) { setVal($('[data-save="bw' + k + '-' + c + '"]'), String(b[j + 1])); setVal($('[data-save="bw' + k + '-' + c + '-warum"]'), BSP_W[c]); });
    });
  }

  /* ---------- Matrix ---------- */
  function feldVon(wert, aufwand) { return wert >= 7 ? (aufwand <= 5 ? 'sofort' : 'planen') : (aufwand <= 5 ? 'nebenbei' : 'streichen'); }
  function matrix() {
    var tool = $('[data-tool="matrix"]'); if (!tool) return;
    $$('.mx-chips', tool).forEach(function (c) { c.innerHTML = ''; });
    var tab = $('.mx-tab', tool); tab.innerHTML = '';
    var haupt = $('[data-haupt]', tool);
    [1, 2, 3].forEach(function (k) {
      var b = bewertung(k), opt = haupt.options[k];
      if (opt) opt.textContent = b.name;
      if (!b.voll) return;
      var wert = b.p.n + b.p.d, aufwand = 12 - b.p.e - b.p.r, f = feldVon(wert, aufwand);
      $('.mx-chips', $('[data-feld="' + f + '"]', tool)).appendChild(el('span', 'mx-chip', k + ' · ' + b.name));
      tab.appendChild(el('p', '', b.name + ': Wert ' + wert + ', Aufwand ' + aufwand + ' → ' + FELD[f][0] + '. ' + FELD[f][1]));
    });
    if (!tab.childNodes.length) tab.appendChild(el('p', '', 'Sobald ein Kandidat alle vier Punkte hat, erscheint er hier in seinem Feld.'));
    var name = hauptName();
    $$('[data-haupt-name]').forEach(function (e) { e.textContent = name || 'noch offen'; });
    var bh = $('[data-bc-haupt]'); if (bh) bh.textContent = name ? 'Du rechnest: ' + name : 'Wähle oben deinen Haupt-Use-Case. Ohne Auswahl kannst du trotzdem rechnen.';
  }
  function hauptName() { var h = val('haupt'); return h ? (val('bw' + h + '-name') || 'Kandidat ' + h) : ''; }

  /* ---------- Business Case ---------- */
  function summe(attr) { return $$('[' + attr + ']').reduce(function (s, f) { return s + num(f.value); }, 0); }
  function basis() {
    return { v: num(val('bc-volumen')), m: num(val('bc-zeit')), a: num(val('bc-anteil')), r: num(val('bc-rest')), s: num(val('bc-satz')), f: num(val('bc-fehler')),
      inv: summe('data-ein'), lauf: summe('data-lauf') };
  }
  function rechne(b, anteil, lauf) {
    var exakt = b.v * anteil / 100 * Math.max(b.m - b.r, 0) / 60, h = Math.round(exakt), brutto = h * b.s + b.f, netto = brutto - lauf;
    return { exakt: exakt, h: h, brutto: brutto, netto: netto, amort: netto > 0 ? b.inv / netto : null,
      roi12: b.inv ? (netto * 12 - b.inv) / b.inv * 100 : null, roi36: b.inv ? (netto * 36 - b.inv) / b.inv * 100 : null, tco: b.inv + lauf * 36 };
  }
  function kachel(wert, text, cls) { var d = el('div', 'bc-kachel ' + (cls || '')); d.appendChild(el('b', '', wert)); d.appendChild(el('span', '', text)); return d; }
  function bc() {
    var tool = $('[data-tool="bc"]'); if (!tool) return;
    var b = basis(), r = rechne(b, b.a, b.lauf), aus = $('.bc-aus', tool), hin = $('.bc-hinweise', tool);
    aus.innerHTML = ''; hin.innerHTML = '';
    if (!b.v || !b.s) { aus.appendChild(el('p', '', 'Trage Volumen, Zeit, Anteil und Stundensatz ein. Die Ergebnisse erscheinen hier sofort.')); stats(null); return; }
    aus.appendChild(kachel('rund ' + de(r.h) + ' Std.', 'Ersparnis pro Monat (genau ' + de(r.exakt, 1) + ')'));
    aus.appendChild(kachel(de(r.brutto) + ' €', 'Bruttonutzen pro Monat'));
    aus.appendChild(kachel(de(b.lauf) + ' €', 'Laufende Kosten pro Monat'));
    aus.appendChild(kachel(de(r.netto) + ' €', 'Nettonutzen pro Monat', r.netto > 0 ? 'gut' : 'warn'));
    aus.appendChild(kachel(de(b.inv) + ' €', 'Investition einmalig'));
    aus.appendChild(kachel(r.amort ? 'rund ' + de(r.amort) + ' Monate' : 'nie', 'Amortisation', r.amort ? 'gut' : 'warn'));
    aus.appendChild(kachel(r.roi12 === null ? '–' : de(r.roi12, 1) + ' %', 'ROI nach 12 Monaten'));
    aus.appendChild(kachel(r.roi36 === null ? '–' : de(r.roi36, 1) + ' %', 'ROI nach 36 Monaten'));
    aus.appendChild(kachel(de(r.tco) + ' €', 'TCO über 3 Jahre'));
    var ohne = 0;
    $$('[data-bc],[data-ein],[data-lauf]', tool).forEach(function (f) { if (f.value !== '' && !val(f.getAttribute('data-save') + '-her')) ohne++; });
    function h(t, warn) { hin.appendChild(el('li', warn ? 'warn' : 'ok', t)); }
    h(ohne ? ohne + ' Zahlen ohne Herkunft. Fertig ist es erst, wenn bei jeder Zahl steht: gemessen, nachgeschlagen oder geschätzt.' : 'Jede Zahl hat eine Herkunft ✓', ohne > 0);
    if (r.netto <= 0) h('Der Nettonutzen ist nicht positiv: So amortisiert sich der Fall nie.', true);
    if (r.amort && r.amort < 6) h('Unter 6 Monaten Amortisation: Meist fehlt etwas in der Rechnung. Prüfe laufende Kosten, Datenaufbereitung und Schulung.', true);
    var daten = num(val('bc-e3'));
    if (b.inv && daten / b.inv < .15) h('Datenaufbereitung liegt unter 15 % des Budgets. Erfahrungswert: 15–25 %.', true);
    if (r.h < 10) h('Unter 10 Stunden im Monat: Nach der Faustregel trägt sich das kaum. Dann müssen Qualität, Risiko oder Vorschriften der Grund sein.', true);
    h('Denk an den Puffer: 20–30 % auf die Schätzung sind die Regel.', false);
    stats(r);
  }
  function stats(r) { $$('[data-stat-amort]').forEach(function (e) { e.textContent = r && r.amort ? 'rund ' + de(r.amort) + ' Monate' : 'noch offen'; }); }
  function beispielBc() {
    var belegt = $$('[data-bc]').some(function (f) { return f.value !== ''; });
    if (belegt && !window.confirm('Deine Zahlen durch das Beispiel Rechnungsfreigabe ersetzen?')) return;
    $$('[data-bsp]').forEach(function (f) { setVal(f, f.getAttribute('data-bsp')); var k = f.getAttribute('data-save'); var her = $('[data-save="' + k + '-her"]'); if (her) { her.value = 'geschätzt'; her.dispatchEvent(new Event('change', { bubbles: true })); } });
  }

  /* ---------- Szenarien ---------- */
  function szKachel(box, r) {
    box.innerHTML = '';
    if (!r) { box.appendChild(el('p', '', 'Noch keine Zahlen.')); return; }
    box.appendChild(kachel(de(r.netto) + ' €', 'Nettonutzen pro Monat', r.netto > 0 ? 'gut' : 'warn'));
    box.appendChild(kachel(r.amort ? 'rund ' + de(r.amort) + ' Monate' : 'nie', 'Amortisation'));
    box.appendChild(kachel(r.roi12 === null ? '–' : de(r.roi12, 1) + ' %', 'ROI nach 12 Monaten'));
  }
  function szenario() {
    var tool = $('[data-tool="szenario"]'); if (!tool) return;
    var b = basis(), hat = b.v && b.s;
    var kA = val('sz-k-anteil'), kL = val('sz-k-lauf'), aA = val('sz-a-anteil'), aL = val('sz-a-lauf');
    var rk = hat && kA !== '' && kL !== '' ? rechne(b, num(kA), num(kL)) : null;
    szKachel($('[data-sz-aus="k"]', tool), rk);
    szKachel($('[data-sz-aus="b"]', tool), hat ? rechne(b, b.a, b.lauf) : null);
    szKachel($('[data-sz-aus="a"]', tool), hat && aA !== '' && aL !== '' ? rechne(b, num(aA), num(aL)) : null);
    var kipp = $('[data-sz-kipp]', tool), ziel = num(val('sz-ziel')) || 24;
    kipp.className = '';
    if (!hat || !b.inv) { kipp.textContent = 'Sobald der Business Case gefüllt ist, steht hier, wann der Fall kippt.'; return; }
    var std = (b.inv / ziel + b.lauf - b.f) / b.s, proMin = b.v * Math.max(b.m - b.r, 0) / 60, grenz = proMin ? std / proMin * 100 : 0;
    var t = grenz > 100 ? 'Selbst bei 100 % Automatisierung wäre die Investition nicht in ' + de(ziel) + ' Monaten drin.'
      : grenz <= 0 ? 'Der Fall trägt schon ohne automatisierten Anteil.'
      : 'Der Fall kippt, wenn der automatisierbare Anteil unter rund ' + de(grenz) + ' % fällt.';
    if (rk) {
      var traegt = rk.amort && rk.amort <= ziel;
      t += traegt ? ' Das konservative Szenario trägt ✓' : ' Das konservative Szenario trägt nicht: kleiner zuschneiden, verschieben oder nicht machen.';
      kipp.className = traegt ? 'ok' : 'warn';
    }
    kipp.textContent = t;
  }
  function vorschlag() {
    var b = basis();
    if (!b.v) { window.alert('Bitte zuerst den Business Case ausfüllen oder das Beispiel laden.'); return; }
    setVal($('[data-save="sz-k-anteil"]'), Math.max(b.a - 20, 0));
    setVal($('[data-save="sz-k-lauf"]'), b.lauf + num(val('bc-l4')));
    setVal($('[data-save="sz-a-anteil"]'), Math.min(b.a + 15, 100));
    setVal($('[data-save="sz-a-lauf"]'), Math.round(b.lauf - num(val('bc-l2')) / 2));
  }

  /* ---------- Empfehlung, Faustregel ---------- */
  function entscheidung() {
    var out = $('.ent-stand'); if (!out) return;
    var offen = [];
    if (!val('ent-wahl')) offen.push('Empfehlung');
    if (!val('ent-text').trim()) offen.push('zwei Sätze');
    if (!val('ab-zahl').trim()) offen.push('Zahl');
    if (!val('ab-zeit').trim()) offen.push('Zeitpunkt');
    if (!val('ab-person').trim()) offen.push('Person');
    out.textContent = offen.length ? 'Noch offen: ' + offen.join(', ') + '.' : 'Fertig: Empfehlung und Abbruchbedingung stehen ✓';
    out.className = 'ent-stand ' + (offen.length ? '' : 'ok');
  }
  function faustregel() {
    var tool = $('[data-tool="faustregel"]'); if (!tool) return;
    var s = num($('[data-fr="v"]', tool).value) * num($('[data-fr="m"]', tool).value) / 60, out = $('.fr-aus', tool);
    out.textContent = de(s, 1) + ' Stunden im Monat: ' + (s >= 15 ? 'trägt sich nach der Faustregel. Jetzt genau rechnen.' : s >= 10 ? 'Grenzbereich. Genau rechnen lohnt sich.' : 'trägt sich nach der Faustregel nicht. Nur mit anderen Gründen wie Qualität oder Vorschriften.');
    out.className = 'fr-aus ' + (s >= 10 ? 'ok' : 'warn');
  }

  /* ---------- Export ---------- */
  function exportMd() {
    var L = ['# Meine Tagesarbeit · Modul 2 · Tag 6 · 02.11.2026', '', 'Person: ' + PERSON + ' · nur erfundene oder freigegebene Angaben', '', '## Bewerten', ''];
    var g = gewichte();
    L.push('Gewichtung: ' + KRIT.map(function (c) { return NAMEN[c] + ' ' + g[c] + ' %'; }).join(', '), '');
    [1, 2, 3].forEach(function (k) {
      var b = bewertung(k);
      L.push('### ' + b.name);
      KRIT.forEach(function (c) { L.push('- ' + NAMEN[c] + ': ' + (b.p[c] || '–') + ' · ' + (val('bw' + k + '-' + c + '-warum') || '(ohne Satz)')); });
      if (b.voll) {
        var w = b.p.n + b.p.d, a = 12 - b.p.e - b.p.r;
        L.push('- Punktzahl: ' + de(KRIT.reduce(function (s, c) { return s + b.p[c] * g[c] / 100; }, 0), 2) + ' · Wert ' + w + ' · Aufwand ' + a + ' · ' + FELD[feldVon(w, a)][0]);
      }
      L.push('');
    });
    L.push('Haupt-Use-Case: ' + (hauptName() || 'offen'), '', '## Business Case', '');
    $$('[data-bc],[data-ein],[data-lauf]').forEach(function (f) {
      var lab = $('label[for="' + f.id + '"]'), k = f.getAttribute('data-save');
      if (f.value !== '') L.push('- ' + (lab ? lab.textContent.trim() : k) + ': ' + f.value + ' (' + (val(k + '-her') || 'Herkunft offen') + ')');
    });
    var b = basis(), r = rechne(b, b.a, b.lauf);
    L.push('', 'Ersparnis ' + r.h + ' Std./Monat · Brutto ' + de(r.brutto) + ' € · Netto ' + de(r.netto) + ' € · Amortisation ' + (r.amort ? de(r.amort) + ' Monate' : 'nie') + ' · TCO ' + de(r.tco) + ' €');
    L.push('Qualitative Effekte: ' + (val('bc-qualitativ') || '–'), '', '## Entscheidung', '');
    L.push('Der Fall kippt: ' + (val('ent-kipp') || '–'), 'Empfehlung: ' + (val('ent-wahl') || '–'), val('ent-text') || '', 'Abbruch: ' + [val('ab-zahl'), val('ab-zeit'), val('ab-person'), val('ab-dann')].filter(Boolean).join(' · '));
    var blob = new Blob([L.join('\n')], { type: 'text/markdown;charset=utf-8' });
    var a = el('a'); a.href = URL.createObjectURL(blob); a.download = 'Tag6-Bewerten-und-Rechnen_' + PERSON + '.md';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  function alles() { scoring(); matrix(); bc(); szenario(); entscheidung(); faustregel(); }
  function init() {
    freitag();
    [1, 2, 3].forEach(function (k) {
      var f = $('[data-save="bw' + k + '-name"]'), n = get('sb' + k + '-name', '');
      if (f && !f.value && n) setVal(f, n);
    });
    document.addEventListener('input', alles);
    document.addEventListener('change', alles);
    var b;
    if ((b = $('[data-bw-beispiel]'))) b.addEventListener('click', function () { beispielScoring(); alles(); });
    if ((b = $('[data-bc-beispiel]'))) b.addEventListener('click', function () { beispielBc(); alles(); });
    if ((b = $('[data-sz-vorschlag]'))) b.addEventListener('click', function () { vorschlag(); alles(); });
    if ((b = $('[data-w2-export]'))) b.addEventListener('click', exportMd);
    alles();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
