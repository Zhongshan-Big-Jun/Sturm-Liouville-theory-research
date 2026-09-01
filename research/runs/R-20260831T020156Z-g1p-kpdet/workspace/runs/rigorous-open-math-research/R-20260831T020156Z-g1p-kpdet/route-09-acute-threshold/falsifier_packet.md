# W15 acute threshold and collar falsifier packet

## Contract

- Subtask ID: `W15-ACUTE-THRESHOLD-FALSIFIER`.
- One model response. Do not spawn subagents.
- Work only in or at rigorously controlled boundaries of the accepted unique
  acute branch.
- Write only `route-09-acute-threshold/falsifier_result.md` and optional
  deterministic checks under `route-09-acute-threshold/falsifier/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Floating-point work is `EVIDENCE` unless upgraded by exact or interval proof.

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

Adversarially test `(T)` and the weaker mass conclusion. Seek, in decreasing
order of value:

1. An exact or interval-certified unique acute-branch tuple with `q>E` but
   failure of one coefficient threshold in `(T)`.
2. An exact or interval-certified complete mass tuple with `q>E`, which would
   refute complete-system `G>=0`.
3. A rigorous blow-up classification of the degenerate collar
   `(alpha,beta,theta,c)->(pi,0,pi/2,2/3)` or another boundary, proving a
   one-sided sign or exposing a real escape scale.
4. A bounded search labeled `EVIDENCE`, together with a precise interval or
   analytic certification plan.

A counterexample to the stronger max threshold need not refute KP-DET. Keep
these outcomes separate. Preserve all strict modal and common-`beta` branch
conditions.

## Required output

The first line must be `REFUTED`, `PARTIAL`, `EVIDENCE`, or `NO_GAIN`. State
the exact admissibility level, threshold signs, mass status, collar scaling,
and first certification gap. End with one `decision_delta:` line. Return
compact JSON with `subtask_id`, `status`, `artifact_path`, `artifact_sha256`,
`exact_gap`, `failure_mechanism`, and `decision_delta`.
