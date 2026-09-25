import AuditRound11
open scoped Matrix
open AuditRound11
example (hwrong : ∀ J : PairedMatrix 1,
    J * reversal 1 = -(reversal 1 * J) →
    J.det = (parity_matrix J).toBlocks₁₁.det * (parity_matrix J).toBlocks₂₂.det) :
    False := by
  have ha : parity_sign 1 * reversal 1 = -(reversal 1 * parity_sign 1) := by
    simp [parity_sign, reversal, Matrix.fromBlocks_multiply, Matrix.fromBlocks_neg]
  have hz := anticommuting_blocks (parity_sign 1) ha
  have he := hwrong (parity_sign 1) ha
  rw [hz.1, hz.2] at he
  norm_num [parity_sign, Matrix.det_fromBlocks_zero₂₁, Matrix.det_neg] at he


example : physical_reflection (fun _ : PairIndex 1 => (1 : ℝ)) -
    physical_reflection (fun _ : PairIndex 1 => (0 : ℝ)) = (fun _ => (-1 : ℝ)) := by
  ext i
  cases i <;>
    simp [physical_reflection, reversal, Matrix.mulVec, dotProduct,
      Fintype.sum_sum_type, Matrix.fromBlocks, Matrix.one_apply]

example (x : PairIndex 0 → ℝ) :
    physical_reflection (x + 0) - physical_reflection x = 0 := by simp

example (x : PairIndex 1 → ℝ) :
    physical_reflection (x + 0) - physical_reflection x = 0 ∧
    reversal 1 *ᵥ (0 : PairIndex 1 → ℝ) = 0 := by simp
