import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

open scoped BigOperators

namespace SL.AuditRound3

noncomputable def recurrence_solution (c : ℝ) (A B : ℕ → ℝ) : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | n + 2 =>
      (A (n + 2) * recurrence_solution c A B (n + 1) -
        B (n + 2) * recurrence_solution c A B n) / c

def solves_recurrence (c : ℝ) (A B u : ℕ → ℝ) : Prop :=
  u 0 = 0 ∧ u 1 = 1 ∧
    ∀ n : ℕ, c * u (n + 2) = A (n + 2) * u (n + 1) - B (n + 2) * u n

noncomputable def epsilon (c : ℝ) (A B : ℕ → ℝ) (n : ℕ) : ℝ :=
  (A n - B n - c) / c

noncomputable def product_bound (c : ℝ) (A B : ℕ → ℝ) (n : ℕ) : ℝ :=
  ∏ k ∈ Finset.Icc 2 n, (A k - B k) / c

theorem recurrence_solution_solves {c : ℝ} (hc : c ≠ 0) (A B : ℕ → ℝ) :
    solves_recurrence c A B (recurrence_solution c A B) := by
  refine ⟨rfl, rfl, ?_⟩
  intro n
  rw [recurrence_solution]
  field_simp

theorem recurrence_solution_unique {c : ℝ} {A B u : ℕ → ℝ}
    (hc : c ≠ 0) (hu : solves_recurrence c A B u) :
    ∀ n : ℕ, u n = recurrence_solution c A B n := by
  intro n
  induction n using Nat.twoStepInduction with
  | zero => exact hu.1
  | one => exact hu.2.1
  | more n h0 h1 =>
      rw [recurrence_solution, ← h0, ← h1]
      apply (eq_div_iff hc).2
      simpa [mul_comm] using hu.2.2 n

theorem second_order_decomposition {c A B v w z : ℝ}
    (hc : c ≠ 0) (hrec : c * z = A * v - B * w) :
    z = (1 + (A - B - c) / c) * v + B / c * (v - w) := by
  field_simp
  nlinarith [hrec]

theorem second_order_lower_bound {c A B v w z : ℝ}
    (hc : 0 < c) (hB : 0 ≤ B) (hmono : w ≤ v)
    (hrec : c * z = A * v - B * w) :
    (A - B) / c * v ≤ z := by
  rw [div_mul_eq_mul_div₀]
  apply (div_le_iff₀ hc).2
  have hterm : 0 ≤ B * (v - w) := mul_nonneg hB (sub_nonneg.mpr hmono)
  nlinarith [hrec]

theorem second_order_exact_iff {c A B v w z : ℝ}
    (hc : c ≠ 0) (hrec : c * z = A * v - B * w) :
    z = (A - B) / c * v ↔ B = 0 ∨ v = w := by
  rw [div_mul_eq_mul_div₀, eq_div_iff hc]
  constructor
  · intro h
    have hz : B * (v - w) = 0 := by nlinarith [hrec]
    simpa only [mul_eq_zero, sub_eq_zero] using hz
  · rintro (h | h)
    · subst B
      nlinarith [hrec]
    · subst w
      nlinarith [hrec]

theorem recurrence_monotone_nonnegative {c : ℝ} {A B u : ℕ → ℝ}
    (hc : 0 < c) (hu : solves_recurrence c A B u)
    (hB : ∀ n : ℕ, 2 ≤ n → 0 ≤ B n)
    (hAB : ∀ n : ℕ, 2 ≤ n → c ≤ A n - B n) :
    ∀ n : ℕ, 0 ≤ u n ∧ u n ≤ u (n + 1) := by
  intro n
  induction n with
  | zero => simp [hu.1, hu.2.1]
  | succ n ih =>
      have hv : 0 ≤ u (n + 1) := ih.1.trans ih.2
      have hb := hB (n + 2) (by omega)
      have hab := hAB (n + 2) (by omega)
      have h1 := mul_nonneg hb (sub_nonneg.mpr ih.2)
      have h2 := mul_nonneg (sub_nonneg.mpr hab) hv
      have hr := hu.2.2 n
      refine ⟨hv, ?_⟩
      change u (n + 1) ≤ u (n + 2)
      nlinarith

theorem recurrence_product_lower_bound {c : ℝ} {A B u : ℕ → ℝ}
    (hc : 0 < c) (hu : solves_recurrence c A B u)
    (hB : ∀ n : ℕ, 2 ≤ n → 0 ≤ B n)
    (hAB : ∀ n : ℕ, 2 ≤ n → c ≤ A n - B n)
    (n : ℕ) (hn : 1 ≤ n) : product_bound c A B n ≤ u n := by
  have hm := recurrence_monotone_nonnegative hc hu hB hAB
  induction n, hn using Nat.le_induction with
  | base => simp [product_bound, hu.2.1]
  | succ n hn ih =>
      have hk : 2 ≤ n + 1 := by omega
      have hrec : c * u (n + 1) = A (n + 1) * u n - B (n + 1) * u (n - 1) := by
        simpa [Nat.sub_add_cancel hn, show n - 1 + 2 = n + 1 by omega] using hu.2.2 (n - 1)
      have hmono : u (n - 1) ≤ u n := by
        simpa [Nat.sub_add_cancel hn] using (hm (n - 1)).2
      have hstep := second_order_lower_bound hc (hB (n + 1) hk) hmono hrec
      have hfactor : 0 ≤ (A (n + 1) - B (n + 1)) / c :=
        div_nonneg (hc.le.trans (hAB (n + 1) hk)) hc.le
      unfold product_bound at *
      rw [Finset.prod_Icc_succ_top hk]
      exact (mul_le_mul_of_nonneg_right ih hfactor).trans (by simpa [mul_comm] using hstep)

theorem recurrence_product_eq_of_B_zero {c : ℝ} {A B u : ℕ → ℝ}
    (hc : c ≠ 0) (hu : solves_recurrence c A B u)
    (hB : ∀ n : ℕ, 2 ≤ n → B n = 0)
    (n : ℕ) (hn : 1 ≤ n) : u n = product_bound c A B n := by
  induction n, hn using Nat.le_induction with
  | base => simp [product_bound, hu.2.1]
  | succ n hn ih =>
      have hk : 2 ≤ n + 1 := by omega
      have hrec : c * u (n + 1) = A (n + 1) * u n - B (n + 1) * u (n - 1) := by
        simpa [Nat.sub_add_cancel hn, show n - 1 + 2 = n + 1 by omega] using hu.2.2 (n - 1)
      have hstep := (second_order_exact_iff hc hrec).2 (Or.inl (hB (n + 1) hk))
      rw [hstep, ih]
      unfold product_bound
      rw [Finset.prod_Icc_succ_top hk]
      ring

theorem product_bound_eq_epsilon {c : ℝ} (hc : c ≠ 0) (A B : ℕ → ℝ) (n : ℕ) :
    product_bound c A B n = ∏ k ∈ Finset.Icc 2 n, (1 + epsilon c A B k) := by
  apply Finset.prod_congr rfl
  intro k _
  unfold epsilon
  field_simp
  ring

noncomputable def exponential_sequence (n : ℕ) : ℝ := (2 : ℝ) ^ n - 1

theorem exponential_sequence_solves :
    solves_recurrence 1 (fun _ => 3) (fun _ => 2) exponential_sequence := by
  refine ⟨by norm_num [exponential_sequence], by norm_num [exponential_sequence], ?_⟩
  intro n
  simp only [exponential_sequence, pow_add, pow_one]
  ring

theorem constant_recurrence_solution (n : ℕ) :
    recurrence_solution 1 (fun _ => 3) (fun _ => 2) n = (2 : ℝ) ^ n - 1 := by
  exact (recurrence_solution_unique (by norm_num) exponential_sequence_solves n).symm

theorem constant_recurrence_parameters :
    (0 : ℝ) < 1 ∧ (∀ n : ℕ, 2 ≤ n → (0 : ℝ) ≤ 2) ∧
    (∀ n : ℕ, 2 ≤ n → (1 : ℝ) ≤ 3 - 2) ∧
    (∀ n : ℕ, epsilon 1 (fun _ => 3) (fun _ => 2) n = 0) := by
  norm_num [epsilon]

theorem constant_recurrence_product (n : ℕ) :
    product_bound 1 (fun _ => 3) (fun _ => 2) n = 1 := by
  norm_num [product_bound]

theorem constant_recurrence_strict_gap (n : ℕ) :
    product_bound 1 (fun _ => 3) (fun _ => 2) (n + 2) <
      recurrence_solution 1 (fun _ => 3) (fun _ => 2) (n + 2) := by
  rw [constant_recurrence_product, constant_recurrence_solution]
  have hpow : (1 : ℝ) ≤ 2 ^ n := one_le_pow₀ (by norm_num)
  rw [pow_add]
  norm_num
  nlinarith

theorem no_general_product_equality :
    ¬ (∀ n : ℕ, 1 ≤ n → recurrence_solution 1 (fun _ => 3) (fun _ => 2) n =
      product_bound 1 (fun _ => 3) (fun _ => 2) n) := by
  intro h
  exact (ne_of_gt (constant_recurrence_strict_gap 0)) (h 2 (by omega))

noncomputable def perturbed_A (m c delta : ℝ) : ℝ :=
  2 * m * (2 * m - 1) + c * (m / (m - 1) + delta)

noncomputable def perturbed_B (m delta : ℝ) : ℝ :=
  (m / (m - 1) + delta) * (2 * m - 2) * (2 * m - 3)

theorem perturbed_coefficient_difference (m c delta : ℝ) (hm : m ≠ 1) :
    perturbed_A m c delta - perturbed_B m delta =
      4 * m + c * m / (m - 1) + delta * (c - (2 * m - 2) * (2 * m - 3)) := by
  unfold perturbed_A perturbed_B
  have hden : m - 1 ≠ 0 := sub_ne_zero.mpr hm
  field_simp
  ring

theorem perturbed_m4_values :
    perturbed_A 4 3 1 = 63 ∧ perturbed_B 4 1 = 70 ∧
      perturbed_A 4 3 1 - perturbed_B 4 1 = -7 := by
  norm_num [perturbed_A, perturbed_B]

theorem old_m4_expression :
    4 * (4 : ℝ) + 3 * 4 / (4 - 1) + 3 * 1 = 23 := by
  norm_num

theorem perturbed_m4_rejects_old_expression :
    perturbed_A 4 3 1 - perturbed_B 4 1 ≠
      4 * (4 : ℝ) + 3 * 4 / (4 - 1) + 3 * 1 := by
  norm_num [perturbed_A, perturbed_B]

noncomputable def p2_moment_formula (m : ℝ) : ℝ :=
  4 * m / ((2 * m + 1) * (2 * m + 3))

noncomputable def p2_image_moment_formula (m : ℝ) : ℝ :=
  -(4 * m * (4 * m ^ 2 + 2 * m - 9)) / ((2 * m + 1) * (2 * m + 3))

noncomputable def p2_delta_formula (m : ℝ) : ℝ :=
  6 * m * (2 * m + 5) / ((m - 1) * (2 * m + 3) * (4 * m ^ 2 - 6 * m - 7))

theorem p2_moment_rational_identity (m : ℝ)
    (h1 : 2 * m + 1 ≠ 0) (h3 : 2 * m + 3 ≠ 0) :
    3 / (2 * m + 3) - 1 / (2 * m + 1) = p2_moment_formula m := by
  unfold p2_moment_formula
  field_simp
  ring

theorem p2_image_moment_rational_identity (m : ℝ)
    (h0 : 2 * m - 1 ≠ 0) (h1 : 2 * m + 1 ≠ 0) (h3 : 2 * m + 3 ≠ 0) :
    3 * p2_moment_formula m - 2 * m * (2 * m - 1) * p2_moment_formula (m - 1) =
      p2_image_moment_formula m := by
  unfold p2_moment_formula p2_image_moment_formula
  have hprev1 : 2 * (m - 1) + 1 = 2 * m - 1 := by ring
  have hprev3 : 2 * (m - 1) + 3 = 2 * m + 1 := by ring
  rw [hprev1, hprev3]
  field_simp (disch := first | assumption |
    exact fun hz => h0 (by nlinarith [hz]) |
    exact fun hz => h1 (by nlinarith [hz]) |
    exact fun hz => h3 (by nlinarith [hz]))
  ring

theorem p2_perturbation_cancellation (m : ℝ)
    (hm : m - 1 ≠ 0) (h0 : 2 * m - 1 ≠ 0) (h1 : 2 * m + 1 ≠ 0)
    (h3 : 2 * m + 3 ≠ 0) (hq : 4 * m ^ 2 - 6 * m - 7 ≠ 0) :
    p2_image_moment_formula m - (m / (m - 1) + p2_delta_formula m) *
      p2_image_moment_formula (m - 1) = 0 := by
  unfold p2_image_moment_formula p2_delta_formula
  have hprev1 : 2 * (m - 1) + 1 = 2 * m - 1 := by ring
  have hprev3 : 2 * (m - 1) + 3 = 2 * m + 1 := by ring
  rw [hprev1, hprev3]
  field_simp (disch := first | assumption |
    exact fun hz => h0 (by nlinarith [hz]) |
    exact fun hz => h1 (by nlinarith [hz]) |
    exact fun hz => h3 (by nlinarith [hz]) |
    exact fun hz => hq (by nlinarith [hz]))
  ring

theorem p2_delta_complement (m : ℝ)
    (hm : m - 1 ≠ 0) (h3 : 2 * m + 3 ≠ 0) (hq : 4 * m ^ 2 - 6 * m - 7 ≠ 0) :
    1 - p2_delta_formula m =
      (m - 3) * (2 * m - 1) * (4 * m ^ 2 + 10 * m + 7) /
        ((m - 1) * (2 * m + 3) * (4 * m ^ 2 - 6 * m - 7)) := by
  unfold p2_delta_formula
  field_simp (disch := first | assumption |
    exact fun hz => h3 (by nlinarith [hz]) |
    exact fun hz => hq (by nlinarith [hz]))
  ring

theorem p2_delta_special_values : p2_delta_formula 2 = -36 / 7 ∧ p2_delta_formula 3 = 1 := by
  norm_num [p2_delta_formula]

end SL.AuditRound3
