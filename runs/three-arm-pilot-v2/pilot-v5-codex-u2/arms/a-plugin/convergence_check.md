# Fresh-context convergence check

Reconstructed only from `problem_contract.md`, `obligation_graph.md`, `approach_registry.md`, `research_ledger.md`, `candidate_proof.md`, and hash-bound subagent artifacts.

Verdict: the run converged structurally but did not reach the frozen target. `O1` and `O2` are proved, an explicit logarithmic-loss upper is independently audited, and all live constant-order upper routes reduce to the same smaller aggregate range-gradient obligation. Continued sampling had begun producing correlated duplicates (AVI/MC without a cancellation invariant), so stopping preserves the exact frontier rather than relabeling it as complete.

First frontier node: prove a fixed numerical bound for the aggregate diagonal variation of `h_t`, equivalently the coarea superlevel-component bound or the periodized-binomial mixed-variation bound in `subagents/aggregate_coarea.md`.

No artifact-only evidence supports a complete `C/sqrt(t)` upper at this boundary.
