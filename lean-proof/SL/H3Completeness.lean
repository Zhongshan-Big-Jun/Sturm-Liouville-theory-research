import Mathlib
import SL.Completeness

open scoped BigOperators

/-!
# H^3 completeness: H1-moment recurrence, polynomial bound, annihilation

Formalization of the algebraic core of `docs/SL_h3_completeness_proof.tex`
(Sections 3-6): the moment-jump mechanism for the third left-definite space
H^3[-1,1].

Let w in H^1 and let M_k = (w, x^k)_1 be the H1-moments (M is the H1 inner
product functional on polynomials, which is Real-linear).  Orthogonality
(w, K_c p_n)_1 = 0 for every admissible n gives M_0 = M_1 = 0 and the second
order jump recurrences

  c * M_{2m}   = A_m   * M_{2m-2}   - B_m   * M_{2m-4},
  c * M_{2m+1} = A'_m  * M_{2m-1}  - B'_m  * M_{2m-3},

hence by the scaling lemma M_{2m} = M_2 u_m and M_{2m+1} = M_3 u'_m.  The
superfactorial growth u_m >= (4/c)^(m-1) * m! (obtained here uniformly for
both coefficient families from `StabilityGrowth.product_growth`, since
A_m - B_m = 4m + c*q_m >= 4m and A'_m - B'_m = 4m + c*q_m >= 4m for m >= 2)
together with a polynomial bound |M_{2m}| <= C * sqrt m forces M_2 = M_3 = 0,
hence all H1-moments vanish (the annihilation step; Section 6 of the source).

The analytic H1 bound (Section 5, Cauchy-Schwarz estimate
|M_{2m}| <= C sqrt m) is stated as an assumption `hbdE`/`hbdO` in
`all_moments_zero_of_orthogonal`; its derivation from the H1 inner product is
the analytic companion that will be formalized together with the isometry
step.

All statements are over Real, reusing the coefficient families
(AR/BR/A'R/B'R, KcR, pEvenR, pOddR) from SL/Completeness.lean.
-/

namespace SL

namespace H3Completeness

open Polynomial

/-- The k-th moment of a Real-linear functional M on polynomials:
mu_k := M (X^k). -/
noncomputable def moments (M : Polynomial ℝ →ₗ[ℝ] ℝ) (k : ℕ) : ℝ :=
  M (X ^ k)

/-- M (C a * X^m) = a * mu_m for the monomials. -/
@[simp] lemma apply_C_mul_X_pow (M : Polynomial ℝ →ₗ[ℝ] ℝ) (a : ℝ) (m : ℕ) :
    M (C a * X ^ m) = a * moments M m := by
  rw [← Polynomial.smul_eq_C_mul]
  exact map_smul M a (X ^ m)

/-- K_c p_0 = c forces mu_0 = 0 when c != 0. -/
lemma constant_orth_moment_zero (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} (hc : c ≠ 0)
    (horth : M (Completeness.KcR c 1) = 0) : moments M 0 = 0 := by
  have hK : Completeness.KcR c 1 = C c := by simp [Completeness.KcR]
  have hM : M (Completeness.KcR c 1) = c * moments M 0 := by
    rw [hK]
    simpa [moments] using (apply_C_mul_X_pow M c 0)
  rw [horth] at hM
  have hmul : c * moments M 0 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

/-- K_c p_1 = c x forces mu_1 = 0 when c != 0. -/
lemma linear_orth_moment_zero (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} (hc : c ≠ 0)
    (horth : M (Completeness.KcR c X) = 0) : moments M 1 = 0 := by
  have hK : Completeness.KcR c X = C c * X := by simp [Completeness.KcR]
  have hM : M (Completeness.KcR c X) = c * moments M 1 := by
    rw [hK]
    simpa [moments] using (apply_C_mul_X_pow M c 1)
  rw [horth] at hM
  have hmul : c * moments M 1 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

/-- The jump recurrence for the even moments (Real):
    c mu_{2n} = A_n mu_{2n-2} - B_n mu_{2n-4}. -/
lemma even_recurrence (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} {n : ℕ} (hn : 2 ≤ n)
    (horth : M (Completeness.KcR c (Completeness.pEvenR n)) = 0) :
    c * moments M (2 * n) =
      Completeness.AR c n * moments M (2 * n - 2) - Completeness.BR n * moments M (2 * n - 4) := by
  have hK := Completeness.KcR_pEven c hn
  have hM : M (Completeness.KcR c (Completeness.pEvenR n)) =
      c * moments M (2 * n) - Completeness.AR c n * moments M (2 * n - 2) +
        Completeness.BR n * moments M (2 * n - 4) := by
    rw [hK]
    rw [map_add, map_sub]
    rw [apply_C_mul_X_pow M c (2 * n), apply_C_mul_X_pow M (Completeness.AR c n) (2 * n - 2),
      apply_C_mul_X_pow M (Completeness.BR n) (2 * n - 4)]
  rw [horth] at hM
  linarith

/-- The jump recurrence for the odd moments (Real):
    c mu_{2n+1} = A'_n mu_{2n-1} - B'_n mu_{2n-3}. -/
lemma odd_recurrence (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} {n : ℕ} (hn : 2 ≤ n)
    (horth : M (Completeness.KcR c (Completeness.pOddR n)) = 0) :
    c * moments M (2 * n + 1) =
      Completeness.A'R c n * moments M (2 * n - 1) - Completeness.B'R n * moments M (2 * n - 3) := by
  have hK := Completeness.KcR_pOdd c hn
  have hM : M (Completeness.KcR c (Completeness.pOddR n)) =
      c * moments M (2 * n + 1) - Completeness.A'R c n * moments M (2 * n - 1) +
        Completeness.B'R n * moments M (2 * n - 3) := by
    rw [hK]
    rw [map_add, map_sub]
    rw [apply_C_mul_X_pow M c (2 * n + 1), apply_C_mul_X_pow M (Completeness.A'R c n) (2 * n - 1),
      apply_C_mul_X_pow M (Completeness.B'R n) (2 * n - 3)]
  rw [horth] at hM
  linarith

/-- Orthogonality + mu_0 = 0 imply the even scaling mu_{2m} = mu_2 u_m
(Real instantiation of the abstract scaling lemma). -/
theorem even_moment_scaling (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} (hc : c ≠ 0)
    (h0 : moments M 0 = 0)
    (horth : ∀ n : ℕ, 2 ≤ n → M (Completeness.KcR c (Completeness.pEvenR n)) = 0) :
    ∀ m : ℕ, moments M (2 * m) =
      moments M 2 * StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m := by
  apply Completeness.even_scaling c (Completeness.AR c) (Completeness.BR) hc (moments M) h0
  intro n hn
  exact even_recurrence M hn (horth n hn)

/-- Orthogonality + mu_1 = 0 imply the odd scaling mu_{2m+1} = mu_3 u'_m. -/
theorem odd_moment_scaling (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c : ℝ} (hc : c ≠ 0)
    (h1 : moments M 1 = 0)
    (horth : ∀ n : ℕ, 2 ≤ n → M (Completeness.KcR c (Completeness.pOddR n)) = 0) :
    ∀ m : ℕ, moments M (2 * m + 1) =
      moments M 3 * StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m := by
  apply Completeness.odd_scaling c (Completeness.A'R c) (Completeness.B'R) hc (moments M) h1
  intro n hn
  exact odd_recurrence M hn (horth n hn)

/-! ## Superfactorial dominance over sqrt

For any lambda > 0 the sequence lambda^(m-1) * m! / sqrt m is unbounded
above (in the eps sense).  This is the analytic input that turns the
superfactorial growth of u into an annihilation argument against the
polynomial bound |mu_{2m}| <= C * sqrt m.
-/

/-- 2^n >= n for every n (elementary). -/
lemma two_pow_ge (n : ℕ) : 2 ^ n ≥ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      calc
        n + 1 ≤ 2 ^ n + 1 := by omega
        _ ≤ 2 ^ n + 2 ^ n := by
          have h1 : (1 : ℕ) ≤ 2 ^ n := Nat.succ_le_of_lt (pow_pos (by norm_num) n)
          omega
        _ = 2 ^ (n + 1) := by
          rw [pow_succ]
          ring

/-- (2n)! >= n^n (real cast). -/
lemma factorial_two_mul_ge_pow (n : ℕ) :
    ((Nat.factorial (2 * n) : ℕ) : ℝ) ≥ (n : ℝ) ^ n := by
  by_cases hn : n = 0
  · subst n; simp
  · have hn1 : 1 ≤ n := by omega
    -- (2n)! = n! * prod_{i<n} (n+i+1) >= n! * n^n
    have hsplit : Nat.factorial (2 * n) =
        Nat.factorial n * ∏ i ∈ Finset.range n, (n + i + 1) := by
      rw [← Finset.prod_range_add_one_eq_factorial, ← Finset.prod_range_add_one_eq_factorial]
      have h2n : 2 * n = n + n := by omega
      rw [h2n, Finset.prod_range_add]
    have hprod : (∏ i ∈ Finset.range n, (n + i + 1 : ℕ)) ≥ n ^ n := by
      calc
        (∏ i ∈ Finset.range n, (n + i + 1 : ℕ))
            ≥ ∏ i ∈ Finset.range n, (n : ℕ) := by
              apply Finset.prod_le_prod
              · intro i hi; positivity
              · intro i hi; omega
        _ = n ^ n := by simp
    rw [hsplit]
    calc
      ((Nat.factorial n * ∏ i ∈ Finset.range n, (n + i + 1) : ℕ) : ℝ)
          = (Nat.factorial n : ℝ) * (∏ i ∈ Finset.range n, (n + i + 1 : ℕ) : ℝ) := by norm_num
      _ ≥ (Nat.factorial n : ℝ) * (n : ℝ) ^ n := by
            exact mul_le_mul_of_nonneg_left (by exact_mod_cast hprod) (Nat.cast_nonneg _)
      _ ≥ 1 * (n : ℝ) ^ n := by
            exact mul_le_mul_of_nonneg_right (by exact_mod_cast (Nat.factorial_pos n)) (pow_nonneg (by positivity) n)
      _ = (n : ℝ) ^ n := by ring

/-- lambda^(m-1) * m! / sqrt m is unbounded: for every X there is m >= 1 with
X < lambda^(m-1) * m! / sqrt m. -/
lemma superfactorial_unbounded (lam : ℝ) (hlam : 0 < lam) (X : ℝ) :
    ∃ m : ℕ, 1 ≤ m ∧ X < lam ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ) := by
  by_cases hX : X ≤ 0
  · refine ⟨1, by norm_num, ?_⟩
    have hpos : 0 < lam ^ (1 - 1) * (Nat.factorial 1 : ℝ) / Real.sqrt (1 : ℝ) := by
      simp [pow_zero]
    linarith
  · have hXpos : 0 < X := lt_of_not_ge hX
    -- pick n with 2 <= n, 2 <= lam^2 * n and 2 * lam^2 * X^2 < n
    let bound : ℝ := max 2 (max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2))
    rcases exists_nat_gt bound with ⟨n, hn⟩
    have hn2 : 2 ≤ n := by
      have hlt : (2 : ℝ) < (n : ℝ) :=
        lt_of_le_of_lt (le_max_left 2 (max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2))) hn
      exact_mod_cast (le_of_lt hlt)
    have hnlam : 2 ≤ lam ^ 2 * (n : ℝ) := by
      have hb : 2 / lam ^ 2 < (n : ℝ) := by
        have hb1 : 2 / lam ^ 2 ≤ max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2) := le_max_left _ _
        have hb2 : max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2) ≤ bound := le_max_right _ _
        exact lt_of_le_of_lt (le_trans hb1 hb2) hn
      have hdiv : 2 < (n : ℝ) * lam ^ 2 := (div_lt_iff₀ (by positivity : 0 < lam ^ 2)).mp hb
      simpa [mul_comm] using le_of_lt hdiv
    have hnX : 2 * lam ^ 2 * X ^ 2 < (n : ℝ) := by
      have hb1 : 2 * lam ^ 2 * X ^ 2 ≤ max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2) := le_max_right _ _
      have hb2 : max (2 / lam ^ 2) (2 * lam ^ 2 * X ^ 2) ≤ bound := le_max_right _ _
      exact lt_of_le_of_lt (le_trans hb1 hb2) hn
    -- use m = 2n
    refine ⟨2 * n, by omega, ?_⟩
    have hfac := factorial_two_mul_ge_pow n
    have hmain : X < lam ^ (2 * n - 1) * ((n : ℝ) ^ n) / Real.sqrt ((2 * n : ℕ) : ℝ) := by
      have hlam_ne : lam ≠ 0 := ne_of_gt hlam
      have hpow' : lam ^ (2 * n - 1) = (lam ^ 2) ^ n / lam := by
        rw [← pow_mul]
        have hsub : 2 * n - 1 + 1 = 2 * n := by omega
        rw [← hsub, pow_succ]
        field_simp [hlam_ne]
        exact congrArg (fun k : ℕ => lam ^ k) (by omega)
      have hnlam_pow : (lam ^ 2 * (n : ℝ)) ^ n ≥ (2 : ℝ) ^ n := by
        exact pow_le_pow_left₀ (by norm_num) hnlam n
      have hA : lam ^ (2 * n - 1) * (n : ℝ) ^ n / Real.sqrt ((2 * n : ℕ) : ℝ)
          ≥ (2 : ℝ) ^ n / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := by
        calc
          lam ^ (2 * n - 1) * (n : ℝ) ^ n / Real.sqrt ((2 * n : ℕ) : ℝ)
              = ((lam ^ 2) ^ n / lam) * (n : ℝ) ^ n / Real.sqrt ((2 * n : ℕ) : ℝ) := by rw [hpow']
          _ = (lam ^ 2 * (n : ℝ)) ^ n / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := by
                field_simp [hlam_ne, (show Real.sqrt ((2 * n : ℕ) : ℝ) ≠ 0 by positivity)]
                ring
          _ ≥ (2 : ℝ) ^ n / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := by
                exact div_le_div_of_nonneg_right hnlam_pow (by positivity)
      have hB : (2 : ℝ) ^ n / (lam * Real.sqrt ((2 * n : ℕ) : ℝ))
          ≥ (n : ℝ) / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := by
        exact div_le_div_of_nonneg_right (by exact_mod_cast (two_pow_ge n)) (by positivity)
      have hC : (n : ℝ) / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) = Real.sqrt (n : ℝ) / (lam * Real.sqrt 2) := by
        have hsqrt : Real.sqrt ((2 * n : ℕ) : ℝ) = Real.sqrt 2 * Real.sqrt (n : ℝ) := by
          rw [← Real.sqrt_mul (by positivity : 0 ≤ (2 : ℝ)) (n : ℝ)]
          norm_num
        rw [hsqrt]
        field_simp [(show lam ≠ 0 by positivity), (show Real.sqrt 2 ≠ 0 by positivity),
          (show Real.sqrt (n : ℝ) ≠ 0 by positivity)]
        rw [Real.sq_sqrt (by positivity : 0 ≤ (n : ℝ))]
      have hD : X < Real.sqrt (n : ℝ) / (lam * Real.sqrt 2) := by
        have hside : (X * (lam * Real.sqrt 2)) ^ 2 < (n : ℝ) := by
          calc
            (X * (lam * Real.sqrt 2)) ^ 2 = X ^ 2 * (lam ^ 2 * 2) := by
              ring_nf
              rw [Real.sq_sqrt (by norm_num : 0 ≤ (2 : ℝ))]
            _ = 2 * lam ^ 2 * X ^ 2 := by ring
            _ < (n : ℝ) := hnX
        have hsq : (X * (lam * Real.sqrt 2)) ^ 2 < (Real.sqrt (n : ℝ)) ^ 2 := by
          simpa [Real.sq_sqrt (by positivity : 0 ≤ (n : ℝ))] using hside
        have hltabs : |X * (lam * Real.sqrt 2)| < |Real.sqrt (n : ℝ)| := (sq_lt_sq).1 hsq
        have hX0 : 0 ≤ X * (lam * Real.sqrt 2) := by positivity
        have hs0 : 0 < Real.sqrt (n : ℝ) := by positivity
        have hlt' : X * (lam * Real.sqrt 2) < Real.sqrt (n : ℝ) := by
          simpa [abs_of_nonneg hX0, abs_of_pos hs0] using hltabs
        exact (lt_div_iff₀ (by positivity : 0 < lam * Real.sqrt 2)).2 hlt'
      calc
        X < Real.sqrt (n : ℝ) / (lam * Real.sqrt 2) := hD
        _ = (n : ℝ) / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := hC.symm
        _ ≤ (2 : ℝ) ^ n / (lam * Real.sqrt ((2 * n : ℕ) : ℝ)) := hB
        _ ≤ lam ^ (2 * n - 1) * (n : ℝ) ^ n / Real.sqrt ((2 * n : ℕ) : ℝ) := hA
    have hfinal : lam ^ (2 * n - 1) * (n : ℝ) ^ n / Real.sqrt ((2 * n : ℕ) : ℝ)
        ≤ lam ^ (2 * n - 1) * (Nat.factorial (2 * n) : ℝ) / Real.sqrt ((2 * n : ℕ) : ℝ) := by
      exact div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_left hfac (pow_nonneg (by positivity) (2 * n - 1)))
        (by positivity)
    have hgoal : X < lam ^ (2 * n - 1) * (Nat.factorial (2 * n) : ℝ) / Real.sqrt ((2 * n : ℕ) : ℝ) :=
      lt_of_lt_of_le hmain hfinal
    simpa using hgoal

/-! ## Superfactorial growth for the Krein coefficient families

Both the even family (AR, BR) and the odd family (A'R, B'R) satisfy the
quantitative growth lemma with A k - B k >= 4k (since
A k - B k = 4k + c*q k and q k >= 0 for k >= 2), hence
u m >= ∏_{k=2..m} (4k/c) = (4/c)^(m-1) * m!.
-/

/-- prod_{k=2..m} k = m! (real cast). -/
lemma prod_Icc_two_cast_factorial (m : ℕ) :
    (∏ k ∈ Finset.Icc 2 m, (k : ℝ)) = (Nat.factorial m : ℝ) := by
  induction m with
  | zero => simp
  | succ m ih =>
      by_cases hm : 2 ≤ m + 1
      · rw [Finset.prod_Icc_succ_top hm, ih, Nat.factorial_succ, Nat.cast_mul]
        ring
      · have hm0 : m = 0 := by omega
        subst m
        simp

/-- Superfactorial growth for the even Krein coefficients:
    (4/c)^(m-1) * m! <= u_m. -/
lemma even_growth {c : ℝ} (hc : 0 < c) :
    ∀ m : ℕ, 1 ≤ m → (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
      StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m := by
  intro m hm
  have hB : ∀ n : ℕ, 2 ≤ n → 0 ≤ Completeness.BR n := fun n hn => Completeness.BR_nonneg hn
  have hAB : ∀ n : ℕ, 2 ≤ n → c ≤ Completeness.AR c n - Completeness.BR n :=
    fun n hn => Completeness.AR_sub_BR_ge_c c (le_of_lt hc) hn
  have hprod := StabilityGrowth.product_growth (K := ℝ) (c0 := c) (A := Completeness.AR c)
    (B := Completeness.BR) hc hB hAB m hm
  have hle : (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
      ∏ k ∈ Finset.Icc 2 m, ((Completeness.AR c k - Completeness.BR k) / c) := by
    have hcoef : ∀ k : ℕ, 2 ≤ k → 4 * (k : ℝ) ≤ Completeness.AR c k - Completeness.BR k := by
      intro k hk
      rw [Completeness.AR_sub_BR c hk]
      have hcq : 0 ≤ c * Completeness.qR k :=
        mul_nonneg (le_of_lt hc) (Completeness.qR_nonneg hk)
      nlinarith
    have hle_prod : (∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c) ≤
        ∏ k ∈ Finset.Icc 2 m, ((Completeness.AR c k - Completeness.BR k) / c) := by
      refine Finset.prod_le_prod ?_ ?_
      · intro k hk
        positivity
      · intro k hk
        exact div_le_div_of_nonneg_right (hcoef k (Finset.mem_Icc.mp hk).1) (le_of_lt hc)
    have hprod_id : (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
        ∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c := by
      have hfac : ∀ k : ℕ, ((4 : ℝ) * (k : ℝ)) / c = (4 / c) * (k : ℝ) := by
        intro k
        ring
      have hcard : (Finset.Icc 2 m).card = m - 1 := by
        rw [Nat.card_Icc]
        omega
      have hprod_eq : (∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c) =
          (4 / c) ^ (m - 1) * (∏ k ∈ Finset.Icc 2 m, (k : ℝ)) := by
        rw [Finset.prod_congr rfl (by intro k hk; exact hfac k)]
        rw [Finset.prod_mul_distrib, Finset.prod_const, hcard]
      have hfact : (∏ k ∈ Finset.Icc 2 m, (k : ℝ)) = (Nat.factorial m : ℝ) :=
        prod_Icc_two_cast_factorial m
      rw [hprod_eq, hfact]
    exact le_trans hprod_id hle_prod
  exact le_trans hle hprod

/-- Superfactorial growth for the odd Krein coefficients:
    (4/c)^(m-1) * m! <= u'_m. -/
lemma odd_growth {c : ℝ} (hc : 0 < c) :
    ∀ m : ℕ, 1 ≤ m → (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
      StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m := by
  intro m hm
  have hB : ∀ n : ℕ, 2 ≤ n → 0 ≤ Completeness.B'R n := fun n hn => Completeness.B'R_nonneg hn
  have hAB : ∀ n : ℕ, 2 ≤ n → c ≤ Completeness.A'R c n - Completeness.B'R n :=
    fun n hn => Completeness.A'R_sub_B'R_ge_c c (le_of_lt hc) hn
  have hprod := StabilityGrowth.product_growth (K := ℝ) (c0 := c) (A := Completeness.A'R c)
    (B := Completeness.B'R) hc hB hAB m hm
  have hle : (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
      ∏ k ∈ Finset.Icc 2 m, ((Completeness.A'R c k - Completeness.B'R k) / c) := by
    have hcoef : ∀ k : ℕ, 2 ≤ k → 4 * (k : ℝ) ≤ Completeness.A'R c k - Completeness.B'R k := by
      intro k hk
      rw [Completeness.A'R_sub_B'R c hk]
      have hcq : 0 ≤ c * Completeness.qR k :=
        mul_nonneg (le_of_lt hc) (Completeness.qR_nonneg hk)
      nlinarith
    have hle_prod : (∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c) ≤
        ∏ k ∈ Finset.Icc 2 m, ((Completeness.A'R c k - Completeness.B'R k) / c) := by
      refine Finset.prod_le_prod ?_ ?_
      · intro k hk
        positivity
      · intro k hk
        exact div_le_div_of_nonneg_right (hcoef k (Finset.mem_Icc.mp hk).1) (le_of_lt hc)
    have hprod_id : (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤
        ∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c := by
      have hfac : ∀ k : ℕ, ((4 : ℝ) * (k : ℝ)) / c = (4 / c) * (k : ℝ) := by
        intro k
        ring
      have hcard : (Finset.Icc 2 m).card = m - 1 := by
        rw [Nat.card_Icc]
        omega
      have hprod_eq : (∏ k ∈ Finset.Icc 2 m, ((4 : ℝ) * (k : ℝ)) / c) =
          (4 / c) ^ (m - 1) * (∏ k ∈ Finset.Icc 2 m, (k : ℝ)) := by
        rw [Finset.prod_congr rfl (by intro k hk; exact hfac k)]
        rw [Finset.prod_mul_distrib, Finset.prod_const, hcard]
      have hfact : (∏ k ∈ Finset.Icc 2 m, (k : ℝ)) = (Nat.factorial m : ℝ) :=
        prod_Icc_two_cast_factorial m
      rw [hprod_eq, hfact]
    exact le_trans hprod_id hle_prod
  exact le_trans hle hprod

/-! ## Annihilation

The superfactorial growth u_m >= (4/c)^(m-1) * m! (even_growth / odd_growth)
combined with the polynomial bound |mu_{2m}| <= C * sqrt m forces the free
parameters mu_2, mu_3 to vanish.
-/

/-- If |a| * u_m <= C * sqrt m for all m >= 1 and u grows at least like
(4/c)^(m-1) * m!, then a = 0. -/
theorem superfactorial_annihilate {c : ℝ} (hc : 0 < c) {a C : ℝ}
    {u : ℕ → ℝ} (hu : ∀ m : ℕ, 1 ≤ m → (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤ u m)
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| * u m ≤ C * Real.sqrt (m : ℝ)) : a = 0 := by
  by_contra ha
  have hδ : 0 < |a| := abs_pos.mpr ha
  rcases superfactorial_unbounded (4 / c) (by positivity) (C * |a|⁻¹) with ⟨m, hm1, hm⟩
  have hbig : C < |a| * (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ) := by
    have hpos : 0 < |a| := hδ
    have hmain : C * |a|⁻¹ < (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ) := hm
    have hrewrite : C = |a| * (C * |a|⁻¹) := by
      field_simp [ne_of_gt hpos]
    rw [hrewrite]
    calc
      |a| * (C * |a|⁻¹) < |a| * ((4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ)) :=
        mul_lt_mul_of_pos_left hmain hpos
      _ = |a| * (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ) := by ring
  have hsmall : |a| * u m ≤ C * Real.sqrt (m : ℝ) := hbd m hm1
  have hgrow : (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤ u m := hu m hm1
  have hbig' : C < |a| * u m / Real.sqrt (m : ℝ) := by
    have hsqrt : 0 < Real.sqrt (m : ℝ) := by positivity
    have hle : |a| * (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) ≤ |a| * u m := by
      simpa [mul_assoc] using (mul_le_mul_of_nonneg_left hgrow (le_of_lt hδ))
    have hd : C < |a| * (4 / c) ^ (m - 1) * (Nat.factorial m : ℝ) / Real.sqrt (m : ℝ) := hbig
    have hmain' : C < |a| * u m / Real.sqrt (m : ℝ) := by
      exact lt_of_lt_of_le hd (div_le_div_of_nonneg_right hle (le_of_lt hsqrt))
    exact hmain'
  have hsmall' : |a| * u m / Real.sqrt (m : ℝ) ≤ C := by
    exact (div_le_iff₀ (by positivity : 0 < Real.sqrt (m : ℝ))).2 hsmall
  linarith

/-- The even free parameter mu_2 vanishes: growth vs polynomial bound. -/
theorem even_annihilation {c : ℝ} (hc : 0 < c) {a C : ℝ}
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| * StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m
      ≤ C * Real.sqrt (m : ℝ)) : a = 0 := by
  refine superfactorial_annihilate hc
    (u := fun m => StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m) ?_ hbd
  exact even_growth hc

/-- The odd free parameter mu_3 vanishes. -/
theorem odd_annihilation {c : ℝ} (hc : 0 < c) {a C : ℝ}
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| * StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m
      ≤ C * Real.sqrt (m : ℝ)) : a = 0 := by
  refine superfactorial_annihilate hc
    (u := fun m => StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m) ?_ hbd
  exact odd_growth hc

/-! ## H1-moment bound (assumption form)

The analytic Section 5 bound: for w in H^1 the H1-moments satisfy
|M_k| <= C * sqrt k for a constant C = C(c, ||w||_H1).  The full derivation
from the H1 inner product (Cauchy-Schwarz) is the analytic companion; here
we state the concrete bound assumptions used by the annihilation step and
package the complete orthogonality -> all-moments-zero theorem.
-/

/-- Orthogonality against {K_c p_n} in the H1 inner product, together with the
polynomial H1-moment bound, forces all H1-moments of the functional to
vanish. -/
theorem all_moments_zero_of_orthogonal {M : Polynomial ℝ →ₗ[ℝ] ℝ} {c : ℝ} (hc : 0 < c)
    (h0 : moments M 0 = 0) (h1 : moments M 1 = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n → M (Completeness.KcR c (Completeness.pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n → M (Completeness.KcR c (Completeness.pOddR n)) = 0)
    (hC : ℝ)
    (hbdE : ∀ m : ℕ, 1 ≤ m → |moments M (2 * m)| ≤ hC * Real.sqrt (m : ℝ))
    (hbdO : ∀ m : ℕ, 1 ≤ m → |moments M (2 * m + 1)| ≤ hC * Real.sqrt (m : ℝ)) :
    ∀ k : ℕ, moments M k = 0 := by
  have hcne : c ≠ 0 := ne_of_gt hc
  have hscalE := even_moment_scaling M hcne h0 horthE
  have hscalO := odd_moment_scaling M hcne h1 horthO
  have hbdE' : ∀ m : ℕ, 1 ≤ m →
      |moments M 2| * StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m
        ≤ hC * Real.sqrt (m : ℝ) := by
    intro m hm
    have hsc := hscalE m
    have hbdm := hbdE m hm
    rw [hsc] at hbdm
    have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c (Completeness.AR c) (Completeness.BR) m := by
      exact StabilityGrowth.u_nonneg (K := ℝ) (c0 := c) (A := Completeness.AR c) (B := Completeness.BR)
        hc (fun n hn => Completeness.BR_nonneg hn)
        (fun n hn => Completeness.AR_sub_BR_ge_c c (le_of_lt hc) hn) (j := m) hm
    rw [abs_mul, abs_of_nonneg hu0] at hbdm
    exact hbdm
  have hμ2 : moments M 2 = 0 :=
    even_annihilation hc hbdE'
  have hbdO' : ∀ m : ℕ, 1 ≤ m →
      |moments M 3| * StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m
        ≤ hC * Real.sqrt (m : ℝ) := by
    intro m hm
    have hsc := hscalO m
    have hbdm := hbdO m hm
    rw [hsc] at hbdm
    have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c (Completeness.A'R c) (Completeness.B'R) m := by
      exact StabilityGrowth.u_nonneg (K := ℝ) (c0 := c) (A := Completeness.A'R c) (B := Completeness.B'R)
        hc (fun n hn => Completeness.B'R_nonneg hn)
        (fun n hn => Completeness.A'R_sub_B'R_ge_c c (le_of_lt hc) hn) (j := m) hm
    rw [abs_mul, abs_of_nonneg hu0] at hbdm
    exact hbdm
  have hμ3 : moments M 3 = 0 :=
    odd_annihilation hc hbdO'
  intro k
  rcases Nat.even_or_odd k with ⟨m, rfl⟩ | ⟨m, rfl⟩
  · rw [← two_mul m, hscalE m, hμ2]
    simp
  · rw [hscalO m, hμ3]
    simp

end H3Completeness

end SL
