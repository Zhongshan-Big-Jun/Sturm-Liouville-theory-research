import AuditRound11
open scoped Matrix
open AuditRound11
example : (Matrix.fromBlocks (0 : Square 1) 1 1 (0 : Square 1)).det = -1 := by
  rw [off_diagonal_determinant]
  norm_num
example : (Matrix.fromBlocks (0 : Square 0) 1 1 (0 : Square 0)).det = 1 := by
  rw [off_diagonal_determinant]
  norm_num
example : parity_sign 1 * reversal 1 = -(reversal 1 * parity_sign 1) := by
  simp [parity_sign, reversal, Matrix.fromBlocks_multiply, Matrix.fromBlocks_neg]
example : (boundary_even 4).det = 336 ∧ (boundary_odd 4).det = 432 := by
  norm_num [boundary_even, boundary_odd, Matrix.det_fin_two]
example : (boundary_even 0).det = 0 ∧ (boundary_odd 0).det = 0 := by
  norm_num [boundary_even, boundary_odd, Matrix.det_fin_two]
example (L : ℕ) (h : 4 ≤ L) (b : PairIndex 2 → ℝ) :
    ∃! a, boundary_full (L : ℝ) *ᵥ a = b := (boundary_correction L h).2 b
example (x v : PairIndex 3 → ℝ) (h : reversal 3 *ᵥ v = v) :
    physical_reflection (x + v) - physical_reflection x = -v :=
  (reflection_parity x v).2.mpr h
