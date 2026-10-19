/* Kleine, deterministische Wiederholungslogik. Browser und Node verwenden denselben Code. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LerntrainingCore = factory();
}(typeof window !== 'undefined' ? window : this, function () {
  'use strict';
  function today(date) {
    var d = date || new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function shift(day, days) { var d = new Date(day + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + days); return d.toISOString().slice(0, 10); }
  function validDay(s) { return typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && !isNaN(Date.parse(s + 'T12:00:00Z')) && new Date(s + 'T12:00:00Z').toISOString().slice(0,10) === s; }
  function record(value) {
    return value && Number.isInteger(value.step) && value.step >= 0 && value.step <= 3 && validDay(value.due) && validDay(value.lastDay) ? value : null;
  }
  function rate(previous, known, day) {
    var p = record(previous);
    // Mehrmaliges Aufdecken am selben Tag ist keine langfristige Erinnerung.
    var step = known ? (p && p.lastDay === day ? Math.max(1, p.step) : Math.min(3, (p ? p.step : 0) + 1)) : 0;
    return {step: step, due: shift(day, [0, 1, 3, 7][step]), lastDay: day};
  }
  function due(cards, records, day) {
    return cards.filter(function (c) { var p = record(records[c.id]); return p && p.due <= day; })
      .sort(function (a, b) { return records[a.id].due.localeCompare(records[b.id].due) || a.day - b.day; });
  }
  function round(cards, records, day, currentDay, random) {
    var waiting = due(cards, records, day);
    var fresh = cards.filter(function (c) { return c.day === currentDay && !record(records[c.id]); });
    var pool = waiting.concat(fresh);
    var practice = pool.length === 0;
    if (practice) pool = cards.filter(function (c) { return c.day === currentDay; });
    // Fälliges bleibt vorn; neue Karten und freiwillige Zusatzrunden variieren.
    var offset = practice ? 0 : waiting.length;
    for (var i = pool.length - 1; i > offset; i--) {
      var j = offset + Math.floor((random || Math.random)() * (i - offset + 1));
      var tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp;
    }
    return {cards: pool.slice(0, 5), practice: practice};
  }
  return {today: today, shift: shift, record: record, rate: rate, due: due, round: round};
}));
