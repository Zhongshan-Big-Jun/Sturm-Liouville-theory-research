# rigorous-open-math-research v1.6.0 Codex context optimization

Date: 2026-08-24

Parent plugin commit: `88e1c970b3bec580429a968b5015ac58c0404e67`

DSH adapter commit: `0cc9961`

## Optimization basis

This revision used the four existing benchmark reports as its empirical basis:

- `plugin-performance-a6-ab.md`
- `plugin-performance-b3-ab.md`
- `plugin-performance-o1p-ab.md`
- `plugin-performance-b3-o1o2-current.md`

The evidence showed that heavy mandatory reuse can increase context and tool cost on a bounded problem, while lightweight targeted reuse can reduce cost on a harder problem. The v1.6.0 design therefore keeps evidence gates and explicit mathematical decisions, but reduces always-loaded instructions and makes reuse adaptive.

The Codex execution guidance also follows the official OpenAI recommendation to use leaner prompts, remove repeated instructions, batch bounded tool work where supported, and reconstruct state from artifacts when context grows. See [OpenAI model optimization guidance](https://developers.openai.com/api/docs/guides/latest-model).

## Static context result

`EVIDENCE`: The following byte counts were measured from the plugin skill entrypoints before and after the change. This is static context evidence, not a full mathematical runtime benchmark.

| Entrypoint | v1.5.0 bytes | v1.6.0 bytes | Change |
|---|---:|---:|---:|
| rigorous-open-math-research | 19,618 | 11,184 | -43.0% |
| math-research-workflow | 37,819 | 29,426 | -22.2% |
| manage-math-research-program | 44,062 | 37,974 | -13.8% |
| lean-verify | 22,944 | 19,218 | -16.2% |
| Total | 124,443 | 97,802 | -21.4% |

## Implemented changes

- Moved historical changelogs out of all four always-loaded `SKILL.md` files and kept explicit history pointers.
- Repaired an unbalanced Markdown fence introduced by the earlier rigorous skill split. The defect could place anti-patterns and the minimal invocation example inside a code block.
- Added repository validation for balanced Markdown fences, changelog routing, and entrypoint byte budgets.
- Added a Codex fast path for one-time indexed discovery, targeted file slices, bounded batching of independent deterministic work, explicit semantic decision boundaries, and artifact-based reconstruction before compaction.
- Replaced a request for compact chain-of-thought with a compact decision summary.
- Repaired Chinese UI mojibake in plugin manifests.
- Isolated the doctor smoke test from the user's active `CODEX_HOME`.
- Updated all four plugin packages and the DSH adapter to v1.6.0.

## Validation

`EVIDENCE`: All listed checks passed.

- Parent repository: 81 of 81 aggregate validation checks.
- Parent repository: 4 plugin validations and 4 skill validations.
- Parent repository: 9 smoke tests.
- DSH adapter: 51 of 51 aggregate validation checks.
- DSH adapter: bundle validation, sync verification, and 13 smoke tests.
- Local Codex installation: all four v1.6.0 packages installed and enabled. Workflow doctor returned 0 problems, 0 warnings, and 6 successful checks.

## Honest performance status

`EVIDENCE`: The 21.4% reduction in total static skill entrypoint size is verified. The protocol defect fixes and regression gates are also verified.

`OPEN`: No new controlled end-to-end mathematics A/B run comparing v1.5.0 and v1.6.0 was executed in this revision. Therefore no claim is made here that v1.6.0 has already reduced runtime tokens, tool calls, wall time, or improved mathematical success rate.

The next performance run should replay one bounded B3 task and one O1' task under the same model, reasoning effort, starting artifacts, and acceptance contract. It should compare mathematical outcome, independent audit result, uncached input, cache read, output tokens, tool calls, steps, and wall time.
