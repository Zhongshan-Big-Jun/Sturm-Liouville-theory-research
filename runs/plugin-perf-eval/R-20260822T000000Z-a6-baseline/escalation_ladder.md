# Escalation Ladder

Run: `R-20260822T000000Z-a6-baseline`
Cost tiers used: Tier 0 and Tier 1 only. No Tier 2 (concrete small computation)
or Tier 3 (large multi-route fan-out) was needed.

| Tier | What was done | Trigger | Outcome |
| --- | --- | --- | --- |
| 0 | Read problem statement, source document, tools, research map, relevant existing scripts. | Start of run | Context established; identified root-1 vs root-0 gap. |
| 0 | Fixed-point identity and explicit `a_i` simplification. | Need exact recurrences | Coefficients obtained symbolically. |
| 1 | Symbolic asymptotic expansion of the fixed-point identity; order-by-order coefficient analysis. | Need a mechanism for no-go | Triangularity discovered. |
| 1 | Exact symbolic computation of `F_x` first correction `f_1` for free/rigid branches, both parities. | Need to prove formal uniqueness | `f_1 = -2` (free), `f_1 = 0` (rigid); diagonal coefficients nonzero. |
| 2 | Not used | — | — |
| 3 | Not used | — | — |

## Re-use and re-derivation

- Re-used the existing coefficient definitions from `scripts/op13_general_product_classify.py`
  and the source `a_i` formulas. No new coefficient derivation was needed.
- Re-derived the asymptotic classification independently through the symbolic
  `t` expansion (this is the same first step as `scripts/op13_asymptotic_classify.py`,
  but focused on the free/rigid split).
- Did not use `scripts/op13_4param_reduced.py` as a dependency in the proof; the
  degree-`<=2` family is quoted as already known.
