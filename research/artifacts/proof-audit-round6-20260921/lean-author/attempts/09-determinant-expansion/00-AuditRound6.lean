import SL.AuditRound5
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
Local algebra for audit round 6 over the actual ring `Polynomial ℝ`.
Both high families are indexed by every natural m >= 2. The four traces use
polynomial derivatives and evaluation at 1 and -1. No Sobolev, spectral, complex
analytic or topological density assertion is encoded by this file.
-/

namespace SL.AuditRound6

open Polynomial
open SL.AuditRound5
open scoped Matrix

noncomputable section

def sparse_generators : Set (Polynomial ℝ) :=
  {p | p = p_zero ∨ p = p_one ∨
    ∃ m : ℕ, 2 ≤ m ∧ (p = p_even m ∨ p = p_odd m)}

def sparse_span : Submodule ℝ (Polynomial ℝ) :=
  Submodule.span ℝ sparse_generators

def augmented_generators : Set (Polynomial ℝ) :=
  {p | p ∈ sparse_generators ∨ p = X ^ 2 ∨ p = X ^ 3}

def augmented_span : Submodule ℝ (Polynomial ℝ) :=
  Submodule.span ℝ augmented_generators

theorem sparse_span_le_krein : sparse_span ≤ krein_polynomials := by
  apply Submodule.span_le.mpr
  rintro p (rfl | rfl | ⟨m, hm, rfl | rfl⟩)
  · exact low_residues.1
  · exact low_residues.2
  · exact even_residues m hm
  · exact odd_residues m hm

theorem X_sq_not_mem_sparse_span : (X ^ 2 : Polynomial ℝ) ∉ sparse_span := by
  intro h
  have hz : residues (X ^ 2) = 0 := sparse_span_le_krein h
  have he := monomial_even_residues 0
  rw [he] at hz
  have hf := congrArg Prod.fst hz
  norm_num at hf

theorem even_power_mem_augmented (m : ℕ) :
    (X ^ (2 * m) : Polynomial ℝ) ∈ augmented_span := by
  induction m with
  | zero =>
      apply Submodule.subset_span
      exact Or.inl (Or.inl (by simp [p_zero]))
  | succ m ih =>
      by_cases hm : m = 0
      · subst m
        exact Submodule.subset_span (Or.inr (Or.inl (by norm_num)))
      · have hg : p_even (m + 1) ∈ augmented_span :=
          Submodule.subset_span (Or.inl (Or.inr (Or.inr
            ⟨m + 1, by omega, Or.inl rfl⟩)))
        have he : 2 * (m + 1) - 2 = 2 * m := by omega
        have h := augmented_span.add_mem hg
          (augmented_span.smul_mem ((m + 1 : ℕ) / ((m + 1 : ℕ) - 1 : ℝ)) ih)
        simpa [p_even, he, smul_eq_C_mul] using h

theorem odd_power_mem_augmented (m : ℕ) :
    (X ^ (2 * m + 1) : Polynomial ℝ) ∈ augmented_span := by
  induction m with
  | zero =>
      apply Submodule.subset_span
      exact Or.inl (Or.inr (Or.inl (by simp [p_one])))
  | succ m ih =>
      by_cases hm : m = 0
      · subst m
        exact Submodule.subset_span (Or.inr (Or.inr (by norm_num)))
      · have hg : p_odd (m + 1) ∈ augmented_span :=
          Submodule.subset_span (Or.inl (Or.inr (Or.inr
            ⟨m + 1, by omega, Or.inr rfl⟩)))
        have he : 2 * (m + 1) - 1 = 2 * m + 1 := by omega
        have h := augmented_span.add_mem hg
          (augmented_span.smul_mem ((m + 1 : ℕ) / ((m + 1 : ℕ) - 1 : ℝ)) ih)
        simpa [p_odd, he, smul_eq_C_mul] using h

theorem power_mem_augmented (n : ℕ) :
    (X ^ n : Polynomial ℝ) ∈ augmented_span := by
  have h : n % 2 = 0 ∨ n % 2 = 1 := by omega
  rcases h with h | h
  · have hn : n = 2 * (n / 2) := by omega
    rw [hn]
    exact even_power_mem_augmented _
  · have hn : n = 2 * (n / 2) + 1 := by omega
    rw [hn]
    exact odd_power_mem_augmented _

theorem polynomial_mem_augmented (p : Polynomial ℝ) : p ∈ augmented_span := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq => exact augmented_span.add_mem hp hq
  | monomial n a =>
      simpa [smul_eq_C_mul, C_mul_X_pow_eq_monomial] using
        augmented_span.smul_mem a (power_mem_augmented n)

theorem augmented_span_eq_top : augmented_span = ⊤ := by
  apply top_unique
  intro p _
  exact polynomial_mem_augmented p

/-- The ordered trace vector is (B_+ p, B_- p, B_+ p'', B_- p''). -/
def four_traces : Polynomial ℝ →ₗ[ℝ] (Fin 4 → ℝ) where
  toFun p := ![(residues p).1, (residues p).2,
    (residues p.derivative.derivative).1, (residues p.derivative.derivative).2]
  map_add' p q := by ext i; fin_cases i <;> simp
  map_smul' a p := by ext i; fin_cases i <;> simp

theorem four_traces_apply (p : Polynomial ℝ) :
    four_traces p = ![(residues p).1, (residues p).2,
      (residues p.derivative.derivative).1, (residues p.derivative.derivative).2] := rfl

def trace_matrix : Matrix (Fin 4) (Fin 4) ℝ :=
  !![2, 2, 4, 4; -2, 2, -4, 4; 0, 0, 24, 40; 0, 0, -24, 40]

def inverse_matrix : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1/4, -1/4, -1/24, 1/24;
     1/4, 1/4, -1/40, -1/40;
     0, 0, 1/48, -1/48;
     0, 0, 1/80, 1/80]

theorem four_trace_monomial_columns (i : Fin 4) :
    four_traces (X ^ (i.val + 2)) = fun j => trace_matrix j i := by
  ext j
  fin_cases i <;> fin_cases j <;>
    norm_num [four_traces_apply, residues_apply, trace_matrix, derivative_X_pow]

theorem trace_matrix_det : trace_matrix.det = 15360 := by
  rw [Matrix.det_succ_row_zero]
  norm_num [trace_matrix, Matrix.det_fin_three,
    Fin.sum_univ_succ, Matrix.submatrix_apply, Fin.succAbove, Matrix.vecCons]

theorem trace_matrix_two_sided_inverse :
    trace_matrix * inverse_matrix = 1 ∧ inverse_matrix * trace_matrix = 1 := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [trace_matrix, inverse_matrix, Matrix.mul_apply, Fin.sum_univ_succ]

def monomial_lift : (Fin 4 → ℝ) →ₗ[ℝ] Polynomial ℝ where
  toFun a := ∑ i : Fin 4, a i • X ^ (i.val + 2)
  map_add' a b := by simp [add_smul, Finset.sum_add_distrib]
  map_smul' a b := by simp [Finset.smul_sum, smul_smul]

theorem four_traces_monomial_lift (a : Fin 4 → ℝ) :
    four_traces (monomial_lift a) = trace_matrix *ᵥ a := by
  ext j
  simp [monomial_lift, map_sum, four_trace_monomial_columns, Matrix.mulVec,
    dotProduct, mul_comm]

def four_trace_lift : (Fin 4 → ℝ) →ₗ[ℝ] Polynomial ℝ where
  toFun r := monomial_lift (inverse_matrix *ᵥ r)
  map_add' a b := by simp [Matrix.mulVec_add]
  map_smul' a b := by simp [Matrix.mulVec_smul]

theorem four_trace_right_inverse (r : Fin 4 → ℝ) :
    four_traces (four_trace_lift r) = r := by
  change four_traces (monomial_lift (inverse_matrix *ᵥ r)) = r
  rw [four_traces_monomial_lift, Matrix.mulVec_mulVec,
    trace_matrix_two_sided_inverse.1, Matrix.one_mulVec]

def correct_four_traces (p : Polynomial ℝ) : Polynomial ℝ :=
  p - four_trace_lift (four_traces p)

theorem corrected_four_traces_zero (p : Polynomial ℝ) :
    four_traces (correct_four_traces p) = 0 := by
  rw [correct_four_traces, map_sub, four_trace_right_inverse, sub_self]

theorem correction_fixes_kernel (p : Polynomial ℝ) (hp : four_traces p = 0) :
    correct_four_traces p = p := by
  simp [correct_four_traces, hp]

def cancellation : Polynomial ℝ := p_even 3 - (7 / 2 : ℝ) • p_even 2

theorem cancellation_formula :
    cancellation = X ^ 6 - C 5 * X ^ 4 + C 7 * X ^ 2 := by
  ext n
  by_cases h6 : n = 6 <;> by_cases h4 : n = 4 <;> by_cases h2 : n = 2 <;>
    norm_num [cancellation, p_even, smul_eq_C_mul, coeff_C_mul,
      coeff_X_pow, h6, h4, h2]

theorem cancellation_four_traces_zero : four_traces cancellation = 0 := by
  rw [cancellation_formula]
  ext i
  fin_cases i <;> norm_num [four_traces_apply, residues_apply, derivative_X_pow]

theorem p_four_four_traces : four_traces (p_even 2) = ![0, 0, 24, -24] := by
  ext i
  fin_cases i <;> norm_num [four_traces_apply, residues_apply, p_even, derivative_X_pow]

theorem p_four_four_traces_ne_zero : four_traces (p_even 2) ≠ 0 := by
  rw [p_four_four_traces]
  intro h
  have h2 := congrFun h 2
  change (24 : ℝ) = 0 at h2
  norm_num at h2

def detector : EuclideanSpace ℝ (Fin 2) := !₂[1, 1]
def witness : EuclideanSpace ℝ (Fin 2) := !₂[1, -1]
def coordinate_zero : EuclideanSpace ℝ (Fin 2) := !₂[1, 0]
def coordinate_one : EuclideanSpace ℝ (Fin 2) := !₂[0, 1]

theorem coordinate_detection_counterexample :
    inner ℝ detector coordinate_zero = 1 ∧
    inner ℝ detector coordinate_one = 1 ∧
    inner ℝ detector witness = 0 ∧
    inner ℝ witness coordinate_zero = 1 ∧
    inner ℝ witness coordinate_one = -1 := by
  norm_num [detector, witness, coordinate_zero, coordinate_one,
    PiLp.inner_apply, Fin.sum_univ_two]

/-- One materialized, nonconditional root for all advertised local claims. -/
theorem local_algebra_root :
    augmented_span = ⊤ ∧
    (X ^ 2 : Polynomial ℝ) ∉ sparse_span ∧
    (∀ i : Fin 4, four_traces (X ^ (i.val + 2)) = fun j => trace_matrix j i) ∧
    trace_matrix.det = 15360 ∧
    trace_matrix * inverse_matrix = 1 ∧
    inverse_matrix * trace_matrix = 1 ∧
    (∀ r : Fin 4 → ℝ, four_traces (four_trace_lift r) = r) ∧
    (∀ p : Polynomial ℝ, four_traces (correct_four_traces p) = 0) ∧
    cancellation = X ^ 6 - C 5 * X ^ 4 + C 7 * X ^ 2 ∧
    four_traces cancellation = 0 ∧
    four_traces (p_even 2) = ![0, 0, 24, -24] ∧
    four_traces (p_even 2) ≠ 0 ∧
    (inner ℝ detector coordinate_zero = 1 ∧
      inner ℝ detector coordinate_one = 1 ∧
      inner ℝ detector witness = 0 ∧
      inner ℝ witness coordinate_zero = 1 ∧
      inner ℝ witness coordinate_one = -1) := by
  exact ⟨augmented_span_eq_top, X_sq_not_mem_sparse_span,
    four_trace_monomial_columns, trace_matrix_det,
    trace_matrix_two_sided_inverse.1, trace_matrix_two_sided_inverse.2,
    four_trace_right_inverse, corrected_four_traces_zero,
    cancellation_formula, cancellation_four_traces_zero,
    p_four_four_traces, p_four_four_traces_ne_zero,
    coordinate_detection_counterexample⟩

end

end SL.AuditRound6
