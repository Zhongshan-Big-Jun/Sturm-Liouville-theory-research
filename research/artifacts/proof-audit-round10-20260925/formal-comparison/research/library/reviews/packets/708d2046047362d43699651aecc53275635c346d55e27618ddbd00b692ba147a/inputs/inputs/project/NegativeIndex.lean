import AuditRound10
open AuditRound10

example : phase_root (fun x : ℝ => x) 1 (2 * Real.pi) := by
  constructor
  · positivity
  · have hp := Real.pi_pos
    norm_num
    linarith
