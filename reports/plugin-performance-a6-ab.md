# Plugin performance A/B report: A6 rational product solutions

Date: 2026-08-22
Benchmark: single unsolved A6 sub-problem (higher-degree rational product
solutions on the root-1 branch)
Variants:
- baseline: current plugin behavior as-is
- reuse-gate: explicit mandatory reuse pre-scan with REUSE / REUSE_MISS records

Both runs used fresh isolated subagents, same problem statement, separate run
roots, and no nested subagents. Metrics were collected from DSH session
statistics, raw session logs, and the agents' performance_log.md files.

## Raw metrics

| Metric | Baseline | Reuse-gate | Delta |
| --- | ---: | ---: | ---: |
| Steps | 40 | 53 | +32.5% |
| Tool calls | 46 | 67 | +45.7% |
| LLM time (ms) | 571,242 | 578,382 | +1.2% |
| Tool time (ms) | 310,490 | 568,833 | +83.2% |
| Decode tokens | 61,468 | 60,763 | -1.1% |
| Uncached input tokens | 56,739 | 114,304 | +101.5% |
| Cache-read tokens | 2,996,352 | 6,185,600 | +106.4% |
| Artifact bytes | ~24,156 | ~38,695 | +60.2% |
| Reuse records | not logged | 12 hits / 4 misses | n/a |

Note: total wall time is approximated as LLM time plus tool time because DSH
session cache does not expose a single start/end wall clock for subagents in
this run. The reuse-gate run also included two 120-second timeout attempts on
existing degree-test scripts.

## Mathematical outcome

Both variants produced the same scoped STRICT partial result:

- On the root-1 branch (`e_j -> 1`), every rational product ratio has reduced
  degree at most 2 for both even/odd recurrences and all `c > 0`;
- no higher-degree rational product solution exists on the root-1 branch;
- root-0 / minimal branch remains open.

The baseline used an asymptotic triangularity argument. The reuse-gate run
used an exact diagonal-coefficient lemma and additionally re-used the baseline
verification script. Both are self-audited only; an independent audit was
dispatched separately (see `R-20260822T000000Z-a6-audit`).

## Qualitative observations

1. The reuse-gate pre-scan added a real cost: roughly double the uncached
   input and cache-read tokens, 46% more tool calls, and about 30% more
   wall-equivalent time.
2. It did not reduce duplicate mathematical work in this pilot. The baseline
   re-derived some constants that already existed in scripts; the reuse-gate
   run also re-ran them and spent 240s on timeout attempts.
3. A false REUSE_MISS occurred because the reuse agent checked the sibling
   baseline run before its candidate_proof.md/final_report.md existed. This
   is a timing artifact, not a real gap.
4. The reuse-gate did improve artifact explicitness: the
   diagonal-coefficient lemma and its exact sympy verification script are
   cleaner and more auditable than the baseline asymptotic argument. This is a
   qualitative benefit that raw token metrics do not capture.
5. The current reuse-gate as specified is too heavy to recommend as a hard
   mandatory protocol. It should be lightened, and reuse should be evaluated
   post-run rather than as a per-route upfront scan.

## Candidate plugin improvements from this pilot

- P-A: Replace the per-route mandatory reuse scan with a single cheap Tier 0
  read list: `research_map.md`, `tools/README.md`, `lean-proof/LEMMA_INDEX.md`,
  plus the latest relevant run `final_report.md` when available.
- P-B: Do not require REUSE / REUSE_MISS lines for every attempt; record only
  actual reuse actions and a short "duplicate-work" note after the run.
- P-C: When running A/B variants in parallel, do not expect one variant to
  reuse the other's in-flight artifacts; either serialize proof artifact
  creation or treat cross-run reuse as a bonus, not a requirement.
- P-D: Keep full script/context re-reads out of the pre-scan; read summaries
  first and full scripts only on demand.
- P-E: Add a post-run distillation step that turns the more explicit
  reuse-gate artifacts into a reusable tool/lemma entry, so the extra tokens
  spent on explicit recording produce a downstream asset.

## Next steps

- Wait for the independent audit of the root-1 no-go.
- If accepted, register the result as A6 partial progress, create a Lean
  scaffold, update research_map/tools, and add the performance conclusions to
  the plugin-management backlog.
