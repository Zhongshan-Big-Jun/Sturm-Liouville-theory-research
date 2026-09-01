# W14 and W15 independent joint audit packet

## Contract

- Audit ID: `AUDIT-W14-W15-ACUTE-01`.
- One model response. Do not spawn subagents.
- You did not author either submission.
- Treat both analytic packages as unverified first-time candidate content.
- Write only `route-09-acute-threshold/audit/independent_audit.md` and
  `route-09-acute-threshold/audit/independent_audit.json`.
- Do not edit worker artifacts, shared state, accepted packages, Blueprint,
  Lean, or indexes.
- W15's floating-point searches are `EVIDENCE`, never proof.

## Bound inputs

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-04-mass-g-wave/accepted_package.md`, SHA-256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-07-global-sign-coherence/accepted_package.md`, SHA-256
  `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc`.
- `route-08-common-beta-orientation/accepted_package.md`, SHA-256
  `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed`.
- W14 `route-09-acute-threshold/prover_result.md`, SHA-256
  `ef7ad48667026a5eb672c8d4bd48718903fd6dcf2102d9f16b8a6883ece948c2`.
- W15 `route-09-acute-threshold/falsifier_result.md`, SHA-256
  `c961bcba5931957beb2e2e60baed90e9517d2af0d3015efa8605a86e985160a2`.
- Coordinator reconciliation, SHA-256
  `6b9973b8f56b06b1c254696976b9349f0bb5725745ac61e3dcadbd4901fbe959`.

Verify every hash before mathematical use.

## Required W14 checks

1. Reconstruct root existence and uniqueness for each acute `A`, including
   the nonzero endpoint cases.
2. Recheck the full constrained derivative formulas `(3)-(7)`. Audit every
   ordering used to prove positivity of `T`, `d'`, and `J'`.
3. Independently compute the `A->0+` limit of `J` and verify that strict
   monotonicity excludes the acute branch for `c<=2/3`, including `c=2/3`.
4. Verify that this exclusion plus the previously accepted closed chamber
   really proves complete `PHI-SIGN` and KP-DET for `0<c<=2/3`.
5. Independently derive the exact mass collapse `(12)`, including the
   transfer norm identities and every positive scaling factor.
6. Check the strict inequality `(13)`, the definition of `Psi`, its endpoint
   limit, and the logical status of the remaining `q>E -> Psi>0` implication.
7. Audit constrained differentiation formula `(18)` and ensure no derivative
   of the isolated compatibility equation is set to zero.

## Required W15 checks

1. Verify the compactified definitions at `z=0` and the claim of uniformity
   over all `m>1`, including possible double limits `z,t->0`.
2. Reproduce the leading expansions `(C1)-(C3)` from the denominator-free
   common-orientation and positive-lock equations, with correct little-`o`
   scope.
3. Verify the threshold margins, coefficient signs, exact normalized mass
   residual, and the conclusion that no complete tuple approaches the collar.
4. Check compatibility with W14 at `c=2/3` and distinguish boundary sequences
   from strict acute roots.
5. Confirm all numerical scans are isolated as `EVIDENCE` and unused by the
   strict asymptotic theorem.

## Verdict and output

Return exactly one of `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. A `PASS`
accepts only fully rederived strict partial claims and leaves the `c>2/3`
scalar implication open. For each gap, identify the first invalid step and
smallest repair. The JSON must contain `audit_id`, `verdict`, `artifacts`,
`critical_errors`, `gaps`, and `decision_delta`. Return only compact JSON after
writing both authorized audit files.
