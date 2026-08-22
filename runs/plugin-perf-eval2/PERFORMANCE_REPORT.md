# Round 2 plugin performance report: B3 fixed-n supremum

Date: 2026-08-22
Benchmark: B3 fixed-n adjacent ratio supremum (global extremality + 2n-root count)
Difficulty: much higher and larger than round 1 A6
Variants:
- baseline: current plugin behavior as-is
- reuse-gate: explicit reuse pre-scan plus REUSE / REUSE_MISS recording

## Raw metrics

| Metric | Baseline | Reuse-gate | Delta |
| --- | ---: | ---: | ---: |
| Steps | 92 | 53 | -42.4% |
| Tool calls | 116 | 61 | -47.4% |
| LLM time (ms) | 940,558 | 796,286 | -15.3% |
| Tool time (ms) | 127,672 | 315,494 | +147.1% |
| Decode tokens | 93,084 | 81,461 | -12.5% |
| Uncached input tokens | 167,798 | 163,017 | -2.8% |
| Cache-read tokens | 15,788,928 | 8,687,488 | -45.0% |
| Artifact files | 20 | 12 | -40.0% |
| Reuse records | not logged | 10 hits / 6 misses | n/a |

Approximate wall-equivalent time (LLM + tool time):

- baseline: ~17.8 min
- reuse-gate: ~18.5 min

## Mathematical outcome

Both variants independently produced the same two STRICT partial results:

1. **Ratio extremizer structure theorem**: every global fixed-n maximizer of
   `lambda_{n+1}/lambda_n` over `1<=rho<=R` is a bang-bang configuration with
   exactly `2n` switches and material order `[1,R,1,...,1]`.
2. **2n-root count theorem**: the balanced alternating secular polynomial
   `F_n(y)` has exactly `2n` simple roots in `(0,pi)` for every `n>=1`, `R>1`.

This closes the project's O3 (2n-root count) and advances B3. O1 (equal-width
optimum / value `c_n(R)`) and O2 (alternating-family monotonicity) remain open.

The reuse-gate run additionally found at least one asymmetric self-consistent
`[1,R,1,...,1]` configuration with a lower ratio, demonstrating that
self-consistency alone does not force equal widths.

## Qualitative observations

1. On this harder problem, the reuse-gate run used substantially fewer model
   steps and tool calls, and about 45% less cache-read tokens, while the
   wall-equivalent time was roughly the same.
2. The reuse-gate run still independently re-derived both STRICT theorems, so
   it did not avoid duplicate mathematical work. Its efficiency came from a
   more focused path and from discovering the baseline run mid-flight for
   cross-checking.
3. The baseline run produced a more complete documentation package: audit
   report, obligation graph, repro manifest, counterexample log, and more
   scripts. The reuse-gate run stopped at a resource boundary with a handoff
   and fewer standard artifacts.
4. This suggests a trade-off: on hard/large problems, reuse-gate can reduce
   token/cache and model steps, but may trade away documentation depth unless
   paired with a minimum artifact checklist.
5. The per-route REUSE/MISS recording overhead was smaller in absolute terms
   than in round 1, but still contributed to the longer tool-time.

## Recommendation for plugin changes

- P1: Keep a lightweight reuse pre-scan, but require a minimum artifact set
  even in reuse-gate mode: `problem_contract.md`, `candidate_proof.md`,
  `obligation_graph.md`, `audit_report.md` (or an explicit audit note),
  `final_report.md`.
- P2: Make cross-run discovery explicit: when a sibling run is found, record
  it as `REUSE_EXTERNAL` and either deep-reuse it or clearly state what was
  re-derived independently.
- P3: Move per-route REUSE recording to a post-run summary instead of
  requiring it during every route; keep only actual reuse actions.
- P4: Track "wasted duplicate work" separately from reuse hits: if an agent
  re-derives a result that already exists in the project, that should be
  counted as a negative reuse event and trigger a warning.

## Next steps

- Wait for the independent audit of the two STRICT results.
- If accepted with repairs, register the results in research_map/tools/Lean
  scaffold and commit/push.
- Seed a follow-up experiment on O1/O2 or on a different hard problem to test
  the lightened reuse protocol.
