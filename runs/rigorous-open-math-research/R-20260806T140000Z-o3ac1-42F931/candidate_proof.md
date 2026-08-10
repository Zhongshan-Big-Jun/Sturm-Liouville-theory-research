# Candidate proof: C1 (unique zero of h = g1 - g2; O3a)

## Status line

RIGOROUS_PARTIAL_RESULT. The reflection theorem (Lemma R1-R4), the
good-root/zero-set reductions (Lemma R5) and the C1-reduction to the M-shape
(Lemma R6) are PROVED rigorously in this run (proofs below, all elementary).
Conjecture C1 itself (h = g1 - g2 has exactly one zero in the common range
I = [a0, beta] for every R > 1, at the symmetric fixed point) remains OPEN.
It is reduced to two structural facts (E1) endpoint signs and (M) the M-shape
of h', which are numerically verified for R in {1.05, 1.2, 2, 4, 10, 100,
1000, 1500, 3000, 1e4, 1e5, 1e6} but not analytically closed.  No claim of a
complete proof is made.

## Notation

Barrier family, R > 1, 0 < a < b < 1, rho = R on (a,b), 1 elsewhere,
Dirichlet on [0,1].  s_k = sqrt(lambda_k); y_k slope-normalized
(y_k(0) = 0, y_k'(0) = 1); u_k = y_k/||y_k||_{L^2(rho)};
f = lambda_1 u_1^2 - lambda_2 u_2^2; R1 = f(a), R2 = f(b);
v = y_2/y_1 (strictly decreasing on (0,1), O1c, re-verified);
x_- < x_+ the (at most two) zeros of f with v(x_-) = q > 0, v(x_+) = -q,
q = (s_1/s_2) sqrt(n_2/n_1).  Good root: R1 = R2 = 0 with a = x_-, b = x_+
(equivalently v(a) = q, v(b) = -q).

Branches (main sheets through the symmetric fixed point): Gamma_1 =
{(a, g1(a)) : a in I_1}, I_1 = [a0, a_max1]; Gamma_2 = {(a, g2(a)) : a in I_2},
I_2 = [1 - g1(a_max1), b0].  Common range I = I_1 cap I_2 = [a0, beta],
beta = min(a_max1, b0).  a0 = arccos(1/4)/pi ~ 0.419569, b0 = 1 - a0.
h(a) = g1(a) - g2(a) on I.  a_fp(R): the symmetric fixed point (exists by O2,
assumed in the completion chain).  sigma(a,b) = (1-b, 1-a).

## Lemma R1 (reflection of the residuals)

For all 0 < a < b < 1 and R > 1:

    R1(sigma(a,b)) = R2(a,b),   R2(sigma(a,b)) = R1(a,b).

Proof.  Let (a',b') = sigma(a,b).  The density of the reflected problem is
rho'(x) = rho(1-x).  The map y -> phi, phi(x) = y(1-x), is a bijection between
the eigenfunctions of the (a,b)-problem and the (a',b')-problem with the same
eigenvalue; the L^2(rho)-norms are equal by the substitution t = 1-x, so
u'_k(x) = u_k(1-x) and f'(x) = f(1-x).  Hence R1(a',b') = f'(a') = f(1-a') =
f(b) = R2(a,b), and R2(a',b') = f'(b') = f(1-b') = f(a) = R1(a,b).  QED.

Verification (this run): max|R1(a,b) - R2(sigma(a,b))| ~ 1e-9..1e-11 for
R in {2, 4, 100, 1000, 1e4} over dense branch samples; identities hold to
machine precision at generic points (1e-16).

## Lemma R2 (sigma(Gamma_1) = Gamma_2 on the main sheets)

sigma maps the main-sheet branch Gamma_1 onto the main-sheet branch Gamma_2;
consequently, on the common range I,

    g2(a) = 1 - g1^{-1}(1 - a).                    (R2.1)

Proof.  Sign tracking under reflection: the slope-normalized ratio of the
reflected problem is v'(x) = c_v v(1-x) with c_v = y_2'(1)/y_1'(1) < 0
(y_1'(1) < 0, y_2'(1) > 0 for the first two Dirichlet modes on (0,1)).
If (a,b) in Gamma_1 (R1 = 0, v(a) = q > 0, a = x_-), then by Lemma R1,
R2(sigma(a,b)) = 0.  Moreover v'(b') = c_v v(1 - b') = c_v v(a) = c_v q < 0,
so b' = x_+' and v'(a') = c_v v(b) = c_v (-q) = -c_v q > 0, so a' = x_-'.
Hence sigma(a,b) in Gamma_2 with the sign-consistency conditions.  sigma is an
involution and fixes the symmetric fixed point (a_fp, 1-a_fp), so the image of
the main-sheet component through (a_fp, 1-a_fp) is the main-sheet component of
Gamma_2 (the component through (b0, b0) in the limit R -> 1+; see H2/Lemma C
for the single-component structure).  Writing the image point (1-g1(a), 1-a)
in Gamma_2 gives g2(1 - g1(a)) = 1 - a; substituting a -> g1^{-1}(1 - a)
yields (R2.1) on the a-range [1 - g1(a_max1), b0], which contains I.  QED.

## Lemma R3 (h-reflection formulas)

On I, with u(a) = g1^{-1}(1 - a):

    h(a) = g1(a) - 1 + u(a),                        (R3.1)
    h'(a) = g1'(a) - 1/g1'(u(a)).                   (R3.2)

Proof.  (R3.1): h = g1 - g2 and g2(a) = 1 - g1^{-1}(1-a) by Lemma R2.
(R3.2): differentiate (R3.1); u'(a) = -1/g1'(u(a)) by the inverse function
theorem (g1' > 0 on I, verified; branch slope positivity is part of Lemma C).
QED.

## Lemma R4 (integral identity)

On I, with u(a) = g1^{-1}(1 - a):

    h(a) = integral from u(a) to a of (g1'(t) - 1) dt.    (R4.1)

Proof.  g1(u(a)) = 1 - a, so h(a) = g1(a) - 1 + u(a) = g1(a) - g1(u(a)) - (a
- u(a)) = integral (fundamental theorem of calculus).  QED.

Remark.  The mean-value form h(a) = (a - u(a))(g1'(xi) - 1) with xi between
u(a) and a is an immediate corollary; it shows that the sign of h is the sign
of (a - u(a)) times the sign of (g1'(xi) - 1), but the naive sufficient
condition "g1' > 1 on I" is FALSE for large R (g1' dips to ~0.98 near
a ~ 0.42-0.44 for R ~ 1000..1e6; see counterexample_log CE-3), so the
integral form (R4.1) is the correct exact statement to attack.

## Lemma R5 (good roots = zeros of h; algebraic reductions)

(i) Every solution of the system R1(a,b) = R2(a,b) = 0 with 0 < a < b < 1 is
a sign-consistent good root.
(ii) On I, h(a) = 0 if and only if (a, g1(a)) is a good root.
(iii) On I, h(a) = 0 if and only if a is a fixed point of
J(a) = 1 - g1(1 - g1(a)).

Proof.  (i) f has at most two zeros (O1c: v strictly decreasing, f = 0 iff
|v| = q), namely x_- < x_+.  If f(a) = f(b) = 0 with a < b, then {a, b} =
{x_-, x_+} as sets, and the ordering a < b forces a = x_-, b = x_+.  Hence
v(a) = q > 0, v(b) = -q < 0: sign-consistent good root.
(ii) h(a) = 0 iff g1(a) = g2(a) iff (a, g1(a)) in Gamma_1 cap Gamma_2; by the
definition of the branches this is exactly a good root with b = g1(a).
(iii) h(a) = 0 iff g1(a) = g2(a) = 1 - g1^{-1}(1-a) iff 1 - g1(a) =
g1^{-1}(1-a) iff g1(1 - g1(a)) = 1 - a iff a = 1 - g1(1 - g1(a)) = J(a).  QED.

Consequence.  C1 is equivalent to: the real-analytic system {R1 = 0, R2 = 0}
has exactly one solution in {0 < a < b < 1} for every R > 1 (the symmetric
fixed point).  Equivalently, Gamma_1 and Gamma_2 cross exactly once.

## Lemma R6 (C1-reduction: endpoint signs + M-shape)

For a fixed R > 1, C1 holds provided the following conditions hold:

(E1) h(a0) < 0 and h(beta) > 0;
(M)  h' has at most two zeros x1 <= x2 in (a0, beta); if two zeros exist they
     are simple, x1 < fp < x2, h(x1) < 0 < h(x2), and h' < 0 near a0 and near
     beta (sign pattern - + -); if no zero exists then h' > 0 on I;
(Z)  h(fp) = 0.

Proof.  If h' > 0 on I (no critical points), h is strictly increasing and
(E1) gives exactly one zero.  If h' has exactly two zeros x1 < x2 with the
sign pattern - + -, then h is strictly decreasing on [a0, x1], increasing on
[x1, x2], decreasing on [x2, beta].  Hence h < 0 on [a0, x1] (it starts at
h(a0) < 0 and decreases), h crosses zero exactly once on (x1, x2) (strictly
increasing from h(x1) < 0 to h(x2) > 0), and h > 0 on [x2, beta] (strictly
decreasing from h(x2) > 0 down to h(beta) > 0).  By (Z) the unique zero is
fp.  QED.

## Numerical verification (evidence, not proof)

Scripts and data (run root reproducibility/): shape_v6.json, dip_study.json,
final_shape.json, g1p_profile runs, verify_refl3.py logic.  R values
{1.05, 1.2, 2, 4, 10, 100, 1000, 1500, 3000, 1e4, 1e5, 1e6}:

- h(a0) < 0 and h(beta) > 0 for every tested R; h(beta) -> 0+ as R -> inf
  (h(b0) ~ +0.38/sqrt(R)), h(a0) ~ -0.38/sqrt(R).
- h'(fp) > 0 for every tested R; g1'(fp) -> ~1.4102 (consistent with sqrt(2)),
  h'(fp) -> ~0.70 (sqrt(2) - 1/sqrt(2)).
- h > 0 on (fp, beta] for every tested R (min values 1e-5..8e-3, strictly
  positive with margin).
- M-shape: for R <= ~1350, h' > 0 on all of I; for R >= ~1500 (narrow dip)
  and R >= ~3000 (both dips), h' < 0 on an interval left of fp
  (a ~ 0.43-0.46) and on an interval right of fp (a ~ 0.52..beta); both dips
  are shallow (|h'| <= ~0.012) and h stays positive on (fp, beta].
- Nondegeneracy: det J_res = AC + B^2 < 0 at the symmetric fixed point for
  every tested R (e.g. R=4: -107576.4; R=1e6: -1.4); det Hess(D) > 0 with
  D_aa, D_bb < 0 (fp is a local maximum of D = lambda_2 - lambda_1).
- sigma(Gamma_1) = Gamma_2 with residual ~1e-9..1e-11; identities (R2.1),
  (R3.1), (R3.2) verified to ~1e-6 (trace-limited).

## Exact remaining gap

A proof of C1 requires, for every R > 1:
(1) E1: h(a0) < 0 and h(beta) > 0 (equivalently g1(b0) > b0 when beta = b0);
(2) M: the M-shape of h' (at most two zeros, ordered around fp, h(x1) < 0 <
    h(x2), sign pattern - + -).
Both are numerically verified over the tested R-grid but not analytically
closed.  The candidate routes and their failure points are registered in
approach_registry.md; the chronological record is in research_ledger.md.

## Summary of failed routes (honest registration)

- Lemma A (g1' > g2' pointwise on I): FALSE for R >= ~1350, interval-
  arithmetic certificate CE-1 (prior run, rechecked here).  Not usable.
- "g1' > 1 on I" as a sufficient condition (via the MVT form): FALSE for
  R >= ~1000 (g1' dips below 1 near a ~ 0.42-0.44); see CE-3.  The integral
  form R4 is the correct exact statement.
- Direct sheet tracing of Gamma_2 near the right end is hazardous at large R
  (three R2-roots with v(b) < 0 at R = 1500, a = 0.57364; only the largest is
  the main sheet).  The reflection formula (R2.1) sidesteps this: g2 is
  computed from the single-sheeted g1.
- The R -> 1+ perturbation route (naive IFT on the branch functions) is
  degenerate: at R = 1 the branches are vertical/horizontal lines and the
  good root (a0, b0) is a limit point of the degenerate family; a clean
  analytic expansion was not closed in this run (registered in ledger).
