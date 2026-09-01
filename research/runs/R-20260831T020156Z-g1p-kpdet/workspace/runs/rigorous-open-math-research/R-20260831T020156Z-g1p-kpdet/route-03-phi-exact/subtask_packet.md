# Subtask packet W3-PHI-EXACT

- `subtask_id`: `W3-PHI-EXACT`.
- `obligation_id`: `PHI-SIGN`.
- `owner`: one independent exact-residual worker.

## Claim

On the exact finite-interior n=2 symmetric INF five-phase constraint set in
the frozen W1 derivation, prove

```text
Phi<0,
```

equivalently prove the coordinator's `Xi>0`, or construct a fully admissible
exact tuple satisfying every spectral, band, mass, mode-index, and interior
constraint together with `Phi=Xi=0`.

## Direct attempt and falsification probe

- Direct artifact:
  `route-03-phi-exact/coordinator_direct.md`.
- Direct artifact SHA-256:
  `de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3`.
- Result: safe lossless elimination `Phi<0 iff Xi>0` with no division by
  `cos(beta)` or `cos(c beta)`.
- Falsification result: the spectral and band equations alone do not dominate
  the remaining signed term. The exact mass identity is still load-bearing.

## Decision to change

Current closure decision: `ESCALATE` with one exact worker.

- Success: a self-contained exact proof of `Xi>0` on the complete admissible
  system.
- Refutation: a fully exact admissible equality or negative witness, with all
  constraints checked symbolically.
- Partial success: a strictly smaller exact inequality or monotone scalar
  residual whose proof would settle `PHI-SIGN` and which is not an equivalent
  renaming of `Phi` or `Xi`.
- Budget stop: return the strongest exact identities and the first unresolved
  load-bearing step. Do not replace it with numerical evidence.

## Inputs

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `candidate_proof.md`, SHA-256
  `e9305a8795b31cd528555108c5268b92664e63f48ab728592f2947336a050188`.
- `route-01-transfer-schur/derivation.md`, SHA-256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-02-jacobi-falsifier/derivation.md`, SHA-256
  `1e664a7742ea6a9e5674cc2499e7a47c6c4955309ed14d0b9e1e0b164f851f5d`.
- `route-03-phi-exact/coordinator_direct.md`, SHA-256
  `de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3`.

All paths are relative to
`research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/`.

## Context slice and constraints

- The audited P1-P4 package is trusted input for this subtask only.
- Work through exact transfer, trigonometric, mass, variational, or interval
  identities. Computation may falsify or discover but cannot prove the result
  without a universal certificate.
- Do not repeat the quotient-monotonicity route, which is already closed as a
  dead end.
- Do not claim global KP-DET, KO-DET, non-symmetric results, or G1 prime.
- Do not edit shared artifacts. Write only
  `route-03-phi-exact/worker_result.md` and optional files beneath
  `route-03-phi-exact/worker/`.
- Do not use conversation history or unlisted project files as proof premises.

## Deliverable

Write `route-03-phi-exact/worker_result.md` beginning with exactly one of
`PROVED`, `PARTIAL`, `BLOCKED`, or `REFUTED`. Include the exact derivation,
assumptions, denominator and boundary audit, the first unresolved step, and a
one-line `decision_delta`.

Return raw JSON without a Markdown fence containing `subtask_id`, `status`,
`artifact_path`, `artifact_sha256`, `exact_gap`, `failure_mechanism`, and
`decision_delta`.

## Budget

One research-model response in this checkpoint segment. Use the available
effort on this single mechanism. Do not launch sub-agents. Stop after writing
the deliverable.
