# Run whiteboard (Planner memory)

- **Run ID:** R-20260816T000000Z-densbc-o1
- **Task packet ID:** Q-20260816-densbc-o1-A1B2C3D4
- **Upstream status (verbatim):** RIGOROUS_PARTIAL_RESULT
- **This-run status:** RIGOROUS_PARTIAL_RESULT
- **Last updated:** 2026-08-16

## Core result

STRICT structure theorems for DensBC O1 (exact low-moment-survival criterion for
general non-diagonal H under FORM (a) constraints):
- Theorem 1 (projection density): P_V(Pi) dense in V for any closed V.
- Theorem 2 (obstruction system): V cap Q_sp^perp as a structured moment system.
- Theorem 3 (run lemma + first obstruction D*): kept recursions are H-independent;
  runs/free bases from kept set N; lowest surviving free base = first obstruction.
- Theorem 4 (diagonal reduction): criterion reduces exactly to upstream Theorem E.
- Theorem 5 (finite-rank structure): not purely finite-rank in general; finite
  under banded/diagonal-moment condition (not merely polynomial representers).
- Lemma 6.1 (STRICT): N empty => Q_sp empty => density fails unless V={0}.
  Heuristic 6.2 (genericity) = EVIDENCE, not STRICT.
- Reduced core O1' (honest, OPEN): the realizability/membership moment-problem step.

## Route history

- Projection-density reformulation [PROVED]: Theorem 1.
- Moment-system obstruction [PROVED]: Theorems 2-3 (realization core O1' OPEN).
- Diagonal reduction [PROVED]: Theorem 4.
- Finite-rank classification [PROVED]: Theorem 5 (audit-corrected).
- Generic-emptiness [PARTIAL]: Lemma 6.1 STRICT; Heuristic 6.2 EVIDENCE.
- Fresh-agent independent audit [DONE]: verdict REPAIRABLE_GAP -> repaired.

## Open obligations

- O1': decide free run-base realization (moment representability + membership).
- O2/O3 (inherited upstream): still open.

## Key artifacts (this run)

- candidate_proof.md, problem_contract.md, repro_manifest.md,
  status_and_literature.md, obligation_graph.md, approach_registry.md,
  research_ledger.md, counterexample_log.md, audit_report.md,
  reproducibility/o1_projection_density.py, reproducibility/o1_poly_rep_example.py.
- No git commit/push (per user instruction); manager owns run-manifest.json ingestion.
