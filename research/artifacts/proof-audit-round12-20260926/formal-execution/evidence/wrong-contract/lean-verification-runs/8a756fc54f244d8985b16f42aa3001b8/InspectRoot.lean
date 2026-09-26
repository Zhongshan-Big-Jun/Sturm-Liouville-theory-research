import LeanVerifyProbe
import AuditRound12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : open scoped Matrix in open AuditRound12 in (∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ), rawKo K = E n * rawKe K * E n ∧ KpEven K = E n * rawKo K * E n)
#lean_verify_v2 AuditRound12.sector_exchange expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round12-20260926\\formal-reviewer\\d080d3cc-independent-bk5cllgu\\evidence\\wrong-contract\\lean-verification-runs\\8a756fc54f244d8985b16f42aa3001b8\\declaration.json"
