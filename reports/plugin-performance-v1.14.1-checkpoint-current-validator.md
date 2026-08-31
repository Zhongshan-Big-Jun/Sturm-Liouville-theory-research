# Plugin v1.14.1 checkpoint-current validation

## Outcome

Workflow v1.14.1 fixes a fail-closed validation bug found during the live
KP-DET recovery run. When a run had advanced beyond its original
`whiteboard.md` and `closure_gate.md`, v1.14.0 still validated those immutable
ancestor basenames. It could therefore report obsolete schema errors instead
of validating the records bound by the latest checkpoint.

The new selector verifies the complete checkpoint lineage first and then
validates only the whiteboard and closure gate referenced by the latest valid
checkpoint state. It never falls back to an older checkpoint if the latest
checkpoint is stale or invalid. Runs without checkpoints retain the previous
basename behavior.

This release changes workflow infrastructure only. It adds no mathematical
claim and does not change the KP-DET result from `RIGOROUS_PARTIAL_RESULT`.

## Live BVE regression

The regression scope was:

```text
research/runs/R-20260831T020156Z-g1p-kpdet/workspace
```

The observed sequence was:

1. The v1.14.0 validator reported 11 errors from immutable sequence-00
   ancestor records.
2. The v1.14.1 selector verified the checkpoint lineage, selected sequence-02,
   and exposed 12 real schema defects in the then-current records.
3. Deterministic `advance` produced sequence-03. After the numbered current
   records were sealed, validation reported 0 hard problems and 1 expected
   warning because the mathematics remains partial.
4. No worker was restarted, no task was dispatched twice, and no transcript
   was replayed. The deterministic repair used no model or network call.

The final checkpoint is `READY` and `RESUME_READY`:

```text
checkpoint sequence: 03
checkpoint id: sha256:85d5eafbfe0596c79a94a1be91e42ccc2ae4ae2c6caec6a47e349ef6e66e8f77
next obligation: PHI-SIGN
first future action: FUTURE-PHI-EXACT-ROUTE
```

The scoped result is not a whole-project PASS. It certifies only the logical
project root named above.

## Release and installation

| Target | Version or commit | Result |
| --- | --- | --- |
| Parent plugin repository | `516037f` | pushed to `xsoc1`, then `Zhongshan-Big-Jun` |
| DSH adaptation | `5f2b997` | pushed to `xsoc1/math-research-dsh` |
| Local Codex marketplace | workflow `1.14.1` | installed and enabled |
| BVE mathematics package | `17c5559` | pushed to `origin`, then `fork` |

The installed Codex CLI was `0.151.0-alpha.7.2`. The parent source, installed
Codex cache, and DSH adapter copies of `validate_pipeline.py` have the same
SHA-256:

```text
9313289ECE6CD3C84B728C2C15C2EFEA9C4020CDB4142BCEBE3F455FB9C14D8A
```

The installed v1.14.1 validator was then run directly against the live BVE
scope. It selected sequence-03 and returned:

```text
scoped result: 0 problem(s) found, 1 warning(s), 8 check(s).
```

## Release gates

| Target | Result |
| --- | --- |
| Parent repository validator | 81/81 PASS |
| Parent checkpoint smoke suite | 11/11 PASS |
| Parent plugin, skill, compile, and diff checks | PASS |
| DSH repository validator | 51/51 PASS |
| DSH smoke suite | 18/18 PASS |
| DSH bundle, Node syntax, and upstream sync checks | PASS |
| Installed-cache BVE scoped replay | 0 problems, 1 expected warning |

The smoke regression covers a legacy ancestor, a compliant versioned
successor, a mislabeled checkpoint rejection, and post-seal stale detection.

## Mathematical boundary

The validator fix does not close KP-DET. The accepted strict package proves
`gamma_2>b_0>0`, `KP-DET iff S_KP<0 iff Phi<0`, and the Jacobi flux and locking
identities. The next exact obligation is still to prove `Phi<0` on the full
five-phase admissible system or construct an exact admissible tuple with
`Phi=0`. Complete KP-DET, KO-DET, simultaneous sector singularity,
non-symmetric roots, and global G1 prime remain open.
