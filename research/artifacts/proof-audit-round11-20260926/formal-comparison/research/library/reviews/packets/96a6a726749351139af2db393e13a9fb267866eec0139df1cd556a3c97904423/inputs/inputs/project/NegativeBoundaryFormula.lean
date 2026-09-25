import AuditRound11
open scoped Matrix
open AuditRound11
example : (boundary_even 4).det = 2 * 4 * (4 + 2) * (2 * 4 + 1) := by
  norm_num [boundary_even, Matrix.det_fin_two]
