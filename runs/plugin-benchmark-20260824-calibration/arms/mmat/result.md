# Result: STRICT proof of the B3 O3 root count

**Status: STRICT / complete for the stated claim.**

## Theorem

For every integer `n >= 1` and every real `R > 1`, the function

```
G_{n,s}(y) = (E(y) C_s(y)^n)_{12},    s = sqrt(R),
```

has exactly `2n` zeros in the open interval `(0, pi)`, and every zero is simple.

The proof is uniform in `n` and `R > 1`. The boundary case `R = 1` also satisfies the same conclusion and is checked separately.

---

## Notational setup

Let

```
c = cos(y),  q = sin(y),  x = cos(y).
```

For `y in (0, pi)` we have `q > 0`, so `y <-> x in (-1,1)` is a bijection.

Define the Chebyshev polynomials of the second kind by

```
U_0(t) = 1,  U_1(t) = 2t,  U_{k+1}(t) = 2t U_k(t) - U_{k-1}(t),
```

with the convention `U_{-1}(t) = 0`.

---

## Step 1: determinant and conjugated matrix

A direct computation gives

```
det C_s(y) = (c^2 - s^{-1} q^2)(c^2 - s q^2) + (1+s^{-1})(1+s) c^2 q^2
           = (c^2 + q^2)^2 = 1.
```

Since `E(y)` is a rotation matrix, `det E = 1`. Let

```
D = D_{n,s}(y) := E(y) C_s(y) E(y)^{-1}.
```

Substituting the definitions gives the explicit formula

```
D = [[ c^2 - s q^2,        (1+s^{-1}) c q ],
     [ -(1+s) c q,          c^2 - s^{-1} q^2 ]],
```

and hence

```
tr D = 2 c^2 - (s + s^{-1}) q^2.
```

Because `D` is conjugate to `C_s`, it also has determinant `1`.

---

## Step 2: polynomial reduction

Use Cayley-Hamilton in the form

```
D^k = U_{k-1}(tr D / 2) D - U_{k-2}(tr D / 2) I      (k >= 1),
```

which is valid for every `2 x 2` matrix with trace `T` and determinant `1`, because
`D^2 - T D + I = 0` and the recurrence for `U_k` is exactly the same three-term
recurrence.

Since

```
E C_s^n = D^n E,
```

we obtain

```
G_{n,s}(y) = (D^n E)_{12}
           = U_{n-1}(u) (D E)_{12} - U_{n-2}(u) q,
```

where

```
u := tr D / 2 = alpha x^2 - beta,
alpha := (2 + s + s^{-1}) / 2,
beta  := (s + s^{-1}) / 2.
```

A direct computation gives

```
(D E)_{12} / q = (2 + s + s^{-1}) x^2 - s = 2u + s^{-1}.
```

Therefore, for `y in (0, pi)` (so `q > 0`),

```
Q_{n,s}(x) := G_{n,s}(arccos x) / sqrt(1 - x^2)
            = U_{n-1}(u) (2u + s^{-1}) - U_{n-2}(u)
            = U_n(u) + s^{-1} U_{n-1}(u),
```

where the last equality uses `U_n = 2u U_{n-1} - U_{n-2}`.

Thus `Q_{n,s}` is an even polynomial in `x`, with

```
u = alpha x^2 - beta,    alpha = 1 + beta > 0.
```

The leading coefficient of `Q_{n,s}` is `2^n alpha^n > 0`, so its degree is
exactly `2n`. This is the justified polynomial formulation.

---

## Step 3: root lemma for the Chebyshev-type polynomial

Set

```
lambda := s^{-1} in (0,1),
P_n(t) := U_n(t) + lambda U_{n-1}(t).
```

### Claim

For every `n >= 1` and every `lambda in (0,1]`, the polynomial `P_n` has exactly `n`
real zeros; they are all simple and lie in `(-1,1)`.

### Proof

The zeros of `U_n` are

```
z_k = cos(k pi / (n+1)),   k = 1, ..., n,
```

in decreasing order

```
-1 < z_n < z_{n-1} < ... < z_1 < 1.
```

At these points, using the standard identity `U_{n-1}(cos theta) = sin(n theta) / sin theta`,
with `theta_k = k pi / (n+1)`,

```
P_n(z_k) = lambda U_{n-1}(z_k)
         = lambda * sin(n theta_k) / sin(theta_k)
         = lambda * (-1)^{k+1}.
```

The last equality follows from `sin(n theta_k) = sin(k pi - theta_k) = (-1)^{k+1} sin(theta_k)`
and `sin(theta_k) > 0`. Hence the signs of `P_n(z_k)` alternate as `k` increases:
`+,-,+,-,...`.

Also

```
P_n(-1) = U_n(-1) + lambda U_{n-1}(-1)
        = (-1)^n (n+1) + lambda (-1)^{n-1} n
        = (-1)^n (n + 1 - lambda n).
```

Since `lambda <= 1`, `n + 1 - lambda n > 0`, so `P_n(-1)` has sign `(-1)^n`.
The last Chebyshev zero is `z_n`, and by the alternating formula

```
P_n(z_n) = lambda (-1)^{n+1}.
```

Thus `P_n(-1)` and `P_n(z_n)` always have opposite signs, giving one zero in
`(-1, z_n)`. For each `k = 1, ..., n-1`, the consecutive values `P_n(z_k)` and
`P_n(z_{k+1})` have opposite signs, giving one zero in `(z_{k+1}, z_k)`.

These `n` zero-containing intervals are pairwise disjoint, so `P_n` has at least `n`
distinct real zeros in `(-1,1)`. Since `deg P_n = n`, it has exactly `n` real
zeros, all in `(-1,1)`, and all simple.

---

## Step 4: return to `x` and `y`

Fix `s > 1`, so `beta > 1`. For every root `u` of `P_n` in `(-1,1)`, the equation

```
alpha x^2 - beta = u
```

has exactly two solutions in `(-1,1)`:

```
x = +/- sqrt( (u + beta) / alpha ).
```

Indeed `u > -1` implies `u + beta > beta - 1 > 0`, and `u < 1` implies
`u + beta < 1 + beta = alpha` because `alpha - beta = 1`. Hence both signs lie in
`(-1,1)`, and neither is `0`.

Therefore the even polynomial `Q_{n,s}` has exactly `2n` zeros in `(-1,1)`, all
simple. Since `y = arccos x` is a bijection `(-1,1) -> (0,pi)` and
`sqrt(1-x^2) = sin(y) > 0`, the original function `G_{n,s}` has exactly `2n`
zeros in `(0,pi)`, all simple.

---

## Boundary and special audits

1. **`n = 1`.** The formula gives
   `Q_{1,s}(x) = (2 + s + s^{-1}) x^2 - s`.
   The roots are
   `x = +/- sqrt( s / (2 + s + s^{-1}) )`.
   Since `s > 1`, `0 < s / (2 + s + s^{-1}) < 1`, so exactly two simple roots in
   `(-1,1)`. Hence `G_{1,s}` has exactly two simple zeros in `(0,pi)`. The general
   root lemma also covers this case.

2. **`y = 0`.** Here `c = 1`, `q = 0`, `E(0) = I`, `C_s(0) = I`, hence
   `M_{n,s}(0) = I` and `G_{n,s}(0) = 0`. This is an endpoint zero and is not
   counted.

3. **`y = pi`.** Here `c = -1`, `q = 0`, `E(pi) = -I`, `C_s(pi) = I`, hence
   `M_{n,s}(pi) = -I` and `G_{n,s}(pi) = 0`. This is an endpoint zero and is not
   counted.

4. **`y = pi/2`.** Here `c = 0`, `q = 1`, so
   `E(pi/2) = [[0,1],[-1,0]]` and `C_s(pi/2) = diag(-s^{-1}, -s)`.
   Therefore
   `G_{n,s}(pi/2) = (-s)^n != 0`.
   No zero passes through this point.

5. **`R = 1` (boundary of the parameter domain).** Let `s = 1` and `lambda = 1`.
   The root lemma applies with `lambda = 1` because `P_n(-1) = (-1)^n (1) != 0`
   and the alternating sign argument is unchanged. The same argument then gives
   exactly `2n` simple zeros in `(0,pi)`. Thus the conclusion extends to the
   boundary value `R = 1` as well.

---

## External results used

- Cayley-Hamilton theorem for `2 x 2` matrices, applied to the determinant-one
  matrix `D`.
- Standard identities for Chebyshev polynomials of the second kind:
  `U_n(cos theta) = sin((n+1) theta)/sin theta` and
  `U_{n-1}(cos theta) = sin(n theta)/sin theta`.
- The recurrence `U_{k+1}(t) = 2t U_k(t) - U_{k-1}(t)`.

All hypotheses are satisfied: `D` has determinant one, and `0 < lambda <= 1`.

---

## Verification note

The symbolic derivation has been checked against direct numerical evaluation of
the original matrix product for several `n`, `R`, and `x` (scratch computation
for falsification only; it is not part of the proof). The final result is a
uniform exact proof, not a numerical result.
