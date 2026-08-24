# Result

Status: `RIGOROUS_PARTIAL_RESULT`

The task statement is not completely well posed because the diffusion operator
`D` is never defined. The analysis below therefore splits the problem into the
two most natural readings. Under the reading `D = Delta`, I obtain a rigorous
reduction to per-Fourier-mode statements and a complete proof for the special
case `U = 0` (and for `U` independent of `y`). The full statement under the
stated weak regularity `U in L^\infty_t L^2_y` remains open from this run.

---

## 1. The formal ambiguity: `D` is undefined

The equation in `task.md` is

    d_t rho + U(t,y) d_x rho = D rho

but no definition of `D` is provided. In the advection-diffusion literature
`D` may denote the Laplacian, a negative Laplacian times a diffusivity, or a
degenerate diffusion such as `d_y^2`. Since the conclusion and the possible
proof strategies depend on the symbol of `D`, any complete proof must first
fix `D`.

In this run the two readings analyzed are:

- Reading A: `D = Delta = d_x^2 + d_y^2`.
- Reading B: `D = d_y^2` (y-only diffusion).

The reductions below are written for Reading A; Reading B is mentioned at
the end.

---

## 2. Notation

For each `n in Z`, write

    rho_n(t,y) = (2 pi)^{-1} int_{[-pi,pi]} rho(t,x,y) e^{-i n x} dx.

Then `rho(t,x,y) = sum_{n in Z} rho_n(t,y) e^{i n x}` and the Fourier
multipliers are:

    ||rho||_{L^2}^2 = sum_n ||rho_n||_{L^2_y}^2,

    ||rho||_{dot H^{-1}}^2 = sum_{n,m} |rho_hat_{n,m}|^2 / (n^2 + m^2),

where `rho_hat_{n,m}` is the full two-dimensional Fourier coefficient.

Let `A(t) = ||rho(t)||_{dot H^{-1}}^2`, `B(t) = ||rho(t)||_{L^2}^2`, and

    R(t) = sqrt(A(t) / B(t)) = ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2}.

---

## 3. STRICT: basic structural facts under `D = Delta`

Assume `D = Delta` and `U(t,y)` is real and depends only on `y`. Taking the
Fourier transform in `x` gives, for every fixed `n in Z`,

    d_t rho_n = d_y^2 rho_n - n^2 rho_n - i n U(t,y) rho_n.    (1)

In particular, the equation for each `n` is a linear parabolic equation in
the single variable `y`, with no coupling between different `n`.

**Lemma 1 (x-mode invariance).** Under `D = Delta`, the set of `n` for which
`rho_n(0,.)` is nonzero in `L^2_y` is exactly the set of `n` for which
`rho_n(t,.)` is nonzero for every `t > 0`.

**Proof.** The equation (1) is linear and the trajectory in the `L^2_y`
Hilbert space is uniquely determined by the initial data `rho_n(0,.)`. The
spaces for different `n` are orthogonal and there is no coupling between
different `n`. Hence the support in `n` is invariant. `STRICT`.

**Lemma 2 (per-mode energy bound).** For each `n`, the solution of (1)
satisfies

    d/dt ||rho_n(t)||_{L^2_y}^2 <= -2 n^2 ||rho_n(t)||_{L^2_y}^2.

In particular, every nonzero x-mode decays at least at the rate `n^2`.

**Proof.** The advection term `- i n U rho_n` has zero real inner product
because `U` is real. The diffusion term contributes
`-2(||d_y rho_n||^2 + n^2 ||rho_n||^2)`, which is at most
`-2 n^2 ||rho_n||^2`. `STRICT`.

**Remark.** Lemma 2 gives upper bounds on survival, not a comparison between
different `n`. It is not asserted that the smallest `|n|` mode necessarily
dominates; establishing dominance would require a monotonicity or comparison
theorem for the enhanced-dissipation rates. `STRICT`.

---

## 4. STRICT: complete proof for `U = 0` (heat equation)

Assume `D = Delta` and `U = 0`. Then

    rho(t) = e^{t Delta} rho(0)

and in Fourier variables

    |rho_hat_k(t)|^2 = e^{-2 |k|^2 t} |rho_hat_k(0)|^2.

Let `S = { k in Z^2 : k != 0, rho_hat_k(0) != 0 }`. Since `rho(0,.)` is not
zero and mean-zero, `S` is nonempty. Because `|k|` takes values in a discrete
set, there exists `k_0 in S` with minimal `|k_0|`.

**Lemma 3.** Under `U = 0`, one has

    lim_{t -> infinity} A(t) / B(t) = 1 / |k_0|^2 > 0.

**Proof.** Write `S_j = { k in S : |k| = j }` with `j >= 1`. For every
`k in S_j`,

    |rho_hat_k(t)|^2 = e^{-2 j^2 t} |rho_hat_k(0)|^2.

Then

    A(t) = sum_{j >= |k_0|} e^{-2 j^2 t} j^{-2} sum_{k in S_j} |rho_hat_k(0)|^2

and

    B(t) = sum_{j >= |k_0|} e^{-2 j^2 t} sum_{k in S_j} |rho_hat_k(0)|^2.

All sums are finite or countably infinite with exponentially decaying
weights. Divide numerator and denominator by `e^{-2 |k_0|^2 t}`. Terms with
`j = |k_0|` contribute a nonzero constant, and terms with `j > |k_0|`
contribute `e^{-2(j^2 - |k_0|^2) t}` which tends to `0`. Therefore the limit
is `1 / |k_0|^2`. `STRICT`.

**Corollary 4.** Under `D = Delta` and `U = 0`, the desired conclusion holds
with `liminf = lim = 1 / |k_0|^2 > 0`. `STRICT`.

The same proof applies, with the same conclusion, when `U(t,y) = U(t)` is
independent of `y`: the advection is then a pure translation in `x`, a
unitary that commutes with `Delta` and with the `L^2` and `dot H^{-1}`
norms.

---

## 5. Reduction to per-mode y-frequency lemmas (partial)

For the general `U in L^\infty_t L^2_y`, the x-mode invariance (Lemma 1)
shows that no coupling between different `n` occurs. Therefore the whole
problem can be discussed mode by mode.

**Core Lemma (CL), per mode.** Let `n` be a fixed nonzero integer. Let
`u(t,y)` solve

    d_t u = d_y^2 u - n^2 u - i n U(t,y) u,   y in T^1,

with `U in L^\infty_t L^2_y` real, and let `u(0,.) in L^2(T^1)` be nonzero.
Then

    liminf_{t -> infinity}
      ||(n^2 - d_y^2)^{-1/2} u(t,.)||_{L^2_y}
      / ||u(t,.)||_{L^2_y} > 0.           (CL)

**What (CL) gives and what it does not.** If (CL) holds for every `n`, then
every nonzero x-mode component has a positive lower bound for its own
`dot H^{-1}/L^2` ratio in the limit. However, the total ratio `R(t)` is a
weighted average over the x-modes, and it could still go to zero if the
`L^2` mass persists only on x-modes with `|n| -> infinity` while the
corresponding (CL) constants tend to zero.

Two additional statements would be needed for a complete proof:

- (CL) with an explicit dependence on `n` that is at worst polynomial, and
- a persistence/comparison statement saying that, for the same `U`, lower
  `|n|` modes are at least as persistent as higher `|n|` modes, so the
  surviving `L^2` mass does not sit only on arbitrarily large `|n|`.

Neither of these is proved in this run. `NOT-YET-STRICT`.

**Simpler special cases already handled.** The case `U = 0` (Section 4) is
complete. The case where the initial data has finite Fourier support in both
`x` and `y` is also easy: the support is finite, the ratio at every time is
at least the inverse of the largest wavenumber in that finite support, and
the conclusion follows immediately. `STRICT`.

---

## 6. Discussion of possible routes and why they were not closed

### 6.1 Route A: Fourier localization / Batchelor scale

For a fixed `n`, split the Fourier support in `y` into low frequencies
`|m| <= K` and high frequencies `|m| > K`. The diffusion damps high modes at
rate `K^2`. The advection term moves energy across the cutoff at a rate
controlled by `n` and `||U||_{L^2_y}`. Balancing these rates gives the
classical Batchelor-scale prediction that the high-frequency fraction stays
away from `1`, hence the `dot H^{-1}`-to-`L^2` ratio stays positive.

This route is plausible and was explored with truncated Fourier simulations.
The missing part is a rigorous transfer estimate using only
`U in L^2_y`, not boundedness or derivatives of `U`. The multiplication
operator by a general `L^2_y` function is not bounded on `L^2_y`, so the
usual energy estimates do not apply directly.

### 6.2 Route B: H^{-1} energy identity

Using `D = Delta`, the weak H^{-1} energy identity is

    d/dt A(t) = -2 B(t) + 2 int_{T^2} U(t,y) rho(t) d_x ((-Delta)^{-1} rho(t)) dx dy.

The second term is a commutator term. It can be estimated in terms of
`||U||_{L^2_y}`, `||rho||_{L^2}`, and Sobolev norms of the elliptic
solution, but the resulting differential inequality was not sufficient to
force a positive lower bound for `A/B` in the general case.

### 6.3 Route C: spectral theory for time-independent shear

If `U(t,y) = U(y)` is independent of time and bounded, then for each `n`
the operator

    L_n = d_y^2 - n^2 - i n U(y)

has compact resolvent on `T^1`, its spectrum lies in the left half-plane,
and the long-time dynamics are governed by its slowest eigenmode. The ratio
`dot H^{-1}/L^2` of that eigenmode is a fixed positive number. This gives a
proof for autonomous bounded shears.

The original problem allows time-dependent `U` with only `L^2_y` in `y`;
neither the time-independence nor the boundedness assumption is stated.
Extending the spectral argument to non-autonomous, non-bounded shear is the
hard part.

### 6.4 Route D: counterexample search

No counterexample was found. Truncated spectral simulations with
`U(t,y) = a sin(y)` and with high-frequency `U(t,y) = a sin(N y)` showed the
ratio remaining positive and away from zero (see Section 7). This is only
numerical evidence, not a proof. `EVIDENCE`.

---

## 7. EVIDENCE (not a proof)

The following observations come from finite-dimensional spectral
simulations of the per-mode equation (1) with `D = Delta`, `U = sin(y)`,
and various `n`.

| n | initial y-profile | observed minimum of ratio | comment |
|---|-------------------|---------------------------|---------|
| 1 | Gaussian centered at m=0 | about 0.66 | positive |
| 2 | Gaussian centered at m=0 | about 0.40 | positive |
| 5 | Gaussian centered at m=0 | about 0.19 | positive |
| 2 | single mode m=0 | about 0.46 | positive |
| 2 | single mode m=8 | about 0.12 | positive |

These numbers use a truncated Fourier basis and exact matrix exponentials for
the finite system. They do not constitute a proof of the infinite-dimensional
statement. `EVIDENCE`.

---

## 8. Reading B: `D = d_y^2`

If `D = d_y^2`, the per-mode equation becomes

    d_t rho_n = d_y^2 rho_n - i n U(t,y) rho_n,    (2)

with no `n^2` damping. The x-mode invariance still holds, and the per-mode
lemma would be the same with `(n^2 - d_y^2)^{-1/2}` replaced by the full
`dot H^{-1}` restriction to that `n`. The same Batchelor-scale mechanism
applies but the reduction is not identical because there is no `-n^2` term.
This reading is not resolved here either. `OPEN`.

---

## 9. Summary of strictness

- `STRICT`: x-mode invariance under `D = Delta` (Lemma 1).
- `STRICT`: per-x-mode energy bound (Lemma 2).
- `STRICT`: complete proof for `D = Delta`, `U = 0` (Lemma 3 / Corollary 4).
- `STRICT`: complete proof for finite Fourier support.
- `NOT-YET-STRICT`: the reduction from the original statement to the
  per-mode Core Lemma is only partially carried out; two further statements
  are needed.
- `OPEN`: Core Lemma (CL) for general `U in L^\infty_t L^2_y`, and the
  corresponding statement for Reading B.
- `EVIDENCE`: numerical simulations; not a proof.

Therefore the original problem as stated is not solved in this run. The
strongest rigorously proved results are the `U = 0` case, the finite-support
case, and the structural reduction.
