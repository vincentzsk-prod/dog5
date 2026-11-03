/* SPDX-License-Identifier: GPL-3.0-only */
/* The effects after the output stage: ALLEY, the BBD delay, and DRAIN, a spring re-voiced from a plate reverb
 * (J. Dattorro's figure-of-eight tank, 1997). All lines are int16 in one .pool buffer; the signals are Q15 as the output stage leaves them. Integers only.
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
 *
 * DRAIN (the Psych Chain's stage 3, CLAUDE.md section 6) is the plate pushed toward a spring tank. "The next closest
 * thing", not a waveguide model. What changed from the plate:
 *   - the tank is a spring's size: the figure-eight's loop is 2,926 samples (66 ms, the plate's was 725 ms), so the
 *     tail recirculates as a spring's echoes do (a tank's springs return every 60-75 ms), the flutter you hear as the
 *     "boing"; SIZE is the decay only, 0.3 .. 3.0 s (SPR_DEC_Q15), clamped so it can't bloom into a hall (the
 *     plate ran to a near-freeze), and it glides per sample (a step in a loop gain is a step in the tail: a click);
 *   - the chirp: the plate's two static tank allpasses become chains of four allpasses each, 5 samples long, at
 *     g 0.7 (and one more chain of four at the input). An allpass that short is no longer an echo: it delays the top
 *     more than the bottom (a stretched first-order allpass: 0.9 sample at DC, 28 at 4.4 kHz, the stretch's corner,
 *     near a real spring's transition frequency), so every pass through the loop spreads a transient into a rising
 *     sweep (~3 ms a loop between 3 and 4.4 kHz), the spring's "drip", and the tail grows drippier pass by pass (as a
 *     spring's does: dispersion compounds along the wire);
 *   - the allpasses faster and shallower: the input diffusers half the plate's lengths and g 0.6 / 0.5 (were
 *     0.75 / 0.625: less smear, a splashier attack), the tank's two swaying allpasses g -0.5 (were -0.7), their sway
 *     3.3 / 4.7 Hz +-2.5 samples (were 1.0 / 0.7 Hz +-8): the wire's shimmer, not the plate's slow drift;
 *   - the band of a spring's transducers: a high-pass at 150 Hz into the tank (no low boom: a spring never had it)
 *     and the input's low-pass at 6.5 kHz (was 5 kHz);
 *   - DAMP brighter: open at 0, 20 kHz .. 2.5 kHz along the knob (SPR_DAMP_K; the plate's went down to ~55 Hz);
 *   - PRE-DLY short: 0 .. 35 ms (was 120), a change crossfaded over a block (a jump in the read is a click);
 *   - five output taps a side (were seven; the two on the long allpasses went with them), at the plate's positions
 *     scaled to the new lines.
 * Every allpass here keeps its node in int16 and uses that same saturated node for its output (ap_sat), so each
 * output is bounded (|y| <= 32767 (1 + g)) whatever comes in: nothing in the tank can leave int32 (the plate's tap
 * sum did: the clamp below still guards it). DRAIN 0 adds nothing: the output is the dry, bit for bit.
 * REV_DIV 1: the spring at the full rate (the sound comes first). 2: at half the rate, if the chip turns out to need
 * it: a spring's band ends near 5 kHz anyway, and it halves the spring's time and memory. */
#ifndef REV_DIV
#define REV_DIV 1u
#endif
#define SPL(x) ((uint32_t)(x) / REV_DIV)        /* a length at 44.1 kHz, at the spring's rate */
#define DLY_MAX 32768u                          /* a side of the delay: 743 ms */
#define REV_PRE_N SPL(2048)                     /* up to 35 ms of pre-delay */
#define SP_IN1 SPL(107)                         /* the input diffusers: half the plate's, primes */
#define SP_IN2 SPL(79)
#define SP_IN3 SPL(277)
#define SP_IN4 SPL(199)
#define SP_AP1 SPL(233)                         /* the left half: the swaying allpass, then its line, then the chirp */
#define SP_D1 SPL(797)
#define SP_D2 SPL(389)
#define SP_AP3 SPL(307)                         /* the right half */
#define SP_D3 SPL(863)
#define SP_D4 SPL(337)
/* the spring's lines: one write index for all (sp_w, a tick each), each line a power of two at a fixed place in fx_mem
 * (a mask, not a compare and wrap: cheaper on every read; 13.8 KB, the plate's lines took 83 KB). Sizes for the
 * full rate (the half rate uses half of each) */
#define SPB (2u * DLY_MAX)
#define SPO_PRE SPB                             /* 2048: the pre-delay */
#define SPO_IN1 (SPO_PRE + 2048u)               /* 128, 128, 512, 256: the diffusers */
#define SPO_IN2 (SPO_IN1 + 128u)
#define SPO_IN3 (SPO_IN2 + 128u)
#define SPO_IN4 (SPO_IN3 + 512u)
#define SPO_AP1 (SPO_IN4 + 256u)                /* 256: the left sway (233 + 2.5 + 1) */
#define SPO_D1 (SPO_AP1 + 256u)                 /* 1024 */
#define SPO_D2 (SPO_D1 + 1024u)                 /* 512 */
#define SPO_AP3 (SPO_D2 + 512u)                 /* 512: the right sway (307 + 2.5 + 1) */
#define SPO_D3 (SPO_AP3 + 512u)                 /* 1024 */
#define SPO_D4 (SPO_D3 + 1024u)                 /* 512 */
#define REV_N (SPO_D4 + 512u - SPB)
#define SP_M (REV_DIV == 2u ? 2u : 5u)          /* the chirp's allpasses: 5 samples, the stretch's corner at 4.4 kHz (a
                                                 * spring's transition); at the half rate 2 (5.5 kHz) */
#define SP_NCH 4u                               /* allpasses in a chirp chain; three chains (input, left, right) */
#define SP_CHIRP_G 22938                        /* their g, Q15: 0.7 */
#define RV_BW (REV_DIV == 2u ? 28700 : 19950)   /* the input's one-pole: ~6.5 kHz either way */
#define SP_HP_K (REV_DIV == 2u ? 1408 : 704)    /* the 150 Hz high-pass into the tank (Q15, its state Q8) */
#define FX_MEM_N (2u * DLY_MAX + REV_N)
#define RV_TAP_MAX 65535                        /* the taps' sum, the wet out: at most 2x full scale (the plate fix's
                                                 * guard; the plate's taps x 0.6 could leave int32 past it) */

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
/* the spring's products: rounded (SPF) in the allpasses, toward zero (SPD) at the decay. A floor everywhere (the
 * plate's way) left the short loop parked at a DC; rounding everywhere, in a limit cycle (-83 dBFS at SIZE 80, -76 at
 * 127, for good); toward zero at the four decays makes the loop lose at least a step a pass, so the tail always ends
 * in silence (bench: 0 from ~1.5 s after it falls under -85 dBFS, any SIZE). (+3 instructions a decay) */
#define SPF(t) (((t) + 16384) >> 15)
#define SPD(t) (((t) + (((t) >> 31) & 32767)) >> 15)
static uint32_t sp_w;                           /* the spring's write index (all its lines and the chirp rings) */
/* line at off (size mask + 1): the sample written back ticks ago (0 = this tick's, once written); write this tick's */
#define SP_RD(off, mask, back) ((int32_t)fx_mem[(off) + ((sp_w - (uint32_t)(back)) & (mask))])
#define SP_WR(off, mask, v) (fx_mem[(off) + (sp_w & (mask))] = (int16_t)(v))
/* the allpass (Dattorro's form, the line holds the node) with its node saturated to int16 and that same node in its
 * output: the plain allpass while the node fits int16, and bounded (|y| <= 32767 (1 + |g|)) for any input, so a chain
 * of them can't run away out of range. n: its length */
static inline __attribute__((always_inline)) int32_t ap_sat(uint32_t off, uint32_t mask, uint32_t n, int32_t in, int32_t g)
{
    int32_t d = SP_RD(off, mask, n), v = sat16(in - SPF(d * g));
    SP_WR(off, mask, v);
    return d + SPF(v * g);
}
/* the same with its length swaying by e (Q8 samples, |e| < 3 << 8) around base, read between two samples */
static inline __attribute__((always_inline)) int32_t ap_mod_sat(uint32_t off, uint32_t mask, uint32_t base, int32_t e, int32_t in, int32_t g)
{
    uint32_t back = (uint32_t)((int32_t)base + (e >> 8));
    int32_t f = e & 255, a = SP_RD(off, mask, back), b = SP_RD(off, mask, back + 1u), d = a + (((b - a) * f + 128) >> 8);
    int32_t v = sat16(in - SPF(d * g));
    SP_WR(off, mask, v);
    return d + SPF(v * g);
}
static inline int32_t tri_q(uint32_t ph)        /* a triangle -2048..2047 (so Q8 = +-8 samples) */
{
    int32_t t = (int32_t)(ph >> 19);            /* 0..8191 */
    return t < 4096 ? t - 2048 : 6143 - t;
}

/* ---- the state */
static line_t dl, dr;
static int16_t sp_ch[3][SP_NCH][8];             /* the chirp's allpass nodes: input, left, right chains (SP_M < 8) */
static uint32_t rv_ph1, rv_ph2;                 /* the sways' phases */
static int32_t dly_mix, rev_mix, dly_fb, dly_tone_k, rev_decay, rev_damp_k;   /* (the targets, from the patch) */
static int32_t rv_dec, rv_dk, rv_hp;            /* the decay and damping as they glide (Q15, Q16 state); the HP's state */
static uint32_t rev_pre_old = 1;                /* the pre-delay a crossfade comes from */
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
    fx_used += REV_N;                           /* (the spring's lines: fixed places, SPO_*) */
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
    rev_decay = SPR_DEC_Q15[p->v[P_REV_SIZE] & 127u];   /* RT60 0.3 .. 3.0 s */
    rev_damp_k = SPR_DAMP_K[p->v[P_REV_DAMP] & 127u];   /* open, then 20 kHz .. 2.5 kHz */
    if (REV_DIV == 2u) rev_damp_k = 2 * rev_damp_k - ((rev_damp_k * rev_damp_k) >> 15);   /* the same corner at half
                                                 * the rate: 1 - k' = (1 - k)^2 */
    rev_pre_old = rev_pre_n;                    /* (fx_process crossfades from it over the block) */
    rev_pre_n = 1u + (uint32_t)p->v[P_REV_PRE] * 12u / REV_DIV;   /* 0 .. 34.6 ms */
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
    if (rev_mix) {
        if (!rev_active) {                      /* waking (24 s after the last DRAIN): the old tail is gone, so it never
                                                 * comes back stale, and the glides start where they belong */
            uint32_t k;
            for (k = 2u * DLY_MAX; k < FX_MEM_N; k++) fx_mem[k] = 0;
            for (k = 0; k < 3u * SP_NCH * 8u; k++) (&sp_ch[0][0][0])[k] = 0;
            rv_lp_in = rv_lpl = rv_lpr = rv_yl = rv_yr = rv_hp = 0;
            rv_dec = rev_decay; rv_dk = rev_damp_k; rev_pre_old = rev_pre_n;
        }
        rev_active = 24u * FS;
    } else if (rev_active > HALF_FRAMES) rev_active -= HALF_FRAMES; else rev_active = 0;
}

/* STOP (PLAY, the kill switch, obv_engine.h): every line and filter state of ALLEY and DRAIN to zero, so nothing rings
 * on and nothing comes back when it is let go. The read jumps to its target (no glide in from before); the knobs'
 * glides and the resting timers stay as they are (a stage that was resting stays resting, one running keeps running) */
static void fx_clear(void)
{
    static const bbd_ch_t z0;
    uint32_t k;
    for (k = 0; k < FX_MEM_N; k++) fx_mem[k] = 0;
    for (k = 0; k < 3u * SP_NCH * 8u; k++) (&sp_ch[0][0][0])[k] = 0;
    bbd_ch[0] = bbd_ch[1] = z0;
    dly_lpl = dly_lpr = 0;
    dly_cur = dly_time; dly_vel = 0;
    rv_lp_in = rv_lpl = rv_lpr = rv_yl = rv_yr = rv_hp = 0;
#if REV_DIV == 2u
    rv_hold = 0;
#endif
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
/* the spring's tank writes: linear to 0.75 of full scale, then K + R tanh((|x| - K) / R) (R = 8192, 32,474 at most):
 * the tank (at half level) never reaches it in playing (the factory bank peaks at -3 dBFS there); a hot input rounds
 * into it instead of hard-clipping inside the loop */
static inline __attribute__((always_inline)) int32_t sp_knee(int32_t x)
{
    int32_t s = x >> 31, a = (x ^ s) - s;
    if (a <= 24576) return x;
    a = 24576 + ((bbd_sat(clampi((a - 24576) << 2, 0, 65535)) * 8192) >> 15);
    return (a ^ s) - s;
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
/* the chirp: a chain of SP_NCH (4) allpasses SP_M samples long, written out (rings of 8: each tick reads slot k and
 * writes slot k + SP_M, so the slot read is the one written SP_M ticks ago) */
#define SP_CH1(c, x, r, w) do { int32_t d_ = (c)[r], v_ = sat16((x) - SPF(d_ * SP_CHIRP_G)); (c)[w] = (int16_t)v_; \
                                 (x) = d_ + SPF(v_ * SP_CHIRP_G); } while (0)
static inline __attribute__((always_inline)) int32_t sp_chirp(int16_t (*c)[8], int32_t x, uint32_t r, uint32_t w)
{
    SP_CH1(c[0], x, r, w); SP_CH1(c[1], x, r, w); SP_CH1(c[2], x, r, w); SP_CH1(c[3], x, r, w);
    return x;
}
_Static_assert(SP_NCH == 4u, "sp_chirp is written out for 4");
/* one spring sample (at the spring's rate): in -> pre-delay -> the band (6.5 kHz low-pass, 150 Hz high-pass) -> 4
 * diffusers -> the input chirp -> the two tank halves (sway, line, damping, decay, chirp, line) -> 5 taps a side. The
 * pre-delay is read at pb, crossfading in from pa (q/256 of the way) when they differ; dec, dk: the decay, damping now */
static inline void rev_tick(int32_t in, uint32_t pa, uint32_t pb, int32_t q, int32_t dec, int32_t dk)
{
    int32_t x, a, b, e1 = (tri_q(rv_ph1) * 5) >> 4, e2 = (tri_q(rv_ph2) * 5) >> 4;   /* +-2.5 samples */
    uint32_t r = sp_w & 7u, w = (sp_w + SP_M) & 7u;
    rv_ph1 += 321391u * REV_DIV;                /* 3.3 Hz and 4.7 Hz: the wire's shimmer */
    rv_ph2 += 457738u * REV_DIV;
    SP_WR(SPO_PRE, 2047u, sat16(in));
    x = SP_RD(SPO_PRE, 2047u, pb - 1u);         /* (pb 1 = no pre-delay) */
    if (pa != pb) { int32_t xa = SP_RD(SPO_PRE, 2047u, pa - 1u); x = xa + (((x - xa) * q) >> 8); }
    rv_lp_in += ((x - rv_lp_in) * RV_BW) >> 15;
    rv_hp += ((((rv_lp_in << 8) - rv_hp) >> 4) * SP_HP_K) >> 11;   /* (the difference to Q4 first: x 704 in int32) */
    x = (rv_lp_in - (rv_hp >> 8)) >> 1;         /* the tank at half level: 6 dB of headroom (a pad held on a 66 ms loop
                                                 * builds its modes up to +3 dBFS at full level: factory 08, 13, 16, 24) */
    x = ap_sat(SPO_IN1, 127u, SP_IN1, x, 19661);   /* 0.6, 0.6, 0.5, 0.5: shallower than the plate's */
    x = ap_sat(SPO_IN2, 127u, SP_IN2, x, 19661);
    x = ap_sat(SPO_IN3, 511u, SP_IN3, x, 16384);
    x = ap_sat(SPO_IN4, 255u, SP_IN4, x, 16384);
    x = sp_chirp(sp_ch[0], x, r, w);
    /* left half, fed by the right's end */
    a = x + SPD(SP_RD(SPO_D4, 511u, SP_D4) * dec);
    a = ap_mod_sat(SPO_AP1, 255u, SP_AP1, e1, a, -16384);
    SP_WR(SPO_D1, 1023u, sp_knee(a));
    b = SP_RD(SPO_D1, 1023u, SP_D1 - 1u);
    rv_lpl += ((b - rv_lpl) * dk + 16384) >> 15;
    SP_WR(SPO_D2, 511u, sat16(sp_chirp(sp_ch[1], SPD(rv_lpl * dec), r, w)));
    /* right half, fed by the left's end */
    a = x + SPD(SP_RD(SPO_D2, 511u, SP_D2 - 1u) * dec);
    a = ap_mod_sat(SPO_AP3, 511u, SP_AP3, e2, a, -16384);
    SP_WR(SPO_D3, 1023u, sp_knee(a));
    b = SP_RD(SPO_D3, 1023u, SP_D3 - 1u);
    rv_lpr += ((b - rv_lpr) * dk + 16384) >> 15;
    SP_WR(SPO_D4, 511u, sat16(sp_chirp(sp_ch[2], SPD(rv_lpr * dec), r, w)));
    /* the output taps (the plate's, scaled to these lines; the long allpasses' went with them): their sum at half
     * level is the wet x 0.5, within ~2 dB of the plate's wet level (bench). Held to 2x full scale */
    a = SP_RD(SPO_D3, 1023u, SPL(53)) + SP_RD(SPO_D3, 1023u, SPL(608)) + SP_RD(SPO_D4, 511u, SPL(212))
      - SP_RD(SPO_D1, 1023u, SPL(355)) - SP_RD(SPO_D2, 511u, SPL(110));
    b = SP_RD(SPO_D1, 1023u, SPL(62)) + SP_RD(SPO_D1, 1023u, SPL(648)) + SP_RD(SPO_D2, 511u, SPL(279))
      - SP_RD(SPO_D3, 1023u, SPL(431)) - SP_RD(SPO_D4, 511u, SPL(12));
    rv_yl = clampi(a, -RV_TAP_MAX, RV_TAP_MAX);
    rv_yr = clampi(b, -RV_TAP_MAX, RV_TAP_MAX);
    sp_w++;
}

/* the reverb's glides: a quarter of the way to the target a block (~23 ms), the last few steps at once */
static inline int32_t rv_glide(int32_t d) { return d > -4 && d < 4 ? d : d >> 2; }
static uint32_t fx_to_tape;                     /* CHEW runs after this block (obv_engine.h sets it): hand it the sum
                                                 * unclipped, on a +-2x full-scale rail, for its own record knee */

static __attribute__((noinline)) void fx_process(int32_t *out, uint32_t n)   /* (inlined, it moved the voice loop: +28 a sample with the effects off) */
{
    uint32_t i, do_dly = dly_active != 0, do_rev = rev_active != 0, pa = rev_pre_old, pb = rev_pre_n;
    int32_t dm = dly_mix, rm = rev_mix, rail = fx_to_tape ? 65534 : 32767;
    int32_t d0 = rv_dec, dd = rv_glide(rev_decay - rv_dec), k0 = rv_dk, kd = rv_glide(rev_damp_k - rv_dk);
    if (!do_dly && !do_rev) {                   /* both resting: only the clip (sat16; the rail while CHEW runs) */
        if (!fx_to_tape) for (i = 0; i < 2u * n; i++) out[i] = sat16(out[i]);
        return;                                 /* (CHEW on: the output stage's levels pass as they are) */
    }
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
        if (do_rev) {                           /* DRAIN: the decay and damping glide per sample, a pre-delay change
                                                 * crossfades the two reads over the block (256 frames) */
            int32_t q = (int32_t)i + 1, dec = d0 + ((dd * q) >> 8), dk = k0 + ((kd * q) >> 8);
#if REV_DIV == 2u                               /* half rate: a pair in, the output interpolated between ticks */
            int32_t pl = rv_yl, pr = rv_yr, din = l + r;
            if (!(fx_odd ^= 1u)) {
                rev_tick((rv_hold + din) >> 2, pa, pb, q, dec, dk);
                l += (((pl + rv_yl) >> 1) * rm) >> 8;
                r += (((pr + rv_yr) >> 1) * rm) >> 8;
            } else {
                l += (rv_yl * rm) >> 8;
                r += (rv_yr * rm) >> 8;
            }
            rv_hold = din;
#else
            rev_tick((l + r) >> 1, pa, pb, q, dec, dk);
            l += (rv_yl * rm) >> 8;
            r += (rv_yr * rm) >> 8;
#endif
        }
        out[2u * i] = clampi(l, -rail, rail);   /* (CHEW off: sat16, as always) */
        out[2u * i + 1u] = clampi(r, -rail, rail);
    }
    if (do_rev) { rv_dec = d0 + ((dd * (int32_t)n) >> 8); rv_dk = k0 + ((kd * (int32_t)n) >> 8); rev_pre_old = pb; }
}
