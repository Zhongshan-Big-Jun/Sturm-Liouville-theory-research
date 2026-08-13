import Mathlib
import SL.Completeness

/-!
# General denseness criteria: moment characterization of the sparse basis

Formalization of the algebraic core of `docs/SL_denseness_criteria.tex`
Theorem 2 ("矩刻画"): for a real-linear functional `M` on polynomials
(representing `p ↦ (w, p)_H`), orthogonality to the sparse basis

    p_0 = 1, p_1 = X, p_{2m} = X^{2m} - (m/(m-1)) X^{2m-2},
    p_{2m+1} = X^{2m+1} - (m/(m-1)) X^{2m-1}  (m >= 2)

is equivalent to the moment conditions

    M_0 = M_1 = 0,
    M_{2m} = m * M_2,  M_{2m+1} = m * M_3  (m >= 1).

This is the finite-dimensional/algebraic reduction behind both the
first-moment criterion (`beta < 1`) and the diagonal-space critical-exponent
theorem in the source.  The Hilbert-space and density arguments are not
formalized here.
-/

namespace SL

namespace DensenessCriteria

open Polynomial

/-- The k-th moment of a real-linear functional `M` on polynomials. -/
noncomputable def moments (M : Polynomial ℝ →ₗ[ℝ] ℝ) (k : ℕ) : ℝ :=
  M (X ^ k)

/-- `M (C a * X^m) = a * M_m`. -/
@[simp] lemma apply_C_mul_X_pow (M : Polynomial ℝ →ₗ[ℝ] ℝ) (a : ℝ) (m : ℕ) :
    M (C a * X ^ m) = a * moments M m := by
  rw [← Polynomial.smul_eq_C_mul]
  exact map_smul M a (X ^ m)

/-- Evaluation of the even sparse basis polynomial. -/
lemma sparse_even_apply (M : Polynomial ℝ →ₗ[ℝ] ℝ) {n : ℕ} (_hn : 2 ≤ n) :
    M (Completeness.pEvenR n) =
      moments M (2 * n) - Completeness.qR n * moments M (2 * n - 2) := by
  unfold Completeness.pEvenR
  rw [map_sub]
  rw [apply_C_mul_X_pow]
  simp [moments]

/-- Evaluation of the odd sparse basis polynomial. -/
lemma sparse_odd_apply (M : Polynomial ℝ →ₗ[ℝ] ℝ) {n : ℕ} (_hn : 2 ≤ n) :
    M (Completeness.pOddR n) =
      moments M (2 * n + 1) - Completeness.qR n * moments M (2 * n - 1) := by
  unfold Completeness.pOddR
  rw [map_sub]
  rw [apply_C_mul_X_pow]
  simp [moments]

/-- Even-moment direction of Theorem 2: orthogonality to the sparse even
polynomials forces `M_{2m} = m * M_2`. -/
lemma even_moments_of_orthogonal (M : Polynomial ℝ →ₗ[ℝ] ℝ)
    (horth : ∀ n : ℕ, 2 ≤ n → M (Completeness.pEvenR n) = 0) :
    ∀ m : ℕ, 1 ≤ m → moments M (2 * m) = (m : ℝ) * moments M 2 := by
  have hrec : ∀ n : ℕ, 2 ≤ n →
      moments M (2 * n) = Completeness.qR n * moments M (2 * n - 2) := by
    intro n hn
    have h := sparse_even_apply M hn
    rw [horth n hn] at h
    linarith
  intro m hm
  induction m, hm using Nat.le_induction with
  | base => simp
  | succ m hm ih =>
      have hm1 : 2 ≤ m + 1 := by omega
      rw [hrec (m + 1) hm1]
      have hidx : 2 * (m + 1) - 2 = 2 * m := by omega
      rw [hidx]
      have hden : (m : ℝ) ≠ 0 := by exact_mod_cast (by omega : m ≠ 0)
      have hq : Completeness.qR (m + 1) = ((m + 1 : ℕ) : ℝ) / (m : ℝ) := by
        unfold Completeness.qR
        norm_num
      rw [hq, ih]
      try field_simp [hden]
      try ring

/-- Odd-moment direction of Theorem 2: orthogonality to the sparse odd
polynomials forces `M_{2m+1} = m * M_3`. -/
lemma odd_moments_of_orthogonal (M : Polynomial ℝ →ₗ[ℝ] ℝ)
    (horth : ∀ n : ℕ, 2 ≤ n → M (Completeness.pOddR n) = 0) :
    ∀ m : ℕ, 1 ≤ m → moments M (2 * m + 1) = (m : ℝ) * moments M 3 := by
  have hrec : ∀ n : ℕ, 2 ≤ n →
      moments M (2 * n + 1) = Completeness.qR n * moments M (2 * n - 1) := by
    intro n hn
    have h := sparse_odd_apply M hn
    rw [horth n hn] at h
    linarith
  intro m hm
  induction m, hm using Nat.le_induction with
  | base => simp
  | succ m hm ih =>
      have hm1 : 2 ≤ m + 1 := by omega
      rw [hrec (m + 1) hm1]
      have hidx : 2 * (m + 1) - 1 = 2 * m + 1 := by omega
      rw [hidx]
      have hden : (m : ℝ) ≠ 0 := by exact_mod_cast (by omega : m ≠ 0)
      have hq : Completeness.qR (m + 1) = ((m + 1 : ℕ) : ℝ) / (m : ℝ) := by
        unfold Completeness.qR
        norm_num
      rw [hq, ih]
      try field_simp [hden]
      try ring

/-- Converse even direction: the moment recurrence forces orthogonality. -/
lemma even_orthogonal_of_moments (M : Polynomial ℝ →ₗ[ℝ] ℝ)
    (hmom : ∀ m : ℕ, 1 ≤ m → moments M (2 * m) = (m : ℝ) * moments M 2) :
    ∀ n : ℕ, 2 ≤ n → M (Completeness.pEvenR n) = 0 := by
  intro n hn
  rw [sparse_even_apply M hn]
  have hidx : 2 * n - 2 = 2 * (n - 1) := by omega
  rw [hidx]
  have hden : ((n - 1 : ℕ) : ℝ) ≠ 0 := by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast (by omega : (n - 1 : ℕ) ≠ 0)
  have hq : Completeness.qR n = (n : ℝ) / ((n - 1 : ℕ) : ℝ) := by
    unfold Completeness.qR
    norm_num
  rw [hmom n (by omega : 1 ≤ n), hmom (n - 1) (by omega : 1 ≤ n - 1), hq]
  field_simp [hden]
  ring

/-- Converse odd direction: the moment recurrence forces orthogonality. -/
lemma odd_orthogonal_of_moments (M : Polynomial ℝ →ₗ[ℝ] ℝ)
    (hmom : ∀ m : ℕ, 1 ≤ m → moments M (2 * m + 1) = (m : ℝ) * moments M 3) :
    ∀ n : ℕ, 2 ≤ n → M (Completeness.pOddR n) = 0 := by
  intro n hn
  rw [sparse_odd_apply M hn]
  have hidx : 2 * n - 1 = 2 * (n - 1) + 1 := by omega
  rw [hidx]
  have hden : ((n - 1 : ℕ) : ℝ) ≠ 0 := by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast (by omega : (n - 1 : ℕ) ≠ 0)
  have hq : Completeness.qR n = (n : ℝ) / ((n - 1 : ℕ) : ℝ) := by
    unfold Completeness.qR
    norm_num
  rw [hmom n (by omega : 1 ≤ n), hmom (n - 1) (by omega : 1 ≤ n - 1), hq]
  field_simp [hden]
  ring

/-- Theorem 2 of `docs/SL_denseness_criteria.tex`: the moment
characterization of orthogonality to the sparse basis. -/
theorem sparse_moment_characterization (M : Polynomial ℝ →ₗ[ℝ] ℝ) :
    (M 1 = 0 ∧ M X = 0 ∧
      (∀ n : ℕ, 2 ≤ n → M (Completeness.pEvenR n) = 0) ∧
      (∀ n : ℕ, 2 ≤ n → M (Completeness.pOddR n) = 0)) ↔
    (moments M 0 = 0 ∧ moments M 1 = 0 ∧
      (∀ m : ℕ, 1 ≤ m → moments M (2 * m) = (m : ℝ) * moments M 2) ∧
      (∀ m : ℕ, 1 ≤ m → moments M (2 * m + 1) = (m : ℝ) * moments M 3)) := by
  constructor
  · rintro ⟨h0, h1, hE, hO⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa [moments] using h0
    · simpa [moments] using h1
    · exact even_moments_of_orthogonal M hE
    · exact odd_moments_of_orthogonal M hO
  · rintro ⟨h0, h1, hE, hO⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa [moments] using h0
    · simpa [moments] using h1
    · exact even_orthogonal_of_moments M hE
    · exact odd_orthogonal_of_moments M hO

end DensenessCriteria

end SL
