# Audit report - O1 reduction theorem revision (run R-20260806T140000Z-o1revise-2ED02A)

Status label of the audited artifact: CANDIDATE_COMPLETE_PROOF (self-audited;
independent re-audit of the changed points remains the closing step, per the
upstream skill's revision policy).  All files ASCII punctuation, UTF-8.

## 0. Scope, provenance, and method

Audited artifact: candidate_proof.md in this run (REVISED O1 proof with the
repair list R1-R4 integrated; 310 lines; theorem statement (i)-(ii) unchanged
from the draft).  Obligations audited: O1a-O1f as defined in the draft run's
obligation_graph.md and re-normalized in this run's problem_contract.md.

Provenance chain (sha256 values in repro_manifest.md):
- task packet agenda/task-packets/Q-20260806-o1-revise-2ED02A.md;
- O1 draft runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md;
- O1 audit verdicts runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md;
- repair list R1-R4 runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/candidate_proof.md;
- premise sources: AEH arXiv:2407.02459v2 (papers/fundamental_gap.txt, sha256
  2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14), Keller
  1976 (papers/keller1976.txt), Mahar-Willner 1976 (papers/mw1976.txt).

Method: the auditor independently re-derived every step of the revised proof
(no step accepted on the authority of the draft, the audit run, or the repair
list), rechecked every premise against its primary source, and cross-checked
the numerical battery in reproducibility/.  Numeric checks are evidence only;
every proof-level claim is argued analytically below.  The four repairs R1-R4
were re-derived, not copied: R1 (S_rho presentation), R2 (moving-jump sign),
R3 (u_2 sign convention), R4 (smoothing approximation).

Result: every obligation O1a-O1f closes after the audit.  One localized
arithmetic slip in Lemma 1 (b) was found during this audit and repaired in the
delivered text (finding F-001); two non-substantive imprecisions are recorded
(F-002, F-003).  No fatal gap was found.  The audited artifact is returned as
CANDIDATE_COMPLETE_PROOF: a reviser cannot self-certify closure, so an
independent verifier pass on Lemma 1 and Lemma 3 is required before the
manager closes obligation O1 (see Section 5).

## 1. Verdict taxonomy and summary table

- PASS: the obligation is closed by the delivered text (with any audit
  correction applied and documented).
- REPAIRABLE_GAP: the conclusion is correct and verified, but the written
  argument had a localized defect that the audit specifies and repairs.
- PARTIAL: a meaningful sub-claim is proved; a required sub-claim is not.
- FAILED: the claim is false or the argument is irreparably invalid.
- NOT_VERIFIABLE: no source or reproducible computation could establish it.

| Obligation | Verdict | Basis |
|---|---|---|
| O1a (L^1 continuity, Lemma 1) | PASS (repair F-001 applied) | Section 2.1 |
| O1b (moving-jump FH, Lemma 3) | PASS | Section 2.2 |
| O1c (structure of f, Lemma 2) | PASS | Section 2.3 |
| O1d (compactness, <= 2 effective jumps, Lemma 4) | PASS | Section 2.4 |
| O1e (step functions dense, Lemma 5) | PASS | Section 2.5 |
| O1f (bang-bang at extremizers, Lemma 6) | PASS | Section 2.6 |
| Synthesis (SUP/INF, attainment) | PASS | Section 2.7 |
| Theorem statement and edge cases | PASS | Section 2.8 |

F-001 is classified REPAIRABLE (single arithmetic line, conclusion
unaffected, correction applied to the delivered text).  The overall verdict is
not downgraded to REPAIRABLE_GAP because the delivered text is the corrected
text and the audit records the defect and its fix explicitly.

## 2. Detailed audit findings per obligation

### 2.1 O1a - L^1 continuity of lambda_k on K (Lemma 1)

Claim re-derived: for every k >= 1 and rho, sigma in K,
  |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
  <= (R/4) ||rho - sigma||_1^{1/2},
hence |lambda_k(rho) - lambda_k(sigma)| <= (R/4)(k^2 pi^2)^2 ||rho-sigma||_1^{1/2}.

(a) Operator presentation (repair R1).  The packet/audit formula
"rho^{1/2} T_rho rho^{1/2}" is NOT symmetric as written when
T_rho = T_0 M_rho (multiplication on the right), so it cannot be the
Hilbert-Schmidt operator for Weyl.  The delivered text uses the kernel form
S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)}, i.e. the integral operator with
symmetric kernel sqrt(rho(x)) G(x,t) sqrt(rho(t)).  Checked:
  M_{sqrt(rho)} T_rho M_{sqrt(rho)}^{-1}
    = M_{sqrt(rho)} (T_0 M_rho) M_{sqrt(rho)}^{-1}
    = M_{sqrt(rho)} T_0 M_{sqrt(rho)} M_{sqrt(rho)} M_{sqrt(rho)}^{-1}
    = M_{sqrt(rho)} T_0 M_{sqrt(rho)} = S_rho.
Since 1 <= sqrt(rho) <= sqrt(R), M_{sqrt(rho)} is bounded with bounded inverse
M_{1/sqrt(rho)}; S_rho and T_rho are similar, so their spectra coincide.
S_rho is self-adjoint positive Hilbert-Schmidt: the kernel is bounded by R/4
(sqrt(rho) sqrt(rho') G <= R/4) and symmetric; positivity follows from
S_rho = T_0^{1/2} M_{sqrt(rho)} (T_0^{1/2} M_{sqrt(rho)})^* with T_0 >= 0
(alternatively from the quadratic form int int sqrt(rho(x))G(x,t)sqrt(rho(t))
phi(x) phi(t) dx dt = ||T_0^{1/2} M_{sqrt(rho)} phi||^2 >= 0).

(b) Eigenvalue identity.  The eigenvalue problem -y'' = lambda rho y with
Dirichlet BCs is equivalent to T_0(rho y) = y/lambda, i.e. T_rho y = y/lambda
(T_0 is the inverse of -d^2/dx^2).  Then
  S_rho (sqrt(rho) y) = M_{sqrt(rho)} T_0 (rho y) = (1/lambda) sqrt(rho) y.
So mu_k(S_rho) = 1/lambda_k(rho) for the k-th eigenvalue.  Checked.

(c) Hilbert-Schmidt bound.  With A = |rho - sigma| and
Delta(x,t) = sqrt(rho(x))sqrt(rho(t)) - sqrt(sigma(x))sqrt(sigma(t)):
  |Delta| <= sqrt(rho(t)) |sqrt(rho(x)) - sqrt(sigma(x))|
           + sqrt(sigma(x)) |sqrt(rho(t)) - sqrt(sigma(t))|
  <= (sqrt(R)/2) (A(x) + A(t)),
using |sqrt(u) - sqrt(v)| = |u - v|/(sqrt(u) + sqrt(v)) <= |u - v|/2 for
u, v >= 1.  With G <= 1/4 and the symmetry of G in (x, t):
  ||S_rho - S_sigma||_HS^2 = int int G(x,t)^2 Delta(x,t)^2 dx dt
  <= (R/4) int int G^2 (A(x) + A(t))^2 dx dt
  = (R/2) [ int int G^2 A(x)^2 dx dt + int int G^2 A(x) A(t) dx dt ]
  <= (R/32) ( ||A||_2^2 + ||A||_1^2 ),
because int int G^2 A(x)^2 dx dt <= (1/16)||A||_2^2 (integrate t first,
G^2 <= 1/16) and int int G^2 A(x) A(t) dx dt <= (1/16)||A||_1^2.
Since |A| <= R - 1 a.e., ||A||_2^2 <= ||A||_inf ||A||_1 <= (R-1)||A||_1
<= R||A||_1 and ||A||_1^2 <= (R-1)||A||_1 <= R||A||_1.  Hence
  ||S_rho - S_sigma||_HS^2 <= (R/32)(2R||A||_1) = (R^2/16)||rho - sigma||_1,
so ||S_rho - S_sigma||_HS <= (R/4)||rho - sigma||_1^{1/2}.  Checked.

(d) Weyl inequality.  For self-adjoint compact A, B with eigenvalues
mu_1 >= mu_2 >= ... (repeated with multiplicity, tending to 0),
|mu_k(A) - mu_k(B)| <= ||A - B||; and ||A - B|| <= ||A - B||_HS always.
Applied to S_rho, S_sigma (self-adjoint HS), NOT to T_rho (the draft's error;
T_rho is not self-adjoint on L^2).  Chain:
  |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||
  <= ||S_rho - S_sigma||_HS <= (R/4)||rho - sigma||_1^{1/2}.  Checked.

(e) Conversion to lambda_k.  |lambda_k(rho) - lambda_k(sigma)|
  = lambda_k(rho) lambda_k(sigma) |1/lambda_k(sigma) - 1/lambda_k(rho)|
  <= (k^2 pi^2)^2 (R/4) ||rho - sigma||_1^{1/2},
using the comparison bounds k^2 pi^2 / R <= lambda_k <= k^2 pi^2
(Rayleigh quotient, P4; re-derived in Section 3.1).  Checked.

Numeric evidence: verify_hs_bound.py (recorded out.json) - HS-bound ratios
0.06-0.17 on 8 random pairs in K; Weyl inequality |1/lambda_k(rho)
- 1/lambda_k(sigma)| <= ||S-S||_HS on 16/16 cases; comparison bounds hold;
discretized symmetric-kernel eigenvalues match 1/lambda_k to O(1/N);
eigenfunctions are O(eps)-Lipschitz under jump motion.  Evidence only.

Edge cases: rho = sigma trivial; R -> 1+ : K shrinks to {1} and the bound
degrades continuously (no discontinuity).  Fine.

Finding F-001 (REPAIRABLE, applied): the pre-correction text of Lemma 1 (b)
contained the line
  ||S_rho - S_sigma||_HS^2 <= (R/16)||rho - sigma||_2^2,
which is NOT derivable from |Delta| <= (sqrt(R)/2)(A(x) + A(t)): squaring
gives (R/4)(A_x + A_t)^2, and after integrating against G^2 <= 1/16 the
correct coefficient is (R/32) on (||A||_2^2 + ||A||_1^2), not (R/16) on
||A||_2^2.  The final bound (R/4)||A||_1^{1/2} is unaffected (route above).
The delivered text (candidate_proof.md Section 3 (b)) now carries the
corrected derivation; this audit quotes both versions for the record.

### 2.2 O1b - FH derivative at a moving jump (Lemma 3, repairs R2 + R4)

Claim re-derived: for rho constant on a two-sided neighborhood of x_j with
one-sided values c_-, c_+, c_- != c_+, and rho_eps the config with the jump
at x_j + eps,
  d/d eps lambda_k(rho_eps)|_0 = lambda_k (c_+ - c_-) u_k(x_j)^2,
  d/d eps D(rho_eps)|_0 = -(c_+ - c_-) f(x_j),
f = lambda_1 u_1^2 - lambda_2 u_2^2.  Equivalently: moving the jump right by
delta changes D by -(c_+ - c_-) f(x_j) delta + o(delta); moving left by
+(c_+ - c_-) f(x_j) delta + o(delta).

(a) Sign re-derivation (repair R2).  Let H be C^inf with H(t) = 0 for t <= -1,
H(t) = 1 for t >= 1, H' >= 0, H_delta(s) = H(s/delta), and
  rho_eps^delta(x) = c_- + (c_+ - c_-) H_delta(x - x_j - eps)
on the transition band, equal to rho_eps outside.  Then
  d/d eps rho_eps^delta = -(c_+ - c_-) (1/delta) H'((x - x_j - eps)/delta),
which lies in C_c^inf, hence in L^1.  AEH Lemma 2.1 (V = 0, w = rho_eps^delta,
C = R, dw/d eps in L^1; hypotheses verified against the primary source in
Section 3.1) gives
  d/d eps lambda_k(rho_eps^delta)
    = -lambda_k int (d/d eps rho_eps^delta) (u_k^delta)^2 dx
    = lambda_k (c_+ - c_-) int (1/delta) H'((x - x_j - eps)/delta) (u_k^delta)^2 dx.
So the SIGN is positive for lambda_k with factor (c_+ - c_-) - the draft's
sign for D was wrong because D = lambda_2 - lambda_1 introduces the minus:
dD/d eps = (c_+ - c_-)(lambda_2 u_2^2 - lambda_1 u_1^2) = -(c_+ - c_-) f(x_j).

(b) Limit interchanges (repair R4).  Three ingredients, all verified:
  (i) rho_eps^delta -> rho_eps in L^1 uniformly for |eps| <= eps_0, so by
Lemma 1 the eigenvalues converge uniformly in eps.
  (ii) u_k(rho_eps^delta) -> u_k(rho_eps) uniformly in x (and in eps).  The
eigenfunctions are uniformly bounded in H^2 over K: with int rho u_k^2 = 1 and
rho >= 1, ||u_k||_2 <= 1; ||u_k'||_2^2 = lambda_k <= (k pi)^2; and
-u_k'' = lambda_k rho u_k gives ||u_k''||_2 = lambda_k ||rho u_k||_2
<= (k pi)^2 R.  Arzela-Ascoli gives a uniformly convergent subsequence; any
limit is a normalized eigenfunction of rho_eps with eigenvalue lambda_k(rho_eps)
(simplicity makes the limit unique), so the whole family converges.
  (iii) (1/delta) H'((x - x_j - eps)/delta) is a Dirac family (integral 1,
support in |x - x_j - eps| < delta), so for uniformly convergent bounded u_n,
  int (1/delta) H'((x - x_j - eps)/delta) u_n(x)^2 dx -> u(x_j + eps)^2.
Combining (i)-(iii) and dominated convergence (the integrands are bounded by
(k pi)^2 |c_+ - c_-| ||u_k^delta||_inf^2 <= C(k, R), independent of delta and
eps),
  lambda_k(rho_eps) - lambda_k(rho_0)
    = lim_delta int_0^eps d/d s lambda_k(rho_s^delta) ds
    = int_0^eps lambda_k(rho_s)(c_+ - c_-) u_k(rho_s; x_j + s)^2 ds.
Dividing by eps and letting eps -> 0 uses the continuity of
s |-> u_k(rho_s; x_j + s)^2 at s = 0, which follows from the same compactness
argument (s |-> rho_s is L^1-continuous with distance |c_+ - c_-||s| on the
neighborhood; eigenfunctions converge uniformly along converging densities;
x_j + s -> x_j).  The argument is symmetric in the sign of eps, so the
two-sided derivative exists at every jump position.

(c) Stationarity.  At an interior extremum of D over a cell in which x_j is a
free parameter: rightward distance derivative -(c_+ - c_-) f(x_j) and leftward
+(c_+ - c_-) f(x_j) must both be <= 0 (maximum) or both >= 0 (minimum), which
forces (c_+ - c_-) f(x_j) = 0; since c_+ != c_-, f(x_j) = 0.  Checked.

(d) Sign cross-checks (numeric, evidence): verify_fh_sign.py V1: signed
derivative of lambda_1 under jump translation 30.8283210 vs formula
30.8283199; V2: rightward/leftward one-sided distance derivatives with the
predicted sign flip; V4: for the symmetric barrier family dD/du = -2(R-1) f(u)
at u in {0.2, 0.3, 0.4, 0.49} (error <= 1.4e-6); this matches the two-jump
combination: left jump contributes -(R-1) f(a), right jump (moving left)
contributes -(R-1) f(1-a) = -(R-1) f(a) by symmetry, total -2(R-1) f(a);
V5: stationarity at u* = 0.451485468013 with D* = 32.613983617704 (contract
match 4e-12).  Evidence only.

Finding F-002 (IMPRECISE, documented): the O1 audit run's parenthetical "the
two-sided derivative exists only where f(x_j) = 0" is imprecise.  The
two-sided derivative of eps |-> D(rho_eps) exists at every jump position
(part (b) above); what fails unless f(x_j) = 0 is that the rightward and
leftward DISTANCE derivatives have opposite signs.  The stationarity
consequence f_N(x_j) = 0 is identical under either formulation.  No
mathematical consequence; recorded for the record.

### 2.3 O1c - structure of f (Lemma 2, repair R3)

Claim re-derived: for ANY rho in K, with u_1 > 0 on (0,1), u_2 > 0 on
(0, z_0), u_2 < 0 on (z_0, 1) (z_0 the unique interior zero of u_2; repair
R3 = this explicit sign convention, consistent with AEH's "u_{1,2}(x) > 0
for 0 < x < eps" plus Sturm oscillation), the function
f = lambda_1 u_1^2 - lambda_2 u_2^2 has at most two zeros in (0,1) and
{f > 0} is a single interval (x_-, x_+) with 0 <= x_- < z_0 < x_+ <= 1.

Re-derivation.  W = u_1 u_2' - u_1' u_2 satisfies
  W' = (lambda_1 - lambda_2) rho u_1 u_2,
and W(0) = W(1) = 0 (Dirichlet).  With the sign convention, u_1 u_2 > 0 on
(0, z_0) and u_1 u_2 < 0 on (z_0, 1); lambda_1 - lambda_2 < 0; rho > 0.
So W' < 0 on (0, z_0) and W' > 0 on (z_0, 1).  W(0) = 0 forces W < 0 on
(0, z_0]; W(1) = 0 together with W' > 0 on (z_0, 1) forces W < 0 on
[z_0, 1).  Hence W < 0 on (0, 1) and v = u_2/u_1 satisfies v' = W/u_1^2 < 0:
v is strictly decreasing on (0, 1), v(z_0) = 0, v(0+) = u_2'(0)/u_1'(0) > 0,
v(1-) = u_2'(1)/u_1'(1) < 0 (the endpoint slopes are nonzero by simplicity of
the zeros; u_1'(1) < 0, u_2'(1) > 0 under the sign convention).

Now f = lambda_1 u_1^2 (1 - (lambda_2/lambda_1) v^2); with
c = sqrt(lambda_1/lambda_2) in (0, 1), f = 0 iff |v| = c.  On (0, z_0), v is
positive strictly decreasing, so v = c has at most one solution x_-; on
(z_0, 1), v is negative strictly decreasing, so v = -c has at most one
solution x_+.  Hence at most two zeros.  Moreover
  {f > 0} = {|v| < c} = (x_-, x_+)
(with the convention x_- = 0 when v(0+) <= c and x_+ = 1 when -v(1-) <= c),
and f(z_0) = lambda_1 u_1(z_0)^2 > 0 places z_0 strictly inside the interval.
Checked in full.

Relationship to AEH Lemma 2.2: AEH prove (u_2/u_1)' < 0 only on (0, x_0)
(via W' < 0 there) and finish with a reflection argument; the candidate's
global W < 0 argument is rho-independent, covers (0, 1) directly, and yields
AEH items (1), (4), (5) as consequences.  Both are valid; no conflict.

Numeric evidence: verify_structure_f.py on 22 hostile configs (alternating
1/R blocks, random continuous values, random bang-bang, 3-8 blocks):
u_1 zero-free, u_2 exactly one interior zero, W < 0 on (0, 1), v strictly
decreasing, f at most two interior zeros, {f > 0} a single interval
containing z_0.  Evidence only.

### 2.4 O1d - compactness and at most two effective jumps (Lemma 4)

Claim re-derived: for each N >= 0, D attains its max and min on K_N
(piecewise constant rho in K with at most N jumps), and any extremizer admits
a minimal representation with at most two EFFECTIVE jumps (an effective jump
is an interior point x in (0, 1) at which the one-sided limits differ).

(a) Compactness.  K_N is the image of Omega_N x [1, R]^{N+1}, where Omega_N =
{0 <= x_1 <= ... <= x_N <= 1} is compact, under the map (x, c) |-> rho into
L^1, which is continuous (small changes of jump positions move rho by small
L^1 amounts; small changes of values move rho by small L^1 amounts).  D is
continuous on K in the L^1 topology (Lemma 1).  Hence extrema exist.

(b) Minimal representation.  Boundary jumps (at 0 or 1) have zero measure
effect and are absorbed; adjacent equal values are coalesced; remaining
effective jumps are distinct interior points 0 < x_1 < ... < x_k < 1 with
adjacent distinct values.  Each x_j is a free interior parameter: small
order-preserving perturbations stay in the same combinatorial cell and in
K_N.

(c) Stationarity at every effective jump.  The restricted map D_cell
(delta_1, ..., delta_k) attains a local extremum at 0 (the extremizer is a
global, hence local, extremum of D over K_N, and the cell contains a
neighborhood of the point).  Lemma 3 (two-sided differentiability at every
jump) gives
  d/d delta_j D_cell|_0 = -(c_j - c_{j-1}) f(rho^N)(x_j) = 0,
with c_{j-1}, c_j the adjacent distinct values.  Hence f(rho^N)(x_j) = 0 for
j = 1, ..., k.  By Lemma 2, f has at most two zeros in (0, 1), so k <= 2.
k = 0 (constants) is trivially <= 2.  Checked.

Note on the packet requirement "Numeric spot checks are evidence only": the
2-parameter reduction is verified numerically at the level of the families
(verify_reduction_search.py: R in {2,4,10,50}, bar_max/well_min match the
contract, e.g. R=4: 32.6139836177 / 6.7844823391; 300 adversarial configs,
zero violations), which is consistent with, but not a substitute for, the
proof above.

### 2.5 O1e - step functions are dense (Lemma 5)

Claim re-derived: sup over step functions in K equals sup_K D; with
M_N = max_{K_N} D (exists by Lemma 4), M_N is nondecreasing and
M_N -> sup_K D.  Mirror for m_N = min_{K_N} D.

For rho in K let rho_m be the block average of rho on the uniform partition
of [0, 1] into 2^m intervals.  Then 1 <= rho_m <= R pointwise, rho_m is
piecewise constant with at most 2^m - 1 jumps, and rho_m -> rho in L^1
(standard Lebesgue averaging).  By Lemma 1, D(rho_m) -> D(rho).  Hence the
sup over step functions equals sup_K D.  K_N is nested increasing, so M_N is
nondecreasing, and M_N -> sup_N M_N = sup over all step functions in K =
sup_K D.  The inf statement is identical.  Checked.

### 2.6 O1f - bang-bang structure at a global extremizer (Lemma 6)

Claim re-derived: any global maximizer rho~ of D over K satisfies rho~ = R
a.e. on {f~ > 0} and rho~ = 1 a.e. on {f~ < 0}; any global minimizer
satisfies the reversed assignment.

The proof needs rho~ to be piecewise constant (to get an open cell on which
rho~ is bounded away from R).  In the synthesis (Section 2.7) the maximizer is
constructed inside K_2, so this holds; finding F-003 records that the
hypothesis should be stated as "rho~ in K_2 a global maximizer of D over K".

Argument, re-derived.  If {f~ > 0} cap {rho~ < R} has positive measure, then
because rho~ is piecewise constant there is an open cell I on which rho~ is
constant < R; {f~ > 0} is open (f~ continuous), so the intersection contains
an interval J with closure inside {f~ > 0} and rho~ <= R - eta on J for some
eta > 0 (and f~ >= delta > 0 on J).  For 0 <= kappa <= eta,
w(kappa) = rho~ + kappa chi_J lies in K.  AEH Lemma 2.1 (V = 0, w = w(kappa),
C = R, dw/d kappa = chi_J in L^1; hypotheses verified, Section 3.1) gives
  d/d kappa D(w(kappa))|_0 = int_0^1 chi_J f~ dx = int_J f~ dx > 0,
contradicting maximality (at a maximum every admissible right derivative is
<= 0).  Hence rho~ = R a.e. on {f~ > 0}.  The mirror on {f~ < 0}: if
{f~ < 0} cap {rho~ > 1} had positive measure, take J with rho~ >= 1 + eta on
J and w(kappa) = rho~ - kappa chi_J; then dD/d kappa|_0 = -int_J f~ dx > 0,
again a contradiction; so rho~ = 1 a.e. on {f~ < 0}.  The minimizer is the
mirror (right derivatives >= 0 at a minimum).  "a.e." is the correct level of
precision: null-set changes of rho do not change the operator.  Checked.

Finding F-003 (PRESENTATIONAL, non-substantive): the claim as written says
"Let rho~ be a global maximizer of D over K (which exists by Lemmas 4 and 5
and compactness of K_2, see the synthesis below)" and the proof uses the
piecewise-constant structure of rho~.  The existence argument (sup_K D =
sup_{K_2} D, attained in K_2) is completed in Section 9 of the candidate
BEFORE Lemma 6's conclusion is used, so there is no circularity; the
recommended formulation is "Let rho~ in K_2 be a global maximizer of D over
K".  Non-substantive; no change to the mathematics.

### 2.7 Synthesis (SUP/INF, attainment)

SUP, re-derived.  Lemma 5: sup_K D = lim_N M_N.  Lemma 4: M_N is attained and
its extremizer admits a minimal representation in K_2, so M_N = D(rho^N)
<= sup_{K_2} D; the reverse inequality sup_{K_2} D <= sup_K D is trivial
(K_2 subset K).  Hence sup_K D = sup_{K_2} D.  K_2 is compact (continuous
image of Omega_2 x [1, R]^3) and D is continuous (Lemma 1), so the sup is
attained at rho~ in K_2, which is then a global maximizer over K.  Lemma 6
gives rho~ = R a.e. on {f~ > 0} and = 1 a.e. on {f~ < 0}; Lemma 2 identifies
{f~ > 0} = (x_-, x_+) as a single interval with endpoints allowed to be 0 or
1.  Hence rho~ = rho^{bar}_{x_-, x_+} a.e., so
  sup_K D = D(rho~) <= max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),
and the reverse inequality is trivial (barrier family subset K).  Attainment
of the max: (a, b) |-> D(rho^{bar}_{a, b}) is continuous (rho^{bar}_{a,b} ->
rho^{bar}_{a',b'} in L^1 as (a,b) -> (a',b'), then Lemma 1) on the compact
square [0, 1]^2.  This is (i).  Checked.

INF, re-derived: identical with max/min exchanged; Lemma 6 (minimizer mirror)
gives rho~' = 1 a.e. on {f~' > 0} and R a.e. on {f~' < 0}; Lemma 2 makes
rho~' a.e. a well config; min_{K_2} D = inf_K D by the mirror of Lemmas 4-5.
This is (ii).  Checked.

### 2.8 Theorem statement, normalization, and edge cases

- Statement (i)-(ii): reproduces the draft theorem verbatim in content; no
quantifier or class change (no silent upgrade).  K = {measurable rho :
1 <= rho <= R a.e.}; D = lambda_2 - lambda_1; barrier/well families with
closed parameter domain 0 <= a <= b <= 1.
- Edge cases inside the closed families: a = b gives rho = 1, lambda_k =
k^2 pi^2, D = 3 pi^2; (a, b) = (0, 1) gives rho = R, D = 3 pi^2 / R;
a = 0 or b = 1 give the two-block members.  All covered by the parameter
domain and by Lemma 1 continuity.
- R = 1 is excluded (K = {1}, trivial); the statement is continuous in R at
R = 1.
- Quantifiers: R > 1 fixed; constants depend on R and k, not on rho; "a.e."
statements are w.r.t. Lebesgue measure.
- Normalization: u_k are L^2(rho)-normalized (int rho u_k^2 = 1), matching
AEH Lemma 2.1's convention (int w u_n^2 = 1, verified in the source).

## 3. Cross-cutting checks

### 3.1 Premise rechecks against primary sources

P1. AEH Lemma 2.1 (Feynman-Hellmann), arXiv:2407.02459v2, papers/fundamental_gap.txt
(sha256 2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14).
Verbatim (OCR glyph corruption noted in the txt, e.g. an OCR pi glyph for pi; content
cross-checked): "Suppose that V(.,t) and w(.,t) are one-parameter families of
real-valued, locally L1 functions, with inf V(x,kappa) > -inf, C >= w(x,kappa)
>= 1/C for some C > 0, and dV/dkappa(x,kappa) and dw/dkappa(x,kappa) in
L1(0,pi).  Then d lambda_n(kappa)/dkappa = -lambda_n int_0^pi (dw/dkappa)
u_n^2(x,kappa) dx + int_0^pi (dV/dkappa) u_n^2(x,kappa) dx."  The proof in the
source fixes the normalization int w u_n^2 = 1.  Hypotheses met in both uses:
(a) Lemma 6 pointwise perturbations: V = 0, w(kappa) = rho~ +/- kappa chi_J in
[1, R], dw/dkappa = +/- chi_J in L^1, inf V = 0 > -inf; (b) Lemma 3 smoothed
families: V = 0, w = rho_eps^delta in [1, R] uniformly, dw/deps in C_c^inf
subset L^1.  Interval: the source is on (0, pi); this run's problem on (0, 1)
is an affine rescaling (x |-> pi x), harmless and documented.

P2. AEH Lemma 2.2 (structure of u_2/u_1): verbatim items (1)-(5) confirmed in
the same file, including W' = (lambda_1 - lambda_2) w u_1 u_2 and the sign
convention "u_{1,2}(x) > 0 for 0 < x < eps".  The candidate's Lemma 2 is a
rho-independent re-derivation with the global W < 0 argument; both prove
items (1), (4), (5).  No conflict.

P3. Weyl/min-max inequality for self-adjoint compact operators: standard;
|mu_k(A) - mu_k(B)| <= ||A - B||.  Applied to the self-adjoint S_rho (not to
the non-self-adjoint T_rho; that was the draft's O1a defect).

P4. Comparison bounds k^2 pi^2 / R <= lambda_k(rho) <= k^2 pi^2: Rayleigh
quotient lambda_k = min_{dim S = k} max_{0 != y in S} (int y'^2)/(int rho y^2)
with 1 <= rho <= R; derived in this run; verified numerically (verify_hs_bound
H3).

P5. Sturm oscillation (u_k has exactly k-1 simple interior zeros): classical
for -y'' = lambda rho y with rho bounded below by a positive constant and
Dirichlet BCs; used for z_0.  Verified numerically on hostile configs.

P6. Keller 1976 / Mahar-Willner 1976: context only.  Both treat the RATIO
lambda_2/lambda_1 over piecewise-continuous densities with a bounded number of
jumps; O1 treats the GAP over the full measurable box class.  O1 is not a
corollary of either; the N-jump approximation ladder (Lemmas 4-5) is needed.
No premise obligation for O1 arises from P6.

### 3.2 Non-circularity audit

- Lemma 1 uses: the similarity S_rho ~ T_rho, the eigenvalue identity, the HS
kernel bound, Weyl, and the Rayleigh comparison bounds.  None of these uses
the theorem under proof.
- Lemma 2 uses: the Wronskian computation and Sturm oscillation.
- Lemma 3 uses: AEH Lemma 2.1 (primary source), Lemma 1 (eigenvalue
convergence under L^1 density convergence), and the uniform H^2 bounds.  Lemma
1 does not depend on Lemma 3, so the dependency is acyclic.
- Lemma 4 uses Lemmas 1-3; Lemma 5 uses Lemma 1; Lemma 6 uses AEH Lemma 2.1
and the existence of a global maximizer (established in Section 9 from Lemmas
1, 4, 5 before Lemma 6's conclusion is used - see F-003); the synthesis uses
Lemmas 1-6.
- No lemma uses the theorem being proved.  The only forward reference is
presentational (F-003) and not a logical dependency.

### 3.3 Reproducibility of the numeric battery

All scripts are under reproducibility/ with fixed seeds recorded in their
headers; outputs are recorded as *out.json.  In this continuation session
(2026-08-06) verify_bangbang.py (~14 s) and verify_smoothing_r4.py (~25 s)
were re-run from the committed state and produced bit-identical outputs,
confirming reproducibility of the recorded results.  The heavier battery
(verify_hs_bound.py ~117 s, verify_fh_sign.py ~103 s, verify_structure_f.py
~175 s, verify_reduction_search.py ~144 s) was run earlier in this run's
ledger (R-004..R-009) with outputs preserved under reproducibility/.

### 3.4 Numeric evidence vs proof-level claims

Every proof-level claim in candidate_proof.md is argued analytically; the
scripts are corroborating evidence only.  The R=4 contract values
(sup_K D = 32.6139836177, inf_K D = 6.7844823391) and the stationarity point
u* = 0.451485468013 are reproduced by two independent solvers (transfer-matrix
and finite-difference paths in the battery), which strengthens confidence but
is not part of the proof.

## 4. Findings log

- F-001 (REPAIRABLE, applied): Lemma 1 (b) pre-correction line
  "||S-S||_HS^2 <= (R/16)||rho-sigma||_2^2" is arithmetically wrong; the
  correct chain is (R/32)(||A||_2^2 + ||A||_1^2) <= (R^2/16)||A||_1 via
  ||A||_2^2 <= R||A||_1 and ||A||_1 <= R - 1.  Final bound (R/4)||A||_1^{1/2}
  unaffected.  Corrected in the delivered candidate_proof.md Section 3 (b);
  both versions recorded in Section 2.1.
- F-002 (IMPRECISE, documented): the O1 audit run's claim that the two-sided
  derivative exists only where f(x_j) = 0 is imprecise; the two-sided
  derivative of eps |-> D(rho_eps) exists at every jump position, while the
  one-sided DISTANCE derivatives have opposite signs unless f(x_j) = 0.
  Stationarity consequence unchanged (Section 2.2).
- F-003 (PRESENTATIONAL): Lemma 6 should state its hypothesis as "rho~ in K_2
  a global maximizer of D over K"; the piecewise-constant hypothesis used in
  the proof is satisfied by the synthesis's construction.  No circularity
  (Section 2.6).
- F-004 (CONTEXT): the draft run's u* digit discrepancy (~2e-9 in the last
  digits) is a precision artifact of the draft-run solver; this run's
  D*/lambda values agree with the contract to 1e-11 (ledger R-003 / C-003).
  No mathematical consequence.
- F-005 (PROCESS): ledger entry R-010 falsely claimed that audit_report.md was
  written in the original session; the file was lost and is delivered in this
  continuation session.  R-010 is not retro-edited; new entries (R-011+) record
  the actual work.

## 5. Residual gaps and independent re-audit instructions

Residual obligations for the independent verifier pass (required by the
upstream skill's revision policy before the manager closes O1):
- Re-verify Lemma 1 (O1a): the similarity algebra, the HS kernel bound with
  the F-001 correction, the Weyl chain |1/lambda_k(rho) - 1/lambda_k(sigma)|
  <= ||S_rho - S_sigma||_HS, and the conversion to lambda_k via the comparison
  bounds.
- Re-verify Lemma 3 (O1b): the smoothing construction (R4), the uniform H^2
  bounds, the Dirac-family limit, the dominated-convergence step, and the
  two-sided differentiability; confirm the sign dD/d eps = -(c_+ - c_-) f(x_j)
  (R2).
- Confirm the theorem statement was not silently upgraded (Section 2.8).
Out of scope for this run (packet scope = O1): O2 (symmetric 1-parameter
analysis) and O3 (2-parameter symmetry), owned by the draft run.
Novelty status: see status_and_literature.md (Sun 2022 covers the minimum gap
in a bounded-jump subclass; the S1/S2 class definitions are unresolved from
public metadata; the box-class reduction theorem and the SUP side appear not
to be in the literature).

## 6. Confidence by axis

- Semantic fidelity (statement matches draft and audit): HIGH.  (i)-(ii)
  verbatim; repairs R1-R4 applied exactly as listed and re-derived, not
  copied.
- Mathematical correctness: HIGH for O1a-O1f after the F-001 correction,
  which is applied to the delivered text and re-verified here.  The remaining
  step is the independent verifier pass (Section 5); a reviser cannot
  self-certify closure.
- Completeness: HIGH for the O1 scope (all six obligations plus synthesis and
  edge cases closed).  O2/O3 are excluded by the packet.
- Novelty: MEDIUM-HIGH.  No source was found for the box-class reduction
  theorem (sup_K D = max over the barrier family and inf_K D = min over the
  well family over the full measurable class).  Sun 2022 proves a minimum-gap
  result in a bounded-jump piecewise-continuous class (S1/S2 definitions not
  available from public metadata); its relationship to O1's INF side is
  analyzed in status_and_literature.md and the final report.
- Reproducibility: HIGH.  Scripts, seeds, outputs, and hashes are recorded;
  two scripts were re-run fresh in this session with bit-identical outputs.
