# W8 near-one alpha-pi endpoint prover packet

## Contract

- Subtask ID: `W8-ALPHA-PI-PROVER`.
- One model response. Do not spawn subagents.
- Work only on complete admissible tuples in the frozen phase system.
- Write only `route-06-alpha-pi/prover_result.md` and optional deterministic
  checks under `route-06-alpha-pi/prover/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Numerical evidence is not proof.

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

Decide whether complete admissible tuples can satisfy

```text
m->1+,
alpha->pi.
```

At the uniform spectral limit, the total phases suggest

```text
beta+theta->pi/2,
X->0,
Y->sin(pi/3)>0.
```

The band equation may force `C=cos(theta)->0`, while the mass equation has a
positive right side. Prove or disprove this mechanism rigorously. Seek, in
decreasing order of value:

1. An exact sequential exclusion and equivalent uniform empty wedge near
   `(m,alpha)=(1,pi)`.
2. A complete classification of forced limits for `theta`, `C/(pi-alpha)`,
   `X/(pi-alpha)`, both norms, and the mass residual.
3. If exclusion fails, a uniform sign theorem for `G` or `Xi` in this regime.

Remove all apparent norm singularities using exact spectral equations before
passing to the limit. Audit the modal bounds, both total-phase identities,
the signs in the band equation, and every nonzero limiting factor.

## Required output

The first line must be `PROVED`, `PARTIAL`, or `NO_GAIN`. State the theorem,
proof, norm and denominator audit, quantifier upgrade, and remaining gap. End
with one `decision_delta:` line. Return compact JSON with `subtask_id`,
`status`, `artifact_path`, `artifact_sha256`, `exact_gap`,
`failure_mechanism`, and `decision_delta`.
