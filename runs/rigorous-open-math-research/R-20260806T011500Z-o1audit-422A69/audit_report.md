# Audit report - O1 reduction theorem (O1a-O1f)

- Audit run: R-20260806T011500Z-o1audit-422A69
- Audit target: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md
- Packet: agenda/task-packets/Q-20260806-o1-audit-422A69.md
- Mode: READ-ONLY.  The draft was not modified.  Gaps are reported precisely.

## Verdict (overall)

REPAIRABLE_GAP.  The O1 reduction theorem statement is TRUE; the draft proof
is not acceptable as written because of two local defects (O1a operator
presentation; O1b sign error).  No fatal gap, no circularity, no wrong
problem, and no unverifiable citation was found.  Obligation-level verdicts:

| ID | Verdict | One-line reason |
|---|---|---|
| O1a | PARTIAL | statement true; draft proof invalid as written (T_rho not self-adjoint on L^2); standard repair supplied |
| O1b | FAILED | sign error in dD/deps formula as stated; downstream zero condition unaffected |
| O1c | PROVED | Wronskian argument correct; matches AEH Lemma 2.2 (1),(4),(5) |
| O1d | PROVED | N-jump compactness + at-most-two-effective-jumps valid given O1a and corrected O1b |
| O1e | PROVED | step-function density + continuity |
| O1f | PROVED | bang-bang at global extremizer valid (correct FH sign) |

## O1a - L^1 continuity of lambda_k on the box class
Line-by-line:
- "lambda_k(rho)^{-1} = mu_k(T_rho), the k-th eigenvalue of the self-adjoint
  compact operator T_rho on L^2": the eigenvalue identity is TRUE (T_rho is
  similar to the symmetric Hilbert-Schmidt operator S_rho), but "self-adjoint
  on L^2" is FALSE for the kernel G(x,t)rho(t) (asymmetric kernel).  Failing
  claim: self-adjointness of T_rho on L^2.
- "|mu_k(T_rho) - mu_k(T_sigma)| <= ||T_rho - T_sigma|| by the min-max
  principle": NOT valid for non-self-adjoint operators as written.
- Operator-norm estimate itself is fine: |(T_rho - T_sigma) f|(x) <=
  ||G(x,.)||_inf ||rho - sigma||_2 ||f||_2 <= (1/4) sqrt(2R) sqrt(||rho-sigma||_1) ||f||_2,
  hence ||T_rho - T_sigma|| -> 0.
- Repair (state only, per packet): apply min-max to S_rho = rho^{1/2} T_rho
  rho^{1/2}; ||S_rho - S_sigma||_HS -> 0 (bound in candidate_proof.md), so
  |1/lambda_k(rho) - 1/lambda_k(sigma)| -> 0; lambda_k is bounded away from 0
  and infinity on K, so lambda_k itself is continuous.
- Numeric spot check: moving a jump by eps in {1e-3,1e-4,1e-5} changes
  lambda_1 by (1.0e-2, 1.0e-3, 1.0e-4) and lambda_2 by (7.4e-2, 7.4e-3,
  7.4e-4): consistent with Lipschitz-in-L^1 behavior (evidence only).
Decision: PARTIAL (repairable).  The obligation graph marked it OPEN with
"standard; cite" - the audit agrees a precise citation or the repair above is
required; the draft's own proof does not suffice as written.

## O1b - FH derivative at a moving jump
Line-by-line:
- Draft: "rho_eps = rho + (c_+ - c_-) chi_(x_j, x_j+eps) (up to the sign of
  eps)": for eps > 0 the correct expression is rho_eps = rho - (c_+ - c_-)
  chi_(x_j,x_j+eps); the parenthetical "up to the sign of eps" conceals a
  definite sign choice.
- Draft: "d lambda_k/d eps = -lambda_k int d(rho)/d eps u_k^2 dx -> -lambda_k
  (c_+ - c_-) u_k(x_j)^2": with d(rho)/d eps = -(c_+ - c_-) delta_{x_j} the
  correct limit is +lambda_k (c_+ - c_-) u_k(x_j)^2.
- Draft conclusion "dD/deps = (c_+ - c_-) f(x_j)": FALSE.  Correct:
  dD/deps = -(c_+ - c_-) f(x_j) for rightward motion (and +(c_+ - c_-) f(x_j)
  for leftward motion; the two-sided derivative exists only if f(x_j) = 0).
- Cross-check vs the draft-run's own verified identity (R-003 ledger and the
  draft problem contract): dD/du = -2(R-1) f(u) for the symmetric barrier
  family.  Reproduced here at u in {0.2,0.3,0.4,0.49}: (dD/du_num,
  -2(R-1)f) = (32.418877, 32.418877), (89.290717, 89.290716),
  (143.281690, 143.281690), (-96.305793, -96.305793); at u* =
  0.45148546576 both ~ 0 (4e-8 / -2.6e-7).  The draft's Lemma 3 sign would
  give +2(R-1) f(u), contradicting these numbers.
- Consequence audit: the only downstream use is Lemma 4's stationarity
  condition at effective jumps.  At an interior extremum both one-sided
  derivatives are <= 0 (max) / >= 0 (min), forcing f_N(x_j) = 0 in all cases.
  The zero condition is unaffected by the sign error.
- Note on hypotheses: AEH Lemma 2.1 requires dw/dkappa in L^1; for a moving
  jump the derivative is a Dirac measure.  The formula is standard via
  approximation, but the draft should justify it (minor gap R4).
Decision: FAILED (as stated), with the consequence valid.  The obligation
graph's O1b entry "PROVED by L^1 perturbation + continuity of eigenfunctions"
is therefore not correct as written; the repaired statement holds.

## O1c - structure of f (Wronskian)
Line-by-line:
- W' = (lambda_1 - lambda_2) rho u_1 u_2: correct (difference of the two
  eigenvalue equations).
- W(0) = W(1) = 0: correct (Dirichlet boundary conditions).
- Sign pattern W' < 0 on (0,z_0), W' > 0 on (z_0,1): correct for u_1 > 0 on
  (0,1), u_2 > 0 on (0,z_0), u_2 < 0 on (z_0,1) (sign convention WLOG; the
  draft should state it explicitly - R3).
- W < 0 on (0,1): correct (from W(0)=0, W' < 0 on (0,z_0), and W(1)=0,
  W' > 0 on (z_0,1), continuity at z_0).
- v = u_2/u_1 strictly decreasing with v(z_0)=0, v(0+) > 0 > v(1-): correct.
- f = u_1^2 (lambda_1 - lambda_2 v^2): f = 0 iff |v| = sqrt(lambda_1/lambda_2);
  at most one solution in each of (0,z_0), (z_0,1); {f > 0} = {|v| < c} is a
  single interval containing z_0 (f(z_0) = lambda_1 u_1(z_0)^2 > 0): correct.
- Matches AEH Lemma 2.2 items (1),(4),(5); the rho-independence claim is
  correct (Wronskian computation needs only positive bounded measurable rho
  and C^1 eigenfunctions; rho in L^infty gives u_k in H^2, hence C^1).
- Numerics: 10 x 3-block + 4 x 5-block configs at R=4: nzeros_u2 = 1,
  nzeros_f = 2, one positive interval containing z_0, W < 0, v strictly
  decreasing, all pass.
Decision: PROVED.

## O1d - N-jump compactness and rho^N existence
Line-by-line:
- K_N is the continuous image of the compact parameter set into L^1:
  correct (coalescing jumps and equal adjacent values cause L^1-null
  differences; D continuous by O1a).  Need O1a (PARTIAL) - dependency noted.
- Existence of extremizer over K_N: correct.
- Minimal representation with k effective jumps has all jumps interior
  (0 < x_1 < ... < x_k < 1) and adjacent values distinct: correct; hence each
  effective jump is a free interior parameter.
- Stationarity at effective jumps f_N(x_j) = 0: correct with corrected O1b.
- k <= 2 by O1c: correct.
Decision: PROVED (given O1a and corrected O1b).  The packet's boundary
cases (a=0, b=1, a=b, constants) are covered by the closed-family
parameterization; numerically verified.

## O1e - M_N -> sup_K D
Line-by-line:
- Block averages in [1,R] converge to rho in L^1: correct (standard
  Lebesgue-differentiation/averaging fact for L^1 functions).
- D(block) -> D(rho): correct by O1a.
- sup over step functions = sup_K D, and sup_K D = sup_N M_N = lim M_N
  (nondecreasing): correct.  Mirror argument for inf: correct.
Decision: PROVED (given O1a).

## O1f - bang-bang at a global extremizer
Line-by-line:
- Existence of a global extremizer rho~ in K_2: correct (O1d/O1e give
  sup_K D = max_{K_2} D, so the K_2 maximizer is a global maximizer; same for
  the minimizer).
- Pointwise FH: dD/dt = int delta rho f~ dx for admissible L^1 perturbations:
  correct (AEH Lemma 2.1, V=0; sign independently verified).
- Maximizer: rho~ = R a.e. on {f~>0}, rho~ = 1 a.e. on {f~<0}: correct
  (raising rho on a positive-measure subset of {f~>0} with rho~ < R strictly
  increases D; the subset can be taken open by continuity of f~ and the
  finite-value structure of the piecewise-constant extremizer).
- Minimizer: reversed: correct.
- Densities taking interior values on intervals: handled (the extremizer is
  piecewise constant with finitely many values; perturbing sets are open by
  continuity of f~).
- Measure-zero changes: eigenvalues depend only on the L^1 class of rho
  (operator and quadratic form), so changes on null sets are irrelevant:
  correct.
- Numerics (local perturbation test): raising rho on {f > 0} by delta on a
  strip of width w = 0.01 raises D by +0.0423 (prediction w f = +0.0442);
  raising on {f < 0} lowers D by -0.1124 (prediction w f = -0.0633, sign
  match): evidence for the direction.
Decision: PROVED.

## Theorem-level synthesis (SUP/INF)
- sup_K D = sup_{K_2} D = max_{K_2} D, attained; bang-bang + O1c make the
  maximizer a barrier config; hence sup_K D = max over barrier family:
  correct.
- inf_K D = min over well family: correct by the mirror argument.
- Attainment over the two-parameter families: correct (compact parameter
  domain [0,1]^2, continuous map into L^1, D continuous).
Decision: theorem TRUE; draft REPAIRABLE_GAP (R1 + R2 required; R3, R4
minor).

## Citation audit summary
- AEH arXiv:2407.02459v2 Lemma 2.1: EXISTS, states the needed FH formula;
  hypotheses met for pointwise perturbations; not literally met for moving
  jumps (R4).  Sign of the draft's application: wrong (O1b).
- AEH Lemma 2.2: EXISTS, states items (1)-(5); draft Lemma 2 is a correct
  re-derivation; all hypotheses met.
- Min-max continuity of self-adjoint compact operators: standard; misapplied
  in the draft to T_rho (O1a).
- Keller 1976, Mahar-Willner 1976, Cheng-Kung-Law-Lian 2010, Ashbaugh-
  Benguria 1989: NOT used as premises in O1_reduction_draft.md; their role in
  the draft-run status file is contextual/template and consistent with the
  primary sources (ratio problems, bounded-jump classes).  No citation
  obligation for O1 arises from them.

## Gap list (for the reviser; smallest failing claims)
- G1 (O1a, structural): "T_rho is self-adjoint on L^2" - false; Weyl
  inequality step invalid.  Repair: S_rho argument or exact citation.
- G2 (O1b, sign): "dD/deps = (c_+ - c_-) f(x_j)" - wrong sign.  Repair:
  -(c_+ - c_-) f(x_j) for rightward motion; note one-sided derivative
  asymmetry.
- G3 (O1b/O1a, hypothesis): moving-jump derivative not literally covered by
  AEH Lemma 2.1 (dw/dkappa is a delta).  Repair: approximation argument
  (standard).
- G4 (O1c, presentation): sign convention on u_2 not stated.
- No FATAL gaps found.

## Confidence by axis
- Semantic fidelity: HIGH.  The audited statement matches the draft theorem
  and the packet's description (box class, Dirichlet, D = lambda_2 - lambda_1,
  barrier/well families, attainment).
- Mathematical correctness: HIGH for O1c-O1f and the synthesis (each verified
  line-by-line and, where computational, cross-checked to ~1e-7); O1a is
  PROVED after a standard repair (draft text itself PARTIAL); O1b is FAILED
  as stated but the theorem consequence is valid.
- Completeness: obligations O1a-O1f all carry verdicts; O2/O3 out of scope
  per packet.
- Novelty: not assessed in this run (O5 belongs to the draft run).
- Reproducibility: scripts + seeds + outputs stored under
  reproducibility/; hashes of all inputs recorded in repro_manifest.md.
