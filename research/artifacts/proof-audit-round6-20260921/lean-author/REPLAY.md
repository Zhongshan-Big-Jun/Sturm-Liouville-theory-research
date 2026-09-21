# Replay the exact author target

From WSL, with the original pinned Windows Lean and package cache still present:

```bash
python3 -B /mnt/f/tools/math-audit-round6-20260921/lean-author/replay.py /mnt/f/tools/CHOOSE_A_NEW_OUTPUT_DIRECTORY
```

The output directory must not already exist. The script checks frozen source,
contract, tool and runtime hashes, rebuilds both local Lean modules in the new
output, runs the maintained exact-root verifier and both controls, exports
actual public types/reachable definitions/axioms, and records root resolution.
It changes no source, pin, package, plugin or previous object. It uses package
cache artifacts without downloading or rebuilding all Mathlib.

For execution clients that may terminate a long foreground command, use the
optional durable wrapper. The checking command and frozen replay.py are the
same:

```bash
python3 -B /mnt/f/tools/math-audit-round6-20260921/lean-author/launch_replay.py /mnt/f/tools/CHOOSE_A_NEW_OUTPUT_DIRECTORY --job-id CHOOSE_A_UNIQUE_JOB_ID
```

This dispatches a local process through the installed workflow job supervisor;
it does not spawn an agent. Read status using the unchanged installed tool:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B /mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.0/scripts/research_state.py status --project /mnt/f/tools/math-audit-round6-20260921/lean-author --job-id CHOOSE_A_UNIQUE_JOB_ID
```

The mathematical result is in the new directory's `REPLAY_RESULT.json` and
`positive/run-manifest.json`, not inferred from job status alone. The negative
manifest must report `target_mismatch` with machine execution successful; its
strict verifier exit 1 is expected. A missing receipt or interrupted process
is incomplete evidence. Full command logs and generated Lean probes are kept.

For blind readback use `HANDOFF.json`'s blind list, governed by
`HANDOFF_RULES.md`. Do not supply full R5 source, intended comments or proofs in
that packet. Full unchanged R5 source is available for semantic/execution work.

The optional `check_receipt.py OUTPUT_DIRECTORY` consumes and checks an existing
positive receipt. It does not rerun the kernel proof. The actual replay above
already performs a new compile and the complete module inventory; redundant
per-theorem environment dumps are unnecessary.
