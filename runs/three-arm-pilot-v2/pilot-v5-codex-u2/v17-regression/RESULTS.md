# Pilot v5 v1.7 closure-first regression results

## Status

`COMPLETED_WITH_AUDITED_PARTIAL_RESULT`.

The scored solver resumed the same root session after the quota reset and
completed its stopping-boundary package in 569.206 additional active seconds.
The two scored segments total 1881.050 root seconds. Route A and Route C were
hash-verified and integrated; Route B remained an `INCOMPLETE_RETURN` and no
claim was inferred from its missing artifact. The solver wrote a final
response, coordinator audit, files-only convergence check, replay scripts, and
hash manifest. It honestly retained the label `RIGOROUS_PARTIAL_RESULT`.

A post-hoc independent audit is excluded from scored usage. The original
fixed-constant upper bound remains `OPEN` at obligation `O3`. The regression
therefore confirms the v1.7 efficiency hypothesis for producing an honest,
auditable partial package, not mathematical completion of the frozen target.

Repository capture note: the CLI launcher replaced `final_response.md` with
the actual completed-turn answer after the solver had generated its manifest.
The archived manifest updates only that capture-file hash; all mathematical
artifact hashes are unchanged. See `repro_manifest.md` for both bindings.

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

## Final scored resource comparison

| Metric | v1.6 Arm A | v1.7 final | Change | Target | Target met |
| --- | ---: | ---: | ---: | ---: | --- |
| Root active wall | 4052 s | 1881.050 s | -53.58% | <=3039 s | met |
| Model responses | 307 | 72 | -76.55% | <=184 | met |
| Tool calls | 216 | 58 | -73.15% | <=151 | met |
| Child sessions | 7 | 3 | -57.14% | <=4 | met |
| Uncached input | 1,108,074 | 338,812 | -69.42% | <=609,441 | met |
| Output | 390,390 | 125,692 | -67.80% | <=234,234 | met |
| Cost proxy | USD 21.7088192 | USD 5.183904 | -76.12% | <=USD 13.0252915 | met |

The cost proxy is
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`.
It is a comparison metric, not an actual bill.

All preregistered efficiency thresholds were met after the end-to-end v1.7
stopping package completed. The comparison is matched on task, prompt, model,
reasoning effort, isolation, and scoring definitions. It measures workflow
efficiency and audit honesty on this reused U2 regression task; it does not by
itself establish broad out-of-distribution superiority.

## Scheduling observations

- The coordinator performed the closure-first direct reduction and exact
  falsification probe before delegation.
- It then launched all three allowed research routes at once. This respected
  the preregistered concurrency cap, but was more aggressive than the v1.7
  smallest-batch recommendation.
- Two routes returned hash-bound partial artifacts. Route B consumed scored
  resources but hit the hard limit before writing its promised artifact.
- The same-session continuation launched no new child session, no new route,
  and no Route B retry. It only ingested existing artifacts and froze the
  stopping package.
- No network was used.

## Quota and audit

- First segment ended at the five-hour hard limit after 1311.844 seconds.
- Continuation observed five-hour usage from 50% to 71% and weekly usage from
  90% to 93%.
- The first-segment neutral audit returned
  `PASS_FOR_RETAINED_PARTIAL_THEOREMS`; SHA256
  `1f5e907b3fcbbe2190cbb6b4611c558d165a8cb51ec28e0f554cadd8d6ce00b8`.
- The exact final-package independent verdict and hash are recorded in
  `arm-a-plugin-v17/external_final_audit.md` and
  `external_final_audit_verdict.json`. The verdict is `PASS` for the retained
  partial theorem and `FAIL` for frozen-target completion. Review SHA256:
  `12ee19bf382c8e7e391180febca1706a75bb69771321dc5f9e50de2200ed9f0d`.
- Repository-corrected artifact manifest SHA256:
  `cb811d40be24ec74ed301463affb32ade7bc7b27fa93e51385acbbc1e9ddcd1a`.

See `arm-a-plugin-v17/stage_report.md`, `candidate_proof.md`,
`final_report.md`, `subagents/route_a.md`, `subagents/route_c.md`, and the two
external audit records for the bound package.
