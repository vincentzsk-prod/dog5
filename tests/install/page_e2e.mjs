// SPDX-License-Identifier: GPL-3.0-only
// Headless Chromium drives the real docs/install/index.html (served on http://localhost) against a fake WebMIDI FM-1
// (fake_midi.js). Checks the dry run (no MIDI at all), the confirm step (no UPGRADE byte before it), a full install, a
// cut-off and the resume. NOT a hardware test. Needs the pre-installed Playwright (require("playwright")).
//   node page_e2e.mjs PY.json docs/install [screenshot.png]
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const [pyPath, dir, shot] = process.argv.slice(2);
const py = JSON.parse(fs.readFileSync(pyPath, "utf8"));
let bad = 0, n = 0;
const check = (what, ok, extra = "") => { n++; if (!ok) bad++; console.log(`${ok ? "ok  " : "FAIL"} ${what}${extra ? "  " + extra : ""}`); };

const srv = http.createServer((req, res) => {
  const f = path.join(dir, req.url === "/" ? "index.html" : req.url.split("?")[0]);
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); res.end(); } else { res.writeHead(200, { "content-type": f.endsWith(".html") ? "text/html; charset=utf-8" : "application/octet-stream" }); res.end(b); } });
}).listen(0);
const port = srv.address().port;
const external = [];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1040, height: 1000 }, userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" });   // (headless reports HeadlessChrome)
const page = await ctx.newPage();
page.on("request", (r) => { const u = new URL(r.url()); if (u.hostname !== "localhost" && !r.url().startsWith("blob:") && !r.url().startsWith("data:")) external.push(r.url()); });
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));
const replies = Object.fromEntries(py.requests.map((r) => [JSON.stringify(r.parsed), r.reply]));
await page.addInitScript({ content: `window.__FAKE = ${JSON.stringify({ hs: py.hs, upgrade: py.upgrade, step1: py.step1, write: py.write, replies, product: py.product })};` });
await page.addInitScript({ path: new URL("./fake_midi.js", import.meta.url).pathname });
await page.goto(`http://localhost:${port}/`);
const fast = () => page.evaluate(() => { for (const k of Object.keys(FM1.DELAY)) FM1.DELAY[k] = 0.002; FM1.DELAY.poll = 0.05; FM1.DELAY.hs = 0.3; FM1.DELAY.idle_check = FM1.DELAY.idle_write = 10; FM1.DELAY.wait_loader = FM1.DELAY.wait_reboot = 10; });
await fast();
const txt = (id) => page.locator("#" + id).innerText();

check("loads, no page errors", errors.length === 0, errors.join(" | "));
check("package self-check shown ok", (await txt("pkgcheck")).includes("header, file list and file CRCs ok") && (await txt("pkgid")) === py.product, await txt("pkgid"));
check("SHA-256 shown == Python's", (await txt("pkgsha")) === py.rawSha256);
check("Install is disabled at the start (checklist, no unit)", await page.locator("#btninstall").isDisabled());

// dry run: no MIDI access at all
await page.click("#btndry");
const sum = await txt("drysum");
check("dry run builds every frame and reports the same stream hash", sum.includes(`${py.sweepCount} reply frames`) && sum.includes(py.sweepSha256), `${py.sweepCount} frames`);
check("dry run requested no MIDI access and sent nothing", await page.evaluate(() => __FAKE.log.requestMIDIAccess === 0 && __FAKE.log.sends.length === 0));
check("dry run lists one line per frame", (await page.locator("#frames").innerText()).split("\n").length === py.sweepCount);

// find, checklist, confirm
await page.click("#btnfind");
await page.waitForFunction(() => document.getElementById("devbox").textContent.includes("Found"));
check("asks for MIDI with SysEx", await page.evaluate(() => __FAKE.log.requestMIDIAccess === 1 && __FAKE.log.sysex === true));
check("finds the unit, reads its identity (stock 015)", (await txt("devbox")).includes("FM-1_015"));
check("Install still disabled with the checklist unticked", await page.locator("#btninstall").isDisabled());
for (const c of await page.locator(".pre").all()) await c.check();
check("Install enabled once the checklist is ticked and the unit found", await page.locator("#btninstall").isEnabled());
await page.click("#btninstall");
check("confirm step shown; no UPGRADE byte sent yet", await page.locator("#confirm").isVisible() && await page.evaluate(() => __FAKE.log.upgrades === 0));
if (shot) await page.screenshot({ path: shot, fullPage: true });
await page.click("#btncancel");
check("cancel sends nothing", await page.evaluate(() => __FAKE.log.upgrades === 0));

// full install
await page.click("#btninstall"); await page.click("#btngo");
await page.waitForSelector("#done:not(.hide)", { timeout: 90000 });
const r1 = await page.evaluate(() => ({ ...__FAKE.log, sends: __FAKE.log.sends.length }));
check("full install: done, unit reports the package identity", (await txt("done")).includes(py.product));
check("every reply the page sent matched the reference frame", r1.badReplies === 0, `${r1.served} replies served`);
check("exactly two UPGRADE commands (step 1, step 2)", r1.upgrades === 2);
check("no external request, no page error", external.length === 0 && errors.length === 0, external.join(" "));

// cut off in step 2, failure text, resume
await page.evaluate(() => { __FAKE.log.served = 0; __FAKE.cfg.unplugAfter = __FAKE.step1.length + 300; __FAKE.boot("FM-1_015", "FM-1"); });
await page.click("#btnfind"); await page.waitForFunction(() => document.getElementById("devbox").textContent.includes("FM-1_015"));
await page.click("#btninstall"); await page.click("#btngo");
await page.waitForSelector("#fail:not(.hide)", { timeout: 90000 });
const failText = await txt("fail");
check("cut off: failure state says unplug, power-cycle, re-run, M-Flasher", /Unplug the USB cable, power-cycle the FM-1, and run this page again/.test(failText) && /M-Flasher/.test(failText), failText.slice(0, 90));
await page.evaluate(() => __FAKE.boot("ota-FM-1_900", "Felucca Update"));   // replugged: the unit comes back in update mode
await page.click("#btnfind"); await page.waitForFunction(() => document.getElementById("devbox").textContent.includes("update mode"));
check("after the replug the page offers Resume", (await txt("btninstall")).startsWith("Resume"));
await page.click("#btninstall"); await page.click("#btngo");
await page.waitForSelector("#done:not(.hide)", { timeout: 90000 });
check("resume finishes the install", (await txt("done")).includes(py.product) && await page.evaluate(() => __FAKE.log.badReplies === 0));
await browser.close(); srv.close();
console.log(`\n${n - bad}/${n} checks passed` + (bad ? `, ${bad} FAILED` : ""));
process.exit(bad ? 1 : 0);
