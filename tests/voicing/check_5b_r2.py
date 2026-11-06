# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B round 2: the committed slots equal 20 D, 24 C (round 1 results) and 23 D2 (round 2): resolved bytes, and the audio of the program-load path against the variant path (from the boot patch / both from INIT first).
  python3 tests/voicing/check_5b_r2.py"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch05b as X
from lib5b import *

exe = K.build_host()
for slot, key, path in ((20, "D", "20-fire-ice"), (24, "C", "24-fugue-state"), (23, "D2", "23-crypt-dust/round2")):
    res = json.load(open(os.path.join(X.OUT, path, "results.json")))[key]["params"]
    print(f"{slot:02d} {key}: resolved bytes identical: {B.resolve(K.ROOT, slot) == res}")
    for label, extra in (("from the boot patch", ()), ("both from INIT first", ("2000 midi 0xC0 32 0",))):
        out = []
        for ph in X.SPECS[slot]["phrases"][:4]:
            x = K.render(exe, ph, program=slot - 1, extra=extra, tag="c1")[0]; y = K.render(exe, ph, params=res, extra=extra, tag="c2")[0]
            out.append(f"{ph} " + ("bit-identical" if (x == y).all() else f"differs {10 * np.log10(max(((x - y) ** 2).mean(), 1e-9) / (x ** 2).mean()):.1f} dB"))
        print(f"   {label}: " + "; ".join(out))
