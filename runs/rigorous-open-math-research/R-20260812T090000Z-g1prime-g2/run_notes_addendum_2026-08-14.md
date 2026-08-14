# Run addendum R-210 (2026-08-14): M3 large-R cascade structure (STRICT) with the reduced seed, hard-constant forcing, and open numerical root of the corrected branch

Continuation of R-20260812T090000Z-g1prime-g2, obligation M3 (n=2 symmetric
INF branch, R -> infinity asymptotics of the band self-consistency system).
All numerics are EVIDENCE unless flagged STRICT.  This addendum supersedes
the "next actions" plan of the intereupted handoff (handoff-interrupted-
2026-08-13T151546Z.md) for the level-by-level cascade.

## 0. Setup and notation (recalled, all STRICT)

u = R^(-1/6); eps = u^3 = 1/sqrt(R).  The closed 4-equation system
(scripts/_gapn2_largeR_closed.py, verified 1e-12 against the spectral engine
at R=350 in R-207) is written in the ansatz

    k2 = K u,   k3 = K u + C u^5,   p1 = pi/2 + a u^2,
    p3 = pi/4 + b u^2,   eps = u^3,

where K, a, b, c (= C) are full integer-power series in u.  Here and below I
write a = A, b = B, c = C to match the P coefficient dict, and a_j = A_j,
b_j = B_j, c_j = C_j for the series coefficients.  The four equations are
E1, E2, E5, E6 = 0 (exact closed forms; see the Pbuild script), with the
exact truncated coefficient dict P = scripts/_gapn2_largeR_P.pkl.

The three K-independent denominators in E2, E5, E6 are cleared by multiplying
E2 by K^2, E5 by K^5, E6 by K (E1 has none).  Because K > 0 on the physical
branch (K ~ 3.46), this does not change the zero set.  STRICT.

## 1. STRICT: level-0 and level-1 constraints

Substituting the series into the pre-cleared P and collecting coefficients,
the leading equations are exactly (sympy, this session):

    E1_0 = -sqrt(2)/4 (a0 K0 - 2)
    E2_0 =  sqrt(2)/4 K0^2 (a0 K0 - 2)
    E6_3 = -K0 (a0 K0 - 2)
    E5_2 = -K0^2/48 (a0 K0 - 2) * F(a0,b0,c0,K0)

with F the displayed quadratic.  Hence

    (Level 0)  E1_0 = E2_0 = E6_3 = 0  <=>  a0 K0 = 2,     (STRICT)

and E5_2 = (a0 K0 - 2) * F vanishes automatically once a0 K0 = 2 (so at level
0 the three multiplicative equations carry the SAME single constraint, and
E5_2 contributes no independent constraint at this order).

At level 1 the coefficient equations are

    E1_1 = -sqrt(2)/4 (a0 K1 + a1 K0)
    E2_1 =  sqrt(2)/4 K0 (3 a0 K0 K1 + a1 K0^2 - 4 K1)
    E6_4 = - (2 a0 K0 K1 + a1 K0^2 - 2 K1)

Using a0 K0 = 2, all three reduce to the single relation

    (Level 1)  a1 = - 2 K1 / K0^2 .                          (STRICT)

This is the exact statement of the handoff's "A_1 = a0*K1 + a1*K0 vanishes
identically on the branch": E1_1 = -(sqrt(2)/4)(a0 K1 + a1 K0) = 0, and
combining E1_1 with E6_4 gives a1 K0^2 = -2 K1.  Note that level 1 leaves K1
FREE: the odd-in-u component is, at this order, only the relation a1 = f(K1).

## 2. STRICT: the reduced seed (levels 0-2) and the hard-constant mechanism

Substituting a0 = 2/K0 and a1 = -2 K1/K0^2 into the remaining seed equations
gives (sympy-exact; only the structurally relevant variables are shown):

    E1_2 = -sqrt(2)/(24 K0^2) * [ 6 a2 K0^3 + K0^4 + 12 K0 K2
           - 18 pi K0 + 24 K0 - 12 K1^2 ]
    E2_2 =  sqrt(2)/24 * [ 6 a2 K0^3 + 3 pi c0 K0^2 + K0^4 + 12 K0 K2
           - 18 pi K0 - 24 K0 - 12 K1^2 ]
    E6_5 = -1/(12 K0) * [ 12 a2 K0^3 + 3 pi c0 K0^2 + 2 K0^4 + 24 K0 K2
           - 36 pi K0 - 24 K1^2 ]
    E5_4 = (quadratic in a2, c0, K2; no b0, b1)
    E5_5 = -1/(96 K0^3) * [ ... - 48 K0^6 + (linear in K1, C1) + O(K1^3) ]
    E5_6 = (first order at which b0 appears, linearly)

Three consequences are STRICT and are the main structural result of this
continuation:

  (S1) E1_2, E2_2, E6_5 are AFFINE-LINEAR in (a2, K2, c0), with K1 entering
       only through K1^2.  Eliminating a2, K2, c0 from the three linear
       equations is elementary; the consistency of E1_2 = E2_2 = E6_5 = 0 is
       a single scalar condition, and E5_4 (quadratic) is the level-2
       consistency that pins the joint seed.

  (S2) b0 and b1 do NOT appear in E1_2, E2_2, E6_5, E5_4, E5_5; the first
       equation containing b0 is E5_6.  Equivalently b(u) is determined only
       at order u^6, one level later than the assignment in the handoff.

  (S3) THE HARD-CONSTANT MECHANISM (slightly sharpened).  The raw coefficient
       P['E5',5] = 1/(2 K^2) is a hard constant (independent of a,b,c).  After
       K-clearing (x K^5) and series substitution, the u^5 coefficient of E5
       carries the constant term 48 K0^6 /(96 K0^3) = K0^3/2 (# 20.63 for
       K0 = 3.46), plus terms LINEAR in K1 and C1, plus O(K1^3, K1^5,
       K1*C1, ...).  Therefore the u^5 equation E5_5 = 0 is

           K0^3/2  +  (something)*K1  +  (something)*C1  +  O(K1^3)  =  0,

       which is IMPOSSIBLE if K1 = C1 = 0.  Hence every solution branch has a
       NONZERO odd-in-u component; the even-only ansatz (K1 = A1 = B1 = C1 =
       0) is structurally inconsistent.  This is the STRICT failure mechanism
       (handoff: "E5_5 = 1/(2K^2) is a hard constant"); it is here reproduced
       and localized to the pair (K1, C1) as the first forced odd variables.

  (S4) Higher-level linearity.  For j >= 3, by the same truncated series
       argument, the coefficient of u^n in each of E1_n, E2_n, E5_{n+2},
       E6_{n+3} is an AFFINE function of the level-j unknowns (K_j, a_j, b_j,
       c_j): the only way a level-j variable contributes is linearly (one
       factor carrying u^j, all others at order 0), while the constant part
       is computed from the already-solved lower levels.  Thus, provided the
       resulting 4x4 coefficient matrix is nonsingular, each level j >= 3
       determines (K_j, a_j, b_j, c_j) uniquely.  The nonsingularity is a
       nonvanishing exact determinant; it is NOT yet computed in closed form
       (OPEN, see Section 5).

## 3. EVIDENCE: attempted numerical solution of the reduced seed

The reduced seed + higher levels were solved by least_squares on the exact
pre-cleared equations with the truncated power-dict arithmetic
(scripts/_gapn2_cascade_num3.py, _gapn2_cascade_reducedseed.py).  This is the
numerical part; it does not constitute proof.

  - A 40-unknown unconstrained solve (all series coefficients through u^10)
    with the handoff fit seed CONVERGED TO A NON-PHYSICAL ROOT: the solver
    left the physical branch (A0*K0 -> 0.0063 instead of 2, K0 -> -0.0075,
    K2 -> -1.4e4) with residual 7e-1.  Mechanism: the system carries three
    redundant copies of the single constraint a0 K0 = 2 (E1_0, E2_0, E6_3)
    and eleven E5 orders; the residual weights let least_squares trade the
    physical constraint against the degenerate E5 orders.  This is a solver
    failure, not a mathematical obstruction.

  - The reduced-seed solver (a0 = 2/K0 and a1 = -2 K1/K0^2 enforced exactly,
    19 unknowns, orders E1_{2,4,6,8}, E2_{2,4,6,8}, E5_{4,5,6,7,8},
    E6_{5,7,9}) did not finish within the session budget: the per-evaluation
    sp.Poly + truncated-power rebuild on the huge E2/E5 polynomials is too
    slow for least_squares' numerical Jacobian (hundreds of evaluations).

Consequently the CONCRETE corrected-branch coefficients (the nonzero odd
corrections K1, C1, and the corrected b0, c0, K2, ...) are NOT yet numerically
isolated in a clean, converged sense, and the leading observables below are
carried at the even-only seed with their EVIDENCE values from the handoff
free-exponent fits (scripts/_gapn2_largeR_fit.py, _gapn2_largeR_sigma_fit.py),
which themselves are EVIDENCE (extrapolation u -> 0 of the 270-row
continuation scripts/_gapn2_largeR_big.json to R = 8.99e4).

## 4. EVIDENCE: leading observables (STRICT formulas, EVIDENCE numbers)

Formulas (STRICT, from k2 = K u, k3 = K u + C u^5, D = lam3 - lam2 = k3^2 -
k2^2, R = u^-6):

    Dk   := k3 - k2 = c(u) u^5   =>   Dk/u^5 = c(u) -> c0,  Dk/u^7 = c(u)/u^2,
    D*R  = (2 K c u^6 + c^2 u^10)/u^6 = 2 K c + c^2 u^4  ->  2 K0 c0,
    a0 K0 = 2  (STRICT identity, Section 1).

Numbers (EVIDENCE, seed K0 = 3.4553, b0 = 0.2898, c0 = 1.4741):

    a0 = 2/K0 = 0.578821  (matches the fit a0 = 0.5788 to 5e-4; STRICT identity
    verified against the EVIDENCE fit),
    D*R -> 2 K0 c0 = 10.18692  (data last row D*R = 10.8806 at R = 8.99e4,
    monotonically decreasing along the continuation; the limit 10.18692 is a
    lower extrapolation),
    Dk/u^5 = c(u) -> c0 = 1.47410,  hence Dk/u^7 -> c0/u^2 = 1.47410/u^2,
    consistency candidate C := 1 + b K/2 + 3 pi/(2 K) - K^2/12 = 1.86956 at
    the even-only seed (NOT zero, as required: C = 0 holds only on the
    corrected branch carrying the odd components).

Sector determinants (EVIDENCE only, inherited from addendum e Section 5b,
unchanged): det Kp_odd ~ R^{-7/2}, det Ko ~ R^{-9/2} along the INF branch
(local exponents -3.46..-3.55 and -4.49..-4.55, drifting toward -7/2 and
-9/2); both stay positive and decay to 0+.  Their leading coefficients remain
OPEN (route (iii), R-202).

m3D - m3N: the mass-difference observable is defined by the Pbuild half-masses
(ID = m1D + m3D + mL, IN = m1N + m3N + mLN); its leading terms are carried by
the corrected branch and are NOT yet closed numerically (blocked by the same
seed root as Section 3).  OPEN.

## 5. Status and precise remaining gap

STRICT (this continuation, R-210):
  - Pre-clearing of the K denominators preserves the zero set.
  - Level 0:  a0 K0 = 2 (exact).
  - Level 1:  a1 = -2 K1 / K0^2 (exact); K1 remains free at this order.
  - Reduced seed equations E1_2, E2_2, E6_5, E5_4, E5_5, E5_6 displayed
    sympy-exact; E1_2/E2_2/E6_5 affine-linear in (a2, K2, c0); b0,b1 first
    appear at E5_6.
  - Hard-constant mechanism: E5_5 = K0^3/2 + [linear in K1, C1] + O(K1^3)
    forces a nonzero odd component; even-only ansatz structurally impossible.
  - Level j >= 3 is affine in (K_j, a_j, b_j, c_j) with the constant part
    determined by lower levels (formally; the 4x4 nonsingularity is asserted,
    not yet computed in closed form).

EVIDENCE (this continuation):
  - a0 = 2/K0 matches the fit a0 = 0.5788 (identity check, not a proof).
  - D*R -> 2 K0 c0 = 10.18692; Dk/u^5 -> 1.47410; consistency candidate
    1.86956 != 0 at the even-only seed (confirms odd components are needed).
  - The unconstrained numerical solve was captured by a spurious non-physical
    root (solver failure, Section 3).

OPEN (M3 not closed):
  - The corrected-branch seed root (K0, K1, C1, b0, c0, K2, a2, ...) has NOT
    been solved to convergence in exact or high-precision floating form; the
    concrete odd corrections and the corrected leading observables
    (m3D - m3N, the value of C = 0, and the sector-determinant leading
    coefficients) are still missing.
  - The 4x4 level-j coefficient determinant (uniqueness of the cascade at
    each level j >= 3) is asserted structurally but not computed in a closed
    symbolic form.

The precise failure recorded: the reduced-seed least_squares could not
complete in-session because the per-evaluation sp.Poly + truncated-power
rebuild is too expensive for a 19-parameter numerical Jacobian; and the
40-parameter unconstrained solve escaped to a non-physical branch.  The
recommended fix (for the next action) is to precompile the reduced residual
once with the truncated power-dict (eq_coeff in _gapn2_cascade_num3.py, which
builds correctly and fast) parameterized by the 19 reduced unknowns with the
two identities encoded via dict substitution, then run a single lambdified
least_squares; the precompile for the full 40-parameter system already builds
correctly (27 orders, term counts listed in the num3 run).

## 6. Scripts (all under scripts/)

- _gapn2_largeR_cascade.py: STRICT cascade driver (level-0/1/2 seed equation
  extraction with the pre-cleared P).
- _gapn2_cascade_seed.py: joint 12-unknown seed system (orders 0..5).
- _gapn2_cascade_reduce.py: reduced seed (a0 = 2/K0, a1 = -2K1/K0^2) giving
  E1_2/E2_2/E6_5/E5_4/E5_5/E5_6 (STRICT).
- _gapn2_cascade_den.py / _gapn2_cascade_deg.py: denominator and degree audit.
- _gapn2_cascade_timing.py / _gapn2_cascade_num3.py: truncated power-dict
  feasibility; num3 builds the full 40-unknown system correctly (27 orders).
- _gapn2_cascade_num.py / num2.py / _gapn2_cascade_reducedseed.py: numerical
  root attempts (spurious / incomplete; EVIDENCE, see Section 3).
- _gapn2_observables.py: STRICT-formula leading-observable arithmetic.
- Scrap diagnostics (_gapn2_cascade_explore.py, explore2.py, wip.py, diag.py,
  diag2.py) kept as artifacts of the speed investigation.

## 7. R-211 (2026-08-14): decisive corrected-seed solve; the truncated
##    integer-power branch does NOT exist at K0 ~ 3.46

The R-210 recommended fix was implemented exactly (scripts/
_gapn2_cascade_reduced_final.py, then _gapn2_seed_correct.py and
_gapn2_seed_multistart.py): the reduced residual was built ONCE with the
UNAMBIGUOUS full-substitution eq_coeff (the truncated power-dict version of
num3 was found and retired: _gapn2_pddiff_debug.py showed it mis-builds the
series substitution at order 2, dropping the a2 K0^3 / 12 K0 K2 / -12 K1^2
terms), parameterized by the reduced unknowns with a0 = 2/K0 and
a1 = -2 K1/K0^2 enforced, and solved by scipy least_squares.

### 7.1 STRICT: corrected dependency structure of the seed

With the correct full-substitution coefficients, the reduced seed has this
exact dependency structure (K0-cleared):

    E1_2 : {K0, K1, K2, A2}
    E2_2 : {K0, K1, K2, A2, C0}
    E6_5 : {K0, K1, K2, A2, C0}
    E5_4 : {K0, K1, K2, A2, C0}
    E5_5 : {K0, K1, K2, A2, C0, C1}
    E5_6 : {K0, K1, K2, A2, B0, C0, C1}
    E5_7 : {K0, K1, K2, A2, B0, B1, C0, C1}
    E6_7 : {K0, K1, K2, A2, B0, B1, C0, C1}

So (STRICT): the odd corrections forced by the hard constant E5_5 land on the
pair (C1, K1); the first appearance of C1 is E5_5 and of B0, B1 is E5_6, E5_7.
K1 enters E1_2..E5_4 only through K1^2, but enters E5_5..E6_7 linearly, so K1
is NOT pinned at the even level 2 but only jointly with C1 at level 3 (E5_5).

### 7.2 EVIDENCE: the truncated seed has no root at K0 ~ 3.4 (decisive)

Twenty independent starts (K0 in {3.0, 3.4, 3.5, 3.6} x K1 in {0, +-0.3, +-1})
on the 8-equation seed E1_2, E2_2, E6_5, E5_4, E5_5, E5_6, E5_7, E6_7 all
converged to solutions with K0 -> 0 (K0 in 0.001..0.02, smallest residual
1.3e-10); NONE converged to K0 ~ 3.4.  The K0 -> 0 attractor is the degenerate
"empty" limit (K = sqrt(lambda) -> 0, mass vanishes); the physical R -> inf
branch is NOT a zero of the truncated integer-power system at these orders.

Conclusion (honest): the free-exponent fit limit K0 ~ 3.4553 (an EVEN-only
ansatz fit to the 270-row continuation) is NOT a solution of the exact
truncated 4-equation system E1=E2=E5=E6=0 at orders through u^7.  Either
(i) the true large-R branch carries appreciable odd components in K (K1 != 0)
that shift the EVEN leading value away from 3.4553 and require solving the
coupled seed {K0, K1, C0, C1} jointly (the K0 -> 0 attractor may be masking a
genuine root at nonzero K0 not reachable from these seeds), or (ii) the actual
asymptotic expansion is not a pure integer-power series (slower corrections,
e.g. powers of 1/log R, consistent with the handoff's 1/logR fit caveat).
This is recorded as the precise obstacle: the truncated integer-power branch
through u^7 does not reproduce the K0 ~ 3.46 limit; resolving it requires a
joint nonlinear solve of {K0, K1, C0, C1} with continuation in the odd
directions, or a Puiseux/log correction ansatz.

M3 remains NOT closed.  Status stays RIGOROUS_PARTIAL_RESULT.

Scripts added: _gapn2_cascade_reduced_final.py, _gapn2_seed_correct.py,
_gapn2_seed_multistart.py, _gapn2_reduced_dof.py, _gapn2_reduced_reconcile.py,
_gapn2_pddiff_debug.py.
