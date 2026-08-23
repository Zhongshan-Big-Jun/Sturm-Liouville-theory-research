# Performance alert

- Run ID: runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse
- Variant: reuse
- Problem class: easy
- Baseline ID: runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline
- Alert level: WARN

## Changed metrics

| Metric | Run | Baseline | Delta |
| --- | ---: | ---: | ---: |
| steps | 53 | 40 | +32.5% |
| tool_calls | 67 | 46 | +45.7% |
| uncached_input_tokens | 114304 | 56739 | +101.5% |
| cache_read_tokens | 6185600 | 2996352 | +106.4% |
| wall_ms | 1147215 | 881732 | +30.1% |
| artifact_count | 9 | 10 | -10.0% |
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

