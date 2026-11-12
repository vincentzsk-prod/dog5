/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments (the protocol: tools/fm1_install.py)
 *
 * The FM-1 install protocol, ported from tools/fm1_install.py (function by function, same names in camelCase) for
 * the DØG-5 installer page. No DOM here: the page (index.template.html) and the Node test (tests/install/) use this
 * same file. Nothing in it is invented: every constant, frame layout, delay and rule is the Python reference's, and
 * tests/install/ asserts the two produce the same bytes.
 *
 * The FM-1 asks, we answer: the device sends SysEx read requests on the package's "logical image" (the package without
 * its marker bytes) and we reply with that data; the host never pushes. Step 1 (the running firmware reads the package,
 * stages the update loader), step 2 (the loader reads it all and writes the app area), then the unit restarts.
 * This file never touches flash: it serves bytes from the package and nothing else. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.FM1 = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // ---- constants (fm1_install.py lines 33-55)
  const HS_QUERY = Uint8Array.of(0xF0, 0x00, 0x32, 0x45, 0x00, 0x00, 0x00, 0x40, 0x7F, 0xF7);
  const UPGRADE = Uint8Array.of(0xF0, 0x22, 0x24, 0x35, 0x7F, 0xF7);
  const FINISH_CHECK = 0xE0000000, FINISH_WRITE = 0xF0000000;
  const MAXDATA = 512;
  const BLOCKS = 20, BLK = 0x30, KEEP = 0x2F, MAX_BLOCKS = 64;
  const LOADER_MARK = "FELUCCA-LOADER-1";
  // the ports the installer may probe: never other gear (fm1_install.py PORT_RE)
  const PORT_RE = /fm-1|smk|elite|mke-p37|starry|felucca|sloop|clipper|melodee|fomni|x0x|makkuro|maku|rainbow|snoop|vector|vox|ota|composite|sinco|usb-midi/i;
  const OWN_LOADER_RE = /^ota-(FM-1|SMK-37 Pro|SMK-37 Elite|MKE-P37)_9\d\d$/i;
  // seconds (fm1_install.py DELAY); the tests shorten them
  const DELAY = { open: 0.3, start: 2.0, reply: 0.01, loader: 3.0, reboot: 3.0, retry: 1.0, poll: 1.0, hs: 1.0,
                  idle_check: 8.0, idle_write: 180.0, wait_loader: 30.0, wait_reboot: 40.0 };
  const EXIT = { usage: 2, badpkg: 2, notfound: 3, model: 6, lost: 4, stopped: 4, badreq: 4, noloader: 5, noreturn: 5,
                 mismatch: 6, foreign: 6 };

  class InstallError extends Error {
    constructor(code, msg) { super(msg); this.code = code; this.exit = EXIT[code] || 1; }
  }

  // ---- wire format
  function pack7(data) {
    const out = []; let acc = 0, nb = 0;
    for (const b of data) {
      acc |= b << nb; nb += 8;
      while (nb >= 7) { out.push(acc & 0x7F); acc >>>= 7; nb -= 7; }
    }
    if (nb) out.push(acc & 0x7F);
    return Uint8Array.from(out);
  }
  function unpack7(s) {
    const out = []; let acc = 0, nb = 0;
    for (const b of s) {
      acc |= (b & 0x7F) << nb; nb += 7;
      while (nb >= 8) { out.push(acc & 0xFF); acc >>>= 8; nb -= 8; }
    }
    return Uint8Array.from(out);
  }
  function concat(...parts) {
    let n = 0; for (const p of parts) n += p.length;
    const o = new Uint8Array(n); let k = 0;
    for (const p of parts) { o.set(p, k); k += p.length; }
    return o;
  }
  function sumBytes(a, from, to) { let s = 0; for (let i = from; i < to; i++) s += a[i]; return s; }

  /* the reply to a read request: F0 pack7(00 59 30 len24 fl addr32 len24 data chk) F7 (fm1_install.py response) */
  function response(addr, data, fl = 0) {
    const n = data.length;
    const body = new Uint8Array(14 + n + 1);
    body.set([0x00, 0x59, 0x30, (n + 8) & 0xFF, ((n + 8) >> 8) & 0xFF, 0, fl]);
    body[7] = addr & 0xFF; body[8] = (addr >>> 8) & 0xFF; body[9] = (addr >>> 16) & 0xFF; body[10] = (addr >>> 24) & 0xFF;
    body[11] = n & 0xFF; body[12] = (n >> 8) & 0xFF; body[13] = 0;
    body.set(data, 14);
    body[14 + n] = ~sumBytes(body, 6, 14 + n) & 0xFF;
    return concat(Uint8Array.of(0xF0), pack7(body), Uint8Array.of(0xF7));
  }
  /* -> {fl, addr, len} or null (fm1_install.py parse_request) */
  function parseRequest(pkt) {
    if (pkt.length < 2 || pkt[0] !== 0xF0 || pkt[pkt.length - 1] !== 0xF7) return null;
    const u = unpack7(pkt.subarray(1, pkt.length - 1));
    if (u.length !== 15 || u[0] !== 0x00 || u[1] !== 0x59 || u[2] !== 0x30 || (~sumBytes(u, 6, 14) & 0xFF) !== u[14]) return null;
    return { fl: u[6], addr: (u[7] | u[8] << 8 | u[9] << 16 | u[10] << 24) >>> 0, len: u[11] | u[12] << 8 | u[13] << 16 };
  }
  /* -> {text, model, version, loader} or null (fm1_install.py parse_identity) */
  function parseIdentity(pkt) {
    if (pkt.length < 2 || pkt[0] !== 0xF0 || pkt[pkt.length - 1] !== 0xF7) return null;
    const d = unpack7(pkt.subarray(1, pkt.length - 1));
    if (d.length !== 34 || d[0] !== 0x00 || d[1] !== 0x59 || d[2] !== 0x11) return null;
    let txt = "";
    for (let i = 6; i < 33 && d[i] !== 0; i++) txt += String.fromCharCode(d[i]);
    const m = /^([^_]+)_(\d+)$/.exec(txt);
    return m ? { text: txt, model: m[1], version: parseInt(m[2], 10), loader: m[1].toLowerCase().startsWith("ota-") } : null;
  }

  // ---- CRC and ciphers (fm1_install.py _crc16, _dec)
  function crc16(data, crc = 0) {      // CRC-16/XMODEM, as the package and the device use
    for (let k = 0; k < data.length; k++) {
      crc ^= data[k] << 8;
      for (let i = 0; i < 8; i++) crc = (crc & 0x8000) ? ((crc << 1) ^ 0x1021) & 0xFFFF : (crc << 1) & 0xFFFF;
    }
    return crc;
  }
  function dec(b) {                    // JieLi ENC stream cipher (its own inverse)
    const out = Uint8Array.from(b); let key = 0xFFFF;
    for (let i = 0; i < out.length; i++) {
      out[i] ^= key & 0xFF;
      key = ((key << 1) ^ ((key & 0x8000) ? 0x1021 : 0)) & 0xFFFF;
    }
    return out;
  }
  const rd16 = (a, o) => a[o] | a[o + 1] << 8;
  const rd32 = (a, o) => (a[o] | a[o + 1] << 8 | a[o + 2] << 16 | a[o + 3] << 24) >>> 0;

  /* what is wrong with the update image (header, file list, each file's CRC), or null (fm1_install.py package_damage) */
  function packageDamage(image) {
    if (image.length < 0x40) return "too short";
    const hdr = dec(image.subarray(0, 0x40));
    if (crc16(hdr.subarray(2, 0x40)) !== rd16(hdr, 0)) return "header CRC";
    const count = rd16(hdr, 8);
    if (!(count >= 1 && count <= 8) || image.length < 0x40 + 0x50 * count) return "file list";
    const lst = image.subarray(0x40, 0x40 + 0x50 * count);
    if (crc16(lst) !== rd16(hdr, 2)) return "file list CRC";
    for (let i = 0; i < count; i++) {
      const e = dec(lst.subarray(i * 0x50, (i + 1) * 0x50));
      const dcrc = rd16(e, 4), off = rd32(e, 8), size = rd32(e, 12);
      let name = ""; for (let k = 0x40; k < 0x50 && e[k] !== 0; k++) name += String.fromCharCode(e[k]);
      if (off + size > image.length) return name + ": cut short";
      const typ = rd16(e, 0);
      // flash.bin (0) and ota.bin (100), what the device installs, carry the CRC of their bytes as served; the
      // stock packer's other entries are checked for their bounds only (as in the reference)
      if ((typ === 0 || typ === 100) && crc16(image.subarray(off, off + size)) !== dcrc) return name + ": CRC";
    }
    return null;
  }

  // ---- the package (.fwsc): 20 interleave blocks of 0x2F bytes + 1 marker byte (the identity), then the rest
  const idChar = (m, i) => { const c = (m - i - 1) & 0xFF; return c >= 0x20 && c < 0x7F; };
  function identityBlocks(raw) {
    const marker = (k) => ((k + 1) * BLK <= raw.length ? raw[k * BLK + KEEP] : null);
    let n = BLOCKS, m;
    while (n < MAX_BLOCKS && (m = marker(n)) !== null && m !== 0x7D && idChar(m, n)) n++;
    return (n > BLOCKS && marker(n) === 0x7D) ? n : BLOCKS;
  }
  function blockCount(raw) {
    let n = identityBlocks(raw);
    while (n < MAX_BLOCKS && (n + 1) * BLK <= raw.length && raw[n * BLK + KEEP] === 0x7D) n++;
    return n;
  }
  function logicalImage(raw, blocks = BLOCKS) {   // the image the device reads: the package without the marker bytes
    const parts = [];
    for (let i = 0; i < blocks; i++) parts.push(raw.subarray(i * BLK, i * BLK + KEEP));
    parts.push(raw.subarray(blocks * BLK));
    return concat(...parts);
  }
  function deinterleave(raw) {                    // -> {image, blocks}
    const n = blockCount(raw);
    const image = logicalImage(raw, n);
    if (n !== BLOCKS && packageDamage(image)) {
      const alt = logicalImage(raw, BLOCKS);
      if (!packageDamage(alt)) return { image: alt, blocks: BLOCKS };
    }
    return { image, blocks: n };
  }
  function productOf(raw) {                       // the package identity, e.g. "FM-1_960"
    if (raw.length < BLOCKS * BLK) throw new InstallError("badpkg", "not an FM-1 package (too short)");
    const ib = identityBlocks(raw);
    const n = ib === BLOCKS ? BLOCKS : Math.min(ib, deinterleave(raw).blocks);
    let s = "";
    for (let i = 0; i < n; i++) { const m = raw[i * BLK + KEEP]; if (m !== 0x7D) s += String.fromCharCode((m - i - 1) & 0xFF); }
    return s;
  }
  function hasBytes(raw, text) {                  // `text in raw` (fm1_install.py: LOADER_MARK not in raw)
    const t = Array.from(text, (c) => c.charCodeAt(0));
    outer: for (let i = 0; i + t.length <= raw.length; i++) {
      if (raw[i] !== t[0]) continue;
      for (let j = 1; j < t.length; j++) if (raw[i + j] !== t[j]) continue outer;
      return true;
    }
    return false;
  }
  /* -> {product, image, blocks}: fm1_install.py load_package, from bytes. Throws InstallError("badpkg"). */
  function loadPackage(raw, force = false) {
    const product = productOf(raw);
    if (!/^[^_]+_\d+$/.test(product)) throw new InstallError("badpkg", `not an FM-1 package (identity ${JSON.stringify(product)})`);
    if (!force && !hasBytes(raw, LOADER_MARK))
      throw new InstallError("badpkg", "no Felucca update loader in this package; only Felucca-family packages are installed");
    const { image, blocks } = deinterleave(raw);
    const bad = packageDamage(image);
    if (bad) throw new InstallError("badpkg", `damaged package (${bad}); nothing was written. Download it again.`);
    return { product, image, blocks };
  }
  const modelOf = (text) => text.split("_")[0].replace(/^ota-/i, "");
  const SMK_FAMILY = /^(SMK-37[ +].*|MKE-P37|STARRYKEY-37.*)$/i;
  function sameKeyboard(a, b) {                   // the models of two identities are the same hardware
    const ma = modelOf(a), mb = modelOf(b);
    return ma === mb || (SMK_FAMILY.test(ma) && SMK_FAMILY.test(mb));
  }

  // ---- SHA-256 (the page shows it; no crypto.subtle needed, so a downloaded copy works too)
  const K256 = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be,
    0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
    0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85,
    0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f,
    0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
  function sha256(data) {                         // -> lowercase hex
    const h = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
    const n = data.length, total = ((n + 9 + 63) >> 6) << 6;
    const buf = new Uint8Array(total); buf.set(data); buf[n] = 0x80;
    const dv = new DataView(buf.buffer);
    dv.setUint32(total - 8, Math.floor(n / 0x20000000)); dv.setUint32(total - 4, (n << 3) >>> 0);
    const w = new Uint32Array(64);
    const rotr = (x, k) => (x >>> k) | (x << (32 - k));
    for (let off = 0; off < total; off += 64) {
      for (let i = 0; i < 16; i++) w[i] = dv.getUint32(off + i * 4);
      for (let i = 16; i < 64; i++) {
        const s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >>> 3);
        const s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
      }
      let [a, b, c, d, e, f, g, hh] = h;
      for (let i = 0; i < 64; i++) {
        const S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25), ch = (e & f) ^ (~e & g);
        const t1 = (hh + S1 + ch + K256[i] + w[i]) >>> 0;
        const S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22), maj = (a & b) ^ (a & c) ^ (b & c);
        const t2 = (S0 + maj) >>> 0;
        hh = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
      }
      h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
    }
    return Array.from(h, (x) => x.toString(16).padStart(8, "0")).join("");
  }
  const toHex = (a) => Array.from(a, (b) => b.toString(16).padStart(2, "0")).join("");
  const fromHex = (s) => Uint8Array.from(s.match(/../g) || [], (x) => parseInt(x, 16));
  function fromBase64(b64) {
    if (typeof atob === "function") { const s = atob(b64); const o = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) o[i] = s.charCodeAt(i); return o; }
    return new Uint8Array(Buffer.from(b64, "base64"));
  }

  // ---- the frames the host sends, for the dry run and the tests
  /* The reply the host sends to one request (what Updater.serve sends): the finish asks get "success\0", anything
   * else is image[addr .. addr+len] with the request's flags. Throws InstallError("badreq") outside the package. */
  function replyFor(image, req) {
    if (req.addr === FINISH_CHECK || req.addr === FINISH_WRITE) return response(req.addr, Uint8Array.from("success\0", (c) => c.charCodeAt(0)));
    if (req.len > MAXDATA || req.addr + req.len > image.length)
      throw new InstallError("badreq", `the device asked for 0x${req.addr.toString(16)}+${req.len}, outside the package`);
    return response(req.addr, image.subarray(req.addr, req.addr + req.len), req.fl);
  }
  /* Every reply for a straight read of the whole image in MAXDATA chunks (what the dry run builds and shows), then the
   * two "success" replies. -> array of Uint8Array */
  function sweepFrames(image) {
    const frames = [];
    for (let a = 0; a < image.length; a += MAXDATA) frames.push(replyFor(image, { fl: 0, addr: a, len: Math.min(MAXDATA, image.length - a) }));
    frames.push(replyFor(image, { fl: 0, addr: FINISH_CHECK, len: 8 }), replyFor(image, { fl: 0, addr: FINISH_WRITE, len: 8 }));
    return frames;
  }
  function dryRun(raw) {
    const pkg = loadPackage(raw);
    const frames = sweepFrames(pkg.image);
    const all = concat(...frames);
    return { product: pkg.product, imageBytes: pkg.image.length, packageBytes: raw.length, blocks: pkg.blocks,
             frames: frames.length, streamBytes: all.length, streamSha256: sha256(all), packageSha256: sha256(raw),
             imageSha256: sha256(pkg.image), handshake: HS_QUERY, upgrade: UPGRADE, framesList: frames };
  }

  // ---- the updater (fm1_install.py Updater), async. The MIDI side is a "backend" (see tests/install and the page):
  //   backend.inputNames() / outputNames() -> arrays of names
  //   backend.open(inName, outName) -> Promise<link>; link.send(bytes) -> bool, link.read(ms) -> Promise<bytes|null>,
  //   link.drain(), link.lost (bool), link.close()
  let sleepFn = (ms) => new Promise((r) => setTimeout(r, ms));
  const sleep = (sec) => sleepFn(sec * 1000);
  const now = () => (typeof performance !== "undefined" ? performance.now() : Date.now()) / 1000;
  function pairOutput(name, outs) {
    if (outs.includes(name)) return name;
    const base = name.replace(/\s+\d+$/, "");
    const same = outs.filter((o) => o.replace(/\s+\d+$/, "") === base);
    if (same.length === 1) return same[0];
    return outs.length === 1 ? outs[0] : null;
  }
  async function handshake(link, tries = 3) {
    link.drain();
    for (let t = 0; t < tries; t++) {
      if (!link.send(HS_QUERY)) return null;
      const end = now() + DELAY.hs;
      let left;
      while ((left = end - now()) > 0) {
        const p = await link.read(left * 1000);
        if (p === null) break;
        const id = parseIdentity(p);
        if (id) return id;
      }
    }
    return null;
  }

  class Updater {
    constructor(backend, opts = {}) { this.backend = backend; this.port = opts.port || null; this.log = opts.log || (() => {}); this.onFrame = opts.onFrame || null; }
    candidates(onlyPort) {
      const names = this.backend.inputNames();
      if (this.port) {
        const mine = names.filter((n) => n.toLowerCase().includes(this.port.toLowerCase()));
        if (onlyPort) return mine;
        return mine.concat(names.filter((n) => !mine.includes(n) && PORT_RE.test(n)));
      }
      return names.filter((n) => PORT_RE.test(n));
    }
    async find(want = null, onlyPort = true) {   // the first matching port that answers the handshake (and want(identity))
      const outs = this.backend.outputNames();
      for (const name of this.candidates(onlyPort)) {
        const out = pairOutput(name, outs);
        if (!out) continue;
        let link;
        try { link = await this.backend.open(name, out); } catch (e) { continue; }
        const id = await handshake(link, 2);
        if (id && (!want || want(id))) return { link, id, name };
        link.close();
      }
      return null;
    }
    async waitFor(want, secs) {
      const end = now() + secs;
      while (now() < end) {
        const dev = await this.find(want, false);
        if (dev) return dev;
        await sleep(DELAY.retry);
      }
      return null;
    }
    /* answer read requests until the device asks for `finish`; -> {served, finished, lost} */
    async serve(link, image, finish, idle, progress) {
      let served = 0, last = now();
      for (;;) {
        const pkt = await link.read(DELAY.poll * 1000);
        if (pkt === null) {
          if (link.lost) return { served, finished: false, lost: true };
          if (now() - last > idle) return { served, finished: false, lost: false };
          continue;
        }
        const r = parseRequest(pkt);
        if (!r) continue;
        last = now();
        if (r.addr === FINISH_CHECK || r.addr === FINISH_WRITE) {
          const ack = replyFor(image, r);
          link.send(ack);
          if (this.onFrame) this.onFrame(r, ack);
          if (r.addr === finish) return { served, finished: true, lost: false };
          continue;
        }
        const frame = replyFor(image, r);      // throws "badreq" outside the package
        await sleep(DELAY.reply);
        if (!link.send(frame)) return { served, finished: false, lost: true };
        if (this.onFrame) this.onFrame(r, frame);
        served++;
        progress(served, r.addr + r.len);
      }
    }
    async check(dev, image, step) {              // step 1: the running firmware checks the package and starts the loader
      step("start", dev.id.text);
      dev.link.send(UPGRADE);
      await sleep(DELAY.start);
      const res = await this.serve(dev.link, image, FINISH_CHECK, DELAY.idle_check, (k) => step("check", k));
      dev.link.close();
      if (!res.finished)
        throw new InstallError(res.lost ? "lost" : "stopped",
          `the FM-1 ${res.lost ? "was disconnected" : "stopped answering"} after ${res.served} requests; nothing was written`);
      step("loader");
      await sleep(DELAY.loader);
      const ota = await this.waitFor((i) => i.loader, DELAY.wait_loader);
      if (!ota) throw new InstallError("noloader", "the update loader did not appear. Replug the USB cable and run the install again: the FM-1 stays in update mode until it is done");
      return ota;
    }
    async write(ota, image, step) {              // step 2: the loader reads and writes the whole package, then restarts
      step("write", 0);
      ota.link.send(UPGRADE);
      await sleep(DELAY.start);
      const res = await this.serve(ota.link, image, FINISH_WRITE, DELAY.idle_write,
        (k, end) => step("write", Math.min(99, Math.floor(end * 100 / image.length))));
      ota.link.close();
      if (!res.finished)
        throw new InstallError(res.lost ? "lost" : "stopped",
          `the loader ${res.lost ? "was disconnected" : "stopped answering"} after ${res.served} requests. Replug the USB cable and run the install again to finish`);
      step("write", 100);
    }
    async verify(product, step) {
      step("reboot");
      await sleep(DELAY.reboot);
      const back = await this.waitFor((i) => !i.loader, DELAY.wait_reboot);
      if (!back) throw new InstallError("noreturn", "the FM-1 did not come back: power-cycle it");
      back.link.close();
      if (back.id.text !== product) throw new InstallError("mismatch", `written, but the FM-1 reports ${back.id.text} (expected ${product})`);
      step("done", back.id.text);
      return back.id.text;
    }
    /* running firmware -> loader -> new firmware; dev from find(). A device already in update mode only needs the write. */
    async install(dev, image, product, step = () => {}) {
      if (!sameKeyboard(dev.id.text, product)) { dev.link.close(); throw new InstallError("model", `the device is ${dev.id.text}, the package is for ${product}`); }
      if (dev.id.loader && !OWN_LOADER_RE.test(dev.id.text)) {
        dev.link.close();                        // another firmware's loader: its image layout may differ
        throw new InstallError("foreign", `the FM-1 is in the update mode of another firmware (${dev.id.text}): finish that update with its own updater (M-UPGRADE), then install again`);
      }
      const ota = dev.id.loader ? dev : await this.check(dev, image, step);
      await this.write(ota, image, step);
      return this.verify(product, step);
    }
  }

  return {
    HS_QUERY, UPGRADE, FINISH_CHECK, FINISH_WRITE, MAXDATA, BLOCKS, BLK, KEEP, LOADER_MARK, PORT_RE, OWN_LOADER_RE, DELAY, EXIT,
    InstallError, Updater, pack7, unpack7, response, parseRequest, parseIdentity, crc16, dec, packageDamage, identityBlocks,
    blockCount, logicalImage, deinterleave, productOf, loadPackage, sameKeyboard, modelOf, sha256, toHex, fromHex, fromBase64,
    replyFor, sweepFrames, dryRun, handshake, pairOutput, concat,
    setSleep(fn) { sleepFn = fn; },
  };
});
