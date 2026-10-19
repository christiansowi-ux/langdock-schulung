// HTML -> PDF ohne Fusszeile (Uebungsdokumente):  node render_plain.mjs jobs.json   jobs = [{html, pdf}]
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const PW = "C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs";
const { chromium } = await import(pathToFileURL(PW).href);
const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch();
for (const job of jobs) {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(job.html).href, { waitUntil: "networkidle" });
  await page.pdf({ path: job.pdf, format: "A4", printBackground: true, preferCSSPageSize: true });
  await page.close();
}
await browser.close();
console.log(`${jobs.length} PDFs`);
