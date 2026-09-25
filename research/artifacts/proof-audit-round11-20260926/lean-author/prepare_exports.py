from pathlib import Path
import json,re
Base=Path(__file__).resolve().parent
Project=Base/'project'
Source=(Project/'AuditRound11.lean').read_text()
Names=['AuditRound11.'+M[1] for M in re.finditer(r'^(?:noncomputable )?(?:def|abbrev|theorem) (\w+)',Source,re.M)]
(Base/'declaration-names.json').write_text(json.dumps(Names,indent=2)+'\n')
Lines=['import AuditRound11','set_option pp.all true','set_option pp.maxSteps 10000000','set_option pp.deepTerms true']
for Name in Names:
	Lines.extend(['#print '+Name,'#print axioms '+Name])
(Project/'PrintDeclarations.lean').write_text('\n'.join(Lines)+'\n')
Exporter=r'''import Lean
import AuditRound11
open Lean Elab Command Meta
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.maxSteps 10000000
set_option pp.deepTerms true
partial def auditBinderKinds : Expr → List String
  | .forallE _ _ body bi => reprStr bi :: auditBinderKinds body
  | _ => []
elab "#export_round11 " out:str : command => do
  let env := (← getEnv).setExporting false
  let names := env.constants.toList.map Prod.fst |>.filter (fun n =>
    n.toString.startsWith "AuditRound11.")
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
    let axioms ← collectAxioms name
    let mut fields := [("name", toJson name.toString), ("kind", toJson kind),
      ("universes", toJson (info.levelParams.map Name.toString)),
      ("binder_kinds", toJson (auditBinderKinds info.type)),
      ("transitive_axioms", toJson (axioms.map Name.toString)),
      ("type_explicit", toJson typ), ("type_readable", toJson readable)]
    if !info.isTheorem then
      if let some value := info.value? (allowOpaque := true) then
        let body ← liftTermElabM <| withOptions
          (fun o => o.setBool `pp.all true |>.setBool `pp.explicit true |>.setBool `pp.universes true)
          (do return (← ppExpr value).pretty)
        fields := fields ++ [("value_explicit", toJson body)]
    entries := entries.push (Json.mkObj fields)
  IO.FS.writeFile out.getString ((Json.arr entries).pretty ++ "\n")
#export_round11 "F:\\tools\\math-audit-round11-20260926\\formal-author\\declarations-full.json"
'''
(Project/'ExportDeclarations.lean').write_text(Exporter)
print('prepared',len(Names),'named declarations')
