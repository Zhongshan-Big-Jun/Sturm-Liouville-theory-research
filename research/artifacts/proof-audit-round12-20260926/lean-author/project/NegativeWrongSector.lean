import AuditRound12
open scoped Matrix
open AuditRound12

-- Deliberately false identification; this must fail by the proved counterexample.
theorem wrong_sector_identification :
    ∀ (K : Matrix (Pair 1) (Pair 1) ℝ), rawKo K = KpOdd K := by
  intro K
  exact (sector_exchange K).1
