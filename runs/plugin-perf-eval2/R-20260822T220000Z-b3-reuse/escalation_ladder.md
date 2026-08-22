# Escalation ladder

| Tier | Cost | What was tried | Outcome |
|------|------|----------------|---------|
| 0 | read-only | Pre-scan: required docs, tools, Lean index, op02 scripts | Done; baseline not initially discovered |
| 1 | cheap symbolic | Symbolic cell transfer matrix; trace/Chebyshev; phase lemma | STRICT R1 |
| 1 | cheap adaptation | Adapt gap exact-2n-switch proof to ratio functional | STRICT R2 |
| 2 | numerical | Numeric root count, alternating-family scan, self-consistency probes | EVIDENCE; found asymmetric self-consistent solution |
| 2 | reuse | Cross-check with baseline run artifacts | Confirms R1/R2 already present in baseline |
| 3 | hard | Attempt O2/O1 equal-width/uniqueness proof | OPEN; blocked by complexity of global finite-dimensional optimization |
| 3 | literature | Web search for fixed-n adjacent ratio supremum | No direct match found in first-pass search |

Current tier: Tier 2/3 boundary. The run produced two STRICT partial results
(also in baseline) and made no new progress beyond baseline on O1/O2.
