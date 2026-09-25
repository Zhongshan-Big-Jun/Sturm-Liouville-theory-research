import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : False
#lean_verify_v2 Round11Control.valid expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-author\\evidence\\closure-wrong-type-01\\lean-verification-runs\\37694e83d22d498eb516f9c04000d25c\\declaration.json"
