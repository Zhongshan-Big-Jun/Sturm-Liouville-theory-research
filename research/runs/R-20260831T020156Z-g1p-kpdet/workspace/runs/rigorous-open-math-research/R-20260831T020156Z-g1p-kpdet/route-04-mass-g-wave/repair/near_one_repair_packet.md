# W5 near-one bounded repair packet

## Contract

- Repair ID: `REPAIR-W5-NEARONE-01`.
- Exactly one model response. Do not spawn subagents.
- Write only `route-04-mass-g-wave/repair/near_one_repair.md` and optional
  deterministic checks under `route-04-mass-g-wave/repair/checks/`.
- Do not edit the immutable original W5 result or its audit.
- No numerical observation can replace a uniform proof.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-04-mass-g-wave/falsifier_result.md`, SHA256
  `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9`.
- `route-04-mass-g-wave/audit/independent_audit.json`, SHA256
  `7e56fc988a361efa5aeec7d232fb43b03b7889dacfc8ebc3d4afd6a02231c175`.

Verify every hash before use.

## Exact repair target

Let complete admissible tuples satisfy

```text
m -> 1+,
eta<=alpha<=pi-eta
```

for fixed `eta>0`. Repair the claim that `G>0` for all sufficiently small
`m-1` by explicitly proving the missing uniform chain:

1. Use the modal inequalities to obtain compactness of the phase variables,
   including a uniform bound on `beta`.
2. Prove uniform spectral convergence for the moving three-layer densities,
   for example from `||rho_m-1||_infinity<=m^2-1`, and derive
   `c->2/3` and both total-phase limits independently of switch motion.
3. Along every convergent phase subsequence, pass the exact continuous norm
   formulas to `I3hat->3pi/4` and `I2hat->pi/2`.
4. Use the limiting mass equation to obtain
   `cos(theta)=(2/3)sin(2theta/3)`, exclude `theta=0,pi/2`, and upgrade this by
   compactness to uniform endpoint separation.
5. Deduce uniform positivity of
   `U->cos((2/3)alpha)-cos(alpha)` on the stated alpha interval, boundedness
   of `X Ttheta^2/C^2`, and positive divergence of the `Dtheta U` term.

Audit every scale factor and explain why all convergence is uniform on the
moving-switch family. If any item cannot be proved, do not improvise: state
`DOWNGRADED` and give the exact maximal conditional theorem.

## Required output

The first line must be `REPAIRED` or `DOWNGRADED`. State a precise theorem,
full proof, denominator and boundary audit, and remaining scope. End with one
`decision_delta:` line. Return compact JSON with `repair_id`, `status`,
`artifact_path`, `artifact_sha256`, `remaining_gap`, and `decision_delta`.
