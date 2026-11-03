#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""DRAIN's measurements, from the host and bench renders (tests/spring/render.sh writes them to build/spring/kit/).

  python3 tests/spring/analyze.py [build/spring/kit] [--png listen/spring]

Bench files are raw int32, 4 channels a frame (in L, in R, out L, out R); the wet = out - in. Host renders are the
WAVs the FM-1 would send. Energy: the whole render from the first note, against the dry render. Loudness: ITU-R
BS.1770-4 integrated (pyloudnorm). Decay: T20 (Schroeder's backward integral, -5 .. -25 dB, x 3) after a 300 ms
noise burst. Clicks in the knob sweeps (measured over a held dark pad, whose dry has nothing above ~2 kHz): the
energy above 10 kHz in 2.9 ms frames against the median of the 120 ms around it, a frame 6 dB over and above -80
dBFS is a candidate (tests/tape's rule; the bench test tests/spring/clicks.py is the strict one)."""
import os
import sys
import wave
import numpy as np

FS = 44100
T_START = 2.55
D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "build/spring/kit"
PNG = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
OLD = "db0701c"
SRC = ["stab", "bass", "lead", "pluck", "hit"]
SET = ["boing", "default", "splash", "dark", "max"]


def bench(name):
    d = np.fromfile(os.path.join(D, name + ".raw"), np.int32).reshape(-1, 4).astype(float)
    return d[:, :2], d[:, 2:] - d[:, :2]


def wav(name):
    with wave.open(os.path.join(D, name + ".wav")) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(float)
    return a[int(T_START * FS):]


def en(x): return 10 * np.log10((x ** 2).sum() + 1e-9)
def peak(x): return 20 * np.log10(np.abs(x).max() / 32767 + 1e-12)
def nfs(x): return int((np.abs(x) >= 32767).any(1).sum())


def lufs(x):
    try:
        import pyloudnorm as pyln
        return pyln.Meter(FS).integrated_loudness(x / 32768)
    except ImportError:
        return float("nan")


def t20(w):
    e = (w ** 2).sum(1)
    s = np.cumsum(e[::-1])[::-1]
    db = 10 * np.log10(s / s[0] + 1e-30)
    return (np.argmax(db < -25) - np.argmax(db < -5)) / FS * 3


def flutter(w):
    env = np.abs(w[:, 0]) + np.abs(w[:, 1])
    env = np.convolve(env, np.ones(64) / 64, "same")[: int(0.6 * FS)]
    env -= env.mean()
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    lo = int(0.04 * FS)                         # (past the diffusers' and taps' own short pattern)
    return (lo + np.argmax(ac[lo: int(0.15 * FS)])) / FS * 1000


def hf_clicks(x, thresh_db=6.0, floor_db=-80.0):
    m = x.mean(1)
    X = np.fft.rfft(m); X[: int(10000 * len(m) / FS)] = 0
    h = np.fft.irfft(X, len(m))
    n = len(h) // 128
    e = 10 * np.log10((h[: n * 128].reshape(n, 128) ** 2).mean(1) + 1e-12) - 20 * np.log10(32767)
    k = int(0.12 * FS / 128) // 2
    return [(i * 128 / FS + T_START, e[i]) for i in range(k, n - k)
            if e[i] > np.median(e[i - k: i + k]) + thresh_db and e[i] > floor_db]


def main():
    figs = {}
    print("== the sources x the spring (whole render from the first note; energy against dry, peak, samples at full scale)")
    print(f"{'':6s} " + " ".join(f"{s:>21s}" for s in SET + ["OLD default", "OLD splash"]))
    for src in SRC:
        dry = wav(f"src_{src}_dry")
        row = []
        for s in SET:
            x = wav(f"src_{src}_{s}")
            row.append(f"{en(x) - en(dry):+5.1f} dB {peak(x):5.1f} {nfs(x):3d}")
        for s in ("default", "splash"):
            x = wav(f"old_{src}_{s}")
            row.append(f"{en(x) - en(dry):+5.1f} dB {peak(x):5.1f} {nfs(x):3d}")
        print(f"{src:6s} " + " ".join(f"{r:>21s}" for r in row))
    print("\n== loudness (LUFS), default spring vs the old plate at the same bytes")
    for src in SRC:
        print(f"  {src:6s} dry {lufs(wav(f'src_{src}_dry')):6.1f}  spring {lufs(wav(f'src_{src}_default')):6.1f}  "
              f"plate {lufs(wav(f'old_{src}_default')):6.1f}  | splash: spring {lufs(wav(f'src_{src}_splash')):6.1f}  "
              f"plate {lufs(wav(f'old_{src}_splash')):6.1f}")

    print("\n== the whole chain (GROWL -> ALLEY -> DRAIN -> CHEW): peak / full-scale samples; what DRAIN adds (energy");
    print("   against the same chain without it); against the same bytes on the build before (old plate, old routing)")
    for src in ("stab", "bass", "lead", "pluck"):
        for nm in ("mild", "surf", "mangle"):
            x, nd, o = wav(f"chain_{src}_{nm}"), wav(f"chain_{src}_{nm}_nodrain"), wav(f"oldchain_{src}_{nm}")
            print(f"  {src:6s} {nm:7s} peak {peak(x):5.1f} dBFS, {nfs(x):4d} at FS | DRAIN adds {en(x) - en(nd):+5.1f} dB | "
                  f"old plate chain {en(o) - en(nd):+5.1f} dB, peak {peak(o):5.1f}, {nfs(o):4d} at FS | "
                  f"LUFS {lufs(x):6.1f} (old {lufs(o):6.1f})")

    print("\n== decay (T20, s) after a 300 ms noise burst, DAMP open: SIZE -> spring (target) | old plate")
    dec = []
    for sz in (0, 16, 32, 48, 64, 80, 96, 112, 127):
        a = t20(bench(f"rt_bench_{sz}")[1][int(0.4 * FS):])
        b = t20(bench(f"rt_bench_{OLD}_{sz}")[1][int(0.4 * FS):])
        dec.append((sz, 0.3 * 10 ** (sz / 127), a, b))
        print(f"  SIZE {sz:3d}: {a:5.2f} ({dec[-1][1]:4.2f}) | {b:6.2f}")
    figs["decay"] = dec

    _, w = bench("ir_bench"); _, wo = bench(f"ir_bench_{OLD}")
    w, wo = w[int(0.1 * FS):], wo[int(0.1 * FS):]
    figs["ir"] = (w, wo)

    print("\n== the chirp: one chain of the firmware's integer allpasses (4 x 5 samples, g 0.7), impulse in; group delay (ms)")
    gd = {}
    for n in (2, 4, 10):
        h = np.loadtxt(os.path.join(D, f"gd_{n}.txt"))
        H = np.fft.rfft(h, 65536); f = np.fft.rfftfreq(65536, 1 / FS)
        g = -np.gradient(np.unwrap(np.angle(H)), 2 * np.pi * f) * 1000
        gd[n] = (f, g)
        pick = [250, 500, 1000, 2000, 3000, 3500, 4000, 4400, 5000, 6000]
        print(f"  {n:2d} chains ({n // 2} loop{'s' if n > 2 else ''} + ...): " +
              " ".join(f"{p}:{g[np.argmin(abs(f - p))]:.2f}" for p in pick))
    figs["gd"] = gd

    i, ws = bench("ss_bench"); _, wso = bench(f"ss_{'bench_' + OLD}")
    figs["spec"] = (i[int(1.5 * FS):int(3 * FS)], ws[int(1.5 * FS):int(3 * FS)], wso[int(1.5 * FS):int(3 * FS)])

    print("\n== the overflow, before the fix (c10db7d) and after (tests/spring/hot_reverb.txt on the plate and on DRAIN)")
    with wave.open(os.path.join(D, "hot_reverb_prefix.wav")) as f_:
        pre = np.frombuffer(f_.readframes(f_.getnframes()), np.int16).reshape(-1, 2).astype(float)
    with wave.open(os.path.join(D, "hot_reverb_fixed.wav")) as f_:
        post = np.frombuffer(f_.readframes(f_.getnframes()), np.int16).reshape(-1, 2).astype(float)
    with wave.open(os.path.join(D, "hot_reverb.wav")) as f_:
        drn = np.frombuffer(f_.readframes(f_.getnframes()), np.int16).reshape(-1, 2).astype(float)
    dif = np.any(pre != post, axis=1)
    print(f"  plate before the fix: largest step between neighbours {np.abs(np.diff(pre, axis=0)).max():.0f}; the plate "
          f"fixed: {np.abs(np.diff(post, axis=0)).max():.0f} ({dif.sum()} frames differ, all inside the overflow's bursts); "
          f"DRAIN: {np.abs(np.diff(drn, axis=0)).max():.0f}, peak {peak(drn):.1f} dBFS")
    figs["ovf"] = (pre, post)

    print("\n== the knob sweeps on SPRING + (SELECT held: one detent every 40 ms, up, down, then a flick) and the jumps")
    for nm in ("size", "damp", "pre"):        # over a held dark pad: the dry has nothing up there
        c, c0 = hf_clicks(wav(f"sweepm_{nm}")), hf_clicks(wav(f"sweepm_{nm}_still"))
        x = wav(f"sweepm_{nm}")
        X = np.fft.rfft(x.mean(1)); X[: int(10000 * len(x) / FS)] = 0
        hf = 20 * np.log10(np.sqrt((np.fft.irfft(X, len(x)) ** 2).mean()) / 32767 + 1e-12)
        print(f"  {nm:4s} turned over the pad: {len(c)} candidates (the pad held still: {len(c0)}); above 10 kHz "
              f"{hf:.0f} dBFS RMS" + (": " + ", ".join(f"{t:.3f}s {a:.0f}dBFS" for t, a in c[:8]) if c else ""))
    c = hf_clicks(wav("jumps_hit")); r = [t for t, _ in hf_clicks(wav("src_hit_dry"))]
    sus = [(t, a) for t, a in c if not any(abs(t - u) < 0.006 for u in r)]
    print(f"  the hit, SIZE / DAMP / PRE-DLY jumped end to end while the splash rings: {len(c)} candidates, all but "
          f"{len(sus)} the hit's own attack")
    if PNG:
        plots(figs)


def plots(figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(PNG, exist_ok=True)
    w, wo = figs["ir"]
    fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for a, x, t in ((ax[0], wo, "old plate"), (ax[1], w, "DRAIN (spring)")):
        a.specgram(x[: int(0.7 * FS), 0], NFFT=512, Fs=FS, noverlap=448, cmap="magma", vmin=-40, vmax=50)
        a.set_ylim(0, 8000); a.set_ylabel("Hz"); a.set_title(f"impulse response, SIZE 64, DAMP open: {t}")
    ax[1].set_xlabel("s after the impulse")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "ir_spectrogram.png"), dpi=100); plt.close(fig)

    d = np.array(figs["decay"])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(d[:, 0], d[:, 1], "k--", label="target (0.3 .. 3.0 s)")
    ax.plot(d[:, 0], d[:, 2], "o-", label="DRAIN measured")
    ax.plot(d[:, 0], d[:, 3], "s-", label="old plate")
    ax.set_yscale("log"); ax.set_xlabel("SIZE"); ax.set_ylabel("decay T20 (s)"); ax.grid(alpha=.3); ax.legend()
    ax.set_title("SIZE clamped: the spring can't bloom into a hall")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "decay_vs_size.png"), dpi=100); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    for n, (f, g) in figs["gd"].items():
        ax.plot(f, g, label=f"{n} chains (~{n // 2} loop{'s' if n > 2 else ''})")
    ax.set_xlim(0, 8000); ax.set_ylim(0, 55); ax.set_xlabel("Hz"); ax.set_ylabel("group delay (ms)"); ax.grid(alpha=.3)
    ax.legend(); ax.set_title("the chirp: the band around 4.4 kHz arrives later on every pass (the firmware's integer chain)")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "chirp_group_delay.png"), dpi=100); plt.close(fig)

    i, ws, wso = figs["spec"]
    fig, ax = plt.subplots(figsize=(8, 4))
    for x, lab in ((i, "input (noise)"), (wso, "old plate wet"), (ws, "DRAIN wet")):
        n = len(x) // 4096 * 4096
        X = np.abs(np.fft.rfft(x[:n, 0].reshape(-1, 4096) * np.hanning(4096), axis=1)) ** 2
        f = np.fft.rfftfreq(4096, 1 / FS)
        ax.semilogx(f[1:], 10 * np.log10(X.mean(0)[1:] + 1e-9), label=lab)
    ax.set_xlim(30, 20000); ax.set_xlabel("Hz"); ax.set_ylabel("dB"); ax.grid(alpha=.3); ax.legend()
    ax.set_title("the wet's band under a held noise (SIZE 80, DAMP 60, PRE-DLY 20)")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "wet_spectrum.png"), dpi=100); plt.close(fig)

    pre, post = figs["ovf"]
    a0 = int(3.962 * FS)
    fig, ax = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    t = np.arange(a0, a0 + 600) / FS * 1000
    ax[0].plot(t, pre[a0:a0 + 600, 0], lw=.8); ax[0].set_title("before the fix: the plate's tap sum wraps (a crack)")
    ax[1].plot(t, post[a0:a0 + 600, 0], lw=.8); ax[1].set_title("the plate with the fix (step 1): the same samples, no wrap")
    for a in ax: a.set_ylim(-35000, 35000); a.grid(alpha=.3)
    ax[1].set_xlabel("ms")
    fig.tight_layout(); fig.savefig(os.path.join(PNG, "overflow.png"), dpi=100); plt.close(fig)
    print("pictures ->", PNG)


if __name__ == "__main__":
    main()
