#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Writes the Batch 4B voicing logs (dog5-docs/voicing/13-ghost-board.md, 14-reef-break.md) and the index README of listen/voicing/batch-04b/ from results.json and the texts below.
   python3 tests/voicing/batch04b_docs.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch04b as P
import batch04b_report as RP
import batch04a_docs as D4
from batch04b_variants import PATCHES

DOCS = os.path.join(K.ROOT, "dog5-docs", "voicing")
BASE = os.path.join(K.BUILD, "base")
r1 = lambda x, p=1: f"{x:.{p}f}"
ms = lambda v: ">window" if v is None else f"{v:.0f}"


def vtable(spec, R):
    L = ["| variant | what | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU |", "|---|---|---|---|---|---|---|"]
    for key, tag, desc, _ in spec["variants"]:
        m = R[key]
        cpu = f"{m['cost']['idle'] + m['cost']['load']:.0f}" if m.get("cost") else "-"
        L.append(f"| {key} {tag}{' (recommended, committed)' if key == spec['recommend'] else ''} | {desc} | {m['volume']} | {m['level']:.1f} | {m['b']:.1f} | {m[spec['level']]['peak']:.1f} | {cpu} |")
    return L


def head(spec, R, brief, near, uncertain, limits, plan, orig):
    key = spec["recommend"]
    return [f"# Voicing log — {spec['slot']:02d} \"{spec['name']}\" (FACTORY[{spec['slot'] - 1}], Batch 4B, Chapter II, the tape / crash pair)", "",
            f"6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *{brief}* Method and kit: `README.md` here (§1 phrases, §3 loudness, §17 Batch 4B).", "",
            f"## RECOMMENDED: variant {key} ({R[key]['tag']}) — committed as the patch, awaiting Vincent's listening", "",
            f"**Status: round 1 rendered, not yet heard.** Variant {key} is committed as `PF_{spec['cname']}` in `firmware/src/obv_patches.h` (equals variant {key} byte for byte: `tests/voicing/check_slot.py {spec['slot']} {key} 4b`); the others are render-only. "
            f"**Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no `reference-renders/` yet. WAVs: the never-merged `listen/batch-04b-chapter2-ghost-and-reef` branch, `listen/voicing/batch-04b/{spec['dir']}/`; tables: `README.md` and `probes.md` there.", "",
            "### The starting point (the patch as it stood)", "",
            f"* **Current values (the whole list; every parameter not named is at the table's default):** {D4.nondefault(orig)}.",
            f"* **Nearest starting patch:** {near}", f"* **The 1-2 axes judged most uncertain:** {uncertain}", f"* **Control limits foreseen:** {limits}", f"* **Plan:** {plan}", ""]


def changes_block(spec, R, orig):
    key = spec["recommend"]
    return [f"* **Final values (variant {key}), each change before -> after (the original is the nearest-base patch as it stood):**", ""] + [f"  * {c}" for c in RP.changes(orig, R[key]["params"])] + [""]


def write_13():
    spec = PATCHES[0]
    R = json.load(open(os.path.join(P.OUT, spec["dir"], "results.json")))
    orig = B.resolve(BASE, 13)
    A, B_, C, Dd = (R[k] for k in "ABCD")
    t = lambda m: m["tape"]["tape"]
    L = head(spec, R, "submerged and warped: a near-sine filtered triangle, maximum tape wow/flutter, heavy spring (the original screen brief: a 1-bit coastal deluge swamping the text). Vincent's notes: a MEDIUM level of muddy as the benchmark (MUD 150-400 over 1.2k+ roughly 10-40 over the note-on region, tail windows no worse than about 80); the Mellotron M400 (warped, wobbly tape, soft flute-like tone) to come through as much as possible, against the Space Echo's wet body: middle first, then he judges; B middle, C leans Mellotron, D leans Space Echo.",
             "PWM STRINGS (`PF_PWM_STRINGS`, 13's alone since 16 got its own array): POLY 5, a 50 % pulse and a 31 % pulse 7.0 cents sharp, a 24 dB low-pass (CUTOFF 75 = 988 Hz at C4, 50 % key tracking), a slow PWM (TRI 0.62 Hz, +-5.5 points, PHASE SPREAD), **LFO PITCH 3 (inert: the law is zero below 12)**, a spring at DRAIN 35, **no echo, no tape (CHEW 0)**. It is hot (-13.2 dBFS RMS on the ghost phrase, peak -0.2) and dark (centroid 609 Hz, MUD 108, 0.7 % above 1.2 kHz).",
             "(1) the tape wobble's depth against the tone's clarity (CHEW 70 / 100 / 127: s.d. 4.2 / 6.2 / 6.6 cents); (2) the echo and spring body against clarity (the MUD in the tail windows).",
             "there is no triangle or sine oscillator (the nearest soft tone is a narrow pulse through a key-tracking low-pass); CHEW costs about +780 host instr/sample whenever it is on (the patch is then the heaviest voiced so far: see CPU); the deck sits LAST in the chain (VOICES, DRIVE, BBD, SPRING, TAPE) so it wobbles the whole mixed signal, not each repeat; the tape's wobble is wow-leaning at most (flutter-only reads smaller in the 100 ms-frame probe); no tempo sync, one LFO (unused here).",
             "a soft, triangle-leaning tone: a narrow pulse (PW 25 %) through a 12 dB low-pass at 100 % key tracking (the 11 / 16 D recipe) plus a copy two octaves up (OSC 2 +24 st: a measured necessity, see below); LFO PITCH **0** (not 12: the deck is the wobble, a second vibrato would only add to it) and LFO PWM 0 (PWM would change the harmonics the triangle probe reads); a short organ-like start (AA 45) and a tape-stop release (AR 80); CHEW 100 with WOW/FLT leaning to wow (48), a lower hiss (HISS 40) and fewer dropouts (DROPS 50); then BBD (275 ms, FEEDBK 82) -> spring -> deck.", orig)
    L += ["### Axes chosen, variants", ""] + vtable(spec, R) + [""] + changes_block(spec, R, orig)
    L += [f"* **Level:** VOLUME {B_['volume']}; **{B_['level']:.1f} dBFS RMS** on the ghost phrase (t: 1 + 4 + 6 note-ons, echo, spring and tape included, tails excluded); phrase (b) {B_['b']:.1f} ({B_['b'] - B_['level']:+.1f} dB); peak {B_['peak_all']:.1f} dBFS; crest {B_['t_ghost']['crest']:.1f} dB; worst-case CPU **{B_['cost']['idle'] + B_['cost']['load']:.0f} host instr/sample** (idle {B_['cost']['idle']:.0f} + load {B_['cost']['load']:.0f}; the original {A['cost']['idle'] + A['cost']['load']:.0f}). **That is above every voiced patch so far (15 D 2375, 10 B-style DUAL chorus 2294): CHEW alone is +784 (B with CHEW 0: 1895, `probes.md`).**",
          "* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04b/13-ghost-board/README.md`, `probes.md`):",
          f"  * **Medium muddy:** note-on MUD {B_['notes']['mud']:.1f} (C {C['notes']['mud']:.1f}, D {Dd['notes']['mud']:.1f}, the original {A['notes']['mud']:.0f}); the tail windows 0-250 / 250-750 / 750-1500 ms after the chord: MUD {' / '.join(f'{x['mud']:.0f}' for x in B_['tailsplit'])} (centroids {' / '.join(f'{x['cent']:.0f}' for x in B_['tailsplit'])} Hz at {' / '.join(f'{x['db']:.0f}' for x in B_['tailsplit'])} dBFS); C {' / '.join(f'{x['mud']:.0f}' for x in C['tailsplit'])}; D {' / '.join(f'{x['mud']:.0f}' for x in Dd['tailsplit'])}. B sits inside the 10-40 note-on band and under about 90 in the tail; D is the murky one (49 note-on, about 300 in the tail).",
          f"  * **The soft tone, honestly:** OSC 1 through the filter measures harmonics 3 / 5 / 7 at {' / '.join(f'{x:.1f}' for x in B_['tri'])} dB against an ideal triangle's -19.1 / -28.0 / -34.2 (a square: -9.5 / -14.0 / -16.9); C {' / '.join(f'{x:.1f}' for x in C['tri'])} (nearest to a triangle), D {' / '.join(f'{x:.1f}' for x in Dd['tri'])}. It is a triangle-LEANING tone, not a triangle and not a sine. **A lone soft pulse is far too dark for 'medium muddy'** (MUD 245 with OSC 2 off; CUTOFF 84 would reach MUD 4.5 but harmonics -11 / -17 / -23: no longer triangle-like): the energy above 1.2 kHz comes from the two-octave-up copy (OSC 2 LEVEL 0 / 50 / 80 / 112 / 127: MUD 245 / 163 / 59 / 18.6 / 11), which is why the second oscillator is on.",
          f"  * **Tape wobble (one voice A3, echo and spring off):** B {t(B_)['sd']:.1f} cents s.d. ({t(B_)['range']:.1f} cents 5-95 %), strongest rate {t(B_)['rate']:.1f} Hz, one dropout of {t(B_)['dip_db']:.1f} dB; C {t(C)['sd']:.1f} cents ({t(C)['range']:.1f}); D {t(Dd)['sd']:.1f} cents ({t(Dd)['range']:.1f}); the voice alone 0.0. The ladder (`probes.md`): CHEW 40 / 70 / 100 / 127 = 2.3 / 4.1 / 6.2 / 6.5 cents s.d.; WOW/FLT 127 (flutter only) reads 2.0-2.4 cents: the 100 ms-frame probe resolves the wow (0.3-0.5 Hz) but not the faster flutter, so flutter is not measured here. CHEW 127 is the most the deck gives (about 23 cents 5-95 %): 'maximum wow/flutter' of the original brief is C.",
          f"  * **Does the deck smear the top?** With the deck (CHEW 100) the note-on region has {B_['notes']['shares']['1.2k+']:.1f} % above 1.2 kHz and MUD {B_['notes']['mud']:.1f}; with CHEW 0, {B_['notes_nochew']['shares']['1.2k+']:.1f} % and {B_['notes_nochew']['mud']:.1f}: the share above 1.2 kHz falls by about a fifth and the MUD rises by about a third; the centroid goes UP ({B_['notes_nochew']['cent']:.0f} -> {B_['notes']['cent']:.0f} Hz) because the tape hiss adds top. The tape also lengthens the tail a little (40 dB down at {ms(B_['tail']['t40'])} ms with it, {ms(B_['tail_nochew']['t40'])} without; 20 dB: {ms(B_['tail']['t20'])} / {ms(B_['tail_nochew']['t20'])}). For the tone the smear is small; the cost of CHEW is CPU and the tail, not the top.",
          f"  * **Echo and spring:** echo {B_['delay_ms']:.0f} ms (ALLEY 98), FEEDBK 82, MIX 70; the first repeat of an isolated 150 ms E4 is **{B_['first']['dly_re_note']:.1f} dB re the note** (C {C['first']['dly_re_note']:.1f}, D {Dd['first']['dly_re_note']:.1f}) with the echo {B_['first']['margin']:.1f} dB above the spring in its window; the repeats fall {' '.join(f'{v:+.1f}' for _, _, v in B_['train'])} dB. Spring DRAIN 50, SIZE 90, DAMP 40: on the isolated E4 {' / '.join(f'{x['re_dry_db']:.1f}' for x in B_['solo_onwin']['spr'])} dB re the note in 0-20 / 20-100 / 100-250 ms; after the chord's note-off the echo's return is {' / '.join(f'{x['dly']:.1f}' for x in B_['ret']['ch1'])} dB re the chord and the spring's {' / '.join(f'{x['spr']:.1f}' for x in B_['ret']['ch1'])} dB (0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms).",
          "  * **What the chain order means (chain: voices, DRIVE, BBD echo, spring, TAPE deck, Tape Stop, kill switch):** the echo takes the dry voice, the spring takes voice plus echo, and the deck takes the sum of all three. So the wobble is applied to the finished wet mix at the moment it passes the deck: a repeat arriving 275 ms later is pitched by the deck's state THEN, not by the state when it was played; every layer (note, repeats, spring tail) wobbles together, coherently. A real Space Echo has its own tape inside the echo, so each repeat is warped separately (and a runaway one warps more every pass); here that is not possible, and the repeats themselves are clean copies (the BBD's band-limit only). This follows from the chain; I did not measure the wobble separately on the repeats.",
          "", "### Recommendation (vocabulary)", "",
          "**B (middle):** a triangle-leaning, medium-muddy tone with a 6-cent wobbling tape, a clear echo above the spring and a medium wet body. C leans Mellotron (the nearest to a triangle, the most wobble, little echo); D leans Space Echo (more echo and spring, murkier, less wobble). Turn it by ear on: CHEW (wobble, and CPU), the 2-octave copy (O2 LEVEL: the clarity/mud axis), the echo (MIX, FEEDBK), the spring (DRAIN).", "",
          "### Surprising / hard with existing controls", "",
          "* A soft triangle-leaning tone is NOT medium muddy by the dictionary's ratio: it needs an octave-up copy to reach MUD 10-40 (see above).",
          "* CHEW makes this the heaviest patch so far (2679 against 2375); no lever short of CHEW 0 (-784) or dropping the echo (-16) changes it.",
          "* The deck cannot warp each repeat separately: one wobble on the whole mix.",
          "* The pitch-wander probe reads wow only; the flutter is not measured.", ""]
    open(os.path.join(DOCS, "13-ghost-board.md"), "w").write("\n".join(L) + "\n")


def write_14():
    spec = PATCHES[1]
    R = json.load(open(os.path.join(P.OUT, spec["dir"], "results.json")))
    orig = B.resolve(BASE, 14)
    A, B_, C, Dd = (R[k] for k in "ABCD")
    d = B_["bands_low"]["decay"]
    L = head(spec, R, "percussive crash: a noise burst on attack, a thick sub, long delay feedback (the original screen brief: a tidal maelstrom over the top-right corner). Vincent's notes: the noise must be a burst but not a complete blow-out; short to very short attack and/or a swell in quick (but not immediate) peak, then the decay ringing a crash-cymbal emulation out; the Space Echo reference and reach; emphasis on the burst with a medium-length tail.",
             "PERC HIT (`PF_PERC_HIT`, 14's alone): POLY 5, NOISE 60 over a saw at the key (the only 'sub': it measures 26 dB above the noise in the first 100 ms) and a saw two octaves up, a 12 dB LOW-pass at CUTOFF 90 with ENV AMT +60 (opens at the strike), filter decay 25 / amp decay 30 / sustain 0 / release 25, a spring at DRAIN 40, **no echo**. It rings 12 ms (the 4k+ band is 20 dB down 9 ms after its peak) and measures -47.9 dBFS RMS on the crash phrase (noise 26 dB under the saw in the first 100 ms): a click, not a crash.",
             "(1) the tail (the ring-out of the top bands: 0.5 / 0.9 / 1.3 s to -40 dB) and the attack (near-instant against a quick swell); (2) how far the echo runs (FEEDBK 96 / 100 / 114) without washing the burst.",
             "ONE filter per voice, shared by the noise and the oscillators; ONE amp envelope for both (the sub cannot decay faster than the noise except through the filter); no inharmonic partials of a cymbal (only noise, plus X-MOD which was not used); the level is limited by the peak, not by VOLUME alone (the noise's peak and a stack of hits); a noise patch's peak follows the random seed (two seeds checked).",
             "**the cymbal's decay from a HIGH-PASS that climbs:** a 12 dB high-pass whose cutoff is pushed down at the strike by a NEGATIVE ENV AMT (0 = about -97 semitones at the envelope's peak: the cutoff starts at 15 Hz, under the sub) and climbs back to 4186 Hz as the filter envelope falls: the sub and the low noise pass at the strike and go first (the sub's own decay is set by FD), the top of the noise rings longest (4k+ outlasts 60-150 by a factor of 5 here), and the amp envelope (AD = AR) sets the ring-out; NOISE 127 against a square sub (O1 80, O2 an octave up 45) puts the noise 3-6 dB above the sub; then a BBD echo, **no spring** (not in this patch's gear list; DRAIN 0) and no tape.", orig)
    L += ["### Axes chosen, variants", ""] + vtable(spec, R) + [""] + changes_block(spec, R, orig)
    L += [f"* **Level (note-on region = the 300 ms gates of the 11 hits: the burst and about the first 250 ms of its decay, echo included; the release, the rest of the decay and the tails excluded):** VOLUME {B_['volume']}; **{B_['level']:.1f} dBFS RMS** (seed 2: {B_['seed2']['rms']:.1f}; C {C['level']:.1f}, D {Dd['level']:.1f}); phrase (b) {B_['b']:.1f} dBFS (three stacked noise voices: peak {B_['b_stabs']['peak']:.1f}, no clipped sample); own-phrase peak {B_['u_crash']['peak']:.1f} dBFS (seed 2 {B_['seed2']['peak']:.1f}); crest {B_['u_crash']['crest']:.1f} dB; worst-case CPU {B_['cost']['idle'] + B_['cost']['load']:.0f} host instr/sample (the original {A['cost']['idle'] + A['cost']['load']:.0f}). **B ({B_['level']:.1f}) and D ({Dd['level']:.1f}) sit 0.4 and 0.6 dB under the -19.5 floor of the band: with the peak held at -4 dBFS on both seeds the level falls there (VOLUME {B_['volume']} / {Dd['volume']}, of 127); C {C['level']:.1f} is inside.**",
          "* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04b/14-reef-break/README.md`, `probes.md`):",
          f"  * **Not a blow-out:** own-phrase peak {B_['u_crash']['peak']:.1f} / {B_['seed2']['peak']:.1f} dBFS on two seeds (the second seed = a quiet note struck first, so the hits land on other voice cards' noise generators), crest {B_['u_crash']['crest']:.1f} / {B_['seed2']['crest']:.1f} dB, {B_['rail']:.0f} % of samples within 10 % of the rail (noise: the pixelation measure of 05 reads 98 % on a clipped square), no clipped sample in any render; the isolated hit with the echo peaks at {B_['echo_peak']:.1f} dBFS.",
          f"  * **Noise against sub (first 100 ms):** noise {B_['nvs']['low']['ratio']:+.1f} dB over the sub on A1 ({B_['nvs']['mid']['ratio']:+.1f} on A2); the original was {A['nvs']['low']['ratio']:+.1f}. The sub-only A1 hit's first 150 ms: {B_['sub_shares']['low']['<60']:.0f} % under 60 Hz, {B_['sub_shares']['low']['60-150']:.0f} % in 60-150 (an A1 fundamental is 55 Hz); on A2 {B_['sub_shares']['mid']['60-150']:.0f} % in 60-150. The sub's 40-150 Hz band falls 20 / 40 dB in {ms(B_['sub_decay']['t20'])} / {ms(B_['sub_decay']['t40'])} ms (C {ms(C['sub_decay']['t20'])} / {ms(C['sub_decay']['t40'])}, D {ms(Dd['sub_decay']['t20'])} / {ms(Dd['sub_decay']['t40'])}): thick for about a quarter of a second, then the noise alone.",
          f"  * **Attack (A1, 10 / 50 / 90 % of the peak, ms):** B {B_['att']['low']['t10']:.1f} / {B_['att']['low']['t50']:.1f} / {B_['att']['low']['t90']:.1f} (near-instant: the first millisecond; the 90 % mark at {B_['att']['low']['t90']:.1f} ms is the noise's own random peaks); C **{C['att']['low']['t10']:.1f} / {C['att']['low']['t50']:.1f} / {C['att']['low']['t90']:.1f}** (AA 52: the quick swell, peak at {C['att']['low']['peak_ms']:.0f} ms); D {Dd['att']['low']['t10']:.1f} / {Dd['att']['low']['t50']:.1f} / {Dd['att']['low']['t90']:.1f} (AA 44: 50 % at about 7 ms).",
          f"  * **The cymbal's decay (A1 hit, voice alone, band energy to -20 / -40 dB after each band's own peak, ms):** 60-150: {ms(d['60-150']['t20'])} / {ms(d['60-150']['t40'])}; 400-1.2k: {ms(d['400-1.2k']['t20'])} / {ms(d['400-1.2k']['t40'])}; 1.2k-4k: {ms(d['1.2k-4k']['t20'])} / {ms(d['1.2k-4k']['t40'])}; **4k+: {ms(d['4k+']['t20'])} / {ms(d['4k+']['t40'])}** (the main body rings out to -40 dB in ~0.9 s). Tail options: B 0.93 s, **C 1.33 s** (AD = AR 97), **D 0.70 s** (AD = AR 88; FD 92). The bands fall in order, low first, as a cymbal does. For comparison the same noise through a closing LOW-pass (the original's way) has the top band 20 / 40 dB down at 223 / 302 ms and the sub still ringing at 499 / 964 ms: the wrong way round (`probes.md`).",
          f"  * **The echo (Space Echo):** ALLEY 106 = {B_['delay_ms']:.0f} ms, FEEDBK 96, MIX 90. Repeats 1..6 re the burst: {' '.join(f'{v:+.0f}' for _, v in B_['echo'][:6])} dB; {B_['echo_n40']} repeats stay above -40 dB (C {C['echo_n40']}; **D, FEEDBK 114: all 16 slots, 5.4 s, {' '.join(f'{v:+.0f}' for _, v in Dd['echo'][:6])} dB**); the whole hit with echo is 20 / 40 / 60 dB down at {ms(B_['tail']['t20'])} / {ms(B_['tail']['t40'])} / {ms(B_['tail']['t60'])} ms (D {ms(Dd['tail']['t20'])} / {ms(Dd['tail']['t40'])} / {ms(Dd['tail']['t60'])}). Stability: no clipped sample at any FEEDBK 96-127 on the isolated hit and its peak stays {B_['echo_peak']:.1f} dBFS; from FEEDBK 118 the repeats no longer fall below -40 dB (24 slots: -28 dB at repeat 24; 122: -10; 127: -1: the loop is held by its own ceiling, `probes.md`). The echo under the figure's hits: {' '.join(f'{v:+.0f}' for v in B_['under'])} dB re each hit (hits 3-11): it stays under the hits even at 400 ms spacing (D: {' '.join(f'{v:+.0f}' for v in Dd['under'])}).",
          f"  * **The sub in the repeats (MUD / centroid Hz / % in 60-150, repeat slots 1, 2, 3):** {' ; '.join(f'{t['mud']:.0f} / {t['cent']:.0f} / {t['shares']['60-150']:.0f}' for t in B_['echo_windows'])}: no tubby 150-400 Hz body (the echo's feedback path has a high-pass at 80 Hz; the repeats are mostly noise).",
          "  * **What the filter can and cannot do (`probes.md`, one control changed):** the climbing high-pass is what makes the top outlast the lows and keeps the sub only at the strike; a closing low-pass does the opposite; a wide-open low-pass or a notch leave every band the same length (the amp envelope's); a high-pass without the envelope removes the sub (noise 27 dB over it); a band-pass at CUTOFF 100 leaves the noise 17 dB under the sub and the level 11 dB down. FD sets the sub's length (FD 85 / 92 / 100 / 108: sub -20 dB at 58 / 93 / 163 / 255 ms).",
          "  * **What I could not do:** a cymbal's inharmonic metallic partials (only noise; X-MOD not tried, it is a cross-FM of the two oscillators); a sub that decays faster than the noise through the amp (one amp envelope: the high-pass does it); a separate envelope for the burst and the ring (one filter envelope, one amp envelope); the level reference at VOLUME 127 without raising the peak above -4 on a hit this peaky (B and D sit slightly under the band).",
          "", "### Recommendation (vocabulary)", "",
          "**B (burst):** an instant noise burst with a square sub that goes first, then the top of the noise ringing out over about a second into a runaway-leaning echo that stays well under the hits. C is the quick swell (peak in 27 ms) with the longest tail and the level inside the band; D is the shortest tail with a near-runaway echo that never falls below -40 dB. Turn it by ear on: AA (instant against swell), AD = AR (the ring-out), FD (the sub's length), NOISE / O1 / O2 (burst against sub), FEEDBK and MIX (the echo).", "",
          "### Surprising / hard with existing controls", "",
          "* The original rings 12 ms: it is a click; the brief's burst-and-ring needed a new filter strategy, not a re-trim.",
          "* The sub can only leave early through the filter: a NEGATIVE ENV AMT on a high-pass is the one way to have the sub at the strike and the cymbal's top last.",
          "* The peak limits the level (B -19.9, D -20.1) because a noise burst's crest is 15-16 dB; the swell (C) lowers it to 13.5.",
          "* Phrase (b) (three notes at once) peaks at -1.0 / -1.5 / -1.7 dBFS on B / C / D: three noise voices stack; not the patch's use, not clipped.", ""]
    open(os.path.join(DOCS, "14-reef-break.md"), "w").write("\n".join(L) + "\n")


def write_index():
    L = ["# Batch 4B (Chapter II): 13 Ghost Board, 14 Reef Break", "",
         "Round 1, rendered, not yet heard. Per patch: `README.md` (variants and numbers), `probes.md` (one control stepped), `results.json`, and (on the listen branch only) the WAVs `<NN-name>_<KEY>_<phrase>.wav` "
         "(A is the original through the base program path; B, C, D are variants over INIT; VOLUME is trimmed so the own phrase's peak is <= -4 dBFS and the level near -18.0 dBFS RMS). Phrases: `ghost` = t_ghost (13), `crash` = u_crash (14), `stabs` = b_stabs. Method: `dog5-docs/voicing/README.md` section 17.", ""]
    for spec in PATCHES:
        R = json.load(open(os.path.join(P.OUT, spec["dir"], "results.json")))
        L += [f"## {spec['slot']:02d} {spec['name']}", ""] + vtable(spec, R) + [""]
    open(os.path.join(P.OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    write_13()
    write_14()
    write_index()
    print("logs written")
