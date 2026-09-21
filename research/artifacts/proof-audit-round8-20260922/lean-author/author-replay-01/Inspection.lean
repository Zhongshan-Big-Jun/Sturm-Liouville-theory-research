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
theorem positive_control : (∀ (lambda2 : ℝ), 0 ≤ lambda2 → lambda2 ≤ 4 * Real.pi ^ 2 →
    0 ≤ phase lambda2 ∧ phase lambda2 ≤ Real.pi / 20 ∧ Real.pi / 20 < Real.pi / 2) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    I2 a u = u * (1 + b + b ^ 2 * a ^ 2) / (2 * (1 + b ^ 2 * a ^ 2)) ∧
    0 < I2 a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    S a u = Real.pi ^ 2 / (2 * u ^ 3) -
      2 * a ^ 4 * b ^ 2 / (u ^ 3 * (1 + b + b ^ 2 * a ^ 2))) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 →
    C a b u = 4 * mubar1 u * ell u / (3 * u) + (ell u / 3) * S a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 → S a u = 0 →
    C a b u = Real.pi ^ 2 * ell u / (3 * u ^ 3) ∧ 0 < C a b u) ∧
  scalarRatio < (8256 / 10000 : ℚ) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (19 / 100 : ℝ) < 48743 / 100000 ∧ (48743 / 100000 : ℝ) < 1 / 2 ∧
    wCritical 1500 < 48743 / 100000 ∧
    (48743 / 100000 : ℝ) < wCritical (3015 / 2)) ∧
  (capGap (3015 / 2) (4995815 / 10000000) < 25 ∧
    25 < capGap 1515 (4995815 / 10000000)) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (0 : ℝ) < 4995815 / 10000000 ∧ (4995815 / 10000000 : ℝ) < 1 / 2 ∧
    wCap (3015 / 2) < 4995815 / 10000000 ∧
    (4995815 / 10000000 : ℝ) < wCap 1515) := AuditRound8.local_root

run_cmd do
  let env := (← getEnv).setExporting false
  let names ← env.constants.foldM (init := (#[] : Array Name)) fun acc name _ => do
    if name.toString.startsWith "AuditRound8." then return acc.push name
    return acc
  let names := names.qsort Name.lt
  let mut publicDecls := #[]
  for name in names do
    let some info := env.checked.get.find? name | throwError "Missing {name}"
    let actualType ← liftTermElabM <| withOptions
      (fun o => o.setBool `pp.universes true |>.setBool `pp.fullNames true |>.setBool `pp.explicit true)
      do return (← ppExpr info.type).pretty
    let valueText ← match info.value? (allowOpaque := true) with
      | some value => if info.isTheorem then pure "[proof term omitted; dependency closure and axioms exported]"
        else liftTermElabM <| withOptions (fun o => o.setBool `pp.fullNames true)
          do return (← ppExpr value).pretty
      | none => pure "[no value]"
    let axioms ← collectAxioms name
    publicDecls := publicDecls.push <| Json.mkObj [
      ("declaration", toJson name.toString), ("kind", toJson (kind_name info)),
      ("actual_type", toJson actualType), ("value_readback", toJson valueText),
      ("type_expression", expr_json info.type),
      ("value_expression", if info.isTheorem then Json.null else
        (info.value? (allowOpaque := true)).map expr_json |>.getD Json.null),
      ("universes", toJson (info.levelParams.map Name.toString)),
      ("binder_kinds", toJson (binder_kinds info.type)),
      ("unsafe", toJson info.isUnsafe), ("axioms", names_json axioms)]
  let some actual := env.checked.get.find? `AuditRound8.local_root | throwError "Missing root"
  let some expected := env.checked.get.find? `Round8Exporter.positive_control | throwError "Missing contract"
  let same ← liftTermElabM <| withTransparency .all <| isDefEq actual.type expected.type
  unless same && actual.levelParams == expected.levelParams && binder_kinds actual.type == binder_kinds expected.type do
    throwError "Complete root type does not match expected contract"
  let used := dependency_closure env (names.toList ++ expected.type.getUsedConstants.toList)
  let mut bad := #[]
  let nodes := used.toArray.qsort Name.lt |>.map fun name => node_json env name false
  for name in used.toArray do
    match env.checked.get.find? name with
    | none => bad := bad.push name.toString
    | some info => if info.isUnsafe then bad := bad.push name.toString
  unless bad.isEmpty do throwError "Unknown or unsafe dependencies: {bad}"
  let mut modules := #[]
  for name in env.header.moduleNames.qsort Name.lt do
    let path ← findOLean name
    modules := modules.push <| Json.mkObj [("module",toJson name.toString),("olean",toJson path.toString)]
  let result := Json.mkObj [
    ("public_declarations", Json.arr publicDecls),
    ("expected_type_expression", expr_json expected.type),
    ("expected_type_match", toJson same), ("dependencies", Json.arr nodes),
    ("loaded_module_count", toJson env.header.moduleNames.size),
    ("modules", Json.arr modules)]
  IO.FS.writeFile "F:\\tools\\math-audit-round8-20260922\\lean-author\\author-replay-01\\declarations.json" (result.compress ++ "\n")
end Round8Exporter
