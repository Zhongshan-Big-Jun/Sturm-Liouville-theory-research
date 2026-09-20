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
    dsimp
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
  <;> ring

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
  · rw [(integrate_initial r0 s).1]
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
  have h0 : (n : ℚ) + 1 ≠ 0 := by linarith
  have h1 : (n : ℚ) + 2 ≠ 0 := by linarith
  have h2 : (n : ℚ) + 3 ≠ 0 := by linarith
  have h3 : 2 * ((n : ℚ) + 3) - 1 ≠ 0 := by linarith
  have h4 : 2 * ((n : ℚ) + 3) + 1 ≠ 0 := by linarith
  have hs1 := factorial_step_ne_zero ε n
  have hs2 := factorial_step_ne_zero ε (n + 1)
  have hs3 := factorial_step_ne_zero ε (n + 2)
  rcases hε with rfl | rfl <;>
    simp only [p, q, r, PEven, QEven, REven, POdd, QOdd, ROdd, theta,
      factorial_step, Nat.cast_add, Nat.cast_ofNat, Nat.cast_zero, Nat.cast_one,
      if_pos, if_neg, zero_ne_one, one_ne_zero, mul_zero, mul_one, add_zero] at *
  all_goals
    refine ⟨?_, ?_, ?_⟩
    all_goals
      field_simp
      <;> ring

end SL.AuditRound4
