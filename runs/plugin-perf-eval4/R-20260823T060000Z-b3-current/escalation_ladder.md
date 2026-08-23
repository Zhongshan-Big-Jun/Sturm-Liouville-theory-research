# Escalation ladder

Current tier: Tier 2 (moderate systematic, local run).

## Tier log

| Tier | Actions | Outcome |
| --- | --- | --- |
| 0 | Read required context, quick web search, check local papers | No direct fixed-n theorem; baseline reproduced |
| 1 | Symbolic derivation of general alternating Chebyshev secular representation | New STRICT tool |
| 2 | Derive elliptic phase equation, Chebyshev monotonicity; numerical scans | O2 still open; exact gap identified |
| 3 | Heavy parallel route portfolio (not used) | Not needed for this run |

## Triggers considered

- Literature hit: no direct fixed-n ratio theorem found -> did not import.
- Numerical peak at `r=sqrt R`: not a proof trigger; did not escalate to claim.
- A possible proof route through x-dependent delta monotonicity was identified
  but not completed; would be the next Tier 3 route.

## Future minimal first step

For O2, prove that the function
`x -> (theta(x), delta(x))` crosses the central Chebyshev branch in a way
that makes `(x_{n+1}/x_n)^2` monotone away from `r = s`. A helpful intermediate
would be a strict bound on `delta(x)` on the central pair as a function of `r`.
