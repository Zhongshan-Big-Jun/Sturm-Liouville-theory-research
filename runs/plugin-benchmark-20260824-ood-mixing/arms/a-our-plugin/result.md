# Result: Exponential mixing by a bounded time-dependent shear is impossible

**Status: CANDIDATE_COMPLETE_PROOF** (negative answer: **No**)

This document gives a complete rigorous argument that for every nonzero
smooth mean-zero `theta_0` on `T^2` and every admissible time-dependent shear
`u`, the solution cannot have exponential decay in `H^{-1}`. No numerical
evidence is used.

---

## 0. Statement of the theorem

**STRICT / 严格证明.** The following theorem is proved from first principles
(standard integration by parts, Fubini, Fourier representation); no numerical
evidence is used.

**Theorem (Negative answer).**
Let `T = R/(2pi Z)`. Let `theta_0 in C^infty(T^2)` be nonzero and satisfy

    int_{T^2} theta_0(x,y) dx dy = 0.

Let `u in L_t^infty(W_y^{1,1}(T))` satisfy, for a.e. `t`,

    int_T |partial_y u(y,t)| dy <= C < infinity.

Let `theta` be the solution of

    theta_t + u(y,t) partial_x theta = 0,
    theta(x,y,0) = theta_0(x,y),

in the distributional/characteristic sense. Then there is a constant
`c = c(theta_0, C) > 0` such that for all `t >= 0`,

    ||theta(t)||_{dot H^{-1}_{x,y}} >= c / (1 + t^2).

Consequently there do NOT exist constants `C_1, C_2 > 0` with

    ||theta(t)||_{dot H^{-1}_{x,y}} <= C_1 e^{-C_2 t}   for all t >= 0.

Thus the answer to the frozen problem is **No**.

---

## 1. Fourier conventions

For `h in L^1(T^2)` write

    hat h(n) = (1/(2pi)^2) int_{T^2} h(x,y) e^{-i(n_1 x + n_2 y)} dx dy,
    n = (n_1,n_2) in Z^2.

For a function `a in L^1(T)` write

    hat a(l) = (1/(2pi)) int_T a(y) e^{-ily} dy.

Thus for a function `g(y) = sum_l hat g(l) e^{ily}`, Parseval gives
`int_T |g|^2 dy = 2pi sum_l |hat g(l)|^2`. The decay/nondegeneracy
question is invariant under harmless scaling of the Fourier normalization;
our normalization is the one used in the statement, up to constants.

---

## 2. Explicit solution of the transport equation

Define

    U(y,t) = int_0^t u(y,s) ds.

Because `u(.,s) in W^{1,1}(T)` for a.e. `s`, for each `t` the function
`U(.,t)` is absolutely continuous on `T` and

    partial_y U(y,t) = int_0^t partial_y u(y,s) ds,

so, using Fubini and the hypothesis,

    ||partial_y U(.,t)||_{L^1(T)} <= int_0^t ||partial_y u(.,s)||_{L^1} ds
                                   <= C t.                                  (2.1)

For smooth data the characteristic equations are

    dot y = 0,          dot x = u(y,t),

so `y(t) = y_0` and `x(t) = x_0 + U(y_0,t)`. Hence the solution is

    theta(x,y,t) = theta_0(x - U(y,t), y).                                  (2.2)

This formula also gives the unique distributional solution under our
hypotheses: `U(.,t)` is continuous, the transport map is measure-preserving,
and for smooth `theta_0` the mode-wise ODE below is valid in the sense of
absolutely continuous functions of `t`.

For each `k in Z` let

    F_k(y) = (1/(2pi)) int_T theta_0(x,y) e^{-ikx} dx,

the `k`-th partial Fourier coefficient of `theta_0` in `x`. Taking the
`k`-th Fourier mode in `x` of (2.2) gives

    theta^k(y,t) = e^{-ik U(y,t)} F_k(y).                                    (2.3)

Indeed, this is the unique solution of the parameterized ODE

    d/dt theta^k + i k u(y,t) theta^k = 0.

For later use define

    g_{k,t}(y) = e^{-ik U(y,t)} F_k(y).                                      (2.4)

Then by (2.3) and the y-direction Fourier formula,

    hat theta(k,l,t) = (1/(2pi)) int_T e^{-ily} g_{k,t}(y) dy
                     = hat g_{k,t}(l).                                       (2.5)

---

## 3. Two easy cases: the `k=0` mode is frozen

The `k=0` partial mode `F_0(y)` is the x-average of `theta_0` and is
invariant under the flow (2.2). Its contribution to the `H^{-1}` norm is

    sum_{l != 0} |hat F_0(l)|^2 / l^2,

which is independent of `t`. Since `int_{T^2} theta_0 = 0`, we have
`hat F_0(0) = 0`. If `F_0` is not identically zero, some `l != 0` has
`hat F_0(l) != 0`, so this contribution is a fixed positive number. Then
`||theta(t)||_{dot H^{-1}}` cannot tend to `0`, let alone decay exponentially.

Therefore, from now on we may assume `F_0(y) = 0` for all `y`. Since
`theta_0 != 0`, there is some `k != 0` with `F_k` not identically zero.
Fix one such `k != 0`.

---

## 4. A quantitative lower bound for phase-modulated `W^{1,1}` profiles

This section proves the only analytic ingredient.

**Lemma 1 (low-frequency projection of a `W^{1,1}` function).**
Let `g in W^{1,1}(T)`. Put

    V = ||g'||_{L^1(T)},        L^2 = sum_{l in Z} |hat g(l)|^2.

Then there is an absolute constant `C_1 > 0` (for instance any number
`>= 1/(2 pi^2)`) such that for every `N >= 1`,

    sum_{|l| <= N} |hat g(l)|^2 >= L^2 - C_1 V^2 / N.                        (4.1)

**Proof.** For `l != 0`, integration by parts on the circle gives

    hat g'(l) = i l hat g(l).

Since `|hat g'(l)| = |(1/(2pi)) int_T g'(y) e^{-ily} dy| <= V/(2pi)`, we get

    |hat g(l)| <= V/(2 pi |l|)   for all l != 0.                              (4.2)

Using (4.2),

    sum_{|l| > N} |hat g(l)|^2 <= (V^2/(4 pi^2)) sum_{|l| > N} 1/l^2
                                <= (V^2/(4 pi^2)) * (2/N)
                                <= V^2/(2 pi^2 N).

Taking `C_1 = 1/(2 pi^2)` proves (4.1). QED.

Now choose

    N = max(1, ceil(4 C_1 V^2 / L^2))

whenever `L > 0`. Then `C_1 V^2/N <= L^2/4` (this is immediate from the
ceiling; if `V=0` the bound is trivial). Hence

    sum_{|l| <= N} |hat g(l)|^2 >= 3L^2/4.                                   (4.3)

(Using `L^2/2` instead of `3L^2/4` would also suffice.)

Therefore

    sum_{l in Z} |hat g(l)|^2 / (1 + l^2)
        >= (1/(1+N^2)) sum_{|l| <= N} |hat g(l)|^2
        >= (3L^2)/(4(1+N^2)).                                               (4.4)

Since `N <= 1 + 4 C_1 V^2/L^2`, we have `1+N^2 <= (2+4C_1 V^2/L^2)^2`
(for `V>=0`), and hence

    sum_{l} |hat g(l)|^2/(1+l^2)
        >= (3 L^2)/(4(2+4 C_1 V^2/L^2)^2)
        = (3 L^6)/(16 (L^2 + 2 C_1 V^2)^2).                                 (4.5)

Taking square roots gives the clean form

    (sum_l |hat g(l)|^2/(1+l^2))^{1/2}
        >= (sqrt(3) L^3)/(4 (L^2 + 2 C_1 V^2)).                             (4.6)

In particular, for fixed `L>0`, the right-hand side is bounded below by
`c(L)/(1+V^2)` with `c(L)>0` depending only on `L` (and `C_1`).

---

## 5. The polynomial lower bound for the fixed nonzero mode `k`

Apply Lemma 1 to `g = g_{k,t}` from (2.4). Let

    L_k^2 = sum_l |hat F_k(l)|^2  (= (1/(2pi)) ||F_k||_{L^2}^2) > 0,
    M_k   = ||F_k||_{L^infty}  < infinity,
    W_k   = ||F_k'||_{L^1}     < infinity.

Since `F_k in C^infty(T)` and `theta_0 in C^infty(T^2)`, these are finite;
`L_k > 0` by choice of `k`.

For `g_{k,t}` we have

    g'_{k,t}(y) = e^{-ik U(y,t)} ( -ik partial_y U(y,t) F_k(y) + F_k'(y) ).

Hence

    ||g'_{k,t}||_{L^1}
        <= |k| ||partial_y U(.,t)||_{L^1} ||F_k||_{L^infty} + ||F_k'||_{L^1}
        <= |k| M_k C t + W_k.                                                (5.1)

Call this quantity `V_k(t)`. Note `V_k(t) <= |k| M_k C t + W_k`.

The contribution of this fixed mode `k` to the full `H^{-1}` norm is

    S_k(t) = sum_{l in Z} |hat theta(k,l,t)|^2 / (k^2 + l^2)
           = sum_{l in Z} |hat g_{k,t}(l)|^2 / (k^2 + l^2).                 (5.2)

Since `|k| >= 1`, for every `l`,

    k^2 + l^2 <= k^2 (1 + l^2),

so

    S_k(t) >= (1/k^2) sum_l |hat g_{k,t}(l)|^2 / (1 + l^2).                  (5.3)

By (4.6) applied to `g_{k,t}`, there is a constant `c_k > 0`, depending on
`k`, `F_k`, `C`, and the universal constant `C_1`, such that

    S_k(t)^{1/2} >= c_k / (1 + V_k(t)^2).                                    (5.4)

Using (5.1), `V_k(t)^2 <= (|k| M_k C t + W_k)^2 <= C_k (1 + t^2)` for some
`C_k > 0`. Therefore

    S_k(t)^{1/2} >= c_k' / (1 + t^2)                                        (5.5)

for some `c_k' > 0` and all `t >= 0`.

Finally, since the full norm contains the nonnegative summand `S_k(t)`,

    ||theta(t)||_{dot H^{-1}_{x,y}}^2 >= S_k(t),

so

    ||theta(t)||_{dot H^{-1}_{x,y}} >= c_k' / (1 + t^2).                     (5.6)

This is the claimed polynomial lower bound.

---

## 6. Exponential decay is impossible

Suppose there were constants `C_1,C_2 > 0` with

    ||theta(t)||_{dot H^{-1}_{x,y}} <= C_1 e^{-C_2 t}    for all t >= 0.

Then for every `t >= 0`,

    c_k' / (1 + t^2) <= C_1 e^{-C_2 t}.

Multiplying by `e^{C_2 t}` gives

    (c_k' e^{C_2 t}) / (1 + t^2) <= C_1.

But `e^{C_2 t}/(1+t^2) -> infinity` as `t -> infinity`, so the left-hand
side becomes arbitrarily large. This contradicts the fixed constant `C_1`
for all sufficiently large `t`. Hence exponential decay is impossible.

Hence no such `u, theta_0` exists.

---

## 7. External facts used, with hypotheses

1. **Periodic integration by parts.** If `g in W^{1,1}(T)`, then
   `hat g'(l) = i l hat g(l)` and `|hat g(l)| <= ||g'||_{L^1}/(2pi |l|)`.
   This is standard; it uses the periodicity of `g` and the absolute
   continuity of `W^{1,1}` functions on the circle.

2. **Fubini and the fundamental theorem of absolutely continuous functions.**
   They give (2.1) and the mode formula (2.3). The hypotheses are the stated
   `u in L_t^infty(W_y^{1,1})` with derivative `L^1` bound.

3. **Fourier representation of `H^{-1}`.** The given definition is a
   weighted `l^2` sum over Fourier coefficients; all inequalities are applied
   to that exact sum.

No unverified literature results are used.

---

## 8. Rigour notes

- The lower bound is **polynomial in `t`** (`c/(1+t^2)`), not just
  "positive". This is what forbids exponential decay.
- The constants `c_k'` depend on the fixed nonzero mode of `theta_0`, on `C`,
  and on the universal constant `C_1`; they do not depend on `t`.
- The proof covers the `k=0` frozen mode separately and the `k != 0`
  modes with the BV lemma.
- No numerical computation is used as evidence.

## 9. Remaining gaps / status

There are no proof gaps in the theorem as stated under the given Fourier
normalization. The proof has not been through a fresh-context independent
adversarial audit (subagents were forbidden by the task instructions); the
internal self-audit found no error. Hence the honest label is
**CANDIDATE_COMPLETE_PROOF**, not `INDEPENDENTLY_AUDITED_PROOF`.
