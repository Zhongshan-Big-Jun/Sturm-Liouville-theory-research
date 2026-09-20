import SL.ThirdOrderClosedForms
import SL.ThirdOrderMinimal

namespace SL.AuditRound4

open ThirdOrder ThirdOrderClosedForms ThirdOrderMinimal

set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

variable {K : Type*} [Field K]

def second_difference (v : ℕ → K) (n : ℕ) : K :=
  v (n + 2) - 2 * v (n + 1) + v n

theorem recurrence_iff_second_difference (t v : ℕ → K) :
    IsSolution (fun j => 2 + t j) (fun j => -(1 + 2 * t j)) t v ↔
      ∀ n, second_difference v (n + 1) = t (n + 3) * second_difference v n := by
  constructor <;> intro h n
  · have hn := h n
    dsimp [second_difference]
    simp only [Nat.add_assoc] at *
    linear_combination hn
  · have hn := h n
    dsimp [second_difference] at hn
    simp only [Nat.add_assoc] at *
    try dsimp
    linear_combination hn

theorem affine_second_difference (A B : K) (n : ℕ) :
    second_difference (fun j => A + B * (j : K)) n = 0 := by
  simp only [second_difference, Nat.cast_add, Nat.cast_ofNat]
  ring

theorem affine_solution (t : ℕ → K) (A B : K) :
    IsSolution (fun j => 2 + t j) (fun j => -(1 + 2 * t j)) t
      (fun j => A + B * (j : K)) := by
  apply (recurrence_iff_second_difference t _).mpr
  intro n
  rw [affine_second_difference, affine_second_difference, mul_zero]

theorem zero_second_difference_iff_affine (v : ℕ → K) :
    (∀ n, second_difference v n = 0) ↔
      ∀ n, v n = v 0 + (v 1 - v 0) * (n : K) := by
  constructor
  · intro h n
    induction n using Nat.twoStepInduction with
    | zero => simp
    | one => simp
    | more n ih0 ih1 =>
      have hn := h n
      dsimp [second_difference] at hn
      rw [ih0, ih1] at hn
      push_cast at *
      linear_combination hn
  · intro h n
    dsimp [second_difference]
    rw [h (n + 2), h (n + 1), h n]
    push_cast
    ring

theorem difference_proportional {t v a : ℕ → K}
    (hv : ∀ n, second_difference v (n + 1) = t (n + 3) * second_difference v n)
    (ha : ∀ n, a (n + 1) = t (n + 3) * a n) (ha0 : a 0 ≠ 0) :
    ∀ n, second_difference v n = (second_difference v 0 / a 0) * a n := by
  intro n
  induction n with
  | zero => field_simp
  | succ n ih =>
    rw [hv, ha, ih]
    ring

theorem first_difference_sum (v : ℕ → K) (n : ℕ) :
    v (n + 1) - v n = v 1 - v 0 + ∑ k ∈ Finset.range n, second_difference v k := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ]
    dsimp [second_difference] at ih ⊢
    simp only [Nat.add_assoc]
    linear_combination ih

theorem reconstruct_second_difference (v : ℕ → K) (n : ℕ) :
    v n = v 0 + (v 1 - v 0) * (n : K) +
      ∑ i ∈ Finset.range n, ∑ k ∈ Finset.range i, second_difference v k := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ]
    push_cast
    have h := first_difference_sum v n
    linear_combination ih + h

theorem reduction_residual_identity {a1 a2 a3 E : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (r : ℕ → K) (n : ℕ) :
    E (n + 3) * r (n + 3) -
      (a1 (n + 3) * (E (n + 2) * r (n + 2)) +
       a2 (n + 3) * (E (n + 1) * r (n + 1)) + a3 (n + 3) * (E n * r n)) =
    E (n + 3) * (r (n + 3) - r (n + 2)) +
      (a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) *
        (r (n + 2) - r (n + 1)) +
      a3 (n + 3) * E n * (r (n + 1) - r n) := by
  rw [hE n]
  ring

theorem reduction_product_iff {a1 a2 a3 E : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (r : ℕ → K) :
    IsSolution a1 a2 a3 (fun j => E j * r j) ↔
      ∀ n, E (n + 3) * (r (n + 3) - r (n + 2)) +
        (a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) *
          (r (n + 2) - r (n + 1)) +
        a3 (n + 3) * E n * (r (n + 1) - r n) = 0 := by
  constructor <;> intro h n
  · rw [← reduction_residual_identity hE r n]
    exact sub_eq_zero.mpr (h n)
  · apply sub_eq_zero.mp
    rw [reduction_residual_identity hE r n]
    exact h n

theorem reduction_iff {a1 a2 a3 E z : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j, E j ≠ 0) :
    IsSolution a1 a2 a3 z ↔
      IsSolution2 (Acoef a2 a3 E) (Bcoef a3 E)
        (fun j => z j / E j - z (j - 1) / E (j - 1)) := by
  constructor
  · exact reduction_named hE hEnz
  · intro hs
    have hprod : IsSolution a1 a2 a3 (fun j => E j * (z j / E j)) := by
      apply (reduction_product_iff hE _).mpr
      intro n
      have hn := hs n
      change z (n + 3) / E (n + 3) - z (n + 2) / E (n + 2) =
        (-(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) / E (n + 3)) *
          (z (n + 2) / E (n + 2) - z (n + 1) / E (n + 1)) +
        (- (a3 (n + 3) * E n) / E (n + 3)) *
          (z (n + 1) / E (n + 1) - z n / E n) at hn
      have hc := congrArg (fun x => E (n + 3) * x) hn
      field_simp [hEnz] at hc ⊢
      linear_combination hc
    simpa only [mul_div_cancel₀ _ (hEnz _)] using hprod

def integrate_from_zero (r0 : K) (s : ℕ → K) (j : ℕ) : K :=
  withInitial (r0 + s 1) s j

theorem integrate_initial (r0 : K) (s : ℕ → K) :
    integrate_from_zero r0 s 0 = r0 ∧
    integrate_from_zero r0 s 1 = r0 + s 1 ∧
    integrate_from_zero r0 s 2 = r0 + s 1 + s 2 := by
  simp [integrate_from_zero, withInitial, Finset.sum_range_succ]
  <;> constructor <;> ring

theorem integrate_increment (r0 : K) (s : ℕ → K) (j : ℕ) :
    integrate_from_zero r0 s (j + 1) - integrate_from_zero r0 s j = s (j + 1) := by
  rw [integrate_from_zero, withInitial_succ]
  simp [integrate_from_zero]

theorem reduction_reconstruction {a1 a2 a3 E : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j, E j ≠ 0)
    {s : ℕ → K} (hs : IsSolution2 (Acoef a2 a3 E) (Bcoef a3 E) s) (r0 : K) :
    IsSolution a1 a2 a3 (fun j => E j * integrate_from_zero r0 s j) ∧
    (fun j => E j * integrate_from_zero r0 s j) 0 = E 0 * r0 ∧
    ∀ j, (E (j + 1) * integrate_from_zero r0 s (j + 1)) / E (j + 1) -
      (E j * integrate_from_zero r0 s j) / E j = s (j + 1) := by
  refine ⟨reduction_converse hE hEnz hs (r0 + s 1), ?_, ?_⟩
  · change E 0 * integrate_from_zero r0 s 0 = E 0 * r0
    rw [(integrate_initial r0 s).1]
  · intro j
    simp only [mul_div_cancel_left₀ _ (hEnz _)]
    exact integrate_increment r0 s j

noncomputable def p (ε : ℕ) (c : ℚ) (j : ℕ) : ℚ :=
  if ε = 0 then PEven c j else POdd c j

noncomputable def q (ε : ℕ) (c : ℚ) (j : ℕ) : ℚ :=
  if ε = 0 then QEven c j else QOdd c j

noncomputable def r (ε : ℕ) (c : ℚ) (j : ℕ) : ℚ :=
  if ε = 0 then REven c j else ROdd c j

def theta (ε : ℕ) (c : ℚ) (j : ℕ) : ℚ :=
  c / (2 * ((j : ℚ) - 1) * (2 * (j : ℚ) + 2 * ε - 1))

def factorial_step (ε j : ℕ) : ℚ :=
  (2 * (j : ℚ) + ε) * (2 * (j : ℚ) + ε - 1)

def factorial_weight (ε j : ℕ) : ℚ := (Nat.factorial (2 * j + ε) : ℚ)

theorem factorial_weight_ne_zero (ε j : ℕ) : factorial_weight ε j ≠ 0 := by
  unfold factorial_weight
  exact_mod_cast Nat.factorial_ne_zero (2 * j + ε)

theorem factorial_weight_succ (ε n : ℕ) :
    factorial_weight ε (n + 1) = factorial_step ε (n + 1) * factorial_weight ε n := by
  unfold factorial_weight factorial_step
  rw [show 2 * (n + 1) + ε = (2 * n + ε + 1) + 1 by omega]
  rw [Nat.factorial_succ, Nat.factorial_succ]
  push_cast
  ring

theorem factorial_step_ne_zero (ε n : ℕ) : factorial_step ε (n + 1) ≠ 0 := by
  have h := factorial_weight_ne_zero ε (n + 1)
  rw [factorial_weight_succ] at h
  exact (mul_ne_zero_iff.mp h).1

theorem parity_coefficient_factors (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (n : ℕ) :
    p ε c (n + 3) / (c * factorial_step ε (n + 3)) = 2 + theta ε c (n + 3) ∧
    q ε c (n + 3) / (factorial_step ε (n + 3) * factorial_step ε (n + 2)) =
      1 + 2 * theta ε c (n + 3) ∧
    c * r ε c (n + 3) /
      (factorial_step ε (n + 3) * factorial_step ε (n + 2) * factorial_step ε (n + 1)) =
      theta ε c (n + 3) := by
  have hn : 0 ≤ (n : ℚ) := Nat.cast_nonneg n
  rcases hε with rfl | rfl <;>
    norm_num only [p, q, r, PEven, QEven, REven, POdd, QOdd, ROdd, theta,
      factorial_step, Nat.cast_add, Nat.cast_ofNat, if_true, if_false] at *
  all_goals
    refine ⟨?_, ?_, ?_⟩
    all_goals
      ring_nf
      field_simp [hc]
      <;> ring


def scale_factor (ε : ℕ) (c : ℚ) (j : ℕ) : ℚ :=
  c ^ j / factorial_weight ε j

def scaled_sequence (ε : ℕ) (c : ℚ) (μ : ℕ → ℚ) (j : ℕ) : ℚ :=
  scale_factor ε c j * μ j

def moment_solution (ε : ℕ) (c : ℚ) (μ : ℕ → ℚ) : Prop :=
  ∀ n, c ^ 2 * μ (n + 3) = p ε c (n + 3) * μ (n + 2) -
    q ε c (n + 3) * μ (n + 1) + r ε c (n + 3) * μ n

theorem scale_factor_ne_zero (ε : ℕ) {c : ℚ} (hc : c ≠ 0) (j : ℕ) :
    scale_factor ε c j ≠ 0 :=
  div_ne_zero (pow_ne_zero j hc) (factorial_weight_ne_zero ε j)

theorem scale_factor_succ (ε : ℕ) (c : ℚ) (n : ℕ) :
    scale_factor ε c (n + 1) =
      c / factorial_step ε (n + 1) * scale_factor ε c n := by
  unfold scale_factor
  rw [pow_succ, factorial_weight_succ]
  ring

theorem conjugate_solution_iff (a1 a2 a3 w z : ℕ → K) (hw : ∀ j, w j ≠ 0) :
    IsSolution a1 a2 a3 z ↔
      IsSolution (fun j => w j * a1 j / w (j - 1))
        (fun j => w j * a2 j / w (j - 2))
        (fun j => w j * a3 j / w (j - 3)) (fun j => w j * z j) := by
  constructor <;> intro h n
  · change w (n + 3) * z (n + 3) =
      w (n + 3) * a1 (n + 3) / w (n + 2) * (w (n + 2) * z (n + 2)) +
      w (n + 3) * a2 (n + 3) / w (n + 1) * (w (n + 1) * z (n + 1)) +
      w (n + 3) * a3 (n + 3) / w n * (w n * z n)
    rw [h n]
    field_simp [hw]
    <;> ring
  · have hn := h n
    change w (n + 3) * z (n + 3) =
      w (n + 3) * a1 (n + 3) / w (n + 2) * (w (n + 2) * z (n + 2)) +
      w (n + 3) * a2 (n + 3) / w (n + 1) * (w (n + 1) * z (n + 1)) +
      w (n + 3) * a3 (n + 3) / w n * (w n * z n) at hn
    field_simp [hw] at hn
    try dsimp
    exact hn

theorem scaled_coefficients (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (n : ℕ) :
    scale_factor ε c (n + 3) * (p ε c (n + 3) / c ^ 2) /
      scale_factor ε c (n + 2) = 2 + theta ε c (n + 3) ∧
    scale_factor ε c (n + 3) * (-q ε c (n + 3) / c ^ 2) /
      scale_factor ε c (n + 1) = -(1 + 2 * theta ε c (n + 3)) ∧
    scale_factor ε c (n + 3) * (r ε c (n + 3) / c ^ 2) /
      scale_factor ε c n = theta ε c (n + 3) := by
  obtain ⟨hp, hq, hr⟩ := parity_coefficient_factors ε hε c hc n
  have h1 := scale_factor_succ ε c n
  have h2 := scale_factor_succ ε c (n + 1)
  have h3 := scale_factor_succ ε c (n + 2)
  simp only [Nat.add_assoc] at h1 h2 h3
  have hw := scale_factor_ne_zero ε hc
  have hf := factorial_step_ne_zero ε
  refine ⟨?_, ?_, ?_⟩
  · rw [h3, ← hp]
    field_simp [hc, hw, hf]
    <;> ring
  · rw [h3, h2, ← hq]
    field_simp [hc, hw, hf]
    <;> ring
  · rw [h3, h2, h1, ← hr]
    field_simp [hc, hw, hf]
    <;> ring

theorem moment_iff_normalized (ε : ℕ) (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) :
    moment_solution ε c μ ↔
      IsSolution (fun j => p ε c j / c ^ 2)
        (fun j => -q ε c j / c ^ 2) (fun j => r ε c j / c ^ 2) μ := by
  constructor <;> intro h n
  · have hn := h n
    try dsimp
    apply (mul_left_cancel₀ (pow_ne_zero 2 hc))
    field_simp
    linear_combination hn
  · have hn := h n
    dsimp at hn
    try dsimp
    field_simp at hn
    linear_combination hn

theorem moment_iff_scaled (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) :
    moment_solution ε c μ ↔
      IsSolution (fun j => 2 + theta ε c j) (fun j => -(1 + 2 * theta ε c j))
        (theta ε c) (scaled_sequence ε c μ) := by
  rw [moment_iff_normalized ε c hc μ,
    conjugate_solution_iff _ _ _ (scale_factor ε c) μ (scale_factor_ne_zero ε hc)]
  constructor <;> intro h n
  · have hn := h n
    change _ = _
    simpa only [show n + 3 - 1 = n + 2 by omega,
      show n + 3 - 2 = n + 1 by omega, show n + 3 - 3 = n by omega,
      scaled_sequence, (scaled_coefficients ε hε c hc n).1,
      (scaled_coefficients ε hε c hc n).2.1,
      (scaled_coefficients ε hε c hc n).2.2] using hn
  · have hn := h n
    change _ = _
    simpa only [show n + 3 - 1 = n + 2 by omega,
      show n + 3 - 2 = n + 1 by omega, show n + 3 - 3 = n by omega,
      scaled_sequence, (scaled_coefficients ε hε c hc n).1,
      (scaled_coefficients ε hε c hc n).2.1,
      (scaled_coefficients ε hε c hc n).2.2] using hn

theorem moment_iff_second_difference (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) :
    moment_solution ε c μ ↔ ∀ n,
      second_difference (scaled_sequence ε c μ) (n + 1) =
        theta ε c (n + 3) * second_difference (scaled_sequence ε c μ) n := by
  rw [moment_iff_scaled ε hε c hc μ, recurrence_iff_second_difference]

def difference_weight (ε : ℕ) (c : ℚ) (n : ℕ) : ℚ :=
  ((n : ℚ) + 2) * scale_factor ε c (n + 2)

theorem difference_weight_ne_zero (ε : ℕ) (c : ℚ) (hc : c ≠ 0) (n : ℕ) :
    difference_weight ε c n ≠ 0 := by
  unfold difference_weight
  apply mul_ne_zero
  · positivity
  · exact scale_factor_ne_zero ε hc _

theorem difference_weight_recurrence (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (n : ℕ) :
    difference_weight ε c (n + 1) = theta ε c (n + 3) * difference_weight ε c n := by
  unfold difference_weight
  simp only [Nat.cast_add, Nat.cast_one, Nat.add_assoc]
  rw [scale_factor_succ ε c (n + 2)]
  have hn : 0 ≤ (n : ℚ) := Nat.cast_nonneg n
  rcases hε with rfl | rfl <;>
    unfold theta factorial_step <;> push_cast
  all_goals
    ring_nf
    field_simp
    <;> ring

theorem moment_difference_formula (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) (hμ : moment_solution ε c μ) (n : ℕ) :
    second_difference (scaled_sequence ε c μ) n =
      (second_difference (scaled_sequence ε c μ) 0 / difference_weight ε c 0) *
        difference_weight ε c n := by
  exact difference_proportional ((moment_iff_second_difference ε hε c hc μ).mp hμ)
    (difference_weight_recurrence ε hε c) (difference_weight_ne_zero ε c hc 0) n

theorem moment_finite_reconstruction (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) (hμ : moment_solution ε c μ) (n : ℕ) :
    scaled_sequence ε c μ n = scaled_sequence ε c μ 0 +
      (scaled_sequence ε c μ 1 - scaled_sequence ε c μ 0) * (n : ℚ) +
      ∑ i ∈ Finset.range n, ∑ k ∈ Finset.range i,
        (second_difference (scaled_sequence ε c μ) 0 / difference_weight ε c 0) *
          difference_weight ε c k := by
  rw [reconstruct_second_difference (scaled_sequence ε c μ) n]
  congr 1
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro k hk
  exact moment_difference_formula ε hε c hc μ hμ k

def affine_moment (ε : ℕ) (c A B : ℚ) (j : ℕ) : ℚ :=
  factorial_weight ε j / c ^ j * (A + B * (j : ℚ))

theorem scaled_affine_moment (ε : ℕ) (c A B : ℚ) (hc : c ≠ 0) :
    scaled_sequence ε c (affine_moment ε c A B) = fun j : ℕ => A + B * (j : ℚ) := by
  funext j
  unfold scaled_sequence affine_moment scale_factor
  field_simp [factorial_weight_ne_zero ε j, pow_ne_zero j hc]

theorem affine_moment_solution (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c A B : ℚ) (hc : c ≠ 0) : moment_solution ε c (affine_moment ε c A B) := by
  rw [moment_iff_scaled ε hε c hc, scaled_affine_moment ε c A B hc]
  exact affine_solution _ A B

theorem normalized_solution_with_zero_term (ε : ℕ) (hε : ε = 0 ∨ ε = 1)
    (c : ℚ) (hc : c ≠ 0) :
    moment_solution ε c (affine_moment ε c 1 (-1 / 3)) ∧
    affine_moment ε c 1 (-1 / 3) 0 = 1 ∧
    affine_moment ε c 1 (-1 / 3) 3 = 0 := by
  refine ⟨affine_moment_solution ε hε c 1 (-1 / 3) hc, ?_, ?_⟩
  · rcases hε with rfl | rfl <;> norm_num [affine_moment, factorial_weight]
  · norm_num [affine_moment]

def table_ratio (a b cc d j : ℚ) : ℚ := (j ^ 2 + a * j + b) / (j ^ 2 + cc * j + d)

theorem table_cancellation (τ j : ℚ) (hj : j ≠ 0) (ht : j + τ ≠ 0) :
    table_ratio (τ + 1 / 2) (τ / 2) τ 0 j = 1 + 1 / (2 * j) := by
  unfold table_ratio
  rw [show j ^ 2 + τ * j + 0 = j * (j + τ) by ring]
  field_simp
  <;> ring

theorem missed_table_parameter (j : ℕ) (hj : 1 ≤ j) :
    table_ratio (-1 / 4) (-3 / 8) (-3 / 4) 0 j = 1 + 1 / (2 * (j : ℚ)) := by
  have hq : (1 : ℚ) ≤ j := by exact_mod_cast hj
  have h1 : (j : ℚ) ≠ 0 := by linarith
  have h2 : (j : ℚ) + (-3 / 4) ≠ 0 := by linarith
  convert table_cancellation (-3 / 4) j h1 h2 using 1 <;> norm_num

theorem missed_table_not_in_old_branches :
    (|2 * (-3 / 4 : ℚ) + 1| - 1) / 4 ≠ (-3 / 8 : ℚ) ∧
    -((-3 / 4 : ℚ) + 1) / 2 ≠ (-3 / 8 : ℚ) := by norm_num

def legendre2 (x : K) : K := (3 * x ^ 2 - 1) / 2

def legendre3 (x : K) : K := (5 * x ^ 3 - 3 * x) / 2

theorem low_mode_representative_differences (x a b : K) :
    legendre2 x / a - (legendre2 x - 1) / a = 1 / a ∧
    legendre3 x / b - (legendre3 x - x) / b = x / b := by
  constructor <;> ring

theorem low_mode_difference_nonzero (a b : K) (ha : a ≠ 0) (hb : b ≠ 0) :
    legendre2 0 / a ≠ (legendre2 0 - 1) / a ∧
    legendre3 1 / b ≠ (legendre3 1 - 1) / b := by
  constructor
  · intro h
    have hd := (low_mode_representative_differences 0 a b).1
    rw [h, sub_self] at hd
    exact (one_div_ne_zero ha) hd.symm
  · intro h
    have hd := (low_mode_representative_differences 1 a b).2
    rw [h, sub_self] at hd
    exact (one_div_ne_zero hb) hd.symm

def a4 (c : ℚ) : ℚ := 1 + 15 / c

def a6 (c : ℚ) : ℚ := 1 + 105 / c + 945 / c ^ 2

theorem remainder_identity (c : ℚ) : a6 c - (63 / c) * a4 c = 1 + 42 / c := by
  unfold a4 a6
  by_cases hc : c = 0
  · subst c; norm_num
  · field_simp
    <;> ring

theorem remainder_unbounded_on_reciprocals (M : ℚ) (N : ℕ) :
    ∃ n : ℕ, N < n ∧ 0 < (1 : ℚ) / (n + 1) ∧
      M < a6 (1 / ((n : ℚ) + 1)) -
        (63 / (1 / ((n : ℚ) + 1))) * a4 (1 / ((n : ℚ) + 1)) := by
  obtain ⟨n, hn⟩ := exists_nat_gt (max M (N : ℚ))
  have hM : M < (n : ℚ) := lt_of_le_of_lt (le_max_left _ _) hn
  have hN : (N : ℚ) < (n : ℚ) := lt_of_le_of_lt (le_max_right _ _) hn
  refine ⟨n, by exact_mod_cast hN, by positivity, ?_⟩
  rw [remainder_identity]
  have hpos : 0 ≤ (n : ℚ) := Nat.cast_nonneg n
  have heq : (42 : ℚ) / (1 / ((n : ℚ) + 1)) = 42 * ((n : ℚ) + 1) := by
    field_simp
  rw [heq]
  linarith


noncomputable def even_z_plus (j : ℕ) : ℚ :=
  muEvenPlus 1 j / ((Nat.factorial j : ℚ) ^ 2 * 4 ^ j)

noncomputable def even_z_minus (j : ℕ) : ℚ :=
  muEvenMinus 1 j / ((Nat.factorial j : ℚ) ^ 2 * 4 ^ j)

noncomputable def example_ratio_difference (j : ℕ) : ℚ :=
  even_z_minus j / even_z_plus j - even_z_minus (j - 1) / even_z_plus (j - 1)

noncomputable def printed_reduction_residual : ℚ :=
  a2Even 1 3 * even_z_plus 1 * (example_ratio_difference 3 + example_ratio_difference 2) +
  a3Even 1 3 * even_z_plus 0 *
    (example_ratio_difference 3 + example_ratio_difference 2 + example_ratio_difference 1) -
  even_z_plus 3 * example_ratio_difference 3

theorem printed_reduction_counterexample : printed_reduction_residual = 69 / 224 := by
  norm_num [printed_reduction_residual, example_ratio_difference, even_z_plus, even_z_minus,
    muEvenPlus, muEvenMinus, a2Even, a3Even, QEven, REven, lambda, Nat.factorial]

theorem corrected_reduction_same_data :
    even_z_plus 3 * example_ratio_difference 3 +
      (a2Even 1 3 * even_z_plus 1 + a3Even 1 3 * even_z_plus 0) * example_ratio_difference 2 +
      a3Even 1 3 * even_z_plus 0 * example_ratio_difference 1 = 0 := by
  norm_num [example_ratio_difference, even_z_plus, even_z_minus,
    muEvenPlus, muEvenMinus, a2Even, a3Even, QEven, REven, lambda, Nat.factorial]

end SL.AuditRound4
