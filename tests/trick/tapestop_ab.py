#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""TAPE STOP, A/B: the approved render (the per-voice dive, 3 Nov) against the current build's, on the same scripts.

  python3 tests/trick/tapestop_ab.py APPROVED_DIR NEW_DIR

Each dir holds tapestop_note.wav and tapestop_chord.wav, full length (from 0 ms, as the host writes them; the kit's
files are cut at 2.55 s). Prints, from each press:
  - the pitch of the single saw (note: SEQ held 3.3 .. 4.8 s);
  - on the chord's full hold (5.5 .. 7.1 s): the level (rms dB) and the brightness (spectral centroid, Hz) every 100 ms;
  - the clicks: the largest sample step and second difference at the press and the release, against the music's own
    (the second before the press)."""
import sys
import wave
import numpy as np

FS = 44100


def load(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64)


def f0(x, t, n=1024):
    s = x[int(t * FS):int(t * FS) + n]
    s = s - s.mean()
    z = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
    if len(z) < 3 or np.abs(s).max() < 200:
        return 0.0
    fr = z + (-s[z]) / (s[z + 1] - s[z])
    return FS * (len(fr) - 1) / (fr[-1] - fr[0])


def frame(x, t, n=2048):
    s = x[int(t * FS):int(t * FS) + n]
    rms = np.sqrt((s ** 2).mean())
    sp = np.abs(np.fft.rfft(s * np.hanning(len(s))))
    fr = np.fft.rfftfreq(len(s), 1 / FS)
    cen = (sp * fr).sum() / max(sp.sum(), 1e-9)
    return 20 * np.log10(max(rms, 1e-3) / 32768), cen


def clicks(x, t, w=0.03):
    a = x[int(t * FS):int((t + w) * FS)]
    return np.abs(np.diff(a)).max(), np.abs(np.diff(a, 2)).max()


def main():
    A, B = sys.argv[1], sys.argv[2]
    na, nb = load(A + "/tapestop_note.wav").mean(1), load(B + "/tapestop_note.wav").mean(1)
    print("note, C5 saw: pitch (semitones) from the press      approved   new")
    for ms in (0, 100, 200, 300, 400, 500, 600, 700, 800, 900):
        fa, fb = f0(na, 3.3 + ms / 1000), f0(nb, 3.3 + ms / 1000)
        st = lambda f: f"{12 * np.log2(f / 523.25):+7.1f}" if f else "  (silent)"
        print(f"  {ms:4d} ms {st(fa):>36} {st(fb):>10}")
    ca, cb = load(A + "/tapestop_chord.wav"), load(B + "/tapestop_chord.wav")
    print("chord, the full hold (5.5 s), from the press:  level dB (approved / new)   centroid Hz (approved / new)")
    for ms in range(-200, 1700, 100):
        la, ea = frame(ca.mean(1), 5.5 + ms / 1000)
        lb, eb = frame(cb.mean(1), 5.5 + ms / 1000)
        print(f"  {ms:5d} ms   {la:6.1f} / {lb:6.1f}            {ea:6.0f} / {eb:6.0f}")
    for lab, x in (("approved", ca), ("new", cb)):
        m = x[:, 0]
        play = clicks(m, 4.5, 1.0)
        out = [play] + [clicks(m, t) for t in (3.995, 4.345, 5.495, 7.095)]
        print(f"  {lab:9s} clicks (largest step, largest 2nd diff): playing {out[0][0]:.0f}, {out[0][1]:.0f} | "
              f"dab press {out[1][0]:.0f}, {out[1][1]:.0f} | dab release {out[2][0]:.0f}, {out[2][1]:.0f} | "
              f"hold press {out[3][0]:.0f}, {out[3][1]:.0f} | hold release {out[4][0]:.0f}, {out[4][1]:.0f}")


if __name__ == "__main__":
    main()
