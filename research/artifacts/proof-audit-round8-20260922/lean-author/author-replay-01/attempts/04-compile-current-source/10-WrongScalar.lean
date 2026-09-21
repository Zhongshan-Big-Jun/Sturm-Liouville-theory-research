import AuditRound8
open AuditRound8
-- A genuinely false stronger rational bound; norm_num computes the contradictory goal.
example : scalarRatio < (4 / 5 : ℚ) := by
  norm_num [scalarRatio]
