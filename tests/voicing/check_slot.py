#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Prove the committed slot equals its approved/recommended variant: the tree's slot N resolved by the firmware's own tables against the
variant's parameter list (byte for byte), and the audio of the program-load path against the variant path on the audition phrases (bit-exact where the
cutoff approaches from the same side, README section 8; the difference in dB otherwise).

  python3 tests/voicing/check_slot.py SLOT KEY      (variant KEY of Batch 2A; add 'round2' as a third argument for round 2, or '3a' for Batch 3A, from listen/voicing/batch-02a/<dir>/results.json)"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
from batch02a_variants import PATCHES


def main():
    slot, key = int(sys.argv[1]), sys.argv[2]
    spec = ([p for p in PATCHES if p["slot"] == slot] or [None])[0]
    r2 = len(sys.argv) > 3 and sys.argv[3] == "round2"
    b3 = len(sys.argv) > 3 and sys.argv[3] == "3a"         # Batch 3A: variants from listen/voicing/batch-03a/<dir>/results.json
    if b3:
        from batch03a_variants import PATCHES as P3
        spec = [p for p in P3 if p["slot"] == slot][0]
    if r2:
        from batch02a_round2 import PATCHES_R2
        spec = [p for p in PATCHES_R2 if p["slot"] == slot][0]
    res = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-03a" if b3 else "batch-02a", "round2" if r2 else "", spec["dir"], "results.json")))["variants"][key]["params"]
    cur = B.resolve(K.ROOT, slot)
    diff = {k: (cur[k], res[k]) for k in res if cur.get(k) != res[k]}
    print(f"slot {slot:02d}: resolved bytes vs variant {key}:", "IDENTICAL" if not diff else f"DIFFER {diff}")
    exe = K.build_host()
    # the slot is loaded from the boot patch (CUTOFF / RESO slew in from wherever it was: a floor of up to 63/256 st); the variant is built over INIT.  Both from INIT
    # first (program 33 at 2000 ms) remove that: then the two should match bit for bit
    for label, extra in (("from boot", ()), ("both from INIT", ("2000 midi 0xC0 32 0",))):
        out = []
        for ph in spec["phrases"]:
            a, _ = K.render(exe, ph, program=slot - 1, extra=extra, tag="chk_a")
            b, _ = K.render(exe, ph, params=res, extra=extra, tag="chk_b")
            same = bool((a == b).all())
            err = None if same else float(10 * np.log10(max(((a - b) ** 2).mean(), 1e-9) / (a ** 2).mean()))
            out.append(f"{ph} " + ("bit-identical" if same else f"differs {err:.1f} dB"))
        print(f"  audio, program-load path vs variant path, {label}: " + "; ".join(out))
    sys.exit(1 if diff else 0)


if __name__ == "__main__":
    main()
