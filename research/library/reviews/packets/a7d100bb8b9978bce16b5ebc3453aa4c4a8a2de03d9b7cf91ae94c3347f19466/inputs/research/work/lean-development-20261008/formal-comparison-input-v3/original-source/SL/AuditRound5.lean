import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Algebra.Polynomial.Eval.SMul
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Span.Basic
import Mathlib.LinearAlgebra.Prod
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
Local real-polynomial algebra for audit round 5. No Sobolev spaces, topological
closures, cutoff estimates, Green integrals or operator isomorphisms occur here.
The high family is indexed by all natural m >= 2, not a finite sample.
-/

namespace SL.AuditRound5

open Polynomial

noncomputable section

def p_zero : Polynomial ℝ := 1

def p_one : Polynomial ℝ := X

def p_even (m : ℕ) : Polynomial ℝ :=
  X ^ (2 * m) - C ((m : ℝ) / ((m : ℝ) - 1)) * X ^ (2 * m - 2)

def p_odd (m : ℕ) : Polynomial ℝ :=
  X ^ (2 * m + 1) - C ((m : ℝ) / ((m : ℝ) - 1)) * X ^ (2 * m - 1)

def eval_linear (x : ℝ) : Polynomial ℝ →ₗ[ℝ] ℝ where
  toFun p := p.eval x
  map_add' p q := by simp
  map_smul' a p := by simp [Polynomial.eval_smul]

def value_trace : Polynomial ℝ →ₗ[ℝ] ℝ := eval_linear 0

def derivative_trace : Polynomial ℝ →ₗ[ℝ] ℝ :=
  (eval_linear 0).comp Polynomial.derivative

def traces : Polynomial ℝ →ₗ[ℝ] ℝ × ℝ := value_trace.prod derivative_trace

def zero_traces : Submodule ℝ (Polynomial ℝ) := LinearMap.ker traces

def oblique : Submodule ℝ (Polynomial ℝ) :=
  LinearMap.ker (value_trace - derivative_trace)

def endpoint_plus : Polynomial ℝ →ₗ[ℝ] ℝ :=
  (eval_linear 1).comp Polynomial.derivative -
    (1 / 2 : ℝ) • (eval_linear 1 - eval_linear (-1))

def endpoint_minus : Polynomial ℝ →ₗ[ℝ] ℝ :=
  (eval_linear (-1)).comp Polynomial.derivative -
    (1 / 2 : ℝ) • (eval_linear 1 - eval_linear (-1))

def residues : Polynomial ℝ →ₗ[ℝ] ℝ × ℝ := endpoint_plus.prod endpoint_minus

def krein_polynomials : Submodule ℝ (Polynomial ℝ) := LinearMap.ker residues

def high_generators (m₀ : ℕ) : Set (Polynomial ℝ) :=
  {p | ∃ m : ℕ, 2 ≤ m ∧ m₀ ≤ m ∧ (p = p_even m ∨ p = p_odd m)}

def high_span (m₀ : ℕ) : Submodule ℝ (Polynomial ℝ) :=
  Submodule.span ℝ (high_generators m₀)

theorem traces_apply (p : Polynomial ℝ) :
    traces p = (p.eval 0, p.derivative.eval 0) := rfl

theorem residues_apply (p : Polynomial ℝ) :
    residues p = (p.derivative.eval 1 - (p.eval 1 - p.eval (-1)) / 2,
      p.derivative.eval (-1) - (p.eval 1 - p.eval (-1)) / 2) := by
  simp [residues, endpoint_plus, endpoint_minus, eval_linear, div_eq_mul_inv, mul_comm]

theorem mem_zero_traces (p : Polynomial ℝ) :
    p ∈ zero_traces ↔ p.eval 0 = 0 ∧ p.derivative.eval 0 = 0 := by
  simp [zero_traces, traces_apply, Prod.mk_eq_zero]

theorem mem_oblique (p : Polynomial ℝ) :
    p ∈ oblique ↔ p.eval 0 = p.derivative.eval 0 := by
  simp [oblique, value_trace, derivative_trace, eval_linear, sub_eq_zero]

theorem low_traces : traces p_zero = (1, 0) ∧ traces p_one = (0, 1) := by
  simp [traces_apply, p_zero, p_one]

theorem low_residues : residues p_zero = 0 ∧ residues p_one = 0 := by
  simp [residues_apply, p_zero, p_one]

theorem even_traces (m : ℕ) (hm : 2 ≤ m) : traces (p_even m) = 0 := by
  have h0 : 2 * m ≠ 0 := by omega
  have h1 : 2 * m - 2 ≠ 0 := by omega
  have h2 : 2 * m - 1 ≠ 0 := by omega
  have h3 : 2 * m - 2 - 1 ≠ 0 := by omega
  simp [traces_apply, p_even, derivative_X_pow, h0, h1, h2, h3]

theorem odd_traces (m : ℕ) (hm : 2 ≤ m) : traces (p_odd m) = 0 := by
  have h0 : 2 * m + 1 ≠ 0 := by omega
  have h1 : 2 * m - 1 ≠ 0 := by omega
  have h2 : 2 * m + 1 - 1 ≠ 0 := by omega
  have h3 : 2 * m - 1 - 1 ≠ 0 := by omega
  have hm0 : m ≠ 0 := by omega
  simp [traces_apply, p_odd, derivative_X_pow, hm0, h1, h3]

theorem monomial_even_residues (k : ℕ) :
    residues (X ^ (2 * k + 2)) = ((2 * k + 2 : ℝ), -(2 * k + 2 : ℝ)) := by
  have he : 2 * k + 2 - 1 = 2 * k + 1 := by omega
  rw [residues_apply, derivative_X_pow]
  simp only [eval_mul, eval_C, eval_pow, eval_X, one_pow, mul_one, he]
  norm_num [pow_add, pow_mul]

theorem monomial_odd_residues (k : ℕ) :
    residues (X ^ (2 * k + 3)) = ((2 * k + 2 : ℝ), (2 * k + 2 : ℝ)) := by
  have he : 2 * k + 3 - 1 = 2 * k + 2 := by omega
  rw [residues_apply, derivative_X_pow]
  simp only [eval_mul, eval_C, eval_pow, eval_X, one_pow, mul_one, he]
  norm_num [pow_add, pow_mul] <;> ring

theorem residues_C_mul (a : ℝ) (p : Polynomial ℝ) :
    residues (C a * p) = a • residues p := by
  rw [← smul_eq_C_mul]
  exact map_smul residues a p

theorem even_residues (m : ℕ) (hm : 2 ≤ m) : residues (p_even m) = 0 := by
  obtain ⟨k, rfl⟩ : ∃ k : ℕ, m = k + 2 := ⟨m - 2, by omega⟩
  have h1 : 2 * (k + 2) = 2 * (k + 1) + 2 := by omega
  have h2 : 2 * (k + 2) - 2 = 2 * k + 2 := by omega
  rw [p_even, map_sub, residues_C_mul, h2, h1,
    monomial_even_residues, monomial_even_residues]
  have hk : (k : ℝ) + 1 ≠ 0 := by positivity
  have hd : (k : ℝ) + 2 - 1 = (k : ℝ) + 1 := by ring
  ext <;> simp [Nat.cast_add, Nat.cast_one, Nat.cast_ofNat, hd] <;> field_simp [hk] <;> ring

theorem odd_residues (m : ℕ) (hm : 2 ≤ m) : residues (p_odd m) = 0 := by
  obtain ⟨k, rfl⟩ : ∃ k : ℕ, m = k + 2 := ⟨m - 2, by omega⟩
  have h1 : 2 * (k + 2) + 1 = 2 * (k + 1) + 3 := by omega
  have h2 : 2 * (k + 2) - 1 = 2 * k + 3 := by omega
  rw [p_odd, map_sub, residues_C_mul, h2, h1,
    monomial_odd_residues, monomial_odd_residues]
  have hk : (k : ℝ) + 1 ≠ 0 := by positivity
  have hd : (k : ℝ) + 2 - 1 = (k : ℝ) + 1 := by ring
  ext <;> simp [Nat.cast_add, Nat.cast_one, Nat.cast_ofNat, hd] <;> field_simp [hk] <;> ring

theorem high_span_zero_traces (m₀ : ℕ) : high_span m₀ ≤ zero_traces := by
  apply Submodule.span_le.mpr
  rintro p ⟨m, hm, _, rfl | rfl⟩
  · exact even_traces m hm
  · exact odd_traces m hm

theorem high_span_krein (m₀ : ℕ) : high_span m₀ ≤ krein_polynomials := by
  apply Submodule.span_le.mpr
  rintro p ⟨m, hm, _, rfl | rfl⟩
  · exact even_residues m hm
  · exact odd_residues m hm

theorem span_member_has_zero_traces (m₀ : ℕ) (p : Polynomial ℝ)
    (hp : p ∈ high_span m₀) : p.eval 0 = 0 ∧ p.derivative.eval 0 = 0 :=
  (mem_zero_traces p).mp (high_span_zero_traces m₀ hp)

theorem one_add_X_mem_oblique : (1 + X : Polynomial ℝ) ∈ oblique := by
  rw [mem_oblique]
  simp

theorem one_not_mem_oblique : (1 : Polynomial ℝ) ∉ oblique := by
  rw [mem_oblique]
  simp

theorem X_not_mem_oblique : (X : Polynomial ℝ) ∉ oblique := by
  rw [mem_oblique]
  simp

theorem one_add_X_not_mem_high_span (m₀ : ℕ) :
    (1 + X : Polynomial ℝ) ∉ high_span m₀ := by
  intro hp
  have h := (span_member_has_zero_traces m₀ _ hp).1
  norm_num at h

theorem zero_traces_le_oblique : zero_traces ≤ oblique := by
  intro p hp
  obtain ⟨hv, hd⟩ := (mem_zero_traces p).mp hp
  exact (mem_oblique p).mpr (hv.trans hd.symm)

theorem high_span_lt_oblique (m₀ : ℕ) : high_span m₀ < oblique := by
  refine lt_of_le_of_ne ((high_span_zero_traces m₀).trans zero_traces_le_oblique) ?_
  intro h
  exact one_add_X_not_mem_high_span m₀ (h ▸ one_add_X_mem_oblique)

def endpoint_matrix (L : ℕ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![(L : ℝ), (L : ℝ); -(L : ℝ), (L : ℝ)]

def correction_matrix (L : ℕ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1 / (2 * (L : ℝ)), -1 / (2 * (L : ℝ));
     1 / (2 * (L : ℝ)), 1 / (2 * (L : ℝ))]

theorem endpoint_matrix_det (L : ℕ) :
    (endpoint_matrix L).det = 2 * (L : ℝ) ^ 2 := by
  simp [endpoint_matrix, Matrix.det_fin_two]
  ring

theorem endpoint_matrix_det_ne_zero (L : ℕ) (hL : 0 < L) :
    (endpoint_matrix L).det ≠ 0 := by
  rw [endpoint_matrix_det]
  exact mul_ne_zero (by norm_num) (pow_ne_zero _ (by exact_mod_cast Nat.ne_of_gt hL))

theorem endpoint_matrix_inverse (L : ℕ) (hL : 0 < L) :
    endpoint_matrix L * correction_matrix L = 1 ∧
      correction_matrix L * endpoint_matrix L = 1 := by
  have h : (L : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hL
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [endpoint_matrix, correction_matrix, Matrix.mul_apply, Fin.sum_univ_two] <;>
    field_simp <;> ring

theorem endpoint_monomial_columns (L : ℕ) (hL : 0 < L) (he : Even L) :
    residues (X ^ L) = ((L : ℝ), -(L : ℝ)) ∧
      residues (X ^ (L + 1)) = ((L : ℝ), (L : ℝ)) := by
  obtain ⟨k, hk⟩ := he
  obtain ⟨j, hj⟩ : ∃ j : ℕ, k = j + 1 := ⟨k - 1, by omega⟩
  have h : L = 2 * j + 2 := by omega
  rw [h]
  simpa only [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.add_assoc] using
    And.intro (monomial_even_residues j) (monomial_odd_residues j)

def correction_alpha (L : ℕ) (r : ℝ × ℝ) : ℝ :=
  (r.1 - r.2) / (2 * (L : ℝ))

def correction_beta (L : ℕ) (r : ℝ × ℝ) : ℝ :=
  (r.1 + r.2) / (2 * (L : ℝ))

theorem correction_solves_residues (L : ℕ) (hL : 0 < L) (r : ℝ × ℝ) :
    ((L : ℝ) * correction_alpha L r + (L : ℝ) * correction_beta L r,
      -(L : ℝ) * correction_alpha L r + (L : ℝ) * correction_beta L r) = r := by
  have h : (L : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hL
  ext <;> dsimp [correction_alpha, correction_beta] <;> field_simp <;> ring

def correct_endpoints (L : ℕ) (p : Polynomial ℝ) : Polynomial ℝ :=
  p - C (correction_alpha L (residues p)) * X ^ L -
    C (correction_beta L (residues p)) * X ^ (L + 1)

theorem corrected_residues_zero (L : ℕ) (hL : 0 < L) (he : Even L)
    (p : Polynomial ℝ) : residues (correct_endpoints L p) = 0 := by
  obtain ⟨h₁, h₂⟩ := endpoint_monomial_columns L hL he
  have h := correction_solves_residues L hL (residues p)
  rw [correct_endpoints, map_sub, map_sub, residues_C_mul, residues_C_mul, h₁, h₂]
  have hp := congrArg Prod.fst h
  have hm := congrArg Prod.snd h
  ext <;> dsimp at * <;> linarith

theorem correction_preserves_divisibility (L : ℕ) (p : Polynomial ℝ)
    (hp : (X : Polynomial ℝ) ^ L ∣ p) :
    (X : Polynomial ℝ) ^ L ∣ correct_endpoints L p := by
  apply dvd_sub
  · exact dvd_sub hp (dvd_mul_left _ _)
  · rw [pow_succ]
    exact dvd_mul_of_dvd_right (dvd_mul_right _ _) _

def trace_lift (r : ℝ × ℝ) : Polynomial ℝ := C r.1 + C r.2 * X

theorem traces_trace_lift (r : ℝ × ℝ) : traces (trace_lift r) = r := by
  ext <;> simp [traces_apply, trace_lift]

theorem trace_lift_krein (r : ℝ × ℝ) : residues (trace_lift r) = 0 := by
  ext <;> simp [residues_apply, trace_lift]

theorem traces_surjective : Function.Surjective traces := by
  intro r
  exact ⟨trace_lift r, traces_trace_lift r⟩

theorem subtract_trace_lift (p : Polynomial ℝ) :
    p - trace_lift (traces p) ∈ zero_traces := by
  change traces (p - trace_lift (traces p)) = 0
  rw [map_sub, traces_trace_lift, sub_self]

/- The kernel-inclusion hypothesis below is algebraic and explicit. Deriving
it from a cofinite family in a Sobolev space is not formalized here. -/
theorem trace_membership_iff (W : Submodule ℝ (Polynomial ℝ))
    (hW : zero_traces ≤ W) (p : Polynomial ℝ) :
    p ∈ W ↔ trace_lift (traces p) ∈ W := by
  have hr := hW (subtract_trace_lift p)
  constructor
  · intro hp
    have h := W.sub_mem hp hr
    simpa using h
  · intro ht
    have h := W.add_mem hr ht
    simpa using h

theorem oblique_with_krein_witness :
    (1 + X : Polynomial ℝ) ∈ oblique ⊓ krein_polynomials ∧
    (1 : Polynomial ℝ) ∉ oblique ⊓ krein_polynomials ∧
    (X : Polynomial ℝ) ∉ oblique ⊓ krein_polynomials := by
  refine ⟨⟨one_add_X_mem_oblique, ?_⟩, ?_, ?_⟩
  · change residues (1 + X : Polynomial ℝ) = 0
    simpa [trace_lift] using trace_lift_krein (1, 1)
  · exact fun h => one_not_mem_oblique h.1
  · exact fun h => X_not_mem_oblique h.1

theorem high_span_lt_krein_oblique (m₀ : ℕ) :
    high_span m₀ < oblique ⊓ krein_polynomials := by
  refine lt_of_le_of_ne
    (le_inf ((high_span_zero_traces m₀).trans zero_traces_le_oblique)
      (high_span_krein m₀)) ?_
  intro h
  exact one_add_X_not_mem_high_span m₀ (h ▸ oblique_with_krein_witness.1)

/-- A concrete conjunction of the local results. It has no analytic hypotheses. -/
theorem local_algebra_root :
    (traces p_zero = (1, 0) ∧ traces p_one = (0, 1)) ∧
    (residues p_zero = 0 ∧ residues p_one = 0) ∧
    (∀ m : ℕ, 2 ≤ m →
      traces (p_even m) = 0 ∧ traces (p_odd m) = 0 ∧
      residues (p_even m) = 0 ∧ residues (p_odd m) = 0) ∧
    (∀ m₀ : ℕ, high_span m₀ ≤ zero_traces ∧
      high_span m₀ < oblique ⊓ krein_polynomials) ∧
    ((1 + X : Polynomial ℝ) ∈ oblique ⊓ krein_polynomials ∧
      (1 : Polynomial ℝ) ∉ oblique ⊓ krein_polynomials ∧
      (X : Polynomial ℝ) ∉ oblique ⊓ krein_polynomials) ∧
    (∀ L : ℕ, 0 < L → (endpoint_matrix L).det ≠ 0 ∧
      endpoint_matrix L * correction_matrix L = 1 ∧
      correction_matrix L * endpoint_matrix L = 1) ∧
    (∀ L : ℕ, 0 < L → Even L → ∀ p : Polynomial ℝ,
      residues (correct_endpoints L p) = 0 ∧
      ((X : Polynomial ℝ) ^ L ∣ p →
        (X : Polynomial ℝ) ^ L ∣ correct_endpoints L p)) ∧
    (∀ W : Submodule ℝ (Polynomial ℝ), zero_traces ≤ W →
      ∀ p : Polynomial ℝ, p ∈ W ↔ trace_lift (traces p) ∈ W) := by
  refine ⟨low_traces, low_residues, ?_, ?_, oblique_with_krein_witness, ?_, ?_, ?_⟩
  · intro m hm
    exact ⟨even_traces m hm, odd_traces m hm, even_residues m hm, odd_residues m hm⟩
  · intro m₀
    exact ⟨high_span_zero_traces m₀, high_span_lt_krein_oblique m₀⟩
  · intro L hL
    exact ⟨endpoint_matrix_det_ne_zero L hL, endpoint_matrix_inverse L hL⟩
  · intro L hL he p
    exact ⟨corrected_residues_zero L hL he p, correction_preserves_divisibility L p⟩
  · exact trace_membership_iff

end

end SL.AuditRound5
