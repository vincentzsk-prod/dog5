#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The SLOP ride at three depths, to choose by ear: 1x (0..127 added to VINTAGE), 1.5x, 2x (chosen
by ear on 3 Nov: shipped).

  python3 tests/trick/slop_depths.py [build/trick/depths] [listen/trick/slop_depths]

Builds the host app three times (-DSLOP_SCALE_X2=2/3/4; the firmware ships 4), renders the kit's slop_note and
slop_chord scripts (tests/trick/make_kit.py, unchanged) and logs each sounding voice card's vintage pitch from inside
the engine ("T vlog"), at ride 0 (3.0-5.7 s) and over the full-ride hold (9.8-13.7 s): its mean (the static flat /
sharp the card's VINTAGE offset gives) and the wander around it (sd, range). The held note's pitch is also read off
the audio as a cross-check. Writes the WAVs and README.md into the output folder."""
import os
import re
import subprocess
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_kit as K                            # the same sources, the same cut, the same pitch reader

DEPTHS = (("1x", 2), ("1.5x", 3), ("2x", 4))
WIN = {"ride 0": (3000, 5700), "full ride": (9800, 13700)}


def main():
    bd = os.path.join(K.ROOT, sys.argv[1] if len(sys.argv) > 1 else "build/trick/depths")
    out = os.path.join(K.ROOT, sys.argv[2] if len(sys.argv) > 2 else "listen/trick/slop_depths")
    os.makedirs(bd, exist_ok=True); os.makedirs(out, exist_ok=True)
    rows = []
    for label, x2 in DEPTHS:
        exe = os.path.join(bd, f"obervave_{x2}")
        subprocess.run(["cc", "-O2", "-Wall", "-Wno-unused-function", "-DOBV_HOST", f"-DSLOP_SCALE_X2={x2}",
                        '-DAPP_VER="dev"', "-Ifirmware/src", "-Ifirmware/gen", "-o", exe, "firmware/src/obervave.c"],
                       cwd=K.ROOT, check=True)
        for src in ("slop_note", "slop_chord"):
            lines = list(K.SCRIPTS[src])
            for w, (t0, t1) in WIN.items():
                lines += [f"{t0} vlog 1", f"{t1} vlog 0"]
            sp = os.path.join(bd, f"{src}_{x2}.txt")
            with open(sp, "w") as f:
                f.write("\n".join(sorted(lines, key=lambda l: int(l.split()[0]))) + "\n")
            r = subprocess.run([exe, os.path.join(bd, f"{src}_{x2}"), sp], cwd=K.ROOT, check=True,
                               capture_output=True, text=True).stdout
            for p in os.listdir(bd):
                if p.endswith(".ppm"):
                    os.unlink(os.path.join(bd, p))
            logs = re.findall(r"vlog card (\d+): mean ([-+\d.]+) cents  sd ([\d.]+)  range ([-+\d.]+) \.\. ([-+\d.]+)", r)
            n = len(logs) // 2                  # (the ride-0 window's cards first, then the full ride's)
            for wi, w in enumerate(WIN):
                for c, m, sd, lo, hi in logs[wi * n:(wi + 1) * n]:
                    rows.append((label, src, w, int(c), float(m), float(sd), float(lo), float(hi)))
            a = K.load(os.path.join(bd, f"{src}_{x2}.wav"))
            K.write(os.path.join(out, f"{src}_{label}.wav"), a[int(K.T0 * K.FS):])
            if src == "slop_note":
                x = a.mean(1)
                cs = np.array([1200 * np.log2(K.f0_zc(x, t) / 440) for t in np.arange(9.8, 13.6, 0.02)])
                c0 = np.array([1200 * np.log2(K.f0_zc(x, t) / 440) for t in np.arange(3.0, 5.6, 0.02)])
                rows.append((label, src, "audio", -1, cs.mean() - c0.mean(), cs.std(), cs.min() - c0.mean(),
                             cs.max() - c0.mean()))

    L = ["| depth | source | window | voice card | mean (cents) | wander sd | range |", "|---|---|---|---|---|---|---|"]
    for d, s, w, c, m, sd, lo, hi in rows:
        L.append(f"| {d} | {s.replace('slop_', '')} | {w} | {'audio*' if c < 0 else c} | {m:+.1f} | {sd:.1f} | "
                 f"{lo:+.1f} .. {hi:+.1f} |")
    summ = ["| depth | VINTAGE at full ride (patch 30 + ride) | note: card 0 mean | chord: per-card means | chord: "
            "average of the cards | wander sd (note / chord average) |", "|---|---|---|---|---|---|"]
    for label, x2 in DEPTHS:
        note = [r for r in rows if r[0] == label and r[1] == "slop_note" and r[2] == "full ride"]
        ch = [r for r in rows if r[0] == label and r[1] == "slop_chord" and r[2] == "full ride"]
        summ.append(f"| {label} | {30 + 127 * x2 // 2} | {note[0][4]:+.1f} | "
                    + " / ".join(f"{r[4]:+.1f}" for r in ch) + f" | {np.mean([r[4] for r in ch]):+.1f} | "
                    f"{note[0][5]:.1f} / {np.mean([r[5] for r in ch]):.1f} |")
    print("\n".join(summ)); print(); print("\n".join(L))
    with open(os.path.join(out, "numbers.md"), "w") as f:
        f.write("\n".join(summ) + "\n\n" + "\n".join(L) + "\n")


if __name__ == "__main__":
    main()
