# W7 near-one alpha-collision falsifier packet

## Contract

- Subtask ID: `W7-ALPHA-COLLISION-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work only on the frozen complete admissible phase system.
- Write only `route-05-alpha-collision/falsifier_result.md` and optional
  deterministic checks under `route-05-alpha-collision/falsifier/`.
- Do not edit shared ledgers, checkpoints, accepted packages, Blueprint, Lean,
  or repository indexes.
- Formal series or numerics are `EVIDENCE` until accompanied by a rigorous
  existence and remainder certificate.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-04-mass-g-wave/repair/near_one_repair.md`, SHA256
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.
- `route-04-mass-g-wave/repair/reaudit.json`, SHA256
  `3f88a6ed8cf6da7f7adc41a195776fbfa9f00c8cec97153156a98f773a0c573d`.

Verify every hash.

## Exact task

Adversarially test the unresolved simultaneous face

```text
m->1+,
alpha->0.
```

Seek, in decreasing order of value:

1. A rigorously existing complete branch segment with `G<=0` or `Xi<=0`.
2. A rigorously existing scaling family showing that a proposed lower bound
   on `alpha/(m-1)` is false while preserving every exact constraint.
3. A formal or interval-certified leading-order system that identifies a
   candidate critical scale and sign, together with an explicit list of the
   missing implicit-function or remainder obligations.
4. An exact obstruction that rules out a common asymptotic shortcut, even if
   it does not refute `PHI-SIGN`.

Use the full exact mass equation. The earlier mass-defective witness cannot be
reused as a complete counterexample. Distinguish a counterexample to `G>=0`
from one to `Xi>0`. Audit modal indices, strict interior reconstruction,
denominators, and branch existence.

## Required output

The first line of `falsifier_result.md` must be `REFUTED`, `PARTIAL`,
`EVIDENCE`, or `NO_GAIN`. State the exact finding, existence status,
admissibility audit, remainder gap, and effect on `PHI-SIGN`. End with one
`decision_delta:` line. Return compact JSON with `subtask_id`, `status`,
`artifact_path`, `artifact_sha256`, `exact_gap`, `failure_mechanism`, and
`decision_delta`.
