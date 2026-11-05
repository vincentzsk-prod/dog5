# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 3A (the decisions).  Each variant = the changes over the patch's ORIGINAL (resolved from the base firmware); VOLUME is trimmed by the run.
Names as in obv_params.h without the P_ prefix.  Enums: WAVE 0 off 1 saw 2 pulse 3 both; MODE 0 poly 1 dual 2 unison 3 mono; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM;
LFO_SHAPE 0 tri 1 saw 2 ramp 3 square 4 S&H 5 random; LFO_PHASE 0 sync 1 free 2 spread."""

# ---- 01 Red Pill ----------------------------------------------------------------------------------------------------
RED_B = dict(MODE=3, O1_WAVE=1, O1_LVL=110, O2_WAVE=1, O2_SEMI=24, O2_LVL=104, O2_FINE=74, GLIDE=0, VINTAGE=10, SPREAD=40,
             CUTOFF=92, RESO=58, FENV_AMT=104, KEYTRK=100, FTYPE=4, DRIVE=88, FA=0, FD=52, FS=30, FR=40,
             AA=0, AD=70, AS=127, AR=26,
             ALLEY=62, DLY_FB=10, DLY_TONE=60, DLY_MIX=30, BBD_SPREAD=0,
             REV_MIX=30, REV_SIZE=40, REV_DAMP=70, REV_PRE=20)
RED_C = {**RED_B, "DRIVE": 110, "GROWL": 46, "GRL_BIAS": 30, "GRL_TONE": 55, "DLY_MIX": 16, "REV_MIX": 18}
RED_D = {**RED_B, "DLY_MIX": 52, "REV_MIX": 52, "REV_SIZE": 55}

# ---- 02 Cement Grind ------------------------------------------------------------------------------------------------
CEM_B = dict(MODE=3, O1_WAVE=2, O1_PW=46, O1_LVL=110, O2_WAVE=2, O2_PW=46, O2_SEMI=24, O2_LVL=104, O2_FINE=74, GLIDE=12,
             LFO_SHAPE=0, LFO_RATE=100, LFO_PHASE=0, LFO_PWM=100, LFO_PWM_TO=2, LFO_FLT=0, LFO_PITCH=0, LFO_DELAY=0,
             CUTOFF=60, RESO=62, FENV_AMT=96, KEYTRK=64, FTYPE=0, DRIVE=78, FA=0, FD=58, FS=45, FR=40,
             AA=1, AD=70, AS=127, AR=20, VINTAGE=30)
CEM_C = {**CEM_B, "LFO_RATE": 90, "LFO_PWM": 120, "O1_PW": 40, "O2_PW": 40, "O2_FINE": 80}
CEM_D = {**CEM_B, "LFO_RATE": 108, "LFO_PWM": 110, "LFO_FLT": 28}

# ---- 06 zzuFuzz -----------------------------------------------------------------------------------------------------
FUZZ_B = dict(MODE=0, POLY_N=6, O1_WAVE=1, O1_LVL=118, O2_WAVE=1, O2_SEMI=24, O2_LVL=118, O2_FINE=76, GLIDE=0, VINTAGE=60, SPREAD=70,
              CUTOFF=88, RESO=80, FENV_AMT=120, KEYTRK=64, FTYPE=4, DRIVE=100, FA=2, FD=58, FS=40, FR=40,
              AA=20, AD=75, AS=127, AR=70,
              GROWL=76, GRL_BIAS=45, GRL_TONE=55, ALLEY=0, DLY_MIX=0, REV_MIX=0, CHEW=0)
FUZZ_C = {**FUZZ_B, "GROWL": 104, "GRL_BIAS": 72, "GRL_TONE": 64}
FUZZ_D = {**FUZZ_B, "MODE": 1, "UNI_DET": 40}

# ---- 08 Wire Bite ---------------------------------------------------------------------------------------------------
WIRE_B = dict(MODE=2, UNI_N=6, UNI_DET=50, O1_WAVE=2, O1_PW=22, O1_LVL=108, O2_WAVE=2, O2_PW=50, O2_SEMI=36, O2_LVL=100, O2_FINE=67,
              GLIDE=0, VINTAGE=127, SPREAD=100,
              LFO_SHAPE=5, LFO_RATE=34, LFO_PHASE=2, LFO_PITCH=16, LFO_DELAY=0, LFO_PITCH_TO=2,
              CUTOFF=80, RESO=60, FENV_AMT=120, KEYTRK=70, FTYPE=0, DRIVE=40, FA=0, FD=44, FS=20, FR=30,
              AA=2, AD=70, AS=127, AR=14,
              DLY_MIX=0, REV_MIX=0)
WIRE_C = {**WIRE_B, "LFO_PITCH": 25, "LFO_RATE": 44}
WIRE_D = {**WIRE_B, "O2_SEMI": 43, "O1_PW": 18, "CUTOFF": 90, "RESO": 66, "FENV_AMT": 124, "FD": 40}


def _worst(B):
    """the loudest the wet return gets against the dry note in each window over the three isolated notes: [0-20, 20-100, 100-250] (dB re dry)"""
    return [max(B["wet"][n][w]["re_dry_db"] for n in range(3)) for w in range(3)]


def _why01(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    wb, wc, wd = _worst(B), _worst(C), _worst(D)
    d0, d88 = P['DRIVE'][0], P['DRIVE'][2]
    return (f"a MONO bass of two saws at the same pitch 7.8 cents apart (beating 0.25 Hz at A1, 0.5 Hz at A2), tight: VINTAGE 10 (the card's wander s.d. {B['vlog']['0'][1]:.1f} cents on a held A2, "
            f"static offset {B['vlog']['0'][0]:+.1f}), no LFO, no glide. A 24 dB low-pass (CUTOFF 92, KEY TRK 100, RESO 58) with a filter envelope that falls in 29 ms: the spit "
            f"(the first 23 ms of the isolated A1 are {B['snap'][0]:.0f} Hz against {B['snap'][1]:.0f} Hz in the next 67 ms), and the per-voice DRIVE at 88 for the grit and the warmth "
            f"(crest factor {d88['crest']:.1f} dB against {d0['crest']:.1f} at DRIVE 0; the centroid hardly moves, {d88['cent']:.0f} against {d0['cent']:.0f} Hz, because the drive sits before the filter). "
            f"Centroid {B['i_spit']['centroid']:.0f} Hz on the spit riff, {B['b_stabs']['centroid']:.0f} Hz on the stabs; {B['i_spit']['bands']['<60']:.0f} % of the riff's energy sits under 60 Hz (the A1 fundamental, 55 Hz). "
            f"The wet is a slap at 80 ms (ALLEY 62, FEEDBK 10, MIX 30) and a short spring (DRAIN 30, SIZE 40): its return is, at the loudest of the three isolated notes, "
            f"{wb[0]:+.1f} / {wb[1]:+.1f} / {wb[2]:+.1f} dB re the dry note in the 0-20 / 20-100 / 100-250 ms windows (every window under the note; the 100-250 ms window, where the 150 ms note is already dying, is the tightest); "
            f"the voice alone is 60 dB down {B['tail_dry']['t60']:.0f} ms after the key-up, with the wet {B['tail']['t60']:.0f} ms. Level {B['level']:.1f} dBFS on the spit riff, {B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f}, "
            f"worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample. C is the grit axis: DRIVE 110 plus GROWL 46 (crest {C['i_spit']['crest']:.1f} dB, and +{(C['cost']['idle'] + C['cost']['load']) - (B['cost']['idle'] + B['cost']['load']):.0f} instr/sample), "
            f"with the wet turned down (worst window {wc[2]:+.1f} dB); D is the wet axis (worst windows {wd[0]:+.1f} / {wd[1]:+.1f} / {wd[2]:+.1f} dB: the echo is nearly as loud as the note in the last window, which is too much).")


def _why02(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    pb = B["pwm"]["bands"]
    return (f"a MONO low-mid grinder: two PULSE oscillators (PW 36 %, 7.8 cents apart) with a triangle LFO on the pulse width at {B['lfo_hz']:.1f} Hz (LFO RATE 100) ±15 points deep (LFO PWM 100), "
            f"restarting with every detached note (LFO PHASE SYNC). Measured on the held A2 the PWM moves the 150-400 Hz band {pb['150-400'][0]:.1f} dB peak to peak at {pb['150-400'][1]:.1f} Hz, the 400-1.2k band {pb['400-1.2k'][0]:.1f} dB, "
            f"the 3k+ band {pb['3k+'][0]:.1f} dB and the overall level {pb['level'][0]:.1f} dB; on the riff's 400 ms notes (about 3 swings in each) {B['pwm_riff']['150-400']:.1f} dB in the 150-400 band, {B['pwm_riff']['400-1.2k']:.1f} dB in 400-1.2k, "
            f"{B['pwm_riff']['level']:.1f} dB of level. The original had no PWM at all (its 0.5 Hz filter wobble moved the same band {A['pwm']['bands']['150-400'][0]:.0f} dB, at {A['pwm']['bands']['150-400'][1]:.1f} Hz). "
            f"The filter is a biting 12 dB low-pass (CUTOFF 60, RESO 62) with an envelope decay of 46 ms (FILTER DECAY 58; the first 23 ms of a riff note are {B['snap'][0]:.0f} Hz against {B['snap'][1]:.0f} Hz after) and a 12-step glide for the skid; DRIVE 78 before the filter for the crunch "
            f"(crest {P['DRIVE'][2]['crest']:.1f} dB against {P['DRIVE'][0]['crest']:.1f} at DRIVE 0). Centroid {B['j_grind']['centroid']:.0f} Hz, {B['j_grind']['bands']['150-400']:.0f} % of the energy at 150-400 Hz. Level {B['level']:.1f} dBFS on the grind riff, "
            f"{B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f}, worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample. C is slower ({C['pwm']['bands']['150-400'][1]:.1f} Hz) and deeper, with narrower pulses and a wider pair (12.5 cents); "
            f"D is faster ({D['pwm']['bands']['150-400'][1]:.1f} Hz) with the filter wobbling at the same rate.")


def _why06(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    so = {r["reso"]: r["diff"] for r in B["selfosc"]}
    return (f"POLY (6 voices), every voice two saws 9 cents apart, both oscillators at full tilt, per-voice DRIVE 100 into GROWL 76 (BIAS 45, TONE 55), the filter open (24 dB, CUTOFF 88, RESO 80) and the amp at full sustain, dry (ALLEY, DRAIN, CHEW 0). "
            f"The wall: the held A2's crest factor is {B['crest_hold']:.1f} dB (GROWL 0 on the same patch: {P['GROWL'][0]['hold_crest']:.1f}; a square wave is 0, a sine 3), and the 3 s hold loses {B['sustain_loss']:.1f} dB from its first to its last half second. "
            f"Attack: AMP ATTACK 20 = 2.4 ms by the engine's time table; measured, the voice alone rises 10-90 % in {B['attack']['voice']['rise']:.1f} ms and the fuzzed note in {B['attack']['as']['rise']:.1f} ms, "
            f"with the level {B['attack']['as']['bloom']['2']:+.1f} dB at 2 ms and {B['attack']['as']['bloom']['10']:+.1f} dB at 10 ms re its plateau (from silence). The tail: -60 dB {B['tail']['t60']:.0f} ms after a 3 s note, {B['chord_tail']['t60']:.0f} ms after the held chord. "
            f"RESO 80 is nowhere near singing: the noise-fed filter answers a 12 dB drop in its input with {so[100]:.1f} dB at RESO 100, {so[115]:.1f} at 115, {so[120]:.1f} at 120, and starts to sing at {so[124]:.1f} at 124 and {so[127]:.1f} at 127. "
            f"Centroid {B['k_wall']['centroid']:.0f} Hz; level {B['level']:.1f} dBFS on the wall phrase, {B['b_stabs']['rms']:.1f} on phrase (b) (the chords of phrase (b) read {B['b_stabs']['rms'] - B['level']:+.1f} dB over the wall phrase), peak {B['peak_all']:.1f}, crest {B['k_wall']['crest']:.1f} dB over the phrase; "
            f"worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample. C is fiercer (GROWL 104, BIAS 72, TONE 64: centroid {C['k_wall']['centroid']:.0f} Hz, hold crest {C['crest_hold']:.1f} dB); D is DUAL (four saws a note: "
            f"{D['cost']['idle'] + D['cost']['load']:.0f} instr/sample, VOLUME {D['volume']}).")


def _why08(R, P):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    v = B["vlog_hold"]
    sd = sum(x[1] for x in v.values()) / len(v)
    return (f"a 6-voice UNISON of narrow pulses (OSC 1 PW 17 %, OSC 2 at 50 % an octave up) in the high register, through a resonant 12 dB low-pass (CUTOFF 80, RESO 60) whose envelope falls in 15 ms (FILTER DECAY 44) to a low sustain (20): a zap at every note start "
            f"(top above 1.2 kHz {B['zap']['burst_db']:+.1f} dB over the body on the held A4, {B['zap_chop']['burst_db']:+.1f} dB on the first bite; centroid {B['zap']['c_attack']:.0f} Hz in the first 23 ms against {B['zap']['c_body']:.0f} Hz after). "
            f"Drift: VINTAGE 127, where the engine's own log gives the six voices static offsets of {min(x[0] for x in v.values()):+.1f} to {max(x[0] for x in v.values()):+.1f} cents and a random-walk wander of {sd:.1f} cents s.d. each "
            f"(ranges {min(x[2] for x in v.values()):+.0f} to {max(x[3] for x in v.values()):+.0f} cents), and a smooth-random LFO on the pitch (LFO RATE 34 = {B['lfo_hz']:.2f} Hz, a new target about every {1 / B['lfo_hz']:.1f} s, "
            f"PHASE SPREAD so each voice sits at another point of the line, LFO PITCH 16 = ±{B['lfo_pitch_cents']:.0f} cents peak). No delay, no spring: chopped, {B['tail_chop']['t40']:.0f} ms to -40 dB after a 110 ms bite. "
            f"Centroid {B['l_wire']['centroid']:.0f} Hz on the wire phrase. Level {B['level']:.1f} dBFS on the wire phrase, {B['b_stabs']['rms']:.1f} on phrase (b), peak {B['peak_all']:.1f}, worst case {B['cost']['idle'] + B['cost']['load']:.0f} host instr/sample "
            f"(the original: {A['cost']['idle'] + A['cost']['load']:.0f} with its delay and spring, peak {A['peak_all']:.1f} dBFS at VOLUME 100). C doubles the pitch LFO (±{C['lfo_pitch_cents']:.0f} cents, {C['lfo_hz']:.2f} Hz); "
            f"D goes up in register and brightness (second oscillator +19 st, CUTOFF 90: centroid {D['l_wire']['centroid']:.0f} Hz) and trades the zap away ({D['zap']['burst_db']:+.1f} dB burst).")


LISTEN01 = """`*_spit.wav` is the one to judge (a sixteenth-note spit riff, then three isolated notes with silence after each: the wet return sits in those gaps), `*_riff.wav` is the pilot's low riff and `*_stabs.wav` the chord phrase.
Listen for: is B tight and stable under a vocal (no wobble), the grit (B against C's RAT-style GROWL), the warmth, and whether the slap and spring in B lift the presence without ever sounding like an effect. D is there to show where 'slight' ends."""
NOTES01 = """*Notes.* Level is read on the note-on region of the spit riff (phrase i); phrase (b) is in the table with the difference. The wet is read per time window on the three isolated notes of phrase (i): the effects' own return (the render minus the same render with the slap and spring off) re the dry note's
RMS in that window; the dry is read as it falls, so the 100-250 ms window of a 150 ms note compares the return with a note that has already ended. The per-voice DRIVE sits before the filter (voices -> DRIVE -> filter), so it adds density and warmth and the later low-pass takes the edge back: the grit that survives is in
the 150-400 Hz band; GROWL (after the filter) is the RAT-style edge, at +578 instr/sample whenever it is on (C). MONO does not re-fire the envelopes on legato: the spit is a detached-note sound. Variant A is rendered through the base program path."""
LISTEN02 = """`*_grind.wav` is the one to judge (eight quarter notes with a long gate, a 2.4 s held A2, three short chops): is the PWM obvious on the riff, is it thick, is the filter biting. `*_riff.wav` and `*_stabs.wav` are the pilot phrases (a chord on a MONO patch plays only the last note).
Listen for: the fast sweep of the pulse widths (B at 7.7 Hz against C's slower 4.7 Hz and D's 11.5 Hz with the filter wobbling), the pair's thickness, the drive crunch, the skid at the start of the notes."""
NOTES02 = """*Notes.* The PWM is read on the held A2 (7.2-9.6 s of phrase j) from the energy of five bands in 20 ms frames (depth = 95th minus 5th percentile in dB, rate = strongest component 0.8-20 Hz of that series); the nominal LFO rate is in the table (RATE 100 = 7.7 Hz) and the measured rate matches it.
Deeper or lower-base settings were tried (LFO PWM 127 with PW 34-36: the depth does not grow past about 12 dB in the 150-400 band, and the sweep crosses 50 % so the timbre cycles at twice the LFO rate, 15 Hz): B's sweep runs 21-51 % (just past 50 % at the top of each swing, the measured rate still equals the LFO's). The pitch of the pair moves with the VINTAGE offset of card 0 only (MONO).
MONO does not re-fire the envelopes on legato (the riff is detached; LFO PHASE SYNC restarts the PWM with each detached note). Variant A is rendered through the base program path."""
LISTEN06 = """`*_wall.wav` is the one to judge: a 3 s held A2 (does the wall hold), a held power chord, three 300 ms power-chord stabs, one low A1 (does it bark). `*_stabs.wav` and `*_riff.wav` are the pilot phrases (the riff is single notes: a fuzz on single low notes is the harsh case).
Listen for: the size of the wall (B against D's DUAL), the sustain, whether C's higher GROWL and BIAS spit or just squash, the very short punch of the strike, and whether the tail after a note is a slight tail or too long."""
NOTES06 = """*Notes.* Level is read on the note-on region of the wall phrase (phrase k) and is a heavily compressed signal: the crest factor of the held note is 2.3 dB (a square is 0 dB, a sine 3), so RMS and peak sit close together and the patch sounds louder than its RMS says, next to a patch with a 9 dB crest at the same RMS;
phrase (b), with its three-note chords, reads about 2 dB hotter than the wall phrase, outside the +-1.5 dB band. GROWL leaves the loudness nearly where it was (its static law and slow trim) so it is the VOLUME that is trimmed. The attack probe strikes a high note (A5, 1.1 ms period) from silence so that the millisecond-scale attack is resolvable; the fuzz stage's loudness trim
makes a note from silence start a little under its plateau. TONE moves the centroid (1251 -> 2051 Hz for 25 -> 90), BIAS only the peak (+0.8 dB for 15 -> 80): the probe tables. Existing controls only: no gate, no octave-up fuzz. Variant A is rendered through the base program path."""
LISTEN08 = """`*_wire.wav` is the one to judge: A4 held 3.5 s (the stack, the drift, the zap of the start), eight 110 ms bites, one low A3. `*_riff.wav` and `*_stabs.wav` are the pilot phrases (a UNISON patch plays one note at a time: chords play the last note).
Listen for: the wander (B against C's deeper pitch LFO), the zap on every note start, whether it is fat or just buzzy, whether the medium-to-high brightness bites without piercing (D is the bright end), and the chop on release."""
NOTES08 = """*Notes.* The cents of drift are the engine's own log of the six voice cards over the held A4 (exact), plus the pitch LFO's law (LFO PITCH 16 = ±19 cents peak; the original's LFO PITCH 10 rounds to 0, so its vibrato never existed). The audio estimate of pitch wander was tried and dropped: the beating of a six-voice stack alone moves the
centroid of its fundamental band by about 8 cents s.d., more than the wander. 'Zap' is the energy above 1.2 kHz in the first 40 ms against the same band in the body (150-300 ms of the held note, 40-100 ms of a bite). UNISON does not re-fire the envelopes on legato: play it detached. The attack from silence (A5 probe) reads about 13 ms to 90 % of the plateau, but the same patch with UNI_N 1 or 2 reads 1.2-1.5 ms: with six detuned voices the sum's level moves a couple of dB with the beating, so the 90 % crossing lands where the beat does; it is not the amp envelope (AMP ATTACK 2 = 0.5 ms). Variant A is rendered through the base program path."""

PATCHES = [
    dict(slot=1, dir="01-red-pill", name="Red Pill", cname="RED_PILL", level="i_spit", level_def="RMS over the note-on region of the spit riff (phrase i)", id="red",
         phrases=["a_riff", "b_stabs", "c_held", "i_spit"], kind="plain", note=(6000, 6150, 55.0), tail=(9300, 10900, 11300, 1500), vlog_off=5400, wet=[6000, 7500, 9000],
         wet_names=["A1 150 ms", "D2 150 ms", "A1 300 ms"], probes=[("DRIVE", [0, 40, 88, 110, 127])], load="a fifth-and-octave chord + a fourth note", recommend="B centre",
         why=_why01, listen=LISTEN01, notes=NOTES01,
         variants=[("A", "original", "the nearest-base patch as it stood (shared with 06 and 27: MONO, saw + pulse an octave down, DRIVE 40, no effects)", {}),
                   ("B", "centre", "detuned saw pair, tight (VINTAGE 10), driven (DRIVE 88), a slight spring and a short slap", RED_B),
                   ("C", "grit", "B along the grit axis: DRIVE 110 and a RAT-style GROWL step (46), less wet", RED_C),
                   ("D", "wet", "B along the wet axis: more slap and spring (the upper limit of 'slight')", RED_D)]),
    dict(slot=2, dir="02-cement-grind", name="Cement Grind", cname="CEMENT_GRIND", level="j_grind", level_def="RMS over the note-on region of the grind riff (phrase j)", id="cem",
         phrases=["a_riff", "b_stabs", "c_held", "j_grind"], kind="plain", note=(3000, 3400, 110.0), tail=(10650, 12300, 12900, 1200), vlog_off=5400, pwm=(7200, 9600), probes=[("DRIVE", [0, 40, 78, 110, 127])],
         load="a fifth-and-octave chord + a fourth note", recommend="B centre", why=_why02, listen=LISTEN02, notes=NOTES02,
         variants=[("A", "original", "the nearest-base patch as it stood (MONO, saw + saw an octave down, a 0.5 Hz filter wobble)", {}),
                   ("B", "centre", "dual pulse, fast PWM, biting LP12, moderate drive", CEM_B),
                   ("C", "slower", "B along the PWM axis: slower and deeper, narrower pulses", CEM_C),
                   ("D", "wobble", "B along the PWM axis: faster, with the filter wobbling at the same rate", CEM_D)]),
    dict(slot=6, dir="06-zzufuzz", name="zzuFuzz", cname="ZZUFUZZ", level="k_wall", level_def="RMS over the note-on region of the wall phrase (phrase k)", id="fuzz",
         phrases=["a_riff", "b_stabs", "c_held", "k_wall"], kind="plain", note=(3000, 6000, 110.0), tail=(6000, 6800, 6950, 800), vlog_off=5400, curve=(3000, 6000), probes=[("GROWL", [0, 28, 40, 55, 76, 100, 127]), ("GRL_TONE", [25, 55, 90]), ("GRL_BIAS", [15, 45, 80])],
         load="a fifth-and-octave chord + a fourth note", recommend="B centre", why=_why06, listen=LISTEN06, notes=NOTES06,
         variants=[("A", "original", "the nearest-base patch as it stood (shared with 01 and 27: MONO, saw + pulse an octave down, DRIVE 40, GROWL 0)", {}),
                   ("B", "centre", "POLY, two detuned saws a voice, DRIVE 100 into GROWL 76, open filter, sustain full, dry", FUZZ_B),
                   ("C", "fiercer", "B along the intensity axis: GROWL 104, BIAS 72, TONE 64", FUZZ_C),
                   ("D", "wall", "B along the wall axis: DUAL (four saws a note)", FUZZ_D)]),
    dict(slot=8, dir="08-wire-bite", name="Wire Bite", cname="WIRE_BITE", level="l_wire", level_def="RMS over the note-on region of the wire phrase (phrase l)", id="wire",
         phrases=["a_riff", "b_stabs", "c_held", "l_wire"], kind="plain", note=(3000, 6500, 440.0), tail=(10300, 11800, 12500, 1200), vlog_off=5400, drift=(3000, 6500, 440.0), chop=7200,
         load="a fifth-and-octave chord + a fourth note", recommend="B centre", why=_why08, listen=LISTEN08, notes=NOTES08,
         variants=[("A", "original", "the nearest-base patch as it stood (6-voice unison, delay and reverb, a pitch LFO that rounds to nothing)", {}),
                   ("B", "centre", "unison of narrow pulses, octave-up second oscillator, resonant zap, random pitch wander, dry and chopped", WIRE_B),
                   ("C", "drift", "B along the drift axis: deeper, faster random pitch wander", WIRE_C),
                   ("D", "zap", "B along the register / zap axis: brighter and zappier, second oscillator +19 st", WIRE_D)]),
]
