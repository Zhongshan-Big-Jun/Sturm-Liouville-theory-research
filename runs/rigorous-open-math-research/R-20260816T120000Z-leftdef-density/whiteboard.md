# Run whiteboard (Planner memory)

- **Run ID:** `R-20260816T120000Z-leftdef-density`
- **Task packet ID:** `Q-20260816-leftdef-density-E5F6A7B8`
- **Upstream status (verbatim):** `RIGOROUS_PARTIAL_RESULT`
- **This-run status:** `RIGOROUS_PARTIAL_RESULT`
- **Last updated:** `2026-08-16T17:45:00Z`

## Current plan

Run is closed with `RIGOROUS_PARTIAL_RESULT`.  STRICT structural theorems
L1-L6 for left-definite constrained density are produced; an independent
adversarial audit returned `REPAIRABLE_GAP` and the solver applied repairs.
The repaired changed points still need an independent re-check.  The reduced
open core is `O1'LD` (realization/membership moment problem for general proper
`V ⊂ H^s`).

## Route history

- Whole-space recovery (V=H^s) `[SUCCEEDED]`: L1, all integer s>=1.
- Structural projection density `[SUCCEEDED]`: L2.
- Transfer descent `[SUCCEEDED]`: L3 core; remark corrected after audit.
- Proper V characterization `[SUCCEEDED]`: L4.
- Concrete non-density instance `[SUCCEEDED]`: L5 (V=ker Δ in H^2).
- O1' status `[PARTIAL]`: L6 decided for V=H^s, open for general proper V (O1'LD).
- Independent adversarial audit `[PARTIAL]`: REPAIRABLE_GAP; repairs applied,
  independent re-check still pending.

## Ideas to return to

- Re-run an independent verifier on the repaired changed points (L1 proof,
  L3 remark, L6(3)).
- Attack `O1'LD` via H^1/L^2 moment-matrix structure.
- Investigate whether the parity/boundary obstruction mechanism (L5) extends
  to other natural functionals.

## Open obligations

- `O1'LD`: decide whether a free jump-base moment sequence is realized by a
  nonzero element of the descended constraint `K_c^r V` in `H^{s'}` (`s' ∈ {0,1}`).
- `O2'` (inherited): constraints guaranteeing density for all c.
- `O3` (inherited): fractional window `3/2 ≤ s < 2`.

## Key artifacts

- `runs/.../candidate_proof.md` -- Theorems L1-L6 (repaired).
- `runs/.../audit_report.md` -- independent audit REPAIRABLE_GAP + repairs.
- `runs/.../final_report.md` -- run final report.
- `runs/.../problem_contract.md` -- normalized contract.
- `runs/.../repro_manifest.md` -- input/env/hash manifest.
- `runs/.../reproducibility/ld_struct_facts.py` -- EVIDENCE structural facts.
- `runs/.../reproducibility/ld_counterexample.py` -- EVIDENCE L5 counterexample.
