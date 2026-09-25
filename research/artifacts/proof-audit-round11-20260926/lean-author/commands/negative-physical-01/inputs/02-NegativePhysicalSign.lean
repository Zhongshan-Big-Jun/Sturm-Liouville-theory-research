import AuditRound11
open scoped Matrix
open AuditRound11
example : physical_reflection (fun _ : PairIndex 1 => (1 : ℝ)) -
    physical_reflection (fun _ : PairIndex 1 => (0 : ℝ)) = (fun _ => (1 : ℝ)) := by
  ext i
  cases i <;>
    simp [physical_reflection, reversal, Matrix.mulVec, dotProduct,
      Fintype.sum_sum_type, Matrix.fromBlocks, Matrix.one_apply]
