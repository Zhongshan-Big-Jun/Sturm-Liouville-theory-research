# Approach registry

## `R-LB-ENDPOINT` — projection and central atom

- Route key/family: `endpoint-projection`; direct inequality.
- Target: `O2`.
- Mechanism: project to the base endpoint; compare a simple-walk law with its shift by 2.
- Strict simplification: removes all lamp variables.
- First deliverable: exact TV formula or a single separating event plus elementary lower bound.
- Falsification: test `t=0,1,2` and both parities.
- Expected bottleneck: explicit all-time central-binomial lower bound.
- Cost tier: 0/1.
- Minimal first step: enumerate endpoint probabilities and the optimal threshold event.
- Escalation criterion: only if an elementary variance/unimodality estimate fails.
- Status: PROMISING.
- Exact gap: written inequality and audit.

## `R-UP-RANGE` — range-triple translation

- Route key/family: `range-triple-gradient`; probabilistic/combinatorial.
- Target: `O3a`.
- Mechanism: conditional lamp law is a common kernel of `(L,U,Z)`; estimate the TV gradient of the range triple under a spatial shift by 2.
- Strict simplification: a finite-dimensional simple-walk statistic replaces the lamplighter state.
- Required results: reflection/path-count identities proved in-run.
- First deliverable: an explicit summable formula or coupling.
- Falsification: exact enumeration for small `t`, boundary ranges, parity.
- Expected bottleneck: summing the three-variable discrete derivative without a logarithmic loss.
- Cost tier: 2.
- Minimal first step: compute exact small-time distributions and search for a telescoping identity.
- Escalation criterion: a stable exact identity justifies full symbolic proof.
- Status: PARTIAL.
- Exact gap: exact diagonal-variation and coarea formulas are proved; a uniform aggregate component/cancellation estimate is open.

## `R-UP-COUPLE` — full-state coupling

- Route key/family: `successful-coupling`; probabilistic.
- Target: `O3b`.
- Mechanism: couple base paths and resampling coins so all residual pre-meeting lamps are erased.
- Strict simplification: a coupling-time tail would directly imply TV.
- First deliverable: exact marginal-preserving coupling with a tail formula.
- Falsification: reflection coupling can leave uncoupled lamps over an expanding pre-meeting range; test this explicitly.
- Expected bottleneck: avoiding a hidden logarithmic or constant mismatch probability from old lamps.
- Cost tier: 2.
- Minimal first step: audit reflection/meeting constructions.
- Escalation criterion: proceed only if residual lamps can be coupled without exponentially small coincidence.
- Status: BLOCKED for reflection-then-synchronization; other coupling mechanisms unsearched.
- Exact gap: `subagents/direct_coupling.md` proves an intrinsic logarithmic loss from residual exclusive lamps. Reopen only with a base-path pairing that is not this reflection/synchronous law or without pathwise conditional lamp coupling.

## `R-UP-COUNT` — exact killed-walk counts

- Route key/family: `reflection-inclusion-exclusion`; analytic/combinatorial.
- Target: `O3c`.
- Mechanism: express joint extrema/endpoint probabilities through walks killed in an interval, then telescope the translation difference.
- Strict simplification: deterministic finite sums of binomial coefficients.
- First deliverable: exact formula and an absolute-sum estimate.
- Falsification: ranges of width 0/1, endpoints on boundaries, parity.
- Expected bottleneck: absolute values can destroy telescoping.
- Cost tier: 2.
- Minimal first step: derive formula and check by enumeration.
- Escalation criterion: observed sign pattern or bounded-variation identity.
- Status: PARTIAL.
- Exact gap: `subagents/aggregate_coarea.md` gives exact killed-kernel, image, and coarea reductions. Termwise absolute values lose cancellation; no fixed-constant aggregate estimate is proved.

## `R-UP-ONESIDED` — one-sided extrema and mixed comparison

- Route key/family: `one-sided-reflection-mixed-TV`; reflection/coarea.
- Target: `O3a`.
- Mechanism: reflection gives exact min-endpoint and max-endpoint formulas; a path-specific comparison `(MC)` would lift their TVs to the full triple.
- Strict simplification: both one-sided TVs are already bounded by `12/sqrt(t)`.
- First deliverable: prove or refute `(MC)` for the signed exact-extrema matrices.
- Falsification: exact integer enumeration; generic-array and coordinatewise-order analogues are known false and cannot be invoked.
- Expected bottleneck: controlling the zero-row/zero-column cycle component of the signed joint extrema array.
- Cost tier: 2/3.
- Minimal first step: killed-walk/reflection sign and coarea analysis.
- Escalation criterion: a genuine path-specific sign invariant, not finite testing.
- Status: BLOCKED at the stated comparison.
- Exact gap: `(MC)` is unproved; no counterexample was found through `t=160`, but coordinatewise ordering and generic-array analogues are insufficient. The interrupted continuation returned no mergeable artifact, so only the hash-validated one-sided module is retained.
