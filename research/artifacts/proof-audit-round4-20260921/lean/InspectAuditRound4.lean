import SL.AuditRound4
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

#print SL.AuditRound4.second_difference
#print axioms SL.AuditRound4.second_difference

#print SL.AuditRound4.recurrence_iff_second_difference
#print axioms SL.AuditRound4.recurrence_iff_second_difference

#print SL.AuditRound4.affine_second_difference
#print axioms SL.AuditRound4.affine_second_difference

#print SL.AuditRound4.affine_solution
#print axioms SL.AuditRound4.affine_solution

#print SL.AuditRound4.zero_second_difference_iff_affine
#print axioms SL.AuditRound4.zero_second_difference_iff_affine

#print SL.AuditRound4.difference_proportional
#print axioms SL.AuditRound4.difference_proportional

#print SL.AuditRound4.first_difference_sum
#print axioms SL.AuditRound4.first_difference_sum

#print SL.AuditRound4.reconstruct_second_difference
#print axioms SL.AuditRound4.reconstruct_second_difference

#print SL.AuditRound4.reduction_residual_identity
#print axioms SL.AuditRound4.reduction_residual_identity

#print SL.AuditRound4.reduction_product_iff
#print axioms SL.AuditRound4.reduction_product_iff

#print SL.AuditRound4.reduction_iff
#print axioms SL.AuditRound4.reduction_iff

#print SL.AuditRound4.integrate_from_zero
#print axioms SL.AuditRound4.integrate_from_zero

#print SL.AuditRound4.integrate_initial
#print axioms SL.AuditRound4.integrate_initial

#print SL.AuditRound4.integrate_increment
#print axioms SL.AuditRound4.integrate_increment

#print SL.AuditRound4.reduction_reconstruction
#print axioms SL.AuditRound4.reduction_reconstruction

#print SL.AuditRound4.p
#print axioms SL.AuditRound4.p

#print SL.AuditRound4.q
#print axioms SL.AuditRound4.q

#print SL.AuditRound4.r
#print axioms SL.AuditRound4.r

#print SL.AuditRound4.theta
#print axioms SL.AuditRound4.theta

#print SL.AuditRound4.factorial_step
#print axioms SL.AuditRound4.factorial_step

#print SL.AuditRound4.factorial_weight
#print axioms SL.AuditRound4.factorial_weight

#print SL.AuditRound4.factorial_weight_ne_zero
#print axioms SL.AuditRound4.factorial_weight_ne_zero

#print SL.AuditRound4.factorial_weight_succ
#print axioms SL.AuditRound4.factorial_weight_succ

#print SL.AuditRound4.factorial_step_ne_zero
#print axioms SL.AuditRound4.factorial_step_ne_zero

#print SL.AuditRound4.parity_coefficient_factors
#print axioms SL.AuditRound4.parity_coefficient_factors

#print SL.AuditRound4.scale_factor
#print axioms SL.AuditRound4.scale_factor

#print SL.AuditRound4.scaled_sequence
#print axioms SL.AuditRound4.scaled_sequence

#print SL.AuditRound4.moment_solution
#print axioms SL.AuditRound4.moment_solution

#print SL.AuditRound4.scale_factor_ne_zero
#print axioms SL.AuditRound4.scale_factor_ne_zero

#print SL.AuditRound4.scale_factor_succ
#print axioms SL.AuditRound4.scale_factor_succ

#print SL.AuditRound4.conjugate_solution_iff
#print axioms SL.AuditRound4.conjugate_solution_iff

#print SL.AuditRound4.scaled_coefficients
#print axioms SL.AuditRound4.scaled_coefficients

#print SL.AuditRound4.moment_iff_normalized
#print axioms SL.AuditRound4.moment_iff_normalized

#print SL.AuditRound4.moment_iff_scaled
#print axioms SL.AuditRound4.moment_iff_scaled

#print SL.AuditRound4.moment_iff_second_difference
#print axioms SL.AuditRound4.moment_iff_second_difference

#print SL.AuditRound4.difference_weight
#print axioms SL.AuditRound4.difference_weight

#print SL.AuditRound4.difference_weight_ne_zero
#print axioms SL.AuditRound4.difference_weight_ne_zero

#print SL.AuditRound4.difference_weight_recurrence
#print axioms SL.AuditRound4.difference_weight_recurrence

#print SL.AuditRound4.moment_difference_formula
#print axioms SL.AuditRound4.moment_difference_formula

#print SL.AuditRound4.moment_finite_reconstruction
#print axioms SL.AuditRound4.moment_finite_reconstruction

#print SL.AuditRound4.affine_moment
#print axioms SL.AuditRound4.affine_moment

#print SL.AuditRound4.scaled_affine_moment
#print axioms SL.AuditRound4.scaled_affine_moment

#print SL.AuditRound4.affine_moment_solution
#print axioms SL.AuditRound4.affine_moment_solution

#print SL.AuditRound4.normalized_solution_with_zero_term
#print axioms SL.AuditRound4.normalized_solution_with_zero_term

#print SL.AuditRound4.table_ratio
#print axioms SL.AuditRound4.table_ratio

#print SL.AuditRound4.table_cancellation
#print axioms SL.AuditRound4.table_cancellation

#print SL.AuditRound4.missed_table_parameter
#print axioms SL.AuditRound4.missed_table_parameter

#print SL.AuditRound4.missed_table_not_in_old_branches
#print axioms SL.AuditRound4.missed_table_not_in_old_branches

#print SL.AuditRound4.legendre2
#print axioms SL.AuditRound4.legendre2

#print SL.AuditRound4.legendre3
#print axioms SL.AuditRound4.legendre3

#print SL.AuditRound4.low_mode_representative_differences
#print axioms SL.AuditRound4.low_mode_representative_differences

#print SL.AuditRound4.low_mode_difference_nonzero
#print axioms SL.AuditRound4.low_mode_difference_nonzero

#print SL.AuditRound4.a4
#print axioms SL.AuditRound4.a4

#print SL.AuditRound4.a6
#print axioms SL.AuditRound4.a6

#print SL.AuditRound4.coefficient_step
#print axioms SL.AuditRound4.coefficient_step

#print SL.AuditRound4.remainder_coefficients_from_initials
#print axioms SL.AuditRound4.remainder_coefficients_from_initials

#print SL.AuditRound4.remainder_identity
#print axioms SL.AuditRound4.remainder_identity

#print SL.AuditRound4.remainder_unbounded_on_reciprocals
#print axioms SL.AuditRound4.remainder_unbounded_on_reciprocals

#print SL.AuditRound4.even_z_plus
#print axioms SL.AuditRound4.even_z_plus

#print SL.AuditRound4.even_z_minus
#print axioms SL.AuditRound4.even_z_minus

#print SL.AuditRound4.example_ratio_difference
#print axioms SL.AuditRound4.example_ratio_difference

#print SL.AuditRound4.printed_reduction_residual
#print axioms SL.AuditRound4.printed_reduction_residual

#print SL.AuditRound4.printed_reduction_counterexample
#print axioms SL.AuditRound4.printed_reduction_counterexample

#print SL.AuditRound4.corrected_reduction_same_data
#print axioms SL.AuditRound4.corrected_reduction_same_data

open Lean Elab Command Meta AuthorInspection in
run_cmd do
  let Targets : Array Name := #[`SL.AuditRound4.second_difference, `SL.AuditRound4.recurrence_iff_second_difference, `SL.AuditRound4.affine_second_difference, `SL.AuditRound4.affine_solution, `SL.AuditRound4.zero_second_difference_iff_affine, `SL.AuditRound4.difference_proportional, `SL.AuditRound4.first_difference_sum, `SL.AuditRound4.reconstruct_second_difference, `SL.AuditRound4.reduction_residual_identity, `SL.AuditRound4.reduction_product_iff, `SL.AuditRound4.reduction_iff, `SL.AuditRound4.integrate_from_zero, `SL.AuditRound4.integrate_initial, `SL.AuditRound4.integrate_increment, `SL.AuditRound4.reduction_reconstruction, `SL.AuditRound4.p, `SL.AuditRound4.q, `SL.AuditRound4.r, `SL.AuditRound4.theta, `SL.AuditRound4.factorial_step, `SL.AuditRound4.factorial_weight, `SL.AuditRound4.factorial_weight_ne_zero, `SL.AuditRound4.factorial_weight_succ, `SL.AuditRound4.factorial_step_ne_zero, `SL.AuditRound4.parity_coefficient_factors, `SL.AuditRound4.scale_factor, `SL.AuditRound4.scaled_sequence, `SL.AuditRound4.moment_solution, `SL.AuditRound4.scale_factor_ne_zero, `SL.AuditRound4.scale_factor_succ, `SL.AuditRound4.conjugate_solution_iff, `SL.AuditRound4.scaled_coefficients, `SL.AuditRound4.moment_iff_normalized, `SL.AuditRound4.moment_iff_scaled, `SL.AuditRound4.moment_iff_second_difference, `SL.AuditRound4.difference_weight, `SL.AuditRound4.difference_weight_ne_zero, `SL.AuditRound4.difference_weight_recurrence, `SL.AuditRound4.moment_difference_formula, `SL.AuditRound4.moment_finite_reconstruction, `SL.AuditRound4.affine_moment, `SL.AuditRound4.scaled_affine_moment, `SL.AuditRound4.affine_moment_solution, `SL.AuditRound4.normalized_solution_with_zero_term, `SL.AuditRound4.table_ratio, `SL.AuditRound4.table_cancellation, `SL.AuditRound4.missed_table_parameter, `SL.AuditRound4.missed_table_not_in_old_branches, `SL.AuditRound4.legendre2, `SL.AuditRound4.legendre3, `SL.AuditRound4.low_mode_representative_differences, `SL.AuditRound4.low_mode_difference_nonzero, `SL.AuditRound4.a4, `SL.AuditRound4.a6, `SL.AuditRound4.coefficient_step, `SL.AuditRound4.remainder_coefficients_from_initials, `SL.AuditRound4.remainder_identity, `SL.AuditRound4.remainder_unbounded_on_reciprocals, `SL.AuditRound4.even_z_plus, `SL.AuditRound4.even_z_minus, `SL.AuditRound4.example_ratio_difference, `SL.AuditRound4.printed_reduction_residual, `SL.AuditRound4.printed_reduction_counterexample, `SL.AuditRound4.corrected_reduction_same_data]
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
      ("transitive_axioms", names_json Axioms),
      ("type_dependencies", names_json Info.type.getUsedConstants),
      ("body_dependencies", names_json (body_dependencies Info)),
      ("transitive_dependencies", names_json (dependency_closure Env [Target]).toArray),
      ("semantic_dependencies", names_json (semantic_closure Env Info.type.getUsedConstants.toList).toArray)]
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
            LocalDefinitions := LocalDefinitions ++ N.toString ++ " :\n" ++ T ++ "\n:=\n" ++ V ++ "\n\n"
  let mut Modules : Array Json := #[]
  for N in Env.header.moduleNames do
    let File ← findOLean N
    Modules := Modules.push (Json.mkObj [("module", toJson N.toString), ("olean", toJson File.toString)])
  let Base := "F:/tools/math-audit-round4-20260921/lean-author/final/"
  IO.FS.writeFile (Base ++ "declarations.json")
    ((Json.mkObj [("declarations", Json.arr Results), ("dependencies", Json.arr Nodes), ("semantic_dependencies", names_json SemanticUsed.toArray)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "loaded-modules.json")
    ((Json.mkObj [("module_count", toJson Env.header.moduleNames.size), ("modules", Json.arr Modules)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "formal-statements.txt") Readable
  IO.FS.writeFile (Base ++ "formal-statements-fully-explicit.txt") Explicit
  IO.FS.writeFile (Base ++ "local-definition-closure.txt") LocalDefinitions
