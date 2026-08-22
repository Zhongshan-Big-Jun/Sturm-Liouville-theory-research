# Round 3 plugin performance report: DensBC O1' general H

Date: 2026-08-23
Benchmark: DensBC O1' general non-diagonal Hilbert space (beyond H_beta/H_lambda)
Variants:
- baseline: current plugin behavior as-is
- light-reuse: revised lightweight reuse-gate (compact pre-scan, no per-route tags,
  minimum artifact checklist, post-run reuse_summary.md)

## Raw metrics

| Metric | Baseline | Light-reuse | Delta |
| --- | ---: | ---: | ---: |
| Steps | 85 | 50 | -41.2% |
| Tool calls | 106 | 50 | -52.8% |
| LLM time (ms) | 631,667 | 572,115 | -9.4% |
| Tool time (ms) | 245,228 | 129,070 | -47.4% |
| Decode tokens | 63,937 | 61,519 | -3.8% |
| Uncached input tokens | 127,210 | 93,980 | -26.1% |
| Cache-read tokens | 11,861,376 | 4,905,984 | -58.6% |
| Artifact files | 15 | 14 | -6.7% |
| reuse_summary.md | no | yes | n/a |

Approximate wall-equivalent time:

- baseline: ~14.6 min
- light-reuse: ~11.7 min (-20%)

## Mathematical outcome

Both variants produced complementary STRICT partial results on O1'.

### Baseline

- New structure theorem: for a Hilbert space with monomials `x^k = A e_k`,
  `A` bounded invertible and Gram banded, O1' is decidable by
  `closure(span Q_sp) = V <=> ker(T|B_fin) = {0}`.
- Concrete stable banded-shift family `H_shift(m,lambda)` for all bandwidths
  `m>=1`: the finite-rank criterion holds and Pi is dense.
- Bandwidth-2 example: for stable lambda and `v_1 = x^4`, the sparse family is
  never dense in `V = ker M_4` (obstruction `delta_2`).

### Light-reuse

- New weighted shift family `H_{beta,lambda}` with monomials
  `x^k = (k+1)^beta e_k + lambda e_{k+1}`.
- Exact criterion `dense <=> ker(T|B_adm) = {0}`, where `B_adm` includes
  finite runs plus infinite runs exactly when `beta > 3/2`.
- This unifies the previously closed `H_beta` and `H_lambda` cases and is
  complementary to the baseline Toeplitz family.

General O1' remains OPEN.

## Qualitative observations

1. The lightweight reuse protocol was clearly more efficient in this round:
   about 41% fewer steps, 53% fewer tool calls, 59% less cache-read, and 20%
   less wall-equivalent time.
2. It did NOT lose documentation depth: the light-reuse run produced 14
   artifacts including the required minimum set plus `reuse_summary.md`;
   baseline produced 15 artifacts including a Lean scaffold and two scripts.
   The only real artifact gap is the Lean scaffold (light-reuse did not create
   one).
3. The light-reuse agent explicitly avoided re-deriving the master criterion,
   run/free-base machinery, and the closed H_beta/H_lambda cases. It still did
   some targeted reading and one small re-derivation, which are honestly
   recorded.
4. The two runs produced complementary mathematical results rather than the
   same theorem; this is a positive outcome for parallel isolated research.

## Recommendation

The revised lightweight reuse protocol is a net improvement over both round-1
heavy reuse-gate and round-2 hard reuse-gate:

- keep the compact pre-scan (research_map + tool index + LEMMA_INDEX + latest
  final/handoff);
- keep the minimum artifact checklist;
- add a post-run reuse_summary.md;
- ensure at least one Lean scaffold is required for new STRICT results (the
  light-reuse run lacked it; baseline had one).

Suggested future plugin defaults:
- For hard open problems, use the light-reuse protocol as the default.
- Require a minimum artifact set that includes a Lean scaffold or an explicit
  `formalization: scaffold` record even in light-reuse mode.

## Next steps

- Wait for the independent audit of the two round-3 STRICT results.
- If accepted, register the results in research_map/tools/Lean scaffolds and
  commit/push.
- Optionally run a fourth round on a different problem to confirm the improved
  protocol's stability.
