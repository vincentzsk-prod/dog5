#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The ALLEY listening kit: listen/bbd/ from the host renders (run tests/bbd/render.sh first).

  python3 tests/bbd/make_kit.py [build/bbd] [listen/bbd]

WAVs (16-bit stereo 44.1 kHz, as the FM-1 sends it over USB) from just before the first note, the splash cut, and
the pictures (tests/bbd/analyze.py draws them)."""
import os
import subprocess
import sys
import wave
import numpy as np

FS = 44100
T0 = 2.55
HERE = os.path.dirname(os.path.abspath(__file__))


def write(dst, a):
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(np.clip(np.round(a), -32767, 32767).astype(np.int16).tobytes())


def trim(src, dst, start=T0):
    with wave.open(src) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    write(dst, a[int(start * FS):].astype(np.float64))


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "build/bbd"
    out = sys.argv[2] if len(sys.argv) > 2 else "listen/bbd"
    os.makedirs(out, exist_ok=True)
    for src in ("stab", "bass", "lead", "slap"):
        for s in ("dry", "dbl", "slap", "sync", "long", "runaway"):
            trim(f"{d}/src_{src}_{s}.wav", f"{out}/{src}_{s}.wav")
        trim(f"{d}/old_{src}_sync.wav", f"{out}/{src}_sync_OLD_DELAY.wav")
    for src in ("stab", "bass", "lead"):
        for nm in ("g050_sync", "sync_c050", "g050_sync_c050", "g100_runaway_c100"):
            trim(f"{d}/combo_{src}_{nm}.wav", f"{out}/{src}_{nm.replace('g050', 'growl50').replace('g100', 'growl100').replace('c050', 'chew50').replace('c100', 'chew100')}.wav")
        for nm in ("g050_sync_c050", "g100_runaway_c100"):
            trim(f"{d}/combo_{src}_{nm}_noalley.wav", f"{out}/{src}_{nm.replace('g050', 'growl50').replace('g100', 'growl100').replace('c050', 'chew50').replace('c100', 'chew100').replace('_sync', '').replace('_runaway', '')}_no_alley.wav")
    for nm in ("tap_bass", "sweep_lead", "sweep_runaway"):
        trim(f"{d}/{nm}.wav", f"{out}/{nm}.wav")
    # the time-change bench as audio: a 1 kHz sine's echo alone (FEEDBK 0), -12 dBFS: one step, a dive, a rise
    x = np.fromfile(f"{d}/tc.raw", np.int32).reshape(-1, 4).astype(float)
    e = x[:, 2:] - x[:, :2]
    write(f"{out}/sine1k_echo_time_changes.wav", np.stack([e[:, 0], e[:, 0]], 1)[FS:] * 0.5)
    subprocess.run([sys.executable, os.path.join(HERE, "analyze.py"), d, "--png", out], check=True,
                   stdout=subprocess.DEVNULL)
    print("kit ->", out)


if __name__ == "__main__":
    main()
