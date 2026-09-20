import SL.AuditRound2
example : SL.AuditRound2.second_difference (SL.AuditRound2.k1_scaled SL.AuditRound2.k1_n3_segment) 3 = 0 := by
  norm_num [SL.AuditRound2.second_difference, SL.AuditRound2.k1_scaled, SL.AuditRound2.k1_n3_segment]
