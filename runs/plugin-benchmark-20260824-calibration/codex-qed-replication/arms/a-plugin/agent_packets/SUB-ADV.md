# Subtask packet - SUB-ADV

- Subtask ID: `SUB-ADV`
- Parent obligation / route: `O4`, Route C, later `O5`
- Spawned at: 2026-08-24
- Budget: one concentrated adversarial/counterexample turn, then availability for a fresh proof audit.

## Claim

Attack literally the universal statement: for every integer `n>=1` and every real `s>1`, `G_{n,s}` has exactly `2n` simple zeros in `(0,pi)`. Search exact boundary, low-degree, critical-point, and repeated-root failures. Audit `n=1`, `y=0`, `y=pi`, `y=pi/2`, and `s=1` separately. If no counterexample is found, report only exact derived constraints, not universal truth.

## Inputs (by path and hash)

- `problem_contract.md` (sha256: `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`)
- `obligation_graph.md` (sha256: `eb2d9efa1212101734d22e6e9d80f9cd6b76119e02b9a1551dfe9bf3732fffbd`)

## Context slice (allowed dependencies)

Only the frozen definitions and constraints in the two input files. Exact symbolic computation is allowed for falsification. Test potential proof lemmas for missing intervals, endpoint contamination, a root at a quadratic-substitution vertex, and parameter values causing repeated roots.

## Deliverable

- Return artifact: `subagents/SUB-ADV.md`.
- Allowed status labels: `FALSIFIED | NONE_FOUND | PARTIAL | BLOCKED`.
- Exact gap to report: tested domain and first untested general obligation.

## Constraints

- Do not claim global completion.
- Do not mutate shared artifacts; write only `subagents/SUB-ADV.md`.
- Do not inspect any other repository file, Git history, internet source, memory, or prior solution. Do not read outside the current directory.
- Do not fabricate run data or citations.
- Absence of a counterexample is not a proof.

## Return format

Return raw JSON with keys `subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `claim_tested`, `exact_gap`, `failure_mechanism`, `evidence`.
