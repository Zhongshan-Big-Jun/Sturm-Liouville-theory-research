# Result: B3 O3 root count (Danus arm)

## Main theorem

**Theorem (STRICT).** For every integer `n>=1` and every `R>1` (equivalently `s=sqrt(R)>1`), the matrix entry
`G_{n,s}(y) = (M_{n,s}(y))_{12}` has **exactly `2n` zeros in `(0,pi)`, all simple**. Endpoint zeros at `y=0` and `y=pi` (coming from the `sin y` factor) are not counted.

No unresolved obligation remains for this frozen task.

---

## Proof summary

All facts are filed under `facts/`; the identifiers `F1`-`F11` are cited below.

### Step 1: Matrix factorization

Define
```text
E(y) = [[cos y, sin y], [-sin y, cos y]],
S(y) = [[cos y, sin y/s], [-s sin y, cos y]].
```
Then `C_s(y)=S(y)E(y)` and all three matrices have determinant 1 (**F1**). Hence
```text
M_{n,s} = E C_s^n = (E S)^n E = A^n E,   A := E S.
```

### Step 2: Exact polynomial form

Put `x=cos y`, `q=sin y`, `alpha = s + 2 + s^{-1} = (s+1)^2/s > 4`, `r=s^{-1}`. Writing `P(x)=1-alpha/2 + alpha x^2/2`, one has (**F2**)

```text
tr(A) = 2P(x),   det(A)=1.
```

By Cayley-Hamilton and the Chebyshev recurrence (**F3**),

```text
A^n = U_{n-1}(P) A - U_{n-2}(P) I.
```

A direct computation (**F4**) gives

```text
(AE)_{12} = q (alpha x^2 - s),   alpha x^2 - s = 2P + r.
```

Therefore, for `x in (-1,1)`,

```text
Q_{n,s}(x) := G_{n,s}(arccos x)/sqrt(1-x^2)
 = (alpha x^2 - s) U_{n-1}(P) - U_{n-2}(P)
 = U_n(P(x)) + r U_{n-1}(P(x)).
```

This is an exact polynomial extension of the divided entry, not just a numerical identity (**F5**). Moreover:

- `Q_{n,s}` is even and has exact degree `2n` with leading coefficient `alpha^n` (**F6**).

### Step 3: Locate all roots

Let `delta = sqrt((alpha-4)/alpha)`, which lies in `(0,1)`, the unique positive point where `P=-1`.

1. **Hyperbolic region `0<|x|<delta`.** Since `P<-1`, write `P=-cosh v`, `v>0`. The standard hyperbolic Chebyshev formula gives
   ```text
   Q_n = (-1)^n/sinh v [ sinh((n+1)v) - r sinh(nv) ].
   ```
   The bracket is strictly positive because `sinh((n+1)v)>sinh(nv)>r sinh(nv)`. Hence no roots there; also `Q_n(delta) != 0` (**F7**).

2. **Elliptic region `delta<|x|<1`.** For `x in (delta,1)`, write `P=cos theta` with `theta in (0,pi)`. Then
   ```text
   Q_n = [ sin((n+1)theta) + r sin(n theta) ] / sin theta.
   ```
   Define
   ```text
   Phi(theta) = n theta + arg(e^{i theta}+r).
   ```
   Since `arg(e^{i theta}+r)` has positive derivative on `(0,pi)` and `Phi(0)=0`, `Phi(pi)=(n+1)pi`, the function `Phi` is strictly increasing from `0` to `(n+1)pi` (**F8**). Hence the equation `Phi(theta)=k pi` has exactly one solution for each `k=1,...,n`. These are precisely the zeros of `Q_n` in `(delta,1)`, all simple: the change of variable has `d theta/dx = -alpha x/sin theta != 0` there (**F9**).

3. By evenness, the same gives exactly `n` simple roots in `(-1,-delta)`. Together with degree `2n`, `Q_n` has exactly `2n` simple real roots in `(-1,1)`.

### Step 4: Transfer back to `y`

For every `y`,

```text
G_{n,s}(y) = sin y * Q_{n,s}(cos y).
```

On `(0,pi)`, `sin y>0` and `y |-> cos y` is a bijection from `(0,pi)` to `(-1,1)`. Thus the `2n` distinct simple roots of `Q_{n,s}` in `(-1,1)` correspond bijectively to `2n` distinct simple zeros of `G_{n,s}` in `(0,pi)`. At a zero `x=cos y`, `G'(y) = -sin^2 y Q'(x) != 0`, so simplicity is preserved. At `y=0,pi`, `sin y=0`, giving endpoint zeros that are excluded by the statement.

---

## Required audits

- **n=1**: `Q_1(x)=alpha x^2 - s`, roots `x = +/- s/(s+1)`, both in `(-1,1)`. Hence exactly 2 zeros in `(0,pi)`, simple.
- **y=0**: `G=0` from `sin y=0`; endpoint zero, not counted.
- **y=pi**: `G=0` from `sin y=0`; endpoint zero, not counted.
- **y=pi/2**: `x=0`, in the hyperbolic region, and `Q_n(0)!=0`; so `G != 0`.
- **R=1 (s=1)**: `alpha=4`, `P=2x^2-1`, and `Q_n(x)=U_{2n}(x)`. Consequently `G=sin((2n+1)y)`, which also has exactly `2n` simple zeros in `(0,pi)`, at `y=k pi/(2n+1)`, `k=1,...,2n`.

These checks are recorded in **F11**.

---

## External theorems used (with hypotheses)

1. **Cayley-Hamilton**: for a real `2x2` matrix with `det=1`, the identity `A^2 - tr(A) A + I=0` holds.
2. **Chebyshev U polynomial formula**: if `det A=1` and `tr A=2P`, then `A^n = U_{n-1}(P)A - U_{n-2}(P)I`; here `U_k(cos theta)=sin((k+1)theta)/sin theta` for `theta in (0,pi)`.
3. **Hyperbolic Chebyshev forms**: `U_k(-cosh v)=(-1)^k sinh((k+1)v)/sinh v` for `v>0`.
4. **IVT + strict monotonicity**: a continuous strictly increasing function crossing each integer multiple of `pi` exactly once.

---

## Status

**RIGOROUS_PARTIAL_RESULT?** No — this is a **complete STRICT proof** of the frozen theorem.

`result.md` path: `F:\LaTeX\BVE research\runs\plugin-benchmark-20260824-calibration\arms\danus\result.md`
