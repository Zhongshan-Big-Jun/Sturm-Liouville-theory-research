import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : True
#lean_verify_v2 Round11Control.missing expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-reviewer\\stateless-a8e81148d09f\\evidence\\closure-missing-target-01\\lean-verification-runs\\60a0d3dc9d6348939f5c04575f178a12\\declaration.json"
