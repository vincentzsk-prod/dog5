#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The voicing kit: render a factory patch (or a variant of it) on the audition phrases and measure it.

Everything runs on the host build (tests/host.c runs the firmware's own integer code; numpy only for the numbers).
Documented in dog5-docs/voicing/README.md.

  from voicekit import *
  exe = build_host()                                  # build/voicing/obervave (the working tree's firmware)
  wav, log = render(exe, "b_stabs", program=2)        # factory slot 3 as it stands in the tree
  wav, log = render(exe, "b_stabs", params={"VINTAGE": 100, ...})   # INIT + every parameter given (a variant)
  m = level_metrics(wav, "b_stabs")                   # the loudness reference's numbers
  python3 tests/voicing/voicekit.py bank              # RMS / peak of all 32 factory slots on phrase (b)

A variant is a full parameter dict (names as in obv_params.h without the P_ prefix; see PARAM_IDS): the kit selects
INIT (program 33, all defaults) and sets every byte given 10 ms later, so a variant never depends on what the tree's
slot currently holds."""
import os
import re
import subprocess
import sys
import wave
import numpy as np

FS = 44100
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUILD = os.path.join(ROOT, "build", "voicing")
PHRASES = os.path.join(ROOT, "tests", "voicing", "phrases")
T_SELECT = 2600                                 # ms: the program select (the phrases start at 3000)
T_PARAMS = T_SELECT + 10                        # ms: the parameters, after the program change has loaded INIT (the MIDI queue
                                                # is read by the main loop: a "param" in the same ms would be overwritten)
T_CUT = 2.9                                     # s: the WAVs start here (100 ms before the first note)
INIT_PROGRAM = 32                               # program change data byte: slot 33 = INIT, all defaults
PHRASE_FILES = {"a_riff": "a_riff.txt", "b_stabs": "b_stabs.txt", "c_held": "c_held.txt", "x_stress": "x_stress.txt",
                "d_lead": "d_lead.txt", "e_lowuni": "e_lowuni.txt", "f_slow": "f_slow.txt", "f2_slowmid": "f2_slowmid.txt", "g_skank": "g_skank.txt",
                "h_surf": "h_surf.txt", "x_register": "x_register.txt"}
AUDITION = ("a_riff", "b_stabs", "c_held")      # the three phrases every variant is rendered on (x_stress is CPU only)


def param_ids(src=None):
    """P_* name -> byte, from the enum at the top of obv_params.h (src: that file's text; default the tree's)"""
    txt = src if src is not None else open(os.path.join(ROOT, "firmware", "src", "obv_params.h")).read()
    body = txt[txt.index("enum {"):txt.index("NPARAM")]
    names = re.findall(r"\bP_([A-Z0-9_]+)", body)
    return {n: i for i, n in enumerate(names)}


PARAM_IDS = param_ids()


def build_host(src_dir=ROOT, out=None, extra=()):
    """compile the host app from src_dir's firmware (the tree, or an exported older revision for A/B proofs)"""
    out = out or os.path.join(BUILD, "obervave")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["cc", "-O2", "-Wall", "-Wno-unused-function", "-DOBV_HOST", '-DAPP_VER="dev"', *extra,
                    "-I" + os.path.join(src_dir, "firmware", "src"), "-I" + os.path.join(src_dir, "firmware", "gen"),
                    "-I" + os.path.join(ROOT, "tests"), "-o", out, os.path.join(src_dir, "firmware", "src", "obervave.c")],
                   cwd=src_dir, check=True)
    return out


def phrase_text(phrase):
    with open(os.path.join(PHRASES, PHRASE_FILES[phrase])) as f:
        return f.read()


def compose(phrase, program=None, params=None, extra=(), notes=True):
    """the host script: program select (+ parameters over INIT), extra lines (e.g. vlog), then the phrase"""
    lines = []
    if params is None:
        lines.append(f"{T_SELECT} midi 0xC0 {program} 0")
    else:
        lines.append(f"{T_SELECT} midi 0xC0 {INIT_PROGRAM} 0")
        for k, v in params.items():
            lines.append(f"{T_PARAMS} param {PARAM_IDS[k]} {v}")
    body = [l for l in phrase_text(phrase).splitlines() if l.strip()]
    ev = [l for l in body if not l.startswith("#")]
    if not notes:
        ev = [l for l in ev if " midi " not in l]
    ev += list(extra)
    ev.sort(key=lambda l: int(l.split()[0]) if not l.endswith(" end") else 10 ** 9)
    return "\n".join(lines + ev) + "\n"


def read_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64)


def write_wav(path, a):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(np.clip(np.round(a), -32767, 32767).astype(np.int16).tobytes())


def render(exe, phrase, program=None, params=None, extra=(), tag=None):
    """run the host app on a composed script; returns (stereo float array from t=0, the app's stdout)"""
    os.makedirs(BUILD, exist_ok=True)
    tag = tag or f"{phrase}_{os.getpid()}"
    sp = os.path.join(BUILD, tag + ".txt")
    with open(sp, "w") as f:
        f.write(compose(phrase, program, params, extra))
    r = subprocess.run([exe, os.path.join(BUILD, tag), sp], cwd=ROOT, check=True, capture_output=True, text=True,
                       errors="replace")
    for p in os.listdir(BUILD):
        if p.endswith(".ppm"):
            os.unlink(os.path.join(BUILD, p))
    return read_wav(os.path.join(BUILD, tag + ".wav")), r.stdout


def notes_of(phrase):
    """[(note, on_ms, off_ms)] from the phrase file"""
    on, out = {}, []
    for l in phrase_text(phrase).splitlines():
        m = re.match(r"(\d+) midi 0x(90|80) (\d+) (\d+)", l)
        if not m:
            continue
        t, st, n, v = int(m[1]), m[2], int(m[3]), int(m[4])
        if st == "90" and v:
            on.setdefault(n, []).append(t)
        else:
            out.append((n, on[n].pop(0), t))
    return sorted(out, key=lambda x: x[1])


def gate_mask(phrase, n):
    """boolean per sample: inside a note-on .. note-off interval of the phrase (the 'note-on region')"""
    m = np.zeros(n, bool)
    for _, a, b in notes_of(phrase):
        m[int(a * FS / 1000):int(b * FS / 1000)] = True
    return m


# ---- loudness -----------------------------------------------------------------------------------------------------
def k_weight(x):
    """ITU-R BS.1770 K-weighting (shelf + 38 Hz high-pass) for 44.1 kHz, applied as a frequency response (informational)"""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / FS)
    w = 2 * np.pi * f / FS
    z1, z2 = np.exp(-1j * w), np.exp(-2j * w)

    def resp(b, a):
        return (b[0] + b[1] * z1 + b[2] * z2) / (a[0] + a[1] * z1 + a[2] * z2)

    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = np.tan(np.pi * f0 / FS); Vh = 10 ** (G / 20); Vb = Vh ** 0.499666774155; a0 = 1 + K / Q + K * K
    h1 = resp([(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0],
              [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0])
    f0, Q = 38.13547087602444, 0.5003270373238773
    K = np.tan(np.pi * f0 / FS); a0 = 1 + K / Q + K * K
    h2 = resp([1, -2, 1], [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0])
    return np.fft.irfft(np.fft.rfft(x) * h1 * h2, n)


def level_metrics(a, phrase):
    """THE LOUDNESS REFERENCE'S NUMBERS.  a: the stereo render.  RMS dBFS over the note-on region (both channels, one
    power average, full scale = 32767), peak dBFS over the whole render, and the same RMS K-weighted (informational)."""
    m = gate_mask(phrase, len(a))
    p = (a[m] ** 2).mean()                      # (mean over samples and both channels)
    rms = 10 * np.log10(p / 32767 ** 2)
    pk = 20 * np.log10(np.abs(a).max() / 32767)
    k = np.stack([k_weight(a[:, 0]), k_weight(a[:, 1])], 1)
    rk = 10 * np.log10((k[m] ** 2).mean() / 32767 ** 2)
    return {"rms": rms, "peak": pk, "rms_k": rk}


# ---- tone ---------------------------------------------------------------------------------------------------------
def tone_metrics(a, phrase, nfft=2048):
    """spectral centroid (Hz; |X|-weighted per frame, frames weighted by their energy, the note-on region only, mono
    sum) and the share of the energy below 150 Hz (the 'weight')"""
    x = a.mean(1)
    m = gate_mask(phrase, len(x))
    win = np.hanning(nfft)
    num = den = lo = tot = 0.0
    f = np.fft.rfftfreq(nfft, 1 / FS)
    for s in range(0, len(x) - nfft, nfft // 2):
        if not m[s:s + nfft].all():
            continue
        X = np.abs(np.fft.rfft(x[s:s + nfft] * win))
        e = (X ** 2).sum()
        if e <= 0:
            continue
        num += e * (f * X).sum() / X.sum(); den += e
        lo += (X[f < 150] ** 2).sum(); tot += e
    return {"centroid": num / den if den else 0.0, "low_share": 100 * lo / tot if tot else 0.0}


# ---- envelope, release, sputter -----------------------------------------------------------------------------------
def env_db(a, hop_ms=2.0, win_ms=1000 / 110):
    """stereo power envelope in dBFS: the power over a sliding window of win_ms (default one period of A2, 9.09 ms, so a
    110 Hz saw's own cycle does not ripple the reading) every hop_ms (2 ms)"""
    h, w = int(FS * hop_ms / 1000), int(round(FS * win_ms / 1000))
    p = (a ** 2).mean(1)
    c = np.concatenate([[0.0], np.cumsum(p)])
    idx = np.arange(0, len(p) - w, h)
    pw = (c[idx + w] - c[idx]) / w
    return 10 * np.log10(np.maximum(pw, 1e-12) / 32767 ** 2), hop_ms / 1000


def release_metrics(a, off_ms, hop_ms=2.0, pre_ms=150, win_ms=900):
    """release and sputter of the note let go at off_ms.  Level before = RMS over the 150 ms before the release.  Times
    in ms after note-off: first and last time the envelope is above (before - 20 / 40 / 60 dB); SPAN = last - first
    crossing of -40 dB (a smooth tail has span 0, a sputtering one is open and shut inside it); RE-RISES = how often the
    envelope climbs 6 dB or more out of a dip inside the tail (a smooth fall has none); CLIMB = the total upward travel
    (dB) of the envelope along the tail down to -50 dB, the one-number sputter index (a smooth tail: ~0)"""
    e, dt = env_db(a, hop_ms)
    i0 = int(off_ms / hop_ms)
    pre = 10 * np.log10(np.mean(10 ** (e[i0 - int(pre_ms / hop_ms):i0] / 10)))
    tail = e[i0:i0 + int(win_ms / hop_ms)]
    out = {"pre_db": pre}
    for d in (20, 40, 60):
        above = np.nonzero(tail > pre - d)[0]
        out[f"first{d}"] = None
        out[f"last{d}"] = (above.max() * hop_ms if len(above) else 0.0)
        below = np.nonzero(tail <= pre - d)[0]
        out[f"first{d}"] = below.min() * hop_ms if len(below) else None
    out["span40"] = (out["last40"] - out["first40"]) if out["first40"] is not None else 0.0
    last = int(out["last60"] / hop_ms) + 1
    seg = tail[:max(last, 2)]
    rises, mn, mx, rising = 0, seg[0], seg[0], False
    for v in seg[1:]:                           # 6 dB hysteresis state machine
        if rising:
            if v > mx: mx = v
            elif mx - v >= 6: rising, mn = False, v
        else:
            if v < mn: mn = v
            elif v - mn >= 6: rising, mx, rises = True, v, rises + 1
    out["rerises"] = rises
    live = tail[:max(int(np.nonzero(tail > pre - 50)[0].max()) + 1, 2)] if (tail > pre - 50).any() else tail[:2]
    out["climb_db"] = float(np.maximum(np.diff(live), 0).sum())   # total upward travel of the tail above -50 dB: 0 = smooth
    return out


def body_flutter(a, t0_ms, t1_ms, hop_ms=10.0):
    """level flicker of a held body: the s.d. of the 10 ms RMS in dB over [t0, t1] after the settling (the amp LFO's work)"""
    e, _ = env_db(a, hop_ms, 2 * 1000 / 110)
    seg = e[int(t0_ms / hop_ms):int(t1_ms / hop_ms)]
    return float(seg.std()), float(seg.max() - seg.min())


# ---- the pitch: detune beating (audio) ----------------------------------------------------------------------------
def beat_metrics(a, f0, t0_ms, t1_ms, win_s=1.0, hop_s=0.25):
    """the beat of the pair of detuned voices, read from the mono sum around the fundamental (f0 +-15 %): the envelope of
    that band (analytic signal) is spectrally analysed over 1 s windows, its strongest component 0.3 .. 12 Hz is the
    beat rate; depth = peak-to-peak of the band's envelope in dB.  Returns the mean / min / max rate over the windows
    and the mean depth"""
    x = a.mean(1)[int(t0_ms * FS / 1000):int(t1_ms * FS / 1000)]
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / FS)
    X[(f < f0 * 0.85) | (f > f0 * 1.15)] = 0
    A = np.zeros(n, complex)
    A[:len(X)] = X * 2                          # analytic signal: one-sided spectrum
    env = np.abs(np.fft.ifft(A))
    rates, depths = [], []
    w = int(win_s * FS)
    for s in range(0, n - w, int(hop_s * FS)):
        ev = env[s:s + w]
        ev = ev[int(0.05 * FS):-int(0.05 * FS)]
        E = np.abs(np.fft.rfft((ev - ev.mean()) * np.hanning(len(ev)), 1 << 18))
        fe = np.fft.rfftfreq(1 << 18, 1 / FS)
        sel = (fe >= 0.3) & (fe <= 12)
        rates.append(float(fe[sel][np.argmax(E[sel])]))
        sm = np.convolve(ev, np.ones(441) / 441, "valid")
        depths.append(float(20 * np.log10(sm.max() / max(sm.min(), 1e-9))))
    return {"rate_mean": float(np.mean(rates)), "rate_min": min(rates), "rate_max": max(rates),
            "depth_db": float(np.mean(depths))}


def vlog_parse(stdout):
    """the engine's own per-card vintage pitch ('vlog card N: mean .. cents sd .. range lo .. hi'): {card: (mean, sd, lo, hi)}"""
    return {int(c): (float(m), float(sd), float(lo), float(hi))
            for c, m, sd, lo, hi in re.findall(r"vlog card (\d+): mean ([-+\d.]+) cents  sd ([\d.]+)  range ([-+\d.]+) \.\. ([-+\d.]+)",
                                               stdout)}


def callgrind_exe(src_dir=ROOT):
    return build_host(src_dir, os.path.join(BUILD, "obervave-cg"), ("-DOBV_CALLGRIND",))


def callgrind_ips(cg_exe, phrase, program=None, params=None, tag="cg", notes=True):
    """total host instructions / frames collected for a script under callgrind (deterministic, a relative yardstick)"""
    sp = os.path.join(BUILD, "cg-" + tag + ".txt")
    with open(sp, "w") as f:
        f.write(compose(phrase, program, params, notes=notes))
    r = subprocess.run(["valgrind", "--tool=callgrind", "--collect-atstart=no", "--combine-dumps=yes",
                        f"--callgrind-out-file={BUILD}/cg-{tag}.out", cg_exe, os.path.join(BUILD, "cg-" + tag), sp],
                       cwd=ROOT, capture_output=True, text=True, errors="replace")
    txt = r.stdout + r.stderr
    return int(re.search(r"Collected : (\d+)", txt)[1]), int(re.search(r"callgrind frames (\d+)", txt)[1])


def cost(cg_exe, program=None, params=None, tag="cg"):
    """(avg host instr/sample over phrase (b) as played, instr/sample while the stress chord sounds: the stress script's
    instructions minus the same script's without its notes, over the 4.65 s the notes sound (3 s + 1.5 s + the tails))"""
    ir, fr = callgrind_ips(cg_exe, "b_stabs", program, params, tag + "b")
    on, _ = callgrind_ips(cg_exe, "x_stress", program, params, tag + "x")
    off, _ = callgrind_ips(cg_exe, "x_stress", program, params, tag + "y", notes=False)
    return ir / fr, (on - off) / (4.65 * FS)


def main():
    if sys.argv[1:2] == ["bank"]:               # RMS / peak of all 32 factory slots on phrase (b)
        exe = build_host()
        for slot in range(1, 33):
            a, _ = render(exe, "b_stabs", program=slot - 1, tag="bank")
            m = level_metrics(a, "b_stabs")
            print(f"{slot:02d}  rms {m['rms']:6.1f} dBFS  K-rms {m['rms_k']:6.1f}  peak {m['peak']:6.1f}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
