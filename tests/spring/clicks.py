#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""DRAIN's clicks: SIZE, DAMP and PRE-DLY jumped (end to end, at once) while the spring rings, on the bench
(tests/spring/spring_bench.c). Two cases: a 440 Hz sine still playing into it (a PRE-DLY jump moves the read under a
live input) and a tail ringing on its own after a burst. The source is a pure 440 Hz sine (its burst with 2 ms
raised-cosine edges), so a linear reverb's wet holds nothing above 2.5 kHz but the sway's sidebands around 440 Hz; a
click is broadband: the wet's energy above 2.5 kHz in 2.9 ms frames, against the median of the 120 ms around it; a
frame 6 dB over and above -80 dBFS is a click candidate (tests/tape's rule; a 9 kHz band missed the plate's
pre-delay jumps, which its 5 kHz input low-pass rounds). The old plate (OLD bench, the build before the re-voice)
with the same jumps is the control: it stepped its decay and jumped its pre-delay read. Its clicks ring on in its tail,
so they barely stand out from their own 120 ms; the second measure catches that: at each jump, the loudest 2.9 ms
above 2.5 kHz in the 300 ms after it against the median of the 300 ms before (the jump's "rise"; fails over 6 dB
when that loudest frame is above -80 dBFS: under it, a "rise" is the last bits flickering).
  python3 tests/spring/clicks.py BENCH [OLD_BENCH]"""
import subprocess, sys, os, numpy as np
FS = 44100
JUMPS = ["1000:pre=127", "1500:pre=0", "2000:pre=64", "2500:size=0", "3000:size=127", "3500:damp=127", "4000:damp=0",
         "4500:size=10", "4500:damp=100", "4500:pre=127", "5000:size=127", "5000:damp=0", "5000:pre=0"]
CASES = {"live sine": ["sine:440:8000", "0:mix=127", "0:size=100", "0:damp=30", "0:pre=0"],
         "tail alone": ["burst:440:16000:850", "0:mix=127", "0:size=127", "0:damp=30", "0:pre=0"]}

def hf_frames(w):
    X = np.fft.rfft(w)
    X[: int(2500 * len(w) / FS)] = 0
    h = np.fft.irfft(X, len(w))
    n = len(h) // 128
    return 10 * np.log10((h[: n * 128].reshape(n, 128) ** 2).mean(1) + 1e-12) - 20 * np.log10(32767)

def clicks(w, t0=0.95, t1=5.6):
    e = hf_frames(w)
    k = int(0.12 * FS / 128) // 2
    out = []
    for i in range(int(t0 * FS / 128), min(len(e) - k, int(t1 * FS / 128))):
        med = np.median(e[i - k: i + k])
        if e[i] > med + 6 and e[i] > -80:
            out.append((i * 128 / FS, e[i] - med, e[i]))
    return out

def rises(w):
    e = hf_frames(w)
    out = []
    for t in sorted({int(j.split(":")[0]) for j in JUMPS}):
        i = int(t / 1000 * FS / 128); k = int(0.3 * FS / 128)
        out.append((t / 1000, float(e[i: i + k].max() - np.median(e[i - k: i])), float(e[i: i + k].max())))
    return out

def run(bench, sig_args, path):
    subprocess.run([bench, path, sig_args[0], "6"] + sig_args[1:] + JUMPS, check=True)
    x = np.fromfile(path, dtype=np.int32).reshape(-1, 4).astype(float)
    return (x[:, 2] - x[:, 0] + x[:, 3] - x[:, 1]) / 2

if __name__ == "__main__":
    benches = sys.argv[1:]
    TMP = os.path.join(os.path.dirname(os.path.abspath(benches[0])), "clicks_tmp.raw")
    bad = 0
    for name, args in CASES.items():
        for b in benches:
            w = run(b, args, TMP)
            c, r = clicks(w), rises(w)
            tag = "spring" if b == benches[0] else "old plate"
            print(f"{name:10s} {tag:9s}: {len(c):3d} click candidates" + (": " + ", ".join(f"{t:.3f}s +{d:.0f}dB ({a:.0f}dBFS)" for t, d, a in c[:4]) if c else ""))
            print(f"{'':10s} {'':9s}  rise at each jump (dB, to dBFS): " + "  ".join(f"{t:.1f}s {d:+.0f}/{a:.0f}" for t, d, a in r))
            if b == benches[0] and (c or any(d > 6 and a > -80 for _, d, a in r)): bad = 1
    print("clicks: none in the spring" if not bad else "clicks: FOUND in the spring")
    sys.exit(bad)
