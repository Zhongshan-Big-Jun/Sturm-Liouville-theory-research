# Fresh re-audit packet for the W5 near-one repair

## Contract

- Re-audit ID: `REAUDIT-W5-NEARONE-01`.
- You authored the prior audit but did not author the repair.
- Exactly one model response. Do not spawn subagents.
- Review only the immutable repair against the original gap and frozen phase
  definitions. Do not silently repair it.
- Write only `route-04-mass-g-wave/repair/reaudit.md` and
  `route-04-mass-g-wave/repair/reaudit.json`.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-04-mass-g-wave/falsifier_result.md`, SHA256
  `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9`.
- `route-04-mass-g-wave/audit/independent_audit.json`, SHA256
  `7e56fc988a361efa5aeec7d232fb43b03b7889dacfc8ebc3d4afd6a02231c175`.
- `route-04-mass-g-wave/repair/near_one_repair.md`, SHA256
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.

Verify every hash.

## Mandatory checks

1. Check the modal bound `beta<3pi/2` and compact phase closure.
2. Check the min-max eigenvalue estimate uniformly in moving switches and the
   identification of the uniform DD and DN mode indices.
3. Check the phase length identities, especially every factor of `m`.
4. Recompute both limiting norm formulas and their scale conventions.
5. Recompute the limiting mass equation and the exclusion of both theta
   endpoints before any denominator is used.
6. Check that sequential compactness really upgrades all subsequential limits
   to uniform statements.
7. Check the formulas for `D_0`, `N_0`, `U`, the uniform positive lower bound,
   the divergence of `Dtheta`, and the bounded remainder.
8. Confirm the scope excludes `alpha->0` and makes no global `G`, `PHI-SIGN`,
   or KP-DET claim.

## Verdict

Return `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. The JSON must contain
`reaudit_id`, `verdict`, `critical_errors`, `gaps`, `covered_scope`,
`residual_risk`, `reviewed_artifacts`, `first_error`, and `decision_delta`.
The Markdown must contain enough independent calculation to justify the
verdict. Return both artifact paths and SHA256 values in compact JSON.
