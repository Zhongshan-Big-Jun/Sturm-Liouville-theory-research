# Subtask packet — SUB-O3-routeB

- **Subtask ID:** `SUB-O3-routeB`.
- **Parent:** `O3` / `R-B`.
- **Spawned:** 2026-08-27.
- **Budget:** one focused research turn; return strongest exact result at boundary.
- **Coordinator attempt:** `closure_gate.md`; conditional range route remains open.
- **Falsification:** generic reversible-chain gradient claims are disallowed without a proof;
  parity must be handled because one-step supports alternate base parity.
- **Decision:** can close `O3` directly or identify the first invalid analytic interface.

## Claim

For the literal switch-walk-switch law, seek a self-contained convolution/operator/probability
argument giving explicit `C_B,t_B` with full-state TV at most `C_B/sqrt(t)`.  You may derive a
general lemma only if you prove its exact form and verify all hypotheses.  Audit noncommuting
switches, parity, and the two all-zero starting configurations.

## Inputs

- `problem_contract.md` (`15a22e80...2342eb8`).
- `obligation_graph.md` (`8f755050...5a21d1`).
- `closure_gate.md` (`c2c72bbc...df68e`).
- `reproducibility/exact_small_cases.py` (`3ce81aff...42fbc2`).

## Constraints and deliverable

No internet or reads outside the current directory.  No silent recalled theorem.  Do not
mutate shared files.  Write `subagents/route_b.md`.  Return raw JSON with status in
`PROVED|PARTIAL|BLOCKED|REFUTED`, path, full sha256, exact gap, evidence, and decision delta.
Do not claim global completion.
