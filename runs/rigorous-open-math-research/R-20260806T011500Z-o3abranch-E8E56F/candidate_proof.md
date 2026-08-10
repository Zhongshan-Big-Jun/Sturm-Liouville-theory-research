# Candidate proof: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

This file contains the rigorously proved propositions of this run (P1-P4) and
the corrected structural conjecture (C1) with its numerical support.  It does
NOT claim a proof of O3a: Lemma A as stated is refuted with a rigorous
interval-arithmetic certificate (reproducibility/cert_ce1.py, see
counterexample_log.md CE-1 and audit_report.md G1), and Lemmas B, C remain open.

Notation (matching the source): rho_(a,b) = R on (a,b), 1 elsewhere,
0 < a < b < 1, R > 1.  s_k = sqrt(lambda_k), y_k solves
-y_k'' = lambda_k rho y_k, y_k(0) = 0, y_k'(0) = 1; u_k = y_k/||y_k||_{L^2(rho)};
f = lambda_1 u_1^2 - lambda_2 u_2^2; R1 = f(a), R2 = f(b);
D = lambda_2 - lambda_1.  v = y_2/y_1 is strictly decreasing on (0,1)
(O1c, prior run; re-verified).  Good root: R1 = R2 = 0 with a = x_-, b = x_+.

## P1 (Feynman-Hellmann with the eigenvalue factor)

Theorem.  On the barrier family, for k = 1, 2:
  d lambda_k/da = (R-1) lambda_k u_k(a)^2,   d lambda_k/db = -(R-1) lambda_k u_k(b)^2.
Hence dD/da = -(R-1) R1 and dD/db = (R-1) R2.

Proof.  Write rho = 1 + eps chi_(a,b) with eps = R-1 and regard lambda_k(eps).
For the problem -y'' = lambda rho y on (0,1), y(0) = y(1) = 0, with
normalization int rho u^2 = 1, differentiate the Rayleigh quotient
lambda = int (u')^2 dx / int rho u^2 dx at the eigenfunction:

  d lambda/d eps = [2 int u''u_eps dx - lambda(int rho_eps u^2 dx + 2 int rho u u_eps dx)]/N
                 = -lambda int rho_eps u^2 dx,

where N = int rho u^2 = 1, int u' u_eps' dx = -int u'' u_eps dx =
lambda int rho u u_eps dx (integration by parts twice, u(0) = u(1) = 0), and
the u_eps terms cancel.  Here d rho/d a = -(R-1) delta_a and
d rho/d b = +(R-1) delta_b, giving the two formulas.  The two displayed
identities for D follow by subtracting k = 2 and k = 1.

Verification.  (a,b,R) = (0.42, 0.56, 4): FD d lambda_1/da = 16.739241 vs
(R-1) lambda_1 u_1(a)^2 = 16.739; FD d lambda_2/da = 55.626551 vs
3*37.097975*0.49981660 = 55.627; dD/da = 38.88731049 = -(R-1) R1
(R1 = -12.96243683).  All to 1e-6.

Note: the naive formula without the lambda factor is WRONG for this
normalization and was initially misused by this run's author; the factor is
essential (see research_ledger R-101).

## P2 (T3, residual exactness)

Theorem.  On 0 < a < b < 1:  dR1/db = -dR2/da.

Proof.  By P1, dD/da = -(R-1) R1 and dD/db = (R-1) R2.  D is C^2 on the open
set: the secular function M01(s; a, b, R) is real-analytic in (s, a, b), the
Dirichlet eigenvalues of a positive bounded weight are simple (standard SL
theory), so by the implicit function theorem s_k(a,b), hence D(a,b), are
real-analytic.  Schwarz's theorem: d^2D/db da = d^2D/da db, i.e.
-(R-1) dR1/db = (R-1) dR2/da.  QED.

Verification.  At (0.42,0.56,4), (fp R=4), (0.45,0.55,10), (0.3,0.7,2):
dR1/db + dR2/da ~ 1e-8.

## P3 (branch-slope identities and Hessian reduction at a good root)

Theorem.  At a point (a,b) with R1 = R2 = 0 (good root), with
A = dR1/da, B = dR2/da, C = dR2/db (partial derivatives, s_k implicit):

  (i) g1' = A/B and g2' = -B/C (slopes of the two residual curves through the
      point);
  (ii) A = -D_aa/(R-1), B = D_ab/(R-1), C = D_bb/(R-1);
  (iii) g1' = -D_aa/D_ab, g2' = -D_ab/D_bb, h' = -D_aa/D_ab + D_ab/D_bb;
  (iv) if D_aa < 0, D_bb < 0, D_ab > 0 then g1', g2' > 0, and if moreover
      D_aa D_bb > D_ab^2 then h' > 0 (i.e. the Hessian of D is negative
      definite at the point);
  (v) at the symmetric fixed point (a, 1-a): A = -C (reflection), hence
      g1' g2' = -A/C = 1 and h' = g1' - 1/g1'.

Proof.  (i) Along Gamma_1: 0 = dR1/da = A + (dR1/db) g1' = A - B g1' by P2,
hence g1' = A/B.  Along Gamma_2: 0 = dR2/da = B + C g2', hence g2' = -B/C.
(ii) P1 gives D_a = -(R-1) R1 and D_b = (R-1) R2; differentiate once more:
D_aa = -(R-1) A, D_ab = (R-1) B, D_bb = (R-1) C.  (iii) substitute (ii)
into (i).  (iv) immediate from (iii) and the sign assumptions (B = D_ab/(R-1)
> 0, C = D_bb/(R-1) < 0).  (v) at the symmetric point the reflection
sigma(a,b) = (1-b, 1-a) fixes (a, 1-a); D is invariant under sigma, so
D_aa = D_bb there (the Hessian commutes with the reflection), hence
A = -D_aa/(R-1) = -D_bb/(R-1) = -C.  Then g1' g2' = (A/B)(-B/C) = -A/C = 1.
QED.

Verification.  R = 4 fp: A = 352.05, B = 127.92, C = -352.05, g1' = 2.752,
g2' = 0.363, h' = 2.389, det Jres = AC + B^2 = -107576 < 0, consistent with
(iv).  g1' g2' = 1 to ~1e-12 at all large-R fixed points (R up to 1e7).

Remark (proof-route obstruction).  The Hessian of D is NOT negative definite
on the whole triangle (violations with D_bb > 0 near a ~ 0.08 exist), so (iv)
can only hold on the branches.  Proving (iv) on the branches is exactly the
"second-order sensitivity" problem left open by the prior run; no clean
closed form for A, B, C was obtained in this run (the resolvent/Green
function representation was identified as the natural tool).

## P4 (R = 1 base facts)

Theorem.  For rho = 1 (R = 1), with the slope normalization:
  v(x) = y_2/y_1 = cos(pi x),  q = (s_1/s_2) sqrt(n_2/n_1) = 1/4,
  and f_0(x) = 2 pi^2 sin^2(pi x) (1 - 16 cos^2(pi x)),
  whose zeros in (0,1) are a0 = arccos(1/4)/pi and b0 = arccos(-1/4)/pi
  = 1 - a0, with x_- = a0, x_+ = b0.

Proof.  y_k = sin(k pi x)/(k pi); v = sin(2 pi x)/(2 sin(pi x)) = cos(pi x);
n_k = int_0^1 sin^2(k pi x)/(k^2 pi^2) dx = 1/(2 k^2 pi^2), so
q = (1/2) sqrt((1/8)/(1/2)) = 1/4.  f_0 = pi^2*2 sin^2(pi x)
- 4 pi^2*2 sin^2(2 pi x) = 2 pi^2 sin^2(pi x)(1 - 16 cos^2(pi x)).
Zeros: cos(pi x) = +/- 1/4.  QED.

Consequence: for R -> 1+, the branches Gamma_1, Gamma_2 degenerate to the
vertical line a = a0 and the horizontal line b = b0, and the common-range
endpoints limit to a0 and b0 (Lemma B's endpoint constants).  This is the
base point for the (incomplete) perturbation analysis of Route R-C.

## C1 (corrected structural conjecture; NUMERICALLY SUPPORTED, NOT PROVED)

Conjecture.  For every R > 1: h = g1 - g2 has exactly one zero in the common
range I = [a0, beta], where beta = min(a_max1(R), b0); the zero is the
symmetric fixed point a_fp(R).  Equivalently, O3a holds.

Supporting structure (numerics):
- h(a0) < 0 < h(beta) for all R in {1.02, ..., 1e7} (Lemma B, unproved).
- h' > 0 on the left part of I for all tested R; for R < ~1350, h' > 0 on all
  of I (Lemma A holds there); for R >= ~1350, h' < 0 on an interior interval
  near the right end, with h(b0) > 0, so h still crosses zero exactly once.
- h(b0) ~ 0.38/sqrt(R) -> 0+ and the negative-h' dip is bounded in magnitude
  (~4e-3 max at R ~ 3000, shrinking support), so no second zero is seen up to
  R = 1e6.

A proof of C1 requires: Lemma C (single-graph branches; every good root in
I), the endpoint signs of Lemma B, and a replacement for Lemma A that only
needs h to cross zero once (e.g. h' > 0 up to the fixed point and h > 0
after, or an explicit zero-counting argument).

## Status of the three task lemmas
- Lemma A (pointwise g1' > g2' on the whole common range): REFUTED
  rigorously for R >= ~1400 (CE-1, interval-arithmetic certificate
  reproducibility/cert_ce1.py).  Holds numerically for R <= 1000.
- Lemma B: OPEN (numerically verified; R -> 1+ perturbation incomplete).
- Lemma C: OPEN (numerically verified; no proof strategy found beyond
  single-component tracing).
