# Subtask packet - SUB-OSC

- Subtask ID: `SUB-OSC`
- Parent obligation / route: `O2`, Route B
- Spawned at: 2026-08-24
- Budget: one concentrated proof-search turn; return strongest exact result if incomplete.

## Claim

For every integer `n>=1` and every real `s>1`, find an independent exact oscillation, phase, or Sturm-style proof that `G_{n,s}` has exactly `2n` simple zeros in `(0,pi)`, or isolate the smallest scalar root lemma needed. Audit interval endpoints and multiplicities explicitly.

## Inputs (by path and hash)

- `problem_contract.md` (sha256: `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`)
- `obligation_graph.md` (sha256: `eb2d9efa1212101734d22e6e9d80f9cd6b76119e02b9a1551dfe9bf3732fffbd`)

## Context slice (allowed dependencies)

Only the frozen definitions and constraints in the two input files. Prefer a mechanism distinct from the matrix/Cayley-Hamilton route: Prüfer angle, exact sign bracketing, Sturm oscillation proved in the special finite setting, or another direct oscillation argument. State every theorem used with hypotheses, or prove it.

## Deliverable

- Return artifact: `subagents/SUB-OSC.md`.
- Allowed status labels: `PROVED | PARTIAL | BLOCKED | REFUTED`.
- Exact gap to report: first unproved counting, location, or simplicity obligation.

## Constraints

- Do not claim global completion.
- Do not mutate shared artifacts; write only `subagents/SUB-OSC.md`.
- Do not inspect any other repository file, Git history, internet source, memory, or prior solution. Do not read outside the current directory.
- Do not fabricate run data or citations.
- Finite scans are not proof.

## Return format

Return raw JSON with keys `subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `claim_tested`, `exact_gap`, `failure_mechanism`, `evidence`.
