// Lernplattform quint-games.de/hefte: statische Seiten + PDF-Export (Chromium) + "Unklar?"-Fragen mit Dozenten-Zugang.
// Gespeichert wird nur, was Teilnehmende selbst als unklar melden (data/fragen.json). Heft-Antworten bleiben im Browser
// und gehen nur beim PDF-Export kurz in den Arbeitsspeicher.
import http from 'node:http';
import crypto from 'node:crypto';
import { readFile, stat, writeFile, rename, mkdir } from 'node:fs/promises';
import { createReadStream, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const DIR = path.dirname(fileURLToPath(import.meta.url));
// .env neben dem Server (lokal); im Container kommen die Werte ueber env_file
if (existsSync(path.join(DIR, '.env'))) {
  for (const line of readFileSync(path.join(DIR, '.env'), 'utf8').split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$/);
    if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}
const PUB = path.join(DIR, 'public');
const DATA = process.env.DATA_DIR || path.join(DIR, 'data');
const PORT = Number(process.env.PORT || 8080);
const BASE = (process.env.BASE || '/hefte').replace(/\/$/, '');
const PASSWORT = process.env.DOZENT_PASSWORT || '';
const SECRET = process.env.COOKIE_SECRET || crypto.randomBytes(32).toString('hex');
const CHROMIUM = process.env.CHROMIUM || [
  '/usr/bin/chromium', '/usr/bin/chromium-browser',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].find((p) => existsSync(p));

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2',
  '.pdf': 'application/pdf', '.zip': 'application/zip', '.txt': 'text/plain; charset=utf-8',
};
const HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'DENY',
  'X-Robots-Tag': 'noindex, nofollow',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self'; frame-src https://www.youtube-nocookie.com; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
};
const PERSONEN = ['carmen', 'ingo', 'tabea'];

let manifest = { hefte: {}, lernblaetter: {} };
async function loadManifest() { manifest = JSON.parse(await readFile(path.join(PUB, 'manifest.json'), 'utf8')); }
await loadManifest();

// ---------- Drosselung je IP ----------
const buckets = new Map();
function limited(kind, ip, max, win) {
  const now = Date.now(), k = kind + '|' + ip;
  const list = (buckets.get(k) || []).filter((t) => now - t < win);
  list.push(now); buckets.set(k, list);
  if (buckets.size > 20000) buckets.clear();
  return list.length > max;
}
const ipOf = (req) => String(req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();

// ---------- Fragen ("Unklar?") ----------
let fragen = [];
let saveTimer = null;
try { fragen = JSON.parse(await readFile(path.join(DATA, 'fragen.json'), 'utf8')); if (!Array.isArray(fragen)) fragen = []; } catch { fragen = []; }
function persist() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(async () => {
    try {
      await mkdir(DATA, { recursive: true });
      const tmp = path.join(DATA, 'fragen.json.tmp');
      await writeFile(tmp, JSON.stringify(fragen));
      await rename(tmp, path.join(DATA, 'fragen.json'));
    } catch (e) { console.error('Speichern der Fragen fehlgeschlagen:', e.message); }
  }, 200);
}
const str = (v, max) => (typeof v === 'string' ? v : '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '').trim().slice(0, max);
const publicFrage = (q) => ({ id: q.id, status: q.status, antwort: q.antwort || '', antwortTs: q.antwortTs || 0, ts: q.ts });

async function handleFragen(req, res, url) {
  const ip = ipOf(req);
  if (req.method === 'GET') {
    const ids = String(url.searchParams.get('ids') || '').split(',').filter((x) => /^[\w-]{10,40}$/.test(x)).slice(0, 100);
    const set = new Set(ids);
    return json(res, 200, fragen.filter((q) => set.has(q.id)).map(publicFrage));
  }
  if (req.method !== 'POST') return send(res, 405, 'Nicht erlaubt.');
  if (!sameOrigin(req)) return send(res, 403, 'Nicht erlaubt.');
  if (limited('frage', ip, 20, 10 * 60_000)) return send(res, 429, 'Sehr viele Meldungen – bitte kurz warten oder direkt fragen.');
  let d;
  try { d = JSON.parse(await readBody(req, 8000)); } catch (e) { return send(res, e.code || 400, e.code ? e.message : 'Ungültige Anfrage.'); }
  const person = str(d.person, 20);
  if (!PERSONEN.includes(person)) return send(res, 400, 'Bitte zuerst den eigenen Namen wählen.');
  const ref = str(d.ref, 80);
  if (!/^[\w:.\-]+$/.test(ref)) return send(res, 400, 'Ungültige Stelle.');
  let urlPath = str(d.url, 300);
  if (!urlPath.startsWith(BASE + '/') || /[\s<>"'\\]/.test(urlPath)) urlPath = '';
  const q = {
    id: crypto.randomBytes(12).toString('base64url'), person, tag: Math.max(0, Math.min(99, parseInt(d.tag, 10) || 0)),
    ref, label: str(d.label, 240) || ref, text: str(d.text, 1000), url: urlPath, ts: Date.now(), status: 'offen', antwort: '', antwortTs: 0,
  };
  fragen.push(q);
  if (fragen.length > 3000) {
    const i = fragen.findIndex((x) => x.status !== 'offen');
    fragen.splice(i >= 0 ? i : 0, 1);
  }
  persist();
  console.log(`Frage ${q.id} von ${q.person} (Tag ${q.tag}, ${q.ref})`);
  return json(res, 201, { id: q.id, status: q.status });
}

// ---------- Dozenten-Zugang ----------
function sign(exp) { return crypto.createHmac('sha256', SECRET).update('dozent.' + exp).digest('base64url'); }
function cookies(req) {
  const out = {};
  for (const part of String(req.headers.cookie || '').split(';')) {
    const i = part.indexOf('=');
    if (i > 0) out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  return out;
}
function isDozent(req) {
  const c = cookies(req).dz;
  if (!c || !PASSWORT) return false;
  const [exp, sig] = c.split('.');
  if (!exp || !sig || !(Number(exp) > Date.now())) return false;
  const a = Buffer.from(sig), b = Buffer.from(sign(exp));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
function sameOrigin(req) {
  const o = req.headers.origin;
  if (!o) return true; // alte Browser/curl: SameSite=Strict + JSON-Pflicht schuetzen trotzdem
  try { return new URL(o).host === req.headers.host; } catch { return false; }
}
function cookieHeader(value, maxAge, req) {
  const secure = String(req.headers['x-forwarded-proto'] || '').includes('https') ? '; Secure' : '';
  return `dz=${value}; Path=${BASE}; HttpOnly; SameSite=Strict; Max-Age=${maxAge}${secure}`;
}
async function handleDozent(req, res, rest) {
  const ip = ipOf(req);
  if (rest === 'status') {
    if (!isDozent(req)) return json(res, 200, { dozent: false });
    const offen = fragen.filter((q) => q.status === 'offen');
    const neu = offen.slice(-8).reverse().map((q) => ({ id: q.id, person: q.person, tag: q.tag, label: q.label, text: q.text.slice(0, 200), ts: q.ts }));
    return json(res, 200, { dozent: true, offen: offen.length, neu });
  }
  if (req.method !== 'GET' && !sameOrigin(req)) return send(res, 403, 'Nicht erlaubt.');
  if (req.method !== 'GET' && !String(req.headers['content-type'] || '').startsWith('application/json') && req.method !== 'DELETE') return send(res, 415, 'Nur JSON.');
  if (rest === 'login' && req.method === 'POST') {
    if (!PASSWORT) return send(res, 503, 'Der Zugang ist auf dem Server noch nicht eingerichtet (DOZENT_PASSWORT fehlt).');
    if (limited('login', ip, 6, 10 * 60_000)) return send(res, 429, 'Zu viele Versuche.');
    let d;
    try { d = JSON.parse(await readBody(req, 2000)); } catch { return send(res, 400, 'Ungültige Anfrage.'); }
    const a = crypto.createHash('sha256').update(String(d.passwort || '')).digest();
    const b = crypto.createHash('sha256').update(PASSWORT).digest();
    if (!crypto.timingSafeEqual(a, b)) { console.log('Dozenten-Login fehlgeschlagen'); return send(res, 401, 'Falsches Passwort.'); }
    const exp = String(Date.now() + 30 * 24 * 3600 * 1000);
    return json(res, 200, { ok: true }, { 'Set-Cookie': cookieHeader(`${exp}.${sign(exp)}`, 30 * 24 * 3600, req) });
  }
  if (rest === 'logout' && req.method === 'POST') return json(res, 200, { ok: true }, { 'Set-Cookie': cookieHeader('', 0, req) });
  if (!isDozent(req)) return send(res, 401, 'Bitte anmelden.');
  if (rest === 'fragen' && req.method === 'GET') return json(res, 200, fragen.slice().reverse());
  const m = rest.match(/^fragen\/([\w-]{10,40})$/);
  if (m) {
    const q = fragen.find((x) => x.id === m[1]);
    if (!q) return send(res, 404, 'Diese Frage gibt es nicht mehr.');
    if (req.method === 'DELETE') { fragen = fragen.filter((x) => x !== q); persist(); return json(res, 200, { ok: true }); }
    if (req.method === 'POST') {
      let d;
      try { d = JSON.parse(await readBody(req, 8000)); } catch { return send(res, 400, 'Ungültige Anfrage.'); }
      if (typeof d.antwort === 'string') { q.antwort = str(d.antwort, 2000); q.antwortTs = Date.now(); }
      if (['offen', 'beantwortet', 'erledigt'].includes(d.status)) q.status = d.status;
      if (q.status === 'beantwortet' && !q.antwort) q.status = 'erledigt';
      persist();
      return json(res, 200, q);
    }
  }
  return send(res, 404, 'Unbekannt.');
}

// ---------- PDF: ein Browser, hoechstens 2 gleichzeitig ----------
let browser = null, idleTimer = null, running = 0;
const waiting = [];
async function getBrowser() {
  if (browser && browser.connected) return browser;
  if (!CHROMIUM) throw new Error('Kein Chromium gefunden');
  browser = await puppeteer.launch({
    executablePath: CHROMIUM, headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--font-render-hinting=none', '--disable-extensions'],
  });
  browser.on('disconnected', () => { browser = null; });
  return browser;
}
function touchIdle() {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { if (browser && running === 0) { browser.close().catch(() => {}); browser = null; } }, 5 * 60 * 1000);
}
async function slot() {
  if (running < 2) { running++; return; }
  if (waiting.length > 20) throw Object.assign(new Error('Gerade sehr viele PDF-Anfragen – bitte in einer Minute noch einmal.'), { code: 503 });
  await new Promise((r) => waiting.push(r));
  running++;
}
function release() { running--; const n = waiting.shift(); if (n) n(); touchIdle(); }

async function renderPdf(pagePath, ready, prepare) {
  await slot();
  let page;
  try {
    const b = await getBrowser();
    page = await b.newPage();
    const allowed = `http://127.0.0.1:${PORT}${BASE}/`;
    await page.setRequestInterception(true);
    page.on('request', (r) => (r.url().startsWith(allowed) || r.url().startsWith('data:') ? r.continue() : r.abort()));
    await page.goto(allowed + pagePath, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.waitForFunction(ready, { timeout: 10000 });
    if (prepare) await prepare(page);
    await page.evaluate(() => document.fonts.ready);
    return await page.pdf({ printBackground: true, preferCSSPageSize: true, timeout: 60000 });
  } finally {
    if (page) await page.close().catch(() => {});
    release();
  }
}

function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > limit) { reject(Object.assign(new Error('Zu viel Text.'), { code: 413 })); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}
function clean(answers) {
  const out = {};
  if (!answers || typeof answers !== 'object' || Array.isArray(answers)) return out;
  let n = 0;
  for (const [k, v] of Object.entries(answers)) {
    if (!/^f\d{1,4}$/.test(k) || typeof v !== 'string') continue;
    out[k] = v.slice(0, 20000);
    if (++n >= 3000) break;
  }
  return out;
}

async function handlePdf(req, res) {
  if (limited('pdf', ipOf(req), 8, 60_000)) return send(res, 429, 'Bitte kurz warten – zu viele PDF-Anfragen in einer Minute.');
  let data;
  try { data = JSON.parse(await readBody(req, 400_000)); } catch (e) { return send(res, e.code || 400, e.code ? e.message : 'Ungültige Anfrage.'); }
  let pdf, file;
  try {
    if (data && data.lernblatt) {
      const key = String(data.lernblatt);
      const lb = Object.prototype.hasOwnProperty.call(manifest.lernblaetter, key) ? manifest.lernblaetter[key] : null;
      if (!lb) return send(res, 404, 'Dieses Lernblatt gibt es nicht.');
      const valid = new Set(Object.values(lb.ids).flat());
      const ids = (Array.isArray(data.ids) ? data.ids : []).map(String).filter((x) => valid.has(x)).slice(0, 60);
      const pagePath = (key.endsWith('/alle') ? key.replace(/\/alle$/, '/lernblatt/') : key + '/lernblatt/') + '?pdf=1' + (ids.length ? '&ids=' + ids.join(',') : '');
      pdf = await renderPdf(pagePath, 'window.LERNBLATT && window.LERNBLATT.ready');
      file = lb.file + (ids.length ? '_Auswahl' : '');
    } else {
      const heft = String(data && data.heft || '');
      if (!Object.prototype.hasOwnProperty.call(manifest.hefte, heft)) return send(res, 404, 'Dieses Heft gibt es nicht.');
      const answers = clean(data.answers);
      const hp = String(manifest.hefte[heft].path || heft + '/');
      pdf = await renderPdf(`${hp}?pdf=1`, 'window.HEFT && window.HEFT.ready', (page) => page.evaluate((a) => window.HEFT.apply(a), answers));
      file = manifest.hefte[heft].file;
    }
  } catch (e) {
    console.error('PDF-Fehler', e && e.message); // keine Antworten ins Log
    return send(res, e.code || 500, e.code ? e.message : 'Das PDF konnte nicht erstellt werden.');
  }
  res.writeHead(200, { ...HEADERS, 'Content-Type': 'application/pdf', 'Content-Length': pdf.length, 'Cache-Control': 'no-store',
    'Content-Disposition': `attachment; filename="${file}.pdf"` });
  res.end(pdf);
}

// ---------- Antworten ----------
function send(res, code, text, extra = {}) {
  res.writeHead(code, { ...HEADERS, 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store', ...extra });
  res.end(text);
}
function json(res, code, obj, extra = {}) {
  const body = JSON.stringify(obj);
  res.writeHead(code, { ...HEADERS, 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extra });
  res.end(body);
}

async function serveStatic(req, res, rel) {
  let p;
  try { p = decodeURIComponent(rel); } catch { return send(res, 400, 'Ungültige Adresse.'); }
  let file = path.normalize(path.join(PUB, p));
  if (!file.startsWith(PUB)) return send(res, 403, 'Nein.');
  let st = await stat(file).catch(() => null);
  if (st && st.isDirectory()) {
    if (!rel.endsWith('/')) return send(res, 301, '', { Location: BASE + rel + '/' });
    file = path.join(file, 'index.html');
    st = await stat(file).catch(() => null);
  }
  if (!st || !st.isFile() || path.basename(file) === 'manifest.json') return notFound(res);
  const ext = path.extname(file).toLowerCase();
  const lm = st.mtime.toUTCString();
  const cache = ext === '.woff2' ? 'public, max-age=2592000'
    : ext === '.png' || ext === '.jpg' || ext === '.svg' ? 'public, max-age=86400'
      : ext === '.pdf' ? 'public, max-age=3600' : 'no-cache';
  if (req.headers['if-modified-since'] === lm) { res.writeHead(304, { ...HEADERS, 'Last-Modified': lm, 'Cache-Control': cache }); return res.end(); }
  res.writeHead(200, { ...HEADERS, 'Content-Type': MIME[ext] || 'application/octet-stream', 'Content-Length': st.size, 'Last-Modified': lm, 'Cache-Control': cache });
  if (req.method === 'HEAD') return res.end();
  createReadStream(file).pipe(res);
}
async function notFound(res) {
  const html = `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Nicht gefunden</title><link rel="stylesheet" href="${BASE}/assets/app.css"><link rel="stylesheet" href="${BASE}/assets/kurs.css"></head><body class="kurs"><main class="wrap hero"><p class="kicker">Fehler 404</p><h1>Diese Seite gibt es nicht.</h1><p class="lead"><a href="${BASE}/">Zur Lernplattform</a></p></main></body></html>`;
  res.writeHead(404, { ...HEADERS, 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(html);
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    const p = url.pathname;
    if (p === BASE) return send(res, 301, '', { Location: BASE + '/' });
    if (!p.startsWith(BASE + '/')) return notFound(res);
    const rel = p.slice(BASE.length);
    if (rel === '/healthz') return send(res, 200, 'ok');
    if (rel === '/api/pdf') return req.method === 'POST' ? handlePdf(req, res) : send(res, 405, 'Nur POST.', { Allow: 'POST' });
    if (rel === '/api/fragen') return handleFragen(req, res, url);
    if (rel.startsWith('/api/dozent/')) return handleDozent(req, res, rel.slice('/api/dozent/'.length));
    if (rel.startsWith('/api/')) return send(res, 404, 'Unbekannt.');
    if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'Nicht erlaubt.');
    return serveStatic(req, res, rel);
  } catch (e) {
    console.error(e);
    if (!res.headersSent) send(res, 500, 'Serverfehler.');
  }
});
server.requestTimeout = 120_000;
server.listen(PORT, () => console.log(`Lernplattform auf :${PORT}${BASE}/ · Chromium: ${CHROMIUM || 'FEHLT'} · Dozenten-Zugang: ${PASSWORT ? 'an' : 'AUS (DOZENT_PASSWORT fehlt)'} · Fragen: ${fragen.length}`));
async function shutdown() {
  clearTimeout(saveTimer);
  try { await mkdir(DATA, { recursive: true }); await writeFile(path.join(DATA, 'fragen.json'), JSON.stringify(fragen)); } catch { /* egal */ }
  if (browser) await browser.close().catch(() => {});
  process.exit(0);
}
for (const sig of ['SIGTERM', 'SIGINT']) process.on(sig, shutdown);
