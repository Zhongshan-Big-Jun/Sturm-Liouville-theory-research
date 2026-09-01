# W13 common-beta orientation falsifier packet

## Contract

- Subtask ID: `W13-COMMON-BETA-ORIENTATION-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work on the complete exact finite-interior phase system for arbitrary
  finite `m>1`.
- Write only `route-08-common-beta-orientation/falsifier_result.md` and
  optional deterministic checks under
  `route-08-common-beta-orientation/falsifier/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Floating-point continuation is `EVIDENCE` unless upgraded by interval or
  exact certification.

## Bound inputs

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA-256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA-256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA-256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-07-global-sign-coherence/accepted_package.md`, SHA-256
  `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc`.
- `route-07-global-sign-coherence/audit/independent_audit.json`, SHA-256
  `11b3b68b8aa9b1dcfd593b1e919169f9057f3daa63ef1dfb6ccb09a46da7e1db`.

Verify every hash before use.

## Exact task

Adversarially test the orientation-sensitive remainder. Seek, in decreasing
order of value:

1. An exact or interval-certified complete tuple with `q>E`, hence `G<0`,
   including all modal, common-`beta`, mass, and strict reconstruction checks.
2. An exact common-`beta` spectral-band tuple with `q>E` in a mixed
   coefficient chamber, refuting `(SC-rem)` before mass.
3. A rigorous obstruction showing that a candidate negative-`G` branch cannot
   cross the mass surface or cannot satisfy the common-`beta` orientation.
4. A bounded numerical map labeled `EVIDENCE`, with an explicit interval
   certification plan and no proof claim.

Use the accepted W11 family only as a regression seed. It is mass-defective
and cannot by itself answer this task. Preserve the distinction between
refuting `(SC-rem)` and refuting complete-system `PHI-SIGN`.

## Required output

The first line must be `REFUTED`, `PARTIAL`, `EVIDENCE`, or `NO_GAIN`. State
the exact admissibility level, common-`beta` branch, chamber signs, mass defect
or mass equality, and the first certification gap. End with one
`decision_delta:` line. Return compact JSON with `subtask_id`, `status`,
`artifact_path`, `artifact_sha256`, `exact_gap`, `failure_mechanism`, and
`decision_delta`.
