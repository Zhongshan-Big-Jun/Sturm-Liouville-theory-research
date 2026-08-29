# Run audit report

## Verdict

`VERIFIED_REPLICATION`, with no new standalone theorem promotion.

## Checks

- Isolation chronology: PASS. The independent result and Whiteboard checkpoint were frozen before Blueprint retrieval.
- Model binding: PASS. The replication used the exact source four-equation system and sector conventions.
- Seed equations: PASS. The cubic seed and `A0`, `B0`, and `C0` values were reproduced symbolically.
- Observable signs: PASS. The mass difference and upstream scalar agree with direct symbolic reduction.
- Full determinant reconstruction: PASS as high-precision formal computation. Both matrices were rebuilt from transfer data, and the first nonzero terms were stable under higher truncation and free-jet changes.
- Finite-u regression: PASS as EVIDENCE. Exact-equation roots and full Jacobians show the predicted scaling and signs.
- Exact coefficient-field certificate: NOT COMPLETED in this independent run. No theorem claim is based on that attempt.
- Independent review of the theorem: supplied by the separate accepted Blueprint package, not by this run. The final Blueprint review verdict is `approve`, and the integration receipt status is `merged`.

## Correction of the prior project state

The 2026-08-14 staged cascade claimed a hard odd-correction obstruction. The accepted Blueprint proof reconstructs the exact closed D-side mass and shows that the staged builder used incorrect powers of `u`. The old obstruction and its log-correction follow-up are therefore superseded, not additional branches of the corrected theorem.

## Remaining project-level scope

M3 is closed only in its stated n=2 symmetric INF, finite-nonzero-interior, large-R scope. Global n>=2 reflection symmetry and all-R control still require the remaining `(G1')` and `(G2)` obligations outside this M3 closure.
