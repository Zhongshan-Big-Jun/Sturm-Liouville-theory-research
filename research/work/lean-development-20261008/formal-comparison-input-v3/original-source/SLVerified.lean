import SL.Krein.PolynomialEnergy
import SL.Krein.LinearDomain
import SL.Krein.IntegralConstruction
import SL.Krein.WeakDerivative
import SL.Weighted.ConstantDD

noncomputable section

namespace SLVerified

open MeasureTheory

theorem krein_domain_root :
    (∀ (R : SL.Krein.IntegralRepresentative) {x : ℝ}, x ∈ Set.Ioo (-1) 1 → HasDerivAt R.Value (R.First x) x) ∧
    (∀ (R : SL.Krein.IntegralRepresentative), ∀ᵐ x ∂SL.Krein.intervalMeasure, HasDerivAt R.First (R.Second x) x) ∧
    (∀ (R S : SL.Krein.IntegralRepresentative), R.to_L2 = S.to_L2 → R.Second =ᵐ[SL.Krein.intervalMeasure] S.Second) ∧
    (∀ (c : ℝ) (F G : SL.Krein.domain_submodule), SL.Krein.operator_linear c (F + G) = SL.Krein.operator_linear c F + SL.Krein.operator_linear c G) ∧
    (∀ (c : ℝ) (a : ℂ) (F : SL.Krein.domain_submodule), SL.Krein.operator_linear c (a • F) = a • SL.Krein.operator_linear c F) ∧
    (∀ (F : ℝ → ℂ) (HF : MeasureTheory.MemLp F 2 SL.Krein.intervalMeasure) (a b : ℂ), (SL.Krein.from_l2_second F HF a b).Value (-1) = b ∧ (SL.Krein.from_l2_second F HF a b).First (-1) = a ∧ (SL.Krein.from_l2_second F HF a b).Second = F) ∧
    (∀ (R : SL.Krein.IntegralRepresentative), Set.EqOn (SL.Krein.from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).Value R.Value (Set.Icc (-1) 1) ∧ Set.EqOn (SL.Krein.from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).First R.First (Set.Icc (-1) 1)) ∧
    (∀ (R : SL.Krein.IntegralRepresentative) (Q : ℂ →L[ℝ] ℝ) (Phi : ℝ → ℝ), ContDiff ℝ 1 Phi → Phi (-1) = 0 → Phi 1 = 0 → (∫ x in (-1 : ℝ)..1, Q (R.Value x) * deriv Phi x) = -(∫ x in (-1 : ℝ)..1, Q (R.First x) * Phi x) ∧ (∫ x in (-1 : ℝ)..1, Q (R.First x) * deriv Phi x) = -(∫ x in (-1 : ℝ)..1, Q (R.Second x) * Phi x)) := by
  exact ⟨SL.Krein.IntegralRepresentative.value_has_deriv,
    SL.Krein.IntegralRepresentative.first_has_deriv_ae,
    SL.Krein.IntegralRepresentative.second_eq_ae,
    SL.Krein.operator_linear_add,
    SL.Krein.operator_linear_smul,
    SL.Krein.from_l2_second_initial,
    SL.Krein.representative_parameterization,
    SL.Krein.IntegralRepresentative.weak_derivative_pair⟩

theorem krein_polynomial_root :
    (∀ (p : Polynomial ℝ), SL.AuditRound5.residues p = 0 → SL.Krein.polynomial_L2 p ∈ SL.Krein.domain) ∧
    (∀ (p : Polynomial ℝ) (hp : SL.AuditRound5.residues p = 0) (c : ℝ), SL.Krein.operator c (SL.Krein.polynomial_domain p hp) = SL.Krein.polynomial_L2 (-p.derivative.derivative + Polynomial.C c * p)) ∧
    (SL.Krein.polynomial_L2 SL.AuditRound5.p_zero ∈ SL.Krein.domain ∧ SL.Krein.polynomial_L2 SL.AuditRound5.p_one ∈ SL.Krein.domain ∧ (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_even m) ∈ SL.Krein.domain) ∧ (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_odd m) ∈ SL.Krein.domain)) ∧
    (∀ (p : Polynomial ℝ) (hp : SL.AuditRound5.residues p = 0) (c : ℝ), SL.Krein.first_linear_inner (SL.Krein.operator c (SL.Krein.polynomial_domain p hp)) (SL.Krein.polynomial_L2 p) = (((∫ x in (-1 : ℝ)..1, (p.derivative.eval x) ^ 2) + c * (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2) - (p.eval 1 - p.eval (-1)) ^ 2 / 2 : ℝ) : ℂ)) := by
  exact ⟨SL.Krein.polynomial_mem_domain,
    SL.Krein.operator_on_polynomial,
    SL.Krein.original_family_mem_domain,
    SL.Krein.operator_polynomial_energy⟩

theorem weighted_dd_root :
    (∀ (Length : ℝ) (LengthPos : 0 < Length) (Rho : SL.Weighted.Density Length) (Value : ℝ → ℂ) (Regular : ContinuousOn Value (Set.Icc 0 Length)), ‖SL.Weighted.weighted_vector Rho Value Regular‖ ^ 2 = SL.Weighted.mass Length Rho.value Value) ∧
    (∀ (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length) (RhoPos : 0 < Rho) (IndexPos : 0 < Index), 0 < SL.Weighted.ConstantDD.frequency Length Rho Index ∧ SL.Weighted.ConstantDD.eigenvalue Length Rho Index = SL.Weighted.ConstantDD.frequency Length Rho Index ^ 2 ∧ SL.Weighted.NormalizedEigenfunction SL.Weighted.Boundary.DD Length (fun _ => Rho) (SL.Weighted.ConstantDD.eigenvalue Length Rho Index) (SL.Weighted.ConstantDD.solution Length Rho Index RhoPos) ∧ ‖SL.Weighted.ConstantDD.eigenvector Length Rho Index RhoPos‖ ^ 2 = 1) := by
  exact ⟨SL.Weighted.weighted_norm_eq_mass,
    SL.Weighted.ConstantDD.constant_dd_l2_root⟩

end SLVerified
