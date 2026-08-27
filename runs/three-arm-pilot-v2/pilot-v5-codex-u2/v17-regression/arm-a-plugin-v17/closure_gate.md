# Closure gate

- **Target ID:** `O0`.
- **Target claim:** explicit two-sided `t^{-1/2}` TV bounds for the frozen chain for all
  integers beyond one explicit threshold.
- **Shortest dependency chain:** transition definition -> `O1` -> `O3` -> `O0`, with `O2`
  parallel and `O4` final.
- **First open load-bearing claim:** `O3`, an explicit full-state upper bound.
- **Why it is load-bearing:** endpoint smoothing proves only the lower bound; without control
  of the lamps/range, the target is not reached.
- **Existing support:** `candidate_proof.md` proves `O1`, `O1b`, `O2`, `O3p`, and `O5`;
  hash-verified Route A/C artifacts support the partial upper bound and exact frontier.
- **Coordinator direct attempt:** the reflected coupling was completed quantitatively and gives
  `O(log(t)/sqrt(t))`; its own failure probability has the same logarithmic obstruction.
- **Cheapest falsification probe:** completed exact dynamic programming through `t=80` for
  triples and `t=12` for full states, plus exact replay of the Route C V-shaped slice.
- **Gate decision:** `OPEN_EXACT_GAP` at stopping boundary.
- **Spawn trigger:** none; the continuation instruction forbids a new wave and Route B retry.
- **Next decision-changing action:** outside this run, prove the normalized-range array bound
  `O3c` or find a full-state cancellation/coupling that avoids harmonic pre-depth cost.
- **Last updated:** 2026-08-27.
