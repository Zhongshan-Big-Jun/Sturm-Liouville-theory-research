# Frozen harness

- Runtime: Codex collaboration agents in the current local task.
- Planner: one bounded research agent, no nested agents.
- Escalation wave: at most two distinct workers.
- Fault injection: seal checkpoint after the first worker returns while the
  second remains live.
- Resume invariant: reconcile that exact worker before any new dispatch.
- Checkpoint implementation: installed
  `math-research-workflow/1.9.0/scripts/checkpoint_resume.py`.
- Recovery calls after sealing: deterministic local scripts only until the
  canonical receipt exists.
- Emergency reserve: none.
