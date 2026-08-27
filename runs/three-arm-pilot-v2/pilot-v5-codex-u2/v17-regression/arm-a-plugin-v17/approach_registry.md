# Approach registry

## R-A — path/range coupling

- **Route key / family:** `path_range_coupling`; probabilistic path decomposition.
- **Core mechanism:** couple or compare simple-random-walk paths so that endpoint and visited
  interval agree, then share the conditional lamp bits.
- **Target obligation:** `O3a`.
- **Strictly easier feature:** the path statistic has only three integer coordinates and exact
  reflection/strong-Markov tools, whereas the state has exponentially many lamp patterns.
- **Required results:** all must be derived in the route artifact; no external citation allowed.
- **First deliverable:** explicit `C_A,t_A` for translated triple-law TV, or a precise obstruction.
- **Fast tests:** compare with exact probe through `t=80`; audit the two-extreme coverage event.
- **Expected bottleneck:** simultaneously covering both pre-coupling extremes.
- **First open claim:** a quantitative path/range coupling with failure `O(t^{-1/2})`.
- **Cost tier:** 3, authorized by explicit user request and closure-gate `ESCALATE`.
- **Status:** ACTIVE (subagent A).

## R-B — convolution/analytic smoothing

- **Route key / family:** `group_convolution_gradient`; analytic/probabilistic operator method.
- **Core mechanism:** use the exact switch measures and convolution structure to bound the
  translation gradient of the full state law directly.
- **Target obligation:** `O3b`.
- **Strictly easier feature:** may bypass explicit extrema by exploiting independent uniform
  switch projections or a self-contained one-dimensional smoothing factor.
- **Required results:** any general inequality must be stated and proved in exact form.
- **First deliverable:** explicit full-state `C_B,t_B`, or the first invalid factorization.
- **Fast tests:** parity; noncommutation of adjacent lamp-switch projections; compare small TV.
- **Expected bottleneck:** a universal group gradient estimate is false without extra structure.
- **First open claim:** locate a one-dimensional convolution factor that survives the lamps.
- **Cost tier:** 3.
- **Status:** ACTIVE (subagent B).

## R-C — exact combinatorial state comparison

- **Route key / family:** `exact_state_mass_transport`; enumeration/reflection/injection.
- **Core mechanism:** derive state probabilities as weighted sums over enclosing ranges and
  compare a state with its two-site translate by a sign-controlled telescoping or injection.
- **Target obligation:** `O3`.
- **Strictly easier feature:** boundary-zero weights are geometric and may collapse the range
  mixture more sharply than the triple-law bound.
- **Required results:** exact counting/reflection identities derived locally.
- **First deliverable:** explicit comparison lemma or minimal counterexample to monotonicity.
- **Fast tests:** exact state enumeration through `t=12`; lamp supports empty/singleton and
  states touching only one range boundary.
- **Expected bottleneck:** signs after summing over latent ranges.
- **First open claim:** an `l1`-summable translation difference formula.
- **Cost tier:** 3.
- **Status:** ACTIVE (subagent C).

## Avoid list

- Do not infer the full-state upper bound from endpoint TV (data processing has the opposite
  useful direction).
- Do not use a generic reversible-chain neighbour-gradient assertion: it fails on chains with
  persistent boundary information unless extra hypotheses are proved.
- Do not require equality of full paths; their distinct starting vertices make that impossible.
