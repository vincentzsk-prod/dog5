# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B round 2: README.md of listen/voicing/batch-05b/23-crypt-dust/round2 from results.json + lose.json.  python3 tests/voicing/batch05b_r2_report.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch05b_r2 as Y
from lib5b import *

R = json.load(open(os.path.join(Y.OUT, "results.json"))); LS = json.load(open(os.path.join(Y.OUT, "lose.json")))
R1 = Y.R1
f = lambda x, n=1: "n/a" if x is None else f"{x:.{n}f}"
cpu = lambda m: f"{m['cost']['idle'] + m['cost']['load']:.0f}"
L = ["# 23 Crypt Dust: Batch 5B round 2 (rendered, not yet heard): the noise removed, a trace of dust kept", "",
     "From round 1's C (half tape) and D (tapeless): only NOISE (and, for C2 / C3, the tape HISS; D3's POLY) change. Trace = NOISE set so that the noise component (OSC 1 LEVEL 0 render) sits 25 dB under the pulse component (NOISE 0 render) of the whole chain, RMS over +4 .. +10 s of the held triad.", "",
     "| var | from | VOLUME before -> after | NOISE | HISS | POLY | level | K-RMS | peak | noise vs pulse dB | (b) stabs | CPU |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
src = {"C2": "C", "C3": "C", "D2": "D", "D3": "D2"}
for k in ("C2", "C3", "D2", "D3"):
    m = R[k]; p = m["params"]; s = R1[src[k]] if k != "D3" else R["D2"]
    L.append(f"| {k} | {src[k]} | {s['params']['VOLUME']} -> {p['VOLUME']} | {p['NOISE']} | {p['TP_HISS']} | {p['POLY_N']} | {m['level']:.2f} | {m['krms']:.2f} | {m['peak_all']:.2f} | {m['comp']['diff']:.1f} | {m['b']:.1f} | {cpu(m)} |")
L += ["", "Round 1 for comparison: C and D had NOISE 127 and measured the noise **6.0 / 5.8 dB under the pulse** (C: noise-only -24.6, pulse-only -18.6 dBFS; D: -24.9 / -19.1), so removing it to -25 dB lowers the total by only about 0.5 dB (at VOLUME 127: C -17.57 -> C2 -18.06, D -18.69 -> D2 -19.23) and VOLUME could not come down.", "",
      "## Parameter changes (everything else as in round 1)", "",
      "* **C2** (from C): NOISE 127 -> 43 (-66% of range; the knob is a square law: 43 against 127 is -18.8 dB), TP_HISS 64 -> 0 (off; -50% of range)",
      "* **C3** (from C): NOISE 127 -> 0 (-100%), TP_HISS 64 -> 0 (off)",
      "* **D2** (from D): NOISE 127 -> 43 (-66%; -18.8 dB), POLY 2 as before (HISS has no effect: CHEW is 0)",
      "* **D3** (from D2): POLY 2 -> 4 voices (+25% of the 8 voices); NOISE 43 as D2 (the noise reads -24.4 dB under the pulse with four voices)",
      "* VOLUME: C 123 -> C2 127, C3 127; D 127 -> D2 127, D3 120 (all re-trimmed; the three at 127 have no VOLUME headroom; peaks -5.5 / -5.4 / -4.7 / -4.0)", "",
      "## Which keys of A3 C#4 E4 sound, and the cost by POLY (D2, pulse only, fundamentals exposed; dB re the strongest)", "",
      "| POLY | A3 | C#4 | E4 | CPU worst (idle + load) |", "|---|---|---|---|---|"]
for n, v in R["_poly"].items():
    nn = v["notes"]; L.append(f"| {n} | {nn['A3']:.1f} | {nn['C#4']:.1f} | {nn['E4']:.1f} | {v['cpu']['worst']:.0f} (load {v['cpu']['load']:.0f}) |")
L += ["", "With POLY 2 the first key (A3) is stolen when the third arrives: C#4 and E4 sound. POLY 3, 4 and 5 sound all three (POLY 5 costs the same as 4 on the four-note stress chord).", "",
      "## Tone in windows (held triad, seconds after the note-on) and release", "", "| var | window | RMS | centroid | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |", "|---|---|---|---|---|---|---|---|---|"]
for k in ("C2", "C3", "D2", "D3"):
    for w, x in R[k]["windows"].items():
        s = x["shares"]; L.append(f"| {k} | {w} | {x['rms']:.1f} | {x['cent']:.0f} | {x['mud']:.2f} | {s['<60'] + s['60-150']:.0f} | {s['150-400']:.0f} | {s['400-1.2k']:.0f} | {s['1.2k+']:.1f} |")
L += ["", "## The pulse on the real patch, the tape, taps", "",
      "Wobble = the thin pulse's strongest harmonic (1100 Hz) tracked on a held A3 of the REAL patch (noise trace, echo, spring and tape in); `CHEW 0` row = the same patch without tape (VINTAGE and the slow filter LFO move the tracked partial too: the method floor). Dips = level dips over 6 dB under the running median (10 ms RMS), 7 s of A3 / the held triad. Floor = RMS in the 1 s windows 14 s and 15 s after the chord's note-on (17-18 s, 18-19 s), notes off.", "",
      "| var | pulse pitch s.d. cents (5-95 %) | rate Hz | CHEW 0 s.d. | dips A3 (count / deepest dB) | dips chord | floor 17-18 / 18-19 s | centroid 4-10 s | 1.2k+ share | 150 ms tap (dBFS, re held) | A4 tap | stabs (b) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for k in ("C2", "C3", "D2", "D3"):
    m = R[k]; w = m["wobble"]["as"]
    L.append(f"| {k} | {f(w['sd'])} ({f(w['p5'])} .. {f(w['p95'])}) | {f(w['rate'], 2)} | {f(m['wobble']['chew0']['sd'])} | {w['dips']['count']} / {w['dips']['deepest']:.1f} | {m['dips_chord']['count']} / {m['dips_chord']['deepest']:.1f} | {m['floor']['14']:.1f} / {m['floor']['15']:.1f} | {m['cent']:.0f} | {m['hf']:.1f} | {m['tap']['gate']:.1f} ({m['tap']['re_held']:+.1f}) | {m['tap']['a4_gate']:.1f} | {m['b']:.1f} |")
L += ["", "Hiss: with HISS 64 (round 1 C) the floor after the chord was -65.4 / -66.8 dBFS; with HISS 0 (C2, C3) it is -70.8 / -84.3 and -69.2 / -84.3, the same as D2 / D3 (-74.0 / -87.3, no tape) within the echo and spring tails. During the held chord HISS makes no difference to the noise-to-pulse figure (HISS 64 on C2: noise-only -43.2 either way): the hiss shows only in the quiet after the notes (it rests 2 s after silence).", "",
      f"Release: -20 / -40 / -60 dB after the note-off (ms): " + "; ".join(f"{k} {R[k]['hover']['t20']:.0f}/{R[k]['hover']['t40']:.0f}/{R[k]['hover']['t60']:.0f}" for k in ("C2", "C3", "D2", "D3")), "",
      "## What the patch loses when the noise goes (held triad 4-10 s, round 1 against round 2)", "",
      "| var | NOISE | centroid Hz | 1.2-4 kHz % | above 4 kHz % | spectral flatness 0.4-10 kHz dB | floor after chord |", "|---|---|---|---|---|---|---|"]
for k, lab in (("C(r1)", "C round 1"), ("C2", "C2"), ("C3", "C3"), ("D(r1)", "D round 1"), ("D2", "D2"), ("D3", "D3")):
    x = LS[k]; nz = {"C(r1)": 127, "D(r1)": 127, "C2": 43, "C3": 0, "D2": 43, "D3": 43}[k]
    L.append(f"| {lab} | {nz} | {x['cent']:.0f} | {x['s1_4']:.1f} | {x['s4k']:.1f} | {x['flat']:.1f} | {x['floor'][0]:.1f} / {x['floor'][1]:.1f} |")
open(os.path.join(Y.OUT, "README.md"), "w").write("\n".join(L) + "\n")
print("ok")
