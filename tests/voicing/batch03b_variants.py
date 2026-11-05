# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 3B, "the wreck and chop set" (05 ZEAROX, 07 Tape Splice, 15 Trem Chop): the decisions.  Each variant = the changes over the patch's
ORIGINAL (resolved from the base firmware); VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix.
Enums: WAVE 0 off 1 saw 2 pulse 3 both; MODE 0 poly 1 dual 2 unison 3 mono; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM;
LFO_SHAPE 0 tri 1 saw 2 ramp 3 square 4 S&H 5 random; LFO_PHASE 0 sync 1 free 2 spread; LFO_PITCH_TO 0 osc1 1 osc2 2 both; TP_WOWFLT 0 wow only .. 127 flutter only."""

# ---- 05 ZEAROX ------------------------------------------------------------------------------------------------------------------------
# a kick substitute: O1 pulse = the sub at the note's own pitch (the bonus), O2 saw an octave UP = the body (60-400 Hz), swept down by ENV>O2 (the filter envelope
# drives the O2 pitch: the 808 chirp), NOISE through the same fast filter envelope = the click, CHEW at the top = the cassette overload
ZEA_B = dict(MODE=3, GLIDE=0, O1_WAVE=2, O1_LVL=90, O2_WAVE=1, O2_SEMI=36, O2_LVL=127, ENV_O2=110, NOISE=50,
             CUTOFF=65, RESO=10, FENV_AMT=120, KEYTRK=20, FA=0, FD=58, FS=0, AA=0, AD=82, AS=0, AR=30,
             CHEW=127, TP_HISS=0, GROWL=104, GRL_BIAS=72, GRL_TONE=64)
ZEA_C = {**ZEA_B, "O1_LVL": 70, "AD": 86, "NOISE": 110, "CUTOFF": 80, "FENV_AMT": 127, "FD": 44, "ENV_O2": 127}
ZEA_D = {**ZEA_B, "GROWL": 55, "GRL_BIAS": 40, "GRL_TONE": 50}

# ---- 07 Tape Splice -------------------------------------------------------------------------------------------------------------------
# two square pulses a few cents apart (the fat square), OSC 2 -> OSC 1 linear FM (X-MOD: this engine's OSC B -> OSC A cross-mod), a smooth-random pitch LFO on
# both oscillators (the nervous wobble), a fast release (the chop), CHEW as the splice: wow / flutter / dropouts at the note edges
SPL_B = dict(MODE=3, O1_WAVE=2, O2_WAVE=2, O2_SEMI=24, O2_FINE=68, XMOD=70, GLIDE=0, CUTOFF=60, DRIVE=40,
             LFO_SHAPE=5, LFO_RATE=94, LFO_PHASE=1, LFO_PITCH=16, LFO_PITCH_TO=2,
             FS=60, AA=2, AD=70, AS=100, AR=25, CHEW=80, TP_HISS=0, TP_DROPS=90)
SPL_C = {**SPL_B, "XMOD": 100, "LFO_PITCH": 22, "CHEW": 127, "TP_DROPS": 110}
SPL_D = {**SPL_B, "XMOD": 40, "LFO_PITCH": 12, "CHEW": 30, "TP_DROPS": 64}

# ---- 15 Trem Chop ---------------------------------------------------------------------------------------------------------------------
# a bright saw pair through a SQUARE LFO on the amp (AMP 127 = full level / -42 dB, a hard gate), LFO PHASE SYNC (every detached note starts the chop ON), a touch of slop
CHOP_B = dict(MODE=3, O1_WAVE=1, O1_LVL=127, O2_WAVE=1, O2_LVL=127, O2_FINE=69, LFO_SHAPE=3, LFO_RATE=101, LFO_AMP=127, LFO_PITCH=0, LFO_PHASE=0, LFO_DELAY=0,
              DLY_MIX=0, GLIDE=0, CUTOFF=95, DRIVE=60, AS=127, VINTAGE=60)
CHOP_C = {**CHOP_B, "LFO_PHASE": 1}
CHOP_D = {**CHOP_B, "MODE": 1, "POLY_N": 6, "LFO_PHASE": 2}


def _ph(*a):
    return list(a)


PATCHES = [
    dict(slot=5, dir="05-zearox", name="ZEAROX", cname="ZEAROX", level="m_kick", level_def="RMS over the note-on region of the kick phrase (phrase m: 11 hits x 150 ms)",
         phrases=["a_riff", "b_stabs", "c_held", "m_kick"], kind="plain", recommend="B blown", load="a fifth-and-octave chord + a fourth note",
         variants=[("A", "original", "the nearest-base patch as it stood (shared with 19 Blackwater: MONO, pulse + a saw an octave down, CUTOFF 35: sub only, no effects)", {}),
                   ("B", "blown", "the kick lives in the body and is blown: sub + an octave-up saw swept down by the filter envelope, a noise click, GROWL 104 / BIAS 72 / TONE 64 and CHEW at the top", ZEA_B),
                   ("C", "click", "B along the where-it-lives axis: the click leads (more noise, a brighter and faster filter envelope, less sub)", ZEA_C),
                   ("D", "tamer", "B along the overload axis: GROWL 55 (BIAS 40, TONE 50), CHEW still at the top", ZEA_D)]),
    dict(slot=7, dir="07-tape-splice", name="Tape Splice", cname="TAPE_SPLICE", level="n_splice", level_def="RMS over the note-on region of the splice phrase (phrase n)",
         phrases=["a_riff", "b_stabs", "c_held", "n_splice"], kind="plain", recommend="B centre", load="a fifth-and-octave chord + a fourth note",
         variants=[("A", "original", "the nearest-base patch as it stood (MONO, saw + saw a fourth down, X-MOD 90, DRIVE 40, no tape)", {}),
                   ("B", "centre", "fat square pair, cross-mod, random pitch LFO, tape degrade at 80", SPL_B),
                   ("C", "glitchy", "B along the glitch axis: X-MOD 100, pitch LFO 22, CHEW 127 with more dropouts", SPL_C),
                   ("D", "gentle", "B along the glitch axis: X-MOD 40, CHEW 30", SPL_D)]),
    dict(slot=15, dir="15-trem-chop", name="Trem Chop", cname="TREM_CHOP", level="o_chop", level_def="RMS over the note-on region of the chop phrase (phrase o), off parts of the chop included",
         phrases=["a_riff", "b_stabs", "c_held", "o_chop", "p_chopshort"], kind="plain", recommend="B centre", load="a fifth-and-octave chord + a fourth note",
         variants=[("A", "original", "the nearest-base patch as it stood (shared with nobody: MONO square lead, delay, LFO PITCH 8 inert)", {}),
                   ("B", "centre", "bright saw pair, SQUARE LFO on the amp at 8.1 Hz, every note starts the chop ON (LFO PHASE SYNC), dry", CHOP_B),
                   ("C", "free", "B along the wavering axis: LFO PHASE FREE (the chop runs on, whatever the note does: a note can begin in an off part)", CHOP_C),
                   ("D", "smeared", "B along the wavering axis: DUAL with LFO PHASE SPREAD (the two voices of a note chop an eighth of a cycle apart)", CHOP_D)]),
]


# ---- the texts (numbers come from the run) ---------------------------------------------------------------------------------------------
def _ms(v):
    return 0.5 * 20000 ** (v / 127)


def _above(w, i0=1):
    return sum(w[i0:])


def _why05(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    pb = B["params"]
    k1, k0, k2 = B["kick"]["A1"], B["kick"]["A0"], B["kick"]["A2"]
    gr0 = {r[0]: r[1] for r in P["GROWL"][1]}["0"][2]
    return (f"MONO, three layers in one voice. THE SUB: OSC 1 pulse at the note's own pitch (LEVEL {pb['O1_LVL']}); the original was this plus a saw an octave down and nothing else (sub only: {A['level']:.1f} dBFS on the kick phrase at VOLUME 100, "
            f"{A['small']['100']:.1f} dB of it left after a 100 Hz high-pass, no energy above 400 Hz). THE BODY: OSC 2 saw an octave UP (SEMI +12) at LEVEL {pb['O2_LVL']}, swept down by the filter envelope through ENV>O2 {pb['ENV_O2']} "
            f"(+{(pb['ENV_O2'] - 64) * 97 / 256:.0f} st at the strike, falling over FILTER DECAY {pb['FD']} = {_ms(pb['FD']):.0f} ms): the 808-style chirp, and it puts the pitch in the 60-400 Hz bands. THE CLICK: NOISE {pb['NOISE']} through the same fast filter "
            f"envelope (CUTOFF {pb['CUTOFF']}, ENV AMT {pb['FENV_AMT']}, SUSTAIN 0, KEY TRK {pb['KEYTRK']} so a low note is not darker than a high one). The amp is a drum's: attack 0.5 ms, DECAY {pb['AD']} (= {_ms(pb['AD']):.0f} ms), SUSTAIN 0, "
            f"RELEASE {pb['AR']}. THE OVERLOAD: GROWL {pb['GROWL']} (BIAS {pb['GRL_BIAS']}, TONE {pb['GRL_TONE']}) and CHEW {pb['CHEW']}, HISS 0. "
            f"Where the kick lives on the isolated A1 hit (share of the energy above 60 Hz in the click / body / tail windows): B {' / '.join(f'{_above(w):.0f}' for w in k1['wins'])} %, the original {' / '.join(f'{_above(w):.0f}' for w in A['kick']['A1']['wins'])} %; "
            f"the click window (0-10 ms) has {_above(k1['wins'][0], 3):.0f} % of its energy above 400 Hz (the original: 0), the body window {k1['wins'][1][2]:.0f} % at 150-400 Hz and {k1['wins'][1][1]:.0f} % at 60-150 Hz, the true sub (under 60 Hz) {k1['wins'][1][0]:.0f} % of the body. "
            f"On A0 the energy above 60 Hz is {' / '.join(f'{_above(w):.0f}' for w in k0['wins'])} % (click / body / tail) and on A2 {' / '.join(f'{_above(w):.0f}' for w in k2['wins'])} %. The click is spectral, not a level spike: the first 5 ms of an A1 hit sit {k1['click_re_body']:+.1f} dB against the body (the original: {A['kick']['A1']['click_re_body']:+.1f}), and the hit reaches 90 % of its peak at {B['hit_attack']['A1']['t90']:.0f} ms (the sub beating with the swept body); a click that spiked over the body would need a quieter body, which the {-18.0} dBFS level over a 150 ms gate does not leave room for (README section 8). A small speaker that stops at 100 Hz keeps {B['small']['100']:.1f} dB of the kick phrase "
            f"(the original {A['small']['100']:.1f}). Level {B['level']:.1f} dBFS on the kick phrase, {B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f} dBFS, crest {B['m_kick']['crest']:.1f} dB over the phrase; the first 30 ms of an A1 hit have a crest of "
            f"{B['hit_crest30']['A1']:.1f} dB (GROWL 0 on this patch: {gr0}; a sine is 3). Worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample (the original {A['cost']['idle'] + A['cost']['load']:.0f}): CHEW costs {B['cost']['idle'] - B['cost']['no_chew']:.0f}, GROWL {B['cost']['idle'] - B['cost']['no_growl']:.0f}. "
            f"C puts the click first (click above 400 Hz: {_above(C['kick']['A1']['wins'][0], 3):.0f} % on A1, the sub down from {pb['O1_LVL']} to {C['params']['O1_LVL']}), D is the tamer overload (GROWL {D['params']['GROWL']}: hit crest {D['hit_crest30']['A1']:.1f} dB, click above 400 Hz {_above(D['kick']['A1']['wins'][0], 3):.0f} % on A1).")


LISTEN05 = """`*_kick.wav` is the one to judge: three isolated hits (A0, A1, A2) with a second of silence after each, then four hits a bar at 120 BPM. `*_riff.wav` / `*_stabs.wav` / `*_held.wav` are the pilot phrases (a MONO patch plays the last note of a chord; a kick held for 2.4 s decays by itself).
Listen for: whether A1 and A2 read as a kick and not as a bass note (the chirp and the click), whether A0 gives anything but air, how blown B is against D, and whether C's click is a click or a hiss. Play it on the small speaker."""
def _notes05(R, P):
    B = R["B"]
    ch = {r[0]: r[1] for r in P["CHEW"][1]}
    hs = {r[0]: r[1] for r in P["TP_HISS"][1]}
    gr = {r[0]: r[1] for r in P["GROWL"][1]}
    o1 = {r[0]: r[1] for r in P["O1_LVL"][1]}
    return (f"""*Notes.* Level is read on the note-on region of the kick phrase (11 hits x 150 ms), a short transient sound; crest factor over that region is in the table, and the crest of the first 30 ms of each hit is the overload reading (sine 3 dB, saw 4.8, a flattened wave lower). The band windows start at each hit's real onset (the host quantises note events to its blocks, so the sound begins up to a few ms either side of the nominal time).
'Small speaker' = a zero-phase 2nd-order high-pass at 60 / 100 Hz on the whole phrase: the level that remains against the unfiltered one. **Noise:** the voice NOISE goes through the filter and the amp envelope, so it stops with the note (B's isolated A1 hit is 60 dB down {B['tail']['t60']:.0f} ms after the key-up, the voice alone {B['tail_voice']['t60']:.0f} ms); the TAPE hiss (HISS, 0 here) is
not gated: it comes up with CHEW, stays about 2 s after the last note and then fades (the HISS probe, dBFS right after the last note / at +2.4 s: HISS 32 {hs['32'][-1]}, HISS 64 {hs['64'][-1]}, HISS 96 {hs['96'][-1]}; a hit is at -18). **CHEW at the top changes little in the numbers here:** with CHEW 0 / 127 the level reading moves {ch['127'][0]} against {ch['0'][0]} dBFS, the first-30-ms crest {ch['0'][2]} -> {ch['127'][2]} dB,
the click's share above 400 Hz {ch['0'][4]} -> {ch['127'][4]} %; the dropout probe (48 hits, 24 s, DROPS at its default 64) found {B['drops']['n3']} hits more than 3 dB under the median. What it adds that these numbers do not show (wow, flutter, head loss) is untested by ear. The flattening is GROWL's (the GROWL probe: crest {gr['0'][2]} at 0, {gr['76'][2]} at 76, {gr['104'][2]} at 104). The sub is OSC 1 LEVEL (the O1_LVL probe: 50 -> 110 moves the energy under 60 Hz from {o1['50'][5].split(' / ')[0]} to {o1['110'][5].split(' / ')[0]} %, all at the same level reading after VOLUME).
**The tape's effect on A0:** a 27.5 Hz fundamental is inaudible on a small speaker whatever is done to it; what is heard on A0 is the swept body and the GROWL harmonics (energy above 60 Hz in the body window: {B['kick']['A0']['wins'][1] and 100 - B['kick']['A0']['wins'][1][0]:.0f} %).""")


def _why07(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    xm = {r[0]: r[1] for r in P["XMOD"][1]}
    ch = {r[0]: r[1] for r in P["CHEW"][1]}
    sub = lambda k: xm[k][5].split(" / ")[0]
    pb = B["params"]
    pr = B["pair"][""]["onset"]
    return (f"MONO: two 50 % pulses a unison apart, 3.1 cents (OSC 2 FINE {pb['O2_FINE']}), the fat square, into a 24 dB low-pass (CUTOFF {pb['CUTOFF']}, per-voice DRIVE {pb['DRIVE']}); OSC 2 frequency-modulates OSC 1 (X-MOD {pb['XMOD']}: this engine's OSC B -> OSC A cross-mod; "
            f"there is no separate Poly-Mod, X-MOD is the closest control; the original's was 90). THE NERVOUS WOBBLE: a smooth-random LFO on both oscillators' pitch (RATE {pb['LFO_RATE']} = {B['lfo_hz']:.1f} Hz, a new target about every {1 / B['lfo_hz'] * 1000:.0f} ms, "
            f"PITCH {pb['LFO_PITCH']} = +-{((pb['LFO_PITCH'] ** 2) >> 7) * 9.4:.0f} cents peak, PHASE FREE). Measured on the held A2 the pitch track has a s.d. of {B['wobble']['sd']:.1f} cents ({B['wobble']['range']:.0f} cents 5-95 %), of which the tape adds {B['wobble']['sd'] - B['wobble_notape']['sd']:+.1f}; "
            f"X-MOD does not move the measured pitch in any clear way (the X-MOD probe: pitch s.d. {min(float(v[0].split(' · ')[0]) for v in xm.values()):.1f}-{max(float(v[0].split(' · ')[0]) for v in xm.values()):.1f} cents across X-MOD 0-127, with no order to it); what it adds, measurably, is energy BELOW the note: the share of the held A2's energy under 60 Hz is {sub('0')} / {sub('40')} / {sub('70')} / {sub('100')} / {sub('127')} % at X-MOD 0 / 40 / 70 / 100 / 127 (this suggests FM sidebands; not isolated). THE CHOP: AMP ATTACK 2, DECAY 70 to SUSTAIN 100, RELEASE {pb['AR']} (= {_ms(pb['AR']):.0f} ms), so a 60 ms note is 40 dB down {B['tail_short']['t40']:.0f} ms after the key-up and 60 dB down at {B['tail_short']['t60']:.0f} ms. "
            f"THE SPLICE: CHEW {pb['CHEW']} (HISS 0, DROPS {pb['TP_DROPS']}): the tape stage delays every note by {pr['mean']:+.1f} ms on average with a per-note jitter of {pr['sd']:.2f} ms s.d. ({pr['min']:+.1f} .. {pr['max']:+.1f} ms over the 12 staccato notes) at the onset and "
            f"{B['pair']['']['end']['mean']:+.1f} ms +-{B['pair']['']['end']['sd']:.1f} at the end of a note; dips of 6 dB or more in a 12 s hold (the CHEW probe, n · deepest dB): {ch['0'][3]} at CHEW 0, {ch['30'][3]} at 30, {ch['60'][3]} at 60, {ch['100'][3]} at 100, {ch['127'][3]} at 127. Level {B['level']:.1f} dBFS on the splice phrase, {B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f}, "
            f"crest {B['n_splice']['crest']:.1f} dB, centroid {B['n_splice']['centroid']:.0f} Hz (the original {A['n_splice']['centroid']:.0f}); worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample (the original {A['cost']['idle'] + A['cost']['load']:.0f}). "
            f"C turns X-MOD, the pitch LFO and the tape up (wobble s.d. {C['wobble']['sd']:.0f} cents, {C['dips'][1]} dips in the held note); D turns them down (wobble s.d. {D['wobble']['sd']:.0f} cents).")


LISTEN07 = """`*_splice.wav` is the one to judge: twelve staccato sixteenths, a 2.4 s held A2 (the wobble, the timbre of the cross-mod, any dropout), three short A3 notes. `*_riff.wav` / `*_stabs.wav` are the pilot phrases (MONO: a chord plays its last note).
Listen for: whether B is nervous without being out of tune, whether the chop is short enough to sound broken, how often the tape drops the sound (C), and what the cross-mod adds against D."""
NOTES07 = """*Notes.* The pitch wobble is an autocorrelation track of the held A2 (40 ms frames, a 10 ms hop; frames with a weak peak are dropped: the original's rough FM tone keeps 56 % of them, so its 57 cents s.d. is an unreliable number and is marked so). 'Without the tape' re-renders the same variant with CHEW 0, so the difference is the tape's own. The edge timing is the 1 ms peak envelope: onset = note-on to
-20 dB of the note's body, end = note-off to -40 dB of the body; the tape's contribution is the per-note difference between the two renders. **There is no Poly-Mod in this engine:** X-MOD is OSC 2 -> OSC 1 linear FM (square law, `(d*d)>>7`); the modulator is taken before OSC 2's level knob, so OSC 2 LEVEL 0 would still modulate (read in the code, **untested**). ENV>O2 (the filter envelope on OSC 2's pitch) makes the FM sweep with each
note (the original used neither). The dips in a held note are counted in a separate 12 s hold probe; with DROPS 0 the same 4 dips remain at CHEW 60, so those are not the dropouts (cause not isolated); the deeper and more numerous dips at CHEW 100-127 suggest dropouts (the count and depth grow with CHEW). MONO does not re-fire the envelopes on legato: play the chop detached."""


def _why15(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    pb = B["params"]
    c, e = B["chop"], B["edge"]
    return (f"MONO: two bright saws 3.9 cents apart, both oscillators at LEVEL 127, the 24 dB low-pass open (CUTOFF {pb['CUTOFF']}, DRIVE {pb['DRIVE']}), amp SUSTAIN 127, no delay (the original's 1/8 delay at MIX 30 is removed: a choice to keep the chop dry; on a held note it changed the depth by 0.1 dB in a trial render). THE CHOP: the LFO is a SQUARE at RATE {pb['LFO_RATE']} = {B['lfo_hz']:.2f} Hz, "
            f"AMP 127 (the amp law is `1 - AMP/256 x (1 - lfo)`: full level for the high half, 1/128 = -42 dB for the low half, never exactly silent). Measured on the held A3: rate {c['rate']:.2f} Hz, on {c['on_db']:.1f} / off {c['off_db']:.1f} dBFS, "
            f"depth {c['depth']:.1f} dB, on {c['duty'] * 100:.0f} % of the cycle; the edge rises 10-90 % in {e['median']:.2f} ms on an A6 probe (the reading is limited by its one-period window, 0.57 ms; the engine's own amp ramp across a 16-sample block is 0.36 ms): a hard gate, not a tremolo. "
            f"LFO PITCH was 8, inert (the law is (d*d)>>7 = 0 below 12); it is now 0 (the first real value, 12, would put a square +-9 cent pitch step on every edge; untested). LFO PHASE SYNC: every detached note starts the chop ON "
            f"(phrase p: {B['first']['n_on']} of {B['first']['n']} notes start ON, the first edge at {B['first']['mean']:.0f} ms +-{B['first']['sd']:.1f} after the note-on); a legato note in MONO slides without restarting it. **The wavering:** the edge timing is tidy: s.d. of the rising edges about a straight line {c['edge_sd']:.2f} ms "
            f"(the reading's resolution is 0.5 ms), the period s.d. {c['period_sd']:.2f} ms, and VINTAGE does not move it (0 / 60 / 127: 0.18 / 0.24 / 0.16 ms in the VINTAGE probe): VINTAGE 60 wanders the pitch and cutoff, not the LFO. What does waver the edges is in the other variants: C lets the chop free-run "
            f"({C['first']['n_on']} of {C['first']['n']} notes start ON at this rate and phase, the first edge slides {C['first']['vals'][0]:.0f} -> {C['first']['vals'][-1]:.0f} ms over the phrase), D puts the two voices of each note an eighth of a cycle apart (rise {D['edge']['median']:.1f} ms; the held note spends {D['levels3'][0]:.0f} % of the time off, {D['levels3'][1]:.0f} % at one voice's level, {D['levels3'][2]:.0f} % at full, B: {B['levels3'][0]:.0f} / {B['levels3'][1]:.0f} / {B['levels3'][2]:.0f} %). Level {B['level']:.1f} dBFS on the chop phrase "
            f"(off parts included), {B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f}, crest {B['o_chop']['crest']:.1f} dB, centroid {B['o_chop']['centroid']:.0f} Hz; worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample (the original {A['cost']['idle'] + A['cost']['load']:.0f}).")


LISTEN15 = """`*_chop.wav` is the one to judge (a 2.4 s held A3, a six-note riff of long notes, the chord A3+E4+A4: a MONO patch plays its last note, D plays all three), `*_chopshort.wav` has eight 110 ms notes and four 240 ms notes (the chop against the gate), `*_riff.wav` / `*_stabs.wav` / `*_held.wav` are the pilot phrases.
Listen for: how hard the edges are (B), whether C's free-running chop (a note can start in an off part) is broken or just unreliable, and whether D's two-voice smear is a stutter or a mush."""
NOTES15 = """*Notes.* Chop figures are read on the held A3 (3.3-5.3 s of phrase o) from a 2 ms RMS envelope: ON = the median of the upper half, OFF = the median of the lowest tenth, depth = ON - OFF; edges = the midpoint crossings. **Tempo:** the LFO has NO tempo sync: its rate is the RATE knob alone (`0.05 x 600^(RATE/127)` Hz, a step is about 5 %). The tempo (GLOBAL page, a MIDI clock, REC tap on the BBD page) drives the arp, the delay's SYNC and ALLEY, never the LFO. Nearest RATE bytes
(cycles per second; one cycle = one on and one off): 90 BPM quarter / eighth / sixteenth = 1.5 / 3.0 / 6.0 Hz = RATE 68 (1.54) / 81 (2.96) / 95 (5.99); 120 BPM = 2.0 / 4.0 / 8.0 Hz = RATE 73 (1.98) / 87 (4.00) / 101 (8.10); 140 BPM = 2.33 / 4.67 / 9.33 Hz = RATE 76 (2.30) / 90 (4.65) / 104 (9.42). A byte can be up to 2.5 % off the tempo, so a free-running chop slides against a long phrase (8.10 Hz against 120 BPM eighths drifts 3 ms a step; the phrase p
reading with LFO PHASE FREE shows it). The nearest thing to a lock the existing controls give is LFO PHASE SYNC (the first key of a detached note restarts the LFO, so the chop is aligned to each note, not to the beat). **A free chop at a tempo-matched rate can start every note OFF** (C, phrase p at 120 BPM: all eight notes begin in an off part and the first edge slides 46 -> 24 ms; where it starts depends on where the free-running LFO happens to be): the reason B is SYNC. LFO DELAY would fade the chop in (untested here).
The shape options (all one shared LFO): SQUARE = the hard on/off used; RAMP / SAW = one hard edge and one linear ramp per cycle (a rising or falling swell; untested here); S&H = a random level at each step; TRI = the gentle tremolo not wanted; RANDOM = a smooth wander. Only SQUARE was rendered in the variants; the others are read from the LFO code (`lfo_shape`) and **untested here**."""



for _p in PATCHES:
    _p["why"], _p["listen"], _p["notes"] = {5: (_why05, LISTEN05, _notes05), 7: (_why07, LISTEN07, NOTES07), 15: (_why15, LISTEN15, NOTES15)}[_p["slot"]]
