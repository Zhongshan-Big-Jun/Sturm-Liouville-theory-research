import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : True
#lean_verify_v2 Round11Control.missing expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-author\\evidence\\closure-missing-target-01\\lean-verification-runs\\2b77b08251344679a7c7d4c26a5e784f\\declaration.json"
