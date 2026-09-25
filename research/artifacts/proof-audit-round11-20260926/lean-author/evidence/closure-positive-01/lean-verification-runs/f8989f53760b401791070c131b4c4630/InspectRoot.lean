import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : True
#lean_verify_v2 Round11Control.valid expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-author\\evidence\\closure-positive-01\\lean-verification-runs\\f8989f53760b401791070c131b4c4630\\declaration.json"
