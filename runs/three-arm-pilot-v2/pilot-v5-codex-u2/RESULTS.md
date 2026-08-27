# Pilot v5 final three-arm results

## Bottom line

No arm completed the frozen `C/sqrt(t)` upper bound. The benchmark therefore does not support a
claim that any tested system solved U2.

Arm A and Arm C produced independently audited rigorous partial theorems. Arm B was cheaper and
faster, but its claimed complete proof depended on a strictly false finite-combinatorial lemma.
On this one problem, QED produced the best audited lower constant and was substantially cheaper
than the full research plugin. The research plugin produced the broadest research package and a
somewhat stronger asymptotic logarithmic upper coefficient. One task per arm is a calibration,
not a statistically meaningful ranking of plugins.

## Scored comparison

| Arm | System | Audit label | Strongest audited result | Wall | Uncached input | Output | Cost proxy |
|---|---|---|---|---:|---:|---:|---:|
| A | Our plugin v1.6.0 with subagents | `PARTIAL_NOT_COMPLETE` | `1/(4 sqrt(t)) <= TV`; `TV <= (2 log(t)+15)/sqrt(t)` for `t>=16` | 4052 s root | 1108074 | 390390 | USD 21.7088192 |
| B | Blank Codex | `FATAL_GAP` | Only `1/(4 sqrt(t)) <= TV` and kernel reductions survive | 1254.674 s | 56607 | 40387 | USD 1.2287280 |
| C | QED with offline Codex adapter | `PARTIAL_NOT_COMPLETE` | `1/(2 sqrt(t)) <= TV <= (5+3 log(t))/sqrt(t)` for `t>=1` | 2198.87 s | 131517 | 67782 | USD 1.8848824 |

All scored roles used `gpt-5.6-sol` at `xhigh`. Arm A used seven research child sessions. Arm B
disabled subagents. Arm C used seven sequential QED roles and no model-side tools or subagents.

## Mathematical comparison

### Arm A

Arm A established the largest collection of audited structural results: conditional lamp
uniformity, one-sided translated marginal bounds, exact killed-kernel and coarea reductions, and
a route-specific `Theta(log(t)/sqrt(t))` obstruction. Its upper theorem has logarithmic loss and
the constant-order target remains open.

### Arm B

Arm B claimed constants `c=1/4`, `C=12`, and `t_0=1`. The external audit found a load-bearing
false claim that every parity fiber has at most one change of monotonicity. Exact integer counting
at `(t,w,e)=(48,8,4)` gives consecutive signs `[+,-,+,-]`. The advertised upper bound is therefore
not proved.

### Arm C

QED planned a constant-order range-triple estimate but its prover refused to invent the missing
cross-period cancellation. It instead proved an explicit reflection-coupling bound with one
logarithmic loss. The external audit accepted every stated partial claim, including the improved
lower constant `1/2`, but agreed that the original target remains incomplete.

The project-level audited theorem obtained after combining valid outputs is

```text
1/(2 sqrt(t)) <= TV(P_t^x,P_t^y),                     t>=1,
TV(P_t^x,P_t^y) <= (2 log(t)+15)/sqrt(t),            t>=16.
```

This combines Arm C's stronger lower bound with Arm A's retained upper bound. It is a rigorous
partial theorem, not a solution of the frozen problem.

## Efficiency and behavior

- Arm B used the fewest resources, but lacked a robust internal mechanism for rejecting its false
  key lemma.
- Arm C used about `8.4x` less uncached input and `11.5x` less normalized cost than Arm A while
  producing a valid partial theorem. Its fixed decomposition and structural review prevented a
  false completion claim.
- Arm A spent much more on route diversity, subagent cross-checks, exact replay, research ledgers,
  and reusable artifacts. That extra cost produced more reusable structure, but not closure of
  the main bound on this task.
- Arm C's seven sequential calls produced only seven exposed model responses because model tools
  were disabled. Arm A made 307 model responses and 216 tool calls across eight sessions.

These observations are descriptive for U2 only. They do not establish average performance,
variance, or significance across mathematical tasks.

## Protocol qualifications

Two Arm C launches were excluded before the scored run:

1. Run1 was `INFRA_INVALID` because the adapter exposed nested Web calls during QED Stage 0.
2. Run2 was `INFRA_INVALID` because disabling the Code Mode host also blocked QED roles from
   reading path-only inputs.

The scored run used a disclosed offline I/O adapter that appended the contents of explicitly
named isolated files to QED role prompts. Stage 0 was pre-seeded with neutral metadata, and one
valid YAML response required a format-only normalization after QED's fallback parser selected an
inner Markdown fence. No mathematical text was changed. The prompt probe and sanitized sessions
show no project-context leakage, model tool calls, or network calls.

Arm A spanned two five-hour quota windows. Arm B and scored Arm C each ran in fresh isolated
workspaces. External anonymous audits were post-hoc and excluded from scored usage.

## Reusable output and open obligation

The improved lower bound and all accepted range-translation tools are registered in
`tools/lamplighter-range-translation-tv.md`. The remaining theorem-strength obligation is to prove
an explicit `C/sqrt(t)` upper bound, either through the signed joint range variation or through a
direct comparison after the lamp kernel. Numerical evidence cannot close this obligation.
