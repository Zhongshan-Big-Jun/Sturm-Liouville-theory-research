# Independent audit packet W3-AUDIT

- `subtask_id`: `AUDIT-W3-MASS-SLOPE-01`.
- `reviewer_role`: fresh independent mathematics auditor.
- `author_exclusion`: the reviewer did not author the coordinator or W3
  artifacts.

## Exact audit target

Audit every strict identity and sign claim in
`route-03-phi-exact/coordinator_direct.md` and
`route-03-phi-exact/worker_result.md`, with emphasis on:

1. the safe spectral elimination and `Phi<0 iff Xi>0`;
2. the Lagrange-identity signs, scale derivatives, and factors in `(M3)` and
   `(M2)`;
3. equivalence of the original exact mass equation and `(M-slope)`;
4. `K-id`, `K<0`, and `Xi=X^2G-rKDtheta`;
5. every denominator, modal-domain, and boundary assertion;
6. whether `G>=0` is described only as sufficient and not as an equivalent
   reduction.

## Inputs

All paths are relative to
`research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/`.

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA-256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/coordinator_direct.md`, SHA-256
  `de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3`.
- `route-03-phi-exact/worker_result.md`, SHA-256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.

## Audit method

- Treat the package as a first-time proof.
- Re-derive the formulas rather than trusting the author's prose.
- Exact symbolic differentiation or algebraic replay is allowed and should be
  recorded. Floating-point agreement is corroboration only.
- Seek the first erroneous step and classify it as statement, proof,
  dependency, or boundary-convention.
- A `PASS` requires zero critical errors and zero gaps in the strict partial
  claims. `PHI-SIGN` and KP-DET are explicitly outside the claimed closure.
- If a defect is local, identify the smallest correction. Do not repair or
  rewrite the author artifacts.

## Deliverables

Write only:

- `route-03-phi-exact/audit/independent_audit.json`;
- `route-03-phi-exact/audit/independent_audit.md`.

The JSON must contain `verdict`, `critical_errors`, `gaps`, `repair_hints`,
`covered_scope`, `residual_risk`, `reviewer_id`, `reviewed_artifacts`, and
`decision_delta`. Allowed verdicts are `PASS`, `REPAIRABLE_GAP`, `FATAL_GAP`,
`WRONG_PROBLEM`, `CIRCULAR_OR_EQUIVALENT_REDUCTION`, and `UNCERTAIN`.

Return raw JSON without a Markdown fence containing `subtask_id`, `verdict`,
both artifact paths and SHA-256 hashes, the first error, and `decision_delta`.

## Budget

One audit-model response in checkpoint sequence 05. Use the full response on
independent derivation and exact checking. Do not spawn sub-agents. Stop after
writing the two audit artifacts.
