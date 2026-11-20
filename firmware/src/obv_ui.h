/* SPDX-License-Identifier: GPL-3.0-only */
/* The screen of every page but HOME (HOME is the scene: dog5_scene.h). DØG-5's look since Batch 21, in the brand palette
 * (dog5_palette.h): black, the legends Foam White, the dim ones Grime Olive, the accent (the page's name, the knobs' value
 * arcs, the scope's trace) Acid Chartreuse, the program number as 7-segment digits in Acid Chartreuse over unlit Plum
 * Night segments (as the update screen's bar), the rules and the knobs' tracks Sky Violet, the scope on Jungle Deep, the
 * voice LEDs Ray Pink, the pixel wordmark (Sun Yellow, outlined, an Acid Chartreuse shadow) in the header. The layout is
 * OberVave's (zvenson); its blue-black panel, red digits and banded logo are gone. 240 x 240:
 *   0..43    header: program number, name, tags, the wordmark
 *   46..143  the page: title between rules, four knobs (label above, value below)
 *   146..195 the scope
 *   200..236 the voice LEDs */
#include "dog5_palette.h"
#include "dog5_ui_art.h"
#define C_PANEL BR_BLACK                        /* the background */
#define C_TEXT BR_FOAM_WHITE                    /* the legends and values */
#define C_ACCENT BR_ACID_CHARTREUSE             /* what is being touched / where we are */
#define C_ALERT BR_RAY_PINK                     /* SAVE?, the CPU readout */
#define C_DIM BR_GRIME_OLIVE                    /* the knobs' labels, the tags, the second hint line */
#define C_RULE BR_SKY_VIOLET                    /* rules, the knobs' tracks */
#define C_KNOB BR_PLUM_NIGHT
#define C_KNOB_HI BR_SKY_VIOLET
#define C_DIGIT BR_ACID_CHARTREUSE
#define C_DIGIT_OFF BR_PLUM_NIGHT
#define C_SCOPE_BG BR_JUNGLE_DEEP
#define C_SCOPE_MID BR_JUNGLE
#define C_LED_OFF BR_PLUM_NIGHT
#define C_LED_ON BR_RAY_PINK

/* a * (1 - t) + b * t for RGB565, t = 0..256 */
static uint16_t blend565(uint16_t a, uint16_t b, uint32_t t)
{
    uint32_t r = ((a >> 11) * (256u - t) + (b >> 11) * t) >> 8;
    uint32_t g = (((a >> 5) & 63u) * (256u - t) + ((b >> 5) & 63u) * t) >> 8;
    uint32_t bl = ((a & 31u) * (256u - t) + (b & 31u) * t) >> 8;
    return (uint16_t)(r << 11 | g << 5 | bl);
}

static inline uint16_t cv_get(int32_t x, int32_t y)
{
    y += cv_oy;
    if ((uint32_t)x < cv_w && (uint32_t)y < cv_h)
        return swap16(cv_px[(uint32_t)y * cv_w + (uint32_t)x]);
    return C_PANEL;
}

/* an anti-aliased disc: coverage from the distance to the centre (pixel centres at +0.5, so in doubled units),
 * blended over what is there. r in pixels, ring: 0 = full disc, else only r - ring .. r */
static void cv_disc(int32_t cx, int32_t cy, int32_t r, int32_t ring, uint16_t c)
{
    int32_t x, y, ro2 = (2 * r + 1) * (2 * r + 1), ri2 = (2 * r - 1) * (2 * r - 1);
    int32_t in2 = ring ? (2 * (r - ring) + 1) * (2 * (r - ring) + 1) : -1, in1 = ring ? (2 * (r - ring) - 1) * (2 * (r - ring) - 1) : -1;
    for (y = cy - r - 1; y <= cy + r + 1; y++)
        for (x = cx - r - 1; x <= cx + r + 1; x++) {
            int32_t dx = 2 * (x - cx), dy = 2 * (y - cy), d2 = dx * dx + dy * dy, t;
            if (d2 >= ro2 || (ring && d2 < in1))
                continue;
            t = 256;
            if (d2 > ri2)                       /* the outer edge: 1 px of coverage */
                t = 256 * (ro2 - d2) / (ro2 - ri2);
            if (ring && d2 < in2)               /* the inner edge */
                t = 256 * (d2 - in1) / (in2 - in1);
            cv_pset(x, y, t >= 256 ? c : blend565(cv_get(x, y), c, (uint32_t)t));
        }
}

/* a line of width 2, for the arcs and pointers */
static void cv_line2(int32_t x0, int32_t y0, int32_t x1, int32_t y1, uint16_t c)
{
    cv_line(x0, y0, x1, y1, c);
    cv_line(x0 + 1, y0, x1 + 1, y1, c);
    cv_line(x0, y0 + 1, x1, y1 + 1, c);
}

/* the knob's angle: value 0 at 225 deg (lower left), max at -45 deg (lower right), 270 deg of travel */
static void knob_xy(int32_t cx, int32_t cy, int32_t rad, int32_t deg, int32_t *x, int32_t *y)
{
    int32_t i;
    while (deg < 0) deg += 360;
    while (deg >= 360) deg -= 360;
    i = deg / 5;
    *x = cx + ((rad * COS_Q8[i]) >> 8);
    *y = cy - ((rad * COS_Q8[(i + 54u) % 72u]) >> 8);   /* sin = cos(deg - 90): 90 deg = 18 steps back = 54 on */
}

static void cv_arc(int32_t cx, int32_t cy, int32_t rad, int32_t deg0, int32_t deg1, uint16_t c)   /* clockwise on screen */
{
    int32_t d, x0, y0, x1, y1;
    knob_xy(cx, cy, rad, deg0, &x0, &y0);
    for (d = deg0 - 5; d >= deg1; d -= 5) {
        knob_xy(cx, cy, rad, d, &x1, &y1);
        cv_line2(x0, y0, x1, y1, c);
        x0 = x1; y0 = y1;
    }
}

/* a knob: label above, the value's arc and pointer, the value below. v / max, bip: the arc grows from the middle */
static void cv_knob(int32_t cx, int32_t cy, const char *label, const char *value, int32_t v, int32_t max, int32_t bip)
{
    int32_t ang = 225 - (max ? 270 * v / max : 0), px, py, qx, qy, r = 15;
    cv_text(cx - text_w(&FONT_S, label) / 2, cy - 44, &FONT_S, label, C_DIM);
    cv_arc(cx, cy, r + 6, 225, -45, C_RULE);
    if (bip) {
        if (ang < 90) cv_arc(cx, cy, r + 6, 90, ang, C_ACCENT);
        else cv_arc(cx, cy, r + 6, ang, 90, C_ACCENT);
    } else
        cv_arc(cx, cy, r + 6, 225, ang, C_ACCENT);
    cv_disc(cx, cy, r, 0, C_KNOB);
    cv_disc(cx, cy, r, 2, C_KNOB_HI);
    knob_xy(cx, cy, 5, ang, &px, &py);
    knob_xy(cx, cy, r - 2, ang, &qx, &qy);
    cv_line2(px, py, qx, qy, C_TEXT);
    cv_text(cx - text_w(&FONT_S, value) / 2, cy + 24, &FONT_S, value, C_TEXT);
}

/* 7-segment digit, w 16 x h 28, thickness 4: segments a (top) b c d (bottom) e f g (middle) */
static void cv_seg7(int32_t x, int32_t y, uint32_t digit, uint16_t on, uint16_t off)
{
    static const uint8_t SEG[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};
    uint32_t m = SEG[digit % 10u];
    const int32_t t = 4, w = 16, h = 28;
    cv_rect(x + 2, y, w - 4, t, m & 1u ? on : off);                       /* a */
    cv_rect(x + w - t, y + 2, t, h / 2 - 3, m & 2u ? on : off);           /* b */
    cv_rect(x + w - t, y + h / 2 + 1, t, h / 2 - 3, m & 4u ? on : off);   /* c */
    cv_rect(x + 2, y + h - t, w - 4, t, m & 8u ? on : off);               /* d */
    cv_rect(x, y + h / 2 + 1, t, h / 2 - 3, m & 16u ? on : off);          /* e */
    cv_rect(x, y + 2, t, h / 2 - 3, m & 32u ? on : off);                  /* f */
    cv_rect(x + 2, y + h / 2 - 2, w - 4, t, m & 64u ? on : off);          /* g */
}

/* the pixel wordmark (dog5_ui_art.h, 2 bits a pixel: 0 clear, 2 Sun Yellow, 3 Acid Chartreuse) with its top left at x, y */
static void draw_wordmark(int32_t x, int32_t y)
{
    uint32_t i, j;
    for (j = 0; j < UI_WORD_H; j++)
        for (i = 0; i < UI_WORD_W; i++) {
            uint32_t v = UI_WORD[j * ((UI_WORD_W + 3u) / 4u) + i / 4u] >> (6u - 2u * (i & 3u)) & 3u;
            if (v >= 2u) cv_pset(x + (int32_t)i, y + (int32_t)j, v == 2u ? BR_SUN_YELLOW : BR_ACID_CHARTREUSE);
        }
}

/* ---- the parts of the screen (the app decides when) */
static void ui_header(uint32_t prog, const uint8_t *name, uint32_t edited, const char *tags)
{
    char n[PATCH_NAME + 2];
    uint32_t i;
    cv_begin(240, 44, C_PANEL);
    cv_seg7(6, 6, (prog + 1u) / 10u, C_DIGIT, C_DIGIT_OFF);
    cv_seg7(26, 6, (prog + 1u) % 10u, C_DIGIT, C_DIGIT_OFF);
    for (i = 0; i < PATCH_NAME; i++) n[i] = (char)name[i];
    n[PATCH_NAME] = edited ? '*' : 0;
    n[PATCH_NAME + 1] = 0;
    cv_text(54, 4, &FONT_S, n, C_TEXT);
    cv_text(54, 22, &FONT_S, tags, C_DIM);
    draw_wordmark(240 - 4 - (int32_t)UI_WORD_W, 5);
    cv_rect(0, 42, 240, 1, C_RULE);
    cv_blit(0, 0);
}

typedef struct { const char *label; char value[12]; int32_t v, max, bip, present; } knob_view_t;
static void ui_page(const char *title, const knob_view_t *k, const char *note)
{
    int32_t tw = text_w(&FONT_S, title), i;
    cv_begin(240, 98, C_PANEL);
    cv_rect(6, 9, (240 - tw) / 2 - 14, 1, C_RULE);
    cv_text((240 - tw) / 2, 1, &FONT_S, title, C_ACCENT);
    cv_rect((240 + tw) / 2 + 8, 9, (240 - tw) / 2 - 14, 1, C_RULE);
    for (i = 0; i < 4; i++)
        if (k[i].present) {
            cv_knob(30 + 60 * i, 62, k[i].label, k[i].value, k[i].v, k[i].max, k[i].bip);
            app_idle();                         /* (a knob is ~1 ms: the keys and MIDI in between) */
        }
    if (note)
        cv_text(240 - 4 - text_w(&FONT_S, note), 1, &FONT_S, note, C_ALERT);
    cv_blit(0, 46);
}

/* HOLD HOME: the control map of the page you are on. Two strips under a 32 px head (the canvas is 120 rows at most), each
 * followed by app_idle(), and app_idle() after every row: the DRAW RULE (CLAUDE.md section 6), a draw that takes time
 * lets the notes through.
 *   head   the page's name, and under it the four knobs (what each one is on this page; "-" = none)
 *   rows   MAP_ROWS lines, 16 px each, down to the bottom edge. A row is a button / control with its dog name and the label
 *          printed on the panel ("DIG (EDIT)") and what it does (for the page buttons: where a press goes NOW, so the map
 *          stays true as the families' memories change); a row with no `what` is a line of its own, drawn across the
 *          screen (the EDIT-held key shortcuts) */
typedef struct { const char *label, *what; } map_row_t;
#define MAP_ROWS 13
#define MAP_HEAD 32                             /* the head; the rows run from here to y 240 (13 x 16 = 208) */
static void ui_map(const char *title, const knob_view_t *k, const char *knob_note, const map_row_t *r, int32_t hi)
{
    int32_t i, xw = 0;
    cv_begin(240, MAP_HEAD, C_PANEL);
    cv_text((240 - text_w(&FONT_S, title)) / 2, 0, &FONT_S, title, C_ACCENT);
    for (i = 0; i < 4; i++) {
        if (k[i].present)
            cv_text(30 + 60 * i - text_w(&FONT_S, k[i].label) / 2, 16, &FONT_S, k[i].label, C_TEXT);
        else if (!knob_note)
            cv_text(30 + 60 * i - text_w(&FONT_S, "-") / 2, 16, &FONT_S, "-", C_RULE);
        if (i && !knob_note) cv_rect(60 * i, 18, 1, 13, C_RULE);
    }
    if (knob_note)
        cv_text((240 - text_w(&FONT_S, knob_note)) / 2, 16, &FONT_S, knob_note, C_DIM);
    cv_rect(0, 31, 240, 1, C_RULE);
    cv_blit(0, 0);
    app_idle();
    for (i = 0; i < MAP_ROWS; i++)              /* "what" starts after the widest label */
        if (r[i].what && text_w(&FONT_S, r[i].label) > xw) xw = text_w(&FONT_S, r[i].label);
    xw += 4 + 4;
    for (i = 0; i < MAP_ROWS; i++) {
        int32_t y;
        if (i == 0 || i == 6) cv_begin(240, i ? 112 : 96, C_PANEL);   /* a new strip: rows 0-5 from y 32, rows 6-12 from y 128 */
        y = i < 6 ? i * 16 : (i - 6) * 16;
        if (!r[i].what)
            cv_text((240 - text_w(&FONT_S, r[i].label)) / 2, y, &FONT_S, r[i].label, C_ACCENT);
        else {
            cv_text(4, y, &FONT_S, r[i].label, i == hi ? C_ACCENT : C_TEXT);
            cv_text(xw, y, &FONT_S, r[i].what, i == hi ? C_ACCENT : C_DIM);
        }
        app_idle();                             /* (a row is ~1 ms: the keys and MIDI in between) */
        if (i == 5) { cv_blit(0, MAP_HEAD); app_idle(); }
    }
    cv_blit(0, 128);
    app_idle();
}

static void ui_scope(const int16_t *s, uint32_t n)
{
    uint32_t i;
    cv_begin(240, 50, C_SCOPE_BG);
    cv_rect(0, 25, 240, 1, C_SCOPE_MID);
    for (i = 1; i < n; i++)
        cv_line((int32_t)i - 1, 25 - clampi(s[i - 1u] >> 9, -23, 23), (int32_t)i, 25 - clampi(s[i] >> 9, -23, 23), C_ACCENT);
    cv_blit(0, 146);
}

static void ui_leds(const volatile int32_t *level, uint32_t n)
{
    uint32_t v;
    cv_begin(240, 36, C_PANEL);
    for (v = 0; v < n; v++) {
        uint32_t l = (uint32_t)level[v] >> 7;   /* 0..255 */
        uint16_t c = blend565(C_LED_OFF, C_LED_ON, l), halo = blend565(C_PANEL, C_LED_ON, l / 4u);
        int32_t cx = 22 + (int32_t)v * 28;
        if (l > 8u) cv_disc(cx, 17, 10, 0, halo);
        cv_disc(cx, 17, 6, 0, c);
        cv_disc(cx, 17, 6, 1, blend565(C_PANEL, c, 160));
    }
    cv_blit(0, 200);
}

/* the step view's hints (instead of the voice LEDs): what the keys do now, two lines */
static void ui_hints(const char *l1, const char *l2, uint16_t c1)
{
    cv_begin(240, 36, C_PANEL);
    cv_text((240 - text_w(&FONT_S, l1)) / 2, 1, &FONT_S, l1, c1);
    cv_text((240 - text_w(&FONT_S, l2)) / 2, 19, &FONT_S, l2, C_DIM);
    cv_blit(0, 200);
}
