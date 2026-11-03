#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The DRAIN listening kit: listen/spring/ from the host renders (run tests/spring/render.sh first).

  python3 tests/spring/make_kit.py [build/spring/kit] [listen/spring]

WAVs (16-bit stereo 44.1 kHz, as the FM-1 sends it over USB) from just before the first note, the splash cut, and
the pictures (tests/spring/analyze.py draws them)."""
import os
import subprocess
import sys
import wave
import numpy as np

FS = 44100
T0 = 2.55
HERE = os.path.dirname(os.path.abspath(__file__))


def trim(src, dst, start=T0):
    with wave.open(src) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(a[int(start * FS):].tobytes())


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "build/spring/kit"
    out = sys.argv[2] if len(sys.argv) > 2 else "listen/spring"
    os.makedirs(out, exist_ok=True)
    for src in ("stab", "bass", "lead", "pluck", "hit"):
        for s in ("dry", "boing", "default", "splash", "dark"):
            trim(f"{d}/src_{src}_{s}.wav", f"{out}/{src}_{s}.wav")
        trim(f"{d}/old_{src}_default.wav", f"{out}/{src}_default_OLD_PLATE.wav")
    for src in ("stab", "pluck", "hit"):
        trim(f"{d}/src_{src}_max.wav", f"{out}/{src}_max.wav")
    for src in ("stab", "pluck"):
        trim(f"{d}/old_{src}_splash.wav", f"{out}/{src}_splash_OLD_PLATE.wav")
    for src in ("stab", "bass", "lead", "pluck"):
        for nm in ("mild", "surf", "mangle"):
            trim(f"{d}/chain_{src}_{nm}.wav", f"{out}/chain_{src}_{nm}.wav")
        trim(f"{d}/chain_{src}_surf_nodrain.wav", f"{out}/chain_{src}_surf_no_drain.wav")
        trim(f"{d}/oldchain_{src}_mangle.wav", f"{out}/chain_{src}_mangle_OLD_PLATE.wav")
    trim(f"{d}/chain_stab_mangle_nodrain.wav", f"{out}/chain_stab_mangle_no_drain.wav")
    trim(f"{d}/oldchain_pluck_surf.wav", f"{out}/chain_pluck_surf_OLD_PLATE.wav")
    for nm in ("sweep_size", "sweep_damp", "sweep_pre", "jumps_hit"):
        trim(f"{d}/{nm}.wav", f"{out}/{nm}.wav")
    # the overflow: the plate before the fix (c10db7d), the plate with it (db0701c), DRAIN; from 3.5 s (the crack ~3.97)
    trim(f"{d}/hot_reverb_prefix.wav", f"{out}/overflow_plate_BEFORE_FIX.wav", 3.5)
    trim(f"{d}/hot_reverb_fixed.wav", f"{out}/overflow_plate_fixed.wav", 3.5)
    trim(f"{d}/hot_reverb.wav", f"{out}/overflow_case_on_drain.wav", 3.5)
    subprocess.run([sys.executable, os.path.join(HERE, "analyze.py"), d, "--png", out], check=True,
                   stdout=open(os.path.join(out, "numbers.txt"), "w"))
    print("kit ->", out)


if __name__ == "__main__":
    main()
