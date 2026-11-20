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
 * The DRAW RULE holds: lcd_blit waits through app_idle, and every strip ends with app_idle(). */
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
            int32_t Y = sy + y, sr = Y - d->y;
            const uint8_t *f = S->px + (uint32_t)(Y - SA_FIELD_Y) * 240u + (uint32_t)x0;
            uint16_t *o = cv_px + (uint32_t)y * (uint32_t)w;
            for (x = 0; x < w; x++) o[x] = S->pal[f[x]];
            if (sr >= 0 && sr < (int32_t)d->h) {  /* the dog's row: index 0 is clear */
                const uint8_t *s = d->px + (uint32_t)sr * d->w;
                int32_t a = x0 > dx ? x0 : dx, b = x1 < dx + (int32_t)d->w ? x1 : dx + (int32_t)d->w;
                for (x = a; x < b; x++) {
                    uint32_t i = s[x - dx];
                    if (i) o[x - x0] = d->pal[i - 1u];
                }
            }
        }
        if (bm_n > 1u) {                         /* the beam, 2 px thick, white */
            uint32_t i;
            cv_oy = -sy;
            for (i = 1; i < bm_n; i++) {
                cv_line(bm_x[i - 1u] - x0, bm_y[i - 1u], bm_x[i] - x0, bm_y[i], C_WHITE);
                cv_line(bm_x[i - 1u] - x0, bm_y[i - 1u] + 1, bm_x[i] - x0, bm_y[i] + 1, C_WHITE);
            }
            cv_oy = 0;
        }
        cv_blit((uint32_t)x0, (uint32_t)sy);
        app_idle();
    }
}

/* the bars: status on top (the chapter on the right), number and name below */
static void sc_bars(uint32_t prog_n, const uint8_t *name, uint32_t edited, const char *status)
{
    char n[PATCH_NAME + 6];
    uint32_t i, j = 0;
    const char *ch = sc_k < 4u ? SC_CHAPTER[sc_k] : "";
    cv_begin(240, 19, C_BLACK);
    cv_text(4, 2, &FONT_S, status, C_WHITE);
    if (4 + text_w(&FONT_S, status) + 12 + text_w(&FONT_S, ch) <= 236)   /* the chapter, when the status leaves room */
        cv_text(240 - 4 - text_w(&FONT_S, ch), 2, &FONT_S, ch, RGB(0x84, 0x92, 0x6C));   /* Grime Olive */
    cv_blit(0, 0);
    lcd_fill(0, 19, 240, 1, C_WHITE);
    lcd_fill(0, 220, 240, 1, C_WHITE);
    n[j++] = (char)('0' + (prog_n + 1u) / 10u % 10u);
    n[j++] = (char)('0' + (prog_n + 1u) % 10u);
    n[j] = 0;
    cv_begin(240, 19, C_BLACK);
    i = (uint32_t)cv_text(4, 2, &FONT_S, n, RGB(0xDE, 0xF4, 0x02));   /* Acid Chartreuse */
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
    sc_pose = pose; sc_dx = dx;
    sc_paint(r[0], r[1], r[2], r[3]);
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
