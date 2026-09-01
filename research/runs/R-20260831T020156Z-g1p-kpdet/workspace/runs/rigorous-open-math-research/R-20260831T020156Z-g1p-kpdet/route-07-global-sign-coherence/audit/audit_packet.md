# W10 and W11 independent joint audit packet

## Contract

- Audit ID: `AUDIT-W10-W11-GLOBAL-01`.
- One model response. Do not spawn subagents.
- You did not author either submission.
- Treat both submissions as unverified first-time candidate content.
- Write only `route-07-global-sign-coherence/audit/independent_audit.md`
  and `route-07-global-sign-coherence/audit/independent_audit.json`.
- Do not edit either worker artifact, shared state, accepted packages,
  Blueprint, Lean, or indexes.
- Numerical continuation and search output are `EVIDENCE`, never proof.

## Bound inputs

- `problem_contract.md`, SHA-256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA-256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA-256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA-256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- W10 `route-07-global-sign-coherence/prover_result.md`, SHA-256
  `8f5c381223b476fcf2b2d6af7f1a51e90086c3146b45a48bdd8362ad126f11aa`.
- W11 `route-07-global-sign-coherence/falsifier_result.md`, SHA-256
  `18f2e57dfd18784527dac95d07477e89da935fff4065658f2a847af9137e4ba8`.
- Coordinator reconciliation, SHA-256
  `ecaa7a9d572a72f117b7b0055c571f67f5e515eead0cd3bd3ac6b4ee92f3646d`.

Verify every hash before reading mathematically.

## Required independent checks

1. Reconstruct the W10 phase lock from the unsquared transfer equations and
   audit every sign and modal-domain denominator.
2. Independently expand the factorization
   `G=X(M Dtheta/P)(q-E)`, including the formula and equality set for `E`.
   Running the deterministic replay is allowed but cannot replace the
   derivation.
3. Recheck the exact `B`-to-`H` identity and whether the positive mass weights
   really exclude `B>=0`, including `B=0`.
4. Decide whether W10's remaining chamber statement is stated at exactly the
   strength proved, without accidentally claiming global `(SC)` or `G>=0`.
5. Independently verify the W11 one-parameter family's spectral, band, modal,
   chamber, mass-residual, and `G<0` formulas. Check the strict inequalities at
   both endpoint limits and the specialization to W5.
6. Check that W11's numerical table and scan are isolated as `EVIDENCE` and
   that no completeness claim depends on them.
7. Look for hidden branch, orientation, squaring, equality, or sign errors.

## Verdict and output

Return exactly one of `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. A `PASS`
accepts only claims fully rederived; it does not close global `PHI-SIGN`.
For every gap, name the first invalid step and smallest repair. The JSON must
contain `audit_id`, `verdict`, `artifacts`, `critical_errors`, `gaps`, and
`decision_delta`. Return only compact JSON after writing both artifacts.
