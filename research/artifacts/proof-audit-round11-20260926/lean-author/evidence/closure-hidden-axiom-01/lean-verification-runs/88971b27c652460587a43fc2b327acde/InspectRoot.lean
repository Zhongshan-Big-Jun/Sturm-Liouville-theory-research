import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : Round11Control.hiddenProp
#lean_verify_v2 Round11Control.contaminated expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-author\\evidence\\closure-hidden-axiom-01\\lean-verification-runs\\88971b27c652460587a43fc2b327acde\\declaration.json"
