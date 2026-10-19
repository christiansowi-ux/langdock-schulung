// Prueft im Druck-Layout, ob jede .lp-Seite auf ihre A4-Seite passt:  node measure_lp.mjs datei.html [--fit ausgabe.json]
// --fit: misst den Platzbedarf (Merksatz direkt unter dem Inhalt) und schreibt je Seite einen Zoom, der die Seite fuellt.
import { pathToFileURL } from "node:url";
import { writeFileSync } from "node:fs";
const PW = "C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs";
const { chromium } = await import(pathToFileURL(PW).href);
const fitOut = process.argv.includes("--fit") ? process.argv[process.argv.indexOf("--fit") + 1] : null;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 673, height: 1000 } }); // 178 mm bei 96 dpi
await p.emulateMedia({ media: "print" });
await p.goto(pathToFileURL(process.argv[2]).href, { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const MM = 96 / 25.4;
if (fitOut) {
  // je Seite die groesste Zoomstufe suchen, bei der nichts ueberlaeuft (Hoehe und Breite)
  const zoom = await p.$$eval(".lp", (els) => els.map((e, i) => {
    if (i === 0) return 1;
    let best = 1;
    for (let z = 1.36; z >= 1.0; z = Math.round((z - 0.02) * 100) / 100) {
      e.style.setProperty("--z", String(z));
      const okH = e.scrollHeight - e.clientHeight <= 1;
      const okW = e.scrollWidth - e.clientWidth <= 1;
      const merk = e.querySelector(".merk");
      const okM = !merk || !merk.previousElementSibling || merk.getBoundingClientRect().top - merk.previousElementSibling.getBoundingClientRect().bottom >= 14;
      if (okH && okW && okM) { best = z; break; }
    }
    e.style.removeProperty("--z");
    return best;
  }));
  writeFileSync(fitOut, JSON.stringify(zoom));
  console.log("Zoom je Seite:", zoom.join(" "));
  await b.close();
  process.exit(0);
}
const res = await p.$$eval(".lp", (els) => els.map((e, i) => {
  const mm = (px) => Math.round(px * 25.4 / 96 * 10) / 10;
  const z = parseFloat(getComputedStyle(e).zoom || 1);
  const merk = e.querySelector(".merk");
  let free = null;
  if (merk && merk.previousElementSibling) free = mm(merk.getBoundingClientRect().top - merk.previousElementSibling.getBoundingClientRect().bottom);
  const r = e.getBoundingClientRect();
  return { i: i + 1, id: e.id || "", z, h: mm(r.height), over: e.scrollHeight - e.clientHeight, wide: e.scrollWidth - e.clientWidth, free };
}));
let bad = 0;
for (const r of res) {
  const over = r.over > 2 || r.wide > 2;
  if (over) bad++;
  console.log(`Seite ${String(r.i).padStart(2)} ${r.id.padEnd(4)} ${over ? "ZU GROSS" : "ok      "} Zoom ${r.z}, Hoehe ${r.h} mm${r.free != null ? `, Luft vor Merksatz ${r.free} mm` : ""}${r.wide > 2 ? `, ${r.wide}px zu breit` : ""}`);
}
await b.close();
if (bad) { console.log(`${bad} Seite(n) passen nicht`); process.exit(1); }
