NUMERICAL_EVIDENCE

# R9 deterministic falsification/discovery contract

## Exact object and predicates

Reuse only already frozen trajectory records from
`../r8_certified_search/results.json`.  Reconstruct

```text
L_-=B D^(-1)B^T+K
```

and evaluate deterministic candidate vectors or local inequalities proposed
from exact algebra.  A record is admissible only if its stored
`contract_valid=true` and `trajectory_physical_valid=true`.  The validity
predicate is separate from the sign/score being explored.

## Domain, arithmetic, and reproducibility

The inherited retained set contains finite binary64 points through `n=7`;
its exact scope and exclusions remain those of the frozen R8 computation
contract.  New analysis uses IEEE-754 binary64 and deterministic iteration,
with no random seed and no optimizer.  Source hashes and output hashes must
be recorded if a new output file is frozen.

A second, separately labeled deterministic local-triplet scout is permitted
on the Cartesian grid

```text
mu in {1.05,1.2,1.5,2,3},
R in {1.01,1.5,2,10,100},
C=q^2-1 in {0.01,0.1,1,10},
initial p/U in {-5,-2,-1,0,1,2,5}.
```

It starts at a transverse `+` quotient event with `U=1`, chooses
`V=1/mu`, `V_t=-sqrt(p^2+C)` so the common energy is exactly `-C`, and
propagates the min material word `1,R,1` to the first three opposite-label
quotient events by analytic oscillator formulas plus deterministic Brent
bracketing.  Retain only strict-sign cells with `0<theta<pi/mu`, correct
crossing orientation, nonzero event amplitudes, and relative event-energy
residual at most `1e-9`.  This scout tests whether a local three-cell theorem
follows from cell gluing and R8 phase thresholds alone.  Even an exact-looking
binary64 witness is not an O3a counterexample because common indexed terminal
zeros and the global initial/terminal word are absent.

## Adversarial tests and proof bridge

Test max/min labels separately, the smallest `n=2` records, extreme stored
`R`, asymmetric-labeled records, and ill-conditioned points.  A sampled
inequality can only nominate or falsify a symbolic lemma.  Universal `(T)`
requires an exact derivation from globally glued relay identities; no finite
run is a proof.  A sign anomaly is only a counterexample candidate until all
premises are interval/exactly certified.

## Deterministic longer local-word scout

A third, separately labeled discovery check may propagate the same exact
initial-event data through `2n-1` alternating min cells on the Cartesian
grid

```text
n in {3,4,5,6},
mu in {1.05,1.5,3},
R in {1.01,2,100},
C in {0.1,1,10},
initial p/U in {-2,0,2}.
```

It uses the same first-opposite-event, strict-cell-sign, phase-threshold,
orientation, and event-energy predicates as the local-triplet scout.  The
tested statements are only `H>0` and the proposed dual vector certificate

```text
z_j=(gamma_(2j+1)-gamma_(2j))/abs(K_(2j))^(3/2)>0,
H z>0.
```

These 324 initial conditions omit the common terminal, terminal index, and
global initial predicates.  Success is `NUMERICAL_EVIDENCE`; failure is only
a local-mechanism falsifier until the relevant exact premises are certified.

## Relaxed interface-factor falsification

To test whether the R8 phase thresholds plus only continuity of the switch
derivative could prove the `n=2` scalar, a deterministic grid may use
`mu in {1.05,1.5,2,3}`, `sqrt(R) in {1.005,1.2,2,10}`, 12 equally spaced
positive phases on `(0,pi/(mu+1))`, 12 negative phases on
`(pi/(mu+1),pi/mu)`, and `abs(z_2)` in
`{0.01,0.03,0.1,0.3,1,3,10,30,100}`.  The exact endpoint derivative
relations determine `z_1,z_3`; reject any point outside the positive-cell
amplitude branch.  A nonpositive scalar here refutes only that relaxed
proof mechanism, because the second (energy/log-momentum) interface
equation is deliberately omitted.  It is not a physical counterexample.
