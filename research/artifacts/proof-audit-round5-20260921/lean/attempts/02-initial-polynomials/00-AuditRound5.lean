import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Algebra.Polynomial.Eval.SMul
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Span.Basic
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
  simp [traces_apply, p_odd, derivative_X_pow, h0, h1, h2, h3]

theorem monomial_even_residues (k : ℕ) :
    residues (X ^ (2 * k + 2)) = ((2 * k + 2 : ℝ), -(2 * k + 2 : ℝ)) := by
  have he : 2 * k + 2 - 1 = 2 * k + 1 := by omega
  simp [residues_apply, derivative_X_pow, he, pow_add, pow_mul]
  ring

theorem monomial_odd_residues (k : ℕ) :
    residues (X ^ (2 * k + 3)) = ((2 * k + 2 : ℝ), (2 * k + 2 : ℝ)) := by
  have he : 2 * k + 3 - 1 = 2 * k + 2 := by omega
  simp [residues_apply, derivative_X_pow, he, pow_add, pow_mul]
  constructor <;> ring

end

end SL.AuditRound5
