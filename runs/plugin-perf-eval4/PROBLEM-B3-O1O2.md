# Current-plugin performance benchmark: B3 remaining O1/O2

Project: Sturm-Liouville spectral optimization (MRP-20260731-BVE-SL)
Local root: F:\LaTeX\BVE research

## Why this benchmark

This is a continuation of the round-2 B3 benchmark. Round 2 produced two STRICT
results (ratio extremizer structure + 2n-root count, closing O3). The remaining
open obligations are O1 and O2:

- O1: prove that among all `[1,R,1,...,1]` bang-bang configurations with exactly
  2n switches, the equal-width balanced configuration is optimal, i.e. the
  supremum value is `c_n(R)`.
- O2: prove that inside the one-parameter equal-within-type alternating family,
  the ratio `lambda_{n+1}/lambda_n` is maximized at `w_1/w_2 = sqrt(R)`.

This benchmark tests the current v1.5.0 plugin (lightweight reuse protocol +
performance observability) on a hard open continuation problem with an existing
comparable baseline from round 2.

## Output

Rigorously attack O1/O2. Any strict partial result, structure theorem,
counterexample, or honest negative/blocked route is valuable. Follow the
lightweight reuse protocol:

- compact pre-scan (research_map, tools/README, LEMMA_INDEX, latest B3
  final/handoff);
- no per-route REUSE tags;
- write minimum artifacts including `reuse_summary.md`;
- write Lean scaffold if a new STRICT/partial result is produced.

Status labels must follow the rigorous-open-math-research output protocol.
