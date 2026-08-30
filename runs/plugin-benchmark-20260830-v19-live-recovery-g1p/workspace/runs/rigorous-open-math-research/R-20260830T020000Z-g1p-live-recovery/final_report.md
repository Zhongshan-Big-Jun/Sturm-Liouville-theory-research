# Result

## Exact theorem or result proved

`RIGOROUS_PARTIAL_RESULT`, independently audited `PASS`.

On the prescribed finite-interior n=2 symmetric INF branch:

1. determinant positivity preserves the near-one negative inertia, so each
   sector trace sign follows from its determinant sign;
2. the odd-sector Green difference has an exact semiseparable two-point form;
3. the odd off-diagonal entry is strictly positive, so a first loss cannot be a
   double-zero matrix;
4. the only odd-sector first-loss alternative is a one-dimensional same-sign
   Jacobi kernel satisfying one explicit scalar equality;
5. when `Ko` is nonsingular, an exact symmetric-branch chart passes through the
   odd-sector singular point without inverting the singular full Jacobian.

## Proof or construction

The proof package is `candidate_proof.md`, supported by the two route reports
and derivations. The W1 route gives the semiseparable Green reduction and scalar
equality. The W2 route gives the Jacobi and transfer realization, strict
off-diagonal sign, and Ko-regular branch chart.

## Verification performed

- Fresh independent informal audit: `PASS`.
- Numerical proof premises: none.
- Two immutable recovery checkpoints verify `READY`.
- The in-flight W2 session was reconciled as `INGESTED` before any new dispatch.
- Lean: Tier 0 scaffold only, with `sorry`; not formally verified.

## Remaining gaps

1. Exclude the one-dimensional same-sign Jacobi kernel or prove the forbidden
   crossing-form sign.
2. Treat simultaneous singularity of `Kp_odd` and `Ko`.
3. Prove or refute `KO-DET`.
4. Non-symmetric roots and global G1 prime remain outside this run.

## Failed and blocked routes

- Full-Jacobian `J^(-1)` determinant monotonicity is circular at a hypothetical
  singular point without an independent branch chart.
- Semiseparability and penalty positivity alone are insufficient; the abstract
  scalar witness in `counterexample_log.md` realizes the residual equality but
  is not a branch counterexample.

## Novelty status

`POTENTIALLY_NEW`, with medium novelty risk. The bounded search found related
gap theorems but no exact all-finite-R result for this sector determinant.

## Human/model/tool contributions

- User: authorized the benchmark, no reserve, live recovery test, and repository
  preservation requirement.
- Planner agent: theorem contract, direct reduction, and escalation gate.
- W1 and W2 agents: mechanism-distinct strict partial results.
- Independent auditor: fresh `PASS` verdict on the partial package.
- Root agent: preregistration, checkpoint lineage, reconciliation, synthesis,
  formalization scaffold, validation, and repository integration.

## Reproducibility manifest

- Frozen source commit: `afc6044b22fcab4828cd4bda2aa6c824c4e63d2b`.
- Segment 00 checkpoint ID:
  `sha256:758e11a3080e964e2884c1066447cb1e195644627065de0a9d3cb7064306867f`.
- Segment 01 checkpoint ID:
  `sha256:b31a2c568f5768c296e277da17a7fb9fcefdb93efb01d6211bf2e3de575002fc`.
- Candidate SHA256:
  `4e688ad5d7c0e3f4869e4aa43cad823549fc66db76bcd9293341eb85b0d8e556`.
- Independent audit JSON SHA256:
  `c8132d54952902e90838a733d431033fdc998a85e92a4f5b50181265988811da`.

## Confidence by axis

- Semantic fidelity: high within the declared symmetric finite-interior scope.
- Mathematical correctness: high for the audited strict partial claims.
- Completeness: incomplete; three exact obligations remain.
- Novelty: potentially new, not expert novelty checked.
- Reproducibility: high for files and recovery lineage; agent token and cost
  counters were unavailable.

## Trusted closure and transaction state

- Research status: `partial_progress`.
- Transaction status: pending repository commit at report creation.
- Trusted partial closure: inertia reduction, semiseparable odd-sector form,
  strict odd off-diagonal sign, double-zero exclusion, Jacobi/transfer
  realization, and the Ko-regular branch chart.
- Target `KP-DET` is not in trusted closure.
