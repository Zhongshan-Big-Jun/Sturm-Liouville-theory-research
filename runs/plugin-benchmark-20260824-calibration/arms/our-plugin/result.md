CANDIDATE_COMPLETE_PROOF

(Proof label. The proof is self-contained and self-audited; it was not independently audited by a fresh subagent because the benchmark explicitly forbids spawning nested subagents.)

## Exact theorem proved (STRICT / 严格证明)

**Theorem.** For every integer `n >= 1` and every real `R > 1`, the function
`G_{n,s}(y)` has exactly `2n` zeros in the open interval `(0, pi)`, and every
such zero is simple.

This is the affirmative resolution of the frozen task.

## Proof

### 1. Matrix notation and a useful conjugation

Let

```text
B_1(y) = [[c, q], [-q, c]],
B_R(y) = [[c, q/s], [-s q, c]],
D = [[1, 0], [0, s]].
```

Then `B_R = D B_1 D^{-1}`. Both `B_1` and `B_R` have determinant `1` (the
latter is a diagonal conjugation of the former), so `det C_s = det(B_R B_1) = 1`.
The given matrix is

```text
C_s(y) = B_R(y) B_1(y),
M_{n,s}(y) = E(y) C_s(y)^n = B_1(y) (B_R(y) B_1(y))^n,
G_{n,s}(y) = (M_{n,s}(y))_{12}.
```

We will not use the physical Sturm–Liouville interpretation after this point; the
calculation below is purely algebraic and exact.

### 2. Cayley–Hamilton expansion

Write `a = s + 1/s` and

```text
tau = tr C_s = C_11 + C_22 = 2c^2 - a q^2,
z = tau/2 = ((a+2)c^2 - a)/2.
```

Since `det C_s = 1`, the Cayley–Hamilton theorem gives the standard Chebyshev
expansion for powers of a unimodular 2x2 matrix:

```text
C_s^k = U_{k-1}(z) C_s - U_{k-2}(z) I,
```

where `U_{-1}=0`, `U_0=1`, and `U_k` are the Chebyshev polynomials of the second
kind. Therefore

```text
G_{n,s} = U_{n-1}(z) (E C_s)_{12} - U_{n-2}(z) q.
```

A direct calculation gives

```text
(E C_s)_{12}
= c C_12 + q C_22
= q [ ((s+1)^2/s) c^2 - s ].
```

Since `((s+1)^2/s = a+2`, the bracket equals

```text
(a+2)c^2 - s = 2z + (a-s) = 2z + 1/s.
```

Hence

```text
G_{n,s}(y)
= sin(y) [ U_{n-1}(z)(2z+1/s) - U_{n-2}(z) ].
```

Using the Chebyshev recurrence `U_n(z) = 2z U_{n-1}(z) - U_{n-2}(z)`, we obtain the
key exact identity:

```text
G_{n,s}(y) = sin(y) P_n(z),   P_n(z) = U_n(z) + alpha U_{n-1}(z),
```

with

```text
alpha = 1/s in (0,1),
z = z(y) = ((a+2) cos^2(y) - a)/2,   a = s + 1/s.
```

### 3. Justified polynomial formulation

For `y in (0,pi)`, put `x = cos(y)`; then `sin(y) = sqrt(1-x^2)`. The identity above gives

```text
Q_{n,s}(x) = G_{n,s}(arccos(x))/sqrt(1-x^2) = P_n(z(x)),
z(x) = ((a+2)x^2 - a)/2.
```

Because `P_n` is a degree-`n` polynomial and `z(x)` is quadratic in `x`, `Q_{n,s}`
is an even polynomial in `x` of degree exactly `2n`. A zero `y in (0,pi)` of
`G_{n,s}` corresponds exactly to a zero `x = cos(y) in (-1,1)` of `Q_{n,s}`, and
hence equivalently to a zero `z(x)` of `P_n` in the interval `(-a/2,1)`. This is
the polynomial formulation used below.

### 4. Polynomial lemma (STRICT)


**Lemma.** For every `n >= 1` and every `alpha in (0,1)`, the polynomial
`P_n(z) = U_n(z) + alpha U_{n-1}(z)` has exactly `n` distinct real roots, all
lying in the open interval `(-1,1)`, and all are simple.

**Proof.** The leading coefficient of `U_n` is `2^n`, so `P_n` has degree exactly
`n`; hence it has at most `n` real roots.

Let `z = cos(theta)` with `theta in (0,pi)`. Then

```text
P_n(cos(theta)) = [ sin((n+1)theta) + alpha sin(n theta) ] / sin(theta).
```

Define

```text
F(theta) = sin((n+1)theta) + alpha sin(n theta),
theta_k = k pi/(n+1),   k = 0,1,...,n+1.
```

For `k = 1,...,n`, since `(n+1)theta_k = k pi`,

```text
sin(n theta_k) = sin(k pi - theta_k) = (-1)^{k+1} sin(theta_k) != 0.
```

Therefore, for `k = 1,...,n-1`, the signs of

```text
F(theta_k) = alpha (-1)^{k+1} sin(theta_k),
F(theta_{k+1}) = alpha (-1)^{k+2} sin(theta_{k+1})
```

are opposite. By the intermediate value theorem, `F` has at least one zero in
each open interval `(theta_k, theta_{k+1})`, `k = 1,...,n-1`.

For the last interval `(theta_n, pi)`, let `epsilon > 0` be small. Then

```text
F(pi-epsilon)
= (-1)^n [ sin((n+1)epsilon) - alpha sin(n epsilon) ].
```

The bracket has derivative `(n+1) - alpha n > 0` at `epsilon = 0`, so it is
positive for all sufficiently small `epsilon > 0`. Thus the sign of `F(pi-epsilon)`
is `(-1)^n`, opposite to

```text
F(theta_n) = alpha (-1)^{n+1} sin(theta_n).
```

Again by the intermediate value theorem, `F` has a zero in `(theta_n, pi)`.

So `F` has at least one zero in each of the `n` disjoint intervals
`(theta_k, theta_{k+1})`, `k = 1,...,n`. Hence `P_n` has at least `n` distinct
zeros in `(-1,1)`. Since the degree is exactly `n`, these are all the zeros, they
are distinct, and therefore they are simple. ∎

### 5. Counting and simplicity in `y`

From `z(y) = ((a+2)cos^2(y) - a)/2`, the map `y -> z(y)` is even about
`y = pi/2`, strictly decreasing on `(0,pi/2)`, strictly increasing on
`(pi/2,pi)`, and its range is the interval `[-a/2, 1]`. Since `alpha = 1/s in (0,1)`,
we have `a/2 = (alpha + 1/alpha)/2 > 1`. The `n` roots `z_1,...,z_n` of `P_n`
lie in `(-1,1) subset (-a/2,1)`. For each such `z_j`, the equation `z(y)=z_j`
has exactly two solutions `y` in `(0,pi)`, one in `(0,pi/2)` and one in
`(pi/2,pi)`. The endpoints `y=0,pi` are not counted.

Thus `G_{n,s}` has exactly `2n` zeros in `(0,pi)`.

For simplicity, let `y_0` be one of these zeros and `z_0 = z(y_0)`. Then
`z_0 in (-1,1)`, so `y_0 != pi/2` and `z'(y_0) != 0`. The lemma gives
`P_n'(z_0) != 0`, and `sin(y_0) > 0`. Differentiating

```text
G(y) = sin(y) P_n(z(y))
```

at `y_0` gives

```text
G'(y_0) = sin(y_0) P_n'(z_0) z'(y_0) != 0.
```

Hence every zero of `G_{n,s}` in `(0,pi)` is simple. ∎

## Verification performed

- Exact symbolic identity `G_{n,s}(y) = sin(y) P_n(z(y))` was checked with SymPy for
  `n = 1,...,6` (scratch file `scratch_verify.py`). This is auxiliary evidence, not
  part of the proof.
- The polynomial root pattern was checked numerically for `n = 1,...,4` and
  `s = 2,5`; all `n` roots were real, simple, and in `(-1,1)`. Again this is
  `EVIDENCE`, not proof.
- Edge cases audited: `n=1`, `y=0`, `y=pi`, `y=pi/2`, and the boundary `R=1`.
  See below.

## Edge-case audit (STRICT)

- `n=1`: the proof applies; `P_1(z)=2z+alpha` has one root in `(-1,1)`, and
  `G` has two zeros in `(0,pi)`.

- `y=0`: `c=1,q=0`, so `C_s(0)=I`, `E(0)=I`, `M_{n,s}(0)=I`, and `G=0`.
  Endpoint, not counted.

- `y=pi`: `c=-1,q=0`, so `C_s(pi)=I`, `E(pi)=-I`, `M_{n,s}(pi)=-I`, and `G=0`.
  Endpoint, not counted.

- `y=pi/2`: here `c=0,q=1`, so `z=-a/2<-1`. Since all roots of `P_n` lie in
  `(-1,1)`, `P_n(z) != 0`. Hence `G != 0`; no zero at the midpoint.

- `R=1` boundary (outside the stated hypothesis): `s=1`, `alpha=1`, and the same
  formula gives `C_s=E^2`, `M_{n,1}=E^{2n+1}`, so
  `G_{n,1}(y)=sin((2n+1)y)`. This has exactly `2n` simple zeros in `(0,pi)`, so
  the conclusion also holds on the boundary. The proof of the polynomial lemma
  works verbatim for `alpha=1` as well (the small-`epsilon` bracket has derivative
  `(n+1)-n=1>0`), although the statement only requires `R>1`.

## Remaining gaps

For the stated theorem, there are no unresolved proof obligations.

## Failed and blocked routes

- The route of trying to derive an explicit closed form for the roots was not
  needed and is not pursued in the final proof.
- Direct numerical root-counting was used only as a consistency check and is not
  part of the completed proof.

## Novelty status

- Literature/novelty audit could not be performed because the benchmark forbids
  internet and repository inspection. No novelty claim is made beyond the exact
  proof above.

## Human/model/tool contributions

- The proof was produced in this isolated benchmark arm.
- No nested subagents were spawned; no prior solution, git history, internet, or
  external memory was inspected.
- Scratch files: `problem_contract.md`, `scratch_verify.py`.

## Reproducibility manifest

- Arm root: `F:\LaTeX\BVE research\runs\plugin-benchmark-20260824-calibration\arms\our-plugin`
- Environment: WSL Python 3.14.4, SymPy 1.14.0.
- Commands: `python3 scratch_verify.py`.
- The proof itself is independent of the computational check.

## Confidence by axis

- Semantic fidelity: high; all definitions and quantifiers match the frozen task.
- Mathematical correctness: high; the only external theorem used is the standard
  Cayley–Hamilton/Chebyshev expansion for 2x2 unimodular matrices, stated with
  hypotheses.
- Completeness: complete for the stated `R>1` theorem; boundary `R=1` audited
  although outside the hypothesis.
- Novelty: not assessed (benchmark isolation).
- Reproducibility: high; the proof is self-contained and the scratch verification
  command is recorded.
