import AuditRound12
open scoped Matrix
open AuditRound12

example : ¬ (∀ (K : Matrix (Pair 1) (Pair 1) ℝ), rawKo K = KpOdd K) := by
  intro h
  obtain ⟨K, _, _, hk⟩ := distinct_sectors_counterexample
  exact hk (h K)

example : sign 1 (Sum.inr (0 : Fin 1)) ≠ sign 1 (Sum.inl (0 : Fin 1)) := by
  norm_num [sign]

example : (Be 1)ᵀ * Be 1 ≠ (1 : Matrix (Fin 1) (Fin 1) ℝ) := by
  rw [(basis_relations 1).2.2.1]
  intro h
  have h00 := congrArg (fun M : Matrix (Fin 1) (Fin 1) ℝ => M 0 0) h
  norm_num [Matrix.smul_apply, Matrix.one_apply] at h00

example (n : ℕ) : (normalizedBe n)ᵀ * normalizedBe n = 1 :=
  (normalization (0 : Matrix (Pair n) (Pair n) ℝ)).1

example {n : ℕ} (v : Fin n → ℝ) :
    (normalizedBo n)ᵀ * outer (oddVector v) * normalizedBo n = (2 : ℝ) • outer v := by
  rw [(normalization _).2.2.2, (odd_rank_one v).1]
  norm_num [smul_smul]

example : (normalizedBo 0)ᵀ * normalizedBo 0 = 1 :=
  (normalization (0 : Matrix (Pair 0) (Pair 0) ℝ)).2.1

example : rawKo (P 1) 0 0 = -2 ∧ KpOdd (P 1) 0 0 = 2 := by
  rw [(sector_exchange (P 1)).1]
  norm_num [rawKo, rawKe, Bo, Be, P, E, Matrix.mul_apply,
    Matrix.transpose_apply, Matrix.diagonal_apply, Matrix.one_apply]
