# O1 Reduction theorem (draft proof, coordinator)

THEOREM (reduction to 2-parameter families).  Let R > 1 and let
K = { rho measurable on [0,1] : 1 <= rho <= R a.e. }.  For the Dirichlet
string -y'' = lambda rho y on [0,1] with eigenvalues 0 < lambda_1 < lambda_2
and D(rho) := lambda_2 - lambda_1:

(i)  sup_{rho in K} D(rho)  =  max_{0<=a<=b<=1} D( rho = R on (a,b), 1 elsewhere ),
(ii) inf_{rho in K} D(rho)  =  min_{0<=a<=b<=1} D( rho = 1 on (a,b), R elsewhere ),

and both extrema over the two-parameter families are attained.

## Lemma 1 (continuity).  rho |-> (lambda_1, lambda_2) is continuous in the
L^1 topology on K.

Proof.  Let G(x,t) = min(x,t)(1-max(x,t)) be the Dirichlet Green function of
-d^2/dx^2 on [0,1], and T_rho f = int_0^1 G(x,t) rho(t) f(t) dt.  Then
lambda_k(rho)^{-1} = mu_k(T_rho), the k-th eigenvalue of the self-adjoint
compact operator T_rho on L^2.  For rho, sigma in K,
  |T_rho f|(x) <= |G(x,.)|_inf ||(rho-sigma) f||_1 <= ||rho-sigma||_2 ||f||_2
with ||rho-sigma||_2^2 <= ||rho-sigma||_inf ||rho-sigma||_1 <= 2R ||rho-sigma||_1,
so ||T_rho - T_sigma|| -> 0 as ||rho-sigma||_1 -> 0.  By the min-max principle
for self-adjoint compact operators, |mu_k(T_rho) - mu_k(T_sigma)| <=
||T_rho - T_sigma||, hence lambda_k is continuous.  QED.

## Lemma 2 (structure of f).  For ANY rho in K, with u_1,u_2 the
L^2(rho)-normalized first two eigenfunctions:
  f := lambda_1 u_1^2 - lambda_2 u_2^2
has at most two zeros in (0,1) and {f > 0} is a single interval containing
the unique zero z_0 of u_2.

Proof.  W := u_1 u_2' - u_1' u_2 satisfies W' = (lambda_1 - lambda_2) rho u_1 u_2,
W(0) = W(1) = 0.  With u_1 > 0, u_2 > 0 on (0,z_0), u_2 < 0 on (z_0,1):
W' < 0 on (0,z_0) and W' > 0 on (z_0,1); W(0)=W(1)=0 forces W < 0 on (0,1).
Hence v := u_2/u_1 satisfies v' = W/u_1^2 < 0 on (0,1): v is strictly
decreasing, v(z_0) = 0.  Now f = 0 iff v^2 = lambda_1/lambda_2; since v is
strictly decreasing with v(0+) > 0 > v(1-), the equation v = +c (c>0) has at
most one solution in (0,z_0) and v = -c at most one in (z_0,1).  So f has at
most two zeros; {f>0} = {|v| < c} is a single interval, and it contains z_0
since f(z_0) = lambda_1 u_1(z_0)^2 > 0.  QED.

(Remark: this is AEH arXiv:2407.02459v2 Lemma 2.2 re-derived; the
monotonicity of v is rho-independent.)

## Lemma 3 (FH derivative at a moving jump).  Let rho have a jump at x_j in
(0,1) from value c_- to c_+ (c_- != c_+), and let rho_eps be rho with the
jump moved to x_j + eps.  Then
  d/d eps D(rho_eps)|_{0} = (c_+ - c_-) f(x_j).

Proof.  rho_eps = rho + (c_+ - c_-) chi_{(x_j, x_j+eps)} (up to the sign of
eps), an L^1 perturbation; by Lemma 1 applied to the family and the
Feynman-Hellmann formula (AEH Lemma 2.1), d lambda_k/d eps = -lambda_k
int d(rho)/d eps u_k^2 dx -> -lambda_k (c_+ - c_-) u_k(x_j)^2; subtracting
gives the claim.  QED.

## Lemma 4 (N-jump maximizers have at most two jumps).
Let K_N = { piecewise constant rho in K with at most N jumps }.  For each N
the map rho |-> D(rho) attains its maximum (resp. minimum) on K_N, and any
attaining rho^N has at most two effective jumps.

Proof.  K_N is the continuous image of the compact set
{ (x_1,...,x_N, c_0,...,c_N) : 0<=x_1<=...<=x_N<=1, 1<=c_i<=R }, so the
maximum/minimum is attained (Lemma 1).  If the parameter point lies on the
boundary of the simplex (coalesced jumps), view the config in the smaller
family; iterate until the parameter point is interior for the family with
k = number of effective jumps.  At each effective jump x_j (values c_{j-1},
c_j, c_{j-1} != c_j), x_j is an interior free parameter, so by Lemma 3 and
maximality/minimality, (c_j - c_{j-1}) f_N(x_j) = 0, hence f_N(x_j) = 0.
By Lemma 2, f_N has at most two zeros, so k <= 2.  QED.

## Lemma 5 (step functions are dense).  sup_K D = sup over step functions in K.

Proof.  Every rho in K is the L^1 limit of its block averages on fine
partitions (which lie in [1,R]); Lemma 1 gives convergence of D.  QED.

## Proof of the theorem.

SUP.  Let M_N = max_{K_N} D (exists by Lemma 4).  By Lemma 5, M_N is
nondecreasing and M_N -> sup_K D.  By Lemma 4, rho^N in K_2, so
M_N <= sup_{K_2} D for every N; hence sup_K D <= sup_{K_2} D.  The reverse
inequality is trivial (K_2 subset K).  So sup_K D = sup_{K_2} D.
K_2 = continuous image of {0<=a<=b<=1} x [1,R]^3, compact, so the sup is
attained at some rho~ with D(rho~) = sup_K D: rho~ is a global maximizer
over K.  At a global maximizer the one-sided FH derivative must be <= 0 in
every admissible direction; if f~ > 0 on a set of positive measure where
rho~ < R, increasing rho~ there would strictly increase D, contradiction;
so rho~ = R a.e. on {f~>0} and rho~ = 1 a.e. on {f~<0} (bang-bang).  By
Lemma 2, {f~>0} = (x_-, x_+) is a single interval, so rho~ = R on (x_-,x_+)
and 1 elsewhere: rho~ lies in the barrier family, and
sup_K D = max over the barrier family.  QED.

INF.  Identical with max replaced by min; the one-sided derivative condition
at a global minimizer gives rho~ = 1 on {f~>0} and R on {f~<0}, and Lemma 2
makes rho~ a single-well config.  QED.

## Status
PROVED (draft).  All steps are elementary; the only citations are the
min-max continuity of eigenvalues of self-adjoint compact operators, the
FH formula, and Lemma 2 (Wronskian argument), each re-derived above.
PENDING: independent audit by a verifier role; then formal write-up in
docs/SL_gap_n1_proof.tex or the research summary.

## Consequences
- The SUP problem reduces to the 2-parameter barrier family and the INF
  problem to the 2-parameter well family.
- Any maximizer/minimizer is bang-bang and has the single-interval sign
  structure, so its two jumps (if interior) are zeros of f.
- Remaining obligations: O2 (symmetric 1-parameter single crossing) and
  O3 (the 2-parameter extremum is attained at the symmetric point).
