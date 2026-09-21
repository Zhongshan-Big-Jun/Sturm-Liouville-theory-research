from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'package'
sys.path.insert(0,str(PACKAGE))
from run_lean import run, environment, win, write_json, digest
from replay import hash_files
OUT=ROOT/'supplemental-01'
OUT.mkdir(exist_ok=False)
REPLAY=ROOT/'replay-01'
config=json.loads((PACKAGE/'runtime-config.json').read_text())
paths={k:Path(k) for k in json.loads((REPLAY/'imports-after.json').read_text())}
runtime_paths={k:Path(k) for k in json.loads((REPLAY/'runtime-after.json').read_text())}
before=hash_files(paths);runtime_before=hash_files(runtime_paths)
write_json(OUT/'imports-before.json',before);write_json(OUT/'runtime-before.json',runtime_before)
assert before==json.loads((REPLAY/'imports-after.json').read_text())
assert runtime_before==json.loads((REPLAY/'runtime-after.json').read_text())
root_hash=digest(REPLAY/'lib/AuditRound8.olean')
prefix=(PACKAGE/'ExporterPrefix.lean.txt').read_text()
checks=r"""
open AuditRound8

theorem independent_reject_phase (lambda2 : ℝ) (h0 : 0 ≤ lambda2)
    (hmax : lambda2 ≤ 4 * Real.pi ^ 2) : ¬ Real.pi / 2 < phase lambda2 := by
  have h := phase_bound lambda2 h0 hmax
  intro bad
  linarith [h.2.1, h.2.2]

theorem independent_reject_stationary (a b u : ℝ) (ha : 0 < a) (hu : 0 < u)
    (hh : u < 1 / 2) (hb : b = ell u / u)
    (hr : Real.sin a + b * a * Real.cos a = 0) (hs : S a u = 0) :
    C a b u ≠ Real.pi ^ 2 * ell u / (2 * u ^ 3) := by
  have h := stationary_coefficient a b u ha hu hh hb hr hs
  intro bad
  have factor : Real.pi ^ 2 * ell u / (2 * u ^ 3) =
      (3 / 2 : ℝ) * (Real.pi ^ 2 * ell u / (3 * u ^ 3)) := by
    field_simp <;> ring
  rw [← h.1, ← bad] at factor
  linarith [h.2]

theorem independent_reject_scalar : (4 / 5 : ℚ) < scalarRatio := by
  norm_num [scalarRatio]

theorem total_operation_boundary_values :
    phase 0 = 0 ∧ I2 0 1 = 1 / 2 ∧ wCritical 0 = 1 / 2 ∧ wCap 0 = 1 / 2 := by
  norm_num [phase, I2, wCritical, wCap]

run_cmd do
  let env := (← getEnv).setExporting false
  let names ← env.constants.foldM (init := (#[] : Array Name)) fun acc name _ => do
    if name.toString.startsWith "AuditRound8." then return acc.push name
    return acc
  let semanticNames := semantic_closure env names.toList
  let nodes := semanticNames.toArray.qsort Name.lt |>.map fun n => node_json env n true
  let mut selected := #[]
  for n in [`Real.pi, `Real.sqrt, `Real.sin, `Real.cos] do
    let some info := env.checked.get.find? n | throwError "Missing {n}"
    let typ ← liftTermElabM <| withOptions (fun o => o.setBool `pp.fullNames true |>.setBool `pp.explicit true) do
      return (← ppExpr info.type).pretty
    let val ← match info.value? (allowOpaque := true) with
      | some v => liftTermElabM <| withOptions (fun o => o.setBool `pp.fullNames true) do
        return (← ppExpr v).pretty
      | none => pure "[no value]"
    selected := selected.push <| Json.mkObj [("name",toJson n.toString),("type",toJson typ),("value",toJson val)]
  let mut controls := #[]
  for n in [`Round8Exporter.independent_reject_phase, `Round8Exporter.independent_reject_stationary,
      `Round8Exporter.independent_reject_scalar, `Round8Exporter.total_operation_boundary_values] do
    let ax ← collectAxioms n
    controls := controls.push <| Json.mkObj [("name",toJson n.toString),("axioms",names_json ax)]
  let mut modules := #[]
  for n in env.header.moduleNames.qsort Name.lt do
    let p ← findOLean n
    modules := modules.push <| Json.mkObj [("module",toJson n.toString),("olean",toJson p.toString)]
  IO.FS.writeFile OUTPUT_PATH ((Json.mkObj [("semantic_nodes",Json.arr nodes),
    ("selected_definitions",Json.arr selected),("controls",Json.arr controls),
    ("modules",Json.arr modules)]).compress ++ "\n")
end Round8Exporter
"""
source=OUT/'SupplementalInspection.lean'
source.write_text(prefix+'\n'+checks.replace('OUTPUT_PATH',json.dumps(win(OUT/'semantic-definitions.json'))))
rec=run(OUT,'01-semantic-definitions-and-negations',[config['lean'],win(source)],
    environment(OUT,[REPLAY/'lib']),REPLAY/'src',
    [source,PACKAGE/'ExporterPrefix.lean.txt',REPLAY/'src/AuditRound8.lean'],
    [OUT/'semantic-definitions.json',REPLAY/'lib/AuditRound8.olean'])
after=hash_files(paths);runtime_after=hash_files(runtime_paths)
write_json(OUT/'imports-after.json',after);write_json(OUT/'runtime-after.json',runtime_after)
write_json(OUT/'stability.json',{'imports_unchanged':before==after,'runtime_unchanged':runtime_before==runtime_after,
    'root_unchanged':root_hash==digest(REPLAY/'lib/AuditRound8.olean'),'exit_code':rec['exit_code']})
assert before==after and runtime_before==runtime_after and root_hash==digest(REPLAY/'lib/AuditRound8.olean')
sys.exit(rec['exit_code'])
