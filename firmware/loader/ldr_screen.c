/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 zvenson (OberVave; the Firmware Hub's look)
 * Copyright (C) 2026 illuminus5 (Skiff: the idea, a loader that draws, its 5 x 7 letters and the order of things)
 * Copyright (C) 2026 ZIGGY, DØGS (DØG-5: the dog head, the wordmark and the brand colours) */
/* The update loader's screen (loader.c; tests/ldr_screen_test.c). A unit whose install was cut off comes back to the
 * loader at every power-on and showed a black screen; now it says what it does, in DØG-5's brand colours on black:
 *   the dog head and the DØG-5 wordmark (ldr_art.h, pictures drawn row by row)
 *   what happens (UPDATE MODE, WRITING and its percent, UPDATE FAILED in red) and what to do, white and olive
 *   20 segments: a light running to and fro while it waits (ldr_anim), the share written while it writes
 *   thefirmwarehub.com at the foot, in pink
 * Drawn with the loader's own letters (the app area may be half written: never read), before USB starts (USB is
 * polled: the panel's ~0.3 s init would leave the host's enumeration unanswered). FM-1 only.
 * LDR_COLOUR: the lit segments and the waiting light (RGB565). Colours: claude/DOG-5-brand-palette.md. */
#include "ldr_art.h"
#ifndef LDR_COLOUR
#define LDR_COLOUR 0xDFA0u               /* Acid Chartreuse, #DEF402 */
#endif
#define LDR_BG 0x0000u                   /* Black */
#define LDR_INK 0xFFFFu                  /* Foam White */
#define LDR_SUB 0x848Du                  /* Grime Olive, #84926C */
#define LDR_DIM 0x3028u                  /* a segment off: Plum Night, #320444 */
#define LDR_HUB 0xEAAFu                  /* Ray Pink, #EC5579 */
#define LDR_BAD 0xE063u                  /* Ray Red, #E20D1D: UPDATE FAILED */
#define LDR_YEL 0xFE66u                  /* Sun Yellow, #F8CD30: the wordmark */
#define LDR_MIX(a, b) ((((a) >> 11) + ((b) >> 11)) / 2u << 11 | ((((a) >> 5) & 63u) + (((b) >> 5) & 63u)) / 2u << 5 | \
                       (((a) & 31u) + ((b) & 31u)) / 2u)
#define LDR_TAIL LDR_MIX(LDR_COLOUR, LDR_DIM)   /* the waiting light's afterglow: halfway to a segment off */

/* the letters the screens use (others: a space): capitals, digits, % and the hub's address in small letters */
static const char LDR_CH[] = "ABCDEFGHIKLMNOPRSTUVWXY0123456789%abcefhimortuw.";
static const uint8_t LDR_FONT[sizeof LDR_CH - 1u][7] = {         /* rows, bit 4 the left dot */
    {0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11}, {0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E},   /* A B */
    {0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E}, {0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E},   /* C D */
    {0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F}, {0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10},   /* E F */
    {0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F}, {0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11},   /* G H */
    {0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E}, {0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11},   /* I K */
    {0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F}, {0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11},   /* L M */
    {0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11}, {0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E},   /* N O */
    {0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10}, {0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11},   /* P R */
    {0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E}, {0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04},   /* S T */
    {0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E}, {0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04},   /* U V */
    {0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A}, {0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11},   /* W X */
    {0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04},                                               /* Y */
    {0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E}, {0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E},   /* 0 1 */
    {0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F}, {0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E},   /* 2 3 */
    {0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02}, {0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E},   /* 4 5 */
    {0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E}, {0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08},   /* 6 7 */
    {0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E}, {0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C},   /* 8 9 */
    {0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03},                                               /* % */
    {0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F}, {0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x1E},   /* a b */
    {0x00, 0x00, 0x0E, 0x10, 0x10, 0x11, 0x0E}, {0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E},   /* c e */
    {0x06, 0x09, 0x08, 0x1C, 0x08, 0x08, 0x08}, {0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x11},   /* f h */
    {0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E}, {0x00, 0x00, 0x1A, 0x15, 0x15, 0x11, 0x11},   /* i m */
    {0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E}, {0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10},   /* o r */
    {0x08, 0x08, 0x1C, 0x08, 0x08, 0x09, 0x06}, {0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D},   /* t u */
    {0x00, 0x00, 0x11, 0x11, 0x15, 0x15, 0x0A}, {0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C},   /* w . */
};
#define LDR_SEGS 20u                     /* the segments: 9 px and a 2 px gap, 218 px, centred */
#define LDR_SEG_W 9u
#define LDR_SEG_X 11u
#define LDR_SEG_Y 206u
#define LDR_SEG_H 9u
#define LDR_HEAD_Y 6u                    /* the head, centred; the wordmark under it */
#define LDR_WORD_Y 110u
#define LDR_SAY_Y 166u                   /* the status (size 2) and what to do (size 1) */
#define LDR_SUB_Y 188u

static uint32_t ldr_missing;                        /* letters drawn as gaps: 0 (ldr_screen_test) */
static uint32_t ldr_len(const char *t)
{
    uint32_t n = 0;
    while (t[n])
        n++;
    return n;
}
static void ldr_text(uint32_t y, uint32_t s, uint16_t c, const char *t)   /* centred, a dot s x s px */
{
    uint32_t n = ldr_len(t), x, r, k, i, b;
    if (!n)
        return;
    for (x = (240u - (n * 6u - 1u) * s) / 2u; *t; t++, x += 6u * s) {
        for (k = 0; LDR_CH[k] && LDR_CH[k] != *t; k++)
            ;
        if (!LDR_CH[k]) {
            ldr_missing += *t != ' ';                   /* (a letter the font lacks: a gap) */
            continue;
        }
        for (r = 0; r < 7u; r++)
            for (i = 0; i < 5u; i = b) {                /* each run of dots in the row: one fill */
                for (; i < 5u && !(LDR_FONT[k][r] >> (4u - i) & 1u); i++)
                    ;
                for (b = i; b < 5u && (LDR_FONT[k][r] >> (4u - b) & 1u); b++)
                    ;
                if (b > i)
                    lcd_fill(x + i * s, y + r * s, (b - i) * s, s, c);
            }
    }
}
static void ldr_seg(uint32_t i, uint16_t c)
{
    lcd_fill(LDR_SEG_X + i * (LDR_SEG_W + 2u), LDR_SEG_Y, LDR_SEG_W, LDR_SEG_H, c);
}
static uint16_t ldr_row[240];                     /* one picture row, as the panel takes it (bytes swapped) */
static void ldr_pic(uint32_t y, uint32_t w, uint32_t h, uint32_t bpp, const uint8_t *p, const uint16_t *pal)
{                                                   /* a picture from ldr_art.h, centred, one row a transfer */
    uint32_t x0 = (240u - w) / 2u, bpr = (w * bpp + 7u) / 8u, r, x, v, c;
    for (r = 0; r < h; r++, p += bpr) {
        lcd_sync();                                 /* (the last row's transfer reads ldr_row) */
        for (x = 0; x < w; x++) {
            v = p[x * bpp / 8u] >> (8u - bpp - x * bpp % 8u) & ((1u << bpp) - 1u);
            c = pal[v];
            ldr_row[x] = (uint16_t)(c >> 8 | c << 8);
        }
        lcd_blit(x0, y + r, w, 1, ldr_row);
    }
}
static void ldr_say(const char *what, const char *sub, uint16_t c)   /* the status and what to do */
{
    lcd_fill(0, LDR_SAY_Y, 240, LDR_SUB_Y + 7u - LDR_SAY_Y, LDR_BG);
    ldr_text(LDR_SAY_Y, 2, c, what);
    ldr_text(LDR_SUB_Y, 1, LDR_SUB, sub);
}
static void ldr_percent(uint32_t p)                  /* the status line while it writes: "WRITING 57%" */
{
    char t[13] = "WRITING ";
    uint32_t n = 8;
    if (p > 100u)
        return;
    lcd_fill(0, LDR_SAY_Y, 240, 14, LDR_BG);
    if (p >= 100u)
        t[n++] = '1';
    if (p >= 10u)
        t[n++] = (char)('0' + p / 10u % 10u);
    t[n++] = (char)('0' + p % 10u);
    t[n++] = '%';
    t[n] = 0;
    ldr_text(LDR_SAY_Y, 2, LDR_INK, t);
}

static uint32_t ldr_lit;                            /* segments lit for the write */
static uint32_t ldr_pct = 0xFFFFu;                  /* the percent on the screen */
static uint8_t ldr_writing;                         /* WRITING is on the screen */
static uint8_t ldr_idle = 1;                        /* the waiting light runs (not after a write, nor a failure) */
static uint32_t ldr_pos, ldr_next;                  /* the waiting light: its segment (0..37, to and fro), its next move */
static void ldr_screen(void)
{
    static const uint16_t head[2] = {LDR_BG, LDR_INK}, word[4] = {LDR_BG, LDR_BG, LDR_YEL, LDR_COLOUR};
    uint32_t i;
    lcd_init();                                     /* (the panel cleared, on) */
    lcd_fill(0, 0, 240, 240, LDR_BG);
    ldr_pic(LDR_HEAD_Y, LDR_HEAD_W, LDR_HEAD_H, 1, LDR_HEAD, head);
    ldr_pic(LDR_WORD_Y, LDR_WORD_W, LDR_WORD_H, 2, LDR_WORD, word);
    ldr_say("UPDATE MODE", "WAITING FOR THE INSTALL", LDR_INK);
    for (i = 0; i < LDR_SEGS; i++)
        ldr_seg(i, LDR_DIM);
    ldr_text(222, 1, LDR_HUB, "thefirmwarehub.com");
    lcd_sync();
}
static uint32_t ldr_at(uint32_t pos) { return pos < LDR_SEGS ? pos : 2u * LDR_SEGS - 2u - pos; }   /* to and fro */
static void ldr_anim(uint32_t ms)                   /* while it waits: a light runs to and fro, its afterglow behind */
{
    uint32_t n = 2u * LDR_SEGS - 2u;
    if (!ldr_idle || (int32_t)(ms - ldr_next) < 0)
        return;
    ldr_next = ms + 60u;                            /* (a step every 60 ms: across in 1.2 s) */
    ldr_seg(ldr_at((ldr_pos + n - 1u) % n), LDR_DIM);    /* the old afterglow goes out */
    ldr_seg(ldr_at(ldr_pos), LDR_TAIL);                  /* the light becomes the afterglow */
    ldr_pos = (ldr_pos + 1u) % n;
    ldr_seg(ldr_at(ldr_pos), LDR_COLOUR);
    lcd_sync();
}
static void ldr_bar(uint32_t done, uint32_t total)
{
    uint32_t n = done * LDR_SEGS / total, i;         /* (the app area: below 2^32 / 20) */
    uint32_t p = done * 100u / total;               /* (the app area * 100: below 2^32) */
    if (!ldr_writing || n < ldr_lit) {              /* a write starts (again) */
        ldr_idle = 0;
        ldr_say("WRITING", "DO NOT SWITCH OFF", LDR_INK);
        for (i = 0; i < LDR_SEGS; i++)
            ldr_seg(i, LDR_DIM);
        ldr_lit = 0;
        ldr_writing = 1;
        ldr_percent(ldr_pct = 0);
    }
    for (; ldr_lit < n && ldr_lit < LDR_SEGS; ldr_lit++)
        ldr_seg(ldr_lit, LDR_COLOUR);
    if (p > 100u)
        p = 100u;
    if (p != ldr_pct)                               /* (the number only when it changes: few fills) */
        ldr_percent(ldr_pct = p);
    lcd_sync();
}
static void ldr_failed(void)                        /* a session that wrote nothing or stopped: the way out */
{
    uint32_t i;
    ldr_say("UPDATE FAILED", "INSTALL AGAIN", LDR_BAD);
    for (i = 0; i < LDR_SEGS; i++)
        ldr_seg(i, LDR_DIM);
    ldr_percent(ldr_pct = 0xFFFFu);
    lcd_sync();
    ldr_writing = 0;
    ldr_idle = 0;
}
