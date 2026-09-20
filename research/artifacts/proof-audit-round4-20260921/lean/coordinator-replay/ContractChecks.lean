import SL.AuditRound4
import Lean

open SL.AuditRound4 SL.ThirdOrderClosedForms SL.ThirdOrder

open Lean Elab Command in
run_cmd do
  let P ← findOLean `SL.AuditRound4
  logInfo m!"CONTRACT_ROOT={P}"

example (ε : ℕ) (hε : ε = 0 ∨ ε = 1) (c : ℚ) (j : ℕ) :
    p ε c j = 4 * c * (j : ℚ) * (2 * (j : ℚ) + 2 * ε - 1) +
      c ^ 2 * (j : ℚ) / ((j : ℚ) - 1) ∧
    q ε c j = 4 * (j : ℚ) * ((j : ℚ) - 1) *
      (2 * (j : ℚ) + 2 * ε - 1) * (2 * (j : ℚ) + 2 * ε - 3) +
        4 * c * (j : ℚ) * (2 * (j : ℚ) + 2 * ε - 3) ∧
    r ε c j = 4 * (j : ℚ) * ((j : ℚ) - 2) *
      (2 * (j : ℚ) + 2 * ε - 3) * (2 * (j : ℚ) + 2 * ε - 5) := by
  rcases hε with rfl | rfl <;>
    norm_num only [p, q, r, PEven, QEven, REven, POdd, QOdd, ROdd,
      Nat.cast_ofNat, if_true, if_false]
  all_goals exact ⟨by ring, by ring, by ring⟩

example (ε : ℕ) (hε : ε = 0 ∨ ε = 1) (c : ℚ) (hc : c ≠ 0) (μ : ℕ → ℚ) :
    (∀ n, c ^ 2 * μ (n + 3) = p ε c (n + 3) * μ (n + 2) -
      q ε c (n + 3) * μ (n + 1) + r ε c (n + 3) * μ n) ↔
    (let v : ℕ → ℚ := fun j => c ^ j * μ j / (Nat.factorial (2 * j + ε) : ℚ)
     ∀ n, v (n + 3) - 2 * v (n + 2) + v (n + 1) =
       (c / (2 * ((n : ℚ) + 2) * (2 * ((n : ℚ) + 3) + 2 * ε - 1))) *
         (v (n + 2) - 2 * v (n + 1) + v n)) := by
  have h := moment_iff_second_difference ε hε c hc μ
  have hadd (x : ℚ) : x + 3 - 1 = x + 2 := by ring
  simpa [moment_solution, second_difference, scaled_sequence, scale_factor,
    factorial_weight, theta, Nat.add_assoc, div_mul_eq_mul_div, hadd] using h

example {K : Type*} [Field K] (t v : ℕ → K) :
    (∀ n, v (n + 3) = (2 + t (n + 3)) * v (n + 2) -
      (1 + 2 * t (n + 3)) * v (n + 1) + t (n + 3) * v n) ↔
    ∀ n, v (n + 3) - 2 * v (n + 2) + v (n + 1) =
      t (n + 3) * (v (n + 2) - 2 * v (n + 1) + v n) := by
  simpa only [IsSolution, second_difference, Nat.add_assoc, neg_mul, ← sub_eq_add_neg] using
    recurrence_iff_second_difference t v
