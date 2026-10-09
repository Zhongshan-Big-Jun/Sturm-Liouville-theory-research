import Lean
set_option pp.maxSteps 10000000
set_option pp.deepTerms true
set_option pp.proofs true
set_option maxRecDepth 8192
open Lean Elab Command
run_cmd do
  let Options ← getOptions
  IO.println s!"maxSteps={Lean.getPPMaxSteps Options} deepTerms={Lean.getPPDeepTerms Options} proofs={Lean.getPPProofs Options} maxRecDepth={Options.get `maxRecDepth (0 : Nat)}"
