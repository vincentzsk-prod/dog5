/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments */
/* The flash map: which ranges the RAM flash driver (fm1_flash.h) may erase / program. Macros and compile-time checks only, so host tests can include it. */
#pragma once
#include <stdint.h>
#include "fm1_cc.h"

/* [off, off + n) inside [lo, hi), without wrapping: off + n can overflow, and
 * the 1 MiB part ignores the high address bits, so a wrapped range lands low. */
#define FL_IN(off, n, lo, hi) ((uint32_t)(off) >= (lo) && (uint32_t)(off) <= (hi) && \
                               (uint32_t)(n) <= (hi) - (uint32_t)(off))
/* The flash chip the app's storage and the update loader accept (JEDEC id from 0x9F). One place
 * for the app (platform.c, recovery.c) and the loader (loader.c); extend it here for another part. */
/* FM-1: the Puya P25Q80 (0x856014); newer units from AliExpress carry a UC25HQ80 (0xB36014, 1 MiB – Paul Nederhoed,
 * 2026-11-02: SAVED (RAM), projects lost at power-off). The driver uses only generic SPI NOR commands (as above). */
#define FL_JEDEC_OK(id) ((id) == 0x856014u || (id) == 0xB36014u)

#define FL_PLAIN_LO     0x00093000u                /* plain XIP window from the FM-1 VM start */
#define FL_DATA_LO      0x00097000u                /* Felucca main store */
#define FL_DATA_HI      0x000E0000u
#define FL_GLOB_LO      0x000FC000u                /* Felucca superblock / globals */
#define FL_GLOB_HI      0x000FF000u
#define FL_OTA_LO       0x000E0000u                /* M-UPGRADE loader staging, ota.c */
#define FL_OTA_HI       0x000E5000u
/* Felucca's own store (projects, user samples; settings); OberVave's platform.c gives its own FL_RANGE_OK */
#define FL_STORE_OK(off, n) (FL_IN(off, n, FL_DATA_LO, FL_DATA_HI) || FL_IN(off, n, FL_GLOB_LO, FL_GLOB_HI))
/* Where the RAM driver may erase / program. The app build allows only its own
 * data regions; the update loader (firmware/loader) defines its own window. */
#ifndef FL_RANGE_OK
#define FL_RANGE_OK(off, n) (FL_STORE_OK(off, n) || FL_IN(off, n, FL_OTA_LO, FL_OTA_HI))
#endif
#define FL_GUARD(off, n) FL_RANGE_OK(off, n)
