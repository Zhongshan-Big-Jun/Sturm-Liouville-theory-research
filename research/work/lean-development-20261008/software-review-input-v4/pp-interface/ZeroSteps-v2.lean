import Lean
open Lean Elab Command Meta
run_cmd do
  let Environment := (← getEnv).setExporting false
  let some Info := Environment.checked.get.find? `Nat.add_zero | throwError "missing declaration"
  let FullType ← liftTermElabM <| withOptions (fun Options => Options.setBool `pp.all true |>.set `pp.maxSteps (0 : Nat)) (do return (← ppExpr Info.type).pretty)
  IO.println FullType
