# Formalization progress: DensBC O1

Run: `R-20260816T000000Z-densbc-o1`
Status: `RIGOROUS_PARTIAL_RESULT`
Formalization mode: `SCAFFOLD` (not verified)

## New results in this run (partial/structural)

- STRICT structural theorems for DensBC O1: projection-density, obstruction
  moment system, run/first-obstruction, diagonal reduction, finite-rank
  structure.
- Reduced open core: `O1'` (moment-realizability / membership step).

## Lean files

- `lean-proof/SL/ProjectionDensity.lean` — DensBC O1 Theorem 1 abstract core
  (continuous surjection maps dense sets to dense images; orthogonal
  projection onto a closed subspace is a continuous surjection). Status:
  formalized, `lake build` passed, sorry/axiom 0.
- `lean-proof/SL/DensBCEmpty.lean` — DensBC O1 Lemma 6.1 abstract core (empty
  candidate family closure spans `{0}`; dense empty family forces `V = {0}`).
  Status: formalized, `lake build` passed, sorry/axiom 0.

## Remaining scaffold obligation

- `O1'` (moment-realizability / membership step) is not yet formalized. When
  the remaining core is closed or further structural progress appears, create
  `lean-proof/SL/DensBC_O1_core.lean` as a scaffold with declarations and open
  obligations marked `-- SCAFFOLD`, then update this file and
  `lean-proof/STATUS.md`.

## Rule

Per plugin rule (2026-08-16): every new result, even partial, must have a
Lean scaffold and formalization-progress registration. This file is the
registration point for this run.
