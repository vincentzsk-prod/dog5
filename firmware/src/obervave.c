/* SPDX-License-Identifier: GPL-3.0-only */
/* DØG-5 (forked from OberVave): one 8-voice analog-style polysynth for the M-VAVE FM-1. Built on Dinghy's
 * platform (platform.c: boot, USB, updates, audio ISR, settings).
 *
 *   obv_dsp.h       oscillators (polyBLEP events), filter (trapezoidal SVF), tanh
 *   obv_params.h    the parameter table: patches, pages, MIDI CC
 *   obv_drive.h     GROWL, the preamp drive (on the voice bus, before the output stage)
 *   obv_tape.h      CHEW, the tape (wow, flutter, saturation, head loss, hiss, dropouts; last, after the reverb)
 *   obv_deck.h      TAPE STOP: the whole mix slows and darkens (SEQ held), after everything, before STOP's gate
 *   obv_fx.h        ALLEY (the BBD delay), DRAIN (the spring) (after the output stage, same ISR)
 *   obv_engine.h    the voices, envelopes, LFO, arpeggiator: all in the audio ISR
 *   obv_patches.h   the factory programs
 *   this file       the panel, MIDI, the screen, the storage
 *
 * (OberVave's step sequencer, obv_seq.h, and the two-sound track B it alone drove, are gone: CLAUDE.md §5.
 * PLAY is STOP, the kill switch; SEQ held, TAPE STOP; ALGORITHM, the SLOP ride; REC, HOLD; SELECT on HOME, the LFO
 * rate; EDIT held + a black key, a page jump. The tap tempo is gone.)
 *
 * Integers only (no FPU, no 64-bit division); tests/host.c runs this on a computer. */
static void app_idle(void);
#define LCD_IDLE() app_idle()                   /* (lcd.c: while the DMA runs) */
#include "platform.c"
#include "obv_dsp.h"
#include "obv_params.h"
#include "obv_fx.h"
#include "obv_drive.h"
#include "obv_tape.h"
#include "obv_engine.h"
#include "obv_deck.h"                             /* (after the engine: it reads the tempo; the engine calls it) */
#include "obv_patches.h"

static void app_audio(int32_t *out, uint32_t n)
{
#ifndef OBV_HOST
    uint32_t t0 = fm1_ticks();
#endif
    engine_audio(out, n);
#ifndef OBV_HOST
    ui_render_us = (fm1_ticks() - t0) / FM1_TICKS_PER_US;
#endif
}

/* ---- what survives a power-off: the user programs and the globals, one settings sector */
#define SET_VERSION 3u                          /* 3: the programs in their own sectors (99); 2: 32 in here, 80 bytes */
static struct {
    uint8_t version, prog, tempo, midi_ch;      /* midi_ch 0 = omni, else 1..16 */
    int8_t tune, oct;
    uint8_t fleas, click;                       /* fleas: FLEAS, the screen's rot, 0..100 (Batch 23: the byte the sequencer's
                                                  * pattern number had); click: unused (the sequencer's). The layout and
                                                  * SET_VERSION are unchanged */
} set;
#define MIDI_OUT_CH (set.midi_ch ? set.midi_ch - 1u : 0u)   /* the keys go out on the MIDI channel set (OMNI: 1) */
/* (the OberVave SET_VERSION 2 migration that brought 32 old programs over embedded an 80-byte patch_t; with the
 * 96-byte DØG-5 record its layout no longer matches, and a DØG-5 FM-1 arrives empty, so it is dropped -- old
 * settings/program sectors read as empty, never misread.) */
static uint32_t set_dirty, set_t;
/* the user's programs: PS_N to a flash sector (psect_load / psect_save), all of them in RAM */
#define PS_N 42u                                /* 96-byte patches: 42 per 4 KiB sector (42*96=4032; psect_t=4080 <= SETTINGS_MAX=4084) */
#define PS_TAG 0x35474F44u                      /* "DOG5": the 96-byte program format. Old "BOVP"/80-byte sectors fail
                                                 * sector_load's length check (and this tag check) and read as empty. */
typedef struct { uint32_t tag; uint8_t used[PS_N], pad[2]; patch_t p[PS_N]; } psect_t;
_Static_assert(sizeof(psect_t) <= SETTINGS_MAX, "a program sector outgrew its flash sector");
_Static_assert(NPSECT * PS_N >= NPROG, "too few program sectors");
static psect_t psect[NPSECT];
static uint32_t ps_dirty;                       /* bit i: program sector i to save */

static uint32_t prog, edited, page = PG_PERFORM, hold, save_armed, save_t, save_to;   /* save_to: SAVE's slot (PRESETS) */   /* hold: the sound's HOLD */
static uint32_t toast_t;
static const char *toast;
/* the panel as sloopDX's: a function button tapped (let go, nothing else touched) opens its pages; FX held is a
 * layer (its knobs change job until it is let go; HOME tapped while it is held locks it open). (DØG-5 deleted the
 * sequencer and the two-sound track B it alone drove: obv_seq.h, CLAUDE.md §5.) The live tricks claim the buttons it
 * freed: PLAY = STOP, the kill switch (below); SEQ held = TAPE STOP (obv_deck.h); ALGORITHM = the SLOP ride. */
enum { L_NONE, L_FX };
/* PLAY (HEEL) = STOP, the kill switch (obv_engine.h: a 5.8 ms fade, then every voice and effect cleared). A tap stops,
 * a tap starts again; the PLAY LED is lit and the header says STOPPED while it is down. KILL_MOMENTARY 1: silence only
 * while PLAY is held */
#define KILL_MOMENTARY 0
static uint32_t killed;
static uint32_t layer, layer_lock, layer_used, layer_t, layer_btn;
#define KEY_VEL(k) 100
#define NM_PRESETS "PRESETS"
static void say(const char *s) { toast = s; toast_t = fm1_ms; }
static uint8_t cc_map[128];                     /* MIDI CC -> parameter + 1, 0 = none */

/* THE POUND and THE PACK: programs 1-32 (0-idx < NFACT) are the factory's and locked, always read from the firmware (so a
 * firmware update brings its voicing with it); SAVE writes only 33-99, the user's. The store below the lock (psect,
 * prog_put) is unchanged and still has room for all 99. */
#define PACK_N (NPROG - NFACT)                  /* THE PACK: 67 slots */
static void prog_get(uint32_t n, patch_t *p)    /* program n: 1-32 the factory's; 33-99 the user's, else INIT */
{
    n %= NPROG;
    if (n >= NFACT && psect[n / PS_N].used[n % PS_N]) *p = psect[n / PS_N].p[n % PS_N];
    else {
        patch_from_factory(p, n < NFACT ? &FACTORY[n] : &FACT_INIT);
        if (n < NFACT) p->v[PATCH_CHAPTER_AT] = (uint8_t)(n / 8u + 1u);   /* the factory patch's own scene (Batch 22) */
    }
}

/* the scene HOME shows for a patch in slot n: the chapter it carries, else the slot's (1-8 I, 9-16 II, ..., THE PACK cycling) */
static uint32_t patch_chapter(const patch_t *p, uint32_t n)
{
    uint32_t c = p->v[PATCH_CHAPTER_AT];
    return c >= 1u && c <= 4u ? c - 1u : n % NFACT / 8u;
}

static void prog_put(uint32_t n, const patch_t *p)   /* program n is the user's now; saved when quiet */
{
    n %= NPROG;
    psect[n / PS_N].p[n % PS_N] = *p;
    psect[n / PS_N].used[n % PS_N] = 1;
    ps_dirty |= 1u << (n / PS_N);
    set_t = fm1_ms;
}

static uint32_t pack_free(void)                 /* the first PACK slot never saved to (all used: the first, 33) */
{
    uint32_t n;
    for (n = NFACT; n < NPROG; n++) if (!psect[n / PS_N].used[n % PS_N]) return n;
    return NFACT;
}

/* once, at power-on: a save over a POUND slot from before the lock (v0.1 / v0.2 let SAVE write 1-32) moves to the first free
 * PACK slot, so nothing saved is lost and the POUND reads the factory. With no free slot it stays where it was, unread. */
static void pound_rescue(void)
{
    uint32_t n, d;
    for (n = 0; n < NFACT; n++) {
        if (!psect[n / PS_N].used[n % PS_N]) continue;
        if ((d = pack_free()) == NFACT && psect[NFACT / PS_N].used[NFACT % PS_N]) break;   /* THE PACK is full */
        if (!psect[n / PS_N].p[n % PS_N].v[PATCH_CHAPTER_AT])   /* (it keeps the scene of the slot it was saved over) */
            psect[n / PS_N].p[n % PS_N].v[PATCH_CHAPTER_AT] = (uint8_t)(n / 8u + 1u);
        prog_put(d, &psect[n / PS_N].p[n % PS_N]);
        psect[n / PS_N].used[n % PS_N] = 0;
        ps_dirty |= 1u << (n / PS_N);
    }
}

static void load_program(uint32_t n)
{
    patch_t p;
    n %= NPROG;
    prog_get(n, &p);
    live = p;
    prog = n;
    edited = 0;
}

static void play_note(uint32_t on, uint32_t note, uint32_t vel) { note_event(on, note & 127u, vel); }

static void cc_map_init(void)
{
    uint32_t i, next = 20;
    for (i = 0; i < NPARAM; i++)
        if (PDEF[i].cc) cc_map[PDEF[i].cc] = (uint8_t)(i + 1u);
    for (i = 0; i < NPARAM; i++) {
        if (PDEF[i].cc) continue;
        while (next < 120u && (cc_map[next] || next == 64u)) next++;
        if (next < 120u) cc_map[next++] = (uint8_t)(i + 1u);
    }
}

static void set_param(uint32_t p, int32_t v)
{
    v = clampi(v, p == P_POLY_N ? 1 : 0, PDEF[p].max);   /* POLY is 1-8: the knob never shows 0 voices */
    if (live.v[p] == v) return;
    live.v[p] = (uint8_t)v;
    edited = 1;
}

/* REC: a new sound within useful ranges */
static uint32_t rnd;
static uint32_t rn(uint32_t lo, uint32_t hi) { return lo + xorshift(&rnd) % (hi - lo + 1u); }
static void randomize(void)
{
    uint32_t i, r;
    patch_t *d = &live;
    for (i = 0; i < NPARAM; i++) d->v[i] = PDEF[i].def;
    d->v[P_O1_WAVE] = (uint8_t)rn(1, 3);
    d->v[P_O2_WAVE] = (uint8_t)rn(0, 3);
    d->v[P_O1_PW] = (uint8_t)rn(10, 110);
    d->v[P_O2_PW] = (uint8_t)rn(10, 110);
    d->v[P_O2_LVL] = (uint8_t)rn(60, 127);
    r = rn(0, 9);
    d->v[P_O2_SEMI] = (uint8_t)(r < 4 ? 24 : r < 6 ? 12 : r < 8 ? 36 : r == 8 ? 31 : 43);
    d->v[P_O2_FINE] = (uint8_t)rn(60, 76);
    d->v[P_NOISE] = (uint8_t)(rn(0, 5) ? 0 : rn(10, 70));
    d->v[P_SYNC] = (uint8_t)(rn(0, 4) == 0);
    d->v[P_XMOD] = (uint8_t)(rn(0, 4) ? 0 : rn(20, 100));
    d->v[P_ENV_O2] = (uint8_t)(d->v[P_SYNC] ? rn(70, 110) : 64);
    d->v[P_CUTOFF] = (uint8_t)rn(30, 110);
    d->v[P_RESO] = (uint8_t)rn(0, 90);
    d->v[P_FENV_AMT] = (uint8_t)rn(60, 120);
    d->v[P_FTYPE] = (uint8_t)(rn(0, 2) ? F_LP24 : rn(0, NFTYPE - 1));
    d->v[P_FMORPH] = (uint8_t)rn(0, 127);
    d->v[P_DRIVE] = (uint8_t)(rn(0, 2) ? 0 : rn(10, 70));
    d->v[P_FA] = (uint8_t)rn(0, 90); d->v[P_FD] = (uint8_t)rn(30, 100); d->v[P_FS] = (uint8_t)rn(0, 100); d->v[P_FR] = (uint8_t)rn(20, 100);
    d->v[P_AA] = (uint8_t)rn(0, 80); d->v[P_AD] = (uint8_t)rn(30, 100); d->v[P_AS] = (uint8_t)rn(0, 127); d->v[P_AR] = (uint8_t)rn(20, 100);
    d->v[P_LFO_SHAPE] = (uint8_t)rn(0, 5);
    d->v[P_LFO_RATE] = (uint8_t)rn(20, 100);
    d->v[P_LFO_PITCH] = (uint8_t)(rn(0, 2) ? 0 : rn(5, 40));
    d->v[P_LFO_PWM] = (uint8_t)(rn(0, 1) ? 0 : rn(20, 90));
    d->v[P_LFO_FLT] = (uint8_t)(rn(0, 2) ? 0 : rn(10, 70));
    d->v[P_LFO_DELAY] = (uint8_t)rn(0, 70);
    d->v[P_LFO_PHASE] = (uint8_t)rn(0, 2);
    r = rn(0, 9);
    d->v[P_MODE] = (uint8_t)(r < 6 ? M_POLY : r < 7 ? M_DUAL : r < 9 ? M_UNISON : M_MONO);
    d->v[P_UNI_N] = (uint8_t)rn(2, 6);
    d->v[P_UNI_DET] = (uint8_t)rn(10, 80);
    d->v[P_GLIDE] = (uint8_t)(d->v[P_MODE] >= M_UNISON && rn(0, 1) ? rn(5, 40) : 0);
    d->v[P_VINTAGE] = (uint8_t)rn(0, 100);
    d->v[P_SPREAD] = (uint8_t)rn(20, 127);
    d->v[P_GROWL] = (uint8_t)(rn(0, 2) ? 0 : rn(30, 100));
    d->v[P_DLY_TIME] = (uint8_t)rn(0, NDDIV - 1);
    d->v[P_DLY_FB] = (uint8_t)rn(20, 80);
    d->v[P_DLY_MIX] = (uint8_t)(rn(0, 1) ? 0 : rn(20, 70));
    d->v[P_REV_SIZE] = (uint8_t)rn(40, 127);
    d->v[P_REV_MIX] = (uint8_t)(rn(0, 3) ? rn(15, 60) : 0);
    d->v[P_CHEW] = (uint8_t)(rn(0, 3) ? 0 : rn(15, 70));   /* (last: the draws above stay as they were) */
    edited = 1;
}

/* ---- the screen (obv_ui.h draws; this decides what and when) */
#include "obv_ui.h"
#include "dog5_scene.h"
#include "dog5_splash.h"

static void fmt_u(char *s, uint32_t v)          /* decimal, no leading zeros */
{
    char b[12];
    uint32_t i = 0, j = 0;
    do { b[i++] = (char)('0' + v % 10u); v /= 10u; } while (v);
    while (i) s[j++] = b[--i];
    s[j] = 0;
}
static uint32_t slen(const char *s) { uint32_t n = 0; while (s[n]) n++; return n; }
static void scat(char *d, const char *s) { d += slen(d); while ((*d++ = *s++)) ; }

static void fmt_ms(char *s, uint32_t ms_x10)
{
    char t[4];
    if (ms_x10 < 1000u) { fmt_u(s, ms_x10 / 10u); scat(s, "."); fmt_u(t, ms_x10 % 10u); scat(s, t); scat(s, "ms"); }
    else if (ms_x10 < 10000u) { fmt_u(s, ms_x10 / 10u); scat(s, "ms"); }
    else { fmt_u(s, ms_x10 / 10000u); scat(s, "."); fmt_u(t, (ms_x10 / 1000u) % 10u); scat(s, t); scat(s, "s"); }
}

static void param_value(char *s, uint32_t p, uint32_t v)   /* <= 7 characters */
{
    char t[8];
    s[0] = 0;
    switch (PDEF[p].kind) {
    case K_BIP: if (v < 64u) { scat(s, "-"); fmt_u(t, 64u - v); } else { scat(s, v > 64u ? "+" : ""); fmt_u(t, v - 64u); } scat(s, t); break;
    case K_ONOFF: scat(s, v ? "ON" : "OFF"); break;
    case K_WAVE: scat(s, WAVE_NAME[v & 3u]); break;
    case K_FTYPE: scat(s, FTYPE_NAME[v % NFTYPE]); break;
    case K_MODE: scat(s, MODE_NAME[v & 3u]); break;
    case K_LSHAPE: scat(s, LSHAPE_NAME[v % 6u]); break;
    case K_LPHASE: scat(s, LPHASE_NAME[v % 3u]); break;
    case K_TO: scat(s, TO_NAME[v % 3u]); break;
    case K_ARP: scat(s, ARP_NAME[v % NARPMODE]); break;
    case K_DIV: scat(s, DIV_NAME[v % NDIV]); break;
    case K_DDIV: scat(s, DDIV_NAME[v % NDDIV]); break;
    case K_MORPH:                               /* LP64 .. NOTCH .. HP63 */
        if (v == 64u) scat(s, "NOTCH");
        else { scat(s, v < 64u ? "LP " : "HP "); fmt_u(t, v < 64u ? 64u - v : v - 64u); scat(s, t); }
        break;
    case K_SEMI: if (v < 24u) { scat(s, "-"); fmt_u(t, 24u - v); } else { scat(s, v > 24u ? "+" : ""); fmt_u(t, v - 24u); } scat(s, t); break;
    case K_MS:
        if (p == P_GLIDE) { if (!v) scat(s, "OFF"); else { fmt_u(s, GLIDE_MS[v & 127u]); scat(s, "ms"); } }
        else fmt_ms(s, TIME_MS_X10[v & 127u]);
        break;
    case K_HZ: { uint32_t h = LFO_HZ_X100[v & 127u]; fmt_u(s, h / 100u); scat(s, "."); fmt_u(t, (h / 10u) % 10u); scat(s, t); scat(s, "Hz"); } break;
    case K_PCT: fmt_u(s, (v * 100u + 63u) / 127u); scat(s, "%"); break;
    case K_CUT: { uint32_t hz = CUT_HZ[(v + 8u) % 137u]; if (hz < 10000u) { fmt_u(s, hz); scat(s, "Hz"); } else { fmt_u(s, hz / 1000u); scat(s, "."); fmt_u(t, (hz / 100u) % 10u); scat(s, t); scat(s, "k"); } } break;
    case K_OCT: fmt_u(s, v); scat(s, " OCT"); break;
    case K_WF: if (v == 64u) scat(s, "BOTH"); else { scat(s, v < 64u ? "WOW+" : "FLT+"); fmt_u(t, v < 64u ? 64u - v : v - 64u); scat(s, t); } break;
    case K_DB12:                                /* 0 off, 1..127 = -12 .. +12 dB */
        if (!v) { scat(s, "OFF"); break; }
        { uint32_t d = ((v > 64u ? v - 64u : 64u - v) * 12u + 31u) / 63u; scat(s, v < 64u && d ? "-" : v > 64u && d ? "+" : ""); fmt_u(t, d); scat(s, t); scat(s, "dB"); }
        break;
    case K_REL: if (!v) scat(s, "OFF"); else { fmt_u(s, v < 64u ? (v * 100u + 32u) / 64u : 100u + ((v - 64u) * 200u + 31u) / 63u); scat(s, "%"); } break;
    case K_ALLEY: case K_AFINE:                 /* the time ALLEY + FINE make (both knobs show it); SYNC: the note value */
        {
            uint32_t a = p == P_ALLEY ? v : live.v[P_ALLEY], f = p == P_ALLEY_FINE ? v : live.v[P_ALLEY_FINE];
            if (!a) { if (p == P_ALLEY) { scat(s, "S "); scat(s, DDIV_NAME[live.v[P_DLY_TIME] % NDDIV]); } else scat(s, "-"); }
            else {                              /* (to the nearest ms from 100 ms: fmt_ms cuts the tenths there) */
                uint32_t x10 = (((uint32_t)alley_q16(a, f) >> 8) * 100u / 441u + 128u) >> 8;
                fmt_ms(s, x10 >= 1000u ? (x10 + 5u) / 10u * 10u : x10);
            }
        }
        break;
    case K_RVSIZE: fmt_ms(s, SPR_RT_MS[v & 127u] * 10u); break;   /* the decay: 300ms .. 3.0s */
    case K_RVDAMP:
        if (!v) { scat(s, "OPEN"); break; }
        { uint32_t hz = SPR_DAMP_HZ[v & 127u]; fmt_u(s, hz / 1000u); scat(s, "."); fmt_u(t, (hz / 100u) % 10u); scat(s, t); scat(s, "k"); }
        break;
    case K_RVPRE: fmt_ms(s, (uint32_t)v * 12u * 10000u / 44100u); break;   /* (the spring's read: 1 + 12 v samples) */
    case K_WIDTH: if (!v) scat(s, "MONO"); else if (v >= 127u) scat(s, "FULL"); else { fmt_u(s, (v * 100u + 63u) / 127u); scat(s, "%"); } break;
    default: fmt_u(s, v);
    }
}

static uint32_t cut_shown_t;                    /* the header shows the cutoff for a second after it moved */
static char ro_msg[24];                         /* Batch 9B: a transient readout in the header's tag line, a second: what a control
                                                 * without a knob on the screen just changed (SELECT's LFO RATE, the MONO / POLY keys) */
static uint32_t ro_t;
static void readout(const char *label, uint32_t p)
{
    char v[12];
    ro_msg[0] = 0;
    scat(ro_msg, label); scat(ro_msg, " ");
    param_value(v, p, live.v[p]);
    scat(ro_msg, v);
    ro_t = fm1_ms + 1u;
}
static uint32_t slop, slop_shown_t;             /* ALGORITHM's ride (obv_engine.h ctl_slop), 0..127; shown a second */
/* the header: on the scene (HOME, Batch 20) the bars, a toast on top while it shows; elsewhere the panel's header */
static void hdr(uint32_t pn, const uint8_t *name, uint32_t ed, const char *tags)
{
    if (sc_k != 0xFFu) sc_bars(pn, name, ed, toast && fm1_ms - toast_t < 1500u ? toast : tags);
    else ui_header(pn, name, ed, tags);
}
static void draw_header(void)
{
    char tags[40];
    tags[0] = 0;
    if (save_armed) {                           /* SAVE armed: the slot it saves into and what is there now */
        patch_t t;
        prog_get(save_to, &t);
        scat(tags, "SAVE HERE? " NM_PRESETS);
        hdr(save_to, t.v + PATCH_NAME_AT, 0, tags);
        return;
    }
    if (killed) {                               /* STOP: says so until it is let go (the art is Stage 3) */
        hdr(prog, live.v + PATCH_NAME_AT, edited, "STOPPED (PLAY)");
        return;
    }
    if (slop_shown_t && fm1_ms + 1u - slop_shown_t < 1000u) {   /* SLOP +40 = VINTAGE 95: the ride and what sounds */
        uint32_t sum = live.v[P_VINTAGE] + (uint32_t)SLOP_RIDE(slop);
        scat(tags, "SLOP +"); fmt_u(tags + slen(tags), (uint32_t)SLOP_RIDE(slop));
        scat(tags, " = VINTAGE "); fmt_u(tags + slen(tags), sum > (uint32_t)SLOP_MAX ? (uint32_t)SLOP_MAX : sum);
        hdr(prog, live.v + PATCH_NAME_AT, edited, tags);
        return;
    }
    if (ro_t && fm1_ms + 1u - ro_t < 1000u) {   /* LFO RATE 4.2Hz, MODE MONO */
        hdr(prog, live.v + PATCH_NAME_AT, edited, ro_msg);
        return;
    }
    if (cut_shown_t && fm1_ms + 1u - cut_shown_t < 1000u) {
        char v[12];
        param_value(v, P_CUTOFF, live.v[P_CUTOFF]);
        scat(tags, "CUTOFF ");
        scat(tags, v);
        hdr(prog, live.v + PATCH_NAME_AT, edited, tags);
        return;
    }
    {   /* short words; mode, filter, HOLD always (at most 14 characters: MONO NOTCH HOLD); then, as far as it fits, ARP, FX */
        static const char *const MODE_S[4] = {"POLY", "DUAL", "UNI", "MONO"};
        static const char *const FT_S[NFTYPE] = {"LP12", "HP12", "BP12", "NOTCH", "LP24", "SEM"};
        const uint8_t *pv = live.v;
        uint32_t arp = pv[P_ARP_MODE] != 0, fx = live.v[P_GROWL] || live.v[P_DLY_MIX] || live.v[P_REV_MIX] || live.v[P_CHEW];
        uint32_t n = slen(MODE_S[pv[P_MODE] & 3u]) + 1u + slen(FT_S[pv[P_FTYPE] % NFTYPE]) + (hold ? 5u : 0u);
        if (arp && n + 4u <= 23u) n += 4u; else arp = 0;
        if (fx && n + 3u <= 23u) n += 3u; else fx = 0;
        scat(tags, MODE_S[pv[P_MODE] & 3u]);
        scat(tags, " ");
        scat(tags, FT_S[pv[P_FTYPE] % NFTYPE]);
        if (arp) scat(tags, " ARP");
        if (fx) scat(tags, " FX");
        if (hold) scat(tags, " HOLD");
    }
    hdr(prog, live.v + PATCH_NAME_AT, edited, tags);
}

/* ALLEY's knobs. The time is ALLEY (a step of BBD_T) + FINE (1/128 of a step): turning ALLEY clears FINE (the knob
 * walks clean steps); leaving SYNC (ALLEY 0) by ALLEY or FINE starts from the time that was sounding, so the echo never
 * jumps; turning SYNC (the note value, BBD +) goes back to SYNC. (REC's tap tempo went in Batch 9B: REC is HOLD now.
 * A CC sets its byte as it is: CC 87 at 0 is SYNC) */
static uint32_t sync_samples(void)              /* the time SYNC gives now (as fx_block works it out) */
{
    uint32_t q = ctl_ext_quarter ? ctl_ext_quarter : 60u * FS / clampi(ctl_tempo, 40, 240), d = live.v[P_DLY_TIME] % NDDIV;
    return clampi((int32_t)(q * DDIV_NUM[d] / DDIV_DEN[d]), 64, DLY_MAX - 4u);
}
static void alley_from_sync(void)               /* SYNC -> the free step + FINE nearest the time sounding now */
{
    uint32_t f, a;
    if (live.v[P_ALLEY]) return;
    a = alley_index(sync_samples(), &f);
    live.v[P_ALLEY] = (uint8_t)a; live.v[P_ALLEY_FINE] = (uint8_t)f;
}
static void alley_turn(uint32_t p, int32_t e)   /* a knob on ALLEY, FINE or SYNC turned by e detents */
{
    if (p == P_DLY_TIME) { set_param(P_DLY_TIME, (int32_t)live.v[P_DLY_TIME] + (e > 0 ? 1 : -1)); live.v[P_ALLEY] = 0; live.v[P_ALLEY_FINE] = 0; return; }
    if (!live.v[P_ALLEY]) { alley_from_sync(); edited = 1; }
    if (p == P_ALLEY) { set_param(P_ALLEY, clampi((int32_t)live.v[P_ALLEY] + e, 1, 127)); live.v[P_ALLEY_FINE] = 0; }
    else set_param(P_ALLEY_FINE, (int32_t)live.v[P_ALLEY_FINE] + e * 2);
}
/* FX held: its knobs are the Psych Chain's four macros, in the chain's order (DOG-5-presets.md section 2: GROWL ALLEY
 * DRAIN CHEW; the only layer left: SEQ/EDIT/GLO/SAVE's hold-layers were sequencer content and went with it; EDIT, GLO
 * and SAVE are plain tap buttons now, see app_main) */
static const int8_t FX_LAYER[4] = {P_GROWL, P_ALLEY, P_DRAIN, P_CHEW};
static void layer_knob(knob_view_t *k, uint32_t i)
{
    uint32_t p2 = (uint32_t)FX_LAYER[i];
    k->present = 1; k->label = PDEF[p2].name; k->v = live.v[p2]; k->max = PDEF[p2].max;
    param_value(k->value, p2, live.v[p2]);
}

static uint32_t sel_held(void) { return fm1_in.buttons >> BTN_SEL & 1u; }
static const page_t *page_now(void)             /* the page's knobs, or its secondaries while SELECT is held */
{
    if (sel_held() && page == PG_DRIVE) return &PAGE_DRIVE_SEL;
    if (sel_held() && page == PG_TAPE) return &PAGE_TAPE_SEL;
    if (sel_held() && page == PG_BBD) return &PAGE_BBD_SEL;
    if (sel_held() && page == PG_SPRING) return &PAGE_SPRING_SEL;
    return &PAGE[page];
}

static void draw_page(void)
{
    knob_view_t k[4];
    uint32_t i;
    const page_t *pg = page_now();
    for (i = 0; i < 4u; i++) {
        int32_t p = pg->p[i];
        k[i].present = 0;
        k[i].bip = 0;
        k[i].value[0] = 0;
        if (page == PG_GLOBAL && !layer) {
            static const char *const GL[4] = {"TEMPO", "FLEAS", "MIDI CH", "TUNE"};
            k[i].label = GL[i];
            k[i].present = 1;
            if (i == 0) { fmt_u(k[i].value, set.tempo); k[i].v = set.tempo - 40; k[i].max = 200; }
            else if (i == 1) {                  /* FLEAS (Batch 23): the stage and the dial, "ITCH 40" */
                scat(k[i].value, set.fleas <= 15u ? "CLEAN " : set.fleas <= 65u ? "ITCH " : set.fleas <= 90u ? "SCRATCH " : "MANGE ");
                fmt_u(k[i].value + slen(k[i].value), set.fleas); k[i].v = set.fleas; k[i].max = 100;
            }
            else if (i == 2) { if (set.midi_ch) fmt_u(k[i].value, set.midi_ch); else scat(k[i].value, "OMNI"); k[i].v = set.midi_ch; k[i].max = 16; }
            else { scat(k[i].value, set.tune < 0 ? "-" : "+"); fmt_u(k[i].value + 1, (uint32_t)(set.tune < 0 ? -set.tune : set.tune)); scat(k[i].value, "c"); k[i].v = set.tune + 50; k[i].max = 100; k[i].bip = 1; }
        } else if (layer == L_FX) {
            layer_knob(&k[i], i);
        } else if (p >= 0) {
            k[i].label = PDEF[p].name;
            k[i].v = live.v[p];
            k[i].max = PDEF[p].max;
            k[i].bip = PDEF[p].kind == K_BIP || PDEF[p].kind == K_SEMI || PDEF[p].kind == K_MORPH;
            k[i].present = 1;
            param_value(k[i].value, (uint32_t)p, (uint32_t)live.v[p]);
        }
    }
    {
        const char *t = pg->title;
        if (layer == L_FX) t = "PSYCH CHAIN";
        {
            static char cpu[16];                /* the GLOBAL page: the render time of an audio half (budget 5800 us) */
            cpu[0] = 0; scat(cpu, "CPU "); fmt_u(cpu + slen(cpu), ui_render_us); scat(cpu, "us");
            ui_page(t, k, save_armed ? "SAVE?" : page == PG_GLOBAL && !layer ? cpu : 0);
        }
    }
}

/* the hint line under the scope: a toast after an action, else FX held's knob hint (the only layer left) */
static uint32_t hints_key = 0xFFFFFFFFu;
static void draw_hints(void)
{
    uint32_t key;
    int toasting = toast && fm1_ms - toast_t < 1500u;
    key = toasting ? 100u + ((toast_t / 7u) & 0xFFu) : 400u + layer;
    if (key == hints_key) return;
    hints_key = key;
    if (toasting) ui_hints(toast, "", C_ACCENT);
    else if (layer == L_FX) ui_hints("KNOBS: GROWL ALLEY", "DRAIN CHEW (THE CHAIN)", C_ACCENT);
}

#ifdef OBV_HOST
static uint32_t host_page_now(void) { return page; }   /* (tests/host.c: "T expect page N") */
static uint32_t host_slot_now(void) { return prog + 1u; }   /* ("T expect slot N": the program sounding, 1-99) */
static void host_set_param(uint32_t p, int32_t v) { set_param(p, v); }   /* (tests/host.c: "T param P V") */
static uint32_t host_voices_on(void) { uint32_t v, n = 0; for (v = 0; v < NV; v++) n += vc[v].gate; return n; }   /* ("T expect voices N") */
static uint32_t host_get_param(uint32_t p) { return live.v[p % PATCH_BYTES]; }   /* ("T expect param P V") */
static uint32_t host_map_idle_calls(void);
static void host_vlog_set(uint32_t on)          /* ("T vlog 1" .. "T vlog 0": each gated card's vintage pitch, in cents) */
{
    uint32_t c;
    if (on) { for (c = 0; c < NV; c++) { host_vl_sum[c] = host_vl_sq[c] = 0; host_vl_n[c] = 0; } host_vlog = 1; return; }
    host_vlog = 0;
    for (c = 0; c < NV; c++) if (host_vl_n[c]) {   /* Q8 semitones -> cents: x 100 / 256 */
        double m = (double)host_vl_sum[c] / host_vl_n[c], var = (double)host_vl_sq[c] / host_vl_n[c] - m * m, sd = var > 0 ? var : 0;
        int it;
        for (it = 0; it < 60 && sd > 0; it++) sd = 0.5 * (sd + var / sd);   /* (sqrt, no libm) */
        printf("vlog card %u: mean %+.1f cents  sd %.1f  range %+.1f .. %+.1f  (%u blocks)\n", c, m * 100 / 256, sd * 100 / 256,
               host_vl_min[c] * 100.0 / 256, host_vl_max[c] * 100.0 / 256, host_vl_n[c]);
    }
}
static uint32_t host_tricks_rest(void) { return deck_rest() && kill_g == KILL_ONE && !kill_dead && !ctl_slop && !slop_sm; }   /* ("T expect rest 1") */
#endif
static uint8_t fam_last[NFAM];                  /* each family's last page (set to FAM[].first at start) */
static uint32_t in_fam(uint32_t f) { return page >= FAM[f].first && page < (uint32_t)FAM[f].first + FAM[f].count; }
static uint32_t cycle_fam(uint32_t f)           /* a button steps through its pages (FAM in obv_params.h) */
{
    uint32_t first = FAM[f].first, count = FAM[f].count;
    if (in_fam(f)) return first + (page - first + 1u) % count;   /* in the family: the next page */
    return fam_last[f];                         /* from elsewhere: back where it was left (HOME, play, EDIT = the same page) */
}
static void fam_note(uint32_t pg)               /* a page is entered: its family remembers it */
{
    uint32_t f;
    for (f = 0; f < NFAM; f++)
        if (pg >= FAM[f].first && pg < (uint32_t)FAM[f].first + FAM[f].count) fam_last[f] = (uint8_t)pg;
}

/* HOLD HOME: the control map of the page you are on (ui_map in obv_ui.h). The page buttons show where a press goes
 * NOW (the next page in their family if you are in it, else the page the family was left on), so the map stays true
 * as the pages and the families' memories change */
static uint32_t map_on, map_dirty, home_down, home_t;
#define MAP_HOLD_MS 350u                        /* HOME held this long: the map (a tap, shorter, goes HOME on its release) */
#ifdef OBV_HOST
static uint32_t host_idle_n, host_map_idle;     /* tests: app_idle calls that got through, and during the last map draw */
#endif
static void draw_map(void)
{
    /* each button as "DOG NAME (PRINTED NAME)" (CLAUDE.md section 5); FX has no dog name in the brief */
    static const struct { uint8_t fam; const char *label; } PB[6] = {
        {FAM_EDIT, "DIG (EDIT)"}, {FAM_ENV, "HOWL (ENV)"}, {FAM_LFO, "PANT (LFO)"},
        {FAM_FX, "FX"}, {FAM_GLO, "FLEAS (GLO)"}, {FAM_ARP, "ZOOMIES (ARP)"}};
    /* the three lines of the EDIT-held shortcuts, in the unit's key groups (3 2 3 2 1): OP1 OP2 OP3 | OP4 OP5 + MONO POLY |
     * OP6 PIT GLO. (OP4 again = FILTER +, GLO again = OUTPUT: the manual's) */
    static const char *const EK_LINES[3] = {"OP1 OSC1  OP2 OSC2  OP3 MIXER", "OP4 FILTER OP5 VOICE MONO POLY",
                                            "OP6 VOICE+ PIT MOD GLO GLOBAL"};
    map_row_t R[MAP_ROWS];
    knob_view_t k[4];
    int32_t i, hi = -1;
    uint32_t none = 1, n;
#ifdef OBV_HOST
    uint32_t idle0 = host_idle_n;
#endif
    for (i = 0; i < 4; i++) {
        int32_t p = page_now()->p[i];
        k[i].present = 0;
        if (page == PG_GLOBAL) {                /* (the globals are drawn by hand: tempo, -, MIDI channel, tune) */
            static const char *const GL[4] = {"TEMPO", "FLEAS", "MIDI CH", "TUNE"};
            k[i].label = GL[i]; k[i].present = 1;
        } else if (p >= 0) { k[i].label = PDEF[p].name; k[i].present = 1; }
        none &= !k[i].present;
    }
    for (i = 0; i < 6; i++) {                   /* the page buttons: where a press goes NOW (the live part) */
        R[i].label = PB[i].label;
        R[i].what = PB[i].fam == FAM_ARP && page == PG_ARP ? "HOLD" : PAGE[cycle_fam(PB[i].fam)].title;
        if (in_fam(PB[i].fam)) hi = i;
    }
    R[6].label = "HEEL (PLAY)"; R[6].what = killed ? "RESUME" : "STOP";   /* the live tricks (all pages) */
    R[7].label = "FLOP (SEQ)"; R[7].what = "HOLD=TAPE STOP";
    R[8].label = "SLOBBER (ALGO)"; R[8].what = "SLOP RIDE";
    R[9].label = "WAG (REC)"; R[9].what = "HOLD";
    n = 10;
    if (in_fam(FAM_EDIT)) {                     /* EDIT-family pages: the shortcuts take the rest of the screen */
        for (i = 0; i < 3; i++) { R[n].label = EK_LINES[i]; R[n].what = 0; n++; }
    } else {
        if (page == PG_PERFORM) { R[n].label = "FETCH (SELECT)"; R[n].what = "LFO RATE"; n++; }
        else if (page == PG_DRIVE || page == PG_TAPE || page == PG_BBD || page == PG_SPRING) {
            R[n].label = "FETCH (SELECT)";
            R[n].what = page == PG_DRIVE ? "HOLD: DRIVE +" : page == PG_TAPE ? "HOLD: TAPE +" : page == PG_BBD ? "HOLD: BBD +" : "HOLD: SPRING +";
            n++;
        }
        R[n].label = "BURY (SAVE)"; R[n].what = "TAP TWICE"; n++;
        R[n].label = "BARKS (" NM_PRESETS ")"; R[n].what = "SOUND"; n++;
        if (n < MAP_ROWS) { R[n].label = "OCT-/+"; R[n].what = "OCTAVE"; n++; }
    }
    ui_map(page_now()->title, k, none ? "NO KNOBS HERE YET" : 0, R, hi);
#ifdef OBV_HOST
    host_map_idle = host_idle_n - idle0;
#endif
}

#ifdef OBV_HOST
static uint32_t host_map_idle_calls(void) { return host_map_idle; }
#endif
static void draw_tags(void) { draw_header(); }
static void draw_scope(void) { ui_scope(scope, SCOPE_N); }
static void draw_leds(void) { ui_leds(ui_vlevel, NV); }

/* ---- the main loop */
#define KEY0 53u                               /* key 0 = F3 */
/* the keys and MIDI in: read by the main loop, and while the screen is drawn (app_idle, notes only), so the notes
 * of a chord or among a stream of CCs are not held up by a redraw (a knob page is ~30 ms on the SPI alone) */
static uint32_t dirty_hdr = 1, dirty_page = 1, dirty_tags = 1;
static uint32_t keys_prev, clk_n, clk_t0, clk_last, idle_ok;
static uint8_t held_key[27];


/* HOLD, one latch with two buttons (Batch 9B): the ARP button on its page and REC on any page both come here, so they
 * cannot disagree. It ORs with the sustain pedal in part_sus() (obv_engine.h); the PLAY / STOP kill switch releases it
 * (below, where PLAY is handled); nothing else does (a patch change, MIDI panic and the pedal leave it as it is) */
static void hold_toggle(void) { hold ^= 1u; ctl_hold = hold; dirty_tags = 1; }

/* EDIT held + a black key of the upper row = a jump (Batch 9B). Note-key indices, 0 = F3: the keybed starts on F, so its
 * 11 black keys are F#3 G#3 A#3 | C#4 D#4 | F#4 G#4 A#4 | C#5 D#5 | F#5, in groups of 3 2 3 2 1, which are the unit's
 * printing OP1 OP2 OP3 | OP4 OP5 | OP6 PIT GLO | MONO POLY | (none). By index, not by note number: the octave buttons
 * don't move it. The last key (25) is no shortcut: it plays as always. A shortcut never sounds, and never leaves a stuck
 * note: a key already down when EDIT was pressed keeps its note and ends it as always */
enum { EK_OP1 = 1, EK_OP2 = 3, EK_OP3 = 5, EK_OP4 = 8, EK_OP5 = 10, EK_OP6 = 13, EK_PIT = 15, EK_GLO = 17, EK_MONO = 20,
       EK_POLY = 22, EK_NONE = 25 };
#define EK_BIT(k) (1u << (k))
#define EDIT_KEYS (EK_BIT(EK_OP1) | EK_BIT(EK_OP2) | EK_BIT(EK_OP3) | EK_BIT(EK_OP4) | EK_BIT(EK_OP5) | EK_BIT(EK_OP6) | \
                   EK_BIT(EK_PIT) | EK_BIT(EK_GLO) | EK_BIT(EK_MONO) | EK_BIT(EK_POLY))
#define IS_BLACK(k) ((0x54Au >> ((KEY0 + (k)) % 12u)) & 1u)   /* pitch classes C# D# F# G# A# */
_Static_assert(IS_BLACK(EK_OP1) && IS_BLACK(EK_OP2) && IS_BLACK(EK_OP3) && IS_BLACK(EK_OP4) && IS_BLACK(EK_OP5) &&
               IS_BLACK(EK_OP6) && IS_BLACK(EK_PIT) && IS_BLACK(EK_GLO) && IS_BLACK(EK_MONO) && IS_BLACK(EK_POLY) &&
               IS_BLACK(EK_NONE), "the EDIT shortcuts sit on black keys");
_Static_assert(IS_BLACK(0) + IS_BLACK(1) + IS_BLACK(2) + IS_BLACK(3) + IS_BLACK(4) + IS_BLACK(5) + IS_BLACK(6) + IS_BLACK(7) +
               IS_BLACK(8) + IS_BLACK(9) + IS_BLACK(10) + IS_BLACK(11) + IS_BLACK(12) + IS_BLACK(13) + IS_BLACK(14) +
               IS_BLACK(15) + IS_BLACK(16) + IS_BLACK(17) + IS_BLACK(18) + IS_BLACK(19) + IS_BLACK(20) + IS_BLACK(21) +
               IS_BLACK(22) + IS_BLACK(23) + IS_BLACK(24) + IS_BLACK(25) + IS_BLACK(26) == 11, "27 keys from F: 11 black");
static const struct { uint8_t key, page, page2; int8_t mode; } EDIT_KEY[] = {   /* page2: the key again (a toggle), = page: it stays */
    {EK_OP1, PG_OSC1, PG_OSC1, -1}, {EK_OP2, PG_OSC2, PG_OSC2, -1}, {EK_OP3, PG_MIXER, PG_MIXER, -1},
    {EK_OP4, PG_FILTER, PG_FILTER2, -1}, {EK_OP5, PG_VOICE, PG_VOICE, -1}, {EK_OP6, PG_VOICE2, PG_VOICE2, -1},
    {EK_PIT, PG_OSCMOD, PG_OSCMOD, -1}, {EK_GLO, PG_GLOBAL, PG_OUTPUT, -1},
    {EK_MONO, 0, 0, M_MONO}, {EK_POLY, 0, 0, M_POLY},
};
static uint32_t edit_swallow;                   /* bit k: key k went down with EDIT held: it did its job, its release sounds nothing */
static uint32_t edit_used;                      /* a shortcut was used during this EDIT hold: letting go does not cycle the family */
static uint8_t edit_q[8];                       /* the shortcuts pressed, for the main loop (keys_in also runs inside a draw) */
static uint32_t edit_qr, edit_qw;

static void keys_in(void)
{
    uint32_t keys = fm1_in.notes, down = keys & ~keys_prev, up = keys_prev & ~keys, base = (uint32_t)(KEY0 + 12 * set.oct), k;
    uint32_t edit = fm1_in.buttons >> BTN_EDIT & 1u;
    for (k = 0; k < 27u; k++) {
        if (down >> k & 1u) {
            keys_prev |= 1u << k;
            if (edit && (EDIT_KEYS >> k & 1u)) {    /* EDIT held: a jump, not a note (no sound, no MIDI out) */
                edit_swallow |= 1u << k;
                edit_used = 1;
                if (edit_qw - edit_qr < 8u) edit_q[edit_qw++ & 7u] = (uint8_t)k;
                continue;
            }
            held_key[k] = (uint8_t)(base + k);
            play_note(1, held_key[k], KEY_VEL(k)); midi_send(0x90u | MIDI_OUT_CH, held_key[k], KEY_VEL(k));
        }
        if (up >> k & 1u) {
            keys_prev &= ~(1u << k);
            if (edit_swallow >> k & 1u) { edit_swallow &= ~(1u << k); continue; }   /* (it never sounded) */
            play_note(0, held_key[k], 0); midi_send(0x80u | MIDI_OUT_CH, held_key[k], 0);
        }
    }
}

/* the main loop: what a shortcut does. cur = the page the panel is on (after this pass's buttons); returns the page to go to.
 * MONO / POLY set the patch's MODE as the VOICE page's knob does, with the readout in the header */
static uint32_t edit_key_do(uint32_t k, uint32_t cur)
{
    uint32_t i;
    for (i = 0; i < sizeof EDIT_KEY / sizeof EDIT_KEY[0]; i++) {
        if (EDIT_KEY[i].key != k) continue;
        if (EDIT_KEY[i].mode >= 0) {
            set_param(P_MODE, EDIT_KEY[i].mode);
            readout("MODE", P_MODE);
            dirty_hdr = dirty_tags = dirty_page = 1;
            return cur;
        }
        return cur == EDIT_KEY[i].page ? EDIT_KEY[i].page2 : EDIT_KEY[i].page;
    }
    return cur;
}

static uint8_t midi_back[4];                    /* a message left for the main loop (app_idle met a program change) */
static void midi_in(uint32_t notes_only)
{
    uint8_t st, d1, d2;
    for (;;) {
        uint32_t ch, kind;
        if (midi_back[3]) { st = midi_back[0]; d1 = midi_back[1]; d2 = midi_back[2]; midi_back[3] = 0; }
        else if (!midi_get(&st, &d1, &d2)) break;
        if (notes_only && (st & 0xF0u) == 0xC0u) {   /* a program change loads a sound: not in the middle of a draw */
            midi_back[0] = st; midi_back[1] = d1; midi_back[2] = d2; midi_back[3] = 1;
            break;
        }
        ch = (st & 15u) + 1u; kind = st & 0xF0u;
        if (st == 0xF8u) {                  /* clock: 24 per quarter; the tempo follows, 2 s without it and it is gone */
            if (!clk_n) clk_t0 = fm1_ms;
            clk_last = fm1_ms;
            if (++clk_n == 25u) {
                uint32_t ms = fm1_ms - clk_t0;
                if (ms > 200u && ms < 1600u) ctl_ext_quarter = ms * 441u / 10u;
                clk_n = 0;
            }
            continue;
        }
        if (st == 0xFAu || st == 0xFBu) {   /* start / continue: the arp from the top */
            ctl_arp_restart = 1; clk_n = 0;
            continue;
        }
        if (st >= 0xF0u) continue;
        if (set.midi_ch && ch != set.midi_ch) continue;
        if (kind == 0x90u && d2) play_note(1, d1, d2);
        else if (kind == 0x80u || kind == 0x90u) play_note(0, d1, 0);
        else if (kind == 0xE0u) ctl_bend = (int32_t)(d1 | d2 << 7) - 8192;
        else if (kind == 0xC0u && d1 < NPROG) { load_program(d1); dirty_hdr = dirty_page = dirty_tags = 1; set.prog = (uint8_t)prog; }
        else if (kind == 0xB0u) {
            if (d1 == 7u) ctl_cc7 = d2;
            else if (d1 == 64u) ctl_sustain = d2 >= 64u;
            else if (d1 == 120u || d1 == 123u) {   /* a panic: and a latched HOLD goes, as on STOP */
                if (hold) { hold = 0; ctl_hold = 0; dirty_tags = 1; }
                ctl_panic = 1;
            }
            else if (cc_map[d1]) {
                uint32_t p = cc_map[d1] - 1u;
                set_param(p, PDEF[p].max == 127 ? (int32_t)d2 : ((int32_t)d2 * PDEF[p].max + 63) / 127);
                if (p == P_CUTOFF) cut_shown_t = fm1_ms + 1u;
                dirty_page = dirty_hdr = 1;
                if (p == P_MODE || p == P_FTYPE || p == P_ARP_MODE) dirty_tags = 1;
            }
        }
    }
}

static void app_idle(void)                      /* lcd.c while a strip goes out, ui_page between the knobs: the notes */
{
    static uint32_t busy;
    if (!idle_ok || busy) return;
#ifdef OBV_HOST
    host_idle_n++;                              /* (tests: "T expect idle N" -- a draw that waits must call this) */
#endif
    busy = 1;
    keys_in();
    midi_in(1);
    busy = 0;
}

#ifdef OBV_HOST
/* a host self-test of the 96-byte / 3-sector / DOG5 program store, exercising the REAL app code (prog_put,
 * prog_get, psect_save, psect_load, the boot reload) over tests/host.c's flash model. Run: `obervave selftest`.
 * (The device's own sector_load/save -- magic + length + CRC32 at real flash addresses -- run only on the
 * toolchain/device; here the host model's length guard stands in for the format/version check.) */
static int sf_fail;
static void sf_check(const char *what, int ok) { printf("selftest: %-64s %s\n", what, ok ? "ok" : "FAIL"); sf_fail += !ok; }
static void sf_seed(patch_t *p, uint32_t seed)   /* a distinct, fully-filled 96-byte patch (all bytes vary by seed) */
{
    uint32_t i, s = seed * 2654435761u + 1u;
    for (i = 0; i < PATCH_BYTES; i++) { s = s * 1103515245u + 12345u; p->v[i] = (uint8_t)(s >> 24); }
}
static patch_t sf_expect[NPROG];
static uint8_t sf_snap_ps[NPSECT][sizeof host_psect[0]], sf_snap_set[sizeof host_store], sf_snap_bl[NBLOB][sizeof host_blob[0]];
static void store_selftest(void)
{
    uint32_t n, s;
    patch_t got;
    printf("selftest: PATCH_BYTES=%u NPARAM=%u name@%u  PS_N=%u NPSECT=%u sizeof(psect_t)=%zu PS_TAG=%08X\n",
           PATCH_BYTES, NPARAM, PATCH_NAME_AT, PS_N, NPSECT, sizeof(psect_t), PS_TAG);

    /* fresh flash + fresh RAM caches */
    memset(host_psect, 0, sizeof host_psect);
    for (n = 0; n < NPSECT; n++) { memset(&psect[n], 0, sizeof psect[n]); psect[n].tag = PS_TAG; }
    ps_dirty = 0;

    /* ---- c: with no user saves, programs 1-32 are the DØG-5 factory, 33-99 all read INIT ---- */
    {
        int c_ok = 1;
        for (n = 32; n < NPROG; n++) {           /* 0-idx 32-98 == programs 33-99 */
            prog_get(n, &got);
            if (memcmp(got.v + PATCH_NAME_AT, "INIT", 4) != 0 || got.v[PATCH_NAME_AT + 4] != ' ') c_ok = 0;
        }
        sf_check("with no user saves, programs 33-99 all read INIT", c_ok);
    }

    /* ---- a1: 99 distinct patches into all 99 slots, power-cycle, reload, compare every byte ---- */
    for (n = 0; n < NPROG; n++) { sf_seed(&sf_expect[n], n + 1u); live = sf_expect[n]; prog_put(n, &live); }
    for (s = 0; s < NPSECT; s++) if (ps_dirty >> s & 1u) psect_save(s, &psect[s], sizeof psect[s]);
    ps_dirty = 0;
    sf_check("all 3 program sectors were written (99 slots span 3 sectors)",
             host_slen(host_psect[0]) == sizeof(psect_t) && host_slen(host_psect[1]) == sizeof(psect_t) &&
             host_slen(host_psect[2]) == sizeof(psect_t));
    memset(psect, 0, sizeof psect);                  /* power cycle: the RAM caches are lost, the flash survives */
    for (n = 0; n < NPSECT; n++)
        if (psect_load(n, &psect[n], sizeof psect[n]) || psect[n].tag != PS_TAG) { memset(&psect[n], 0, sizeof psect[n]); psect[n].tag = PS_TAG; }
    {
        int all = 1, s3 = 1;
        for (n = 0; n < NPROG; n++) {           /* (the store itself: all 99, the POUND's too, below the lock) */
            got = psect[n / PS_N].p[n % PS_N];
            if (!psect[n / PS_N].used[n % PS_N] || memcmp(&got, &sf_expect[n], PATCH_BYTES)) { all = 0; printf("  slot %u differs\n", n + 1u); }
        }
        for (n = 84; n < NPROG; n++) if (n / PS_N != 2u) s3 = 0;   /* programs 85-99 (0-idx 84-98) */
        sf_check("all 99 patches survive the power-cycle byte-exact (every byte of every patch)", all);
        sf_check("programs 85-99 live in the 3rd sector (index 2)", s3);
    }

    /* ---- d: the lock: with all 99 stored, 1-32 still read the factory, 33-99 the user's ---- */
    {
        int pound = 1, pack = 1;
        patch_t f;
        for (n = 0; n < NFACT; n++) { prog_get(n, &got); patch_from_factory(&f, &FACTORY[n]); f.v[PATCH_CHAPTER_AT] = (uint8_t)(n / 8u + 1u); if (memcmp(&got, &f, PATCH_BYTES)) pound = 0; }
        for (n = NFACT; n < NPROG; n++) { prog_get(n, &got); if (memcmp(&got, &sf_expect[n], PATCH_BYTES)) pack = 0; }
        sf_check("THE POUND: with saves stored over 1-32, programs 1-32 still read the factory", pound);
        sf_check("THE PACK: programs 33-99 read the user's saves", pack);
    }

    /* ---- a2: saving one slot touches only its sector; the other two + all other flash unchanged ---- */
    memcpy(sf_snap_ps, host_psect, sizeof host_psect);
    memcpy(sf_snap_set, host_store, sizeof host_store);
    memcpy(sf_snap_bl, host_blob, sizeof host_blob);
    sf_seed(&live, 7777u); prog_put(50u, &live);     /* program 51 (0-idx 50) -> sector 50/42 = 1 */
    for (s = 0; s < NPSECT; s++) if (ps_dirty >> s & 1u) psect_save(s, &psect[s], sizeof psect[s]);
    ps_dirty = 0;
    sf_check("saving program 51 rewrote only its sector (1); sectors 0 and 2 unchanged",
             memcmp(host_psect[1], sf_snap_ps[1], sizeof host_psect[1]) != 0 &&
             memcmp(host_psect[0], sf_snap_ps[0], sizeof host_psect[0]) == 0 &&
             memcmp(host_psect[2], sf_snap_ps[2], sizeof host_psect[2]) == 0);
    sf_check("that save left the settings sector and all 8 pattern sectors untouched",
             memcmp(host_store, sf_snap_set, sizeof host_store) == 0 && memcmp(host_blob, sf_snap_bl, sizeof host_blob) == 0);

    /* ---- b: an old 80-byte-format sector (tag "BOVP", 4056 bytes) reads as empty, is never misread ---- */
    {
        static uint8_t old[4056];                    /* the old psect_t size: 4 tag + 50 used + 2 pad + 50*80 */
        uint32_t oldtag = 0x50564F42u;               /* psect_t.tag == "BOVP" at offset 0 */
        int rej, empty = 1;
        memset(old, 0xAB, sizeof old);
        memcpy(old, &oldtag, 4);
        host_sput(host_psect[0], old, sizeof old);   /* sector 0 now holds the old format (stored length 4056) */
        memset(host_psect[1], 0, 4); memset(host_psect[2], 0, 4);   /* sectors 1,2 empty */
        rej = (psect_load(0, &psect[0], sizeof psect[0]) != 0);     /* must reject: stored 4056 != requested 4080 */
        for (n = 0; n < NPSECT; n++)
            if (psect_load(n, &psect[n], sizeof psect[n]) || psect[n].tag != PS_TAG) { memset(&psect[n], 0, sizeof psect[n]); psect[n].tag = PS_TAG; }
        for (n = 0; n < NPROG; n++) if (psect[n / PS_N].used[n % PS_N]) empty = 0;
        sf_check("the old 80-byte \"BOVP\" sector (4056 B) is rejected by the length guard", rej);
        sf_check("after rejection every slot reads empty (factory/INIT); the DOG5 tag is set, no BOVP/junk leaked",
                 empty && psect[0].tag == PS_TAG);
    }

    /* ---- e: the rescue at power-on: old saves over 1-32 (v0.1 / v0.2) move to the first free PACK slots, in order ---- */
    {
        patch_t a, b2;
        int moved, kept;
        for (n = 0; n < NPSECT; n++) { memset(&psect[n], 0, sizeof psect[n]); psect[n].tag = PS_TAG; }
        sf_seed(&a, 501u); prog_put(4u, &a);       /* program 5: an old save */
        sf_seed(&b2, 502u); prog_put(20u, &b2);    /* program 21: another */
        sf_seed(&live, 503u); prog_put(32u, &live);   /* program 33: the user's, already in THE PACK */
        ps_dirty = 0;
        pound_rescue();
        moved = !memcmp(&psect[33 / PS_N].p[33 % PS_N], &a, PATCH_BYTES) && !memcmp(&psect[34 / PS_N].p[34 % PS_N], &b2, PATCH_BYTES);
        kept = !memcmp(&psect[0].p[32], &live, PATCH_BYTES);
        sf_check("rescue: old saves on 5 and 21 moved to 34 and 35 (33 was taken), 33 untouched", moved && kept);
        sf_check("rescue: 5 and 21 are free again (read the factory) and sector 0 is due to be saved",
                 !psect[0].used[4] && !psect[0].used[20] && (ps_dirty & 1u));
        ps_dirty = 0;
        pound_rescue();
        sf_check("rescue: a second power-on moves nothing", ps_dirty == 0);
        for (n = 0; n < NPSECT; n++) { memset(&psect[n], 0, sizeof psect[n]); psect[n].tag = PS_TAG; }
        for (n = 0; n < NPROG; n++) { sf_seed(&live, n + 900u); prog_put(n, &live); }   /* THE PACK full */
        ps_dirty = 0;
        pound_rescue();
        sf_check("rescue: with THE PACK full nothing is overwritten (the old save stays, unread)", ps_dirty == 0 && psect[0].used[0]);
    }

    printf("selftest: %s\n", sf_fail ? "FAILED" : "all ok");
    exit(sf_fail ? 1 : 0);
}
#endif

/* HOME's scene, once a pass of the main loop: the chapter, the bars, the dog's pose and sway, the beam */
static uint32_t sc_on_t, sc_off_t, sc_sound, sc_toast_key, t_sway, sway_i, t_beam;
static int32_t home_dial_p = -1;
static uint32_t home_dial_t, home_dial_dirty, t_dial;
static const int8_t SWAY[10] = {0, 0, 1, 1, 1, 0, 0, -1, -1, -1};   /* 200 ms a step: a ~2 s rock */
static void scene_tick(uint32_t *t_hdr)
{
    uint32_t k = patch_chapter(&live, prog), v, best = 0, bl = 0, pose, tk;
    static uint32_t t_fence, fd_drawn;
    if (sc_fleas != set.fleas) sc_fleas = set.fleas;   /* (FLEAS: the full repaint below draws it, the tick keeps it) */
    if (sc_k != k) {                            /* a new chapter (or coming HOME): the whole screen */
#ifdef OBV_HOST
        uint32_t idle0 = host_idle_n;
        sc_enter(k);
        host_map_idle = host_idle_n - idle0;    /* (tests: "expect idle N" reads the last full-screen draw) */
#else
        sc_enter(k);
#endif
        dirty_hdr = 1; *t_hdr = fm1_ms - 30u; sc_sound = 0; sway_i = 0; t_sway = sc_off_t = fm1_ms;
    }
    tk = toast && fm1_ms - toast_t < 1500u ? 1u + (toast_t & 0xFFFFu) : 0u;
    if (tk != sc_toast_key) { sc_toast_key = tk; dirty_hdr = 1; }
    if ((dirty_hdr || dirty_tags) && fm1_ms - *t_hdr >= 30u) { dirty_hdr = dirty_tags = 0; *t_hdr = fm1_ms; draw_header(); }
    dirty_page = 0;
    for (v = 0; v < NV; v++)                    /* the loudest voice: its period sets the scope's stride */
        if ((uint32_t)ui_vlevel[v] > bl) { bl = (uint32_t)ui_vlevel[v]; best = ui_vnote[v]; }
    if (killed) bl = 0;
    if ((bl > 600u) != sc_sound) {
        sc_sound = bl > 600u;
        if (sc_sound) { sc_on_t = fm1_ms; if (sc_fd < 160u) sc_fd = 160u; t_fence = fm1_ms - 1000u; }   /* the bark hits the fence */
        else sc_off_t = fm1_ms;
    }
    if (fm1_ms - t_fence >= 150u) {             /* THE FENCE (and MANGE's scramble): 6.7 Hz at most, the top bar only */
        t_fence = fm1_ms;
        if (sc_sound) sc_fd = sc_fd + 12u > 256u ? 256u : sc_fd + 12u;   /* chipped while the bark sounds */
        else sc_fd = sc_fd > 32u ? sc_fd - 32u : 0u;   /* healed within 1.2 s of the sound stopping (canon U1) */
        if (sc_fd || fd_drawn || sc_fleas > 90u) { sc_fd_seed++; sc_top(); fd_drawn = sc_fd; }
    }
    sc_fleas_tick(set.fleas, fm1_ms);
    if (home_dial_dirty && home_dial_p >= 0 && fm1_ms - t_dial >= 30u) {   /* a HOME knob turned: its dial (30 ms at most) */
        knob_view_t kv;
        int32_t p = home_dial_p;
        home_dial_dirty = 0; t_dial = fm1_ms;
        kv.label = PDEF[p].name; kv.v = live.v[p]; kv.max = PDEF[p].max; kv.present = 1;
        kv.bip = PDEF[p].kind == K_BIP || PDEF[p].kind == K_SEMI || PDEF[p].kind == K_MORPH;
        kv.value[0] = 0;
        param_value(kv.value, (uint32_t)p, (uint32_t)live.v[p]);
        sc_dial(&kv);
    } else if (sc_dial_on && fm1_ms - home_dial_t >= 1200u) sc_dial_off();   /* 1.2 s after the last turn: the art */
    if (sc_sound) {
        uint32_t held = fm1_ms - sc_on_t;
        pose = SC_POSE_BARK;                    /* MOONSHINE howls a held note: bark, draw breath, howl */
        if (SA_SCENE[sc_k].pose[SC_POSE_HOWL] && held >= 350u) pose = held < 900u ? SC_POSE_INHALE : SC_POSE_HOWL;
        if (pose != sc_pose || sc_dx) { sc_set_pose(pose, 0); sc_beam(scope, SCOPE_N); t_beam = fm1_ms; }
        if (scope_state == 3u && fm1_ms - t_beam >= 50u) {   /* a fresh capture: the beam carries it */
            uint32_t inc = pitch_inc((int32_t)best << 8), period = inc ? 0xFFFFFFFFu / inc : 1000u;
            t_beam = fm1_ms;
            sc_beam(scope, SCOPE_N);
            scope_stride = clampi((int32_t)(period * 2u / SCOPE_N), 1, 64);
            scope_state = 1;
        } else if (scope_state == 1u && fm1_ms - t_beam >= 150u) {   /* no crossing to trigger on (a tape stop's silence):
                                                                       * the beam goes flat, as a scope's does */
            static const int16_t FLAT[2] = {0, 0};
            t_beam = fm1_ms;
            sc_beam(FLAT, 2);
        }
    } else {
        if (bm_n) sc_beam(0, 0);
        if (sc_pose != SC_POSE_REST) { sc_set_pose(SC_POSE_REST, 0); sway_i = 0; t_sway = fm1_ms; }
        if (fm1_ms - sc_off_t >= 500u && fm1_ms - t_sway >= 200u) {   /* at rest: the sway */
            t_sway = fm1_ms;
            sway_i = sway_i + 1u >= sizeof SWAY ? 0u : sway_i + 1u;
            sc_set_pose(SC_POSE_REST, SWAY[sway_i]);
        }
        if (scope_state == 3u) scope_state = 1;
    }
}

static void app_main(void)
{
    uint32_t k, i, t_led = 0, t_scope = 0, t_page = 0, t_hdr = 0, leds_q = 1;
    uint32_t leds_prev = 0xFFFFFFFFu, glow = 0, glow_prev = 0xFFFFFFFFu;
#ifdef OBV_HOST
    if (host_selftest) store_selftest();             /* runs the store self-test and exit()s */
#endif
    rnd = 0xC0FFEE42u;
    engine_init();
    cc_map_init();
    {
        uint32_t n;
        for (n = 0; n < NPSECT; n++)
            if (psect_load(n, &psect[n], sizeof psect[n]) || psect[n].tag != PS_TAG) {
                memset(&psect[n], 0, sizeof psect[n]);
                psect[n].tag = PS_TAG;
            }
        set.version = 0;
        if (settings_load(&set, sizeof set) || set.version != SET_VERSION) {
            memset(&set, 0, sizeof set);
            set.version = SET_VERSION;
            set.tempo = 120;
        }
    }
    pound_rescue();
    if (set.prog >= NPROG) set.prog = 0;
    if (set.tempo < 40u || set.tempo > 240u) set.tempo = 120;
    if (set.oct < -2 || set.oct > 2) set.oct = 0;
    if (set.midi_ch > 16u) set.midi_ch = 0;
    if (set.fleas > 100u) set.fleas = 0;          /* (an old sequencer pattern number reads as CLEAN) */
    ctl_tempo = set.tempo;
    ctl_tune8 = set.tune * 256 / 100;
    load_program(set.prog);
    ctl_panic = 0;
    for (k = 0; k < NFAM; k++) fam_last[k] = FAM[k].first;

    dog5_splash(patch_chapter(&live, prog));            /* the boot animation, ending on this program's scene */
    scope_state = 1;

    for (;;) {
        uint32_t rel, b, lit = 0, base = (uint32_t)(KEY0 + 12 * set.oct), np = page;
        int32_t e;
        platform_poll();

        keys_in();

        /* buttons, as sloopDX: FX held is a layer (its knobs change job until it is let go), HOME while held
         * locks it open; EDIT, GLO and SAVE are plain taps now (their hold-layers were sequencer content: erase
         * notes, mute/solo/tap-tempo, pattern slots -- all gone with it, see the enum above) */
        b = fm1_input_edges(&rel);
        {
            static uint32_t dead;               /* a press that only unlocked FX: its release does nothing */
            if (b & (1u << BTN_FX)) {
                if (layer_lock) { layer = L_NONE; layer_lock = 0; dead = 1; }
                else { layer = L_FX; layer_used = 0; layer_t = fm1_ms; layer_btn = BTN_FX; }
                dirty_page = dirty_tags = 1; hints_key = 0xFFFFFFFFu; leds_q = 0xFFFFFFFFu;
            }
            if (rel & (1u << BTN_FX)) {
                if (dead) dead = 0;
                else if (layer == L_FX && !layer_lock) {
                    if (!layer_used && fm1_ms - layer_t < 600u) np = cycle_fam(FAM_FX);
                    layer = L_NONE;
                    dirty_page = dirty_tags = 1; hints_key = 0xFFFFFFFFu; leds_q = 0xFFFFFFFFu;
                }
            }
        }
        if (b & (3u << BTN_OCT_DOWN)) {
            if ((fm1_in.buttons & (3u << BTN_OCT_DOWN)) == (3u << BTN_OCT_DOWN)) {   /* both: octave 0 */
                set.oct = 0; set_dirty = 1; set_t = fm1_ms; say("OCTAVE 0");
            } else {
                if (b & (1u << BTN_OCT_DOWN) && set.oct > -2) { set.oct--; set_dirty = 1; set_t = fm1_ms; }
                if (b & (1u << BTN_OCT_UP) && set.oct < 2) { set.oct++; set_dirty = 1; set_t = fm1_ms; }
            }
            dirty_page = 1;
        }
        if (b & (1u << BTN_HOME)) {             /* HOME: PERFORM; while a layer is held: lock it open; locked: let it go */
            if (layer && !layer_lock) { layer_lock = 1; layer_used = 1; say("LOCKED: ITS BUTTON ENDS IT"); }
            else if (layer_lock) { layer = L_NONE; layer_lock = 0; dirty_page = dirty_tags = 1; leds_q = 0xFFFFFFFFu; }
            else { home_down = 1; home_t = fm1_ms; }   /* tap: HOME when it is let go; held: the control map */
        }
        if (home_down && (rel & (1u << BTN_HOME))) {
            home_down = 0;
            if (map_on) {                       /* the map is dismissed, the page stays */
                map_on = 0;
                lcd_fill(0, 0, 240, 240, C_PANEL);
                dirty_hdr = dirty_page = dirty_tags = 1; hints_key = leds_q = 0xFFFFFFFFu; scope_state = 1; t_scope = 0;
            } else np = PG_PERFORM;
        }
        if (home_down && !map_on && fm1_ms - home_t >= MAP_HOLD_MS) {
            map_on = 1; map_dirty = 1;
            lcd_fill(0, 0, 240, 240, C_PANEL);  /* (the map's strips do not tile the screen like the page's) */
        }
        if (b & ((1u << BTN_ENV) | (1u << BTN_LFO) | (1u << BTN_ARP)) && layer_lock) {   /* (another button lets a lock go) */
            layer = L_NONE; layer_lock = 0; b &= ~((1u << BTN_ENV) | (1u << BTN_LFO) | (1u << BTN_ARP));
            dirty_page = dirty_tags = 1; leds_q = 0xFFFFFFFFu;
        }
        if (rel & (1u << BTN_EDIT)) {           /* EDIT is a hold now (EDIT + a key = a jump, keys_in): the tap acts on release, */
            if (!edit_used) np = cycle_fam(FAM_EDIT);   /* unless a shortcut was used while it was down */
            edit_used = 0;
        }
        while (edit_qr != edit_qw) np = edit_key_do(edit_q[edit_qr++ & 7u], np);   /* (in the order pressed) */
        if (b & (1u << BTN_ENV)) np = cycle_fam(FAM_ENV);
        if (b & (1u << BTN_LFO)) np = cycle_fam(FAM_LFO);
        if (b & (1u << BTN_ARP)) {
            if (page == PG_ARP) hold_toggle();   /* on its page: HOLD (REC's latch, on any page) */
            else np = PG_ARP;
        }
        if (b & (1u << BTN_GLO)) np = cycle_fam(FAM_GLO);
        if (b & (1u << BTN_SAVE)) {              /* a tap: armed (the slot to save into); tapped again: saved */
            if (save_armed && save_to < NFACT) {   /* (never: the slot is kept in THE PACK) */
                save_armed = 0;
                dirty_hdr = dirty_page = 1;
            } else if (save_armed) {
                uint32_t n = save_to % NPROG;
                prog_put(n, &live);
                prog = n; set.prog = (uint8_t)n; edited = 0; set_dirty = 1;
                save_armed = 0;
                say("SAVED");
                dirty_hdr = dirty_tags = dirty_page = 1;
            } else {                            /* armed: on THE PACK, this slot; on THE POUND (locked), the first free PACK slot */
                save_armed = 1; save_t = fm1_ms; save_to = prog >= NFACT ? prog : pack_free(); dirty_hdr = dirty_page = 1;
            }
        }
        if (b & (1u << BTN_SEL) && save_armed) {   /* SAVE armed + SELECT pressed: a new sound (dice) instead */
            randomize();
            save_armed = 0;
            dirty_hdr = dirty_tags = dirty_page = 1;
        }
        if (b & (1u << BTN_REC) && !layer) hold_toggle();   /* WAG: HOLD, on any page, the ARP button's latch */
        ctl_tstop = fm1_in.buttons >> BTN_SEQ & 1u;   /* FLOP: TAPE STOP while SEQ is held (obv_deck.h) */
        if (b & (1u << BTN_PLAY) || (KILL_MOMENTARY && killed && (rel & (1u << BTN_PLAY)))) {   /* HEEL: STOP / live */
            killed = KILL_MOMENTARY ? (b >> BTN_PLAY & 1u) : killed ^ 1u;
            ctl_kill = killed;
            if (killed && hold) { hold = 0; ctl_hold = 0; dirty_tags = 1; }   /* STOP lets a latched HOLD go (the notes it held are cleared) */
            dirty_hdr = 1;
        }
        if (save_armed && fm1_ms - save_t > 3000u) { save_armed = 0; dirty_page = dirty_hdr = 1; }
        {
            static uint32_t sel_was;            /* SELECT pressed or let go on a page with secondaries: its knobs change */
            if (sel_held() != sel_was) { sel_was = sel_held(); if (page == PG_DRIVE || page == PG_TAPE || page == PG_BBD || page == PG_SPRING) { dirty_page = 1; map_dirty = map_on; } }
        }
        if (np != page) {
            if (layer_lock) { layer = L_NONE; layer_lock = 0; }
            page = np; fam_note(np); dirty_page = 1; map_dirty = map_on;   /* (the map follows the page) */
            hints_key = 0xFFFFFFFFu; leds_q = 0xFFFFFFFFu;
        }

        /* encoders */
        if ((e = fm1_enc_take(ENC_PRESETS)) != 0) {
            if (save_armed) {                   /* SAVE armed: PRESETS picks the slot to save into ("save as"), 33-99 only */
                save_to = NFACT + (uint32_t)((int32_t)(save_to - NFACT) + e + (int32_t)PACK_N * 4) % PACK_N;
                save_t = fm1_ms;
                dirty_hdr = 1;
            } else {
                load_program((uint32_t)((int32_t)prog + e + (int32_t)NPROG * 4) % NPROG);
                set.prog = (uint8_t)prog; set_dirty = 1; set_t = fm1_ms;
                dirty_hdr = dirty_page = dirty_tags = 1;
            }
        }
        if ((e = fm1_enc_take(ENC_SELECT)) != 0) {   /* SELECT: LFO RATE on HOME (nothing held), 2 a detent; nowhere else (the tempo
                                                 * lives on GLOBAL knob 1 and the MIDI clock, as before) */
            if (page == PG_PERFORM && !layer) {
                set_param(P_LFO_RATE, (int32_t)live.v[P_LFO_RATE] + e * 2);
                readout("LFO RATE", P_LFO_RATE);
                dirty_hdr = dirty_page = 1;
            }
        }
        if ((e = fm1_enc_take(ENC_ALGORITHM)) != 0) {   /* SLOBBER: the SLOP ride, on any page, on top of the sound's
                                                 * VINTAGE; never stored, 0 at power-on */
            if (e > 1 || e < -1) e *= 3;        /* (a fast turn goes further, as the knobs) */
            slop = (uint32_t)clampi((int32_t)slop + e * 2, 0, 127);
            ctl_slop = slop;
            slop_shown_t = fm1_ms + 1u; dirty_hdr = 1;
        }
        if (slop_shown_t && fm1_ms + 1u - slop_shown_t >= 1000u) { slop_shown_t = 0; dirty_hdr = 1; }   /* (back to the tags) */
        if (ro_t && fm1_ms + 1u - ro_t >= 1000u) { ro_t = 0; dirty_hdr = 1; }   /* (the readout is gone: back to the tags) */
        for (k = 0; k < 4u; k++) {
            int32_t p = page_now()->p[k];
            if ((e = fm1_enc_take(ENC_KNOB1 + k)) == 0) continue;
            if (e > 1 || e < -1) e *= 3;        /* a fast turn goes further */
            if (page == PG_GLOBAL && !layer) {  /* (a held layer has the knobs, on every page) */
                if (k == 0) { set.tempo = (uint8_t)clampi(set.tempo + e, 40, 240); ctl_tempo = set.tempo; }
                else if (k == 1) set.fleas = (uint8_t)clampi(set.fleas + e * 2, 0, 100);   /* FLEAS, 2 a detent */
                else if (k == 2) set.midi_ch = (uint8_t)clampi(set.midi_ch + e, 0, 16);
                else { set.tune = (int8_t)clampi(set.tune + e, -50, 50); ctl_tune8 = set.tune * 256 / 100; }
                set_dirty = 1; set_t = fm1_ms;
            } else if (layer == L_FX) {
                layer_used = 1;
                if (FX_LAYER[k] == P_ALLEY) alley_turn(P_ALLEY, e);   /* (from SYNC: the time sounding, as on its page) */
                else set_param((uint32_t)FX_LAYER[k], (int32_t)live.v[FX_LAYER[k]] + e * 2);
                dirty_tags = 1;
            } else if (p == P_ALLEY || p == P_ALLEY_FINE || p == P_DLY_TIME) {
                alley_turn((uint32_t)p, e);
                dirty_hdr = 1;
            } else if (p >= 0) {
                int32_t step = PDEF[p].max >= 100 ? 2 : 1;
                set_param((uint32_t)p, (int32_t)live.v[p] + e * step);
                if (page == PG_PERFORM && !layer) { home_dial_p = p; home_dial_t = fm1_ms; home_dial_dirty = 1; }   /* HOME:
                                                                     the knob's dial over the art (Batch 24; scene_tick) */
                if (p == P_MODE || p == P_FTYPE || p == P_ARP_MODE || p >= P_GRL_BIAS) dirty_tags = 1;
                dirty_hdr = 1;
            }
            dirty_page = 1;
        }

        midi_in(0);
        if (ctl_ext_quarter && fm1_ms - clk_last > 2000u) { ctl_ext_quarter = 0; clk_n = 0; }

        /* LEDs: the keys that sound, the lit buttons */
        glow = 0;
        for (k = 0; k < NV; k++)
            if (ui_vlevel[k] > 300 && ui_vnote[k] >= base && ui_vnote[k] < base + 27u)
                lit |= 1u << (ui_vnote[k] - base);
        {
            uint32_t on = set.oct < 0, up2 = set.oct > 0;
            lit |= ((uint32_t)(live.v[P_ARP_MODE] != 0) << 28) | (on << 29) | (up2 << 30);
        }
        if (lit != leds_prev || glow != glow_prev) {
            leds_prev = lit;
            glow_prev = glow;
            for (k = 0; k < 27u; k++) { fm1_led_key(KEY_LED(k), lit >> k & 1u); fm1_led_key_glow(KEY_LED(k), glow >> k & 1u); }
            fm1_led_key(BTN_ARP, lit >> 28 & 1u);
            fm1_led_key(BTN_OCT_DOWN, lit >> 29 & 1u);
            fm1_led_key(BTN_OCT_UP, lit >> 30 & 1u);
        }
        fm1_led_key(BTN_HOME, page == PG_PERFORM);
        fm1_led_key(BTN_EDIT, in_fam(FAM_EDIT));
        fm1_led_key(BTN_ENV, in_fam(FAM_ENV));
        fm1_led_key(BTN_LFO, in_fam(FAM_LFO));
        fm1_led_key(BTN_FX, in_fam(FAM_FX));
        fm1_led_key(BTN_GLO, in_fam(FAM_GLO));
        fm1_led_key(BTN_SAVE, save_armed);
        fm1_led_key(BTN_REC, hold);             /* WAG lit: HOLD is latched */
        fm1_led_key(BTN_PLAY, killed);          /* HEEL lit: stopped */
        fm1_led_key(BTN_SEQ, ctl_tstop);        /* FLOP lit: the tape stops */

        /* the screen: only what changed */
        idle_ok = 1;
        if (map_on) {                           /* HOME held: the map has the whole screen (notes still sound) */
            sc_leave();
            if (map_dirty && fm1_ms - t_page >= 30u) { map_dirty = 0; t_page = fm1_ms; draw_map(); }
        } else if (page == PG_PERFORM && !layer) {   /* HOME: the scene (dog5_scene.h) */
            scene_tick(&t_hdr);
        } else {
            if (sc_k != 0xFFu) {                /* leaving the scene: the panel back */
                sc_leave();
                lcd_fill(0, 0, 240, 240, C_PANEL);
                dirty_hdr = dirty_page = dirty_tags = 1; hints_key = leds_q = 0xFFFFFFFFu; scope_state = 1; t_scope = 0;
            }
            if (dirty_hdr && fm1_ms - t_hdr >= 30u) { dirty_hdr = 0; t_hdr = fm1_ms; draw_header(); }
            if (dirty_page && fm1_ms - t_page >= 30u) { dirty_page = 0; t_page = fm1_ms; draw_page(); }
            if (dirty_tags) { dirty_tags = 0; draw_tags(); }
            if (fm1_ms - t_led >= 40u) {
                uint32_t q = 0;
                t_led = fm1_ms;
                for (k = 0; k < NV; k++) q = q * 9u + ((uint32_t)ui_vlevel[k] >> 12);   /* 8 steps a LED: redraw on a change */
                if (layer) draw_hints();
                else if (q != leds_q) { leds_q = q; draw_leds(); }
                if (page == PG_GLOBAL && fm1_ms - t_page >= 250u) dirty_page = 1;
            }
            if (scope_state == 3u && fm1_ms - t_scope >= 50u) {
                uint32_t v, best = 0, bl = 0;
                t_scope = fm1_ms;
                draw_scope();
                for (v = 0; v < NV; v++)            /* the stride from the loudest voice's period: ~2 cycles across */
                    if ((uint32_t)ui_vlevel[v] > bl) { bl = (uint32_t)ui_vlevel[v]; best = ui_vnote[v]; }
                if (bl) {
                    uint32_t inc = pitch_inc((int32_t)best << 8), period = inc ? 0xFFFFFFFFu / inc : 1000u;
                    scope_stride = clampi((int32_t)(period * 2u / SCOPE_N), 1, 64);
                }
                scope_state = 1;
            } else if (scope_state == 1u && fm1_ms - t_scope >= 400u) {   /* silence: a flat line */
                t_scope = fm1_ms;
                for (i = 0; i < SCOPE_N; i++) scope[i] = 0;
                draw_scope();
            }
        }
        idle_ok = 0;
        if ((set_dirty || ps_dirty) && engine_quiet() && fm1_ms - set_t > 2000u) {   /* when silent: an erase stalls the sound */
            uint32_t i;
            for (i = 0; i < NPSECT; i++)        /* the programs before the settings (a 1.4 update: they leave the settings) */
                if (ps_dirty >> i & 1u) psect_save(i, &psect[i], sizeof psect[i]);
            ps_dirty = 0;
            if (set_dirty) settings_save(&set, sizeof set);
            set_dirty = 0;
        }
    }
}
