# Approach registry - independent re-audit of O1 Lemma 1 and Lemma 3

Run scope: bounded re-audit; no new research directions.  Routes are audit
mechanisms, not conjecture-solving routes.

## Route A - Analytic from-scratch re-derivation (OWNER: verifier, this run)
- Core mechanism: re-derive Lemma 1 and Lemma 3 line by line without accepting
  the draft, the producer self-audit, or the prior audit as authority.
- Target obligations: O1a, O1b, F-001 chain, theorem-statement fidelity.
- Required known results: operator algebra (S_rho ~ T_rho), Weyl/min-max,
  AEH Lemma 2.1/2.2 (primary source), Sturm oscillation, Rayleigh bounds.
- Status: PROVED (all checks passed).
- Exact gap: none.

## Route B - Independent numerical verification (OWNER: computation, this run)
- Core mechanism: fresh finite-difference solver (fd_lib.py) for the HS/Weyl
  checks and fresh exact transfer-matrix solver (tm_lib.py) for the
  moving-jump and smoothing checks; independent of the audited run's battery.
- Target obligations: O1a (HS bound, Weyl chain, F-001 chain), O1b (sign,
  smoothing limit, stationarity), premise hypotheses (AEH pointwise FH,
  H^2 bounds).
- Status: COMPLETED (all evidence collected; see *out.json).
- Exact gap: evidence only; proof-level claims are argued in Route A.

## Route C - Adversarial sweep (OWNER: counterexample hunter, this run)
- Core mechanism: attack each claim on boundary cases (R near 1, a=b,
  (a,b)=(0,1), 2-block members, alternating 1/R blocks, barrier vs well),
  and attack each check method for artifacts.
- Target obligations: all.
- Status: COMPLETED (no counterexample found; one check-method artifact
  detected and eliminated, see counterexample_log.md F-102).
- Exact gap: none.

## Route D - Consistency read of unchanged obligations (OWNER: verifier)
- Core mechanism: re-read O1c-O1f and the synthesis in the revised text for
  internal consistency and compatibility with the prior independent audit
  (422A69, PROVED).
- Target obligations: O1c-O1f, synthesis.
- Status: COMPLETED (no new gap).
- Exact gap: none within O1 scope; O2/O3 out of scope (draft run owns them).

## Route states
- A: PROVED
- B: COMPLETED (evidence)
- C: COMPLETED (no counterexample)
- D: COMPLETED (consistency only)