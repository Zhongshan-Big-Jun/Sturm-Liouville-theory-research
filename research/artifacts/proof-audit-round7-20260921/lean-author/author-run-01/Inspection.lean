import Lean
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.fullNames true
#check SL.AuditRound7.normalized_mode
#print axioms SL.AuditRound7.normalized_mode
#print SL.AuditRound7.normalized_mode
#check SL.AuditRound7.normalized_mode_slope
#print axioms SL.AuditRound7.normalized_mode_slope
#print SL.AuditRound7.normalized_mode_slope
#check SL.AuditRound7.normalized_mode_has_deriv
#print axioms SL.AuditRound7.normalized_mode_has_deriv
#check SL.AuditRound7.wronskian
#print axioms SL.AuditRound7.wronskian
#print SL.AuditRound7.wronskian
#check SL.AuditRound7.wronskian_is_derivative_expression
#print axioms SL.AuditRound7.wronskian_is_derivative_expression
#check SL.AuditRound7.trig_product_to_sum
#print axioms SL.AuditRound7.trig_product_to_sum
#check SL.AuditRound7.wronskian_product_to_sum
#print axioms SL.AuditRound7.wronskian_product_to_sum
#check SL.AuditRound7.sin_square_sum
#print axioms SL.AuditRound7.sin_square_sum
#print SL.AuditRound7.sin_square_sum
#check SL.AuditRound7.sin_odd_step
#print axioms SL.AuditRound7.sin_odd_step
#check SL.AuditRound7.finite_sin_square
#print axioms SL.AuditRound7.finite_sin_square
#check SL.AuditRound7.wronskian_finite_sum
#print axioms SL.AuditRound7.wronskian_finite_sum
#check SL.AuditRound7.sin_square_sum_pos
#print axioms SL.AuditRound7.sin_square_sum_pos
#check SL.AuditRound7.wronskian_neg
#print axioms SL.AuditRound7.wronskian_neg
#check SL.AuditRound7.wronskian_two_half
#print axioms SL.AuditRound7.wronskian_two_half
#check SL.AuditRound7.old_wronskian_two_half
#print axioms SL.AuditRound7.old_wronskian_two_half
#check SL.AuditRound7.old_wronskian_counterexample
#print axioms SL.AuditRound7.old_wronskian_counterexample
#check SL.AuditRound7.endpoint_coefficient
#print axioms SL.AuditRound7.endpoint_coefficient
#print SL.AuditRound7.endpoint_coefficient
#check SL.AuditRound7.endpoint_coefficient_algebra
#print axioms SL.AuditRound7.endpoint_coefficient_algebra
#check SL.AuditRound7.endpoint_coefficient_expanded
#print axioms SL.AuditRound7.endpoint_coefficient_expanded
#check SL.AuditRound7.endpoint_coefficient_neg
#print axioms SL.AuditRound7.endpoint_coefficient_neg
#check SL.AuditRound7.fh_term
#print axioms SL.AuditRound7.fh_term
#print SL.AuditRound7.fh_term
#check SL.AuditRound7.gap_switch
#print axioms SL.AuditRound7.gap_switch
#print SL.AuditRound7.gap_switch
#check SL.AuditRound7.mirrored_pair_from_single_interface
#print axioms SL.AuditRound7.mirrored_pair_from_single_interface
#check SL.AuditRound7.mirrored_gap_from_single_interface
#print axioms SL.AuditRound7.mirrored_gap_from_single_interface
#check SL.AuditRound7.mirrored_stationarity_iff
#print axioms SL.AuditRound7.mirrored_stationarity_iff
#check SL.AuditRound7.old_mirror_factor_counterexample
#print axioms SL.AuditRound7.old_mirror_factor_counterexample
#check SL.AuditRound7.local_algebra_root
#print axioms SL.AuditRound7.local_algebra_root
open Lean Elab Command in
run_cmd do
  let Env := (← getEnv).setExporting false
  let Targets : Array Name := #[`SL.AuditRound7.normalized_mode, `SL.AuditRound7.normalized_mode_slope, `SL.AuditRound7.normalized_mode_has_deriv, `SL.AuditRound7.wronskian, `SL.AuditRound7.wronskian_is_derivative_expression, `SL.AuditRound7.trig_product_to_sum, `SL.AuditRound7.wronskian_product_to_sum, `SL.AuditRound7.sin_square_sum, `SL.AuditRound7.sin_odd_step, `SL.AuditRound7.finite_sin_square, `SL.AuditRound7.wronskian_finite_sum, `SL.AuditRound7.sin_square_sum_pos, `SL.AuditRound7.wronskian_neg, `SL.AuditRound7.wronskian_two_half, `SL.AuditRound7.old_wronskian_two_half, `SL.AuditRound7.old_wronskian_counterexample, `SL.AuditRound7.endpoint_coefficient, `SL.AuditRound7.endpoint_coefficient_algebra, `SL.AuditRound7.endpoint_coefficient_expanded, `SL.AuditRound7.endpoint_coefficient_neg, `SL.AuditRound7.fh_term, `SL.AuditRound7.gap_switch, `SL.AuditRound7.mirrored_pair_from_single_interface, `SL.AuditRound7.mirrored_gap_from_single_interface, `SL.AuditRound7.mirrored_stationarity_iff, `SL.AuditRound7.old_mirror_factor_counterexample, `SL.AuditRound7.local_algebra_root]
  let mut Results : Array Json := #[]
  for Target in Targets do
    let some Info := Env.checked.get.find? Target | throwError "Missing public declaration: {Target}"
    let Type ← liftTermElabM <| withOptions (fun O => O.setBool `pp.universes true |>.setBool `pp.fullNames true) do
      return (← ppExpr Info.type).pretty
    let Axioms ← collectAxioms Target
    Results := Results.push <| Json.mkObj [
      ("declaration", toJson Target.toString), ("actual_type", toJson Type),
      ("is_theorem", toJson Info.isTheorem),
      ("universes", toJson (Info.levelParams.map Name.toString)),
      ("transitive_axioms", toJson (Axioms.toList.map Name.toString))]
  IO.FS.writeFile "F:\\tools\\math-audit-round7-20260921\\lean-author\\author-run-01\\public-declarations.json" ((Json.arr Results).pretty ++ "\n")
