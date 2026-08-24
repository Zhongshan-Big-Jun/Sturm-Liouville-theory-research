# DeepSeek-adapted system test: Batchelor-scale liminf

Date: 2026-08-25
Problem: QED analysis-Apr-24 problem 4 (`Batchelor-scale liminf`), unpolluted and hard.
Goal: after separating DeepSeek-adapted copies and preserving original configs, run the adapted external systems on a new hard problem.

## Adaptation separation (user request)

Original repositories preserved (configs restored / not further modified):

- Rethlas: `F:\tools\rethlas-clone\Rethlas`
- Danus: `F:\tools\danus-clone\Danus` (back on `main`)
- MMAT: `F:\tools\mmat-agent-team`

DeepSeek-adapted copies (labeled with `DEEPSEEK-ADAPT.md`):

- Rethlas: `F:\tools\rethlas-deepseek`
- Danus: `F:\tools\danus-deepseek`
- MMAT: `F:\tools\mmat-deepseek`

Global label: `F:\tools\DEEPSEEK-ADAPT-README.md`.

Adaptation verified:
- Rethlas verification service now returns `verdict: correct` for a trivial proof (previously HTTP 500).
- Danus doctor: codex API ping ok, verify service up.
- MMAT dependencies installed and writable workspace created.

## Test results (31-minute cap)

| Arm | System | Outcome | Independent review |
|---|---|---|---|
| A | local plugin v1.6.0 | `RIGOROUS_PARTIAL_RESULT`; proves special cases and reduces to an open per-mode Batchelor lemma | PARTIAL_NOT_COMPLETE | 
| B | blank control | Uses stated external Batchelor-scale theorem, not reproved; not fully self-contained | REPAIRABLE_GAP |
| C | Rethlas DeepSeek-adapted | No final result within cap; iter0 still running at stop, no blueprint | n/a |
| D | Danus DeepSeek-adapted | No verified fact within cap; workers in round 1 | n/a |
| E | MMAT DeepSeek-adapted | Progressed to sketch phase (`STATUS.md`, queue), no complete proof within cap | n/a |

## Local A/B metrics

| Arm | Wall (s) | Steps | Tool calls | Input tok | Cache tok | Output tok | Artifact (no task) |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 1042.7 | 38 | 38 | 42,522 | 3,059,840 | 103,207 | 18,099 B |
| B | 832.0 | 13 | 12 | 77,033 | 577,280 | 82,169 | 15,693 B |

## External attempt metrics

- Rethlas adapted: ~31 min wall, iter0 log ~135 KB, no blueprint.
- Danus adapted: ~31 min wall, two workers round 1, no facts in fact graph.
- MMAT adapted: ~31 min wall, workspace with `STATUS.md` and sketch-phase queue, no proof artifacts.

## Interpretation

The adapted systems are operational on DeepSeek (verifier works, workers/harness start and create artifacts). The Batchelor problem was too hard for all three external systems to close within the 31-minute cap; this is a problem-difficulty result, not an adaptation failure. Local A gave a partial result; B gave an argument relying on an external theorem.
