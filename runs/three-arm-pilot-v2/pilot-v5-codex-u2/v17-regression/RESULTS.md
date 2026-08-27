# Pilot v5 v1.7 closure-first regression results

## Status

`PAUSED_QUOTA_WITH_AUDITED_PARTIAL_RESULT`.

The scored solver reached the service-enforced five-hour limit after 1311.844
seconds. It had completed two of three research routes and written a live
candidate proof, but had not written a final response or performed its own
global package audit. A post-hoc independent neutral audit, excluded from
scored usage, returned `PASS` for every retained partial theorem claim. The
original fixed-constant upper bound remains `OPEN`.

This checkpoint is valid evidence about time to an audited partial package. It
is not a completed end-to-end regression and does not confirm the full v1.7
optimization hypothesis.

## Audited mathematics

For the literal switch-walk-switch chain and every integer `t>=2`, with
`n=floor(t/2)`, the retained strict partial theorem is

```text
1/(4 sqrt(t)) <= ||P_t^(0,0)-P_t^(0,2)||_TV
               <= 1/sqrt(n+1)+2 H_(n+1)/sqrt(t-n+1)
               <= sqrt(2)[3+2 log(t+1)]/sqrt(t).
```

Additional `STRICT` results are:

- conditional i.i.d. fair lamps on the visited interval for `t>=1`;
- exact translation and parity handling;
- exact equality between full-state TV and the TV of the visible-hull
  statistic `(min(supp eta union {z}),max(supp eta union {z}),z)`;
- the exact endpoint TV identity and lower bound `1/(4 sqrt(t))`;
- a coupling-specific `Omega(log(t)/sqrt(t))` mismatch obstruction for Route
  A, which does not imply the same lower bound for TV;
- Route C's exact finite full-state and translated-triple formulas; and
- the exact `(26,16,26)` counterexample to parity-class unimodality at
  `(t,r,j)=(10,4,2)`.

The fixed numerical `C` in a full-state `C/sqrt(t)` upper bound remains
`OPEN`. Finite exact replays are labeled `EVIDENCE`, not proof. Novelty is
`UNKNOWN` because the scored and neutral runs prohibited literature access.

## Scored resource checkpoint

| Metric | v1.6 Arm A | v1.7 quota checkpoint | Change | Target | Checkpoint target |
| --- | ---: | ---: | ---: | ---: | --- |
| Root active wall | 4052 s | 1311.844 s | -67.62% | <=3039 s | met |
| Model responses | 307 | 56 | -81.76% | <=184 | met |
| Tool calls | 216 | 44 | -79.63% | <=151 | met |
| Child sessions | 7 | 3 | -57.14% | <=4 | met |
| Uncached input | 1,108,074 | 211,820 | -80.88% | <=609,441 | met |
| Output | 390,390 | 101,940 | -73.89% | <=234,234 | met |
| Cost proxy | USD 21.7088192 | USD 3.5672448 | -83.57% | <=USD 13.0252915 | met |

The cost proxy is
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`.
It is a comparison metric, not an actual bill.

All six preregistered efficiency thresholds were met at the interruption
boundary. Because v1.6 completed after two five-hour segments and v1.7 has not
yet resumed, these percentages establish an early-checkpoint efficiency
signal only.

## Scheduling observations

- The coordinator performed the closure-first direct reduction and exact
  falsification probe before delegation.
- It then launched all three allowed research routes at once. This respected
  the preregistered concurrency cap, but was more aggressive than the v1.7
  smallest-batch recommendation.
- Two routes returned hash-bound partial artifacts. Route B consumed scored
  resources but hit the hard limit before writing its promised artifact.
- No network was used and no extra child sessions were launched.

## Quota and audit

- First observed five-hour usage: 55%.
- Last observed five-hour usage: 100%.
- First observed weekly usage: 75%.
- Last observed weekly usage: 82%.
- Termination log: `You've hit your usage limit ... try again at 7:06 PM.`
- Neutral audit: `PASS_FOR_RETAINED_PARTIAL_THEOREMS`.
- Neutral audit SHA256:
  `1f5e907b3fcbbe2190cbb6b4611c558d165a8cb51ec28e0f554cadd8d6ce00b8`.

See `arm-a-plugin-v17/stage_report.md`, `candidate_proof.md`,
`subagents/route_a.md`, `subagents/route_c.md`, and
`external_neutral_audit.md` for the bound package.
