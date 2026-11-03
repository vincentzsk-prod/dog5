/* SPDX-License-Identifier: GPL-3.0-only */
/* DRAIN's chirp on its own: one chain of the firmware's integer allpasses (obv_fx.h sp_chirp: 4 x SP_M samples at
 * g 0.7), fed an impulse; writes its impulse response (int32 text, one a line) for tests/spring/analyze.py, which
 * reads the group delay against frequency from it. N chains in a row: one pass through the input and one half of the
 * tank is 2, a loop (both halves) adds 2 more.
 *   cc -O2 -Ifirmware/src -Ifirmware/gen -o build/spring/chirp_gd tests/spring/chirp_gd.c && build/spring/chirp_gd N */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#define FS 44100u
#define HALF_FRAMES 256u
#include "obv_dsp.h"
#include "obv_params.h"
#include "obv_fx.h"
int main(int argc, char **argv)
{
    int n = argc > 1 ? atoi(argv[1]) : 1, k, i;
    static int16_t ch[16][SP_NCH][8];
    for (i = 0; i < 4096; i++) {
        int32_t x = i == 0 ? 16384 : 0;
        uint32_t r = sp_w & 7u, w = (sp_w + SP_M) & 7u;
        for (k = 0; k < n; k++) x = sp_chirp(ch[k], x, r, w);
        sp_w++;
        printf("%d\n", x);
    }
    return 0;
}
