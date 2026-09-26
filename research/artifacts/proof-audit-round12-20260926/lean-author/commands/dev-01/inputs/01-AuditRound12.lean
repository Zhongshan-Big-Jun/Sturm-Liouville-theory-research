import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Data.Fin.Rev
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

set_option autoImplicit false

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

def Be (n : ℕ) : Matrix (Pair n) (Fin n) ℝ := Sum.elim 1 1

def Bo (n : ℕ) : Matrix (Pair n) (Fin n) ℝ := Sum.elim 1 (-1)

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
  have hpos (i : Fin n) : 0 < n := by omega
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
      nlinarith
  refine ⟨?_, hswap, hsign, ?_, ?_⟩
  · intro i; exact ⟨rfl, hval i⟩
  · ext i j
    simp only [paired, orderedP, P, Matrix.submatrix_apply, ← hswap,
      Equiv.apply_eq_iff_eq]
  · ext i j
    by_cases h : i = j
    · subst j; simp [paired, orderedS, S, hsign]
    · simp [paired, orderedS, S, Matrix.diagonal_apply, h, (order n).injective.ne h]

theorem involutions (n : ℕ) :
    P n * P n = 1 ∧ E n * E n = 1 ∧ S n * S n = 1 ∧
    (P n)ᵀ = P n ∧ (E n)ᵀ = E n ∧ (S n)ᵀ = S n := by
  have hs (i : Fin n) : ((-1 : ℝ)^i.val) * ((-1 : ℝ)^i.val) = 1 := by
    rw [← pow_add, ← two_mul, pow_mul]; norm_num
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j
    simp [P, Matrix.mul_apply, Matrix.one_apply]
  · simp [E, Matrix.diagonal_mul_diagonal, hs, Matrix.diagonal_one]
  · rw [S, Matrix.diagonal_mul_diagonal]
    convert Matrix.diagonal_one (n := Pair n) (α := ℝ) using 1
    funext i; cases i <;> simp [sign, hs]
  · ext i j
    simp only [P, Matrix.transpose_apply]
    congr 1
    constructor <;> intro h <;> simpa using congrArg Sum.swap h.symm
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
    split_ifs <;> norm_num
  · ext i j
    simp [Bo, Matrix.mul_apply, Matrix.transpose_apply, Fintype.sum_sum_type,
      Matrix.one_apply, Matrix.smul_apply, smul_eq_mul]
    split_ifs <;> norm_num
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

end
end AuditRound12
