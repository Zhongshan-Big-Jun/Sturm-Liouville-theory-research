import Lean
import AuditRound10

open Lean Elab Command Meta

set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.maxSteps 10000000
set_option pp.deepTerms true

elab "#export_round10 " out:str : command => do
  let env := (← getEnv).setExporting false
  let names := env.constants.toList.map Prod.fst |>.filter (fun n =>
    n.toString.startsWith "AuditRound10.")
  let mut entries := #[]
  for name in names.mergeSort (fun a b => a.toString ≤ b.toString) do
    let some info := env.checked.get.find? name | continue
    let kind := match info with
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | .axiomInfo _ => "axiom"
      | .opaqueInfo _ => "opaque"
      | _ => "other"
    let typ ← liftTermElabM <| withOptions
      (fun o => o.setBool `pp.all true |>.setBool `pp.explicit true |>.setBool `pp.universes true)
      (do return (← ppExpr info.type).pretty)
    let readable ← liftTermElabM <| withOptions
      (fun o => o.setBool `pp.explicit true |>.setBool `pp.universes true)
      (do return (← ppExpr info.type).pretty)
    let mut fields := [("name", toJson name.toString), ("kind", toJson kind),
      ("universes", toJson (info.levelParams.map Name.toString)),
      ("type_explicit", toJson typ), ("type_readable", toJson readable)]
    if !info.isTheorem then
      if let some value := info.value? (allowOpaque := true) then
        let body ← liftTermElabM <| withOptions
          (fun o => o.setBool `pp.all true |>.setBool `pp.explicit true |>.setBool `pp.universes true)
          (do return (← ppExpr value).pretty)
        fields := fields ++ [("value_explicit", toJson body)]
    entries := entries.push (Json.mkObj fields)
  IO.FS.writeFile out.getString ((Json.arr entries).pretty ++ "\n")

#export_round10 "F:\\tools\\math-audit-round10-20260925\\formal-author\\formal-declarations-full.json"
