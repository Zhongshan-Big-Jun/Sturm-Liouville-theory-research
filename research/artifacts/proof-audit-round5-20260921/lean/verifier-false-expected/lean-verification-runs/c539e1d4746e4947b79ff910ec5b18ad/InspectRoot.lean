import LeanVerifyProbe
import SL.AuditRound5
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : ∀ m₀ : ℕ, SL.AuditRound5.high_span m₀ = SL.AuditRound5.oblique ⊓ SL.AuditRound5.krein_polynomials
#lean_verify_v2 SL.AuditRound5.high_span_lt_krein_oblique expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round5-20260921\\lean-author\\verifier-false-expected\\lean-verification-runs\\c539e1d4746e4947b79ff910ec5b18ad\\declaration.json"
