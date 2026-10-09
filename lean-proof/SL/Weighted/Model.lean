import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
An interval model for measurable positive bounded densities and complex solutions.
The derivative is represented by two actual integral identities, so jumps in the
density require no pointwise second derivative at the jump. This is an integral
solution model, not a claim of spectral existence, simplicity or completeness.
Source: docs/SL_ratio_proof.tex, problem definition; and
docs/SL_bounded_direction_spectral_tail.md, Sections 1-2.
-/

noncomputable section

namespace SL.Weighted

open MeasureTheory Set

def interval_measure (Length : ℝ) : Measure ℝ := volume.restrict (Ioo 0 Length)

/-- Bounds are almost everywhere, and no continuity or finite partition is imposed. -/
structure Density (Length : ℝ) where
  value : ℝ → ℝ
  measurable : Measurable value
  lower : ℝ
  upper : ℝ
  lower_pos : 0 < lower
  bounds : ∀ᵐ x ∂interval_measure Length, lower ≤ value x ∧ value x ≤ upper

def weighted_measure {Length : ℝ} (Rho : Density Length) : Measure ℝ :=
  (interval_measure Length).withDensity (fun x => ENNReal.ofReal (Rho.value x))

abbrev WeightedL2 {Length : ℝ} (Rho : Density Length) := Lp ℂ 2 (weighted_measure Rho)

inductive Boundary where
  | DD
  | DN
  deriving DecidableEq

def boundary_condition (Kind : Boundary) (Length : ℝ) (Value Velocity : ℝ → ℂ) : Prop :=
  Value 0 = 0 ∧ match Kind with
    | .DD => Value Length = 0
    | .DN => Velocity Length = 0

/-- The mathematical eigenvalue is Lambda; it is not a frequency. -/
structure Solution (Length : ℝ) (Rho : ℝ → ℝ) (Lambda : ℝ) where
  value : ℝ → ℂ
  velocity : ℝ → ℂ
  value_continuous : ContinuousOn value (Icc 0 Length)
  velocity_continuous : ContinuousOn velocity (Icc 0 Length)
  force_integrable : IntervalIntegrable (fun x => (Rho x : ℂ) * value x) volume 0 Length
  first_integral : ∀ x ∈ Icc 0 Length, value x = value 0 + ∫ t in 0..x, velocity t
  second_integral : ∀ x ∈ Icc 0 Length,
    velocity x = velocity 0 - (Lambda : ℂ) * ∫ t in 0..x, (Rho t : ℂ) * value t

def mass (Length : ℝ) (Rho : ℝ → ℝ) (Value : ℝ → ℂ) : ℝ :=
  ∫ x in 0..Length, Rho x * ‖Value x‖ ^ 2

/-- Source convention: linear in the first variable, conjugate-linear in the second.
Mathlib's inner product uses the opposite ordering; future bridges must reverse it. -/
def inner_first_linear (Length : ℝ) (Rho : ℝ → ℝ) (Value Other : ℝ → ℂ) : ℂ :=
  ∫ x in 0..Length, (Rho x : ℂ) * Value x * star (Other x)

def NormalizedEigenfunction (Kind : Boundary) (Length : ℝ) (Rho : ℝ → ℝ)
    (Lambda : ℝ) (Sol : Solution Length Rho Lambda) : Prop :=
  0 < Lambda ∧ boundary_condition Kind Length Sol.value Sol.velocity ∧
    mass Length Rho Sol.value = 1

theorem normalized_not_zero {Kind : Boundary} {Length Lambda : ℝ} {Rho : ℝ → ℝ}
    {Sol : Solution Length Rho Lambda} (Valid : NormalizedEigenfunction Kind Length Rho Lambda Sol) :
    Sol.value ≠ 0 := by
  intro Zero
  have Contradiction := Valid.2.2
  simp [mass, Zero] at Contradiction

def constant_density (Length Rho : ℝ) (Positive : 0 < Rho) : Density Length where
  value := fun _ => Rho
  measurable := measurable_const
  lower := Rho
  upper := Rho
  lower_pos := Positive
  bounds := Filter.Eventually.of_forall (fun _ => ⟨le_rfl, le_rfl⟩)

end SL.Weighted
