import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

open scoped Matrix

namespace AuditRound11

abbrev PairIndex (n : ℕ) := Fin n ⊕ Fin n
abbrev Square (n : ℕ) := Matrix (Fin n) (Fin n) ℝ
abbrev PairedMatrix (n : ℕ) := Matrix (PairIndex n) (PairIndex n) ℝ

noncomputable def reversal (n : ℕ) : PairedMatrix n :=
  Matrix.fromBlocks 0 1 1 0

noncomputable def parity_basis (n : ℕ) : PairedMatrix n :=
  Matrix.fromBlocks 1 1 1 (-1)

noncomputable def parity_inverse (n : ℕ) : PairedMatrix n :=
  (1 / 2 : ℝ) • parity_basis n

noncomputable def parity_sign (n : ℕ) : PairedMatrix n :=
  Matrix.fromBlocks 1 0 0 (-1)

noncomputable def parity_matrix {n : ℕ} (J : PairedMatrix n) : PairedMatrix n :=
  parity_inverse n * J * parity_basis n

noncomputable def physical_reflection {n : ℕ} (x : PairIndex n → ℝ) : PairIndex n → ℝ :=
  fun i => 1 - (reversal n *ᵥ x) i

noncomputable def boundary_even (L : ℝ) : Square 2 :=
  !![L, L + 2; L * (L - 1) * (L - 2), L * (L + 1) * (L + 2)]

noncomputable def boundary_odd (L : ℝ) : Square 2 :=
  !![L, L + 2; L * (L + 1) * (L - 2), L * (L + 2) * (L + 3)]

theorem parity_basis_identities (n : ℕ) :
    parity_inverse n * parity_basis n = 1 ∧
    parity_basis n * parity_inverse n = 1 ∧
    reversal n * parity_basis n = parity_basis n * parity_sign n ∧
    parity_inverse n * reversal n = parity_sign n * parity_inverse n := by
  have ht : parity_basis n * parity_basis n = (2 : ℝ) • (1 : PairedMatrix n) := by
    simp only [parity_basis, Matrix.fromBlocks_multiply, Matrix.mul_one, Matrix.mul_neg, neg_neg]
    ext (i | i) (j | j) <;> simp [Matrix.one_apply, Matrix.fromBlocks]
    <;> split_ifs <;> norm_num
  have htp : reversal n * parity_basis n = parity_basis n * parity_sign n := by
    simp [reversal, parity_basis, parity_sign, Matrix.fromBlocks_multiply]
  have hpt : parity_basis n * reversal n = parity_sign n * parity_basis n := by
    simp [reversal, parity_basis, parity_sign, Matrix.fromBlocks_multiply]
  refine ⟨?_, ?_, htp, ?_⟩
  · rw [parity_inverse, Matrix.smul_mul, ht, smul_smul]
    norm_num
  · rw [parity_inverse, Matrix.mul_smul, ht, smul_smul]
    norm_num
  · simp only [parity_inverse, Matrix.smul_mul, Matrix.mul_smul, hpt]

theorem parity_relation {n : ℕ} (J : PairedMatrix n) (a : ℝ)
    (h : J * reversal n = a • (reversal n * J)) :
    parity_matrix J * parity_sign n = a • (parity_sign n * parity_matrix J) := by
  have ht := (parity_basis_identities n).2.2.1
  have hs := (parity_basis_identities n).2.2.2
  calc
    parity_matrix J * parity_sign n = parity_inverse n * J *
        (parity_basis n * parity_sign n) := by simp [parity_matrix, Matrix.mul_assoc]
    _ = parity_inverse n * (J * reversal n) * parity_basis n := by
      rw [← ht]
      simp only [Matrix.mul_assoc]
    _ = a • ((parity_inverse n * reversal n) * J * parity_basis n) := by
      rw [h]
      simp only [Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_assoc]
    _ = a • (parity_sign n * parity_matrix J) := by
      rw [hs]
      simp only [parity_matrix, Matrix.mul_assoc]

theorem anticommuting_blocks {n : ℕ} (J : PairedMatrix n)
    (h : J * reversal n = -(reversal n * J)) :
    (parity_matrix J).toBlocks₁₁ = 0 ∧ (parity_matrix J).toBlocks₂₂ = 0 := by
  have hp := parity_relation J (-1) (by simpa using h)
  constructor
  · ext i j
    have he := congrFun (congrFun hp (Sum.inl i)) (Sum.inl j)
    simp [parity_sign, Matrix.mul_apply, Fintype.sum_sum_type, Matrix.fromBlocks,
      Matrix.one_apply] at he
    change parity_matrix J (Sum.inl i) (Sum.inl j) = 0
    linarith
  · ext i j
    have he := congrFun (congrFun hp (Sum.inr i)) (Sum.inr j)
    simp [parity_sign, Matrix.mul_apply, Fintype.sum_sum_type, Matrix.fromBlocks,
      Matrix.one_apply] at he
    change parity_matrix J (Sum.inr i) (Sum.inr j) = 0
    linarith

theorem commuting_blocks {n : ℕ} (J : PairedMatrix n)
    (h : J * reversal n = reversal n * J) :
    (parity_matrix J).toBlocks₁₂ = 0 ∧ (parity_matrix J).toBlocks₂₁ = 0 := by
  have hp := parity_relation J 1 (by simpa using h)
  constructor
  · ext i j
    have he := congrFun (congrFun hp (Sum.inl i)) (Sum.inr j)
    simp [parity_sign, Matrix.mul_apply, Fintype.sum_sum_type, Matrix.fromBlocks,
      Matrix.one_apply] at he
    change parity_matrix J (Sum.inl i) (Sum.inr j) = 0
    linarith
  · ext i j
    have he := congrFun (congrFun hp (Sum.inr i)) (Sum.inl j)
    simp [parity_sign, Matrix.mul_apply, Fintype.sum_sum_type, Matrix.fromBlocks,
      Matrix.one_apply] at he
    change parity_matrix J (Sum.inr i) (Sum.inl j) = 0
    linarith

theorem parity_determinant {n : ℕ} (J : PairedMatrix n) :
    (parity_matrix J).det = J.det := by
  have hd := congrArg Matrix.det (parity_basis_identities n).1
  rw [Matrix.det_mul, Matrix.det_one] at hd
  simp only [parity_matrix, Matrix.det_mul]
  calc
    (parity_inverse n).det * J.det * (parity_basis n).det =
        ((parity_inverse n).det * (parity_basis n).det) * J.det := by ring
    _ = J.det := by rw [hd, one_mul]

theorem off_diagonal_determinant {n : ℕ} (C D : Square n) :
    (Matrix.fromBlocks (0 : Square n) C D (0 : Square n)).det =
      (-1 : ℝ) ^ n * C.det * D.det := by
  have hp : (parity_matrix (reversal n)) = parity_sign n := by
    unfold parity_matrix
    rw [Matrix.mul_assoc, (parity_basis_identities n).2.2.1,
      ← Matrix.mul_assoc, (parity_basis_identities n).1, Matrix.one_mul]
  have hd : (reversal n).det = (-1 : ℝ) ^ n := by
    rw [← parity_determinant, hp, parity_sign, Matrix.det_fromBlocks_zero₂₁]
    simp [Matrix.det_neg]
  have he : Matrix.fromBlocks (0 : Square n) C D (0 : Square n) =
      Matrix.fromBlocks C 0 0 D * reversal n := by
    simp [reversal, Matrix.fromBlocks_multiply]
  rw [he, Matrix.det_mul, Matrix.det_fromBlocks_zero₂₁, hd]
  ring

theorem anticommuting_determinant {n : ℕ} (J : PairedMatrix n)
    (h : J * reversal n = -(reversal n * J)) :
    J.det = (-1 : ℝ) ^ n * (parity_matrix J).toBlocks₁₂.det *
      (parity_matrix J).toBlocks₂₁.det := by
  have hz := anticommuting_blocks J h
  rw [← parity_determinant J, ← Matrix.fromBlocks_toBlocks (parity_matrix J),
    hz.1, hz.2, off_diagonal_determinant]
  simp

theorem reflection_increment {n : ℕ} (x v : PairIndex n → ℝ) :
    physical_reflection (x + v) - physical_reflection x = -(reversal n *ᵥ v) := by
  ext i
  simp [physical_reflection, Matrix.mulVec_add]

theorem reflection_parity {n : ℕ} (x v : PairIndex n → ℝ) :
    (physical_reflection (x + v) - physical_reflection x = v ↔
      reversal n *ᵥ v = -v) ∧
    (physical_reflection (x + v) - physical_reflection x = -v ↔
      reversal n *ᵥ v = v) := by
  rw [reflection_increment]
  exact ⟨neg_eq_iff_eq_neg, neg_inj⟩

theorem boundary_determinants (L : ℝ) :
    (boundary_even L).det = 2 * L * (L + 2) * (2 * L - 1) ∧
    (boundary_odd L).det = 2 * L * (L + 2) * (2 * L + 1) := by
  constructor <;> simp [boundary_even, boundary_odd, Matrix.det_fin_two] <;> ring

theorem boundary_positive (L : ℝ) (h : 4 ≤ L) :
    0 < (boundary_even L).det ∧ 0 < (boundary_odd L).det := by
  rw [(boundary_determinants L).1, (boundary_determinants L).2]
  have hl : 0 < L := by linarith
  have ha : 0 < L + 2 := by linarith
  constructor <;> apply mul_pos (mul_pos (mul_pos (by norm_num) hl) ha) <;> linarith

theorem paired_coordinate_actions {n : ℕ} (v : PairIndex n → ℝ) (i : Fin n) :
    (reversal n *ᵥ v) (Sum.inl i) = v (Sum.inr i) ∧
    (reversal n *ᵥ v) (Sum.inr i) = v (Sum.inl i) ∧
    (parity_basis n *ᵥ v) (Sum.inl i) = v (Sum.inl i) + v (Sum.inr i) ∧
    (parity_basis n *ᵥ v) (Sum.inr i) = v (Sum.inl i) - v (Sum.inr i) := by
  simp [reversal, parity_basis, Matrix.mulVec, dotProduct, Fintype.sum_sum_type,
    Matrix.fromBlocks, Matrix.one_apply, sub_eq_add_neg]

noncomputable def boundary_full (L : ℝ) : PairedMatrix 2 :=
  Matrix.fromBlocks (boundary_even L) 0 0 (boundary_odd L)

theorem boundary_correction (L : ℕ) (h : 4 ≤ L) :
    0 < (boundary_full (L : ℝ)).det ∧
    (∀ b : PairIndex 2 → ℝ, ∃! a : PairIndex 2 → ℝ,
      boundary_full (L : ℝ) *ᵥ a = b) := by
  have hL : (4 : ℝ) ≤ L := by exact_mod_cast h
  have hp := boundary_positive (L : ℝ) hL
  have hd : 0 < (boundary_full (L : ℝ)).det := by
    rw [boundary_full, Matrix.det_fromBlocks_zero₂₁]
    exact mul_pos hp.1 hp.2
  refine ⟨hd, ?_⟩
  have hu : IsUnit (boundary_full (L : ℝ)) :=
    (Matrix.isUnit_iff_isUnit_det _).mpr (isUnit_iff_ne_zero.mpr (ne_of_gt hd))
  intro b
  obtain ⟨a, ha⟩ := Matrix.mulVec_surjective_iff_isUnit.mpr hu b
  refine ⟨a, ha, ?_⟩
  intro a' ha'
  exact Matrix.mulVec_injective_iff_isUnit.mpr hu (ha'.trans ha.symm)

end AuditRound11
