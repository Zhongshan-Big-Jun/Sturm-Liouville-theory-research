# Plugin performance report: v1.10 recovery usability

Date: 2026-08-30.

## Scope

This is a deterministic recovery-usability regression, not a scored
plugin-versus-control mathematics benchmark. It uses no research-model call and
makes no claim about mathematical solver quality.

The regression targets three defects observed during the v1.9 live recovery
run `R-20260830T020000Z-g1p-live-recovery`:

1. editing checkpoint-bound whiteboard or closure files made a predecessor
   checkpoint stale;
2. project-prefixed relative paths could duplicate the project root;
3. PowerShell seven-digit fractional timestamps could be rejected;
4. a sharper open obligation required manual old-ID preservation and
   `do_not_repeat` repair.

## v1.10 changes

- `checkpoint_resume.py advance` verifies the predecessor checkpoint/receipt,
  copies mutable whiteboard and closure bindings to the next numbered paths,
  rewrites exact bindings, and writes a guarded next-state draft.
- `advance_draft=true` is a deterministic seal blocker until the semantic delta
  is finalized.
- Path resolution accepts project-relative paths and unambiguous cwd-relative
  paths already prefixed by the project directory.
- Canonical UTC timestamps are available by default; explicit ISO-8601 input
  accepts seven fractional-second digits.
- Typed `REFINES` and `SUPERSEDES` obligation lineage automatically retires and
  propagates predecessor actions without retaining the old open ID.

## Real-artifact replay

Replay root: `F:/benchmark/V110-RECOVERY-REPLAY-20260830-01`.

Input: a byte copy of the v1.9 G1 prime live recovery scoped workspace.

Observed results:

- v1.9 checkpoint sequence 01 verified `READY` under v1.10.
- The `advance` command accepted project-prefixed relative paths and
  `2026-08-30T16:00:00.1234567+08:00`.
- It produced sequence 02 with verdict `ADVANCE_DRAFT_READY`.
- `whiteboard-02.md` matched `whiteboard-01.md`, SHA256
  `37d3977f9e99ddd3804970e388ace546c0e79ba3d88c5c32e9894d0e079fd23b`.
- `closure_gate-02.md` matched `closure_gate-01.md`, SHA256
  `71261e957d6d900509d570976a7c919f58824f79e332d9a50fa7fb1de79091f3`.
- The predecessor checkpoint remained `READY` after advance.
- Sealing the unfinished sequence 02 draft failed with the expected
  `advance draft must be finalized` guard.
- Worker restarts, model calls, research dispatches, transcript replay, and
  network calls inside the replay were all 0.

## Static context cost

| Entrypoint | v1.9 bytes | v1.10 bytes | Delta |
| --- | ---: | ---: | ---: |
| workflow `SKILL.md` | 31818 | 31701 | -117 |
| rigorous `SKILL.md` | 13618 | 13731 | +113 |
| combined | 45436 | 45432 | -4 |

The new behavior therefore did not increase the combined always-loaded static
entrypoint size. Detailed mechanics remain behind the quota-recovery reference.

## Validation

Parent plugin repository:

- `validate_all.py`: 81/81 PASS.
- Smoke tests: 11/11 PASS.
- Plugin validators: 2/2 PASS.
- UTF-8 skill validators: 2/2 PASS.
- Python compile and `git diff --check`: PASS.
- Release commit: `dff224887210de731ef4ca455aefcc0e10f5f84c`, pushed to
  `xsoc1/rigorous-open-math-research` and
  `Zhongshan-Big-Jun/rigorous-open-math-research`.

DSH repository:

- `validate_all.py`: 51/51 PASS.
- Smoke tests: 15/15 PASS.
- Bundle gate: PASS.
- Upstream sync check: clean at parent `dff2248`, 107 locked files.
- Release commit: `09aa74d`, pushed to `xsoc1/math-research-dsh`.

Local Codex installation:

- `math-research-workflow@math-research`: installed and enabled at 1.10.0.
- `rigorous-open-math-research@math-research`: installed and enabled at 1.10.0.

## Verdict

`PASS_WITHOUT_MATHEMATICS_BENCHMARK`.

The four observed v1.9 recovery usability defects now have deterministic
implementation and regression coverage. No three-arm mathematics benchmark is
warranted for this release because the changes do not alter route selection,
proof synthesis, or audit policy.
