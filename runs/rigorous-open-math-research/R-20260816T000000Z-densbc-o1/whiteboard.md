# Run whiteboard (Planner memory)

- **Run ID:** `R-20260816T000000Z-densbc-o1`
- **Task packet ID:** `Q-20260816-densbc-o1-A1B2C3D4`
- **Upstream status (verbatim):** `RIGOROUS_PARTIAL_RESULT`
- **This-run status:** `RIGOROUS_PARTIAL_RESULT`
- **Last updated:** `2026-08-16T16:50:00Z`

## Current plan

Run is closed with `RIGOROUS_PARTIAL_RESULT`.  New STRICT structure theorems for
DensBC O1 are produced and independently audited; the precise remaining core is
`O1'` (free run-base realization / moment representability + membership).  No
active solver plan; next step is either attack `O1'` or move to the
left-definite-space specialization.

## Route history

- Projection-density reformulation `[SUCCEEDED]`: Theorem 1, P_V(Pi) dense in V.
- Moment-system obstruction `[SUCCEEDED]`: Theorems 2-3; realization core O1' left open.
- Diagonal reduction `[SUCCEEDED]`: Theorem 4 reduces to upstream Theorem E.
- Finite-rank classification `[SUCCEEDED]`: Theorem 5 after audit repair (banded/diagonal condition).
- Generic-emptiness `[PARTIAL]`: Lemma 6.1 STRICT; Heuristic 6.2 EVIDENCE only.
- Fresh-agent independent audit `[SUCCEEDED]`: REPAIRABLE_GAP -> repaired and re-checked.

## Ideas to return to

- Attack `O1'` via moment-problem / membership feasibility for general non-diagonal H.
- Specialize the criterion to left-definite spaces `H^s` with structural boundary constraints.
- Investigate whether banded/diagonal-moment structure is the right sufficient condition for finiteness.

## Open obligations

- `O1'`: decide whether a free run-base admits a nonzero `w ∈ V` realizing the prescribed moments (moment representability + membership).
- `O2` (inherited): general `L_j` expansions killing free parameters in all beta.
- `O3` (inherited): fractional left-definite window `3/2 ≤ s < 2`.

## Key artifacts

- `runs/.../candidate_proof.md` -- Theorems 1-5, Lemma 6.1, Heuristic 6.2, O1'.
- `runs/.../audit_report.md` -- independent audit, REPAIRABLE_GAP repair record.
- `runs/.../problem_contract.md` -- normalized contract.
- `runs/.../repro_manifest.md` -- input/env/hash manifest.
- `runs/.../reproducibility/o1_projection_density.py` -- EVIDENCE scripts.
- `runs/.../reproducibility/o1_poly_rep_example.py` -- EVIDENCE scripts.
