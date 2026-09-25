# Round10 evidence entry

Current conclusions and limits are in [the report](../../../reports/proof-audit-round10-20260925/REPORT.md). This directory preserves submitted evidence, actual old failures, author attempts, current proof, independent checks and correction receipts separately.

- `analytic-repair.md`: current analytical contract; old rejected text remains under `author-development/mathematical-first-review/` and its original frozen packet.
- `software-review/`, `software-execution/`: independent review and actual executions of the unchanged final Python sources. Its older analytical snapshot is not approval of the subsequently corrected signed-step sentence.
- `formal-readback/`: blind38-declaration translation; `formal-comparison/` and `formal-execution/`: different reviewer's actual compilation and semantic comparison. Local scope only.
- `lean-author/`: original author machine evidence, including stale first exact-root run. Large JSON evidence uses lossless gzip with both hashes recorded in manifests.
- `pdf-reviewed-final/`: build record and inspected pages for the current active PDF. Earlier `pdf-final/` and `pdf-evidence/` are superseded build evidence, retained as history.
- `integration/`: original API results,15 current exact obligations, actual query, warnings and version-bound annotations. Earlier unchanged-card releases became stale after the independent mathematical review's document corrections and were renewed.
- `replays/`, `checks/`, `caller-inventory.json`: actually rerun configurations and exact current static caller identities. Historical experiments outside this scope are not revalidated.
- `coordinator/`: task-specific external helpers as used; they are not new generic plugin infrastructure. Replay into a new private output directory, following each command's inputs/environment, rather than overwriting old paths.

The final scoped publication manifest lives with the report. Canonical and historical project artifacts retain baseline bytes. Compiler success, blind readback, analytic review, numerical observations and library release are distinct evidence levels.
