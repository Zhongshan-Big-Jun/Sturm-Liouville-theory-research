import AuditRound11
open scoped Matrix
open AuditRound11
example : (Matrix.fromBlocks (0 : Square 1) 1 1 (0 : Square 1)).det = 1 := by
  rw [off_diagonal_determinant]
  norm_num
