#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Batch 11: crash character of 14 Reef Break before / after, in ABSOLUTE time from the note-on (the older decay figures count from each band's own
peak, which moved).  Dry voice (sends off), the low hit (A1, note-on 3000 ms, gate 300 ms) and the mid hit (A2, 6500 ms).  python3 batch11_bands.py MAIN_TREE"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K, batch01a as B, batch04a_metrics as Q, batch04b_metrics as Z

def run(exe, p, tag, on):
    R = Q.fx_set(exe, "u_crash", p, tag)
    ts_on = on
    fr, ts = Z.band_frames(R["dry"], on, on + 3000)
    out = {}
    for n, e in fr.items():
        k = int(np.argmax(e))
        pk = e[k]
        def first_after(d):
            b = np.nonzero(e[k:] <= pk - d)[0]
            return float(ts[k + b[0]]) if len(b) else None
        def first_before(d):                     # first frame within d dB of its peak (rise)
            b = np.nonzero(e >= pk - d)[0]
            return float(ts[b[0]])
        last = np.nonzero(e >= pk - 20)[0]
        out[n] = {"rise_to_-20dB_ms": first_before(20), "peak_ms": float(ts[k]), "last_within_20dB_ms": float(ts[last[-1]]),
                  "falls_20dB_ms": first_after(20), "falls_40dB_ms": first_after(40), "peak_dB": float(pk)}
    return out
exe = K.build_host()
res = {}
for name, tree in (("before", sys.argv[1]), ("after", K.ROOT)):
    p = B.resolve(os.path.abspath(tree), 14)
    res[name] = {"A1": run(exe, p, "b11" + name, 3000), "A2": run(exe, p, "b11m" + name, 6500)}
json.dump(res, open(os.path.join(K.BUILD, "batch11_bands.json"), "w"), indent=1)
for hit in ("A1", "A2"):
    print(hit)
    for n in res["before"][hit]:
        b, a = res["before"][hit][n], res["after"][hit][n]
        f = lambda d: f"{d['peak_ms']:6.0f} {d['last_within_20dB_ms']:6.0f} {str(None if d['falls_20dB_ms'] is None else round(d['falls_20dB_ms'])):>6} {str(None if d['falls_40dB_ms'] is None else round(d['falls_40dB_ms'])):>6}"
        print(f"{n:9s} before(pk last f20 f40) {f(b)} | after {f(a)}")
