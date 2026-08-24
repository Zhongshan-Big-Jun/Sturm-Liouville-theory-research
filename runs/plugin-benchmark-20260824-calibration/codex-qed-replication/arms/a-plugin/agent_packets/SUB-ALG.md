# Subtask packet - SUB-ALG

- Subtask ID: `SUB-ALG`
- Parent obligation / route: `O1`, Route A
- Spawned at: 2026-08-24
- Budget: one concentrated proof-search turn; return strongest exact result if incomplete.

## Claim

For every integer `n>=1` and every real `s>1`, derive and justify an exact polynomial extension of `Q_{n,s}(x)=G_{n,s}(arccos x)/sqrt(1-x^2)`, including its exact degree, and reduce the root problem to a scalar polynomial family. Pursue a complete exact root proof if your mechanism yields one.

## Inputs (by path and hash)

- `problem_contract.md` (sha256: `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`)
- `obligation_graph.md` (sha256: `eb2d9efa1212101734d22e6e9d80f9cd6b76119e02b9a1551dfe9bf3732fffbd`)

## Context slice (allowed dependencies)

Only the frozen definitions and constraints transcribed in the two input files. You may derive elementary algebra, Cayley-Hamilton recurrences, or explicitly defined orthogonal-polynomial identities. No external source or unproved recollection may be used.

## Deliverable

- Return artifact: `subagents/SUB-ALG.md`.
- Allowed status labels: `PROVED | PARTIAL | BLOCKED | REFUTED`.
- Exact gap to report: first formula, root-location, degree, or simplicity step not proved.

## Constraints

- Do not claim global completion.
- Do not mutate shared artifacts; write only `subagents/SUB-ALG.md`.
- Do not inspect any other repository file, Git history, internet source, memory, or prior solution. Do not read outside the current directory.
- Do not fabricate run data or citations.
- All numerical/symbolic experimentation is only for falsification; the delivered mathematics must be exact.

## Return format

Return raw JSON with keys `subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `claim_tested`, `exact_gap`, `failure_mechanism`, `evidence`.
