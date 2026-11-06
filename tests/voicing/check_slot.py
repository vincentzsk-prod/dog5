#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Prove the committed slot equals its approved/recommended variant: the tree's slot N resolved by the firmware's own tables against the
variant's parameter list (byte for byte), and the audio of the program-load path against the variant path on the audition phrases (bit-exact where the
cutoff approaches from the same side, README section 8; the difference in dB otherwise).

  python3 tests/voicing/check_slot.py SLOT KEY      (variant KEY of Batch 2A; add 'round2' as a third argument for round 2, '3a' for Batch 3A, '3b' for Batch 3B, '4a' for Batch 4A, '4b' for Batch 4B ('4b-r2': 13 round 2) or '3b-r2' for 05 ZEAROX round 2, from listen/voicing/batch-0Xx/<dir>/results.json)"""
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
    b3b = len(sys.argv) > 3 and sys.argv[3] == "3b"       # Batch 3B: variants from listen/voicing/batch-03b/<dir>/results.json
    if b3:
        from batch03a_variants import PATCHES as P3
        spec = [p for p in P3 if p["slot"] == slot][0]
    if b3b:
        from batch03b_variants import PATCHES as P3B
        spec = [p for p in P3B if p["slot"] == slot][0]
    b4a = len(sys.argv) > 3 and sys.argv[3] == "4a"        # Batch 4A: variants from listen/voicing/batch-04a/<dir>/results.json (the keys are the variants)
    if b4a:
        from batch04a_variants import PATCHES as P4
        spec = [p for p in P4 if p["slot"] == slot][0]
    b4b = len(sys.argv) > 3 and sys.argv[3] == "4b"        # Batch 4B: variants from listen/voicing/batch-04b/<dir>/results.json
    if b4b:
        from batch04b_variants import PATCHES as P4B
        spec = [p for p in P4B if p["slot"] == slot][0]
    b4br2 = len(sys.argv) > 3 and sys.argv[3] == "4b-r2"   # Batch 4B round 2 (13 only): variants from listen/voicing/batch-04b/13-round2/results.json
    if b4br2:
        spec = {"slot": 13, "phrases": ["b_stabs", "t_ghost"]}
    r3 = len(sys.argv) > 3 and sys.argv[3] == "3b-r2"     # 05 ZEAROX round 2: variants from listen/voicing/batch-03b/round2/05-zearox/results.json
    if r3:
        spec = {"slot": 5, "phrases": ["a_riff", "b_stabs", "c_held", "m_kick"]}
    if r2:
        from batch02a_round2 import PATCHES_R2
        spec = [p for p in PATCHES_R2 if p["slot"] == slot][0]
    if b4br2:
        res = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-04b", "13-round2", "results.json")))[key]["params"]
    elif b4a or b4b:
        res = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-04b" if b4b else "batch-04a", spec["dir"], "results.json")))[key]["params"]
    elif r3:
        res = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-03b", "round2", "05-zearox", "results.json")))["variants"][key]["params"]
    else:
      res = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-03b" if b3b else "batch-03a" if b3 else "batch-02a", "round2" if r2 else "", spec["dir"], "results.json")))["variants"][key]["params"]
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
