# Whiteboard: DensBC O1' (round 2 - banded/non-diagonal extension)

- **Run ID:** `R-20260816T220000Z-densbc-o1p2`
- **Task packet ID:** `Q-20260816-densbc-o1p2-F1A2B3C4`

## Current plan

- Objective: concrete verifiable advance on O1' beyond the diagonal H_beta
  subclass.
- Selected route: banded non-diagonal Hilbert space H_lambda
  (x^k = e_k + lambda e_{k+1}, lambda in (-1,1)); exact finite-rank criterion;
  complete decision for v_1 = x^4.

## Route history

- `H_lambda finite-rank` `[SUCCEEDED]`: density iff ker(T|_{B_fin}) = {0};
  infinite runs inadmissible (moment sequences grow linearly, not l^2).
- `v_1 = x^4 decision` `[SUCCEEDED]`: density fails for all lambda in (-1,1);
  obstruction w = lambda^2 e_0 - lambda e_1 + e_2.
- `general banded-Gram O1'` `[PARTIAL]`: kept set cofinite and finite runs
  obtained; infinite-run realizability not finite in arbitrary banded H
  (H_lambda is the tractable case with an explicit l^2 isomorphism).
- `single-representer density search` `[FAILED]` (EVIDENCE only): no density-
  holding low-degree representer found in tried grids; not used in proof.

## Ideas to return to

- Exact realizability condition for infinite-run moment sequences in general
  banded H.
- Whether any single non-coordinate representer in H_lambda (or a small
  perturbation family) can make density hold.

## Open obligations

- O1' for general banded H: exact realizability condition for infinite run
  moment sequences.
- O1' for general non-diagonal H: full moment-representability + membership.
- General O1' remains open.

## Key artifacts

- problem_contract: runs/rigorous-open-math-research/R-20260816T220000Z-densbc-o1p2/problem_contract.md
- candidate_proof: runs/rigorous-open-math-research/R-20260816T220000Z-densbc-o1p2/candidate_proof.md
- audit_report: runs/rigorous-open-math-research/R-20260816T220000Z-densbc-o1p2/audit_report.md
- research_ledger / approach_registry / run-manifest.json in the same run dir
