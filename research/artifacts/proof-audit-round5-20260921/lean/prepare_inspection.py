from pathlib import Path
import hashlib
import json
import re

OUT = Path('/mnt/f/tools/math-audit-round5-20260921/lean-author')
SOURCE = Path('/mnt/f/LaTeX/BVE research/lean-proof/SL/AuditRound5.lean')
TEMPLATE = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.0/scripts/LeanVerifyProbe.lean.template')
Text = SOURCE.read_text()
Entries = re.findall(r'^(?:noncomputable )?(def|theorem|lemma) (\w+)', Text, re.M)
Names = ['SL.AuditRound5.' + Name for _, Name in Entries]
Helpers = TEMPLATE.read_text().split('def inspect_declaration', 1)[0]
Helpers = Helpers.replace('import Lean\n', 'import SL.AuditRound5\nimport Lean\n')
Helpers = Helpers.replace('namespace LeanVerifyV2', 'namespace AuthorInspection')
Helpers = Helpers.expandtabs(2)
Probe = Helpers + '\nend AuthorInspection\n\n'
Probe += 'set_option maxRecDepth 8192\nset_option maxHeartbeats 0\n'
Probe += 'set_option pp.universes true\nset_option pp.explicit true\nset_option pp.fullNames true\nset_option pp.proofs false\n\n'
for Name in Names:
	Probe += '#print ' + Name + '\n#print axioms ' + Name + '\n\n'
Probe += 'open Lean Elab Command Meta AuthorInspection in\nrun_cmd do\n'
Probe += '  let Targets : Array Name := #[' + ', '.join('`' + Name for Name in Names) + ']\n'
Probe += '''  let Env := (← getEnv).setExporting false
  let mut Results : Array Json := #[]
  let mut Readable : String := ""
  let mut Explicit : String := ""
  for Target in Targets do
    let some Info := Env.checked.get.find? Target
      | throwError "Missing declaration: {Target}"
    let Axioms ← collectAxioms Target
    let ActualType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.explicit false) do
        return (← ppExpr Info.type).pretty
    let FullType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
        return (← ppExpr Info.type).pretty
    let mut Fields := [
      ("declaration", toJson Target.toString), ("kind", toJson (kind_name Info)),
      ("actual_type", toJson ActualType), ("fully_explicit_type", toJson FullType),
      ("type_expression", expr_json Info.type),
      ("universes", toJson (Info.levelParams.map Name.toString)),
      ("binder_kinds", toJson (binder_kinds Info.type)),
      ("transitive_axioms", names_json Axioms),
      ("type_dependencies", names_json Info.type.getUsedConstants),
      ("body_dependencies", names_json (body_dependencies Info)),
      ("transitive_dependencies", names_json (dependency_closure Env [Target]).toArray),
      ("semantic_dependencies", names_json (semantic_closure Env Info.type.getUsedConstants.toList).toArray)]
    Readable := Readable ++ kind_name Info ++ " " ++ Target.toString ++ " :\n" ++ ActualType
    Explicit := Explicit ++ kind_name Info ++ " " ++ Target.toString ++ " :\n" ++ FullType
    if !Info.isTheorem then
      if let some Value := Info.value? (allowOpaque := true) then
        let Body ← liftTermElabM <| withOptions
          (fun O => O.setBool `pp.explicit false) do
            return (← ppExpr Value).pretty
        let FullBody ← liftTermElabM <| withOptions
          (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
            return (← ppExpr Value).pretty
        Fields := Fields ++ [("definition_body", toJson Body),
          ("fully_explicit_definition_body", toJson FullBody), ("value_expression", expr_json Value)]
        Readable := Readable ++ "\n:=\n" ++ Body
        Explicit := Explicit ++ "\n:=\n" ++ FullBody
    Readable := Readable ++ "\n\n"
    Explicit := Explicit ++ "\n\n"
    Results := Results.push (Json.mkObj Fields)
  let Used := dependency_closure Env Targets.toList
  let mut SemanticUsed : NameSet := {}
  for Target in Targets do
    if let some Info := Env.checked.get.find? Target then
      let Seeds := if Info.isTheorem then Info.type.getUsedConstants.toList else [Target]
      SemanticUsed := semantic_closure Env Seeds SemanticUsed
  let Nodes := Used.toArray.qsort Name.lt |>.map fun N =>
    node_json Env N (SemanticUsed.contains N)
  let mut LocalDefinitions : String := ""
  for N in Used.toArray.qsort Name.lt do
    if N.toString.startsWith "SL." then
      if let some Info := Env.checked.get.find? N then
        if !Info.isTheorem then
          if let some Value := Info.value? (allowOpaque := true) then
            let T ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
                return (← ppExpr Info.type).pretty
            let V ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
                return (← ppExpr Value).pretty
            LocalDefinitions := LocalDefinitions ++ N.toString ++ " :\\n" ++ T ++ "\\n:=\\n" ++ V ++ "\\n\\n"
  let mut Modules : Array Json := #[]
  for N in Env.header.moduleNames do
    let File ← findOLean N
    Modules := Modules.push (Json.mkObj [("module", toJson N.toString), ("olean", toJson File.toString)])
  let Base := "F:/tools/math-audit-round5-20260921/lean-author/final/"
  IO.FS.writeFile (Base ++ "declarations.json")
    ((Json.mkObj [("declarations", Json.arr Results), ("dependencies", Json.arr Nodes), ("semantic_dependencies", names_json SemanticUsed.toArray)]).compress ++ "\\n")
  IO.FS.writeFile (Base ++ "loaded-modules.json")
    ((Json.mkObj [("module_count", toJson Env.header.moduleNames.size), ("modules", Json.arr Modules)]).compress ++ "\\n")
  IO.FS.writeFile (Base ++ "formal-statements.txt") Readable
  IO.FS.writeFile (Base ++ "formal-statements-fully-explicit.txt") Explicit
  IO.FS.writeFile (Base ++ "local-definition-closure.txt") LocalDefinitions
'''
(OUT / 'InspectAuditRound5.lean').write_text(Probe)
(OUT / 'inspection-targets.json').write_text(json.dumps({
	'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
	'helper_template': str(TEMPLATE),
	'helper_template_sha256': hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
	'entries': [{'kind': Kind, 'name': 'SL.AuditRound5.' + Name} for Kind, Name in Entries]
}, indent=2) + '\n')
print('Prepared', len(Names), 'declaration inspections.')
