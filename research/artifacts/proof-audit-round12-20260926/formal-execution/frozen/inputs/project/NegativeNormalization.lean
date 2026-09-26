import AuditRound12
open scoped Matrix
open AuditRound12

-- Deliberately false omission of the unnormalized Gram factor 2.
example : (Be 1)ᵀ * Be 1 = (1 : Matrix (Fin 1) (Fin 1) ℝ) := by
  rw [(basis_relations 1).2.2.1]
  norm_num [Matrix.smul_apply, Matrix.one_apply]
