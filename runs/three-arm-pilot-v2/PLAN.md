# Three-arm pilot v2 (adapted from GPT plan)

Date: 2026-08-25
Environment: existing Codex/QED benchmark harness at `F:\benchmark\B3-O3-CAL-20260824`.
Model: `gpt-5.6-sol`, reasoning `xhigh`, via local proxy (`harness/selected-proxy.txt`).
Quota note: currently arm homes show ~57-68% weekly used; runs may become budget-limited.

## Arms

| Arm | Configuration |
|---|---|
| A | rigorous-open-math-research v1.6.0, parent commit 88e1c97; subagents enabled (max 3 concurrent); same Codex runtime as B/C |
| B | blank Codex: same task, no plugins/skills/memories/multi-agent |
| C | QED pinned at `1219009`, matched-budget config: max_proof_attempts=1, max_revisions=1, max_decompositions=1 |

## Tasks

1. Calibration (not ranked): B3 O3 root-count task from `runs/plugin-perf-eval2/PROBLEM-B3-FIXN`.
   - 3 runs: A x1, B x1, C x1.
   - Purpose: verify harness, measure matched budget.
2. Main: H^s operator-domain membership.
   - Blind start: `e9aee2c`; hidden gold: `0f9b2b0`.
   - Scoring targets:
     1. necessary/sufficient condition for `Q_n^(s) in D(K_c^(s/2))`;
     2. equality of operator-domain and abstract completion;
     3. density of `span{Q_n^(s)}` in operator-domain.
   - Complete polynomial degree spectrum is bonus only.
   - 9 runs: A/B/C each 3 times, Latin square order:
     1. A->B->C
     2. B->C->A
     3. C->A->B

## Isolation/Fairness

- Each run gets its own work root and independent `CODEX_HOME`.
- Solver only reads the neutral task bundle; no `.git`, project repo, run IDs, answer paths, sibling outputs, or network.
- QED safe adapter already implemented in the existing harness (`harness/qed-safe-bin`, `config.safe.yaml`).
- All child-agent and verifier usage is charged to that arm.
- No mid-run hints, rescue, or time extensions.

## Scoring (100 pts)

- Mathematical correctness/closure: 40
- Contract fidelity/completeness: 20
- Strict progress over blind start: 15
- Epistemological calibration: 10
- Citation/evidence fidelity: 10
- Reproducibility: 5

Accepted: score >= 70, correctness >= 32/40, no FATAL_GAP/WRONG_PROBLEM/circular load-bearing citation, no numerical-evidence-as-proof.

## Metrics

Quality-first: blind quality score, accepted rate, strict obligations closed, false-complete/fabricated-citation count. Then cost: uncached/cache/output tokens, tool calls, child-agent calls, wall time, aggregate agent-minutes, cost per accepted result.

## Current status

Attempted calibration launch on 2026-08-25; blocked because the GPT-5.6 model proxy (172.22.112.1:7898) is closed. A/B/C runs were prepared but produced no solver output. See `BLOCKER.md`.
