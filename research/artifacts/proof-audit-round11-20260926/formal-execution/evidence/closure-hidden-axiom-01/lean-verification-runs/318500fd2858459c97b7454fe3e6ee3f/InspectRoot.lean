import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : Round11Control.hiddenProp
#lean_verify_v2 Round11Control.contaminated expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-reviewer\\stateless-a8e81148d09f\\evidence\\closure-hidden-axiom-01\\lean-verification-runs\\318500fd2858459c97b7454fe3e6ee3f\\declaration.json"
