/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Vincent Kruger (DØG-5) */
/* The DØG-5 brand palette, as RGB565 (locked 19 Nov 2026; the Project doc DOG-5-brand-palette.md has the hex and where
 * each colour comes from). Thirteen from Chapter II (BEE-TCH), two from the other chapters. Every screen of the app
 * takes its colours from here; the update loader (a separate program) repeats the few it uses in ldr_screen.c. */
#ifndef DOG5_PALETTE_H
#define DOG5_PALETTE_H
#define BR_BLACK 0x0000u                        /* #000000 */
#define BR_PLUM_NIGHT 0x3028u                   /* #320444 */
#define BR_SKY_VIOLET 0x60EBu                   /* #621C5D */
#define BR_RAY_RED 0xE063u                      /* #E20D1D */
#define BR_RAY_PINK 0xEAAFu                     /* #EC5579 */
#define BR_SUN_YELLOW 0xFE66u                   /* #F8CD30 */
#define BR_SUN_GLOW 0xFFF2u                     /* #FFFF93 */
#define BR_WAVE_TURQUOISE 0x1635u               /* #10C5AF */
#define BR_DEEP_TEAL 0x0391u                    /* #007289 */
#define BR_FOAM_WHITE 0xFFFFu                   /* #FFFFFF */
#define BR_PALM_LIME 0xA7EAu                    /* #A3FF52 */
#define BR_JUNGLE 0x01A0u                       /* #033504 */
#define BR_JUNGLE_DEEP 0x00C2u                  /* #001913 */
#define BR_ACID_CHARTREUSE 0xDFA0u              /* #DEF402, from IV ACID CAN: the loudest accent */
#define BR_GRIME_OLIVE 0x848Du                  /* #84926C, from I JALOPY */
#endif
