# W9 near-one alpha-pi endpoint falsifier packet

## Contract

- Subtask ID: `W9-ALPHA-PI-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work only on the complete exact phase system.
- Write only `route-06-alpha-pi/falsifier_result.md` and optional deterministic
  checks under `route-06-alpha-pi/falsifier/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Formal series and numerics are `EVIDENCE` without existence and uniform
  remainder proofs.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-04-mass-g-wave/repair/near_one_repair.md`, SHA256
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.
- `route-05-alpha-collision/accepted_package.md`, SHA256
  `49d1691a384a6b7d550d8b547dfc25de5daf14fd575d6018462417b04e7257ba`.

Verify every hash.

## Exact task

Adversarially test the candidate exclusion of

```text
m->1+,
alpha->pi.
```

Try to construct a complete exact or rigorously implicit branch scaling,
including possible coupled limits `theta->pi/2` and
`C~k(pi-alpha)`. If this is impossible, independently derive the earliest
exact contradiction and identify which of spectral, band, mass, or modal data
is load-bearing. Distinguish:

1. Exact nonexistence of complete tuples.
2. Failure of only a proposed scaling ansatz.
3. A formal or numerical candidate without existence proof.

Check both norm limits and do not reuse the mass-defective W5 point. If a
complete family exists, compute the signs of `G` and `Xi`; if not, state
precisely why no sign statement is needed on the empty face.

## Required output

The first line must be `REFUTED`, `PARTIAL`, `EVIDENCE`, or `NO_GAIN`.
State the exact finding, existence or nonexistence proof, admissibility and
denominator audit, and effect on `PHI-SIGN`. End with one
`decision_delta:` line. Return compact JSON with `subtask_id`, `status`,
`artifact_path`, `artifact_sha256`, `exact_gap`, `failure_mechanism`, and
`decision_delta`.
