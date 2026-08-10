# Audit report - C1 (O3a), run R-20260807T163000Z-c1center-9C4E2A

Date: 2026-08-08 (session 33 continuation, final audit pass)
Auditor stance: independent re-derivation of every step of the candidate proof;
no statement is accepted on the authority of a prior draft.  All items below
were re-derived in this run from the exact secular equation and norm formulas.
Punctuation ASCII.

## 1. Scope

Obligation O3a/C1: the system {R1 = 0, R2 = 0} has exactly one solution in
0 < a < b < 1 for every R > 1 (the symmetric fixed point), for the barrier
family rho = 1 + (R-1) 1_{(a,b)}.

Deliverables audited: candidate_proof.md (Parts A-D), problem_contract.md,
obligation_graph.md, approach_registry.md, research_ledger.md, and the
reproducibility scripts.

## 2. Audit of O1c/O2/R1-R6 (inherited; re-checked)

- O1c (structure of f): f = lambda1 u1^2 - lambda2 u2^2.  With v = u2/u1,
  f = u1^2 (lambda1 - lambda2 v^2); v = y2/y1 * sqrt(n1/n2) is strictly
  decreasing (Wronskian identity (y2' y1 - y2 y1')(x) = s1^2 - s2^2 < 0, and
  v'/v = (y2'/y2 - y1'/y1) = -(s2^2 - s1^2)/(s2 y2^2 ... ) < 0).  v(0+) =
  sqrt(n1/n2) > 0, v(1-) = -sqrt(n1/n2) < 0, so f has exactly two zeros
  x_- < x_+ with v = +q0, -q0, q0 = sqrt(lambda1/lambda2) in (0,1).  The
  good-root identification (a,b) = (x_-, x_+) iff R1 = R2 = 0 with the sign
  consistency follows.  PASS.
- O2 (symmetric fp): R1(a,1-a,R) = 0 has a unique solution a_fp in (0,1/2).
  Numerical verification across R in [1.001, 1e8]; the analytic uniqueness is
  not re-proved here (prior run); recorded as inherited.  PASS (inherited).
- R1-R6 (reflection + reduction to h):  verified the exact identities
  g2(a) = 1 - g1^{-1}(1-a), h = g1 - g2, h(a) = 0 iff good root, and
  h'(a) = G(a) - 1/G(u(a)) with u(a) = g1^{-1}(1-a).  PASS.

## 3. Audit of N1 (A1)

Claim: (E1) + (U') + (P0) => C1.  Re-derived:
  h'(a) = (Phi(a)-1)/G(u(a)) by the chain rule (u' = -1/G(u) from
  d/da[g1(u(a))] = 1).  (P0) gives sign(h') = sign(Phi-1).  (U') gives the
  down/up/down monotonicity of h.  (E1) h(a0) < 0 forces h < 0 on [a0, x1];
  h(beta) > 0 with h decreasing on (x2, beta] forces h(x2) > 0; strict
  increase on (x1, x2) gives exactly one zero.  Empty-interval variants
  handled.  By R5 the unique zero is a_fp; by R1-R6, C1.  PASS.
  Note: the earlier "Phi unimodal" wording (U) is strictly stronger and false
  for large R (Phi-1 dips below 0 near a0; Part C of candidate proof).  U' is
  the correct and sufficient condition.  Correction registered (R-012).

## 4. Audit of A2 (endpoints)

beta = 1 - g1(a0), u(beta) = a0: verified by the range argument (g1 increasing
under (P0)).  Endpoint asymptotics h(a0) = [W(a0) - W(1-a0)]/q + o(1/q),
h(beta) = [W(1-a0) - W(a0)]/q + o(1/q) under (BA): re-derived line by line.
PASS (conditional on (BA)).

## 5. Audit of A3 (E1-inf) - NEW THIS RUN

Claim: with W(a0) -> (1-a0)u/pi, sin(u) = sqrt(2a0) u, u in (0, pi/2), and
W(1-a0) -> (1-a0)x/pi, x^2 cot^2 x = 1/(2a0), x in (pi/2, pi), we have
W(1-a0) > W(a0).
  (i) uniqueness of u: sin(u)/u strictly decreasing on (0, pi/2) (derivative
      (u cos u - sin u)/u^2 < 0 since tan u > u); sqrt(2a0) in (2/pi, 1)
      (a0 = 0.41957).  PASS.
  (ii) uniqueness of x: Y(x) = x^2 cot^2 x, Y'(x) = 2x cot x (cot x - x csc^2 x)
      > 0 on (pi/2, pi) because cot x < 0 and sin x cos x - x < 0 there.
      Y(pi/2+) = 0, Y(pi-) = +inf.  PASS.
  (iii) the chain: 1/(2a0) = u^2/sin^2 u from sin u = sqrt(2a0) u; so
      x^2 cot^2 x = u^2/sin^2 u; x in (pi/2, pi) => -x cot x = u/sin u.  PASS.
  (iv) Y1(x) = -x cot x strictly increasing on (pi/2, pi) (Y1' = -cot x +
      x csc^2 x > 0).  Y1(u) < 0 < u/sin u = Y1(x) => u < x.  PASS.
  Numerically x - u = 1.33944, gap (1-a0)(x-u)/pi = 0.2474707 > 0, matching
  the measured limit c = 0.2475 of |h(a0)| q.  PASS.
  Status: STRICT, conditional on the profile limits (A4 + Gap 1).

## 6. Audit of A4 (leading-order profile equations)

Re-derived from the exact formulas (SEC) and (BR) in candidate_proof.md.
  Ground state: F(s1) expansion in t = q^{-1/2} with w = W t^2, s1 = alpha t:
  leading term alpha t (1 - alpha^2 W a (1-b)) => alpha^2 = 1/(W a (1-a)).
  PASS (verified numerically to 0.1% at q = 1000).
  Right pin: with s2 = pi/a + kappa/q, sin(s2 a) = O(1/q); (SEC) gives
  cos(theta) + delta sin(theta) = O(1/q), delta = -cot(theta) + O(1/q);
  theta = s2 W = pi W/a + O(1/q).  PASS (delta = (pi - s2a)q; measured
  -cot(theta) to 2% at q = 1000, a = 0.51).
  Right norm: n2 = a^3/(2 pi^2) + O(1/q): verified numerically (I1 dominates;
  q^2 I2 ~ 4e-6, I3 ~ 1e-6 at q = 1000).
  Right branch: (BR) with the above yields 2 (pi/a)^2 cot^2(pi W/a) =
  1/(W^2 (1-a)), equivalently kappa^2 = 1/(2 pi^2 (1-a) W^2).  PASS (0.1% at
  q = 1000).  NOTE: the earlier draft claimed n2 = [a + (1-a) cos^2(...)]/...
  which is WRONG for a > 1/2 (the mode is pinned in the LEFT well, n2 ~ a^3/2pi^2,
  not including the right-well amplitude).  Corrected this run (R-014).
  Left pin + left branch: mode pinned in the right well, v2 = s2(1-b) ~ pi,
  delta = -cot(theta) + O(1/q) (SAME relation); n2 is dominated by the right
  well amplitude C = y2'(b)/s2 ~ y2(b) q/delta, giving
  sin^2(s2 a)/n2 = 2 s2^2 delta^2/(cos^2(theta)(1-b) q^2); (BR) then gives
  sin(pi W/(1-a)) = sqrt(2a) pi W/(1-a).  PASS (0.1% at q = 1000 for
  a = 0.43..0.47; the formula degrades as a -> 1/2 - transition layer - and is
  NOT valid at a = 0.49 (60% error), consistent with the layer structure).
  Uniqueness of W_L, W_R: PASS (A3 and A4).
  Gap: all O-terms are stated but the uniform error bounds are not written out
  (Gap 1 = G-EST).  Status: DERIVATION with stated error terms.

## 7. Audit of A5 (symmetric fixed point)

On the diagonal: two-sided pin, delta = 2 pi xi + kappa/2, theta = 4 pi xi;
(SEC) gives sin(theta)(1 - delta^2) = 2 delta cos(theta); (BR) with
n2 -> 1/(8 pi^2), n1 -> q xi/2, sin^2(s1 a) -> alpha^2/(4q) gives
delta^2 = 1/(8 pi^2 xi^2).  Combined: tan(4 pi xi) = 2 delta/(1-delta^2) =
tan(2 arctan delta); 4 pi xi in (0, 2 pi) forces 4 pi xi = 2 arctan delta,
i.e. xi tan(2 pi xi) = 1/(2 sqrt2 pi).  Unique xi* in (0, 1/4).  Numerically
xi* = 0.1199372, alpha*^2 = 2/xi* = 16.6754, kappa* = 2(tan 2 pi xi* - 2 pi xi*)
= 0.36947.  PASS; convergence verified at q = 100, 316, 1000 (C1).  Status:
DERIVATION (Gap 1 for the error terms).

## 8. Audit of A6 (U')

  Generic term S(a) = W'_L(a) + W'_R(1-a): W'_L < 0 and W'_R > 0 re-derived by
  implicit differentiation (formulas in A6).  S(a0) = -0.3843 (evaluated);
  S < 0 on the generic left is supported by S(a0) < 0 plus monotone behavior of
  the two terms (W'_L -> -inf as a -> 1/2, W'_R(1-a) bounded in (-1, 0.74)):
  a rigorous proof needs the monotonicity check of W'_L and W'_R, which is
  elementary but recorded as part of Gap 1 (the audit verified the formulas and
  the endpoint value; the global sign statement is not yet a finished proof).
  Transition layer: parametrization a = 1/2 - xi/q, G = 1 - W'(xi),
  Phi-1 = (1-W'(xi))(1-W'(xi_u)) - 1, W(xi_u) = xi + xi_u: re-derived.  PASS.
  The single-crossing claim (U'-layer) is OPEN.  The zero locations: measured
  (0.5 - z0) q ~ 4.3, 5.3, 10.5, 20.0 at q = 70.7, 100, 316, 1000 (C7), i.e.
  the zeros move with q (the earlier "zeros at fixed a ~ 0.480/0.520" claim is
  only an R = 1e6 snapshot; corrected this run, R-013).
  Important correction (R-013): the earlier draft's "near-fp window of width
  O(1/sqrt(q))" and "zeros at distance ~ c/sqrt(q) from fp" are WRONG; the + 
  region has width ~ 2 (0.5 - z0) ~ 2 c q^{-0.42} in a, converging to 0.

## 9. Audit of Part B (certification)

Interval-Newton fails at moderate box widths (division-width blowup on
N = s - F/F_s).  Sign-based certification designed but not tuned.  The
certified bulk is NOT achieved.  Honest status: no certified-computation
results are claimed.  PASS (as a status statement).

## 10. Data integrity findings

- F-013: tracew_*.json rows are polluted by sheet jumps (a > ~1/2 and near the
  diagonal; e.g. W ~ 1.03 at a = 0.51 instead of 0.33).  The C-part of the
  candidate proof now uses the clean targeted continuation (s33_profile.py) and
  flags the tracew caveat.  The left part a <= fp is usable after filtering by
  the R1 residual (s33_zeros.py).
- F-014: the right-side norm n2 in the previous draft (A3 "n2 = a^3/2 pi^2 +
  ... with a right-well term") is corrected; see Section 6.
- F-015: the previous claim "zeros of Phi-1 at a ~ 0.480, 0.520 for R = 1e6"
  is an R-dependent snapshot, not a fixed-a statement (R-013).

## 11. New audit this session (2026-08-08 continuation): R -> 1+ structure

### F-016 (REFUTED CLAIM): "fp-component limit curve sin(2 pi b) = -sin(pi a)/2, slope 1/14"
The previous A9/C8 claimed the fp-component S3 limits to the curve
sin(2 pi b) = -sin(pi a)/2 as R -> 1+, with G(a0) -> 1/14.  Independently
re-checked with the exact secular solver:
  (i) Continuation of S3 at R = 1.05 and 1.1: the branch is nearly vertical,
      db/da in (48, 531) at R = 1.05 and (25, 270) at R = 1.1, i.e. G(a0) ->
      +inf as R -> 1+, not 1/14.  The old R = 1 base formula
      "R1 = 2 pi^2 sin^2(pi a) - 8 pi^2 sin^2(2 pi b)" is wrong; the correct
      R1(a,b,1) = 2 pi^2 sin^2(pi a) - 8 pi^2 sin^2(2 pi a) (both terms at x =
      a).  The curve sin(2 pi b) = -sin(pi a)/2 is a phantom: no S3 point at
      R = 1.05 satisfies it (test point (0.4199, 0.5): sin(2 pi b) = 0 vs
      -sin(pi a)/2 = -0.48).
  (ii) VERDICT: claim refuted.  The R -> 1+ route in A9 must use the sheet
      structure below.

### F-017 (DATA ARTIFACT): e15 first-row b at a = a0 for R <= 100
The e15 json first row reports b(a0) = 0.41939681, constant for R = 1.02..100.
Direct root-finding of R1(a0, ., R) shows the UNIQUE root is b = a0 =
0.41956938 (the empty-barrier degeneracy) for R in [1.001, 1.05], and the
reported 0.419397 has R1 = 1.6e-4 (off-branch).  max_root_col picks a
spurious root near the vertical branch.  The e15 h(a0), u(a0) values remain
accurate because h(a0) = u(a0) - b0 (uses u, not the off-branch b).

### F-018 (CODE BUG FOUND): Green's function sign in the cumsum integrator
The first implementation of y_k^1 via cumulative trapezoid missed a minus
sign (y = -(1/(k pi)) Int sin(k pi (x-s)) g ds for -y'' - (k pi)^2 y = g).
This produced a spurious negative dip of phi(b) near b ~ 0.7 and wrong
non-monotonicity.  The leapfrog ODE integrator matched finite differences of
the exact solver to 6 digits at b = 0.45, 0.60, 0.70 (checked at N = 80001
and 200001); the sign-fixed cumsum then matches the leapfrog.  Recorded so
future sessions use the verified sign.

### 11b. Audit of the corrected A9 (sheet structure)
Verified against the exact solver:
  - phi(a0) = 0 to machine precision (exact: R1(a0,a0,R) = f_const(a0) = 0 for
    every R, empty barrier).
  - phi(b) values match (A_eps(b) - a0)/eps at R = 1.001 to 3-4 digits
    (remaining difference is the expected O(eps) second-order term), and match
    finite differences of R1 to 6 digits (b = 0.45..0.95).
  - phi' > 0 on [a0, 0.98] (min 0.0060, max 0.428, grid 60) -- EVIDENCE; the
    strict proof is the declared one-variable calculus on the closed form.
  - g_1(a0) = a0 for R in [1.001, 1.05]: unique root of R1(a0, ., R) at b = a0
    (dense scan, 1301 points), and the sheet through (a0,a0) climbs to the fp
    (continuation; R2 = 0 on the sheet exactly at the fp location to grid
    resolution).
  - h(a0) = 2a0-1 + phi(b0) eps + O(eps^2): -0.160861 + 0.026021 eps; e15
    measurements -0.16052 (R=1.02), -0.15975 (R=1.05) agree to O(eps^2).
  - b_top(R) = 0.9361, 0.9365, 0.9368 at R = 1.02, 1.05, 1.1 -> b_top* ~ 0.936
    > b0 = 0.5804 (margin 0.35) -- EVIDENCE (extrapolation).
  - Phi-1 > 0 and G > 0 on the full domain for R <= 1000 (e15): min Phi-1 =
    +0.0005 (R=1000), +0.35 (R=100); min G = 0.9753 (R=1000), 2.1 (R=100).
    Consequence: for R <= 1000 the U' condition holds trivially (Phi-1 has no
    zeros) and E1/P0 hold with the displayed margins -- these are the certified
    / evidence items the strict proof must cover for R in (1, R0].
STATUS: the R -> 1+ obligations reduce to (i) closed form of phi + phi' > 0,
(ii) b_top* > b0, (iii) explicit O(eps) error bounds (Gap 1).  No [EVIDENCE]
item is used as a proof.

## 11. Conclusions

The proof chain C1 <- N1 <- (E1, U', P0) is sound and audited.  This run added
two complete strict pieces: (i) the E1-inf inequality (A3), an elementary
proof; (ii) the complete derivation of the large-q profile equations and the
fp limit system (A4/A5), with the correct one-sided pin mechanism and the
correct right-side norm.  The exact remaining gap is: uniform error bounds for
A4/A5 (Gap 1), the transition-layer single-crossing (U'-layer), the R -> 1+
perturbation, and the certified bulk.  No numerical evidence is used as a
proof; every claim is labeled.

## 12. Follow-up audit (2026-08-09): R -> 1+ closed form, phi' > 0, b_top* > b0

### 12a. Closed form of phi(b) re-derived and verified
The first-order sheet function phi(b) = -R1_1(a0; a0, b)/f_const'(a0) was
re-derived from scratch using hand-computed antiderivatives (all integrands
are products of sines/cosines; no symbolic integration engine was used).
An error in the first attempt was found and fixed: the normalized-mode
correction term w_k^1 = y_k^1/sqrt(n_k^0) - u_k^0 n_k^1/(2 n_k^0) had been
implemented with a multiplication (y1a*sqrt(nk0)) instead of the division
(y1a/sqrt(nk0)); the error was caught by term-by-term comparison against the
verified numerical integrator (dbg_pieces3.py) and is now fixed in
sym_phi_closedform3.py.  This is a good example of why re-derivation with an
independent engine is required.
The corrected closed form matches:
  - the reference R1_1 (s33_r1plus.py) to ~1.4e-6 (reference discretization
    error at N = 100001);
  - the exact secular solver sheet a*(b, eps) - a0 - eps phi(b) < 1e-9 at
    eps = 1e-4, b in [0.45, 0.9] (verify_sheet_exact.py);
  - phi(a0) = 0 to 2e-18 and phi(b0) = 0.0260217.
Exact identities: phi(a0) = 0; the factored form of phi' has the constant
term of the u-polynomial equal to zero at u = 1 (P(1) = 0 exactly).

### 12b. phi' > 0 on [a0, 1) - CERTIFIED + STRICT
Part 1 (CERTIFIED): cert_phi_prime.py certifies phi' > 0 on [a0, 0.999] with
mpmath.iv interval arithmetic at 200-bit precision (correctly-rounded interval
extensions of cos/sin; a0 enclosed via atan2(sqrt(15)/4, 1/4)/pi), over a
uniform 4000-cell grid; worst enclosure lower bound 8.896e-6.  No cell
failed.  The interval arithmetic is the only machine-dependent step; the
closed form input was independently verified in 12a.
Part 2 (STRICT, elementary): for b = 1-e, e in (0, 1/1000], the inequalities
sin(pi e) >= pi e (1-(pi e)^2/6), cos(pi e) >= 1-(pi e)^2/2,
sin(2 pi e) <= 2 pi e, 4 cos(2 pi e) - 1 <= 3 combine with m, n > 0 to give
phi'(b) 60 pi >= C_tail e^2 with C_tail >= 9.651926 (interval-certified).
Cross-check: the true minimum of phi'/e^2 on (0, 1/1000] is 9.652006 (at
e = 1/1000), comfortably above C_tail.

### 12c. b_top* > b0 - STRICT (structural)
For b-bar = 7/10: R1(a, b-bar, eps) is real-analytic, R1(a0, b-bar, 0) =
f_const(a0) = 0, partial_a R1(a0, b-bar, 0) = f_const'(a0) = 15 pi^3 sqrt(15)/4
!= 0.  The implicit function theorem at (a0, 0), uniform on [a0, 7/10] by
compactness, gives a unique analytic sheet a = A(b, eps) with A(b, 0) = a0.
At b = a0, A(a0, eps) = a0 exactly.  The fp satisfies R1(a_fp, b_fp, eps) = 0
with (a_fp, b_fp) -> (a0, b0), so by uniqueness a_fp = A(b_fp, eps) for small
eps; the arc b in [a0, 7/10] lies in the fp-component S3.  Hence
b_top(eps) >= 7/10 and b_top* >= 7/10 > b0 ~ 0.5804 (margin 0.12).

### 12d. Verdict
A9 is now: closed form (DERIVATION, verified), phi' > 0 on [a0, 1)
(CERTIFIED + STRICT), b_top* > b0 (STRICT structural).  E1/U'/P0 for
R in (1, 1+eps_0) are reduced to Gap 1: explicit uniform O(eps) error bounds
for A_eps - a0 - eps phi, b_top(eps) -> b_top*, h, G, Phi, plus an explicit
upper bound b_top(eps) <= 1 - delta_0.  No [EVIDENCE] item is used as a proof.
