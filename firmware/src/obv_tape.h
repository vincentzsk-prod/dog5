/* SPDX-License-Identifier: GPL-3.0-only */
/* TAPE, the CHEW macro: stage 4 of the Psych Chain (CLAUDE.md section 6). For now it is the last thing before the
 * output, after the delay and the reverb (obv_engine.h; the final chain order waits for the BBD and Spring re-voice).
 * Integers only. One transport for both channels (the wow and the dropouts are the same on L and R, as on one strip
 * of tape); the hiss is two independent noises (tape hiss is wide). Per channel:
 *
 *   in (Q15, as the effects leave it) -> 2x up (Drive's halfband) -> record: the tanh table at 1.5, blended in by CHEW
 *   (a touch of saturation, Drive's curve) -> the tape line (int16, 88.2 kHz) -> play: a 6-point polynomial read at a
 *   moving delay (the wow and the flutter) -> 2x down -> head bump (~+2 dB near 100 Hz) -> head loss (two one-poles,
 *   7.5 kHz each at the top; a dropout closes it further) -> + hiss -> dropout gain -> makeup.
 *
 * The read and the saturation run at 2x: a moving read wobbles the interpolator's response at the rate its fraction
 * turns (hundreds of Hz under wow), which puts sidebands around every partial. A 4-point Hermite at 44.1 kHz leaves
 * them at -30 dB under a 10 kHz tone, at 2x -43 dB; the 6-point read fitted for 2x below, -80 dB (tests/tape).
 *
 * CHEW turns everything at once, in this order along the knob: wow from the start (a^1.4, 1.4 % peak pitch at 127),
 * flutter from 20 %, dropouts from 45 %; the saturation, the head loss, the bump and the hiss rise all the way. The
 * secondaries (SELECT held, TAPE +) shape it: WOW/FLT (0 wow only .. 64 both .. 127 flutter only), HISS (0 off,
 * else -12 .. +12 dB around the macro's own level), DROPS (0 none, 64 the macro's own, 127 three times as many).
 *
 * The head sits TP_D0 behind the record point (3.6 ms of latency while CHEW is on) and the wow swings around it, so a
 * turn of CHEW never bends the pitch: the depth of the wobble follows the knob at a limited rate (~3 s for the whole
 * range; 0.1 % of pitch at most, under any ear's threshold). Leaving 0 the head moves from 3 samples back to TP_D0
 * (the tape spins up: 0.25 % flat for ~1.4 s), coming back to 0 it returns first, then a 256-frame crossfade to the
 * dry signal; CHEW 0 is a bit-exact bypass (the engine skips it). The hiss rests 2 s after the input falls silent
 * (it fades over ~0.7 s and comes back with the next note): a live rig, not a running deck.
 * Patch bytes 64-67 (CC 83-86): P_CHEW, P_TP_WOWFLT, P_TP_HISS, P_TP_DROPS. tests/tape has the measurements. */

#define TP_N 1024u                              /* a channel's line at 88.2 kHz: 11.6 ms (the head at most 6.5) */
#define TP_M (TP_N - 1u)
#define TP_D0 (320 << 16)                       /* the head, Q16 samples at 2x: 3.6 ms */
#define TP_DMIN (3 << 16)                       /* the head at CHEW 0 (the read's 6 points need 2 behind it) */
#define TP_DSLEW 5243                           /* how far the head may move in a block (32 samples at 2x), Q16:
                                                 * 0.08 samples, 0.25 % of pitch */
#define TP_ASLEW 8                              /* how far the wow / flutter depth may move in a block, Q8: 0.03
                                                 * samples, 0.1 % of pitch at most (the wobble is +-1) */
#define TP_HOLD (2u * FS / 16u)                 /* the hiss's rest: 2 s of silence (in 16-frame blocks) */

static int16_t tp_line[2u * TP_N] __attribute__((section(".pool")));   /* L R L R ..: one index for both */
typedef struct {
    int32_t u1x[4], u1y[4], d1x[4], d1y[4];     /* the halfbands (Drive's 4-coefficient pair) */
    int32_t ba, bb, h1, h2, n1, n2;             /* head bump, head loss, the hiss's two filters */
    uint32_t nz;                                /* the hiss's noise */
} tp_ch_t;
static tp_ch_t tp_ch[2];
static uint32_t tp_on, tp_run, tp_w;            /* CHEW > 0; the stage runs; where the line writes next */
static int32_t tp_mix;                          /* 0 .. 16384: the bypass crossfade */
static uint32_t tp_ph1, tp_ph2, tp_ph3, tp_rs, tp_slow_n;   /* the wow and flutter phases, the random, the slow clock */
static int32_t tp_rj, tp_rj_d, tp_ra, tp_ra_d, tp_fna, tp_fnb;   /* slow randoms (value Q15 << 10, step), flutter noise */
static int32_t tp_aw, tp_aw_t, tp_af, tp_af_t;  /* the wow / flutter depth, Q8 samples at 2x */
static int32_t tp_dc, tp_d;                     /* the head's centre, the read delay now (Q16 samples at 2x) */
static int32_t tp_s, tp_s_t, tp_k, tp_k_t, tp_b, tp_b_t, tp_hg, tp_hg_t, tp_mk, tp_mk_t;   /* the sound's numbers */
static int32_t tp_dg, tp_dg20, tp_dg_t, tp_dp, tp_dd;   /* the dropout gain Q12 (Q20 state, target Q12), its chance a
                                                 * block Q24, its depth Q12 */
static uint32_t tp_dlen, tp_hold;               /* the dropout's blocks left; the hiss's rest */
static int32_t tp_gate;                         /* the hiss gate, Q15 */
static int32_t tp_trim, tp_dtr, tp_tw, tp_pin, tp_pout;   /* the slow trim Q12 (as GROWL's), its step, its range 0..256,
                                                 * the slow powers in / out as the ear weights them */
static grl_kw_t tp_kw_in, tp_kw_out;

/* the patch's numbers, once per ISR call */
static void tape_block(const patch_t *p)
{
    uint32_t v = p->v[P_CHEW] & 127u, b = p->v[P_TP_WOWFLT] & 127u, h = p->v[P_TP_HISS] & 127u, d = p->v[P_TP_DROPS] & 127u;
    int32_t ws = b <= 64u ? 4096 : (int32_t)(127u - b) * 4096 / 63, fs = b >= 64u ? 4096 : (int32_t)b * 64;
    int32_t ds = d < 64u ? (int32_t)d * 64 : 4096 + (int32_t)(d - 64u) * 8192 / 63, r = TP_DRAMP_Q12[v];
    tp_on = v != 0;
    if (!v) {                                   /* leaving: everything back to the identity, the head returns */
        tp_aw_t = tp_af_t = 0; tp_s_t = 0; tp_k_t = 16384; tp_b_t = 0; tp_hg_t = 0; tp_mk_t = 4096; tp_dp = 0; tp_tw = 0;
        return;
    }
    tp_aw_t = (int32_t)(((uint32_t)TP_WOW_Q8[v] * (uint32_t)ws) >> 12);
    tp_af_t = (TP_FLT_Q8[v] * fs) >> 12;
    tp_s_t = TP_SAT_Q12[v];
    tp_k_t = TP_KHL_Q14[v];
    tp_b_t = TP_BUMP_Q12[v];
    tp_hg_t = (TP_HISS_Q20[v] * TP_DB12_Q12[h]) >> 12;
    tp_mk_t = TP_MK_Q12[v];
    tp_tw = (int32_t)v * 2;                     /* the trim's range: none at a gentle CHEW, +-3 dB at the top */
    tp_dp = (((r * r) >> 12) * ds) >> 12;       /* Q12: ramp^2 x DROPS */
    tp_dp = (tp_dp * 8523) >> 12;               /* -> Q24 chance a 16-frame block: 1.4 / s at the top, x3 by DROPS */
    tp_dd = 1434 + ((r * 1843) >> 12);          /* the depth, Q12: 0.35 .. 0.8 of the level (-4 .. -14 dB) */
    if (d > 64u) tp_dd = clampi(tp_dd + (((int32_t)(d - 64u) * 410) >> 6), 0, 3686);   /* deeper too, to 0.9 */
}

static inline uint32_t tape_on(void) { return tp_on || tp_run; }   /* else the engine skips it: bit for bit */

static inline int32_t tp_sin(uint32_t ph)       /* a sine, +-32767: the parabola and one refinement (within 0.1 %; a
                                                 * bare parabola's slope, the pitch, would turn in corners) */
{
    int32_t t = (int32_t)ph >> 16, a = t < 0 ? -t : t, y = clampi((t * (32768 - a)) >> 13, -32767, 32767);
    y += (7373 * (((y * (y < 0 ? -y : y)) >> 15) - y)) >> 15;
    return clampi(y, -32767, 32767);
}

/* the record: Drive's tanh table at 1.5 (tanh(1.5 x) / 1.5: unity for small signals, -4.4 dB at full scale), the
 * share s (Q12) of it blended in */
static inline __attribute__((always_inline)) int32_t tp_sat(int32_t u, int32_t s)
{
    int32_t t = (grl_sat((u * 3) >> 1) * 21845) >> 15;
    return sat16(u + (((t - u) * s) >> 12));
}

/* the play head: a 6-point, 5th-order polynomial fitted for the 2x line (tests/tape/interp_fit.py; Niemitalo's
 * z-form). Its tap weights depend only on the fraction, so they are worked out once a sub-sample for both channels.
 * A 4-point Hermite here left the moving read's sidebands at -43 dB under a 10 kHz tone; this keeps them under -80
 * (-56 at 18 kHz). Q15; DC exact */
static const int32_t TP_IC[18] = {19537, -3748, 595, -13167, 15851, -2684, 2254, -3495, 1241, 39053, -2487, 237, -26237, 10514, -1068, 4440, -2293, 491};
static inline __attribute__((always_inline)) void tp_taps(int32_t dq16, int32_t *h)   /* h[0..5]: y-2 .. y3 */
{
    int32_t z = ((dq16 & 65535) >> 1) - 16384, z2 = (z * z) >> 15, z3 = (z2 * z) >> 15, z4 = (z2 * z2) >> 15, z5 = (z4 * z) >> 15;
    int32_t e1 = TP_IC[0] + ((TP_IC[3] * z2 + TP_IC[6] * z4) >> 15), o1 = (TP_IC[9] * z + TP_IC[12] * z3 + TP_IC[15] * z5) >> 15;
    int32_t e2 = TP_IC[1] + ((TP_IC[4] * z2 + TP_IC[7] * z4) >> 15), o2 = (TP_IC[10] * z + TP_IC[13] * z3 + TP_IC[16] * z5) >> 15;
    int32_t e3 = TP_IC[2] + ((TP_IC[5] * z2 + TP_IC[8] * z4) >> 15), o3 = (TP_IC[11] * z + TP_IC[14] * z3 + TP_IC[17] * z5) >> 15;
    h[0] = e3 - o3; h[1] = e2 - o2; h[2] = e1 - o1; h[3] = e1 + o1; h[4] = e2 + o2; h[5] = e3 + o3;
}
/* the sample D (Q16) behind index i (the newest), both channels: y_k is k samples further back than D's whole part.
 * sum |h| <= 1.46: inside 32 bits for any int16 contents */
static inline __attribute__((always_inline)) void tp_read(uint32_t i, int32_t dq16, const int32_t *h, int32_t *o)
{
    uint32_t n = i - ((uint32_t)dq16 >> 16);
    const int16_t *p0 = tp_line + 2u * ((n + 2u) & TP_M), *p1 = tp_line + 2u * ((n + 1u) & TP_M), *p2 = tp_line + 2u * (n & TP_M);
    const int16_t *p3 = tp_line + 2u * ((n - 1u) & TP_M), *p4 = tp_line + 2u * ((n - 2u) & TP_M), *p5 = tp_line + 2u * ((n - 3u) & TP_M);
    int32_t l = h[0] * p0[0] + h[1] * p1[0] + h[2] * p2[0] + h[3] * p3[0] + h[4] * p4[0] + h[5] * p5[0];
    int32_t r = h[0] * p0[1] + h[1] * p1[1] + h[2] * p2[1] + h[3] * p3[1] + h[4] * p4[1] + h[5] * p5[1];
    o[0] = l >> 15;
    o[1] = r >> 15;
}

static inline uint32_t tp_rand(void) { return xorshift(&tp_rs); }

/* s: the effects' output, Q15 (int16 range), in place */
static __attribute__((noinline)) void tape_process(int32_t *s, uint32_t n)
{
    uint32_t i;
    if (tp_on && !tp_run) {                     /* entering from the bypass: clean states, the identity, head close */
        static const tp_ch_t z0;
        uint32_t k;
        tp_ch[0] = tp_ch[1] = z0;
        tp_ch[0].nz = 0x2545F491u; tp_ch[1].nz = 0x9E3779B9u;
        for (k = 0; k < 2u * TP_N; k++) tp_line[k] = 0;
        tp_run = 1; tp_mix = 0; tp_w = 0;
        tp_dc = tp_d = TP_DMIN; tp_aw = tp_af = 0;
        tp_s = 0; tp_k = 16384; tp_b = 0; tp_hg = 0; tp_mk = 4096; tp_dg = tp_dg_t = 4096; tp_dg20 = 4096 << 8; tp_dlen = 0;
        tp_gate = 0; tp_hold = 0;
        { static const grl_kw_t w0; tp_kw_in = tp_kw_out = w0; }
        tp_trim = 4096; tp_dtr = 0; tp_pin = tp_pout = 0;
        if (!tp_rs) tp_rs = 0x1234567u;
    }
    for (i = 0; i < n; i += 16u) {              /* 16 frames a block: the modulation, the glides, the dropouts */
        uint32_t k, j, pk = 0, ein = 0, eout = 0;
        int32_t w, f, d0 = tp_d, d1, dd, e, tgt, s0 = tp_s, ds, mk0 = tp_mk, dmk, kk, bb, hg, tr0 = tp_trim, dtr = tp_dtr, tt;
        /* the slow randoms: a new target every 1024 blocks (0.37 s), reached in a straight line */
        if (!(tp_slow_n++ & 1023u)) {
            tp_rj_d = (((int32_t)(tp_rand() >> 17) - 16384) * 2048 - tp_rj) >> 10;   /* [-1, 1] Q15 << 10 */
            tp_ra_d = ((9830 + (int32_t)(((tp_rand() >> 17) * 22937u) >> 15)) * 1024 - tp_ra) >> 10;   /* [0.3, 1] */
        }
        tp_rj += tp_rj_d; tp_ra += tp_ra_d;
        /* the wow: 0.7 sin(0.55 Hz) + 0.3 sin(1.37 Hz) x the slow amplitude, the rates +-10 % with the slow random */
        tp_ph1 += 857041u + (uint32_t)((85704 * (tp_rj >> 17)) >> 8);    /* (tp_rj >> 17: Q8) */
        tp_ph2 += 2134811u - (uint32_t)((213481 * (tp_rj >> 17)) >> 8);
        tp_ph3 += 14180130u + (uint32_t)((2127020 * (tp_rj >> 17)) >> 8);   /* the flutter: 9.1 Hz +-15 % */
        w = (tp_sin(tp_ph1) * 22938 + ((tp_sin(tp_ph2) * (tp_ra >> 10)) >> 15) * 9830) >> 15;
        tp_fna += ((((int32_t)tp_rand() >> 16) - tp_fna) * 1461) >> 15;   /* noise, two one-poles at ~20 Hz */
        tp_fnb += ((tp_fna - tp_fnb) * 1461) >> 15;
        f = (tp_sin(tp_ph3) * 21299 + clampi(tp_fnb * 6, -32767, 32767) * 11469) >> 15;
        /* the depths follow the knob at a limited rate; the head's centre: TP_D0 while on, else close behind them */
        tp_aw += clampi(tp_aw_t - tp_aw, -TP_ASLEW, TP_ASLEW);
        tp_af += clampi(tp_af_t - tp_af, -TP_ASLEW, TP_ASLEW);
        tgt = tp_on ? TP_D0 : tp_aw + tp_af ? TP_DMIN + ((tp_aw + tp_af + 1024) << 8) : TP_DMIN;
        if (tgt > TP_D0) tgt = TP_D0;
        tp_dc += clampi(tgt - tp_dc, -TP_DSLEW, TP_DSLEW);
        e = ((tp_aw * w) >> 15) + ((tp_af * f) >> 15);
        d1 = clampi(tp_dc + (e << 8), TP_DMIN, (int32_t)(TP_N - 8u) << 16);
        dd = d1 - d0;
        tp_d = d1;
        /* the sound's numbers glide (1/4 of the way a block, the last bit at once); s and the makeup per sample */
        ds = grl_glide(tp_s_t - tp_s, 2); tp_s += ds;
        dmk = grl_glide(tp_mk_t - tp_mk, 2); tp_mk += dmk;
        tp_k += grl_glide(tp_k_t - tp_k, 2);
        tp_b += grl_glide(tp_b_t - tp_b, 2);
        tp_hg += grl_glide(tp_hg_t - tp_hg, 4);
        /* a dropout: a dip of 4 .. 60 ms, its edges smoothed per sample (~3 ms) */
        if (tp_dlen) { if (!--tp_dlen) tp_dg_t = 4096; }
        else if (tp_dp && (tp_rand() >> 8) < (uint32_t)tp_dp) {
            tp_dlen = 11u + tp_rand() % 150u;
            tp_dg_t = 4096 - ((tp_dd * (int32_t)(2048u + (tp_rand() >> 21))) >> 12);
        }
        /* the input's peak this block (the hiss's rest) */
        for (k = i; k < i + 16u && k < n; k++) {
            int32_t a = s[2u * k], b2 = s[2u * k + 1u];
            uint32_t m = (uint32_t)(a < 0 ? -a : a) | (uint32_t)(b2 < 0 ? -b2 : b2);
            pk |= m;
        }
        if (pk > 24u) tp_hold = TP_HOLD; else if (tp_hold) tp_hold--;
        tp_gate += tp_hold ? (32767 - tp_gate) >> 3 : -(tp_gate >> 11) - (tp_gate > 0);
        hg = (tp_hg * tp_gate) >> 15;
        kk = tp_k; bb = tp_b;
        for (k = i, j = 1; k < i + 16u && k < n; k++, j++) {
            int32_t da = d0 + ((dd * (int32_t)(2u * j - 1u)) >> 5), db = d0 + ((dd * (int32_t)(2u * j)) >> 5);
            int32_t sv = s0 + ((ds * (int32_t)j) >> 4), mk = mk0 + ((dmk * (int32_t)j) >> 4), kd, ha[6], hb[6];
            int32_t tr = tr0 + ((dtr * (int32_t)j) >> 4), yd[2], xs = s[2u * k] + s[2u * k + 1u], r0[2], r1[2];
            uint32_t c;
            tp_taps(da, ha);                    /* (the same fraction for both channels) */
            tp_taps(db, hb);
            tp_dg20 += (((tp_dg_t << 8) - tp_dg20) * 250) >> 15;
            tp_dg = tp_dg20 >> 8;
            kd = (kk * tp_dg) >> 12;            /* a dropout closes the head loss too (it dulls, as it dips) */
            for (c = 0; c < 2u; c++) {          /* 2x up and record, both channels (the line is L R L R ..) */
                tp_ch_t *ch = &tp_ch[c];
                int32_t u0 = s[2u * k + c], u1 = u0;
                GRL_AP(u0, ch->u1x, ch->u1y, 0, 346); GRL_AP(u1, ch->u1x, ch->u1y, 1, 1214);
                GRL_AP(u0, ch->u1x, ch->u1y, 2, 2295); GRL_AP(u1, ch->u1x, ch->u1y, 3, 3449);
                tp_line[2u * (tp_w & TP_M) + c] = (int16_t)tp_sat(u0, sv);
                tp_line[2u * ((tp_w + 1u) & TP_M) + c] = (int16_t)tp_sat(u1, sv);
            }
            tp_read(tp_w, da, ha, r0);          /* play: both channels at once */
            tp_read(tp_w + 1u, db, hb, r1);
            for (c = 0; c < 2u; c++) {
                tp_ch_t *ch = &tp_ch[c];
                int32_t x = s[2u * k + c], y, z;
                {                               /* 2x down */
                    int32_t ev = r1[c], od = r0[c];
                    GRL_AP(ev, ch->d1x, ch->d1y, 0, 346); GRL_AP(od, ch->d1x, ch->d1y, 1, 1214);
                    GRL_AP(ev, ch->d1x, ch->d1y, 2, 2295); GRL_AP(od, ch->d1x, ch->d1y, 3, 3449);
                    y = (ev + od) >> 1;
                }
                ch->ba += (((y << 4) - ch->ba) * 912) >> 15;   /* the head bump: 200 Hz minus 60 Hz one-poles */
                ch->bb += (((y << 4) - ch->bb) * 279) >> 15;
                y = clampi(y + ((((ch->ba - ch->bb) >> 4) * bb) >> 12), -65535, 65535);
                ch->h1 += ((y - ch->h1) * kk) >> 14;    /* the head loss */
                ch->h2 += ((ch->h1 - ch->h2) * kd) >> 14;
                z = (int32_t)xorshift(&ch->nz) >> 16;   /* the hiss: 400 Hz high-pass, 7 kHz low-pass */
                ch->n1 += ((z - ch->n1) * 1816) >> 15;
                ch->n2 += (((z - ch->n1) - ch->n2) * 20680) >> 15;
                y = (ch->h2 * mk) >> 12;        /* the static makeup (the detector hears it, not the hiss or a dip) */
                yd[c] = y;
                y = (y * tr) >> 12;             /* the slow trim */
                y = y + (((ch->n2 >> 1) * hg) >> 19);   /* + hiss */
                y = (y * tp_dg) >> 12;          /* a dropout dips the lot */
                if (tp_mix < 16384 || !tp_on) y = x + (((y - x) * tp_mix) >> 14);
                s[2u * k + c] = sat16(y);
            }
            {                                   /* the powers as heard (K-weighted, mono): in, and out before the hiss */
                int32_t q = grl_kweight(&tp_kw_in, xs >> 4);   /* (|xs| <= 65534) */
                ein += (uint32_t)(q * q);
                q = grl_kweight(&tp_kw_out, clampi((yd[0] + yd[1]) >> 4, -4095, 4095));
                eout += (uint32_t)(q * q);
            }
            if (tp_mix < 16384 || !tp_on) {     /* the crossfade in or out of the bypass (out: once the head is back) */
                if (tp_on) tp_mix = tp_mix + 64 > 16384 ? 16384 : tp_mix + 64;
                else if (tp_dc <= TP_DMIN + (1 << 16) && !tp_aw && !tp_af) tp_mix = tp_mix > 64 ? tp_mix - 64 : 0;
            }
            tp_w += 2u;
        }
        tp_trim = tr0 + dtr;                    /* the trim, as GROWL's: ~1.5 s, a step glides over ~23 ms */
        tp_pin += ((int32_t)ein - tp_pin) >> 12;
        tp_pout += ((int32_t)eout - tp_pout) >> 12;
        tt = tp_pin > 64 && tp_pout > 64 ? grl_trim_for((uint32_t)tp_pin, (uint32_t)tp_pout) : tp_trim;
        tt = clampi(tt, 4096 - ((1196 * tp_tw) >> 8), 4096 + ((1690 * tp_tw) >> 8));   /* -3 .. +3 dB at most */
        tp_dtr = grl_glide(tt - tp_trim, 6);
        if (!tp_on && !tp_mix) tp_run = 0;      /* back to the bypass: the engine skips it again */
    }
}
