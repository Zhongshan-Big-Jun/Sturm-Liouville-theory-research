# Independent adversarial audit report

Run: R-20260822T230000Z-b3-audit
Status label: `RIGOROUS_PARTIAL_RESULT` (audit)
Verdict: **REPAIRABLE_GAP** — 0 FATAL_GAP, 3 REPAIRABLE_GAP.

Scope: independent re-derivation of the two claimed STRICT results in
`R-20260822T220000Z-b3-baseline/candidate_proof.md`, cross-check against
`R-20260822T220000Z-b3-reuse/candidate_proof.md`, plus the project source
documents and the two new tool notes. No subagents were spawned.

---

## 1. Statement fidelity

The claims are faithful to the project's B3 contract:

- The box is `1 <= rho <= R` a.e. with `rho in L^infty(0,1)`, Dirichlet
  `-y'' = lambda rho y`, `y(0)=y(1)=0`. Both runroots use exactly this box.
- `Lambda_n(rho) = lambda_{n+1}(rho)/lambda_n(rho)` is the fixed-n adjacent
  ratio; `n >= 1`, `R > 1` fixed. The structure theorem is stated for every
  global maximizer, not merely for a subclass.
- The `[1,R,1,...,1]` balanced alternating family is defined with
  `w_1/w_2 = sqrt(R)`, `t = 1/((n+1)sqrt(R)+n)`, matching
  `docs/SL_fixed_n_supremum.tex` equation (eq:alt).
- The 2n-root-count statement concerns `F_n(y)` in `(0,pi)`; the baseline
  proof works with the scaled secular function `G_n = omega F_n`, whose zeros
  coincide with those of `F_n` for `omega > 0`. This is a legitimate
  normalization, but it should be made explicit (currently `w` in B1 is not
  defined in the Markdown; it is evidently `omega`).

No silent change of `n`, `R`, boundary conditions, or density regularity was
found.

---

## 2. Part A: ratio extremizer structure theorem

Re-derived from scratch.

### 2.1 Feynman-Hellmann derivative and saturation

For `h in L^infty`, with normalization `int rho u_k^2 = 1`,

```
lambda_k'[h] = -lambda_k int h u_k^2,
```

hence

```
Lambda_n'[h] = Lambda_n int h (u_n^2 - u_{n+1}^2) = Lambda_n int h H.
```

Because `Lambda_n > 0`, the one-sided box variations are exactly as written:
for admissibly raising `rho` on `{rho < R}` the derivative is `<= 0`, giving
`H <= 0` a.e. there; for admissibly lowering `rho` on `{rho > 1}` the
derivative is `<= 0`, giving `H >= 0` a.e. there. Therefore

```
rho = R a.e. on {H > 0},   rho = 1 a.e. on {H < 0}.
```

This is correct and uses only the weak-* continuity facts already proved in
`docs/SL_gap_nge2_finite_reduction_proof.tex`.

### 2.2 Zero structure of H

With `W = u_{n+1}' u_n - u_{n+1} u_n'`, the project's Wronskian lemma gives
`W < 0` on `(0,1)`. Thus `Q = u_{n+1}/u_n` is strictly decreasing on each
nodal interval of `u_n`, and `H = u_n^2(1 - Q^2)`. The exact zero count

```
#Z(H;(0,1)) = 2n - 2 + 1_{q0 > 1} + 1_{q1 < -1}
```

is correct; the `n=1` case (no middle nodal interval) is also correctly
represented by giving the two endpoint indicators only. All interior zeros
are simple because `H' = -2 u_n^2 Q Q'` is nonzero at a zero.

### 2.3 Zero-switch identification

The proof that the zero set of `H` equals the effective switch set is valid:
since the zeros are finite and simple, `H` has constant sign on each component;
the saturation law then fixes `rho` to a single endpoint on each component;
a simple zero forces a sign change, hence a material change; conversely an
actual switch must occur at a sign change, hence at a zero. This is exactly the
gap-case argument, and it does not use any hidden continuity/monotonicity of
`rho`.

### 2.4 Ratio energy invariant

Define `a = lambda_n`, `b = lambda_{n+1}`,

```
E_n   = u_n'^2 + a r u_n^2,
E_{n+1} = u_{n+1}'^2 + b r u_{n+1}^2,
E    = b E_n - a E_{n+1}.
```

On a constant block both `E_n` and `E_{n+1}` are constant. At a switch `s`,

```
E(s_+) - E(s_-) = ab (r_+ - r_-) H(s),
```

which vanishes because every switch is a zero of `H`. Hence `E` is globally
constant. Integration with `int rho u_k^2 = 1` and
`int u_k'^2 = lambda_k` gives

```
int_0^1 E dx = b(a + a) - a(b + b) = 2ab - 2ab = 0.
```

So `E = 0` everywhere. At the endpoints, since `u_k(0)=u_k(1)=0`,

```
b u_n'(0)^2 = a u_{n+1}'(0)^2,
b u_n'(1)^2 = a u_{n+1}'(1)^2.
```

With `u_k'(0)>0` and the parity of the right-end derivative, this gives
`q0 = 1/c > 1`, `q1 = -1/c < -1`, where `c = sqrt(a/b) in (0,1)`. Inserting
these strict indicators into the zero-count formula gives exactly `2n`
interior zeros, hence exactly `2n` switches and the alternating order
`[1,R,1,...,1]`.

**No fatal gap in Part A.** The argument is self-contained modulo the cited
project spectral facts (weak-* compactness/continuity, regularity, nodal and
interlacing theory, Wronskian strict sign). It also works for both even and odd
`n` and does not assume continuity, symmetry, or monotonicity of `rho`.

---

## 3. Part B baseline: 2n-root-count theorem

Re-derived and symbolically/numerically checked.

### 3.1 Transfer-matrix recurrence

The cell computation

```
T_cell = [[cos^2 y - s^{-1} sin^2 y,  (1+s) sin y cos y / (omega s)],
          [-omega (1+s) sin y cos y,  cos^2 y - s sin^2 y]],
det T_cell = 1,
tau(y) = 2 cos^2 y - (s + 1/s) sin^2 y
```

is correct. With `G_n = omega (T_end T_cell^n)_{01}`, Cayley-Hamilton gives

```
G_n = tau G_{n-1} - G_{n-2}.
```

Using `G_0 = sin y` and the direct computation

```
G_1 = sin y ( ((s+1)^2/s) C^2 - s ),
```

the recurrence indeed yields `G_n = sin y Q_n(C)` with
`Q_0=1`, `Q_1 = A C^2 - s`, `Q_n = tau Q_{n-1} - Q_{n-2}`, `A=(s+1)^2/s`,
`B=(s^2+1)/s`. I verified this numerically for `n=1..7`, `s=2,5`, and the
factor is exactly `1` for every sample. The earlier `docs/SL_fixed_n_supremum.tex`
closed-form for `n=1` differs by a nonzero scalar (`s`), but the roots are the
same; this scaling is harmless for root counting.

### 3.2 Square-variable and Chebyshev/Jacobi identification

With `x=C^2`, `P_n(x)=Q_n(sqrt(x))` satisfies
`P_0=1`, `P_1=A x - s`, `P_n=(A x - B)P_{n-1}-P_{n-2}`. For
`t=(A x - B)/2`, `delta=1/s`, `z=2t`,

```
P_n(x) = U_n(t) + delta U_{n-1}(t)
       = p_n(z) + delta p_{n-1}(z).
```

The RHS is exactly `det(z I - J_n(delta))` for the unreduced symmetric
tridiagonal Jacobi matrix `J_n(delta)` with diagonal `(0,...,0,-delta)` and
off-diagonals `1`. Hence `p_n+delta p_{n-1}` has `n` distinct real roots. This
part is correct.

### 3.3 REPAIRABLE_GAP B4: exclusion of `z = ±2` is missing

Lines ~350-365 of the baseline candidate show only

- `z > 2` gives `q_n(z) > 0`;
- `z < -2` gives `q_n(z) != 0`.

The conclusion "all roots lie in `(-2,2)`" also requires excluding the
endpoints `z = ±2`. They are easy to add:

```
p_k(2) = k+1,   q_n(2) = (n+1) + delta n > 0.
p_k(-2) = (-1)^k (k+1),
q_n(-2) = (-1)^n [ (n+1) - delta n ] != 0   (because n+1 > delta n).
```

With this one-line repair, the location claim is complete.

### 3.4 REPAIRABLE_GAP B5: simplicity of `F_n` roots is asserted but not proved

The theorem states the roots are simple. The proof establishes:

- `P_n` has `n` distinct real roots in `(0,1)`;
- each such `x` gives two distinct `C = ±sqrt(x)` in `(-1,1)`;
- hence `Q_n` has `2n` distinct roots in `(-1,1)`.

It does not explicitly show `Q_n'(C) != 0` or `F_n'(y) != 0`. This is
repairable in two lines:

```
For a root x of P_n, P_n'(x) != 0 (simple spectrum of J_n).
For C = ±sqrt(x) with x in (0,1), C != 0, so
Q_n'(C) = 2C P_n'(x) != 0.
At y = arccos C in (0,pi), sin y != 0 and
F_n'(y) = cos y Q_n(C) - sin^2 y Q_n'(C) = -sin^2 y Q_n'(C) != 0.
```

Hence every root of `F_n` in `(0,pi)` is simple.

### 3.5 Conclusion for Part B baseline

The mathematical content is correct; the two omissions above are repairable
and do not invalidate the result. After repair, the 2n-root-count theorem is
STRICT.

---

## 4. Reuse-gate cross-check

The reuse-gate candidate gives an alternative elliptic/hyperbolic phase proof
of the same 2n-root-count theorem. I checked the main computations:

### 4.1 Elliptic-zone phase lemma

For `E_n(phi) = sin((n+1)phi) + (1/s) sin(n phi)`, the argument
`e^{i phi} + a = r e^{i theta}` with `a=1/s in (0,1)` gives
`E_n = r sin(n phi + theta)` and `theta' > 0`; hence `psi = n phi + theta`
is strictly increasing from `0` to `(n+1)pi`, so `E_n` has exactly `n` simple
zeros in `(0,pi)`. This is correct.

### 4.2 Hyperbolic-zone no-root argument

For `|C| < c0`, substitution `p = -cosh mu` leads to the impossible equation
`sinh((n+1)mu) = (1/s) sinh(n mu)`, so no zeros occur in the open hyperbolic
zone. This is correct.

### 4.3 REPAIRABLE_GAP R1: boundary `|C| = c0` / `phi = 0,pi` not checked

The reuse proof counts roots from `phi in (0,pi)` and excludes the open
hyperbolic zone. The boundary `|C| = c0` (equivalently `phi = pi`) is not
covered; similarly `|C| = 1` (`phi = 0`) corresponds to `y=0,pi`, outside the
open interval. A one-line check shows no root at `phi = pi`:

```
At phi = pi, the bracket tends to
lim_{phi->pi} [ sin((n+1)phi) + (1/s) sin(n phi) ] / sin phi
= (-1)^{n+1}[(n+1) - n/s] != 0.
```

Thus the boundary is harmless, but the proof as written has a small gap.

### 4.4 Reuse-gate R2 ratio invariant

The reuse `K_ratio = (u_n'^2/lambda_n + rho u_n^2)
- (u_{n+1}'^2/lambda_{n+1} + rho u_{n+1}^2)` is a scaled version of the
baseline `E`; it is also constant on blocks, has zero jump at switches, and
integrates to `0`. Its endpoint consequences `q0 = sqrt(lambda_{n+1}/lambda_n)`,
`q1 = -sqrt(...)` agree with the baseline. This cross-check passes.

---

## 5. Boundary cases, parity, and hidden assumptions

- `R > 1`: used consistently. The degenerate case `R=1` is outside the
  contract and is not needed.
- `n >= 1`: both proofs work for `n=1`. The baseline zero-count formula
  handles `n=1`; the reuse phase lemma handles `n>=1`.
- Even/odd `n`: no parity-specific obstruction. The parity of `u_k'(1)` is
  used only to fix the sign of `q1`; it holds for every `n`.
- Hidden assumptions: no continuity, symmetry, monotonicity, or finite-jump
  assumption on `rho` is used in Part A. The eigenfunctions are used as
  `W^{2,infty} cap C^1`, which is standard for `L^infty` weights and is
  proved in the finite-reduction document. Part B is purely algebraic and
  needs only `R>1`.
- The baseline's B1 uses an unnamed `w`; it should read `omega` and should
  explicitly state that `G_n = omega F_n` has the same zeros as `F_n`. This
  is a presentation/repair item, not a mathematical flaw.

---

## 6. Error/gap summary

| # | Location | Severity | Description | Suggested repair |
|---|---|---|---|---|
| G1 | baseline `candidate_proof.md` B4 (~lines 350–365) | REPAIRABLE | Excludes `z>2` and `z<-2` but not `z=±2` before claiming `(-2,2)` | Add the two endpoint evaluations: `q_n(2)>0`, `q_n(-2)!=0`. |
| G2 | baseline `candidate_proof.md` B5 (~lines 367–380) | REPAIRABLE | "All simple" asserted but not proved; proof only gives distinct roots | Add `Q_n'(C)=2C P_n'(x)!=0` and `F_n'=-sin^2 y Q_n'(C)!=0`. |
| G3 | reuse `candidate_proof.md` R1 (~lines 63–151) | REPAIRABLE | Elliptic-zone count and hyperbolic no-root proof do not cover the boundary `|C|=c0` / `phi=pi` | Add boundary check showing the limit at `phi=pi` is nonzero. |
| — | baseline `candidate_proof.md` B1 (~line 258) | Presentation | Symbol `w` not defined; should be `omega` and note root-equivalence | Rename to `omega` and add one sentence `G_n = omega F_n`, `omega>0`. |

FATAL_GAP count: **0**.
REPAIRABLE_GAP count: **3** (plus one presentation note).

---

## 7. Registration decision

The two claims are mathematically sound as partial theorems. However, as
written in the baseline candidate, they are not quite fully self-contained
strict proofs because of G1 and G2 (and the reuse cross-check has G3). They
can be registered as STRICT partial results **after the above repairs** are
applied to the documents/tool notes.

- Part A (ratio extremizer structure): no repair needed; it is already strict.
- Part B (2n-root count): needs G1 and G2 to be inserted before it is
  registered as STRICT; after those repairs it is strict.
- The reuse-gate alternative proof needs G3 before it can serve as a strict
  cross-check; after repair it is also acceptable.
