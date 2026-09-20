import SL.AuditRound3

open SL.AuditRound3

example : recurrence_solution 1 (fun _ => 3) (fun _ => 2) 2 =
    product_bound 1 (fun _ => 3) (fun _ => 2) 2 := by
  norm_num [constant_recurrence_solution, constant_recurrence_product]
