# W14 acute scalar threshold prover packet

## Contract

- Subtask ID: `W14-ACUTE-THRESHOLD-PROVER`.
- One model response. Do not spawn subagents.
- Work only in the accepted unique acute branch
  `c>1/2`, `pi/(2c)<alpha<pi`.
- Write only `route-09-acute-threshold/prover_result.md` and optional
  deterministic checks under `route-09-acute-threshold/prover/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Numerical evidence cannot prove a universal threshold.

## Bound inputs

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-04-mass-g-wave/accepted_package.md`, SHA-256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-07-global-sign-coherence/accepted_package.md`, SHA-256
  `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc`.
- `route-08-common-beta-orientation/prover_result.md`, SHA-256
  `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d`.
- `route-08-common-beta-orientation/accepted_package.md`, SHA-256
  `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed`.
- `route-08-common-beta-orientation/audit/independent_audit.json`, SHA-256
  `bb1207baf181f37459345ed3cff4deb560b5c0acc18fdc3952b8410ffb6bd820`.

Verify every hash before use.

## Exact task

At the unique accepted root of

```text
sin(kappa-c d)/sin(d)=sigma,
g=kappa-c d,
```

prove or sharply reduce

```text
q>E implies
D>k(1-c^2) max{sin(A)^2,sin(d)^2}.          (T)
```

Use the intrinsic compatibility through `P_m`, the exact mass balance, and
the branch-safe formulas for `q`, `E`, `D`, and the coefficients. Seek, in
decreasing order of value:

1. Prove `(T)` and close arbitrary finite-`c` KP-DET.
2. Prove directly that `q>E` contradicts the exact mass balance without the
   stronger max threshold.
3. Close a nontrivial full subchamber, such as one ordering of `A` and `d`,
   with exact equality and endpoint audit.
4. Reduce the gap to one explicit scalar function with a proved monotonicity,
   convexity, or endpoint sign and state the first missing inequality.

Do not repeat accepted branch reconstruction. Avoid differentiating an
implicitly constrained root without the full chain rule and Jacobian sign.

## Required output

The first line must be `PROVED`, `PARTIAL`, or `NO_GAIN`. State exact new
claims, denominator and boundary audit, first unresolved step, and effect on
`PHI-SIGN` and KP-DET. End with one `decision_delta:` line. Return compact JSON
with `subtask_id`, `status`, `artifact_path`, `artifact_sha256`, `exact_gap`,
`failure_mechanism`, and `decision_delta`.

