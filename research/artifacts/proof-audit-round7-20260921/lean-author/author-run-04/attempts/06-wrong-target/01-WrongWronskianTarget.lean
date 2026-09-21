import SL.AuditRound7

-- Intentional failure: the old formula predicts -6*pi, but the proof gives -4*pi.
example : SL.AuditRound7.wronskian 2 (1 / 2) = -6 * Real.pi := by
  exact SL.AuditRound7.wronskian_two_half
