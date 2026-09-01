# W4 exact prover packet

## Contract

- Subtask ID: `W4-MASS-G-PROVER`.
- One model response. Do not spawn subagents.
- Work only on the frozen finite-interior, symmetric, `n=2` INF half-string.
- Numerical observations are `EVIDENCE` only and cannot prove a sign.
- Write only `route-04-mass-g-wave/prover_result.md` and optional files under
  `route-04-mass-g-wave/prover/`.
- Do not edit shared ledgers, checkpoints, candidate proofs, Blueprint files,
  Lean files, or repository indexes.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/coordinator_direct.md`, SHA256
  `de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3`.
- `route-03-phi-exact/worker_result.md`, SHA256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-03-phi-exact/audit/independent_audit.json`, SHA256
  `3bace4993b5a14c55950043322dd410e65f7f0135df5e03c95dde18a5ad6b3dd`.

## Exact task

Starting from the audited identities

```text
C E2(F2)/sin(c alpha)+c^3 s E3(F3)/sin(alpha)=0,
K=X[c cot(c alpha)-cot(alpha)]<0,
G=Dtheta(D-c s N/C)+X Ttheta^2/C^2,
Xi=X^2 G-r K Dtheta,
```

prove one of the following, in decreasing order of value:

1. `Xi>0` on the complete exact admissible phase system.
2. A sharp lower bound `G>r K Dtheta/X^2` on that system.
3. The sufficient inequality `G>=0` on that system.
4. A strictly smaller exact identity or inequality whose hypotheses and
   equality cases are fully audited and which advances one of items 1-3.

Preferred mechanisms are constrained spectral-slope differentiation,
Lagrange identities, or a denominator-safe sum-of-squares/factorization.
Do not repeat the W1 phase reduction, W2 quotient monotonicity, or W3
mass-slope derivation. Every division must have a strict sign audit. Do not
claim an implication from the mass-slope equation unless it is derived.

## Required return

The first line of `prover_result.md` must be one of `PROVED`, `PARTIAL`, or
`NO_GAIN`. State the exact theorem proved, assumptions, derivation, equality
and boundary audit, and first unresolved step. End with a single
`decision_delta:` line. In the final response return JSON containing
`subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `exact_gap`,
`failure_mechanism`, and `decision_delta`.
