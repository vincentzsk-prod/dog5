// SPDX-License-Identifier: GPL-3.0-only
// The page's side of the installer test (tests/install/run.sh): loads the JavaScript that SHIPS in docs/install/index.html
// (not web/install/fm1install.js: the text inside the page), and asserts it does exactly what tools/fm1_install.py does:
// package reading, request parsing, identity parsing, every reply frame byte for byte, the dry-run stream, and whole
// install sessions (the same fake FM-1 as py_side.py) with identical host->device transcripts and outcomes.
//   node js_side.mjs PY.json docs/install/index.html web/install/fm1install.js
import fs from "node:fs";
import vm from "node:vm";
import crypto from "node:crypto";

const [pyPath, pagePath, corePath] = process.argv.slice(2);
const py = JSON.parse(fs.readFileSync(pyPath, "utf8"));
const html = fs.readFileSync(pagePath, "utf8");
let bad = 0, n = 0;
const check = (what, ok, extra = "") => { n++; if (!ok) bad++; console.log(`${ok ? "ok  " : "FAIL"} ${what}${extra ? "  " + extra : ""}`); };
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
const hex = (u8) => Buffer.from(u8).toString("hex");

// ---- the script the page ships
const core = /<script id="core">\n([\s\S]*?)\n<\/script>/.exec(html)[1];
const b64 = /<script id="pkg" type="text\/plain">([\s\S]*?)<\/script>/.exec(html)[1].trim();
check("the page's core script is exactly web/install/fm1install.js", core === fs.readFileSync(corePath, "utf8").replace(/\n$/, "").replace(/^/, "") || core.trim() === fs.readFileSync(corePath, "utf8").trim());
const ctx = { module: { exports: {} }, performance, setTimeout, clearTimeout, Buffer };
vm.runInNewContext(core, ctx);
const FM1 = ctx.module.exports;

// ---- the package inside the page
const raw = Uint8Array.from(Buffer.from(b64, "base64"));
check("embedded package == the .fwsc beside the page", fs.readdirSync(pagePath.replace(/index\.html$/, "")).filter((f) => f.endsWith(".fwsc")).every((f) => hex(fs.readFileSync(pagePath.replace(/index\.html$/, "") + f)) === hex(raw)));
check("embedded package SHA-256 == Python's", sha(raw) === py.rawSha256 && FM1.sha256(raw) === py.rawSha256, py.rawSha256);
const pkg = FM1.loadPackage(raw);
check("package identity == Python's", pkg.product === py.product, pkg.product);
check("update image SHA-256 / length / blocks == Python's", FM1.sha256(pkg.image) === py.imageSha256 && pkg.image.length === py.imageLen && pkg.blocks === py.blocks, `${py.imageLen} B, ${py.blocks} blocks`);
check("FM1.sha256 == hashlib on odd lengths", [0, 1, 55, 56, 63, 64, 65, 1000].every((k) => { const d = crypto.randomBytes(k); return FM1.sha256(d) === sha(d); }));

// ---- frames
check("handshake query and upgrade command == Python's", hex(FM1.HS_QUERY) === py.hs && hex(FM1.UPGRADE) === py.upgrade);
let okReq = true, okRep = true;
for (const r of py.requests) {
  const p = FM1.parseRequest(Uint8Array.from(Buffer.from(r.req, "hex")));
  if (!p || !eq([p.fl, p.addr, p.len], r.parsed)) okReq = false;
  if (hex(FM1.replyFor(pkg.image, p)) !== r.reply) okRep = false;
}
check(`request parsing: ${py.requests.length} requests == Python's`, okReq);
check(`reply frames: ${py.requests.length} frames byte-identical to fm1_install.response`, okRep);
const sweep = FM1.sweepFrames(pkg.image);
const swh = sha(Buffer.concat(sweep.map((f) => Buffer.from(f))));
check(`dry-run sweep: ${sweep.length} frames, stream hash == Python's`, sweep.length === py.sweepCount && swh === py.sweepSha256, swh);
const dr = FM1.dryRun(raw);
check("FM1.dryRun() reports the same count and hash", dr.frames === py.sweepCount && dr.streamSha256 === py.sweepSha256 && dr.product === py.product);
const idOk = Object.entries(py.idents).every(([t, want]) => {
  if (t === "bad-length") return FM1.parseIdentity(Uint8Array.of(0xF0, 1, 2, 0xF7)) === null;
  const body = Buffer.alloc(27); body.write(t, "latin1");
  const u = Buffer.concat([Buffer.from([0, 0x59, 0x11, 27, 0, 0]), body, Buffer.from([~[...body].reduce((a, b) => a + b, 0) & 0xFF])]);
  const w = Uint8Array.from([0xF0, ...FM1.pack7(u), 0xF7]);
  const g = FM1.parseIdentity(w);
  return eq(g ? [g.text, g.model, g.version, g.loader] : null, want);
});
check("identity parsing == Python's (stock, loader, DØG-5, SMK, garbage)", idOk);
check("pack7 / unpack7 round trip", [0, 1, 7, 100, 513].every((k) => { const d = crypto.randomBytes(k); return hex(FM1.unpack7(FM1.pack7(d)).subarray(0, k)) === hex(d); }));
// the package self-check must reject damage
const dmg = Uint8Array.from(raw); dmg[0x3000] ^= 1;
let rejected = false; try { FM1.loadPackage(dmg); } catch (e) { rejected = e.code === "badpkg"; }
check("a damaged package is refused (one flipped bit)", rejected);

// ---- whole sessions against the same fake FM-1
for (const k of Object.keys(FM1.DELAY)) FM1.DELAY[k] = 0.0005;
FM1.DELAY.poll = 0.02; FM1.DELAY.idle_check = FM1.DELAY.idle_write = 5; FM1.DELAY.wait_loader = FM1.DELAY.wait_reboot = 5; FM1.DELAY.hs = 0.2;
FM1.setSleep(() => Promise.resolve());
const reqFrame = (fl, addr, len) => { const u = Buffer.alloc(15); u.set([0, 0x59, 0x30, 8, 0, 0, fl]); u.writeUInt32LE(addr, 7); u[11] = len & 255; u[12] = len >> 8; u[14] = ~[...u.subarray(6, 14)].reduce((a, b) => a + b, 0) & 255; return Uint8Array.from([0xF0, ...FM1.pack7(u), 0xF7]); };
const idFrame = (t) => { const body = Buffer.alloc(27); body.write(t, "latin1"); const u = Buffer.concat([Buffer.from([0, 0x59, 0x11, 27, 0, 0]), body, Buffer.from([~[...body].reduce((a, b) => a + b, 0) & 255])]); return Uint8Array.from([0xF0, ...FM1.pack7(u), 0xF7]); };
const replyOf = new Map(py.requests.map((r) => [JSON.stringify(r.parsed), r.reply]));

class FakeDevice {
  constructor(o) { Object.assign(this, { loader: ["ota-FM-1_900", "Felucca Update"], unplugAfter: null, badAddr: null, served: 0, transcript: [], gen: 0 }, o); this.boot(o.identity || "FM-1_015", o.name || "FM-1"); }
  boot(identity, name) { this.gen++; Object.assign(this, { identity, name, connected: true, waiting: null, queue: [], link: null }); }
  inputNames() { return this.connected ? [this.name] : []; }
  outputNames() { return this.inputNames(); }
  async open(inName) { if (inName !== this.name || !this.connected) throw new Error("no such port"); return new FakeLink(this, this.gen); }
  rx(d, link) {
    const h = hex(d);
    if (h === py.hs) link.q.push(idFrame(this.identity));
    else if (h === py.upgrade) {
      let sched = this.identity.startsWith("ota-") ? py.write : py.step1;
      if (this.badAddr !== null && this.identity.startsWith("ota-")) sched = [[0, this.badAddr, 512], ...sched];
      this.queue = sched.slice(); this.link = link; this.ask();
    } else if (this.waiting) {
      const [fl, addr, len] = this.waiting;
      const want = replyOf.get(JSON.stringify([fl, addr, len])) ?? hex(FM1.response(addr, pkg.image.subarray(addr, addr + len), fl));
      if (h !== want) throw new Error(`reply to ${this.waiting} differs from the reference frame`);
      this.waiting = null; this.served++;
      if (this.unplugAfter && this.served >= this.unplugAfter) { this.connected = false; return; }
      if (addr === FM1.FINISH_CHECK) this.boot(...this.loader);
      else if (addr === FM1.FINISH_WRITE) this.boot(py.product, "Felucca");
      else this.ask();
    }
  }
  ask() { if (this.queue.length) { this.waiting = this.queue.shift(); this.link.q.push(reqFrame(...this.waiting)); } }
}
class FakeLink {
  constructor(dev, gen) { this.dev = dev; this.gen = gen; this.q = []; }
  get lost() { return !this.dev.connected || this.gen !== this.dev.gen; }
  send(pkt) { if (this.lost) return false; this.dev.transcript.push(hex(pkt)); this.dev.rx(pkt, this); return true; }
  async read() { await Promise.resolve(); return this.q.length ? this.q.shift() : null; }
  drain() { this.q.length = 0; }
  close() {}
}
async function attempt(dev, steps) {
  const up = new FM1.Updater(dev);
  try { const d = await up.find(); if (!d) throw new Error("no device"); await up.install(d, pkg.image, pkg.product, (k) => steps.push(k)); return "ok"; }
  catch (e) { if (e instanceof FM1.InstallError) return `${e.code}: ${e.message}`; throw e; }
}
const scenarios = [
  ["install from stock 015 (step 1 + loader + write + verify)", {}],
  ["resume: unit already in update mode", { identity: "ota-FM-1_900", name: "Felucca Update" }],
  ["cut off after 400 reads in step 2, then resume", { replug: true, unplugAfter: py.step1.length + 400 }],
  ["SMK-37 is refused for this FM-1 package", { identity: "SMK-37 Pro_016", name: "SMK-37" }],
  ["another firmware's loader is refused", { identity: "ota-FM-1_015", name: "FM-1 Update" }],
  ["a read outside the package is refused", { identity: "ota-FM-1_900", name: "Felucca Update", badAddr: py.imageLen + 512 }],
];
for (const [label, o] of scenarios) {
  const want = py.sessions.find((s) => s.name === label);
  const dev = new FakeDevice(o); const steps = [];
  let result = await attempt(dev, steps);
  if (o.replug && result !== "ok") { dev.unplugAfter = null; dev.boot(...dev.loader); steps.push("replug"); result += " | resume: " + await attempt(dev, steps); }
  const same = result === want.result && eq(dev.transcript, want.transcript) && eq(steps, want.steps) && dev.served === want.served;
  check(`session "${label}": same outcome, same ${dev.transcript.length} host->device messages`, same, `${result.slice(0, 60)}  sha ${sha(Buffer.from(dev.transcript.join("\n"))).slice(0, 16)}`);
  if (!same) console.log("   JS :", result, "\n   PY :", want.result);
}
console.log(`\n${n - bad}/${n} checks passed` + (bad ? `, ${bad} FAILED` : ""));
process.exit(bad ? 1 : 0);
