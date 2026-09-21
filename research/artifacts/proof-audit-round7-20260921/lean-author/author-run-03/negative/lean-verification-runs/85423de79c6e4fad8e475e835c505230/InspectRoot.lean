import LeanVerifyProbe
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : SL.AuditRound7.wronskian 2 (1 / 2) = -6 * Real.pi
#lean_verify_v2 SL.AuditRound7.wronskian_two_half expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round7-20260921\\lean-author\\author-run-03\\negative\\lean-verification-runs\\85423de79c6e4fad8e475e835c505230\\declaration.json"
