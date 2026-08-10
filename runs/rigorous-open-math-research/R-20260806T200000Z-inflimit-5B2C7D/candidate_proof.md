# Candidate proof - Theorem A (INF R->infinity limit of the n=1 adjacent gap)

Run: R-20260806T200000Z-inflimit-5B2C7D
Status: CANDIDATE_COMPLETE_PROOF (self-audited in audit_report.md; per the
upstream skill revision policy an independent verifier pass remains the
closing step before the manager closes this portfolio item).
All files ASCII punctuation, UTF-8 without BOM.

The full formal text (10 pages, xelatex, zero warnings) is delivered as
docs/SL_gap_n1_inf_limit_proof.pdf (source docs/SL_gap_n1_inf_limit_proof.tex).
This document is the markdown summary with the theorem-level argument;
section references (e.g. Sec. 2.3) point to that PDF.  Strict proofs are in
Sec. 2 of the PDF; computer-assisted certification of three explicit
constants is in Sec. 3; Sec. 4 is numerical evidence only (explicitly NOT a
proof).  The same separation is respected here: the argument below is
analytic except for the explicitly flagged interval certifications.

## 1. Theorem statement (normalized)

Dirichlet string -y'' = lambda rho y on (0,1), y(0) = y(1) = 0.  Symmetric
well family: for u in (0,1/2),
  rho_{R,u} = R on (0,u) union (1-u,1),  rho_{R,u} = 1 on (u,1-u).
0 < lambda_1(R,u) < lambda_2(R,u) are the first two eigenvalues,
D_R(u) = lambda_2 - lambda_1,  m_R = inf_{u in (0,1/2)} D_R(u).

Limiting system: mu_1bar(u) = pi^2/(4u^2); a(u) in (pi/2, pi) the unique
root of tan a = -a(1/2 - u)/u;  mu_2bar(u) = (a(u)/u)^2;
Dbar(u) = mu_2bar(u) - mu_1bar(u);
S(u) = mu_1bar(u)*2/u - mu_2bar(u)*sin^2(a(u))/I_2(u),
I_2(u) = u/2 - u sin(2a(u))/(4a(u)).
u* in (0,1/2) is the (unique) root of S(u) = 0, equivalently of Dbar'(u) = 0.

Theorem A:  lim_{R->inf} R*m_R = Dbar(u*) = 24.9438661384324769... < 3 pi^2,
and every near-minimizer sequence u_R (D_R(u_R) <= m_R + R^{-2}) converges to
u*.

Scope: the limit over the symmetric subfamily.  The equality of this inf with
the full box-class inf (1 <= rho <= R measurable) is portfolio item O3a/C1
and is NOT part of this theorem.

## 2. Proof decomposition: T1 (convergence), T2 (monotone structure), T3 (value)

Theorem A = T1 + T2 + T3 (PDF Sec. 2.7).  T2 and T3 are fully analytic
(except the interval enclosures in T3); T1 rests on Lemma A'' (Sec. 2.3),
the deep-sliver lemma (Sec. 2.4), and T2/T3.

## 3. T2: unique critical point and global strict minimum of Dbar

Parametrize a in (pi/2, pi) |-> u(a) = a/(2(a - tan a)) in (0,1/2); this is a
diffeomorphism (u' > 0; u -> 0+ as a -> pi/2+, u -> 1/2- as a -> pi-).

Sign chain (PDF Sec. 2.5, all identities elementary):
  J'(a) = 4a K~(a)/sin^2 a,   G'(a) = 4 sin^2 a * J(a),
  Dbar'(u(a)) = S(u(a)) = -[4(a - tan a)^3/(a^3(2a - sin 2a))] * G(a),
  K~(a) = -a^2 + 3 sin^2 a + (3/2)a sin 2a = sin^2 a * h(a),
  h'(a) sin^3 a = 3 cos a sin^2 a - 5a sin a + 2a^2 cos a < 0  on (pi/2, pi)
  (each term negative: cos a < 0, sin a > 0, a > 0).
  J(a) = 4a^3 cot a + 6a^2 - pi^2,   G(a) = 8a^3 sin^2 a - pi^2(2a - sin 2a).

From h strictly decreasing with h(pi/2) > 0 and h(pi-) = -inf: K~ has a
unique zero a_1.  Then J increases on (pi/2, a_1) and decreases on (a_1, pi)
with J(pi/2) > 0 and J(pi-) = -inf, so J has a unique zero a* in (a_1, pi).
Then G increases on (pi/2, a*) and decreases on (a*, pi) with G(pi/2) = 0,
G'(pi/2) > 0, G(pi) < 0: G has a unique zero a_G in (pi/2, pi), sign + then
-.  The prefactor in S(u(a)) is strictly negative, so S < 0 on (0, u*),
S = 0 at u* = u(a_G), S > 0 on (u*, 1/2).  Since Dbar' = S, Dbar decreases on
(0,u*) and increases on (u*,1/2); with Dbar -> +inf (u->0+) and Dbar -> 3 pi^2
(u->1/2-), u* is the global strict minimizer.  Correction note: the unique
zero of G is a_G ~ 2.2766; the zero of J is a* ~ 1.9856.  An earlier draft
mixed the two zeros (G(a*) = G'(a*) = 0 cannot both hold); the delivered text
uses the correct G-zero a_G throughout.

## 4. T3: interval enclosure

mpmath.iv interval bisection encloses
  u* in [0.32992250812006654958, 0.32992250812006654960],
  Dbar(u*) in [24.9438661384324768968, 24.9438661384324769084],
  margin 3 pi^2 - Dbar(u*) >= 4.664947  (hence 25 - Dbar(u*) > 0.0561).
Script: reproducibility/05_interval_value.py (PASS).

## 5. Lemma A'': R*D_R(u) >= Dbar(u) for w := u sqrt(R) >= 2  (PDF Sec. 2.3)

Phase coordinates: theta_k = sqrt(mu_k) u with theta_1 = pi/2 - delta_1,
theta_2 = pi/2 + delta_2; z_k = sqrt(lambda_k) (1/2 - u);
epsilon = 1/sqrt(R), ell = 1/2 - u, alpha = (ell/u) epsilon^2.
Secular equations: tan delta_1 = epsilon tan z_1,
tan delta_2 = epsilon cot z_2.

Exact identity (verified to 1e-42 at 480 points; analytic derivation in the
PDF):
  G(R,u) - Dbar(u) = (def_1 - def_2)/u^2,
  def_1 = pi delta_1 - delta_1^2,  def_2 = (theta_2bar - theta_2)(theta_2bar + theta_2),
  theta_2bar = a(u).

Lower bound for def_1 (PDF Lemma 2.3): using tan z >= z, arctan x >= x - x^3/3
and the phase bracket delta_1 <= delta_1+ (PDF Lemma 2.1(a)):
  def_1 >= (3 pi^2/8)(ell/u) epsilon^2 c_1 c_2,
  c_1 >= 0.99319...,  c_2 >= 0.99996... .

Upper bound for def_2 (PDF Lemma 2.4): psi_2 = theta_2bar - theta_2 >= 0 (PDF
Lemma 2.1(d)) satisfies, from tan psi_2 = (A - B)/(1 + AB) with
A = tan(theta_2bar - pi/2) = u/(theta_2bar ell), B = tan delta_2:
  psi_2 [ (tan psi_2/psi_2)(1 + AB) + u/(theta_2bar theta_2 ell) ] = epsilon R(z_2),
  R(z) = 1/z - cot z <= C_z z on [0, pi/8],  C_z = R(pi/8)/(pi/8) < 0.337.
With z_2 <= pi/8 (PDF Lemma 2.1(c)):
  def_2 <= C_z theta epsilon^2 (ell/u) (t + theta)/(1 + v(v+1)/(t theta) - delta),
  t = theta_2bar,  v = u/ell = -t cot t,  delta <= 4.5e-4.

Ratio (PDF Lemma 2.5):
  def_2/def_1 <= [4 C_z/(3 pi (pi/2 - delta_1+) c_2)] * B(theta) * (1 + 4.6e-4)
  <= 0.8256 < 1,
where B(theta) <= B(t) = 2 t^4/(t^2 + v^2 + v) <= 9: for t <= 3/sqrt(2) by
B(t) <= 2 t^2 <= 9 analytically; for t in [3/sqrt(2), pi) certified by 500
directed-rounding interval cells with worst cell bound 5.422510 (script 19).
Hence def_2 < def_1, so G(R,u) > Dbar(u).  Lemma A'' is analytic except the
three explicit constants C_z < 0.337, B(t) <= 9, ratio 0.8256, which are
certified by interval arithmetic (scripts 18-19) as documented in PDF Sec. 3.

Correction note (recorded): the parameter v is v = u/ell = -t cot t (from
tan t = -t ell/u), NOT -cot t as in the earliest draft and script 19 v1.
Because f(t) = 2t^4/(t^2+v^2+v) is decreasing in v >= 0, the old certificate
remained a valid upper bound, but the formula is now correct; the certified
f-maximum is 5.4225 (vs 8.3 with the wrong v).

## 6. Deep sliver: R*D_R(u) >= 25 for w <= 2  (PDF Sec. 2.4 + Sec. 3.1)

For w in (0,2], R >= 1500, the region is covered by four elementary bounds
with certified worst values (script 16, all >= 25):
  A: w in (0,0.19], B_1 = 3 pi^2 R - 32 pi^4 R epsilon w^2/c, worst 42724;
  B: w in [0.19, w_c], B_2 = pi^2 R((1 - 2 epsilon w)^{-2} - 1), worst 293.36;
  C: w in (w_c, w_cap], B_3 = pi^2 R(1/(4w^2) - 1), analytic, min exactly 25
     at w = w_cap(R) = (1/2)(1 + 25/(pi^2 R))^{-1/2};
  D: w in (w_cap, 2], max(THB, D2B), worst 77.67,
     THB = (pi/2 - theta_1+)(pi/2 + theta_1-)/(w^2 epsilon^2),
     D2B = delta_2-(pi - epsilon tan(pi/(4w)))/(w^2 epsilon^2).
Grid [1500, 1e8] geometric; analytic tails for R >= 57050 (regions A, B) and
R >= 1e8 (region D: THB >= 0.1529 sqrt(R) >= 1529).  The medium region
w >= 2, u in [0.02, 0.2] is additionally certified by a monotonicity grid
(script 17, 115185 cells, worst corner bound 27.99 >= 25; Feynman-Hellmann
monotonicity d mu_k/du < 0, d mu_k/dR > 0).  These certifications do NOT rely
on Lemma A'' and are independent of Sec. 2.3.

## 7. T1: convergence and near-minimizer convergence  (PDF Sec. 2.6)

(i) limsup <= Dbar(u*): fix u*, Lemma 2.1 + Lemma 2.4 give delta_1 -> 0 and
psi_2 -> 0 as R -> inf, hence G(R, u*) -> Dbar(u*); m_R <= D_R(u*).

(ii) liminf >= Dbar(u*): for every u in (0,1/2) with R >= 1500,
  - w <= 2: G >= 25 > Dbar(u*)  (Sec. 6 + T3 margin 0.0561);
  - w >= 2: G >= Dbar(u) >= Dbar(u*)  (Lemma A'' + T2).
Hence R*m_R = inf_u G(R,u) >= min{25, Dbar(u*)} = Dbar(u*) for all R >= 1500.

(iii) Limit follows.  (iv) Near-minimizer convergence: if w_R <= 2 infinitely
often then G >= 25 > Dbar(u*) contradicts R*D_R(u_R) -> Dbar(u*); eventually
w_R >= 2, so Dbar(u_R) <= G(R,u_R) -> Dbar(u*) and Dbar(u_R) >= Dbar(u*);
thus Dbar(u_R) -> Dbar(u*).  Any accumulation point u_inf in [0,1/2]: u_inf = 0
and u_inf = 1/2 are excluded by the tail limits (Dbar -> +inf resp. 3 pi^2);
for u_inf in (0,1/2) continuity plus the strict monotonicity of Dbar (T2)
forces u_inf = u*.  Hence u_R -> u*.

## 8. Premise ledger (rechecked in this run)

- Secular/phase equations for piecewise constant rho: derived from first
  principles in the PDF (Sec. 2.1) via the transfer-matrix matching; not cited
  from memory.  Cross-checked numerically (script 03).
- Feynman-Hellmann monotonicity d mu_k/du < 0, d mu_k/dR > 0 used only in the
  medium-region certification (script 17): standard theorem, hypotheses met
  (piecewise constant rho, moving u/R parameters).
- cot-series remainder R(z)/z increasing with positive coefficients: the
  Bernoulli expansion of cot is standard; the sign of the coefficients
  c_k = 2^{2k}|B_{2k}|/(2k)! > 0 is classical (rechecked; script 19 certifies
  the numerical constant C_z only).
- Interval arithmetic: mpmath.iv, outward rounding; enclosures double-checked
  with an independent directed-rounding Decimal engine in scripts 16-19.
- No external literature result is a premise of Theorem A; Keller 1976,
  Mahar-Willner 1976, Willner-Mahar 1982 are context only (see
  status_and_literature.md).

## 9. Status and remaining gaps

No open obligation remains inside this run's contract (T1, T2, T3 all closed).
Status CANDIDATE_COMPLETE_PROOF (self-audited): the upstream revision policy
requires an independent verifier pass before the manager closes the portfolio
item.  Out of scope, explicitly NOT closed here:
- O3a/C1: equality of the symmetric-family inf with the full box-class inf;
- the SUP side (barrier family [1,R,1]) limit D -> 4 pi^2 (different
  framework, center-mass pinning);
- n >= 2 adjacent gaps.