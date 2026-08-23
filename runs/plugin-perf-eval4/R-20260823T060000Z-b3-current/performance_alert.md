# Performance alert

- Run ID: runs/plugin-perf-eval4/R-20260823T060000Z-b3-current
- Variant: current-v1.5.0
- Problem class: hard
- Baseline ID: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline
- Alert level: INFO

## Changed metrics

| Metric | Run | Baseline | Delta |
| --- | ---: | ---: | ---: |
| steps | 77 | 92 | -16.3% |
| tool_calls | 81 | 116 | -30.2% |
| uncached_input_tokens | 106210 | 167798 | -36.7% |
| cache_read_tokens | 8251520 | 15788928 | -47.7% |
| wall_ms | 833661 | 1068230 | -22.0% |
| artifact_count | 12 | 19 | -36.8% |
| duplicate_work_count | 0 | 0 | n/a |

## Output/artifact assessment

- Did mathematical output improve, stay similar, or degrade? (needs run-level judgement)
- Did documentation/artifact completeness improve, stay similar, or degrade?
- Is the change plausibly explained by problem difficulty or class?

## Candidate interpretation

The alert is a candidate, not a verdict. A single run may be misleading.
Confirm before changing a protocol based on this alert.

## Next checks

- [ ] Repeat the same variant in the same problem class.
- [ ] Repeat on a different problem class with a comparable baseline.
- [ ] Inspect `reuse_summary.md` for duplicate work or avoided work.
- [ ] Re-run after any intended protocol/config change.

