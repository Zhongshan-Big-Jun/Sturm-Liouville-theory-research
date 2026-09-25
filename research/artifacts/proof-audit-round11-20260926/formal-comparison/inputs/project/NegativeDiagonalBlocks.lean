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

example : ∀ J : PairedMatrix 1, J * reversal 1 = -(reversal 1 * J) →
    J.det = (parity_matrix J).toBlocks₁₁.det * (parity_matrix J).toBlocks₂₂.det := by
  intro J h
  rw [(anticommuting_blocks J h).1, (anticommuting_blocks J h).2]
  norm_num
