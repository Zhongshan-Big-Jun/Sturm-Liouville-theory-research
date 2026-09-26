import AuditRound12
open scoped Matrix
open AuditRound12

-- Deliberately false same-sign mirror convention at two original coordinates.
example : sign 1 (Sum.inr (0 : Fin 1)) = sign 1 (Sum.inl (0 : Fin 1)) := by
  norm_num [sign]
