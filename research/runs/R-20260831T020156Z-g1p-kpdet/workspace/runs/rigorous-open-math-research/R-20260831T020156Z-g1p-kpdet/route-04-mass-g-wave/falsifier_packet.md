# W5 exact falsifier packet

## Contract

- Subtask ID: `W5-G-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work only on the frozen finite-interior, symmetric, `n=2` INF half-string.
- Numerical observations are `EVIDENCE` only and cannot refute a universal
  statement without an exact admissible certificate.
- Write only `route-04-mass-g-wave/falsifier_result.md` and optional files
  under `route-04-mass-g-wave/falsifier/`.
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

Adversarially test the sufficient subroute

```text
G=Dtheta(D-c s N/C)+X Ttheta^2/C^2>=0
```

under the complete spectral, band, modal-domain, and exact mass-slope system.
Seek, in decreasing order of value:

1. An exact admissible certificate with `G<0`, even if `Xi>0` remains true.
2. An exact boundary or asymptotic argument proving that `G>=0` cannot be the
   correct global sublemma.
3. A rigorous restricted-region sign theorem or a proof that a proposed
   elementary sign shortcut fails.
4. A numerical candidate isolated with intervals and a precise list of
   missing certification obligations, labeled only `EVIDENCE`.

Also compute the sign of `Xi=X^2G-rKDtheta` for any candidate. A counterexample
to `G>=0` is not a counterexample to `PHI-SIGN`; preserve that distinction.
Do not repeat the W1 reduction, W2 quotient route, or W3 derivation. Audit all
branch constraints and denominators.

## Required return

The first line of `falsifier_result.md` must be one of `REFUTED_SUBROUTE`,
`PARTIAL`, `EVIDENCE`, or `NO_GAIN`. State the exact finding, admissibility
audit, proof or certification gap, and whether `PHI-SIGN` changed. End with a
single `decision_delta:` line. In the final response return JSON containing
`subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `exact_gap`,
`failure_mechanism`, and `decision_delta`.
