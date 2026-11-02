#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""TAPE's measurements, from the host renders and the bench's (tests/tape/render.sh writes them to build/tape/).

  python3 tests/tape/analyze.py [build/tape] [--png listen/tape]

Loudness: ITU-R BS.1770-4 integrated (pyloudnorm), the musical window of each render (the splash cut), as GROWL's.
Wow and flutter: a 1 kHz sine through TAPE alone; its instantaneous frequency (Hilbert), smoothed over 4.5 ms (the
saturation's 3rd harmonic would ripple it at 2 kHz), as a pitch deviation in %; wow = below 4 Hz, flutter = 4-200 Hz.
Aliasing, three ways:
  1. the synth: a held saw (an exact harmonic comb) at CHEW 0 and 100; anything outside each harmonic's own wobble
     (+-(k f0 x the peak pitch deviation + a margin)) counts as inharmonic, as in GROWL's table;
  2. the read alone (the bench, TP_ONLY=read): a pure tone through the moving head, against the ideal output for the
     head's exact logged trajectory (the residual is the read's own error: interpolation, rounding, aliasing);
  3. the record alone (TP_ONLY=sat): the 2x saturation on a pure tone, everything not a harmonic of it.
Clicks: a knob sweep's energy above 10 kHz in 2.9 ms frames against the median of the 120 ms around it, as GROWL's,
but only where the frame is above -80 dBFS (below that a "click" is a flicker of the last bits); and the bench's sweep
against fixed settings (the largest step over the RMS: 1.0 = nothing a fixed CHEW near it would not do).
Hiss: a DC input (it keeps the hiss awake), the output's AC part. GROWL + CHEW: each combination's loudness, and its
music against its hiss band by band (the hiss = the render minus the same render with HISS 0, sample for sample:
everything else in TAPE is deterministic and the same)."""
import os
import sys
import wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _drive_analyze():                           # GROWL's (read, lufs, the window, the spectrum, the fundamental),
    import importlib.util                       # under its own name: both kits call theirs analyze.py
    spec = importlib.util.spec_from_file_location("drive_analyze", os.path.join(HERE, "..", "drive", "analyze.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D = _drive_analyze()

FS = 44100
T_START = 2.65
SOURCES = ["lowsaw", "chord", "bass", "lead"]
LEVELS = [0, 25, 50, 75, 100]
RAW = {0: 0, 25: 32, 50: 64, 75: 95, 100: 127}
COMBOS = [(25, 25), (50, 50), (100, 50), (50, 100), (100, 100)]
BANDS = [(100, 1000), (1000, 4000), (4000, 8000), (8000, 16000)]


def raw(path):
    return np.fromfile(path, np.int32).reshape(-1, 2).astype(np.float64)


def pitch_dev(x, f0=1000.0):
    from scipy.signal import hilbert
    a = hilbert(x)
    inst = np.diff(np.unwrap(np.angle(a))) * FS / (2 * np.pi)
    k = 200
    sm = np.convolve(inst, np.ones(k) / k, "same")[2000:-2000]
    return (sm / f0 - 1) * 100


def wow_flutter(dev):
    from scipy.signal import butter, sosfiltfilt
    dev = dev - dev.mean()
    w = sosfiltfilt(butter(2, 4 / (FS / 2), "low", output="sos"), dev)
    f = sosfiltfilt(butter(2, [4 / (FS / 2), 200 / (FS / 2)], "band", output="sos"), dev)
    return np.abs(dev).max(), dev.std(), np.abs(w).max(), np.abs(f).max(), f.std()


def guard_inharmonic(f, p, f0, delta, extra, fmax=16000.0):
    df = f[1] - f[0]
    ok = np.zeros_like(f, bool)
    k = 1
    while k * f0 < FS / 2 + 2000:
        ok |= np.abs(f - k * f0) <= k * f0 * delta + extra + 6 * df
        k += 1
    band = (f >= 20) & (f <= fmax)
    fund = p[np.abs(f - f0) <= f0 * delta + extra + 6 * df].max()
    i = np.argmax(np.where(band & ~ok, p, 0))
    return 10 * np.log10(p[band & ~ok].sum() / p[band & ok].sum()), 10 * np.log10(p[i] / fund), f[i]


def read_residual(d, f0):
    """the bench's read-only render against the ideal moving delay (the logged head, the downsampler's lag fitted)"""
    y = raw(f"{d}/bench_read_{f0}.raw")[:, 0]
    dl = np.fromfile(f"{d}/bench_read_{f0}.d", np.int32).astype(np.float64) / 65536
    prev = np.concatenate([[dl[0]], dl[:-1]])
    j = np.arange(1, 17)
    da = (prev[:, None] + (dl - prev)[:, None] * (2 * j - 1) / 32).ravel()
    db = (prev[:, None] + (dl - prev)[:, None] * (2 * j) / 32).ravel()
    dd = (da + db) / 4                          # the head, in 44.1 kHz samples
    n = np.arange(len(y))
    seg = slice(3 * FS, 6 * FS)
    best = None
    for lag in np.arange(0.0, 4.001, 0.05):
        th = 2 * np.pi * f0 * (n[seg] - np.interp(n[seg] - lag, n, dd)) / FS
        M = np.vstack([np.sin(th), np.cos(th)]).T
        c, *_ = np.linalg.lstsq(M, y[seg], rcond=None)
        r = y[seg] - M @ c
        e = np.sum(r ** 2)
        if best is None or e < best[0]:
            best = (e, lag, r, M @ c)
    e, lag, r, ideal = best
    N = 1 << 16
    w = D.bh_window(N)
    pr = np.abs(np.fft.rfft(r[:N] * w)) ** 2
    pi = np.abs(np.fft.rfft(ideal[:N] * w)) ** 2
    f = np.fft.rfftfreq(N, 1 / FS)
    i = np.argmax(pr * (f > 20))
    return 10 * np.log10(e / np.sum(ideal ** 2)), 10 * np.log10(pr[i] / pi.max()), f[i], lag


def skirt_vs_ideal(d, f0):
    """the ideal tone on TAPE's own logged head vs TAPE's output: energy outside the tone's own wobble, for both"""
    y = raw(f"{d}/bench_read_{f0}.raw")[:, 0]
    dl = np.fromfile(f"{d}/bench_read_{f0}.d", np.int32).astype(np.float64) / 65536
    prev = np.concatenate([[dl[0]], dl[:-1]])
    j = np.arange(1, 17)
    dd = ((prev[:, None] + (dl - prev)[:, None] * (2 * j - 1) / 32).ravel()
          + (prev[:, None] + (dl - prev)[:, None] * (2 * j) / 32).ravel()) / 4
    n = np.arange(len(y))
    seg = slice(3 * FS, 3 * FS + (1 << 16))
    out = []
    for x in (np.sin(2 * np.pi * f0 * (n[seg] - dd[seg]) / FS), y[seg]):
        f, p = D.spectrum(x)
        out.append(guard_inharmonic(f, p, f0, 0.019, 150.0, fmax=min(20000, 3 * f0)))
    return out


def dropouts(x):
    fr = int(0.005 * FS)
    env = np.array([np.sqrt(np.mean(x[i:i + fr] ** 2)) for i in range(0, len(x) - fr, fr)])
    db = 20 * np.log10(env / np.median(env))
    dip = db < -2.0
    n, depths, lens, i = 0, [], [], 0
    while i < len(dip):
        if dip[i]:
            j = i
            while j < len(dip) and dip[j]: j += 1
            n += 1; depths.append(-db[i:j].min()); lens.append((j - i) * 5); i = j
        else:
            i += 1
    return n, np.array(depths), np.array(lens)


def sat_only(d, f0):
    x = raw(f"{d}/bench_sat_{f0}.raw")[3 * FS:, 0]
    f, p = D.spectrum(x)
    return guard_inharmonic(f, p, f0, 0.0, 3.0, fmax=20000)


def clicks(x, thresh_db=6.0, floor_db=-80.0):
    from scipy.signal import butter, sosfilt
    m = x.mean(axis=1)
    h = sosfilt(butter(4, 10000 / (FS / 2), "high", output="sos"), m)
    fr = 128
    e = np.array([np.mean(h[i:i + fr] ** 2) for i in range(0, len(h) - fr, fr)]) + 1e-20
    out, w, floor = [], 21, 10 ** (floor_db / 10)
    for i in range(w, len(e) - w):
        med = np.median(e[i - w:i + w + 1])
        if e[i] > med * 10 ** (thresh_db / 10) and e[i] > floor:
            out.append((i * fr / FS, 10 * np.log10(e[i] / med), 10 * np.log10(e[i])))
    return out


def knob_blocks(seconds=12):
    g, nxt, dirn, out = 0, FS // 2, 1, []
    for s in range(0, FS * seconds, 256):
        if s >= nxt:
            nxt += FS * 60 // 1000; g += 2 * dirn
            if g >= 127: g, dirn, nxt = 127, -1, nxt + FS // 2
            if g <= 0 and dirn < 0: g, dirn = 0, 0
        out.append(g)
    return np.array(out)


def sweep_check(d, nm, f0):
    st = np.loadtxt(f"{d}/bench_fixed_{nm}.txt")
    jmp = {int(g): m / r for g, m, r in st}
    lvl = {int(g): r for g, m, r in st}
    x = raw(f"{d}/bench_sweep_{nm}.raw")[:, 0]
    K = knob_blocks()
    W = int(round(FS / f0 * 8))
    worst, lw = (0, 0, 0), (0, 0, 0)
    for b in range(8, len(K) - 8):
        s0 = b * 256
        seg = x[s0 - W // 2:s0 + W // 2 + 256]
        r = np.sqrt(np.mean(seg ** 2))
        j = np.abs(np.diff(seg)).max() / r / max(jmp[g] for g in set(K[b - 8:b + 9]))
        if j > worst[0]: worst = (j, s0 / FS, K[b])
        dv = 20 * np.log10(r / lvl[K[b]])
        if abs(dv) > abs(lw[0]): lw = (dv, s0 / FS, K[b])
    return worst, lw


def band_db(x, lo, hi):
    n = len(x)
    p = np.abs(np.fft.rfft(x * np.hanning(n))) ** 2
    f = np.fft.rfftfreq(n, 1 / FS)
    return 10 * np.log10(p[(f >= lo) & (f < hi)].sum() + 1e-20)


def music_vs_hiss(d, with_hiss, no_hiss, t0=3.0, t1=5.5):
    a = D.read(f"{d}/{with_hiss}.wav")[int(t0 * FS):int(t1 * FS)].mean(axis=1)
    b = D.read(f"{d}/{no_hiss}.wav")[int(t0 * FS):int(t1 * FS)].mean(axis=1)
    h = a - b
    return [band_db(b, lo, hi) - band_db(h, lo, hi) for lo, hi in BANDS], 20 * np.log10(np.sqrt(np.mean(h ** 2)) + 1e-12)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "build/tape"
    png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
    s0 = int(T_START * FS)
    print("== loudness (ITU-R BS.1770-4 integrated, LUFS; delta against CHEW 0)")
    print(f"{'source':8s}" + "".join(f"{f'{v}%':>14s}" for v in LEVELS))
    for src in SOURCES:
        row = [D.lufs(D.read(f"{d}/src_{src}_{v:03d}.wav")[s0:]) for v in LEVELS]
        print(f"{src:8s}" + "".join(f"{r:7.1f} ({r - row[0]:+5.2f})" for r in row))

    print("\n== wow and flutter: a 1 kHz sine through TAPE alone (pitch deviation, %; wow < 4 Hz, flutter 4-200 Hz)")
    for v, wf in ((32, 64), (64, 64), (95, 64), (127, 64), (127, 0), (127, 127)):
        nm = f"bench_wow_{v}" + ("" if wf == 64 else f"_wf{wf}")
        pk, rms, wpk, fpk, frms = wow_flutter(pitch_dev(raw(f"{d}/{nm}.raw")[2 * FS:, 0]))
        print(f"CHEW {round(v * 100 / 127):3d}% WOW/FLT {wf:3d}: peak {pk:5.2f} %  rms {rms:5.3f} %   wow peak {wpk:5.2f} %"
              f"   flutter peak {fpk:5.3f} % rms {frms:5.3f} %")

    print("\n== the record's saturation: a 1 kHz sine at -6 dBFS (harmonics re the fundamental)")
    for v in (32, 64, 95, 127):
        x = raw(f"{d}/bench_thd_{v}.raw")[3 * FS:, 0]
        f, p = D.spectrum(x)
        h = [p[np.abs(f - k * 1000) < 30].sum() for k in (1, 2, 3, 5)]
        print(f"CHEW {round(v * 100 / 127):3d}%: H2 {10 * np.log10(h[1] / h[0]):6.1f}  H3 {10 * np.log10(h[2] / h[0]):6.1f}"
              f"  H5 {10 * np.log10(h[3] / h[0]):6.1f} dB")

    print("\n== hiss (a DC input keeps it awake; RMS of the output's AC part, dBFS)")
    for v in (1, 16, 32, 48, 64, 80, 95, 111, 127):
        x = raw(f"{d}/bench_hiss_{v}.raw")[FS:, 0]
        print(f"CHEW {round(v * 100 / 127):3d}%, HISS 0 dB: {20 * np.log10(np.std(x) / 32768):6.1f} dBFS")
    for h, nm in ((1, "-12 dB"), (127, "+12 dB")):
        x = raw(f"{d}/bench_hiss_127_{h}.raw")[FS:, 0]
        print(f"CHEW 100%, HISS {nm}: {20 * np.log10(np.std(x) / 32768):6.1f} dBFS")

    print("\n== dropouts: a 1 kHz sine for 30 s (the envelope, 5 ms frames; a dip = > 2 dB under the median)")
    for c in (64, 95, 127):
        for dr in (64, 127):
            n, depths, lens = dropouts(raw(f"{d}/bench_drops_{c}_{dr}.raw")[FS:, 0])
            print(f"CHEW {round(c * 100 / 127):3d}% DROPS {'100%' if dr == 64 else '300%'}: {n / 29:4.2f} a second"
                  + (f", depth {np.median(depths):4.1f} dB median ({np.max(depths):4.1f} deepest), {np.median(lens):3.0f} ms"
                     f" median length" if n else ""))
    print("\n== aliasing 1: the synth, a held saw (VINTAGE 0), hiss and dropouts off. Inharmonic = outside every harmonic's"
          "\n   own wobble +-(k f0 x 1.7 % + 20 Hz) with wow alone, +-(k f0 x 1.9 % + 150 Hz) with wow + flutter")
    for nm, guess in (("c6", 1046.5), ("c7", 2093.0)):
        for v, wf, dl, ex in ((0, 0, 0.0, 0.0), (100, 0, 0.017, 20.0), (100, 64, 0.019, 150.0)):
            x = D.read(f"{d}/alias_{nm}_{v:03d}_wf{wf:03d}.wav")[int(3.2 * FS):]
            f, p = D.spectrum(x)
            f0 = D.fundamental(f, p, guess)
            a, b, fw = guard_inharmonic(f, p, f0, dl, ex)
            print(f"{nm.upper()} CHEW {v:3d}% WOW/FLT {wf:3d}: inharmonic {a:6.1f} dB, loudest inharmonic bin {b:6.1f} dB at {fw:7.0f} Hz")
    print("\n== aliasing 2: the moving read alone (CHEW 100, wow + flutter), against the ideal output for its own logged head")
    for f0 in (1000, 5000, 10000, 15000, 18000):
        e, b, fw, lag = read_residual(d, f0)
        print(f"sine {f0:5d} Hz: residual {e:6.1f} dB re the tone, loudest residual bin {b:6.1f} dB at {fw:7.0f} Hz"
              f"  (the downsampler's lag {lag:.2f} samples)")
    print("\n   the same tones: the ideal output for the logged head against TAPE's, outside +-(1.9 % + 150 Hz) of the tone"
          "\n   (if TAPE's skirt is the ideal's, everything outside the partials is the wobble itself, not an artefact)")
    for f0 in (1000, 5000, 10000):
        (ia, ib, ifw), (ta, tb, tfw) = skirt_vs_ideal(d, f0)
        print(f"sine {f0:5d} Hz: ideal {ia:6.1f} dB (loudest {ib:6.1f} at {ifw:6.0f} Hz)   TAPE {ta:6.1f} dB (loudest {tb:6.1f} at {tfw:6.0f} Hz)")
    print("\n== aliasing 3: the 2x record (saturation) alone, CHEW 100, a -6 dBFS tone: everything not a harmonic of it")
    for f0 in (1000, 5000, 10000, 15000, 18000):
        a, b, fw = sat_only(d, f0)
        print(f"sine {f0:5d} Hz: inharmonic {a:6.1f} dB, loudest inharmonic bin {b:6.1f} dB at {fw:7.0f} Hz")

    print("\n== clicks")
    for sw in ("sweep_chord", "sweep_lead", "toggle_chord"):
        c = clicks(D.read(f"{d}/{sw}.wav")[s0:])
        print(f"{sw}: {len(c)} click candidates (HF frame > 6 dB over its 120 ms median and above -80 dBFS)" +
              "".join(f"\n   {t + T_START:6.3f} s  +{db:.1f} dB (frame {lv:.0f} dB)" for t, db, lv in c[:10]))
    for nm, f0 in (("1k", 1000), ("5k", 5000)):
        (j, tj, gj), (lv, tl, gl) = sweep_check(d, nm, f0)
        print(f"bench sweep, {nm} sine: worst step ratio {j:.3f} (at {tj:.2f} s, CHEW {gj}); level against fixed settings"
              f" at worst {lv:+.2f} dB (at {tl:.2f} s, CHEW {gl})")

    print("\n== GROWL + CHEW: loudness (LUFS; against the same GROWL with CHEW 0, and against both at 0)")
    for src in SOURCES:
        dry = D.lufs(D.read(f"{d}/combo_{src}_g025c000.wav")[s0:])   # (GROWL 25: the dry reference is GROWL's own)
        base0 = D.lufs(D.read(f"{d}/src_{src}_000.wav")[s0:])
        out = []
        for g, c in COMBOS:
            ref = D.lufs(D.read(f"{d}/combo_{src}_g{g:03d}c000.wav")[s0:])
            x = D.lufs(D.read(f"{d}/combo_{src}_g{g:03d}c{c:03d}.wav")[s0:])
            out.append(f"G{g}/C{c}: {x - ref:+5.2f} ({x - base0:+5.2f})")
        print(f"{src:7s} " + "  ".join(out))
        del dry
    print("\n== music over hiss, band by band (dB; 3.0-5.5 s), CHEW alone and with GROWL")
    print(f"{'':22s}" + "".join(f"{f'{lo}-{hi} Hz':>15s}" for lo, hi in BANDS) + "   hiss RMS")
    for src in SOURCES:
        for g, c in [(0, 50), (0, 100)] + COMBOS:
            if g == 0:
                m, hr = music_vs_hiss(d, f"src_{src}_{c:03d}", f"nohiss_{src}_{c:03d}")
            else:
                m, hr = music_vs_hiss(d, f"combo_{src}_g{g:03d}c{c:03d}", f"combonh_{src}_g{g:03d}c{c:03d}")
            print(f"{src:7s} GROWL {g:3d} CHEW {c:3d}" + "".join(f"{x:15.1f}" for x in m) + f"   {hr:6.1f} dBFS")
    if png:
        plots(d, png)


def plots(d, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(out, exist_ok=True)
    colours = ("#999999", "#4a90d9", "#2ca02c", "#ff7f0e", "#d62728")
    # the wow: pitch against time
    fig, axs = plt.subplots(2, 1, figsize=(9, 6), dpi=110, sharex=True)
    for v, c in zip((32, 64, 95, 127), colours[1:]):
        dev = pitch_dev(raw(f"{d}/bench_wow_{v}.raw")[2 * FS:, 0])
        axs[0].plot(np.arange(len(dev)) / FS, dev, color=c, lw=0.7, label=f"CHEW {round(v * 100 / 127)}%")
    for nm, c, lab in (("bench_wow_127_wf0", "#4a90d9", "WOW/FLT 0 (wow only)"), ("bench_wow_127", "#d62728", "64 (both)"),
                       ("bench_wow_127_wf127", "#2ca02c", "127 (flutter only)")):
        dev = pitch_dev(raw(f"{d}/{nm}.raw")[2 * FS:, 0])
        axs[1].plot(np.arange(len(dev)) / FS, dev, color=c, lw=0.6, label=lab)
    axs[0].set(ylabel="pitch, % off", title="TAPE's wow and flutter: a 1 kHz sine, pitch deviation over 10 s")
    axs[1].set(ylabel="pitch, % off", xlabel="s", title="CHEW 100 %: the WOW/FLT balance")
    for a in axs:
        a.grid(alpha=0.3); a.legend(loc="upper right", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{out}/wow_flutter.png"); plt.close(fig)
    # one held note: its harmonics
    for src, f0, w in (("lowsaw", 65.4, (3.3, 5.3)), ("lead", 1046.5, (3.6, 5.2))):
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=110)
        k = np.arange(1, 41)
        for v, c in zip(LEVELS, colours):
            x = D.read(f"{d}/nohiss_{src}_{v:03d}.wav" if v else f"{d}/src_{src}_000.wav")[int(w[0] * FS):int(w[1] * FS)]
            ax.plot(k, D.harmonics(x, f0), "o-", color=c, ms=3, lw=0.8, label=f"CHEW {v}%")
        ax.set(xlim=(0.5, 40.5), ylim=(-80, 3), xlabel="harmonic", ylabel="dB re the fundamental",
               title=f"{src}: harmonics 1-40 at CHEW 0 / 25 / 50 / 75 / 100 % (hiss off for the picture)")
        ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=8)
        fig.tight_layout(); fig.savefig(f"{out}/harmonics_{src}.png"); plt.close(fig)
    # several notes: the spectra stacked
    s0 = int(3.0 * FS)
    for src in ("chord", "bass"):
        fig, axs = plt.subplots(len(LEVELS), 1, figsize=(9, 8), dpi=110, sharex=True)
        for ax, v, c in zip(axs, LEVELS, colours):
            f, p = D.spectrum(D.read(f"{d}/src_{src}_{v:03d}.wav")[s0:])
            ax.semilogx(f[1:], 10 * np.log10(p[1:] / p.max() + 1e-14), color=c, lw=0.6)
            ax.set(ylim=(-110, 3), xlim=(20, 22050)); ax.grid(alpha=0.3, which="both")
            ax.text(0.99, 0.85, f"CHEW {v}%", transform=ax.transAxes, ha="right", fontsize=8)
        axs[0].set_title(f"{src}: spectrum at CHEW 0 / 25 / 50 / 75 / 100 % (dB, each to its own peak; hiss on)")
        axs[-1].set_xlabel("Hz")
        fig.tight_layout(); fig.savefig(f"{out}/spectrum_{src}.png"); plt.close(fig)
    # the aliasing proof: the synth's saw, harmonics and their wobble in blue, everything else red
    for nm, guess in (("c6", 1046.5), ("c7", 2093.0)):
        fig, axs = plt.subplots(2, 1, figsize=(9, 7), dpi=110, sharex=True)
        for ax, (wf, dl, ex) in zip(axs, ((0, 0.017, 20.0), (64, 0.019, 150.0))):
            x = D.read(f"{d}/alias_{nm}_100_wf{wf:03d}.wav")[int(3.2 * FS):]
            f, p = D.spectrum(x)
            f0 = D.fundamental(f, p, guess)
            db = 10 * np.log10(p / p.max() + 1e-14)
            ok = np.zeros_like(f, bool)
            k = 1
            while k * f0 < FS / 2 + 2000:
                ok |= np.abs(f - k * f0) <= k * f0 * dl + ex + 6 * (f[1] - f[0]); k += 1
            a, b, fw = guard_inharmonic(f, p, f0, dl, ex)
            ax.plot(f, np.where(ok, db, np.nan), color="#4a90d9", lw=0.6, label="the harmonics and their own wobble")
            ax.plot(f, np.where(~ok, db, np.nan), color="#d62728", lw=0.6, label="everything else (aliasing would be here)")
            ax.set(xlim=(0, 22050), ylim=(-140, 3), ylabel="dB re the fundamental",
                   title=f"{nm.upper()} saw, CHEW 100 %, WOW/FLT {wf}: inharmonic {a:.1f} dB, loudest {b:.1f} dB at {fw:.0f} Hz")
            ax.axvline(16000, color="#888", lw=0.5, ls="--"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=8)
        axs[-1].set_xlabel("Hz")
        fig.tight_layout(); fig.savefig(f"{out}/aliasing_{nm}.png"); plt.close(fig)
    # GROWL + CHEW: the music and the hiss, the chord and the bass at GROWL 100 / CHEW 100 and CHEW 100 alone
    fig, axs = plt.subplots(2, 2, figsize=(11, 6.5), dpi=110, sharex=True, sharey=True)
    for row, src in enumerate(("chord", "lead")):
        for col, (wh, nh, lab) in enumerate(((f"src_{src}_100", f"nohiss_{src}_100", "CHEW 100 %"),
                                             (f"combo_{src}_g100c100", f"combonh_{src}_g100c100", "GROWL 100 % + CHEW 100 %"))):
            a = D.read(f"{d}/{wh}.wav")[int(3.0 * FS):int(5.5 * FS)].mean(axis=1)
            b = D.read(f"{d}/{nh}.wav")[int(3.0 * FS):int(5.5 * FS)].mean(axis=1)
            n = 1 << 16
            for sig, c, l2 in ((b, "#4a90d9", "the music"), (a - b, "#d62728", "the hiss")):
                p = np.abs(np.fft.rfft(sig[:n] * D.bh_window(n))) ** 2
                f = np.fft.rfftfreq(n, 1 / FS)
                k = 64
                ps = np.convolve(p, np.ones(k) / k, "same")
                axs[row][col].semilogx(f[1:], 10 * np.log10(ps[1:] / (32768.0 ** 2 * n) + 1e-20), color=c, lw=0.7, label=l2)
            axs[row][col].set(xlim=(50, 22050), ylim=(-165, -75), title=f"{src}: {lab}", ylabel="dB per FFT bin re full scale")
            axs[row][col].grid(alpha=0.3, which="both"); axs[row][col].legend(loc="lower left", fontsize=8)
    axs[1][0].set_xlabel("Hz"); axs[1][1].set_xlabel("Hz")
    fig.tight_layout(); fig.savefig(f"{out}/growl_chew_hiss.png"); plt.close(fig)
    print("plots ->", out)


if __name__ == "__main__":
    main()
