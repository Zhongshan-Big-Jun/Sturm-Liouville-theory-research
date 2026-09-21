**Verdict: CHANGES_REQUIRED.** The ten numerical patches passed the bounded review. One reproducible scope-check defect prevents approval of the submitted package.

`regression/regression.py:295` retains only module paths already inside the replay directory; `regression/replay.py:80–81` then checks that filtered list for outside paths. An outside project module disappears before validation. The reviewer executed these actual AST predicates with synthetic module metadata and obtained empty bindings and no rejection. This does **not** show an outside import occurred during the actual replay. Record provenance before filtering, validate required project modules against the selected tree, and add an outside-path negative control; alternatively withdraw the runtime isolation claim explicitly. Candidates and harness were left unchanged.

The required command was actually run from this directory:

```text
/usr/bin/python3 -B regression/replay.py --label independent-review
```

The completed replay returned **0**: candidates **117/117** in normal and `-O`; originals **79 failures/117** in each mode, with the expected exit **1**; both actual four-point candidate op03 CLIs returned **0**. The reviewer recomputed all saved pass predicates, checked every recorded expression against the frozen AST, and found a failing actual-original control for each changed file. A separate reviewer program passed **47/47** bounded checks, including an independent augmented-IVP reference and asymmetric n=2 SUP/INF derivatives. These counts are finite checks, not independent mathematical theorems.

All **48** listed input hashes and PACKET identity were checked and remained unchanged. The first replay attempt stopped before tests because reviewer isolation hid installed user-site NumPy/SciPy; its failure is retained. The same required command succeeded after explicitly enabling only the permitted installed package path.

The fixed backend matched the independent IVP values to at most **2.84e-12** on the three tested profiles. Unmodified `op03_gap_precise` remains faulty: weighted masses on the symmetric SUP fixture are **0.9487027, 0.9313559**, rather than one. Its tested low roots still agree; the demonstrated fault is normalization. Correcting its paired factor alone gives **83.03444**, versus the correct **89.29072**. This legacy dependency is excluded from certification.

[REVIEW.json](REVIEW.json) contains all input hashes, findings, fix requests, per-patch results, commands and evidence links. Raw successful replay evidence is in [work/replay-20260921T122930Z-e64f7d](work/replay-20260921T122930Z-e64f7d/replay-summary.json). Reviewer capture receipts and independent probes are in [independent-verifier-20260921T122457Z](independent-verifier-20260921T122457Z/replay-audit.json). The final [artifact hash manifest](independent-verifier-20260921T122457Z/artifact-hashes.json) binds the deliverables.

Scope is limited to ten edits and their finite behavior. It excludes historical Green/spectral Jacobians, all-R scans, full main programs other than op03, P1/P2/P3 theory, full platform robustness and global mathematical theorems. Hessian expressions tested with an injected finite-difference J do not certify their historical analytic backends.
