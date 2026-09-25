# Local replay instructions

All commands below run from `/mnt/f/tools/math-audit-round10-20260925/formal-author/`. This workspace uses an existing Windows Lean 4.31.0 executable from WSL. No Lake build, package download, project write or old-run rewrite is required. Existing labels are immutable; choose a new label on every replay.

```bash
python3 -B run.py version replay-version-02
python3 -B run.py compile replay-source-02
python3 -B launch_frozen.py replay-root-03
```

The exact-root launcher dispatches a durable local job on the frozen minimal root-project, then exits. Launcher exit 0 only means dispatch. Actual completion is recorded in `.research-state/jobs/replay-root-03-durable.json`, `commands/replay-root-03/command.json` and `evidence/replay-root-03/run-manifest.json`. Inspect their real completed status and compiler output. Do not edit any file under root-project; the first historical root run against the changing development project was correctly marked stale.

For a direct foreground exact-root run with a new output label:

```bash
python3 -B verify_frozen.py replay-root-04
```

To replay controls against the newly compiled module, specify its object directory label as the last argument. The controls themselves import the actual AuditRound10 declaration.

```bash
python3 -B run.py compile replay-refutations-02 Counterexamples.lean replay-source-02
python3 -B run.py compile replay-negative-flip-02 NegativeFlip.lean replay-source-02
python3 -B run.py compile replay-negative-reflection-02 NegativeReflection.lean replay-source-02
python3 -B run.py compile replay-negative-index-02 NegativeIndex.lean replay-source-02
python3 -B run.py compile replay-print-main-02 PrintAuditRound10.lean replay-source-02
python3 -B run.py compile replay-print-controls-02 PrintCounterexamples.lean replay-source-02 replay-refutations-02
```

Counterexamples and print files should exit 0. Each Negative file should exit 1 at a false mathematical goal; an import error, syntax error, timeout or missing tool does not count as the desired negative observation. Use the exact command/environment records as the authority. The original control run additionally snapshots its imported local objects.

`ReadbackExport.lean` writes to the literal output path encoded in it. Its completed output is frozen evidence; for a later export first make a new source with a new output path, then compile that new source under a fresh label. Do not overwrite the delivered formal-declarations.json.

The installed verifier is `/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.1/scripts/verify_lean_project.py`. The runner uses `--direct --strict-exit --contract root-contract.json`, the explicit Lean and Lake executable paths, and the read-only package paths listed in every command.json. Python bytecode and temporary files are confined by the runner. Exact-root checks are author-side machine checks; independent semantic reviews are separate work.
