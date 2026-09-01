# W11 complete-system global falsifier packet

## Contract

- Subtask ID: `W11-GLOBAL-SIGN-COHERENCE-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work on the complete exact finite-interior phase system for arbitrary
  finite `m>1`.
- Write only `route-07-global-sign-coherence/falsifier_result.md` and optional
  deterministic checks under `route-07-global-sign-coherence/falsifier/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Floating-point continuation is `EVIDENCE` unless upgraded by exact or
  interval-certified branch existence and signs.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-06-alpha-pi/accepted_package.md`, SHA256
  `1177c02076694ebf95ce912719846b3143e5e9099614e66492586296ae7526ba`.

Verify every hash.

## Exact task

Adversarially test `(SC)` and the weaker complete-system target `G>=0`.
Seek, in decreasing order of value:

1. An exact or interval-certified complete admissible tuple with `G<0`, with
   signs of `A,B,H,Xi,Phi` and strict mode inequalities.
2. An exact spectral-band tuple with `G<0` but coefficients outside both
   same-sign orthants, thereby refuting `(SC)` even if it fails mass.
3. A rigorous chamber obstruction showing why such a counterexample cannot
   cross the mass surface.
4. A bounded numerical continuation map labeled `EVIDENCE`, with an explicit
   certification plan and no proof claim.

The accepted mass-defective W5 point is a valid regression seed but not a
complete counterexample. Check its coefficient signs exactly before choosing
a route. A counterexample to `(SC)` is not automatically a counterexample to
`PHI-SIGN`; preserve that distinction. Do not repeat near-one endpoint work.

## Required output

The first line must be `REFUTED`, `PARTIAL`, `EVIDENCE`, or `NO_GAIN`.
State the exact finding, admissibility or mass defect, chamber signs,
certification gap, and effect on `PHI-SIGN`. End with one `decision_delta:`
line. Return compact JSON with `subtask_id`, `status`, `artifact_path`,
`artifact_sha256`, `exact_gap`, `failure_mechanism`, and `decision_delta`.
