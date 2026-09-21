import SL.AuditRound5
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

#print SL.AuditRound5.p_zero
#print axioms SL.AuditRound5.p_zero

#print SL.AuditRound5.p_one
#print axioms SL.AuditRound5.p_one

#print SL.AuditRound5.p_even
#print axioms SL.AuditRound5.p_even

#print SL.AuditRound5.p_odd
#print axioms SL.AuditRound5.p_odd

#print SL.AuditRound5.eval_linear
#print axioms SL.AuditRound5.eval_linear

#print SL.AuditRound5.value_trace
#print axioms SL.AuditRound5.value_trace

#print SL.AuditRound5.derivative_trace
#print axioms SL.AuditRound5.derivative_trace

#print SL.AuditRound5.traces
#print axioms SL.AuditRound5.traces

#print SL.AuditRound5.zero_traces
#print axioms SL.AuditRound5.zero_traces

#print SL.AuditRound5.oblique
#print axioms SL.AuditRound5.oblique

#print SL.AuditRound5.endpoint_plus
#print axioms SL.AuditRound5.endpoint_plus

#print SL.AuditRound5.endpoint_minus
#print axioms SL.AuditRound5.endpoint_minus

#print SL.AuditRound5.residues
#print axioms SL.AuditRound5.residues

#print SL.AuditRound5.krein_polynomials
#print axioms SL.AuditRound5.krein_polynomials

#print SL.AuditRound5.high_generators
#print axioms SL.AuditRound5.high_generators

#print SL.AuditRound5.high_span
#print axioms SL.AuditRound5.high_span

#print SL.AuditRound5.traces_apply
#print axioms SL.AuditRound5.traces_apply

#print SL.AuditRound5.residues_apply
#print axioms SL.AuditRound5.residues_apply

#print SL.AuditRound5.mem_zero_traces
#print axioms SL.AuditRound5.mem_zero_traces

#print SL.AuditRound5.mem_oblique
#print axioms SL.AuditRound5.mem_oblique

#print SL.AuditRound5.low_traces
#print axioms SL.AuditRound5.low_traces

#print SL.AuditRound5.low_residues
#print axioms SL.AuditRound5.low_residues

#print SL.AuditRound5.even_traces
#print axioms SL.AuditRound5.even_traces

#print SL.AuditRound5.odd_traces
#print axioms SL.AuditRound5.odd_traces

#print SL.AuditRound5.monomial_even_residues
#print axioms SL.AuditRound5.monomial_even_residues

#print SL.AuditRound5.monomial_odd_residues
#print axioms SL.AuditRound5.monomial_odd_residues

#print SL.AuditRound5.residues_C_mul
#print axioms SL.AuditRound5.residues_C_mul

#print SL.AuditRound5.even_residues
#print axioms SL.AuditRound5.even_residues

#print SL.AuditRound5.odd_residues
#print axioms SL.AuditRound5.odd_residues

#print SL.AuditRound5.high_span_zero_traces
#print axioms SL.AuditRound5.high_span_zero_traces

#print SL.AuditRound5.high_span_krein
#print axioms SL.AuditRound5.high_span_krein

#print SL.AuditRound5.span_member_has_zero_traces
#print axioms SL.AuditRound5.span_member_has_zero_traces

#print SL.AuditRound5.one_add_X_mem_oblique
#print axioms SL.AuditRound5.one_add_X_mem_oblique

#print SL.AuditRound5.one_not_mem_oblique
#print axioms SL.AuditRound5.one_not_mem_oblique

#print SL.AuditRound5.X_not_mem_oblique
#print axioms SL.AuditRound5.X_not_mem_oblique

#print SL.AuditRound5.one_add_X_not_mem_high_span
#print axioms SL.AuditRound5.one_add_X_not_mem_high_span

#print SL.AuditRound5.zero_traces_le_oblique
#print axioms SL.AuditRound5.zero_traces_le_oblique

#print SL.AuditRound5.high_span_lt_oblique
#print axioms SL.AuditRound5.high_span_lt_oblique

#print SL.AuditRound5.endpoint_matrix
#print axioms SL.AuditRound5.endpoint_matrix

#print SL.AuditRound5.correction_matrix
#print axioms SL.AuditRound5.correction_matrix

#print SL.AuditRound5.endpoint_matrix_det
#print axioms SL.AuditRound5.endpoint_matrix_det

#print SL.AuditRound5.endpoint_matrix_det_ne_zero
#print axioms SL.AuditRound5.endpoint_matrix_det_ne_zero

#print SL.AuditRound5.endpoint_matrix_inverse
#print axioms SL.AuditRound5.endpoint_matrix_inverse

#print SL.AuditRound5.endpoint_monomial_columns
#print axioms SL.AuditRound5.endpoint_monomial_columns

#print SL.AuditRound5.correction_alpha
#print axioms SL.AuditRound5.correction_alpha

#print SL.AuditRound5.correction_beta
#print axioms SL.AuditRound5.correction_beta

#print SL.AuditRound5.correction_solves_residues
#print axioms SL.AuditRound5.correction_solves_residues

#print SL.AuditRound5.correct_endpoints
#print axioms SL.AuditRound5.correct_endpoints

#print SL.AuditRound5.corrected_residues_zero
#print axioms SL.AuditRound5.corrected_residues_zero

#print SL.AuditRound5.correction_preserves_divisibility
#print axioms SL.AuditRound5.correction_preserves_divisibility

#print SL.AuditRound5.trace_lift
#print axioms SL.AuditRound5.trace_lift

#print SL.AuditRound5.traces_trace_lift
#print axioms SL.AuditRound5.traces_trace_lift

#print SL.AuditRound5.trace_lift_krein
#print axioms SL.AuditRound5.trace_lift_krein

#print SL.AuditRound5.traces_surjective
#print axioms SL.AuditRound5.traces_surjective

#print SL.AuditRound5.subtract_trace_lift
#print axioms SL.AuditRound5.subtract_trace_lift

#print SL.AuditRound5.trace_membership_iff
#print axioms SL.AuditRound5.trace_membership_iff

#print SL.AuditRound5.oblique_with_krein_witness
#print axioms SL.AuditRound5.oblique_with_krein_witness

#print SL.AuditRound5.high_span_lt_krein_oblique
#print axioms SL.AuditRound5.high_span_lt_krein_oblique

#print SL.AuditRound5.local_algebra_root
#print axioms SL.AuditRound5.local_algebra_root

open Lean Elab Command Meta AuthorInspection in
run_cmd do
  let Targets : Array Name := #[`SL.AuditRound5.p_zero, `SL.AuditRound5.p_one, `SL.AuditRound5.p_even, `SL.AuditRound5.p_odd, `SL.AuditRound5.eval_linear, `SL.AuditRound5.value_trace, `SL.AuditRound5.derivative_trace, `SL.AuditRound5.traces, `SL.AuditRound5.zero_traces, `SL.AuditRound5.oblique, `SL.AuditRound5.endpoint_plus, `SL.AuditRound5.endpoint_minus, `SL.AuditRound5.residues, `SL.AuditRound5.krein_polynomials, `SL.AuditRound5.high_generators, `SL.AuditRound5.high_span, `SL.AuditRound5.traces_apply, `SL.AuditRound5.residues_apply, `SL.AuditRound5.mem_zero_traces, `SL.AuditRound5.mem_oblique, `SL.AuditRound5.low_traces, `SL.AuditRound5.low_residues, `SL.AuditRound5.even_traces, `SL.AuditRound5.odd_traces, `SL.AuditRound5.monomial_even_residues, `SL.AuditRound5.monomial_odd_residues, `SL.AuditRound5.residues_C_mul, `SL.AuditRound5.even_residues, `SL.AuditRound5.odd_residues, `SL.AuditRound5.high_span_zero_traces, `SL.AuditRound5.high_span_krein, `SL.AuditRound5.span_member_has_zero_traces, `SL.AuditRound5.one_add_X_mem_oblique, `SL.AuditRound5.one_not_mem_oblique, `SL.AuditRound5.X_not_mem_oblique, `SL.AuditRound5.one_add_X_not_mem_high_span, `SL.AuditRound5.zero_traces_le_oblique, `SL.AuditRound5.high_span_lt_oblique, `SL.AuditRound5.endpoint_matrix, `SL.AuditRound5.correction_matrix, `SL.AuditRound5.endpoint_matrix_det, `SL.AuditRound5.endpoint_matrix_det_ne_zero, `SL.AuditRound5.endpoint_matrix_inverse, `SL.AuditRound5.endpoint_monomial_columns, `SL.AuditRound5.correction_alpha, `SL.AuditRound5.correction_beta, `SL.AuditRound5.correction_solves_residues, `SL.AuditRound5.correct_endpoints, `SL.AuditRound5.corrected_residues_zero, `SL.AuditRound5.correction_preserves_divisibility, `SL.AuditRound5.trace_lift, `SL.AuditRound5.traces_trace_lift, `SL.AuditRound5.trace_lift_krein, `SL.AuditRound5.traces_surjective, `SL.AuditRound5.subtract_trace_lift, `SL.AuditRound5.trace_membership_iff, `SL.AuditRound5.oblique_with_krein_witness, `SL.AuditRound5.high_span_lt_krein_oblique, `SL.AuditRound5.local_algebra_root]
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
  let Base := "F:/tools/math-audit-round5-20260921/lean-replay/final/"
  IO.FS.writeFile (Base ++ "declarations.json")
    ((Json.mkObj [("declarations", Json.arr Results), ("dependencies", Json.arr Nodes), ("semantic_dependencies", names_json SemanticUsed.toArray)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "loaded-modules.json")
    ((Json.mkObj [("module_count", toJson Env.header.moduleNames.size), ("modules", Json.arr Modules)]).compress ++ "\n")
  IO.FS.writeFile (Base ++ "formal-statements.txt") Readable
  IO.FS.writeFile (Base ++ "formal-statements-fully-explicit.txt") Explicit
  IO.FS.writeFile (Base ++ "local-definition-closure.txt") LocalDefinitions
