# Arm C initial launch classification

Status: `INFRA_INVALID`, excluded from scoring.

The process exited before any model was created because QED commit `1219009` checks for a command
named `claude` unconditionally. The frozen configuration assigned every active role to Codex.

Evidence:

- `pipeline.log` contains only `ERROR: Missing required tools: claude` and the installation hint.
- No `wrapper.log` exists.
- No Codex session JSONL exists under the initial `codex-home-c`.
- No mathematical output was produced.

The preregistration records the fail-closed shim and fresh-root replacement.
