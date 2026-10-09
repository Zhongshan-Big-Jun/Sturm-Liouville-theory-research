import LeanVerifyProbe
import SLVerified
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (∀ (R : SL.Krein.IntegralRepresentative) {x : ℝ}, x ∈ Set.Ioo (-1) 1 → HasDerivAt R.Value (R.First x) x) ∧
    (∀ (R : SL.Krein.IntegralRepresentative), ∀ᵐ x ∂SL.Krein.intervalMeasure, HasDerivAt R.First (R.Second x) x) ∧
    (∀ (R S : SL.Krein.IntegralRepresentative), R.to_L2 = S.to_L2 → R.Second =ᵐ[SL.Krein.intervalMeasure] S.Second) ∧
    (∀ (c : ℝ) (F G : SL.Krein.domain_submodule), SL.Krein.operator_linear c (F + G) = SL.Krein.operator_linear c F + SL.Krein.operator_linear c G) ∧
    (∀ (c : ℝ) (a : ℂ) (F : SL.Krein.domain_submodule), SL.Krein.operator_linear c (a • F) = a • SL.Krein.operator_linear c F) ∧
    (∀ (F : ℝ → ℂ) (HF : MeasureTheory.MemLp F 2 SL.Krein.intervalMeasure) (a b : ℂ), (SL.Krein.from_l2_second F HF a b).Value (-1) = b ∧ (SL.Krein.from_l2_second F HF a b).First (-1) = a ∧ (SL.Krein.from_l2_second F HF a b).Second = F) ∧
    (∀ (R : SL.Krein.IntegralRepresentative), Set.EqOn (SL.Krein.from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).Value R.Value (Set.Icc (-1) 1) ∧ Set.EqOn (SL.Krein.from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).First R.First (Set.Icc (-1) 1)) ∧
    (∀ (R : SL.Krein.IntegralRepresentative) (Q : ℂ →L[ℝ] ℝ) (Phi : ℝ → ℝ), ContDiff ℝ 1 Phi → Phi (-1) = 0 → Phi 1 = 0 → (∫ x in (-1 : ℝ)..1, Q (R.Value x) * deriv Phi x) = -(∫ x in (-1 : ℝ)..1, Q (R.First x) * Phi x) ∧ (∫ x in (-1 : ℝ)..1, Q (R.First x) * deriv Phi x) = -(∫ x in (-1 : ℝ)..1, Q (R.Second x) * Phi x))
#lean_verify_v2 SLVerified.krein_domain_root expected LeanVerifyV2.expected_statement output "F:\\LaTeX\\BVE research\\research\\artifacts\\lean-development-20261008\\verification\\targets\\krein-domain\\lean-verification-runs\\57676d2c426542679602fd08dbac0c95\\declaration.json"
