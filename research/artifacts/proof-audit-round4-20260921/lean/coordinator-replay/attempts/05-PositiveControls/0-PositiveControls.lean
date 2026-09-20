import SL.AuditRound4
import Lean
open SL.AuditRound4
open Lean Elab Command in
run_cmd do
  let P ← findOLean `SL.AuditRound4
  logInfo m!"CONTROL_ROOT={P}"

example : printed_reduction_residual = 69 / 224 := printed_reduction_counterexample
example : printed_reduction_residual ≠ 0 := by
  rw [printed_reduction_counterexample]
  norm_num
example : table_ratio (-1 / 4) (-3 / 8) (-3 / 4) 0 1 = 1 + 1 / (2 * (1 : ℚ)) := by
  norm_num [table_ratio]
example : table_ratio (-1 / 4) (-1 / 8) (-3 / 4) 0 1 ≠ 1 + 1 / (2 * (1 : ℚ)) := by
  norm_num [table_ratio]
