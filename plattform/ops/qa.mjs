// Prueflauf der Lernplattform:  node ops/qa.mjs [basis-url] [ausgabeordner] [--flow]
// Bilder Desktop 1280 / Handy 390 je Seitentyp, Querscrollen + JS-Fehler; mit --flow zusaetzlich der Ablauf
// "Unklar? melden -> Schulungsleitung antwortet -> Antwort erscheint" und die PDF-Exporte (Heft, Lernblatt, Auswahl).
// Passwort fuer --flow: Umgebungsvariable DOZENT_PASSWORT oder plattform/.env (wird nie ausgegeben).
import { pathToFileURL, fileURLToPath } from 'node:url';
import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
const PW = 'C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs';
const { chromium } = await import(pathToFileURL(PW).href);
const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const FLOW = process.argv.includes('--flow');
const base = (args[0] || 'http://localhost:8080/hefte').replace(/\/$/, '');
const out = args[1] || '.';
mkdirSync(out, { recursive: true });
const DIR = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let pass = process.env.DOZENT_PASSWORT || '';
if (!pass && existsSync(path.join(DIR, '.env'))) pass = (readFileSync(path.join(DIR, '.env'), 'utf8').match(/^DOZENT_PASSWORT=(.*)$/m) || [])[1] || '';

const pages = [
  ['index', '/'], ['uebersicht', '/carmen/'], ['tag3', '/carmen/tag-3/'], ['tag3_karten', '/carmen/tag-3/#karten'],
  ['tag3_test', '/carmen/tag-3/#test'], ['tag3_folien', '/carmen/tag-3/?folie=7#folien'], ['tag3_woerter', '/carmen/tag-3/#woerter'],
  ['tag3_heftkarte', '/tabea/tag-3/#heft'], ['heft3', '/carmen/tag-3/heft/'], ['heft1', '/ingo/tag-1/heft/'], ['heft2', '/carmen/tag-2/heft/'],
  ['lernblatt', '/carmen/tag-3/lernblatt/'], ['dozent', '/dozent/'], ['tag1', '/ingo/tag-1/'], ['tag2', '/tabea/tag-2/'],
  ['tag4', '/ingo/tag-4/'], ['tag4_folien', '/carmen/tag-4/?folie=8#folien'], ['tag4_heftkarte', '/carmen/tag-4/#heft'], ['heft4', '/tabea/tag-4/heft/'], ['material4', '/material/tag-4/'], ['lernheft4', '/tabea/tag-4/lernheft/'], ['lernheft4_k5', '/ingo/tag-4/lernheft/#k5'], ['lernheft4_k9', '/carmen/tag-4/lernheft/#k9'], ['tag5', '/carmen/tag-5/'], ['tag5_lernheft', '/ingo/tag-5/#heft'], ['lernheft5', '/tabea/tag-5/lernheft/'], ['lernheft5_k10', '/tabea/tag-5/lernheft/#k10'], ['uebersicht_ingo', '/ingo/'], ['lernblatt_alle', '/ingo/lernblatt/'], ['tag6', '/carmen/tag-6/'], ['tag6_folien', '/ingo/tag-6/?folie=21#folien'], ['lernheft6', '/carmen/tag-6/lernheft/'], ['lernheft6_ueb', '/tabea/tag-6/lernheft/#k11'], ['tag7', '/tabea/tag-7/'], ['tag7_folien', '/carmen/tag-7/#folien'], ['lernheft7', '/ingo/tag-7/lernheft/'], ['lernheft7_k10', '/carmen/tag-7/lernheft/#k10'], ['lernheft7_ueb', '/carmen/tag-7/lernheft/#k14'], ['aufgaben_alle', '/carmen/aufgaben/'], ['tag6_aufgaben', '/ingo/tag-6/#aufgaben'], ['tag1_aufgaben', '/tabea/tag-1/#aufgaben'], ['tag8', '/ingo/tag-8/'], ['tag8_folien', '/carmen/tag-8/?folie=5#folien'], ['lernheft8', '/tabea/tag-8/lernheft/'], ['lernheft8_k6', '/ingo/tag-8/lernheft/#k6'], ['tag8_aufgaben', '/carmen/tag-8/#aufgaben'], ['tag9', '/tabea/tag-9/'], ['tag9_folien', '/ingo/tag-9/?folie=7#folien'], ['lernheft9', '/carmen/tag-9/lernheft/'], ['lernheft9_k4', '/tabea/tag-9/lernheft/#k4'], ['tag9_aufgaben', '/ingo/tag-9/#aufgaben'], ['tag10', '/carmen/tag-10/'], ['tag10_folien', '/tabea/tag-10/?folie=26#folien'], ['lernheft10', '/ingo/tag-10/lernheft/'], ['lernheft10_k10', '/carmen/tag-10/lernheft/#k10'], ['tag10_aufgaben', '/tabea/tag-10/#aufgaben'], ['praxis10', '/carmen/tag-10/praxis/'], ['praxis10_k6', '/ingo/tag-10/praxis/#k6'], ['praxis10_k8', '/tabea/tag-10/praxis/#k8'], ['tag10_heft', '/ingo/tag-10/#heft'], ['tag11', '/tabea/tag-11/'], ['tag11_folien', '/carmen/tag-11/?folie=12#folien'], ['lernheft11', '/ingo/tag-11/lernheft/'], ['lernheft11_k9', '/tabea/tag-11/lernheft/#k9'], ['tag11_aufgaben', '/carmen/tag-11/#aufgaben'],
];
pages.push(['tag12', '/carmen/tag-12/'], ['tag12_folien', '/ingo/tag-12/?folie=23#folien'], ['tag12_test', '/tabea/tag-12/#test'], ['tag12_aufgaben', '/ingo/tag-12/#aufgaben'], ['lernheft12', '/tabea/tag-12/lernheft/'], ['lernheft12_ueb', '/carmen/tag-12/lernheft/#k14'], ['lernheft12_quellen', '/ingo/tag-12/lernheft/#k18']);
const b = await chromium.launch();
let fail = 0;
for (const [tag, vp] of [['desk', { width: 1280, height: 860 }], ['mob', { width: 390, height: 844 }]]) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: tag === 'mob', hasTouch: tag === 'mob' });
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', (e) => errors.push(e.message));
  p.on('console', (m) => m.type() === 'error' && !/youtube/.test(m.text()) && errors.push(m.text()));
  for (const [name, url] of pages) {
    await p.goto(base + url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(250);
    const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    await p.screenshot({ path: `${out}/${tag}_${name}.png`, fullPage: false });
    if (ov > 0) { fail++; console.log(`FEHL ${tag} ${name}: Querscrollen ${ov}px`); }
  }
  // Heft: Learnings am Ende
  await p.goto(base + '/carmen/tag-3/heft/#lrn-anchor', { waitUntil: 'networkidle' });
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/${tag}_heft3_learnings.png` });
  // Lernkarte umdrehen, Test beantworten
  await p.goto(base + '/carmen/tag-3/#karten', { waitUntil: 'networkidle' });
  await p.click('.kcard'); await p.waitForTimeout(700);
  await p.screenshot({ path: `${out}/${tag}_karte_hinten.png` });
  await p.goto(base + '/carmen/tag-3/#test', { waitUntil: 'networkidle' });
  await p.click('.qopt >> nth=1'); await p.waitForTimeout(200);
  await p.screenshot({ path: `${out}/${tag}_test_antwort.png` });
  console.log(tag, errors.length ? 'JS-FEHLER: ' + [...new Set(errors)].join(' | ') : 'keine JS-Fehler');
  if (errors.length) fail++;
  await ctx.close();
}

if (FLOW) {
  const ctx = await b.newContext({ viewport: { width: 1280, height: 860 }, acceptDownloads: true });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', (e) => errs.push(e.message));
  const ok = (cond, msg) => { console.log((cond ? 'OK   ' : 'FEHL ') + msg); if (!cond) fail++; };
  // 1. Teilnehmerin meldet Learning 3 als unklar
  await p.goto(base + '/carmen/tag-3/', { waitUntil: 'networkidle' });
  await p.click('#lrn-l3 .unklar');
  await p.fill('#ux-text', 'Prueflauf: Was genau ist HTTPS?');
  await p.click('.ux-btn.primary');
  await p.waitForSelector('.ux-toast');
  ok(await p.$eval('#lrn-l3 .unklar', (e) => e.classList.contains('sent')), 'Unklar gemeldet, Knopf zeigt „Gemeldet“');
  // im Heft: Knopf an Aufgabe 2 Schritt 1
  await p.goto(base + '/carmen/tag-3/heft/', { waitUntil: 'networkidle' });
  const nHeft = await p.$$eval('.step-t .unklar, .task-head .unklar', (x) => x.length);
  ok(nHeft >= 15, `Heft hat ${nHeft} Unklar-Knöpfe`);
  const nLrn = await p.$$eval('.lrn-section li .unklar', (x) => x.length);
  ok(nLrn === 12, `Learnings am Heftende mit Unklar + Auswahl (${nLrn})`);
  // Lernblatt-PDF (Auswahl) aus dem Heft
  await p.click('.lrn-section li:nth-child(2) .lrn-ctl input');
  await p.click('.lrn-section li:nth-child(5) .lrn-ctl input');
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 60000 }), p.click('.lrn-tools button:nth-of-type(2)')]);
  const f1 = path.join(out, 'auswahl.pdf'); await dl.saveAs(f1);
  ok(readFileSync(f1).slice(0, 4).toString() === '%PDF', 'Auswahl-Lernblatt als PDF: ' + dl.suggestedFilename());
  // Heft-PDF mit Eingabe
  await p.click('.nfv'); await p.keyboard.type('Carmen Prueflauf');
  await p.waitForTimeout(500);
  const [dl2] = await Promise.all([p.waitForEvent('download', { timeout: 90000 }), p.click('#wb-pdf')]);
  const f2 = path.join(out, 'heft.pdf'); await dl2.saveAs(f2);
  ok(readFileSync(f2).slice(0, 4).toString() === '%PDF', 'Heft-PDF: ' + dl2.suggestedFilename());
  // 2. Schulungsleitung
  const d = await b.newContext({ viewport: { width: 1280, height: 860 } });
  const dp = await d.newPage();
  await dp.goto(base + '/dozent/', { waitUntil: 'networkidle' });
  await dp.fill('#dz-pw', 'falsch'); await dp.click('#dz-login button');
  await dp.waitForSelector('.dz-err:not([hidden])');
  ok(true, 'Falsches Passwort wird abgelehnt');
  if (!pass) { ok(false, 'kein DOZENT_PASSWORT fuer den Test'); }
  else {
    await dp.fill('#dz-pw', pass); await dp.click('#dz-login button');
    await dp.waitForSelector('#dz-board:not([hidden]) .dz-item', { timeout: 10000 });
    const txt = await dp.$eval('.dz-item', (e) => e.textContent);
    ok(/Carmen/.test(txt) && /HTTPS/.test(txt), 'Frage ist bei der Schulungsleitung angekommen');
    await dp.screenshot({ path: `${out}/desk_dozent_board.png` });
    // Glocke auf einer Personenseite
    await dp.goto(base + '/carmen/', { waitUntil: 'networkidle' });
    await dp.waitForSelector('.dz-bell .badge', { timeout: 8000 });
    ok(+(await dp.$eval('.dz-bell .badge', (e) => e.textContent)) >= 1, 'Glocke oben zeigt offene Fragen');
    await dp.click('.dz-bell > button'); await dp.waitForTimeout(200);
    await dp.screenshot({ path: `${out}/desk_glocke.png` });
    await dp.goto(base + '/dozent/', { waitUntil: 'networkidle' });
    await dp.waitForSelector('.dz-item textarea');
    const item = await dp.$('.dz-item:has-text("Prueflauf")');
    await (await item.$('textarea')).fill('HTTPS heißt: Die Nachricht reist verschlüsselt – wie ein versiegelter Brief.');
    await (await item.$('.btn.primary')).click();
    await dp.waitForTimeout(800);
  }
  // 3. Antwort erscheint bei Carmen
  await p.goto(base + '/carmen/tag-3/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  ok(await p.$eval('#lrn-l3 .unklar', (e) => e.classList.contains('answered')), 'Antwort erscheint am Knopf („Antwort da“)');
  await p.screenshot({ path: `${out}/desk_antwort_toast.png` });
  await p.goto(base + '/carmen/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  ok(/versiegelter Brief/.test(await p.$eval('#meine-fragen', (e) => e.textContent)), 'Antwort steht in „Meine Fragen“');
  await p.screenshot({ path: `${out}/desk_meine_fragen.png`, fullPage: true });
  // Aufraeumen: Testfrage loeschen
  if (pass) {
    await dp.goto(base + '/dozent/', { waitUntil: 'networkidle' });
    await dp.click('[data-f="alle"]');
    dp.on('dialog', (x) => x.accept());
    for (let i = 0; i < 20; i++) {
      const it = await dp.$('.dz-item:has-text("Prueflauf") .btn.del');
      if (!it) break;
      await it.click(); await dp.waitForTimeout(600);
    }
    ok(!(await dp.$('.dz-item:has-text("Prueflauf")')), 'Testfrage wieder gelöscht');
  }
  // Lernheft Tag 6: Uebungs-Prompts haben Kopier-Knoepfe
  await p.goto(base + '/carmen/tag-6/lernheft/#k11', { waitUntil: 'networkidle' });
  const nCopy = await p.$$eval('.ucode .ucopy', (x) => x.length);
  ok(nCopy === 7, `Lernheft 6: ${nCopy} Kopier-Knöpfe an den Übungs-Prompts`);
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write']).catch(() => {});
  await p.click('.ucode .ucopy'); await p.waitForTimeout(300);
  ok(await p.$eval('.ucode .ucopy', (e) => e.classList.contains('done')), 'Kopieren bestätigt („Kopiert“)');
  // Praxisheft Tag 10: Knopf auf der Tagesseite, Kopier-Knoepfe an Adressen und Prompts
  await p.goto(base + '/carmen/tag-10/', { waitUntil: 'networkidle' });
  ok(!!(await p.$('.hero .btn.praxis[href$="/tag-10/praxis/"]')), 'Tag 10 hat den Praxisheft-Knopf');
  await p.goto(base + '/carmen/tag-10/praxis/', { waitUntil: 'networkidle' });
  const nPx = await p.$$eval('.ucode .ucopy', (x) => x.length);
  const nReg = await p.$$eval('.reg code .ucopy', (x) => x.length);
  ok(nPx >= 18 && nReg === 16, `Praxisheft: ${nPx} Kopier-Knöpfe an Schritten, ${nReg} an den Server- und API-Listen`);
  ok((await p.$$eval('.unklar[data-unklar-ref^="t10:praxis:"]', (x) => x.length)) === 12, 'Praxisheft: Unklar an jeder Station');
  // Aufgabengenerator: wuerfeln, Filter, gleiche Nummer = gleiche Aufgabe, Geschafft
  await p.goto(base + '/carmen/tag-7/#aufgaben', { waitUntil: 'networkidle' });
  await p.waitForSelector('.aufg-card .aufg-title');
  const code1 = await p.$eval('.aufg-code code', (e) => e.textContent);
  ok(/^t7-|^g-\w+~7\./.test(code1), 'Generator Tag 7 würfelt eine Tag-7-Aufgabe: ' + code1);
  const n1 = await p.$$eval('.aufg-card .aprompt .ucopy', (x) => x.length);
  ok(n1 >= 1, `Aufgabe hat ${n1} Prompt(s) mit Kopier-Knopf`);
  await p.click('.aufg-roll'); await p.waitForTimeout(250);
  const code2 = await p.$eval('.aufg-code code', (e) => e.textContent);
  ok(code2 !== code1, 'Neue Aufgabe würfeln ändert die Aufgabe');
  await p.selectOption('.aufg-dauer', '10'); await p.waitForTimeout(250);
  ok(/10 Min/.test(await p.$eval('.aufg-kicker', (e) => e.textContent)), 'Filter „10 Minuten“ wirkt');
  await p.selectOption('.aufg-dauer', ''); await p.selectOption('.aufg-bereich', 'video'); await p.waitForTimeout(250);
  ok(/Video/.test(await p.$eval('.aufg-kicker', (e) => e.textContent)), 'Bereich „Video & Design“ wirkt');
  await p.selectOption('.aufg-bereich', 'mein');
  const prompt1 = await p.$eval('.aufg-card .aprompt', (e) => e.firstChild.textContent);
  const code3 = await p.$eval('.aufg-code code', (e) => e.textContent);
  const p2 = await ctx.newPage();
  await p2.goto(base + '/ingo/tag-7/?aufgabe=' + encodeURIComponent(code3) + '#aufgaben', { waitUntil: 'networkidle' });
  await p2.waitForSelector('.aufg-card .aprompt');
  ok((await p2.$eval('.aufg-card .aprompt', (e) => e.firstChild.textContent)) === prompt1, 'Gleiche Nummer = gleiche Aufgabe (auch für eine andere Person)');
  await p2.close();
  await p.click('.aufg-done'); await p.waitForTimeout(150);
  ok((await p.$eval('.aufg-done', (e) => e.getAttribute('aria-pressed'))) === 'true' && /ausprobiert/.test(await p.$eval('.aufg-stat', (e) => e.textContent)), '„Geschafft“ wird gezählt');
  await p.click('.aufg-done');
  ok(!!(await p.$('.aufg-card .unklar[data-unklar-ref^="t7:aufgabe:"]')), 'Aufgabe hat „Unklar?“ für die Schulungsleitung');
  await p.goto(base + '/carmen/aufgaben/', { waitUntil: 'networkidle' });
  await p.waitForSelector('.aufg-card .aufg-title');
  ok((await p.$$eval('.aufg-days input', (x) => x.length)) >= 7, 'Seite „Aufgaben aus allen Tagen“ mit Tag-Auswahl');
  // Deep Learn: Modus, 5 Etappen = 60 Min, Uhr, Etappe abhaken bleibt gespeichert
  await p.goto(base + '/tabea/tag-7/#aufgaben', { waitUntil: 'networkidle' });
  await p.waitForSelector('.aufg-card .aufg-title');
  await p.click('.aufg-mode [data-mode="deep"]'); await p.waitForTimeout(300);
  const dcode = await p.$eval('.aufg-code code', (e) => e.textContent);
  ok(/^dl-/.test(dcode), 'Modus „Deep Learn“ würfelt eine Stunden-Aufgabe: ' + dcode);
  const mins = await p.$$eval('.aufg-fahrplan small', (x) => x.reduce((n, e) => n + parseInt(e.textContent, 10), 0));
  ok((await p.$$eval('.aufg-etappe', (x) => x.length)) === 5 && mins === 60, `5 Etappen mit zusammen ${mins} Minuten`);
  await p.click('.aufg-uhr-start'); await p.waitForTimeout(1200);
  ok(/von 60:00/.test(await p.$eval('.aufg-uhr-info', (e) => e.textContent)), 'Stunden-Uhr läuft');
  await p.check('#etappe-1 .et-done input'); await p.waitForTimeout(150);
  await p.reload({ waitUntil: 'networkidle' }); await p.waitForSelector('#etappe-1');
  ok(await p.$eval('#etappe-1 .et-done input', (e) => e.checked) && /Etappe 2/.test(await p.$eval('.aufg-uhr-info', (e) => e.textContent)),
    'Etappe 1 bleibt abgehakt, Uhr zeigt jetzt Etappe 2');
  ok((await p.$$eval('.aufg-etappe .unklar', (x) => x.length)) === 5, '„Unklar?“ an jeder Etappe');
  await p.click('.aufg-uhr-reset'); await p.uncheck('#etappe-1 .et-done input');
  await p.click('.aufg-mode [data-mode="kurz"]'); await p.waitForTimeout(250);
  ok(!/^dl-/.test(await p.$eval('.aufg-code code', (e) => e.textContent)), 'Zurück zu den Kurzaufgaben');
  // Aufgabengenerator: jede Tagesseite zeigt nur Aufgaben ihres Tages (kurz und Deep Learn), fremde Nummer -> richtige Tagesseite
  const dayOf = () => p.$eval('.aufg-kicker', (e) => { const t = [...e.querySelectorAll('span:not(.sep)')].map((x) => x.textContent).find((x) => /^Tag \d+$/.test(x)); return t ? t.slice(4) : '?'; });
  const wrong = [];
  for (const n of Object.keys(JSON.parse(readFileSync(path.join(DIR, 'public', 'manifest.json'), 'utf8')).lernblaetter).map((k) => (k.match(/tag-(\d+)$/) || [])[1]).filter(Boolean).filter((v, i, a) => a.indexOf(v) === i)) {
    await p.goto(`${base}/ingo/tag-${n}/#aufgaben`, { waitUntil: 'networkidle' });
    await p.waitForSelector('.aufg-card .aufg-title');
    for (const mode of ['kurz', 'deep']) {
      await p.click(`.aufg-mode [data-mode="${mode}"]`); await p.waitForTimeout(120);
      for (let i = 0; i < 6; i++) { await p.click('.aufg-roll'); await p.waitForTimeout(20); const d = await dayOf(); if (d !== n) wrong.push(`Tag ${n} ${mode}: ${d}`); }
    }
    await p.click('.aufg-mode [data-mode="kurz"]');
  }
  ok(!wrong.length, 'Generator zeigt auf jeder Tagesseite nur den eigenen Tag ' + wrong.slice(0, 5).join(' | '));
  await p.goto(base + '/ingo/tag-3/?aufgabe=t7-json.d1.55#aufgaben', { waitUntil: 'networkidle' });
  await p.waitForSelector('.aufg-card .aufg-title');
  ok(/\/tag-7\//.test(p.url()) && (await dayOf()) === '7', 'Aufgaben-Nummer eines anderen Tages führt zur richtigen Tagesseite');
  ok(!errs.length, 'keine JS-Fehler im Ablauf ' + errs.join(' | '));
  await d.close(); await ctx.close();
}
await b.close();
console.log(fail ? `${fail} Problem(e)` : 'Alles in Ordnung');
process.exit(fail ? 1 : 0);
