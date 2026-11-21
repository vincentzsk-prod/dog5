/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Vincent Kruger (DØG-5) */
/* HOME: the scene (Stage 3, Batch 20). The chapter's field, the dog on it, and his bark: the live scope fired from his
 * mouth to the top-right corner (the bark IS the scope, CLAUDE.md section 1). The art is hand-painted by Vincent
 * (firmware/gen/dog5_screen_art.h, made by tools/make_screen_art.py from assets/screen/).
 *
 *   rows 0..18     the top bar: the status (the tags, or a readout / toast), the chapter on the right
 *   row 19         a white rule
 *   rows 20..219   the field, the dog, the beam (the field is static; only the dog and the beam move)
 *   row 220        a white rule
 *   rows 221..239  the bottom bar: the program number and name (sacred: never covered)
 *
 * No framebuffer: every change repaints a small rectangle, composed in the strip canvas (gfx.c cv_px) from the field,
 * the dog and the beam, then blitted. A note-on swaps REST for BARK in the head's rectangle only (the generator works
 * it out: REST and BARK share the body). The rest sway (1 px each way, ~2 s, silence only) repaints the dog's box.
 * The DRAW RULE holds: lcd_blit waits through app_idle, and every strip ends with app_idle().
 *
 * Batch 23: the beam is Acid Chartreuse in every chapter (Vincent, 21 Nov). The top bar is THE FENCE: where the bark lands
 * (the top-right corner) it breaks, each chapter its own way, and heals within ~1.2 s of the sound stopping (canon U1);
 * the bottom bar is never touched. FLEAS (GLOBAL knob 2, a global 0..100) rots the picture in four stages: CLEAN, ITCH
 * (the dog's edges boil), SCRATCH (+ scanlines of the field shear sideways), MANGE (+ the fence's text scrambles,
 * mustard blotches spread on the field, the art drops frames). FLEAS never touches the beam or the bottom bar. Safety
 * (canon 9.1): every change is a small area at <= ~6.7 Hz, boil and shear move in 2 px steps, nothing swings the whole
 * screen's brightness. */
#include "dog5_screen_art.h"

#define SC_POSE_REST 0u
#define SC_POSE_BARK 1u
#define SC_POSE_INHALE 2u
#define SC_POSE_HOWL 3u
#define SC_BEAM_MAX 256u                         /* points in the beam (one a pixel along it, at most) */
#define SC_BEAM_AMP 10                           /* the waveform's height either side of the beam, px */
#define SC_END_X 239                             /* the beam lands in the top-right corner of the field */
#define SC_END_Y SA_FIELD_Y

static const char *const SC_CHAPTER[4] = {"I JALOPY", "II BEE-TCH", "III MOONSHINE", "IV ACID CAN"};
/* the chapter accents (the brand palette, each from its scene): the taxi, the wave, the moonlight, the ooze. They colour the
 * chapter's name in the top bar and its damage to the fence */
static const uint16_t SC_ACCENT[4] = {BR_SUN_YELLOW, BR_WAVE_TURQUOISE, BR_FOAM_WHITE, BR_ACID_CHARTREUSE};
#define SC_BEAM_C BR_ACID_CHARTREUSE            /* the beam, every chapter */
#define SC_MUSTARD 0xCE60u                       /* Radioactive Mustard #CCCC00: MANGE's infection (canon's alarm colour) */

/* FLEAS: the state of the rot, as drawn (sc_paint composes it) */
static uint32_t sc_fleas;                        /* 0..100 */
static int8_t sc_boil[32];                       /* ITCH: the dog's rows, 8 at a time, shifted -2 / 0 / +2 px */
static int8_t sc_shear[240];                     /* SCRATCH: each screen row of the field shifted sideways (even px) */
#define SC_MUS_N 6u
static struct { int16_t x, y, r; } sc_mus[SC_MUS_N];   /* MANGE: mustard blotches (r 0: none) */
static uint32_t sc_hash(uint32_t a) { a ^= a >> 16; a *= 0x7FEB352Du; a ^= a >> 15; a *= 0x846CA68Bu; a ^= a >> 16; return a; }

static uint32_t sc_k = 0xFFu;                    /* the scene drawn (0..3), 0xFF: none */
static uint32_t sc_pose;                         /* the pose drawn */
static int32_t sc_dx;                            /* the sway drawn: -1, 0, +1 */
static int16_t bm_x[SC_BEAM_MAX], bm_y[SC_BEAM_MAX];
static uint32_t bm_n;                            /* the beam drawn: its points (0: none) */
static int32_t bm_box[4];                        /* and its box (x0, y0, x1, y1; exclusive) */

static const sa_sprite_t *sc_sprite(uint32_t k, uint32_t pose)
{
    const sa_sprite_t *s = SA_SCENE[k].pose[pose & 3u];
    if (!s) s = SA_SCENE[k].pose[pose == SC_POSE_REST ? 0 : 1];   /* a scene without the howl barks */
    return s;
}

/* a pose's box on the screen (exclusive), with the sway */
static void sc_box(uint32_t k, uint32_t pose, int32_t dx, int32_t *b)
{
    const sa_sprite_t *s = sc_sprite(k, pose);
    b[0] = s->x + dx; b[1] = s->y; b[2] = s->x + dx + (int32_t)s->w; b[3] = s->y + (int32_t)s->h;
}

static void box_union(int32_t *a, const int32_t *b)
{
    if (b[2] <= b[0] || b[3] <= b[1]) return;
    if (a[2] <= a[0] || a[3] <= a[1]) { a[0] = b[0]; a[1] = b[1]; a[2] = b[2]; a[3] = b[3]; return; }
    if (b[0] < a[0]) a[0] = b[0];
    if (b[1] < a[1]) a[1] = b[1];
    if (b[2] > a[2]) a[2] = b[2];
    if (b[3] > a[3]) a[3] = b[3];
}

/* repaint x0..x1, y0..y1 (exclusive) of the field area as it is now: field, dog, beam */
static void sc_paint(int32_t x0, int32_t y0, int32_t x1, int32_t y1)
{
    const sa_scene_t *S = &SA_SCENE[sc_k];
    const sa_sprite_t *d = sc_sprite(sc_k, sc_pose);
    int32_t w, rows, sy, dx = d->x + sc_dx;
    if (x0 < 0) x0 = 0;
    if (x1 > 240) x1 = 240;
    if (y0 < SA_FIELD_Y) y0 = SA_FIELD_Y;
    if (y1 > SA_FIELD_Y + SA_FIELD_H) y1 = SA_FIELD_Y + SA_FIELD_H;
    if (x1 <= x0 || y1 <= y0) return;
    w = x1 - x0;
    rows = (int32_t)(CV_MAX / (uint32_t)w);
    for (sy = y0; sy < y1; sy += rows) {
        int32_t h = y1 - sy < rows ? y1 - sy : rows, y, x;
        lcd_sync();                              /* (the last blit may still read cv_px) */
        cv_w = (uint32_t)w; cv_h = (uint32_t)h;
        for (y = 0; y < h; y++) {
            int32_t Y = sy + y, sr = Y - d->y, sh = sc_shear[Y], m;
            const uint8_t *f = S->px + (uint32_t)(Y - SA_FIELD_Y) * 240u;
            uint16_t *o = cv_px + (uint32_t)y * (uint32_t)w;
            if (!sh) for (x = 0; x < w; x++) o[x] = S->pal[f[x0 + x]];
            else for (x = 0; x < w; x++) {      /* SCRATCH: the row read from sh px to the side (the edge pixel held) */
                int32_t xs = x0 + x - sh;
                o[x] = S->pal[f[xs < 0 ? 0 : xs > 239 ? 239 : xs]];
            }
            if (sr >= 0 && sr < (int32_t)d->h) {  /* the dog's row: index 0 is clear */
                const uint8_t *s = d->px + (uint32_t)sr * d->w;
                int32_t rx = dx + sh + sc_boil[(uint32_t)sr >> 3 & 31u];   /* (the shear and the boil move him too) */
                int32_t a = x0 > rx ? x0 : rx, b = x1 < rx + (int32_t)d->w ? x1 : rx + (int32_t)d->w;
                for (x = a; x < b; x++) {
                    uint32_t i = s[x - rx];
                    if (i) o[x - x0] = d->pal[i - 1u];
                }
            }
            for (m = 0; m < (int32_t)SC_MUS_N; m++) {   /* MANGE: the blotches, a 50 % dither of mustard */
                int32_t r = sc_mus[m].r, dyy = Y - sc_mus[m].y;
                if (!r || dyy < -r || dyy > r) continue;
                for (x = 0; x < w; x++) {
                    int32_t X = x0 + x, dxx = X - sc_mus[m].x;
                    if (((X ^ Y) & 1) == 0 && dxx * dxx + dyy * dyy <= r * r - (int32_t)(sc_hash((uint32_t)(X * 131 + Y)) % (uint32_t)(r * 3 + 1)))
                        o[x] = swap16(SC_MUSTARD);
                }
            }
        }
        if (bm_n > 1u) {                         /* the beam, 2 px thick, Acid Chartreuse (FLEAS never touches it) */
            uint32_t i;
            cv_oy = -sy;
            for (i = 1; i < bm_n; i++) {
                cv_line(bm_x[i - 1u] - x0, bm_y[i - 1u], bm_x[i] - x0, bm_y[i], SC_BEAM_C);
                cv_line(bm_x[i - 1u] - x0, bm_y[i - 1u] + 1, bm_x[i] - x0, bm_y[i] + 1, SC_BEAM_C);
            }
            cv_oy = 0;
        }
        cv_blit((uint32_t)x0, (uint32_t)sy);
        app_idle();
    }
}

/* the fence's damage, drawn into the top bar's canvas (240 x 20: the bar and its rule). fd 0..256 how broken; seed: this
 * frame's grain. The zone grows in from the top-right corner where the beam lands, ragged; each chapter breaks it its own
 * way (the canon's four verbs): I scorches (deleted to black behind a burning taxi-yellow edge, sparks), II soaks (the wave
 * pours down over it from the top, dithered), III fogs (moonlight grain rises through it), IV wrecks (it cracks into
 * shards that drop, acid in the cracks) */
static void sc_fence(uint32_t fd, uint32_t seed)
{
    uint32_t k = sc_k & 3u, r;
    int32_t W = 18 + (int32_t)(fd * 132u >> 8);
    uint16_t ac = swap16(SC_ACCENT[k]);
    if (!fd) return;
    for (r = 20u; r-- > 0u;) {                  /* (bottom up: a shard reads its rows above before they break) */
        int32_t wr = W * (256 - (int32_t)r * 5) / 256 + (int32_t)(sc_hash(r * 977u + seed) % 7u), x0 = 240 - wr, x;
        uint16_t *o = cv_px + r * 240u;
        if (x0 < 0) x0 = 0;
        for (x = x0; x < 240; x++) {
            uint32_t h = sc_hash((uint32_t)x * 7919u + r * 104729u + seed), t = (uint32_t)(x - x0) * 256u / (uint32_t)(wr + 1);
            switch (k) {
            case 0:                             /* SCORCH */
                if (x - x0 < 2) o[x] = h & 1u ? ac : swap16(BR_RAY_RED);
                else o[x] = (h & 63u) < fd / 32u ? ac : 0;   /* (a few sparks in the char) */
                break;
            case 1:                             /* SOAK: from the top down, the depth grows with the damage */
                if ((int32_t)r < 3 + (int32_t)(fd * 17u >> 8) - (int32_t)(h % 3u))
                    o[x] = (h & 255u) < 150u ? ac : swap16(BR_DEEP_TEAL);
                break;
            case 2:                             /* FOG: denser low (it rises) and nearer the corner */
                if ((h & 255u) < (fd * (t + 64u) >> 9) + (r * 4u)) o[x] = ac;
                break;
            default: {                          /* WRECK: 8 px shards, each dropped its own way */
                uint32_t c = (uint32_t)x >> 3, drop = fd * (sc_hash(c * 31u + 7u) % 12u) >> 8;
                if ((x & 7) == 0) o[x] = (h & 3u) ? ac : 0;   /* the cracks, acid in them */
                else o[x] = r >= drop ? cv_px[(r - drop) * 240u + (uint32_t)x] : 0;
                break;
            }
            }
        }
    }
}

static char sc_status[48];                       /* the top bar's text, as last given (the fence redraws it on its own) */
static uint32_t sc_fd, sc_fd_seed;               /* the fence: its damage now (scene_tick), and the grain */

/* the top bar (the fence): status on the left, the chapter on the right in its accent, the rule; then the damage */
static void sc_top(void)
{
    char st[48];
    uint32_t i;
    const char *ch = sc_k < 4u ? SC_CHAPTER[sc_k] : "";
    for (i = 0; i < sizeof st - 1u && sc_status[i]; i++) {   /* MANGE: the status scrambles (never the bottom bar) */
        char c = sc_status[i];
        uint32_t h = sc_hash(i * 2654435761u + sc_fd_seed / 2u);
        st[i] = sc_fleas > 90u && c != ' ' && h % 100u < 40u ? "#%&@$*!?<>/=+~^"[h >> 8 & 15u] : c;
    }
    st[i] = 0;
    cv_begin(240, 20, C_BLACK);
    cv_text(4, 2, &FONT_S, st, C_WHITE);
    if (4 + text_w(&FONT_S, st) + 12 + text_w(&FONT_S, ch) <= 236)   /* the chapter, when the status leaves room */
        cv_text(240 - 4 - text_w(&FONT_S, ch), 2, &FONT_S, ch, sc_k < 4u ? SC_ACCENT[sc_k] : C_WHITE);
    for (i = 0; i < 240u; i++) cv_px[19u * 240u + i] = 0xFFFFu;   /* the rule */
    sc_fence(sc_fd, sc_fd_seed);
    cv_blit(0, 0);
    lcd_sync();
}

/* the bars: status on top (the chapter on the right), number and name below */
static void sc_bars(uint32_t prog_n, const uint8_t *name, uint32_t edited, const char *status)
{
    char n[PATCH_NAME + 6];
    uint32_t i, j = 0;
    for (i = 0; i < sizeof sc_status - 1u && status[i]; i++) sc_status[i] = status[i];
    sc_status[i] = 0;
    sc_top();
    lcd_fill(0, 220, 240, 1, C_WHITE);
    n[j++] = (char)('0' + (prog_n + 1u) / 10u % 10u);
    n[j++] = (char)('0' + (prog_n + 1u) % 10u);
    n[j] = 0;
    cv_begin(240, 19, C_BLACK);
    i = (uint32_t)cv_text(4, 2, &FONT_S, n, BR_ACID_CHARTREUSE);
    j = 0;
    while (j < PATCH_NAME && name[j]) { n[j] = (char)name[j]; j++; }
    while (j && n[j - 1u] == ' ') j--;
    if (edited) n[j++] = '*';
    n[j] = 0;
    cv_text((int32_t)i + 8, 2, &FONT_S, n, C_WHITE);
    cv_blit(0, 221);
    lcd_sync();
}

/* enter (or change) the scene: the whole field, the dog at rest */
static void sc_enter(uint32_t k)
{
    sc_k = k; sc_pose = SC_POSE_REST; sc_dx = 0; bm_n = 0;
    sc_paint(0, SA_FIELD_Y, 240, SA_FIELD_Y + SA_FIELD_H);
}

static void sc_leave(void) { sc_k = 0xFFu; bm_n = 0; }

/* one pixel of scene k as HOME first draws it (the field, the dog at rest, no sway), stored byte-swapped as cv_px; the
 * bars' rows are black. The boot animation (dog5_splash.h) reveals the scene through its burn with this */
static uint16_t sc_px_rest(uint32_t k, int32_t x, int32_t y)
{
    const sa_scene_t *S = &SA_SCENE[k & 3u];
    const sa_sprite_t *d = S->pose[SC_POSE_REST];
    int32_t sx = x - d->x, sy = y - d->y;
    if (y < SA_FIELD_Y || y >= SA_FIELD_Y + SA_FIELD_H || x < 0 || x >= 240) return 0;
    if (sx >= 0 && sy >= 0 && sx < (int32_t)d->w && sy < (int32_t)d->h) {
        uint32_t i = d->px[(uint32_t)sy * d->w + (uint32_t)sx];
        if (i) return d->pal[i - 1u];
    }
    return S->pal[S->px[(uint32_t)(y - SA_FIELD_Y) * 240u + (uint32_t)x]];
}

/* a new pose (and sway): repaints only what changes. REST <-> BARK at no sway: the head's rectangle */
static void sc_set_pose(uint32_t pose, int32_t dx)
{
    int32_t r[4] = {0, 0, 0, 0}, b[4];
    if (pose == sc_pose && dx == sc_dx) return;
    if (dx == 0 && sc_dx == 0 && ((pose == SC_POSE_REST && sc_pose == SC_POSE_BARK) || (pose == SC_POSE_BARK && sc_pose == SC_POSE_REST))
        && sc_sprite(sc_k, SC_POSE_REST) != sc_sprite(sc_k, SC_POSE_BARK)) {
        const int16_t *h = SA_SCENE[sc_k].head;
        r[0] = h[0]; r[1] = h[1]; r[2] = h[2]; r[3] = h[3];
    } else {
        sc_box(sc_k, sc_pose, sc_dx, b); box_union(r, b);
        sc_box(sc_k, pose, dx, b); box_union(r, b);
    }
    if (sc_fleas > 15u) { r[0] -= 12; r[2] += 12; }   /* (the boil and the shear move him up to 12 px) */
    sc_pose = pose; sc_dx = dx;
    sc_paint(r[0], r[1], r[2], r[3]);
}

/* FLEAS, a pass of the main loop on HOME: f the dial (0..100), now the clock. Each stage re-rolls its rot on its own clock
 * (the boil every 150 ms = 6.7 Hz, on a 2 px lattice; the shear every 330 ms, even steps; the blotches every second)
 * and repaints only what moved. Below a stage's threshold its rot is cleared */
static uint32_t fl_t_boil, fl_t_shear, fl_t_mus, fl_rnd = 0xF1EA5u, sc_shear_on;
static uint32_t fl_rand(void) { fl_rnd = fl_rnd * 1664525u + 1013904223u; return fl_rnd >> 8; }
static void sc_dogbox(int32_t *b) { sc_box(sc_k, sc_pose, sc_dx, b); b[0] -= 14; b[2] += 14; }
static void sc_fleas_tick(uint32_t f, uint32_t now)
{
    uint32_t i, ch = 0;
    int32_t b[4];
    if (f > 100u) f = 100u;
    sc_fleas = f;
    /* ITCH and up: the dog boils */
    if (f > 15u ? now - fl_t_boil >= 150u : 0) {
        uint32_t p = f <= 65u ? 15u + (f - 16u) * 45u / 49u : 60u;
        fl_t_boil = now;
        if (!(f > 90u && fl_rand() % 100u < 30u)) {   /* (MANGE drops frames) */
            for (i = 0; i < 32u; i++) {
                uint32_t h = fl_rand();
                int8_t o = h % 100u < p ? ((h >> 9) & 1u ? 2 : -2) : 0;
                if (o != sc_boil[i]) { sc_boil[i] = o; ch = 1; }
            }
        }
    } else if (f <= 15u)
        for (i = 0; i < 32u; i++) if (sc_boil[i]) { sc_boil[i] = 0; ch = 1; }
    if (ch) { sc_dogbox(b); sc_paint(b[0], b[1], b[2], b[3]); }
    /* SCRATCH and up: bands of the field shear sideways (below SCRATCH: any left are cleared) */
    if (f > 65u ? now - fl_t_shear >= 330u : sc_shear_on) {
        int32_t y, a = -1;
        uint32_t nb = f > 65u ? 1u + (f - 66u) * 5u / 25u : 0u;
        fl_t_shear = now;
        for (y = SA_FIELD_Y; y <= SA_FIELD_Y + SA_FIELD_H; y++) {   /* the old bands go */
            int32_t on = y < SA_FIELD_Y + SA_FIELD_H && sc_shear[y];
            if (on && a < 0) a = y;
            if (!on && a >= 0) { int32_t k; for (k = a; k < y; k++) sc_shear[k] = 0; sc_paint(0, a, 240, y); a = -1; }
        }
        sc_shear_on = nb != 0;
        for (i = 0; i < nb; i++) {              /* the new ones */
            int32_t yy = SA_FIELD_Y + (int32_t)(fl_rand() % (uint32_t)(SA_FIELD_H - 8)), hh = 2 + (int32_t)(fl_rand() % 7u), k;
            int32_t sh = 2 * (1 + (int32_t)(fl_rand() % 5u)) * ((fl_rand() & 1u) ? 1 : -1);
            for (k = 0; k < hh; k++) sc_shear[yy + k] = (int8_t)sh;
            sc_paint(0, yy, 240, yy + hh);
        }
    }
    /* MANGE: mustard blotches */
    if (f > 90u ? now - fl_t_mus >= 1000u : 0) {
        uint32_t n = 2u + (f - 91u) * 4u / 9u;
        fl_t_mus = now;
        for (i = 0; i < SC_MUS_N; i++) {
            int32_t r = sc_mus[i].r, x = sc_mus[i].x, y = sc_mus[i].y;
            sc_mus[i].r = 0;
            if (r) sc_paint(x - r, y - r, x + r + 1, y + r + 1);
            if (i < n) {
                sc_mus[i].x = (int16_t)(10 + fl_rand() % 220u); sc_mus[i].y = (int16_t)(SA_FIELD_Y + 10 + fl_rand() % 180u);
                sc_mus[i].r = (int16_t)(6 + fl_rand() % 14u);
                sc_paint(sc_mus[i].x - sc_mus[i].r, sc_mus[i].y - sc_mus[i].r, sc_mus[i].x + sc_mus[i].r + 1, sc_mus[i].y + sc_mus[i].r + 1);
            }
        }
    } else if (f <= 90u)
        for (i = 0; i < SC_MUS_N; i++)
            if (sc_mus[i].r) { int32_t r = sc_mus[i].r; sc_mus[i].r = 0; sc_paint(sc_mus[i].x - r, sc_mus[i].y - r, sc_mus[i].x + r + 1, sc_mus[i].y + r + 1); }
}

/* the beam from the mouth of the pose drawn, carrying s[0..n) (the scope: one cycle or two, zero-crossing
 * triggered); s = 0: the beam goes. Repaints the old beam's box and the new one's */
static void sc_beam(const int16_t *s, uint32_t n)
{
    const sa_sprite_t *d = sc_sprite(sc_k, sc_pose);
    int32_t old[4] = {bm_box[0], bm_box[1], bm_box[2], bm_box[3]}, had = bm_n > 1u;
    bm_n = 0;
    bm_box[0] = bm_box[1] = bm_box[2] = bm_box[3] = 0;
    if (s && n > 1u && d->bx >= 0) {
        int32_t mx = d->x + sc_dx + d->bx, my = d->y + d->by, ex = SC_END_X - mx, ey = SC_END_Y - my;
        int32_t L = (int32_t)isqrt32((uint32_t)(ex * ex + ey * ey)), N, i;
        if (L < 2) L = 2;
        N = L < (int32_t)SC_BEAM_MAX ? L : (int32_t)SC_BEAM_MAX;
        bm_box[0] = bm_box[2] = mx; bm_box[1] = bm_box[3] = my;
        for (i = 0; i < N; i++) {
            int32_t a = s[(uint32_t)i * (n - 1u) / (uint32_t)(N - 1)] >> 10, x, y;
            if (a > SC_BEAM_AMP) a = SC_BEAM_AMP;
            if (a < -SC_BEAM_AMP) a = -SC_BEAM_AMP;
            if (i < 8) a = a * i / 8;            /* it leaves the mouth on the centre line */
            x = mx + ex * i / (N - 1) - ey * a / L;
            y = my + ey * i / (N - 1) + ex * a / L;
            bm_x[i] = (int16_t)x; bm_y[i] = (int16_t)y;
            if (x < bm_box[0]) bm_box[0] = x;
            if (y < bm_box[1]) bm_box[1] = y;
            if (x + 2 > bm_box[2]) bm_box[2] = x + 2;
            if (y + 2 > bm_box[3]) bm_box[3] = y + 2;
        }
        bm_n = (uint32_t)N;
    }
    if (had) box_union(old, bm_box); else { old[0] = bm_box[0]; old[1] = bm_box[1]; old[2] = bm_box[2]; old[3] = bm_box[3]; }
    if (old[2] > old[0] && old[3] > old[1]) sc_paint(old[0], old[1], old[2], old[3]);
}
