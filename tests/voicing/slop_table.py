#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""What VINTAGE does, in cents, from the engine's own per-card log (the host-only `vlog`): a note held 13 s on the
INIT sound in DUAL (two cards), each card's static offset (mean), the s.d. and the range of its random walk, at several
VINTAGE values and with the SLOP ride (ALGORITHM, enc 1) at the top.  Reused by every voicing batch for "how much slop".

  python3 tests/voicing/slop_table.py            prints a markdown table"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K


def run(exe, vint, ride=False):
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0", f"{K.T_PARAMS} param {K.PARAM_IDS['VINTAGE']} {vint}",
             f"{K.T_PARAMS} param {K.PARAM_IDS['MODE']} 1", "3000 midi 0x90 45 100", "4000 vlog 1", "17000 vlog 0"]
    if ride:
        lines += [f"{4500 + i * 20} enc 1 2" for i in range(70)]            # the ride up to 127 well before the window
    lines += ["17100 midi 0x80 45 0", "18000 end"]
    lines.sort(key=lambda l: int(l.split()[0]) if " end" not in l else 10 ** 9)
    sp = os.path.join(K.BUILD, "slop.txt")
    open(sp, "w").write("\n".join(lines) + "\n")
    r = subprocess.run([exe, os.path.join(K.BUILD, "slop"), sp], cwd=K.ROOT, capture_output=True, text=True,
                       errors="replace").stdout
    return K.vlog_parse(r)


def main():
    exe = K.build_host()
    print("| VINTAGE | engine value (patch + ride) | static offset of the two cards (cents) | wander s.d. | wander range |")
    print("|---|---|---|---|---|")
    for vint, ride in ((30, 0), (55, 0), (90, 0), (100, 0), (127, 0), (90, 1), (127, 1)):
        v = run(exe, vint, bool(ride))
        c = sorted(v)
        print(f"| {vint}{' + ride 127' if ride else ''} | {vint + 254 * ride} | "
              + " / ".join(f"{v[k][0]:+.1f}" for k in c) + " | " + " / ".join(f"{v[k][1]:.1f}" for k in c) + " | "
              + " / ".join(f"{v[k][2]:+.0f}..{v[k][3]:+.0f}" for k in c) + " |")


if __name__ == "__main__":
    main()
