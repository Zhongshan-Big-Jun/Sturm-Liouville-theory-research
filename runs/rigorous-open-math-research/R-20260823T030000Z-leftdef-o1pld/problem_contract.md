# Problem Contract — O1'LD run R-20260823T030000Z-leftdef-o1pld

Run root: runs/rigorous-open-math-research/R-20260823T030000Z-leftdef-o1pld
Task packet: agenda/task-packets/Q-20260823-leftdef-o1pld-D4E5F6A7.md
Status label of this run: RIGOROUS_PARTIAL_RESULT

## Objects and definitions
- H^s = D(K_c^{s/2}) on L^2(-1,1), K_c f = -f'' + cf, c > 0, Krein BC.
- Sparse family p_0 = 1, p_1 = x, p_{2m} = x^{2m} - m/(m-1)x^{2m-2},
  p_{2m+1} = x^{2m+1} - m/(m-1)x^{2m-1} (m >= 2).  Index set D = {0,1} ∪ {4,5,...}.
- For s = 2, the isometry K_c : H^2 -> L^2 gives q_n = K_c p_n.
- For s = 3, K_c : H^3 -> H^1.
- V is a closed subspace of H^s (proper unless stated); W = K_c V in the
  descended space; N = {n ∈ D : p_n ∈ V} = {n ∈ D : q_n ∈ K_c V}.

## Hypotheses
- s ∈ {1,2,3} (or the descended H^{s'} = L^2/H^1).
- The problem is the open core O1'LD inherited from the left-definite density run.
- No assumption that V is finite-codimension is made unless explicitly stated.

## Target conclusion
A general criterion for closure(span Q_sp) = V would settle O1'LD.  This run
does not settle it; it proves new structural theorems and one concrete new
density/non-density example, and identifies the exact remaining obstruction.

## Quantifiers
- c > 0 fixed; s = 2 or 3; V arbitrary closed; all constants depend on c, s, V.

## Equivalent formulations
- (Master) closure(span Q_sp) = V iff V ∩ (span Q_sp)^\perp = {0}.
- For s = 2, closure(span Q_sp) = V iff closure(span{q_n : q_n ∈ W}) = W.
- Parity split: closure(span Q_sp) = closure(span even kept) ⊕ closure(span odd kept).

## Boundary and degenerate cases
- V = {0}: trivial.
- V = H^s: prior whole-space L1' gives density.
- V parity-invariant: Corollary 7 reduces to two parity problems.
- N cofinite: Corollary 6 would force V = H^2 for s = 2 if Theorem 5 becomes STRICT; currently NOT-YET-STRICT.

## Permitted outcomes
- New STRICT criterion/reduction for a broad subclass.
- Concrete non-density class.
- Falsification of a natural finite-data criterion (partial: the cofinite-N
  criterion is shown impossible for proper H^2 subspaces).
- Honest RIGOROUS_PARTIAL_RESULT with exact remaining gaps.

## Completion criteria
This run does not meet the general completion criteria for O1'LD.  It meets
the subcriteria:
1. Prove the L^2 finite-support moment rigidity (Lemma 1/Corollary 2). [MET]
2. Prove the cofinite-N density theorem for s = 2 (Theorem 5/Corollary 6). [NOT-YET-STRICT, conditional on Claim 4]
3. Prove the parity decomposition (Theorem 6/Corollary 7). [MET]
4. Prove a concrete non-density class (Theorem 8). [MET]
5. State honest remaining core for s = 2 and s = 3. [MET]

## Results that do not count as completion
- Claiming O1'LD solved.
- Claiming the H_beta/H_lambda finite-rank criterion transfers to L^2/H^1.
- Presenting the H^1 finite-support numerical residual as a proof.

## Forbidden moves
- Numerical evidence as proof.
- Silent transfer of banded/diagonal O1' criteria to L^2/H^1.
- Claiming s = 3 finite-run realizability without proof.

## Tool, citation, and search constraints
- Exact arithmetic via sympy (Python3) for the μ_4 example; numerical residual
  for H^1 is labeled EVIDENCE only.
- No git commit/push in this run.
- Müntz-Szász theorem cited as a standard classical theorem for finite-deletion
  monomials.

## Ambiguities
- H^1 finite-support moment sequences: numerical evidence suggests non-total
  monomials after a finite gap; this is left open/not proved.
