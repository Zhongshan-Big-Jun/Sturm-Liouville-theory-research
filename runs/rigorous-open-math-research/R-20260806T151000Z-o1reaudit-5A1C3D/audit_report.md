# Audit report - independent re-audit of O1 Lemma 1 and Lemma 3

- Audit run: R-20260806T151000Z-o1reaudit-5A1C3D
- Task packet: agenda/task-packets/Q-20260806-o1-reaudit-5A1C3D.md
- Audit target: runs/rigorous-open-math-research/R-20260806T140000Z-o1revise-2ED02A/candidate_proof.md
  (REVISED O1 proof; Lemma 1 and Lemma 3 are the changed points; F-001 already
  repaired in the delivered text)
- Mode: READ-ONLY with respect to the audited artifact.  The candidate proof
  was NOT modified.  All files ASCII punctuation, UTF-8 no BOM.
- Scope: bounded re-audit of the two changed points (per the packet):
  Lemma 1 (O1a, L^1-continuity via S_rho) and Lemma 3 (O1b, moving-jump
  Feynman-Hellmann with the corrected sign), plus the F-001 repair-chain
  arithmetic, the theorem-statement fidelity, and every premise against its
  primary source.  O1c-O1f were re-read for internal consistency only (their
  from-scratch independent audit was run R-20260806T011500Z-o1audit-422A69,
  verdicts PROVED); no new gap was found in the re-read.

## Status label (verbatim)

INDEPENDENTLY_AUDITED_PROOF

Scope of the label: the O1 reduction theorem (sup_K D = max over the barrier
family, inf_K D = min over the well family, attained) with all obligations
O1a-O1f and the synthesis closed.  O2/O3 (symmetric 1-parameter and 2-parameter
analysis) remain open obligations of the portfolio problem and are OUT of this
run's scope.  The two changed points were re-audited from scratch in this run;
the unchanged points rest on the prior independent audit (PROVED) plus this
run's consistency read.  Details in Section 11.

## 1. Verdict summary

| Obligation | Prior audit (422A69, on the draft) | This run (on the revised text) | Basis |
|---|---|---|---|
| O1a (Lemma 1, L^1 continuity) | PARTIAL (draft invalid as written) | PASS | Section 2 |
| O1b (Lemma 3, moving-jump FH) | FAILED-as-stated (sign error) | PASS | Section 3 |
| O1c (structure of f) | PROVED | consistent, no new gap | Section 6 |
| O1d (compactness, <= 2 jumps) | PROVED | consistent, no new gap | Section 6 |
| O1e (step functions dense) | PROVED | consistent, no new gap | Section 6 |
| O1f (bang-bang) | PROVED | consistent, no new gap | Section 6 |
| Synthesis (SUP/INF, attainment) | PROVED | consistent, no new gap | Section 6 |
| Theorem statement fidelity | HIGH | PASS | Section 5 |
| F-001 repair chain | repaired in delivered text | VERIFIED (arithmetic) | Section 4 |

Verdict taxonomy (upstream skill): PASS, REPAIRABLE_GAP, PARTIAL, FAILED,
NOT_VERIFIABLE.  No obligation in this run's scope received anything but PASS.
Two presentational notes are recorded (F-101, F-102); neither is a
mathematical gap and neither changes any proof step.

## 2. O1a - Lemma 1: L^1-continuity of lambda_k on K (re-derived from scratch)

### 2.1 Statement under audit

For every k >= 1 and rho, sigma in K = {1 <= rho <= R a.e.}:
  |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
  <= (R/4) ||rho - sigma||_1^{1/2},
hence |lambda_k(rho) - lambda_k(sigma)| <= (R/4)(k^2 pi^2)^2 ||rho-sigma||_1^{1/2}.

### 2.2 Operator algebra (repair R1)

T_0 = (-d^2/dx^2)^{-1} on L^2(0,1), Dirichlet, with Green kernel
G(x,t) = min(x,t)(1 - max(x,t)); G symmetric, 0 <= G <= 1/4.  T_rho := T_0 M_rho.
The symmetric Hilbert-Schmidt operator is S_rho := M_{sqrt(rho)} T_0 M_{sqrt(rho)}
with kernel sqrt(rho(x)) G(x,t) sqrt(rho(t)).

Similarity (checked step by step):
  M_{sqrt(rho)} T_rho M_{sqrt(rho)}^{-1}
    = M_{sqrt(rho)} (T_0 M_rho) M_{1/sqrt(rho)}
    = M_{sqrt(rho)} T_0 M_{sqrt(rho)} M_{sqrt(rho)} M_{1/sqrt(rho)}
    = M_{sqrt(rho)} T_0 M_{sqrt(rho)} = S_rho.
Since 1 <= sqrt(rho) <= sqrt(R), M_{sqrt(rho)} is bounded with bounded inverse
M_{1/sqrt(rho)}; hence S_rho and T_rho are similar and their spectra coincide.
S_rho is self-adjoint, positive, Hilbert-Schmidt (symmetric bounded kernel
bounded by R/4; positivity via S_rho = T_0^{1/2} M_{sqrt(rho)}
(T_0^{1/2} M_{sqrt(rho)})^*).

The packet/audit notation "rho^{1/2} T_rho rho^{1/2}" is NOT symmetric as
written (kernel sqrt(rho(x)) G(x,t) rho(t) sqrt(rho(t))); the delivered
text's NOTE is correct and the kernel form S_rho is the right object.

Eigenvalue identity: -y'' = lambda rho y with Dirichlet BCs is equivalent to
T_0(rho y) = y/lambda, i.e. T_rho y = y/lambda; then
  S_rho (sqrt(rho) y) = M_{sqrt(rho)} T_0 (rho y) = (1/lambda) sqrt(rho) y.
With the descending order mu_1 >= mu_2 >= ..., mu_k(S_rho) = 1/lambda_k(rho).

### 2.3 Hilbert-Schmidt bound with the F-001-corrected chain

A(x) := |rho(x) - sigma(x)|, Delta(x,t) := sqrt(rho(x))sqrt(rho(t))
- sqrt(sigma(x))sqrt(sigma(t)).  Then
  |Delta(x,t)| <= sqrt(rho(t)) |sqrt(rho(x)) - sqrt(sigma(x))|
                + sqrt(sigma(x)) |sqrt(rho(t)) - sqrt(sigma(t))|
  <= (sqrt(R)/2) (A(x) + A(t)),
because |sqrt(u) - sqrt(v)| = |u-v|/(sqrt(u)+sqrt(v)) <= |u-v|/2 for u,v >= 1
and sqrt(rho), sqrt(sigma) <= sqrt(R).  With G <= 1/4 and G symmetric,
  ||S_rho - S_sigma||_HS^2 = int int G(x,t)^2 Delta(x,t)^2 dx dt
  <= (R/4) int int G^2 (A(x)+A(t))^2 dx dt
  = (R/2) [ int int G^2 A(x)^2 dx dt + int int G^2 A(x) A(t) dx dt ]
  <= (R/32) ( ||A||_2^2 + ||A||_1^2 ),
where int int G^2 A(x)^2 <= (1/16)||A||_2^2 (integrate t first, G^2 <= 1/16)
and int int G^2 A(x) A(t) <= (1/16)||A||_1^2 (G^2 <= 1/16 pointwise).
Since |A| <= R-1 a.e., ||A||_2^2 <= ||A||_inf ||A||_1 <= (R-1)||A||_1 and
||A||_1^2 <= (R-1)||A||_1 (as ||A||_1 <= R-1), so
  ||S_rho - S_sigma||_HS^2 <= (R/32)(2(R-1)||A||_1) <= (R^2/16)||A||_1,
i.e. ||S_rho - S_sigma||_HS <= (R/4) ||rho - sigma||_1^{1/2}.  Verified.

### 2.4 Weyl inequality and conversion

For self-adjoint compact A, B with eigenvalues mu_1 >= mu_2 >= ... (counted
with multiplicity, tending to 0): |mu_k(A) - mu_k(B)| <= ||A - B||.  This is
the standard min-max/Weyl result: from (Ax,x) <= (Bx,x) + ||A-B|| the
min-max characterization gives mu_k(A) <= mu_k(B) + ||A-B||, and the reverse
by symmetry.  Since ||A-B|| <= ||A-B||_HS and S_rho, S_sigma are self-adjoint
Hilbert-Schmidt:
  |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||
  <= ||S_rho - S_sigma||_HS <= (R/4)||rho - sigma||_1^{1/2}.
Applied to S_rho, S_sigma - NOT to T_rho (T_rho is not self-adjoint on L^2;
that was the draft's O1a defect, correctly repaired by R1).

Conversion to lambda_k:
  |lambda_k(rho) - lambda_k(sigma)|
    = lambda_k(rho) lambda_k(sigma) |1/lambda_k(rho) - 1/lambda_k(sigma)|
    <= (k^2 pi^2)^2 (R/4) ||rho - sigma||_1^{1/2},
using the comparison bounds k^2 pi^2 / R <= lambda_k <= k^2 pi^2 (Rayleigh
quotient: lambda_k = min_{dim S = k} max_{0 != y in S} (int y'^2)/(int rho y^2)
with 1 <= rho <= R).  Verified.

### 2.5 Edge cases

rho = sigma trivial; R -> 1+ shrinks K to {1} and the bound degrades
continuously; k >= 1 arbitrary.  No issue.

## 3. O1b - Lemma 3: moving-jump Feynman-Hellmann with the corrected sign

### 3.1 Statement under audit

rho constant on a two-sided neighborhood of x_j in (0,1), one-sided values
c_- (left), c_+ (right), c_- != c_+; rho_eps = rho with the jump moved to
x_j + eps.  Claim:
  d/d eps lambda_k(rho_eps)|_0 = lambda_k (c_+ - c_-) u_k(x_j)^2,
  d/d eps D(rho_eps)|_0 = -(c_+ - c_-) f(x_j),   f = lambda_1 u_1^2 - lambda_2 u_2^2.
Moving right by delta changes D by -(c_+ - c_-) f(x_j) delta + o(delta);
moving left by delta changes D by +(c_+ - c_-) f(x_j) delta + o(delta).
At an interior extremum over a family in which x_j is free, (c_+ - c_-) f(x_j)
= 0, hence f(x_j) = 0.

### 3.2 Sign from first principles (repair R2)

For eps > 0, rho_eps - rho_0 = (c_- - c_+) chi_{(x_j, x_j+eps)}; hence as a
distribution d/d eps rho_eps|_0 = -(c_+ - c_-) delta_{x_j}.  The FH formula
(AEH Lemma 2.1, V = 0, eigenfunctions normalized by int rho u_k^2 = 1):
  d lambda_k/d eps = -lambda_k int (dw/d eps) u_k^2 dx.
Formally substituting the Dirac limit:
  d lambda_k/d eps = -lambda_k (-(c_+ - c_-) u_k(x_j)^2)
                   = +lambda_k (c_+ - c_-) u_k(x_j)^2.   (positive sign)
Subtracting k = 2 and k = 1:
  dD/d eps = (c_+ - c_-)(lambda_2 u_2^2 - lambda_1 u_1^2) = -(c_+ - c_-) f(x_j).
This is the corrected sign (the draft had the opposite sign for D; the
zero-condition f(x_j) = 0 is unchanged).  The independent re-derivation
confirms the delivered text.

### 3.3 Smoothing approximation (repair R4)

H C^inf with H(t) = 0 for t <= -1, H(t) = 1 for t >= 1, H' >= 0;
H_delta(s) = H(s/delta); rho_eps^delta(x) = c_- + (c_+ - c_-) H_delta(x - x_j - eps)
on the transition band |x - x_j - eps| < delta, equal to rho_eps outside.
Then d/d eps rho_eps^delta = -(c_+ - c_-)(1/delta) H'((x - x_j - eps)/delta)
in C_c^inf, hence in L^1; rho_eps^delta in [1, R] uniformly.  AEH Lemma 2.1
applies for each delta > 0:
  d/d eps lambda_k(rho_eps^delta)
    = lambda_k(rho_eps^delta)(c_+ - c_-) int (1/delta) H'((x - x_j - eps)/delta)
      u_k(rho_eps^delta; x)^2 dx.

Limit interchange (each ingredient checked):
(i) rho_eps^delta -> rho_eps in L^1 uniformly for |eps| <= eps_0 (the
    symmetric difference has measure <= 2 delta, value difference |c_+ - c_-|),
    so by Lemma 1 the eigenvalues converge uniformly in eps.
(ii) u_k(rho_eps^delta) -> u_k(rho_eps) uniformly in x (and eps).  Uniform H^2
    bounds over K: ||u_k||_2 <= 1 (rho >= 1), ||u_k'||_2^2 = lambda_k <= (k pi)^2,
    ||u_k''||_2 = lambda_k ||rho u_k||_2 <= (k pi)^2 R.  Arzela-Ascoli gives a
    uniformly convergent subsequence; any limit satisfies -u*'' = lambda rho_eps u*
    (pass the equation to the limit: u_n'' is bounded in L^2 so u_n'' -> u*''
    weakly; the RHS lambda_n rho_n u_n -> lambda rho_eps u* in L^1), and the
    normalization passes (||rho_n u_n^2 - rho_eps u*^2||_1 -> 0).  Simplicity of
    the Sturm-Liouville eigenvalues makes the limit unique; the sign convention
    fixes the sign, so the whole family converges.
(iii) (1/delta) H'((x - a)/delta) is a Dirac family: integral 1, support in
    |x - a| < delta; for continuous bounded g, int (1/delta) H'((x-a)/delta) g(x) dx
    -> g(a) (change of variable y = (x-a)/delta + dominated convergence).
    Applying it to g = u_k(rho_eps)^2 and bounding the difference
    |(u_k^delta)^2 - u_k^2| uniformly gives the limit for the eigenfunctions.

Hence, for every fixed eps,
  d/d eps lambda_k(rho_eps^delta)
    -> lambda_k(rho_eps)(c_+ - c_-) u_k(rho_eps; x_j + eps)^2   (delta -> 0),
with the integrands uniformly bounded by (k pi)^2 |c_+ - c_-| ||u_k^delta||_inf^2
<= C(k, R) independent of delta and eps.

FTC + dominated convergence:
  lambda_k(rho_eps) - lambda_k(rho_0)
    = lim_delta int_0^eps d/d s lambda_k(rho_s^delta) ds
    = int_0^eps lambda_k(rho_s)(c_+ - c_-) u_k(rho_s; x_j + s)^2 ds.
Dividing by eps and letting eps -> 0 uses the continuity of s -> u_k(rho_s;
x_j + s) at s = 0 (s -> rho_s is L^1-continuous with ||rho_s - rho_0||_1 =
|c_+ - c_-| |s|; eigenfunctions converge uniformly along L^1-convergent
densities by the same compactness argument; x_j + s -> x_j).  The argument is
symmetric in the sign of eps, so the two-sided derivative exists at every jump
position, equal to lambda_k (c_+ - c_-) u_k(x_j)^2.  Verified.

### 3.4 Stationarity consequence

Rightward distance derivative: -(c_+ - c_-) f(x_j); leftward distance
derivative: +(c_+ - c_-) f(x_j).  At an interior maximum both are <= 0, which
forces (c_+ - c_-) f(x_j) = 0; at an interior minimum both are >= 0, again
forcing (c_+ - c_-) f(x_j) = 0.  Since c_+ != c_-, f(x_j) = 0.  Verified.

### 3.5 Notes on the prior audit's F-002

The delivered text's characterization is correct: the two-sided derivative of
eps -> D(rho_eps) exists at EVERY jump position (part 3.3 above); what fails
unless f(x_j) = 0 is that the rightward and leftward DISTANCE derivatives have
opposite signs.  The stationarity consequence f(x_j) = 0 is identical under
either formulation.  Confirmed numerically (Section 8, V2b).

## 4. F-001 repair-chain arithmetic (verified)

Delivered corrected chain (candidate_proof.md Section 3 (b)):
  ||S_rho - S_sigma||_HS^2 <= (R/32)(||A||_2^2 + ||A||_1^2)
  <= (R/32)(2R||A||_1) = (R^2/16)||A||_1,
via ||A||_2^2 <= (R-1)||A||_1 <= R||A||_1 and ||A||_1^2 <= (R-1)||A||_1
<= R||A||_1.  Hence ||S_rho - S_sigma||_HS <= (R/4)||A||_1^{1/2}.

Audit of the arithmetic: (i) the coefficient (R/32) on (||A||_2^2 + ||A||_1^2)
is correct (Section 2.3); (ii) ||A||_2^2 <= ||A||_inf ||A||_1 <= (R-1)||A||_1
is correct; (iii) ||A||_1 <= R-1 on the unit interval, so ||A||_1^2 <= (R-1)||A||_1
is correct; (iv) (R/32)(2R||A||_1) = (R^2/16)||A||_1 is correct; (v) the
pre-correction line "<= (R/16)||rho - sigma||_2^2" was indeed not derivable
from |Delta| <= (sqrt(R)/2)(A(x)+A(t)) (squaring gives the (R/4)(A_x+A_t)^2
factor, and after G^2 <= 1/16 the correct coefficient is (R/32), not (R/16)).
Final constant (R/4)||A||_1^{1/2} unaffected by the repair.  The delivered
text carries the corrected derivation; the arithmetic is sound.  Verified
numerically on 11 independent pairs (Section 8, H4).

## 5. Theorem-statement fidelity

The audited candidate's theorem statement (Section 1 of candidate_proof.md)
reproduces the draft theorem and the prior audit's audited statement verbatim
in content: K = {measurable rho : 1 <= rho <= R a.e.}, Dirichlet string,
D = lambda_2 - lambda_1, barrier family rho = R on (a,b), 1 elsewhere,
well family rho = 1 on (a,b), R elsewhere, closed parameter domain 0 <= a <= b
<= 1, both extrema attained.  R = 1 is excluded (trivial); edge cases a = b
(rho = 1, D = 3 pi^2), (a,b) = (0,1) (rho = R, D = 3 pi^2 / R), a = 0 or b = 1
(2-block members) are inside the closed families.  No quantifier, class, or
constant change was found; the statement was NOT silently upgraded.

## 6. Consistency read of O1c-O1f and the synthesis

The packet bounds this run to the two changed points; O1c-O1f were re-read for
internal consistency and for compatibility with the prior independent audit
(422A69, verdicts PROVED on the draft's O1c-O1f).  Findings of the re-read:

- Lemma 2 (structure of f): Wronskian argument re-checked.  W = u_1 u_2'
  - u_1' u_2 satisfies W' = (lambda_1 - lambda_2) rho u_1 u_2 and W(0) = W(1)
  = 0; with the sign convention u_1 > 0, u_2 > 0 on (0, z_0), u_2 < 0 on
  (z_0, 1), W' < 0 on (0, z_0) and W' > 0 on (z_0, 1), so W < 0 on (0, 1),
  v = u_2/u_1 strictly decreasing with v' = W/u_1^2; f = 0 iff |v| = c,
  c = sqrt(lambda_1/lambda_2) in (0,1); at most two zeros; {f > 0} = (x_-, x_+)
  contains z_0.  Correct.  This is a rho-independent re-derivation of AEH
  Lemma 2.2 items (1), (4), (5).
- Lemma 4 (N-jump compactness, <= 2 effective jumps): K_N is the continuous
  image of the compact Omega_N x [1,R]^{N+1}; D continuous by Lemma 1; each
  effective jump is an interior free parameter; Lemma 3 gives
  d/d delta_j D_cell = -(c_j - c_{j-1}) f(rho^N)(x_j) = 0 at an extremizer;
  Lemma 2 caps the number of zeros at 2.  Consistent.
- Lemma 5 (step functions dense): block averages -> rho in L^1; D(rho_m)
  -> D(rho) by Lemma 1; M_N nondecreasing -> sup_K D; mirror for inf.
  Consistent.
- Lemma 6 (bang-bang): at a global maximizer rho~ (constructed in K_2, hence
  piecewise constant), AEH Lemma 2.1 with w(kappa) = rho~ +/- kappa chi_J
  gives d/d kappa D = +/- int_J f~ dx; maximality forces rho~ = R a.e. on
  {f~ > 0} and rho~ = 1 a.e. on {f~ < 0}; mirror for minimizers.  The
  presentational point F-003 (hypothesis should be stated as "rho~ in K_2 a
  global maximizer of D over K") remains valid; the existence of the K_2
  maximizer is established in the synthesis before Lemma 6's conclusion is
  used, so there is no circularity.
- Synthesis: sup_K D = sup_{K_2} D (Lemmas 4-5), attainment in K_2, bang-bang
  + Lemma 2 identify the maximizer with rho^{bar}_{x_-, x_+} a.e.; the reverse
  inequalities are trivial; attainment over [0,1]^2 by continuity.  Consistent.

No new gap was found in this re-read.

## 7. Premise rechecks against primary sources

P1. AEH Lemma 2.1 (Feynman-Hellmann), arXiv:2407.02459v2,
    papers/fundamental_gap.txt (sha256 2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14),
    lines 84-101.  The source states, for one-parameter families V(.,kappa),
    w(.,kappa) with inf V > -inf, C >= w >= 1/C, and dV/dkappa, dw/dkappa in
    L1(0,pi):
      d lambda_n/dkappa = -lambda_n int_0^pi (dw/dkappa) u_n^2 dx
                          + int_0^pi (dV/dkappa) u_n^2 dx,
    and the proof fixes int w u_n^2 = 1.  The source interval is (0,pi); the
    problem here is on (0,1) via the affine rescaling x -> pi x, which does
    not change the formula (the FH identity is scale-invariant).  Hypotheses
    met in both uses: Lemma 6 (V = 0, w = rho~ +/- kappa chi_J in [1,R],
    dw/dkappa = +/- chi_J in L^1) and Lemma 3 (smoothed families in [1,R],
    dw/deps in C_c^inf subset L^1).  Verified.
P2. AEH Lemma 2.2 (structure of u_2/u_1), same source, lines 197-220: items
    (1)-(5) confirmed verbatim, including W' = (lambda_1 - lambda_2) w u_1 u_2
    and the sign convention u_{1,2} > 0 near 0.  The candidate's Lemma 2 is a
    rho-independent re-derivation; both are valid; no conflict.  Verified.
P3. Weyl/min-max inequality for self-adjoint compact operators: standard
    (min-max characterization); |mu_k(A) - mu_k(B)| <= ||A - B||.  Applied to
    the self-adjoint S_rho, not to the non-self-adjoint T_rho.  Verified.
P4. Comparison bounds k^2 pi^2 / R <= lambda_k(rho) <= k^2 pi^2: Rayleigh
    quotient derivation, verified numerically (H3).  Verified.
P5. Sturm oscillation (u_k has exactly k-1 simple interior zeros) for the
    weight bounded below by a positive constant with Dirichlet BCs: classical;
    used for z_0 and simplicity.  Verified numerically on hostile configs.
P6. Keller 1976 (DOI 10.1137/0131042, papers/keller1976.txt) and Mahar-
    Willner 1976 (DOI 10.1002/cpa.3160290505, papers/mw1976.txt): confirmed to
    be the ratio problems in the piecewise-continuous bounded-jump class (both
    source headers verified).  They are NOT premises of O1: the candidate's
    premise ledger classifies them as context only, and this audit confirms by
    reading candidate_proof.md that neither is cited in any lemma of O1.  The
    box class K with the gap functional D requires the N-jump approximation
    ladder (Lemmas 4-5).  No citation obligation arises.  Verified.

## 8. Numeric evidence (independent implementation)

All scripts under reproducibility/ were written from scratch for this run
(finite-difference solver fd_lib.py for the HS/Weyl checks; exact
transfer-matrix solver tm_lib.py for the moving-jump checks; seeds and exact
commands recorded in repro_manifest.md).  Evidence only; every proof-level
claim is argued analytically in Sections 2-4.

- verify_hs_weyl_independent.py: H1 (HS bound <= (R/4)||A||_1^{1/2}): 11/11
  pairs, ratios 0.073-0.165; H2 (Weyl |1/lambda_k(rho) - 1/lambda_k(sigma)|
  <= ||S_rho - S_sigma||_HS): 22/22; H3 (comparison bounds): 22/22;
  H4 (F-001 chain: I1 <= ||A||_2^2/16, I2 <= ||A||_1^2/16, (R/32)(||A||_2^2
  + ||A||_1^2) <= (R^2/16)||A||_1, ||A||_2^2 <= (R-1)||A||_1, ||A||_1^2
  <= (R-1)||A||_1): 11/11.
- verify_fh_sign_independent.py: V1 (d lambda_k/d eps = lambda_k (c_+ - c_-)
  u_k(x_j)^2): 16/16 entries at eps = 1e-4 within 5.3e-6 (tolerance 1e-5);
  V2 (dD/d eps = -(c_+ - c_-) f(x_j)): 16/16 at eps = 1e-4 within 5.3e-6;
  V2b (rightward/leftward distance derivatives have opposite signs):
  confirmed at 3 configs; V3 (symmetric barrier dD/du = -2(R-1) f(u)): 5/5
  points, errors <= 1.9e-6; V4 (stationarity at u* = 0.45148546584):
  f(u*) ~ 2.9e-7, right = -0.0144, left = +0.0144 (sign flip).
- verify_smoothing_dirac_independent.py: D1 (Dirac family point evaluation):
  error O(delta^2), 7.2e-3 at delta = 0.05 down to 2-4e-6 at delta = 0.001;
  D2 (smoothed moving-jump derivative -> lambda_k (c_+ - c_-) u_k(x_j)^2):
  within 0.03-0.3% for delta in [0.002, 0.04] (residual = block discretization
  of the smoothed density; sign and magnitude correct).
- verify_aeh_pointwise_independent.py: A1 (AEH pointwise FH formula): matches
  to 6e-8 and 9e-11; A2 (H^2 bounds ||u_k||_2 <= 1, ||u_k'||_2 <= k pi,
  ||u_k''||_2 <= (k pi)^2 R): 8/8 hostile configs; A3 (R = 4 contract sanity):
  sup over barrier family ~ 32.6138 (rel err 5e-6 vs 32.6139836177),
  inf over well family ~ 6.7845 (rel err 1.6e-6 vs 6.7844823391),
  argmax ~ (0.451, 0.548) on the symmetric line (consistent with u*).

## 9. Findings log (this run)

- No new mathematical gap was found in the audited changed points.
- F-101 (PRESENTATIONAL, low priority): candidate_proof.md Lemma 3 (b)
  justifies the uniformity in eps of the delta -> 0 convergence by "the
  integrands are uniformly bounded".  Uniform boundedness plus pointwise
  convergence does not alone imply uniformity; the claim is nevertheless true,
  by the uniform convergence of eigenfunctions and the uniform modulus of
  continuity of u_k (from the H^2 bound).  The proof step that actually needs
  this (step (c), dominated convergence) only requires pointwise convergence
  plus the uniform bound, both of which are established.  No repair needed;
  recorded for precision.
- F-102 (METHOD, resolved): the first independent check of the moving-jump
  derivatives used a fixed-grid finite-difference solver; sub-cell jump motion
  (eps << grid spacing) produced grid-pinning artifacts (spurious derivatives).
  The check was replaced by the exact transfer-matrix solver (tm_lib.py); the
  failure mode is recorded in counterexample_log.md as a failed check method,
  not as a counterexample to any claim.
- The delivered text's F-001 correction is arithmetically sound (Section 4);
  the pre-correction line was indeed not derivable; the final bound is
  unchanged.  The delivered text's notes on F-002 are confirmed correct.

## 10. Residual gaps

None within the O1 scope.  Two presentational notes (F-101, F-102) do not
affect any proof step.  Out of scope: O2 (symmetric 1-parameter analysis) and
O3 (2-parameter symmetry), owned by the draft run; the exact values
sup_K D = 32.6139836177 and inf_K D = 6.7844823391 at R = 4 and the
stationarity point u* are contract-level data (verified numerically as a
sanity check, A3) but their full derivation belongs to O2/O3.

## 11. Overall verdict

- O1a (Lemma 1): PASS.  Re-derived from scratch (S_rho presentation, HS bound
  with the corrected constant chain, Weyl, conversion); numerically verified.
- O1b (Lemma 3): PASS.  Re-derived from scratch (sign via the Dirac-limit
  identity and smoothing; two-sided differentiability; stationarity);
  numerically verified.
- F-001 repair chain: VERIFIED (arithmetic sound; final constant unchanged).
- Theorem statement: PASS (no silent upgrade; edge cases covered).
- O1c-O1f and the synthesis: consistent with the prior independent audit
  (PROVED); no new gap found in this run's re-read.
- Overall: the revised candidate (R-20260806T140000Z-o1revise-2ED02A) is
  returned as INDEPENDENTLY_AUDITED_PROOF for the O1 reduction theorem.  The
  manager MAY close obligation O1.

The upstream revision policy's requirement (an independent verifier pass on
the two changed points before closing O1) is satisfied by this run.

## 12. Confidence by axis

- Semantic fidelity: HIGH.  The audited statement matches the draft and the
  prior audit; the repairs R1-R4 are applied exactly as listed and were
  re-derived here, not copied.
- Mathematical correctness: HIGH for O1a and O1b (from-scratch re-derivation
  plus independent numerics); HIGH for O1c-O1f (prior independent audit plus
  this run's consistency read).
- Completeness: HIGH within the O1 scope (all six obligations plus synthesis
  and edge cases closed; O2/O3 excluded by the packet).
- Novelty: not the focus of this audit run; see status_and_literature.md of
  the revise run (box-class reduction theorem and the SUP side appear not to
  be in the literature; Sun 2022 class definitions NOT_VERIFIABLE from public
  metadata; the INF side in a bounded-jump subclass is the nearest known
  result).
- Reproducibility: HIGH.  All scripts, seeds, exact commands, and outputs are
  recorded under reproducibility/; hashes in repro_manifest.md.