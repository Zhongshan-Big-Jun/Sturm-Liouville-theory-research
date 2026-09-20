# Fourth-round scoped Lean author delivery

41 theorems and 23 definitions compiled with native Lean 4.31.0. The actual imported root object was inspected; all 64 declaration closures were exported and independently recomputed from the dependency graph. The union of axioms is {propext, Classical.choice, Quot.sound}; no missing/unsafe node or sorryAx occurs in the inspected closure.

- Source: `/mnt/f/LaTeX/BVE research/lean-proof/SL/AuditRound4.lean`.
- Exact scope and exclusions: `CONTRACT.md`.
- Compiler/run summaries: `FINAL_CHECKS.json`, `command-index.json`, and unabridged `logs/`.
- Actual declarations and definitions: `final/declarations.json`, `final/formal-statements*.txt`, `final/local-definition-closure.txt`.
- Root identity before/after inspection and controls: `root-object-bindings.json`.
- Loaded environment: `environment.json`, `final/loaded-modules.json`, `final/module-artifact-hashes.json`.
- Blind readback entry: `final/READBACK_INPUTS.json`.
- Separate semantic review entry: `SEMANTIC_REVIEW_INPUTS.json`.
- Parallel-author coordination: `COORDINATION.md`.

Both intentional negative controls fail at False, while paired positive controls pass. The hand-written input contracts pass after recorded simplification repairs. Fresh compilation into a second external directory produces identical root bytes. All 44 prior project Lean sources remain byte-identical.

The original broad Mathlib import was cancelled. Four external source copies change only that import header and were freshly compiled; their mathematical bodies are byte-identical to the original files. The exact adapted-source/module provenance is disclosed in DEPENDENCY_ADAPTATION.json. No old project build object is on LEAN_PATH. All 3217 actually loaded modules and 12853 available artifact files are hash-pinned. No whole Lake build or download ran.

All failed source attempts, full Lean execution records, and the cancelled import are retained. One harmless linter warning remains; it does not affect theorem closure. The separate inline Python ordering diagnostic failure is recorded explicitly and the corrected set-based graph check passes.

This is author evidence ready for review, not independent acceptance. Concrete parity/moment results are rational-valued. General difference and reduction theorems are field-polymorphic. Sobolev/quotient convergence, analytic tail series and asymptotics, minimality, K(c), and all-degree rational classification are excluded. No docs, cards, statuses, AGENTS.md, canonical data, plugins, or git state were modified by this author.
