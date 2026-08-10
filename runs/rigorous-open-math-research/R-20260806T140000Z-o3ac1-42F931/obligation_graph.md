# Obligation graph (run R-20260806T140000Z-o3ac1-42F931)

Graph nodes: ID | statement | depends on | status.  Root theorem first.

## ROOT

ID: O3a
Statement: the sign-consistent critical point of D = lambda_2 - lambda_1
over the barrier family rho_(a,b), 0 < a < b < 1, R > 1, is unique up to
reflection sigma(a,b) = (1-b, 1-a).
Quantifiers: for every R > 1.
Depends on: C1 (via T1, T2, P1-P3 reductions; see below).
Status: OPEN.  Equivalent to C1 by Lemma R5(ii)-(iii) and the prior-run
reductions T1-T3.

## Core chain

ID: C1
Statement: for every R > 1, h = g1 - g2 has exactly one zero in the common
range I = [a0, beta]; the zero is a_fp(R).
Quantifiers: for every R > 1; beta = min(a_max1(R), b0).
Depends on: E1, M, Z, H2 (branch structure), O2 (existence of fp).
Evidence/status: OPEN (numerically verified over R in {1.02..1e7}).
Reduction (this run, Lemma R6): C1 <= E1 + M + Z.
Known edge cases: R -> 1+ (I degenerates to {a0}); R -> inf (beta = b0,
h(b0) ~ 0.38/sqrt(R) -> 0+).
Verifier notes: the naive sufficient condition g1' > 1 on I is refuted
(CE-3); the integral identity R4 is the exact object to attack.

ID: E1 (endpoint signs)
Statement: h(a0) < 0 and h(beta) > 0 for every R > 1.
Depends on: definitions of branch endpoints; P4 (R=1 base); asymptotics.
Evidence/status: OPEN.  Numerically verified; h(a0) ~ -0.38/sqrt(R),
h(beta) ~ +0.38/sqrt(R) for large R.
Verifier notes: when beta = b0, h(beta) > 0 is g1(b0) > b0; at R -> 1+ both
endpoints collapse to a0 and h -> 0, so the proof must control the first
order in (R-1) and the sign at the collapse point.

ID: M (M-shape of h')
Statement: h' has at most two zeros x1 <= x2 in (a0, beta); if two, they are
simple, x1 < fp < x2, h(x1) < 0 < h(x2), and h' < 0 near a0 and near beta
(sign pattern - + -); if none, h' > 0 on I.
Depends on: R3, R4 (h' = g1'(a) - 1/g1'(u(a))), the shape of g1'.
Evidence/status: OPEN.  Numerically verified: R <= ~1350 -> h' > 0 on I;
R >= ~1500 -> right dip; R >= ~3000 -> both dips; |h'| <= ~0.012.
Verifier notes: h'(fp) > 0 for all tested R, converging to ~0.70 as R -> inf.

ID: Z (h(fp) = 0)
Statement: the symmetric fixed point a_fp(R) is a zero of h.
Depends on: O2 (existence of fp as a good root), H2 (coverage), R5.
Evidence/status: PROVED conditional on O2 + H2 (Lemma R5(iii): fixed points
of J are exactly zeros of h; fp is a fixed point of J by definition).
Verifier notes: O2 is a separate obligation in the portfolio chain, assumed
available here (stated in problem_contract.md section 2).

## Proved structural lemmas (this run)

ID: R1
Statement: R1(sigma(a,b)) = R2(a,b) and R2(sigma(a,b)) = R1(a,b) for all
0 < a < b < 1, R > 1.
Depends on: definition of f, reflection y(x) -> y(1-x), norm equality.
Status: PROVED (elementary).  Verified to 1e-16 at generic points.

ID: R2
Statement: sigma maps the main-sheet Gamma_1 onto the main-sheet Gamma_2;
on I, g2(a) = 1 - g1^{-1}(1-a).
Depends on: R1, sign tracking c_v = y_2'(1)/y_1'(1) < 0, H2
(single-component structure of the main sheets).
Status: PROVED modulo H2 (the sign-tracking part is complete; the
identification of the image with the main-sheet component uses H2's
single-component statement, which is part of Lemma C and remains OPEN).
Verified: max|R2| on the image ~1e-9..1e-11 for R in {2,4,100,1000,1e4}.

ID: R3
Statement: h(a) = g1(a) - 1 + u(a), h'(a) = g1'(a) - 1/g1'(u(a)),
u(a) = g1^{-1}(1-a).
Depends on: R2, inverse function theorem (g1' > 0 on I, verified).
Status: PROVED.

ID: R4
Statement: h(a) = integral_{u(a)}^a (g1'(t) - 1) dt on I.
Depends on: R3, FTC.
Status: PROVED.  Corollary: sign(h) = sign(a - u(a)) * sign(g1'(xi) - 1).
Note: the naive sufficient condition "g1' > 1 on I" is FALSE (CE-3).

ID: R5
Statement: (i) R1 = R2 = 0 with 0 < a < b < 1 forces a sign-consistent good
root; (ii) on I, h = 0 iff (a, g1(a)) is a good root; (iii) on I, h = 0 iff
a = J(a) = 1 - g1(1 - g1(a)).
Depends on: O1c (v strictly decreasing, f has at most two zeros).
Status: PROVED.  Consequence: C1 iff {R1 = R2 = 0} has a unique solution in
0 < a < b < 1 iff Gamma_1 cap Gamma_2 is a single point.

ID: R6
Statement: C1 follows from (E1) + (M) + (Z).
Depends on: E1, M, Z.
Status: PROVED (elementary monotonicity argument).

## Proved premises rechecked from the source run (R-20260806T011500Z-o3abranch-E8E56F)

ID: P1
Statement: FH formulas with the eigenvalue factor; dD/da = -(R-1) R1,
dD/db = (R-1) R2.
Status: PROVED (rechecked; FD 1e-6).

ID: P2
Statement: dR1/db = -dR2/da.
Status: PROVED (rechecked; ~1e-8 at four points).

ID: P3
Statement: branch-slope identities; at the symmetric fp g1' g2' = 1,
h' = g1' - 1/g1'.
Status: PROVED (rechecked; g1' g2' = 1 to ~1e-12).

ID: P4
Statement: R = 1 base facts (v = cos(pi x), q = 1/4, a0, b0).
Status: PROVED (rechecked by direct computation).

ID: O1c
Statement: v strictly decreasing on (0,1); f has at most two zeros.
Status: PROVED (prior run + AEH arXiv:2407.02459v2 Lemma 2.2, v2, checked).

ID: T1-T3 (prior-run reductions)
Statement: good root <=> fixed point of T; T sigma = sigma T; dR1/db =
-dR2/da.
Status: PROVED (rechecked; T3 = P2).
ID: T4 (conditional uniqueness from monotonicity of h)
Status: NOT USABLE.  Hypothesis (g1' > g2' pointwise) is REFUTED (CE-1,
interval certificate).  Logically sound as a conditional only.

## Open assumptions from the portfolio chain (not proved in this run)

ID: O2
Statement: a symmetric fixed point a_fp(R) with (a_fp, 1-a_fp) a good root
exists for every R > 1.
Status: ASSUMED (separate obligation O2 in the portfolio; this run uses it
only through Z).

ID: H2 (Lemma C structure)
Statement: Gamma_1, Gamma_2 are single connected graphs over I_1, I_2 with
real-analytic branch functions; every good root lies in I.
Status: OPEN (hypothesis).  Multi-sheet hazards documented (CE-4): extra
points with R2 = 0, v(b) < 0, v(a) < 0 exist at large R and are excluded by
the main-sheet convention; they are not sign-consistent fixed points.

## Edge cases tracked (see counterexample_log.md)

- R -> 1+: I degenerates; branches vertical/horizontal; perturbation route
  degenerate (BLOCKED, ledger R-108).
- R -> inf: fp -> 1/2, lambda_1 -> 0, lambda_2 -> 4 pi^2, h(b0) ~
  0.38/sqrt(R).
- a = b: zero-width barrier, rho = 1, not a good root for R > 1.
- Near-diagonal roots (b - a ~ 4e-4 at large R): required geometric scans
  (ledger R-104).
- Multi-sheet Gamma_2 at R = 1500, a = 0.57364: three R2-roots with v(b) < 0;
  only the largest is the main sheet (CE-4).

## Overall graph status

ROOT O3a: OPEN, reduced to C1 (C1 <= E1 + M + Z, all three OPEN/PARTIAL).
All supporting premises P1-P4, O1c, T1-T3, R1-R6 audited; T4 discarded.