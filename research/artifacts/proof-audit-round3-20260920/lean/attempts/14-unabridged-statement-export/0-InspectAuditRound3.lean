import SL.AuditRound3
import Lean

open Lean Elab Command Meta

namespace AuthorInspection

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

def modules_for_names (Environment : Environment) (Names : NameSet) : NameSet := Id.run do
  let mut Modules : NameSet := {}
  for Name in Names.toArray do
    if let some Index := Environment.getModuleIdxFor? Name then
      if let some ModuleName := Environment.header.moduleNames[Index.toNat]? then
        Modules := Modules.insert ModuleName
  return Modules


end AuthorInspection

set_option maxRecDepth 8192
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
set_option pp.proofs false

#print SL.AuditRound3.recurrence_solution
#print axioms SL.AuditRound3.recurrence_solution

#print SL.AuditRound3.solves_recurrence
#print axioms SL.AuditRound3.solves_recurrence

#print SL.AuditRound3.epsilon
#print axioms SL.AuditRound3.epsilon

#print SL.AuditRound3.product_bound
#print axioms SL.AuditRound3.product_bound

#print SL.AuditRound3.recurrence_solution_solves
#print axioms SL.AuditRound3.recurrence_solution_solves

#print SL.AuditRound3.recurrence_solution_unique
#print axioms SL.AuditRound3.recurrence_solution_unique

#print SL.AuditRound3.second_order_decomposition
#print axioms SL.AuditRound3.second_order_decomposition

#print SL.AuditRound3.second_order_lower_bound
#print axioms SL.AuditRound3.second_order_lower_bound

#print SL.AuditRound3.second_order_exact_iff
#print axioms SL.AuditRound3.second_order_exact_iff

#print SL.AuditRound3.recurrence_monotone_nonnegative
#print axioms SL.AuditRound3.recurrence_monotone_nonnegative

#print SL.AuditRound3.recurrence_product_lower_bound
#print axioms SL.AuditRound3.recurrence_product_lower_bound

#print SL.AuditRound3.recurrence_product_eq_of_B_zero
#print axioms SL.AuditRound3.recurrence_product_eq_of_B_zero

#print SL.AuditRound3.product_bound_eq_epsilon
#print axioms SL.AuditRound3.product_bound_eq_epsilon

#print SL.AuditRound3.exponential_sequence
#print axioms SL.AuditRound3.exponential_sequence

#print SL.AuditRound3.exponential_sequence_solves
#print axioms SL.AuditRound3.exponential_sequence_solves

#print SL.AuditRound3.constant_recurrence_solution
#print axioms SL.AuditRound3.constant_recurrence_solution

#print SL.AuditRound3.constant_recurrence_parameters
#print axioms SL.AuditRound3.constant_recurrence_parameters

#print SL.AuditRound3.constant_recurrence_product
#print axioms SL.AuditRound3.constant_recurrence_product

#print SL.AuditRound3.constant_recurrence_strict_gap
#print axioms SL.AuditRound3.constant_recurrence_strict_gap

#print SL.AuditRound3.no_general_product_equality
#print axioms SL.AuditRound3.no_general_product_equality

#print SL.AuditRound3.perturbed_A
#print axioms SL.AuditRound3.perturbed_A

#print SL.AuditRound3.perturbed_B
#print axioms SL.AuditRound3.perturbed_B

#print SL.AuditRound3.perturbed_coefficient_difference
#print axioms SL.AuditRound3.perturbed_coefficient_difference

#print SL.AuditRound3.perturbed_m4_values
#print axioms SL.AuditRound3.perturbed_m4_values

#print SL.AuditRound3.old_m4_expression
#print axioms SL.AuditRound3.old_m4_expression

#print SL.AuditRound3.perturbed_m4_rejects_old_expression
#print axioms SL.AuditRound3.perturbed_m4_rejects_old_expression

#print SL.AuditRound3.p2_moment_formula
#print axioms SL.AuditRound3.p2_moment_formula

#print SL.AuditRound3.p2_image_moment_formula
#print axioms SL.AuditRound3.p2_image_moment_formula

#print SL.AuditRound3.p2_delta_formula
#print axioms SL.AuditRound3.p2_delta_formula

#print SL.AuditRound3.p2_moment_rational_identity
#print axioms SL.AuditRound3.p2_moment_rational_identity

#print SL.AuditRound3.p2_image_moment_rational_identity
#print axioms SL.AuditRound3.p2_image_moment_rational_identity

#print SL.AuditRound3.p2_perturbation_cancellation
#print axioms SL.AuditRound3.p2_perturbation_cancellation

#print SL.AuditRound3.p2_delta_complement
#print axioms SL.AuditRound3.p2_delta_complement

#print SL.AuditRound3.p2_delta_special_values
#print axioms SL.AuditRound3.p2_delta_special_values

open Lean Elab Command Meta AuthorInspection in
run_cmd do
  let Targets : Array Name := #[`SL.AuditRound3.recurrence_solution, `SL.AuditRound3.solves_recurrence, `SL.AuditRound3.epsilon, `SL.AuditRound3.product_bound, `SL.AuditRound3.recurrence_solution_solves, `SL.AuditRound3.recurrence_solution_unique, `SL.AuditRound3.second_order_decomposition, `SL.AuditRound3.second_order_lower_bound, `SL.AuditRound3.second_order_exact_iff, `SL.AuditRound3.recurrence_monotone_nonnegative, `SL.AuditRound3.recurrence_product_lower_bound, `SL.AuditRound3.recurrence_product_eq_of_B_zero, `SL.AuditRound3.product_bound_eq_epsilon, `SL.AuditRound3.exponential_sequence, `SL.AuditRound3.exponential_sequence_solves, `SL.AuditRound3.constant_recurrence_solution, `SL.AuditRound3.constant_recurrence_parameters, `SL.AuditRound3.constant_recurrence_product, `SL.AuditRound3.constant_recurrence_strict_gap, `SL.AuditRound3.no_general_product_equality, `SL.AuditRound3.perturbed_A, `SL.AuditRound3.perturbed_B, `SL.AuditRound3.perturbed_coefficient_difference, `SL.AuditRound3.perturbed_m4_values, `SL.AuditRound3.old_m4_expression, `SL.AuditRound3.perturbed_m4_rejects_old_expression, `SL.AuditRound3.p2_moment_formula, `SL.AuditRound3.p2_image_moment_formula, `SL.AuditRound3.p2_delta_formula, `SL.AuditRound3.p2_moment_rational_identity, `SL.AuditRound3.p2_image_moment_rational_identity, `SL.AuditRound3.p2_perturbation_cancellation, `SL.AuditRound3.p2_delta_complement, `SL.AuditRound3.p2_delta_special_values]
  let Env := (← getEnv).setExporting false
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
      ("transitive_axioms", names_json Axioms)]
    Readable := Readable ++ kind_name Info ++ " " ++ Target.toString ++ " :
" ++ ActualType
    Explicit := Explicit ++ kind_name Info ++ " " ++ Target.toString ++ " :
" ++ FullType
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
        Readable := Readable ++ "
:=
" ++ Body
        Explicit := Explicit ++ "
:=
" ++ FullBody
    Readable := Readable ++ "

"
    Explicit := Explicit ++ "

"
    Results := Results.push (Json.mkObj Fields)
  let Used := dependency_closure Env Targets.toList
  let Nodes := Used.toArray.qsort Name.lt |>.map fun N =>
    node_json Env N (N.toString.startsWith "SL.AuditRound3.")
  let mut LocalDefinitions : String := ""
  for N in Used.toArray.qsort Name.lt do
    if N.toString.startsWith "SL.AuditRound3." then
      if let some Info := Env.checked.get.find? N then
        if !Info.isTheorem then
          if let some Value := Info.value? (allowOpaque := true) then
            let T ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
                return (← ppExpr Info.type).pretty
            let V ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
                return (← ppExpr Value).pretty
            LocalDefinitions := LocalDefinitions ++ N.toString ++ " :\n" ++ T ++ "\n:=\n" ++ V ++ "\n\n"
  let mut Modules : Array Json := #[]
  for N in Env.header.moduleNames do
    let File ← findOLean N
    Modules := Modules.push (Json.mkObj [("module", toJson N.toString), ("olean", toJson File.toString)])
  let Base := "F:/tools/math-audit-round3-20260920/lean-author/final/"
  IO.FS.writeFile (Base ++ "declarations.json")
    ((Json.mkObj [("declarations", Json.arr Results), ("dependencies", Json.arr Nodes)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "loaded-modules.json")
    ((Json.mkObj [("module_count", toJson Env.header.moduleNames.size), ("modules", Json.arr Modules)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "formal-statements.txt") Readable
  IO.FS.writeFile (Base ++ "formal-statements-fully-explicit.txt") Explicit
  IO.FS.writeFile (Base ++ "local-definition-closure.txt") LocalDefinitions
