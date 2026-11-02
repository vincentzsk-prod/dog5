#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The GROWL listening kit: listen/drive/ from the host renders (run tests/drive/render.sh first).

  python3 tests/drive/make_kit.py [build/drive] [listen/drive]

WAVs (16-bit stereo 44.1 kHz, as the FM-1 sends it over USB) from just before the first note, the splash cut; the
spectrum and aliasing plots; the loudness table printed for the README."""
import os
import sys
import wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze  # noqa: E402

FS = analyze.FS
T0 = 2.65


def trim(src, dst, start=T0, end=None):
    with wave.open(src) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    a = a[int(start * FS):int(end * FS) if end else None]
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(a.tobytes())
    return len(a) / FS


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "build/drive"
    out = sys.argv[2] if len(sys.argv) > 2 else "listen/drive"
    os.makedirs(out, exist_ok=True)
    rows = []
    for src in analyze.SOURCES:
        lu = []
        for v in analyze.LEVELS:
            secs = trim(f"{d}/src_{src}_{v:03d}.wav", f"{out}/{src}_growl{v:03d}.wav")
            lu.append(analyze.lufs(analyze.read(f"{out}/{src}_growl{v:03d}.wav")))
        rows.append((src, lu, secs))
    for sw in ("sweep_chord", "sweep_lead"):
        trim(f"{d}/{sw}.wav", f"{out}/{sw}.wav")
    analyze.plots(d, out)
    print("| source | " + " | ".join(f"GROWL {v} %" for v in analyze.LEVELS) + " |")
    print("|---|" + "---:|" * len(analyze.LEVELS))
    for src, lu, secs in rows:
        print(f"| {src} | " + " | ".join(f"{x:.1f} LUFS ({x - lu[0]:+.1f})" for x in lu) + " |")


if __name__ == "__main__":
    main()
