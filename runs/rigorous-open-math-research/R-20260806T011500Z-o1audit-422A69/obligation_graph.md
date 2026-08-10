# Obligation graph - audit verdicts (O1a-O1f)

This file is the audit verdict graph for the O1 reduction theorem of run
R-20260805T000000Z-gapn1-a1b2c3.  Verdicts are those of this independent audit
run (R-20260806T011500Z-o1audit-422A69).  Each obligation carries the exact
reason and the smallest failing claim.  The draft itself was NOT modified.

Root: THEOREM (O1): sup_K D = max over barrier family B; inf_K D = min over
well family W; both attained over the 2-parameter families.
(R = upper density bound > 1; K = {1 <= rho <= R a.e. measurable}; D = lambda_2 - lambda_1.)

## O1a  lambda_k continuous in L^1 on K.
Verdict: PARTIAL (statement TRUE; draft proof NOT acceptable as written).
Reason: The draft (Lemma 1) claims lambda_k(rho)^{-1} = mu_k(T_rho) with
T_rho f = int G(x,t) rho(t) f(t) dt "the k-th eigenvalue of the self-adjoint
compact operator T_rho on L^2", and then applies min-max (Weyl) as
|mu_k(T_rho) - mu_k(T_sigma)| <= ||T_rho - T_sigma||.
Defect: T_rho is NOT self-adjoint on L^2(0,1) (kernel G(x,t)rho(t) is not
symmetric in (x,t)); Weyl's inequality does not apply to it.  The claim is
repaired by using the similar symmetric Hilbert-Schmidt operator
S_rho = rho^{1/2} T_rho rho^{1/2} on L^2 with kernel
K_rho(x,t) = sqrt(rho(x)) G(x,t) sqrt(rho(t)): eigenvalues coincide
(mu_k(T_rho) = mu_k(S_rho)), and
||S_rho - S_sigma||_HS -> 0 as ||rho - sigma||_1 -> 0
(|K_rho - K_sigma| <= G(x,t)(sqrt(rho(x)) sqrt(|rho-sigma|(t)) + sqrt(sigma(t)) sqrt(|rho-sigma|(x))),
then |mu_k(S_rho) - mu_k(S_sigma)| <= ||S_rho - S_sigma|| by Weyl).  An
equivalent alternative is working on the weighted space L^2(rho).  The numeric
spot check (moving a jump by eps = 1e-3..1e-5) shows dlambda = O(eps),
consistent with L^1 continuity.  Evidence: verify_o1_audit_out.json
(L1_continuity_check).
Status in draft obligation graph: OPEN ("standard; cite").  Audit decision:
the draft does NOT provide an acceptable proof as written; it needs the
operator correction above or an exact citation.  Statement is standard and true.

## O1b  FH derivative wrt moving a jump point equals (c_{j+1}-c_j) f(x_j).
Verdict: FAILED (as stated; sign error).  The zero-condition conclusion used
downstream survives.
Reason: Moving the jump at x_j (values c_- left, c_+ right) RIGHT by eps
gives rho_eps = rho - (c_+ - c_-) chi_{(x_j, x_j+eps)}, i.e. distributionally
partial rho / partial eps = -(c_+ - c_-) delta_{x_j}.  AEH Lemma 2.1 (V=0)
gives dlambda_k/deps = +lambda_k (c_+ - c_-) u_k(x_j)^2, hence
    dD/deps = -(c_+ - c_-) f(x_j)   (moving right),
    dD/deps = +(c_+ - c_-) f(x_j)   (moving left),
so the two-sided derivative exists only when f(x_j) = 0.  The draft formula
dD/deps = +(c_+ - c_-) f(x_j) is the LEFT-moving derivative, not the stated
RIGHT-moving one; the draft's own verified identity dD/du = -2(R-1) f(u) for
the symmetric barrier family (R-003 ledger; reproduced here to ~1e-7 at
u in {0.2,0.3,0.4,0.49} and ~1e-8 at u*) is inconsistent with the draft
Lemma 3 sign and consistent with the corrected formula.
Consequence: in Lemma 4 the stationarity condition at an interior effective
jump is -(c_j - c_{j-1}) f_N(x_j) = 0 (max: both one-sided derivatives <= 0)
and +(c_j - c_{j-1}) f_N(x_j) = 0 for the left side; either way f_N(x_j) = 0
with the same conclusion.  So O1b as stated FAILS but the only use of O1b
(zeros of f at extremal effective jumps) is valid.
Evidence: verify_o1_audit_out.json (O1b_jump0, O1b_jump1, O1b_symmetric_family);
direct one-sided differences match the corrected prediction to ~1e-4..1e-7 and
fail the draft sign.

## O1c  f = lambda_1 u_1^2 - lambda_2 u_2^2 has at most 2 zeros and
       {f > 0} is a single interval containing the unique zero z_0 of u_2.
Verdict: PROVED.
Reason: Wronskian argument in the draft (Lemma 2) is correct and class-free:
W = u_1 u_2' - u_2 u_1', W' = (lambda_1 - lambda_2) rho u_1 u_2, W(0) = W(1) = 0;
with u_1 > 0 on (0,1), u_2 > 0 on (0,z_0), u_2 < 0 on (z_0,1) (sign convention
as in AEH), W' < 0 on (0,z_0) and W' > 0 on (z_0,1) force W < 0 on (0,1),
hence v = u_2/u_1 is strictly decreasing, v(z_0) = 0, v(0+) > 0 > v(1-).
f = u_1^2 (lambda_1 - lambda_2 v^2) vanishes iff |v| = sqrt(lambda_1/lambda_2),
at most once in (0,z_0) and at most once in (z_0,1); {f > 0} = {|v| < c} is a
single interval containing z_0 (f(z_0) = lambda_1 u_1(z_0)^2 > 0).  This
matches AEH Lemma 2.2 items (1),(4),(5) exactly (the draft's rho-independence
remark is correct: the Wronskian computation holds for any positive bounded
measurable rho).  Numeric: 10 random 3-block configs + 4 random 5-block
configs at R = 4 all satisfy nzeros_u2 = 1, nzeros_f <= 2, one positive
interval containing z_0, W < 0, v strictly decreasing.
Evidence: verify_o1_audit_out.json (O1c_structure), verify_o1_audit2_out.json
(O1c_5block).
Notes: the draft should state the sign convention on u_2 explicitly (AEH does);
u_1, u_2 are C^1 (rho in L^infty) so point evaluation is legitimate.

## O1d  Compactness of the N-jump family; existence of rho^N extremizer.
Verdict: PROVED (given O1a).
Reason: K_N (piecewise constant, at most N jumps, values in [1,R]) is the
continuous image in L^1 of the compact parameter set
{(x_1,...,x_N,c_0,...,c_N) : 0 <= x_1 <= ... <= x_N <= 1, 1 <= c_i <= R}
(the map is continuous in L^1 including coalescing jumps and equal adjacent
values); D is continuous on K_N by O1a; extrema are attained.  The minimal
representation with k effective jumps has 0 < x_1 < ... < x_k < 1 and pairwise
distinct adjacent values, so each effective jump is an interior free parameter
and the one-sided FH stationarity (O1b corrected) applies.  At each effective
jump f_N(x_j) = 0; by O1c, f_N has at most two zeros, so k <= 2.
Evidence: structural; boundary cases checked numerically (rho=1, rho=R,
2-block, a=b all in the closed families).

## O1e  M_N -> sup_K D (step functions are dense + continuity).
Verdict: PROVED (given O1a).
Reason: block averages on fine partitions of any rho in K lie in [1,R] and
converge to rho in L^1 (standard Lebesgue-averaging theorem); by O1a,
D(block) -> D(rho); hence sup over step functions equals sup_K D; since
M_N = max over K_N is nondecreasing and the step functions form the union of
the K_N, sup_K D = sup_N M_N = lim_N M_N.  Same argument for inf.
Evidence: structural.

## O1f  Bang-bang at a global extremizer.
Verdict: PROVED.
Reason: pointwise FH: for an admissible perturbation delta rho in L^1,
dD/dt = int delta rho f dx (from AEH Lemma 2.1 with V = 0; sign checked
independently).  At a global maximizer rho~, every admissible one-sided
perturbation must satisfy dD/dt <= 0; if f~ > 0 on a positive-measure set with
rho~ < R there, raising rho on a small open subset strictly increases D
(contradiction), so rho~ = R a.e. on {f~ > 0}; similarly rho~ = 1 a.e. on
{f~ < 0}.  At a global minimizer, rho~ = 1 on {f~ > 0}, R on {f~ < 0}.
Combined with O1c ({f~ > 0} a single interval) the maximizer is a barrier
config and the minimizer a well config.  The argument handles densities with
interior values on intervals (finitely many values for the K_2 extremizer;
continuity of f makes the perturbing set open).  Measure-zero changes of rho
do not affect eigenvalues (the operator and quadratic form only depend on the
L^1 class).
Evidence: verify_o1_audit3_out.json (raising rho on {f>0} increases D,
raising on {f<0} decreases D).

## Overall O1 theorem
Verdict: the theorem statement is TRUE, and every obligation is PROVED except
O1a (PARTIAL; standard repair given) and O1b (FAILED as stated; sign error,
consequence valid).  The draft is NOT acceptable as a final proof in its
current form: it requires (i) the O1a operator correction and (ii) the O1b
sign correction.  Both are local, repairable defects; neither is fatal.
Overall audit verdict: REPAIRABLE_GAP (draft), with the theorem itself
holding after the two stated repairs.  Per the packet instruction, the draft
was NOT repaired by this run.

## Boundary and degenerate cases
- a = 0 or b = 1: 2-block configs are inside the closed barrier/well families;
  covered by the compact parameterization; numerically D(2-block) < SUP and
  > INF.
- a = b and constant densities: rho = 1 gives D = 3 pi^2, rho = R gives
  D = 3 pi^2 / R; both inside the closed families (empty barrier / full
  barrier).  Numerically verified to 1e-8.
- Densities taking interior values on intervals: handled by the bang-bang
  argument (O1f) and the finite-value structure of the K_2 extremizer.
- Measure-zero changes: no effect on eigenvalues (L^1 equivalence class).
- Unbounded number of jumps: class K is not a bounded-jump class; the N-jump
  approximation (O1d/O1e) is what extends the argument beyond the
  Keller/MW bounded-jump framework.

## Dependencies
THEOREM(O1) = O1a + O1b(corrected) + O1c + O1d + O1e + O1f.
O1d depends on O1a, O1b, O1c.  O1e depends on O1a.  O1f depends on O1c and
AEH Lemma 2.1.  O2/O3 are OUT OF SCOPE for this audit (packet: audit only the
reduction).
