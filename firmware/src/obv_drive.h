/* SPDX-License-Identifier: GPL-3.0-only */
/* GROWL, the preamp drive: stage 1 of the Psych Chain (CLAUDE.md section 6). It takes the summed voice bus before the
 * output stage (so CC 7 never changes how hard it is driven), at the bus's full resolution (a quiet tail into a
 * high GROWL keeps its detail), and hands the output stage its usual scale (the bus >> 2); the delay and the reverb
 * follow. Integers only. Per channel (L and R alike: the voices' stereo spread stays):
 *
 *   in (clamped +-131071) -> pre-clip low-pass (two one-poles: open up to GROWL 25, then down to 3 kHz at 127; a
 *   high-gain stage's bandwidth falls, as the classic op-amp fuzz's does, and it keeps the clipped edges from
 *   aliasing) -> 4x up (two polyphase allpass halfbands) -> x gain + bias -> soft clip (the tanh table) - its value at
 *   the bias -> 4x down -> DC block (~10 Hz) -> TONE (a one-pole, weighted in as GROWL rises, so a gentle setting
 *   stays open) -> makeup.
 *
 * The makeup is a static law per GROWL (tools/gen_tables.py: a saw at one voice's level comes out at its own RMS),
 * which moves with the gain, times a slow trim (~1.5 s) to the input's loudness: a chord or a hotter patch clips harder
 * than one voice, and the trim takes that back. It may go +-12 dB from GROWL 40 up, less below, none at a gentle
 * setting (where the static law is exact), so a fast turn down to clean never leaves a stale trim behind. Turning GROWL up changes the sound, not the level,
 * while a note's own swell and sustain inside that time stay. GROWL 0 is a bit-exact bypass;
 * entering and leaving it crossfades over 256 frames. Patch bytes (the chorus's three, CC 67-69): P_GROWL,
 * P_GRL_BIAS (the asymmetry: even harmonics), P_GRL_TONE. tests/drive/ has the measurements. */

/* the halfbands (hb1_*, hb2_* below; tests/drive/halfband.py designs and checks them), Q12: 44.1 <-> 88.2 kHz passes
 * 18 kHz, -65 dB from 26 kHz (4 coefficients); 88.2 <-> 176.4 kHz -61 dB from 66 kHz (2). More buys nothing here:
 * tests/drive measured the same aliasing with 5 + 3 */

typedef struct {
    int32_t lp1, lp2;                           /* the pre-clip low-pass */
    int32_t u1x[4], u1y[4], u2x[2], u2y[2], d2x[2], d2y[2], d1x[4], d1y[4];   /* the halfbands' sections */
    int32_t dcx, dcy, tone;
} grl_ch_t;
static grl_ch_t grl_ch[2];
static int32_t grl_g, grl_g_t;                  /* the gain into the clip, Q4 (on the bus): it glides to its target */
static int32_t grl_kpre, grl_kt, grl_bias, grl_sb;   /* pre-LP k Q12, TONE k Q14, the bias, the clip's value there */
static int32_t grl_ms, grl_ms_t, grl_trim, grl_dtr, grl_tw;   /* the static makeup Q15 (glides with the gain), the slow trim
                                                 * Q12, and how far it may go (0..256 of +-12 dB) */
static int32_t grl_mix;                         /* 0 .. 16384: the bypass crossfade */
static uint32_t grl_on;                         /* GROWL > 0 */
static int32_t grl_pin, grl_pout;               /* the slow input / output powers, as the ear weights them */
typedef struct { int32_t hp, lp; } grl_kw_t;
static grl_kw_t grl_kw_in, grl_kw_out;

/* the patch's numbers, once per ISR call */
static void drive_block(const patch_t *p)
{
    uint32_t v = p->v[P_GROWL] & 127u, b = p->v[P_GRL_BIAS] & 127u;
    int32_t kt = GRL_KTONE[p->v[P_GRL_TONE] & 127u];
    grl_on = v != 0;
    if (!v) return;                             /* (leaving: the crossfade keeps the last numbers) */
    grl_g_t = GRL_G_Q4[v];
    grl_kpre = GRL_KPRE[v];
    grl_kt = 16384 - (((16384 - kt) * (int32_t)GRL_TONEW[v]) >> 8);
    grl_bias = (int32_t)(b * b * 2u);           /* 0 .. ~1 of tanh's input: 40 (the default) ~0.1, a little warmth */
    grl_ms_t = GRL_M_Q15[v];
    grl_tw = GRL_TONEW[v];                      /* (the same ramp as TONE's: none at a gentle GROWL, all of it from 40) */
}

/* the existing tanh table (softclip's, obv_dsp.h), branch-free: 32767 tanh(x / 32768) up to |x| = 2 (0.964), flat
 * beyond (the slope there is already 0.07: the knee is all but round) */
static inline __attribute__((always_inline)) int32_t grl_sat(int32_t x)
{
    int32_t s = x >> 31, a = (x ^ s) - s, i, y;
    a = a > 65535 ? 65535 : a;
    i = a >> 8;
    y = TANH_Q15[i] + (((TANH_Q15[i + 1] - TANH_Q15[i]) * (a & 255)) >> 8);
    return (y ^ s) - s;
}

/* the polyphase allpass halfbands (as L. de Soras' HIIR): a section is y = a (x - y1) + x1 at the low rate, the even
 * coefficients on one path, the odd on the other. Up: one in, two out (the earlier first); down: two in (the earlier
 * first), their mean out. Written out (coefficients as constants): the inner loop of the drive */
#define GRL_AP(v, xs, ys, i, a) do { int32_t t_ = ((((v) - (ys)[i]) * (a)) >> 12) + (xs)[i]; (xs)[i] = (v); (ys)[i] = t_; (v) = t_; } while (0)
static inline __attribute__((always_inline)) void hb1_up(grl_ch_t *c, int32_t v, int32_t *o0, int32_t *o1)
{
    int32_t e = v, o = v;
    GRL_AP(e, c->u1x, c->u1y, 0, 346); GRL_AP(o, c->u1x, c->u1y, 1, 1214); GRL_AP(e, c->u1x, c->u1y, 2, 2295);
    GRL_AP(o, c->u1x, c->u1y, 3, 3449);
    *o0 = e; *o1 = o;
}
static inline __attribute__((always_inline)) int32_t hb1_down(grl_ch_t *c, int32_t v0, int32_t v1)
{
    int32_t e = v1, o = v0;
    GRL_AP(e, c->d1x, c->d1y, 0, 346); GRL_AP(o, c->d1x, c->d1y, 1, 1214); GRL_AP(e, c->d1x, c->d1y, 2, 2295);
    GRL_AP(o, c->d1x, c->d1y, 3, 3449);
    return (e + o) >> 1;
}
static inline __attribute__((always_inline)) void hb2_up(grl_ch_t *c, int32_t v, int32_t *o0, int32_t *o1)
{
    int32_t e = v, o = v;
    GRL_AP(e, c->u2x, c->u2y, 0, 565); GRL_AP(o, c->u2x, c->u2y, 1, 2395);
    *o0 = e; *o1 = o;
}
static inline __attribute__((always_inline)) int32_t hb2_down(grl_ch_t *c, int32_t v0, int32_t v1)
{
    int32_t e = v1, o = v0;
    GRL_AP(e, c->d2x, c->d2y, 0, 565); GRL_AP(o, c->d2x, c->d2y, 1, 2395);
    return (e + o) >> 1;
}

static inline int32_t grl_glide(int32_t d, int32_t sh)   /* 1 / 2^sh of the way, the last bit at once */
{
    return d > -(1 << sh) && d < (1 << sh) ? d : d >> sh;
}

static uint32_t isqrt32(uint32_t x)
{
    uint32_t r = 0, b = 1u << 30;
    while (b > x) b >>= 2;
    for (; b; b >>= 2)
        if (x >= r + b) { x -= r + b; r = (r >> 1) + b; } else r >>= 1;
    return r;
}

/* the trim, Q12: 4096 * sqrt(pin / pout), held to 1/4 .. 4 (+-12 dB). 32-bit only: both normalised, one 32-bit
 * division */
static int32_t grl_trim_for(uint32_t pin, uint32_t pout)
{
    int32_t e = 24;
    uint32_t q;
    if (pin >= pout << 4) return 16384;
    if (pout >= pin << 4) return 1024;
    while (pin < (1u << 29)) { pin <<= 1; e--; }
    while (pout >= (1u << 15)) { pout >>= 1; e--; }
    while (pout < (1u << 14)) { pout <<= 1; e++; }
    q = pin / pout;                             /* 2^14 .. 2^16: the ratio x 2^(24 - e) */
    return (int32_t)isqrt32(e >= 0 ? q << e : q >> -e);   /* (< 2^28: the ratio is < 16) */
}

/* loudness as the ear hears it, near enough: ITU-R BS.1770's K-weighting as a 50 Hz one-pole low cut and +4 dB above
 * 1.5 kHz (a one-pole shelf); within 0.9 dB of the real curve from 50 Hz to 16 kHz. x: |x| < 2^12 (the output stage's
 * Q15 >> 3) */
static inline __attribute__((always_inline)) int32_t grl_kweight(grl_kw_t *w, int32_t x)
{
    int32_t h;
    w->hp += (((x << 8) - w->hp) * 233) >> 15;  /* (state Q8: the 50 Hz pole is slow) */
    h = x - (w->hp >> 8);
    w->lp += ((h - w->lp) * 6308) >> 15;
    return clampi(h + (((h - w->lp) * 19173) >> 15), -11585, 11585);   /* (16 squares of it < 2^31) */
}

static inline __attribute__((always_inline)) int32_t grl_one(grl_ch_t *c, int32_t x, int32_t g, int32_t kpre)
{
    int32_t a, b, h0, h1, h2, h3, bias = grl_bias, sb = grl_sb;
    c->lp1 += ((x - c->lp1) * kpre) >> 12;      /* (x: the bus, |x| < 2^17) */
    c->lp2 += ((c->lp1 - c->lp2) * kpre) >> 12;
    hb1_up(c, c->lp2, &a, &b);
    hb2_up(c, a, &h0, &h1);
    hb2_up(c, b, &h2, &h3);
    h0 = grl_sat(((h0 * g) >> 6) + bias) - sb;
    h1 = grl_sat(((h1 * g) >> 6) + bias) - sb;
    h2 = grl_sat(((h2 * g) >> 6) + bias) - sb;
    h3 = grl_sat(((h3 * g) >> 6) + bias) - sb;
    a = hb2_down(c, h0, h1);                    /* (in this order: the two calls share one filter) */
    b = hb2_down(c, h2, h3);
    a = hb1_down(c, a, b);
    c->dcy = a - c->dcx + ((c->dcy * 16361) >> 14);   /* (1 - 2 pi 10 Hz / fs, Q14) */
    c->dcx = a;
    c->tone += ((c->dcy - c->tone) * grl_kt) >> 14;
    return c->tone;
}

static inline uint32_t drive_on(void) { return grl_on || grl_mix; }   /* else the engine skips it: bit for bit */

/* s: the voice bus in, the output stage's scale (the bus >> 2) out */
static void drive_process(int32_t *s, uint32_t n, int32_t vol_q12)
{
    uint32_t i;
    if (grl_on && !grl_mix) {                   /* entering from the bypass: clean states, the trim at 0 dB */
        static const grl_ch_t z0;
        static const grl_kw_t w0;
        grl_ch[0] = grl_ch[1] = z0;
        grl_kw_in = grl_kw_out = w0;
        grl_g = grl_g_t; grl_ms = grl_ms_t; grl_trim = 4096; grl_dtr = 0; grl_pin = grl_pout = 0;
    }
    grl_sb = grl_sat(grl_bias);
    for (i = 0; i < n; i += 16u) {              /* 16 frames a step: the gain and the static makeup glide together
                                                   (~1.5 ms) to a new GROWL, the trim (~23 ms) to its target; every
                                                   glide is linear sample by sample and lands exactly: no steps */
        uint32_t ein = 0, eout = 0, k, j;
        int32_t g0 = grl_g, dg = grl_glide(grl_g_t - grl_g, 2), ms0 = grl_ms, dms = grl_glide(grl_ms_t - grl_ms, 2);
        int32_t tr0 = grl_trim, dtr = grl_dtr, kpre = grl_kpre, tt;
        for (k = i, j = 1; k < i + 16u && k < n; k++, j++) {
            int32_t g = g0 + ((dg * (int32_t)j) >> 4), ms = ms0 + ((dms * (int32_t)j) >> 4), tr = tr0 + ((dtr * (int32_t)j) >> 4);
            int32_t xl = clampi(s[2u * k], -262144, 262143) >> 2, xr = clampi(s[2u * k + 1u], -262144, 262143) >> 2;
            int32_t yl = grl_one(&grl_ch[0], clampi(s[2u * k], -131071, 131071), g, kpre);   /* (xl, xr: the dry, */
            int32_t yr = grl_one(&grl_ch[1], clampi(s[2u * k + 1u], -131071, 131071), g, kpre), d;   /* as without it) */
            yl = (yl * ms) >> 15;               /* the static law: one voice's saw at its own RMS */
            yr = (yr * ms) >> 15;
            /* the powers as heard: through the output stage's tanh (mono, CC 7 included), then K-weighted */
            d = grl_kweight(&grl_kw_in, grl_sat(((xl + xr) >> 1) * vol_q12 >> 10) >> 3); ein += (uint32_t)(d * d);
            d = grl_kweight(&grl_kw_out, grl_sat(((yl + yr) >> 1) * vol_q12 >> 10) >> 3); eout += (uint32_t)(d * d);
            yl = (yl * tr) >> 12;               /* the slow trim: the rest of the way to the input's loudness */
            yr = (yr * tr) >> 12;
            if (grl_mix < 16384 || !grl_on) {   /* the crossfade in or out of the bypass */
                grl_mix = clampi(grl_mix + (grl_on ? 64 : -64), 0, 16384);
                yl = xl + (((yl - xl) * grl_mix) >> 14);
                yr = xr + (((yr - xr) * grl_mix) >> 14);
            }
            s[2u * k] = yl;
            s[2u * k + 1u] = yr;
        }
        grl_g = g0 + dg;                        /* (= the block's last sample: (d * 16) >> 4 = d) */
        grl_ms = ms0 + dms;
        grl_trim = tr0 + dtr;
        grl_pin += ((int32_t)ein - grl_pin) >> 12;   /* ~1.5 s (each < 2^31: 16 x 11585^2) */
        grl_pout += ((int32_t)eout - grl_pout) >> 12;
        tt = grl_pin > 64 && grl_pout > 64 ? grl_trim_for((uint32_t)grl_pin, (uint32_t)grl_pout) : grl_trim;
        tt = clampi(tt, 4096 - ((3072 * grl_tw) >> 8), 4096 + ((12288 * grl_tw) >> 8));   /* a gentle GROWL needs none */
        grl_dtr = grl_glide(tt - grl_trim, 6);  /* the next 16 frames go 1/64 of the way */
    }
}
