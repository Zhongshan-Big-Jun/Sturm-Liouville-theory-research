import LeanVerifyProbe
import ClosureControl
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : False
#lean_verify_v2 Round11Control.valid expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round11-20260926\\formal-reviewer\\stateless-a8e81148d09f\\evidence\\closure-wrong-type-01\\lean-verification-runs\\a18ed5d23e754ae8b22d1d564b697af5\\declaration.json"
