/* SPDX-License-Identifier: GPL-3.0-only */
/* The effects stage (firmware/src/obv_fx.h, the firmware's integer code: ALLEY + the reverb) on its own, fed ideal
 * inputs instead of the synth. Levels are Q15, the scale the output stage hands the effects. Writes raw int32, 4
 * channels a frame: in L, in R, out L, out R (out = dry + the wet; the wet = out - in). For the overflow hunt
 * (-fsanitize) it also takes the worst inputs an int16 line can see: a full-scale square and alternating rails.
 *
 *   cc -O2 -Ifirmware/src -Ifirmware/gen -o build/spring/bench tests/spring/spring_bench.c -lm
 *   bench OUT.raw SIGNAL SECONDS [MS:NAME=VALUE ...]
 *     SIGNAL  imp:PEAK                one sample at 100 ms
 *             burst:F:PEAK:MS         a sine burst from 100 ms (raised-cosine edges, 2 ms)
 *             sine:F:PEAK             a sine all the way
 *             square:F:PEAK:MS        a square (no smoothing: the hardest edges) from 100 ms
 *             nyq:PEAK:MS             +PEAK, -PEAK, ... from 100 ms (the highest frequency there is)
 *             noise:PEAK:MS           white noise from 100 ms
 *             none                    silence
 *     NAME    size damp pre mix drain (the reverb's bytes), alley fine fb tone dmix spread sync (the delay's)
 *     e.g.    bench x.raw burst:1000:16384:50 3 0:mix=127 0:size=100 1500:size=20
 * Without a setting: the patch defaults (both effects at MIX 0). The float only makes the test signals. */
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

typedef struct { uint32_t ms; int p; int v; } ev_t;
static ev_t ev[1024];
static int nev;

static int pnum(const char *n)
{
    static const struct { const char *n; int p; } T[] = {
        {"size", P_REV_SIZE}, {"damp", P_REV_DAMP}, {"pre", P_REV_PRE}, {"mix", P_REV_MIX},
#ifdef P_DRAIN
        {"drain", P_DRAIN},
#endif
        {"alley", P_ALLEY}, {"fine", P_ALLEY_FINE}, {"fb", P_DLY_FB}, {"tone", P_DLY_TONE}, {"dmix", P_DLY_MIX},
        {"spread", P_BBD_SPREAD}, {"sync", P_DLY_TIME}, {"tempo", -2},
    };
    uint32_t i;
    for (i = 0; i < sizeof T / sizeof T[0]; i++) if (!strcmp(n, T[i].n)) return T[i].p;
    fprintf(stderr, "unknown %s\n", n);
    exit(1);
}

int main(int argc, char **argv)
{
    static patch_t pt;
    static int32_t buf[2u * HALF_FRAMES], rec[4u * HALF_FRAMES];
    char kind[16] = "";
    double a1 = 0, a2 = 0, a3 = 0, ph = 0;
    uint32_t i, n, k, t, tempo = 120;
    uint32_t rs = 0x2545F491u;
    FILE *out;
    int e;
    if (argc < 4) { fprintf(stderr, "see the comment at the top\n"); return 1; }
    out = fopen(argv[1], "wb");
    if (!out) { perror(argv[1]); return 1; }
    sscanf(argv[2], "%15[a-z]:%lf:%lf:%lf", kind, &a1, &a2, &a3);
    n = (uint32_t)(atof(argv[3]) * FS);
    for (e = 4; e < argc && nev < 1024; e++) {
        char name[16];
        if (sscanf(argv[e], "%u:%15[a-z]=%d", &ev[nev].ms, name, &ev[nev].v) != 3) { fprintf(stderr, "bad %s\n", argv[e]); return 1; }
        ev[nev++].p = pnum(name);
    }
    patch_defaults(&pt);
    fx_init();
    for (t = 0; t < n; t += HALF_FRAMES) {
        uint32_t ms = (uint32_t)((uint64_t)t * 1000u / FS);
        for (e = 0; e < nev; e++)
            if (ev[e].ms <= ms && ev[e].ms + 6u > ms) {      /* (applied at the block it falls in; a block is 5.8 ms) */
                if (ev[e].p == -2) tempo = (uint32_t)ev[e].v;
                else pt.v[ev[e].p] = (uint8_t)ev[e].v;
                ev[e].ms = 0xFFFFFFF0u;
            }
        for (i = 0; i < HALF_FRAMES; i++) {
            uint32_t s = t + i;
            double x = 0, tt = (double)s / FS - 0.1;
            if (!strcmp(kind, "imp")) x = s == FS / 10u ? a1 : 0;
            else if (!strcmp(kind, "burst") || !strcmp(kind, "sine")) {
                double env = 1;
                if (kind[0] == 'b') {
                    double d = a3 / 1000;
                    env = tt < 0 || tt > d ? 0 : tt < 0.002 ? 0.5 - 0.5 * cos(M_PI * tt / 0.002)
                        : tt > d - 0.002 ? 0.5 - 0.5 * cos(M_PI * (d - tt) / 0.002) : 1;
                }
                x = env * a2 * sin(ph);
                ph += 2 * M_PI * a1 / FS;
                if (ph > 2 * M_PI) ph -= 2 * M_PI;
            } else if (!strcmp(kind, "square")) {
                x = tt >= 0 && tt < a3 / 1000 ? (ph < M_PI ? a2 : -a2) : 0;
                ph += 2 * M_PI * a1 / FS;
                if (ph > 2 * M_PI) ph -= 2 * M_PI;
            } else if (!strcmp(kind, "nyq")) {
                x = tt >= 0 && tt < a2 / 1000 ? (s & 1u ? a1 : -a1) : 0;
            } else if (!strcmp(kind, "noise")) {
                rs ^= rs << 13; rs ^= rs >> 17; rs ^= rs << 5;
                x = tt >= 0 && tt < a2 / 1000 ? a1 * ((double)(int32_t)rs / 2147483648.0) : 0;
            }
            buf[2u * i] = buf[2u * i + 1u] = (int32_t)lrint(x);
            rec[4u * i] = rec[4u * i + 1u] = buf[2u * i];
        }
        fx_block(&pt, 60u * FS / tempo);
        fx_process(buf, HALF_FRAMES);
        for (i = 0; i < HALF_FRAMES; i++) { rec[4u * i + 2u] = buf[2u * i]; rec[4u * i + 3u] = buf[2u * i + 1u]; }
        k = n - t < HALF_FRAMES ? n - t : HALF_FRAMES;
        fwrite(rec, 4, 4u * k, out);
    }
    fclose(out);
    return 0;
}
