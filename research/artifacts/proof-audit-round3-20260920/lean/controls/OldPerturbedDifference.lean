import SL.AuditRound3

open SL.AuditRound3

example : perturbed_A 4 3 1 - perturbed_B 4 1 =
    4 * (4 : ℝ) + 3 * 4 / (4 - 1) + 3 * 1 := by
  norm_num [perturbed_A, perturbed_B]
