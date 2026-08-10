# Status and literature - audit recheck

This file records, for each premise cited by the O1 draft and each source
named in the task packet, the exact statement found in the primary source and
whether the draft's use is valid.

## Premises actually used by O1_reduction_draft.md

### 1. AEH arXiv:2407.02459v2 Lemma 2.1 (Feynman-Hellmann)
Source: papers/fundamental_gap.txt, Lemma 2.1 (verbatim content):
"Suppose that V(.,t) and w(.,t) are one-parameter families of real-valued,
locally L1 functions, with inf V(x,kappa) > -inf, C >= w(x,kappa) >= 1/C for
some C > 0, and dV/dkappa and dw/dkappa in L1(0,pi). Then
d lambda_n/dkappa = -lambda_n int_0^pi (dw/dkappa) u_n^2 dx
                  + int_0^pi (dV/dkappa) u_n^2 dx."  (u_n normalized by
int w u_n^2 = 1; the proof is by Kato analytic perturbation theory and
integration by parts; interval [0,pi].)
Audit of the draft's use: for our problem V = 0, w = rho in [1,R], interval
[0,1] (affine rescaling is harmless).  (a) Pointwise perturbations of rho by
L^1 functions: hypotheses met exactly; formula valid.  (b) Moving-a-jump
families rho_eps = rho - (c_+ - c_-) chi_(x_j,x_j+eps): the perturbation is
L^1, but d(rho)/deps is a Dirac measure, not in L^1; AEH Lemma 2.1 does NOT
literally cover this.  The derivative is obtained by the standard
approximation/regularization of the step (or directly by the transfer-matrix
computation); the draft's claim "by Lemma 1 ... and the Feynman-Hellmann
formula (AEH Lemma 2.1)" skips this justification.  This is a presentation
gap, not a fatal one (standard).  CRITICAL: the SIGN in the draft Lemma 3 is
wrong even after this justification (see O1b verdict).
Status of the lemma itself: KNOWN (verified from primary source).

### 2. AEH arXiv:2407.02459v2 Lemma 2.2 (monotonicity / structure of f)
Source: papers/fundamental_gap.txt, Lemma 2.2 (verbatim content), items:
(1) u_2/u_1 is decreasing on (0,pi);
(2) |u_1| = |u_2| has one or two solutions on (0,pi);
(3) there are x_-, x_+ with 0 <= x_- < x_+ <= pi, at least one interior, with
    u_1^2 > u_2^2 on (x_-,x_+) and u_1^2 <= u_2^2 on the complement;
(4) lambda_1 |u_1^2| = lambda_2 |u_2^2| has one or two solutions on (0,pi);
(5) there are xhat_-, xhat_+ with lambda_1 u_1^2 > lambda_2 u_2^2 on
    (xhat_-,xhat_+) and <= on the complement.
Hypotheses: "the same assumptions on V and w as in Lemma 2.1" (V, w locally
L^1, inf V > -inf, C >= w >= 1/C); sign convention u_{1,2} > 0 near 0.
Proof uses W' = (lambda_1 - lambda_2) w u_1 u_2 and v' = W/u_1^2 < 0 on
(0,x_0) with u_2(x_0) = 0, then reflects.
Audit: the draft Lemma 2 is a correct re-derivation of (1),(4),(5) (with the
same Wronskian, stated rho-independently).  All hypotheses met for V = 0,
w = rho in [1,R] (bounded measurable).  The draft adds the explicit claim
"the unique zero z_0 of u_2" (Sturm oscillation: u_2 has exactly one interior
zero) and "{f>0} contains z_0" (f(z_0) = lambda_1 u_1(z_0)^2 > 0); both are
correct.  One presentation note: the draft should state the sign convention on
u_2, as AEH does.
Status of the lemma: KNOWN (verified from primary source); draft use: valid.

### 3. Min-max (Weyl) continuity of eigenvalues of self-adjoint compact operators
Source: standard (not a paper); the draft cites it in Lemma 1.
Audit: the inequality |mu_k(A) - mu_k(B)| <= ||A - B|| is valid for
self-adjoint compact operators.  The draft applies it to T_rho, which is not
self-adjoint on L^2; see O1a verdict (repair: apply to S_rho).
Status: standard fact, TRUE; draft use: invalid as written, repairable.

## Sources named in the packet (relevance recheck)

### Keller 1976 (SIAM J. Appl. Math. 31(3), 485-491), DOI 10.1137/0131042
Source: papers/keller1976.txt.  Problem: ratio lambda_2/lambda_1 for
y'' + lambda phi y = 0, y(+-1/2) = 0, over piecewise continuous phi with a
bounded number of jumps, a <= phi <= A; min of lambda_2/lambda_1; minimizer
piecewise constant = a on (-x_0,x_0), A elsewhere (abstract; Theorem 0
attributed in MW).
Audit: Keller is NOT used as a premise in O1_reduction_draft.md.  It is a
template (ratio, bounded-jump class).  No verification obligation arises for
O1 from Keller; the status_and_literature.md description of the draft run is
consistent with the source.
Class difference to note: Keller/MW work in the bounded-jump class; O1 treats
the full measurable box class via N-jump approximation.  O1 is not a
corollary of Keller 1976.

### Mahar-Willner 1976 (CPAM 29, 517-529), DOI 10.1002/cpa.3160290505
Source: papers/mw1976.txt.  Problem: extremal ratios lambda_2/lambda_1 (and
lambda_j/lambda_k) over piecewise continuous phi, a <= phi <= 1, bounded
number of jumps.  Theorem 0 (attributed to Keller): extremizing function
piecewise constant taking values a and 1.  Theorems 1-2: extremizer has no
jumps or exactly two, symmetric about 0.  Theorem 3: periodic extension
extremizes lambda_{2n}/lambda_n.  Lemma 1-2: extension identities.
Audit: MW is NOT used as a premise in O1_reduction_draft.md.  The draft-run
status file describes it as structural template.  The O1 bang-bang argument is
independent of MW Theorem 0 (it uses AEH Lemma 2.1 directly).  No verification
obligation for O1 arises from MW.

### Cheng-Kung-Law-Lian 2010 (CAMWA 60, 2556-2563)
Source: papers/cheng2010.txt (not quoted in detail; context only).
Audit: NOT used in O1_reduction_draft.md.  Referenced in the draft-run
status_and_literature.md as a symmetrization template; no O1 premise.

### Ashbaugh-Benguria 1989 (PAMS 105, 419-424)
Listed in the draft problem_contract.md citation constraints; NOT used in
O1_reduction_draft.md.  No O1 premise.

## Status of the audited theorem (novelty scope note)

The reduction statement (sup/inf over box class = sup/inf over the two
parameter barrier/well families) is, to the coverage of this audit, not
present in the four sources above (Keller/MW solve the ratio problem in the
bounded-jump class; AEH solve the gap MINIMUM over the single-barrier class,
not the box-class maximum; CKKL/AB89 are different classes).  Novelty for the
FINAL theorem is out of scope for this audit run (O5 in the draft run); the
audit only certifies the O1 reduction obligations.
