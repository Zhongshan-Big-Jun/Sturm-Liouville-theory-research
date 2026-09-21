# Independent Lean execution review — PASS

Agent: 01a0c260-fa2c-71f1-aa9a-8ccfdf5befc5 (native CODEX_THREAD_ID; independent of the frozen authors).

Target: SL.AuditRound5.local_algebra_root. The exact frozen source was compiled by this agent into a fresh object with Windows PE Lean 4.31.0 through WSL. All 196 checks passed.

- Packet and all 104 snapshots matched their hashes before and after the audit.
- All 11 runtime files and 14,845 declared artifacts (3,712 modules; 3,028,880,240 module-artifact bytes) matched current-byte hashes before and after execution.
- All 59 declarations (37 theorems, 22 definitions), exported types, definition bodies and dependency identities matched both frozen exports byte for byte.
- Independent graph traversal reproduced every declaration's Lean axiom closure. The 12,604-node union and 12,601-node root closure contain only propext, Classical.choice and Quot.sound as axioms; no sorryAx, unknown or unsafe dependency.
- The explicitly typed eight-conjunct root contract compiled with exit 0. It is local real-polynomial algebra, with explicit parameter and kernel-inclusion hypotheses inside the relevant conjuncts.
- Positive controls compiled with exit 0, including the 1+X witness and explicit negation of high-span equality.
- The false-equality control exited 1 with the expected strict-inclusion/equality type mismatch. This was not a failed proof of False.
- Import resolution before and after the probes selected only the new SL.AuditRound5 object. Every probe retained its path/hash. All other module paths matched the pinned manifest.
- Source, pins and controls were copied unchanged. Only the exporter's literal output directory was adapted; both hashes and the one-line diff are retained.
- One source-line-119 style warning was retained. No mathematical source was authored or repaired.

Source SHA-256: 035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45

Fresh root SHA-256: 59448f94c4791e647b2ec7a541519415390458d1a95e164fc802fa07499eb59e

The fresh root has a different physical-source/output provenance and its own binary hash; binary equality with the author's object is not claimed. Export equality is exact.

The root's eight components are low traces, low residues, the all-index high-family trace/residue conclusions, high-span inclusion/strictness, the oblique 1+X witness, positive-L determinant/inverse, positive-even-L endpoint correction/divisibility, and trace-lift membership under the explicit kernel-inclusion hypothesis.

All eight compiler invocations have exact argument vectors, effective LEAN_PATH/WSLENV, separate raw stdout/stderr, exit codes and source/object hashes in logs/. REPORT.json, checks/, the exporter diff, hash inventory and changed-path list give the structured evidence.

The optional maintained-verifier replay was not performed because its implementation is absent from the frozen packet. This execution review complements the separate semantic comparison; it does not certify complex/Sobolev analysis, topological closure, cutoff approximation, Green integration, leading-term tail equality or full cofinite classification. No installation, download or full Lake build was performed, and no offline self-contained toolchain distribution is claimed.

Receipt qualification: the initial two bootstrap display outputs were truncated by the tool transport; their deterministic reconstructed streams are explicitly labelled in receipts/. All actual Lean compiler streams were captured raw without this limitation.

All audit writes are under this new directory. The project, library, toolchain and packages were not modified.
