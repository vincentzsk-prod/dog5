#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The live tricks' listening kit: listen/trick/ from host renders (tests/host.c runs the firmware's own integer code).

  python3 tests/trick/make_kit.py [build/trick] [listen/trick]

Writes the scripts (build/trick/*.txt), renders them with a fresh host build, trims the splash, measures, and draws
listen/trick/tapestop.png and listen/trick/slop.png. Prints the numbers the README quotes.
FM-1 ids: BTN_SEQ 11, BTN_PLAY 12, ENC_ALGORITHM 1. Bytes: 4 O2 WAVE, 12 CUTOFF, 43 SPREAD, 54 GROWL, 56 FEEDBK,
58 DLY MIX, 59 SIZE, 62 DRAIN, 64 CHEW, 68 ALLEY."""
import os
import subprocess
import sys
import wave
import numpy as np
from PIL import Image, ImageDraw

FS = 44100
T0 = 2.55                                       # the cut: just before the first note (the splash takes 2.4 s)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def riff(t, bars, root=33):
    """Red Pill's 8th-note riff (the GROWL / CHEW / ALLEY kits' bass line), from t ms, 250 ms a step"""
    notes = [root, root, root + 12, root, root + 3, root, root - 2, root]
    ev = []
    for b in range(bars):
        for i, n in enumerate(notes):
            on = t + (b * 8 + i) * 250
            ev += [f"{on} midi 0x90 {n} 100", f"{on + 200} midi 0x80 {n} 0"]
    return ev


def chord(t_on, t_off, notes, vel=100):
    return [f"{t_on} midi 0x90 {n} {vel}" for n in notes] + [f"{t_off} midi 0x80 {n} 0" for n in notes]


def ride(t0, t1, frm, to):
    """ALGORITHM turned from ride frm to ride to (0..127) between t0 and t1, a detent every ~40 ms"""
    steps = abs(to - frm) // 2
    d = 1 if to > frm else -1
    return [f"{t0 + (t1 - t0) * i // max(steps, 1)} enc 1 {d}" for i in range(steps)]


PAD = ["2600 midi 0xC0 32 0", "2601 param 43 110", "2601 param 62 40", "2601 param 59 90", "2601 param 58 30",
       "2601 param 68 80", "2601 param 12 85"]
LEAD = ["2600 midi 0xC0 32 0", "2601 param 12 60", "2601 param 4 0"]   # one saw, filter half shut: the pitch reads clean
CHAIN = ["2600 midi 0xC0 0 0", "2601 param 54 127", "2601 param 56 124", "2601 param 58 70", "2601 param 68 100",
         "2601 param 62 60", "2601 param 59 110", "2601 param 64 127"]

SCRIPTS = {
    # STOP during a hard-driven full chain: GROWL 127, ALLEY near runaway, DRAIN, CHEW 127. Bar 2: STOP mid-note, 1.5 s
    # of silence, PLAY, the riff again (no tail comes back in); then the riff stops and the runaway builds, STOP in it,
    # PLAY: silence (cleared, not muted)
    "kill_fullchain": CHAIN + riff(2700, 1) + ["4800 midi 0x90 33 100", "4880 btn 12", "4950 midi 0x80 33 0",
                                               "6400 btn 12"] + riff(6450, 2) + ["11200 btn 12", "11900 btn 12",
                                                                                 "14000 end"],
    # the same without STOP: what the two STOPs cut off
    "kill_fullchain_REF": CHAIN + riff(2700, 1) + ["4800 midi 0x90 33 100", "4950 midi 0x80 33 0"] + riff(6450, 2)
                          + ["14000 end"],
    # TAPE STOP on a held pad chord (spread, a little ALLEY and DRAIN): a short dab (0.35 s: a sag, let go mid-dive),
    # then held 1.6 s to the full stop, let go: the chord again at once
    "tapestop_chord": PAD + chord(2700, 9000, [48, 55, 58, 63]) + ["4000 btndown 11", "4350 btnup 11",
                                                                    "5500 btndown 11", "7100 btnup 11", "10500 end"],
    # TAPE STOP on the bass riff, as an ending: held over the last two steps, let go, the riff goes on
    "tapestop_bass": ["2600 midi 0xC0 0 0"] + riff(2700, 2) + ["5900 btndown 11", "7000 btnup 11"] + riff(7000, 1)
                     + ["9800 end"],
    # one saw (for the pitch track): TAPE STOP held 1.5 s
    "tapestop_note": LEAD + chord(2700, 5800, [72]) + ["3300 btndown 11", "4800 btnup 11", "6300 end"],
    # the SLOP ride under a held note: 3 s plain (the patch's VINTAGE 30), up to +127 over 4 s, held 4 s, back over 2 s
    "slop_note": LEAD + chord(2700, 18500, [69]) + ride(5700, 9700, 0, 127) + ride(13700, 15700, 127, 0)
                 + ["19000 end"],
    "slop_chord": PAD + chord(2700, 18500, [48, 55, 58, 63]) + ride(5700, 9700, 0, 127) + ride(13700, 15700, 127, 0)
                  + ["19000 end"],
}


def load(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64)


def write(dst, a):
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(np.clip(np.round(a), -32767, 32767).astype(np.int16).tobytes())


def f0_zc(x, t, n=4096):
    """the pitch over n samples from t s, by interpolated rising zero crossings (one saw through a low-pass)"""
    s = x[int(t * FS):int(t * FS) + n]
    s = s - s.mean()
    z = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
    if len(z) < 3:
        return 0.0
    fr = z + (-s[z]) / (s[z + 1] - s[z])
    return FS * (len(fr) - 1) / (fr[-1] - fr[0])


def plot(path, title, series, ylabel, yr, xr):
    """a plain line chart: series = [(name, colour, [(x, y)])]"""
    W, H, L, R, T, B = 900, 380, 70, 20, 40, 50
    im = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(im)
    X = lambda v: L + (v - xr[0]) / (xr[1] - xr[0]) * (W - L - R)
    Y = lambda v: T + (yr[1] - v) / (yr[1] - yr[0]) * (H - T - B)
    d.text((L, 12), title, fill=(20, 20, 20))
    for i in range(6):
        yv = yr[0] + (yr[1] - yr[0]) * i / 5
        d.line([(L, Y(yv)), (W - R, Y(yv))], fill=(225, 225, 222))
        d.text((8, Y(yv) - 6), f"{yv:.0f}", fill=(90, 90, 90))
    for i in range(11):
        xv = xr[0] + (xr[1] - xr[0]) * i / 10
        d.text((X(xv) - 10, H - B + 8), f"{xv:.1f}", fill=(90, 90, 90))
    d.text((W // 2 - 20, H - 20), "seconds", fill=(90, 90, 90))
    d.text((8, T - 22), ylabel, fill=(90, 90, 90))
    for k, (name, col, pts) in enumerate(series):
        seg = []
        for a, b in pts + [(1e9, 0)]:           # (a gap in the track breaks the line: no ramp drawn across a silence)
            if seg and a - seg[-1][0] > 0.05:
                if len(seg) > 1:
                    d.line([(X(u), Y(v)) for u, v in seg], fill=col, width=2)
                seg = []
            seg.append((a, max(yr[0], min(yr[1], b))))
        d.text((W - R - 260, T + 6 + 16 * k), name, fill=col)
    im.save(path)


def main():
    bd = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "build/trick")
    out = os.path.join(ROOT, sys.argv[2] if len(sys.argv) > 2 else "listen/trick")
    os.makedirs(bd, exist_ok=True); os.makedirs(out, exist_ok=True)
    exe = os.path.join(bd, "obervave")
    subprocess.run(["cc", "-O2", "-Wall", "-Wno-unused-function", "-DOBV_HOST", '-DAPP_VER="dev"', "-Ifirmware/src",
                    "-Ifirmware/gen", "-o", exe, "firmware/src/obervave.c"], cwd=ROOT, check=True)
    for name, lines in SCRIPTS.items():
        sp = os.path.join(bd, name + ".txt")
        with open(sp, "w") as f:
            f.write("# generated by tests/trick/make_kit.py\n" + "\n".join(sorted(lines, key=lambda l: int(l.split()[0])))
                    + "\n")
        subprocess.run([exe, os.path.join(bd, name), sp], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        for p in os.listdir(bd):
            if p.endswith(".ppm"):
                os.unlink(os.path.join(bd, p))
        a = load(os.path.join(bd, name + ".wav"))
        if not name.startswith("tapestop_note"):
            write(os.path.join(out, name + ".wav"), a[int(T0 * FS):])

    # ---- STOP: press to silence, the fade's largest step against playing's, what comes back after PLAY
    a = load(os.path.join(bd, "kill_fullchain.wav")); m = np.abs(a).max(1); dl = np.abs(np.diff(a[:, 0]))
    ref = load(os.path.join(bd, "kill_fullchain_REF.wav"))
    for press, play, nxt in ((4.880, 6.400, 6.450), (11.200, 11.900, 14.0)):
        i0 = int(press * FS)
        last = i0 + np.nonzero(m[i0:i0 + FS] > 0)[0].max()
        print(f"STOP at {press:.3f} s: last sample {1000 * (last - i0) / FS:.1f} ms after the press; "
              f"largest step in the fade {dl[last - 300:last + 1].max():.0f} (playing, the 0.5 s before: "
              f"{dl[i0 - FS // 2:i0].max():.0f}); peak after PLAY until the next note "
              f"{m[int(play * FS):int((nxt - 0.012) * FS)].max():.0f} (without STOP there: "
              f"{np.abs(ref[int(play * FS):int((nxt - 0.012) * FS)]).max():.0f})")

    # ---- TAPE STOP: the pitch and level of one saw
    a = load(os.path.join(bd, "tapestop_note.wav")); x = a.mean(1)
    pts, lv = [], []
    for t in np.arange(3.0, 5.2, 0.01):
        f = f0_zc(x, t, 1024)
        if f > 0 and np.abs(x[int(t * FS):int(t * FS) + 1024]).max() > 200:
            pts.append((t - 3.3, 12 * np.log2(f / 523.25)))
        r = np.sqrt((x[int(t * FS):int(t * FS) + 441] ** 2).mean())
        lv.append((t - 3.3, 20 * np.log10(max(r, 1) / 1300)))
    for ms in (0, 250, 500, 600, 700, 800):
        f = f0_zc(x, 3.3 + ms / 1000, 1024)
        print(f"TAPE STOP held {ms} ms: {f:.0f} Hz ({12 * np.log2(f / 523.25):+.1f} semitones)" if f else "")
    back = 4.8 + np.nonzero(np.abs(x[int(4.8 * FS):]) > 200)[0][0] / FS
    print(f"TAPE STOP let go at 4.800 s: sound from {1000 * (back - 4.8):.1f} ms; pitch 20 ms later "
          f"{12 * np.log2(f0_zc(x, 4.82, 2048) / 523.25):+.2f} semitones")
    plot(os.path.join(out, "tapestop.png"), "TAPE STOP (SEQ held 0 .. 1.5 s, let go at 1.5): one saw, C5, 120 BPM",
         [("pitch, semitones", (200, 40, 40), pts), ("level, dB (rms over 10 ms)", (40, 90, 200), lv)],
         "semitones / dB", (-40, 5), (-0.3, 1.9))

    # ---- the SLOP ride: the pitch's wander (cents) under a held A4
    a = load(os.path.join(bd, "slop_note.wav")); x = a.mean(1)
    cs = [(t - T0, 1200 * np.log2(f0_zc(x, t) / 440)) for t in np.arange(3.0, 18.4, 0.02)]
    for lab, t0, t1 in (("ride 0 (VINTAGE 30)", 3.0, 5.7), ("ride +127 (VINTAGE 157)", 9.8, 13.7),
                        ("back to 0", 15.8, 18.4)):
        c = np.array([v for t, v in cs if t0 <= t + T0 < t1])
        print(f"SLOP {lab}: pitch {c.mean():+.1f} cents mean, wander sd {c.std():.1f}, range {c.min():+.1f} .. "
              f"{c.max():+.1f}")
    plot(os.path.join(out, "slop.png"), "SLOP ride (ALGORITHM) under a held A4: 0 -> +127 (3.2-7.2 s), held, -> 0 "
         "(11.2-13.2 s)", [("pitch, cents from 440 Hz", (200, 40, 40), cs)], "cents", (-30, 30), (0, 16))
    for name in ("slop_note", "slop_chord"):
        a = load(os.path.join(bd, name + ".wav")); dl = np.abs(np.diff(a[:, 0]))
        print(f"{name}: largest sample step while the ride turns {dl[int(5.7 * FS):int(9.7 * FS)].max():.0f}, "
              f"before it {dl[int(3.0 * FS):int(5.7 * FS)].max():.0f}")


if __name__ == "__main__":
    main()
