# v1.9 quota recovery drill results

## Verdict

`PASS`.

The released v1.9 recovery protocol reconstructed and closed a real historical
five-hour quota interruption without replaying a transcript, launching a model,
starting a sub-agent, using the network, or changing any historical benchmark
artifact. The mathematical label remains `RIGOROUS_PARTIAL_RESULT`, and the
fixed-constant `C/sqrt(t)` upper bound remains open at `O3`.

## Frozen subject

- Source run: `R-20260827T063025Z-u2-v17-regression`.
- Drill run: `R-20260829T014000Z-v19-recovery-drill`.
- Source commit: `0d25f52c8f40e590dde7e285e7b367064f2a0f0f`.
- Recovery script SHA256:
  `be6e1d6cad3089451c9213c6f81b3a4ec962d9c939de5aa71fd63f5a7ab9dc1a`.
- Classification: `PROGRAM_ONLY`, files only, unscored.

## Segment 00

The first checkpoint reconstructs the recorded quota boundary.

| Operation | Verdict | Checked artifacts | Wall time |
| --- | --- | ---: | ---: |
| Seal | `SEALED` | 10 | 271.630 ms |
| Verify | `READY` | 10 | 263.165 ms |
| Resume | `RESUME_READY` | 10 | 247.867 ms |

- Checkpoint ID:
  `sha256:3f34de576ba1e195716822533c9eb30a47627bc61cba402c05b243407d34e78d`.
- Checkpoint file SHA256:
  `e4495641353d620470261a4361278badb004ca170c640b51242c375399a4434e`.
- Canonical receipt SHA256:
  `bffc6243dbea008d3322f5292cf2e188365e54cdf483769822a1cbf80205c2ad`.
- First action: `RECONCILE_INFLIGHT` for `route-b-operator`.
- Worker session:
  `01a04203-2e61-7293-b637-4a6f4a313c06`.
- Minimal read set: `task_contract.md` and `whiteboard-00.md` only.

The reconstructed cumulative historical metrics are 56 model responses, 44
tool calls, 211820 uncached input tokens, 1702912 cached input tokens, 101940
output tokens, 1311.844 root wall seconds, and USD 3.5672448 proxy cost.

## Segment 01

The successor records the same Route B worker and session as `NO_RETURN`, binds
the predecessor checkpoint and its canonical receipt, and converges without
relaunching any route.

| Operation | Verdict | Checked artifacts | Wall time |
| --- | --- | ---: | ---: |
| Seal | `SEALED` | 13 | 261.273 ms |
| Verify | `READY` | 13 | 250.623 ms |

- Checkpoint ID:
  `sha256:04632ea0aab7abb70ed4a549112138afb18742b46ae2a13960d9910ee1d7624d`.
- Checkpoint file SHA256:
  `1e886ab7a11102df3c30de5782484c13b1b2c372d63af46e2b83a279abe488b2`.
- Route B reconciliation: `NO_RETURN`.
- Final first action: `AWAIT_INPUT`.
- Minimal read set: `task_contract.md` and `whiteboard-01.md` only.
- No successor receipt was created because the preregistered stop condition was
  the segment 01 `READY` verdict.

The preserved final cumulative historical metrics are 72 model responses, 58
tool calls, 338812 uncached input tokens, 3287040 cached input tokens, 125692
output tokens, 1881.050 root wall seconds, and USD 5.183904 proxy cost. These
are copied from the frozen source run and are not drill consumption.

## Overhead and integrity

- Total measured deterministic drill overhead: 1294.558 ms.
- Drill model responses: 0.
- Drill sub-agent sessions: 0.
- Drill network calls: 0.
- New proof or audit calls: 0.
- Historical scored metrics changed: no.
- Historical benchmark artifacts edited: no.
- Repeated completed action IDs: none.
- Result-status transition: none.

All six preregistered pass criteria are met. The checkpoint lineage preserves
the completed Route A and Route C obligations, records Route B exactly once as
`NO_RETURN`, carries the final external audit, and leaves `O3` explicitly open.
The deterministic recovery mechanism therefore prevents a quota reset from
causing duplicate sub-agent work or transcript-replay overhead in this case.

Both checkpoint verifications and all 11 frozen artifact hashes passed on the
final replay. `git diff --check` also passed. The generic program validator
returned `INVALID` because the repository at `HEAD` already lacks the required
Blueprint knowledge files and contains historical protected artifacts outside
its registered upstream-run layout. This is a project-wide pre-existing
condition, not a drill regression; it was not repaired because the files-only
drill does not authorize a repository migration. Exact evidence is recorded in
`VALIDATION.md`.

## Limitations

This is a deterministic reconstruction over frozen real-run artifacts, not a
second live service interruption. It tests checkpoint integrity, lineage,
minimal restart context, and duplicate-work prevention. It does not measure the
quality of a model response after recovery and does not add mathematical
evidence.

The project-wide current research state was intentionally not changed because
this drill is plugin infrastructure validation and authorizes no new research.
