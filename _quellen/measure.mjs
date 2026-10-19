// Misst Hoehen in mm bei A4-Druckbreite (178 mm Satzspiegel): node measure.mjs <html> [selector]
import { pathToFileURL } from "node:url";
const PW = "C:/Users/chris/Documents/Unreal Projects/Stille/website/node_modules/playwright-core/index.mjs";
const { chromium } = await import(pathToFileURL(PW).href);
const [, , html, sel = ".cover"] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(html).href, { waitUntil: "networkidle" });
await page.emulateMedia({ media: "print" });
await page.evaluate(() => { document.body.style.width = "178mm"; });
await page.evaluate(() => document.fonts.ready);
const mm = await page.evaluate((s) => [...document.querySelectorAll(s)].map(e => (e.getBoundingClientRect().height * 25.4 / 96).toFixed(1)), sel);
console.log(sel, mm.join(" "), "mm  (Seite: 266 mm)");
await browser.close();
