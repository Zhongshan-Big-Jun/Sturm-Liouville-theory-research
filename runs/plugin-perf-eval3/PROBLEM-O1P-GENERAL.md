# Round 3 benchmark problem: DensBC O1' general non-diagonal H

Project: Sturm-Liouville spectral optimization (MRP-20260731-BVE-SL)
Local root: F:\LaTeX\BVE research

## Why this is a good third-round benchmark

This is a different hard open problem from A6 / B3. It is an open reduced
core in the boundary-constrained polynomial density line, with several prior
STRICT sub-results (H_beta diagonal family, H_lambda banded family), a rich
tool library, and a clear general obstacle. It tests reuse because a good
agent should build on the prior subclass results instead of re-deriving them.

## Problem statement (O1')

Let H be a Hilbert space whose monomials Pi = span{x^k : k >= 0} are dense and
whose moment functionals M_k(w) = <w, x^k>_H are well defined.  For finite r,
let v_1, ..., v_r in H define

    V = { w in H : <w, v_j>_H = 0 for all j = 1..r }.

The sparse family is

    p_0 = 1,  p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},   m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.

Let N = { n : p_n in V } and Q_sp = { p_n : n in N }.

Reduced core O1': decide, from the run structure determined by N and the
membership data, whether closure(span Q_sp) = V.

Known prior progress:
- Diagonal H_beta + finite polynomial constraints: CLOSED
  (R-20260816T210000Z-densbc-o1p), criterion `dense <=> ker(T|B_adm) = {0}`.
- Banded H_lambda (bandwidth 1) + finite polynomial representers: CLOSED
  (R-20260816T220000Z-densbc-o1p2), criterion `dense <=> ker(T|B_fin) = {0}`,
  with explicit non-density for v_1 = x^4.
- General O1', general banded H, and general non-diagonal H remain OPEN.

## Open target for this round

Make a rigorous advance beyond the closed subclasses. Examples of acceptable
outcomes:

- an exact criterion or strict decision for a new concrete non-diagonal H
  (e.g. infinite-band, weighted l^2, finite-rank perturbation, or a new
  banded family with bandwidth >= 2);
- a new structure theorem showing where the H_beta / H_lambda criteria break;
- a general reduction or obstruction that narrows general O1' further;
- a decisive counterexample to a natural general criterion.

Honest partial progress is a success. Do not claim O1' is solved unless the
general criterion is actually proved.

## Required project context to read

- `runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`
- `runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/candidate_proof.md`
- `runs/rigorous-open-math-research/R-20260816T220000Z-densbc-o1p2/candidate_proof.md`
- `agenda/task-packets/Q-20260816-densbc-o1p2-F1A2B3C4.md`
- `research_map.md`
- `tools/README.md` and tools `constrained-denseness-runs`, `run-free-base`,
  `denseness-criteria`, `moment-jump-completeness`
- `lean-proof/LEMMA_INDEX.md`
- relevant scripts under `scripts/` from the DensBC runs

## Output requirements

Write standard rigorous-open-math-research artifacts in the run root:
`problem_contract.md`, `status_and_literature.md`, `approach_registry.md`,
`research_ledger.md`, `obligation_graph.md`, `candidate_proof.md`,
`escalation_ladder.md`, `audit_report.md` (or an explicit audit note),
`performance_log.md`, `final_report.md`. If you stop at a resource boundary,
also write `handoff-interrupted-<UTC>.md`.

Status labels must follow the rigorous-open-math-research output protocol.
Numerical evidence must never be presented as proof.
