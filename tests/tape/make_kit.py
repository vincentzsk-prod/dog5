#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The TAPE listening kit: listen/tape/ from the host renders (run tests/tape/render.sh first).

  python3 tests/tape/make_kit.py [build/tape] [listen/tape]

WAVs (16-bit stereo 44.1 kHz, as the FM-1 sends it over USB) from just before the first note, the splash cut; the
pictures; the loudness tables printed for the README. CHEW 0 is a bit-exact bypass, so the 0 % files are the GROWL kit's
own (listen/drive/*_growl000.wav), and GROWL alone at 25 / 50 / 100 % is listen/drive/*_growl025/050/100.wav."""
import os
import sys
import wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze  # noqa: E402

FS = analyze.FS
T0 = 2.65


def write(dst, a):
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(np.clip(np.round(a), -32767, 32767).astype(np.int16).tobytes())


def trim(src, dst, start=T0, end=None):
    with wave.open(src) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    a = a[int(start * FS):int(end * FS) if end else None]
    write(dst, a.astype(np.float64))


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "build/tape"
    out = sys.argv[2] if len(sys.argv) > 2 else "listen/tape"
    os.makedirs(out, exist_ok=True)
    for src in analyze.SOURCES:
        for v in analyze.LEVELS[1:]:
            trim(f"{d}/src_{src}_{v:03d}.wav", f"{out}/{src}_chew{v:03d}.wav")
        for g, c in analyze.COMBOS:
            trim(f"{d}/combo_{src}_g{g:03d}c{c:03d}.wav", f"{out}/{src}_growl{g:03d}_chew{c:03d}.wav")
    for sw in ("sweep_chord", "sweep_lead", "toggle_chord"):
        trim(f"{d}/{sw}.wav", f"{out}/{sw}.wav")
    # the hiss alone (the chord at CHEW 100 minus the same with HISS 0), as it is and 30 dB up to hear its colour
    a = analyze.D.read(f"{d}/src_chord_100.wav") - analyze.D.read(f"{d}/nohiss_chord_100.wav")
    a = a[int(T0 * FS):] * 32768
    write(f"{out}/hiss_only_chew100.wav", a)
    write(f"{out}/hiss_only_chew100_plus30dB.wav", a * 10 ** 1.5)
    # the wobble on a plain 1 kHz sine (TAPE alone, the bench): both, wow only, flutter only (6 s each)
    for nm, dst in (("bench_wow_127", "sine1k_chew100.wav"), ("bench_wow_127_wf0", "sine1k_chew100_wow_only.wav"),
                    ("bench_wow_127_wf127", "sine1k_chew100_flutter_only.wav")):
        x = analyze.raw(f"{d}/{nm}.raw")[2 * FS:8 * FS]
        write(f"{out}/{dst}", x * 0.5)          # (-12 dBFS: a bare sine at -6 is loud)
    analyze.plots(d, out)
    print("kit ->", out)


if __name__ == "__main__":
    main()
