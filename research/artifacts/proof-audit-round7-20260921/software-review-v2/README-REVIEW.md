# Round7 independent software review v2 — APPROVED

The ten local source deltas and repaired R7-SW-001 provenance gate have no substantive blocking discrepancy within the frozen packet and the executed scope.

Packet SHA-256: `a22df2037cfdfa602da9db061f4b15a2f24bfbf1c33d37a1e019b267122c747c`. All 52 listed input files matched before and after review; PACKET.json was also unchanged. No frozen file, main source, external referenced source, private context or sibling directory was edited/read beyond the stated boundary; no Git operation or push was used.

| Own execution | Normal outer | -O outer |
| --- | --- | --- |
| Actual package verifier, 50 entries plus manifest sidecar | exit 0 | exit 0 |
| Complete fresh replay, both inner modes, 14 cases | exit 0 | exit 0 |
| Candidate numerical checks per process | 117/117 | 117/117 |
| Original negative checks per process | 38 pass, 79 fail; exit 1 | 38 pass, 79 fail; exit 1 |
| Actual candidate CLI | all four points pass in each inner mode | all four points pass in each inner mode |
| Eight real provenance controls per replay | all exit 86 for intended sole reason | all exit 86 for intended sole reason |
| Separate rebound old-filter mutant, eight controls | replay exit 1 as expected | replay exit 1 as expected |

The four CLI points are u=0.400, 0.430, 0.450, 0.458. Clean numerical snapshots contain 666 file-backed modules (17 required project/harness, 147 stdlib, 502 installed package); clean CLI snapshots contain 179 (3 required, 92 stdlib, 84 installed package). Outside controls add a real imported module and refuse; missing controls remove a real required binding and refuse. Exact selected paths and frozen digests were checked independently. NumPy/SciPy package directories and stdlib excluding site/dist-packages are the runtime allowances; their parent directories receive no blanket acceptance.

Restoring only the old collector filter in a **separate, explicitly rebound mutant** makes each of the four outside controls incorrectly exit 0, while the four missing controls still exit 86. Each mutant replay therefore exits 1. This is own sensitivity evidence, not an author result or a candidate modification.

The reviewer-written output audit passed across all 44 repaired/mutant children. It independently recomputed the 117 numerical truth checks, checked the 16 distinct recorded AST expressions across all ten patches, checked required and observed source hashes/paths, and verified raw stream hashes, statuses and exact refusal reasons. All original failures, mutant failures and the initial `python`-not-found bootstrap failure are retained. Actual commands and per-process evidence paths are in REVIEW.json and the receipts.

Approval covers finite tests, the documented source functions/AST nodes, the complete instrumented op03 CLI, and the observed file-backed provenance gate. It does **not** certify OS isolation, import prevention, transient/malicious module behavior, full old analytic/spectral Jacobians, global scans, historical proofs, or density-path P1/P2/P3 calculations. The simplified Hessian requires stationarity; the general product-rule term remains necessary. The unchanged legacy op03_gap_precise normalization defect (R7-SW-002) is reobserved and explicitly excluded from approval.

The historical `inputs/tools-AGENTS.md` reference is disclosed in unchanged supplied manifests. The file was not supplied or read, is not an executable dependency, and gives no permission to follow that reference. The old prior-review.json remains CHANGES_REQUIRED for its old snapshot.

- [Structured verdict, checks, limitations and actual commands](REVIEW.json)
- [Independent derivation and ten-source review](independent-review-20260921-v2/source-review.md)
- [Independently audited execution evidence](independent-review-20260921-v2/execution-audit.json)
- [Before hashes](independent-review-20260921-v2/initial-hashes.json) and [after hashes](independent-review-20260921-v2/final-hashes.json)
- [Separate mutant description](independent-review-20260921-v2/filter-only-mutation.json)
- [All own artifact hashes](independent-review-20260921-v2/artifact-index.json)

Only supplied inputs and installed Python/NumPy/SciPy were used, together with this reviewer's new own work. The reviewer-owned AGENTS.md records the method and this request; frozen AGENTS.md was preserved.
