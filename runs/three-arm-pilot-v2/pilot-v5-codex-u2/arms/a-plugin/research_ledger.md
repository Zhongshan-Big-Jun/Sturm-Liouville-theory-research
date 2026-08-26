# Research ledger

## 2026-08-26 — provenance and contract

- Read the complete skill contract and the phase references required for contract, route search, computation, synthesis/audit, reporting, and subagent delegation. All reads were inside the current directory.
- Authoritative task is `PROMPT.md` (SHA-256 recorded in `problem_contract.md`). No per-problem references, accepted knowledge base, or Lean project were found. The directory is not a Git worktree.
- Restrictions frozen: blind/no internet; no reads outside current directory; autonomous; at most three concurrent subagents.
- Exact structural observation: for a fixed nearest-neighbour base path, the visited set is its integer interval `[L,U]`. Every visited site has a last resampling coin, and those last coins are distinct members of the independent coin family, hence final lamps on `[L,U]` are iid fair; unvisited lamps remain their forced initial zero. This includes the initial sites because the time-zero switch resamples the starting lamp for `t>=1`.
- Lower-bound route: endpoint projection compares `S_t` and `S_t+2`; their common parity makes the threshold-event difference a central atom, expected order `t^{-1/2}`.
- Upper-bound reduction: the state is the image of `(L,U,Z)` under a common Markov kernel, so its TV is at most the TV between the physical range triples for starts 0 and 2. The live obligation is an explicit `O(t^{-1/2})` diagonal-translation estimate for this triple, or a stronger direct coupling.
- Escalation: Tier 0 structural probes exposed the load-bearing range-gradient estimate; user explicitly requested research subagents and adversarial audit, justifying Tier 2/3 mechanism-distinct delegation after the contract and routes were recorded.

## 2026-08-26 — exact range-triple computation

- Added `reproducibility/enumerate_triples.py`, an exact-integer dynamic program for counts by `(L,U,Z)` and the diagonal-shift TV numerator. Replay: `python3 reproducibility/enumerate_triples.py 100`.
- Exact values show `sqrt(t)*TV` increasing slowly from `1` to about `2.657` by `t=100`, consistent with (but not proving) `O(t^{-1/2})`. No parity anomaly appeared.
- A candidate numerical inequality `TV(triple shift) <= 4 p_t`, where `p_t=2^{-t} binom(t,floor(t/2))`, survived exact tests through `t=150`; it is recorded only as a conjectural proof target.
- Reparameterization: for range width `R`, put `A=-L` and `e=Z-L`. The relevant count is `H_t^R(A,e)`, paths in `[0,R]` from `A` to `e` that visit both endpoints. Diagonal translation compares `H_t^R(A,e)` with `H_t^R(A+2,e)`. This exact identity converts `O3a` into a summed discrete-variation estimate in the starting coordinate.
- Attempted monotonicity of `A -> H_t^R(A,e)` is false (e.g. the exact sequence for `t=6,R=4,e=2`, even `A`, is `[1,0,1]`). Decomposition by order of first extrema looked monotone at small times but also fails in general (counterexample found at `t=30,R=6,e=0` for the upper-first component). Any proof relying on simple unimodality is on the avoid list.

## 2026-08-26 — subagent `SUB-O3b-COUPLE`

- Hash-verified artifact: `subagents/direct_coupling.md`, SHA-256 `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c`; returned status `FALSIFIED` for reflection-then-synchronization as an `O(t^{-1/2})` route.
- The artifact independently supplies a complete proof of `O1`, including last resampling, repeated visits, the forced initial zero, and `t=0` separation.
- It computes the exact overlap of fair interval-lamp kernels as `2^{-max(|I\J|,|J\I|)}` and therefore audits optimal conditional lamp coupling.
- Precise failure mechanism: the reflection pre-meeting depth has harmonic mass `1/[k(k+1)]`, while a post-meeting walk misses an exclusive depth with probability of order `k/sqrt(t)`; the accumulated optimal conditional mismatch is of order `log(t)/sqrt(t)`. Thus a base reflection coupling followed by synchronization cannot close `O3`, even with maximal conditional lamp coupling.
- This is a route obstruction, not a disproof of the target. The range-gradient and counting routes remain live.

## 2026-08-26 — post-rate-limit continuation

- Resumed from the persisted contract and artifacts without reopening completed searches. The authoritative prompt and contract hashes were unchanged.
- Discovered a completed but previously unmerged partial artifact `subagents/range_translation.md`, locally SHA-256 `07f2c63d3a0670fff434b78778c35ddfecc1ffdb41dc8c7c1b3fa70b9890d5e7`. Because the earlier agent return was interrupted before it supplied a hash, the module was sent to a fresh validator rather than merged on self-report.
- Hash-verified validation artifact: `subagents/partial_validator.md`, returned and recomputed SHA-256 `82f3f1b8261ea9c6d75af2d01cc25c6ab758713581771eab1c361006fa797542`, verdict `REPAIRABLE_GAP`. It confirms the exact range-shape identity, both one-sided `12/sqrt(t)` estimates, and the explicit range-triple `(6+4 log(t+1))/sqrt(t)` estimate. It found one local false display: recurrence (13) in `range_translation.md` omits new-extremum transitions. The correct forward update is the one implemented in `reproducibility/enumerate_triples.py`; the error does not enter any proof or displayed exact table.
- Integrated a stronger full-state near-target estimate from the already hash-verified `direct_coupling.md`: for every `t>=16`, TV is at most `(2 log(t)+15)/sqrt(t)`. The endpoint lower bound is now proved for every `t>=1` with `c=1/4`.
- Added `reproducibility/audit_exact.py` (SHA-256 `0b1efa20baed0081cd549444aa5001502fe9b19352166baacbd43fdd9d90ccbf`). Replay through `t=100` passed exact small-time triple numerators, the conjectural AVI inequality, and the conjectural path-specific marginal comparison. The last two remain finite falsification tests only.
- Continued only the two unresolved mechanisms: the aggregate coarea/killed-kernel estimate and the path-specific comparison of triple TV to its two one-sided marginal TVs. A separate fresh global auditor was launched against candidate SHA-256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`.

## 2026-08-26 — terminal route and audit returns

- Hash-verified aggregate artifact: `subagents/aggregate_coarea.md`, returned and recomputed SHA-256 `537b367fb01bd1175781daa3e543273e0912a9a2d3c266b359d0ff8d03e22fff`, status `RIGOROUS_PARTIAL_RESULT`. It proves exact inclusion-exclusion in killed interval kernels, an explicit periodized-binomial mixed-difference representation, and an exact discrete coarea formula. It does not prove the fixed-constant aggregate estimate. The first gap is a bound on aggregate superlevel components or the explicit `V_t^D+V_t^E` variations.
- The separate `(MC)` continuation was stopped at the resource boundary after reporting no proof or counterexample and no artifact; it is not merged. Its reusable negative findings (generic ordered couplings do not imply `(MC)`; reflection coupling ceases to be one-sided maximal after small times) remain marked unverified because no hash-bound artifact was returned.
- Hash-verified fresh global audit: `subagents/global_audit.md`, returned and recomputed SHA-256 `ba55ad7ed8a2f05a458b45f9ada841aa8fe28ad92fbd3c0040a6a82bace2d82a`, verdict `PASS` with zero critical errors and zero gaps for candidate SHA-256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`. The auditor explicitly states this is not a pass for the frozen target: `O3` remains open.
- Terminal status is therefore `RIGOROUS_PARTIAL_RESULT`, not a complete proof. Strongest audited theorem: for every `t>=16`,
  `1/(4sqrt(t)) <= TV <= (2log(t)+15)/sqrt(t)`, with the lower bound valid already for every `t>=1`.
