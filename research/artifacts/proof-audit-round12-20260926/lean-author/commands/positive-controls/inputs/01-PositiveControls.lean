import AuditRound12
open scoped Matrix
open AuditRound12

example {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) :
    KpOdd K = E n * rawKe K * E n := (sector_exchange K).1

example (K : Matrix (Pair 0) (Pair 0) ℝ) :
    KpEven K = E 0 * rawKo K * E 0 := (sector_exchange K).2

example : (order 3 (Sum.inr (0 : Fin 3))).val = 5 := by
  norm_num [order, Fin.revPerm, Fin.rev]

example : ∃ K : Matrix (Pair 1) (Pair 1) ℝ,
    Kᵀ = K ∧ P 1 * K = K * P 1 ∧ rawKo K ≠ KpOdd K :=
  distinct_sectors_counterexample

example {n : ℕ} (v : Fin n → ℝ) (hv : v ≠ 0) :
    rawKo (outer (oddVector v)) ≠ 0 := (odd_rank_one v).2.2.2 hv
