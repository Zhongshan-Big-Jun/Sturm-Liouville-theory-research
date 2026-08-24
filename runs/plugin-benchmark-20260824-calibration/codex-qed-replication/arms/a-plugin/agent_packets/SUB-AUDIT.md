# Subtask packet - SUB-AUDIT

- Subtask ID: `SUB-AUDIT`
- Parent obligation / route: `O5`
- Spawned at: 2026-08-24 after candidate freeze
- Budget: one fresh first-time verifier pass; return the earliest error and all gaps if non-PASS.

## Claim

Audit the frozen candidate proof against the exact contract: for every integer `n>=1` and `s>1`, `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, all simple, with the polynomial extension, exact degree, root location/simplicity, and separate audits required by the contract.

## Inputs (by path and hash)

- `problem_contract.md` (sha256: `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`)
- `candidate_proof.md` (sha256: `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6`)

## Context slice (allowed dependencies)

Read only the two hash-bound files. Treat the candidate as a first-time submission and do not rely on your earlier route or any conversational memory. Recompute every load-bearing identity. Check semantic fidelity, logic, quantifiers, endpoint conventions, `n=1`, `y=0`, `y=pi`, `y=pi/2`, `s=1`, degree, root intervals, exhaustiveness, and every derivative-based simplicity implication.

## Deliverable

- Return artifact: `subagents/SUB-AUDIT.md`.
- Allowed verdicts: `PASS | REPAIRABLE_GAP | FATAL_GAP | WRONG_PROBLEM | CIRCULAR_OR_EQUIVALENT_REDUCTION | COMPUTATIONAL_ONLY | UNCERTAIN`.
- For any non-PASS verdict, localize the first erroneous step, classify its layer, list all critical errors/gaps, and give nonempty repair hints.
- For PASS, critical errors and gaps must both be empty; state covered scope and residual risk.

## Constraints

- Do not mutate the candidate or shared artifacts; write only `subagents/SUB-AUDIT.md`.
- Do not inspect any other repository file, Git history, internet source, memory, prior solution, or earlier subagent artifact. Do not read outside the current directory.
- Do not fabricate citations or run data.
- An argument-style objection may identify a gap, but a refutation requires a concrete contradiction/counterexample or impossible-precondition audit.

## Return format

Return raw JSON with keys `subtask_id`, `verdict`, `artifact_path`, `artifact_sha256`, `critical_errors`, `gaps`, `repair_hints`, `covered_scope`, `residual_risk`, and `first_error`.
