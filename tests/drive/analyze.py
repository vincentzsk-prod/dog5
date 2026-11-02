#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""GROWL's measurements, from the host renders (tests/drive/render.sh writes them to build/drive/).

  python3 tests/drive/analyze.py [build/drive] [--png listen/drive]

Loudness: integrated loudness per ITU-R BS.1770-4 (pyloudnorm), the musical window of each render (the splash cut).
Aliasing: a held saw's spectrum (Blackman-Harris, 2^16 points, the -92 dB sidelobes leave room to see -85 dB); every
bin more than 6 bins from a harmonic of the measured fundamental, 20 Hz - 16 kHz, is "inharmonic". Reported: the
inharmonic energy against the harmonic energy, and the loudest inharmonic bin against the fundamental.
Clicks: a knob sweep's energy above 10 kHz in 2.9 ms frames, against the median of the 120 ms around it; a frame
more than 6 dB over is a click candidate (a click is broadband: it shows up there first)."""
import os
import sys
import wave
import numpy as np

FS = 44100
T_START = 2.65                                  # the splash is over, the first note starts at 2.7 s
SOURCES = ["lowsaw", "chord", "bass", "lead"]
LEVELS = [0, 25, 50, 75, 100]


def read(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64)
    return a / 32768.0


def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(FS).integrated_loudness(x)


def bh_window(n):
    a = (0.35875, 0.48829, 0.14128, 0.01168)
    k = np.arange(n) / (n - 1) * 2 * np.pi
    return a[0] - a[1] * np.cos(k) + a[2] * np.cos(2 * k) - a[3] * np.cos(3 * k)


def spectrum(x, n=1 << 16):
    m = x[:n] if x.ndim == 1 else x[:n].mean(axis=1)
    p = np.abs(np.fft.rfft(m * bh_window(len(m)))) ** 2
    return np.fft.rfftfreq(len(m), 1 / FS), p


def fundamental(f, p, guess):
    band = (f > guess * 0.97) & (f < guess * 1.03)
    i = np.argmax(np.where(band, p, 0))
    a, b, c = np.log(p[i - 1] + 1e-30), np.log(p[i] + 1e-30), np.log(p[i + 1] + 1e-30)
    return f[i] + 0.5 * (a - c) / (a - 2 * b + c) * (f[1] - f[0])


def inharmonic(f, p, f0, fmax=16000.0, guard_bins=6):
    df = f[1] - f[0]
    k = np.round(f / f0)
    near = (k >= 1) & (np.abs(f - k * f0) <= guard_bins * df)
    band = (f >= 20) & (f <= fmax)
    harm, inh = p[band & near].sum(), p[band & ~near].sum()
    fund = p[np.abs(f - f0) <= guard_bins * df].max()
    worst_i = np.argmax(np.where(band & ~near, p, 0))
    return 10 * np.log10(inh / harm), 10 * np.log10(p[worst_i] / fund), f[worst_i]


def jump_ratio(x, block=256):
    """a sweep's clicks against fixed settings, level-free: per block the largest sample-to-sample step over the
    block's RMS (x: mono int-ish array). A click raises it; a level change does not."""
    out = []
    for b in range(0, len(x) - block, block):
        seg = x[b:b + block]
        r = np.sqrt(np.mean(seg ** 2))
        out.append(np.abs(np.diff(seg)).max() / r if r > 0 else 0.0)
    return np.array(out)


def knob_blocks(seconds=10):
    """GROWL per 256-frame block as drive_bench's sweep turns it: from 0.5 s +2 every 60 ms to 127, 0.5 s, back to 0"""
    g, nxt, dirn, out = 0, FS // 2, 1, []
    for s in range(0, FS * seconds, 256):
        if s >= nxt:
            nxt += FS * 60 // 1000; g += 2 * dirn
            if g >= 127: g, dirn, nxt = 127, -1, nxt + FS // 2
            if g <= 0 and dirn < 0: g, dirn = 0, 0
        out.append(g)
    return np.array(out)


def sweep_check(raw, fixed, f0):
    """the bench's knob sweep against the same sine at fixed GROWL: (worst click ratio, t, GROWL), (worst level dB,
    t, GROWL). Click ratio: the largest step over the RMS (4 cycles around), against the most any fixed GROWL near
    it gives (1.0 = nothing a fixed setting would not do). Level: the RMS against the fixed setting's."""
    st = np.loadtxt(fixed)
    jmp = {int(g): m / r for g, m, r in st}
    lvl = {int(g): r for g, m, r in st}
    x = np.fromfile(raw, np.int32).reshape(-1, 2)[:, 0].astype(float)
    K = knob_blocks()
    W = int(round(FS / f0 * 4))
    worst, lw = (0, 0, 0), (0, 0, 0)
    for b in range(8, len(K) - 8):
        s0 = b * 256
        seg = x[s0 - W // 2:s0 + W // 2 + 256]
        r = np.sqrt(np.mean(seg ** 2))
        j = np.abs(np.diff(seg)).max() / r / max(jmp[g] for g in set(K[b - 8:b + 9]))
        if j > worst[0]: worst = (j, s0 / FS, K[b])
        d = 20 * np.log10(r / lvl[K[b]])
        if abs(d) > abs(lw[0]): lw = (d, s0 / FS, K[b])
    return worst, lw


def clicks(x, thresh_db=6.0):
    """frames of HF energy > thresh over the local median: (time s, dB over)"""
    from scipy.signal import butter, sosfilt
    m = x.mean(axis=1)
    h = sosfilt(butter(4, 10000 / (FS / 2), "high", output="sos"), m)
    fr = 128
    e = np.array([np.mean(h[i:i + fr] ** 2) for i in range(0, len(h) - fr, fr)]) + 1e-20
    out = []
    w = 21
    for i in range(w, len(e) - w):
        med = np.median(e[i - w:i + w + 1])
        if e[i] > med * 10 ** (thresh_db / 10):
            out.append((i * fr / FS, 10 * np.log10(e[i] / med)))
    return out


def main():
    d = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "build/drive"
    png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
    s0 = int(T_START * FS)
    print("== loudness (ITU-R BS.1770-4 integrated, LUFS; delta against GROWL 0)")
    print(f"{'source':8s}" + "".join(f"{f'{v}%':>14s}" for v in LEVELS))
    table = {}
    for src in SOURCES:
        row = []
        for v in LEVELS:
            x = read(f"{d}/src_{src}_{v:03d}.wav")[s0:]
            row.append(lufs(x))
        table[src] = row
        print(f"{src:8s}" + "".join(f"{r:7.1f} ({r - row[0]:+4.1f})" for r in row))
    print("\n== aliasing: a held saw at GROWL 100 % (inharmonic energy / harmonic energy; loudest inharmonic bin / the fundamental)")
    for nm, guess in (("c6", 1046.5), ("c7", 2093.0)):
        for v in (0, 100):
            x = read(f"{d}/alias_{nm}_{v:03d}.wav")[int(3.2 * FS):]
            f, p = spectrum(x)
            f0 = fundamental(f, p, guess)
            a, b, fw = inharmonic(f, p, f0)
            print(f"{nm.upper()} f0 {f0:8.2f} Hz  GROWL {v:3d}%: inharmonic {a:6.1f} dB, loudest inharmonic bin {b:6.1f} dB at {fw:7.0f} Hz")
    for sw in ("sweep_chord", "sweep_lead"):
        p = f"{d}/{sw}.wav"
        if os.path.exists(p):
            c = clicks(read(p)[s0:])
            print(f"\n== {sw}: {len(c)} click candidates (HF frame > 6 dB over its 120 ms median)" +
                  "".join(f"\n   {t + T_START:6.3f} s  +{db:.1f} dB" for t, db in c[:10]))
    if png:
        plots(d, png)


def harmonics(x, f0_guess, n=40, nfft=1 << 15):
    f, p = spectrum(x, nfft)
    f0 = fundamental(f, p, f0_guess)
    df = f[1] - f[0]
    h = np.array([p[np.abs(f - k * f0) <= 3 * df].max() if k * f0 < FS / 2 - 4 * df else np.nan
                  for k in range(1, n + 1)])
    return 10 * np.log10(h / h[0])


def plots(d, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(out, exist_ok=True)
    colours = ("#999999", "#4a90d9", "#2ca02c", "#ff7f0e", "#d62728")
    # one held note: its harmonics one by one (an overlaid spectrum hides how they change)
    for src, f0, w in (("lowsaw", 65.4, (3.3, 5.3)), ("lead", 1046.5, (3.6, 5.2))):
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=110)
        k = np.arange(1, 41)
        for v, c in zip(LEVELS, colours):
            x = read(f"{d}/src_{src}_{v:03d}.wav")[int(w[0] * FS):int(w[1] * FS)]
            ax.plot(k, harmonics(x, f0), "o-", color=c, ms=3, lw=0.8, label=f"GROWL {v}%")
        ax.set(xlim=(0.5, 40.5), ylim=(-70, 3), xlabel="harmonic", ylabel="dB re the fundamental",
               title=f"{src}: harmonics 1-40 at GROWL 0 / 25 / 50 / 75 / 100 %")
        ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=8)
        fig.tight_layout(); fig.savefig(f"{out}/harmonics_{src}.png"); plt.close(fig)
    # several notes: the spectra stacked, one row a setting
    s0 = int(3.0 * FS)
    for src in ("chord", "bass"):
        fig, axs = plt.subplots(len(LEVELS), 1, figsize=(9, 8), dpi=110, sharex=True)
        for ax, v, c in zip(axs, LEVELS, colours):
            f, p = spectrum(read(f"{d}/src_{src}_{v:03d}.wav")[s0:])
            ax.semilogx(f[1:], 10 * np.log10(p[1:] / p.max() + 1e-14), color=c, lw=0.6)
            ax.set(ylim=(-100, 3), xlim=(20, 22050)); ax.grid(alpha=0.3, which="both")
            ax.text(0.99, 0.85, f"GROWL {v}%", transform=ax.transAxes, ha="right", fontsize=8)
        axs[0].set_title(f"{src}: spectrum at GROWL 0 / 25 / 50 / 75 / 100 % (dB, each to its own peak)")
        axs[-1].set_xlabel("Hz")
        fig.tight_layout(); fig.savefig(f"{out}/spectrum_{src}.png"); plt.close(fig)
    for nm, guess in (("c6", 1046.5), ("c7", 2093.0)):
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=110)
        x = read(f"{d}/alias_{nm}_100.wav")[int(3.2 * FS):]
        f, p = spectrum(x)
        f0 = fundamental(f, p, guess)
        db = 10 * np.log10(p / p.max() + 1e-14)
        k = np.round(f / f0)
        near = (k >= 1) & (np.abs(f - k * f0) <= 6 * (f[1] - f[0]))
        ax.plot(f, np.where(near, db, np.nan), color="#4a90d9", lw=0.6, label="harmonics of f0")
        ax.plot(f, np.where(~near, db, np.nan), color="#d62728", lw=0.6, label="inharmonic (aliasing would be here)")
        a, b, fw = inharmonic(f, p, f0)
        ax.set(xlim=(0, 22050), ylim=(-140, 3), xlabel="Hz", ylabel="dB re the fundamental",
               title=f"{nm.upper()} saw at GROWL 100 %: inharmonic {a:.1f} dB, loudest inharmonic bin {b:.1f} dB")
        ax.axvline(16000, color="#888", lw=0.5, ls="--")
        ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=8)
        fig.tight_layout(); fig.savefig(f"{out}/aliasing_{nm}.png"); plt.close(fig)
    print("plots ->", out)


if __name__ == "__main__":
    main()
