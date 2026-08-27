# Subtask packet — SUB-O3-routeA

- **Subtask ID:** `SUB-O3-routeA`.
- **Parent:** `O3` / `R-A`.
- **Spawned:** 2026-08-27.
- **Budget:** one focused research turn; return strongest exact result at boundary.
- **Coordinator attempt:** `closure_gate.md`; reflected coupling exposes two-extreme coverage.
- **Falsification:** `reproducibility/exact_small_cases.py`; triple TV survives through `t=80`
  but has a slowly rising rescaled constant.
- **Decision:** can close the sufficient triple-law upper bound or eliminate this route.

## Claim

Find explicit numerical `C_A,t_A` and prove that for a length-`t` simple symmetric random walk
started at zero, the TV distance between `(L_t,U_t,S_t)` and its translate by two is at most
`C_A/sqrt(t)` for every integer `t>=t_A`; alternatively give a precise obstruction or a
strictly smaller exact gap.  Explain why triple agreement couples the frozen final lamps.

## Inputs

- `problem_contract.md` (`15a22e80...2342eb8`).
- `obligation_graph.md` (`8f755050...5a21d1`).
- `closure_gate.md` (`c2c72bbc...df68e`).
- `reproducibility/exact_small_cases.py` (`3ce81aff...42fbc2`).

## Constraints and deliverable

No internet or reads outside the current directory.  No external theorem unless proved in the
artifact.  Do not mutate shared files.  Write `subagents/route_a.md`.  Return raw JSON with
status in `PROVED|PARTIAL|BLOCKED|REFUTED`, path, full sha256, exact gap, evidence, and decision
delta.  Do not claim global completion.
