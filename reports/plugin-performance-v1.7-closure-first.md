# Plugin performance optimization v1.7.0

## Status

`IMPLEMENTED_AND_STATICALLY_VALIDATED`. This report does not yet claim an
end-to-end performance improvement. The matched v1.7 regression arm below is
the confirmatory test.

## Benchmark evidence used

Pilot v5 Arm A used `rigorous-open-math-research` v1.6.0 with seven research
child sessions on the frozen U2 task. It returned an independently audited
partial theorem, but did not close the target.

| Metric | v1.6.0 Arm A |
| --- | ---: |
| Root active wall | 4052 s |
| Model responses | 307 |
| Tool calls | 216 |
| Child sessions | 7 |
| Uncached input | 1,108,074 |
| Output | 390,390 |
| API-equivalent cost proxy | USD 21.7088192 |
| External verdict | `PASS_FOR_PARTIAL_THEOREM` |

The main observed inefficiency was a scheduling conflict. The light-first
protocol required cheap probes, but the agent orchestration protocol also
asked the solver to start several route families and keep a verifier active
throughout. The run therefore expanded seven child sessions and repeatedly
built or audited partial-result packages before the first constant-order
upper-bound obligation was closed.

## v1.7.0 change

The new closure-first path applies to a single bounded target:

1. Write the shortest target dependency chain.
2. Select the first open load-bearing claim.
3. Run one coordinator-owned direct attempt.
4. Run the cheapest decisive falsification probe.
5. Spawn only when the return can change a named gate decision.
6. Require a durable `decision_delta` before another Worker wave.
7. Materialize nonessential artifacts lazily and place global audits at
   completion or stopping boundaries.

The change preserves independent audit for every result used as a
load-bearing dependency. Empty, duplicate, or no-delta Worker returns are
rejected without purchasing a separate global review.

## Source and installation bindings

- Parent plugin commit: `957d80b7f1c58b60972a4ece87945cd93c0a1476`.
- DSH adapter commit: `0a852d1`.
- Local Codex rigorous SKILL SHA-256:
  `FFCDDCA13446F35A275EBE199E136E26FE1EE5F960BDC58023260F7C0CFDCDE3`.
- Local Codex workflow SKILL SHA-256:
  `B7EA6D50CBC7BBD986C252EEEFDF29D33F33D1614A13A6622D63B1EFAEE557B3`.
- Installed versions: rigorous `1.7.0`, workflow `1.7.0`.

## Validation evidence

- Parent marketplace: `81/81` repository checks.
- Parent marketplace: `10/10` smoke tests.
- Modified skill quick validation: `PASS` for rigorous and workflow.
- Modified plugin validation: `PASS` for rigorous and workflow.
- DSH adapter: `51/51` checks, `BUNDLE OK`, `14/14` smoke tests.
- DSH deterministic sync: clean against parent commit `957d80b` with 100
  locked files.
- Local Codex cache hashes equal the parent source hashes.

## Matched regression hypothesis

The regression arm reuses the exact Arm A prompt, model, reasoning effort,
concurrency ceiling, blind restrictions, and 75 minute cap. It changes only
the plugin from v1.6.0 to v1.7.0 and uses a fresh `CODEX_HOME`.

Primary quality gate:

- no false completion claim;
- external audit no worse than `PASS_FOR_PARTIAL_THEOREM` for the strongest
  claimed result.

Pre-registered efficiency targets relative to v1.6.0 Arm A:

| Metric | Target |
| --- | ---: |
| Root wall | at most 3039 s |
| Model responses | at most 184 |
| Tool calls | at most 151 |
| Child sessions | at most 4 |
| Uncached input | at most 609,441 |
| Output | at most 234,234 |
| Cost proxy | at most USD 13.0252915 |

These targets are hypotheses, not achieved results. Reusing U2 makes the run
a matched scheduling regression, not a new OOD quality benchmark. No v1.6
solution or result artifact is exposed to the solver.
