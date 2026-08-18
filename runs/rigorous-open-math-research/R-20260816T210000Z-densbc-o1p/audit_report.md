# Independent Adversarial Audit Report — R-20260816T210000Z-densbc-o1p

- Audit target: `candidate_proof.md` (current 286-line version) in
  `R-20260816T210000Z-densbc-o1p`.
- Upstream context read: `R-20260816T000000Z-densbc-o1/candidate_proof.md`,
  `R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md` (Theorem E and run-graph
  definitions), and the run contracts.
- Method: independent re-derivation of every strict claim; no step accepted on
  authority.

## Structured summary

- **Critical errors:** 0
- **Gaps:** 1 (minor, localized to a proof wording in Theorem 6)
- **Verdict:** REPAIRABLE_GAP
- Overall: the central mathematical argument is sound and does close the reduced
  core O1' on the stated subclass; the only defect is a one-line imprecision in
  the coordinate-case proof, which is trivial to repair.

## Per-obligation notes

### 1. Theorem 2 — moment parameterization of V cap Q_sp^orth

PASS.

- The Riesz representer is correctly written as
  `v_j = Sum \overline{c^{(j)}_k} x^k`, and the representer moments are
  `a^{(j)}_k = \overline{c^{(j)}_k} (k+1)^{2 beta}` for `k <= d_j`, zero above.
  This is the correct conjugate formula for complex coefficients.
- The kept-set condition `p_n in V` is correctly equivalent to vanishing of the
  conjugate sum because the `p_n` have real coefficients.
- The run recursion is correct: a kept `p_{2m}` forces
  `M_{2m} = (m/(m-1)) M_{2m-2}`, and iteration gives
  `rho_b(k) = floor(k/2)/floor(b/2)` for `b >= 2`. The formulas for `b=0,1` are
  handled separately.
- The parameterization
  `M_k(w) = Sum_{b : k in R_b} t_b rho_b(k)` is correct because runs are
  disjoint and every vertex lies in exactly one run. Pinned vertices `0,1` are
  correctly represented by omitting them from `B` when they are in `N`.
- The membership matrix `T` is correct: it uses the original coefficients `c`,
  not the conjugated representer moments, and truncation at `D` is valid because
  `c^{(j)}_k = 0` for `k > d_j`.
- The norm identity
  `||w||_beta^2 = Sum_b |t_b|^2 C_b(beta)` is exact because the runs are
  disjoint, so there are no cross terms.
- Injectivity is valid: if two parameter vectors give the same `w`, all moments
  agree; in fact `t_b = M_b(w)` for each free base, and `Pi` density gives the
  uniqueness of `w`. The added `0 * inf` convention in condition (iii) is
  appropriate.

### 2. Lemma 3 — summability classification

PASS.

- For an even infinite run with base `b = 2a`, the computation is
  `C_b(beta) = a^{-2} Sum_{m=a}^inf m^2 (2m+1)^{-2 beta}`.
  The summand is asymptotic to `(1/4^beta) m^{2 - 2 beta}`, which converges iff
  `2 - 2 beta < -1`, i.e. iff `beta > 3/2`.
- For an odd infinite run with base `b = 2a+1`, the analogous sum is
  `a^{-2} Sum_{m=a}^inf m^2 (2m+2)^{-2 beta}`, with the same threshold.
- Finite runs and the singleton runs `b=0,1` are finite sums, hence admissible
  for every `beta >= 0`.
- The corrected ratio `rho_b(k) = floor(k/2)/floor(b/2)` is used consistently and
  does not change the threshold.

### 3. Theorem 4 — exact decision criterion

PASS.

- By upstream Theorem A, density is equivalent to `V cap Q_sp^orth = {0}`.
- Theorem 2 gives the exact isomorphism
  `V cap Q_sp^orth ~= { t in C^B : T t = 0, t_b = 0 whenever C_b(beta) = inf }`.
- The "no cancellation" remark is correct: because the `R_b` are disjoint, the
  norm is a sum of nonnegative terms `|t_b|^2 C_b(beta)`, so a nonzero `t_b`
  with `C_b(beta) = inf` cannot be cancelled by another run.
- Restricting to `B_adm = { b : C_b(beta) < inf }` gives exactly
  `ker(T|_{B_adm}) = {0}` as the density criterion, equivalently the linear
  independence of the columns `A m_b` for `b in B_adm`.
- The `r=0` convention is handled correctly: `T` is the zero map to `{0}`, and
  `ker(T|_{B_adm}) = {0}` iff `B_adm = empty`, which recovers the whole-space
  criterion.

### 4. Theorem 6 — regression to coordinate/diagonal Theorem E

PASS with one minor wording gap.

- In the coordinate case, each row of `A` is a unit vector, so the `i`-th row of
  `A m_b` is `rho_b(i)` if `i in R_b` and `0` otherwise. Since runs are disjoint,
  a row `i` kills exactly the one run containing degree `i`.
- For `beta > 3/2`, the top infinite run on each parity is admissible and
  contains no constrained degree; it gives a zero column, so density fails.
- For `beta <= 3/2`, only finite runs are admissible. A finite free run with no
  constrained degree is exactly a finite run in the sense of Theorem E and gives
  a zero column. Conversely, if there is no such finite run, every finite
  **free-base component** contains a constrained degree and is killed by the
  corresponding row; infinite runs are inadmissible. Hence the kernel is trivial
  exactly when `R` has no finite run and `beta <= 3/2`.
- **Gap:** the proof says literally "every finite component contains at least one
  constrained degree". This is false for the pinned singleton components `{0}`
  and `{1}` when `0,1 notin R` (e.g. `R = empty`). Those components contain no
  free base, so the intended conclusion is unaffected. The sentence should be
  restricted to finite components that contain a free base, or to finite runs in
  the sense of Theorem E.
- The `r=0` / `R=empty` recovery is correct: density holds iff `beta <= 3/2`.

### 5. Example 7 — non-coordinate obstruction

PASS.

- For the stated family, `p_4 = x^4 - 2x^2`: the coefficient is
  `m/(m-1) = 2/(2-1) = 2`. The value `4/3` appearing in some older notes belongs
  to `p_8`, not `p_4`. Since `a_2 = 0`, the computed value is unchanged either
  way, but the candidate's `a_4 - 2 a_2` is the correct formula for `p_4`.
- With `v_1 = x^4 + alpha x^6`, `alpha` real, one has
  `a_4 = <v_1,x^4>_beta = 5^{2 beta}` and `a_2 = 0`, so
  `<v_1,p_4>_beta = 5^{2 beta} != 0`. Hence `4 notin N`.
- `w = x^2` is nonzero and in `H_beta` for every `beta`; it lies in `V` because
  `M_4(w) = M_6(w) = 0`.
- For every kept `p_n`, `<w,p_n>_beta = 0`: `p_0,p_1` have zero moments, and for
  `n >= 4` the only sparse element whose support contains degree `2` is `p_4`,
  which is not kept.
- Degree `2` is a finite free base with `R_2 = {2}`, `m_2` supported at `M_2`,
  and `A m_2 = 0`. By Theorem 4/Corollary 5, `closure(span Q_sp) != V` for every
  `beta >= 0`. The example is genuinely non-coordinate.

### 6. Hidden assumptions and cofinite kept set

PASS.

- For `n > D+2`, the support of `p_n` is `{n,n-2}` and both entries exceed `D`,
  so all `a^{(j)}_n = a^{(j)}_{n-2} = 0`; hence `p_n in V`. This is correct.
- The index set clarification (`N = {0,1} union {4,5,...}`, with `2,3` absent and
  always treated as free bases) removes the earlier ambiguity.
- `D = -1` for `r=0` is handled consistently.
- Minor clarification: the proof should explicitly state that the number of
  constraints `r` is finite. This is implicit in the finite matrix formalism and
  in the upstream `r < inf` convention, but it is a standing hypothesis that
  should be written down.

### 7. Algorithmic content and complexity

PASS.

- The algorithm is finite and correct on the subclass:
  1. `N` for `n <= D+2` costs `O(rD)` inner-product evaluations (each `p_n` has
     support of size at most 2).
  2. The run graph has `O(D)` vertices below the cofinite threshold plus two
     infinite tails; building it costs `O(D)`.
  3. The free-base list `B` has `O(D)` elements.
  4. Each column `A m_b` costs `O(rD)`, so building `T|_{B_adm}` costs
     `O(r D |B|)`.
  5. Kernel/rank computation costs `O(r |B|^2)` or `O(|B|^3)` using exact linear
     algebra.
- Thus the criterion is genuinely finite-dimensional on this subclass. The only
  caveat is the usual one for "decidability": coefficients and `beta` must be
  given in a form admitting exact arithmetic; as a mathematical decision
  criterion this is not a defect.

## Findings

- **Critical errors:** none.
- **Gaps:**
  1. Theorem 6 proof wording: "every finite component contains at least one
     constrained degree" should be "every finite component that contains a free
     base" (or "every finite run in the sense of Theorem E"). The pinned
     components `{0}`, `{1}` when unconstrained are counterexamples to the
     literal sentence, but they carry no free parameter and do not affect the
     kernel.
- **Repair hints:**
  1. In Theorem 6, replace the sentence with:
     "Conversely, if R has no finite run, then every finite component containing
     a free base contains at least one constrained degree; the corresponding row
     forces its t_b to vanish."
  2. Optionally add an explicit standing hypothesis `r < inf` in Section 0.

## Verdict

**REPAIRABLE_GAP** — the core proof is mathematically correct and closes O1' on
the structured subclass; only a one-line clarification in Theorem 6 (and an
optional explicit finiteness of `r`) is needed.
