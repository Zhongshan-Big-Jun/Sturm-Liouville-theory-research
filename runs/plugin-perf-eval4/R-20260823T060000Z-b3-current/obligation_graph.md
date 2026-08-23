# Obligation graph

## Claims / dependencies / status

```mermaid
graph TD
  A[O1: sup over 2n-switch [1,R,1,...,1] = c_n(R)] --> B[O1a: symmetric/equal widths optimal]
  A --> C[O1b: value c_n(R)]
  A --> D[Baseline: every global max is [1,R,1,...,1] with 2n switches (STRICT)]
  D --> A
  E[O2: equal-within-type family max at r=sqrt R] --> F[Baseline: balanced secular root count (STRICT)]
  E --> G[New STRICT: general alternating Chebyshev secular representation]
  G --> H[O2 attempt: elliptic phase equation]
  H --> I[Gap: x-dependent delta]
  E --> B
  A --> J[Open: no proof]
  E --> J
```

## Proof statuses

| Node | Status | Detail |
| --- | --- | --- |
| D ratio extremizer structure | STRICT | baseline |
| F 2n-root count | STRICT | baseline, O3 closed |
| G general alternating Chebyshev representation | STRICT | this run, new |
| K amplitude equality in maximizers | STRICT | this run corollary |
| H elliptic phase equation | STRICT derivation | this run |
| I central-pair monotonicity in r | OPEN | exact O2 gap |
| O1 global equal-width optimality | OPEN | not proved |
| O2 alternating-family maximum | OPEN | not proved |

## Register of unresolved obligations

- Prove `Lambda_n(r) <= Lambda_n(sqrt(R))` for all `r>0`, `n>=1`, `R>1`.
- Prove among arbitrary widths `a_i,b_i`, `Lambda_n` is bounded by `c_n(R)`.
- If using the Chebyshev representation, quantify how the x-dependent `delta`
  changes the central Chebyshev branch.
