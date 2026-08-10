# Candidate proof - O1 reduction theorem (REVISED, repair run R-20260806T140000Z-o1revise-2ED02A)

Status: CANDIDATE_COMPLETE_PROOF (self-audited; independent re-audit by the
manager remains the closing step, per the upstream skill revision policy).
This document replaces the draft obligations O1a (repair R1) and O1b
(repairs R2 + R4) and restates O1c (repair R3) with the explicit sign
convention.  O1c-O1f content is audited as unchanged-correct; the repairs
are integrated line by line.

## 1. Theorem statement (normalized, unchanged from the draft)

Let R > 1 and K = { rho measurable on [0,1] : 1 <= rho <= R a.e. }.  For the
Dirichlet string -y'' = lambda rho y on (0,1), y(0) = y(1) = 0, with
eigenvalues 0 < lambda_1(rho) < lambda_2(rho) and D(rho) := lambda_2(rho)
- lambda_1(rho):

(i)  sup_{rho in K} D(rho) = max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),
     rho^{bar}_{a,b} = R on (a,b), 1 elsewhere;
(ii) inf_{rho in K} D(rho) = min_{0<=a<=b<=1} D(rho^{well}_{a,b}),
     rho^{well}_{a,b} = 1 on (a,b), R elsewhere;

and both extrema over the two-parameter families are attained.

Edge cases are inside the closed families: a = b gives rho = 1 (D = 3 pi^2),
(a,b) = (0,1) gives rho = R (D = 3 pi^2 / R); a = 0 or b = 1 give the 2-block
members.  The case R = 1 is excluded from the statement (K = {1}, trivial).

## 2. Notation and conventions

- T_0 = inverse of -d^2/dx^2 on L^2(0,1) with Dirichlet boundary conditions,
  with Green kernel G(x,t) = min(x,t)(1 - max(x,t)); G is symmetric,
  0 <= G <= 1/4, and T_0 is self-adjoint positive compact with eigenvalues
  1/(k^2 pi^2).
- M_phi = multiplication by phi.  T_rho := T_0 M_rho.
- S_rho := M_{sqrt(rho)} T_0 M_{sqrt(rho)}, the operator with symmetric kernel
  K_rho(x,t) = sqrt(rho(x)) G(x,t) sqrt(rho(t)).  S_rho is self-adjoint,
  positive, Hilbert-Schmidt (kernel bounded).  It is similar to T_rho:
  S_rho = M_{sqrt(rho)} T_rho M_{sqrt(rho)}^{-1}, so the spectra coincide.
  (NOTE: the audit/packet expression "rho^(1/2) T_rho rho^(1/2)" is not
  symmetric as written; the intended operator is the kernel form above, which
  is used throughout.)
- Eigenfunctions u_k(rho), k = 1, 2, are L^2(rho)-normalized:
  int_0^1 rho u_k^2 dx = 1, and u_1 > 0 on (0,1).  u_2 has exactly one
  interior zero z_0(rho) (Sturm oscillation), and the sign convention
  (repair R3) is u_2 > 0 on (0, z_0), u_2 < 0 on (z_0, 1).
- f(rho) := lambda_1 u_1^2 - lambda_2 u_2^2, continuous on [0,1]
  (u_k, u_k' continuous; rho enters only through lambda_k and the
  normalization).
- Lambda bounds: for every rho in K, k^2 pi^2 / R <= lambda_k(rho)
  <= k^2 pi^2 (Rayleigh quotient comparison with the constant densities;
  eigenvalues decrease as the density increases pointwise).

## 3. Lemma 1 (O1a, repair R1): L^1 continuity of lambda_k on K

Claim. For every k >= 1 and rho, sigma in K:
  |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
  <= (R/4) ||rho - sigma||_1^{1/2},
hence lambda_k is continuous in the L^1 topology on K, with
  |lambda_k(rho) - lambda_k(sigma)| <= (R/4)(k^2 pi^2)^2 ||rho-sigma||_1^{1/2}.

Proof.
(a) Eigenvalue identity.  The nonzero spectra of T_rho and S_rho coincide by
similarity, and the eigenvalue equation -y'' = lambda rho y, y(0) = y(1) = 0
is equivalent to T_rho y = (1/lambda) y (since T_rho = T_0 M_rho, T_rho y = T_0(rho y) = y/lambda), so the k-th nonzero eigenvalue
of S_rho is mu_k(S_rho) = 1/lambda_k(rho).  (Explicitly, S_rho(sqrt(rho) y)
= (1/lambda) sqrt(rho) y.)
(b) Hilbert-Schmidt bound.  For rho, sigma in K, write
  A(x) := |rho(x) - sigma(x)|,
  Delta(x,t) := sqrt(rho(x))sqrt(rho(t)) - sqrt(sigma(x))sqrt(sigma(t)).
Then
  |Delta(x,t)| <= sqrt(rho(t)) |sqrt(rho(x)) - sqrt(sigma(x))|
                  + sqrt(sigma(x)) |sqrt(rho(t)) - sqrt(sigma(t))|
  <= (sqrt(R)/2)( A(x) + A(t) ),
using |sqrt(u) - sqrt(v)| = |u - v|/(sqrt(u)+sqrt(v)) <= |u-v|/2
(u, v >= 1).  With G <= 1/4 and the symmetry of G in x, t,
  ||S_rho - S_sigma||_HS^2 = int int G(x,t)^2 Delta(x,t)^2 dx dt
  <= (R/4) int int G^2 (A(x)+A(t))^2 dx dt
  = (R/2) [ int int G^2 A(x)^2 dx dt + int int G^2 A(x) A(t) dx dt ]
  <= (R/32) ( ||A||_2^2 + ||A||_1^2 ),
because int int G^2 A(x)^2 dx dt <= (1/16)||A||_2^2 and
int int G^2 A(x) A(t) dx dt <= (1/16)||A||_1^2.  Since |A| <= R - 1 a.e.,
||A||_2^2 <= (R-1)||A||_1 <= R||A||_1 and ||A||_1^2 <= (R-1)||A||_1
<= R||A||_1, so
  ||S_rho - S_sigma||_HS^2 <= (R/32)(2R||A||_1) = (R^2/16)||rho-sigma||_1.
Hence the claim with constant R/4.
(c) Weyl inequality.  For self-adjoint compact operators A, B with
eigenvalues mu_1 >= mu_2 >= ... (counting multiplicity, tending to 0),
|mu_k(A) - mu_k(B)| <= ||A - B|| (standard min-max/Weyl).  Applying this to
S_rho, S_sigma gives (a) + (b) and the first inequality of the claim.
(d) Passing from 1/lambda_k to lambda_k uses the bounds in Section 2:
|lambda_k(rho) - lambda_k(sigma)|
  = lambda_k(rho) lambda_k(sigma) |1/lambda_k(sigma) - 1/lambda_k(rho)|
  <= (k^2 pi^2)^2 (R/4) ||rho - sigma||_1^{1/2}.  QED.

Note.  The draft's error was to apply (c) to T_rho itself; T_rho is not
self-adjoint on L^2, so (c) does not apply.  The symmetrized S_rho closes
the gap.  Numeric spot check: verify_hs_bound.py (16/16 Weyl cases, bound
ratios 0.06-0.17).

## 4. Lemma 2 (O1c, repair R3): structure of f

Claim.  For every rho in K, with the conventions of Section 2, f = lambda_1
u_1^2 - lambda_2 u_2^2 has at most two zeros in (0,1), and {f > 0} is a
single interval (x_-, x_+) with 0 <= x_- < z_0 < x_+ <= 1.

Proof.  Wronskian argument (rho-independent re-derivation of AEH Lemma 2.2
(1),(4),(5)).  Let W := u_1 u_2' - u_1' u_2.  From the eigenvalue equations,
  W' = (lambda_1 - lambda_2) rho u_1 u_2,
and W(0) = W(1) = 0 (Dirichlet).  With the sign convention of Section 2,
u_1 u_2 > 0 on (0, z_0) and u_1 u_2 < 0 on (z_0, 1); lambda_1 - lambda_2
< 0; rho > 0.  Hence W' < 0 on (0, z_0) and W' > 0 on (z_0, 1).  Since
W(0) = 0, W < 0 on (0, z_0]; since W(1) = 0 and W' > 0 on (z_0, 1),
W < 0 on [z_0, 1).  Thus W < 0 on (0, 1), and for v := u_2/u_1,
  v' = W/u_1^2 < 0 on (0,1).
So v is strictly decreasing, v(z_0) = 0, v(0+) > 0, v(1-) < 0.
Now f = lambda_1 u_1^2 (1 - (lambda_2/lambda_1) v^2); with c := sqrt(lambda_1/
lambda_2) > 0, f = 0 iff |v| = c.  On (0, z_0), v is positive strictly
decreasing, so v = c has at most one solution x_-; on (z_0, 1), v is
negative strictly decreasing, so v = -c has at most one solution x_+.  Hence
f has at most two zeros in (0,1), and
  {f > 0} = {x in (0,1) : |v(x)| < c} = (x_-, x_+)
(with the convention that an endpoint is 0 or 1 when the corresponding
equation has no solution in (0,1)).  Since f(z_0) = lambda_1 u_1(z_0)^2
> 0, z_0 lies in the interval.  QED.

Numeric check: verify_structure_f.py, 22 hostile configs, all structure
claims pass (including W < 0 and v strictly decreasing).

## 5. Lemma 3 (O1b, repairs R2 + R4): FH derivative at a moving jump

Setup.  Let rho in K be constant on a two-sided neighborhood of x_j in (0,1)
with one-sided values c_- (left) and c_+ (right), c_- != c_+.  (In Lemma 4
below rho is piecewise constant, so this holds.)  For |eps| small, let rho_eps
be rho with the jump moved to x_j + eps (constant on the same neighborhood,
values c_- left of x_j + eps, c_+ right of it).

Claim.  eps |-> lambda_k(rho_eps) is differentiable at 0, and
  d/d eps lambda_k(rho_eps)|_0 = lambda_k (c_+ - c_-) u_k(x_j)^2,
hence
  d/d eps D(rho_eps)|_0 = -(c_+ - c_-) f(x_j).
Equivalently, moving the jump RIGHT by delta changes D by
-(c_+ - c_-) f(x_j) delta + o(delta), and moving it LEFT by delta changes D
by +(c_+ - c_-) f(x_j) delta + o(delta).  In particular, at an interior
extremum of D over a family in which x_j is a free parameter, the one-sided
conditions force (c_+ - c_-) f(x_j) = 0, i.e., f(x_j) = 0.

Proof (repair R4: approximation of the Dirac measure limit).  Let H be a
C^inf function with H(t) = 0 for t <= -1, H(t) = 1 for t >= 1, H' >= 0, and
let H_delta(s) := H(s/delta).  Define the smoothed family
  rho_eps^delta(x) = c_- + (c_+ - c_-) H_delta(x - x_j - eps)
on the transition band |x - x_j - eps| < delta and equal to rho_eps outside
(possible because rho is constant on a neighborhood of x_j).  Then
  rho_eps^delta -> rho_eps in L^1(0,1) uniformly for |eps| <= eps_0 as
delta -> 0, and
  d/d eps rho_eps^delta = -(c_+ - c_-) (1/delta) H'((x - x_j - eps)/delta)
in C_c^inf, in particular in L^1.
(a) For each fixed delta > 0, the family eps |-> rho_eps^delta satisfies the
hypotheses of AEH Lemma 2.1 (V = 0, w = rho_eps^delta bounded below and
above uniformly, dw/d eps in L^1); hence
  d/d eps lambda_k(rho_eps^delta)
    = lambda_k(rho_eps^delta) (c_+ - c_-)
      int (1/delta) H'((x - x_j - eps)/delta) u_k(rho_eps^delta; x)^2 dx.
(b) As delta -> 0, u_k(rho_eps^delta) -> u_k(rho_eps) uniformly in x.
Indeed, rho_eps^delta -> rho_eps in L^1, so by Lemma 1 the eigenvalues
converge; the normalized eigenfunctions are bounded in H^2 uniformly over K
(||u_k||_{L^2} <= 1, ||u_k'||_{L^2}^2 = lambda_k <= (k pi)^2, ||u_k''||_{L^2}
= lambda_k ||rho u_k||_{L^2} <= (k pi)^2 R), so by Arzela-Ascoli a subsequence
converges uniformly; the limit is the (simple, hence unique) normalized
eigenfunction u_k(rho_eps).  Also (1/delta) H'((x - x_j - eps)/delta) is a
Dirac family: it has integral 1 and is supported in |x - x_j - eps| < delta,
so for uniformly convergent bounded u_n,
  int (1/delta) H'((x - x_j - eps)/delta) u_n(x) dx -> u(x_j + eps).
Hence, for every fixed eps,
  d/d eps lambda_k(rho_eps^delta) -> lambda_k(rho_eps)(c_+ - c_-)
    u_k(rho_eps; x_j + eps)^2   (delta -> 0).
The convergence is uniform for |eps| <= eps_0 because the integrands are
uniformly bounded (|d/d eps lambda_k^delta| <= (k pi)^2 (c_+ - c_-)
||u_k^delta||_inf^2 <= C(k, R), independent of delta and eps).
(c) By Lemma 1, lambda_k(rho_eps) = lim_delta lambda_k(rho_eps^delta)
uniformly in eps, so
  lambda_k(rho_eps) - lambda_k(rho_0)
    = lim_delta int_0^eps d/d s lambda_k(rho_s^delta) ds
    = int_0^eps lambda_k(rho_s)(c_+ - c_-) u_k(rho_s; x_j + s)^2 ds
by dominated convergence (step (b)).
(d) Divide by eps and let eps -> 0.  By the continuity of s |-> u_k(rho_s;
x_j + s) (uniform convergence from (b) plus O1a),
  (1/eps)[lambda_k(rho_eps) - lambda_k(rho_0)]
    -> lambda_k(rho_0)(c_+ - c_-) u_k(rho_0; x_j)^2.
This is the two-sided derivative (the argument is symmetric in the sign of
eps).  Subtracting k = 2 and k = 1 gives dD/d eps = -(c_+ - c_-) f(x_j).
(e) Stationarity.  At an interior maximum of D over a cell in which x_j is a
free parameter, the one-sided derivatives of the DISTANCE parametrization
must satisfy: moving right does not increase D: -(c_+ - c_-) f(x_j) <= 0;
moving left does not increase D: +(c_+ - c_-) f(x_j) <= 0.  Both together
force (c_+ - c_-) f(x_j) = 0.  For an interior minimum the two one-sided
derivatives are >= 0, again forcing (c_+ - c_-) f(x_j) = 0.  Since c_+ !=
c_-, f(x_j) = 0.  QED.

Note on the sign.  The draft had +(c_+ - c_-) f(x_j) for the rightward
derivative; the correct sign is negative (verify_fh_sign.py V1/V2, and the
independently verified identity dD/du = -2(R-1) f(u) for the symmetric
barrier family).  The audit's parenthetical "the two-sided derivative exists
only if f(x_j) = 0" is recorded as imprecise: the two-sided derivative of
eps |-> D(rho_eps) exists at every x_j (part (d)); the rightward and leftward
DISTANCE derivatives have opposite signs unless f(x_j) = 0.

## 6. Lemma 4 (O1d): N-jump compactness and at most two effective jumps

Setup.  K_N := { rho in K : rho piecewise constant with at most N jumps }.
K_N is the image of the compact set Omega_N = {0 <= x_1 <= ... <= x_N <= 1}
x [1, R]^{N+1} under the continuous map (x, c) |-> rho (into L^1), so by
Lemma 1 the extrema of D over K_N are attained.

Claim.  Any extremizer rho^N of D over K_N (max or min) admits a minimal
representation with at most two EFFECTIVE jumps, where an effective jump is
an interior point x in (0,1) at which the one-sided limits of rho^N differ.

Proof.  Let k be the number of effective jumps of rho^N (k <= N; jumps at
the boundary 0 or 1 have zero measure effect on the operator and are
absorbed).  If k <= 2 there is nothing to prove.  Otherwise let the effective
jumps be 0 < x_1 < ... < x_k < 1 with adjacent distinct values.  Each x_j is
a free interior parameter: for small |delta_j| the config with the same
value sequence and jump positions x_j + delta_j (kept ordered) still lies in
K_N, with the same combinatorial cell.  The restricted map D_cell(delta_1,
..., delta_k) attains a local extremum at 0, and by Lemma 3 the partial
derivatives vanish:
  d/d delta_j D_cell|_0 = -(c_j - c_{j-1}) f(rho^N)(x_j) = 0,
where c_{j-1}, c_j are the values left and right of x_j.  Since c_{j-1} !=
c_j (effective), f(rho^N)(x_j) = 0 for j = 1, ..., k.  By Lemma 2, f(rho^N)
has at most two zeros in (0,1), so k <= 2.  QED.

## 7. Lemma 5 (O1e): step functions are dense

Claim.  sup over step functions in K equals sup_K D; with M_N := max_{K_N} D
(exists by Lemma 4), M_N is nondecreasing and M_N -> sup_K D.  Mirror:
m_N := min_{K_N} D is nonincreasing and m_N -> inf_K D.

Proof.  For rho in K, let rho_m be the block average of rho on the uniform
partition of [0,1] into 2^m intervals.  Then 1 <= rho_m <= R, rho_m is
piecewise constant with at most 2^m - 1 jumps, and rho_m -> rho in L^1
(standard Lebesgue averaging).  By Lemma 1, D(rho_m) -> D(rho).  Hence the
sup over step functions in K equals sup_K D, and the monotone sequence
M_N = max_{K_N} D satisfies M_N -> sup_K D.  The inf statement is identical.
QED.

## 8. Lemma 6 (O1f): bang-bang structure at a global extremizer

Claim.  Let rho~ be a global maximizer of D over K (which exists by Lemmas 4
and 5 and compactness of K_2, see the synthesis below).  Then rho~ = R a.e.
on {f~ > 0} and rho~ = 1 a.e. on {f~ < 0}, where f~ = f(rho~).  A global
minimizer satisfies the reversed assignment.  Hence, by Lemma 2, a global
maximizer is a.e. a barrier config and a global minimizer is a.e. a well
config.

Proof.  Let J be an interval with closure inside {f~ > 0} on which rho~ is
bounded away from R: rho~ <= R - eta on J (such J exists if {f~ > 0} cap
{rho~ < R} has positive measure, because rho~ is piecewise constant and f~
is continuous, so the intersection contains an interval).  For 0 <= kappa <=
eta, w(kappa) := rho~ + kappa chi_J lies in K.  AEH Lemma 2.1 (V = 0, w =
w(kappa), dw/dkappa = chi_J in L^1) gives
  d/d kappa D(w(kappa))|_0 = int_0^1 chi_J f~ dx = int_J f~ dx > 0,
contradicting maximality (D(rho~) is the maximum, so the right derivative in
any admissible direction is <= 0).  Hence rho~ = R a.e. on {f~ > 0}.
Similarly, if {f~ < 0} cap {rho~ > 1} had positive measure, taking
J subset of it with rho~ >= 1 + eta on J and w(kappa) := rho~ - kappa chi_J
would give d/d kappa D|_0 = -int_J f~ dx > 0, again contradicting maximality;
so rho~ = 1 a.e. on {f~ < 0}.  The minimizer case is the mirror argument
(right derivatives >= 0 at a minimum).  Measure-zero changes of rho do not
change the operator, so "a.e." is the correct level of precision.  QED.

## 9. Synthesis

SUP.  By Lemma 5, sup_K D = lim_N M_N.  By Lemma 4, each M_N = D(rho^N)
with rho^N in K_2, so M_N <= sup_{K_2} D for every N, hence
sup_K D <= sup_{K_2} D; the reverse inequality is trivial, so sup_K D =
sup_{K_2} D.  K_2 is compact (continuous image of Omega_2) and D is
continuous (Lemma 1), so the sup is attained at some rho~ in K_2, which is
then a global maximizer over K.  By Lemma 6 and Lemma 2, rho~ = rho^{bar}_{a,
b} a.e. for (a, b) = (x_-, x_+) (the single interval {f~ > 0}, allowing
degenerate endpoints), so
  sup_K D = D(rho~) = max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),
the maximum being attained by compactness of [0,1]^2 and continuity of
(a,b) |-> D(rho^{bar}_{a,b}) (Lemma 1).  This is (i).

INF.  Identical with max/min exchanged; Lemma 6 gives rho~' = 1 a.e. on
{f~' > 0} and R a.e. on {f~' < 0}, and Lemma 2 makes rho~' a.e. a well
config; min_{K_2} D = inf_K D by the mirror of Lemmas 4-5.  This is (ii).

Attainment over the two-parameter families and the boundary cases
(a = 0, b = 1, a = b, constants) are covered in Sections 1 and 9.  QED.

## 10. Premise ledger (each cited result rechecked in this run)

- AEH arXiv:2407.02459v2 Lemma 2.1 (FH formula): verified verbatim against
  papers/fundamental_gap.txt; hypotheses met for L^1 pointwise perturbations;
  for moving jumps used via the smoothing argument (Lemma 3).
- AEH Lemma 2.2 (structure of u_2/u_1 and f): verified verbatim; Lemma 2 is
  a rho-independent re-derivation with a global W < 0 argument.
- Weyl/min-max inequality for self-adjoint compact operators: standard;
  applied to S_rho (not to the non-self-adjoint T_rho).
- Sturm oscillation (u_k has k-1 simple interior zeros): classical, verified
  numerically.
- Keller 1976 / Mahar-Willner 1976: context only (ratio problems in the
  bounded-jump class); NOT premises of O1.  The box class requires the
  N-jump approximation ladder (Lemmas 4-5).
- Eigenvalue comparison bounds (Section 2): Rayleigh quotient derivation,
  verified numerically (verify_hs_bound.py H3).

## 11. Remaining gaps and status

No open obligation remains in O1a-O1f.  The status of this document is
CANDIDATE_COMPLETE_PROOF: the proof is self-audited (audit_report.md) but the
upstream skill revision policy requires an independent verifier pass from the
changed points (Lemma 1 and Lemma 3) before the manager can close obligation
O1.  Out of scope: O2/O3 (symmetric 1-parameter and 2-parameter symmetry),
owned by the draft run.

