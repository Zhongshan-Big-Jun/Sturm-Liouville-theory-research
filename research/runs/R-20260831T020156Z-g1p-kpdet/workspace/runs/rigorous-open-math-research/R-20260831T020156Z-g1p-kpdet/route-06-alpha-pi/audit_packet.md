# Fresh joint audit packet for W8 and W9

## Contract

- Audit ID: `AUDIT-W8-W9-ALPHA-PI-01`.
- You did not author either endpoint result.
- Exactly one model response. Do not spawn subagents.
- Review both as first-time submissions and do not silently repair them.
- Write only `route-06-alpha-pi/audit/independent_audit.md` and
  `route-06-alpha-pi/audit/independent_audit.json`.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-04-mass-g-wave/repair/near_one_repair.md`, SHA256
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.
- `route-05-alpha-collision/accepted_package.md`, SHA256
  `49d1691a384a6b7d550d8b547dfc25de5daf14fd575d6018462417b04e7257ba`.
- `route-06-alpha-pi/prover_result.md`, SHA256
  `b0f66b3090280f946d2ec4d49df54eed942ae56913aa77d286e1ce8e028881cb`.
- `route-06-alpha-pi/falsifier_result.md`, SHA256
  `ece86c1ff05afa17a3fdb6f9bab94e31b69cbdf38190e2a6c1d1b77a10e5b514`.

Verify every hash.

## Mandatory checks

1. Verify switch-uniform spectral limits and both total-phase identities.
2. Check all transfer expansions and the undivided band equation used to
   force `theta->pi/2` and `beta->0`.
3. Check the first-order limits for `X`, `C`, `theta`, and W8's optional
   `beta/(pi-alpha)->2` claim.
4. Remove both norm singularities independently and recompute
   `I3hat->3pi/4`, `I2hat->pi/2`.
5. Recompute the mass residual limit `-pi/6` and W8's uniform
   `Delta_M<-pi/12` consequence.
6. Verify the sequential-to-uniform empty-wedge quantifier.
7. Check the combined near-one claim: two accepted endpoint wedges plus one
   fixed strip must yield a single common epsilon for all alpha values.
8. Confirm that arbitrary finite-R `G`, `Xi`, `PHI-SIGN`, and KP-DET remain
   open.

## Verdict

Return `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. The JSON must contain
`audit_id`, `verdict`, `critical_errors`, `gaps`, `repair_hints`,
`covered_scope`, `residual_risk`, `reviewed_artifacts`, `first_error`, and
`decision_delta`. The Markdown must include enough independent algebra to
justify the verdict. Return both artifact paths and SHA256 values in compact
JSON.
