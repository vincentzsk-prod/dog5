/* SPDX-License-Identifier: GPL-3.0-only */
/* TAPE STOP (SEQ held, FLOP): the deck loses power. One motor, one speed. It is one stage at the very end, after
 * everything is summed (the voices, GROWL, ALLEY's repeats, DRAIN's tail, CHEW's hiss) and before STOP's gate, so all of
 * it slows and darkens together.
 *
 *   the mix -> a history line (int16, L R L R) -> a read that falls behind as the speed drops (tape's 6-point read,
 *   tp_taps, the one the wow and flutter use) -> one low-pass for both channels (the voices' SVF, svf_coef / svf_lp)
 *   closing with the dive -> the level -> crossfaded with the live mix
 *
 * The curve is the one approved on the chord on 3 Nov:
 *   - held, the speed falls in a straight line over half a bar at the tempo (1 s at 120 BPM), so the frequency falls
 *     in a straight line (a platter's friction);
 *   - the low-pass goes from wide open down by DK_CUT_K times the dive, in semitones;
 *   - the level stays flat to a third of the speed, then goes to nothing with it (a stopped deck is silent, so
 *     holding it never leaves a rumble).
 * The read starts 3 samples behind the live mix, crossfaded in over DK_XIN samples (no jump).
 * Let go: the live mix is back over DK_XOUT samples (5.8 ms; a crossfade, so no click), then the stage rests.
 *
 * At rest only the last 16 frames of each block are recorded (the read's start needs 3) and the output is untouched,
 * bit for bit. The half bar is clamped to 0.5 .. 1.1 s: the read falls behind by half the stop time (0.55 s at most),
 * and that is what the line holds (DK_N, 96 KB of the pool). */
#define DK_N 24576u                             /* frames: 557 ms, > 1.1 s / 2 + the read's 6 points */
#define DK_DMIN (3 << 16)                       /* the read's start, Q16 samples behind the newest */
#define DK_XIN 128                              /* samples: live -> the deck at a press */
#define DK_XOUT 256                             /* samples: the deck -> live at the release */
#define DK_CUT_K 5                              /* the low-pass's dive, x 1/4 of the pitch's (checked against the
                                                 * approved render's brightness: tests/trick/tapestop_ab.py) */
#define DK_TMAX (FS * 11u / 10u)                /* the longest stop, frames */

static int16_t dk_line[2u * DK_N] __attribute__((section(".pool")));
static volatile uint32_t ctl_tstop;             /* main loop: SEQ held */
static uint32_t dk_w;                           /* where the next frame is written (0 .. DK_N - 1) */
static uint32_t dk_run;                         /* the stage is sounding (from a press to the end of its release) */
static int32_t ts_pos;                          /* how far stopped, Q16: 0 full speed .. TS_ONE stopped */
static int32_t dk_d;                            /* the read's lag, Q16 samples */
static int32_t dk_x;                            /* the crossfade: 0 live .. 32768 the deck */
static int32_t dk_g = 32768;                    /* the level, Q15 */
static svf_state_t dk_f[2];
#define TS_ONE 65536

static void deck_clear(void)                    /* (STOP: nothing recorded plays back) */
{
    static const svf_state_t z0;
    uint32_t k;
    for (k = 0; k < 2u * DK_N; k++) dk_line[k] = 0;
    dk_f[0] = dk_f[1] = z0;
    dk_run = 0; ts_pos = 0; dk_d = DK_DMIN; dk_x = 0; dk_g = 32768;
}

static inline uint32_t deck_rest(void) { return !dk_run && !ts_pos && dk_x == 0; }

/* the frame lag (Q16) behind the newest frame i, both channels: tape's 6-point read (tp_taps' weights), on this line */
static inline __attribute__((always_inline)) void dk_read(uint32_t i, int32_t dq16, const int32_t *h, int32_t *o)
{
    uint32_t b = i + DK_N - ((uint32_t)dq16 >> 16) - 3u, k, j;   /* the oldest of the six (y3) */
    int32_t l, r;
    if (b >= DK_N) b -= DK_N;
    if (b + 5u < DK_N) {                        /* (all but 5 in 24,576 reads: no wrap inside) */
        const int16_t *p = dk_line + 2u * b;
        l = h[5] * p[0] + h[4] * p[2] + h[3] * p[4] + h[2] * p[6] + h[1] * p[8] + h[0] * p[10];
        r = h[5] * p[1] + h[4] * p[3] + h[3] * p[5] + h[2] * p[7] + h[1] * p[9] + h[0] * p[11];
    } else {
        l = r = 0;
        for (k = 0; k < 6u; k++) {
            j = b + k; if (j >= DK_N) j -= DK_N;
            l += h[5u - k] * dk_line[2u * j];
            r += h[5u - k] * dk_line[2u * j + 1u];
        }
    }
    o[0] = l >> 15;
    o[1] = r >> 15;
}

static __attribute__((noinline)) void deck_process(int32_t *s, uint32_t n)
{
    uint32_t i, held = ctl_tstop;
    if (!held && deck_rest()) {                 /* at rest: keep the newest 16 frames, the output untouched */
        uint32_t k, from = n > 16u ? n - 16u : 0;
        for (k = from; k < n; k++) {
            uint32_t w = (dk_w + k) % DK_N;
            dk_line[2u * w] = (int16_t)s[2u * k]; dk_line[2u * w + 1u] = (int16_t)s[2u * k + 1u];
        }
        dk_w = (dk_w + n) % DK_N;
        return;
    }
    if (held && !dk_run) {                      /* a press: from full speed, 3 samples behind, filter open */
        static const svf_state_t z0;
        dk_run = 1; dk_d = DK_DMIN; dk_f[0] = dk_f[1] = z0;
        if (!dk_x) ts_pos = 0;
    }
    for (i = 0; i < n; i += CTL) {              /* a block: the speed, the filter, the level */
        uint32_t k, j;
        int32_t s0, s1, d0 = dk_d, dd, g0 = dk_g, g1, tgt, f, dive, ix;
        svf_coef_t c;
        if (held) {
            uint32_t q = ctl_ext_quarter ? ctl_ext_quarter : 60u * FS / clampi(ctl_tempo, 40, 240);
            int32_t step = (int32_t)((uint32_t)TS_ONE * CTL / clampi((int32_t)q * 2, FS / 2, (int32_t)DK_TMAX));
            ts_pos = ts_pos + step > TS_ONE ? TS_ONE : ts_pos + step;
        }
        s0 = TS_ONE - ts_pos;                   /* the speed, Q16 (held at the release: the fade is the return) */
        s1 = s0;
        dd = (TS_ONE - s1) * (int32_t)CTL;      /* the read falls behind by 1 - speed a sample */
        if (d0 + dd > (int32_t)(DK_N - 8u) << 16) dd = 0;   /* (only once the deck is silent: the lag is then frozen) */
        dk_d = d0 + dd;
        tgt = s1 * 3 >> 1;                      /* the level: 3 x the speed (Q16 -> Q15: x 3 / 2) */
        g1 = tgt > 32768 ? 32768 : tgt;
        dk_g = g1;
        ix = ts_pos >> 10; f = ts_pos & 1023;
        dive = ix >= 64 ? TS_DIVE8[64] : TS_DIVE8[ix] + (((TS_DIVE8[ix + 1] - TS_DIVE8[ix]) * f) >> 10);
        svf_coef(&c, (136 << 8) + ((dive * DK_CUT_K) >> 2), 5793);   /* Q 0.71, from wide open (19.8 kHz) */
        for (k = i, j = 1; k < i + CTL && k < n; k++, j++) {
            int32_t h[6], y[2], dq = d0 + ((dd * (int32_t)j) >> 4), g = g0 + (((g1 - g0) * (int32_t)j) >> 4), ch;
            uint32_t w = dk_w;
            dk_line[2u * w] = (int16_t)s[2u * k]; dk_line[2u * w + 1u] = (int16_t)s[2u * k + 1u];
            tp_taps(dq, h);
            dk_read(w, dq, h, y);
            if (++dk_w >= DK_N) dk_w = 0;
            if (held) dk_x = dk_x + (32768 / DK_XIN) > 32768 ? 32768 : dk_x + 32768 / DK_XIN;
            else dk_x = dk_x > 32768 / DK_XOUT ? dk_x - 32768 / DK_XOUT : 0;
            for (ch = 0; ch < 2; ch++) {
                int32_t v = (svf_lp(&c, &dk_f[ch], y[ch]) * g) >> 15, x = s[2u * k + (uint32_t)ch];
                s[2u * k + (uint32_t)ch] = sat16(x + (((v - x) * (dk_x >> 3)) >> 12));
            }
        }
    }
    if (!held && !dk_x) { dk_run = 0; ts_pos = 0; dk_d = DK_DMIN; dk_g = 32768; }   /* released and faded: rest */
}
