# Task packet Q-20260823-leftdef-o1pld-D4E5F6A7 (左定空间稠密性一般判据 O1'LD)

- Task ID: Q-20260823-leftdef-o1pld-D4E5F6A7
- Project ID: MRP-20260731-BVE-SL
- Created: 2026-08-23
- Task type: solve
- Portfolio problem: A3/A4 (O1'LD)
- Mode: PROGRAM_AND_DELEGATE
- Run root: runs/rigorous-open-math-research/R-20260823T030000Z-leftdef-o1pld

## Project reason

The left-definite density run R-20260816T120000Z-leftdef-density established
STRICT structural facts L1-L6 and reduced the remaining general density
criterion to the open core O1'LD: for a general proper closed subspace V of
H^s (s in {1,2,3}, or surviving candidates for s>=4), decide whether
closure(span{p_n in V}) = V. This task attacks that core.

## Authoritative sources

- `runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/problem_contract.md`
- `.../candidate_proof.md` (L1-L6)
- `.../status_and_literature.md`
- `.../final_report.md`
- `runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`
  (Theorems 1-5, reduced core O1')
- `runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/candidate_proof.md`
  (H_beta criterion)
- `runs/rigorous-open-math-research/R-20260816T220000Z-densbc-o1p2/candidate_proof.md`
  (H_lambda criterion)
- `docs/SL_h2_completeness_proof.tex`, `docs/SL_h3_completeness_proof.tex`,
  `docs/SL_denseness_criteria.tex`, `docs/SL_hs_orthogonal_systems_proof.tex`
- `research_map.md`
- `tools/README.md`, `tools/constrained-denseness-runs.md`,
  `tools/left-definite-moment-recurrence.md`, `tools/moment-jump-completeness.md`
- `lean-proof/LEMMA_INDEX.md`

## Problem statement (O1'LD)

Let H^s = D(K_c^{s/2}) (Krein BC, c>0), s in {1,2,3} (or surviving candidates
for s>=4), and let V be a closed proper subspace defined by bounded constraint
functionals. Let {p_n} be the sparse gapped family and Q_sp = {p_n in V}.
Determine, with exact verifiable conditions, when

    closure(span Q_sp) = V.

The latest run reduced this to a moment/membership problem in the descended
space H^{s'} (s' in {0,1}) via the transfer descent L3. The core is whether
the general proper-V moment/membership problem is decidable by finite data or
what exact obstruction captures it.

## Allowed outcomes

- New STRICT criterion or decisive reduction for a broad subclass of V.
- Concrete non-trivial V class with exact density/non-density decision.
- Falsification of a natural finite-data criterion.
- A new structural theorem that narrows O1'LD.
- If no closure, an honest RIGOROUS_PARTIAL_RESULT with exact remaining gaps.

## Novelty preflight

Inherited from R-20260816T120000Z-leftdef-density: no published exact
constrained-density criterion for this left-definite class surfaced;
POTENTIALLY_NEW. The target O1'LD is open.

## Output requirements

Write standard rigorous-open-math-research artifacts under the run root:
`problem_contract.md`, `status_and_literature.md`, `approach_registry.md`,
`research_ledger.md`, `obligation_graph.md`, `candidate_proof.md`,
`escalation_ladder.md`, `audit_report.md` (or explicit audit note),
`performance_log.md`, `reuse_summary.md`, `final_report.md`, and Lean scaffold
if a new STRICT/partial result is produced.
