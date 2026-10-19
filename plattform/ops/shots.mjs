// QA-Bilder der Plattform: node ops/shots.mjs [basis-url] [ausgabeordner]
// Desktop 1280 und Handy 390: Uebersicht, Heft-Anfang, Quiz-Stelle, geoeffnetes "Mehr"-Menue; meldet Querscrollen.
import { pathToFileURL } from 'node:url';
const PW = 'C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs';
const { chromium } = await import(pathToFileURL(PW).href);
const base = process.argv[2] || 'http://localhost:8080/hefte';
const out = process.argv[3] || '.';
const b = await chromium.launch();
for (const [tag, vp] of [['desk', { width: 1280, height: 800 }], ['mob', { width: 390, height: 844 }]]) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: tag === 'mob', hasTouch: tag === 'mob' });
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', (e) => errors.push(e.message));
  p.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: `${out}/${tag}_index.png` });
  const heft = await p.$eval('.heft', (a) => a.getAttribute('href'));
  await p.goto(new URL(heft, base).href, { waitUntil: 'networkidle' });
  await p.screenshot({ path: `${out}/${tag}_heft_top.png` });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  await p.$eval('[data-kind=quiz]', (e) => e.scrollIntoView({ block: 'center' }));
  await p.screenshot({ path: `${out}/${tag}_heft_quiz.png` });
  await p.$eval('.webbar', (e) => e.scrollIntoView());
  await p.click('.wb-more summary');
  await p.screenshot({ path: `${out}/${tag}_menu.png` });
  console.log(tag, 'Querscrollen:', overflow, 'px', errors.length ? 'FEHLER: ' + errors.join(' | ') : 'keine JS-Fehler');
  await ctx.close();
}
await b.close();
