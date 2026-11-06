# Batch 4B, 13 Ghost Board, ROUND 2: variants and numbers

Round 2 (6 Nov 2026), **rendered, not yet heard**. The ORIGINAL's voice with round-1 variant D's echo and spring, the tape deck OFF (CHEW 0). Definitions: `dog5-docs/voicing/README.md` section 17. Level phrase `t_ghost`; reference -18.0 dBFS RMS +-1.5, peak <= -4. LFO PITCH 3 against 0, bit-identical renders: {'t_ghost': True, 'b_stabs': True}. WAVs only on the listen branch.

## Variants

* **A2 as-is** (RECOMMENDED, committed): the original's voice (oscillators, filter, envelopes, LFO, VINTAGE, SPREAD) with round-1 D's echo and spring, deck off, LFO PITCH 0.
* **B2 more-top**: A2 with the filter opened: CUTOFF 75 -> 84.
* **C2 no-pwm**: A2 with LFO PWM 0 (no pulse-width movement).
* **D2 no-beat**: A2 with OSC 2 FINE 64 (no detune: no beating).
* **Aorig orig-ref**: the ORIGINAL patch (its own spring, no echo, no deck) re-trimmed to the bank level: render-only reference.
* **D1 round1-D**: round-1 variant D exactly (CHEW 70, CUTOFF 70 voice, its echo and spring): render-only reference.

## Numbers

| | A2 as-is | B2 more-top | C2 no-pwm | D2 no-beat | Aorig orig-ref | D1 round1-D |
|---|---|---|---|---|---|---|
| VOLUME | 55 | 54 | 55 | 73 | 75 | 62 |
| level, ghost phrase (t) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -18.04 | -18.07 | -17.97 | -19.99 | -17.94 | -17.88 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -23.5 / -5.5 | -23.5 / -5.5 | -23.4 / -5.5 | -21.7 / -1.7 | -18.9 / -1.0 | -23.4 / -5.5 |
| peak of the own phrase (dBFS) / whole renders incl. (b) (limit -4 on the own phrase) | -5.0 / -5.0 | -4.8 / -4.8 | -4.9 / -4.9 | -4.3 / -4.3 | -4.5 / -4.5 | -5.0 / -5.0 |
| clipped samples in all renders | 0 | 0 | 0 | 0 | 0 | 0 |
| crest factor, own phrase (dB) | 13.0 | 13.3 | 13.1 | 15.7 | 13.5 | 12.9 |
| K-weighted RMS, (b) (dBFS) | -24.2 | -24.1 | -24.1 | -22.2 | -19.6 | -24.0 |
| note-on region: centroid (Hz) | 564 | 731 | 562 | 686 | 605 | 812 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 0 / 74 / 25 / 0 | 0 / 0 / 73 / 26 / 1 | 0 / 0 / 74 / 25 / 0 | 0 / 0 / 71 / 28 / 2 | 0 / 0 / 78 / 22 / 1 | 0 / 0 / 72 / 26 / 1 |
| MUD = share(150-400) / share(1.2k+), note-on region | 278.5 | 81.9 | 314.9 | 46.8 | 109.8 | 49.3 |
| worst-case CPU (host instr/sample: idle + load) | 2084 (1180 + 905) | 2084 (1180 + 904) | 2084 (1180 + 905) | 2084 (1180 + 904) | 2069 (1164 + 905) | 2680 (1948 + 731) |
| harmonics 3 / 5 / 7 re the fundamental, OSC 1 through the filter at rest (dB; triangle -19.1 / -28.0 / -34.2) | -10.9 / -18.5 / -26.1 | -10.0 / -15.5 / -20.1 | -10.9 / -18.5 / -26.1 | -10.9 / -18.5 / -26.1 | -10.9 / -18.5 / -26.1 | -14.4 / -23.2 / -32.0 |
| MOVEMENT, one held voice A3, sends and deck off: band-energy depth dB / strongest rate Hz in 150-400 | 13.8 / 0.9 | 13.8 / 0.9 | 13.6 / 0.9 | 0.3 / 0.8 | 13.8 / 0.9 | 0.0 / 20.0 |
| same in 400-1.2k | 3.9 / 2.4 | 4.0 / 2.3 | 1.2 / 2.7 | 3.1 / 0.8 | 3.9 / 2.4 | 0.0 / 20.0 |
| same, the broadband level | 10.2 / 0.9 | 9.4 / 0.9 | 9.0 / 0.9 | 0.9 / 0.8 | 10.1 / 0.9 | 0.4 / 18.7 |
| same on the held chord (dry), 150-400 / 400-1.2k depth dB | 6.0 / 5.0 | 6.0 / 4.9 | 6.2 / 4.7 | 6.3 / 5.0 | 5.9 / 5.1 | 4.9 / 2.7 |
| filter / CUTOFF (Hz at C4) / key tracking % / RESO | LP24 / 75 (988) / 50 / 5 | LP24 / 84 (1661) / 50 / 5 | LP24 / 75 (988) / 50 / 5 | LP24 / 75 (988) / 50 / 5 | LP24 / 75 (988) / 50 / 5 | LP12 / 70 (740) / 100 / 0 |
| LFO PWM / OSC 2 FINE (cents) / LFO PITCH / CHEW | 60 / 73 (+7.0) / 0 / 0 | 60 / 73 (+7.0) / 0 / 0 | 0 / 73 (+7.0) / 0 / 0 | 60 / 64 (+0.0) / 0 / 0 | 60 / 73 (+7.0) / 3 / 0 | 0 / 64 (+0.0) / 0 / 70 |
| echo: ALLEY (ms) / FEEDBK / MIX; spring DRAIN / SIZE / DAMP | 337 / 95 / 105; 70 / 100 / 25 | 337 / 95 / 105; 70 / 100 / 25 | 337 / 95 / 105; 70 / 100 / 25 | 337 / 95 / 105; 70 / 100 / 25 | 10 / 50 / 0; 35 / 100 / 60 | 337 / 95 / 105; 70 / 100 / 25 |
| first repeat of an isolated 150 ms E4: peak re the note (dB) / at ms after the note-on | -8.6 / 491 | -8.7 / 466 | -8.7 / 460 | -8.8 / 385 | - / -20 | -8.8 / 374 |
| the echo's margin over the spring in that window (dB) | 10.1 | 9.1 | 10.3 | 9.4 | - | 9.4 |
| the repeats 1..6 (dB re the first) | +0.0 -3.1 -6.1 -9.2 -12.3 -15.6 | +0.0 -3.1 -6.2 -9.2 -12.4 -15.6 | +0.0 -3.0 -6.0 -9.1 -12.3 -15.6 | +0.0 -3.2 -5.9 -9.0 -12.3 -15.5 | +0.0 +0.0 +0.0 +0.0 +0.0 +0.0 | +0.0 -3.3 -6.7 -10.1 -13.6 -17.0 |
| echo return after the held chord's note-off (dB re the chord) 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms | -5.7 / -6.1 / -6.2 / -9.3 / -16.0 | -5.8 / -6.2 / -6.3 / -9.5 / -16.2 | -5.6 / -6.1 / -6.2 / -9.4 / -16.0 | -5.2 / -5.0 / -5.9 / -9.2 / -15.9 | - / - / - / - / - | -6.0 / -6.1 / -7.2 / -10.8 / -17.7 |
| spring return, same windows (dB) | 6.2 / 3.3 / -2.3 / -9.8 / -27.1 | 6.0 / 3.1 / -2.2 / -9.6 / -26.8 | 6.1 / 3.2 / -2.1 / -9.2 / -26.5 | -0.9 / -2.4 / -6.0 / -13.9 / -31.1 | -0.2 / -3.1 / -8.0 / -15.0 / -31.6 | 4.5 / 2.5 / -2.2 / -11.4 / -29.0 |
| the tail after the chord: MUD / centroid Hz / level dBFS in 0-250 / 250-750 / 750-1500 ms | 1370 / 491 / -15 ; 2302 / 512 / -19 ; 3233 / 530 / -26 | 328 / 605 / -15 ; 611 / 591 / -19 ; 1009 / 574 / -27 | 1108 / 488 / -15 ; 2198 / 509 / -19 ; 3331 / 528 / -26 | 212 / 578 / -18 ; 463 / 564 / -22 ; 695 / 581 / -29 | 1021 / 479 / -17 ; 2376 / 538 / -26 ; 5592 / 803 / -41 | 225 / 757 / -15 ; 298 / 851 / -20 ; 305 / 1231 / -27 |
| tail after the held chord to -20 / -40 / -60 dB (ms, DC out) | 1670 / >win / >win | 1686 / >win / >win | 1686 / >win / >win | 1650 / >win / >win | 770 / 1460 / 1990 | 1644 / >win / >win |

## Parameter changes against the ORIGINAL (before -> after); the echo and spring values are round-1 D's

### A2 as-is

* LFO_PITCH 3 -> 0 (-2%)
* VOLUME 100 -> 55 (-35%)
* DLY_FB 50 -> 95 (+35%)
* DLY_MIX 0 -> 105 (+83%)
* REV_DAMP 60 -> 25 (-28%)
* REV_MIX 35 -> 70 (+28%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

### B2 more-top

* CUTOFF 75 -> 84 (+7%) (988 Hz -> 1661 Hz)
* LFO_PITCH 3 -> 0 (-2%)
* VOLUME 100 -> 54 (-36%)
* DLY_FB 50 -> 95 (+35%)
* DLY_MIX 0 -> 105 (+83%)
* REV_DAMP 60 -> 25 (-28%)
* REV_MIX 35 -> 70 (+28%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

B2 against A2:

* CUTOFF 75 -> 84 (+7%) (988 Hz -> 1661 Hz)

### C2 no-pwm

* LFO_PITCH 3 -> 0 (-2%)
* LFO_PWM 60 -> 0 (-47%)
* VOLUME 100 -> 55 (-35%)
* DLY_FB 50 -> 95 (+35%)
* DLY_MIX 0 -> 105 (+83%)
* REV_DAMP 60 -> 25 (-28%)
* REV_MIX 35 -> 70 (+28%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

C2 against A2:

* LFO_PWM 60 -> 0 (-47%)

### D2 no-beat

* O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)
* LFO_PITCH 3 -> 0 (-2%)
* VOLUME 100 -> 73 (-21%)
* DLY_FB 50 -> 95 (+35%)
* DLY_MIX 0 -> 105 (+83%)
* REV_DAMP 60 -> 25 (-28%)
* REV_MIX 35 -> 70 (+28%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

D2 against A2:

* O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)

### the echo and spring copied from round-1 D (value = D = what A2 has; the original's value in brackets)

* DLY_TIME 3 (3)
* DLY_FB 95 (50)
* DLY_TONE 70 (70)
* DLY_MIX 105 (0)
* ALLEY 104 (0)
* ALLEY_FINE 0 (0)
* BBD_SPREAD 127 (127)
* REV_SIZE 100 (100)
* REV_DAMP 25 (60)
* REV_PRE 20 (20)
* REV_MIX 70 (35)
