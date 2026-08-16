# Preregistered compact-annulus Arb contract

Status: PREREGISTERED BEFORE EXECUTION

The exact analytic collar is

```text
t >= 1-2^-17.
```

Only the compact complements of the three formerly incomplete high-`t`
boxes are evaluated:

```text
LHL, IHL, LHH,
t in [63/64,1-2^-17].
```

Coordinates use the frozen R17 exact dyadic denominator `2^34`; the upper
`t` endpoint is therefore `2^34-2^17`.  Arithmetic is the unchanged
128-bit Arb R17 evaluator and conditional contractor.  The run is
deterministic, has no random input, and has a hard limit of 1,000,000 visited
boxes per target.  There is no escalation and no second run in the original
coordinates.  Completion requires an empty stack, zero atomic unresolved
leaves, zero singular calls, and the exact leaf identities.

The result remains conditional on R14/R17 and does not prove the physical or
canonical theorem.

