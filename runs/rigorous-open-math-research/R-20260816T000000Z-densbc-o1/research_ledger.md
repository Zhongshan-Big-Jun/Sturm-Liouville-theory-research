# Research Ledger

Run: R-20260816T000000Z-densbc-o1
Task: Q-20260816-densbc-o1-A1B2C3D4

## Phase 0-1 (2026-08-16): normalize and audit the problem statement

- Loaded rigorous-open-math-research skill; read phase files 01/23/45/6/78/91011/12.
- Read task packet Q-20260816-densbc-o1-A1B2C3D4 (project context, not a theorem
  contract).  Normalized FORM (a): V = Intersection ker L_j, W = V^\perp =
  span{v_j}, kept set N = {n : p_n in V}, representer moments a^{(j)}_k =
  <v_j, x^k>_H.  Recorded in problem_contract.md.
- Audited the packet's three deliverable requirements (express obstruction space;
  reduce to diagonal Theorem E; identify first obstruction) and its known
  ambiguity (finite-rank vs moment-problem data).
- Upstream status captured verbatim: RIGOROUS_PARTIAL_RESULT (run-manifest.json).
- Git state recorded: HEAD c0ba1d9e5022d2e028d7c3204b81e1aba1ae74fa; tree very
  dirty (pre-existing); this run creates files only under its own run root and
  commits/pushes NOTHING (per user).

## Phase 2-3: literature + novelty

- R-O1-001: web search returned only whole-space / moment-problem material
  (Hausdorff moment problem; local moment problem arXiv:1311.0501; Pinkus Zbl
  1068.41011); no constrained-subspace criterion for general non-diagonal H
  found.  Novelty recorded as POTENTIALLY_NEW (fetch: general-web level; upstream
  novelty audit already recorded the same).  status_and_literature.md.
- Obligation graph written (N0-N7, O1'/O2/O3).

## Phase 4-5: routes

- Approach registry: 5 routes (projection reformulation, moment-system,
  diagonal reduction, finite-rank classification, generic-emptiness).

## Phase 6: computation (EVIDENCE only)

- R-O1-002 (o1_projection_density.py): H = L^2([-1,1]), V = {f: <e^x,f>=0,
  <1,f>=0}.  Kept set N = empty (both representers non-coordinate); runs collapse
  to isolated bases; projection-density rank check: rank(Gram{P_V x^k}) = 11 =
  dim V (D=12, r=2) => projected monomials span V (EVIDENCE corroborating
  Theorem 1).
- R-O1-003 (o1_poly_rep_example.py): H = L^2([-1,1]), V = {f: <x - 1/2 x^2,f>=0}
  (single polynomial non-coordinate representer).  Kept set N = empty; all runs
  isolated.  Confirms Proposition 6 generic-emptiness in a polynomial-representer
  case (EVIDENCE).
- These are EVIDENCE; they do NOT constitute the proofs (Theorems 1-6).

## Phase 7-8: synthesis + adversarial audit

- Synthesized candidate_proof.md: Theorems 1-5 + Proposition 6 (STRICT), reduced
  core O1'.  See candidate_proof.md.
- Adversarial audit: see audit_report.md.

## Decisions / stop

- Stop: STRICT structure theorems produced; the realizability/membership step is
  honestly OPEN (O1').  Numerical evidence does not close it.  This matches the
  upstream status RIGOROUS_PARTIAL_RESULT with a strictly reduced core.
