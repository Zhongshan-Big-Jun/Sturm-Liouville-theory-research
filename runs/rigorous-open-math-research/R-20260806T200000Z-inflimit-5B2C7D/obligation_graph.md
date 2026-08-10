# Obligation graph - Theorem A (R-20260806T200000Z-inflimit-5B2C7D)

Root: THEOREM_A (lim_R R*m_R = Dbar(u*), Dbar(u*) < 3 pi^2, u_R -> u*).
Scope: this run only (T1/T2/T3 of the packet Q-20260806-inflimit-5B2C7D).
O3a/C1 (full box-class inf = symmetric inf) and the SUP side are separate
portfolio items, listed for dependency context only.
All files ASCII punctuation, UTF-8 without BOM.

## T2 - unique critical point and global strict minimum of Dbar

Statement: S(u) = 0 has exactly one root u* in (0,1/2); Dbar decreases on
(0,u*) and increases on (u*,1/2); Dbar(u) -> +inf (u->0+), -> 3 pi^2
(u->1/2-).
Depends on: the parametrization u(a) = a/(2(a - tan a)) (diffeomorphism),
the sign chain (K~ -> J -> G -> S), h'(a) sin^3 a < 0 on (pi/2, pi).
Evidence/status: PROVED (analytic, PDF Sec. 2.5).  Script 07 (symbolic
identities) re-verifies the chain identities; numeric zero locations
(a_1 ~ 1.6351, a* ~ 1.9856, a_G ~ 2.2766) are evidence only.
Edge cases: endpoints a -> pi/2+, pi- are covered by the limits; no
degeneracy (all zeros simple by the strict monotonicity chain).
Correction applied: the delivered text labels the unique zero of G as
a_G ~ 2.2766 = a(u*) (earlier draft conflated it with the J-zero a*).

## T3 - verified enclosure of Dbar(u*) with margin vs 3 pi^2

Statement: u* in [0.32992250812006654958, 0.32992250812006654960];
Dbar(u*) in [24.9438661384324768968, 24.9438661384324769084];
3 pi^2 - Dbar(u*) >= 4.664947; hence 25 - Dbar(u*) > 0.0561.
Depends on: T2 (u* well defined), interval arithmetic (mpmath.iv, outward
rounding), script 05.
Evidence/status: PROVED as a verified computation (computer-assisted
certification).  The enclosure is interval-arithmetic certified; the margin
inequalities are rational arithmetic consequences of the enclosure.
Edge cases: none (closed interval assertions).
Verifier note: an independent directed-rounding re-evaluation of Dbar(u*) was
performed in script 19-style cells; consistent (recorded in repro_manifest).

## L1 - Lemma A'' : G(R,u) >= Dbar(u) for w = u sqrt(R) >= 2

Statement: for R >= 1500, w >= 2, G(R,u) = mu_2 - mu_1 >= Dbar(u).
Depends on:
  - L1.1 phase brackets (delta_1 <= delta_1+ < 0.011, delta_2 <= delta_2+,
    z_2 <= pi/8, psi_2 >= 0) - PROVED analytically (PDF Lemma 2.1);
  - L1.2 def_1 lower bound (3 pi^2/8)(ell/u) eps^2 c_1 c_2 - PROVED (PDF
    Lemma 2.3);
  - L1.3 def_2 upper bound with cot-series certificate C_z < 0.337 - PROVED
    analytically given C_z (PDF Lemma 2.4);
  - L1.4 ratio def_2/def_1 <= 0.8256 < 1 - PROVED analytically given
    B(t) <= 9 (PDF Lemma 2.5).
Evidence/status: PROVED (analytic) modulo the three explicit constants
C_z < 0.337, B(t) <= 9, ratio 0.8256, which are certified by directed-rounding
interval cells (scripts 18-19; PDF Sec. 3.3-3.4).  The exact identity
G - Dbar = (def_1 - def_2)/u^2 is derived analytically and additionally
verified to 1e-42 at 480 points (evidence).
Edge cases: w = 2 endpoint included (all estimates continuous); w < 2 is the
deep-sliver region (L2).  Corrected parameter v = u/ell = -t cot t (not
-cot t); f(t) decreasing in v keeps the bound valid (recorded).

## L2 - Deep sliver: G(R,u) >= 25 for w <= 2, R >= 1500

Statement: for all u in (0, 2/sqrt(R)], G(R,u) >= 25.
Depends on: the four elementary bounds B_1, B_2, B_3, max(THB, D2B) with the
region split A/B/C/D (PDF Sec. 2.4, Sec. 3.1), analytic tails for R >= 57050
and R >= 1e8, and the certified grids (script 16, 424460 + 687915 + 193241
cells).  Region C (B_3) is fully analytic with min exactly 25 at
w_cap(R).  Medium region w >= 2, u in [0.02, 0.2]: monotonicity grid
(script 17, 115185 cells, Feynman-Hellmann P4).
Evidence/status: PROVED (elementary bounds + computer-assisted certification).
Worst certified values: 42724 / 293.36 / 25 / 77.67 (regions A/B/C/D).
Verifier note: the D-region bound requires pi - epsilon tan(pi/(4w)) > 0,
which holds on (w_cap, 2] (checked; the endpoint w = 2 corner is the worst
cell, bound 77.67).

## T1 - convergence and near-minimizer convergence

Statement: lim_R R*m_R = Dbar(u*); every near-minimizer sequence
(D_R(u_R) <= m_R + R^{-2}) satisfies u_R -> u*.
Depends on: L1 (w >= 2 lower bound), L2 (w <= 2 lower bound), T2 (Dbar >=
Dbar(u*) and strict monotonicity), T3 (25 > Dbar(u*)), and the fixed-u
convergence G(R,u*) -> Dbar(u*) (from L1.1 + L1.3 with u fixed at u*).
Evidence/status: PROVED (PDF Sec. 2.6), four steps (i) limsup, (ii) liminf,
(iii) limit, (iv) near-minimizer convergence by the accumulation-point
argument (u_inf = 0 or 1/2 excluded by tail limits; u_inf in (0,1/2) forced
to u* by continuity + strict monotonicity).
Edge cases: near-minimizer sequences with w_R <= 2 infinitely often are
excluded by G >= 25 > Dbar(u*) (T3 margin 0.0561).

## Synthesis

THEOREM_A = T1 + T2 + T3 (PDF Corollary 2.7).  All obligations above are
CLOSED within this run; the run-level status is CANDIDATE_COMPLETE_PROOF
(self-audited) pending an independent verifier pass per the upstream skill
revision policy.