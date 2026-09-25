import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : True
#lean_verify_v2 Round11Control.valid expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-reviewer\\stateless-a8e81148d09f\\evidence\\closure-positive-01\\lean-verification-runs\\367c19bb4c1e4cfa9a0f4f2a3991b0b7\\declaration.json"
