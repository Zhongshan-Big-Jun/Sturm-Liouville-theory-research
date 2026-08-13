# Run addendum R-208 (2026-08-13, session 3): R->1+ anchor for (G1') and (I1)/(I2) (STRICT), half-gap Hessian interpretation, monotonicity evidence

Continuation of R-20260812T090000Z-g1prime-g2 (route (i) of addendum d,
Section 6).  All numerics are EVIDENCE unless flagged STRICT.

## 1. STRICT: W0 does not vanish at the zeros of f0 (all n >= 1)

At the constant string rho = 1: lambda_k^0 = k^2 pi^2, u_k^0(x) = sqrt(2)
sin(k pi x), and

    f0(x) = lambda_n^0 (u_n^0)^2 - lambda_{n+1}^0 (u_{n+1}^0)^2
          = 2 pi^2 [ n^2 sin^2(n t) - (n+1)^2 sin^2((n+1)t) ],  t = pi x,

    W0(x) = (u_{n+1}^0)' u_n^0 - u_{n+1}^0 (u_n^0)'
          = 2 pi [ (n+1) cos((n+1)t) sin(n t) - n sin((n+1)t) cos(n t) ].

Lemma A.  If f0(x) = 0 and x in (0,1), then W0(x) != 0.  Consequently f0 has
exactly 2n simple zeros in (0,1) (Sturm) and f0'(x_j) = -2 lambda_{n+1}^0
eps_j c0 W0(x_j) != 0 at each zero.

Proof.  Set t = pi x, p = cos^2((n+1)t), q = cos^2(n t), c0 = n/(n+1).
f0(x) = 0 gives sin^2((n+1)t) = c0^2 sin^2(n t), i.e.

    1 - p = c0^2 (1 - q).                                        (E1)

If also W0(x) = 0, then (n+1) cos((n+1)t) sin(n t) = n sin((n+1)t)
cos(n t).  If sin(n t) = 0, then sin((n+1)t) = 0 by (E1); sin(n t) =
sin((n+1)t) = 0 with gcd(n, n+1) = 1 forces t = a pi/n = b pi/(n+1),
a(n+1) = bn, hence n | a, so t >= pi, contradicting t in (0, pi).  Hence
sin(n t) != 0, and squaring the Wronskian relation with (E1) gives

    (n+1)^2 p = n^2 sin^2((n+1)t) cos^2(n t) / sin^2(n t) = n^2 c0^2 q,

so p = n^4 q/(n+1)^4.  Substituting into (E1),

    1 - n^4 q/(n+1)^4 = c0^2 (1 - q)
    => (n+1)^2 (2n+1) = - n^2 q (2n+1)
    => q = -(n+1)^2 / n^2 < 0,

contradiction (q >= 0).  QED.

EVIDENCE: for n = 2..5 the 2n zeros of f0 are computed and min_j |W0(x_j)|
= 13.733 (n=2), 14.452 (n=3), 14.758 (n=4), 14.915 (n=5); the identity
f0'(x_j) = -2 lambda_{n+1}^0 eps_j c0 W0(x_j) holds to 1.2e-11.

## 2. STRICT: solution set and Jacobian at R = 1; the anchor theorem

At R = 1 the band system F(1,x) = 0 reads f0(x_j) = 0 for j = 1..2n with
x_1 < ... < x_{2n}; since the zeros of f0 satisfy f0(1-x) = f0(x), the
unique solution is the sorted 2n-tuple, which is reflection symmetric.
By the (A2) identity f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j) with W < 0
and eps_j = (-1)^{j+1} (R-205, global interleaving; elementary at R = 1),

    D_x F(1, x*) = diag(f0'(x_j)),
    sgn det D_x F(1, x*) = prod_j sgn f0'(x_j)
        = (-1)^{ sum_j (j+1) } = (-1)^{ n(2n+3) } = (-1)^n,

reproducing the base-document R = 1 analysis.  Lemma A gives D_xF(1,x*)
invertible, so by the Implicit Function Theorem the solution set
Sigma_sigma(R) in a neighborhood of R = 1 is a single smooth branch, the
symmetric one, on some interval (1, 1+delta_0).

Uniqueness near R = 1 (cleaner argument).  Every coordinate x_j of a
solution is a zero of the SAME scalar function f(.;R) = lambda_n u_n^2 -
lambda_{n+1} u_{n+1}^2 (with the widths determined by the x_j).  For R in
(1, 1+delta), f(.;R) has exactly 2n simple zeros in (0,1), each near a
distinct zero of f0 (Sturm oscillation, continuity, Lemma A).  Hence any
solution must be the sorted 2n-tuple of these zeros; in particular
Sigma_sigma(R) has at most one point near R = 1.  A symmetric branch
exists by IFT on the symmetric submanifold (the restriction of D_xF(1,x*)
to symmetric variations is again diag(f0'(z_j)) on the n independent
pairs, nonsingular), so Sigma_sigma(R) equals that symmetric branch for
R in (1, 1+delta_0).

Theorem B (anchor for the second variation).  Along this branch, as
R -> 1+, all off-diagonal entries of K stay O(1): in the R-206 identity
Kp = diag(d) + r vv^T + 2 lambda_n diag(u_n) S diag(u_n) the rank term has
r -> 2 n^2 (2n+1) / (n+1)^4 and v_j = u_n(x_j)^2 -> 2 sin^2(n pi x_j),
and S = eps Gt_{n+1} eps - c^2 Gt_n converges to the constant-string
reduced-resolvent combination (lambda_n^0 != lambda_{n+1}^0, no pole), a
finite symmetric matrix on the limiting grid.  Hence, with
d_j = sigma 2 c |W(x_j)|/(R-1),

    (R-1) K(R) -> (sigma/lambda_{n+1}^0) diag(|f0'(x_j)|)   as R -> 1+,

a strictly sign-definite diagonal matrix (sigma = +1 SUP, -1 INF).  Since
det J = prod_j s_j det K with prod_j s_j = (R-1)^{2n} (-1)^n and K is
strictly definite for R in (1, 1+delta_1),

    sgn det D_x F_sigma(R, x) = (-1)^n   for every x in Sigma_sigma(R),
    R in (1, 1+delta),   delta = min(delta_0, delta_1) > 0.

This closes (G1') in a right neighborhood of R = 1 for every n >= 1
(even and odd), independently of the sector decomposition.  For n = 2 it
also gives (I1)/(I2) on (1, 1+delta): both (R-1) Kp_odd and (R-1) Ko
converge to diag(sigma 2 c0 |W0(x_j)|)_{j<2}, strictly definite with the
required sign.

Proof of the limit.  The diagonal converges because 2c|W(x_j)| -> 2 c0
|W0(x_j)| = |f0'(x_j)|/lambda_{n+1}^0 by the (A2) identity and continuity;
the off-diagonal parts of K are multiplied by (R-1) and stay bounded as
argued.  Strict definiteness of the limit is Lemma A.  Continuity of the
rescaled matrices in R on [1, 1+delta) then propagates definiteness
(persistence of strict definiteness under small perturbations).  QED.

EVIDENCE (n=2, scripts/_gapn2_r1_anchor_probe.py): continuation of the
symmetric branch down to R = 1.00001 gives (R-1)Kp_odd = diag(18.31122,
20.66434) + O(1e-4) (SUP) and the negative of it (INF), matching
diag(2 c0 |W0(x_j)|) = diag(18.3113267, 20.66432239) with error linear
in (R-1); switches converge to the f0 zeros (error 3e-7 at R = 1.00001);
D -> 5 pi^2.  n=3: max_j |2c|W(x_j)| - 2c0|W0(x_j)|| = 3.8e-4 at
R = 1.0001 (SUP), 3.1e-3 (INF), again linear in (R-1).

## 3. STRICT: half-gap Hessian interpretation (signs corrected)

At a symmetric point, the full gap equals the half-gap
g(x1,x2) = mu_2^N - mu_1^D (n=2), and the band equations f(x_j) = 0 are
equivalent to dg/dx_j = 0: with s_j = p_{j+1} - p_j (half blocks),

    dg/dx_j = s_j [ mu_2^N w_2(x_j)^2 - mu_1^D v_1(x_j)^2 ]
            = -2 s_j f(x_j)     (u_2 = v_1/sqrt(2), u_3 = w_2/sqrt(2)
                                 on the left half, band identity f=0).

Differentiating again, with J_{j,i} = df(x_j)/dx_i and J = diag(s) K,

    grad^2 g = -2 diag(s) J = -2 (R-1)^2 K = +(2/lambda_3) Hess(D_n),

using the R-206/A3 relation Hess(D_n) = -lambda_3 diag(s) J.  Therefore
(I1)+(I2) (both mirror sectors of K sign-definite) is equivalent to: the
symmetric band-consistent point is a strict local minimum of the half-gap
g for INF (K negative definite) and a strict local maximum for SUP (K
positive definite).  All four statements hold on (1, 1+delta) by Theorem B.

## 4. FALSIFIED route: global convexity of the half-gap (EVIDENCE)

Hypothesis: g is globally convex (INF) / concave (SUP) on the switch
triangle 0 < x1 < x2 < 1/2, which would close (I1)/(I2) without any
R-monotonicity.  FALSE: FD Hessian eigenvalues of g at R = 4 on a 6x6
interior grid are indefinite at most points (INF: min eigenvalue -4838 at
(0.0714, 0.3571); SUP: max eigenvalue +7529 at (0.0714, 0.1429));
violations on 11/15 (INF) and 12/15 (SUP) of the sampled points.  The
definiteness of grad^2 g holds only AT the critical point; the global-
convexity route is dead (scripts/_gapn2_gap_convexity_probe.py).

## 5. EVIDENCE: monotonicity of the sector determinants and the derivative structure

R-scan n=2 (scripts/_gapn2_r1_monotonicity_probe.py, 30 points,
[1.05,100]): det Kp_odd and det Ko are strictly DECREASING in R along the
symmetric branch for BOTH modes; traces stay sign-correct (tr < 0 INF,
tr > 0 SUP) but are not monotone (INF tr has an interior minimum, e.g.
-7.5 at R=1.05 -> -2.85 at R=33 -> -1.58 at R=100).  Chain-rule
structure verified to 4-5 digits at R = 1.5, 2, 4, 10 (scripts/
_gapn2_r1_det_derivative_probe.py):

    d/dR M = dM/dR|_x + sum_j (dM/dx_j) (dx_j/dR),
    dx/dR = - J^{-1} dF/dR,   F_j = f(x_j)/lambda_{n+1},

with dM/dx_j and dM/dR computed at fixed x from the closed forms
(width shifts move x_j alone: w_j += h, w_{j+1} -= h).  Direct branch FD
and the chain agree: R=4 INF d/dR det Kp_odd = -5.8405 (both), d/dR det
Ko = -3.6637 (both); signs negative at every tested R.  (Earlier
dx/dR = 0 was a probe bug: Recon caches pat at init, so mutating rc.R
does nothing; fixed by rebuilding the Recon object.)

## 6. Reduced open core after the anchor (updated)

## 5b. EVIDENCE: large-R decay exponents of the sector determinants

Log-log local exponents along the branch (R ladder 10..500):
  INF: det Kp_odd ~ R^{-3.46..-3.55} (drifting toward -7/2), det Ko ~
  R^{-4.49..-4.55} (consistent with -9/2);
  SUP: det Kp_odd, det Ko ~ R^{-2.83..-2.90} (continuation of the SUP
  branch becomes solver-sensitive beyond R ~ 100-200; INF continuation
  fails at R = 500 with the current seed, values at R = 200 included).
  Both determinants stay positive and decay to 0+; the exact leading
  coefficients belong to route (iii) (bonding-antibonding asymptotics,
  R-202) and remain OPEN.

(G1') is now open only on [1+delta, infinity).  For n = 2, (I1)/(I2)
reduce further to: prove, for all R > 1+delta along the symmetric branch,
  (M1)  d/dR det Kp_odd < 0  and  d/dR det Ko < 0  (then det > 0 by the
        +infinity anchor and the 0+ large-R limit, EVIDENCE);
  (M2)  tr Kp_odd < 0, tr Ko < 0 (INF) / > 0 (SUP);
  (M3)  match the R -> infinity bonding-antibonding asymptotics (R-202)
        as the lower endpoint of the monotonicity argument.
The derivative objects in (M1) are now explicitly identified by the chain
rule of Section 5; signing them uniformly in R is the next proof
obligation.  The Cauchy/Binet determinant expansion (addendum d, Section
6) is the alternative algebraic route.

## 7. Scripts (all under scripts/)

- _gapn2_r1_anchor_probe.py: R->1+ continuation and rescaled-limit checks
  (A1/A2/A3 of its docstring), closed sectors from the d-addendum forms.
- _gapn2_r1_monotonicity_probe.py: det/trace/eig ladder, monotonicity
  flags, both modes.
- _gapn2_gap_convexity_probe.py: half-gap Hessian grid scan (falsified
  global convexity).
- _gapn2_r1_det_derivative_probe.py: chain-rule vs direct FD for
  d/dR det/trace; fixed-x partials; J and dF/dR.

## 8. Status

(G2) unchanged CLOSED STRICT (R-204).  (G1') now holds STRICT on
(1, 1+delta) for every n >= 1 (Theorem B); the open core is [1+delta,
infinity), with (M1)-(M3) above for the n=2 sector inequalities.  All
numerical tables in this addendum are EVIDENCE.
