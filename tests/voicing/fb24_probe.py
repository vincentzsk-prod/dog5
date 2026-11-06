# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B: how far is 24 D's FEEDBK from runaway?  D with FEEDBK stepped up, the 30 s held triad (phrase ad_longhold) and the 12 repeated chords (ae_repeat): peak per 4 s window, growth, clip count.
  python3 tests/voicing/fb24_probe.py   (prints the table; the numbers are in README section 19)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch05b as X
from lib5b import *

exe = K.build_host()
orig = B.resolve(X.BASE, 24)
res = __import__("json").load(open(os.path.join(X.OUT, "24-fugue-state", "results.json")))
pD = res["D"]["params"]
print("| FEEDBK | long hold peak per 4 s window 0..28 s (dBFS) | growth (24-28 s window minus the 4-8 s window) | clipped samples | repeated chords: peak of chord 1 / best later | growth |")
print("|---|---|---|---|---|---|")
for fb in (110, 114, 118, 122, 127):
    p = {**pD, "DLY_FB": fb}
    h = K.render(exe, "ad_longhold", params=p, tag="fbp")[0]
    e = K.render(exe, "ae_repeat", params=p, tag="fbp2")[0]
    pk = [M.peak_db(h, 3000 + s * 1000, 3000 + (s + 4) * 1000) for s in range(0, 28, 4)]
    g = pk[6] - pk[1]
    rep = [M.peak_db(e, 3000 + k * 1000, 3000 + (k + 1) * 1000) for k in range(12)]
    clip = int((np.abs(h) >= 32767).sum() + (np.abs(e) >= 32767).sum())
    print(f"| {fb} | " + " ".join(f"{v:.1f}" for v in pk) + f" | {g:+.1f} | {clip} | {rep[0]:.1f} / {max(rep[3:]):.1f} | {max(rep[3:]) - rep[0]:+.1f} |")
