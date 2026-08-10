# Audit report: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

## 1. Scope and method
Audit of (a) the authoritative source
R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md (theorems T1-T4,
Lemma A/B/C statements), (b) the task packet Q-20260806-o3a-branch-E8E56F,
(c) the numerical methods used in this run.  The auditor role was executed by
the run itself: every premise was re-derived or re-verified against primary
sources or first principles; every computational claim was checked with at
least two independent implementations where it mattered.

## 2. Audit of the theorems (verdict: SOUND, with one formula clarification)

T1 (fixed points = sign-consistent critical points = good roots).
Sound.  Depends only on O1c (at most two zeros of f, single positive
interval) and the sign pattern.  O1c re-verified (Wronskian argument).

T2 (sigma-equivariance; uniqueness implies b = 1 - a).
Sound.  Reflection maps the barrier family to itself, preserves Dirichlet
data and eigenvalues (simplicity), and maps zeros of f accordingly.

T3 (dR1/db = -dR2/da).
Sound.  The proof in the source uses dD/da = -(R-1) R1 and dD/db = (R-1) R2
with D = lambda_2 - lambda_1, then Schwarz.  AUDIT FINDING: the formula is
correct only when the Feynman-Hellmann derivative carries the eigenvalue
factor, d lambda_k/d eps = -lambda_k int rho_eps u_k^2 dx (P1).  This run
re-derived the formula, initially using the version without the lambda
factor and obtaining a contradiction with finite differences; the correct
version matches finite differences to 1e-6 and confirms the source's
numerical claim (dD/da = 38.88731049 = -(R-1) R1 at (0.42, 0.56, 4)).
The identity dR1/db = -dR2/da itself was re-verified to ~1e-8 at four
points.  No other issue found in T3.

T4 (conditional uniqueness).
Sound as a conditional.  AUDIT FINDING: hypothesis (b) (g1' > g2' on the
common range) is FALSE for R >= ~1400 (CE-1), so T4 cannot be applied for
large R.  Hypotheses (a) and (c) are numerically supported but unproved.
The conclusion of T4 (at most one fixed point) is numerically true for all
tested R, so the failure is in the sufficiency route, not in the claim.

## 3. Audit of the lemma statements (verdict: Lemma A REFUTED; B, C OPEN)

Lemma A (g1' > g2' > 0 pointwise on the common range, all R).
REFUTED rigorously (this continuation upgraded the finding).  Witness
R = 1500, a = 0.57364 (inside the common range): h' = -0.000344
(closed-form implicit derivatives).  An interval-arithmetic certificate
(reproducibility/cert_ce1.py, mpmath.iv, outward-directed rounding,
iv.prec = 220) now proves h'(a*) in [-3.4298e-4, -3.4298e-4] < 0 with
verified root enclosures (width ~5e-28), sign-definite partials and
denominators, and certified good-root checks; the same at R = 1e4 gives
h' in [-3.2030e-3, -3.2030e-3] < 0.  The packet's "R-uniform positive
lower bound" is false (min h' -> 0 as R -> infinity), and the pointwise
inequality fails for R >= R* in (1200, 1500).  The prior run's
verification range (R <= 1000) did not reach R*, which is why the
failure was missed.

Lemma B (h(a0) < 0 < h(beta)).
OPEN.  Verified numerically for R in {1.02, ..., 1e7}; h(b0) ~ 0.38/sqrt(R).
The R -> 1+ perturbation analysis needed for a proof was started (base facts
P4 proved) but not completed.

Lemma C (single-graph branches; coverage).
OPEN.  Verified numerically for R <= 1e6 (single smooth branch components;
exactly one zero of h).  No proof strategy was completed.

## 4. Audit of the numerical methods

1. Solver independence: the finding CE-1 was reproduced with (i) the prior
   run's agentB_lib (FD of branch roots), (ii) clean_lib (FD of branch
   roots), (iii) closed-form implicit derivatives (closed_check.py), and
   (iv) an ODE-shooting cross-check (qualitative).  Methods (i)-(iii) agree
   to ~1e-6 or better; CE-1 is not a single-implementation artifact.
2. FD stability: h' computed with steps h = 1e-6..1e-4 gives identical
   results (-0.003203 at R = 1e4), and direct h(a) values confirm the
   monotone decrease.  Branch roots have residuals ~1e-13..1e-14 with
   correct v-signs, ruling out root-selection errors.
3. Known limitations: at very large R (>= 1e6), the agentB_lib config()
   can fail (v-sign assertion) for near-degenerate narrow-barrier configs;
   absolute residual tolerances are scale-dependent (spurious least-squares
   minima were found and excluded); ODE-shooting precision (~2.5e-4 grid)
   is insufficient for the h' sign at the needed accuracy; the interval
   certificate inherits the trust model of mpmath.iv (standard verified
   computation, not a machine-checked formal proof).  All limitations are
   documented in the ledger.
4. No randomized computation was used; all grids are deterministic.

## 5. Exact remaining gaps
- G1: CLOSED (2026-08-06).  Interval-arithmetic certificate proves
  h'(a*) < 0 at (R, a*) = (1500, 0.57364) and (1e4, 0.57364); Lemma A
  rigorously refuted.  (The certificate itself is reproducible from
  reproducibility/cert_ce1.py; its trust model is mpmath.iv outward
  rounding, standard but not formally machine-checked.)
- G2: proof of C1 (unique zero of h), i.e. O3a; includes Lemma C structure
  and the endpoint signs of Lemma B.
- G3: proof of Lemma B (endpoint signs) and Lemma C (single graphs +
  coverage) as stated; note the multi-sheet structure of Gamma_2 found in
  this run (extra points with R2 = 0, v(b) < 0, v(a) < 0), which must be
  excluded by the fixed-point-relevant branch definition.
- G4: asymptotic proof that h(b0) - (dip) > 0 for all large R.

## 6. Verdict
The prior-run reduction T1-T4 is mathematically sound (with the FH formula
clarification P1).  The task's Lemma A is REFUTED, now with a rigorous
interval-arithmetic certificate (G1 closed).  Lemmas B and C remain open;
O3a (unique fixed point) is numerically supported but unproved, and the
T4 route requires a corrected hypothesis.  No complete proof of O3a was
obtained in this run.
