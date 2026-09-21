import LeanVerifyProbe
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : SL.AuditRound7.wronskian 2 (1 / 2) = -6 * Real.pi
#lean_verify_v2 SL.AuditRound7.wronskian_two_half expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round7-20260921\\independent-execution\\lean-package\\independent-positive-negative-20260921\\supplemental-negative\\lean-verification-runs\\4d338a2edc7c42af9176a1b2229a6317\\declaration.json"
