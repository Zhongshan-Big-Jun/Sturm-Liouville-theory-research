import AuditRound8
open AuditRound8
example : (∀ (lambda2 : ℝ), 0 ≤ lambda2 → lambda2 ≤ 4 * Real.pi ^ 2 →
    0 ≤ phase lambda2 ∧ phase lambda2 ≤ Real.pi / 20 ∧ Real.pi / 20 < Real.pi / 2) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    I2 a u = u * (1 + b + b ^ 2 * a ^ 2) / (2 * (1 + b ^ 2 * a ^ 2)) ∧
    0 < I2 a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    S a u = Real.pi ^ 2 / (2 * u ^ 3) -
      2 * a ^ 4 * b ^ 2 / (u ^ 3 * (1 + b + b ^ 2 * a ^ 2))) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 →
    C a b u = 4 * mubar1 u * ell u / (3 * u) + (ell u / 3) * S a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 → S a u = 0 →
    C a b u = Real.pi ^ 2 * ell u / (3 * u ^ 3) ∧ 0 < C a b u) ∧
  scalarRatio < (8256 / 10000 : ℚ) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (19 / 100 : ℝ) < 48743 / 100000 ∧ (48743 / 100000 : ℝ) < 1 / 2 ∧
    wCritical 1500 < 48743 / 100000 ∧
    (48743 / 100000 : ℝ) < wCritical (3015 / 2)) ∧
  (capGap (3015 / 2) (4995815 / 10000000) < 25 ∧
    25 < capGap 1515 (4995815 / 10000000)) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (0 : ℝ) < 4995815 / 10000000 ∧ (4995815 / 10000000 : ℝ) < 1 / 2 ∧
    wCap (3015 / 2) < 4995815 / 10000000 ∧
    (4995815 / 10000000 : ℝ) < wCap 1515) := AuditRound8.local_root
