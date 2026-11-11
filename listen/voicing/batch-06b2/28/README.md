# 28 Bell Tolls, Batch 6B2 round 2: the top grit (rendered, not yet heard)

**Brief change, logged:** a clean base with no top grit; Vincent's premise ('it is coming from the CHEW and GROWL') was **not in the patch** (below). Round 1 (Batch 6B) stays as the record: variants B / C / D = 2.1 / 4.1 / 6.0 s rings, the shimmer on C and D.

## The correction: there is no CHEW, GROWL or DRIVE in any 6B variant

* The committed array of 6B round 1 (`ad8345c`, `PF_BELL_XMOD`) carries **no** `P_CHEW`, `P_GROWL` or `P_DRIVE` entry (0 of its 27 entries; the original array neither), and the resolved parameters of every variant read GROWL 0, CHEW 0, DRIVE 0 (`base.json`, `params`). The variants differ in the voice (X-MOD, levels, filter), the envelopes, the shimmer, the echo and the spring only.
* The CPU says the same: base variant C reads 2017 host instr/sample; CHEW 45 adds +783 and GROWL 44 +595 (the 6B figures: +784 and +595): none of that is in the base.
* So removing CHEW and halving GROWL would change nothing. The grit is somewhere else; this round finds where.

## Verdict in short (numbers below; Vincent's ear decides)

* **Where the grit comes from: the FM.** X-MOD 64 with OSC 2 at the inharmonic tierce ratio (+15 st = 2.378x) makes inharmonic sidebands: 13-18 spectral peaks within -30 dB that are not on the key's harmonic series or the tierce (the original array's +19 st = 3.0x is a harmonic ratio: 0-6) and a noise-like floor in 2-10 kHz (flatness at A4, 100-400 ms: C -17.2 dB, the original -27.2, X-MOD 0 -35.5, OSC 1 alone -39.2). With the FM off the five classical partials, the ring and the 150 Hz / 800 Hz / 4 kHz energy shares do not move (ladder within 0.1 dB, ring within 0.8 %, shares within 0.1 pp): **what Vincent likes underneath is not in the FM**.
* **Not the source:** the echo and spring (dry: flatness -17.5), VINTAGE, SPREAD, the shimmer (none moves the flatness by more than 0.7 dB; the echo accounts for 3 of the 13 off-ladder peaks), the engine's saturators (the voice mix never clamps, no sample reaches full scale, the filter's soft state acts on 0.15 % of the voice samples and 0.02 % in the first 100 ms at A4, the output tanh compresses a few thousand samples by more than 0.1 dB, a few hundred by more than 0.35 dB at the chord's peaks and by about 1.0 dB at its highest input; halving the mixer levels with the saturations at zero (VOLUME at its maximum, the level 9 dB lower) left every proxy at A4 within 0.4 dB) and the oscillator's aliasing (real but at 14-19 kHz, -26 dB re the energy above 4 kHz in an open-filter test; in the patch the share above 14 kHz is 0.08 % at A4, 1.0 % at A6 in the first 100 ms and is not separable from the saw's real harmonics there: **not isolated**). **OSC 2's LEVEL 0 does not remove the FM** (the modulator is taken before its level): `o2_off` keeps the grit (flatness -17.0); only `o1only` (LEVEL 0 and X-MOD 0) removes both.
* **The fix: X-MOD 64 -> 32** (one value, the same in B2 / C2 / D2). Flatness at A4 100-400 ms -17.2 -> -25.9 dB (-8.7 dB; -6.8 dB at A3, -10.1 dB at A6), off-ladder peaks 13 -> 3 (A4, 100-400 ms), the 20-100 ms flatness -10.1 -> -17.2. **It does not reach the second target: the share above 4 kHz moves by only -0.6 .. +0.3 dB** (a 6 dB fall is a quarter of the share: 4.6 % -> 1.1 % at A4 in the strike), because that share is the saw's harmonics through the open filter at the strike, not FM.
* **Where crisp and bell-like trade.** (1) X-MOD 0 is the cleanest (flatness -35.5, off-ladder 4) and leaves the ring, the ladder and the energy shares untouched (its wet returns were not measured), but the 100-400 ms centroid falls 13.7 % (A4) against a +-10 % limit: the sidebands are part of the strike's body, and a real bell carries more inharmonic partials than the five of the ladder (general knowledge, not measured here), so some of the FM is bell-like, not only grit; X-MOD 32 is the lowest round value inside the limit (-9.2 % at A4). (2) A 6 dB fall of the share above 4 kHz in the body needs the filter lower (CUTOFF 80: -4.7 dB at 100-400 ms, -9.4 dB at 1-2 s at A4, but the centroid falls 26 % and the 150-800 Hz share rises 2.6 pp): that is the strike's top, the part that reads as crisp or as bright, and it is the part a bell's definition lives in. **Not done in B2 / C2 / D2; cal6 (C2 with CUTOFF 84) lets Vincent hear one step of it.**

## 1. The grit baseline (the Batch 6B variants rendered again with this kit: the ring times and levels reproduce the 6B figures exactly)

| var | VOLUME | toll (ar) dB | chord dB | peak dBFS | CPU | ring A4 to -6 / -12 / -20 / -40 ms |
|---|---|---|---|---|---|---|
| A | 127 | -20.91 | -25.0 | -4.30 | 1855 | 256 / 400 / 709 / 1287 |
| B | 113 | -20.11 | -24.0 | -4.07 | 1910 | 298 / 612 / 1034 / 2069 |
| C | 108 | -19.73 | -22.2 | -4.09 | 2017 | 648 / 1218 / 2147 / 4062 |
| D | 100 | -19.97 | -21.8 | -4.08 | 2118 | 900 / 1895 / 3096 / 5979 |

Proxies (a number, not a verdict): the share of the energy above 4 kHz and in 2-8 kHz; the spectral flatness over 2-10 kHz (geometric over arithmetic mean of the averaged power spectrum: 0 dB is a flat, noise-like floor, a large negative number is a few clean partials); the count of spectral peaks within -30 dB (and -20 dB) of the strongest that are neither on the key's harmonic series (+-0.06 f0) nor the bell's tierce (2.4 x the key, +-3 %); the crest factor of the dry output.

| var | note | window | >4 kHz % | 2-8 kHz % | flatness 2-10 kHz dB | off-ladder partials within -30 / -20 dB | RMS dB |
|---|---|---|---|---|---|---|---|
| A | A3 | 0-20 ms | 4.45 | 10.1 | -5.2 | - | -17.3 |
| A | A3 | 20-100 ms | 3.21 | 8.5 | -18.5 | 5 / 0 | -17.5 |
| A | A3 | 100-400 ms | 1.85 | 5.9 | -22.2 | 2 / 0 | -22.0 |
| A | A3 | 1-2 s | 0.20 | 2.3 | -17.6 | 6 / 0 | -55.3 |
| A | A4 | 0-20 ms | 9.09 | 17.0 | -12.8 | - | -17.3 |
| A | A4 | 20-100 ms | 8.56 | 17.0 | -24.1 | 1 / 0 | -18.8 |
| A | A4 | 100-400 ms | 5.05 | 17.8 | -27.2 | 0 / 0 | -23.0 |
| A | A4 | 1-2 s | 1.17 | 12.0 | -23.6 | 5 / 1 | -56.6 |
| A | A6 | 0-20 ms | 53.89 | 52.6 | -26.1 | - | -17.8 |
| A | A6 | 20-100 ms | 52.94 | 49.4 | -28.7 | 0 / 0 | -19.3 |
| A | A6 | 100-400 ms | 53.19 | 53.8 | -29.7 | 0 / 0 | -23.5 |
| A | A6 | 1-2 s | 44.60 | 55.2 | -27.0 | 0 / 0 | -58.6 |
| B | A3 | 0-20 ms | 1.89 | 5.2 | -2.8 | - | -17.2 |
| B | A3 | 20-100 ms | 1.55 | 4.9 | -4.7 | 18 / 1 | -18.3 |
| B | A3 | 100-400 ms | 0.43 | 3.2 | -11.7 | 16 / 1 | -21.7 |
| B | A3 | 1-2 s | 0.05 | 1.5 | -20.7 | 12 / 1 | -42.6 |
| B | A4 | 0-20 ms | 4.56 | 11.6 | -3.4 | - | -17.2 |
| B | A4 | 20-100 ms | 4.19 | 11.6 | -10.1 | 18 / 1 | -18.3 |
| B | A4 | 100-400 ms | 1.91 | 9.3 | -17.0 | 13 / 1 | -21.7 |
| B | A4 | 1-2 s | 0.51 | 6.5 | -25.2 | 8 / 1 | -42.8 |
| B | A6 | 0-20 ms | 21.18 | 30.2 | -15.7 | - | -17.7 |
| B | A6 | 20-100 ms | 21.83 | 28.7 | -22.9 | 5 / 1 | -18.6 |
| B | A6 | 100-400 ms | 16.89 | 26.6 | -24.7 | 3 / 1 | -21.4 |
| B | A6 | 1-2 s | 10.80 | 24.1 | -26.8 | 2 / 0 | -42.0 |
| C | A3 | 0-20 ms | 1.89 | 5.2 | -2.8 | - | -18.5 |
| C | A3 | 20-100 ms | 1.54 | 4.9 | -4.7 | 18 / 1 | -19.2 |
| C | A3 | 100-400 ms | 0.40 | 3.1 | -11.9 | 16 / 1 | -21.1 |
| C | A3 | 1-2 s | 0.05 | 1.5 | -19.5 | 4 / 1 | -32.0 |
| C | A4 | 0-20 ms | 4.58 | 11.7 | -3.4 | - | -18.5 |
| C | A4 | 20-100 ms | 4.19 | 11.6 | -10.1 | 18 / 1 | -19.2 |
| C | A4 | 100-400 ms | 1.83 | 9.2 | -17.2 | 13 / 1 | -21.1 |
| C | A4 | 1-2 s | 0.49 | 6.3 | -21.1 | 3 / 0 | -32.1 |
| C | A6 | 0-20 ms | 21.26 | 30.3 | -15.7 | - | -19.0 |
| C | A6 | 20-100 ms | 21.86 | 28.8 | -22.9 | 5 / 1 | -19.5 |
| C | A6 | 100-400 ms | 16.96 | 26.9 | -24.8 | 3 / 1 | -20.8 |
| C | A6 | 1-2 s | 13.00 | 27.4 | -24.0 | 2 / 0 | -32.5 |
| D | A3 | 0-20 ms | 1.89 | 5.3 | -2.8 | - | -19.8 |
| D | A3 | 20-100 ms | 1.61 | 5.1 | -4.7 | 20 / 1 | -20.4 |
| D | A3 | 100-400 ms | 0.41 | 3.3 | -12.1 | 17 / 1 | -21.7 |
| D | A3 | 1-2 s | 0.05 | 1.6 | -19.6 | 4 / 1 | -29.4 |
| D | A4 | 0-20 ms | 4.59 | 11.7 | -3.4 | - | -19.8 |
| D | A4 | 20-100 ms | 4.36 | 11.9 | -10.0 | 19 / 1 | -20.3 |
| D | A4 | 100-400 ms | 1.89 | 9.3 | -16.9 | 12 / 1 | -21.6 |
| D | A4 | 1-2 s | 0.50 | 6.6 | -20.9 | 4 / 0 | -29.4 |
| D | A6 | 0-20 ms | 21.35 | 30.4 | -15.7 | - | -20.3 |
| D | A6 | 20-100 ms | 22.40 | 28.0 | -22.5 | 5 / 1 | -20.6 |
| D | A6 | 100-400 ms | 15.95 | 25.6 | -24.6 | 3 / 0 | -21.0 |
| D | A6 | 1-2 s | 12.70 | 26.9 | -23.8 | 2 / 0 | -29.5 |

### Crest, clipping and where the engine's own saturators act (instrumented host)

The engine's chain: voice mix (hard clamp at +-65535, a headroom of 2x), the filter's band-pass state (linear below +-0.75 of full scale, soft above: `svf_step`), the output stage (`softclip`, a tanh: x/32768 -> 0.76 at 32768; 0.1 dB of compression from an input of about 6000 = -14.7 dBFS, 0.5 dB at about 13000), the effects' 16-bit clip (`sat16`).

| var | note | crest, dry, strike 0-400 ms / the note | dry peak dBFS | filter state saturating, % of voice samples (whole note / first 100 ms) | mix clamp (hard) | output tanh: samples input over 6000 (0.1 dB) / 12000 / 20000, max input | samples at full scale |
|---|---|---|---|---|---|---|---|
| A | A3 | 13.2 / 21.8 dB | -7.8 | 0.05 / 0.00 | 0 | 1792 / 14 / 0, 14105 | 0 (all phrases) |
| A | A4 | 13.3 / 21.9 dB | -8.1 | 0.10 / 0.00 | 0 | 1721 / 17 / 0, 13581 | 0 (all phrases) |
| A | A6 | 14.3 / 22.8 dB | -8.2 | 0.25 / 0.00 | 0 | 1107 / 13 / 0, 13494 | 0 (all phrases) |
| B | A3 | 11.4 / 19.3 dB | -8.9 | 0.07 / 0.02 | 0 | 2228 / 2 / 0, 12333 | 0 (all phrases) |
| B | A4 | 12.0 / 19.9 dB | -8.4 | 0.13 / 0.02 | 0 | 2140 / 3 / 0, 13132 | 0 (all phrases) |
| B | A6 | 12.3 / 20.3 dB | -8.4 | 0.37 / 0.00 | 0 | 1851 / 4 / 0, 13053 | 0 (all phrases) |
| C | A3 | 10.3 / 16.5 dB | -10.0 | 0.08 / 0.02 | 0 | 2179 / 0 / 0, 10762 | 0 (all phrases) |
| C | A4 | 10.7 / 17.0 dB | -9.6 | 0.15 / 0.02 | 0 | 2046 / 0 / 0, 11254 | 0 (all phrases) |
| C | A6 | 11.0 / 17.4 dB | -9.8 | 0.39 / 0.00 | 0 | 1638 / 0 / 0, 11053 | 0 (all phrases) |
| D | A3 | 9.9 / 15.1 dB | -11.1 | 0.08 / 0.02 | 0 | 1295 / 0 / 0, 9332 | 0 (all phrases) |
| D | A4 | 10.3 / 15.6 dB | -10.8 | 0.15 / 0.02 | 0 | 1185 / 0 / 0, 9702 | 0 (all phrases) |
| D | A6 | 10.5 / 15.9 dB | -11.0 | 0.39 / 0.00 | 0 | 855 / 0 / 0, 9494 | 0 (all phrases) |

## 2. Where the grit comes from (the isolation set on C, one change at a time, each re-fitted to -18.0 dBFS on the toll)

| key | what | VOLUME | toll dB | peak | CPU | A4 >4 kHz % 0-20 / 20-100 / 100-400 / 1-2 s | flatness A4 / A3 / A6 (100-400 ms) | off-ladder A4 (-30 dB, 100-400) | crest A4 strike | filter-state sat % |
|---|---|---|---|---|---|---|---|---|---|---|
| C | C, round 1 | 108 | -19.73 | -4.09 | 2017 | 4.58 / 4.19 / 1.83 / 0.49 | -17.2 / -11.9 / -24.8 | 13 | 10.7 | 0.15 |
| xmod0 | X-MOD 64 -> 0 (no FM) | 117 | -18.41 | -4.03 | 1965 | 4.02 / 4.32 / 1.84 / 0.47 | -35.5 / -29.9 / -45.7 | 4 | 10.8 | 0.15 |
| xmod32 | X-MOD 64 -> 32 | 113 | -19.00 | -4.03 | 2017 | 4.03 / 4.21 / 1.64 / 0.45 | -25.9 / -18.7 / -34.9 | 3 | 10.9 | 0.14 |
| o2_35 | OSC 2 LEVEL 70 -> 35 | 114 | -19.13 | -4.08 | 2017 | 4.04 / 3.67 / 1.58 / 0.40 | -16.6 / -11.5 / -24.3 | 10 | 9.8 | 0.02 |
| o2_off | OSC 2 off (LEVEL 0) | 115 | -19.00 | -4.11 | 2017 | 4.01 / 3.65 / 1.56 / 0.39 | -17.0 / -11.5 / -24.5 | 9 | 9.6 | 0.00 |
| o1only | OSC 1 alone (OSC 2 LEVEL 0, X-MOD 0) | 122 | -18.02 | -4.08 | 1965 | 3.93 / 3.59 / 1.56 / 0.37 | -39.2 / -33.4 / -49.4 | 0 | 9.6 | 0.00 |
| cut72 | CUTOFF 88 -> 72 | 121 | -18.42 | -4.05 | 2017 | 2.05 / 1.13 / 0.10 / 0.00 | -28.0 / -24.7 / -28.0 | 5 | 10.2 | 0.26 |
| envamt64 | ENV AMT 88 -> 64 | 110 | -20.16 | -4.08 | 2017 | 0.04 / 0.04 / 0.04 / 0.04 | -32.0 / -27.0 / -30.0 | 5 | 9.1 | 0.25 |
| fd75 | FILTER DECAY 90 -> 75 | 108 | -19.91 | -4.09 | 2016 | 4.39 / 2.17 / 0.60 / 0.49 | -22.5 / -19.4 / -25.8 | 9 | 10.9 | 0.15 |
| vint0 | VINTAGE 20 -> 0 | 110 | -19.46 | -4.07 | 2021 | 4.54 / 4.23 / 1.96 / 0.51 | -17.9 / -11.7 / -27.2 | 14 | 10.7 | 0.14 |
| spread0 | SPREAD 70 -> 0 | 114 | -18.77 | -4.09 | 2017 | 4.58 / 4.19 / 1.83 / 0.49 | -17.2 / -11.9 / -24.8 | 13 | 9.0 | 0.15 |
| noshim | no LFO shimmer (the C extras off) | 104 | -19.58 | -4.06 | 2017 | 4.58 / 4.19 / 1.83 / 0.50 | -17.2 / -11.9 / -24.8 | 13 | 10.7 | 0.15 |
| dry | echo and spring off (MIX 0) | 115 | -18.79 | -4.00 | 2001 | 4.57 / 3.95 / 1.70 / 0.46 | -17.5 / -11.8 / -25.0 | 10 | 10.7 | 0.15 |
| head | mixer headroom: OSC 1 LEVEL 127 -> 64, OSC 2 70 -> 35 (VOLUME re-fitted) | 127 | -28.80 | -12.38 | 2017 | 4.56 / 4.15 / 1.80 / 0.48 | -17.1 / -11.9 / -24.7 | 13 | 10.9 | 0.00 |
| c2cut84 | C2 (X-MOD 32) with CUTOFF 88 -> 84: the second axis, the strike's top trimmed | 112 | -19.26 | -4.11 | 2017 | 3.88 / 3.49 / 1.04 / 0.17 | -27.8 / -21.4 / -35.0 | 3 | 11.0 | 0.18 |

What each does to the bell (A4; the ladder is dB re the strongest partial, first 300 ms: hum / prime / tierce / quint / nominal; the ring is to -6 / -12 / -20 / -40 dB; the centroid and the shares are the strike's body):

| key | ladder | ring | centroid 100-400 ms Hz (change) | shares 150-800 / 800-4k / >4k over 0-400 ms (pp change) |
|---|---|---|---|---|
| C | +0.0 / -6.9 / -10.7 / -9.5 / -11.9 | 648 / 1218 / 2147 / 4062 | 2635 (+0.0 %) | 60.8 / 36.7 / 2.52 (+0.0 / +0.0 / +0.00) |
| xmod0 | +0.0 / -6.9 / -10.7 / -9.5 / -11.8 | 648 / 1223 / 2147 / 4067 | 2276 (-13.6 %) | 60.8 / 36.8 / 2.47 (-0.0 / +0.1 / -0.04) |
| xmod32 | +0.0 / -7.1 / -10.9 / -10.3 / -13.2 | 649 / 1225 / 2132 / 4066 | 2395 (-9.1 %) | 62.8 / 34.8 / 2.38 (+2.1 / -1.9 / -0.13) |
| o2_35 | +0.0 / -6.9 / -23.2 / -9.6 / -11.9 | 648 / 1223 / 2154 / 4067 | 2643 (+0.3 %) | 65.4 / 32.4 / 2.16 (+4.6 / -4.3 / -0.36) |
| o2_off | +0.0 / -6.9 / - / -9.6 / -11.9 | 648 / 1223 / 2156 / 4069 | 2660 (+1.0 %) | 65.7 / 32.2 / 2.13 (+4.9 / -4.5 / -0.38) |
| o1only | +0.0 / -6.9 / - / -9.5 / -11.8 | 648 / 1223 / 2161 / 4076 | 2182 (-17.2 %) | 65.7 / 32.2 / 2.10 (+4.9 / -4.5 / -0.42) |
| cut72 | +0.0 / -7.3 / -11.0 / -10.3 / -13.1 | 521 / 1139 / 2069 / 3985 | 1439 (-45.4 %) | 67.7 / 32.0 / 0.32 (+6.9 / -4.7 / -2.20) |
| envamt64 | +0.0 / -7.3 / -11.5 / -10.8 / -14.4 | 707 / 1255 / 2202 / 4099 | 1335 (-49.3 %) | 70.2 / 29.8 / 0.04 (+9.4 / -6.9 / -2.48) |
| fd75 | +0.0 / -7.1 / -10.8 / -9.9 / -12.4 | 648 / 1223 / 2149 / 4062 | 1937 (-26.5 %) | 63.7 / 35.4 / 0.90 (+2.9 / -1.3 / -1.62) |
| vint0 | +0.0 / -6.4 / -10.8 / -9.6 / -12.2 | 670 / 1222 / 2122 / 4095 | 2669 (+1.3 %) | 60.0 / 37.4 / 2.63 (-0.8 / +0.7 / +0.11) |
| spread0 | +0.0 / -6.9 / -10.7 / -9.5 / -11.9 | 666 / 1237 / 2138 / 4083 | 2637 (+0.1 %) | 60.8 / 36.7 / 2.52 (+0.0 / -0.0 / -0.00) |
| noshim | +0.0 / -6.9 / -10.7 / -9.5 / -11.9 | 576 / 1214 / 2076 / 4071 | 2635 (+0.0 %) | 60.8 / 36.7 / 2.52 (+0.0 / -0.0 / -0.00) |
| dry | +0.0 / -6.2 / -10.6 / -9.8 / -12.6 | 677 / 1255 / 2039 / 4092 | 2607 (-1.1 %) | 60.3 / 37.3 / 2.40 (-0.5 / +0.6 / -0.11) |
| head | +0.0 / -6.9 / -11.2 / -9.5 / -11.8 | 641 / 1207 / 2131 / 4058 | 2633 (-0.1 %) | 61.1 / 36.4 / 2.49 (+0.3 / -0.3 / -0.03) |
| c2cut84 | +0.0 / -7.1 / -10.9 / -10.4 / -13.4 | 624 / 1209 / 2125 / 4048 | 2078 (-21.1 %) | 64.0 / 34.3 / 1.72 (+3.2 / -2.4 / -0.79) |

### Does the oscillator alias? (OSC 1 alone, a saw, the filter open, VINTAGE 0, effects off; the energy off the harmonic series k f0 +-6 Hz)

| note | f0 Hz | off-harmonic energy re the whole, dB | re the energy above 4 kHz, dB | >4 kHz % | strongest off-harmonic peaks: Hz, dB re the fundamental, the harmonic it reflects (fs - k f0) |
|---|---|---|---|---|---|
| A2 | 110.02 | -53.2 | -32.7 | 0.83 | 10980.0 Hz -58.2 dB (k 301); 21960.0 Hz -66.9 dB (k None); 116.3 Hz -68.5 dB (k None) |
| A3 | 219.96 | -43.4 | -26.5 | 2.01 | 17260.0 Hz -55.6 dB (k 122); 17480.0 Hz -55.6 dB (k 121); 17920.0 Hz -55.7 dB (k 119) |
| A4 | 440.00 | -40.5 | -26.5 | 3.90 | 18140.0 Hz -49.7 dB (k 59); 17700.0 Hz -49.7 dB (k 60); 18580.0 Hz -49.9 dB (k 58) |
| A5 | 880.00 | -37.4 | -26.8 | 8.72 | 17700.0 Hz -43.7 dB (k 30); 18580.0 Hz -43.9 dB (k 29); 16820.0 Hz -44.1 dB (k 31) |
| A6 | 1760.00 | -34.1 | -26.0 | 15.49 | 17700.0 Hz -37.5 dB (k 15); 15940.0 Hz -38.9 dB (k 16); 19460.0 Hz -39.7 dB (k 14) |
| A7 | 3520.01 | -30.4 | -24.4 | 24.90 | 15940.0 Hz -32.8 dB (k 8); 19460.0 Hz -33.5 dB (k 7); 12420.0 Hz -37.8 dB (k 9) |

## 3. Candidates B2 / C2 / D2: the grit fix is X-MOD 64 -> 32, applied identically (A = the original array, level-matched)

| var | VOLUME | toll (ar) | chord | peak (all phrases) | clipped samples | CPU | what |
|---|---|---|---|---|---|---|---|
| A | 127 | -20.91 | -25.0 | -4.30 | 0 | 1855 | the original, level-matched |
| B2 | 114 | -19.97 | -23.9 | -4.09 | 0 | 1910 | B (round 1) with X-MOD 32 |
| C2 | 113 | -19.00 | -21.6 | -4.03 | 0 | 2017 | C (round 1) with X-MOD 32 |
| D2 | 105 | -19.13 | -21.0 | -4.03 | 0 | 2118 | D (round 1) with X-MOD 32 |

**Every change over the original array (percent = of the parameter's range):**

* **B2:** O1_LVL 100 -> 127 (+21%); O2_LVL 100 -> 70 (-24%); O2_SEMI 43 -> 39 (-8%); XMOD 70 -> 32 (-30%); O2_FINE 70 -> 64 (-5%); CUTOFF 100 -> 88 (-9%); RESO 20 -> 0 (-16%); FENV_AMT 94 -> 88 (-5%); FA 20 -> 0 (-16%); FS 0 -> 30 (+24%); FR 60 -> 70 (+8%); AA 1 -> 0 (-1%); AD 95 -> 102 (+6%); AR 80 -> 102 (+17%); LFO_PHASE FREE -> SYNC; VINTAGE 30 -> 20 (-8%); SPREAD 60 -> 70 (+8%); DLY_FB 50 -> 25 (-20%); DLY_TONE 70 -> 80 (+8%); DLY_MIX 40 -> 30 (-8%); REV_SIZE 110 -> 70 (-31%); REV_DAMP 60 -> 35 (-20%); REV_PRE 20 -> 15 (-4%); REV_MIX 45 -> 20 (-20%); ALLEY 0 -> 80 (+63%); VOLUME 100 -> 114; against round 1's B: X-MOD 64 -> 32, VOLUME 113 -> 114
* **C2:** O1_LVL 100 -> 127 (+21%); O2_LVL 100 -> 70 (-24%); O2_SEMI 43 -> 39 (-8%); XMOD 70 -> 32 (-30%); O2_FINE 70 -> 64 (-5%); CUTOFF 100 -> 88 (-9%); RESO 20 -> 0 (-16%); FENV_AMT 94 -> 88 (-5%); FA 20 -> 0 (-16%); FS 0 -> 30 (+24%); FR 60 -> 70 (+8%); AA 1 -> 0 (-1%); AD 95 -> 111 (+13%); AR 80 -> 111 (+24%); LFO_RATE 70 -> 40 (-24%); LFO_DELAY 0 -> 35 (+28%); LFO_PHASE FREE -> SYNC; LFO_PITCH 0 -> 14 (+11%); LFO_AMP 0 -> 20 (+16%); VINTAGE 30 -> 20 (-8%); SPREAD 60 -> 70 (+8%); DLY_FB 50 -> 25 (-20%); DLY_TONE 70 -> 80 (+8%); DLY_MIX 40 -> 30 (-8%); REV_SIZE 110 -> 70 (-31%); REV_DAMP 60 -> 35 (-20%); REV_PRE 20 -> 15 (-4%); REV_MIX 45 -> 20 (-20%); ALLEY 0 -> 80 (+63%); VOLUME 100 -> 113; against round 1's C: X-MOD 64 -> 32, VOLUME 108 -> 113
* **D2:** O1_LVL 100 -> 127 (+21%); O2_LVL 100 -> 70 (-24%); O2_SEMI 43 -> 39 (-8%); XMOD 70 -> 32 (-30%); O2_FINE 70 -> 64 (-5%); CUTOFF 100 -> 88 (-9%); RESO 20 -> 0 (-16%); FENV_AMT 94 -> 88 (-5%); FA 20 -> 0 (-16%); FS 0 -> 30 (+24%); FR 60 -> 70 (+8%); AA 1 -> 0 (-1%); AD 95 -> 116 (+17%); AR 80 -> 116 (+28%); LFO_RATE 70 -> 40 (-24%); LFO_DELAY 0 -> 35 (+28%); LFO_PHASE FREE -> SYNC; LFO_PITCH 0 -> 14 (+11%); LFO_AMP 0 -> 20 (+16%); VINTAGE 30 -> 20 (-8%); SPREAD 60 -> 70 (+8%); DLY_FB 50 -> 25 (-20%); DLY_TONE 70 -> 80 (+8%); DLY_MIX 40 -> 45 (+4%); REV_SIZE 110 -> 70 (-31%); REV_DAMP 60 -> 35 (-20%); REV_PRE 20 -> 15 (-4%); REV_MIX 45 -> 35 (-8%); ALLEY 0 -> 80 (+63%); VOLUME 100 -> 105; against round 1's D: X-MOD 64 -> 32, VOLUME 100 -> 105

### The grit against the baseline (dB change of the share above 4 kHz; flatness before -> after; off-ladder count before -> after)

| var | note | >4 kHz dB change 0-20 / 20-100 / 100-400 / 1-2 s | flatness 0-20 / 20-100 / 100-400 / 1-2 s (dB) | off-ladder (-30 dB) 20-100 / 100-400 / 1-2 s | crest strike (dry) |
|---|---|---|---|---|---|
| B2 | A3 | -0.0 / +0.3 / -0.2 / -0.5 | -2.8 -> -3.2 / -4.7 -> -9.0 / -11.7 -> -18.4 / -20.7 -> -25.3 | 18 -> 14 / 16 -> 5 / 12 -> 2 | 11.4 -> 11.2 dB |
| B2 | A4 | -0.5 / +0.0 / -0.5 / -0.7 | -3.4 -> -6.7 / -10.1 -> -17.1 / -17.0 -> -25.6 / -25.2 -> -31.5 | 18 -> 8 / 13 -> 3 / 8 -> 3 | 12.0 -> 12.1 dB |
| B2 | A6 | -0.0 / +0.1 / +0.2 / +0.8 | -15.7 -> -22.4 / -22.9 -> -32.7 / -24.7 -> -34.6 / -26.8 -> -36.3 | 5 -> 2 / 3 -> 2 / 2 -> 1 | 12.3 -> 12.2 dB |
| C2 | A3 | -0.0 / +0.3 / -0.2 / -0.4 | -2.8 -> -3.2 / -4.7 -> -9.0 / -11.9 -> -18.7 / -19.5 -> -24.6 | 18 -> 14 / 16 -> 4 / 4 -> 1 | 10.3 -> 10.0 dB |
| C2 | A4 | -0.6 / +0.0 / -0.5 / -0.4 | -3.4 -> -6.7 / -10.1 -> -17.2 / -17.2 -> -25.9 / -21.1 -> -29.7 | 18 -> 8 / 13 -> 3 / 3 -> 1 | 10.7 -> 10.9 dB |
| C2 | A6 | -0.0 / +0.1 / +0.2 / -0.1 | -15.7 -> -22.4 / -22.9 -> -32.8 / -24.8 -> -34.9 / -24.0 -> -35.0 | 5 -> 2 / 3 -> 2 / 2 -> 1 | 11.0 -> 10.9 dB |
| D2 | A3 | -0.0 / +0.4 / -0.2 / -0.4 | -2.8 -> -3.2 / -4.7 -> -9.1 / -12.1 -> -18.5 / -19.6 -> -24.7 | 20 -> 14 / 17 -> 5 / 4 -> 1 | 9.9 -> 9.7 dB |
| D2 | A4 | -0.6 / +0.0 / -0.7 / -0.6 | -3.4 -> -6.7 / -10.0 -> -17.0 / -16.9 -> -25.4 / -20.9 -> -29.6 | 19 -> 10 / 12 -> 3 / 4 -> 1 | 10.3 -> 10.5 dB |
| D2 | A6 | -0.0 / +0.1 / +0.1 / -0.0 | -15.7 -> -22.3 / -22.5 -> -31.8 / -24.6 -> -34.5 / -23.8 -> -34.9 | 5 -> 2 / 3 -> 2 / 2 -> 1 | 10.5 -> 10.5 dB |

### Keep underneath unchanged (the acceptance numbers; PASS = inside the stated tolerance)

| var | ring A4 to -6 / -12 / -20 / -40 ms (6B figure; change %) | ladder A4 first 300 ms, dB change hum / prime / tierce / quint / nominal | shares A4 strike, pp change <150 / 150-800 / 800-4k | shares A3 | centroid 100-400 ms A4 / A3 (change %) | wet return re dry, dB change 4 windows | verdict |
|---|---|---|---|---|---|---|---|
| B2 | 309 (298; +3.7) / 620 (612; +1.3) / 1040 (1034; +0.6) / 2079 (2069; +0.5) | +0.0 / -0.3 / -0.3 / -0.8 / -1.4 | -0.0 / +2.0 / -1.9 | -0.1 / +0.0 / +0.1 | 2439 (-9.2) / 1631 (-5.0) | -0.1 / +0.3 / +1.2 / +0.8 | ring FAIL, ladder PASS, shares PASS, returns FAIL, centroid PASS |
| C2 | 649 (648; +0.2) / 1225 (1218; +0.6) / 2132 (2147; -0.7) / 4066 (4062; +0.1) | +0.0 / -0.2 / -0.2 / -0.7 / -1.3 | -0.0 / +2.1 / -1.9 | -0.1 / +0.1 / +0.1 | 2395 (-9.1) / 1596 (-5.2) | -0.1 / +0.3 / +1.3 / +0.7 | ring PASS, ladder PASS, shares PASS, returns FAIL, centroid PASS |
| D2 | 915 (900; +1.7) / 1962 (1895; +3.5) / 3094 (3096; -0.1) / 5963 (5979; -0.3) | +0.0 / -0.2 / -0.3 / -1.0 / -2.1 | -0.0 / +3.0 / -2.8 | -0.1 / +0.1 / +0.1 | 2383 (-9.4) / 1596 (-5.4) | -0.1 / +0.3 / +1.4 / +0.8 | ring FAIL, ladder PASS, shares PASS, returns FAIL, centroid PASS |

Ladder of C2 against the 6B text (hum 0, prime -7, tierce 1.196 at -11, quint 1.498 at -10, nominal 1.997 at -12): +0.0 / -7.1 / -10.9 / -10.3 / -13.2 (ratios 0.499 / 0.997 / 1.196 / 1.496 / 1.995).

Space (A4 held 400 ms: return against the dry note, dry / return / re dry dB, windows 0-20 / 20-100 / 100-250 / 250-1000 ms):

* B: -17.2 / -49.2 / -32.1; -18.2 / -36.9 / -18.7; -20.4 / -36.4 / -16.1; -27.4 / -42.4 / -14.9
* B2: -17.1 / -49.2 / -32.2; -18.0 / -36.5 / -18.4; -20.2 / -35.0 / -14.8; -27.3 / -41.4 / -14.1
* C: -18.5 / -50.7 / -32.2; -19.1 / -38.1 / -19.0; -20.2 / -37.2 / -16.9; -24.1 / -40.0 / -15.9
* C2: -17.8 / -50.0 / -32.3; -18.3 / -37.0 / -18.7; -19.5 / -35.1 / -15.7; -23.4 / -38.6 / -15.2
* D: -19.8 / -47.1 / -27.3; -20.2 / -34.5 / -14.3; -21.0 / -33.9 / -12.9; -23.8 / -35.9 / -12.1
* D2: -19.0 / -46.4 / -27.5; -19.4 / -33.3 / -14.0; -20.2 / -31.7 / -11.5; -23.0 / -34.3 / -11.3

### Level, peak, clipping

| var | note | crest, dry, strike 0-400 ms / the note | dry peak dBFS | filter state saturating, % of voice samples (whole note / first 100 ms) | mix clamp (hard) | output tanh: samples input over 6000 (0.1 dB) / 12000 / 20000, max input | samples at full scale |
|---|---|---|---|---|---|---|---|
| B2 | A3 | 11.2 / 19.1 dB | -9.0 | 0.07 / 0.02 | 0 | 2369 / 2 / 0, 12226 | 0 (all phrases) |
| B2 | A4 | 12.1 / 20.0 dB | -8.2 | 0.13 / 0.00 | 0 | 2271 / 4 / 0, 13542 | 0 (all phrases) |
| B2 | A6 | 12.2 / 20.2 dB | -8.4 | 0.34 / 0.00 | 0 | 1968 / 4 / 0, 13156 | 0 (all phrases) |
| C2 | A3 | 10.0 / 16.3 dB | -9.5 | 0.08 / 0.02 | 0 | 3252 / 0 / 0, 11451 | 0 (all phrases) |
| C2 | A4 | 10.9 / 17.2 dB | -8.7 | 0.14 / 0.00 | 0 | 3048 / 1 / 0, 12636 | 0 (all phrases) |
| C2 | A6 | 10.9 / 17.3 dB | -9.1 | 0.36 / 0.00 | 0 | 2481 / 1 / 0, 12053 | 0 (all phrases) |
| D2 | A3 | 9.7 / 14.9 dB | -10.5 | 0.08 / 0.02 | 0 | 2442 / 0 / 0, 10080 | 0 (all phrases) |
| D2 | A4 | 10.5 / 15.7 dB | -9.8 | 0.14 / 0.00 | 0 | 2242 / 0 / 0, 11014 | 0 (all phrases) |
| D2 | A6 | 10.5 / 15.8 dB | -10.2 | 0.36 / 0.00 | 0 | 1668 / 0 / 0, 10447 | 0 (all phrases) |

### The tail and register of C2: level dB, centroid Hz, >4 kHz % per window after the strike (A4; X-MOD does not touch the tail's top: the same windows as C, which has no tail table in this kit's baseline)

* C2 A4: 0-20 ms: -17.8 dB, 4147 Hz, 4.2 %; 20-100 ms: -18.5 dB, 3682 Hz, 4.2 %; 100-400 ms: -20.1 dB, 2447 Hz, 1.7 %; 1000-2000 ms: -31.2 dB, 1804 Hz, 0.4 %; 2000-4000 ms: -42.8 dB, 1918 Hz, 0.4 %; 4000-6000 ms: -64.4 dB, 3495 Hz, 0.5 %

Register (C2, RMS 0-300 ms dB / centroid 0-100 ms Hz): A2 -19.0 / 1587; A3 -19.3 / 2563; A4 -19.2 / 3834; A5 -19.6 / 5018; A6 -19.0 / 6140

## 4. Live controls on the base (C2, A3; one step each way) and the CPU of the add-ons

| control | base | step | value | hum | prime | tierce | quint | nominal | centroid 0-100 ms | ring -20 / -40 ms | level 0-300 ms | off-harmonic partials above -25 dB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CUTOFF | 88 | -10 | 78 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.495 (-9) | 1.993 (-13) | 1739 | 1953 / 4053 | -19.5 | 2 |
| CUTOFF | 88 | +0 | 88 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| CUTOFF | 88 | +10 | 98 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-8) | 1.994 (-12) | 3543 | 2012 / 4089 | -19.2 | 3 |
| XMOD | 32 | -20 | 12 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.495 (-9) | 1.993 (-12) | 2436 | 1985 / 4072 | -19.3 | 3 |
| XMOD | 32 | +0 | 32 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| XMOD | 32 | +20 | 52 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.495 (-9) | 1.993 (-12) | 2557 | 1999 / 4072 | -19.3 | 3 |
| ENV_O2 | 64 | -10 | 54 | 0.499 (+0) | 0.997 (-5) | - | 1.495 (-9) | 1.994 (-13) | 2462 | 1943 / 4066 | -19.2 | 1 |
| ENV_O2 | 64 | +0 | 64 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| ENV_O2 | 64 | +10 | 74 | 0.499 (+0) | 0.996 (-5) | - | 1.496 (-8) | 1.994 (-12) | 2515 | 2016 / 4093 | -19.3 | 1 |
| O2_FINE | 64 | -8 | 56 | 0.499 (+0) | 0.996 (-5) | 1.201 (-11) | 1.496 (-9) | 1.994 (-12) | 2551 | 2007 / 4075 | -19.3 | 3 |
| O2_FINE | 64 | +0 | 64 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| O2_FINE | 64 | +8 | 72 | 0.499 (+0) | 0.996 (-5) | 1.192 (-10) | 1.496 (-9) | 1.994 (-12) | 2528 | 1980 / 4080 | -19.3 | 3 |
| DLY_MIX | 30 | -15 | 15 | 0.499 (+0) | 0.996 (-6) | 1.210 (-10) | 1.495 (-9) | 1.994 (-12) | 2563 | 2003 / 4089 | -19.2 | 3 |
| DLY_MIX | 30 | +0 | 30 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| DLY_MIX | 30 | +15 | 45 | 0.499 (+0) | 0.996 (-5) | 1.211 (-10) | 1.496 (-8) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.4 | 3 |
| REV_MIX | 20 | -15 | 5 | 0.499 (+0) | 0.996 (-6) | 1.212 (-10) | 1.496 (-9) | 1.994 (-12) | 2547 | 1980 / 4080 | -19.3 | 3 |
| REV_MIX | 20 | +0 | 20 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-9) | 1.994 (-12) | 2563 | 1980 / 4076 | -19.3 | 3 |
| REV_MIX | 20 | +15 | 35 | 0.499 (+0) | 0.996 (-5) | 1.210 (-10) | 1.496 (-8) | 1.994 (-12) | 2576 | 2003 / 4080 | -19.3 | 3 |
| CHEW | 0 | +45 | 45 | 0.497 (+0) | 0.994 (-6) | 1.207 (-11) | 1.492 (-9) | 2.006 (-13) | 2348 | 1955 / 4073 | -19.1 | 6 |

CPU of the live add-ons on C2 (host instr/sample, worst case): base 2017; CHEW 45 2801; GROWL 44 2612; CHEW 45 + GROWL 44 3395 (soft limit 2400). The grit fix itself: C 2017 -> C2 2017 (+0); X-MOD 0 (isolation) 1965 (the engine skips the FM at 0).

