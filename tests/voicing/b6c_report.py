# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B: the per-slot READMEs (28, 32) from results.json.   python3 tests/voicing/b6c_report.py"""
import json
import os

import b6_report as R6
from b6c_28 import OUT as OUT28, BASE
from b6c_32 import OUT as OUT32
from lib6c import *


def f(v, n=1):
    return "n/a" if v is None else f"{v:.{n}f}"


def r28():
    R = json.load(open(os.path.join(OUT28, "results.json")))
    orig = B.resolve(BASE, 28)
    keys = ["A", "B", "C", "D", "Xopen", "Yrise"]
    L = ["# 28 Bell Tolls, Batch 6B round 1 (rendered, not yet heard)", "",
         "The old brief (an inharmonic FM chime against the hard-chop gate, 'the friction is the point') is retired; Vincent wants a full ringing bell with body, a clean base to be shaped live. A = the original array level-matched (a reference); B, C, D = the candidates (a ring of about 2 / 4 / 6 s to -40 dB); Xopen and Yrise are calibration renders of the crystal-tail try. Level phrase: the note-on region of the slow toll (ar); peak limit -4 dBFS over every audition phrase (the three-note chord limits).", "",
         "| var | tag | VOLUME | toll (ar) | chord (at) | run (au) | peak | stabs (b) | CPU | what |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]; c = m.get("cost")
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {m['level']:.2f} | {m['level_chord']:.1f} | {m['level_run']:.1f} | {m['peak_all']:.1f} | {m['b']:.1f} | {('%.0f' % c['total']) if c else 'n/a'} | {m['desc']} |")
    L += ["", "**Every change over the original array (percent = of the parameter's range):**", ""]
    for k in keys[1:]:
        L.append(f"* **{k} {R[k]['tag']}:** " + R6.changes(orig, R[k]["params"]) + f"; VOLUME {orig['VOLUME']} -> {R[k]['params']['VOLUME']}")
    L += ["", "## Ring (the whole patch, held 6 s; ms after the strike's peak to fall 6 / 12 / 20 / 30 / 40 dB; 40 ms power envelope)", "", "| var | A4 | A3 | key-up at 400 ms (A4): level 0.5 / 1 / 2 s later re the held note, dB; to -20 / -40 dB after the strike |", "|---|---|---|---|"]
    for k in keys:
        m = R[k]; fm = lambda d: " / ".join("-" if d[q] is None else f"{d[q]:.0f}" for q in ("6", "12", "20", "30", "40"))
        L.append(f"| {k} | {fm(m['ring']['A4'])} | {fm(m['ring']['A3'])} | {m['keyup']['500']:+.1f} / {m['keyup']['1000']:+.1f} / {m['keyup']['2000']:+.1f}; {f(m['keyup_t']['20'], 0)} / {f(m['keyup_t']['40'], 0)} |")
    L += ["", "## The partial ladder against a struck church bell (hum 0.5, prime 1, tierce 1.2, quint 1.5, nominal 2 x the prime). The patch's prime is an octave above the key: the KEY is the hum. dB re the strongest partial; ratio re the prime; '-' = no peak within 3 %", ""]
    L += ["| var, note, window | hum 0.5 | prime 1 | tierce 1.2 | quint 1.5 | nominal 2 |", "|---|---|---|---|---|---|"]
    for k in keys:
        for nm in ("A4", "A3"):
            for w in ("strike", "body"):
                c = R[k]["ladder"][nm][w]["classical"]
                L.append(f"| {k} {nm} {'0-300 ms' if w == 'strike' else '1-2 s'} | " + " | ".join("-" if c[q] is None else f"{c[q]['ratio']:.3f} ({c[q]['db']:+.0f} dB)" for q in ("0.5", "1.0", "1.2", "1.5", "2.0")) + " |")
    L += ["", "## The strike and the body (centroid Hz over 0-20 / 20-100 / 100-400 ms; energy shares %: under 150 Hz / 150-800 / 800-4k / above 4k over the strike 0-400 ms and the body 1-2 s)", "", "| var | note | centroid | strike shares | body shares |", "|---|---|---|---|---|"]
    for k in keys:
        for nm in ("A4", "A3"):
            c, s1, s2 = R[k]["cent"][nm], R[k]["shares"][nm]["strike_0_400"], R[k]["shares"][nm]["body_1_2s"]
            L.append(f"| {k} | {nm} | " + " / ".join(f"{c[q]:.0f}" for q in ("0-20", "20-100", "100-400")) + " | " + " / ".join(f"{s1[q]:.1f}" for q in ("<150", "150-800", "800-4k", ">4k")) + " | " + " / ".join(f"{s2[q]:.1f}" for q in ("<150", "150-800", "800-4k", ">4k")) + " |")
    L += ["", "## The tail (A4 and A3: level dB, centroid Hz and the share above 4 kHz % in windows after the strike; the crystal-tail question)", ""]
    for k in keys:
        for nm in ("A4", "A3"):
            L.append(f"* {k} {nm}: " + "; ".join(f"{x['w'][0]}-{x['w'][1]} ms: {x['rms']:.1f} dB, {x['cent']:.0f} Hz, {x['over4k']:.1f} %" for x in R[k]["tail"][nm]))
    L += ["", "## Dreamy (a one-voice probe: pitch wobble s.d. cents, 5-95 % range, strongest rate; level swing dB / rate)", "", "| var | wobble s.d. | range | rate Hz | tremolo depth dB / rate Hz |", "|---|---|---|---|---|"]
    for k in keys:
        w, t = R[k]["wobble"], R[k]["tremolo"]
        L.append(f"| {k} | {w['sd']:.2f} | {w['p5']:.1f} .. {w['p95']:.1f} | {w['rate']:.2f} | {t[0]:.2f} / {t[1]:.2f} |")
    L += ["", "## Space (A4 held 400 ms: the echo and spring's own return against the dry note, windows after the strike; dry / return dB, return re dry)", "", "| var | 0-20 ms | 20-100 | 100-250 | 250-1000 |", "|---|---|---|---|---|"]
    for k in keys:
        L.append(f"| {k} | " + " | ".join(f"{x['dry_db']:.1f} / {x['fx_db']:.1f} / {x['re_dry_db']:+.1f}" for x in R[k]["space"]) + " |")
    L += ["", "## Register (one note each, held 1.5 s: RMS 0-300 ms, centroid 0-100 ms and 300-1000 ms, peak, and the ring to -20 / -40 dB when held 6 s)", "", "| var | A2 | A3 | A4 | A5 | A6 |", "|---|---|---|---|---|---|"]
    for k in keys:
        g = R[k]["register"]
        L.append(f"| {k} | " + " | ".join(f"{g[n]['rms']:.1f} dB / {g[n]['cent']:.0f} / {g[n]['cent_ring']:.0f} Hz / {g[n]['peak']:.1f} / {f(g[n]['t20'], 0)} / {f(g[n]['t40'], 0)}" for n in ("45", "57", "69", "81", "93")) + " |")
    L += ["", "## The voice pool (POLY 4 / 5 / 6 against POLY 8, VINTAGE 0 in all; levels of what rings, dB re POLY 8: negative = a ring was cut)", "", "| var | toll slot tail mean / worst | fast run tail | chord tail |", "|---|---|---|---|"]
    for k in keys:
        for nn in ("4", "5", "6"):
            q = R[k]["pool"][nn]
            L.append(f"| {k} POLY {nn} | {q['toll_mean']:+.1f} / {q['toll_worst']:+.1f} | {q['run_tail']:+.1f} | {q['chord_tail']:+.1f} |")
    L += ["", "## The live controls on the base (variant C, A3; one step each way: CUTOFF +-10, X-MOD +-20, ENV>O2 +-10 (= +-3.8 st at the envelope's top), OSC 2 FINE +-8 (= +-6.3 cents), echo MIX +-15, DRAIN +-15; CHEW 0 -> 45 (no way down)). Classical ratios of the strike re the key as 1 / 2 / 2.4 / 3 / 4: hum / prime / tierce / quint / nominal", "",
          "| control | base | step | value | hum | prime | tierce | quint | nominal | centroid 0-100 ms | ring -20 / -40 ms | level 0-300 ms | off-harmonic partials above -25 dB |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in R["live"]:
        c = x["ladder"]
        L.append(f"| {x['control']} | {x['base']} | {x['step']:+d} | {x['value']} | " + " | ".join("-" if c[q] is None else f"{c[q]['ratio']:.3f} ({c[q]['db']:+.0f})" for q in ("0.5", "1.0", "1.2", "1.5", "2.0")) + f" | {x['cent']:.0f} | {f(x['t20'], 0)} / {f(x['t40'], 0)} | {x['rms']:.1f} | {x['inharmonic']} |")
    L += ["", "## CPU of the live add-ons (host instr/sample, worst case): " + "; ".join(f"{k} {v:.0f}" for k, v in R["addons"].items()) + " (soft limit 2400)", "",
          "## Against 29 i scream (main's array, the same measures)", "", "| | ring to -6 / -12 / -20 / -40 ms | centroid 0-20 / 20-100 / 100-400 Hz | shares under 150 / 150-800 / 800-4k / over 4k (strike) | strongest partials Hz (dB, ratio) |", "|---|---|---|---|---|"]
    for n, nm in (("69", "29 at A4"), ("85", "29 at C#6")):
        v = R["vs29"][n]
        L.append(f"| {nm} | " + " / ".join(f"{v['ring'][q]:.0f}" for q in ("6", "12", "20", "40")) + " | " + " / ".join(f"{v['cent'][q]:.0f}" for q in ("0-20", "20-100", "100-400")) + " | " + " / ".join(f"{v['shares']['strike_0_400'][q]:.1f}" for q in ("<150", "150-800", "800-4k", ">4k")) + " | " + ", ".join(f"{a:.0f} ({b:+.0f}, x{c:.2f})" for a, b, c, d in v["top"][:6]) + " |")
    for k in ("C",):
        m = R[k]
        L.append(f"| 28 {k} at A4 | " + " / ".join(f"{m['ring']['A4'][q]:.0f}" for q in ("6", "12", "20", "40")) + " | " + " / ".join(f"{m['cent']['A4'][q]:.0f}" for q in ("0-20", "20-100", "100-400")) + " | " + " / ".join(f"{m['shares']['A4']['strike_0_400'][q]:.1f}" for q in ("<150", "150-800", "800-4k", ">4k")) + " | see the ladder |")
    open(os.path.join(OUT28, "README.md"), "w").write("\n".join(L) + "\n")


def r32():
    R = json.load(open(os.path.join(OUT32, "results.json")))
    orig = B.resolve(BASE, 32)
    keys = ["A", "B", "C", "Craw"]
    L = ["# 32 Init bruv?, Batch 6B round 1 (rendered, not yet heard)", "",
         "A = the original array (it IS the engine defaults); B = the engine defaults with VOLUME on the reference (POLY 5, the default mode); C = the same in MONO; Craw = a calibration render of the brief's WORDS (one raw saw, filter fully open, flat envelopes): **the engine's defaults are not that** (below). Level phrase: the stabs (b); second phrase the riff (a). Peak limit -4 dBFS over b, a, the held note and the chord.", "",
         "| var | tag | VOLUME | stabs (b) | riff (a) | chord (A2 E3 A3, 8 s) | peak | CPU | what |", "|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]; c = m.get("cost")
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {m['level']:.2f} | {m['level_riff']:.1f} | {m['level_chord']:.1f} | {m['peak_all']:.1f} | {('%.0f' % c['total']) if c else 'n/a'} | {m['desc']} |")
    L += ["", "**Every change over the original array:** " + "; ".join(f"{k} {R6.changes(orig, R[k]['params'])}; VOLUME {orig['VOLUME']} -> {R[k]['params']['VOLUME']}" for k in keys[1:]), "",
          "**The engine's defaults (what slot 32 is):** POLY (POLY 5); OSC 1 a saw LEVEL 110; **OSC 2 ON** (a saw, LEVEL 100, SEMI 0, FINE 70 = +4.7 cents); LP24 **CUTOFF 80, RESO 20** (not open), ENV AMT 90 (bipolar, 64 = 0), KEY TRK 64, FILTER ENV A20 D70 S40 R60, AMP ENV A10 D70 S100 R60, LFO TRI RATE 70 with every depth 0 and PHASE FREE, VINTAGE 30, SPREAD 60, GLIDE 0, VOLUME 100, every effect 0 (GROWL, DLY MIX, DRAIN, CHEW), no arp. The original slot 32 array is `{X}` (empty: every parameter at its default): **no difference** between it and the default program; `PF_INIT` is also `FACT_INIT`, the INIT of slots 33-99.", ""]
    L += ["## Harmonics of one held note (dB re the first; deviation from the saw's 1/n law in brackets: a plain saw reads 0 everywhere)", ""]
    for k in keys:
        for n in ("C3", "C5"):
            h = R[k]["harm"][n]
            L.append(f"* {k} {n}: " + ", ".join(f"{i + 1}: {h['db'][i]:.1f} ({h['dev'][i]:+.1f})" for i in range(10)))
    L += ["", "## Bypass proof: the effect chain at 0 renders the same samples with every effect's other controls at extremes (echo time / feedback / tone / pingpong / fine, spring size / damp / pre-delay, tape wow / hiss / drops, GROWL bias / tone), B: " + ", ".join(f"{k} {'bit-identical' if v else 'DIFFERS'}" for k, v in R["bypass"].items()), "",
          "## The note-on (C3, the peak of the first 2 ms after the first sample against the note's own peak, dBFS)", ""]
    for k in keys:
        o = R[k]["onset"]
        L.append(f"* {k}: first 2 ms {o['first2ms_peak']:.1f}, the note {o['note_peak']:.1f} ({o['note_peak'] - o['first2ms_peak']:.1f} dB under the note: no click)")
    L += ["", "## CPU (host instr/sample, worst case) of the whole bank on the same yardstick (slot: cost), lightest first", "", ", ".join(f"{k}: {v:.0f}" for k, v in sorted(R["bank_cost"].items(), key=lambda kv: kv[1])[:10])]
    L += ["", "Strike centroid (C3 / C5, Hz): " + "; ".join(f"{k} {R[k]['cent']['C3']:.0f} / {R[k]['cent']['C5']:.0f}" for k in keys)]
    open(os.path.join(OUT32, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    r28(); r32()
