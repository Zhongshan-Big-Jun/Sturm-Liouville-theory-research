import LeanVerifyProbe
import SL.AuditRound5
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (SL.AuditRound5.traces SL.AuditRound5.p_zero = (1, 0) ∧ SL.AuditRound5.traces SL.AuditRound5.p_one = (0, 1)) ∧
    (SL.AuditRound5.residues SL.AuditRound5.p_zero = 0 ∧ SL.AuditRound5.residues SL.AuditRound5.p_one = 0) ∧
    (∀ m : ℕ, 2 ≤ m →
      SL.AuditRound5.traces (SL.AuditRound5.p_even m) = 0 ∧ SL.AuditRound5.traces (SL.AuditRound5.p_odd m) = 0 ∧
      SL.AuditRound5.residues (SL.AuditRound5.p_even m) = 0 ∧ SL.AuditRound5.residues (SL.AuditRound5.p_odd m) = 0) ∧
    (∀ m₀ : ℕ, SL.AuditRound5.high_span m₀ ≤ SL.AuditRound5.zero_traces ∧
      SL.AuditRound5.high_span m₀ < SL.AuditRound5.oblique ⊓ SL.AuditRound5.krein_polynomials) ∧
    ((1 + Polynomial.X : Polynomial ℝ) ∈ SL.AuditRound5.oblique ⊓ SL.AuditRound5.krein_polynomials ∧
      (1 : Polynomial ℝ) ∉ SL.AuditRound5.oblique ⊓ SL.AuditRound5.krein_polynomials ∧
      (Polynomial.X : Polynomial ℝ) ∉ SL.AuditRound5.oblique ⊓ SL.AuditRound5.krein_polynomials) ∧
    (∀ L : ℕ, 0 < L → (SL.AuditRound5.endpoint_matrix L).det ≠ 0 ∧
      SL.AuditRound5.endpoint_matrix L * SL.AuditRound5.correction_matrix L = 1 ∧
      SL.AuditRound5.correction_matrix L * SL.AuditRound5.endpoint_matrix L = 1) ∧
    (∀ L : ℕ, 0 < L → Even L → ∀ p : Polynomial ℝ,
      SL.AuditRound5.residues (SL.AuditRound5.correct_endpoints L p) = 0 ∧
      ((Polynomial.X : Polynomial ℝ) ^ L ∣ p →
        (Polynomial.X : Polynomial ℝ) ^ L ∣ SL.AuditRound5.correct_endpoints L p)) ∧
    (∀ W : Submodule ℝ (Polynomial ℝ), SL.AuditRound5.zero_traces ≤ W →
      ∀ p : Polynomial ℝ, p ∈ W ↔ SL.AuditRound5.trace_lift (SL.AuditRound5.traces p) ∈ W)
#lean_verify_v2 SL.AuditRound5.local_algebra_root expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round5-20260921\\lean-author\\verifier-positive\\lean-verification-runs\\74e34fd7f55e4dbd9215d579f0344e68\\declaration.json"
