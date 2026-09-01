# W12 common-beta orientation prover packet

## Contract

- Subtask ID: `W12-COMMON-BETA-ORIENTATION-PROVER`.
- One model response. Do not spawn subagents.
- Work on the complete exact finite-interior phase system for arbitrary
  finite `m>1`.
- Write only `route-08-common-beta-orientation/prover_result.md` and optional
  deterministic checks under `route-08-common-beta-orientation/prover/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Numerical evidence cannot prove a universal sign theorem.

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

The accepted reduction is

```text
G<0 iff q>E,
B<0 on every complete tuple.
```

The squared phase lock loses the load-bearing fact that the two reconstructed
angles are the same `beta` and `c beta`. Use the unsquared formulas

```text
sin(beta)=m X(C x-S)/P,
sin(c beta)=-m s X(Cc+s y)/(C Q),
```

together with the corresponding cosine transfer data, the strict modal
intervals, the exact mass balance, and `0<c<1`.

Seek, in decreasing order of value:

1. Prove directly `q<=E` on the complete mass manifold.
2. Prove `(SC-rem)`: `q>E` and `B<0` force the forbidden negative same-sign
   coefficient chamber.
3. Derive a signed, branch-safe common-`beta` identity that strictly reduces
   the remaining decision to one scalar monotonicity or convexity statement.
4. Close one entire remaining chamber, with exact equality and boundary audit.

Do not use inverse trigonometric branches without proving their modal index.
Do not repeat the accepted phase-lock or near-one derivations except as cited
lemmas.

## Required output

The first line must be `PROVED`, `PARTIAL`, or `NO_GAIN`. State every exact
new theorem, branch and denominator audit, first unresolved step, and effect on
`G`, `Phi`, and KP-DET. End with one `decision_delta:` line. Return compact
JSON with `subtask_id`, `status`, `artifact_path`, `artifact_sha256`,
`exact_gap`, `failure_mechanism`, and `decision_delta`.

