# Files-only convergence check

## Verdict

`PASS`.

The retained files alone converge on one honest terminal interpretation:

- Recovery experiment status: `PASS_WITH_USABILITY_FINDINGS`.
- Mathematical status: `RIGOROUS_PARTIAL_RESULT`.
- Independent informal audit: `PASS` for the strict partial package.
- Full target completion: false.
- Numerical proof premises: none.

This check performed no new mathematics. It compared the terminal summaries,
candidate package, audit records, manifests, checkpoint lineage, receipts,
reconciliation record, and current workspace state. It also recomputed every
SHA256 binding used by those records.

## 1. Honest result status

`RESULTS.md`, `final_report.md`, `candidate_proof.md`, `independent_audit.json`,
both interruption states, both resume receipts, and `run-manifest.json` all
retain `RIGOROUS_PARTIAL_RESULT`. The audit JSON sets
`target_completion` to `false`, and the final report says that `KP-DET` is not
in trusted closure. No reviewed file promotes the result to a full theorem.

The workspace stage `completed_live_recovery` means that the controlled
recovery experiment ended. It does not mean that the mathematical target was
completed. This interpretation is explicit in `workspace/state/current.json`
and `workspace/state/RESUME.md`.

## 2. Reconstructible strict partial mathematics

The files consistently identify the following audited partial package on the
prescribed finite-interior, symmetric, n=2 INF branch:

1. Positive determinant preserves the near-one negative inertia in each
   sector, so the trace sign follows once the determinant sign is known.
2. The odd-sector Green difference has the exact normalized semiseparable form
   `U^(-1) H U^(-1) = [[a,b],[b,b]]`, with `b>0`.
3. After the penalty congruence, a first odd-sector singularity cannot be a
   double-zero matrix. The residual alternative is a corank-one matrix with a
   same-sign kernel and the exact scalar condition
   `gamma_2>b` and `gamma_1-a=b^2/(gamma_2-b)`.
4. The reflection-transverse variation has the exact Jacobi residual identity
   `dot(F)_trans=-tau Kp_odd y`, together with the stated moving-level boundary
   conditions.
5. The transfer realization satisfies
   `D_(p,q) A=-tau Kp_odd E` and
   `det D_(p,q) A=-tau^2 det Kp_odd`.
6. If `Ko` is nonsingular, the symmetric branch has a local chart through an
   odd-sector singularity via `D_(a,b) S=-tau E Ko`, without inversion of the
   singular full Jacobian.

These statements are reconstructed from the audited package. This convergence
check did not independently rederive them.

The exact residual obligations also agree across the candidate, audit,
sequence 01 state and receipt, final report, and workspace resume state:

1. Exclude the one-dimensional same-sign Jacobi kernel, equivalently rule out
   the displayed scalar equality or prove the forbidden crossing-form sign.
2. Treat a finite-interior point where `Kp_odd` and `Ko` are simultaneously
   singular, outside the `Ko`-regular chart.
3. Prove or refute `KO-DET` on the all-finite-R branch.

Non-symmetric roots and global G1 prime are outside this run and remain open.

## 3. Recovery lineage and W2 duplication check

The lineage is complete and internally linked:

1. Sequence 00 sealed checkpoint
   `sha256:758e11a3080e964e2884c1066447cb1e195644627065de0a9d3cb7064306867f`
   while W2, worker `W2-KP-FIRSTZERO-JACOBI`, session
   `/root/kp_jacobi`, was still `RUNNING`.
2. `resume_receipt-00.json` made `RECONCILE-W2-SEG00` the unique first action
   and prohibited a new research dispatch before reconciliation.
3. `reconciliation-w2.md` records the same worker and session as `INGESTED`,
   with hashes for exactly one route report, derivation, and route manifest.
4. Sequence 01 links to the exact sequence 00 checkpoint and receipt hashes,
   has no unresolved in-flight work, records the W2 reconciliation, and places
   both `RECONCILE-W2-SEG00` and `W2-KP-FIRSTZERO-JACOBI` in `do_not_repeat`.
5. `resume_receipt-01.json` preserves those completed actions and authorizes
   only `AUDIT-MERGED-PARTIAL` as the next boundary action.

The retained lineage therefore shows no W2 restart, repeated dispatch, or
transcript replay. This agrees with `RECOVERY_METRICS.md`, which reports zero
worker restarts and zero duplicate research dispatches.

## 4. Audit binding and freshness

All 47 recomputed file-to-record SHA256 comparisons matched. This includes all
checkpoint-bound artifacts, both checkpoint state files, both receipt links,
both receipt read sets, the eight audit read-set artifacts, and every artifact
listed in `run-manifest.json`.

The current candidate hash is
`4e688ad5d7c0e3f4869e4aa43cad823549fc66db76bcd9293341eb85b0d8e556`.
It matches sequence 01, receipt 01, both audit records, the final report, and
the run manifest. The current audit JSON hash is
`c8132d54952902e90838a733d431033fdc998a85e92a4f5b50181265988811da`,
matching both the final report and run manifest. The audit verdict is `PASS`,
while its target-completion field remains false.

Thus the audit is fresh with respect to the current candidate and its declared
eight-file read set. No audited input has drifted since the recorded audit.

## 5. Stale conflict check

No stale conflicting mathematical completion label was found.

The following historical markers are not conflicts:

- `candidate_proof.md` says that it is pending fresh independent audit because
  it is the immutable pre-audit candidate. The later audit and manifest bind
  that exact candidate hash.
- `interruption_state-01.json` has `latest_audit: null` because it is the
  pre-audit checkpoint state. Receipt 01 authorizes the audit, and the later
  audit and manifest record its result.
- `final_report.md` says that the repository transaction was pending at report
  creation. That time-qualified transaction marker does not change the
  mathematical label.
- `lifecycle_state: ACTIVE` and `current_stage: completed_live_recovery` refer
  to the continuing research program and the completed experiment,
  respectively.

No file claims that `KP-DET`, simultaneous sector singularity, `KO-DET`,
non-symmetric roots, or global G1 prime is closed.

## Limitations

- This was a files-only convergence check. It did not rerun the mathematics,
  Lean, the checkpoint CLI, or any external validator.
- The files demonstrate hash freshness and assert auditor independence. Files
  alone cannot independently prove the human or agent identity behind that
  assertion.
- The no-duplication conclusion is supported by the canonical session lineage,
  reconciliation artifact, `do_not_repeat` state, and reported counters. It
  cannot exclude unrecorded activity outside the retained experiment files.
- Per-agent token, cache, response, and cost telemetry was unavailable, as
  already disclosed by the run manifest and metrics.
- Parent-repository migration debt and canonical Blueprint integration are
  outside this isolated run boundary and were not evaluated.
