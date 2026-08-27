# Closure gate

- **Target ID:** `O0`.
- **Target claim:** explicit two-sided `t^{-1/2}` TV bounds for the frozen chain for all
  integers beyond one explicit threshold.
- **Shortest dependency chain:** transition definition -> `O1` -> `O3` -> `O0`, with `O2`
  parallel and `O4` final.
- **First open load-bearing claim:** `O3`, an explicit full-state upper bound.
- **Why it is load-bearing:** endpoint smoothing proves only the lower bound; without control
  of the lamps/range, the target is not reached.
- **Existing support:** `problem_contract.md`, `obligation_graph.md`, `research_ledger.md`.
- **Coordinator direct attempt:** exact conditional-lamp reduction plus attempted reflected
  base coupling; the latter leaves the named two-extreme coverage event.
- **Cheapest falsification probe:** exact small-time dynamic programming for range triples and
  full states; pending execution.
- **Gate decision:** `ESCALATE`.
- **Spawn trigger:** determine whether a path/range mechanism or an analytic/convolution
  mechanism closes `O3`, while a separate adversary attacks the first candidate.
- **Next decision-changing action:** run exact small cases and two independent proof routes.
- **Last updated:** 2026-08-27.
