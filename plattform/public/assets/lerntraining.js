(function () {
  'use strict';
  var C = window.LerntrainingCore;
  if (!C) return;
  var person = document.documentElement.dataset.person;
  if (!person) return;
  var storageKey = 'kurs:training:v1:' + person;
  var state = {cards: {}, cases: {}, notes: {}}, storageOK = true;
  function object(x) { return x && typeof x === 'object' && !Array.isArray(x); }
  try {
    var saved = JSON.parse(localStorage.getItem(storageKey));
    if (object(saved)) ['cards', 'cases', 'notes'].forEach(function (k) { if (object(saved[k])) state[k] = saved[k]; });
  } catch (_) { storageOK = false; }
  function q(s, parent) { return (parent || document).querySelector(s); }
  function element(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function button(label, action, primary) { var b = element('button', 'btn' + (primary ? ' primary' : ''), label); b.type = 'button'; b.addEventListener('click', action); return b; }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); storageOK = true; }
    catch (_) { storageOK = false; }
    var warning = q('.lt-storage');
    if (warning) { warning.hidden = storageOK; warning.textContent = 'Der Browser kann den Lernstand gerade nicht speichern. Das Training funktioniert weiter, aber Änderungen bleiben nur bis zum Verlassen der Seite.'; }
    return storageOK;
  }
  function dataFrom(node) { try { return JSON.parse(q('.lt-data', node).textContent); } catch (_) { return null; } }
  function dateLabel(day) { return new Date(day + 'T12:00:00').toLocaleDateString('de-DE', {day: 'numeric', month: 'long'}); }
  var overview = q('[data-training-overview]');
  if (overview) {
    var od = dataFrom(overview), pending = od ? C.due(od.cards, state.cards, C.today()) : [];
    if (pending.length) {
      q('[data-review-summary]', overview).textContent = pending.length + ' Karten sind zur Wiederholung bereit. Die nächste Runde beginnt mit dem, was wieder dran ist.';
      q('[data-review-link]', overview).href = '/hefte/' + person + '/tag-' + Math.max.apply(null, od.cards.map(function (c) { return c.day; })) + '/#training';
    }
  }
  var host = q('[data-training]');
  if (!host) return;
  var data = dataFrom(host);
  if (!data) return;
  var dashboard = q('.lt-dashboard', host), stage = q('.lt-stage', host);
  var sequence = [], position = 0, repeats = {}, confident = 0, roundSize = 0, practice = false;
  var caseQueue = [], casePosition = 0, caseCorrect = 0;
  var note = q('#lt-note', host);
  note.value = typeof state.notes[data.day] === 'string' ? state.notes[data.day].slice(0, 3000) : '';
  note.addEventListener('input', function () {
    state.notes[data.day] = note.value;
    q('.lt-note-status', host).textContent = save() ? 'Auf diesem Gerät gespeichert.' : 'Gerade nicht dauerhaft gespeichert.';
  });
  if (!storageOK) save();
  function focusHeading() { var h = q('h3', stage); if (h) { h.tabIndex = -1; h.focus({preventScroll: true}); h.scrollIntoView({block: 'nearest', behavior: 'instant'}); } }
  function article(kicker, title) {
    stage.replaceChildren();
    var a = element('article', 'lt-work');
    a.append(element('p', 'kicker', kicker), element('h3', '', title)); stage.append(a); return a;
  }
  function controls(parent) { var row = element('div', 'btnrow'); parent.append(row); return row; }
  function home(focus) {
    stage.replaceChildren(); dashboard.hidden = false; dashboard.replaceChildren();
    var current = data.cards.filter(function (c) { return c.day === data.day; });
    var waiting = C.due(data.cards, state.cards, C.today());
    var fresh = current.filter(function (c) { return !C.record(state.cards[c.id]); }).length;
    var review = element('article', 'lt-choice');
    review.append(element('p', 'kicker', 'Erinnern · fünf Fragen'), element('h3', '', 'Was bleibt im Kopf?'),
      element('p', '', 'Ohne nachzulesen antworten. Danach mit der Musterantwort vergleichen und ehrlich einschätzen.'),
      element('p', 'lt-count', waiting.length + ' zur Wiederholung · ' + fresh + ' neue Karten aus Tag ' + data.day));
    var dates = current.map(function (c) { return C.record(state.cards[c.id]); }).filter(function (r) { return r && r.due > C.today(); }).map(function (r) { return r.due; }).sort();
    if (!waiting.length && dates.length) review.append(element('p', 'lt-next', 'Nächste geplante Wiederholung: ' + dateLabel(dates[0]) + '. Eine zusätzliche Runde ist jederzeit möglich.'));
    review.append(button('Erinnerungsrunde starten', startRound, true)); dashboard.append(review);
    var apply = element('article', 'lt-choice lt-choice-case');
    if (data.cases.length) {
      var done = data.cases.filter(function (c) { return state.cases[c.id] === true; }).length;
      apply.append(element('p', 'kicker', 'Anwenden · fünf kleine Fälle'), element('h3', '', 'Was wäre jetzt sinnvoll?'),
        element('p', '', 'Entscheidungen aus dem eigenen Arbeitsbereich. Zu jeder Antwort gibt es eine Erklärung – auch wenn sie noch nicht passt.'),
        element('p', 'lt-count', done + ' von ' + data.cases.length + ' Fällen zuletzt richtig gelöst'),
        button(done && done < data.cases.length ? 'Offene Fälle üben' : 'Fallwerkstatt starten', startCases));
    } else {
      apply.append(element('p', 'kicker', 'Anwenden · aus dem eigenen Bereich'), element('h3', '', 'Vom Merksatz zum Ausprobieren'),
        element('p', '', 'Eine kurze Praxisaufgabe bearbeiten. Danach in eigenen Worten festhalten: Was würde man bei einer ähnlichen Aufgabe wieder so machen?'));
      var link = element('a', 'btn', 'Zu den Praxisaufgaben →'); link.href = '#aufgaben';
      apply.append(link);
    }
    dashboard.append(apply);
    if (focus) { var h = q('h3', dashboard); h.tabIndex = -1; h.focus(); }
  }
  function startRound() {
    var round = C.round(data.cards, state.cards, C.today(), data.day);
    sequence = round.cards.slice(); roundSize = sequence.length; practice = round.practice;
    position = 0; repeats = {}; confident = 0; dashboard.hidden = true; showCard();
  }
  function showCard() {
    if (position >= sequence.length) return finishRound();
    var card = sequence[position], repeat = position >= roundSize;
    var a = article(repeat ? 'Noch einmal festigen · ohne Zeitdruck' : 'Erinnern · Frage ' + (position + 1) + ' von ' + roundSize, card.question);
    a.append(element('p', 'lt-context', 'Aus Tag ' + card.day + ' · ' + card.title));
    var progress = element('progress'); progress.max = sequence.length; progress.value = position; progress.setAttribute('aria-label', 'Bearbeitete Fragen'); a.append(progress);
    var label = element('label', 'lt-label', 'Was fällt einem dazu ein?'); label.htmlFor = 'lt-answer';
    var input = element('textarea'); input.id = 'lt-answer'; input.rows = 3; input.maxLength = 1500;
    input.placeholder = 'Ein oder zwei Stichworte reichen. Man kann auch laut oder im Kopf antworten.';
    input.setAttribute('aria-describedby', 'lt-answer-hint');
    a.append(label, input, element('p', 'lt-small', 'Stichworte nur für diese Frage; keine automatische Bewertung.'));
    a.lastChild.id = 'lt-answer-hint';
    var reveal = button('Mit der Musterantwort vergleichen', function () {
      reveal.remove(); input.readOnly = true;
      var answer = element('div', 'lt-answer'); answer.append(element('h4', '', 'So lässt es sich sagen'), element('p', '', card.answer)); a.append(answer);
      if (card.example) {
        var simple = element('details'); simple.append(element('summary', '', 'Mit einem Beispiel verstehen'), element('p', '', card.explanation), element('p', '', card.example)); answer.append(simple);
        var slideLink = element('a', 'lt-source', 'Folie ' + card.slide + ' in einfachen Worten nachlesen →');
        slideLink.href = '/hefte/' + person + '/tag-' + card.day + '/#einfach-' + card.slide; answer.append(slideLink);
      }
      a.append(element('p', '', 'Die eigenen Worte dürfen anders sein. Entscheidend ist, ob der Gedanke stimmt.'));
      var row = controls(a), used = false;
      function choose(known) {
        if (used) return; used = true;
        // Freiwillige Wiederholung vor Fälligkeit verschiebt einen sicheren Termin nicht.
        var old = C.record(state.cards[card.id]);
        if (!(known && practice && old && old.due > C.today())) state.cards[card.id] = C.rate(old, known, C.today());
        if (!known && !repeats[card.id]) { repeats[card.id] = true; sequence.push(card); }
        if (known && position < roundSize) confident++;
        save(); position++; showCard();
      }
      row.append(button('Noch unsicher – nochmal üben', function () { choose(false); }), button('In eigenen Worten gewusst', function () { choose(true); }, true));
      answer.tabIndex = -1; answer.focus({preventScroll: true}); answer.scrollIntoView({block: 'nearest', behavior: 'instant'});
    }, true);
    controls(a).append(reveal, button('Runde beenden', function () { home(true); })); focusHeading();
  }
  function finishRound() {
    var left = sequence.slice(0, roundSize).filter(function (c) { var r = C.record(state.cards[c.id]); return r && r.step === 0; }).length;
    var a = article('Die Runde ist geschafft', 'Wissen braucht Wiedersehen.');
    a.append(element('p', 'lt-count', confident + ' von ' + roundSize + ' beim ersten Abruf selbst als gewusst eingeschätzt.'),
      element('p', '', left ? left + ' Karten bleiben noch unsicher. Sie bleiben zur Wiederholung bereit. Eine Pause ist jetzt genauso in Ordnung.' : 'Alles aus dieser Runde wurde zuletzt als gewusst eingeschätzt. Die Wiederholungen werden mit Abstand wieder angeboten.'),
      element('p', '', 'Nach einem erfolgreichen Abruf kommt eine Karte nach 1, dann nach 3 und später nach 7 Tagen wieder. Mehrere Antworten am selben Tag zählen nicht als mehrere Lerntage.'));
    var row = controls(a); row.append(button('Zur Trainingsübersicht', function () { home(true); }, true));
    if (data.cases.length) row.append(button('Jetzt einen Praxisfall lösen', startCases)); focusHeading();
  }
  function startCases() {
    caseQueue = data.cases.filter(function (c) { return state.cases[c.id] !== true; });
    if (!caseQueue.length) caseQueue = data.cases.slice();
    casePosition = 0; caseCorrect = 0; dashboard.hidden = true; showCase();
  }
  function showCase() {
    if (casePosition >= caseQueue.length) return finishCases();
    var c = caseQueue[casePosition], a = article('Fall ' + (casePosition + 1) + ' von ' + caseQueue.length + ' · alle Firmen und Situationen ausgedacht', c.title);
    a.append(element('p', 'lt-scene', c.scene));
    var form = element('form'), set = element('fieldset', 'lt-options');
    set.append(element('legend', '', 'Welche Antwort passt am besten?'));
    c.options.forEach(function (text, index) {
      var label = element('label', 'lt-option'), input = element('input'); input.type = 'radio'; input.name = 'lt-choice'; input.value = index; input.required = true;
      label.append(input, element('span', '', text)); set.append(label);
    });
    form.append(set); var check = element('button', 'btn primary', 'Entscheidung prüfen'); check.type = 'submit';
    controls(form).append(check, button('Später weiterüben', function () { home(true); })); a.append(form);
    form.addEventListener('submit', function (event) {
      event.preventDefault(); var selected = q('input:checked', form); if (!selected || check.disabled) return;
      var index = Number(selected.value), correct = index === c.correct; check.disabled = true; set.disabled = true;
      state.cases[c.id] = correct; if (correct) caseCorrect++; save();
      var feedback = element('div', 'lt-feedback' + (correct ? ' is-correct' : ''));
      feedback.append(element('h4', '', correct ? 'Das ist der entscheidende Gedanke.' : 'Hier lohnt sich ein zweiter Blick.'), element('p', '', c.feedback[index]));
      if (!correct) feedback.append(element('p', '', 'Passender wäre: ' + c.options[c.correct]), element('p', '', c.feedback[c.correct]));
      feedback.append(element('p', 'lt-takeaway', 'Merken: ' + c.takeaway));
      var more = element('details'); more.append(element('summary', '', 'Warum die anderen Antworten nicht passen'));
      c.options.forEach(function (option, i) { if (i !== index && i !== c.correct) { more.append(element('h5', '', option), element('p', '', c.feedback[i])); } }); feedback.append(more);
      var link = element('a', '', 'Passendes Learning nachlesen →'); link.href = '#lrn-' + c.learning; feedback.append(link);
      if (c.article) { var source = element('a', 'lt-source', 'Amtliche Quelle: Artikel ' + c.article); source.href = 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-' + c.article; source.target = '_blank'; source.rel = 'noopener'; feedback.append(source); }
      a.append(feedback); controls(a).append(button(casePosition + 1 === caseQueue.length ? 'Runde abschließen' : 'Nächster Fall →', function () { casePosition++; showCase(); }, true));
      feedback.tabIndex = -1; feedback.focus({preventScroll: true}); feedback.scrollIntoView({block: 'nearest', behavior: 'instant'});
    }); focusHeading();
  }
  function finishCases() {
    var unresolved = data.cases.filter(function (c) { return state.cases[c.id] !== true; });
    var a = article('Fallwerkstatt abgeschlossen', 'Jetzt auf eine eigene Situation übertragen.');
    a.append(element('p', 'lt-count', caseCorrect + ' von ' + caseQueue.length + ' Entscheidungen in dieser Runde richtig.'), element('p', '', 'Welche Frage würde man bei einem neuen KI-Einsatz als Erstes stellen? Einen eigenen Merksatz kann man unten festhalten.'));
    if (unresolved.length) { a.append(element('p', '', 'Diese Fälle lohnen sich noch einmal:')); var list = element('ul'); unresolved.forEach(function (c) { list.append(element('li', '', c.title)); }); a.append(list); }
    var row = controls(a); if (unresolved.length) row.append(button('Unsichere Fälle erneut üben', startCases, true));
    row.append(button('Zur Trainingsübersicht', function () { home(true); })); focusHeading();
  }
  home(false);
}());
