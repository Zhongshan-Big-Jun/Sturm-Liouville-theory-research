# W12 and W13 independent joint audit packet

## Contract

- Audit ID: `AUDIT-W12-W13-ORIENTATION-01`.
- One model response. Do not spawn subagents.
- You did not author either submission.
- Treat W12 as unverified first-time candidate mathematics and W13 as an
  evidence artifact only.
- Write only `route-08-common-beta-orientation/audit/independent_audit.md`
  and `route-08-common-beta-orientation/audit/independent_audit.json`.
- Do not edit worker artifacts, shared state, accepted packages, Blueprint,
  Lean, or indexes.

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
- W12 `route-08-common-beta-orientation/prover_result.md`, SHA-256
  `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d`.
- W13 `route-08-common-beta-orientation/falsifier_result.md`, SHA-256
  `61ff0e77fac55e0496d08720b0f06315f9617a8cb38d347e23fbbf43445d6135`.
- Coordinator reconciliation, SHA-256
  `851daf75acc38d2f44cad1d231a4e40d28b87348484c5d56bb88b9f5f98a950e`.

Verify every hash before mathematical use.

## Required independent checks

1. Reconstruct both unsquared sine and cosine formulas without assuming a
   nonzero middle-layer trigonometric factor.
2. Audit the atan2 definitions and prove exactly which modal interval removes
   every possible `pi` multiple in `beta=A+d` and `c beta=B-g`.
3. Recheck the positive square-root lock. Distinguish necessary identities
   from converses and audit the local use of the symbol `A`.
4. Independently derive the coefficient dictionary, especially equations
   `(6)-(13)`, and all strict equivalences involving `Bcoef`, `Acoef`, and
   `Hcoef`.
5. Verify the closed chamber theorem on both sides of `alpha=pi/2` and on the
   boundary `c alpha=pi/2`. Recheck the implications
   `q<0<E -> G>0 -> Xi>0 -> Phi<0 -> KP-DET`.
6. Verify that every complete tuple with `0<c<=1/2` really lies in the closed
   chamber, with strictness at `c=1/2`.
7. Audit uniqueness and unimodality in the remaining acute branch. Ensure the
   proposed scalar threshold is still open and not silently assumed.
8. Confirm W13's numerical counts are labeled `EVIDENCE` and unused by the
   strict proof.
9. Search adversarially for notation collision, quadrant, boundary, equality,
   and sign-direction errors.

## Verdict and output

Return exactly one of `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. A `PASS`
accepts only fully rederived strict partial claims and leaves arbitrary
finite-`c` `PHI-SIGN` open. For each gap, identify the first invalid step and
the smallest repair. The JSON must contain `audit_id`, `verdict`, `artifacts`,
`critical_errors`, `gaps`, and `decision_delta`. Return only compact JSON after
writing both audit artifacts.
