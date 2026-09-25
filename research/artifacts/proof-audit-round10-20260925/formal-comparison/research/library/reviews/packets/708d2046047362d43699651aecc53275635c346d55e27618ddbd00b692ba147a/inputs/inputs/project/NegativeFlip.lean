import AuditRound10
open AuditRound10

example : (-J 1) ((-J 1) (fun _ => (1 : ℝ))) =
    (-J 1) (fun _ => (1 : ℝ)) := by
  funext i
  norm_num [J]
