# Fresh independent audit packet for W7 alpha-collision exclusion

## Contract

- Audit ID: `AUDIT-W7-ALPHA-COLLISION-01`.
- You did not author W7.
- Exactly one model response. Do not spawn subagents.
- Review W7 as a first-time submission and do not silently repair it.
- Write only `route-05-alpha-collision/audit/independent_audit.md` and
  `route-05-alpha-collision/audit/independent_audit.json`.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-04-mass-g-wave/repair/near_one_repair.md`, SHA256
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.
- `route-04-mass-g-wave/repair/reaudit.json`, SHA256
  `3f88a6ed8cf6da7f7adc41a195776fbfa9f00c8cec97153156a98f773a0c573d`.
- `route-05-alpha-collision/falsifier_result.md`, SHA256
  `191b0a1cd621b8f8451647a5273a2f79efd0d57b71e3a7ba570e8644cae6e044`.

Verify every hash.

## Mandatory checks

1. Verify the compact phase subsequence and switch-uniform spectral limits.
2. Recompute the removal of the two apparent left-layer norm singularities
   from the spectral equations, including every factor of `m`, `c`, `Z`, and
   `T`.
3. Recompute the full limits `I3hat->3pi/4` and `I2hat->pi/2` when
   `alpha->0`.
4. Derive the limiting mass equation, exclude both theta endpoints, and
   audit the sign choice in `C=(2/3)s`.
5. Check `Z->-1`, `T->-1`, `X/alpha->-1`, and
   `Y/alpha->2/3` from the exact spectral equations.
6. Check the band-equation limit and whether it really yields the stated
   contradiction.
7. Verify that sequential nonexistence is equivalent to a uniform empty
   wedge and that no unproved branch existence assumption is used.
8. Check the claim about `alpha/(m-1)->infinity`; downgrade it if the uniform
   wedge alone does not justify it.
9. Confirm the theorem does not itself prove arbitrary finite-R
   `PHI-SIGN` or KP-DET.

## Verdict

Return `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. The JSON must contain
`audit_id`, `verdict`, `critical_errors`, `gaps`, `repair_hints`,
`covered_scope`, `residual_risk`, `reviewed_artifacts`, `first_error`, and
`decision_delta`. The Markdown must contain enough independent algebra to
justify the verdict. Return both artifact paths and SHA256 values in compact
JSON.
