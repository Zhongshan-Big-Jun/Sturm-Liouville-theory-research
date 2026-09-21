import LeanVerifyProbe
import SL.AuditRound6
set_option maxRecDepth 100000
set_option maxHeartbeats 0
open Lean Elab Command Meta LeanVerifyV2 in
run_cmd do
  let Env := (← getEnv).setExporting false
  let Targets : Array Name := #[`SL.AuditRound6.sparse_generators, `SL.AuditRound6.sparse_span, `SL.AuditRound6.augmented_generators, `SL.AuditRound6.augmented_span, `SL.AuditRound6.sparse_span_le_krein, `SL.AuditRound6.X_sq_not_mem_sparse_span, `SL.AuditRound6.even_power_mem_augmented, `SL.AuditRound6.odd_power_mem_augmented, `SL.AuditRound6.power_mem_augmented, `SL.AuditRound6.polynomial_mem_augmented, `SL.AuditRound6.augmented_span_eq_top, `SL.AuditRound6.four_traces, `SL.AuditRound6.four_traces_apply, `SL.AuditRound6.trace_matrix, `SL.AuditRound6.inverse_matrix, `SL.AuditRound6.four_trace_monomial_columns, `SL.AuditRound6.trace_matrix_det, `SL.AuditRound6.trace_matrix_two_sided_inverse, `SL.AuditRound6.monomial_lift, `SL.AuditRound6.four_traces_monomial_lift, `SL.AuditRound6.four_trace_lift, `SL.AuditRound6.four_trace_right_inverse, `SL.AuditRound6.correct_four_traces, `SL.AuditRound6.corrected_four_traces_zero, `SL.AuditRound6.correction_fixes_kernel, `SL.AuditRound6.cancellation, `SL.AuditRound6.cancellation_formula, `SL.AuditRound6.cancellation_four_traces_zero, `SL.AuditRound6.p_four_four_traces, `SL.AuditRound6.p_four_four_traces_ne_zero, `SL.AuditRound6.detector, `SL.AuditRound6.witness, `SL.AuditRound6.coordinate_zero, `SL.AuditRound6.coordinate_one, `SL.AuditRound6.coordinate_detection_counterexample, `SL.AuditRound6.local_algebra_root]
  let Out := "F:\\tools\\math-audit-round6-20260921\\lean-author\\replay-author-02"
  let mut Results : Array Json := #[]
  let mut Readable := ""
  for Target in Targets do
    let some Info := Env.checked.get.find? Target
      | throwError "Missing public declaration: {Target}"
    let ActualType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.universes true |>.setBool `pp.fullNames true) do
        return (← ppExpr Info.type).pretty
    let FullType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
        return (← ppExpr Info.type).pretty
    let Axioms ← collectAxioms Target
    Results := Results.push <| Json.mkObj [
      ("declaration", toJson Target.toString), ("kind", toJson (kind_name Info)),
      ("actual_type", toJson ActualType), ("fully_explicit_type", toJson FullType),
      ("type_expression", expr_json Info.type),
      ("universes", toJson (Info.levelParams.map Name.toString)),
      ("binder_kinds", toJson (binder_kinds Info.type)),
      ("transitive_axioms", names_json Axioms),
      ("type_dependencies", names_json Info.type.getUsedConstants),
      ("body_dependencies", names_json (body_dependencies Info))]
    Readable := Readable ++ kind_name Info ++ " " ++ Target.toString ++ " :\n" ++ ActualType ++ "\n\n"
  let Used := dependency_closure Env Targets.toList
  let Nodes := Used.toArray.qsort Name.lt |>.map fun N => node_json Env N false
  let mut Definitions : Array Json := #[]
  let mut DefinitionText := ""
  for N in Used.toArray.qsort Name.lt do
    if N.toString.startsWith "SL." then
      if let some Info := Env.checked.get.find? N then
        if !Info.isTheorem then
          if let some Value := Info.value? (allowOpaque := true) then
            let T ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.fullNames true |>.setBool `pp.universes true) do
                return (← ppExpr Info.type).pretty
            let V ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.fullNames true |>.setBool `pp.universes true) do
                return (← ppExpr Value).pretty
            Definitions := Definitions.push <| Json.mkObj [
              ("name", toJson N.toString), ("type", toJson T), ("body", toJson V),
              ("type_expression", expr_json Info.type), ("value_expression", expr_json Value)]
            DefinitionText := DefinitionText ++ N.toString ++ " :\n" ++ T ++ "\n:=\n" ++ V ++ "\n\n"
  IO.FS.writeFile (Out ++ "/public-declarations.json") ((Json.arr Results).compress ++ "\n")
  IO.FS.writeFile (Out ++ "/public-types.txt") Readable
  IO.FS.writeFile (Out ++ "/shared-public-dependency-graph.json") ((Json.arr Nodes).compress ++ "\n")
  IO.FS.writeFile (Out ++ "/local-definitions.json") ((Json.arr Definitions).compress ++ "\n")
  IO.FS.writeFile (Out ++ "/local-definitions.txt") DefinitionText
