/* SPDX-License-Identifier: GPL-3.0-only */
/* TAPE on its own (firmware/src/obv_tape.h, unchanged), fed ideal inputs instead of the synth: what the stage itself
 * adds. Levels are Q15 (32767 = full scale), the scale the effects hand it. Writes raw int32 stereo (or text).
 *
 *   cc -O2 -Ifirmware/src -Ifirmware/gen -o build/tape/bench tests/tape/tape_bench.c -lm
 *   bench OUT.raw sine F0 PEAK SECONDS CHEW [WF HISS DROPS]   a sine (computed in double: a pure tone)
 *   bench OUT.raw saw F0 PEAK SECONDS CHEW [WF HISS DROPS]    a band-limited saw (every harmonic below fs/2)
 *   bench OUT.raw sweep F0 PEAK [HISS DROPS]                  a sine, CHEW 0 -> 127 -> 0 one detent (2) every 60 ms
 *   bench OUT.txt fixed F0 PEAK                               the sine at each FIXED CHEW 0..127, HISS / DROPS off
 *                                                             (2 s to settle, 1.5 s measured): "CHEW largest-step RMS"
 *   bench OUT.raw toggle F0 PEAK CHEW                         a sine, CHEW 0 -> CHEW -> 0 -> CHEW (entering / leaving
 *                                                             the bypass, 3 s apart)
 *   bench OUT.raw dc LEVEL SECONDS CHEW HISS                  a DC input (keeps the hiss awake): the output's AC part
 *                                                             is the hiss alone
 *   bench OUT.raw worst                                       full-scale squares and noise, every CHEW, the secondaries'
 *                                                             corners, knob jumps (for -fsanitize: no overflow)
 * The float only makes the test signals; the stage is the firmware's integer code. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define FS 44100u
#define HALF_FRAMES 256u
#include "obv_dsp.h"
#include "obv_params.h"
#include "obv_fx.h"
#include "obv_drive.h"
#include "obv_tape.h"

static patch_t pt;
static FILE *out;
static int32_t buf[512];

/* TP_ONLY=read|sat|tone (environment): keep one part, switch the others off after tape_block (the proofs isolate
 * the moving read from the saturation and the head's tone) */
static void isolate(void)
{
    const char *o = getenv("TP_ONLY");
    if (!o) return;
    if (strcmp(o, "read")) { tp_aw_t = tp_af_t = 0; }
    if (strcmp(o, "sat")) tp_s_t = 0;
    if (strcmp(o, "tone")) { tp_k_t = 16384; tp_b_t = 0; }
}

static FILE *dlog;                              /* TP_LOG=path: the head's delay at the end of each 16-frame block */

static void run(const double *l, const double *r, uint32_t n)
{
    uint32_t i;
    for (i = 0; i < n; i++) { buf[2u * i] = sat16((int32_t)lrint(l[i])); buf[2u * i + 1u] = sat16((int32_t)lrint(r[i])); }
    tape_block(&pt);                            /* (as engine_audio: once an ISR call, after the effects) */
    isolate();
    if (!dlog) { if (tape_on()) tape_process(buf, n); }
    else for (i = 0; i < n; i += 16u) {         /* (the same, a block at a time, to log the head) */
        if (tape_on()) tape_process(buf + 2u * i, 16);
        fwrite(&tp_d, 4, 1, dlog);
    }
    fwrite(buf, 4, 2u * n, out);
}

static void secondaries(int argc, char **argv, int at)
{
    if (argc > at) pt.v[P_TP_WOWFLT] = (uint8_t)atoi(argv[at]);
    if (argc > at + 1) pt.v[P_TP_HISS] = (uint8_t)atoi(argv[at + 1]);
    if (argc > at + 2) pt.v[P_TP_DROPS] = (uint8_t)atoi(argv[at + 2]);
}

int main(int argc, char **argv)
{
    static double l[256], r[256];
    uint32_t i, k;
    if (argc < 3) { fprintf(stderr, "see the comment at the top\n"); return 1; }
    out = fopen(argv[1], "wb");
    if (getenv("TP_LOG")) dlog = fopen(getenv("TP_LOG"), "wb");
    patch_defaults(&pt);
    if (!strcmp(argv[2], "saw") || !strcmp(argv[2], "sine")) {
        int sine = argv[2][1] == 'i';
        double f0 = atof(argv[3]), peak = atof(argv[4]), ph = 0;
        uint32_t n = (uint32_t)(atof(argv[5]) * FS), nh = (uint32_t)(FS / 2 / f0);
        pt.v[P_CHEW] = (uint8_t)atoi(argv[6]);
        secondaries(argc, argv, 7);
        for (i = 0; i < n; i += 256u) {
            for (k = 0; k < 256u; k++, ph += f0 / FS) {
                double s = 0;
                uint32_t h;
                if (sine) s = sin(2 * M_PI * ph);
                else { for (h = 1; h <= nh; h++) s += sin(2 * M_PI * h * ph) / h * (h & 1u ? 1 : -1); s *= 2 / M_PI / 1.18; }
                l[k] = r[k] = peak * s;
            }
            run(l, r, 256);
        }
    } else if (!strcmp(argv[2], "sweep")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]), ph = 0;
        int32_t g = 0, dir = 1;
        uint32_t next = FS / 2;
        secondaries(argc, argv, 4);             /* (argv[5], argv[6]: HISS, DROPS; WF stays 64) */
        pt.v[P_TP_WOWFLT] = 64;
        for (i = 0; i < FS * 12u; i += 256u) {
            for (k = 0; k < 256u; k++, ph += f0 / FS) l[k] = r[k] = peak * sin(2 * M_PI * ph);
            if (i >= next) {                    /* a detent (2 steps) every 60 ms: up to 127, a rest, down to 0 */
                next += FS * 60u / 1000u;
                g += 2 * dir;
                if (g >= 127) { g = 127; dir = -1; next += FS / 2; }
                if (g <= 0 && dir < 0) { g = 0; dir = 0; }
            }
            pt.v[P_CHEW] = (uint8_t)g;
            run(l, r, 256);
        }
    } else if (!strcmp(argv[2], "fixed")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]);
        uint32_t g;
        pt.v[P_TP_HISS] = 0; pt.v[P_TP_DROPS] = 0;
        for (g = 0; g < 128u; g++) {
            double ph = 0, ss = 0, mx = 0;
            int32_t prev = 0;
            uint32_t nn = 0;
            tp_run = 0; tp_mix = 0; tp_on = 0;  /* (each from the bypass, as on entering it) */
            pt.v[P_CHEW] = (uint8_t)g;
            for (i = 0; i < FS * 7u / 2u; i += 256u) {
                for (k = 0; k < 256u; k++, ph += f0 / FS) buf[2u * k] = buf[2u * k + 1u] = (int32_t)lrint(peak * sin(2 * M_PI * ph));
                tape_block(&pt);
                isolate();
                if (tape_on()) tape_process(buf, 256);
                for (k = 0; k < 256u; k++) {
                    if (i > 2u * FS) { double d = fabs((double)buf[2u * k] - prev); if (d > mx) mx = d; ss += (double)buf[2u * k] * buf[2u * k]; nn++; }
                    prev = buf[2u * k];
                }
            }
            fprintf(out, "%u %f %f\n", g, mx, sqrt(ss / nn));
        }
    } else if (!strcmp(argv[2], "toggle")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]), ph = 0;
        uint32_t v = (uint32_t)atoi(argv[5]);
        for (i = 0; i < FS * 13u; i += 256u) {
            uint32_t sec = i / FS;
            for (k = 0; k < 256u; k++, ph += f0 / FS) l[k] = r[k] = peak * sin(2 * M_PI * ph);
            pt.v[P_CHEW] = (uint8_t)(sec >= 1u && sec < 4u ? v : sec >= 7u && sec < 10u ? v : 0u);
            run(l, r, 256);
        }
    } else if (!strcmp(argv[2], "dc")) {
        double lev = atof(argv[3]);
        uint32_t n = (uint32_t)(atof(argv[4]) * FS);
        pt.v[P_CHEW] = (uint8_t)atoi(argv[5]);
        pt.v[P_TP_HISS] = (uint8_t)atoi(argv[6]);
        pt.v[P_TP_DROPS] = 0;
        for (k = 0; k < 256u; k++) l[k] = r[k] = lev;
        for (i = 0; i < n; i += 256u) run(l, r, 256);
    } else if (!strcmp(argv[2], "worst")) {     /* the corners: every CHEW with the secondaries at 0 / 127, full scale */
        static const uint8_t S[4][3] = {{0, 0, 0}, {127, 127, 127}, {0, 127, 127}, {127, 0, 0}};
        uint32_t c, g, seed = 1;
        for (c = 0; c < 4u; c++)
            for (g = 0; g < 128u; g += 3u) {
                pt.v[P_CHEW] = (uint8_t)(g & 4u ? 127u - g : g);   /* (jumps as well as steps) */
                pt.v[P_TP_WOWFLT] = S[c][0]; pt.v[P_TP_HISS] = S[c][1]; pt.v[P_TP_DROPS] = S[c][2];
                for (i = 0; i < 40u; i++) {     /* a full-scale square (the hardest edges), then full-scale noise */
                    for (k = 0; k < 256u; k++) {
                        seed = seed * 1103515245u + 12345u;
                        l[k] = i < 20u ? ((k / 37u) & 1u ? 32767 : -32767) : (double)(int32_t)seed / 65536.0;
                        r[k] = i < 20u ? ((k / 23u) & 1u ? -32767 : 32767) : -l[k];
                    }
                    run(l, r, 256);
                }
            }
    }
    fclose(out);
    if (dlog) fclose(dlog);
    return 0;
}
