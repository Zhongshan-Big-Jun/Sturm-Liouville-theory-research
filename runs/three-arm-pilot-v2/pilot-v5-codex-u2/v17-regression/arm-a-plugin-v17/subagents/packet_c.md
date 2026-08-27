# Subtask packet — SUB-O3-routeC

- **Subtask ID:** `SUB-O3-routeC`.
- **Parent:** `O3` / `R-C`.
- **Spawned:** 2026-08-27.
- **Budget:** one focused research turn; return strongest exact result at boundary.
- **Coordinator attempt:** exact conditional state mass is a weighted mixture over enclosing
  path ranges; no sign-controlled comparison yet.
- **Falsification:** full-state exact TV differs substantially from triple TV through `t=12`.
- **Decision:** can produce a direct combinatorial comparison or falsify the needed monotonicity.

## Claim

Derive exact final-state probabilities as sums over simple-walk ranges and seek an explicit
`l1` comparison under translation by two, using reflection, injections, telescoping, or the
geometric weights from zero boundary lamps.  Aim for a proved `C_C/sqrt(t)` full-state bound;
otherwise return a reusable exact formula/counterexample and the first smaller gap.

## Inputs

- `problem_contract.md` (`15a22e80...2342eb8`).
- `obligation_graph.md` (`8f755050...5a21d1`).
- `closure_gate.md` (`c2c72bbc...df68e`).
- `reproducibility/exact_small_cases.py` (`3ce81aff...42fbc2`).

## Constraints and deliverable

No internet or reads outside the current directory.  Do not mutate shared files.  Write
`subagents/route_c.md`.  Return raw JSON with status in
`PROVED|PARTIAL|BLOCKED|REFUTED`, path, full sha256, exact gap, evidence, and decision delta.
Do not claim global completion.
