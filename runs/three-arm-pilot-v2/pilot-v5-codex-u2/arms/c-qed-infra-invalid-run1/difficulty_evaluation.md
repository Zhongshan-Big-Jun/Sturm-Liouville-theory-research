# Difficulty Evaluation

## Classification: Hard

## Justification
The problem asks for matching total-variation bounds with explicit constants for two switch-walk-switch lamplighter laws, not merely a qualitative convergence or recurrence statement. The law depends jointly on the one-dimensional walk's endpoint and visited range, while the two forced initial zero lamps, bipartite parity, and exact conditioning create delicate finite-time effects. Establishing both bounds uniformly for every sufficiently large integer time requires precise probabilistic estimates and careful comparison of range-dependent lamp laws.

## Key Complexity Factors
- The lamp configuration encodes the random walk's visited set and endpoint, so the relevant laws are highly dependent mixtures rather than product measures.
- The shifted starting points interact with parity and with deterministic initial lamp values.
- Both an upper coupling/comparison bound and a lower distinguishing event are required at the sharp order `t^{-1/2}`.
- All constants and the threshold time must be explicit, ruling out purely asymptotic invocations without quantitative remainder control.
