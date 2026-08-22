# Round 2 plugin performance evaluation: B3 fixed-n supremum

This is a longer, larger, and harder follow-up to the round 1 A6 experiment.
It runs two isolated subagents on the same major open problem to compare
baseline behavior with an explicit reuse-gate protocol.

- Problem: `PROBLEM-B3-FIXEDN.md`
- Baseline run: `R-20260822T220000Z-b3-baseline`
- Reuse-gate run: `R-20260822T220000Z-b3-reuse`

The scheduled run is intentionally longer than round 1: the agents are asked
to work on the full problem rather than a tiny subcase, and to write a
handoff if they hit a resource boundary.
