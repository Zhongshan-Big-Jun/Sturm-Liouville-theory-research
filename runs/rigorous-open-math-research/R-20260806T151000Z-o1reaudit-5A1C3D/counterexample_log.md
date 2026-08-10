# Counterexample log - independent re-audit of O1 Lemma 1 and Lemma 3

## C-001 - Edge configurations tested (no counterexample)
- Barrier [1,R,1], well [R,1,R], 4-block alternating [1,R,1,R,1],
  single-jump [1,R] and [R,1], barrier-vs-well pairs, random 6-block pairs,
  R = 4 fixed plus R-dependence reasoning (R -> 1+).
- All HS-bound, Weyl, comparison, FH-sign, and stationarity checks passed.

## C-002 - Boundary cases of the theorem statement
- a = b (rho = 1, D = 3 pi^2); (a,b) = (0,1) (rho = R, D = 3 pi^2/R);
  a = 0, b = 1 (2-block members); jumps at 0 or 1 (zero measure effect).
- All inside the closed families; no counterexample.

## C-003 - F-001 chain arithmetic
- Attacked the corrected chain on 11 random/hostile pairs: I1 <= ||A||_2^2/16,
  I2 <= ||A||_1^2/16, ||A||_2^2 <= (R-1)||A||_1, ||A||_1^2 <= (R-1)||A||_1,
  (R/32)(||A||_2^2 + ||A||_1^2) <= (R^2/16)||A||_1.  All hold; the
  pre-correction line (R/16)||rho - sigma||_2^2 was confirmed NOT derivable.

## C-004 - Attacked Lemma 3's stationarity claim
- Tested the one-sided distance derivatives at interior extrema of the
  symmetric barrier family (u*): right ~ -0.0144, left ~ +0.0144 (opposite
  signs, both near zero), f(u*) ~ 2.9e-7 ~ 0.  Consistent with
  (c_+ - c_-) f(x_j) = 0 at an extremum.  No counterexample.

## C-005 - Attacked the two-sided differentiability claim
- At every tested jump position x_j, the central difference (two-sided
  derivative) of eps -> D(rho_eps) converged to -(c_+ - c_-) f(x_j) as eps
  -> 0, including positions where f(x_j) != 0.  Confirms F-002's correction:
  the two-sided derivative exists everywhere; only the distance derivatives
  flip sign unless f(x_j) = 0.  No counterexample.

## C-006 - Attacked the smoothing limit
- Dirac family point evaluation: error O(delta^2) -> 0 (C^2 mollifier).
- Smoothed moving-jump derivative: within 0.03-0.3% of the Dirac limit for
  delta in [0.002, 0.04]; residual is the block discretization of the smoothed
  density.  No counterexample.

## C-007 - Attacked the HS bound and Weyl chain
- 11 random/hostile pairs: ||S_rho - S_sigma||_HS <= (R/4)||A||_1^{1/2}
  (ratios 0.073-0.165) and |1/lambda_k(rho) - 1/lambda_k(sigma)|
  <= ||S_rho - S_sigma||_HS in all 22 cases.  No counterexample.

## C-008 - Check-method artifact (NOT a counterexample)
- The first independent moving-jump check used a fixed-grid finite-difference
  solver; sub-cell jump motion (eps << grid spacing) produced grid-pinning
  artifacts (spurious O(1) derivatives for eps = 2e-4 with grid 1/3000).
- Diagnosed: the FD eigenvalue error depends on the jump position relative to
  the grid; sub-grid motion is not resolved.  Replaced by the exact
  transfer-matrix solver; all checks then passed to 1e-6.  Recorded as F-102
  (method), no mathematical consequence.

## Conclusion
No counterexample to any claim under audit.  All tested domains are recorded
above; universal truth is claimed only where an analytic proof is given in
audit_report.md Sections 2-4.