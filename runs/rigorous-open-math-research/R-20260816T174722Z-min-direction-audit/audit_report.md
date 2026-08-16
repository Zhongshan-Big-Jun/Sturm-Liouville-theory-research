# Audit Report: `min_direction_progress.tex`

## Verdict

**ACCEPT**

The collaborator's progress report is accepted into the repository. The
supplementary verification package
`collaborator_min_direction_verification/` has been added, and the key
previously-unverifiable certificates have been independently reproduced or
confirmed from the packaged exact outputs.

## Independent adversarial audit

An independent fresh sub-agent reviewed the document and returned
`ACCEPT_WITH_CAVEATS` before the supplementary package was available. After
incorporating the verification package, the material caveats are resolved or
reduced as recorded below.

## Findings / caveats (updated after verification package)

- The source `min_direction_progress.tex` uses `\kappa_0` and `\kappa_D`
  without definitions. The companion package defines them in
  `runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/derivation.md`:
  - `kappa_0 = sqrt(X/Y)(3Y-1)/(1-3X)`,
  - `kappa_D = (X^2+2XY-4X+1)/((1-X)(1-3X))`.
  The progress text itself should ideally reference the companion package or
  include these definitions; this is a documentation improvement, not a
  mathematical error.
- The Bernstein positivity certificate (539 tensor coefficients, 387 positive,
  152 zero, 0 negative) was previously unverifiable. It is now:
  - included in the package JSONs;
  - **independently reproduced locally** by running
    `r10_min_full_interface/independent_bernstein_audit.py` with SymPy
    1.13.1. Output matches the packaged certificate exactly.
- The finite Arb covers (inner cube 5,848,407 boxes; t=0 boundary charts) are
  now included in the package with complete `PASS` outputs and zero
  unresolved/singular boxes. The heavy 5.8M-box Arb run was not re-executed,
  but the packaged JSONs and scripts are hash-bound and available for replay.
- The n=3 four-margin identity is confirmed by the package's
  `charge_compensation/report.md` and independently by our random matrix tests
  with arbitrary gamma endpoints.
- The forest/interval-charge identities are confirmed by re-running
  `det_forest/exact_forest_checker.py`: all checks PASS.
- The general interface and n>=3 mu=2 contraction algebra are confirmed by the
  package's `general_mu_interface` and `r15` exact checkers and by our own
  symbolic/numeric verification.

## What was independently reproduced in this audit

- n=2, mu=2 interface formulas satisfy the general interface momentum
  equations (symbolic).
- General-mu interface mapping formulas satisfy the momentum equations.
- Xi identity in the n=3 shared-contrast section.
- Determinant parity sign identity.
- n>=3, mu=2 contraction algebra and `0<a<1`.
- Weak-contrast Phi rearrangement, square-completion, and positive-margin
  inequalities.
- t=0 boundary analytic inequalities.
- n=3 four-margin identity (random matrix tests, arbitrary gamma endpoints).
- Path-forest formulas and charged-forest reduction.
- **Bernstein positivity certificate (539 coefficients, exact, local replay).**
- **charge_compensation exact checker (PASS).**
- **det_forest exact checker (PASS).**

## Remaining notes

- The full 5.8M-box Arb certificate and the t=0 boundary Arb charts are not
  re-executed in this audit session; they are included as packaged outputs with
  zero unresolved/singular boxes and are available for replay.
- The document itself still does not claim the general n>=2 global reflection
  theorem; it remains Open. This is consistent with the package's
  `PAUSED_REPORT.md`.
