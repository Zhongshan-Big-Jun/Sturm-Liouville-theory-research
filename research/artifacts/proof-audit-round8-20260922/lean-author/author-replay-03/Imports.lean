import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Lean
open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let mut rows := #[]
  for name in env.header.moduleNames.qsort Name.lt do
    let path ← findOLean name
    rows := rows.push <| Json.mkObj [("module", toJson name.toString),("olean",toJson path.toString)]
  IO.FS.writeFile "F:\\tools\\math-audit-round8-20260922\\lean-author\\author-replay-03\\import-discovery.json" ((Json.arr rows).compress ++ "\n")
