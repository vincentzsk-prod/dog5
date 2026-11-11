# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A2: the per-slot README (tables) from results.json.   python3 tests/voicing/b6b_report.py"""
import json
import os

import b6_report as R6
from b6b_29 import *


def rr(v, n=1):
    return "n/a" if v is None else f"{v:.{n}f}"


def main():
    R = json.load(open(os.path.join(OUT, "results.json")))
    orig = B.resolve(BASE, 29)
    keys = ["A", "B", "C", "D", "Dfinal", "Ebox", "Fmetal"]
    L = ["# 29 i scream, Batch 6A2 round 1 (rendered, not yet heard)", "",
         "Slot 29 was VALHALLA (a chordal wash: round 1 of Batch 6A was rejected). It is rebuilt as `i scream`, an ice-cream-van chime. A is the ORIGINAL VALHALLA values level-matched, a reference and not a candidate; B, C, D are the candidates; Dfinal is the APPROVED version (variant D with CHEW 0, re-measured; it has not been heard); Ebox and Fmetal are calibration renders of the OSC 2 interval (on C). Level phrase: the note-on region of the chime melody (aj, 27 notes 580 ms apart, gate 250 ms); peak limit -4 dBFS over every audition phrase (the three-note chord is the limiting one).", ""]
    L += ["| var | tag | VOLUME | level aj | level chord (an) | level run (ao) | peak | (b) stabs | CPU | what |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]; c = m.get("cost")
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {m['level']:.2f} | {m['level_chord']:.1f} | {m['level_run']:.1f} | {m['peak_all']:.1f} | {m['b']:.1f} | {('%.0f' % c['total']) if c else 'n/a'} | {m['desc']} |")
    L += ["", "**Every change over the original VALHALLA values (percent = of the parameter's range):**", ""]
    for k in keys[1:]:
        L.append(f"* **{k} {R[k]['tag']}:** " + R6.changes(orig, R[k]["params"]) + f"; VOLUME {orig['VOLUME']} -> {R[k]['params']['VOLUME']}")
    L += ["", "## Decay of the actual render (C#6 and C#5 held 3 s; ms after the strike's peak to fall 6 / 12 / 20 / 30 / 40 dB; 4 ms power envelope; the voice alone = no tape, echo or spring; the van recording read 19 / 33 / 70 ms for 6 / 12 / 20 dB, one hit, very rough)", "",
          "| var | AMP DECAY nominal ms | FILTER DECAY nominal ms | voice C#6 | voice C#5 | whole patch C#6 | whole patch C#5 |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]; f = lambda d: " / ".join("-" if d[q] is None else f"{d[q]:.0f}" for q in ("6", "12", "20", "30", "40"))
        L.append(f"| {k} | {m['env_ms']['amp_decay']:.0f} | {m['env_ms']['filter_decay']:.0f} | {f(m['decay']['voice']['85'])} | {f(m['decay']['voice']['73'])} | {f(m['decay']['full']['85'])} | {f(m['decay']['full']['73'])} |")
    L += ["", "## Tape and shimmer (a ONE-VOICE probe: a held saw with a sustained envelope, the filter open, CHEW and the LFO as the patch has them; fundamental tracked in 25 ms hops, cents)", "",
          "| var | CHEW | wobble s.d. as built | 5-95 % range | strongest rate Hz | s.d. with CHEW 0 (LFO only) | tremolo depth dB / rate Hz (probe) |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]; w, w0 = m["wobble"]["as_built"], m["wobble"]["chew0"]
        L.append(f"| {k} | {m['params']['CHEW']} | {w['sd']:.2f} | {w['p5']:.1f} .. {w['p95']:.1f} | {w['rate']:.2f} | {w0['sd']:.2f} | {m['tremolo'][0]:.2f} / {m['tremolo'][1]:.2f} |")
    L += ["", "## The front edge (centroid over the first 20 ms from the audible onset, Hz; whole patch with the echo and spring off; CHEW as built against CHEW 0; onset = ms from the note-on to the first sample above -50 dB)", "",
          "| var | C#6 CHEW | C#6 CHEW 0 | change | C#5 CHEW | C#5 CHEW 0 | change | onset (ms) CHEW / 0 |", "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        f = R[k]["front"]
        L.append(f"| {k} | {f['85']['chew']['cent']:.0f} | {f['85']['chew0']['cent']:.0f} | {f['85']['chew']['cent'] - f['85']['chew0']['cent']:+.0f} | {f['73']['chew']['cent']:.0f} | {f['73']['chew0']['cent']:.0f} | {f['73']['chew']['cent'] - f['73']['chew0']['cent']:+.0f} | {f['85']['chew']['onset_ms']:.1f} / {f['85']['chew0']['onset_ms']:.1f} |")
    L += ["", "## The speaker band (the filter read with white noise, settled, 1/6 octave; and the melody's note-on region through the whole patch)", "",
          "| var | honk peak Hz | -3 dB width Hz (from-to) | noise: under 400 Hz % | noise: above 4 kHz % | noise centroid Hz | melody: under 400 % | melody: above 4 kHz % | melody centroid Hz |", "|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        s, b = R[k]["speaker"], R[k]["melody_band"]
        L.append(f"| {k} | {s['peak_hz']:.0f} | {s['w3_hz']:.0f} ({s['w3_lo']:.0f}-{s['w3_hi']:.0f}) | {s['under400']:.1f} | {s['over4k']:.1f} | {s['cent']:.0f} | {b['under400']:.2f} | {b['over4k']:.2f} | {b['cent']:.0f} |")
    L += ["", "## Partials of the first 100 ms (Hz, dB re the strongest, ratio to the played note; the voice alone, 'heard' = through the filter as built, 'raw' = the filter open and DRIVE 0; peaks under -45 dB left out)", ""]
    for k in keys:
        for n, nm in (("85", "C#6 1109 Hz"), ("73", "C#5 554 Hz")):
            for t in ("heard", "raw"):
                pr = R[k]["partials"][n][t]
                inh = [f for f, d, r, dist in pr if dist > 0.1]
                L.append(f"* {k} {nm} {t}: " + ", ".join(f"{f:.0f} ({d:+.0f} dB, x{r:.2f})" for f, d, r, dist in pr) + f"; off the integer ratios by more than 0.1: {len(inh)}")
    L += ["", "## Space (C#6 held 400 ms: the echo and spring's own return against the dry note in the windows after the strike; dry level in dB; the echo is 65 ms)", "",
          "| var | 0-20 ms: dry / return / re dry | 20-100 ms | 100-250 ms | 250-500 ms re dry | 500-1000 ms re dry |", "|---|---|---|---|---|---|"]
    for k in keys:
        s = R[k]["space"]; sl = R[k]["space_late"]
        L.append(f"| {k} | " + " | ".join(f"{x['dry_db']:.1f} / {x['fx_db']:.1f} / {x['re_dry_db']:+.1f}" for x in s) + f" | {sl[0]['re_dry_db']:+.1f} | {sl[1]['re_dry_db']:+.1f} |")
    L += ["", "## Register (one note each, 600 ms, whole patch: RMS 0-300 ms, centroid 0-100 ms and 100-400 ms, peak)", "", "| var | A4 level / centroid / ring centroid | C#6 | A6 |", "|---|---|---|---|"]
    for k in keys:
        g = R[k]["register"]
        L.append(f"| {k} | " + " | ".join(f"{g[n]['rms']:.1f} dB / {g[n]['cent']:.0f} / {g[n]['cent_ring']:.0f} Hz" for n in ("69", "85", "93")) + " |")
    L += ["", "## The voice pool (POLY 4 / 5 / 6 against POLY 8, VINTAGE 0 in all; levels of what rings, dB re POLY 8: negative = a ring was cut)", "", "| var | melody slot tail, mean / worst note | fast run tail 1.4-2.4 s | chord tail |", "|---|---|---|---|"]
    for k in ("B", "C", "D"):
        for nn in ("4", "5", "6"):
            q = R[k]["pool"][nn]
            L.append(f"| {k} POLY {nn} | {q['melody_mean']:+.1f} / {q['melody_worst']:+.1f} | {q['run_tail']:+.1f} | {q['chord_tail']:+.1f} |")
    L += ["", "## Crust and cost (on C: the melody, dry of nothing; crest = peak over RMS of the note-on region, dB; level at the same VOLUME; CPU = worst case idle + load)", "", "| setting | crest | level | peak | CPU |", "|---|---|---|---|---|"]
    for x in R["crust"]:
        L.append(f"| {x['name']} | {x['crest']:.1f} | {x['level']:.1f} | {x['peak']:.1f} | {x['cost']:.0f} |")
    L += ["", "## CPU levers on C (worst case, host instr/sample)", ""] + [f"* {k}: {v}" for k, v in R["levers"].items()]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
