import Lean
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.fullNames true
set_option pp.all true
open Lean Elab Command Meta
run_cmd do
  let env := (← getEnv).setExporting false
  let mut rows : Array Json := #[]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.header.moduleNames[idx.toNat]! == `SL.AuditRound7 then
        let typ ← liftTermElabM do return (← ppExpr info.type).pretty
        let val ← match info.value? (allowOpaque := true) with
          | some v => if info.isTheorem then pure Json.null else do
              let p ← liftTermElabM do return (← ppExpr v).pretty
              pure <| Json.mkObj [("pretty", toJson p), ("expression", toJson (reprStr v))]
          | none => pure Json.null
        let axioms ← collectAxioms name
        rows := rows.push <| Json.mkObj [
          ("declaration", toJson name.toString),
          ("is_theorem", toJson info.isTheorem),
          ("is_unsafe", toJson info.isUnsafe),
          ("is_internal_name", toJson name.isInternal),
          ("universes", toJson (info.levelParams.map Name.toString)),
          ("actual_type", toJson typ),
          ("type_expression", toJson (reprStr info.type)),
          ("definition", val),
          ("transitive_axioms", toJson (axioms.map Name.toString))]
  let resolved ← findOLean `SL.AuditRound7
  let result := Json.mkObj [
    ("module", toJson "SL.AuditRound7"),
    ("resolved_olean", toJson resolved.toString),
    ("owned_constant_count", toJson rows.size),
    ("declarations", Json.arr rows)]
  IO.FS.writeFile "F:\\tools\\math-audit-round7-20260921\\independent-execution\\lean-package\\independent-positive-negative-20260921\\all-module-declarations.json" (result.pretty ++ "\n")
example : (∀ (n : ℕ) (x : ℝ), HasDerivAt (SL.AuditRound7.normalized_mode n) (SL.AuditRound7.normalized_mode_slope n x) x) ∧
    (∀ (n : ℕ) (x : ℝ), SL.AuditRound7.wronskian n x = Real.pi *
      (Real.sin ((2 * (n : ℝ) + 1) * (Real.pi * x)) -
        (2 * (n : ℝ) + 1) * Real.sin (Real.pi * x))) ∧
    (∀ (n : ℕ) (t : ℝ), Real.sin ((2 * (n : ℝ) + 1) * t) -
      (2 * (n : ℝ) + 1) * Real.sin t = -4 * Real.sin t * SL.AuditRound7.sin_square_sum n t) ∧
    (∀ (n : ℕ), 0 < n → ∀ (x : ℝ), 0 < x → x < 1 → SL.AuditRound7.wronskian n x < 0) ∧
    (SL.AuditRound7.wronskian 2 (1 / 2) = -4 * Real.pi) ∧
    (SL.AuditRound7.wronskian 2 (1 / 2) ≠ -2 * ((2 : ℝ) + 1) * Real.pi * Real.sin (Real.pi * (1 / 2))) ∧
    (∀ (n : ℕ), ((n : ℝ) * Real.pi) ^ 2 * (Real.sqrt 2 * ((n : ℝ) * Real.pi)) ^ 2 -
      (((n : ℝ) + 1) * Real.pi) ^ 2 * (Real.sqrt 2 * (((n : ℝ) + 1) * Real.pi)) ^ 2 =
        SL.AuditRound7.endpoint_coefficient n) ∧
    (∀ (n : ℕ), SL.AuditRound7.endpoint_coefficient n < 0) ∧
    (∀ (lower upper jump lowerLeft lowerRight upperLeft upperRight
        lowerDL lowerDR upperDL upperDR : ℝ),
      lowerDL = SL.AuditRound7.fh_term lower jump lowerLeft 1 →
      lowerDR = SL.AuditRound7.fh_term lower (-jump) lowerRight (-1) →
      upperDL = SL.AuditRound7.fh_term upper jump upperLeft 1 →
      upperDR = SL.AuditRound7.fh_term upper (-jump) upperRight (-1) →
      lowerRight ^ 2 = lowerLeft ^ 2 → upperRight ^ 2 = upperLeft ^ 2 →
      (upperDL + upperDR) - (lowerDL + lowerDR) =
        2 * jump * SL.AuditRound7.gap_switch lower upper lowerLeft upperLeft) ∧
    (∀ (jump f : ℝ), jump ≠ 0 → (2 * jump * f = 0 ↔ f = 0)) := SL.AuditRound7.local_algebra_root
