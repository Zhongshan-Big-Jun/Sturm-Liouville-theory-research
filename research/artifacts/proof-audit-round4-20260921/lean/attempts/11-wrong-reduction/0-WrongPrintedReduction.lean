import SL.AuditRound4
import Lean
open SL.AuditRound4
open Lean Elab Command in
run_cmd do
  let P ← findOLean `SL.AuditRound4
  logInfo m!"CONTROL_ROOT={P}"

example : printed_reduction_residual = 0 := by
  rw [printed_reduction_counterexample]
  norm_num
