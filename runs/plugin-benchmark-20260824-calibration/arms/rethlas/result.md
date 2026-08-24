# Result: B3 O3 Root Count

**Theorem (strict).** For every integer `n >= 1` and every real `R > 1`, the function
`G_{n,s}(y) = (E(y) C_s(y)^n)_{12}` has exactly `2n` zeros in `(0, pi)`, all simple.
In fact the conclusion also holds at the boundary `R = 1`.

## 1. Notation

Let `s = sqrt(R)`. Put

```
c = cos(y),    q = sin(y),
A = (s+1)^2/s = 2 + s + 1/s,
B = s + 1/s,
a = 1/s.
```

Let `U_k` denote the Chebyshev polynomial of the second kind, with
`U_{-1} = 0`, `U_0 = 1`, and

```
U_k(cos(theta)) = sin((k+1)theta) / sin(theta).
```

The task's polynomial form is

```
Q_{n,s}(x) = G_{n,s}(arccos(x)) / sqrt(1-x^2).
```

## 2. Reduction to a Chebyshev combination

**Lemma 1.** For all real `y`,

```
det C_s(y) = 1,          trace C_s(y) = A c^2 - B.
```

**Proof.** A direct expansion gives

```
det C_s
= (c^2 - s^{-1} q^2)(c^2 - s q^2) + (1+s^{-1})(1+s) c^2 q^2
= c^4 + 2 c^2 q^2 + q^4 = (c^2+q^2)^2 = 1,
```

and

```
trace C_s
= 2 c^2 - (s + s^{-1}) q^2
= 2 c^2 - B(1-c^2)
= A c^2 - B.
```

**Lemma 2.** For every `n >= 1` and every `x in (-1,1)`,

```
Q_{n,s}(x) = U_n(z) + s^{-1} U_{n-1}(z),
   where z = z(x) = (A x^2 - B)/2.
```

**Proof.** By Cayley-Hamilton applied to the `2x2` matrix `C_s`, which has
determinant `1` and trace `tau = A c^2 - B`,

```
C_s^n = U_{n-1}(tau/2) C_s - U_{n-2}(tau/2) I
```

for all `n >= 1`. Hence, with `z = tau/2`,

```
G_{n,s}
= U_{n-1}(z) (E C_s)_{12} - U_{n-2}(z) E_{12}.
```

A direct computation gives

```
(E C_s)_{12}
= c (1+s^{-1}) c q + q (c^2 - s q^2)
= q (A c^2 - s).
```

Since `E_{12} = q`, we obtain

```
G_{n,s} = q [ U_{n-1}(z) (A c^2 - s) - U_{n-2}(z) ].
```

But

```
A c^2 - s = (2z + B) - s = 2z + 1/s,
```

so the bracket is

```
U_{n-1}(z)(2z + 1/s) - U_{n-2}(z)
= [2z U_{n-1}(z) - U_{n-2}(z)] + s^{-1} U_{n-1}(z)
= U_n(z) + s^{-1} U_{n-1}(z).
```

Therefore, for `x = cos(y)`,

```
Q_{n,s}(x) = G_{n,s}/sin(y) = U_n(z) + s^{-1} U_{n-1}(z).
```

This also proves the stated polynomial extension: `Q_{n,s}` is a polynomial in `x`,
indeed an even polynomial of degree `2n`.

## 3. Root count of the Chebyshev combination

**Lemma 3.** For every `n >= 1` and every `0 < a <= 1`, the polynomial

```
F(z) = U_n(z) + a U_{n-1}(z)
```

has exactly `n` simple zeros in `(-1,1)`.

**Proof.** For `z in (-1,1)`, write `z = cos(theta)` with `theta in (0,pi)`.
Then

```
F(cos(theta)) = [ sin((n+1)theta) + a sin(n theta) ] / sin(theta)
              =: h(theta) / sin(theta).
```

Because `sin(theta) > 0` on `(0,pi)`, the zeros of `F` in `(-1,1)` are in one-to-one
correspondence with the zeros of `h` in `(0,pi)`.

Let `theta_k = k*pi/n` for `k = 0,1,...,n`. At the interior nodes `1 <= k <= n-1`,

```
h(theta_k) = sin((n+1) k pi/n)
           = sin(k pi + k pi/n)
           = (-1)^k sin(k pi/n),
```

which is nonzero and has sign `(-1)^k`.

For small `epsilon > 0`,

```
h(epsilon) = sin((n+1)epsilon) + a sin(n epsilon)
           = (n+1+an) epsilon + O(epsilon^3) > 0,
```

and

```
h(pi - epsilon)
= sin((n+1)pi - (n+1)epsilon) + a sin(n pi - n epsilon)
= (-1)^n [ (n+1 - a n) epsilon + O(epsilon^3) ].
```

Since `0 < a <= 1`, we have `n+1 - a n >= 1 > 0`, so the sign of `h(pi-epsilon)`
is `(-1)^n` for all sufficiently small `epsilon > 0`.

Thus the signs at the sampled points

```
h(epsilon), h(theta_1), h(theta_2), ..., h(theta_{n-1}), h(pi-epsilon)
```

alternate. By the intermediate value theorem, there is at least one zero of `h`
in each of the `n` disjoint intervals

```
(epsilon, theta_1), (theta_1, theta_2), ..., (theta_{n-1}, pi-epsilon).
```

Hence `F` has at least `n` distinct zeros in `(-1,1)`.

On the other hand, `F` is a polynomial of degree exactly `n` (the leading term of
`U_n` is `2^n z^n`), so it has at most `n` roots in `(-1,1)`. Therefore it has
exactly `n` roots, and they are distinct. A degree-`n` polynomial with `n`
distinct zeros has no multiple zero, so all roots are simple.

**Lemma 4.** If `s > 1`, then `F(z) = U_n(z) + s^{-1} U_{n-1}(z)` has no zero for
`z < -1`.

**Proof.** Write `z = -cosh(theta)` with `theta > 0`. Using
`U_k(-cosh(theta)) = (-1)^k sinh((k+1)theta)/sinh(theta)`, we get

```
F(z) = (-1)^n [ sinh((n+1)theta) - s^{-1} sinh(n theta) ] / sinh(theta).
```

For `s > 1` and `theta > 0`,

```
sinh((n+1)theta) > sinh(n theta) > s^{-1} sinh(n theta),
```

so the bracket is strictly positive. Hence `F(z) != 0`.

## 4. Proof of the main theorem

For `x in (0,1)`, the map

```
z(x) = (A x^2 - B)/2
```

is strictly increasing, with

```
z(0) = -(s + 1/s)/2,       z(1) = 1.
```

For `s > 1`, `z(0) < -1`. By Lemma 4, `F(z)` has no zeros for `z < -1`;
hence all zeros of `F(z(x))` for `x in (0,1)` correspond to `z in (-1,1)`.

By Lemma 3, `F` has exactly `n` simple zeros in `(-1,1)`. Because `z` maps `(0,1)`
bijectively onto `(z(0),1)`, those `n` roots give exactly `n` distinct simple
roots of `Q_{n,s}(x)` in `(0,1)`. Since `Q_{n,s}` is even, there are exactly `n`
simple roots in `(-1,0)` as well, and none at `x = 0`.

Finally, `x = cos(y)` is a bijection from `(0,pi)` to `(-1,1)`, and

```
G_{n,s}(y) = sin(y) Q_{n,s}(cos(y)).
```

Because `sin(y) > 0` on `(0,pi)`, the zeros of `G_{n,s}` in `(0,pi)` are exactly
the zeros of `Q_{n,s}` in `(-1,1)`. Therefore `G_{n,s}` has exactly `2n` zeros in
`(0,pi)`.

**Simplicity.** At each positive root `x_0 in (0,1)`, the root `z_0 = z(x_0)` is
simple for `F`. Since

```
d/dx Q_{n,s}(x) = F'(z(x)) A x,
```

and `A > 0`, `x > 0`, the root is simple in `x`. At a negative root the same holds
with `x < 0`; the factor `A x` is still nonzero. The change of variable
`y = arccos(x)` has derivative `dy/dx = -1/sin(y) != 0`, so the root is simple in
`y` as well.

Thus the theorem is proved.

## 5. Boundary audits requested by the task

- **`n = 1`.** From Lemma 2, `Q_{1,s}(x) = A x^2 - s`, whose roots are
  `x = +/- s/(s+1)`. Both lie in `(-1,1)`, so `G_{1,s}` has exactly two simple zeros in `(0,pi)`.

- **`y = 0` and `y = pi`.** At these endpoints `q = 0`, and `E` and `C_s` are both
  diagonal (`C_s = I`), so `G_{n,s} = 0`. These endpoint zeros are not counted.
  The corresponding values `Q_{n,s}(+/-1)` are nonzero: because `Q_{n,s}` is even,
  `Q_{n,s}(-1) = Q_{n,s}(1) = n+1 + n/s > 0`.

- **`y = pi/2`.** Here `x = 0` and `z = -(s+1/s)/2`. For `s > 1` this is `<-1`,
  so Lemma 4 gives `Q_{n,s}(0) != 0`; for `s = 1`, `Q_{n,s}(0) = F(-1) = (-1)^n != 0`.
  Hence `y = pi/2` is never a zero.

- **Boundary `R = 1` (`s = 1`).** Then `a = 1`, and the interval `z in (-1,1)`
  covers the whole range `z(0) = -1` to `z(1) = 1`. Lemma 3 applies for `a = 1`,
  so `Q_{n,1}` still has exactly `2n` simple zeros in `(-1,1)`. Therefore the
  conclusion extends to `R = 1`.

## 6. Conclusion

The claim is **true** for every `n >= 1` and `R > 1`, and in fact for every
`R >= 1`. The proof uses only Cayley-Hamilton, the classical Chebyshev identity,
the intermediate value theorem, and standard properties of polynomials. No external
theorem beyond those elementary facts is needed.
