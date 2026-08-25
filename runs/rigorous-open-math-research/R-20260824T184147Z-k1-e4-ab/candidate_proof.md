# Candidate Proof - K(1) strict anchor

Run: `R-20260824T184147Z-k1-e4-ab`
Status: `STRICT`

The full proof is in `docs/SL_third_order_K1_proof.tex`.

## Core result

The exact normalized minimal solution is

```text
mu*_j = 2 e (2j)! sum_{r=j+2..infinity} (r-j-1)/(2r-1)!.
```

The finite backward solution is

```text
mu^(N)_j = (2j)!/(2N+2) * sum_{r=j+2..N} (r-j-1)/(2r-1)!.
```

## Proof bridge

Set `v_j = mu_j/(2j)!` and
`c_j = 1/(2(j-1)(2j-1))`.  The recurrence becomes

```text
v_j = (2+c_j)v_{j-1} - (1+2c_j)v_{j-2} + c_j v_{j-3}.
```

With `d_j = v_j - 2 v_{j-1} + v_{j-2}`, this is exactly
`d_j = c_j d_{j-1}`.  The terminal conditions give the finite positive
factorial formula above.  Its denominator tends to `1/(2e)`, so every fixed
index limit exists.  The complete scaled solution is `A + B j + C phi_j`,
where `phi_j` is the positive factorial tail and tends to zero.  Hence the
minimal subfactorial branch is one-dimensional and normalization at index zero
fixes its multiplier.  The first term of the tail is
`2e/((2j+1)(2j+2)(2j+3))`; an explicit geometric bound controls all remaining
terms and gives the exact limit `e/4`.

## Strictness boundary

The proof does not claim a closed form for the general `K(c)`.  The previous
high-precision numerical value is retained only as historical provenance in
the source document and is not used as evidence for the strict theorem.
