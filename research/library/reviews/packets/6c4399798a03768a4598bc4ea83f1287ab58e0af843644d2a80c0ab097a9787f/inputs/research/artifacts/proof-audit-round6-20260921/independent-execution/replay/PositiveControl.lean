import SL.AuditRound6
example : SL.AuditRound6.augmented_span = ⊤ ∧
    (Polynomial.X ^ 2 : Polynomial ℝ) ∉ SL.AuditRound6.sparse_span ∧
    (∀ i : Fin 4, SL.AuditRound6.four_traces (Polynomial.X ^ (i.val + 2)) = fun j => SL.AuditRound6.trace_matrix j i) ∧
    SL.AuditRound6.trace_matrix.det = 15360 ∧
    SL.AuditRound6.trace_matrix * SL.AuditRound6.inverse_matrix = 1 ∧
    SL.AuditRound6.inverse_matrix * SL.AuditRound6.trace_matrix = 1 ∧
    (∀ r : Fin 4 → ℝ, SL.AuditRound6.four_traces (SL.AuditRound6.four_trace_lift r) = r) ∧
    (∀ p : Polynomial ℝ, SL.AuditRound6.four_traces (SL.AuditRound6.correct_four_traces p) = 0) ∧
    SL.AuditRound6.cancellation = Polynomial.X ^ 6 - Polynomial.C 5 * Polynomial.X ^ 4 + Polynomial.C 7 * Polynomial.X ^ 2 ∧
    SL.AuditRound6.four_traces SL.AuditRound6.cancellation = 0 ∧
    SL.AuditRound6.four_traces (SL.AuditRound5.p_even 2) = ![0, 0, 24, -24] ∧
    SL.AuditRound6.four_traces (SL.AuditRound5.p_even 2) ≠ 0 ∧
    (inner ℝ SL.AuditRound6.detector SL.AuditRound6.coordinate_zero = 1 ∧
      inner ℝ SL.AuditRound6.detector SL.AuditRound6.coordinate_one = 1 ∧
      inner ℝ SL.AuditRound6.detector SL.AuditRound6.witness = 0 ∧
      inner ℝ SL.AuditRound6.witness SL.AuditRound6.coordinate_zero = 1 ∧
      inner ℝ SL.AuditRound6.witness SL.AuditRound6.coordinate_one = -1) := SL.AuditRound6.local_algebra_root
