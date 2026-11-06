#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Writes the Batch 4A voicing logs (dog5-docs/voicing/10-atlantic-swell.md, 12-kelp-tangle.md, 16-tidal-pull.md) and the index README of listen/voicing/batch-04a/ from
results.json (numbers) and the texts below (the decisions).   python3 tests/voicing/batch04a_docs.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch04a as A
import batch04a_metrics as Q
import batch04a_report as RP
from batch04a_variants import PATCHES

DOCS = os.path.join(K.ROOT, "dog5-docs", "voicing")
BASE = os.path.join(K.BUILD, "base")


def nondefault(p):
    dflt = B._pdef_def()
    SYMD = {"W_OFF": 0, "W_SAW": 1, "W_PLS": 2, "W_BOTH": 3, "M_POLY": 0, "M_DUAL": 1, "M_UNISON": 2, "M_MONO": 3, "F_LP12": 0, "F_HP12": 1, "F_BP12": 2, "F_NOTCH": 3, "F_LP24": 4, "F_SEM": 5,
            "L_TRI": 0, "L_SAW": 1, "L_RAMP": 2, "L_SQR": 3, "L_SH": 4, "L_RND": 5, "LP_SYNC": 0, "LP_FREE": 1, "LP_SPREAD": 2, "TO_O1": 0, "TO_O2": 1, "TO_BOTH": 2, "DD_16": 0, "DD_8T": 1, "DD_8": 2,
            "DD_8D": 3, "DD_4": 4, "DD_4D": 5, "DD_2": 6, "A_OFF": 0, "D_16": 3}
    out = []
    for k, i in sorted(K.PARAM_IDS.items(), key=lambda kv: kv[1]):
        if k in p:
            d = dflt[k]
            d = int(SYMD.get(d, d))
            if p[k] != d:
                out.append(f"{k} {p[k]}")
    return ", ".join(out)


def secs(ms):
    return "later than 3.5 s (the window)" if ms is None else f"{ms / 1000:.1f} s"


def f(x, p=1):
    return f"{x:.{p}f}"


def variants_table(spec, R):
    L = ["| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |", "|---|---|---|---|---|---|---|"]
    for key, tag, desc, _ in spec["variants"]:
        m = R[key]
        cpu = f"{m['cost']['idle'] + m['cost']['load']:.0f}" if m.get("cost") else "-"
        L.append(f"| {key} {tag}{' (recommended, committed)' if key == spec['recommend'] else ''} | {desc} | {m['volume']} | {m['level']:.1f} | {m['b']:.1f} | {m['peak_all']:.1f} | {cpu} |")
    return L


def head(spec, R, brief, near, uncertain, limits, plan, orig):
    L = [f"# Voicing log — {spec['slot']:02d} \"{spec['name']}\" (FACTORY[{spec['slot'] - 1}], Batch 4A, Chapter II, the spring / organ / wash set)", "",
         f"6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *{brief}* Method and kit: `README.md` here (§1 phrases, §3 loudness, §16 Batch 4A).", "",
         f"## RECOMMENDED: variant {spec['recommend']} ({R[spec['recommend']]['tag']}) — committed as the patch, awaiting Vincent's listening", "",
         f"**Status: round 1 rendered, not yet heard.** Variant {spec['recommend']} is committed as `PF_{spec['cname']}` in `firmware/src/obv_patches.h` (equals variant {spec['recommend']} byte for byte: "
         f"`tests/voicing/check_slot.py {spec['slot']} {spec['recommend']} 4a`); the others are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** "
         f"No voice card and no `reference-renders/` yet (after approval). WAVs: the never-merged `listen/batch-04a-chapter2-organ-kelp-wash` branch, `listen/voicing/batch-04a/{spec['dir']}/`; tables: `listen/voicing/batch-04a/{spec['dir']}/README.md` and `probes.md`.", "",
         "### The starting point (the patch as it stood)", "",
         f"* **Current values (the whole list; every parameter not named is at the table's default):** {nondefault(orig)}.",
         f"* **Nearest starting patch:** {near}", f"* **The 1-2 axes judged most uncertain:** {uncertain}", f"* **Control limits foreseen:** {limits}", f"* **Plan:** {plan}", ""]
    return L


def changes_block(spec, R, orig):
    key = spec["recommend"]
    return [f"* **Final values (variant {key}), each change before -> after (the original is the nearest-base patch as it stood):**", ""] + [f"  * {c}" for c in RP.changes(orig, R[key]["params"])] + [""]


def write_10():
    spec = PATCHES[0]
    d = os.path.join(A.OUT, spec["dir"])
    R = json.load(open(os.path.join(d, "results.json")))
    orig = B.resolve(BASE, 10)
    m, a = R["B"], R["A"]
    L = head(spec, R, "a woozy combo-organ. Dual pulse, slow vibrato, heavy BBD delay. Rolls like Cape surf. Vincent's notes: Leslie / roto-sound inspiration welcome; cold, fresh, clear note definition, not a tropical wash, 'cold crispy Atlantic ocean water'; a clear chorus with the vibrato more than a vibrato-led modulation (the TC Electronic June-60 pedal's tone); one shared LFO, so a Leslie-style effect is vibrato plus tremolo at one rate; CHEW only if it demonstrably helps clarity.",
             "HOLLOW PAD (`PF_HOLLOW_PAD`, shared with 12 Kelp Tangle): POLY, two narrow pulses (PW 16 % and PW 85 %, which is an INVERTED 15 % pulse, so the pair partly cancels as it beats: that is the hollow), a notch filter, a 117 ms nominal attack (AA 70; measured 10 / 50 / 90 % at 6 / 29 / 61 ms), a 1.2 s nominal release (AR 100), a slow PWM +-2.3 points, **no pitch LFO (LFO PITCH 0), no delay (DLY MIX 0), a spring at DRAIN 40**. It is bright (centroid 5369 Hz) and has neither the vibrato, the chorus nor the BBD of the brief.",
             "(1) how deep the pitch modulation is against how clear the notes stay (chorus-led against vibrato-led); (2) how much echo: the first repeat's level, its feedback, and whether the repeats pile onto the next staccato note.",
             "ONE LFO per patch: a Leslie's vibrato and tremolo come out IN PHASE (a rotor's loudness peak is 90 degrees from its Doppler pitch peak: not reachable); LFO PHASE SPREAD fixes 45 degrees per voice card; the BBD's time has no LFO (a short BBD is a comb / Haas widener, not a chorus); DLY TONE only shapes the feedback path (the first repeat is the BBD's own band-limit); a DUAL patch doubles the voices (CPU).",
             "chorus = **DUAL** (every note a left / right pair, SPREAD 127) + a slow **TRI pitch LFO in PHASE SPREAD** (the two voices of a note are 45 degrees apart in the LFO, so their pitch difference swings: that is the beating a chorus makes, built from the existing controls; a static detune alone, or a short BBD, does not move); a gentle pitch depth (+-19 cents at 0.72 Hz) keeps the vibrato under the chorus; organ keying (3 ms attack, full sustain, 29 ms release) and an open 12 dB low-pass keep the notes crisp; a heavy ping-pong BBD (361 ms, close to a dotted eighth at 120 BPM) with FEEDBK 95; the spring is only a touch (DRAIN 24: cold, not a wash). The Leslie-style option is variant D: the same LFO on pitch AND amp, PHASE FREE (SPREAD would cancel the tremolo in the sum: probe below). CHEW is not used.", orig)
    L += ["### Axes chosen, variants", ""] + variants_table(spec, R) + [""]
    L += changes_block(spec, R, orig)
    t = m["train"]
    L += ["* **Level:** VOLUME %d; **%.1f dBFS RMS** on the organ phrase (q: %s); phrase (b) %.1f (%+.1f dB), K-weighted (b) %.1f; peak %.1f dBFS; crest %.1f dB; worst-case CPU %.0f host instr/sample (idle %.0f + load %.0f; the original %.0f)." % (
        m["volume"], m["level"], "3 + 1 + 4 + 3 note-ons, echo and spring included, tails excluded", m["b"], m["b"] - m["level"], m["b_stabs"]["rms_k"], m["peak_all"], m["q_organ"]["crest"], m["cost"]["idle"] + m["cost"]["load"], m["cost"]["idle"], m["cost"]["load"], a["cost"]["idle"] + a["cost"]["load"]),
          "* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/10-atlantic-swell/README.md`, `probes.md`):",
          f"  * **Note definition:** centroid {m['notes']['cent']:.0f} Hz over the note-on region (the original {a['notes']['cent']:.0f}), MUD {m['notes']['mud']:.1f}, {m['notes']['shares']['1.2k+']:.0f} % of the energy above 1.2 kHz; the amp attack measures 10 / 50 / 90 % at {m['attack']['voice']['t10']:.0f} / {m['attack']['voice']['t50']:.0f} / {m['attack']['voice']['t90']:.1f} ms (the original 6 / 29 / 61).",
          f"  * **Chorus:** the LFO is TRI {m['lfo']['hz']:.2f} Hz (RATE 53), pitch +-{m['lfo']['cents']:.0f} cents (LFO PITCH 16, the law); the one-voice audio probe reads a {m['pitch_probe']['sd']:.1f} cent s.d. and a {m['pitch_probe']['range']:.1f} cent 5-95 % range at {m['pitch_probe']['rate']:.2f} Hz. The held A minor chord (dry): L/R correlation {m['corr'][0]:.2f} (the original {a['corr'][0]:.2f}), the A3 band beats at {m['beat']['rate_mean']:.2f} Hz ({m['beat']['rate_min']:.2f}-{m['beat']['rate_max']:.2f}) with a {m['beat']['depth_db']:.0f} dB envelope swing (a MONO reading: left and right are separate voices); the stereo level moves {m['am'][0]:.1f} dB. With DETUNE 0 the LFO's phase offset alone makes the beating (SPREAD 37 dB, PHASE FREE 5.8 dB, a plain DUAL pair 5.5 dB); with B's 5.5-cent DETUNE the static detune beats too (a DETUNE-only pair 39 dB, PHASE FREE 39 dB, B 29 dB): the chorus here is the pair's beat, moved by the LFO (`probes.md`). Left / right correlation differences of ~0.1 between settings are within what one render shows (oscillator start phases are random): not a trend.",
          f"  * **Delay:** ALLEY 106 = {m['delay_ms']:.0f} ms, FEEDBK 95, MIX 100, PINGPONG 127. On an isolated 120 ms E4 the first repeat arrives {m['delay_ms']:.0f} ms after the note-on and its peak is **{m['first']['dly_re_note']:.1f} dB re the dry note's peak** (peak at {m['first']['t_ms']:.0f} ms); the repeats fall about 3.2 dB each ({' '.join(f'{v:+.1f}' for _, _, v in t)}), the whole echo is 60 dB down {secs(m['solo_tail']['full']['t60'])} after the note. The spring in the repeat's window is {m['first']['spr_re_note_same']:.1f} dB re the note (the delay is {m['first']['margin']:.0f} dB above it). The echo of the held A minor chord is {m['ret']['ch1'][0]['dly']:.1f} / {m['ret']['ch1'][1]['dly']:.1f} / {m['ret']['ch1'][2]['dly']:.1f} / {m['ret']['ch1'][3]['dly']:.1f} / {m['ret']['ch1'][4]['dly']:.1f} dB re the chord at 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms after the note-off.",
          f"  * **Cold, clear echo:** the first repeat's centroid is {m['solo_split']['cent']:.0f} Hz against the note's {m['solo_note_split']['cent']:.0f} (the BBD's own band-limit, 2.8-8 kHz by time). **DLY TONE does not move the first repeat** (60 / 90 / 127: 1454 Hz each), only the later ones (third repeat 949 / 1082 / 1136 Hz), so the note's own spectrum is where the clarity is. The echoes of the staccato figure land {-m['under']['dly'][1]:.0f} / {-m['under']['dly'][2]:.0f} / {-m['under']['dly'][3]:.0f} dB under notes 2 / 3 / 4 (the delay return re the note, 300 ms apart against a 361 ms delay).",
          f"  * **Spring:** DRAIN 24 (19 %), SIZE 70, DAMP 30: {m['ret']['ch1'][0]['spr']:.1f} dB re the chord in the first 100 ms after the note-off and {m['ret']['ch1'][2]['spr']:.1f} at 250-500 ms: a touch, as the 'cold, not tropical' note asks (the original: DRAIN 40, SIZE 100).",
          "* **Leslie option (D):** the same TRI LFO (0.84 Hz) on pitch +-19 cents and on amp (AMP 45 = a %.1f dB dip on one voice), PHASE FREE: the chord's tremolo measures %.1f dB (B: %.1f). With PHASE SPREAD the 45 degree offsets cancel it (AMP 45: 2.2 dB, AMP 80: 2.8 dB); with SYNC or FREE it is a real tremolo (3.9 / 2.9 dB at AMP 45, 7.8 / 6.5 at 80). Pitch and tremolo are IN PHASE here; a rotary speaker's are not." % (R["D"]["lfo"]["amp_db"], R["D"]["am"][0], m["am"][0]),
          "* **Heavy variant (C):** pitch +-28 cents at 0.84 Hz and MIX 118 / FEEDBK 104 / 387 ms: the first repeat is %.1f dB re the note and the echo is 60 dB down %s after the isolated note (B %s)." % (R["C"]["first"]["dly_re_note"], secs(R["C"]["solo_tail"]["full"]["t60"]), secs(m["solo_tail"]["full"]["t60"])),
          "* **CPU:** DUAL doubles the voices: the worst case is %.0f host instr/sample (the heaviest voiced patches are 15 D 2375, 07 B 2177); as POLY (one voice per note) it would be 1804 and the chorus is gone; one oscillator saves 48 (`probes.md`). The device build was not run; the render time on the device is not measured." % (m["cost"]["idle"] + m["cost"]["load"]),
          "", "### Recommendation (vocabulary)", "",
          "**B (june):** crisp, cold, clear: narrow-pulse organ with a slow, wide chorus (DUAL, TRI pitch, SPREAD) rather than a vibrato, and a heavy ping-pong echo that rolls without covering the notes. C is the same with more wooze and a heavier echo; D is the rotary-speaker reading. Turn it by ear on: pitch depth (LFO PITCH 12 = +-9 cents ... 22 = +-28), RATE, the echo (MIX, FEEDBK, ALLEY), the spring (DRAIN).", "",
          "### Surprising / hard with existing controls", "",
          "* The original had no vibrato, no chorus and no delay at all (LFO PITCH 0, DLY MIX 0): the brief's 'slow vibrato, heavy BBD' had to be built, not tuned.",
          "* The chorus cannot be a modulated delay (the BBD's time has no LFO); it is two voices whose pitches wander out of step, so it can beat deeply in a mono sum (29 dB envelope swing on A3's band) while the stereo level moves 2.4 dB.",
          "* Quadrature Leslie (tremolo 90 degrees from the vibrato) needs two LFO phases: not available. D is in phase.",
          "* A DUAL chorus costs about +490 host instr/sample over a POLY version (2294 against 1804).", ""]
    open(os.path.join(DOCS, "10-atlantic-swell.md"), "w").write("\n".join(L) + "\n")


def write_12():
    spec = PATCHES[1]
    d = os.path.join(A.OUT, spec["dir"])
    R = json.load(open(os.path.join(d, "results.json")))
    orig = B.resolve(BASE, 12)
    m, a, c = R["B"], R["A"], R["C"]
    bp = m["pwm_a2"]["bands"]
    L = head(spec, R, "dense and tangled. Heavy PWM, murky low-pass, a spring tail. Vincent's notes: make the PWM stand out in the mix; stay close to the Moog Prodigy (murky, raw, dark), the Fender spring tank (the tail, springy) and, closest, a Polysix PWM pad into a spring tank; lean on the LFO; murky against PWM audible is the tension (a low cutoff hides PWM); watch tubby (150-400 Hz in the tail).",
             "HOLLOW PAD (`PF_HOLLOW_PAD`, shared with 10 Atlantic Swell): the same patch as the original 10, with a spring at DRAIN 40. Its LFO PWM is +-2.3 points around PW 16 % / 85 %: **the movement it has (14.2 dB in the 150-400 Hz band of a held A2 at 1.2 Hz) is the beating of its inverse narrow-pulse pair, not PWM** (with LFO PWM 0 it is still 14.2 dB; with the detune off too it is 1.0 dB: `probes.md`). It is not murky: centroid 4222 Hz, 13 % of the energy above 1.2 kHz.",
             "(1) the cutoff against the PWM and the tail (the murk): measured by the 150-400 / 400-1.2k / 1.2k+ bands of a held A2 and of a chord, and the tail's MUD; (2) the PWM depth and rate (sweep width, 1 Hz against 2.3 Hz, and whether the voices sweep together).",
             "no Poly-Mod, so the brief's 'PWM driven by OSC B' is not possible: ONE shared TRI LFO drives the pulse widths of both oscillators (what is lost: a modulator with its own pitch / envelope, a different rate per oscillator, a sweep that follows the note); PWM through a low-pass reads as level and low-band movement, and the 150-400 Hz band's modulation saturates near 10 dB; a PWM sweep is one LFO period long (1 s here), so a 150 ms note hears only a slice; the spring is fed the murky voice, so its tail is murky too.",
             "two pulses 7.0 cents apart, both swept by the LFO's TRI on ONE side of 50 % (PW 42 = 33 %, +-15 points: 18-48 %, so no doubled rate), LFO PHASE SYNC (every detached note starts the sweep together), a 24 dB low-pass at 100 % key tracking (the filter sits at the same place in each note's harmonics: murky in every register), RESO 30 for some bite, no filter envelope (nothing moves but the PWM), a medium spring. PWM audibility is measured AFTER the filter (the band energies of a held A2, dry).", orig)
    L += ["### Axes chosen, variants", ""] + variants_table(spec, R) + [""]
    L += changes_block(spec, R, orig)
    L += ["* **Level:** VOLUME %d; **%.1f dBFS RMS** on the tangle phrase (r: 1 + 3 + 6 note-ons, spring included, tails excluded); phrase (b) %.1f (%+.1f dB), K-weighted (b) %.1f; peak %.1f dBFS; crest %.1f dB; worst-case CPU %.0f host instr/sample (idle %.0f + load %.0f; the original %.0f)." % (
        m["volume"], m["level"], m["b"], m["b"] - m["level"], m["b_stabs"]["rms_k"], m["peak_all"], m["r_tangle"]["crest"], m["cost"]["idle"] + m["cost"]["load"], m["cost"]["idle"], m["cost"]["load"], a["cost"]["idle"] + a["cost"]["load"]),
          "* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/12-kelp-tangle/README.md`, `probes.md`):",
          f"  * **PWM after the filter, held A2 (dry):** the LFO is TRI {m['lfo']['hz']:.2f} Hz sweeping the pulse width {m['lfo']['pw_lo']:.0f}-{m['lfo']['pw_hi']:.0f} % (+-{m['lfo']['pts']:.1f} points around {m['lfo']['pw_pct']:.0f} %). Band-energy modulation (95th - 5th percentile over 23 ms frames, depth in dB): **{bp['150-400'][0]:.1f} in 150-400 Hz, {bp['400-1.2k'][0]:.1f} in 400-1.2k, {bp['1.2k-3k'][0]:.1f} in 1.2k-3k**, and the level itself moves {bp['level'][0]:.1f} dB; the strongest component sits at {bp['150-400'][1]:.1f} Hz in 150-400 (the LFO is {m['lfo']['hz']:.2f}: the sweep does not double). **02 D's figure (about 12 dB in 150-400 Hz) is not reached: {bp['150-400'][0]:.1f} dB, and it does not move with the controls tried:** LFO PWM 60 / 80 / 100 / 115 gives 10.3 / 9.9 / 10.1 / 10.0 dB and CUTOFF 78-104 gives 9.8-10.2 (`probes.md`); DRIVE 20-40 lifts it to 12.5-12.7 dB but takes the level swing from 5.9 to 3.4-3.7 dB and the chord's 150-400 depth from 8.9 to 6.9-6.2, so it is not used. On the held chord (A2 E3 C4) the depths are {m['pwm_chord']['bands']['150-400'][0]:.1f} / {m['pwm_chord']['bands']['400-1.2k'][0]:.1f} / {m['pwm_chord']['bands']['1.2k-3k'][0]:.1f} dB and the level moves {m['pwm_chord']['bands']['level'][0]:.1f} dB.",
          f"  * **Murky, with numbers:** held A2 centroid {m['a2']['cent']:.0f} Hz (the original {a['a2']['cent']:.0f}), {m['a2']['shares']['<60'] + m['a2']['shares']['60-150']:.0f} % of its energy under 150 Hz and {m['a2']['shares']['1.2k+']:.1f} % above 1.2 kHz; the chord's centroid {m['chord']['cent']:.0f} Hz, {m['chord']['shares']['1.2k+']:.1f} % above 1.2 kHz. Dictionary: this is DARK (CUTOFF down) with a ratio the dictionary would call MUDDY (MUD {m['notes']['mud']:.0f} over the note-on region); the PWM is what moves inside it.",
          f"  * **The cutoff axis (B 86 against C 98):** C's A2 centroid is {c['a2']['cent']:.0f} Hz and its chord centroid {c['chord']['cent']:.0f} Hz ({c['chord']['shares']['1.2k+']:.1f} % above 1.2k); its PWM depth in 400-1.2k is {c['pwm_a2']['bands']['400-1.2k'][0]:.1f} dB against B's {bp['400-1.2k'][0]:.1f}, in 150-400 the same ({c['pwm_a2']['bands']['150-400'][0]:.1f}); its tail's MUD is {c['tailsplit']['chord'][0]['mud']:.0f} / {c['tailsplit']['chord'][1]['mud']:.0f} / {c['tailsplit']['chord'][2]['mud']:.0f} against B's {m['tailsplit']['chord'][0]['mud']:.0f} / {m['tailsplit']['chord'][1]['mud']:.0f} / {m['tailsplit']['chord'][2]['mud']:.0f}. So a murkier cutoff buys PWM depth in the upper bands and costs a more tubby tail; the cutoff is the lever to turn by ear.",
          f"  * **Spring (DRAIN 55 = 43 %, SIZE 75, DAMP 30, PRE-DLY 20):** the spring's return re the dry chord after its note-on is {m['onwin']['chord'][0]['re_dry_db']:.1f} / {m['onwin']['chord'][1]['re_dry_db']:.1f} / {m['onwin']['chord'][2]['re_dry_db']:.1f} dB in 0-20 / 20-100 / 100-250 ms; after the chord's note-off it is {m['ret']['chord'][0]['spr']:.1f} / {m['ret']['chord'][1]['spr']:.1f} / {m['ret']['chord'][2]['spr']:.1f} dB re the chord in 0-250 / 250-750 / 750-1500 ms; the tail is 20 / 40 / 60 dB down at {m['tail']['chord']['t20']:.0f} / {m['tail']['chord']['t40']:.0f} / {m['tail']['chord']['t60']:.0f} ms (DC out). **Tubby watch:** the tail's MUD (150-400 share over 1.2k+ share) is {m['tailsplit']['chord'][0]['mud']:.0f} / {m['tailsplit']['chord'][1]['mud']:.0f} / {m['tailsplit']['chord'][2]['mud']:.0f} with centroids {m['tailsplit']['chord'][0]['cent']:.0f} / {m['tailsplit']['chord'][1]['cent']:.0f} / {m['tailsplit']['chord'][2]['cent']:.0f} Hz at levels of {m['tailsplit']['chord'][0]['db']:.0f} / {m['tailsplit']['chord'][1]['db']:.0f} / {m['tailsplit']['chord'][2]['db']:.0f} dBFS: it is tubby, as the voice it is fed has nothing above 1.2 kHz (the spring only sees the filtered voice). Spring probes: DRAIN 30 / 55 / 80 and SIZE 50 / 62 / 75 / 90 in `probes.md` (SIZE 62 shortens the tail to 1244 ms at -60 dB).",
          f"  * **Short notes:** the PWM sweep is one LFO period (1 s) long, so a 150 ms note hears {m['pwm_riff']['400-1.2k']:.1f} dB of it in 400-1.2k ({m['pwm_riff']['level']:.1f} dB of level); PHASE SYNC starts each detached note at the same point of the sweep, so every short note has the same timbre. D (2.3 Hz) reads {R['D']['pwm_riff']['400-1.2k']:.1f} dB there. The PWM is a held-note effect.",
          f"  * **Tangle (D):** PWM +-16.8 points (16-50 %) at 2.3 Hz with PHASE SPREAD: the held A2's level moves {R['D']['pwm_a2']['bands']['level'][0]:.1f} dB (B {bp['level'][0]:.1f}), its 150-400 / 400-1.2k depths are {R['D']['pwm_a2']['bands']['150-400'][0]:.1f} / {R['D']['pwm_a2']['bands']['400-1.2k'][0]:.1f} dB; the chord's {R['D']['pwm_chord']['bands']['150-400'][0]:.1f} / {R['D']['pwm_chord']['bands']['400-1.2k'][0]:.1f} (B {m['pwm_chord']['bands']['150-400'][0]:.1f} / {m['pwm_chord']['bands']['400-1.2k'][0]:.1f}). The top of D's sweep is {R['D']['lfo']['pw_hi']:.1f} %: it just touches 50 %.",
          f"  * **CPU:** worst case {m['cost']['idle'] + m['cost']['load']:.0f} host instr/sample (idle {m['cost']['idle']:.0f} + load {m['cost']['load']:.0f}); the original {a['cost']['idle'] + a['cost']['load']:.0f}. The device build was not run.",
          "", "### Recommendation (vocabulary)", "",
          "**B (murk):** dark, raw, murky pulse pad with a PWM you can hear sweep on held notes (1 Hz, one side of 50 %), into a springy tail. If the tail reads too tubby, C (cutoff 98) is the same sweep with a brighter tail and PWM that is as deep in the low band and shallower above; D is the busy, faster, spread version.", "",
          "### Surprising / hard with existing controls", "",
          "* The original's 'PWM' was never PWM: it was the beating of an inverse narrow-pulse pair (this slot shared 10's array).",
          "* PWM depth in 150-400 Hz is a ceiling (about 10 dB here, 12 in 02 D) that no PWM depth or cutoff moved; what the cutoff trades is the upper bands' depth against the tail's MUD.",
          "* Murky against audible is also murky against a clean tail: the spring rings the filtered voice, so a murky patch has a tubby tail (MUD 29 / 39 / 180 over 0-1500 ms; the later windows are at -31 / -52 dBFS).",
          "* A short-note PWM is not possible: the shared LFO's period (1 s at RATE 60) is longer than the notes; LFO DELAY and the rate cannot follow the note.", ""]
    open(os.path.join(DOCS, "12-kelp-tangle.md"), "w").write("\n".join(L) + "\n")


def write_16():
    spec = PATCHES[2]
    d = os.path.join(A.OUT, spec["dir"])
    R = json.load(open(os.path.join(d, "results.json")))
    orig = B.resolve(BASE, 16)
    m, a, c, dd = R["B"], R["A"], R["C"], R["D"]
    L = head(spec, R, "a massive wet chordal wash. Five-voice poly detuned pulses, delay and spring. Threatens to drown the mix. Medium attack, not slow. Vincent's notes: wide polys, wide chorus modulation; medium pulse rates on sine waves (triangle also approved); give options; no square or saw waves; make sure the delay does not get lost; the Fender Twin guides what 'wet' feels like: bright, clear, springy, washy, not punchy; bright and clear by note definition but heavily modulated.",
             "PWM STRINGS (`PF_PWM_STRINGS`, shared with 13 Ghost Board): POLY 5, O1 a 50 % pulse (a SQUARE) and O2 a 31 % pulse 7 cents sharp, a 24 dB low-pass at CUTOFF 75 (988 Hz at C4, 50 % key tracking), a 54 ms attack (measured 3 / 14 / 27 ms), a slow TRI at 0.62 Hz on PWM +-5.5 points in PHASE SPREAD, **LFO PITCH 3 (inert: the law is zero below 12)**, a spring at DRAIN 35, **no delay**. It is very hot (-11.8 dBFS RMS on the wash phrase, peak -0.2) and dark (centroid 593 Hz).",
             "(1) the oscillator: bright pulses against softened toward a triangle (the 'sine' reading); (2) the LFO shape and rate (TRI against smooth RANDOM, medium rates 1.3-2.3 Hz) with the attack (three options: 101 / 160 / 219 ms); (3) the delay against the spring.",
             "there is no sine oscillator and no sine LFO (the TRI is the nearest); no tempo sync; a PWM sweep through 50 % doubles its rate, so no pulse here is a 50 % square; LFO PITCH below 12 is inert; the amp envelope's nominal time is not its 10-90 % time (see below); the spring is fed AFTER the echo, so it rings the repeats; POLY gives each note one voice on one pan position: the width is limited (DUAL is wider and needs 8 voices).",
             "**My reading of the note:** 'sine waves' = the LFO's nearest shape, **TRI** (and **RANDOM**, which is smooth, as the second option); 'medium pulse rates' = **medium LFO rates** (1.3-2.3 Hz here); 'no square or saw waves' = no SQUARE / RAMP / SAW / S&H LFO shapes (none is used), and on the oscillators: **pulses only, never a 50 % square or a saw** (B and C: PW 35 % / 24 %; D: 25 %). The engine has no sine oscillator, so variant D softens the oscillators toward a triangle (narrow pulses through a key-tracking low-pass, as 11 Slapback Strut does). LFO PITCH 3 -> 16 (+-19 cents, a real value); the attack is three options (101 / 160 / 219 ms to 90 %).", orig)
    L += ["### Axes chosen, variants", ""] + variants_table(spec, R) + [""]
    L += changes_block(spec, R, orig)
    L += ["* **Level:** VOLUME %d; **%.1f dBFS RMS** on the wash phrase (s: 2 chords + 3 notes + 3 stabs, echo and spring included, tails excluded); phrase (b) %.1f (%+.1f dB: short stabs do not reach full level through a %.0f ms attack), K-weighted (b) %.1f; peak %.1f dBFS; crest %.1f dB; worst-case CPU %.0f host instr/sample (idle %.0f + load %.0f; the original %.0f). D is peak-limited to %.1f dBFS RMS (VOLUME %d; its peak is -4.4 at that level)." % (
        m["volume"], m["level"], m["b"], m["b"] - m["level"], m["attack"]["voice"]["t90"], m["b_stabs"]["rms_k"], m["peak_all"], m["s_wash"]["crest"], m["cost"]["idle"] + m["cost"]["load"], m["cost"]["idle"], m["cost"]["load"], a["cost"]["idle"] + a["cost"]["load"], dd["level"], dd["volume"]),
          "* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/16-tidal-pull/README.md`, `probes.md`):",
          "  * **Attack (amp envelope, one voice, LFO off):** 10 / 50 / 90 %% of the level at **%.0f / %.0f / %.0f ms** (AA 72, the table's nominal %.0f ms); C %.0f / %.0f / %.0f ms (AA 78); D %.0f / %.0f / %.0f ms (AA 82). **The nominal time is not the attack time: 90 %% arrives at 0.73-0.78 of it and 50 %% at about a third** (`probes.md`). A detuned pair read on its own beats by several dB and moved the plateau the percentages are taken against: it read 87 ms where the envelope alone reads 160 (AA 78): suggests the beating, not isolated; the probe therefore runs with OSC 2 off and VINTAGE 0." % (
              m["attack"]["voice"]["t10"], m["attack"]["voice"]["t50"], m["attack"]["voice"]["t90"], Q.aa_ms(72), c["attack"]["voice"]["t10"], c["attack"]["voice"]["t50"], c["attack"]["voice"]["t90"], dd["attack"]["voice"]["t10"], dd["attack"]["voice"]["t50"], dd["attack"]["voice"]["t90"]),
          f"  * **LFO:** TRI {m['lfo']['hz']:.2f} Hz (RATE 64) on pitch +-{m['lfo']['cents']:.0f} cents (LFO PITCH 16) and on the pulse widths +-{m['lfo']['pts']:.1f} points, PHASE SPREAD; the one-voice probe reads {m['pitch_probe']['sd']:.1f} cents s.d. ({m['pitch_probe']['range']:.1f} cents 5-95 %) at {m['pitch_probe']['rate']:.2f} Hz. C: smooth RANDOM at {c['lfo']['hz']:.2f} Hz (probe {c['pitch_probe']['sd']:.1f} cents s.d.; not periodic, so no rate to read); D: TRI {dd['lfo']['hz']:.2f} Hz on pitch only.",
          f"  * **Width ('wide polys'):** the held chord's L/R correlation is {m['corr'][0]:.2f} dry and {m['corr_full'][0]:.2f} with the echo and spring (the original {a['corr'][0]:.2f}); POLY puts each note on one voice at one pan position. **As DUAL, POLY 8 (a left / right pair per note, a four-note chord uses all eight) it measures 0.38 dry (0.41 full)**: the wider option, not made a variant because the brief is a five-voice poly and the voice count doubles (not costed here).",
          f"  * **Bright / clear / not muddy:** B's chord (dry) centroid {m['chord_dry']['cent']:.0f} Hz, MUD {m['chord_dry']['mud']:.1f}, {m['chord_dry']['shares']['1.2k+']:.1f} % above 1.2 kHz (the original {a['chord_dry']['cent']:.0f} Hz, MUD {a['chord_dry']['mud']:.0f}); its first repeat {m['solo_split']['cent']:.0f} Hz. The tail after the chord: MUD {m['tailsplit'][0]['mud']:.0f} / {m['tailsplit'][1]['mud']:.0f} / {m['tailsplit'][2]['mud']:.0f} at 0-250 / 250-750 / 750-1500 ms (levels {m['tailsplit'][0]['db']:.0f} / {m['tailsplit'][1]['db']:.0f} / {m['tailsplit'][2]['db']:.0f} dBFS), centroids {m['tailsplit'][0]['cent']:.0f} / {m['tailsplit'][1]['cent']:.0f} / {m['tailsplit'][2]['cent']:.0f} Hz: the tail darkens as the BBD takes the top off each repeat; C (more spring, less echo) is brighter in the tail (MUD {c['tailsplit'][0]['mud']:.0f} / {c['tailsplit'][1]['mud']:.0f} / {c['tailsplit'][2]['mud']:.0f}).",
          f"  * **The delay does not get lost:** ALLEY 104 = {m['delay_ms']:.0f} ms, FEEDBK 78, MIX 100, TONE 100, PINGPONG 127. On an isolated 400 ms E4 the first repeat arrives {m['delay_ms']:.0f} ms after the note-on, its peak (the end of the repeated note, {m['first']['t_ms']:.0f} ms) is **{m['first']['dly_re_note']:.1f} dB re the dry note's peak**, the spring in the same window is {m['first']['spr_re_note_same']:.1f} dB re the note, so **the delay is {m['first']['margin']:.1f} dB above the spring** (C: {c['first']['dly_re_note']:.1f} dB, margin {c['first']['margin']:.1f}; D: {dd['first']['dly_re_note']:.1f}, {dd['first']['margin']:.1f}). The repeats fall {' '.join(f'{v:+.1f}' for _, _, v in m['train'])} dB re the first. The echo sits {-m['under']['dly'][0]:.0f} / {-m['under']['dly'][1]:.0f} / {-m['under']['dly'][2]:.0f} dB under the figure's three notes. The spring is in series after the echo (it rings the repeats). Balance table (DLY MIX 70-127 against DRAIN 25-100) in `probes.md`: at MIX 100 the delay stays above the spring up to DRAIN 70 (+2.7 dB) and is level with it at DRAIN 100.",
          f"  * **Spring ('wet' like the Twin: bright, springy, washy):** DRAIN 45 (35 %), SIZE 90, DAMP 35. On the isolated E4 the spring's return re the note is {m['solo_onwin']['spr'][0]['re_dry_db']:.1f} / {m['solo_onwin']['spr'][1]['re_dry_db']:.1f} / {m['solo_onwin']['spr'][2]['re_dry_db']:.1f} dB in 0-20 / 20-100 / 100-250 ms; after the chord's note-off the spring's return is {' / '.join(f'{r['spr']:.1f}' for r in m['ret']['ch1'])} dB re the chord and the delay's {' / '.join(f'{r['dly']:.1f}' for r in m['ret']['ch1'])} dB (0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms). The whole tail is 20 / 40 dB down at {m['tail']['t20']:.0f} / {m['tail']['t40']:.0f} ms and past 2.5 s at -60 dB (a long, washy tail).",
          f"  * **Softened oscillators (D):** the triangle probe on D's OSC 1 through the filter, harmonics 3 / 5 / 7 re the fundamental: **{' / '.join(f'{x:.1f}' for x in dd['tri'])} dB against an ideal triangle's -19.1 / -28.0 / -34.2** (a square is -9.5 / -14.0 / -16.9); B's pulses are -26.0 / -16.1 / -16.9 (a 35 % pulse). What D is and is not: narrow pulses through a key-tracking 12 dB low-pass at 2.0 x the note (CUTOFF 64 = 523 Hz at C4, 100 % key tracking), plus an octave-up pulse the same way: **a triangle-like tone, not a sine** (no filter makes a sine out of this); it is dark (centroid {dd['notes']['cent']:.0f} Hz, {dd['notes']['shares']['1.2k+']:.1f} % above 1.2 kHz, MUD {dd['notes']['mud']:.0f}: by the dictionary's ratio muddy, because a triangle has almost nothing above 1.2 kHz) and its tail MUD is {dd['tailsplit'][0]['mud']:.0f} / {dd['tailsplit'][1]['mud']:.0f} / {dd['tailsplit'][2]['mud']:.0f}. It trades brightness for softness: the 'bright and clear' note and the 'no square or saw' note pull against each other here.",
          f"  * **CPU:** worst case {m['cost']['idle'] + m['cost']['load']:.0f} host instr/sample (idle {m['cost']['idle']:.0f} + load {m['cost']['load']:.0f}); the original {a['cost']['idle'] + a['cost']['load']:.0f}. The device build was not run.",
          "", "### Recommendation (vocabulary)", "",
          "**B (tri):** a bright, wide-ish, heavily modulated pulse wash with a medium (101 ms to 90 %) attack, a clear echo ahead of a springy tail, TRI LFO at 1.26 Hz. C is the RANDOM-LFO, slower-attack, spring-forward reading; D is the soft, triangle-like reading with the slowest attack and the most echo. Mix and match by ear: every difference is one control (LFO SHAPE / RATE, AA, the oscillator block with CUTOFF, DLY MIX, DRAIN).", "",
          "### Surprising / hard with existing controls", "",
          "* The original had no delay and an inert pitch LFO: it was hot (-11.8 dBFS RMS, peak -0.2) and dark (593 Hz).",
          "* The amp envelope's nominal time (the table) is 1.3-1.4x its 90 % time: AA 72 = 137 ms nominal = 101 ms to 90 %.",
          "* 'Wide' is limited in POLY (width 0.70 dry): DUAL doubles the voices for 0.38.",
          "* D is a triangle-like tone and is dark; no brighter softened oscillator exists with one low-pass for both oscillators.", ""]
    open(os.path.join(DOCS, "16-tidal-pull.md"), "w").write("\n".join(L) + "\n")


def write_index():
    L = ["# Batch 4A (Chapter II): 10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull", "",
         "Round 1, rendered, not yet heard. Per patch: `README.md` (variants and numbers), `probes.md` (one control stepped), `results.json`, and (on the listen branch only) the WAVs "
         "`<NN-name>_<KEY>_<phrase>.wav` (A is the original through the base program path; B, C, D are variants over INIT; VOLUME is trimmed to -18.0 dBFS RMS on the patch's own phrase, effects in, tails out). "
         "Phrases: `organ` = q_organ (10), `tangle` = r_tangle (12), `wash` = s_wash (16), `stabs` = b_stabs (the bank's reference phrase); each starts 100 ms before its first note. Method: `dog5-docs/voicing/README.md` section 16.", ""]
    for spec in PATCHES:
        R = json.load(open(os.path.join(A.OUT, spec["dir"], "results.json")))
        L += [f"## {spec['slot']:02d} {spec['name']}", ""] + variants_table(spec, R) + [""]
    open(os.path.join(A.OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    write_10()
    write_12()
    write_16()
    write_index()
    print("logs written")
