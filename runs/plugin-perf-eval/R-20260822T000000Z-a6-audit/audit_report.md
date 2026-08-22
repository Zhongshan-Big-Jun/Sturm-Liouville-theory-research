# Adversarial Audit: Root-1 No-Go for Higher-Degree Rational Product Ratios

Run: `R-20260822T000000Z-a6-audit`
Audited claim (verbatim summary):

> On the root-1 branch of the z-scaled third-order recurrence (Poincare limits
> 2,-1,0), for both even and odd recurrences and all `c > 0`, every rational
> product ratio `e_j = E_j/E_{j-1}` with `e_j -> 1` has reduced degree at most 2.
> Consequently there is no higher-degree (degree > 2) rational product solution
> on the root-1 branch. The known degree-<=2 families `E^(tau)` and `E^-` are
> the only rational root-1 product solutions.

Audited artifacts:

- `R-20260822T000000Z-a6-baseline/candidate_proof.md`
- `R-20260822T000000Z-a6-baseline/reproducibility/verify_asymptotic_no_go.py`
- `R-20260822T000000Z-a6-reuse/candidate_proof.md`
- `R-20260822T000000Z-a6-reuse/reproducibility/verify_diagonal_coefficient.py`
- `docs/SL_third_order_recurrence_theory.tex`
- `tools/third-order-recurrence.md`
- `scripts/op13_*.py` (context only)

The audit was carried out independently: all load-bearing expansions, diagonal
coefficients, and formal-uniqueness assertions were re-derived with exact
symbolic computation (SymPy) and checked against the source recurrence. No
numerical step is used as proof. No subagent was spawned.

---

## 1. Statement fidelity

The claim as stated matches the recurrence and definitions in
`docs/SL_third_order_recurrence_theory.tex`:

- The recurrence is `z_j = a_1(j) z_{j-1} + a_2(j) z_{j-2} + a_3(j) z_{j-3}`
  for `j >= 3`, with explicit even/odd rational coefficients and limits
  `(2,-1,0)`.
- The product-solution equivalence `E_j = prod_{k=1}^j e_k` solves the
  recurrence iff `e_j = a_1(j) + a_2(j)/e_{j-1} + a_3(j)/(e_{j-1} e_{j-2})`
  for `j >= 3` is exactly Lemma 3.1 (`lem:fp`) in the source.
- The root-1 branch is the case `e_j -> 1`; the root-0/minimal branch
  (`e_j -> 0`) is outside the claim and is correctly left open.
- "Reduced degree" is correctly taken after cancellation of common factors.
  The source's degree-2 classification already covers `E^(tau)` and `E^-`;
  the new contribution is, in principle, the exclusion of all higher degrees.

One wording nuance: `E^(tau)` in the source is written for `tau != -1`, while
the explicit ratio `(1 -/+ 1/(2j)) (j+tau+1)/(j+tau)` is an exact rational
solution for all `tau`, including degenerate values such as `tau = -1`
(where it may have a finite pole at a small positive integer). This does not
affect the degree bound: those ratios still have reduced degree at most 2.
The claim can be read as including the degenerate limiting/tail members, and
the project contract already records this convention. The audit treats this as
a notation issue, not a mathematical error.

---

## 2. Independent re-derivation of the asymptotic classification

Using `t = 1/j`, the fixed-point identity is equivalent to the formal identity

```
E(t) E(t/(1-t)) E(t/(1-2t))
  = A_1(t) E(t/(1-t)) E(t/(1-2t)) + A_2(t) E(t/(1-2t)) + A_3(t),
```

where `E(t) = 1 + u t + x_2 t^2 + ...` and `A_i(t) = a_i(1/t)`. The
coefficient expansions are:

- even: `A_1 = 2 - t + (c/4)t^2 + O(t^3)`,
  `A_2 = -1 + t + (1/4 - c/2)t^2 + O(t^3)`,
  `A_3 = (c/4)t^2 + O(t^3)`;
- odd: `A_1 = 2 + t + (c/4)t^2 + O(t^3)`,
  `A_2 = -1 - t + (-3/4 - c/2)t^2 + O(t^3)`,
  `A_3 = (c/4)t^2 + O(t^3)`.

These match the scripts and the source formulas.

The first non-vanishing constraint is at `t^2`:

```
even: (2u-1)(2u+1)/4 = 0,
odd : (2u-3)(2u-1)/4 = 0.
```

Thus

```
u in {-1/2, 1/2}  (even),  u in {1/2, 3/2}  (odd).
```

This agrees with Theorem 6.1 of the source and with both candidate proofs.
The rigid/free split is also correct:

- even `u = -1/2` rigid, `u = 1/2` free;
- odd `u = 1/2` rigid, `u = 3/2` free.

---

## 3. Diagonal-coefficient mechanism

The reuse-gate proof's central Lemma 2 was checked independently. Differentiating
the residual `G(t)` with respect to `x_m` and taking the `t^(m+1)` coefficient
gives exactly

```
even: D_m = 2u - (m-1),
odd : D_m = 2u - (m+1),
```

and the next unknown `x_(m+1)` cancels at the same order (`d/dx_(m+1) = 0`).
I re-derived this for `m = 2..8`, both parities, before substituting allowed
`u`; all results match.

The baseline proof's alternate slope formulation was also checked. In the
unmultiplied residual `F - e`, the coefficient of `t^m` is affine in `A_(m-1)`
with diagonal coefficient

```
(m-1) + f_1,   f_1 = -(epsilon + 2u),
```

where `epsilon = +1` (even), `epsilon = -1` (odd). This gives the same
triangular structure: free branches have zero diagonal at `m=3` and nonzero
thereafter; rigid branches have positive diagonals everywhere. The baseline
formula is correct.

The triangularity argument is load-bearing and is correct:
- at order `t^(m+1)`, the equation is affine linear in `x_m`;
- `x_(m+1)` does not occur;
- on the rigid branches, `D_2 != 0` and `D_m != 0` for all `m >= 3`;
- on the free branches, `D_2 = 0` and `D_m != 0` for all `m >= 3`.

Consequently the formal expansion is uniquely determined by `u` (rigid) or by
`(u, x_2)` (free). This part is mathematically sound.

---

## 4. Known families and rational-function uniqueness

The known families used for comparison are

```
even: e^(tau)_j = (1 - 1/(2j)) (j + tau + 1)/(j + tau),
odd : e^(tau)_j = (1 + 1/(2j)) (j + tau + 1)/(j + tau),
```

plus `E^-`:

```
even: 1 - 1/(2j),   odd: 1 + 1/(2j).
```

I verified symbolically, for generic `c > 0` and generic `tau`, that both
`E^(tau)` and `E^-` satisfy the fixed-point identity exactly (residual
identically zero). Their asymptotic expansions are

```
even E^(tau): 1 + (1/2)t - (tau + 1/2)t^2 + (tau^2 + tau/2)t^3 - ...,
odd  E^(tau): 1 + (3/2)t + (1/2 - tau)t^2 + (tau^2 - tau/2)t^3 - ...,
```

so the parameter map `x_2 <-> tau` is one-to-one on each free branch. These are
exactly the unique formal expansions described above.

The final step, "a rational function is determined by its Laurent expansion at
infinity", is valid in the following sense: if two rational functions have the
same formal expansion in powers of `1/j`, their difference is a rational
function with an identically zero expansion at infinity; multiplying by the
common denominator shows the numerator polynomial is zero. Hence the difference
is the zero rational function. This justifies the identification of any
rational root-1 solution with the corresponding `E^(tau)` or `E^-`.

---

## 5. Boundary cases

- **Even/odd**: both parities are covered and were checked separately.
- **`c > 0`**: all diagonal coefficients and allowed `u` are independent of
  `c`; the constant `c` only enters higher-order terms. The formal uniqueness,
  and hence the no-go, is uniform in `c > 0`.
- **Small `m`**: the free-branch degeneracy is exactly at `m = 2`
  (order `t^3`). The proof correctly identifies that `x_2` is the only free
  parameter. This is the one place where extra justification is desirable
  (see Section 6).
- **Root-0/minimal branch**: correctly left open; not part of the audited
  claim.
- **Degenerate `tau`**: finite poles at small positive integers do not create
  higher-degree solutions; the degree bound remains true.

---

## 6. Gaps and repairs

No fatal gap was found. The mathematical core (asymptotic classification +
diagonal triangularity + formal uniqueness + rational-function uniqueness) is
correct and sufficient to prove the root-1 no-go.

However, two non-fatal, easily repairable proof-exposition gaps were found.

### Gap 1 (minor, both candidate proofs): "x_2 is free" needs the vanishing of the whole `t^3` equation

Locations:

- `R-20260822T000000Z-a6-baseline/candidate_proof.md`, Corollary
  "formal uniqueness", free-branch bullet (line 126).
- `R-20260822T000000Z-a6-reuse/candidate_proof.md`, Theorem, free-branch
  paragraph (lines 146-151).

Issue: `D_2 = 0` shows that the linear coefficient of `x_2` in the `t^3`
equation is zero, but by itself it does not show that every `x_2` is feasible;
there could in principle be a leftover constant term. In this problem the
residual at `t^3` is indeed identically zero for the allowed free `u`
(e.g. substituting `u = 1/2` even or `u = 3/2` odd makes the `t^3`
coefficient vanish identically), and the known `E^(tau)` family proves
existence of a solution for every `x_2`. The proofs do not spell this out.

Suggested repair: add one line saying that, after substituting the allowed
free `u`, the entire `t^3` coefficient of the residual is identically zero
(equiv. the known `E^(tau)` family shows all `x_2` are realized). Then
"`x_2` is free" is fully justified.

### Gap 2 (expository, baseline only): Lemma 2 is a proof sketch

Location: `R-20260822T000000Z-a6-baseline/candidate_proof.md`, Lemma 2
(lines 56-88).

Issue: the proof sketch says the `A_m` term "cancels between `e` and the
leading part of `F`" and sketches the slope, but does not give the full
derivative count that the reuse-gate proof gives. The reuse-gate Lemma 2 is a
complete derivative computation and can be used as the repair; after adopting
it, the baseline proof becomes fully formal.

---

## 7. Decision

The root-1 no-go claim is **mathematically sound as a strict partial result**.
The proof mechanism is not circular: it does not rely on the source's
unproven degree-`>2` exclusion, only on the asymptotic classification and on
the exact known families `E^(tau)`/`E^-` (which I independently verified).
The only issues are minor exposition gaps about the free-branch `t^3`
identically-zero check (and a sketch-level baseline derivation). They are
easy to repair and do not undermine the conclusion.

For the run-level verdict I use `REPAIRABLE_GAP` because the submitted proofs,
as written, omit one small but load-bearing justification in the free-branch
existence step. After the repair described above, the result can be registered
as a STRICT root-1 partial result.

## Verdict summary

- **Critical errors / fatal gaps:** 0
- **Repairable gaps:** 2 (one minor logical-justification gap shared by both
  proofs; one expository gap in the baseline proof)
- **Can the root-1 no-go be registered as a partial STRICT result?**
  Yes, mathematically it is sound; register it after the small free-branch
  `t^3` clarification (and optionally after aligning the baseline proof with
  the reuse proof's diagonal lemma).
