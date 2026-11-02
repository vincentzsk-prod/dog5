/* SPDX-License-Identifier: GPL-3.0-only */
/* GROWL, the preamp drive: stage 1 of the Psych Chain (CLAUDE.md section 6). It runs on the summed voice bus,
 * clamped and shifted to the output stage's own scale (>> 2), before the output stage, the delay and the reverb,
 * so CC 7 never changes how hard it is driven. Integers only. Pass-through for now. */
static void drive_block(const patch_t *p) { (void)p; }
static void drive_process(int32_t *s, uint32_t n) { (void)s; (void)n; }
