/* SPDX-License-Identifier: GPL-3.0-only */
/* A fake WebMIDI (navigator.requestMIDIAccess) with one fake FM-1 on it, injected into the installer page by
 * tests/install/page_e2e.mjs BEFORE the page's own scripts run. The device asks for the real request schedules
 * (window.__FAKE.step1 / .write, from tests/install/trace_requests.c) and checks every reply against the reference
 * frames from Python (window.__FAKE.replies): it does not use the page's code to judge it. */
(() => {
  const F = window.__FAKE;
  F.log = { requestMIDIAccess: 0, sysex: null, sends: [], badReplies: 0, served: 0, upgrades: 0 };
  F.cfg = F.cfg || { identity: "FM-1_015", name: "FM-1", unplugAfter: null };
  const hex = (u) => Array.from(u, (b) => b.toString(16).padStart(2, "0")).join("");
  const unhex = (s) => Uint8Array.from(s.match(/../g) || [], (x) => parseInt(x, 16));
  function pack7(d) { const o = []; let acc = 0, nb = 0; for (const b of d) { acc |= b << nb; nb += 8; while (nb >= 7) { o.push(acc & 127); acc >>>= 7; nb -= 7; } } if (nb) o.push(acc & 127); return o; }
  const sum = (a) => a.reduce((x, y) => x + y, 0);
  function reqFrame(fl, addr, len) { const u = [0, 0x59, 0x30, 8, 0, 0, fl, addr & 255, (addr >>> 8) & 255, (addr >>> 16) & 255, (addr >>> 24) & 255, len & 255, len >> 8, 0]; u.push(~sum(u.slice(6)) & 255); return Uint8Array.from([0xF0, ...pack7(u), 0xF7]); }
  function idFrame(t) { const body = Array.from({ length: 27 }, (_, i) => (i < t.length ? t.charCodeAt(i) : 0)); const u = [0, 0x59, 0x11, 27, 0, 0, ...body, ~sum(body) & 255]; return Uint8Array.from([0xF0, ...pack7(u), 0xF7]); }

  const access = { inputs: new Map(), outputs: new Map(), onstatechange: null };
  const dev = { gen: 0, identity: null, name: null, waiting: null, queue: [], served: 0, inp: null, out: null };
  function boot(identity, name) {
    dev.gen++; dev.identity = identity; dev.name = name; dev.waiting = null; dev.queue = [];
    const gen = dev.gen;
    const mk = (kind) => ({ id: kind + gen, name, type: kind, state: "connected", gen, onmidimessage: null, async open() { return this; } });
    dev.inp = mk("input"); dev.out = mk("output");
    dev.out.send = (d) => { if (dev.out !== this_out(gen)) throw new Error("InvalidStateError: port disconnected"); F.log.sends.push(hex(d)); setTimeout(() => rx(hex(d)), 0); };
    access.inputs = new Map([[dev.inp.id, dev.inp]]); access.outputs = new Map([[dev.out.id, dev.out]]);
    if (access.onstatechange) setTimeout(() => access.onstatechange({}), 0);
  }
  const this_out = (gen) => (dev.gen === gen ? dev.out : null);
  function disconnect() { dev.gen++; access.inputs = new Map(); access.outputs = new Map(); if (access.onstatechange) setTimeout(() => access.onstatechange({}), 0); }
  function tx(u) { setTimeout(() => dev.inp && dev.inp.onmidimessage && dev.inp.onmidimessage({ data: u }), 0); }
  function ask() { if (dev.queue.length) { dev.waiting = dev.queue.shift(); tx(reqFrame(...dev.waiting)); } }
  function rx(h) {
    if (h === F.hs) tx(idFrame(dev.identity));
    else if (h === F.upgrade) {
      F.log.upgrades++;
      dev.queue = (dev.identity.startsWith("ota-") ? F.write : F.step1).map((r) => r.slice()); ask();
    } else if (dev.waiting) {
      const key = JSON.stringify(dev.waiting), want = F.replies[key];
      if (h !== want) F.log.badReplies++;
      const addr = dev.waiting[1]; dev.waiting = null; dev.served++; F.log.served++;
      if (F.cfg.unplugAfter && F.log.served >= F.cfg.unplugAfter) { F.cfg.unplugAfter = null; disconnect(); return; }
      if (addr === 0xE0000000) boot("ota-FM-1_900", "Felucca Update");
      else if (addr === 0xF0000000) boot(F.product, "Felucca");
      else ask();
    }
  }
  F.boot = boot; F.disconnect = disconnect;
  boot(F.cfg.identity, F.cfg.name);
  navigator.requestMIDIAccess = async (opts) => { F.log.requestMIDIAccess++; F.log.sysex = opts && opts.sysex; return access; };
})();
