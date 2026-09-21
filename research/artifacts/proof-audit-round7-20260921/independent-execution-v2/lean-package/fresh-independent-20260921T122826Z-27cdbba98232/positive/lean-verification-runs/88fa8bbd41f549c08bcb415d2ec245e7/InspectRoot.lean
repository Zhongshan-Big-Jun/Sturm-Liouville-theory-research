import LeanVerifyProbe
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (∀ (n : ℕ) (x : ℝ), HasDerivAt (SL.AuditRound7.normalized_mode n) (SL.AuditRound7.normalized_mode_slope n x) x) ∧
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
    (∀ (jump f : ℝ), jump ≠ 0 → (2 * jump * f = 0 ↔ f = 0))
#lean_verify_v2 SL.AuditRound7.local_algebra_root expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round7-20260921\\independent-execution-v2\\lean-package\\fresh-independent-20260921T122826Z-27cdbba98232\\positive\\lean-verification-runs\\88fa8bbd41f549c08bcb415d2ec245e7\\declaration.json"
