#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The Python reference side of the installer page's test (tests/install/run.sh).

  py_side.py PACKAGE.fwsc STEP1.txt WRITE.txt OUT.json

Runs tools/fm1_install.py (the reference) on the package: its frame builder on every request the real device code
sends (STEP1 / WRITE: tests/install/trace_requests.c output) plus edge cases, its package reading, its identity parser,
and whole install sessions (its Updater against a fake FM-1 that asks exactly those requests), recording every byte
the host sends. js_side.mjs does the same with the page's JavaScript and asserts the results are identical."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import fm1_install as I  # noqa: E402

for k in I.DELAY:                                   # no waiting in the test
    I.DELAY[k] = 0.0005
I.DELAY["poll"] = 0.02
I.DELAY["idle_check"] = I.DELAY["idle_write"] = 5.0
I.DELAY["wait_loader"] = I.DELAY["wait_reboot"] = 5.0
I.DELAY["hs"] = 0.2


def request_frame(fl, addr, n):                     # as ota.c ota_send_msg(0x30, ...) builds it
    u = bytearray([0, 0x59, 0x30, 8, 0, 0, fl]) + addr.to_bytes(4, "little") + bytes([n & 0xFF, n >> 8, 0])
    u.append(~sum(u[6:14]) & 0xFF)
    return b"\xF0" + I.pack7(bytes(u)) + b"\xF7"


def identity_frame(text):                           # as ota.c ota_send_msg(0x11, id[27]) builds it
    body = text.encode("latin-1").ljust(27, b"\0")
    u = bytearray([0, 0x59, 0x11, 27, 0, 0]) + body
    u.append(~sum(body) & 0xFF)
    return b"\xF0" + I.pack7(bytes(u)) + b"\xF7"


def read_sched(path):
    return [tuple(int(x) for x in ln.split()) for ln in Path(path).read_text().splitlines() if ln.strip()]


class FakeLink:
    def __init__(self, dev, gen):
        self.dev, self.gen, self.q, self.closed = dev, gen, [], False
        self.name = dev.name

    @property
    def lost(self):
        return not self.dev.connected or self.gen != self.dev.gen

    def send(self, pkt):
        if self.lost:
            return False
        self.dev.transcript.append(bytes(pkt).hex())
        self.dev.rx(bytes(pkt), self)
        return True

    def read(self, timeout):
        return self.q.pop(0) if self.q else None

    def drain(self):
        self.q.clear()

    def close(self):
        self.closed = True


class FakeDevice:
    """an FM-1 backend (the interface fm1_install.Updater wants) that asks for exactly the real schedules"""

    def __init__(self, image, product, step1, write, identity="FM-1_015", name="FM-1", unplug_after=None, bad_addr=None,
                 loader=("ota-FM-1_900", "Felucca Update")):
        self.image, self.product, self.step1, self.write = image, product, step1, write
        self.loader, self.unplug_after, self.bad_addr = loader, unplug_after, bad_addr
        self.served, self.transcript, self.gen = 0, [], 0
        self.boot(identity, name)

    def boot(self, identity, name):
        self.gen += 1
        self.identity, self.name, self.connected, self.waiting, self.queue, self.link = identity, name, True, None, [], None

    def input_names(self):
        return [self.name] if self.connected else []

    output_names = input_names

    def open(self, in_name, out_name):
        if in_name != self.name or not self.connected:
            raise IOError("no such port")
        return FakeLink(self, self.gen)

    def tx(self, link, pkt):
        link.q.append(bytes(pkt))

    def rx(self, d, link):
        if d == I.HS_QUERY:
            self.tx(link, identity_frame(self.identity))
        elif d == I.UPGRADE:
            sched = self.write if self.identity.startswith("ota-") else self.step1
            if self.bad_addr is not None and self.identity.startswith("ota-"):
                sched = [(0, self.bad_addr, 512)] + sched
            self.queue = list(sched)
            self.link = link
            self.ask()
        elif self.waiting:
            fl, addr, n = self.waiting
            want = I.response(addr, b"success\0") if addr >= I.FINISH_CHECK else I.response(addr, self.image[addr:addr + n], fl)
            assert d == want, f"reply to {self.waiting} differs from the reference frame"
            self.waiting = None
            self.served += 1
            if self.unplug_after and self.served >= self.unplug_after:
                self.connected = False
                return
            if addr == I.FINISH_CHECK:
                self.boot(*self.loader)
            elif addr == I.FINISH_WRITE:
                self.boot(self.product, "Felucca")
            else:
                self.ask()

    def ask(self):
        if self.queue:
            self.waiting = self.queue.pop(0)
            self.tx(self.link, request_frame(*self.waiting))


def attempt(dev, image, product, steps):
    up = I.Updater(dev)
    try:
        d = up.find()
        assert d, "no device"
        up.install(d, image, product, lambda *a: steps.append(a[0]))
        return "ok"
    except I.InstallError as e:
        return f"{e.code}: {e}"


def session(label, image, product, step1, write, replug=False, **kw):
    """one install; replug: after a failure the unit is replugged (it comes back in update mode) and the install is run again"""
    dev = FakeDevice(image, product, step1, write, **kw)
    steps = []
    res = {"name": label, "result": attempt(dev, image, product, steps)}
    if replug and res["result"] != "ok":
        dev.unplug_after = None
        dev.boot(*dev.loader)
        steps.append("replug")
        res["result"] += " | resume: " + attempt(dev, image, product, steps)
    res.update(transcript=dev.transcript, steps=steps, served=dev.served)
    return res


def main():
    pkg, s1, wr, out = sys.argv[1:5]
    raw = Path(pkg).read_bytes()
    product, image = I.load_package(pkg, False)
    step1, write = read_sched(s1), read_sched(wr)
    edge = [(0, 0, 1), (7, 0x1000, 511), (0x7F, 0x2000, 512), (0xFF, 0, 512), (0, len(image) - 5, 5), (0, len(image) - 512, 512),
            (1, 0x10, 0), (0, 0x123456 % len(image), 100), (0, I.FINISH_CHECK, 8), (0, I.FINISH_WRITE, 8)]
    reqs = []
    for fl, addr, n in step1 + write + edge:
        rf = request_frame(fl, addr, n)
        want = I.response(addr, b"success\0") if addr in (I.FINISH_CHECK, I.FINISH_WRITE) else I.response(addr, image[addr:addr + n], fl)
        reqs.append({"req": rf.hex(), "parsed": list(I.parse_request(rf)), "reply": want.hex()})
    sweep = [I.response(a, image[a:a + 512]) for a in range(0, len(image), 512)] + [I.response(I.FINISH_CHECK, b"success\0"), I.response(I.FINISH_WRITE, b"success\0")]
    idents = {t: (lambda i: [i.text, i.model, i.version, i.loader] if i else None)(I.parse_identity(identity_frame(t)))
              for t in ("FM-1_015", "ota-FM-1_900", product, "SMK-37 Pro_016", "garbage")}
    idents["bad-length"] = None
    sessions = [
        session("install from stock 015 (step 1 + loader + write + verify)", image, product, step1, write),
        session("resume: unit already in update mode", image, product, step1, write, identity="ota-FM-1_900", name="Felucca Update"),
        session("cut off after 400 reads in step 2, then resume", image, product, step1, write, replug=True, unplug_after=len(step1) + 400),
        session("SMK-37 is refused for this FM-1 package", image, product, step1, write, identity="SMK-37 Pro_016", name="SMK-37"),
        session("another firmware's loader is refused", image, product, step1, write, identity="ota-FM-1_015", name="FM-1 Update"),
        session("a read outside the package is refused", image, product, step1, write, identity="ota-FM-1_900", name="Felucca Update", bad_addr=len(image) + 512),
    ]
    json.dump({"product": product, "rawSha256": hashlib.sha256(raw).hexdigest(), "imageSha256": hashlib.sha256(image).hexdigest(),
               "imageLen": len(image), "blocks": I.deinterleave(raw)[1], "hs": I.HS_QUERY.hex(), "upgrade": I.UPGRADE.hex(),
               "requests": reqs, "sweepCount": len(sweep), "sweepSha256": hashlib.sha256(b"".join(sweep)).hexdigest(),
               "idents": idents, "sessions": sessions, "step1": step1, "write": write}, open(out, "w"))
    print(f"python: {len(reqs)} request/reply pairs, sweep {len(sweep)} frames, {len(sessions)} sessions")


if __name__ == "__main__":
    main()
