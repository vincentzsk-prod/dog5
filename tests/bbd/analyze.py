#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""ALLEY's measurements, from the host and bench renders (tests/bbd/render.sh writes them to build/bbd/).

  python3 tests/bbd/analyze.py [build/bbd] [--png listen/bbd]

Bench files are raw int32, 4 channels a frame (in L, in R, out L, out R); the echo = out - in.
The repeats: an impulse's echoes, each repeat's spectrum against the impulse (MIX and PINGPONG taken out).
The time changes: the echo of a 1 kHz sine at FEEDBK 0 is the read's speed, so its instantaneous frequency is the
pitch bend. Clicks: the echo's 2.5-7 kHz energy (a 1 kHz sine's echo bends at most to 1.5 kHz, so anything there is an
artefact) in 2.9 ms frames, against the median of the 120 ms around it; a control (the same echo with the time jumped
at once, as a plain digital delay does, through the same kind of low-pass) shows what a click scores.
Loudness: ITU-R BS.1770-4 integrated (pyloudnorm), the musical window."""
import os
import sys
import wave
import numpy as np

FS = 44100
T_START = 2.55
SRC = ["stab", "bass", "lead", "slap"]
SET = ["dry", "dbl", "slap", "sync", "long", "runaway"]
D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "build/bbd"
PNG = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None


def bench(name):
    d = np.fromfile(os.path.join(D, name + ".raw"), np.int32).reshape(-1, 4).astype(float)
    return d[:, :2], d[:, 2:] - d[:, :2]


def wav(name):
    with wave.open(os.path.join(D, name + ".wav")) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(float)
    return a[int(T_START * FS):]


def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(FS).integrated_loudness(x / 32768)


def ms_of(a):
    return 10 * 74 ** ((max(a, 1) - 1) / 126)


def repeats(name, a, nrep=5):
    _, e = bench(name)
    w = e[:, 0] + e[:, 1]                       # ping-pong: the repeats alternate sides
    n = int(round(ms_of(a) * FS / 1000)); i0 = FS // 10
    out = []
    for k in range(1, nrep + 1):
        c = i0 + k * n
        seg = w[c - min(n // 2, 300):c + min(n - 300, 4000)]
        g = np.abs(np.fft.rfft(seg, 1 << 16)) / 16384 / (178 / 256)
        f = np.fft.rfftfreq(1 << 16, 1 / FS)
        ref = g[np.argmin(abs(f - 500))]
        m = (f > 500) & (g < ref / np.sqrt(2))
        db = lambda hz: 20 * np.log10(g[np.argmin(abs(f - hz))] + 1e-12)
        out.append((k, db(500), f[m][0] if m.any() else 0, db(100), db(5000), f, g))
    return out


def band_spikes(w, lo=2500, hi=7000, fr=128, W=21):
    from scipy.signal import butter, sosfilt
    h = sosfilt(butter(6, [lo / (FS / 2), hi / (FS / 2)], "band", output="sos"), w)
    n = len(h) // fr
    e = 10 * np.log10(np.array([np.mean(h[i * fr:(i + 1) * fr] ** 2) for i in range(n)]) + 1e-9)
    lv = 10 * np.log10(np.array([np.mean(w[i * fr:(i + 1) * fr] ** 2) for i in range(n)]) + 1e-9)
    rel = e - lv
    sp = np.array([rel[i] - np.median(rel[max(0, i - W):i + W + 1]) for i in range(n)])
    s = int(1.0 * FS / fr)                      # (past the start)
    sp, rel = sp[s:], rel[s:]
    i = int(np.argmax(sp))
    return sp[i], (i + s) * fr / FS, rel[i], int((sp > 6).sum())


def main():
    figs = {}
    print("== the repeats: an impulse through ALLEY, FEEDBK 100 (each repeat against the impulse; MIX/PINGPONG out)")
    print(f"{'ALLEY':>16s} {'TONE':>5s} {'rep':>4s} {'500 Hz':>8s} {'-3 dB at':>9s} {'100 Hz':>8s} {'5 kHz':>8s}")
    rep_plot = {}
    for a in (1, 60, 100, 127):
        for tag, tone in (("imp", 127), ("impt", 70)):
            r = repeats(f"{tag}_{a}", a)
            if tone == 70: rep_plot[a] = r
            for k, d5, f3, d1, d5k, _, _ in r:
                print(f"{a:3d} ({ms_of(a):5.0f} ms) {tone:5d} {k:4d} {d5:7.1f}  {f3:7.0f} Hz {d1:7.1f} {d5k:8.1f}")
    figs["repeats"] = rep_plot

    print("\n== the tapped time: ALLEY 115 + FINE 66 (500 ms taps), an impulse's echo arrives")
    _, e = bench("tapcheck")
    w = e[:, 0]; i0 = FS // 10; pk = int(np.argmax(w)); win = np.arange(pk - 220, pk + 220)
    c = np.sum(win * np.maximum(w[win], 0)) / np.sum(np.maximum(w[win], 0))
    print(f"   at {(c - i0) / FS * 1000:.2f} ms after it (the centroid of the echo's pulse; the BBD filters themselves delay"
          f" it by ~0.1 ms)")

    print("\n== time changes (a 1 kHz sine, FEEDBK 0: the echo's pitch is the read's speed)")
    from scipy.signal import hilbert
    from scipy.ndimage import uniform_filter1d
    _, e = bench("tc")
    w = e[:, 0]
    fr = uniform_filter1d(np.diff(np.unwrap(np.angle(hilbert(w)))) * FS / 2 / np.pi, 64)
    figs["tc"] = fr
    for t0, t1, lab in ((1.5, 2.4, "one step, 80 -> 81 (+3.5 %)"), (2.5, 3.9, "80 -> 110 (103 -> 395 ms)"),
                        (4.0, 5.9, "110 -> 40 (395 -> 42 ms)")):
        s = fr[int(t0 * FS):int(t1 * FS)]
        semis = 12 * np.log2(np.clip(s, 1, None) / 1000)
        bent = (np.abs(semis) > 0.05).sum() / FS
        acc = np.abs(np.diff(uniform_filter1d(semis, 441), 1)).max() * FS
        print(f"   {lab:30s} pitch {semis.min():+6.2f} .. {semis.max():+6.2f} semitones, bent {bent * 1000:4.0f} ms, "
              f"fastest bend {acc:5.0f} semitones/s")
    print("   (the old delay: the speed stepped to 0.5 or 1.5 at once, -12 / +7 semitones in one sample, and back)")

    print("\n== clicks: the echo's 2.5-7 kHz against its own 120 ms median (a spike = a click)")
    from scipy.signal import butter, sosfilt
    t = np.arange(4 * FS) / FS
    for lab, dl in (("control: the time jumped at once", np.where(t < 2, 0.10325, 0.39538)),
                    ("control: no change", np.full(len(t), 0.10325))):
        y = sosfilt(butter(3, 4600 / (FS / 2), output="sos"), 8192 * np.sin(2 * np.pi * 1000 * (t - dl)))
        sp, at, lv, n6 = band_spikes(y)
        print(f"   {lab:40s} worst spike {sp:+5.1f} dB at {at:.3f} s (the band there: {lv:6.1f} dB under the echo), "
              f"frames over +6 dB: {n6}")
    for nm, lab in (("ck0_jump", "ALLEY: jumps 80->120->20->127"), ("ck0_sweep", "ALLEY: swept 1->127->1, a step / 60 ms"),
                    ("tc", "ALLEY: the time-change render above")):
        _, e = bench(nm)
        sp, at, lv, n6 = band_spikes(e[:, 0])
        print(f"   {lab:40s} worst spike {sp:+5.1f} dB at {at:.3f} s (the band there: {lv:6.1f} dB under the echo), "
              f"frames over +6 dB: {n6}")
    print("   (FEEDBK 0 on purpose: with feedback a repeat is bent again on every pass and climbs into the band for real)")

    print("\n== self-oscillation: a 440 Hz burst, then FEEDBK held (80 ms; MIX 127): the echo's RMS, dBFS")
    so = {}
    for nm in [f"so_{v}" for v in (100, 112, 116, 118, 120, 122, 124, 127)] + ["so_127_long", "so_127_short"]:
        _, e = bench(nm)
        rms = [20 * np.log10(np.sqrt((e[int(t * FS):int((t + 1) * FS)] ** 2).mean()) / 32768 + 1e-12) for t in (1, 3, 6, 10, 19)]
        so[nm] = e
        lab = nm.replace("so_", "FEEDBK ").replace("_long", " at 740 ms").replace("_short", " at 10 ms, TONE 127")
        print(f"   {lab:26s} " + " ".join(f"{t:2d}s {r:6.1f}" for t, r in zip((1, 3, 6, 10, 19), rms))
              + f"  | peak {20 * np.log10(np.abs(e).max() / 32768):+5.1f} dBFS")
    figs["so"] = so

    print("\n== the headroom: one repeat of a 200 ms 1 kHz burst (FEEDBK 0, 294 ms), harmonics against the fundamental")
    for p in (3277, 8231, 16423, 32767):
        _, e = bench(f"thd_{p}")
        x = e[int(0.42 * FS):int(0.58 * FS), 0]
        S = np.abs(np.fft.rfft(x * np.blackman(len(x))))
        f = np.fft.rfftfreq(len(x), 1 / FS)
        h = lambda k: S[np.argmin(abs(f - 1000 * k))]
        g = np.sqrt((x ** 2).mean()) * np.sqrt(2) / p / (178 / 256)
        print(f"   {20 * np.log10(p / 32768):5.0f} dBFS in: echo gain {20 * np.log10(g):+5.2f} dB, H3 {20 * np.log10(h(3) / h(1)):6.1f} dB, "
              f"H5 {20 * np.log10(h(5) / h(1)):6.1f} dB")

    print("\n== the kit: energy against the dry render (ungated, the whole file: integrated LUFS's gate reads sparse")
    print("   material with echoes as QUIETER, so it is no use here), the peak in dBFS, and samples at full scale")
    print(f"{'source':8s}" + "".join(f"{s:>15s}" for s in SET) + f"{'old sync':>15s}")
    def en(x): return 10 * np.log10((x ** 2).sum())
    for src in SRC:
        row, d0 = [], en(wav(f"src_{src}_dry"))
        for s in SET + ["old"]:
            x = wav(f"old_{src}_sync" if s == "old" else f"src_{src}_{s}")
            fs = int((np.abs(x) >= 32767).sum())
            row.append(f"{en(x) - d0:+5.1f} {20 * np.log10(np.abs(x).max() / 32768):+5.1f}" + (f" C{fs}" if fs else ""))
        print(f"{src:8s}" + "".join(f"{r:>15s}" for r in row))

    print("\n== old vs new, SYNC 1/8. FEEDBK 60 MIX 70 (the same bytes): the echo's spectrum after the stab (3.0-4.6 s)")
    for src in ("stab", "lead"):
        a, b, d0 = wav(f"old_{src}_sync"), wav(f"src_{src}_sync"), wav(f"src_{src}_dry")
        seg = slice(int((3.0 - T_START) * FS), int((4.6 - T_START) * FS))
        out = []
        for x in (a, b):
            e = (x - d0)[seg].mean(axis=1)          # the echo alone (the dry is bit-exact in both)
            S = np.abs(np.fft.rfft(e * np.hanning(len(e)))) ** 2; f = np.fft.rfftfreq(len(e), 1 / FS)
            bands = [10 * np.log10(S[(f >= lo) & (f < hi)].sum() + 1e-9) for lo, hi in ((100, 1000), (1000, 4000), (4000, 8000), (8000, 16000))]
            out.append(bands)
        d = np.array(out[1]) - np.array(out[0])
        print(f"   {src:5s} new - old: 0.1-1 kHz {d[0]:+5.1f} dB, 1-4 kHz {d[1]:+5.1f}, 4-8 kHz {d[2]:+5.1f}, 8-16 kHz {d[3]:+5.1f}")

    print("\n== with GROWL and CHEW: what ALLEY adds (energy against the same chain without it), the peak, full-scale samples")
    for src in ("stab", "bass", "lead"):
        for nm in ("g050_sync", "sync_c050", "g050_sync_c050", "g100_runaway_c100"):
            x, y = wav(f"combo_{src}_{nm}"), wav(f"combo_{src}_{nm}_noalley")
            fs = int((np.abs(x) >= 32767).sum())
            print(f"   {src:5s} {nm:18s} {en(x) - en(y):+5.1f} dB, peak {20 * np.log10(np.abs(x).max() / 32768):+5.1f} dBFS "
                  f"(without ALLEY {20 * np.log10(np.abs(y).max() / 32768):+5.1f}), samples at full scale {fs}")

    print("\n== bypass with the line ringing (mix_off_ringing: MIX 0 from 4.0 s): differing samples from 4.01 s")
    a, b = wav("mix_off_ringing"), wav("mix_off_ringing_oldbuild")
    i = int((4.01 - T_START) * FS)
    print(f"   {(a[i:] != b[i:]).any(axis=1).sum()} of {len(a) - i} (before 3.99 s: "
          f"{(a[:int((3.99 - T_START) * FS)] != b[:int((3.99 - T_START) * FS)]).any(axis=1).sum()}, ALLEY vs the old delay)")

    if PNG:
        plots(figs)


def plots(figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9})
    fig, ax = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
    for i, a in enumerate((1, 60, 100, 127)):
        for k, _, _, _, _, f, g in figs["repeats"][a]:
            ax[i].semilogx(f[1:], 20 * np.log10(g[1:] + 1e-9), label=f"repeat {k}")
        ax[i].set_title(f"ALLEY {ms_of(a):.0f} ms, FEEDBK 100, TONE 70")
        ax[i].set_xlim(40, 20000); ax[i].set_ylim(-60, 3); ax[i].grid(alpha=.3); ax[i].set_xlabel("Hz")
    ax[0].set_ylabel("dB against the input"); ax[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "repeats.png"), dpi=110); plt.close(fig)

    fr = figs["tc"]
    t = np.arange(len(fr)) / FS
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(t, 12 * np.log2(np.clip(fr, 1, None) / 1000), lw=1)
    for x, lab in ((1.5, "1 step"), (2.5, "103 -> 395 ms"), (4.0, "395 -> 42 ms")):
        ax.axvline(x, color="k", alpha=.2); ax.text(x + .03, 7.5, lab, fontsize=8)
    ax.set_ylim(-13, 9); ax.set_xlim(1, 6); ax.grid(alpha=.3)
    ax.set_xlabel("s"); ax.set_ylabel("echo pitch, semitones")
    ax.set_title("A time change bends the repeats in the line (1 kHz sine, FEEDBK 0): eased in and out, no step")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "time_change_pitch.png"), dpi=110); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 3.2))
    for nm, e in figs["so"].items():
        if nm in ("so_127_long", "so_127_short"): continue
        x = e[:, 0] + e[:, 1]; n = int(0.4 * FS)    # (400 ms: five echoes a window, so the envelope, not the rhythm)
        r = [np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)]
        ax.plot(np.arange(len(r)) * n / FS, 20 * np.log10(np.array(r) / 32768 + 1e-9), label=nm.replace("so_", "FEEDBK "))
    ax.set_ylim(-90, 0); ax.grid(alpha=.3); ax.legend(fontsize=7, ncol=4); ax.set_xlabel("s"); ax.set_ylabel("echo RMS, dBFS")
    ax.set_title("FEEDBK's top: 116 a long decay, ~120 holds, above it runs away and settles under full scale (80 ms, MIX 127)")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "self_oscillation.png"), dpi=110); plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(12, 3.4), sharey=True)
    for i, src in enumerate(("stab", "lead")):
        d0 = wav(f"src_{src}_dry")
        from scipy.ndimage import uniform_filter1d
        ref = None
        for nm, lab in ((f"old_{src}_sync", "old delay"), (f"src_{src}_sync", "ALLEY")):
            e = (wav(nm) - d0)[int((3.0 - T_START) * FS):int((4.6 - T_START) * FS)].mean(axis=1)
            S = np.abs(np.fft.rfft(e * np.hanning(len(e)))); f = np.fft.rfftfreq(len(e), 1 / FS)
            ref = S.max() if ref is None else ref    # (both against the old delay's loudest bin)
            ax[i].semilogx(f[1:], 20 * np.log10(uniform_filter1d(S, 40)[1:] / ref + 1e-9), label=lab, lw=1)
        ax[i].set_title(f"{src}: the echoes alone, SYNC 1/8. FEEDBK 60 MIX 70"); ax[i].set_xlim(40, 20000)
        ax[i].set_ylim(-90, 3); ax[i].grid(alpha=.3); ax[i].legend(); ax[i].set_xlabel("Hz")
    ax[0].set_ylabel("dB")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "spectrum_old_vs_alley.png"), dpi=110); plt.close(fig)
    print("pictures ->", PNG)


if __name__ == "__main__":
    main()
