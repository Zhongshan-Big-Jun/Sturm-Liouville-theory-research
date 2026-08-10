# Candidate proof - audited O1 reduction theorem (status: REPAIRABLE_GAP)

This document records the O1 reduction theorem as verified by the audit.  It
is NOT a substitute for the draft: per the task packet, the draft was not
repaired.  The two defects below (O1a operator presentation, O1b sign) must be
fixed by the revising role before the theorem can be labeled PROVED.  All
other steps are audited as correct.

## Theorem (audited statement)

Let R > 1, K = {rho measurable on [0,1] : 1 <= rho <= R a.e.}, Dirichlet
string -y'' = lambda rho y on [0,1], eigenvalues 0 < lambda_1 < lambda_2,
D(rho) = lambda_2 - lambda_1.  Then

(i)  sup_{rho in K} D(rho) = max_{0 <= a <= b <= 1} D(rho = R on (a,b), 1 elsewhere),
(ii) inf_{rho in K} D(rho) = min_{0 <= a <= b <= 1} D(rho = 1 on (a,b), R elsewhere),

and both extrema over the two-parameter families are attained.

## Proof skeleton with obligation marks (as audited)

1. [O1a - PARTIAL] Continuity: lambda_k is continuous in the L^1 topology on K.
   The draft's proof needs the following repair: with G(x,t) = min(x,t)(1-max(x,t))
   and T_rho f = int G(x,t) rho(t) f(t) dt, the eigenvalues of T_rho are
   1/lambda_k(rho), but T_rho is not self-adjoint on L^2.  Use instead the
   symmetric Hilbert-Schmidt operator S_rho = rho^{1/2} T_rho rho^{1/2}
   (kernel sqrt(rho(x)) G(x,t) sqrt(rho(t))), whose eigenvalues coincide with
   those of T_rho; then
   ||S_rho - S_sigma||_HS <= C(R) * ||rho - sigma||_1^{1/2} -> 0,
   and Weyl's inequality gives |1/lambda_k(rho) - 1/lambda_k(sigma)| <=
   ||S_rho - S_sigma||, hence continuity (lambda_k bounded away from 0 and
   infinity on K: lambda_k in [k^2 pi^2/R, k^2 pi^2]).

2. [O1c - PROVED] Structure of f: for any rho in K, with u_1, u_2 the
   L^2(rho)-normalized eigenfunctions, f = lambda_1 u_1^2 - lambda_2 u_2^2
   has at most two zeros in (0,1) and {f > 0} is a single interval containing
   the unique zero z_0 of u_2.  Proof: Wronskian (as in the draft, verified
   against AEH Lemma 2.2).

3. [O1b - FAILED as stated; consequence valid] Moving-jump derivative:
   moving the jump at x_j (values c_- left, c_+ right) right by eps changes D
   at rate -(c_+ - c_-) f(x_j); moving left at rate +(c_+ - c_-) f(x_j).
   (The draft has the opposite sign.)  At an interior extremum over K_N the
   one-sided derivatives force f_N(x_j) = 0 at every effective jump.

4. [O1d - PROVED] Compactness: K_N (at most N jumps, values in [1,R]) is the
   continuous L^1 image of a compact parameter set; D attains its extrema on
   K_N; a minimizing representation of the extremizer has all effective jumps
   interior, so by (3) + (2) it has at most two effective jumps.

5. [O1e - PROVED] Density: block averages give sup_K D = sup over step
   functions = lim_N M_N (and similarly for inf).

6. [O1f - PROVED] Bang-bang: at a global extremizer rho~ (which exists in K_2
   by (4),(5)), the one-sided FH condition dD/dt = int delta rho f~ dx
   (AEH Lemma 2.1) forces rho~ = R a.e. on {f~ > 0} and rho~ = 1 a.e. on
   {f~ < 0} for a maximizer (reversed for a minimizer).  With (2), a
   maximizer is a barrier config and a minimizer a well config.

7. [Synthesis - PROVED given repairs] (i) follows from 4-6 with the barrier
   family; (ii) with the well family.  Attainment: the two-parameter families
   are compact continuous images and D is continuous (O1a).

## Exact repair list for the reviser (do not merge without these)

- R1 (O1a): replace the T_rho-on-L^2 min-max step by the S_rho argument (or
  an exact citation for L^1 continuity of string eigenvalues), and note
  lambda_k bounded away from 0.
- R2 (O1b): correct the sign in Lemma 3 and in the obligation-graph O1b
  statement to -(c_+ - c_-) f(x_j) for rightward jumps; note the one-sided
  derivative asymmetry and that the zero condition f(x_j) = 0 is unchanged.
- R3 (minor): state the sign convention on u_2 in Lemma 2 (as AEH does).
- R4 (minor): justify the moving-jump FH step by approximation (AEH Lemma 2.1
  requires dw/dkappa in L^1, a delta is a distributional limit).

## Not in scope

O2 (symmetric 1-parameter family) and O3 (2-parameter critical point) are
separate open obligations of the draft run; this audit covers O1 only.

## Status label for this document

CANDIDATE (REPAIRABLE_GAP) - the theorem statement is true as audited; the
draft proof is not yet acceptable as written due to R1 and R2.
