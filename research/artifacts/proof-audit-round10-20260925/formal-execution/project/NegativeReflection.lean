import AuditRound10
open AuditRound10

example : reflect ((0 : Vec 1) + (fun _ => (1 : ℝ))) =
    reflect (0 : Vec 1) + J 1 (fun _ => (1 : ℝ)) := by
  funext i
  norm_num [reflect, J]
