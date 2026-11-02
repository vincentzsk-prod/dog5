/* SPDX-License-Identifier: GPL-3.0-only
 * SMK-37 port of OberVave: Copyright (C) 2026 zvenson */
/* OberVave on the M-Vave SMK-37 (BOARD_SMK37; SMK37.md, smk37-port.yaml). The FM-1's panel keeps its jobs (the
 * middle 27 keys, the 14 buttons by printed name, the knobs: platform.c); this file adds what the SMK has more:
 *
 *   outer keys  C3-E3 and G#5-C6 extend the keyboard (notes below F3 and above G5), with velocity, through the
 *               same path as the keys
 *   keys        velocity from the unit's factory curves (hal/smk_input.h); the FM-1 plays 100
 *   faders      two banks, FADER BANK switches (LED lit on B): A = PERFORM's CUTOFF RESO ENV AMT RELEASE,
 *               B = CHORUS / DELAY / REVERB mix and MASTER (the level K1 turns). A fader acts once it moves (also
 *               after a bank change), so nothing jumps; a short bar under the page shows it
 *   wheels      pitch = bend, +-2 semitones (the program's BEND range, 2 in every factory program), every voice;
 *               mod = a gentle vibrato from the program's LFO, up to +-1/2 semitone (obv_engine.h ctl_vib).
 *               Self-calibrating (smk_wheel.h)
 *   KNOB BANK   held: the panel check (a bring-up screen in place of a serial console: the flash part, the factory
 *               calibration, the ADC, faders, wheels, keys, buttons and every pad's reading above its baseline)
 *
 * (The pads were OberVave's step sequencer and < > its page nav; both free, pads dark, with the sequencer DØG-5
 * deleted: CLAUDE.md §5.)
 */
#include "smk_wheel.h"

static uint32_t smk_bank;                       /* FADER BANK: 0 = A (PERFORM), 1 = B (effects, MASTER) */
static uint8_t smk_fad_last[4] = {0xFF, 0xFF, 0xFF, 0xFF};
static uint8_t smk_ext_note[FM1_NKEY];          /* an outer key's note, so its release knows what to end */
static const char *smk_ov1;                     /* the overlay under the page (faders, banks), 1.5 s */
static char smk_ov2[40];
static uint32_t smk_ov_t, smk_ov_on, smk_ov_dirty;

static void smk_overlay(const char *l1, const char *l2)
{
    uint32_t i;
    smk_ov1 = l1;
    for (i = 0; l2[i] && i + 1u < sizeof smk_ov2; i++) smk_ov2[i] = l2[i];
    smk_ov2[i] = 0;
    smk_ov_t = fm1_ms;
    smk_ov_on = smk_ov_dirty = 1;
}

/* in the screen's 40 ms slot: 1 while the overlay holds the hints / voice-LED strip (it redraws them when it ends) */
static int smk_overlay_draw(uint32_t *leds_q)
{
    if (!smk_ov_on) return 0;
    if (fm1_ms - smk_ov_t >= 1500u) {
        smk_ov_on = 0;
        hints_key = 0xFFFFFFFFu;
        *leds_q = 0xFFFFFFFFu;
        return 0;
    }
    if (smk_ov_dirty) { smk_ov_dirty = 0; ui_hints(smk_ov1, smk_ov2, C_AMBER); }
    return 1;
}

static void smk_bar(char *s, uint32_t v, uint32_t max)   /* [#######---------] */
{
    uint32_t k, f = max ? (v * 16u + max / 2u) / max : 0u;
    s[0] = 0;
    scat(s, "[");
    for (k = 0; k < 16u; k++) scat(s, k < f ? "#" : "-");
    scat(s, "]");
}

/* ---- the outer keys (main loop, after the keys): more notes, the keys' own path */
static void smk_extkeys(uint32_t base)
{
    int32_t e;
    while ((e = smk_extkey_take()) >= 0) {
        uint32_t kk = ((uint32_t)e >> 8) % FM1_NKEY, vel = (uint32_t)e & 0xFFu;
        if (vel) {
            uint32_t n = (uint32_t)clampi((int32_t)base + (int32_t)kk - (int32_t)SMK_KEY_F3, 1, 127);
            smk_ext_note[kk] = (uint8_t)n;
            play_note(1, n, vel); midi_send(0x90u | MIDI_OUT_CH, n, vel);
        } else if (smk_ext_note[kk]) {
            uint32_t n = smk_ext_note[kk];
            smk_ext_note[kk] = 0;
            play_note(0, n, 0); midi_send(0x80u | MIDI_OUT_CH, n, 0);
        }
    }
}

/* ---- FADER BANK (main loop, with the other buttons) */
static void smk_buttons(uint32_t b)
{
    if (b & (1u << BTN_FADER_BANK)) {
        uint32_t i;
        smk_bank ^= 1u;
        for (i = 0; i < 4u; i++) smk_fad_last[i] = 0xFF;   /* a new bank: each fader waits until it moves */
        smk_overlay(smk_bank ? "FADER BANK B" : "FADER BANK A",
                    smk_bank ? "CHORUS DELAY REVERB MASTER" : "CUTOFF RESO ENV AMT RELEASE");
    }
}

/* ---- the faders: two banks, a fader acts once it moves */
static void smk_faders(uint32_t *dirty_page, uint32_t *dirty_hdr, uint32_t *dirty_tags)
{
    static const int8_t FP[2][4] = {{P_CUTOFF, P_RESO, P_FENV_AMT, P_AR}, {P_CHO_MIX, P_DLY_MIX, P_REV_MIX, -1}};
    static const char *const FN[2][4] = {{"CUTOFF", "RESO", "ENV AMT", "RELEASE"}, {"CHORUS", "DELAY", "REVERB", "MASTER"}};
    static char l1[32], l2[32];
    uint32_t i;
    for (i = 0; i < 4u; i++) {
        uint32_t v = fm1_in.fader[i];
        int32_t p = FP[smk_bank][i];
        char val[12];
        if (smk_fad_last[i] == 0xFF || fm1_in.frames < 200u) {   /* (the first readings settle) */
            smk_fad_last[i] = (uint8_t)v;
            continue;
        }
        if (v == smk_fad_last[i]) continue;
        smk_fad_last[i] = (uint8_t)v;
        if (p >= 0) {
            set_param((uint32_t)p, (int32_t)(v * PDEF[p].max + 63u) / 127);
            param_value(val, (uint32_t)p, live.v[p]);
            if (p == P_CUTOFF) cut_shown_t = fm1_ms + 1u;
            *dirty_page = *dirty_hdr = 1;
            if (smk_bank) *dirty_tags = 1;      /* (the FX tag) */
        } else {
            smk_master = (int32_t)(v * 1023u / 127u);   /* MASTER: the level K1 turns (hal/smk_input.h) */
            fmt_u(val, (v * 100u + 63u) / 127u); scat(val, "%");
        }
        l1[0] = 0;
        scat(l1, smk_bank ? "B" : "A"); fmt_u(l1 + 1, i + 1u); scat(l1, " "); scat(l1, FN[smk_bank][i]); scat(l1, " "); scat(l1, val);
        smk_bar(l2, v, 127u);
        smk_overlay(l1, l2);
    }
}

/* ---- the wheels (also between frames: bends follow the wheel, not the screen) */
static void smk_wheels(void)
{
    enum { DEAD = 12, MOD_LO = 485, MOD_HI = 615 };
    static smk_pw_t pw;
    static int32_t mlo, mhi, last_b = 0x7FFFFFFF, last_m = -1;
    int32_t m = fm1_in.wheel[1], mw, b;
    if (fm1_in.frames < 300u)                   /* (the readings settle) */
        return;
    if (!mhi) {
        mlo = m < MOD_LO ? m : MOD_LO;
        mhi = m > MOD_HI ? m : MOD_HI;
    }
    if (m < mlo) mlo = m;
    if (m > mhi) mhi = m;
    mw = mhi - m <= DEAD ? 0 : (mhi - m - DEAD) * 127 / (mhi - mlo - DEAD > 1 ? mhi - mlo - DEAD : 1);   /* up = lower raw */
    mw = clampi(mw, 0, 127);
    b = smk_pw_bend(&pw, fm1_in.wheel[0], fm1_ms) * 8192 / (SMK_PW_ST * 4096);   /* -> the MIDI bend's -8192..8191 */
    b = clampi(b, -8192, 8191);
    if (b != last_b) { last_b = b; ctl_bend = b; }   /* (only on a change: a MIDI bend in still works at rest) */
    if (mw != last_m) { last_m = mw; ctl_vib = mw; }
}

/* ---- the pads' and the extra buttons' lights */
static void smk_leds(void)
{
    uint32_t p;
    for (p = 0; p < 16u; p++) padled_set(p, 0, 0, 0);   /* the pads are free (DØG-5 deleted the sequencer) */
    fm1_led_key(BTN_FADER_BANK, smk_bank != 0u);
    fm1_led_key(BTN_KNOB_BANK, fm1_in.buttons >> BTN_KNOB_BANK & 1u);   /* (lit while the panel check is up) */
    padled_flush();                             /* (only when a colour changed; between LCD transfers) */
}

/* ---- KNOB BANK held: the panel check (OberVave has no serial console; this is what the kit's "smk" command shows) */
static void smk_hex(char *s, uint32_t v, uint32_t n)
{
    uint32_t k;
    for (k = 0; k < n; k++) s[k] = "0123456789ABCDEF"[(v >> (4u * (n - 1u - k))) & 15u];
    s[n] = 0;
}
static int smk_check(uint32_t *redraw)
{
    static uint32_t on, t;
    static char ln[12][32];
    uint32_t i, k;
    if (!(fm1_in.buttons >> BTN_KNOB_BANK & 1u)) {
        if (on) { on = 0; *redraw = 1; }
        return 0;
    }
    if (on && fm1_ms - t < 100u) return 1;
    on = 1;
    t = fm1_ms;
    for (i = 0; i < 12u; i++) ln[i][0] = 0;
    scat(ln[0], "PANEL CHECK");
    scat(ln[1], "FLASH "); smk_hex(ln[1] + 6, smk_jedec, 6); scat(ln[1], smk_trim_ok ? " TRIM OK" : " TRIM DEFAULT");
    scat(ln[2], "ADC "); fmt_u(ln[2] + 4, fm1_in.adc_ok % 100000u); scat(ln[2], " MISS "); fmt_u(ln[2] + slen(ln[2]), fm1_in.adc_miss % 10000u);
    scat(ln[3], "FADER");
    for (k = 0; k < 4u; k++) { scat(ln[3], " "); fmt_u(ln[3] + slen(ln[3]), fm1_in.fader[k]); }
    scat(ln[3], " BAT "); fmt_u(ln[3] + slen(ln[3]), fm1_in.batt);
    scat(ln[4], "WHEEL "); fmt_u(ln[4] + 6, fm1_in.wheel[0]); scat(ln[4], " "); fmt_u(ln[4] + slen(ln[4]), fm1_in.wheel[1]);
    scat(ln[4], " B"); fmt_s(ln[4] + slen(ln[4]), ctl_bend / 64); scat(ln[4], " V"); fmt_u(ln[4] + slen(ln[4]), (uint32_t)ctl_vib);
    scat(ln[5], "BTN "); smk_hex(ln[5] + 4, fm1_in.buttons, 5);
    for (k = 0; k < FM1_NKEY && !(fm1_in.keys >> k & 1u); k++) ;
    if (k < FM1_NKEY) { scat(ln[5], " KEY "); fmt_u(ln[5] + slen(ln[5]), k); scat(ln[5], " V"); fmt_u(ln[5] + slen(ln[5]), fm1_in.key_vel[k]); }
    if (smk_store_cleared) scat(ln[6], "STORE: OTHER DATA CLEARED");
    scat(ln[7], "PADS: READING - BASELINE");
    for (i = 0; i < 4u; i++) {                  /* pads 1-4, 5-8 (top row), 9-12, 13-16 */
        fmt_u(ln[8 + i], 4u * i + 1u); scat(ln[8 + i], "-"); fmt_u(ln[8 + i] + slen(ln[8 + i]), 4u * i + 4u); scat(ln[8 + i], ":");
        for (k = 4u * i; k < 4u * i + 4u; k++) {
            int32_t d = (int32_t)fm1_in.pad_raw[k] - (int32_t)fm1_in.pad_base[k];
            scat(ln[8 + i], " "); fmt_s(ln[8 + i] + slen(ln[8 + i]), d);
        }
    }
    for (k = 0; k < 2u; k++) {
        cv_begin(240, 120, C_PANEL);
        for (i = 0; i < 6u; i++) cv_text(6, (int32_t)i * 19 + 4, &FONT_S, ln[6u * k + i], k == 0u && i == 0u ? C_AMBER : C_CREAM);
        cv_blit(0, 120u * k);
    }
    return 1;
}

#ifdef OBV_HOST
/* the host test's "dump" (tests/host.c): the pads (free, always dark) and the controls */
static void host_dump(void)
{
    uint32_t p;
    printf("%6u ms  PADS", fm1_ms);
    for (p = 0; p < 16u; p++) printf(" %06X", padled_rgb[p]);
    printf("\n%6u ms  STATE bank=%u bend=%d vib=%d master=%d cutoff=%u reso=%u envamt=%u release=%u cho=%u dly=%u rev=%u\n",
           fm1_ms, smk_bank, ctl_bend, ctl_vib, smk_master,
           live.v[P_CUTOFF], live.v[P_RESO], live.v[P_FENV_AMT], live.v[P_AR], live.v[P_CHO_MIX], live.v[P_DLY_MIX],
           live.v[P_REV_MIX]);
}
#endif
