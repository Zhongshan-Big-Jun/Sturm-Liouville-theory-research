# Independent Adversarial Audit Report

Audited file: `R-20260816T220000Z-densbc-o1p2/candidate_proof.md`
Upstream compared: `R-20260816T210000Z-densbc-o1p/candidate_proof.md`, `R-20260816T000000Z-densbc-o1/candidate_proof.md`
Audit method: independent recomputation of all claimed formulas, threshold argument, run decomposition, matrix rows, and explicit obstruction; symbolic verification with SymPy for the `v_1 = x^4` computations (script: `audit_verify.py` in the same run directory).

## Verdict

**REPAIRABLE_GAP**

The main mathematical architecture is sound.  The central criterion (Theorem 2) is correct for the stated `H_lambda` setting, and the `v_1 = x^4` non-density conclusion is correct for every `lambda in (-1,1)`.  There is one concrete computational error in a STRICT line (`p_7` coefficient) and several small omitted justifications.  None of these change the final conclusions.

---

## 1. Verification of the Hilbert space and moment map

**Result: PASS.**

1. `x^k = e_k + lambda e_{k+1}`.  The claimed expansion
   \[
   e_k = \sum_{j=0}^{N}(-\lambda)^j x^{k+j} + (-\lambda)^{N+1} e_{k+N+1}
   \]
   is correct.  Telescoping gives the stated remainder; the remainder has norm `|lambda|^{N+1}`.  Hence finite linear combinations of the `x^k` approximate every `e_k`, and since finite sequences are dense in `l^2(N_0)`, `Pi = span{x^k}` is dense.  So (H1) holds.

2. The moment map
   \[
   (Jw)_k = M_k(w) = \langle w,x^k\rangle = w_k + \lambda w_{k+1}
   \]
   is `J = I + lambda B` with `(Bw)_k = w_{k+1}`, `||B|| <= 1`.  Since `|lambda| < 1`, `I + lambda B` is invertible by Neumann series, with
   \[
   w_k = \sum_{j\ge 0}(-\lambda)^j M_{k+j}(w).
   \]
   Both `J` and `J^{-1}` are bounded; `J` is an isomorphism of `l^2` onto `l^2`.  The statement "realizability of a moment sequence is exactly square summability" is therefore correct.

## 2. Gram matrix

**Result: PASS.**

\[
G_{i,k}=\langle x^i,x^k\rangle
=\delta_{i,k}(1+\lambda^2)+\delta_{|i-k|,1}\lambda.
\]
Direct expansion gives the three contributing terms: `i=k`, `i=k+1`, and `k=i+1`.  Bandwidth is 1.

## 3. Theorem 1: cofinite kept set

**Result: PASS** (with a harmless loose sentence).

For `n >= 4`, `p_n = x^n - c_n x^{n-2}`.  For a representer of degree `d_j`,
\[
\langle v_j,p_n\rangle
= \sum_{i=0}^{d_j} c_i^{(j)}\big(G_{i,n} - c_n G_{i,n-2}\big).
\]
Because `G` has bandwidth 1:
- `G_{i,n} = 0` for all `i <= d_j` once `n > d_j + 1`;
- `G_{i,n-2} = 0` for all `i <= d_j` once `n-2 > d_j + 1`, i.e. `n > d_j + 3`.

Thus for `D = max_j d_j + 1`, every `n > D + 2 = max_j d_j + 3` is kept.  The proof's statement "If `n > d_j + 3` then both `n` and `n-2` are `> d_j + 1`" is correct.  The phrase about `{0,1}` being handled by "the same banded vanishing when D is large enough" is loose — `0,1` are never above `D+2` — but they are only finitely many low cases, so the cofiniteness conclusion is unaffected.  Consequently each parity has exactly one infinite run.

## 4. Theorem 2: obstruction space `=` `ker(T|_{B_fin})`

**Result: PASS in substance; minor proof omissions.**

The run decomposition and `rho_b(k) = floor(k/2)/floor(b/2)` reproduce the upstream corrected recursions.  For `w in V cap Q_sp^perp`, the kept recursions force
\[
M_k(w)=\sum_{b\in B} t_b \rho_b(k) 1_{k\in R_b},\qquad t_b=M_b(w).
\]

Key checks requested:

1. **Infinite-run moment vectors are not in `l^2`.**  For an infinite run `R_b`, `rho_b(k) ~ c k` along that parity (`c = 1/floor(b/2)`), so `sum rho_b(k)^2 = infinity`.  Correct.

2. **Each parity has at most one infinite run.**  Since `N` is cofinite, all sufficiently large vertices on a fixed parity are connected by kept edges, so they form one infinite tail.  Correct.

3. **Finite-support `M` produces `w = J^{-1}M in H_lambda`.**  Finite support is square summable and `J^{-1}` is bounded.  Correct.

4. **Kept edges in the infinite tail have `M_n = M_{n-2} = 0`.**  This is correct because the finite runs are all below the two infinite tails (a finite run cannot contain any vertex above the tail threshold on its parity).  The proof should say this explicitly; the current wording "because M has finite support below the tail" is acceptable but terse.

5. **Pinned `0,1` handling.**  The proof of the converse does not explicitly say that if `0 in N` (resp. `1 in N`) then `M_0 = 0` (resp. `M_1 = 0`).  This is true because `0` and `1` cannot belong to any finite run generated from `B_fin`, but it should be stated.  This is a repairable omission, not a mathematical error.

6. **Injective correspondence.**  The proof maps obstructions to kernel vectors and kernel vectors to obstructions, but does not spell out that the two maps are inverse.  This follows from density of `Pi` (`M=0` implies `w=0`) and from `t_b = M_b(w)`.  Repairable omission.

No fatal gap found in Theorem 2.

## 5. Theorem 4: `v_1 = x^4`

**Result: conclusion PASS; one concrete computational error in a displayed value.**

Representer moments: `a_3 = lambda`, `a_4 = A = 1+lambda^2`, `a_5 = lambda`, all others `0`.

Sparse coefficients used by the proof:
- `p_4 = x^4 - 2x^2` (correct),
- `p_5 = x^5 - 2x^3` (correct),
- `p_6 = x^6 - (3/2)x^4` (correct),
- `p_7 = x^7 - (3/2)x^5` (**the candidate used `4/3` on line 187; this is wrong**),
- `p_8 = x^8 - (4/3)x^6` (correct).

Because
\[
\langle v_1,p_7\rangle = G_{4,7} - c_7 G_{4,5} = -c_7\lambda,
\]
the correct value is `-(3/2)lambda`, not `-(4/3)lambda`.  The zero/nonzero pattern is unchanged: for `lambda != 0` it is nonzero, for `lambda = 0` it is zero.  Therefore the kept-set conclusion is unchanged.

Verified kept sets:
- `lambda != 0`: `N = {0,1} union {8,9,10,...}`.  Correct.
- `lambda = 0`: `N = {0,1,5,7} union {8,9,10,...}`.  Correct.

Free bases and runs:
- `lambda != 0`: even runs `{0}`, `{2}`, `{4}`, `{6,8,10,...}`; odd runs `{1}`, `{3}`, `{5}`, `{7,9,11,...}`.  Hence `B_fin = {2,3,4,5}`, `B_inf = {6,7}`.  Correct.
- `lambda = 0`: even runs `{0}`, `{2}`, `{4}`, `{6,8,10,...}`; odd runs `{1}`, `{3,5,7,9,...}`.  Hence `B_fin = {2,4}`, `B_inf = {3,6}`.  Correct.

T-rows:
- `lambda != 0`: on `B_fin = {2,3,4,5}`, row `(0,0,1,0)`.  Correct.
- `lambda = 0`: on `B_fin = {2,4}`, row `(0,1)`.  Correct.

In both cases `e_2` is in the kernel, so `ker(T|_{B_fin}) != {0}` and density fails.

Explicit obstruction:
\[
w = J^{-1}\delta_2 = \lambda^2 e_0 - \lambda e_1 + e_2.
\]
Verified moments:
\[
M_0 = 0,\quad M_1 = 0,\quad M_2 = 1,\quad M_k = 0\ (k\ge 3).
\]
Thus `w != 0`, `w in V` (since `M_4 = 0`), and `w perp Q_sp`.  The direct certificate is correct for all `lambda in (-1,1)`; at `lambda = 0` it is `w = e_2`.

## 6. Hidden assumptions and edge cases

- **`r` finite.**  The proof requires `r` finite to form the finite `r x B` matrix and to apply finite-dimensional kernel arguments.  The phrase "finite polynomial constraints" is ambiguous: each `v_j` has finite degree, but the theorem also needs the number `r` of constraints finite.  The `v_1 = x^4` part has `r=1`, so it is unaffected.  This should be stated as a standing hypothesis.
- **Polynomial representers with finite degree `d_j`.**  This is used essentially for the cofinite kept set and for the finite membership equations.  Correctly assumed.
- **`lambda in (-1,1)`.**  This is essential for `J = I + lambda B` invertible and for the explicit `l^2` realizability rule.  Correctly assumed.
- **"Each parity at most one infinite run" when `N` is cofinite.**  True; see §3.
- **Pinned `{0},{1}`.**  The definition and usage are correct: they are free only when not in `N`; when in `N`, `M_0 = 0` / `M_1 = 0` are forced and no free parameter is assigned.
- **Use of upstream Theorem A.**  The proof relies on the audited criterion `closure(span Q_sp) = V iff V cap Q_sp^perp = {0}`.  This is valid for closed `V`; here `V` is a finite intersection of kernels of continuous linear functionals, hence closed.

## Critical errors

- **None fatal.**
- One concrete error: line 187 uses `4/3` as the `p_7` sparse coefficient; the correct coefficient is `3/2`.  The displayed value `-(4/3)lambda` is false; it should be `-(3/2)lambda`.  The kept-set and non-density conclusions are unchanged.

## Gaps

1. **`p_7` coefficient error** (Section 5 above).  Must be corrected to maintain the "All statements are STRICT" claim.
2. **Theorem 2 converse does not explicitly handle pinned `n=0,1`.**  It follows from the construction, but should be stated.
3. **Theorem 2 isomorphism is asserted without explicitly proving the two maps are inverses.**  Easy to add using density of `Pi` and `t_b = M_b(w)`.
4. **Standing hypothesis `r` finite is not stated explicitly.**
5. **Theorem 1's sentence about `{0,1}` being handled by the same banded vanishing is imprecise**; harmless but should be reworded.

## Repair hints

- Replace line 187 with:
  \[
  \langle v_1,p_7\rangle = G_{4,7} - \frac{3}{2}G_{4,5} = -\frac{3}{2}\lambda.
  \]
  No further changes are needed: `N`, `B_fin`, `B_inf`, T-rows, and the explicit obstruction remain valid.
- In Theorem 2, add one sentence to the converse: "If `0 in N`, then `M_0 = 0` because no finite run from `B_fin` contains `0`; similarly for `1`."  Then note that the two constructions are inverse by the density of `Pi`.
- In the standing assumptions, state explicitly: "Let `r < infinity` and each `d_j < infinity`."
- Reword the `{0,1}` sentence in Theorem 1 to "the finitely many remaining indices are checked individually; only finitely many can fail."

---

## Summary

The candidate proof is mathematically sound in its main line.  The `H_lambda` moment-map reduction, the finite-rank criterion `ker(T|_{B_fin}) = {0}`, and the explicit `v_1 = x^4` obstruction all check out.  The only actual mathematical slip is the `p_7` coefficient `4/3` instead of `3/2`; it is cosmetic for the stated theorem but must be fixed because the run labels every line as STRICT.  Several small justifications are missing but easily added.  Verdict: **REPAIRABLE_GAP**.
