# W6 near-one alpha-collision prover packet

## Contract

- Subtask ID: `W6-ALPHA-COLLISION-PROVER`.
- One model response. Do not spawn subagents.
- Work only on complete admissible tuples in the frozen finite-interior,
  symmetric, `n=2` INF phase system.
- Write only `route-05-alpha-collision/prover_result.md` and optional
  deterministic checks under `route-05-alpha-collision/prover/`.
- Do not edit shared ledgers, checkpoints, accepted packages, Blueprint, Lean,
  or repository indexes.
- Numerical evidence cannot prove an asymptotic sign.

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

Analyze every hypothetical complete admissible sequence

```text
m->1+,
alpha->0.
```

The fixed-eta theorem does not apply. At the uniform limit,

```text
cos(2alpha/3)-cos(alpha)~(5/18)alpha^2,
r=m^2/(m^2-1)~1/[2(m-1)],
```

so the relative scale of `alpha` and `m-1` is load-bearing. Derive the scale
from the complete spectral, band, and exact mass system, not by assumption.
Seek, in decreasing order of value:

1. Prove `G>0`, or directly `Xi>0`, along every such sequence.
2. Prove that complete admissibility forces a lower bound such as
   `alpha/(m-1)>=kappa>0` or a sharper relation sufficient for the sign.
3. Derive an exact blow-up system in variables such as
   `epsilon=m-1` and `zeta=alpha/epsilon^q`, classify all possible finite and
   infinite scaling limits, and close at least one nontrivial regime.
4. Give a strictly smaller exact asymptotic obligation with all remainders
   uniform and every equality case explicit.

Use the accepted mixed-sign mass balance if helpful. Audit every Taylor
remainder uniformly on the compact theta and beta limits. Do not infer a
physical branch from formal series without an existence argument.

## Required output

The first line of `prover_result.md` must be `PROVED`, `PARTIAL`, or
`NO_GAIN`. State the exact theorem, scaling classification, derivation,
uniform remainder bounds, denominator and boundary audit, and the first
unresolved step. End with one `decision_delta:` line. Return compact JSON
with `subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `exact_gap`,
`failure_mechanism`, and `decision_delta`.
