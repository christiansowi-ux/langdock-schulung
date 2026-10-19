// HTML -> PDF (A4) mit dem Chromium aus playwright-core der STILLE-Website-QA.
//   node render.mjs jobs.json      jobs = [{html, pdf, pdfPlain, label}]
// pdf = mit Fusszeile, pdfPlain = ohne (daraus nimmt build.py nur die Titelseite).
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const PW = "C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs";
const { chromium } = await import(pathToFileURL(PW).href);

const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch();
const margin = { top: "14mm", bottom: "17mm", left: "16mm", right: "16mm" };

for (const job of jobs) {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(job.html).href, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  const fontOk = await page.evaluate(() => document.fonts.check('700 12px "Archivo"') && document.fonts.check('400 12px "Archivo"'));
  const footer = `
    <div style="width:100%; padding:0 16mm; font-family:'Segoe UI',Arial,sans-serif; font-size:7.5pt; color:#6b6f73; display:flex; justify-content:space-between; align-items:center;">
      <span><b style="color:#111">KI Automations Spezialist</b> &nbsp;·&nbsp; Praxisblock Langdock &nbsp;·&nbsp; ${job.label}</span>
      <span>Seite <span class="pageNumber"></span> von <span class="totalPages"></span></span>
    </div>`;
  await page.pdf({ path: job.pdf, format: "A4", printBackground: true, margin,
    displayHeaderFooter: true, headerTemplate: "<span></span>", footerTemplate: footer });
  await page.pdf({ path: job.pdfPlain, format: "A4", printBackground: true, margin });
  await page.close();
  console.log(`PDF ${job.pdf}  (Archivo geladen: ${fontOk})`);
}
await browser.close();
