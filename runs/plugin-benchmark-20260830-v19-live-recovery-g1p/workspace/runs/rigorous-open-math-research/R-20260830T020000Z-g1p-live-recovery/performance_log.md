# Performance log

## Observable research counts

- Planner agents: 1.
- Research workers: 2.
- Independent auditors: 1.
- Nested subagents: 0.
- Web calls inside solver and worker runs: 0.
- Numerical proof premises: 0.
- Planner artifacts: 8.
- Worker artifacts: 6.
- Independent audit artifacts: 2.

Collaboration-agent token, cache, cost, and exact response counters are not
available as auditable measurements. This run is a functional recovery drill
and is not scored as an efficiency arm.

## Recovery overhead

- Segment 00 canonical receipt command: 164.035 ms.
- Segment 01 complete seal, verify, and receipt chain: 698.159 ms.
- Two deterministic operator-input failures occurred before the valid segment
  00 receipt: a duplicated project-relative path and an unsupported seven-digit
  fractional timestamp. They caused no model, worker, network, or mathematics
  replay.
- One sequence 01 semantic preflight rejected a renamed open obligation. The
  state was repaired by preserving the predecessor ID and recording the replaced
  action in `do_not_repeat`.

Checkpoint overhead is separate and unscored.
