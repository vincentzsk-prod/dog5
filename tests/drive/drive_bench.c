/* SPDX-License-Identifier: GPL-3.0-only */
/* GROWL on its own (firmware/src/obv_drive.h, unchanged), fed an ideal input instead of the synth: what the drive
 * itself adds. PEAK is at the drive's output scale (the voice bus >> 2; one voice's saw peaks ~1400 there); the bus
 * it is fed is 4x that. Writes the drive's output as raw int32 stereo.
 *
 *   cc -O2 -Ifirmware/src -Ifirmware/gen -o build/drive/bench tests/drive/drive_bench.c -lm
 *   build/drive/bench OUT.raw saw F0 PEAK SECONDS GROWL [BIAS TONE]   a band-limited saw (every harmonic below fs/2,
 *                                                                   summed in double: no aliasing in the input)
 *   build/drive/bench OUT.raw sweep F0 PEAK                          a sine, GROWL 0 -> 127 -> 0 one detent (2) every
 *                                                                   60 ms, as a knob turned on the DRIVE page
 *   build/drive/bench OUT.txt fixed F0 PEAK                          the sine at each FIXED GROWL 0..127 (1 s to settle,
 *                                                                   1.5 s measured): "GROWL largest-step RMS" lines,
 *                                                                   the sweep's reference (analyze.py)
 *   build/drive/bench OUT.raw worst                                  full-scale squares and noise, every GROWL, BIAS
 *                                                                   and TONE corner (for -fsanitize: no overflow)
 * The float here only makes the test signals; the drive is the firmware's integer code. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define FS 44100u
#include "obv_dsp.h"
#include "obv_params.h"
#include "obv_drive.h"

static patch_t pt;
static FILE *out;
static int32_t buf[512];

static void run(const double *l, const double *r, uint32_t n)
{
    uint32_t i;
    for (i = 0; i < n; i++) { buf[2u * i] = (int32_t)lrint(4 * l[i]); buf[2u * i + 1u] = (int32_t)lrint(4 * r[i]); }
    drive_block(&pt);                           /* (as engine_audio: the bus in, at 4x the drive's scale) */
    if (drive_on()) drive_process(buf, n, 4032);   /* (CC 7 at 127, as the host and the device start) */
    else for (i = 0; i < 2u * n; i++) buf[i] = clampi(buf[i], -262144, 262143) >> 2;
    fwrite(buf, 4, 2u * n, out);
}

int main(int argc, char **argv)
{
    static double l[256], r[256];
    uint32_t i, k;
    if (argc < 3) { fprintf(stderr, "see the comment at the top\n"); return 1; }
    out = fopen(argv[1], "wb");
    patch_defaults(&pt);
    if (!strcmp(argv[2], "saw")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]), ph = 0;
        uint32_t n = (uint32_t)(atof(argv[5]) * FS), nh = (uint32_t)(FS / 2 / f0);
        pt.v[P_GROWL] = (uint8_t)atoi(argv[6]);
        if (argc > 7) pt.v[P_GRL_BIAS] = (uint8_t)atoi(argv[7]);
        if (argc > 8) pt.v[P_GRL_TONE] = (uint8_t)atoi(argv[8]);
        for (i = 0; i < n; i += 256u) {
            for (k = 0; k < 256u; k++, ph += f0 / FS) {
                double s = 0;
                uint32_t h;
                for (h = 1; h <= nh; h++) s += sin(2 * M_PI * h * ph) / h * (h & 1u ? 1 : -1);
                l[k] = r[k] = peak * s * 2 / M_PI / 1.18;   /* (the band-limited saw overshoots to ~1.18) */
            }
            run(l, r, 256);
        }
    } else if (!strcmp(argv[2], "sweep")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]), ph = 0;
        int32_t g = 0, dir = 1;
        uint32_t t = 0, next = FS / 2;
        for (i = 0; i < FS * 10u; i += 256u) {
            for (k = 0; k < 256u; k++, ph += f0 / FS) l[k] = r[k] = peak * sin(2 * M_PI * ph);
            if (i >= next) {                    /* a detent (2 steps) every 60 ms: up to 127, a rest, down to 0 */
                next += FS * 60u / 1000u;
                g += 2 * dir;
                if (g >= 127) { g = 127; dir = -1; next += FS / 2; }
                if (g <= 0 && dir < 0) { g = 0; dir = 0; }
            }
            pt.v[P_GROWL] = (uint8_t)g;
            run(l, r, 256);
            t++;
        }
        (void)t;
    } else if (!strcmp(argv[2], "fixed")) {
        double f0 = atof(argv[3]), peak = atof(argv[4]);
        uint32_t g;
        for (g = 0; g < 128u; g++) {
            static const grl_ch_t z0;
            double ph = 0, ss = 0, mx = 0;
            int32_t prev = 0;
            uint32_t nn = 0;
            grl_ch[0] = grl_ch[1] = z0; grl_mix = 0; grl_on = 0;   /* (each from the bypass, as on entering it) */
            pt.v[P_GROWL] = (uint8_t)g;
            for (i = 0; i < FS * 5u / 2u; i += 256u) {
                for (k = 0; k < 256u; k++, ph += f0 / FS) { buf[2u * k] = buf[2u * k + 1u] = (int32_t)lrint(4 * peak * sin(2 * M_PI * ph)); }
                drive_block(&pt);
                if (drive_on()) drive_process(buf, 256, 4032);
                else for (k = 0; k < 512u; k++) buf[k] = clampi(buf[k], -262144, 262143) >> 2;
                for (k = 0; k < 256u; k++) {
                    if (i > FS) { double d = fabs((double)buf[2u * k] - prev); if (d > mx) mx = d; ss += (double)buf[2u * k] * buf[2u * k]; nn++; }
                    prev = buf[2u * k];
                }
            }
            fprintf(out, "%u %f %f\n", g, mx, sqrt(ss / nn));
        }
    } else if (!strcmp(argv[2], "worst")) {     /* the corners: every GROWL with BIAS / TONE at 0 and 127, full scale */
        static const uint8_t BT[4][2] = {{0, 0}, {0, 127}, {127, 0}, {127, 127}};
        uint32_t c, g, seed = 1;
        for (c = 0; c < 4u; c++)
            for (g = 0; g < 128u; g += 3u) {
                pt.v[P_GROWL] = (uint8_t)g; pt.v[P_GRL_BIAS] = BT[c][0]; pt.v[P_GRL_TONE] = BT[c][1];
                for (i = 0; i < 4u; i++) {      /* a full-scale square (the hardest edges), then full-scale noise */
                    for (k = 0; k < 256u; k++) {
                        seed = seed * 1103515245u + 12345u;
                        l[k] = i < 2u ? ((k / 37u) & 1u ? 40000 : -40000) : (double)(int32_t)(seed >> 1) / 32768.0;
                        r[k] = i < 2u ? ((k / 23u) & 1u ? -40000 : 40000) : -l[k];
                    }
                    run(l, r, 256);
                }
            }
    }
    fclose(out);
    return 0;
}
