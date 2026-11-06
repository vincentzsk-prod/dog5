#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The three Batch 5A voicing logs (dog5-docs/voicing/18-roto-scopo.md, 19-blackwater.md, 22-melting-orb.md) from listen/voicing/batch-05a/<dir>/results.json: the numbers are the run's, the prose is here.

  python3 tests/voicing/batch05a_docs.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
from batch05a_variants import PATCHES
from batch05a_report import changes

DOCS = os.path.join(K.ROOT, "dog5-docs", "voicing")
OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-05a")
BASE = os.path.join(K.BUILD, "base")

CANNOT = {
    18: ["**No Poly-Mod.** The wander is one shared LFO (smooth random or sample-and-hold) added to the cutoff: it cannot follow OSC 2, it is not tied to any oscillator's pitch or phase, and there is one LFO rate for everything the LFO touches (here the filter only; "
         "LFO PITCH is 0). The movement is common to all voices (the per-voice difference is the slop, VINTAGE, which moves pitch and the filter's own per-card offset, not a second wander).",
         "**UNISON is one note at a time.** A three-key chord plays its last key only (the cards gated after a 3-key chord: 3 = one group of three); a chord needs POLY or DUAL (not in this brief).",
         "There is no drone latch: the drone lasts as long as the key is down."],
    19: ["**There is no sub oscillator.** The sub is OSC 2 an octave down (SEMI -12, the lowest the knob offers); OSC 1 is off. On A1 that is 27.5 Hz, on A0 13.75 Hz.",
         "**At A0 and A1 most of the energy is under 60 Hz** (B: A0 85 %, A1 77 %), which small speakers do not reproduce. The ring of the resonant filter (a tone at a multiple of the key) is what is heard there; the sub itself becomes audible from A2 (52 % above 60 Hz) and fully at A3.",
         "VOLUME tops out at 127: B and D sit at the top of the knob and cannot go louder on the same tone (their K-weighted level is 5 dB under the reference).",
         "A MONO patch: a chord plays its last key."],
    22: ["**ENV>O2 routes the FILTER envelope to OSC 2's pitch only** (`obv_engine.h`: `p2 += fenv x (ENV>O2 - 64) x 97 >> 15`, Q8 semitones, i.e. (ENV>O2 - 64) x 24/63 semitones at the envelope's top; measured -675 cents for 46, -1209 for 32 against -6.86 / -12.19 st). "
         "It cannot bend OSC 1 and it cannot use the amp envelope. So the stack that melts is OSC 2 alone, with OSC 1 off; with both oscillators on, only OSC 2 would sink and the two would part.",
         "**An inverted envelope bends the pitch the wrong way for a collapse** if the envelope falls: a negative ENV>O2 with a decaying filter envelope starts low and RISES to the note. The melt here uses a RISING filter envelope (FA = the melt time) with negative ENV AMT and ENV>O2, so cutoff and pitch both sink while the key is down.",
         "**The key-up undoes the melt in the tail:** the filter envelope releases, so pitch and brightness climb back while the note fades, even at the slowest filter release (FR 127): B's pitch reads -634 cents in the first 0.4 s of the tail, -549 at 0.5 s and -472 at 1.0 s (the tail is 40 dB down by 0.94 s), the centroid 242 -> 724 -> 2529 Hz over the same three windows. "
         "Not isolated: whether it is audible at those levels (an untested perceptual question); a shorter AR makes it shorter (B's tail is 60 dB down at 1.43 s).",
         "UNISON is one note at a time (a chord plays its last key: B and C); D is DUAL, where three keys melt together.",
         "One shared LFO is unused here; no Poly-Mod; no drone latch."],
}


def write(spec, kind):
    R = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
    orig = B.resolve(BASE, spec["slot"])
    m = R["B"]
    L = [f"# Voicing log: {spec['slot']:02d} \"{spec['name']}\" (FACTORY[{spec['slot'] - 1}], Batch 5A, Chapter III, the drones)", "",
         "## ROUND 1: rendered, not yet heard. Variant B is committed as the patch (own array); A, C, D are render-only.", "",
         f"Full tables for all four variants (level, peaks, CPU, every change before -> after, the measures below): `listen/voicing/batch-05a/{spec['dir']}/README.md` and `results.json`; the WAVs are on the never-merged `listen/batch-05a-chapter3-drones` branch only.", "",
         "Variants:", ""]
    for k in "ABCD":
        r = R[k]
        c = r["cost"]
        L.append(f"* **{k} ({r['tag']})**: {r['desc']}. VOLUME {r['volume']}, held level {r['level']:.2f} dBFS RMS over +{spec['win'][0] / 1000:.0f}..+{spec['win'][1] / 1000:.0f} s, K-RMS {r['krms']:.1f}, peak {r['peak_all']:.1f} (all phrases), worst-case CPU {c['idle'] + c['load']:.0f} host instr/sample.")
    L += ["", f"**Committed (B), each change before -> after against the patch as it stood:**", ""] + [f"* {c}" for c in changes(orig, m["params"])] + [f"* VOLUME {orig['VOLUME']} -> {m['volume']}", ""]
    L += ["**What this patch cannot do in this engine:**", ""] + [f"* {t}" for t in CANNOT[spec["slot"]]] + ["", "Status: not approved; no card, no `reference-renders/` until Vincent picks."]
    open(os.path.join(DOCS, f"{spec['slot']:02d}-{spec['dir'].split('-', 1)[1]}.md"), "w").write("\n".join(L) + "\n")


def main():
    for spec in PATCHES:
        write(spec, None)


if __name__ == "__main__":
    main()
