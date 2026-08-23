# Current-plugin performance report: B3 O1/O2 benchmark (v1.5.0)

Date: 2026-08-23
Benchmark: B3 remaining O1/O2 (continuation of round-2 hard problem)
Plugin version: v1.5.0 (lightweight reuse protocol + performance observability)
Run: `R-20260823T060000Z-b3-current`

## Raw metrics vs round-2 B3 baseline

| Metric | Current v1.5.0 | Round-2 baseline | Delta |
| --- | ---: | ---: | ---: |
| Steps | 77 | 92 | -16.3% |
| Tool calls | 81 | 116 | -30.2% |
| Uncached input tokens | 106,210 | 167,798 | -36.7% |
| Cache-read tokens | 8,251,520 | 15,788,928 | -47.7% |
| Output tokens | 62,664 | 93,084 | -32.7% |
| Wall time (LLM+tool ms) | 833,661 | 1,068,230 | -22.0% |
| Artifact files | 12 | 19 | -36.8% |

Performance alert: **INFO** (no regression).

## Mathematical outcome

- New STRICT: general equal-within-type alternating Chebyshev secular
  representation
  `(M_n)_{0,1} = sin(p)U_n(m) + (sin q / s)U_{n-1}(m)`.
- New STRICT corollary: any global maximizer has equal amplitudes of `u_n`
  and `u_{n+1}` on each constant block (from `E=0`).
- New STRICT fixed-delta Chebyshev root-location lemma for `0<delta<1`.
- O2 route reduction: elliptic-region secular equation reduces to
  `sin((n+1)theta) + delta(x) sin(n theta) = 0`; exact remaining gap is the
  x-dependence of `delta`.
- O1 still open; O2 still open.
- No previous B3 STRICT results were downgraded.

## Performance observability output

`performance_alert.md` generated with level INFO:

- All major cost metrics improved vs round-2 baseline;
- artifact count lower but minimum artifact set was satisfied;
- alert correctly classifies this as no regression rather than WARN.

## Notes

- The lightweight reuse protocol successfully reused round-2 B3 tools and
  avoided a full library-scan; runtime used fewer steps/tool calls/cache than
  round-2 baseline on the same problem.
- The current benchmark also produced a new reusable tool
  `tools/general-alternating-secular-chebyshev.md`.

## Next steps

- If this is to be registered as a new partial result, the STRICT subset has
  passed an independent audit after repair; general O1/O2 remain open.
- Suggested follow-up: use the general alternating Chebyshev representation to
  attack O2 by handling the x-dependence of `delta`.
