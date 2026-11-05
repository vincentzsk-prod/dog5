/* SPDX-License-Identifier: GPL-3.0-only */
/* The factory programs: each a name and the parameters that differ from the defaults (obv_params.h). */
#define X 255
/* the dark arpeggios: a four-note chord climbed in 16ths, two saws a hair apart, the 24 dB filter half shut, a
 * dotted-eighth ping-pong and a long dark plate */
static const uint8_t PF_DARK_ARP[] = {P_ARP_MODE, A_UP, P_ARP_DIV, D_16, P_ARP_OCT, 1, P_ARP_GATE, 75, P_O2_FINE, 69, P_O2_LVL, 105,
    P_CUTOFF, 46, P_RESO, 22, P_FENV_AMT, 92, P_FA, 0, P_FD, 58, P_FS, 35, P_FR, 55, P_AA, 1, P_AD, 72, P_AS, 55, P_AR, 60,
    P_KEYTRK, 70, P_VINTAGE, 55, P_SPREAD, 50, P_CHO_MIX, 25, P_CHO_RATE, 30, P_CHO_DEPTH, 40,
    P_DLY_TIME, DD_8D, P_DLY_FB, 48, P_DLY_TONE, 45, P_DLY_MIX, 58, P_REV_SIZE, 100, P_REV_DAMP, 75, P_REV_PRE, 30, P_REV_MIX, 52, X};
static const uint8_t PF_UPSIDE_ARP[] = {P_ARP_MODE, A_UPDN, P_ARP_DIV, D_16, P_ARP_OCT, 2, P_ARP_GATE, 60, P_O1_WAVE, W_BOTH, P_O1_PW, 40,
    P_O2_WAVE, W_SAW, P_O2_SEMI, 12, P_O2_LVL, 70, P_O2_FINE, 72, P_FTYPE, F_SEM, P_FMORPH, 18, P_CUTOFF, 40, P_RESO, 35,
    P_FENV_AMT, 100, P_FD, 50, P_FS, 10, P_AA, 1, P_AD, 60, P_AS, 20, P_AR, 70, P_VINTAGE, 70, P_SPREAD, 80,
    P_DLY_TIME, DD_8, P_DLY_FB, 62, P_DLY_TONE, 35, P_DLY_MIX, 64, P_REV_SIZE, 115, P_REV_DAMP, 85, P_REV_PRE, 40, P_REV_MIX, 66, X};
static const uint8_t PF_NEON_PAD[] = {P_O1_WAVE, W_PLS, P_O1_PW, 50, P_O2_WAVE, W_BOTH, P_O2_PW, 80, P_O2_FINE, 74, P_LFO_PWM, 45,
    P_LFO_RATE, 42, P_LFO_PHASE, LP_SPREAD, P_CUTOFF, 52, P_RESO, 12, P_FENV_AMT, 80, P_FA, 90, P_FD, 100, P_FS, 50, P_FR, 100,
    P_AA, 85, P_AR, 110, P_VINTAGE, 60, P_SPREAD, 120, P_LFO_PITCH, 4,
    P_REV_SIZE, 118, P_REV_DAMP, 60, P_REV_PRE, 50, P_REV_MIX, 70, P_DLY_TIME, DD_4D, P_DLY_FB, 40, P_DLY_TONE, 30, P_DLY_MIX, 35, X};
static const uint8_t PF_BRASS_STAB[] = {P_O2_FINE, 72, P_CUTOFF, 60, P_FENV_AMT, 114, P_FA, 30, P_FD, 75, P_FS, 30, P_FR, 50,
    P_AA, 12, P_AD, 60, P_AS, 90, P_AR, 45, P_RESO, 25, P_DRIVE, 20, X};
/* 25 SAWTOOTH (voiced 4 Nov, dog5-docs/voicing/25-sawtooth.md; was PF_POLY_BRASS, this slot's alone): the stable, warm poly brass. POLY, two
 * saws 5.5 cents apart, VINTAGE left at 30, a 24 dB filter swell (CUTOFF 56, ENV AMT 100, attack 117 ms, decay 378 ms to
 * sustain 50), a fade-in vibrato, no GROWL (a touch measured -1 dB of peak for +570 instr/sample; D has the edge). No chop, no sub: where 03 Half-Life is unstable and chopped,
 * this one holds still. VOLUME 97 puts it on the bank reference (-18.0 dBFS RMS, phrase b) */
static const uint8_t PF_SAWTOOTH[] = {P_O2_FINE, 71, P_CUTOFF, 56, P_RESO, 15, P_FENV_AMT, 100, P_FA, 70, P_FD, 85,
    P_FS, 50, P_AA, 50, P_AR, 55, P_LFO_RATE, 75, P_LFO_DELAY, 60, P_LFO_PITCH, 20, P_VOLUME, 97, X};
static const uint8_t PF_SYNC_LEAD[] = {P_MODE, M_MONO, P_O1_LVL, 0, P_O2_LVL, 120, P_SYNC, 1, P_ENV_O2, 104, P_O2_SEMI, 31,
    P_FD, 80, P_FS, 20, P_CUTOFF, 90, P_RESO, 10, P_GLIDE, 20, P_AA, 2, P_AR, 40, P_FENV_AMT, 80, P_DLY_TIME, DD_8D, P_DLY_FB, 40, P_DLY_MIX, 35, P_REV_SIZE, 70, P_REV_MIX, 22, X};
static const uint8_t PF_PWM_STRINGS[] = {P_O1_WAVE, W_PLS, P_O2_WAVE, W_PLS, P_O2_PW, 40, P_O2_FINE, 73, P_LFO_PWM, 60,
    P_LFO_RATE, 50, P_LFO_PHASE, LP_SPREAD, P_AA, 60, P_AR, 90, P_FA, 50, P_CUTOFF, 75, P_FENV_AMT, 74, P_RESO, 5,
    P_SPREAD, 100, P_VINTAGE, 50, P_LFO_PITCH, 3, P_REV_SIZE, 100, P_REV_MIX, 35, X};
static const uint8_t PF_BELL_XMOD[] = {P_O1_LVL, 100, P_O2_SEMI, 43, P_XMOD, 70, P_CUTOFF, 100, P_FD, 90, P_FS, 0, P_AD, 95,
    P_AS, 0, P_AR, 80, P_FENV_AMT, 94, P_AA, 1, P_DLY_TIME, DD_8, P_DLY_FB, 50, P_DLY_MIX, 40, P_REV_SIZE, 110, P_REV_MIX, 45, X};
static const uint8_t PF_FAT_BASS[] = {P_MODE, M_MONO, P_O2_WAVE, W_PLS, P_O2_PW, 50, P_O2_SEMI, 12, P_CUTOFF, 40, P_RESO, 30,
    P_FENV_AMT, 109, P_FD, 60, P_FS, 10, P_AA, 2, P_AR, 30, P_DRIVE, 40, P_GLIDE, 10, X};
static const uint8_t PF_ARP_SEQ[] = {P_ARP_MODE, A_UP, P_ARP_DIV, D_16, P_ARP_OCT, 2, P_ARP_GATE, 50, P_O1_WAVE, W_PLS, P_O1_PW, 40,
    P_O2_SEMI, 12, P_CUTOFF, 50, P_FENV_AMT, 124, P_FD, 45, P_FS, 0, P_AD, 50, P_AS, 0, P_AR, 40, P_RESO, 40, P_AA, 1, P_DLY_TIME, DD_8D, P_DLY_FB, 40, P_DLY_MIX, 35, X};
static const uint8_t PF_SWEEP_PAD[] = {P_O2_FINE, 74, P_CUTOFF, 30, P_FENV_AMT, 127, P_FA, 110, P_FD, 100, P_FS, 60, P_FR, 100,
    P_AA, 90, P_AR, 105, P_RESO, 20, P_LFO_FLT, 15, P_LFO_RATE, 30, P_SPREAD, 110, P_VINTAGE, 60, P_CHO_MIX, 40, P_REV_SIZE, 110, P_REV_MIX, 45, X};
static const uint8_t PF_BP_QUACK[] = {P_FTYPE, F_BP12, P_RESO, 70, P_CUTOFF, 50, P_FENV_AMT, 124, P_FD, 55, P_FS, 0, P_AD, 80,
    P_AS, 70, P_O2_WAVE, W_PLS, P_O2_PW, 30, P_AA, 1, X};
static const uint8_t PF_RESO_ZAP[] = {P_MODE, M_MONO, P_RESO, 110, P_CUTOFF, 20, P_FENV_AMT, 127, P_FD, 40, P_FS, 0, P_AD, 40,
    P_AS, 0, P_FTYPE, F_LP12, P_O1_WAVE, W_PLS, P_NOISE, 20, P_AA, 1, P_AR, 30, X};
static const uint8_t PF_NOISE_WASH[] = {P_NOISE, 100, P_O1_WAVE, W_OFF, P_O2_WAVE, W_OFF, P_FTYPE, F_BP12, P_RESO, 50, P_CUTOFF, 70,
    P_LFO_FLT, 60, P_LFO_RATE, 20, P_AA, 100, P_AR, 110, P_FA, 60, P_FENV_AMT, 64, P_REV_SIZE, 127, P_REV_DAMP, 40, P_REV_MIX, 60, X};
static const uint8_t PF_HOLLOW_PAD[] = {P_O1_WAVE, W_PLS, P_O1_PW, 20, P_O2_WAVE, W_PLS, P_O2_PW, 108, P_O2_FINE, 76, P_FTYPE, F_NOTCH,
    P_CUTOFF, 70, P_LFO_PWM, 40, P_LFO_RATE, 40, P_LFO_PHASE, LP_SPREAD, P_AA, 70, P_AR, 100, P_FENV_AMT, 64, P_SPREAD, 100, P_REV_SIZE, 100, P_REV_MIX, 40, X};
static const uint8_t PF_SQUARE_LEAD[] = {P_MODE, M_MONO, P_O1_WAVE, W_PLS, P_O2_WAVE, W_PLS, P_O2_FINE, 69, P_CUTOFF, 90, P_RESO, 20,
    P_GLIDE, 30, P_LFO_PITCH, 8, P_LFO_DELAY, 50, P_DRIVE, 30, P_AA, 3, P_AR, 40, P_DLY_TIME, DD_8, P_DLY_FB, 35, P_DLY_MIX, 30, X};
static const uint8_t PF_SUB_BASS[] = {P_MODE, M_MONO, P_O1_WAVE, W_PLS, P_O2_SEMI, 12, P_O2_LVL, 60, P_CUTOFF, 35, P_RESO, 10,
    P_FENV_AMT, 84, P_FD, 50, P_FS, 20, P_AA, 1, P_AD, 60, P_AR, 20, P_GLIDE, 5, X};
static const uint8_t PF_SOFT_KEYS[] = {P_O1_LVL, 90, P_O2_WAVE, W_PLS, P_O2_PW, 30, P_O2_LVL, 60, P_O2_SEMI, 36, P_CUTOFF, 60,
    P_FENV_AMT, 99, P_FD, 70, P_FS, 20, P_AA, 3, P_AD, 90, P_AS, 60, P_AR, 60, P_VEL_FLT, 80, P_VEL_AMP, 90, P_RESO, 10, P_CHO_MIX, 30, P_REV_SIZE, 80, P_REV_MIX, 30, X};
static const uint8_t PF_SYNC_BRASS[] = {P_SYNC, 1, P_O1_LVL, 60, P_O2_LVL, 110, P_O2_SEMI, 29, P_ENV_O2, 89, P_CUTOFF, 65,
    P_FENV_AMT, 104, P_FA, 20, P_FD, 70, P_FS, 40, P_AA, 10, P_AR, 50, X};
static const uint8_t PF_DRONE_UNI[] = {P_MODE, M_UNISON, P_UNI_N, 8, P_UNI_DET, 80, P_O2_SEMI, 12, P_CUTOFF, 45, P_FENV_AMT, 79,
    P_FA, 100, P_AA, 100, P_AR, 110, P_LFO_FLT, 20, P_LFO_RATE, 25, P_RESO, 10, P_VINTAGE, 80, P_SPREAD, 127, P_REV_SIZE, 120, P_REV_DAMP, 80, P_REV_MIX, 50, X};
static const uint8_t PF_ARP_PLUCK[] = {P_ARP_MODE, A_UPDN, P_ARP_DIV, D_16, P_ARP_OCT, 3, P_ARP_GATE, 40, P_O2_WAVE, W_PLS,
    P_O2_PW, 40, P_O2_SEMI, 36, P_CUTOFF, 60, P_FENV_AMT, 114, P_FD, 40, P_FS, 0, P_AD, 45, P_AS, 0, P_AR, 50, P_RESO, 30,
    P_SPREAD, 100, P_AA, 1, P_DLY_TIME, DD_8D, P_DLY_FB, 45, P_DLY_TONE, 50, P_DLY_MIX, 45, P_REV_SIZE, 90, P_REV_MIX, 28, X};
static const uint8_t PF_ARP_CHORD[] = {P_ARP_MODE, A_PLAY, P_ARP_DIV, D_8, P_ARP_OCT, 1, P_ARP_GATE, 80, P_MODE, M_DUAL,
    P_UNI_DET, 40, P_CUTOFF, 70, P_AA, 5, P_AR, 60, P_DLY_TIME, DD_8, P_DLY_FB, 30, P_DLY_MIX, 30, P_REV_MIX, 25, X};
static const uint8_t PF_RANDOM_ARP[] = {P_ARP_MODE, A_RND, P_ARP_DIV, D_16T, P_ARP_OCT, 2, P_ARP_GATE, 30, P_O1_WAVE, W_PLS,
    P_O2_SEMI, 31, P_FTYPE, F_BP12, P_RESO, 50, P_CUTOFF, 70, P_FD, 40, P_FS, 0, P_AD, 50, P_AS, 0, P_AA, 1, P_DLY_TIME, DD_8T, P_DLY_FB, 50, P_DLY_MIX, 45, P_REV_MIX, 30, X};
/* 31 Fi(l)fth (voiced 4 Nov, approved 5 Nov: dog5-docs/voicing/31-fifth.md; was a MONO fifths lead): the chord stab. DUAL, a detuned pair per note (DETUNE 36,
 * ~7.8 cents apart, SPREAD 90), POLY 8 so a three-note chord has its six voices, OSC 2 a fifth up in every voice (+7 st, FINE 66), a filter-envelope pluck
 * (ENV AMT 106, decay 29 ms, sustain 22) over an amp that rings on (137 ms decay to sustain 70), DRIVE 20, and a short BBD slap (ALLEY 65 = 89 ms, FEEDBK 28,
 * MIX 36). No spring. VOLUME 92 puts it on the bank reference (-18.0 dBFS RMS, phrase b) */
static const uint8_t PF_FIFTH[] = {P_O2_SEMI, 31, P_O2_FINE, 66, P_CUTOFF, 92, P_RESO, 22, P_FENV_AMT, 106,
    P_DRIVE, 20, P_FA, 0, P_FD, 52, P_FS, 22, P_FR, 50, P_AA, 0, P_AD, 72, P_AS, 70, P_AR, 52, P_MODE, M_DUAL,
    P_UNI_DET, 36, P_VINTAGE, 35, P_SPREAD, 90, P_VOLUME, 92, P_DLY_FB, 28, P_DLY_TONE, 55, P_DLY_MIX, 36,
    P_POLY_N, 8, P_ALLEY, 65, P_BBD_SPREAD, 60, X};
static const uint8_t PF_VINTAGE_PAD[] = {P_VINTAGE, 127, P_O2_FINE, 73, P_CUTOFF, 55, P_FENV_AMT, 94, P_FA, 70, P_AA, 60, P_AR, 90,
    P_FR, 90, P_RESO, 15, P_SPREAD, 120, P_REV_SIZE, 105, P_REV_MIX, 45, X};
static const uint8_t PF_XMOD_GROWL[] = {P_MODE, M_MONO, P_XMOD, 90, P_O2_SEMI, 19, P_CUTOFF, 50, P_FENV_AMT, 114, P_FD, 60, P_FS, 30,
    P_DRIVE, 40, P_AA, 2, P_AR, 40, X};
static const uint8_t PF_PERC_HIT[] = {P_O2_SEMI, 48, P_NOISE, 60, P_CUTOFF, 90, P_FENV_AMT, 124, P_FD, 25, P_FS, 0, P_AD, 30, P_AS, 0,
    P_AR, 25, P_FTYPE, F_LP12, P_RESO, 30, P_AA, 1, P_REV_SIZE, 90, P_REV_MIX, 40, X};
/* 33-64 (1.5): a second set in the same spirit: arpeggios, brass, pads, keys, basses, leads, effects */
static const uint8_t PF_NIGHT_DRIVE[] = {P_ARP_MODE, A_UP, P_ARP_DIV, D_16, P_ARP_OCT, 2, P_ARP_GATE, 55, P_O1_WAVE, W_BOTH, P_O1_PW, 45,
    P_O2_FINE, 72, P_O2_LVL, 90, P_CUTOFF, 52, P_RESO, 38, P_FENV_AMT, 104, P_FA, 0, P_FD, 48, P_FS, 15, P_AA, 1, P_AD, 60, P_AS, 40,
    P_AR, 50, P_KEYTRK, 80, P_SPREAD, 90, P_CHO_MIX, 30, P_DLY_TIME, DD_8D, P_DLY_FB, 55, P_DLY_TONE, 40, P_DLY_MIX, 55,
    P_REV_SIZE, 95, P_REV_MIX, 40, X};
static const uint8_t PF_MINOR_FALL[] = {P_ARP_MODE, A_DOWN, P_ARP_DIV, D_16, P_ARP_OCT, 2, P_ARP_GATE, 45, P_O2_WAVE, W_PLS, P_O2_PW, 35,
    P_O2_FINE, 70, P_CUTOFF, 48, P_RESO, 30, P_FENV_AMT, 110, P_FD, 42, P_FS, 0, P_AA, 1, P_AD, 55, P_AS, 0, P_AR, 55,
    P_DLY_TIME, DD_8, P_DLY_FB, 50, P_DLY_TONE, 35, P_DLY_MIX, 50, P_REV_SIZE, 105, P_REV_MIX, 45, X};
static const uint8_t PF_SHADOW_ARP[] = {P_ARP_MODE, A_UPDN, P_ARP_DIV, D_8T, P_ARP_OCT, 2, P_ARP_GATE, 50, P_FTYPE, F_BP12, P_RESO, 62, P_VOLUME, 127,
    P_CUTOFF, 62, P_FENV_AMT, 100, P_FD, 50, P_FS, 10, P_O2_SEMI, 31, P_O2_LVL, 70, P_AA, 1, P_AD, 60, P_AS, 20, P_AR, 60,
    P_LFO_FLT, 20, P_LFO_RATE, 35, P_DLY_TIME, DD_4, P_DLY_FB, 60, P_DLY_TONE, 30, P_DLY_MIX, 55, P_REV_SIZE, 115, P_REV_MIX, 55, X};
static const uint8_t PF_GLASS_ARP[] = {P_ARP_MODE, A_UP, P_ARP_DIV, D_16, P_ARP_OCT, 3, P_ARP_GATE, 35, P_O2_SEMI, 43, P_XMOD, 55,
    P_CUTOFF, 95, P_FENV_AMT, 90, P_FD, 50, P_FS, 0, P_AA, 1, P_AD, 70, P_AS, 0, P_AR, 70, P_SPREAD, 110,
    P_DLY_TIME, DD_8D, P_DLY_FB, 50, P_DLY_MIX, 45, P_REV_SIZE, 115, P_REV_DAMP, 40, P_REV_MIX, 50, X};
static const uint8_t PF_PULSE_ARP[] = {P_ARP_MODE, A_UPDN, P_ARP_DIV, D_16, P_ARP_OCT, 1, P_ARP_GATE, 60, P_O1_WAVE, W_PLS, P_O2_WAVE, W_PLS,
    P_O2_PW, 30, P_O2_FINE, 71, P_LFO_PWM, 50, P_LFO_RATE, 45, P_CUTOFF, 62, P_RESO, 25, P_FENV_AMT, 100, P_FD, 45, P_FS, 20,
    P_AA, 1, P_AR, 45, P_CHO_MIX, 35, P_DLY_TIME, DD_8D, P_DLY_FB, 40, P_DLY_MIX, 40, P_REV_MIX, 30, X};
static const uint8_t PF_ARP_BASS[] = {P_ARP_MODE, A_UP, P_ARP_DIV, D_16, P_ARP_OCT, 1, P_ARP_GATE, 55, P_MODE, M_MONO, P_O2_SEMI, 12,
    P_O2_LVL, 80, P_CUTOFF, 38, P_RESO, 40, P_FENV_AMT, 112, P_FD, 38, P_FS, 5, P_AA, 1, P_AD, 50, P_AS, 60, P_AR, 25, P_DRIVE, 35, X};
static const uint8_t PF_STAB_CHORD[] = {P_MODE, M_DUAL, P_UNI_DET, 45, P_CUTOFF, 58, P_RESO, 20, P_FENV_AMT, 112, P_FA, 5, P_FD, 50,
    P_FS, 20, P_AA, 2, P_AD, 55, P_AS, 30, P_AR, 40, P_DRIVE, 25, P_SPREAD, 100, P_REV_SIZE, 90, P_REV_MIX, 35, X};
static const uint8_t PF_BIG_BRASS[] = {P_O2_FINE, 73, P_CUTOFF, 52, P_RESO, 18, P_FENV_AMT, 108, P_FA, 65, P_FD, 85, P_FS, 55, P_FR, 70,
    P_AA, 50, P_AS, 110, P_AR, 65, P_VINTAGE, 60, P_SPREAD, 110, P_CHO_MIX, 40, P_REV_SIZE, 100, P_REV_MIX, 35, X};
static const uint8_t PF_HORN_SECT[] = {P_O2_FINE, 71, P_CUTOFF, 62, P_RESO, 12, P_FENV_AMT, 100, P_FA, 35, P_FD, 70, P_FS, 50,
    P_AA, 25, P_AR, 50, P_LFO_PITCH, 18, P_LFO_DELAY, 75, P_LFO_RATE, 72, P_VEL_FLT, 80, P_DRIVE, 15, P_REV_MIX, 25, X};
static const uint8_t PF_WARM_PAD[] = {P_O1_WAVE, W_PLS, P_O1_PW, 45, P_O2_FINE, 74, P_LFO_PWM, 40, P_LFO_RATE, 35, P_LFO_PHASE, LP_SPREAD,
    P_CUTOFF, 50, P_RESO, 10, P_FENV_AMT, 80, P_FA, 80, P_FD, 100, P_FS, 60, P_FR, 100, P_AA, 80, P_AR, 105,
    P_VINTAGE, 55, P_SPREAD, 120, P_CHO_MIX, 60, P_REV_SIZE, 110, P_REV_MIX, 50, X};
static const uint8_t PF_DARK_PAD[] = {P_O2_SEMI, 12, P_O2_FINE, 72, P_CUTOFF, 32, P_RESO, 30, P_FENV_AMT, 90, P_FA, 105, P_FD, 110,
    P_FS, 40, P_FR, 105, P_AA, 95, P_AR, 112, P_LFO_FLT, 12, P_LFO_RATE, 20, P_VINTAGE, 70, P_SPREAD, 120,
    P_REV_SIZE, 122, P_REV_DAMP, 85, P_REV_PRE, 40, P_REV_MIX, 60, P_DLY_TIME, DD_4D, P_DLY_FB, 45, P_DLY_TONE, 25, P_DLY_MIX, 25, X};
static const uint8_t PF_AIR_CHOIR[] = {P_O1_WAVE, W_PLS, P_O1_PW, 30, P_O2_WAVE, W_PLS, P_O2_PW, 95, P_O2_FINE, 75, P_FTYPE, F_SEM,
    P_FMORPH, 40, P_CUTOFF, 66, P_RESO, 30, P_LFO_PWM, 55, P_LFO_RATE, 30, P_LFO_PHASE, LP_SPREAD, P_NOISE, 12,
    P_AA, 90, P_AR, 105, P_FENV_AMT, 64, P_CHO_MIX, 75, P_CHO_DEPTH, 70, P_REV_SIZE, 118, P_REV_MIX, 55, X};
static const uint8_t PF_SLOW_SWEEP[] = {P_O2_FINE, 72, P_CUTOFF, 25, P_RESO, 70, P_FENV_AMT, 120, P_FA, 118, P_FD, 115, P_FS, 50,
    P_FR, 110, P_AA, 70, P_AR, 110, P_SPREAD, 110, P_CHO_MIX, 35, P_REV_SIZE, 115, P_REV_MIX, 50, X};
static const uint8_t PF_GHOST_PAD[] = {P_NOISE, 45, P_O2_FINE, 76, P_FTYPE, F_BP12, P_CUTOFF, 60, P_RESO, 60, P_LFO_SHAPE, L_RND,
    P_LFO_FLT, 45, P_LFO_RATE, 40, P_LFO_PHASE, LP_SPREAD, P_AA, 100, P_AR, 115, P_FENV_AMT, 64,
    P_REV_SIZE, 127, P_REV_DAMP, 50, P_REV_PRE, 60, P_REV_MIX, 70, P_DLY_TIME, DD_2, P_DLY_FB, 50, P_DLY_MIX, 30, X};
static const uint8_t PF_ENSEMBLE[] = {P_O2_FINE, 75, P_O2_LVL, 90, P_CUTOFF, 72, P_RESO, 5, P_FENV_AMT, 70, P_FA, 60, P_AA, 55, P_AR, 85,
    P_LFO_PITCH, 6, P_LFO_RATE, 60, P_LFO_PHASE, LP_SPREAD, P_VINTAGE, 50, P_SPREAD, 115, P_CHO_MIX, 80, P_CHO_RATE, 45,
    P_CHO_DEPTH, 65, P_REV_SIZE, 100, P_REV_MIX, 40, X};
static const uint8_t PF_ICE_BELLS[] = {P_O2_SEMI, 45, P_XMOD, 85, P_O1_LVL, 95, P_CUTOFF, 105, P_FENV_AMT, 96, P_FD, 95, P_FS, 0,
    P_AA, 1, P_AD, 105, P_AS, 0, P_AR, 95, P_SPREAD, 110, P_CHO_MIX, 30, P_DLY_TIME, DD_4, P_DLY_FB, 45, P_DLY_MIX, 35,
    P_REV_SIZE, 122, P_REV_DAMP, 35, P_REV_MIX, 60, X};
static const uint8_t PF_SOFT_EP[] = {P_O1_WAVE, W_PLS, P_O1_PW, 60, P_O2_WAVE, W_PLS, P_O2_PW, 25, P_O2_SEMI, 36, P_O2_LVL, 45,
    P_FTYPE, F_LP12, P_CUTOFF, 55, P_FENV_AMT, 100, P_FD, 75, P_FS, 25, P_AA, 2, P_AD, 95, P_AS, 40, P_AR, 60,
    P_VEL_FLT, 95, P_VEL_AMP, 100, P_KEYTRK, 90, P_CHO_MIX, 55, P_CHO_RATE, 50, P_REV_SIZE, 80, P_REV_MIX, 30, X};
static const uint8_t PF_PULSE_ORGN[] = {P_O1_WAVE, W_PLS, P_O1_PW, 64, P_O2_WAVE, W_PLS, P_O2_PW, 64, P_O2_SEMI, 36, P_O2_LVL, 80,
    P_FTYPE, F_LP12, P_CUTOFF, 85, P_RESO, 0, P_FENV_AMT, 64, P_AA, 2, P_AS, 127, P_AR, 20, P_LFO_PITCH, 5, P_LFO_RATE, 80,
    P_CHO_MIX, 60, P_CHO_RATE, 70, P_REV_MIX, 25, X};
static const uint8_t PF_TAPE_KEYS[] = {P_VINTAGE, 110, P_O2_WAVE, W_PLS, P_O2_PW, 40, P_O2_FINE, 72, P_CUTOFF, 58, P_FENV_AMT, 96,
    P_FD, 80, P_FS, 30, P_AA, 4, P_AD, 90, P_AS, 50, P_AR, 70, P_LFO_PITCH, 4, P_LFO_RATE, 25, P_VEL_FLT, 70,
    P_CHO_MIX, 40, P_DLY_TIME, DD_8D, P_DLY_FB, 45, P_DLY_TONE, 30, P_DLY_MIX, 35, P_REV_MIX, 30, X};
static const uint8_t PF_ACID_LINE[] = {P_MODE, M_MONO, P_O2_WAVE, W_OFF, P_CUTOFF, 30, P_RESO, 95, P_FENV_AMT, 118, P_FD, 45, P_FS, 0,
    P_AA, 1, P_AS, 110, P_AR, 20, P_GLIDE, 25, P_DRIVE, 55, P_VEL_FLT, 90, P_FTYPE, F_LP24, P_DLY_TIME, DD_8D, P_DLY_FB, 30, P_DLY_MIX, 20, X};
static const uint8_t PF_PLUCK_BASS[] = {P_O2_SEMI, 12, P_O2_WAVE, W_PLS, P_O2_PW, 45, P_CUTOFF, 34, P_RESO, 25, P_FENV_AMT, 115,
    P_FD, 40, P_FS, 0, P_AA, 1, P_AD, 60, P_AS, 0, P_AR, 25, P_DRIVE, 30, X};
static const uint8_t PF_DEEP_BASS[] = {P_MODE, M_MONO, P_O1_WAVE, W_BOTH, P_O2_SEMI, 12, P_O2_LVL, 110, P_O2_FINE, 66, P_CUTOFF, 30,
    P_RESO, 15, P_FENV_AMT, 96, P_FD, 70, P_FS, 30, P_AA, 1, P_AR, 25, P_DRIVE, 60, P_GLIDE, 8, X};
static const uint8_t PF_SYNC_BASS[] = {P_MODE, M_MONO, P_SYNC, 1, P_O2_SEMI, 33, P_ENV_O2, 96, P_O1_LVL, 80, P_CUTOFF, 45, P_RESO, 20,
    P_FENV_AMT, 108, P_FD, 45, P_FS, 20, P_AA, 1, P_AR, 25, P_DRIVE, 40, P_GLIDE, 10, X};
static const uint8_t PF_SOLO_LEAD[] = {P_MODE, M_MONO, P_O2_FINE, 70, P_CUTOFF, 80, P_RESO, 25, P_FENV_AMT, 92, P_FD, 70, P_FS, 50,
    P_GLIDE, 35, P_AA, 3, P_AR, 45, P_LFO_PITCH, 14, P_LFO_DELAY, 80, P_LFO_RATE, 72, P_DRIVE, 35,
    P_DLY_TIME, DD_8D, P_DLY_FB, 45, P_DLY_MIX, 35, P_REV_SIZE, 95, P_REV_MIX, 30, X};
static const uint8_t PF_PWM_LEAD[] = {P_MODE, M_MONO, P_O1_WAVE, W_PLS, P_O2_WAVE, W_PLS, P_O2_PW, 40, P_O2_FINE, 68, P_LFO_PWM, 65,
    P_LFO_RATE, 55, P_CUTOFF, 85, P_RESO, 15, P_GLIDE, 25, P_AA, 2, P_AR, 40, P_DLY_TIME, DD_8, P_DLY_FB, 40, P_DLY_MIX, 30, P_REV_MIX, 20, X};
static const uint8_t PF_SCREAM_LD[] = {P_MODE, M_UNISON, P_UNI_N, 4, P_UNI_DET, 35, P_CUTOFF, 75, P_RESO, 85, P_FENV_AMT, 100,
    P_FD, 80, P_FS, 60, P_DRIVE, 80, P_GLIDE, 20, P_AA, 2, P_AR, 40, P_LFO_PITCH, 12, P_LFO_DELAY, 70,
    P_DLY_TIME, DD_8D, P_DLY_FB, 45, P_DLY_MIX, 35, P_REV_MIX, 25, X};
static const uint8_t PF_SOFT_FLUTE[] = {P_MODE, M_MONO, P_O1_WAVE, W_PLS, P_O1_PW, 64, P_O2_WAVE, W_OFF, P_NOISE, 18, P_FTYPE, F_LP12,
    P_CUTOFF, 60, P_RESO, 10, P_FENV_AMT, 75, P_FA, 30, P_AA, 30, P_AR, 50, P_KEYTRK, 100, P_LFO_PITCH, 10, P_LFO_DELAY, 85,
    P_LFO_RATE, 70, P_GLIDE, 15, P_REV_SIZE, 100, P_REV_MIX, 40, X};
static const uint8_t PF_LASER[] = {P_MODE, M_MONO, P_SYNC, 1, P_O2_SEMI, 48, P_ENV_O2, 127, P_O1_LVL, 90, P_CUTOFF, 100, P_RESO, 40, P_VOLUME, 120,
    P_FENV_AMT, 64, P_FA, 0, P_FD, 55, P_FS, 0, P_AA, 1, P_AD, 70, P_AS, 0, P_AR, 40,
    P_DLY_TIME, DD_8D, P_DLY_FB, 60, P_DLY_MIX, 45, P_REV_MIX, 30, X};
static const uint8_t PF_WIND_RISE[] = {P_NOISE, 110, P_O1_WAVE, W_OFF, P_O2_WAVE, W_OFF, P_FTYPE, F_BP12, P_RESO, 75, P_CUTOFF, 30,
    P_FENV_AMT, 124, P_FA, 120, P_FD, 120, P_FS, 100, P_FR, 110, P_AA, 110, P_AR, 115, P_LFO_FLT, 15, P_LFO_RATE, 50,
    P_REV_SIZE, 125, P_REV_MIX, 65, P_DLY_TIME, DD_4, P_DLY_FB, 55, P_DLY_MIX, 30, X};
static const uint8_t PF_SPACE_DRONE[] = {P_MODE, M_UNISON, P_UNI_N, 8, P_UNI_DET, 95, P_O2_SEMI, 31, P_O2_LVL, 70, P_CUTOFF, 54,
    P_RESO, 45, P_LFO_SHAPE, L_SH, P_LFO_FLT, 35, P_LFO_RATE, 30, P_FENV_AMT, 64, P_AA, 90, P_AR, 120, P_VOLUME, 120, P_VINTAGE, 90,
    P_SPREAD, 127, P_DLY_TIME, DD_4D, P_DLY_FB, 70, P_DLY_TONE, 30, P_DLY_MIX, 40, P_REV_SIZE, 127, P_REV_MIX, 65, X};
static const uint8_t PF_SYNC_PAD[] = {P_SYNC, 1, P_O2_SEMI, 31, P_O1_LVL, 70, P_O2_LVL, 100, P_LFO_PITCH, 30, P_LFO_PITCH_TO, TO_O2,
    P_LFO_RATE, 25, P_LFO_PHASE, LP_SPREAD, P_CUTOFF, 60, P_RESO, 15, P_FENV_AMT, 80, P_FA, 70, P_AA, 70, P_AR, 100,
    P_SPREAD, 115, P_CHO_MIX, 50, P_REV_SIZE, 112, P_REV_MIX, 50, X};
static const uint8_t PF_DREAM_ARP[] = {P_ARP_MODE, A_PLAY, P_ARP_DIV, D_8, P_ARP_OCT, 2, P_ARP_GATE, 85, P_O1_WAVE, W_PLS, P_O1_PW, 40,
    P_O2_FINE, 74, P_LFO_PWM, 35, P_LFO_RATE, 40, P_CUTOFF, 60, P_RESO, 20, P_FENV_AMT, 90, P_FA, 20, P_FD, 80, P_FS, 40,
    P_AA, 15, P_AR, 90, P_SPREAD, 120, P_CHO_MIX, 55, P_DLY_TIME, DD_4D, P_DLY_FB, 60, P_DLY_TONE, 35, P_DLY_MIX, 50,
    P_REV_SIZE, 120, P_REV_MIX, 60, X};
/* 03 Half-Life (voiced 4 Nov, dog5-docs/voicing/03-half-life.md; PF_DUAL_SAW, its old base, was 17 Titanic's until Batch 2A gave 17 its own PF_TITANIC): DUAL pair a few cents
 * either side of true over a sub-octave saw, VINTAGE 90 (the SLOP ride goes on top: 90 + 254 = 344 of 381), and the VCA's
 * LFO a 20 Hz SQUARE gate on AMP 100 that fades in over ~110 ms (LFO DELAY): a staccato note's body is clean and its
 * tail spits. POLY 6 so the three-note fifth-and-octave stab needs no stealing. FX macros all 0; VOLUME 112 puts
 * it on the bank reference (-18.0 dBFS RMS, tests/voicing) */
static const uint8_t PF_HALF_LIFE[] = {P_MODE, M_DUAL, P_UNI_DET, 60, P_POLY_N, 6, P_SPREAD, 110, P_VINTAGE, 90,
    P_O2_WAVE, W_SAW, P_O2_SEMI, 12, P_O2_LVL, 80, P_CUTOFF, 76, P_RESO, 30, P_FENV_AMT, 96, P_AR, 62,
    P_LFO_SHAPE, L_SQR, P_LFO_RATE, 119, P_LFO_DELAY, 19, P_LFO_AMP, 100, P_VOLUME, 112, X};
/* 04 V-Sync (voiced 4 Nov, approved 5 Nov: dog5-docs/voicing/04-v-sync.md; PF_SYNC_LEAD stays as 20 Fire & Ice's and 26 BSyncA's): a fat sync lead. UNISON, two
 * voices detuned ~5.5 cents (DETUNE 22), each with OSC 2 a fifth up (+7 st) hard-synced to OSC 1 and swept +18 st by the filter envelope (ENV>O2 112, 219 ms),
 * OSC 1's saw under it (LEVEL 80), DRIVE 20, a 5 ms release that stops the voice dead, only a faint 1/16 slap (MIX 12), no spring. VOLUME 91 puts it on the
 * bank reference (-18.0 dBFS RMS on the lead phrase, tests/voicing) */
static const uint8_t PF_V_SYNC[] = {P_O1_LVL, 80, P_O2_LVL, 127, P_O2_SEMI, 31, P_SYNC, 1, P_ENV_O2, 112,
    P_CUTOFF, 92, P_RESO, 24, P_FENV_AMT, 88, P_DRIVE, 20, P_FD, 78, P_FS, 28, P_FR, 30, P_AA, 0, P_AS, 127,
    P_AR, 30, P_MODE, M_UNISON, P_UNI_N, 2, P_UNI_DET, 22, P_GLIDE, 20, P_VOLUME, 91, P_DLY_TIME, DD_16,
    P_DLY_FB, 18, P_DLY_MIX, 12, X};
/* 30 THE D\xD8G (voiced 4 Nov, round 2 on 5 Nov: dog5-docs/voicing/30-the-dog.md; PF_DRONE_UNI stays as 18 Roto-scopo's; 21 Cowl Shadow has its own since Batch 2A): the
 * signature low stack. UNISON, all 8 voices on one note, DETUNE 35 (the stack spans ~15 cents; round 1 had ~9, the drone ~78), a sub-octave saw under every
 * voice, the filter wide (CUTOFF 104, ENV AMT 88 snaps it open on the attack, KEY TRK 60, sustain 40), a 0.7 ms attack and a 21 ms release
 * for a punchy chop, SPREAD 50 so the bass stays put in a mono PA, per-voice DRIVE 100 (FILTER+ page: warmth and weight without compression or
 * the CPU of GROWL, which stays 0), no spring. VOLUME 56 puts it at the TOP of the loudness band, -16.5 dBFS RMS on the low-unison phrase
 * (+1.5 dB over the -18.0 bank reference: the flagship's presence), peak -7.3 */
static const uint8_t PF_THE_DOG[] = {P_O1_LVL, 114, P_O2_LVL, 94, P_O2_SEMI, 12, P_CUTOFF, 104, P_RESO, 12,
    P_FENV_AMT, 88, P_KEYTRK, 60, P_DRIVE, 100, P_FA, 10, P_FD, 58, P_FR, 50, P_AA, 4, P_AS, 127, P_AR, 48,
    P_MODE, M_UNISON, P_UNI_N, 8, P_UNI_DET, 35, P_VINTAGE, 40, P_SPREAD, 50, P_VOLUME, 56, X};
/* 17 Titanic (voiced Nov 2026, dog5-docs/voicing/17-titanic.md; was PF_DUAL_SAW, this slot's alone): the chapter anchor. A DUAL pair (DETUNE 30, ~5.5 cents) of two
 * saws a fifth apart (OSC 2 +7 st, both at full level), the bass compensated to the extreme: KEY TRK 12 (9 %), so the filter opens for low notes and closes for high ones
 * (8.4 partials under the centroid on A1, 3.4 on A3). Cold: RESO 12, no drive, no effects, VINTAGE 40; a 54 ms attack and a long (~650 ms) release; the filter envelope
 * only breathes (ENV AMT 84, sustain 70). POLY 6 (every note is two voices). VOLUME 93 puts it on the bank reference (-17.9 dBFS RMS on the steady part of the A1 hold,
 * phrase f, tests/voicing; (b) reads -17.1). FX macros 0 */
static const uint8_t PF_TITANIC[] = {P_O2_SEMI, 31, P_CUTOFF, 66, P_RESO, 12, P_FENV_AMT, 84, P_KEYTRK, 12, P_FA, 62,
    P_FD, 90, P_FS, 70, P_FR, 85, P_AA, 60, P_AS, 127, P_AR, 92, P_MODE, M_DUAL, P_VINTAGE, 40, P_SPREAD, 110,
    P_VOLUME, 93, P_POLY_N, 6, X};
/* 21 Cowl Shadow (voiced Nov 2026, approved variant C: dog5-docs/voicing/21-cowl-shadow.md; PF_DRONE_UNI stays as 18 Roto-scopo's): a brass wall that blooms in about 5 s. UNISON, 5 voices of two
 * saws on the same pitch (DETUNE 40: the stack spans +-9.8 cents), a dark start (CUTOFF 40) and a 5.3 s filter attack (ATTACK 119, ENV AMT 118, KEY TRK 127 so the bloom is the same at any
 * pitch), both sustains full (the gate held open), a 0.6 s amp attack. Held, the centroid climbs 3.1 octaves on A2 (10 % of the climb at 0.8 s, 90 % at 4.1 s); let go early it is a dark short
 * note that fades (no latch in the engine: the bloom happens while the key is down); after a long hold the filter closes with the level (RELEASES 2.7 / 2.3 s). Dry, no LFO, no spring.
 * VOLUME 79 puts it on the bank reference: -18.0 dBFS RMS over +6..+10 s of the A2 hold (phrase f2) */
static const uint8_t PF_COWL_SHADOW[] = {P_O2_FINE, 66, P_CUTOFF, 40, P_RESO, 14, P_FENV_AMT, 118, P_KEYTRK, 127,
    P_FA, 119, P_FS, 127, P_FR, 110, P_AA, 90, P_AS, 127, P_AR, 108, P_MODE, M_UNISON, P_UNI_N, 5, P_UNI_DET, 40,
    P_VINTAGE, 45, P_SPREAD, 100, P_VOLUME, 79, X};
/* 09 Skeenhead (voiced Nov 2026, approved round 2 variant E: dog5-docs/voicing/09-skeenhead.md; was PF_CLAV_PLUCK, this slot's alone): the reggae off-beat stab. One 50 % pulse through a resonant 12 dB low-pass (RESO 62) whose envelope
 * still plops (FILTER DECAY 39 ms) but now RESTS above the notes (CUTOFF 46, FILTER SUSTAIN 40: round 1's filter shut below the notes in ~25 ms and left a hum) with the amp holding 64 of 127 through the gate (4 ms release); drenched
 * in spring as before: DRAIN 90, SIZE 70, DAMP 40, PRE-DLY 4 (1.1 ms), tail -60 dB at 1.07 s. VOLUME 92 puts it on the bank reference: -17.9 dBFS RMS over the stabs of the skank phrase (g) with the spring on (peak -6.3) */
static const uint8_t PF_SKEENHEAD[] = {P_O1_WAVE, W_PLS, P_O2_WAVE, W_OFF, P_CUTOFF, 46, P_RESO, 62, P_FENV_AMT, 118,
    P_KEYTRK, 100, P_FTYPE, F_LP12, P_FD, 56, P_AA, 0, P_AS, 64, P_AR, 28, P_VOLUME, 92, P_REV_SIZE, 70,
    P_REV_DAMP, 40, P_REV_PRE, 4, P_REV_MIX, 90, X};
/* 11 Slapback Strut (voiced Nov 2026, approved round 2 variant G: dog5-docs/voicing/11-slapback-strut.md; PF_SUB_BASS stays as 05 ZEAROX's and 19 Blackwater's): the surf bass, a GATED note with a crisp slap. MONO, one narrow
 * pulse (PW 32 %; the engine has no triangle) through a key-tracking 12 dB low-pass (CUTOFF 82, KEY TRK 90) with per-voice DRIVE 40; no real decay (a 36 ms settle to a sustain at 79 %, 1 ms releases): the note starts at once, holds
 * its body for the gate and stops in ~1 ms; one clean mono slap: ALLEY 62 = 80 ms, FEEDBK 6, MIX 127 (the top), TONE 127, PINGPONG 0: the first repeat -6.0 dB under the note's peak, the second 29 dB under the first. Dry (no spring).
 * VOLUME 102 puts it on the bank reference: -18.0 dBFS RMS over the note-on region of the surf riff (phrase h), echo included */
static const uint8_t PF_SLAPBACK_STRUT[] = {P_O1_WAVE, W_PLS, P_O1_PW, 32, P_O1_LVL, 127, P_O2_WAVE, W_OFF,
    P_CUTOFF, 82, P_RESO, 16, P_FENV_AMT, 76, P_KEYTRK, 90, P_FTYPE, F_LP12, P_DRIVE, 40, P_FA, 0, P_FD, 55,
    P_FS, 100, P_FR, 10, P_AA, 0, P_AD, 55, P_AR, 10, P_MODE, M_MONO, P_GLIDE, 5, P_VOLUME, 102, P_DLY_FB, 6,
    P_DLY_TONE, 127, P_DLY_MIX, 127, P_ALLEY, 62, P_BBD_SPREAD, 0, X};
/* 01 Red Pill (voiced Nov 2026, approved Batch 3A variant C: dog5-docs/voicing/01-red-pill.md; was PF_FAT_BASS, which 06 zzuFuzz and 27 R3V3RT shared and 27 keeps): the nervous, spitting bass under a vocal. MONO, two saws at one pitch 7.8 cents
 * apart, TIGHT (VINTAGE 10, no LFO, no glide), a resonant 24 dB low-pass (CUTOFF 92, KEY TRK 100, RESO 58) whose envelope falls in 29 ms (the spit), grit from per-voice DRIVE 110 and a GROWL 46 step (BIAS 30, TONE 55; GROWL costs ~+595 instr/sample);
 * relatively dry: a mono slap at 80 ms (ALLEY 62, FEEDBK 10, MIX 16) and a short spring (DRAIN 18, SIZE 40), worst return -43.6 / -25.0 / -16.5 dB re the dry note in the 0-20 / 20-100 / 100-250 ms windows. VOLUME 87: -18.0 dBFS RMS over the
 * note-on region of the spit riff (phrase i), peak -12.8 (phrase b -18.0). Slot 1 is the boot patch */
static const uint8_t PF_RED_PILL[] = {P_O2_PW, 50, P_O2_LVL, 104, P_O2_FINE, 74, P_CUTOFF, 92, P_RESO, 58,
    P_FENV_AMT, 104, P_KEYTRK, 100, P_DRIVE, 110, P_FA, 0, P_FD, 52, P_FS, 30, P_FR, 40, P_AA, 0, P_AS, 127,
    P_AR, 26, P_MODE, M_MONO, P_VINTAGE, 10, P_SPREAD, 40, P_VOLUME, 87, P_GRL_BIAS, 30, P_GRL_TONE, 55, P_GROWL, 46,
    P_DLY_FB, 10, P_DLY_TONE, 60, P_DLY_MIX, 16, P_REV_SIZE, 40, P_REV_DAMP, 70, P_REV_MIX, 18, P_ALLEY, 62,
    P_BBD_SPREAD, 0, X};
/* 02 Cement Grind (voiced Nov 2026, approved Batch 3A variant D: dog5-docs/voicing/02-cement-grind.md; was PF_WOBBLE_BASS, this slot's alone): the low-mid grinder. MONO, two PULSE oscillators (PW 36 %, 7.8 cents apart) with a FAST PWM:
 * a triangle LFO at 11.5 Hz (LFO RATE 108) on the pulse width, +-18 points (LFO PWM 110), restarting with each detached note (PHASE SYNC), and the same LFO wobbling the filter (LFO FILTER 28): the one LFO serves both, so the original 0.5 Hz filter wobble is gone.
 * Measured on the held A2: 150-400 Hz band 11.9 dB peak to peak, 400-1.2k 6.7 dB, 4.1 dB of level. A biting 12 dB low-pass (CUTOFF 60, RESO 62, filter decay 46 ms), per-voice DRIVE 78, GLIDE 12 for the skid.
 * VOLUME 87: -17.9 dBFS RMS over the note-on region of the grind riff (phrase j), peak -14.6 */
static const uint8_t PF_CEMENT_GRIND[] = {P_O1_WAVE, W_PLS, P_O1_PW, 46, P_O2_WAVE, W_PLS, P_O2_PW, 46,
    P_O2_LVL, 104, P_O2_FINE, 74, P_CUTOFF, 60, P_RESO, 62, P_FENV_AMT, 96, P_FTYPE, F_LP12, P_DRIVE, 78, P_FA, 0,
    P_FD, 58, P_FS, 45, P_FR, 40, P_AA, 1, P_AS, 127, P_AR, 20, P_LFO_RATE, 108, P_LFO_PHASE, LP_SYNC,
    P_LFO_PWM, 110, P_LFO_FLT, 28, P_MODE, M_MONO, P_GLIDE, 12, P_VOLUME, 87, X};
/* 06 zzuFuzz (voiced Nov 2026, approved Batch 3A variant C: dog5-docs/voicing/06-zzufuzz.md; was PF_FAT_BASS, which 01 Red Pill and 27 R3V3RT shared and 27 keeps): the player's fuzz, a wall. POLY (6 voices: a three-note power chord plays whole), every voice two saws
 * 9 cents apart at full level, per-voice DRIVE 100 into GROWL 104 (BIAS 72, TONE 64; ~+595 instr/sample), the filter open (LP24, CUTOFF 88, RESO 80: it only sings from about RESO 124) with a short snap (ENV AMT 120, decay 46 ms to sustain 40), AMP ATTACK 20 (2.4 ms,
 * measured 2.0 ms 10-90 % on the voice alone), AMP SUSTAIN 127 (the held note loses 0.0 dB in 3 s; crest 1.7 dB), AMP RELEASE 70 (-60 dB at 278 ms). Dry: ALLEY, DRAIN, CHEW 0. VOLUME 77: -18.1 dBFS RMS over the note-on region of the wall phrase (k), peak -12.8;
 * phrase (b) reads -16.1 (cause not isolated). VOLUME changes how a note from silence starts (GROWL's loudness trim reads the output stage) */
static const uint8_t PF_ZZUFUZZ[] = {P_O1_LVL, 118, P_O2_PW, 50, P_O2_LVL, 118, P_O2_FINE, 76, P_CUTOFF, 88,
    P_RESO, 80, P_FENV_AMT, 120, P_DRIVE, 100, P_FA, 2, P_FD, 58, P_FR, 40, P_AA, 20, P_AD, 75, P_AS, 127, P_AR, 70,
    P_VINTAGE, 60, P_SPREAD, 70, P_VOLUME, 77, P_GRL_BIAS, 72, P_GRL_TONE, 64, P_GROWL, 104, P_POLY_N, 6, X};
/* 08 Wire Bite (voiced Nov 2026, approved Batch 3A variant D: dog5-docs/voicing/08-wire-bite.md; was PF_UNISON_LEAD, this slot's alone): the anxious drone that bites. A 6-voice UNISON in the high register: OSC 1 a narrow pulse (PW 14 %), OSC 2 a 50 % pulse
 * 19 semitones up, through a resonant 12 dB low-pass (CUTOFF 90, RESO 66, ENV AMT 124, decay 40 = 11 ms to a low sustain). Bright (centroid 3855 Hz on the wire phrase), which reduces the measured zap (top burst -2.0 dB on the held A4, +0.5 dB on a bite; approved by ear).
 * Drifting: VINTAGE 127 (the six voices wander 3.8-5.7 cents s.d. each, static offsets -9 to +7 cents) and a smooth-random pitch LFO (LFO RATE 34 = 0.28 Hz, PITCH 16 = +-19 cents, PHASE SPREAD). Dry (DLY_TIME / FEEDBK are leftovers at DLY MIX 0):
 * chopped, -40 dB 18 ms after a bite. VOLUME 58: -17.9 dBFS RMS over the note-on region of the wire phrase (l), peak -8.9 */
static const uint8_t PF_WIRE_BITE[] = {P_O1_WAVE, W_PLS, P_O1_PW, 18, P_O1_LVL, 108, P_O2_WAVE, W_PLS, P_O2_PW, 50,
    P_O2_SEMI, 43, P_O2_FINE, 67, P_CUTOFF, 90, P_RESO, 66, P_FENV_AMT, 124, P_KEYTRK, 70, P_FTYPE, F_LP12,
    P_DRIVE, 40, P_FA, 0, P_FD, 40, P_FS, 20, P_FR, 30, P_AA, 2, P_AS, 127, P_AR, 14, P_LFO_SHAPE, L_RND,
    P_LFO_RATE, 34, P_LFO_PHASE, LP_SPREAD, P_LFO_PITCH, 16, P_MODE, M_UNISON, P_UNI_N, 6, P_UNI_DET, 50,
    P_VINTAGE, 127, P_SPREAD, 100, P_VOLUME, 58, P_DLY_TIME, DD_4, P_DLY_FB, 35, X};
static const uint8_t PF_INIT[] = {X};
#undef X

static const factory_t FACT_INIT = {"INIT", PF_INIT};   /* 33-99 */

/* The DØG-5 factory: the 32 patches of dog5-docs/DOG-5-presets.md §3, in its slot order, their final names
 * (14-char field; "THE DØG" needs the Ø byte 0xD8, so it is written "\xD8", not a UTF-8 literal). The SOUND of
 * each is, for now, its documented "nearest base patch" (the PF_* above, kept as the starting point) -- the
 * final by-ear voicing is Stage 2 (presets §6), so several slots that share a base sound alike today. Slots
 * 33-99 fall back to FACT_INIT (prog_get). */
static const factory_t FACTORY[NFACT] = {
    {"Red Pill", PF_RED_PILL},      {"Cement Grind", PF_CEMENT_GRIND}, {"Half-Life", PF_HALF_LIFE},    {"V-Sync", PF_V_SYNC},
    {"ZEAROX", PF_SUB_BASS},        {"zzuFuzz", PF_ZZUFUZZ},         {"Tape Splice", PF_XMOD_GROWL},{"Wire Bite", PF_WIRE_BITE},
    {"Skeenhead", PF_SKEENHEAD},   {"Atlantic Swell", PF_HOLLOW_PAD},{"Slapback Strut", PF_SLAPBACK_STRUT},{"Kelp Tangle", PF_HOLLOW_PAD},
    {"Ghost Board", PF_PWM_STRINGS},{"Reef Break", PF_PERC_HIT},      {"Trem Chop", PF_SQUARE_LEAD}, {"Tidal Pull", PF_PWM_STRINGS},
    {"Titanic", PF_TITANIC},       {"Roto-scopo", PF_DRONE_UNI},     {"Blackwater", PF_SUB_BASS},   {"Fire & Ice", PF_SYNC_LEAD},
    {"Cowl Shadow", PF_COWL_SHADOW},  {"Melting Orb", PF_BP_QUACK},     {"Crypt Dust", PF_NOISE_WASH}, {"Fugue State", PF_NEON_PAD},
    {"SAWTOOTH", PF_SAWTOOTH},    {"BSyncA", PF_SYNC_LEAD},         {"R3V3RT", PF_FAT_BASS},       {"Bell Tolls", PF_BELL_XMOD},
    {"VALHALLA", PF_VINTAGE_PAD},   {"THE D\xD8G", PF_THE_DOG},     {"Fi(l)fth", PF_FIFTH},  {"Init bruv?", PF_INIT},
};
