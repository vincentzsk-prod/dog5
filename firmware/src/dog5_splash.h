/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Vincent Kruger (DØG-5) */
/* The boot animation (Batch 21): Vincent's launch screen as approved (the claude.ai artifact "DØG-5 launch screen", 19 Nov
 * 2026, its last version), drawn on the 240 x 240 panel. The page was made at 400 x 400; here everything is x 3/5.
 *
 *     0 ..  500 ms   the favicon, its white areas plain white
 *   500 .. 3540      its white areas run the 16-colour cycle twice (32 steps of 95 ms, smooth)
 *  3540 .. 5060      the favicon fades out (400 ms) as DØG-5 in Yatra One fades in, the cycle running on its letters (16 steps)
 *  5060 .. 5510      the melt: the letters sag and stretch down, column by column, turning acid green
 *  5510 .. 5960      the burn: a green fire front eats up the screen, embers rise, and the chapter's scene fades up
 *                    under it: HOME as it will be drawn (the page revealed a blank white placeholder here; the scene
 *                    now exists, so the burn reveals it)
 * Behind the favicon and the word: a static near-black grain; a halo of the cycle's colour (53 %) that breathes with it; a
 * zig-zag "scope" seal around the edge (78 %), 8 steps out of phase with the letters, wobbling. Halo and seal fade out
 * through the melt.
 *
 * Changes from the page, all deliberate: the acid green of the melt and the fire is the brand's Acid Chartreuse (#DEF402;
 * the page had #39FF14, the retired Chapter I accent) and the fire's white-hot core is Sun Glow; the page's random embers
 * and flickering edge come from a fixed pseudo-random sequence (the same every boot); a key or a button pressed during
 * the animation ends it at once (a live instrument: you never wait to play). The timing is the page's, by the clock, so
 * the device's frame rate (a full screen takes ~77 ms on the SPI link: about 8-10 frames a second) only changes how many
 * frames are seen, never how long it lasts.
 *
 * It draws the whole screen each frame in the strip canvas (gfx.c cv_px: two strips of 120 rows), polling the
 * platform between strips (USB, the watchdog, an installer's request). It runs before the main loop: no notes are
 * played yet, so it has no app_idle() to call. */
#include "dog5_splash_art.h"

#define SPL_HOLD 500u
#define SPL_STEP 95u                            /* ms a colour step (the page's speed) */
#define SPL_T_TITLE (SPL_HOLD + 32u * SPL_STEP) /* 3540: the favicon has cycled twice */
#define SPL_T_MELT (SPL_T_TITLE + 16u * SPL_STEP)   /* 5060 */
#define SPL_T_BURN (SPL_T_MELT + 450u)          /* 5510 */
#define SPL_T_END (SPL_T_BURN + 450u)           /* 5960 */
#define SPL_XFADE 400u                          /* the favicon -> word cross-fade */
#define SPL_FRAME_MS 40u                        /* at most 25 frames a second (the device makes ~10) */
#define SPL_EMBERS 48u

static uint8_t spl_mask[CV_MAX / 8u] __attribute__((section(".pool")));   /* the seal's pixels in this strip */
static struct { int16_t x, y, vy, life; } spl_em[SPL_EMBERS];   /* y, vy in 1/16 px (vy per second); life 0..1000 */
static uint32_t spl_rnd = 0x5EED1E55u, spl_em_n, spl_em_t;

static uint32_t spl_rand(void) { spl_rnd = spl_rnd * 1664525u + 1013904223u; return spl_rnd >> 8; }
static uint32_t spl_hash(uint32_t a)
{
    a ^= a >> 16; a *= 0x7FEB352Du; a ^= a >> 15; a *= 0x846CA68Bu; a ^= a >> 16;
    return a;
}
static uint32_t spl_ease(uint32_t t)            /* smoothstep, t and the result 0..256 */
{
    if (t >= 256u) return 256u;
    return t * t * (768u - 2u * t) >> 16;
}
static inline uint32_t unpack_r(uint32_t c) { return (c >> 11) * 255u / 31u; }
static inline uint32_t unpack_g(uint32_t c) { return ((c >> 5) & 63u) * 255u / 63u; }
static inline uint32_t unpack_b(uint32_t c) { return (c & 31u) * 255u / 31u; }
static inline uint16_t pack565(uint32_t r, uint32_t g, uint32_t b)
{
    return swap16(((r > 255u ? 255u : r) >> 3) << 11 | ((g > 255u ? 255u : g) >> 2) << 5 | (b > 255u ? 255u : b) >> 3);
}
static inline uint32_t lerp8(uint32_t a, uint32_t b, uint32_t t) { return (a * (256u - t) + b * t) >> 8; }   /* t 0..256 */

/* the cycle's colour at step p (Q8 steps), smooth: between two ramp colours */
static void spl_ramp(uint32_t p8, uint32_t *rgb)
{
    uint32_t i = (p8 >> 8) & 15u, j = (i + 1u) & 15u, f = p8 & 255u, k;
    for (k = 0; k < 3u; k++) rgb[k] = lerp8(SPL_RAMP[i * 3u + k], SPL_RAMP[j * 3u + k], f);
}

/* the grain: one cell in 3 x 3 of a quarter has a dot (the page's density, at its x 3/5); 14 % of the dots brighter */
static inline uint32_t spl_grain(int32_t x, int32_t y)
{
    uint32_t cx = (uint32_t)x / 3u, cy = (uint32_t)y / 3u, h = spl_hash(cx * 73856093u ^ cy * 19349663u ^ 0xD06u);
    if ((h & 0xFFFFu) >= 16384u) return 0;
    if ((uint32_t)x != cx * 3u + (h >> 16) % 3u || (uint32_t)y != cy * 3u + (h >> 20) % 3u) return 0;
    return (h & 0xFFFFu) < 2294u ? 70u : 48u;
}

static inline uint32_t spl_nib(const uint8_t *a, uint32_t w, uint32_t x, uint32_t y)   /* a 4-bit coverage, 0..15 (rows
                                                                                          start on a byte) */
{
    uint8_t v = a[y * ((w + 1u) >> 1) + (x >> 1)];
    return x & 1u ? v & 15u : (uint32_t)v >> 4;
}

/* one frame's state */
typedef struct {
    uint32_t stop[7][3];                        /* the gradient's seven stops (the page: 6 bands, 7 colour stops) */
    uint32_t halo[3], seal[3];
    uint32_t bg;                                /* halo and seal strength, 0..256 (fade through the melt) */
    uint32_t logo, word;                        /* the favicon's and the word's opacity, 0..256 */
    uint32_t white;                             /* the hold: the favicon plain white */
    uint32_t melt, burn;                        /* 0..256 each (eased inside) */
    uint32_t chapter;
    uint32_t t;                                 /* ms since the start */
} spl_frame_t;

/* the gradient's colour at u (Q16 of the 0..6 stop axis) */
static void spl_grad(const spl_frame_t *F, int32_t u, uint32_t *rgb)
{
    int32_t k;
    uint32_t f, c;
    if (u < 0) u = 0;
    if (u > (6 << 16) - 1) u = (6 << 16) - 1;
    k = u >> 16;
    f = (uint32_t)(u & 0xFFFF) >> 8;
    for (c = 0; c < 3u; c++) rgb[c] = lerp8(F->stop[k][c], F->stop[k + 1][c], f);
}

/* the CSS linear-gradient(165deg) over a box: u = 6 * (0.5 + ((x - cx) sin a - (y - cy) cos a) / L), L = w sin a + h |cos a|,
 * as Q16 of the 0..6 stop axis. Per box, two steps per doubled pixel (Q4), worked out once: 32-bit only */
#define SIN165_Q16 16962                        /* sin 165 = 0.2588 */
#define COS165_Q16 63303                        /* -cos 165 = 0.9659 */
typedef struct { int32_t kx, ky; } spl_box_t;
static spl_box_t spl_box(int32_t w, int32_t h)
{
    spl_box_t b;
    int32_t L8 = (w * SIN165_Q16 + h * COS165_Q16) >> 8;          /* L in Q8 */
    b.kx = 3 * SIN165_Q16 * 4096 / L8;          /* 6 sin a / L / 2 (doubled pixels), Q16 of u, Q4 */
    b.ky = 3 * COS165_Q16 * 4096 / L8;
    return b;
}
static spl_box_t spl_fav_box, spl_word_box;   /* the favicon's (the screen) and the word's gradient boxes */
static inline int32_t spl_u(const spl_box_t *b, int32_t x2, int32_t y2)   /* x2, y2: doubled, from the box centre */
{
    return 3 * 65536 + ((x2 * b->kx + y2 * b->ky) >> 4);
}

/* the seal's vertices around the edge, for time t: x, y in pixels */
static uint32_t spl_seal_pts(uint32_t t, int16_t *px, int16_t *py)
{
    const int32_t a = SPL_SEAL_PAD, bb = 240 - SPL_SEAL_PAD;
    uint32_t n = 0, g = 0, side;
    px[n] = (int16_t)a; py[n++] = (int16_t)a;
    for (side = 0; side < 4u; side++) {
        int32_t s;
        for (s = a + SPL_SEAL_STEP; s < bb; s += SPL_SEAL_STEP) {
            /* the page: sign from g before the step, size from g after; size = 6.6 px * seal[g] * (0.68 + 0.32 sin(t 0.003 + g' 0.9)) */
            int32_t sg = (g & 1u) ? 1 : -1, deg, sn, m;
            uint32_t g1 = g + 1u;
            deg = (int32_t)((t * 1719u / 10000u + g1 * 5157u / 100u) % 360u);
            sn = COS_Q8[(uint32_t)((deg + 270) % 360) / 5u];      /* sin d = cos (d - 90) */
            m = (1690 * (int32_t)SPL_SEAL[g] >> 8) * (174 + (82 * sn >> 8)) >> 8;   /* Q8 pixels */
            m = (m + 128) >> 8;
            g = g1;
            if (side == 0) { px[n] = (int16_t)s; py[n] = (int16_t)(a + sg * m); }
            else if (side == 1) { px[n] = (int16_t)(bb - sg * m); py[n] = (int16_t)s; }
            else if (side == 2) { px[n] = (int16_t)(240 - s); py[n] = (int16_t)(bb - sg * m); }
            else { px[n] = (int16_t)(a + sg * m); py[n] = (int16_t)(240 - s); }
            n++;
        }
        px[n] = (int16_t)(side == 0 || side == 1 ? bb : a);
        py[n] = (int16_t)(side == 0 ? a : side == 3 ? a : bb);
        n++;
    }
    return n;
}

static void spl_mask_line(int32_t x0, int32_t y0, int32_t x1, int32_t y1, int32_t sy, int32_t h)
{
    int32_t dx = x1 > x0 ? x1 - x0 : x0 - x1, sx = x0 < x1 ? 1 : -1;
    int32_t dy = y1 > y0 ? y0 - y1 : y1 - y0, sy2 = y0 < y1 ? 1 : -1, err = dx + dy, guard = 1000;
    while (guard--) {
        int32_t e2 = 2 * err, k;
        for (k = 0; k < 3; k++) {               /* 2 px wide (the page's 3 px x 3/5): the pixel, right and below */
            int32_t x = x0 + (k == 1), y = y0 + (k == 2) - sy;
            if ((uint32_t)x < 240u && (uint32_t)y < (uint32_t)h) spl_mask[((uint32_t)y * 240u + (uint32_t)x) >> 3] |= (uint8_t)(1u << (x & 7));
        }
        if (x0 == x1 && y0 == y1) break;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy2; }
    }
}

/* the melt's column c: its drop (px) and stretch (Q8) at melt m (0..256 eased) */
static void spl_column(uint32_t c, uint32_t m, int32_t *drop, int32_t *st)
{
    uint32_t n = spl_hash(c * 2654435761u + 77u) & 255u;      /* the page's per-column noise, 0..255 */
    *drop = (int32_t)(m * 173u * (82u + 174u * n / 255u) >> 16);   /* ease(m) * 173 (0.72 * 240) * (0.32 + 0.68 n) */
    *st = 256 + (int32_t)(m * 384u * (64u + 192u * n / 255u) >> 16);   /* 1 + ease(m) * 1.5 * (0.25 + 0.75 n), Q8 */
}

/* a strip: rows y0 .. y0 + h of the screen */
static void spl_strip(const spl_frame_t *F, int32_t y0, int32_t h, const int16_t *spx, const int16_t *spy, uint32_t sn)
{
    int32_t x, y, burn_y = 0;
    uint32_t i, hk = 75u * F->bg >> 8;          /* the halo: 0.55 * 53 % = 0.29 of its colour at the centre */
    uint32_t seal_a = 190u * F->bg >> 8;        /* the seal: 0.95 * 78 % */
    uint32_t mm = spl_ease(F->melt), bb = spl_ease(F->burn), gm = 205u * F->melt >> 8;   /* green over the letters: 0.8 m */
    cv_w = 240; cv_h = (uint32_t)h;
    lcd_sync();
    if (F->burn) burn_y = 230 - (int32_t)(bb * 245u >> 8);   /* the page: 0.96 S - ease(b) (0.96 S + 24), x 3/5 */
    if (seal_a) {                               /* the seal's pixels in this strip */
        for (i = 0; i < 240u * (uint32_t)h / 8u; i++) spl_mask[i] = 0;
        for (i = 1; i < sn; i++) {
            int32_t ya = spy[i - 1u], yb = spy[i];
            if ((ya < y0 - 2 && yb < y0 - 2) || (ya > y0 + h + 1 && yb > y0 + h + 1)) continue;
            spl_mask_line(spx[i - 1u], ya, spx[i], yb, y0, h);
        }
    }
    for (y = 0; y < h; y++) {
        int32_t Y = y0 + y, dy = Y - 120;
        uint16_t *o = cv_px + (uint32_t)y * 240u;
        for (x = 0; x < 240; x++) {
            uint32_t g = spl_grain(x, Y), r = g, gg = g, b = g, c[3];
            if (F->burn) {                      /* the reveal: the scene fades up over the grain */
                uint32_t s = swap16(sc_px_rest(F->chapter, x, Y));
                r = lerp8(r, unpack_r(s), bb); gg = lerp8(gg, unpack_g(s), bb); b = lerp8(b, unpack_b(s), bb);
            }
            if (hk) {                           /* the halo, added (the page's "lighter") */
                int32_t dx = x - 120;
                uint32_t d2 = (uint32_t)(dx * dx + dy * dy) >> 6, w = d2 < SPL_HALO_N ? SPL_HALO[d2] : 0u;
                uint32_t k = w * hk;
                r += F->halo[0] * k >> 16; gg += F->halo[1] * k >> 16; b += F->halo[2] * k >> 16;
            }
            if (seal_a && (spl_mask[((uint32_t)y * 240u + (uint32_t)x) >> 3] >> (x & 7) & 1u)) {
                r = lerp8(r > 255u ? 255u : r, F->seal[0], seal_a);
                gg = lerp8(gg > 255u ? 255u : gg, F->seal[1], seal_a);
                b = lerp8(b > 255u ? 255u : b, F->seal[2], seal_a);
            }
            if (F->logo) {                      /* the favicon (the whole screen is its box) */
                uint32_t cov = spl_nib(SPL_FAV, 240u, (uint32_t)x, (uint32_t)Y);
                if (cov) {
                    uint32_t a = cov * F->logo / 15u;
                    if (F->white) c[0] = c[1] = c[2] = 255u;
                    else spl_grad(F, spl_u(&spl_fav_box, 2 * x + 1 - 240, 2 * Y + 1 - 240), c);
                    r = lerp8(r > 255u ? 255u : r, c[0], a); gg = lerp8(gg > 255u ? 255u : gg, c[1], a); b = lerp8(b > 255u ? 255u : b, c[2], a);
                }
            }
            if (F->word || F->melt) {           /* the word, or its melt */
                int32_t cx = x - SPL_WORD_X, sy = Y - SPL_WORD_Y;
                if (cx >= 0 && cx < SPL_WORD_W) {
                    if (F->melt) {
                        int32_t drop, st;
                        spl_column((uint32_t)cx, mm, &drop, &st);
                        sy = (Y - SPL_WORD_Y - drop) * 256 / st;
                        if (Y - SPL_WORD_Y - drop < 0) sy = -1;
                        if (F->burn && Y >= burn_y) sy = -1;   /* below the fire front the letters are gone */
                    }
                    if (sy >= 0 && sy < SPL_WORD_H) {
                        uint32_t cov = spl_nib(SPL_WORD, SPL_WORD_W, (uint32_t)cx, (uint32_t)sy);
                        if (cov) {
                            uint32_t a = cov * (F->melt ? 256u : F->word) / 15u;
                            spl_grad(F, spl_u(&spl_word_box, 2 * cx + 1 - SPL_WORD_W, 2 * sy + 1 - SPL_WORD_H), c);
                            if (gm) {
                                c[0] = lerp8(c[0], 0xDEu, gm); c[1] = lerp8(c[1], 0xF4u, gm); c[2] = lerp8(c[2], 0x02u, gm);
                            }
                            r = lerp8(r > 255u ? 255u : r, c[0], a); gg = lerp8(gg > 255u ? 255u : gg, c[1], a); b = lerp8(b > 255u ? 255u : b, c[2], a);
                        }
                    }
                }
            }
            if (F->burn) {                      /* the fire front: a jagged band, Acid Chartreuse with a Sun Glow core */
                uint32_t col = (uint32_t)x * 10u / 36u;   /* the page's 6 px steps (3.6 px here), joined by straight lines */
                int32_t j0 = (int32_t)(spl_hash(col * 7919u + F->t * 104729u) % 17u) - 8, j1 = (int32_t)(spl_hash((col + 1u) * 7919u + F->t * 104729u) % 17u) - 8;
                int32_t fx = (int32_t)(x * 10 % 36), top = burn_y + (j0 * (36 - fx) + j1 * fx) / 36 / 2;
                if (Y >= top && Y < burn_y + 16) {
                    int32_t q = (Y - (burn_y - 6)) * 256 / 19;   /* the band's gradient: -6 .. +13 px around the front */
                    uint32_t ac, cr, cg, cb;
                    if (q < 128) { ac = (uint32_t)(q < 0 ? 0 : q) * 218u / 128u; cr = 0xDE; cg = 0xF4; cb = 0x02; }
                    else if (q < 184) { uint32_t f = (uint32_t)(q - 128) * 256u / 56u; ac = 218u + 13u * f / 256u;
                        cr = lerp8(0xDE, 0xFF, f); cg = lerp8(0xF4, 0xFF, f); cb = lerp8(0x02, 0x93, f); }
                    else { uint32_t f = (uint32_t)(q > 256 ? 256 : q - 184) * 256u / 72u; ac = 231u * (256u - (f > 256u ? 256u : f)) / 256u;
                        cr = 0xFF; cg = 0xFF; cb = 0x93; }
                    r = lerp8(r > 255u ? 255u : r, cr, ac); gg = lerp8(gg > 255u ? 255u : gg, cg, ac); b = lerp8(b > 255u ? 255u : b, cb, ac);
                }
            }
            o[x] = pack565(r, gg, b);
        }
    }
    if (F->burn)                                /* the embers, rising from the front */
        for (i = 0; i < spl_em_n; i++) {
            int32_t ey = spl_em[i].y >> 4;
            if (spl_em[i].life > 0 && ey >= y0 && ey < y0 + h && (uint32_t)spl_em[i].x < 240u) {
                uint16_t *p = cv_px + (uint32_t)(ey - y0) * 240u + (uint32_t)spl_em[i].x;
                uint32_t s = swap16(*p), a = (uint32_t)spl_em[i].life * 256u / 1000u;
                *p = pack565(lerp8(unpack_r(s), 0xDE, a), lerp8(unpack_g(s), 0xF4, a), lerp8(unpack_b(s), 0x02, a));
            }
        }
    cv_blit(0, (uint32_t)y0);
}

static void spl_embers(uint32_t t, int32_t burn_y)   /* the page: ~160 a second at its size; here 100, rising 14..61 px/s */
{
    uint32_t i, dt = t - spl_em_t;
    spl_em_t = t;
    for (i = 0; i < spl_em_n; i++)
        if (spl_em[i].life > 0) {
            spl_em[i].y = (int16_t)(spl_em[i].y + spl_em[i].vy * (int32_t)dt / 1000);
            spl_em[i].life = (int16_t)(spl_em[i].life - (int32_t)(720u * dt / 1000u));
            spl_em[i].x = (int16_t)(spl_em[i].x + (int32_t)(spl_rand() % 3u) - 1);
        }
    for (i = dt / 10u; i && spl_em_n < SPL_EMBERS; i--) {
        spl_em[spl_em_n].x = (int16_t)(spl_rand() % 240u);
        spl_em[spl_em_n].y = (int16_t)(burn_y * 16);
        spl_em[spl_em_n].vy = (int16_t)(-(int32_t)(224u + spl_rand() % 752u));   /* -14 .. -61 px/s, in 1/16 px */
        spl_em[spl_em_n].life = 1000;
        spl_em_n++;
    }
}

/* the frame at time t (ms since the start) */
static void spl_draw(uint32_t t, uint32_t chapter)
{
    static spl_frame_t F;
    static int16_t spx[SPL_SEAL_N + 8], spy[SPL_SEAL_N + 8];
    uint32_t k, off8 = 0, sn;
    F.t = t; F.chapter = chapter;
    if (t >= SPL_HOLD) off8 = (t - SPL_HOLD) * 256u / SPL_STEP;   /* the cycle's position, Q8 steps */
    for (k = 0; k < 7u; k++) spl_ramp(off8 + k * 256u, F.stop[k]);
    for (k = 0; k < 3u; k++) {                  /* halo and seal take whole steps (as the page), the seal 8 out of phase */
        F.halo[k] = SPL_RAMP[((off8 >> 8) & 15u) * 3u + k];
        F.seal[k] = SPL_RAMP[(((off8 >> 8) + 8u) & 15u) * 3u + k];
    }
    F.white = t < SPL_HOLD;
    F.logo = t < SPL_T_TITLE ? 256u : t < SPL_T_TITLE + SPL_XFADE ? 256u - spl_ease((t - SPL_T_TITLE) * 256u / SPL_XFADE) : 0u;
    F.word = t < SPL_T_TITLE ? 0u : t < SPL_T_TITLE + SPL_XFADE ? spl_ease((t - SPL_T_TITLE) * 256u / SPL_XFADE) : 256u;
    F.melt = t < SPL_T_MELT ? 0u : t < SPL_T_BURN ? (t - SPL_T_MELT) * 256u / (SPL_T_BURN - SPL_T_MELT) : 256u;
    F.burn = t < SPL_T_BURN ? 0u : t < SPL_T_END ? (t - SPL_T_BURN) * 256u / (SPL_T_END - SPL_T_BURN) : 256u;
    if (F.melt) {                               /* the melt: the word's colours stay as they were when it began */
        F.word = 0;
        off8 = (SPL_T_MELT - SPL_HOLD) * 256u / SPL_STEP;
        for (k = 0; k < 7u; k++) spl_ramp(off8 + k * 256u, F.stop[k]);
    }
    F.bg = t < SPL_T_MELT ? 256u : t < SPL_T_BURN ? 256u - spl_ease(F.melt) : 0u;
    sn = F.bg ? spl_seal_pts(t, spx, spy) : 0u;
    if (F.burn) spl_embers(t, 230 - (int32_t)(spl_ease(F.burn) * 245u >> 8));
    spl_strip(&F, 0, 120, spx, spy, sn);
    platform_poll();
    spl_strip(&F, 120, 120, spx, spy, sn);
    platform_poll();
}

/* the boot animation; returns when it is over or a key or button is pressed. chapter: the scene HOME opens on */
static void dog5_splash(uint32_t chapter)
{
    uint32_t t0 = fm1_ms, btn0 = fm1_in.buttons, key0 = fm1_in.notes, last = 0xFFFFFFFFu, t;
#if defined(OBV_HOST) && !defined(OBV_WASM)
    uint32_t cut = host_splash_full ? SPL_T_END : 2400u;   /* tests: the old splash's 2.4 s, so every script keeps its timing,
                                                              unless it asks for the whole animation ("T splash full") */
#else
    const uint32_t cut = SPL_T_END;
#endif
    spl_rnd = 0x5EED1E55u; spl_em_n = 0; spl_em_t = 0;
    spl_fav_box = spl_box(240, 240); spl_word_box = spl_box(SPL_WORD_W, SPL_WORD_H);
    for (;;) {
        t = fm1_ms - t0;
        if (t >= cut) break;
        if ((fm1_in.buttons & ~btn0) || (fm1_in.notes & ~key0)) break;   /* a press: straight to playing */
        btn0 &= fm1_in.buttons; key0 &= fm1_in.notes;   /* (held at power-on and let go: a new press counts) */
        if (last == 0xFFFFFFFFu || t - last >= SPL_FRAME_MS) {
            last = t;
            spl_draw(t, chapter);
        } else
            platform_poll();
    }
    if (t >= SPL_T_END) spl_draw(SPL_T_END, chapter);   /* the last frame: the scene, whole */
}
