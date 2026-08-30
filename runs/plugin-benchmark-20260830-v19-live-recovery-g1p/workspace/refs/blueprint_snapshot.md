# Accepted-knowledge snapshot

- Parent commit: `2f2f41c9caf2a6aa21e74bbab577108d62b7dc01`.
- Canonical Blueprint SHA256: `3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48`.
- Evidence inventory SHA256: `0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e`.
- Context: `CTX-DEFAULT`.
- Retrieved target: `CLM-SL-B4-M3-TARGET-V1`.
- Target semantic hash: `semantic-sha256:215474312928e28c4f7e2e736ee45ab66ddad22a73ff41a1f37d37b4e6a99d65`.
- Reliability: established and eligible as a proof input.

The accepted M3 result closes the large-R finite-nonzero-interior chart for the
n=2 symmetric INF branch. It does not close the all-finite-R middle regime.

The deterministic query emitted `BROKEN_ARTIFACT_PATH` warnings because its
locator resolution ignored the configured parent artifact root. The actual
proof artifact exists at the parent path recorded in `source_contract.md` and
its SHA256 matches the Blueprint inventory. This is a workflow defect candidate
and not a mathematical defect.
