# Candidate proof / rigorous partial result

Status label: `RIGOROUS_PARTIAL_RESULT`

This run does **not** close O1 or O2. It adds one new STRICT structural tool
for the general equal-within-type alternating family, plus a STRICT corollary
of the existing amplitude/energy invariant. All statements marked STRICT are
proved; all statements marked EVIDENCE are numerical only.

---

## Part A. Recap of round-2 strict results (not new)

1. **Ratio extremizer structure (STRICT).** Every global maximizer of
   `Lambda_n` over `1 <= rho <= R` is bang-bang `[1,R,1,...,1]` with exactly
   `2n` switches. (Reference: baseline candidate_proof Part A.)
2. **Balanced 2n-root count (STRICT).** For the balanced alternating
   configuration, `F_n(y)` has exactly `2n` simple roots in `(0,pi)`, closing O3.

---

## Part B. Notation for the equal-within-type alternating family

Let `R > 1`, `s = sqrt(R)`, `n >= 1`. Let

```
rho = [1, R, 1, R, ..., 1]   (2n+1 blocks)
```

with equal widths:

```
a = width of every 1-block,
b = width of every R-block,
(n+1) a + n b = 1.
```

Set `r = a/b`. Let `omega = sqrt(lambda)`, `x = omega b`. Then

```
p := omega a = r x,
q := omega s b = s x.
```

For an eigenvalue, the Dirichlet condition is the `(0,1)` element of the
total transfer matrix.

---

## Part C. General alternating Chebyshev secular representation (STRICT)

### Definitions

Use normalized transfer matrices (the factor `omega` does not affect zeros):

```
A(p) = [[cos p,  sin p],
        [-sin p, cos p]],

B(q) = [[cos q,  sin q / s],
        [-s sin q, cos q]].
```

Let

```
C(p,q) = A(p) B(q),
M_n(p,q) = C(p,q)^n A(p),
tau(p,q) = trace C(p,q) = 2 cos p cos q - (s + 1/s) sin p sin q,
m(p,q) = tau(p,q)/2,
delta(p,q) = sin q / (s sin p)   (read by continuity when `sin p = 0`;
equivalently `sin(p) delta = sin q / s`).
```

`M_n` is the transfer matrix of the chain `[1,R,1,...,1]` with equal
within-type widths.

### Lemma C1 (secular representation)

For every `n >= 0`,

```
(M_n)_{0,1} = sin(p) U_n(m) + (sin q / s) U_{n-1}(m)
            = sin(p) [ U_n(m) + delta U_{n-1}(m) ],
```

where `U_k` is the Chebyshev polynomial of the second kind
(`U_{-1}=0`, `U_0=1`, `U_k = 2m U_{k-1} - U_{k-2}`).

#### Proof

By Cayley-Hamilton for a real 2x2 matrix with determinant 1,

```
C^n = U_{n-1}(m) C - U_{n-2}(m) I        (n >= 1).
```

Thus

```
(M_n)_{0,1} = (C^n)_{0,0} sin p + (C^n)_{0,1} cos p
= U_{n-1}(m) (C_{0,0} sin p + C_{0,1} cos p) - U_{n-2}(m) sin p.
```

A direct computation gives

```
C_{0,0} = cos p cos q - s sin p sin q,
C_{0,1} = sin p cos q + (sin q cos p)/s,
```

and therefore

```
C_{0,0} sin p + C_{0,1} cos p
 = 2 m sin p + (sin q / s)
 = (2m + delta) sin p.
```

Using `U_n(m) = 2m U_{n-1}(m) - U_{n-2}(m)`, we obtain

```
(M_n)_{0,1} = sin p [ U_n(m) + delta U_{n-1}(m) ].
```

For `n = 0`, the formula reduces to `(M_0)_{0,1} = sin p`, which is true.
QED.

### Remark

For the balanced case `r = s`, we have `p = q = y`, `delta = 1/s`,
`m = cos^2 y - ((s+1/s)/2) sin^2 y`, and Lemma C1 recovers the round-2
Jacobi-matrix tool `P_n(x) = U_n(t) + (1/s) U_{n-1}(t)`.

---

## Part D. Elliptic-zone phase equation (STRICT derivation, O2 still open)

Assume that at a point `x` of interest `|m(x)| < 1`. Write

```
m = cos theta, theta in (0,pi).
```

For any fixed `delta`, the equation `U_n(m) + delta U_{n-1}(m) = 0` is
equivalent to

```
sin((n+1) theta) + delta sin(n theta) = 0.
```

This is a direct consequence of the Chebyshev identities
`U_k(cos theta) = sin((k+1)theta)/sin theta`.

For the equal-within-type family, `delta = delta(x)` is not constant, so the
roots `x` of the secular equation satisfy the x-dependent equation

```
sin((n+1) theta(x)) + delta(x) sin(n theta(x)) = 0.
```

### Lemma D1 (STRICT)

For fixed `0 < delta < 1`, the `n` roots of
`U_n(m) + delta U_{n-1}(m) = 0` are all real and lie in `m in (-1,1)`.

#### Proof

The combination `p_n(z) + delta p_{n-1}(z)` with `z = 2m` is the
characteristic polynomial of a real symmetric tridiagonal `n x n` matrix
with off-diagonal `1` and bottom-right `-delta`; hence it has `n` real
eigenvalues. To see all lie in `(-2,2)`, repeat the hyperbolic/endpoint
argument from the round-2 proof: for `z > 2` the expression is positive;
for `z < -2`, using `z = -2 cosh theta` gives
`(-1)^n [sinh((n+1)theta) - delta sinh(n theta)]/sinh theta`, strictly
positive because `delta < 1` and `sinh((n+1)theta) > sinh(n theta)`;
at `z = +/-2` the expressions are nonzero. QED.

### Exact gap for O2

Lemma D1 is for a constant `delta`. In the actual equal-within-type family,
the `n`-th and `(n+1)`-th roots are two points on the curve
`z = 2m(x)`, `delta = delta(x)`, intersecting different fixed-`delta`
Chebyshev branches. A proof of `Lambda_n(r) <= Lambda_n(s)` thus requires a
quantitative understanding of how the curve moves with `r`. This run did not
obtain that inequality.

---

## Part E. Strict corollary of the ratio energy invariant

**Corollary (amplitude equality, STRICT).** Let `rho*` be any global maximizer
of `Lambda_n`. On each maximal constant block of `rho*`, the normalized
eigenfunctions `u_n` and `u_{n+1}` have equal amplitudes.

#### Proof

On a block with density `rho_0`, the baseline energy invariant gives

```
E = lambda_{n+1} (u_n'^2 + lambda_n rho_0 u_n^2)
  - lambda_n (u_{n+1}'^2 + lambda_{n+1} rho_0 u_{n+1}^2) = 0.
```

Write `u_n = A_n sin(k_n x + phi_n)`, `u_{n+1} = A_{n+1} sin(k_{n+1} x + phi_{n+1})`
on that block. The two parantheses are the constants
`A_n^2 k_n^2` and `A_{n+1}^2 k_{n+1}^2` respectively. Since
`k_{n+1} = k_n / c` with `c = sqrt(lambda_n/lambda_{n+1})`, substitution gives

```
lambda_{n+1} A_n^2 k_n^2 - lambda_n A_{n+1}^2 (k_n/c)^2
= lambda_{n+1} k_n^2 (A_n^2 - A_{n+1}^2)
```

(up to positive factors), so `A_n = A_{n+1}`. QED.

---

## Part F. Numerical evidence (EVIDENCE, not proof)

- O2 scans for `R=4, n=2`: ratio as a function of `r` has a single maximum
  near `r = sqrt(R) = 2` (ratio ~ 4.2846 at `r=2`, ~4.1898 at `r=1.5`,
  ~4.2266 at `r=2.5`).
- O2 scans for `R=2, n=1`: maximum near `r = 1.414` (closed by the known
  B1 result).
- Random width-simplex optimization for `n=2,R=4` repeatedly recovered the
  balanced widths `(0.25,0.125,0.25,0.125,0.25)`; this is EVIDENCE only.
- The general Chebyshev representation was verified numerically to
  machine precision (s=2, r in {1,1.5,2,2.5,3}, n=1..5, max error ~1e-14),
  which is not needed for the proof but confirms the algebra.

## Conclusion

O1 and O2 remain open. The new strict material is a useful reduction and
tool for future attacks on O2, but no claim of closure is made.
