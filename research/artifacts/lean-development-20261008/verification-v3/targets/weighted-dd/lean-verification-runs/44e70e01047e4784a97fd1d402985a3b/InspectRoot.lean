import LeanVerifyProbe
import SLVerified
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (∀ (Length : ℝ) (LengthPos : 0 < Length) (Rho : SL.Weighted.Density Length) (Value : ℝ → ℂ) (Regular : ContinuousOn Value (Set.Icc 0 Length)), ‖SL.Weighted.weighted_vector Rho Value Regular‖ ^ 2 = SL.Weighted.mass Length Rho.value Value) ∧
    (∀ (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length) (RhoPos : 0 < Rho) (IndexPos : 0 < Index), 0 < SL.Weighted.ConstantDD.frequency Length Rho Index ∧ SL.Weighted.ConstantDD.eigenvalue Length Rho Index = SL.Weighted.ConstantDD.frequency Length Rho Index ^ 2 ∧ SL.Weighted.NormalizedEigenfunction SL.Weighted.Boundary.DD Length (fun _ => Rho) (SL.Weighted.ConstantDD.eigenvalue Length Rho Index) (SL.Weighted.ConstantDD.solution Length Rho Index RhoPos) ∧ ‖SL.Weighted.ConstantDD.eigenvector Length Rho Index RhoPos‖ ^ 2 = 1)
#lean_verify_v2 SLVerified.weighted_dd_root expected LeanVerifyV2.expected_statement output "F:\\LaTeX\\BVE research\\research\\artifacts\\lean-development-20261008\\verification-v3\\targets\\weighted-dd\\lean-verification-runs\\44e70e01047e4784a97fd1d402985a3b\\declaration.json"
