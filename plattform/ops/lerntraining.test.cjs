const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const context = {module:{exports:{}}, console};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../public/assets/lerntraining-core.js'),'utf8'), context);
const C = context.module.exports;

test('Wiederholung nach 1, 3 und 7 Tagen; mehrfach am selben Tag zählt nicht doppelt', () => {
  let r = C.rate(null, true, '2026-10-14');
  assert.equal(JSON.stringify(r), JSON.stringify({step:1, due:'2026-10-15', lastDay:'2026-10-14'}));
  assert.equal(JSON.stringify(C.rate(r, true, '2026-10-14')), JSON.stringify(r));
  r = C.rate(r, true, '2026-10-15'); assert.equal(r.due, '2026-10-18');
  r = C.rate(r, true, '2026-10-18'); assert.equal(r.due, '2026-10-25');
  r = C.rate(r, true, '2026-10-25'); assert.equal(r.due, '2026-11-01');
});
test('Unsicher setzt den Abstand zurück und bleibt sofort fällig', () => {
  let r = C.rate({step:3,due:'2026-10-15',lastDay:'2026-10-08'}, false, '2026-10-15');
  assert.equal(r.step, 0); assert.equal(r.due, '2026-10-15');
  r = C.rate(r, true, '2026-10-15'); assert.equal(r.due, '2026-10-16');
});
test('Kalendertage funktionieren über Sommerzeit, Monats- und Jahreswechsel', () => {
  assert.equal(C.shift('2026-10-24', 3), '2026-10-27');
  assert.equal(C.shift('2026-12-31', 1), '2027-01-01');
  assert.equal(C.shift('2028-02-28', 1), '2028-02-29');
});
test('Fällige ältere Tage vor neuen Karten; keine unbegrenzt lange Runde', () => {
  const cards = [{id:'old',day:2}, ...Array.from({length:10}, (_,i)=>({id:'new'+i,day:12})), {id:'later',day:12}];
  const records = {old:{step:1,due:'2026-10-13',lastDay:'2026-10-12'},later:{step:1,due:'2026-10-20',lastDay:'2026-10-19'}};
  const r = C.round(cards, records, '2026-10-14', 12, ()=>0.5);
  assert.equal(r.cards.length, 5); assert.equal(r.cards[0].id, 'old');
  assert(!r.cards.some(c=>c.id==='later')); assert.equal(r.practice, false);
});
test('Keine ungelernten früheren Tage beim Einstieg in den aktuellen Tag', () => {
  const r = C.round([{id:'old',day:1},{id:'new',day:12}], {}, '2026-10-14',12);
  assert.deepEqual(r.cards.map(c=>c.id), ['new']);
});
test('Alles erledigt erlaubt eine zusätzliche Runde ohne neue Fälligkeit zu behaupten', () => {
  const r = C.round([{id:'a',day:12}], {a:{step:1,due:'2026-10-15',lastDay:'2026-10-14'}}, '2026-10-14',12);
  assert.equal(r.practice, true); assert.equal(r.cards.length,1);
});
test('Ungültige lokale Datensätze werden wie neue Karten behandelt', () => {
  for(const value of [null, 'kaputt', {}, {step:99,due:'2026-10-14',lastDay:'2026-10-14'}, {step:1,due:'morgen',lastDay:'2026-10-14'}, {step:1,due:'2026-02-31',lastDay:'2026-10-14'}]) {
    assert.equal(C.record(value), null);
    const r = C.round([{id:'a',day:12}],{a:value},'2026-10-14',12);
    assert.equal(r.practice,false); assert.equal(r.cards.length,1);
  }
});
