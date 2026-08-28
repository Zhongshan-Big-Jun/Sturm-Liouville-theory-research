# Counterexample and falsification log

## Mathematical boundary witnesses

- \(x^2\) is an exact witness against canonical identity of the completions:
  it is a member of the abstract polynomial pre-Hilbert space but violates both
  Krein endpoint equations (its endpoint derivatives are \(-2,2\) while its
  endpoint difference is zero).
- The formal solution \(x^2/c+2/c^2\) of \(Lu=x^2\) has residuals
  \((2/c,-2/c)\); the genuine resolvent adds a nonpolynomial hyperbolic
  correction.  This falsifies the identification
  \(L_{\rm poly}^{-1}=K_c^{-1}\).

## Implementation failure retained

- The first exact-check replay used `c - q''` instead of `c*q - q''` for
  inverse powers \(r>1\).  It failed at `r=2,n=0` and was repaired before the
  accepted replay.  This failure prevents accidental reuse of the malformed
  recurrence.

## Searches not performed

No numerical/random counterexample search, literature search, or project-file
search was performed.  Finite symbolic checks are evidence only.
