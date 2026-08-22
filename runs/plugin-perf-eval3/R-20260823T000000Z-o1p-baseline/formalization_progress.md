# Formalization progress

Run: R-20260823T000000Z-o1p-baseline

## New scaffold

- File: `lean-scaffold/DensBCO1p3BandShift.lean`
  (copied to `lean-proof/SL/DensBCO1p3BandShift.lean`).
- Header: `SCAFFOLD: DensBCO1p3BandShift RIGOROUS_PARTIAL_RESULT`.
- Declarations:
  - `DensBCO1p3BandShift_main` (finite-rank criterion).
  - `DensBCO1p3BandShift_stable_invertible` (Lemma 0.1).
  - `DensBCO1p3BandShift_v1x4_not_dense` (Theorem 4.1).
  - `DensBCO1p3BandShift_abstract_structure` (Theorem 2.3).
- All are `sorry` placeholders. They are NOT verified.

## Verification tiers

- Tier 0 (scaffold skeleton): created; an attempted `lake env lean` check
  timed out after 120 seconds (Mathlib import/build is heavy in this
  environment). The scaffold is structurally simple but was NOT verified.
  A fresh check with a warm build cache is needed.
- Tier 1 (load-bearing lemma machine-check): not run.
- Tier 2 (full formal proof): not attempted.

## Open formalization obligations

- Formalize the Toeplitz inverse coefficient construction (bounded operator).
- Formalize the run/free-base finite-rank equivalence for the family.
- Formalize the bandwidth-2 example.
- Reuse existing verified lemmas: `ProjectionDensity`, `DensBCEmpty`,
  `DensenessCriteria`, `DensBCO1pDecision` scaffolds where applicable.
