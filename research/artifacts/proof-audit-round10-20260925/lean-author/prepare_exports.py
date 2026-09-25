from pathlib import Path
import json, re

BASE = Path(__file__).resolve().parent
PROJECT = BASE / 'project'
SOURCE = (PROJECT / 'AuditRound10.lean').read_text()
NAMES = ['AuditRound10.' + M[1] for M in re.finditer(r'^(?:noncomputable )?(?:def|abbrev|theorem) (\w+)', SOURCE, re.M)]
CONTROL = (PROJECT / 'Counterexamples.lean').read_text()
CONTROLS = ['AuditRound10Controls.' + M[1] for M in re.finditer(r'^theorem (\w+)', CONTROL, re.M)]
(BASE / 'declaration-names.json').write_text(json.dumps({'main':NAMES,'controls':CONTROLS},ensure_ascii=False,indent=2)+'\n')
for File, Import, Names in [('PrintAuditRound10.lean','AuditRound10',NAMES),('PrintCounterexamples.lean','Counterexamples',CONTROLS)]:
	Lines = [f'import {Import}', '', 'set_option pp.universes true', 'set_option pp.explicit true', 'set_option pp.proofs true', '']
	for Name in Names:
		Lines += ['#print ' + Name, '#print axioms ' + Name, '']
	(PROJECT / File).write_text('\n'.join(Lines))

EXPORTER = '''import Lean
import AuditRound10

open Lean Elab Command Meta

set_option maxRecDepth 100000
set_option maxHeartbeats 0

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
  IO.FS.writeFile out.getString ((Json.arr entries).pretty ++ "\\n")

#export_round10 "F:\\\\tools\\\\math-audit-round10-20260925\\\\formal-author\\\\formal-declarations.json"
'''
(PROJECT / 'ReadbackExport.lean').write_text(EXPORTER)
print('Prepared explicit declaration/axiom print commands and structured formal readback export.')
