# Problem Contract: DensBC O1 — general non-diagonal H low-moment-survival criterion

Run root: runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/
Task packet: agenda/task-packets/Q-20260816-densbc-o1-A1B2C3D4.md
Upstream: R-20260814T070000Z-densbc-3F8A2C (status RIGOROUS_PARTIAL_RESULT; O1 open)

## Objects and definitions

- H: Hilbert space over C whose underlying vector space contains all polynomials
  Pi, with inner product <.,.>_H.  (H1): Pi is dense in H.  (H2): moments
  M_k(w) = <w, x^k>_H are well defined (automatic by Cauchy-Schwarz when x^k in H).
- Sparse (project adapted) family: p_0 = 1, p_1 = x,
  p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},  p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}
  (m >= 2); index set {0,1} union {4,5,...} (degrees 2,3 are absent).
  {p_n} is a triangular basis of Pi: span{p_n} = Pi.
- FORM (a): V = Intersection_{j=1..r} ker L_j, L_j nonzero bounded independent
  linear functionals.  W := V^\perp = span{v_1,...,v_r}, v_j = Riesz representer
  of L_j, dim W = r < inf.
- Candidate family: Q_sp = { p_n : p_n in V }, kept sparse family.  Let
  N = { n : p_n in V } = { n : <v_j,p_n>_H = 0 for all j }.  Q_sp = {p_n : n in N}.
- Representer moments: a^{(j)}_k = <v_j, x^k>_H (well defined by H2).
  Then p_n in V  <=>  sum_{k in support(p_n)} coeff_k a^{(j)}_k = 0 for all j.
- Orthogonal projection P_V : H -> V.

## Hypotheses

- (H1) all polynomials in H and dense in H.
- (H2) moments well defined (automatic).
- FORM (a) is in force (closed, codimension r < inf, W = span{v_1..v_r}).
- No assumption that Q_sp is dense in V; that is exactly the question.
- The packet is treated as project context, NOT as a verified theorem contract.
  Upstream Theorems A-H (esp. Theorem E diagonal classification) are audited and
  may be built on; they are not copied.

## Target conclusion

Give an exact, verifiable criterion
    closure(span Q_sp) = V
in terms of the interaction between the constraint functionals L_j (equiv. the
Riesz representers v_j and their moments a^{(j)}_k = <v_j,x^k>_H) and the
recursion/run structure of {p_n}, when the L_j are NOT coordinate projections.

A satisfactory answer must:
1. Express V cap Q_sp^\perp as the solution space of a finite/structured linear
   system in the moment variables M_k = <w,x^k>_H.
2. Characterize when that solution space is trivial, reducing to the diagonal
   Theorem E when L_j are coordinate projections.
3. Identify the first obstruction (which low moments survive) in the
   non-diagonal case.

## Quantifiers and dependency of constants

- r = codim V fixed and finite; all constants may depend on H, V, the v_j, and
  the moment data.
- N, the run structure and the free run-bases are determined by the representer
  moment sequences {a^{(j)}_k}.  Bounds/growth of x^k are not assumed beyond H2.

## Equivalent formulations that are actually proved equivalent

- (Master, upstream Theorem A, audited STRICT) closure(span Q_sp) = V  <=>  V cap
  Q_sp^\perp = {0}.
- (Projection reformulation, THIS run Theorem 1, STRICT) P_V(Pi) is dense in V
  for every closed V; hence closure(span Q_sp) = V  <=>  the excluded projections
  {P_V(p_n) : p_n notin V} are redundant relative to {P_V(p_n): p_n in V} = Q_sp.
- (Obstruction system, THIS run Theorem 2, STRICT) V cap Q_sp^\perp =
  { w in H : <w,v_j>_H = 0 for all j, and <w,p_n>_H = 0 for all n in N }, with
  <w,p_n>_H a fixed linear combination of M_0, M_1, M_n, M_{n-2}.

## Boundary and degenerate cases

- r = 0 (V = H): Q_sp = all p_n; density is the project's whole-space problem
  (regression to Theorem 11 / Theorem E with empty R).  STRICT fallback.
- N empty (generic non-coordinate): Q_sp = empty, closure = {0}; density fails
  unless V = {0}.  Identified by Proposition (this run).
- V = {0}: trivial closure(span Q_sp) = {0} = V.
- Coordinate projections (diagonal H_beta): the criterion must reduce to
  Theorem E (beta <= 3/2 AND no finite run).

## Permitted outcomes

- affirmative proof of the exact criterion in an identified class;
- an exact structured criterion + honest reduced core (moment-problem step);
- a negative/structure result (e.g. criterion is NOT purely finite-rank in
  general);
- precise reduction with a strictly smaller unresolved core.

## Completion criteria

1. Exact statement of V cap Q_sp^\perp as a structured linear system in M_k,
   with N and the run/free-base structure derived from {a^{(j)}_k}.  [MET by
   Theorems 1-3, STRICT]
2. Triviality characterization that reduces to Theorem E in the diagonal case.
   [MET by Theorem 4, STRICT]
3. First-obstruction (lowest surviving free base) identified.  [MET by
   Theorem 3(iv), STRICT]
4. Honest statement of what is still a moment problem (the realizability /
   membership step), including whether the criterion is finite-rank.
   [MET by Theorem 5 + reduced core O1', STRICT]

## Answer space

The deliverable must support a decision: given H, V (via v_j) and the sparse
family, decide density; and it must give the first obstruction.  It must be
honest that the numeric/representability check does not close a proof obligation.

## Acceptance criteria per subproblem

- Projection density theorem: proven STRICT and numerically corroborated
  (EVIDENCE) at finite truncation.
- Diagonal reduction: exact statement + proof that the general instantiation
  equals Theorem E.
- First obstruction: exact degree/minimality characterization.

## Results that do not count as completion

- Numerical verification of a candidate criterion (EVIDENCE only).
- Claiming a purely finite-rank closed form when representers are general
  (false: requires infinite moment data).
- Claiming the realizability/membership step is trivial (it is a moment problem).

## Forbidden moves (per-problem discipline)

- Numerical evidence presented as proof.
- Silent quantifier/domain changes.
- Claiming "solved" while any obligation (esp. the realization step) is open.
- Presenting the packet's framing as verified without re-audit.

## Tool, citation, and search constraints

- Python C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe,
  PYTHONUTF8=1; numpy/scipy/sympy (EVIDENCE only).
- No git commit or push (manager performs git sync at stage close; per user
  instruction this run does NOT commit).
- Novelty claims require a status-or-literature note with fetch status.

## Ambiguities or competing interpretations

- Whether O1 admits a purely finite-rank criterion: RESOLVED (Theorem 5) —
  in general it does NOT; it requires the representer-moment data and a genuine
  moment representability/membership step.  It IS finite/structured when the
  membership equations are finite moment equations AND the moment matrix has
  banded/diagonal structure (so the kept set N is finitely determined), e.g. the
  diagonal case.  (Audit-corrected: polynomial representers ALONE do not make it
  finite in a general H.)
- The kept/free "run" notion carries over verbatim from the diagonal analysis
  because the kept recursions are the same in any H (linearity of moments); only
  the realization step changes.  This is the exact resolution of the packet's
  item-2 ambiguity.

## Contract audit

- Contract built from: task packet Q-20260816-densbc-o1-A1B2C3D4, upstream
  candidate_proof.md / audit_report.md / run-manifest.json (Theorems A-H,
  Theorem E, F-densbc-01), tools/denseness-criteria.md,
  tools/constrained-denseness-runs.md, docs/SL_denseness_criteria.tex (context).
- No verbatim theorem copied; upstream audited results cited by run/name.
- Numerical evidence labeled EVIDENCE, never STRICT.
