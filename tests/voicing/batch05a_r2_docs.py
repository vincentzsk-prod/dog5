#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The Batch 5A round 2 log of the new slot 19 (dog5-docs/voicing/19-micro-mist.md) from listen/voicing/batch-05a/19-micro-mist/results.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch05a_report as R1

R = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-05a", "19-micro-mist", "results.json")))
init = B.resolve(os.path.join(K.BUILD, "base"), 32)
m = R["B"]
L = ['# Voicing log: 19 "Micro-mist" (FACTORY[18], Batch 5A round 2, Chapter III)', "",
     "## ROUND 1 of the new patch: rendered, not yet heard. Take B is committed provisionally (own array `PF_MICRO_MIST`); A, C, D render-only.", "",
     "Slot 19 was Blackwater until 6 Nov 2026; Vincent dropped it completely (\"I don't see myself ever using this\") and the slot was rebuilt from scratch. The old log is `19-blackwater.md` (superseded). There is no original to compare with: A-D are four fresh takes.", "",
     "**Brief:** neon pixels floating in the ether: a soft, glassy chord in the mid-to-upper register that scatters into a hovering, shimmering mist; after the key-up the echo and spring keep it hanging for a few seconds. Chords work (POLY).", "",
     "**It is NOT a granular engine.** What this engine does instead: a slightly detuned octave-up pair (the shimmer), one shared LFO (smooth random or sample-and-hold) on pitch, filter and a little level, per-voice phase offsets (PHASE SPREAD) so the voices flicker out of step, a band-pass at a high cutoff (the glass), a high-feedback BBD echo and a large spring. "
     "**What is lost:** no grains (no slicing or re-triggering of a captured buffer), no freeze (the nearest is high feedback: a decaying hover), no reverse, no pitch-shifted repeats (the repeats are copies of the note; the BBD time has no LFO, so no chorus from the delay), and the LFO has one rate and one shape for everything.", "",
     f"Full tables (level, peaks, CPU, every parameter before -> after, the measures): `listen/voicing/batch-05a/19-micro-mist/README.md` and `results.json`; the WAVs (held chord with 6 s of release, tap, riff, stabs per take) are on the never-merged `listen/batch-05a-chapter3-drones` branch only.", "",
     "Takes (level: RMS over +4..+10 s of the held A3 C#4 E4 chord; peak over the chord, tap, A4 single, riff and stabs):", ""]
for k in "ABCD":
    r = R[k]
    c = r["cost"]
    f, fr = r["flicker"], r["first"]
    L.append(f"* **{k} ({r['tag']})**: {r['desc']}. VOLUME {r['volume']}, {r['level']:.2f} dBFS RMS (K-RMS {r['krms']:.1f}), peak {r['peak_all']:.1f}, {c['idle'] + c['load']:.0f} host instr/sample worst case; settled centroid {r['windows']['4-10s']['cent']:.0f} Hz, "
             f"bands under 150 / 150-400 / 400-1.2k / over 1.2k Hz " + " / ".join(f"{v:.0f}" for v in r['windows']['4-10s']['shares'].values()) + f" %; hover -20 / -40 / -60 dB at {r['hover']['t20']} / {r['hover']['t40']} / {r['hover']['t60']} ms; first repeat {fr['dly_re_note']:+.1f} dB re the note, {r['repeats_n40']} repeats above -40 dB, echo over spring {fr['margin']:+.1f} dB; tap {r['taps']['chord_gate_re_held']:+.1f} dB re the held level.")
L += ["", "**Committed (B), each parameter before -> after against INIT (the defaults):**", ""]
for key in sorted(m["params"], key=lambda x: K.PARAM_IDS[x]):
    if key != "VOLUME" and m["params"][key] != init.get(key):
        L.append("* " + R1.chg(key, init[key], m["params"][key]))
L += [f"* VOLUME 100 -> {m['volume']}", "",
      "**Not used, and why:** CHEW (tape wobble) is off in every take: it costs about +770 host instr/sample and the takes already sit at about 2000 (target <= 2300), so C with CHEW would be about 2770. GROWL is off (inert below about 28, +595 instr/sample). "
      "A pitch LFO at 12 or more is used where it is measured to do something (A, B); C and D keep LFO PITCH 0.", "",
      "**What this patch cannot do in this engine:** see the paragraph on granular above; also no Drone Latch (a held mist needs a held key; the hover after the key-up is the echo and spring tail); the LFO is one shared rate; no tempo sync; the BBD time is not modulated.", "",
      "Status: not approved; no card, no `reference-renders/` until Vincent picks."]
open(os.path.join(K.ROOT, "dog5-docs", "voicing", "19-micro-mist.md"), "w").write("\n".join(L) + "\n")
