import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Data.Fin.Rev
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.SplitIfs

set_option autoImplicit false

open scoped Matrix

namespace AuditRound12

abbrev Pair (n : ℕ) := Fin n ⊕ Fin n

noncomputable section

-- Original order: i on the left, 2n-1-i on the right.
def order (n : ℕ) : Pair n ≃ Fin (n + n) :=
  (Equiv.sumCongr (Equiv.refl _) Fin.revPerm).trans finSumFinEquiv

def sign (n : ℕ) : Pair n → ℝ :=
  Sum.elim (fun i => (-1 : ℝ) ^ i.val) (fun i => -((-1 : ℝ) ^ i.val))

def P (n : ℕ) : Matrix (Pair n) (Pair n) ℝ :=
  fun i j => if Sum.swap i = j then 1 else 0

def S (n : ℕ) : Matrix (Pair n) (Pair n) ℝ := Matrix.diagonal (sign n)

def E (n : ℕ) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.diagonal (fun i => (-1 : ℝ) ^ i.val)

def Be (n : ℕ) : Matrix (Pair n) (Fin n) ℝ :=
  Sum.elim (1 : Matrix (Fin n) (Fin n) ℝ) (1 : Matrix (Fin n) (Fin n) ℝ)

def Bo (n : ℕ) : Matrix (Pair n) (Fin n) ℝ :=
  Sum.elim (1 : Matrix (Fin n) (Fin n) ℝ) (-(1 : Matrix (Fin n) (Fin n) ℝ))

def rawKe {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) := (Be n)ᵀ * K * Be n

def rawKo {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) := (Bo n)ᵀ * K * Bo n

def Kp {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) := S n * K * S n

def KpOdd {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) := rawKo (Kp K)

def KpEven {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) := rawKe (Kp K)

def orderedP (n : ℕ) : Matrix (Fin (n+n)) (Fin (n+n)) ℝ :=
  fun i j => if i.rev = j then 1 else 0

def orderedS (n : ℕ) : Matrix (Fin (n+n)) (Fin (n+n)) ℝ :=
  Matrix.diagonal (fun i => (-1 : ℝ) ^ i.val)

def orderedBe (n : ℕ) : Matrix (Fin (n+n)) (Fin n) ℝ :=
  (Be n).submatrix (order n).symm id

def orderedBo (n : ℕ) : Matrix (Fin (n+n)) (Fin n) ℝ :=
  (Bo n).submatrix (order n).symm id

def paired {n : ℕ} (K : Matrix (Fin (n+n)) (Fin (n+n)) ℝ) :=
  K.submatrix (order n) (order n)

theorem coordinate_bridge (n : ℕ) :
    (∀ i : Fin n, (order n (Sum.inl i)).val = i.val ∧
      (order n (Sum.inr i)).val = n+n-1-i.val) ∧
    (∀ i : Pair n, order n (Sum.swap i) = (order n i).rev) ∧
    (∀ i : Pair n, sign n i = (-1 : ℝ) ^ (order n i).val) ∧
    paired (orderedP n) = P n ∧ paired (orderedS n) = S n := by
  have hval (i : Fin n) : (order n (Sum.inr i)).val = n+n-1-i.val := by
    simp [order, Fin.revPerm, Fin.rev]
    omega
  have hswap (i : Pair n) : order n (Sum.swap i) = (order n i).rev := by
    cases i with
    | inl i => apply Fin.ext; simp [order, Fin.revPerm, Fin.rev]; omega
    | inr i => apply Fin.ext; simp [order, Fin.revPerm, Fin.rev]; omega
  have hsign (i : Pair n) : sign n i = (-1 : ℝ) ^ (order n i).val := by
    cases i with
    | inl i => rfl
    | inr i =>
      change -((-1 : ℝ)^i.val) = (-1 : ℝ)^(order n (Sum.inr i)).val
      rw [hval]
      have hsum : (n+n-1-i.val) + i.val = 2*(n-1)+1 := by omega
      have hs : ((-1 : ℝ)^i.val) * ((-1 : ℝ)^i.val) = 1 := by
        rw [← pow_add, ← two_mul, pow_mul]
        norm_num
      have hp : (-1 : ℝ)^(n+n-1-i.val) * (-1 : ℝ)^i.val = -1 := by
        rw [← pow_add, hsum, pow_add, pow_mul]
        norm_num
      have hh := congrArg (fun x : ℝ => x * (-1 : ℝ)^i.val) hp
      simpa only [mul_assoc, hs, mul_one, neg_one_mul] using hh.symm
  refine ⟨?_, hswap, hsign, ?_, ?_⟩
  · intro i; exact ⟨rfl, hval i⟩
  · ext i j
    simp only [paired, orderedP, P, Matrix.submatrix_apply, ← hswap,
      Equiv.apply_eq_iff_eq]
  · ext i j
    by_cases h : i = j
    · subst j; simp [paired, orderedS, S, hsign]
    · simp [paired, orderedS, S, h, (order n).injective.ne h]

theorem involutions (n : ℕ) :
    P n * P n = 1 ∧ E n * E n = 1 ∧ S n * S n = 1 ∧
    (P n)ᵀ = P n ∧ (E n)ᵀ = E n ∧ (S n)ᵀ = S n := by
  have hs (i : Fin n) : ((-1 : ℝ)^i.val) * ((-1 : ℝ)^i.val) = 1 := by
    rw [← pow_add, ← two_mul, pow_mul]; norm_num
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j
    cases i <;> cases j <;> simp [P, Matrix.mul_apply, Matrix.one_apply]
  · simp [E, Matrix.diagonal_mul_diagonal, hs, Matrix.diagonal_one]
  · rw [S, Matrix.diagonal_mul_diagonal]
    have hh : (fun i => sign n i * sign n i) = fun _ => (1 : ℝ) := by
      funext i; cases i <;> simp [sign, hs]
    rw [hh, Matrix.diagonal_one]
  · ext i j
    cases i <;> cases j <;> simp [P, Matrix.transpose_apply, eq_comm]
  · exact Matrix.diagonal_transpose _
  · exact Matrix.diagonal_transpose _

theorem basis_relations (n : ℕ) :
    P n * Be n = Be n ∧ P n * Bo n = -Bo n ∧
    (Be n)ᵀ * Be n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Bo n)ᵀ * Bo n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Be n)ᵀ * Bo n = 0 ∧
    S n * Be n = Bo n * E n ∧ S n * Bo n = Be n * E n := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j; cases i <;> simp [P, Be, Matrix.mul_apply]
  · ext i j; cases i <;> simp [P, Bo, Matrix.mul_apply]
  · ext i j
    simp [Be, Matrix.mul_apply, Matrix.transpose_apply, Fintype.sum_sum_type,
      Matrix.one_apply, Matrix.smul_apply, smul_eq_mul]
    split_ifs <;> simp_all
    norm_num
  · ext i j
    simp [Bo, Matrix.mul_apply, Matrix.transpose_apply, Fintype.sum_sum_type,
      Matrix.one_apply, Matrix.smul_apply, smul_eq_mul]
    split_ifs <;> simp_all
    norm_num
  · ext i j
    simp [Be, Bo, Matrix.mul_apply, Matrix.transpose_apply, Fintype.sum_sum_type,
      Matrix.one_apply]
  · ext i j; cases i <;>
      simp [S, E, sign, Be, Bo, Matrix.diagonal_mul, Matrix.mul_diagonal, Matrix.one_apply]
    all_goals split_ifs <;> simp_all
  · ext i j; cases i <;>
      simp [S, E, sign, Be, Bo, Matrix.diagonal_mul, Matrix.mul_diagonal, Matrix.one_apply]
    all_goals split_ifs <;> simp_all

theorem sector_exchange {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) :
    KpOdd K = E n * rawKe K * E n ∧
    KpEven K = E n * rawKo K * E n := by
  have htS := (involutions n).2.2.2.2.2
  have htE := (involutions n).2.2.2.2.1
  have hbe := (basis_relations n).2.2.2.2.2.1
  have hbo := (basis_relations n).2.2.2.2.2.2
  have hbot : (Bo n)ᵀ * S n = E n * (Be n)ᵀ := by
    simpa [Matrix.transpose_mul, htS, htE] using congrArg Matrix.transpose hbo
  have hbet : (Be n)ᵀ * S n = E n * (Bo n)ᵀ := by
    simpa [Matrix.transpose_mul, htS, htE] using congrArg Matrix.transpose hbe
  constructor
  · unfold KpOdd rawKo Kp rawKe
    calc
      _ = ((Bo n)ᵀ * S n) * K * (S n * Bo n) := by simp [Matrix.mul_assoc]
      _ = _ := by rw [hbot, hbo]; simp [Matrix.mul_assoc]
  · unfold KpEven rawKo Kp rawKe
    calc
      _ = ((Be n)ᵀ * S n) * K * (S n * Be n) := by simp [Matrix.mul_assoc]
      _ = _ := by rw [hbet, hbe]; simp [Matrix.mul_assoc]

theorem ordered_compressions {n : ℕ} (K : Matrix (Fin (n+n)) (Fin (n+n)) ℝ) :
    (orderedBe n)ᵀ * K * orderedBe n = rawKe (paired K) ∧
    (orderedBo n)ᵀ * K * orderedBo n = rawKo (paired K) ∧
    (orderedBo n)ᵀ * (orderedS n * K * orderedS n) * orderedBo n =
      E n * ((orderedBe n)ᵀ * K * orderedBe n) * E n ∧
    (orderedBe n)ᵀ * (orderedS n * K * orderedS n) * orderedBe n =
      E n * ((orderedBo n)ᵀ * K * orderedBo n) * E n := by
  have hc (A : Matrix (Fin (n+n)) (Fin n) ℝ)
      (M : Matrix (Fin (n+n)) (Fin (n+n)) ℝ) :
      (A.submatrix (order n) id)ᵀ * paired M * A.submatrix (order n) id = Aᵀ * M * A := by
    change Aᵀ.submatrix id (order n) * M.submatrix (order n) (order n) *
      A.submatrix (order n) id = _
    rw [Matrix.submatrix_mul_equiv, Matrix.submatrix_mul_equiv]
    rfl
  have he : (orderedBe n).submatrix (order n) id = Be n := by
    ext i j; simp [orderedBe]
  have ho : (orderedBo n).submatrix (order n) id = Bo n := by
    ext i j; simp [orderedBo]
  have hce (M : Matrix (Fin (n+n)) (Fin (n+n)) ℝ) :
      (orderedBe n)ᵀ * M * orderedBe n = rawKe (paired M) := by
    simpa [he, rawKe] using (hc (orderedBe n) M).symm
  have hco (M : Matrix (Fin (n+n)) (Fin (n+n)) ℝ) :
      (orderedBo n)ᵀ * M * orderedBo n = rawKo (paired M) := by
    simpa [ho, rawKo] using (hc (orderedBo n) M).symm
  have hp : paired (orderedS n * K * orderedS n) = Kp (paired K) := by
    unfold paired Kp
    rw [Matrix.submatrix_mul _ _ (order n) (order n) (order n) (order n).bijective,
      Matrix.submatrix_mul _ _ (order n) (order n) (order n) (order n).bijective]
    change paired (orderedS n) * paired K * paired (orderedS n) = _
    rw [(coordinate_bridge n).2.2.2.2]
    rfl
  refine ⟨hce K, hco K, ?_, ?_⟩
  · rw [hco, hce, hp]
    exact (sector_exchange (paired K)).1
  · rw [hce, hco, hp]
    exact (sector_exchange (paired K)).2

def normalizedBe (n : ℕ) := (Real.sqrt 2)⁻¹ • Be n

def normalizedBo (n : ℕ) := (Real.sqrt 2)⁻¹ • Bo n

theorem normalization {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) :
    (normalizedBe n)ᵀ * normalizedBe n = 1 ∧
    (normalizedBo n)ᵀ * normalizedBo n = 1 ∧
    (normalizedBe n)ᵀ * K * normalizedBe n = (1/2 : ℝ) • rawKe K ∧
    (normalizedBo n)ᵀ * K * normalizedBo n = (1/2 : ℝ) • rawKo K := by
  have hs : (Real.sqrt 2)⁻¹ * (Real.sqrt 2)⁻¹ = (1/2 : ℝ) := by
    rw [← mul_inv, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [normalizedBe, Matrix.transpose_smul, Matrix.smul_mul, Matrix.mul_smul,
      smul_smul, ← mul_assoc, hs, (basis_relations n).2.2.1]
  · simp [normalizedBo, Matrix.transpose_smul, Matrix.smul_mul, Matrix.mul_smul,
      smul_smul, ← mul_assoc, hs, (basis_relations n).2.2.2.1]
  · simp [normalizedBe, rawKe, Matrix.transpose_smul, Matrix.smul_mul,
      Matrix.mul_smul, smul_smul, hs]
  · simp [normalizedBo, rawKo, Matrix.transpose_smul, Matrix.smul_mul,
      Matrix.mul_smul, smul_smul, hs]

def oddVector {n : ℕ} (v : Fin n → ℝ) : Pair n → ℝ := Sum.elim v (-v)

def outer {ι : Type} (v : ι → ℝ) : Matrix ι ι ℝ := fun i j => v i * v j

theorem odd_rank_one {n : ℕ} (v : Fin n → ℝ) :
    rawKo (outer (oddVector v)) = (4 : ℝ) • outer v ∧
    rawKe (outer (oddVector v)) = 0 ∧
    KpOdd (outer (oddVector v)) = 0 ∧
    (v ≠ 0 → rawKo (outer (oddVector v)) ≠ 0) := by
  have ho : rawKo (outer (oddVector v)) = (4 : ℝ) • outer v := by
    ext i j
    simp [rawKo, Bo, outer, oddVector, Matrix.mul_apply, Fintype.sum_sum_type,
      Matrix.transpose_apply, Matrix.one_apply, Matrix.smul_apply, smul_eq_mul]
    ring
  have he : rawKe (outer (oddVector v)) = 0 := by
    ext i j
    simp [rawKe, Be, outer, oddVector, Matrix.mul_apply, Fintype.sum_sum_type,
      Matrix.transpose_apply, Matrix.one_apply]
  refine ⟨ho, he, ?_, ?_⟩
  · rw [(sector_exchange _).1, he]; simp
  · intro hv hz
    apply hv
    funext i
    have hi := congrArg (fun M : Matrix (Fin n) (Fin n) ℝ => M i i) hz
    rw [ho] at hi
    simp [outer, Matrix.smul_apply, smul_eq_mul] at hi
    simpa using (mul_self_eq_zero.mp (by nlinarith : v i * v i = 0))

theorem convention_bridge {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ) :
    (-S n) * K * (-S n) = Kp K ∧
    (-S n) * Be n = Bo n * (-E n) ∧
    (-S n) * Bo n = Be n * (-E n) ∧
    (normalizedBo n)ᵀ * Kp K * normalizedBo n =
      E n * ((normalizedBe n)ᵀ * K * normalizedBe n) * E n ∧
    (normalizedBe n)ᵀ * Kp K * normalizedBe n =
      E n * ((normalizedBo n)ᵀ * K * normalizedBo n) * E n := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp [Kp]
  · simp [(basis_relations n).2.2.2.2.2.1]
  · simp [(basis_relations n).2.2.2.2.2.2]
  · rw [(normalization (Kp K)).2.2.2, (normalization K).2.2.1]
    change (1/2 : ℝ) • KpOdd K = _
    rw [(sector_exchange K).1]
    simp
  · rw [(normalization (Kp K)).2.2.1, (normalization K).2.2.2]
    change (1/2 : ℝ) • KpEven K = _
    rw [(sector_exchange K).2]
    simp

theorem distinct_sectors_counterexample :
    ∃ K : Matrix (Pair 1) (Pair 1) ℝ,
      Kᵀ = K ∧ P 1 * K = K * P 1 ∧ rawKo K ≠ KpOdd K := by
  refine ⟨P 1, (involutions 1).2.2.2.1, rfl, ?_⟩
  have ho : rawKo (P 1) = -(2 : ℝ) • (1 : Matrix (Fin 1) (Fin 1) ℝ) := by
    rw [rawKo, Matrix.mul_assoc, (basis_relations 1).2.1, Matrix.mul_neg,
      (basis_relations 1).2.2.2.1]
    simp
  have he : rawKe (P 1) = (2 : ℝ) • (1 : Matrix (Fin 1) (Fin 1) ℝ) := by
    rw [rawKe, Matrix.mul_assoc, (basis_relations 1).1, (basis_relations 1).2.2.1]
  intro h
  rw [(sector_exchange _).1, ho, he] at h
  have hc := congrArg (fun M : Matrix (Fin 1) (Fin 1) ℝ => M 0 0) h
  norm_num [E, Matrix.mul_apply, Matrix.smul_apply, Matrix.one_apply,
    Matrix.diagonal_apply] at hc


theorem audit_root :
(∀ (n : ℕ),
(∀ i : Fin n, (order n (Sum.inl i)).val = i.val ∧
      (order n (Sum.inr i)).val = n+n-1-i.val) ∧
    (∀ i : Pair n, order n (Sum.swap i) = (order n i).rev) ∧
    (∀ i : Pair n, sign n i = (-1 : ℝ) ^ (order n i).val) ∧
    paired (orderedP n) = P n ∧ paired (orderedS n) = S n) ∧
(∀ (n : ℕ),
P n * P n = 1 ∧ E n * E n = 1 ∧ S n * S n = 1 ∧
    (P n)ᵀ = P n ∧ (E n)ᵀ = E n ∧ (S n)ᵀ = S n) ∧
(∀ (n : ℕ),
P n * Be n = Be n ∧ P n * Bo n = -Bo n ∧
    (Be n)ᵀ * Be n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Bo n)ᵀ * Bo n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Be n)ᵀ * Bo n = 0 ∧
    S n * Be n = Bo n * E n ∧ S n * Bo n = Be n * E n) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
KpOdd K = E n * rawKe K * E n ∧
    KpEven K = E n * rawKo K * E n) ∧
(∀ {n : ℕ} (K : Matrix (Fin (n+n)) (Fin (n+n)) ℝ),
(orderedBe n)ᵀ * K * orderedBe n = rawKe (paired K) ∧
    (orderedBo n)ᵀ * K * orderedBo n = rawKo (paired K) ∧
    (orderedBo n)ᵀ * (orderedS n * K * orderedS n) * orderedBo n =
      E n * ((orderedBe n)ᵀ * K * orderedBe n) * E n ∧
    (orderedBe n)ᵀ * (orderedS n * K * orderedS n) * orderedBe n =
      E n * ((orderedBo n)ᵀ * K * orderedBo n) * E n) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
(normalizedBe n)ᵀ * normalizedBe n = 1 ∧
    (normalizedBo n)ᵀ * normalizedBo n = 1 ∧
    (normalizedBe n)ᵀ * K * normalizedBe n = (1/2 : ℝ) • rawKe K ∧
    (normalizedBo n)ᵀ * K * normalizedBo n = (1/2 : ℝ) • rawKo K) ∧
(∀ {n : ℕ} (v : Fin n → ℝ),
rawKo (outer (oddVector v)) = (4 : ℝ) • outer v ∧
    rawKe (outer (oddVector v)) = 0 ∧
    KpOdd (outer (oddVector v)) = 0 ∧
    (v ≠ 0 → rawKo (outer (oddVector v)) ≠ 0)) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
(-S n) * K * (-S n) = Kp K ∧
    (-S n) * Be n = Bo n * (-E n) ∧
    (-S n) * Bo n = Be n * (-E n) ∧
    (normalizedBo n)ᵀ * Kp K * normalizedBo n =
      E n * ((normalizedBe n)ᵀ * K * normalizedBe n) * E n ∧
    (normalizedBe n)ᵀ * Kp K * normalizedBe n =
      E n * ((normalizedBo n)ᵀ * K * normalizedBo n) * E n) ∧
(∃ K : Matrix (Pair 1) (Pair 1) ℝ,
      Kᵀ = K ∧ P 1 * K = K * P 1 ∧ rawKo K ≠ KpOdd K) := by
  exact ⟨@coordinate_bridge, @involutions, @basis_relations, @sector_exchange, @ordered_compressions, @normalization, @odd_rank_one, @convention_bridge, @distinct_sectors_counterexample⟩

end
end AuditRound12
