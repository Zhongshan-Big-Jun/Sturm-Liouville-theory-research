# Run addendum R-207 (2026-08-13, session 2): corrected half-Green machinery, both 2x2 sector closed forms, precise open core for (G1')

Continuation of R-20260812T090000Z-g1prime-g2.  All numerics are EVIDENCE
unless flagged STRICT.  This addendum closes the R-207 closed-form
infrastructure (C1-C3 of scripts/_gapn2_half_problem_probe.py), RETRACTS two
false handoff claims, and reduces the n=2 sector definiteness question to an
explicit finite-dimensional inequality.

## 1. STRICT: corrected regularized Green of the half problems (bug fix)

Setting: -u'' = mu rho u on [0,L] (L = 1/2), u(0) = 0, and u(L) = 0 (D) or
u'(L) = 0 (N); rho piecewise constant.  Let u be the normalized eigenfunction
at mu_k and v the second solution with W(u,v) = uv' - u'v = 1, v(0) =
-1/u'(0).  The reduced resolvent kernel Gt_k(x,y) = sum_{l != k} v_l(x) v_l(y)
/(mu_l - mu_k) has the STRICT closed form

    Gt_k(x,y) = B(x,y) - u(x) P(y),
    B(x,y) = (u(x)v(y) - v(x)u(y)) 1_{x>y}
             - u(x)u(y) I1(x) + v(x)u(y) I2(x),
    I1(x) = int_0^x rho u v dt,  I2(x) = int_0^x rho u^2 dt,
    P(y) = <rho u, B(.,y)> = v(y)(1 - I2(y)) - u(y)[A1 - A2 + I1(L) - I1(y)],
    A1 = int_0^L rho u^2 I1 dx,  A2 = int_0^L rho u v I2 dx.

Proof.  Variation of parameters for L_x = -d^2/dx^2 - mu rho(x) with source
h(x) = delta(x-y) - rho(x)u(x)u(y) gives L_x B = h (jump of B_x at x = y is
u'v - v'u = -W = -1, so -B_xx carries +delta; the smooth part is verified by
direct differentiation using u'' = -mu rho u, I1' = rho u v, I2' = rho u^2).
Then L_x(Gt_k) = delta - rho u u^T, the boundary conditions hold (B(0,y)=0,
B(L,y)=0 for D, B_x(L,y)=0 for N, using I2(L)=1 and the BCs of u), and
<rho u, Gt_k(.,y)> = P(y) - P(y) = 0.  These three properties characterize
the reduced resolvent uniquely.  A1, A2 are computed EXACTLY by elementary
per-block trig antiderivatives (scripts/_gapn2_half_problem_probe.py,
_prims_9/_fold3/_a1a2_exact: C^2/S^2/CS times iCC/iCS/iSS, nine closed
primitives).  QED.

RETRACTED (handoff draft): the previous green_regularized carried an extra
factor rho(y) in B and in P.  That draft solves the equation up to the
rho(y) factor of the delta (wrong jump) and is discontinuous in y at density
jumps; the constant-density self-check missed the bug because rho(y) = 1
there.  The handoff's diagnosis ("quadrature accuracy of A1/A2") was also
wrong: exact A1/A2 differ from the 200000-point trapezoid rule by 2e-8 only.

EVIDENCE: n=2, INF and SUP, R=4.  C2 vs Richardson-extrapolated spectral
sums (N=80/160): max err Gt_D 7.7e-6 / 2.3e-6, Gt_N 5.8e-6 / 1.3e-6, full
cross Greens G_D(mu_2^N) 7.7e-6 / 2.3e-6, G_N(mu_1^D) 5.8e-6 / 1.3e-6
(residual is the O(1/N^2) spectral tail; the closed form is exact).  Symmetry
of Gt to 1.4e-17 and continuity across density jumps to 6e-10 confirm the
fix; T_D closed vs spectral 1.8e-11.

## 2. STRICT: eps-conjugation sector identity and the convention correction

At any symmetric band-consistent point, with eps_j = (-1)^{j+1}, the mirror
bases Be/Bo (pairs j <-> 2n-1-j, column j = (e_j +- e_{2n-1-j})/sqrt(2))
satisfy eps_{2n-1-j} = -eps_j, hence diag(eps) Bo = Be diag(beta) with
beta_j = -(-1)^j.  Therefore for Kp := diag(eps) K diag(eps),

    Bo^T Kp Bo = diag(beta) (Be^T K Be) diag(beta)   (STRICT).

Correction of the handoff convention claim: sector_data['Ko'] (scripts/
_gapn2_sector_decomposition.py) is the odd sector Bo^T K Bo of the RAW K,
NOT the odd sector of Kp; the identity diag(1,-1) Ke diag(1,-1) = Ko fails
(observed err 6.9 at n=2 INF R=4) because it should read
diag(1,-1) Ke diag(1,-1) = Kp_odd.  Both statements are exact algebra.

EVIDENCE: Kp_odd vs diag(1,-1) Ke_fd diag(1,-1): 2.3e-9 (INF), 8.6e-10 (SUP)
at R=4.

## 3. STRICT: both 2x2 mirror sectors of K in exact half-problem form (even n)

Let n be even (lambda_n = mu_{n/2}^D odd full mode, lambda_{n+1} =
mu_{n/2+1}^N even full mode), c^2 = lambda_n/lambda_{n+1}, e = eps[:n]
(alternating), E = diag(e), u = (u_n(x_j))_{j<n} at the left-half switches,
d = sigma 2 c |W(x_j)|/(R-1).  From the R-206 collapsed identity
Kp = diag(d) + r vv^T + 2 lambda_n diag(u_n) S diag(u_n) (v_j = u_n(x_j)^2,
r = 2 lambda_n D/lambda_{n+1}^2, S = eps Gt_{n+1} eps - c^2 Gt_n) and the
mirror-restriction identities

    Be^T eps Gt_{n+1} eps Be = G_D(mu_2^N) o ee^T,      (full D-half Green at the cross eigenvalue)
    Be^T Gt_n Be             = G_N(mu_1^D),             (full N-half Green at the cross eigenvalue)
    Bo^T v = 0,  Bo^T(eps v) = sqrt(2) (eps v)[:n],     (v mirror-even)

one obtains, after conjugation of the raw K = diag(eps) Kp diag(eps):

    (Sector 1, even sector of K)  Kp_odd := Bo^T Kp Bo = diag(beta) Ke diag(beta),
        Ke = Be^T K Be,  Kp_odd = diag(d[:n]) + 2 lambda_n diag(u)
                [G_D o ee^T - c^2 G_N] diag(u);
    (Sector 2, odd sector of K)  Ko = Bo^T K Bo = diag(d[:n]) + 2 r (eps v)(eps v)^T
                + 2 lambda_n diag(u) [Gt_N - c^2 Gt_D o ee^T] diag(u),

where G_D, G_N are the full D-/N-half Green functions at the respective
cross eigenvalue and Gt_D, Gt_N the regularized ones at the own eigenvalue;
all four are the exact closed forms of Section 1 evaluated at the two
left-half switches.  det K = det(Ke) det(Ko) = det(Kp_odd) det(Ko).

EVIDENCE: n=2, R=4: Ko_closed vs Bo^T K_fd Bo err 4.6e-10 (INF), 3.7e-10
(SUP); Kp_odd vs diag(1,-1) Ke_fd diag(1,-1) err 2.3e-9 / 8.6e-10; both
assemblies (R-205 form and collapsed form) agree to 1.8e-15.  INF eig:
Kp_odd = [-9.123, -0.632], Ko = [-2.914, -1.066]; SUP: Kp_odd = [2.318,
9.048], Ko = [3.183, 7.148].

## 4. STRICT: spectral splits of the four half Green kernels (n=2)

With the classical interleaving mu_1^N < mu_1^D < mu_2^N < mu_2^D
(Gantmacher-Krein) and the half-normalized eigenfunctions v_m (D), w_m (N):

    G_D(mu_2^N)|2 = -alpha v1 v1^T + Ph,   alpha = 1/(mu_2^N - mu_1^D) > 0,
    G_N(mu_1^D)|2 = -beta  w1 w1^T + Qh,   beta  = 1/(mu_1^D - mu_1^N) > 0,
    Ph = sum_{m>=2} v_m v_m^T/(mu_m^D - mu_2^N)   (PD on the 2-point grid),
    Qh = sum_{m>=2} w_m w_m^T/(mu_m^N - mu_1^D)   (PD),
    Gt_D = sum_{m>=2} v_m v_m^T/(mu_m^D - mu_1^D) (PD),
    T_D  = sum_{m>=2} v_m v_m^T/((mu_m^D - mu_1^D)(mu_m^D - mu_2^N)) (PD),
    Gt_N = -alphaN w1 w1^T + Rh, alphaN = 1/(mu_2^N - mu_1^N) > 0,
    Rh = sum_{m>=3} w_m w_m^T/(mu_m^N - mu_2^N)   (PD).

All weights are strictly positive by the interleaving (no half eigenvalue of
either problem lies strictly between lambda_2 and lambda_3), and the
2-point evaluations of the tail sums are positive definite because the
complement of a one-dimensional eigenspace evaluates onto all of R^2 at two
distinct points.  Consequently, with the band identity w_2(x_j) = eps_j c
v_1(x_j) (EVIDENCE: ratio = c, -c to 1e-9), the sector matrices decompose as

    Kp_odd = diag(d) + 2 lam_2 diag(u) [ E Ph E - alpha (Ev1)(Ev1)^T
             + c^2 beta w1 w1^T - c^2 Qh ] diag(u)
           = B1 + 2 lam_2 D diag(u) [E T_D E] diag(u),
    B1 = diag(d) + 2 lam_2 diag(u) [E Gt_D E - alpha (Ev1)(Ev1)^T
         + c^2 beta w1 w1^T - c^2 Qh] diag(u),
    Ko = diag(d) + 2 lam_2 diag(u) [Rh - c^2 E Gt_D E] diag(u)
         + 2 r (eps v)(eps v)^T - 2 lam_2 alphaN diag(u) w1 w1^T diag(u).

EVIDENCE (R=4, closed forms): INF: eig(B1) = [-9.169, -0.720], PD core
2 lam_2 D diag(u) E T_D E diag(u): eig [0.042, 0.091] (it competes against
the negative diagonal); SUP: eig(B1) = [1.880, 8.273], core eig [0.159,
1.053].  The R-205 mixed-inertia observation on M is reproduced exactly:
M = lam_3 eps (G_D/2) eps - lam_2 G_N/2 has eig pair with det < 0 at R=4
INF, so the non-uniform diagonal d is the only sign source for Kp_odd.

## 5. EVIDENCE: R-scan of the two sector determinants (n=2, symmetric branch)

Kp_odd (hence Ke) and Ko stay negative definite (INF) / positive definite
(SUP) on the reachable ladder; det J = det(diag(s) K) stays positive
(consistent with sgn det J = (-1)^n = +1):

    INF: R=1.05 eig(Kp_odd)=[-395.5,-355.9] eig(Ko)=[-399.8,-348.2] detJ=+1.22e+05
         R=1.2  [-95.6,-75.5]  [-92.2,-74.8]  +7.97e+04
         R=2    [-20.6,-6.7]   [-13.7,-8.0]   +1.50e+04
         R=4    [-9.1,-0.63]   [-2.9,-1.1]    +1.45e+03
         R=10   [-5.17,-0.035] [-0.47,-0.10]  +5.68e+01
         R=30   [-3.00,-0.0013] [-0.051,-0.0066] +9.05e-01
         R=100  [-1.58,-5.7e-5] [-0.0042,-0.0003] +7.89e-03
    SUP: R=1.05 [353.7,417.3]  [365.4,408.3]  +1.38e+05
         R=1.2  [79.1,109.1]   [88.5,101.0]   +1.23e+05
         R=2    [10.6,25.2]    [13.8,21.1]    +7.84e+04
         R=4    [2.32,9.05]    [3.18,7.15]    +3.87e+04
         R=10   [0.49,2.80]    [0.65,2.15]    +1.26e+04

As R -> infinity the INF margin degenerates (det K -> 0+, R-202 bonding/
antibonding); the scan is consistent with strict definiteness at every
finite R.

## 6. Reduced open core (precise statement)

(G1') at n=2 symmetric points is now equivalent to the following explicit
finite-dimensional inequalities, for every R > 1, at the symmetric band-
consistent root, with the four kernels of Sections 1-4 in exact closed form:

    (I1)  Kp_odd := diag(d) + 2 lam_2 diag(u) [G_D o ee^T - c^2 G_N] diag(u)
          is negative definite (INF) / positive definite (SUP);
    (I2)  Ko := diag(d) + 2 r (eps v)(eps v)^T
          + 2 lam_2 diag(u) [Gt_N - c^2 Gt_D o ee^T] diag(u) has the same
          definiteness.

Equivalently (after congruence by diag(1/u)): for all y != 0,

    (I1')  d1 y1^2/u1^2 + d2 y2^2/u2^2 + 2 lam_2 [ -alpha (Ev1 . y)^2
           + (Ey)^T Ph (Ey) + c^2 beta (w1 . y)^2 - c^2 y^T Qh y ]  < 0  (INF),
    (I2')  d1 y1^2/u1^2 + d2 y2^2/u2^2 + 2 lam_2 [ (Ey)^T Rh (Ey)
           - c^2 (Ey)^T Gt_D (Ey) ] + 2 r (eps v . y)^2
           - 2 lam_2 alphaN (w1 . y)^2  < 0  (INF),

with the obvious sign flip for SUP.  The Cauchy/Binet determinant expansion
of the 2x2 case (det G|2 = sum_{m<k} [g_m(x1)g_k(x2) - g_m(x2)g_k(x1)]^2
/(p_m p_k) for G = sum g_m g_m^T/p_m) writes det Kp_odd and det Ko as
explicit signed double sums; making their sign strict uniformly in R is the
remaining proof obligation.  EVIDENCE shows the margins are O(1) near R=1
(singular in the (R-1) rescaling of d) and decay polynomially as R -> inf,
so a natural route is: (i) compute the finite rescaled limit
L = lim_{R->1+} (R-1) K at the constant string (all kernels elementary
trigonometric series, STRICT but not yet executed); (ii) prove monotonicity
of det Kp_odd and det Ko in R along the symmetric branch via the
Feynman-Hellmann derivative of the eigenpairs and the band-system
derivative of the switches; (iii) match the R -> inf asymptotics
(bonding-antibonding, R-202).  This remains OPEN.

## 7. Scripts (all under scripts/)

- _gapn2_half_problem_probe.py: rewritten; C0-C3; corrected green_regularized
  with exact _a1a2_exact; C3 now compares the two assemblies against each
  other and against the correct convention identities.
- _gapn2_half_debug2.py / _gapn2_half_debug3.py / _gapn2_half_debug4.py:
  debugging chain (H1/H2 hypothesis tests, FD residual of L_x B, exact A1/A2
  validation).  Keep as artifacts.
- _gapn2_odd2x2_decompose.py: exact A-form / B1 / B2 decomposition of
  Kp_odd with spectral-split cross-checks.
- _gapn2_rawko_closed.py: the new closed form of the raw-K odd sector Ko.
- _gapn2_odd2x2_scan.py: R-scan of the two sector spectra/determinants.

## 8. Status

(G2) unchanged CLOSED STRICT (R-204).  (G1') still OPEN; the n=2 symmetric-
point piece is now reduced to the explicit inequalities (I1)(I2) with exact
closed-form entries, replacing the previous semi-numerical sector
decomposition.  The parity/convention structure is now fully STRICT
(Sections 1-4).  All earlier RETRACTED items of this run are listed in the
ledger.
