import SL.AuditRound2

set_option pp.proofs false
set_option pp.universes true

#print SL.AuditRound2.second_difference
#print SL.AuditRound2.third_order_solution
#print SL.AuditRound2.k1_p
#print SL.AuditRound2.k1_q
#print SL.AuditRound2.k1_r
#print SL.AuditRound2.k1_scaled
#print SL.AuditRound2.k1_n3_segment
#print SL.AuditRound2.signed_transmission
#print SL.AuditRound2.cell_branch
#print SL.AuditRound2.second_sine_mode
#print SL.AuditRound2.candidate_theta
#print SL.AuditRound2.balanced_candidate

#print SL.AuditRound2.terminal_difference
#print axioms SL.AuditRound2.terminal_difference

#print SL.AuditRound2.difference_step_iff
#print axioms SL.AuditRound2.difference_step_iff

#print SL.AuditRound2.solution_difference_step
#print axioms SL.AuditRound2.solution_difference_step

#print SL.AuditRound2.factorial_shift_four
#print axioms SL.AuditRound2.factorial_shift_four

#print SL.AuditRound2.k1_terminal_value
#print axioms SL.AuditRound2.k1_terminal_value

#print SL.AuditRound2.k1_terminal_formula_pos
#print axioms SL.AuditRound2.k1_terminal_formula_pos

#print SL.AuditRound2.k1_n3_last_equation
#print axioms SL.AuditRound2.k1_n3_last_equation

#print SL.AuditRound2.k1_n3_difference
#print axioms SL.AuditRound2.k1_n3_difference

#print SL.AuditRound2.k1_n3_difference_ne_zero
#print axioms SL.AuditRound2.k1_n3_difference_ne_zero

#print SL.AuditRound2.mw_signed_slope_matching
#print axioms SL.AuditRound2.mw_signed_slope_matching

#print SL.AuditRound2.mw_transmission_ne_zero
#print axioms SL.AuditRound2.mw_transmission_ne_zero

#print SL.AuditRound2.mw_affine_has_deriv
#print axioms SL.AuditRound2.mw_affine_has_deriv

#print SL.AuditRound2.cell_branch_has_deriv
#print axioms SL.AuditRound2.cell_branch_has_deriv

#print SL.AuditRound2.mw_cell_interface
#print axioms SL.AuditRound2.mw_cell_interface

#print SL.AuditRound2.mw_affine_ode
#print axioms SL.AuditRound2.mw_affine_ode

#print SL.AuditRound2.mw_scaled_ratio
#print axioms SL.AuditRound2.mw_scaled_ratio

#print SL.AuditRound2.second_sine_mode_has_deriv
#print axioms SL.AuditRound2.second_sine_mode_has_deriv

#print SL.AuditRound2.second_sine_mode_endpoint_slopes
#print axioms SL.AuditRound2.second_sine_mode_endpoint_slopes

#print SL.AuditRound2.second_sine_mode_transmission
#print axioms SL.AuditRound2.second_sine_mode_transmission

#print SL.AuditRound2.attained_le_sup
#print axioms SL.AuditRound2.attained_le_sup

#print SL.AuditRound2.attained_sup_eq_iff_upper_bound
#print axioms SL.AuditRound2.attained_sup_eq_iff_upper_bound

#print SL.AuditRound2.balanced_candidate_le_sup
#print axioms SL.AuditRound2.balanced_candidate_le_sup

#print SL.AuditRound2.adjacent_ratio_le_of_doubled
#print axioms SL.AuditRound2.adjacent_ratio_le_of_doubled

#print SL.AuditRound2.attainment_doubling_countermodel
#print axioms SL.AuditRound2.attainment_doubling_countermodel

#print SL.AuditRound2.no_candidate_upper_bound_from_doubling
#print axioms SL.AuditRound2.no_candidate_upper_bound_from_doubling

open Lean Elab Command in
run_cmd do
  let Env ← getEnv
  let mut Modules : Array Json := #[]
  for Name in Env.header.moduleNames do
    let File ← findOLean Name
    Modules := Modules.push (Json.mkObj [
      ("module", toJson Name.toString), ("olean", toJson File.toString)])
  IO.FS.writeFile "F:/tools/math-audit-round2-20260920/lean-author/loaded-modules.json"
    ((Json.mkObj [("module_count", toJson Env.header.moduleNames.size),
      ("modules", Json.arr Modules)]).compress)
