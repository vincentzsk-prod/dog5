/* SPDX-License-Identifier: GPL-3.0-only */
/* The effects after the output stage: ALLEY, the BBD delay, and a plate reverb (J. Dattorro's figure-of-eight tank,
 * 1997). All lines are int16 in one .pool buffer; the signals are Q15 as the output stage leaves them. Integers only.
 * (The chorus is gone: its three patch bytes carry the preamp drive, obv_drive.h, which runs on the voice bus before
 * the output stage.)
 *
 * ALLEY (the Psych Chain's stage 2, CLAUDE.md section 6) is OberVave's ping-pong delay re-voiced as a bucket brigade:
 *   - the time is free, 10 .. 740 ms (P_ALLEY 1..127, BBD_T; P_ALLEY_FINE splits a step, so a tapped time is exact),
 *     or SYNC (P_ALLEY 0): the note value in P_DLY_TIME at the tempo, as the old delay (the factory patches' times);
 *   - each pass through the line is band-limited as a BBD's filters do it, a 2-pole (Q 0.8) and a 1-pole low-pass,
 *     and the corner falls with the time (8 kHz at 10 ms .. 2.8 kHz at 740 ms: more buckets per second of delay is a
 *     slower clock), so a long echo is darker and every repeat darker than the last;
 *   - the feedback path keeps OberVave's TONE (a 1-pole, the same law), loses its lows (a 1-pole high-pass at 80 Hz,
 *     the coupling caps: repeats thin out instead of booming) and goes through the BBD's headroom (Drive's tanh at
 *     half level: unity for small signals, -0.7 dB and H3 at -34 dB for a full-scale input, a ceiling at 2x full
 *     scale); the repeats on their way back also pass the tanh at full level (a ceiling at full scale), so the
 *     repeats grit up as they build and a runaway settles under full scale. FEEDBK keeps the old law (x 250, Q15) up to 112, then runs to 1.25 at 127: from ~119 the loop gains
 *     more than it loses and the repeats run away into self-oscillation, held by that headroom;
 *   - a time change moves the read like a BBD's clock: the repeats in the line bend in pitch (down while the time
 *     grows, up while it shrinks), at most an octave down / a fifth up, the bend eased in and out (the read's speed
 *     changes at most 0.5 in 1024 samples): never a jump in the read, so never a click (the old delay's speed stepped);
 *   - PINGPONG (P_BBD_SPREAD) 127 is the old ping-pong (the input enters left, the repeats cross), 0 puts every repeat
 *     in the middle as a mono BBD does (equal power: 0.71 each side).
 * DLY_MIX 0 adds nothing to the dry: the output is the old delay's bypass, bit for bit (the line may still run).
 * REV_DIV 1: the reverb at the full rate (the sound comes first). 2: at half the rate, if the chip turns out
 * to need it: a dark hall loses little by it and it halves the reverb's time and memory. */
#ifndef REV_DIV
#define REV_DIV 1u
#endif
#define RVL(x) ((uint32_t)((x) * 44100u / 29761u / REV_DIV))   /* the paper's 29761 Hz lengths at our rate */
#define DLY_MAX 32768u                          /* a side of the delay: 743 ms */
#define REV_PRE_N (8192u / REV_DIV)             /* up to 120 ms of pre-delay */
#define RV_IN1 RVL(142)
#define RV_IN2 RVL(107)
#define RV_IN3 RVL(379)
#define RV_IN4 RVL(277)
#define RV_AP1 RVL(672)
#define RV_D1 RVL(4453)
#define RV_AP2 RVL(1800)
#define RV_D2 RVL(3720)
#define RV_AP3 RVL(908)
#define RV_D3 RVL(4217)
#define RV_AP4 RVL(2656)
#define RV_D4 RVL(3163)
#define REV_N (REV_PRE_N + RV_IN1 + RV_IN2 + RV_IN3 + RV_IN4 + RV_AP1 + 16u + RV_D1 + RV_AP2 + RV_D2 + RV_AP3 + 16u + RV_D3 + RV_AP4 + RV_D4)
#define RV_BW (REV_DIV == 2u ? 24000 : 16700)   /* the input's one-pole: ~5 kHz either way */
#define FX_MEM_N (2u * DLY_MAX + REV_N)
#define RV_TAP_MAX 109225                       /* the largest |sum| whose x 19661 fits int32 */
_Static_assert(RV_TAP_MAX * 19661LL <= 2147483647LL && (RV_TAP_MAX + 1) * 19661LL > 2147483647LL, "RV_TAP_MAX");

typedef struct { int16_t *b; uint32_t len, w; } line_t;   /* w: where the next sample goes */
static int16_t fx_mem[FX_MEM_N] __attribute__((section(".pool")));
static uint32_t fx_used;

static inline int32_t sat16(int32_t v) { return v > 32767 ? 32767 : v < -32767 ? -32767 : v; }
static void line_init(line_t *l, uint32_t len) { l->b = fx_mem + fx_used; l->len = len; l->w = 0; fx_used += len; }
static inline __attribute__((always_inline)) int32_t line_read(const line_t *l, uint32_t back)   /* 1 <= back <= len */
{
    uint32_t i = l->w + l->len - back;
    if (i >= l->len) i -= l->len;
    return l->b[i];
}
static inline __attribute__((always_inline)) void line_write(line_t *l, int32_t v)
{
    l->b[l->w] = (int16_t)sat16(v);
    if (++l->w >= l->len) l->w = 0;
}
/* Dattorro's allpass: the line holds the inner node, the output is tapped from it. g Q15, signed */
static inline __attribute__((always_inline)) int32_t ap_step(line_t *l, int32_t in, int32_t g)
{
    int32_t d = line_read(l, l->len), v = in - ((d * g) >> 15);
    line_write(l, v);
    return d + ((v * g) >> 15);
}
/* the same with the delay swaying by e (Q8 samples, |e| <= 8 << 8) around base; the line is base + 16 long */
static inline __attribute__((always_inline)) int32_t ap_mod(line_t *l, int32_t in, int32_t g, uint32_t base, int32_t e)
{
    uint32_t back = (uint32_t)((int32_t)base + (e >> 8));
    int32_t f = e & 255, a = line_read(l, back), b = line_read(l, back + 1u), d = a + (((b - a) * f) >> 8), v;
    v = in - ((d * g) >> 15);
    line_write(l, v);
    return d + ((v * g) >> 15);
}
static inline int32_t tri_q(uint32_t ph)        /* a triangle -2048..2047 (so Q8 = +-8 samples) */
{
    int32_t t = (int32_t)(ph >> 19);            /* 0..8191 */
    return t < 4096 ? t - 2048 : 6143 - t;
}

/* ---- the state */
static line_t dl, dr, rv_pre, rv_in[4], rv_ap1, rv_d1, rv_ap2, rv_d2, rv_ap3, rv_d3, rv_ap4, rv_d4;
static uint32_t rv_ph1, rv_ph2;
static int32_t dly_mix, rev_mix, dly_fb, dly_tone_k, rev_decay, rev_damp_k;
static int32_t dly_time, dly_cur, dly_vel;      /* Q16 samples: the target and where the read is; its speed (Q16 a sample) */
static int32_t dly_lpl, dly_lpr, rv_lp_in, rv_lpl, rv_lpr, rv_yl, rv_yr;
typedef struct { int32_t ic1, ic2, p3, hp; } bbd_ch_t;   /* a line's filters: the SVF, the third pole, the high-pass */
static bbd_ch_t bbd_ch[2];
static int32_t bbd_a1, bbd_a2, bbd_a3, bbd_k1, bbd_ca, bbd_cb;   /* the bandwidth (Q14, Q15); PINGPONG's gains (Q8) */

#if REV_DIV == 2u
static int32_t rv_hold;
#endif
static uint32_t rev_pre_n = 1, dly_active, rev_active;
#if REV_DIV == 2u
static uint32_t fx_odd;
#endif

static void fx_init(void)
{
    line_init(&dl, DLY_MAX);
    line_init(&dr, DLY_MAX);
    line_init(&rv_pre, REV_PRE_N);
    line_init(&rv_in[0], RV_IN1); line_init(&rv_in[1], RV_IN2); line_init(&rv_in[2], RV_IN3); line_init(&rv_in[3], RV_IN4);
    line_init(&rv_ap1, RV_AP1 + 16u); line_init(&rv_d1, RV_D1); line_init(&rv_ap2, RV_AP2); line_init(&rv_d2, RV_D2);
    line_init(&rv_ap3, RV_AP3 + 16u); line_init(&rv_d3, RV_D3); line_init(&rv_ap4, RV_AP4); line_init(&rv_d4, RV_D4);
    dly_cur = dly_time = 11025 << 16;
}

/* ALLEY's time in samples (Q16) for P_ALLEY a (1..127) and FINE f: BBD_T, f/128 of the way to the next step */
static int32_t alley_q16(uint32_t a, uint32_t f)
{
    uint32_t t0 = BBD_T[a & 127u], t1 = a < 127u ? BBD_T[a + 1u] : t0;
    return (int32_t)((t0 << 16) + (((t1 - t0) * (f & 127u)) << 9));
}
/* the other way: the step at or below n samples (1..127) and the 1/128ths to the next, for a tap or a knob leaving SYNC */
static uint32_t alley_index(uint32_t n, uint32_t *fine)
{
    uint32_t lo = 1, hi = 127;
    if (n <= BBD_T[1]) { *fine = 0; return 1; }
    if (n >= BBD_T[127]) { *fine = 0; return 127; }
    while (hi - lo > 1u) { uint32_t m = (lo + hi) >> 1; if (BBD_T[m] <= n) lo = m; else hi = m; }
    *fine = ((n - BBD_T[lo]) * 128u + ((BBD_T[hi] - BBD_T[lo]) >> 1)) / (BBD_T[hi] - BBD_T[lo]);
    if (*fine > 127u) *fine = 127u;
    return lo;
}

/* the patch's numbers, once per ISR call. quarter: frames per quarter note (the arp's clock) */
static void fx_block(const patch_t *p, uint32_t quarter)
{
    int32_t d, t;
    uint32_t div = p->v[P_DLY_TIME] % NDDIV, samples;
    dly_mix = (p->v[P_DLY_MIX] * 180) >> 7;     /* wet up to 0.7 of the dry (Q8): the sum stays in range */
    rev_mix = (p->v[P_REV_MIX] * 180) >> 7;
    d = p->v[P_DLY_FB];                         /* 0 .. 0.85 as before; 113..127 on to 1.25: the loop holds at ~118 (it
                                                 * loses ~0.3 dB a pass) and runs away above */
    dly_fb = d <= 112 ? d * 250 : 28000 + (d - 112) * 864;
    t = p->v[P_DLY_TONE]; dly_tone_k = clampi(((t * t) >> 6) + 8, 8, 256);
    d = p->v[P_REV_SIZE]; rev_decay = 12000 + ((d * d * 19500) >> 14);   /* 0.37 .. 0.96: the top is a near-freeze */
    d = p->v[P_REV_DAMP]; rev_damp_k = 32768 - d * d * 2;   /* the one-pole's k at the half rate */
    if (REV_DIV == 1u) {                        /* the same corner at the full rate: k' = 1 - sqrt(1 - k) */
        uint32_t x = (uint32_t)(32768 - rev_damp_k) << 15, r = 0, bit = 1u << 15;
        for (; bit; bit >>= 1)
            if ((r + bit) * (r + bit) <= x) r += bit;
        rev_damp_k = 32768 - (int32_t)r;
    }
    rev_pre_n = 1u + (uint32_t)p->v[P_REV_PRE] * (41u / REV_DIV);
    if (p->v[P_ALLEY]) dly_time = alley_q16(p->v[P_ALLEY], p->v[P_ALLEY_FINE]);
    else {                                      /* SYNC: a note value of the tempo, as OberVave's delay */
        samples = quarter * DDIV_NUM[div] / DDIV_DEN[div];
        if (samples > DLY_MAX - 4u) samples = DLY_MAX - 4u;
        if (samples < 64u) samples = 64u;
        dly_time = (int32_t)(samples << 16);
    }
    {                                           /* the bandwidth follows where the read IS (a clock, while it glides) */
        uint32_t f, i = alley_index((uint32_t)dly_cur >> 16, &f);
        bbd_a1 = BBD_A1[i]; bbd_a2 = BBD_A2[i]; bbd_a3 = BBD_A3[i]; bbd_k1 = BBD_K1[i];
    }
    d = p->v[P_BBD_SPREAD];                     /* the near side 0.71 .. 1, the far side 0.71 .. 0 */
    bbd_ca = 181 + ((d * 75) >> 7); bbd_cb = 181 - ((d * 181 + 64) >> 7);
    if (d >= 127) { bbd_ca = 256; bbd_cb = 0; }
    if (dly_mix) {
        if (!dly_active) {                      /* waking (12 s after the last mix): what the lines held is gone, so a
                                                 * patch's old repeats (or a runaway) never come back */
            static const bbd_ch_t z0;
            uint32_t k;
            for (k = 0; k < 2u * DLY_MAX; k++) fx_mem[k] = 0;
            bbd_ch[0] = bbd_ch[1] = z0;
            dly_lpl = dly_lpr = 0;
            dly_cur = dly_time; dly_vel = 0;    /* (and the read starts where it belongs: no glide in from before) */
        }
        dly_active = 12u * FS;
    } else if (dly_active > HALF_FRAMES) dly_active -= HALF_FRAMES; else dly_active = 0;
    if (rev_mix) rev_active = 24u * FS; else if (rev_active > HALF_FRAMES) rev_active -= HALF_FRAMES; else rev_active = 0;
}

static inline __attribute__((always_inline)) int32_t line_read_q16(const line_t *l, int32_t back_q16)
{
    uint32_t b = (uint32_t)back_q16 >> 16;
    int32_t f = (back_q16 >> 8) & 255, a = line_read(l, b), c = line_read(l, b + 1u);
    return a + (((c - a) * f) >> 8);
}
/* the BBD's tanh: softclip's table (tanh(x / full scale), flat from 2x full scale at 0.96), read branch-free (softclip's
 * two branches cost ~20 a call here: ALLEY calls it four times a sample) */
static inline __attribute__((always_inline)) int32_t bbd_sat(int32_t x)
{
    int32_t s = x >> 31, a = (x ^ s) - s, i, y;
    a = a > 65535 ? 65535 : a;
    i = a >> 8;
    y = TANH_Q15[i] + (((TANH_Q15[i + 1] - TANH_Q15[i]) * (a & 255)) >> 8);
    return (y ^ s) - s;
}
/* a line read at back (Q16), through the BBD's filters (a 2-pole SVF, Q 0.8, and a 1-pole at the same corner); the
 * line holds half the level (the headroom), the read gives it back */
static inline __attribute__((always_inline)) int32_t bbd_read(const line_t *l, bbd_ch_t *c, int32_t back_q16)
{
    int32_t x = line_read_q16(l, back_q16), v3 = x - c->ic2, v1, v2;
    v1 = (bbd_a1 * c->ic1 + bbd_a2 * v3 + 8192) >> 14;   /* (rounded: a floor here leaves a DC offset) */
    v2 = c->ic2 + ((bbd_a2 * c->ic1 + bbd_a3 * v3 + 8192) >> 14);
    c->ic1 = 2 * v1 - c->ic1;
    c->ic2 = 2 * v2 - c->ic2;
    c->p3 += ((v2 - c->p3) * bbd_k1 + 16384) >> 15;
    return c->p3 * 2;
}
/* one reverb sample at the half rate: in -> pre-delay -> bandwidth -> 4 diffusers -> the two tank halves */
static inline void rev_tick(int32_t in)
{
    int32_t x, a, b, e1 = tri_q(rv_ph1), e2 = tri_q(rv_ph2), dec = rev_decay, dk = rev_damp_k;
    rv_ph1 += 97391u * REV_DIV;                 /* ~1.0 Hz and ~0.7 Hz: the tank's sway against metallic rings */
    rv_ph2 += 68174u * REV_DIV;
    line_write(&rv_pre, in);
    x = line_read(&rv_pre, rev_pre_n);
    rv_lp_in += ((x - rv_lp_in) * RV_BW) >> 15;
    x = ap_step(&rv_in[0], rv_lp_in, 24576);
    x = ap_step(&rv_in[1], x, 24576);
    x = ap_step(&rv_in[2], x, 20480);
    x = ap_step(&rv_in[3], x, 20480);
    /* left half, fed by the right's end */
    a = x + ((line_read(&rv_d4, RV_D4) * dec) >> 15);
    a = ap_mod(&rv_ap1, a, -22938, RV_AP1, e1);
    line_write(&rv_d1, a);
    b = line_read(&rv_d1, RV_D1);
    rv_lpl += ((b - rv_lpl) * dk) >> 15;
    b = ap_step(&rv_ap2, (rv_lpl * dec) >> 15, 16384);
    line_write(&rv_d2, b);
    /* right half, fed by the left's end */
    a = x + ((line_read(&rv_d2, RV_D2) * dec) >> 15);
    a = ap_mod(&rv_ap3, a, -22938, RV_AP3, e2);
    line_write(&rv_d3, a);
    b = line_read(&rv_d3, RV_D3);
    rv_lpr += ((b - rv_lpr) * dk) >> 15;
    b = ap_step(&rv_ap4, (rv_lpr * dec) >> 15, 16384);
    line_write(&rv_d4, b);
    /* the output taps (the paper's), x 0.6. Seven int16 taps can sum to 7x full scale, and a x 19661 product leaves
     * int32 past |109,225| (3.3x: a hot input fills the tank at a big SIZE). That wrapped on the chip into a
     * polarity-flipped, full-scale crack (listen/spring/STEP0.md). The clamp is the identity below it, and above it
     * still gives 2x full scale, which the output's clip pins exactly where the true product would have */
    a = line_read(&rv_d3, RVL(266)) + line_read(&rv_d3, RVL(2974)) - line_read(&rv_ap4, RVL(1913)) + line_read(&rv_d4, RVL(1996))
      - line_read(&rv_d1, RVL(1990)) - line_read(&rv_ap2, RVL(187)) - line_read(&rv_d2, RVL(1066));
    b = line_read(&rv_d1, RVL(353)) + line_read(&rv_d1, RVL(3627)) - line_read(&rv_ap2, RVL(1228)) + line_read(&rv_d2, RVL(2673))
      - line_read(&rv_d3, RVL(2111)) - line_read(&rv_ap4, RVL(335)) - line_read(&rv_d4, RVL(121));
    rv_yl = (clampi(a, -RV_TAP_MAX, RV_TAP_MAX) * 19661) >> 15;
    rv_yr = (clampi(b, -RV_TAP_MAX, RV_TAP_MAX) * 19661) >> 15;
}

static __attribute__((noinline)) void fx_process(int32_t *out, uint32_t n)   /* (inlined, it moved the voice loop: +28 a sample with the effects off) */
{
    uint32_t i, do_dly = dly_active != 0, do_rev = rev_active != 0;
    int32_t dm = dly_mix, rm = rev_mix;
    for (i = 0; i < n; i++) {
        int32_t l = out[2u * i], r = out[2u * i + 1u];
        if (do_dly) {                           /* ALLEY: the input enters left, the feedback crosses */
            int32_t wl, wr, want, fl, fr;
            if (dly_cur != dly_time || dly_vel) {   /* the read glides: ~46 ms a step, eased */
                want = clampi((dly_time - dly_cur) >> 11, -32768, 32768);
                dly_vel += clampi(want - dly_vel, -32, 32);
                dly_cur += dly_vel;
                if (!want && dly_vel >= -32 && dly_vel <= 32) { dly_cur = dly_time; dly_vel = 0; }   /* (the last 1/32) */
            }
            wl = bbd_read(&dl, &bbd_ch[0], dly_cur);
            wr = bbd_read(&dr, &bbd_ch[1], dly_cur);
            dly_lpl += ((wr - dly_lpl) * dly_tone_k) >> 8;   /* TONE, as before; then the coupling caps' high-pass */
            dly_lpr += ((wl - dly_lpr) * dly_tone_k) >> 8;
            bbd_ch[1].hp += (((dly_lpl * 16) - bbd_ch[1].hp) * 371) >> 15;
            bbd_ch[0].hp += (((dly_lpr * 16) - bbd_ch[0].hp) * 371) >> 15;
            fl = bbd_sat(dly_lpl - (bbd_ch[1].hp >> 4));   /* the loop's own limit (tanh, full scale): a runaway */
            fr = bbd_sat(dly_lpr - (bbd_ch[0].hp >> 4));   /* rounds off here, under the line's 2x headroom */
            line_write(&dl, bbd_sat((((l + r) >> 1) + (((fl >> 1) * dly_fb) >> 14)) >> 1));   /* the BBD's headroom: */
            line_write(&dr, bbd_sat((((fr >> 1) * dly_fb) >> 14) >> 1));   /* tanh(u / 2) at half level */
            if (dm) {
                int32_t ol = (wl * bbd_ca + wr * bbd_cb) >> 8, or_ = (wr * bbd_ca + wl * bbd_cb) >> 8;
                l += (ol * dm) >> 8;
                r += (or_ * dm) >> 8;
            }
        }
        if (do_rev) {
#if REV_DIV == 2u                               /* half rate: a pair in, the output interpolated between ticks */
            int32_t pl = rv_yl, pr = rv_yr, din = l + r;
            if (!(fx_odd ^= 1u)) {
                rev_tick((rv_hold + din) >> 2);
                l += (((pl + rv_yl) >> 1) * rm) >> 8;
                r += (((pr + rv_yr) >> 1) * rm) >> 8;
            } else {
                l += (rv_yl * rm) >> 8;
                r += (rv_yr * rm) >> 8;
            }
            rv_hold = din;
#else
            rev_tick((l + r) >> 1);
            l += (rv_yl * rm) >> 8;
            r += (rv_yr * rm) >> 8;
#endif
        }
        out[2u * i] = sat16(l);
        out[2u * i + 1u] = sat16(r);
    }
}
