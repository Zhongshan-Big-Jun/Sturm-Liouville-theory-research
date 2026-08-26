# Research map

The endpoint lower bound and exact lamp-kernel reduction are the current trusted structural progress. Three upper-bound mechanisms are live: range-triple translation, full-state successful coupling, and killed-walk/reflection counting. The common obstruction is to obtain an absolute `O(t^{-1/2})` estimate without losing a logarithm or leaving residual lamps.

An exact coordinate reduction is now available: `A=-L`, `R=U-L`, `e=Z-L` turns the translated triple difference into the variation of `H_t^R(A,e)` under `A -> A+2`. Straight unimodality arguments are excluded by exact counterexamples, although the aggregate inequality `TV <= 4` times the central endpoint atom remains a computation-supported candidate, not a premise.

The standard reflection/synchronous full-state coupling is now rigorously blocked: even maximal conditional coupling of the terminal interval-lamp laws incurs `Theta(log(t)/sqrt(t))` mismatch. Its artifact nevertheless closes the fixed-path lamp-kernel lemma and gives an exact interval-kernel overlap formula.

Current strongest theorem: for every `t>=16`,
`1/(4sqrt(t)) <= TV <= (2log(t)+15)/sqrt(t)`. Independently, both one-sided extrema/endpoint marginals have TV at most `12/sqrt(t)`. Completion is reduced to either the aggregate variation inequality `AVI` or the path-specific mixed comparison `MC`; generic marginal-TV and simple monotonicity arguments are explicitly excluded.

The terminal independent route added an exact coarea formulation: the diagonal variation is twice the aggregate number of connected components of parity-superlevel sets of the exact range fibers. Equivalently it is controlled by explicit mixed differences of periodized binomial coefficients. This is the narrowest audited frontier; termwise reflection estimates erase the necessary cancellation.

## Methods and tools

- Self-contained probability and path counting.
- Exact small-time enumeration will be used only for falsification and identity discovery.
- Mechanism-distinct subagents will write isolated artifacts under `subagents/`.

## Avoid list

- Different lamp conventions; endpoint-only conditioning for the upper bound; base-only reflection coupling without lamp audit; asymptotic notation without explicit constants.
