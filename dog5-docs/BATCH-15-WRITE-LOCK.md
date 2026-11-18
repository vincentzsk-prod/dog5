# Batch 15 — the write-lock: THE POUND / THE PACK (18 Nov 2026)

Branch `build/batch-15-write-lock`, off `origin/main` 945bc88 (after Batch 14).

## Behaviour

- **THE POUND, programs 1–32, is locked.** They always read the factory patch from the firmware (`prog_get`), so a firmware
  update that revoices a factory patch reaches every unit. Edits on them play as usual; they just can't be saved over.
- **SAVE (BURY):** armed on a PACK slot (33–99), it offers that slot, as before. Armed on a POUND slot, it offers the **first
  free PACK slot** (`pack_free`: the first of 33–99 never saved to; all taken: 33). The header shows it: `33 INIT · SAVE HERE?`.
- **PRESETS while armed** moves through 33–99 only, wrapping 99 ↔ 33; it can never point into THE POUND.
- **Old saves (v0.1 / v0.2 let SAVE write 1–32):** once at power-on (`pound_rescue`), each one moves to the first free PACK
  slot, in order, and its POUND slot reads the factory again. With THE PACK full nothing is overwritten: the old save stays
  where it was, unread. On a unit with nothing saved over 1–32 this does nothing and writes nothing.
- The store below the lock is unchanged (all 99 slots, 3 sectors, `DOG5` tag), so no format change and no migration of
  the file format.

## Proofs

- `tests/controls/write_lock.txt` (new; 11 checks, new host command `expect slot N`): an edit on program 1 saves to 33;
  program 1 still reads the factory CUTOFF (92); the next save from 1 offers 34, PRESETS down twice wraps to 99; from 99,
  PRESETS up wraps to 33; program 1 still the factory. The first check fails on the old code (it saved to slot 1).
- Store selftest (`obervave selftest`, 6 new checks): with saves stored over all 99, 1–32 read the factory and 33–99 the
  user's; the rescue moves old saves on 5 and 21 to 34 and 35 when 33 is taken, frees 5 and 21, marks the sector to save;
  a second power-on moves nothing; with THE PACK full nothing moves. The 99-slot round-trip now checks the store directly.
- Sound unchanged: `tests/drive/bitexact.sh origin/main` byte-identical; `identical_par.py` all 32 patches × 52 phrases
  byte-identical against `main`.
- Device build: image 82,536 B (+272), RAM 32,432 B, pool 304,896 B (both unchanged). `run_tests.sh` ALL TESTS PASSED.
  Web player rebuilt (its SAVE line now explains the lock); `sim_test.mjs` passes.

## Not done

Not on the unit yet: it ships with the 0.3 test build.
