import Lean
import AuditRound8

set_option maxRecDepth 100000
set_option maxHeartbeats 0
open Lean Elab Command Meta

namespace Round8Exporter

def names_json (Names : Array Name) : Json :=
  toJson (Names.qsort Name.lt |>.map Name.toString)

partial def expr_json (Term : Expr) : Json :=
  match Term with
  | .bvar Index => toJson ("bvar", Index)
  | .fvar Id => toJson ("fvar", Id.name.toString)
  | .mvar Id => toJson ("mvar", Id.name.toString)
  | .sort Level => toJson ("sort", reprStr Level)
  | .const Name Levels => toJson ("const", Name.toString, Levels.map reprStr)
  | .app Function Argument => Json.arr #[toJson "app", expr_json Function, expr_json Argument]
  | .lam _ TermType Body Binder => Json.arr #[toJson "lam", toJson (reprStr Binder), expr_json TermType, expr_json Body]
  | .forallE _ TermType Body Binder => Json.arr #[toJson "forall", toJson (reprStr Binder), expr_json TermType, expr_json Body]
  | .letE _ TermType Value Body NonDependent => Json.arr #[toJson "let", expr_json TermType, expr_json Value, expr_json Body, toJson NonDependent]
  | .lit Literal => toJson ("literal", reprStr Literal)
  | .mdata _ Body => expr_json Body
  | .proj Name Index Body => Json.arr #[toJson "projection", toJson Name.toString, toJson Index, expr_json Body]

def kind_name (Info : ConstantInfo) : String :=
  match Info with
  | .axiomInfo _ => "axiom"
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "definition"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient_primitive"

def body_dependencies (Info : ConstantInfo) : Array Name :=
  let Body := Info.value? (allowOpaque := true) |>.map Expr.getUsedConstants |>.getD #[]
  match Info with
  | .inductInfo Value => Body ++ Value.ctors.toArray
  | _ => Body

partial def dependency_closure (Environment : Environment) (Pending : List Name)
  (Seen : NameSet := {}) : NameSet :=
  match Pending with
  | [] => Seen
  | Name :: Rest =>
    if Seen.contains Name then dependency_closure Environment Rest Seen
    else
      let Seen := Seen.insert Name
      match Environment.checked.get.find? Name with
      | none => dependency_closure Environment Rest Seen
      | some Info => dependency_closure Environment
        (Info.type.getUsedConstants.toList ++ (body_dependencies Info).toList ++ Rest) Seen

partial def semantic_closure (Environment : Environment) (Pending : List Name)
  (Seen : NameSet := {}) : NameSet :=
  match Pending with
  | [] => Seen
  | Name :: Rest =>
    if Seen.contains Name then semantic_closure Environment Rest Seen
    else
      let Seen := Seen.insert Name
      match Environment.checked.get.find? Name with
      | none => semantic_closure Environment Rest Seen
      | some Info =>
        let Body := if Info.isTheorem then #[] else body_dependencies Info
        semantic_closure Environment (Info.type.getUsedConstants.toList ++ Body.toList ++ Rest) Seen

def node_json (Environment : Environment) (Name : Name) (Semantic : Bool) : Json := Id.run do
  let some Info := Environment.checked.get.find? Name
    | return Json.mkObj [("name", toJson Name.toString), ("missing", toJson true)]
  let mut Fields := [
    ("name", toJson Name.toString),
    ("kind", toJson (kind_name Info)),
    ("universes", toJson (Info.levelParams.map Lean.Name.toString)),
    ("unsafe", toJson Info.isUnsafe),
    ("type_dependencies", names_json Info.type.getUsedConstants),
    ("body_dependencies", names_json (body_dependencies Info))]
  if Semantic then
    Fields := Fields ++ [("type_expression", expr_json Info.type)]
    if !Info.isTheorem then
      if let some Value := Info.value? (allowOpaque := true) then
        Fields := Fields ++ [("value_expression", expr_json Value)]
  return Json.mkObj Fields

partial def binder_kinds (TermType : Expr) : List String :=
  match TermType with
  | .forallE _ _ Body Binder => reprStr Binder :: binder_kinds Body
  | _ => []



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
  IO.FS.writeFile "F:\\tools\\math-audit-round8-20260922\\formal-reviewer\\review-20260921T171659Z-7dddbb5a\\supplemental-01\\semantic-definitions.json" ((Json.mkObj [("semantic_nodes",Json.arr nodes),
    ("selected_definitions",Json.arr selected),("controls",Json.arr controls),
    ("modules",Json.arr modules)]).compress ++ "\n")
end Round8Exporter
