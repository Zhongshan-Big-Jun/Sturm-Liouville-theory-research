# Approach registry: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

## Route R-A: branch monotonicity (g1' > g2') and T4
- Mechanism: prove Lemma A pointwise and apply T4.
- Outcome: REFUTED as stated.  h' < 0 on a subinterval near the right end for
  R >= ~1400 (counterexample CE-1).  Verified by three independent numerical
  methods.  The T4 hypothesis (b) fails for large R.
- Salvage: the corrected conjecture C1 (h has exactly one zero) does not need
  monotonicity; an "N-shaped" h with h(a0) < 0 < h(b0) and a single crossing
  would suffice.  Route R-A' (zero-count) is the replacement.
- Lesson: the prior run's verification range (R <= 1000) was too short; the
  failure threshold R* ~ 1350 is close to the tested range boundary.

## Route R-B: Hessian reduction of the branch slopes
- Mechanism: express A, B, C through second derivatives of D
  (A = -D_aa/(R-1), B = D_ab/(R-1), C = D_bb/(R-1)) and reduce Lemma A at the
  fixed point to sign and definiteness conditions on the Hessian of D.
- Outcome: PARTIAL.  The algebraic reduction is proved (P3).  The sign
  estimates (D_aa < 0, D_ab > 0, D_bb < 0 on the branches, and
  D_aa*D_bb > D_ab^2) are numerically true on the branches for R in the
  tested range, but a proof requires controlling second-order spectral sums
  (the "second-order sensitivity" problem flagged by the prior run); no clean
  closed form was found in this run either.
- Note: the Hessian is NOT negative definite on the whole triangle
  (violations near small a, e.g. D_bb > 0 for a ~ 0.08); only the
  branch-restricted signs hold.  A global Hessian argument would be wrong.

## Route R-C: R -> 1+ perturbation analysis
- Mechanism: at R = 1, v(x) = cos(pi x), q = 1/4; branches degenerate to the
  vertical line a = a0 and the horizontal line b = b0; prove Lemma A/B/C for
  small R by perturbation theory.
- Outcome: PARTIAL.  Base facts (P4) proved; the boundary-layer structure of
  the branches for small eps = R - 1 (branch domains I_1 = [a0, a_max1(eps)],
  I_2 shrinking; slopes -> infinity) is numerically established but the
  rigorous perturbation argument was not completed in this run.
- Lesson: the R -> 1 side is the easy side (h' huge, ~48 at R = 1.05), but a
  proof still needs the location of the branch endpoints a_max1(eps), b_min2(eps).

## Route R-D: R -> infinity asymptotics
- Mechanism: matched asymptotics with delta = 1/2 - a_fp ~ 0.118/sqrt(R),
  point-mass limit (lambda_1 -> 0, lambda_2 -> 4 pi^2, D -> 4 pi^2).
- Outcome: NUMERICALLY ESTABLISHED leading-order behavior (delta*sqrt(R) ->
  0.12, h(b0)*sqrt(R) -> 0.38, h'(fp) -> ~0.70); rigorous derivation not
  completed.  The asymptotic of the branch gap near the right end (h' sign
  pattern) remains unexplained analytically.

## Route R-E: counterexample hunting (adversarial)
- Mechanism: search for R and a in the common range with h' <= 0, and for
  extra good roots (second zero of h).
- Outcome: found CE-1 (Lemma A falsification, R >= ~1400).  NO second zero of
  h found for R <= 1e6 (h > 0 on the whole tail, h(b0) > 0).  Spurious
  large-R "fixed points" (e.g. (0.4, 0.6) at R = 1e5) were identified as
  least-squares minima of the residual, not roots, and excluded by the
  good-root checks (residual < 1e-9 AND v-sign AND zero-location check).
- Lesson: absolute residual tolerance is insufficient at large R; relative
  checks and the v-based zero location are required.

## Route R-F: independent verification of the falsification
- Mechanism: three independent implementations (agentB_lib FD, clean_lib FD,
  closed-form implicit derivatives) plus an ODE-shooting cross-check.
- Outcome: all agree; CE-1 is robust at float64 precision.

## Route registry summary
- R-A: REFUTED (as stated)
- R-B: PARTIAL (algebra proved; estimates open)
- R-C: PARTIAL (base facts proved; perturbation analysis open)
- R-D: NUMERICAL (leading order; rigorous analysis open)
- R-E: CE-1 found; no O3a counterexample (up to R = 1e6)
- R-F: completed (3-way agreement)
