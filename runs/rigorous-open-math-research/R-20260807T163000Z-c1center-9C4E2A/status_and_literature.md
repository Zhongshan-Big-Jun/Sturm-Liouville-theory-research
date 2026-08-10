# Status and literature - premise log for C1 (R-20260807T163000Z-c1center-9C4E2A)

Legend: KNOWN (verified from primary source), DERIVED (proved in this run),
RECALLED_UNVERIFIED (from prior run summaries, not re-verified here),
CONJECTURED, EVIDENCE (numerics only).  All punctuation ASCII.

## P1. Eigenvalue equation and secular equation for the barrier - DERIVED
-y'' = lambda rho y on (0,1), Dirichlet, rho = 1 + (R-1) 1_(a,b).  Transfer
matrix derivation gives the exact secular equation (SEC) in candidate_proof
A4; verified against the fast numerical solver (roots2_fast) to machine
precision on many (a,b,R).  KNOWN structure (Sturm-Liouville standard).

## P2. Feynman-Hellmann and the critical point equivalence - KNOWN (prior)
The band edges of an extremal configuration satisfy f = lambda1 u1^2 -
lambda2 u2^2 = 0 at both edges (prior runs; docs/SL_gap_n1_proof.tex Section 5).

## P3. Wronskian monotonicity of v = u2/u1 - DERIVED
v strictly decreasing; f has exactly two zeros x_- < x_+.  Re-derived in
audit_report Section 2 (O1c).

## P4. Reflection invariance - KNOWN (prior)
(a,b) -> (1-b, 1-a) maps the problem to itself; gives g2 and h (R1-R6).

## P5. Large-q ground state s1 ~ alpha/sqrt(q) - DERIVED
alpha^2 = 1/(W a (1-a)) + O(1/q) from (SEC) at leading order; verified to
0.1% at q = 1000 (s33_profile.json).

## P6. One-sided pinning of s2 - DERIVED
a > 1/2: s2 a ~ pi; a < 1/2: s2 (1-b) ~ pi; delta = -cot(theta) + O(1/q),
theta = s2 W.  Verified (s33_profile.json; audit Section 6).

## P7. Profile equations (P-) and (P+) - DERIVED
(P-): sin(pi W/(1-a)) = sqrt(2a) pi W/(1-a), a < 1/2.
(P+): kappa^2 = 1/(2 pi^2 (1-a) W^2), a > 1/2, with W_R defined by
x^2 cot^2 x = 1/(2(1-a)).  Verified to ~0.1% (q = 1000).  Error bounds: Gap 1.

## P8. fp limit system - DERIVED
xi* tan(2 pi xi*) = 1/(2 sqrt(2) pi), unique in (0, 1/4); alpha*^2 = 2/xi*;
kappa* = 2(tan 2 pi xi* - 2 pi xi*).  Verified (s33_e1.py, verify_profile_asym.py).

## P9. E1-inf inequality - DERIVED (strict)
W_R(1-a0) - W_L(a0) = (1-a0)(x-u)/pi = 0.2474707 > 0, with u, x the explicit
roots (A3).  Numerics: 0.2474707 vs measured |h| q limit 0.2475.

## P10. U' generic sign - DERIVED (calculus; global monotonicity = Gap 1)
S(a) = W'_L(a) + W'_R(1-a); S(a0) = -0.3843; S < 0 on the generic left.
EVIDENCE: q(Phi(a0)-1) = -0.374 at q = 1000.

## P11. U'-layer single crossing - OPEN (CONJECTURED)
EVIDENCE: Phi-1 pattern -+- with zeros moving with q.

## P12. R -> 1+ structure - DERIVED (leading order, verified) / old claim REFUTED
REFUTED (F-016): the earlier claim "fp-component limit curve sin(2 pi b) =
-sin(pi a)/2, slope 1/14 at a0" is false (branch is nearly vertical, G(a0) ->
+inf; the R=1 formula had the wrong second term sin^2(2 pi b)).  Correct:
with eps = R-1, S3 is the sheet a = a0 + eps phi(b) + O(eps^2), b in
[a0, b_top ~ 0.936], phi(b) = -R1_1(a0; a0, b)/f_const'(a0) (closed formulas,
verified to 6 digits); phi(a0) = 0 (exact, empty-barrier degeneracy);
g_1(a0) = a0 exactly for small R; h(a0) = 2a0-1 + phi(b0) eps + O(eps^2) =
-0.160861 + 0.026021 eps < 0; h(beta) -> b_top* - b0 > 0; Phi-1 > 0 and
G > 0 for R <= 1000.  PROGRESS 2026-08-09: phi has a closed form and phi'(b)
factors as -(1-u)(m(1+u)+n) - 2 sqrt15 pi (1-b)(4u-1) v over 60 pi; phi' > 0
on [a0, 1) is CERTIFIED (interval arithmetic, 4000-cell grid, worst lower
bound 8.896e-6) + STRICT (elementary tail bound C_tail >= 9.651926 on
(0.999, 1)); b_top* >= 7/10 > b0 is STRICT (implicit function theorem).
Remaining: explicit O(eps) bounds and b_top(eps) <= 1 - delta_0 (Gap 1).

## P13. phi' > 0 on [a0, 1) - DERIVED (CERTIFIED + STRICT)
phi'(b) 60 pi = (1-u)(m(1+u)+n) + 2 sqrt15 pi (1-b)(4u-1) v with u = cos(2 pi b),
v = sin(2 pi b), m = 56 pi a0 - 6 sqrt15 > 0, n = 2 pi a0 + 3 sqrt15 > 0.
Part 1 CERTIFIED by mpmath.iv interval arithmetic (200-bit, 4000-cell grid on
[a0, 0.999]; worst enclosure lower bound 8.896e-6).  Part 2 STRICT and
elementary on b = 1-e, 0 < e <= 1/1000: phi'(b) 60 pi >= C_tail e^2 with
C_tail >= 9.651926 (uses sin(pi e) >= pi e (1-(pi e)^2/6), cos(pi e) >=
1-(pi e)^2/2, sin(2 pi e) <= 2 pi e, 4 cos(2 pi e) - 1 <= 3, m, n > 0).

## P14. b_top* > b0 - DERIVED (STRICT, structural)
Implicit function theorem for R1(a, b-bar, eps) at (a0, 0), b-bar in
[a0, 7/10], with partial_a R1(a0, b-bar, 0) = f_const'(a0) = 15 pi^3 sqrt(15)/4
!= 0; the fp arc (a_fp, b_fp) -> (a0, b0) lies on the same analytic sheet, so
the arc b in [a0, 7/10] is contained in the fp-component S3; hence
b_top(eps) >= 7/10 and b_top* >= 7/10 > b0 ~ 0.5804.

## Literature
- No new literature was needed in this run: the analysis is self-contained
  from the exact secular/norm formulas.  Prior-run literature (Keller,
  Mahar-Willner, Hedhly, Chu-Meng etc.) is recorded in the portfolio docs
  (docs/SL_spectral_topics_summary.tex) and does not bear on O3a/C1's
  remaining gaps, which are internal to the barrier family.
- Novelty risk: the fp-component uniqueness statement (C1) is internal to
  this portfolio's gap-extremal theorem; no conflicting published result is
  known to us (searched in prior runs; none found).

## Honest status
No premise is marked KNOWN without a source; every DERIVED item above is
either proved in candidate_proof.md or is a leading-order derivation whose
error terms are explicitly delegated to Gap 1.  No EVIDENCE item is used as
a proof.  The 2026-08-09 additions (P13, P14 and the closed form in P12) are
[STRICT PROOF]/[CERTIFIED]/[DERIVATION] as labeled; the numerics that cross-
checked them (verify_sheet_exact.py, verify_phi_closedform2.py) are recorded
as EVIDENCE only.
