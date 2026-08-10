# Approach registry (audit)

This run is an audit, so "routes" are the independent verification strategies
used to check the O1 obligations, each with its exact status and outcome.

## Route AV1: source-level recheck of cited lemmas (literature auditor)
- Mechanism: quote AEH Lemma 2.1 and 2.2 verbatim from
  papers/fundamental_gap.txt (arXiv:2407.02459v2); check hypotheses and the
  exactness of the draft's use.
- Target obligations: O1b (FH), O1c (Wronskian), and the min-max step in O1a.
- Outcome: Lemma 2.1 verified; its hypothesis (dw/dkappa in L^1) does NOT
  cover moving jumps (delta derivative) - presentation gap.  Lemma 2.2
  verified; draft Lemma 2 is a correct re-derivation.  Min-max fact is
  standard but applied to a non-self-adjoint operator in the draft.
- Status: COMPLETE.

## Route AV2: exact transfer-matrix numerics (computation specialist)
- Mechanism: vectorized transfer-matrix solver for piecewise-constant rho
  (reproducibility/verify_o1_audit.py), bisection in lambda to 1e-13,
  eigenfunctions and f at jump points exactly, one-sided jump derivatives by
  finite differences.
- Target obligations: O1b (sign), O1c (structure), O1e (u*/D* reproduction),
  O1a (L1 continuity spot check).
- Outcome: O1b sign error confirmed (draft formula fails; corrected formula
  matches to ~1e-4..1e-7).  O1c structure holds on 10 x 3-block + 4 x
  5-block configs.  u* = 0.45148546576, D* = 32.61398361770 reproduce the
  contract to 1e-8.  Random search over 1200 configs (2-6 blocks) does not
  beat SUP 32.61398 nor INF 6.78448 (evidence only).
- Status: COMPLETE (evidence; not proof).

## Route AV3: independent finite-difference cross-check
- Mechanism: generalized eigenvalue problem on a 4000-point grid with scipy
  eigh, comparing lambda_1, lambda_2 for the u = 0.2 barrier config.
- Outcome: FD (2.651041, 12.313059) vs transfer matrix (2.650698, 12.308664);
  agreement to discretization accuracy (O(h^2), h = 2.5e-4, relative diff
  ~1.3e-4).  Confirms the solver.
- Status: COMPLETE.

## Route AV4: corrected local bang-bang test
- Mechanism: perturb rho by +delta on a small interval strictly inside
  {f > 0} and strictly inside {f < 0} (splitting the relevant block), compare
  dD with w * f(x_0).
- Outcome: increasing rho on {f > 0} increases D (dD ~ w f > 0); increasing
  on {f < 0} decreases D (dD ~ w f < 0).  Confirms the O1f direction with the
  corrected FH sign.
- Status: COMPLETE (evidence).

## Route AV5: boundary-case sweep
- Mechanism: evaluate D for rho = 1, rho = R, 2-block configs, and a = b
  degeneracies; compare with closed-family membership.
- Outcome: D(rho=1) = 3 pi^2, D(rho=R) = 3 pi^2/R (1e-8); 2-block and a = b
  configs lie inside the closed barrier/well families; all numerically below
  SUP / above INF.
- Status: COMPLETE (evidence).

## Route AV6: hypothesis audit for the N-jump compactness (structural)
- Mechanism: check continuity of the parameter map into L^1, interiority of
  effective jumps, and the one-sided stationarity conditions.
- Outcome: O1d sound given O1a and corrected O1b; the "iterate to minimal
  representation" step is valid; note that a boundary jump (x = 0 or 1) cannot
  occur in the minimal representation (nonempty blocks).
- Status: COMPLETE.

## Route AV7 (NOT pursued): independent re-derivation of O2/O3
- Out of scope: the packet audits only the reduction O1.  O2 (symmetric
  1-parameter uniqueness) and O3 (2-parameter critical point) remain OPEN in
  the draft run and are not re-audited here.
- Status: OUT OF SCOPE.

## Route state summary
- COMPLETE: AV1, AV2, AV3, AV4, AV5, AV6.
- OUT OF SCOPE: AV7.
No route produced a counterexample to the reduction theorem; the two defects
found are the O1a operator presentation gap and the O1b sign error.
