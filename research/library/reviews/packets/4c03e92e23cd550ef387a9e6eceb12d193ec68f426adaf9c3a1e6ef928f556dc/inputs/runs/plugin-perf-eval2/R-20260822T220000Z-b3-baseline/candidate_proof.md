# Candidate proof / rigorous partial result

Status label: `RIGOROUS_PARTIAL_RESULT`
This document contains two newly proved **strict** results:

1. A structural theorem for every global fixed-n ratio maximizer (reduces O1
   to finite-dimensional `[1,R,1,...,1]` optimization).
2. A complete proof of the general 2n-root count for the alternating balanced
   secular polynomial (closes O3).

The full value `c_n(R)` and the equal-width optimum (O2, the remaining part
of O1) are still open.

---

# Part A. Ratio extremizer structure

## Theorem (Ratio extremizer structure)

Fix `R>1` and `n>=1`. Let `rho*` be any global maximizer of

```
Lambda_n(rho) = lambda_{n+1}(rho)/lambda_n(rho)
```

over the measurable box `1 <= rho <= R` a.e. Let `u_n,u_{n+1}` be the
corresponding normalized eigenfunctions with

```
int_0^1 rho* u_k^2 dx = 1,   u_k'(0) > 0,   k = n, n+1.
```

Define the ratio switching function

```
H(x) = u_n(x)^2 - u_{n+1}(x)^2.
```

Then:

1. `rho*` is bang-bang: `rho* = R` a.e. on `{H>0}` and `rho* = 1` a.e. on `{H<0}`.
2. `H` has exactly `2n` simple zeros in `(0,1)`.
3. Every zero of `H` is a switch of `rho*` and every switch is a zero of `H`.
   Consequently `rho*` has exactly `2n` effective switches and exactly `2n+1`
   positive-length blocks, with alternating material order
   `[1, R, 1, R, ..., 1]` (both end blocks are `1`).

## Proof

### 1. Existence and regularity

The same weak-star compactness and spectral continuity argument used for the
gap functional `D_n` (see `docs/SL_gap_nge2_finite_reduction_proof.tex`)
applies verbatim: `lambda_k(rho)` is continuous in the weak-star topology on
`K_R = {1<=rho<=R}` and `K_R` is weak-star compact. Since the ratio is a
positive quotient of two continuous functions, `Lambda_n` attains its maximum
on `K_R`. Let `rho*` be a maximizer.

Regularity is standard: eigenfunctions are `W^{2,infty}(0,1) subset C^1`, and
all eigenvalues are simple. Phase-nodal theory gives that `u_k` has exactly
`k-1` simple interior zeros, and adjacent modes strictly interlace.

### 2. Feynman-Hellmann derivative for the ratio

For `h in L^infty(0,1)` and `rho + eps h in K_R`, the standard eigenvalue
derivative is

```
d/deps lambda_k(rho+eps h)|_{eps=0} = -lambda_k int_0^1 h u_k^2 dx,
```

with the weighted normalization above. Hence

```
d/deps (lambda_{n+1}/lambda_n)
  = (lambda_{n+1}/lambda_n) int_0^1 h (u_n^2 - u_{n+1}^2) dx
  = Lambda_n(rho) int_0^1 h H dx.
```

Since `Lambda_n(rho)>0`, the sign of the derivative is exactly the sign of
`int h H`.

### 3. Complete box saturation

Let `A_delta = {rho* <= R-delta}`. For any bounded `h>=0` supported in
`A_delta`, the direction `h` is admissible and maximality gives
`int h H <= 0`. Taking a countable union over rational `delta`, we get
`H <= 0` a.e. on `{rho* < R}`. Similarly, using `h = -phi` with `phi>=0`
supported in `{rho* > 1}`, we get `H >= 0` a.e. on `{rho* > 1}`.

Therefore, on any set of positive measure where `H>0`, we cannot have
`rho* < R`, so `rho* = R`; on `{H<0}`, we get `rho* = 1`. This is the
saturation law.

### 4. Wronskian and zero count for H

Use the same proof as in the gap case. Let `W = u_{n+1}' u_n - u_{n+1} u_n'`.
Then `W<0` on `(0,1)`. On each interval between consecutive zeros of `u_n`,
the quotient `q = u_{n+1}/u_n` is strictly decreasing, because

```
q' = W/u_n^2 < 0.
```

In each such interval, `u_n != 0`, and

```
H = u_n^2 (1 - q^2).
```

Thus a zero of `H` occurs exactly when `q = +1` or `q = -1`. The ranges of
`q` on the first, middle, and last nodal intervals give the exact count:

```
# {H = 0 in (0,1)} = 2n - 2 + 1_{q0 > 1} + 1_{q1 < -1},
```

where `q0 = u_{n+1}'(0)/u_n'(0) > 0` and
`q1 = u_{n+1}'(1)/u_n'(1) < 0`. (For `n=1` the same formula gives
`1_{q0>1} + 1_{q1<-1}`.)

Each zero is simple: at a zero, `u_n != 0` and `q = ±1`, so

```
H' = u_n^2(-2 q q') != 0.
```

Hence all zeros are simple and `H` changes sign at each.

**Zero-switch identification.** The zero set of `H` is finite and simple.
On each connected component of `(0,1) \ {H=0}`, the sign of `H` is constant.
By saturation, `rho*` is equal to a single box endpoint on that whole
component. Therefore any switch of `rho*` (a boundary between two different
constant values) must be a zero of `H`. Conversely, at each simple zero the
sign of `H` changes, so the assigned material `1` or `R` changes; hence every
zero of `H` is a switch.

### 5. Ratio energy invariant

On a block where `rho* = r` constant, define

```
E_n = u_n'^2 + a r u_n^2,          a = lambda_n,
E_{n+1} = u_{n+1}'^2 + b r u_{n+1}^2,  b = lambda_{n+1},
E = b E_n - a E_{n+1}.
```

Using the eigenvalue equations, each of `E_n` and `E_{n+1}` is constant on the
block. At a switch `s`, with one-sided densities `r_-` and `r_+`, the only
jump in `E` is

```
E(s_+) - E(s_-) = (r_+ - r_-)( b a u_n(s)^2 - a b u_{n+1}(s)^2 )
                = ab (r_+ - r_-) H(s).
```

By the saturation and zero-switch identification, every switch is a zero of
`H`, so this jump is `0`. Therefore `E` is a global constant on `[0,1]`.

Integrating `E` over `[0,1]` and using the normalizations

```
int_0^1 rho* u_n^2 dx = int_0^1 rho* u_{n+1}^2 dx = 1,
int_0^1 u_n'^2 dx = a,   int_0^1 u_{n+1}'^2 dx = b,
```

we get

```
int_0^1 E dx = b a - a b + ab(1-1) = 0.
```

Hence `E = 0` everywhere.

At the endpoints the eigenfunctions vanish, so

```
0 = E(0) = b u_n'(0)^2 - a u_{n+1}'(0)^2,
0 = E(1) = b u_n'(1)^2 - a u_{n+1}'(1)^2.
```

Thus

```
|u_{n+1}'(0)/u_n'(0)| = |u_{n+1}'(1)/u_n'(1)| = sqrt(b/a) = 1/c,
c = sqrt(a/b) in (0,1).
```

With the chosen orientation `u_k'(0)>0`, this gives

```
q0 = 1/c > 1,   q1 = -1/c < -1.
```

### 6. Exact switch count and material order

Inserting `q0>1` and `q1<-1` into the zero-count formula gives exactly
`2n` zeros of `H` in `(0,1)`. Since every zero is simple and each zero is a
switch, the maximizer has exactly `2n` effective switches.

Near both endpoints, `H(x) < 0` because `q0>1` and `q1<-1`:
`H = u_n'^2(1-q0^2)x^2 + o(x^2) < 0` near `0`, and similarly near `1`.
The saturation law for a maximizer then forces `rho*=1` on the first and last
blocks. Since the simple zeros alternate the sign of `H`, the density
necessarily alternates `1, R, 1, R, ..., 1`. This completes the proof.

## Consequences

- Any global maximizer of `Lambda_n` is a finite bang-bang `[1,R,1,...,1]`
  configuration with exactly `2n` switches. This is a strict reduction of O1
  to a finite-dimensional optimization problem.
- The theorem is a direct analogue of the exact `2n` switch theorem for the
  gap `D_n` in `docs/SL_gap_nge2_exact_2n_switches_proof.tex`, but for the
  ratio functional it is even simpler (the switching function has no
  eigenvalue weighting).
- The theorem does **not** prove:
  - the actual switch positions/block lengths;
  - that the maximizing `[1,R,1,...,1]` must be the equal-width balanced
    configuration `w_1/w_2 = sqrt(R)`;
  - the value `c_n(R)` or the 2n-root count of the alternating secular
    polynomial.

## Verification

- Independent numerical checks (EVIDENCE only, not part of the proof):
  - For `R in {2,4,10}`, `n=1..5`, the alternating maximizer has
    `q0 = 1/c`, `q1 = -1/c` to displayed precision.
  - `H` has exactly `2n` interior zeros when endpoint counts are removed
    (small numerical noise at endpoints/interfaces is visible in the grid
    diagnostics).
  - `E` is approximately constant and close to `0` on each block
    (finite-difference integration error ~1e-3).

---

# Part B. 2n-root count for the alternating balanced secular polynomial (O3, STRICT)

**Theorem (O3).** For every `n>=1` and `R>1`, let `F_n(y)` be the secular
function of the balanced alternating configuration

```
rho = [1,R,1,R,...,1],  w_1/w_2 = sqrt(R),
t = 1/((n+1) sqrt(R) + n).
```

Then `F_n(y)` has exactly `2n` roots in `(0,pi)`, all simple. Equivalently,
if `F_n(y)=sin(y) Q_n(cos y)`, then `Q_n(C)` has exactly `2n` distinct roots
in `(-1,1)`.

## Proof

### B1. Recurrence for the secular function

Let `s = sqrt(R)`, `y = omega s t`. Write `T_cell(y)` for the cell transfer
matrix of a `[1,R]` pair and `T_end(y)` for the final `[1]` block. Let

```
G_n(y) = omega * (T_end(y) T_cell(y)^n)_{01},
```

so that the Dirichlet condition is `G_n(y)=0`. Here `omega > 0` and `G_n = omega F_n`, so the zeros of `G_n` coincide exactly with the zeros of `F_n`. A direct computation gives

```
T_cell = [[cos^2 y - s^{-1} sin^2 y, *(1+s) sin y cos y / (omega s)],
          [-omega(1+s) sin y cos y, cos^2 y - s sin^2 y]]
```

and `det T_cell = 1`. Let

```
tau(y) = tr T_cell(y)
       = 2 cos^2 y - (s + 1/s) sin^2 y
       = ((s+1)^2/s) cos^2 y - (s^2+1)/s.
```

By Cayley-Hamilton, `T_cell^2 = tau T_cell - I`. Therefore for `n >= 2`,

```
G_n = tau G_{n-1} - G_{n-2}.
```

With `G_0 = sin y` (the `T_end` alone) and `G_1 = sin y Q_1(cos y)`, we get
`G_n = sin y Q_n(cos y)`, where `Q_0=1` and

```
Q_1(C) = ((s+1)^2/s) C^2 - s,
Q_n(C) = tau(C) Q_{n-1}(C) - Q_{n-2}(C),   n >= 2.
```

### B2. Change to the square variable

Let `x = C^2 in [0,1]` and `P_n(x) = Q_n(sqrt(x))`. Then

```
P_0(x) = 1,
P_1(x) = A x - s,
P_n(x) = (A x - B) P_{n-1}(x) - P_{n-2}(x)   (n >= 2),
```

where

```
A = (s+1)^2/s,   B = (s^2+1)/s = A - 2.
```

### B3. Identification with Chebyshev polynomials and a Jacobi matrix

Set

```
t = (A x - B)/2,   delta = 1/s,   z = 2t,
U_k = Chebyshev second kind (U_0=1, U_1=2t, U_k=2t U_{k-1} - U_{k-2}).
```

Then

```
P_n(x) = U_n(t) + delta U_{n-1}(t).
```

Indeed the right-hand side satisfies the same recurrence and initial values:
`R_0=1`, `R_1=2t+delta = A x - B + 1/s = A x - s = P_1`.

Let `p_k(z) = U_k(z/2)`. Then `p_0=1`, `p_1=z`, `p_k=z p_{k-1}-p_{k-2}` and

```
R_n(t) = p_n(z) + delta p_{n-1}(z).
```

This is exactly the characteristic polynomial of the `n x n` real symmetric
tridiagonal matrix

```
J_n(delta) =
  [0  1  0  ...  0]
  [1  0  1  ...  0]
  [ ...        ... ]
  [0  ...  1  0    1]
  [0  ...  0  1  -delta].
```

More precisely, `det(z I - J_n(delta)) = p_n(z) + delta p_{n-1}(z)` (for
`n>=1`; for `n=1` it is `z+delta`). Because the off-diagonal entries are all
`1`, a real symmetric tridiagonal matrix with non-zero off-diagonal entries
has simple real spectrum. Hence `P_n(x)`, as a polynomial in the affine
variable `x`, has `n` distinct real roots.

### B4. All roots lie in `(-1,1)` in the t variable

We show the roots `z=2t` of `q_n(z)=p_n(z)+delta p_{n-1}(z)` all lie in
`(-2,2)`.

- If `z > 2`, write `z = 2 cosh theta` with `theta > 0`. Then
  `p_k(z) = sinh((k+1)theta)/sinh theta > 0`, so `q_n(z) > 0`.
- If `z < -2`, write `z = -2 cosh theta`. Then
  `p_k(z) = (-1)^k sinh((k+1)theta)/sinh theta`, and

  ```
  q_n(z) = (-1)^n [ sinh((n+1)theta) - delta sinh(n theta) ] / sinh theta.
  ```

  Since `delta = 1/s <= 1` and `sinh((n+1)theta) > sinh(n theta)` for
  `theta > 0`, the bracket is strictly positive. Hence `q_n(z) != 0`.
- At the endpoint `z = 2`: `p_k(2) = k+1`, so
  `q_n(2) = (n+1) + delta n > 0`.
- At the endpoint `z = -2`: `p_k(-2) = (-1)^k (k+1)`, so
  `q_n(-2) = (-1)^n [(n+1) - delta n] != 0`, because `delta = 1/s < 1`
  and hence `n+1 > delta n`.

Thus all `n` roots are in `(-2,2)`, i.e. `t in (-1,1)`.

### B5. Returning to x and C

The map `x -> t = (A x - B)/2` is strictly increasing and has

```
t(0) = -B/2 = -(s + 1/s)/2 < -1,    t(1) = 1.
```

Therefore the interval `(-1,1)` is contained in `t(0,1)`. All `n` roots of
`P_n(x)` are in `(0,1)`. For each such `x`, there are exactly two numbers
`C = ± sqrt(x)` in `(-1,1)`, and `cos y = C` gives exactly one `y in (0,pi)`.
Consequently `Q_n(C)` has exactly `2n` distinct roots in `(-1,1)`, and
`F_n(y) = sin y Q_n(cos y)` has exactly `2n` distinct roots in `(0,pi)`.

To see that those roots are simple, let `x` be a root of `P_n` in `(0,1)`.
The Jacobi matrix has simple spectrum, so `P_n'(x) != 0`. For
`C = ±sqrt(x)`, since `C != 0`, the chain rule gives
`Q_n'(C) = 2C P_n'(x) != 0`. Finally, at `y = arccos(C)` in `(0,pi)`,
`sin y != 0` and
`F_n'(y) = cos y Q_n(C) - sin^2 y Q_n'(C) = -sin^2 y Q_n'(C) != 0`.
Hence every root of `F_n` in `(0,pi)` is simple.

## Remarks

- This proof also shows the roots are all simple and symmetric about
  `pi/2` (the latter is the existing reflection theorem).
- It uses only the recurrence derived from the transfer matrix and a classical
  Jacobi matrix/Chebyshev argument; no numerical evidence is used in the proof.
- This closes obligation O3 in the problem contract.
